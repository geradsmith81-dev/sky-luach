"""The app's pages. Each render_* function draws one page."""
from __future__ import annotations

import html
import io
import os
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

import calendars as cv
import device
import fixed_calendar as fc
import observed_calendar as oc
import sky_engine as se
import sky_layer as sl
import theme
import hebrew_names as hn
import holiday_history as hh
from hebrew_names import bi, bt

HERE = os.path.dirname(os.path.abspath(__file__))
WEEK = hn.GRID_WEEK
MOON_ICON = {"New moon": "🌑", "First quarter": "🌓", "Full moon": "🌕", "Last quarter": "🌗"}


# ----------------------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------------------
def t12(dt) -> str:
    if dt is None:
        return "-"
    return dt.strftime("%I:%M %p").lstrip("0").lower()


def esc(s) -> str:
    return html.escape(str(s))


def sky_ok() -> bool:
    try:
        se.load()
        return True
    except Exception as exc:
        st.warning(f"Sunset times and the Moon need the JPL file de440s.bsp, which could not be loaded: {exc}. "
                   "The calendars still work.")
        return False


@st.cache_data(max_entries=48, show_spinner=False)
def zmanim(lat, lon, tz, start: date, end: date, candle: int) -> dict:
    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    return {r["date"]: r for r in se.zmanim_for_days(lat, lon, tz, days, candle_minutes=candle)}


@st.cache_data(max_entries=48, show_spinner=False)
def moon_days(start: date, end: date, tz: str) -> dict:
    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    return sl.moon_phase_days(days, tz)


@st.cache_data(max_entries=32, show_spinner=False)
def molad_info(month: int, year: int) -> dict:
    return sl.molad_vs_conjunction(month, year)


@st.cache_data(max_entries=16, show_spinner=False)
def seasons_info(gy: int) -> list:
    return sl.seasons_vs_tekufot(gy)


def others(view, ctx):
    return [v for v in (ctx["fixed"], ctx["observed"], ctx["pretemple"]) if v.kind != view.kind]


def other_view(view, ctx):
    return others(view, ctx)[0]


def heb_label(h, view=None) -> str:
    return f"{h.day} {h.month_name} {h.year}" if h else "outside the observed table"


def card(title: str, body: str) -> str:
    return f"<div class='sl-card'><h3>{esc(title)}</h3>{body}</div>"


# ----------------------------------------------------------------------------------------------
# Today
# ----------------------------------------------------------------------------------------------
def render_today(ctx):
    place, view = ctx["place"], ctx["view"]
    tz = ZoneInfo(place["tz"])
    now = datetime.now(tz)
    today = now.date()
    fixed, obs, pre = ctx["fixed"], ctx["observed"], ctx["pretemple"]
    have_sky = sky_ok()
    z = zmanim(place["lat"], place["lon"], place["tz"], today - timedelta(days=2), today + timedelta(days=8),
               ctx["candle"]) if have_sky else {}
    zt = z.get(today, {})
    after_sunset = bool(zt.get("sunset")) and now >= zt["sunset"]

    trio = [(v, v.hdate(today), v.hdate(today + timedelta(days=1))) for v in (fixed, obs, pre)]
    cols = st.columns(1 if device.phone() else 2)
    with cols[0]:
        wd = today.weekday()
        body = (f"<div class='sl-big'>{bi(hn.WEEKDAY_EN[wd], hn.WEEKDAY_HE[wd])}, {today:%d %B %Y}</div>"
                f"<div class='sl-muted'>{bi(place['label'], place.get('he', ''))} · local time {now:%H:%M}</div>")
        st.html(card("Today · היום", body))
        for v, h, n in trio:
            mark = " (shown in the calendar)" if v.kind == view.kind else ""
            title = f"{v.kind} · {cv.KIND_HE[v.kind]}{mark}"
            if h is None:
                st.html(card(title, "<span class='sl-muted'>Outside the range of this calendar.</span>"))
                continue
            line = (f"<div class='sl-big'>{h.day} {esc(h.month_name)} {h.year}</div>"
                    f"<div class='sl-he'>{esc(h.hebrew())}</div>")
            if v.kind != cv.FIXED:
                b = hn.BIBLICAL_MONTH[h.month]
                line += f"<div class='sl-bib'>{bi(b[0], b[1])}{' · ' + bi(b[2], b[3]) if b[2] else ''}</div>"
            if n is not None:
                when = "began at sunset" if after_sunset else "begins at sunset"
                st_txt = f" ({t12(zt.get('sunset'))})" if zt.get("sunset") else ""
                line += (f"<div class='sl-muted'>{n.day} {esc(n.month_name)} {when} this evening{st_txt}.</div>")
            st.html(card(title, line))
    with cols[-1]:
        if have_sky and zt:
            rows = [(bi("Dawn", "עלות השחר") + " (Sun 16.1° below)", zt.get("dawn")),
                    (bi("Sunrise", "הנץ החמה"), zt.get("sunrise")),
                    (bi("Midday", "חצות היום"), zt.get("midday")),
                    (bi("Sunset", "שקיעה") + " — the new Hebrew day begins", zt.get("sunset")),
                    (bi("Nightfall", "צאת הכוכבים") + " (3 stars, Sun 8.5° below)", zt.get("nightfall"))]
            body = "<table class='sl-table'>" + "".join(
                f"<tr><td>{a}</td><td><b>{t12(b)}</b></td></tr>" for a, b in rows) + "</table>"
            if zt.get("shaah_zmanit_min"):
                body += f"<div class='sl-muted'>Seasonal hour ({bt('sha' + chr(39) + 'ah zmanit')}): {zt['shaah_zmanit_min']:.1f} min.</div>"
            st.html(card("Today's times · זמני היום", body))
            # this week's Shabbat
            if today.weekday() == 5:          # it is Shabbat now
                sat = today
            else:
                sat = today + timedelta(days=(5 - today.weekday()) % 7)
            fri = sat - timedelta(days=1)
            zf, zs = z.get(fri, {}), z.get(sat, {})
            parsha = fixed.parsha(sat)
            body = (f"<div>{bt('candle lighting').capitalize()} Friday {fri:%d %b}: <b>{t12(zf.get('candle_lighting'))}</b> "
                    f"<span class='sl-muted'>({ctx['candle']} min before sunset {t12(zf.get('sunset'))})</span></div>"
                    f"<div>{bt('Shabbat')} ends ({bt('Havdalah')}) {sat:%d %b}: <b>{t12(zs.get('nightfall'))}</b></div>")
            if parsha and parsha[0]:
                body += (f"<div>{bt('Torah portion')}: <b>{bi(parsha[0], parsha[1])}</b> "
                         f"<span class='sl-muted'>({'Israel' if fixed.israel else 'diaspora'} reading)</span></div>")
            elif parsha is not None:
                body += "<div>A festival Shabbat: festival reading instead of the weekly portion.</div>"
            st.html(card("This Shabbat · שבת", body))
    # Moon
    if have_sky:
        md = moon_days(today, today, place["tz"])[today]
        conj = se.new_moons(today - timedelta(days=31), today + timedelta(days=31))
        nowu = now.astimezone(timezone.utc)
        past = [c for c in conj if c <= nowu]
        fut = [c for c in conj if c > nowu]
        body = f"<div>Moon {md['illum'] * 100:.0f}% lit this evening"
        if past:
            age = (nowu - past[-1]).total_seconds() / 86400
            body += f", {age:.1f} days since the true new moon ({past[-1].astimezone(tz):%d %b %H:%M})"
        body += ".</div>"
        if fut:
            body += f"<div>Next new moon: <b>{fut[0].astimezone(tz):%a %d %b %Y, %H:%M}</b> (your time).</div>"
            info = None
            for k in range(0, 4):
                info = oc.evening_info(fut[0].date() + timedelta(days=k)) if fut[0].date() + timedelta(days=k) <= date(2150, 1, 1) else None
                if info and info.get("yallop") in ("A", "B"):
                    body += (f"<div class='sl-obs'>First crescent predicted from Jerusalem on the evening of "
                             f"{fut[0].date() + timedelta(days=k):%a %d %b} (Yallop {info['yallop']}: "
                             f"{esc(se.YALLOP_TEXT[info['yallop']])}).</div>")
                    break
        st.html(card("The Moon · הירח", body))
    # upcoming holidays
    hol = [h for h in view.holidays_between(today, today + timedelta(days=75), rosh_chodesh=True)
           if h.kind not in ("omer",)]
    if hol:
        other = other_view(view, ctx)
        rows = []
        for h in hol[:12]:
            rows.append(f"<tr><td>{h.date:%a %d %b}</td><td>{hh.clickable(h.name, theme.chip(h.kind, h.name, h.hebrew))}</td>"
                        f"<td class='sl-muted'>{esc(h.hdate) if h.hdate else ''}<br>"
                        f"<span class='sl-he-i'>{esc(h.hdate.hebrew()) if h.hdate else ''}</span></td></tr>")
        st.html(card(f"Coming up · בקרוב — {view.kind}", "<table class='sl-table'>" + "".join(rows) + "</table>"))


# ----------------------------------------------------------------------------------------------
# Month
# ----------------------------------------------------------------------------------------------
def _move(days: int):
    st.session_state["anchor"] = st.session_state["anchor"] + timedelta(days=days)


def render_month(ctx):
    view, place = ctx["view"], ctx["place"]
    tz = ZoneInfo(place["tz"])
    today = datetime.now(tz).date()
    if "anchor" not in st.session_state:
        st.session_state["anchor"] = today
    anchor = st.session_state["anchor"]
    if not view.covers(anchor):
        anchor = min(max(anchor, view.first_day), view.last_day)
        st.session_state["anchor"] = anchor
    m = view.month_at(anchor)

    c1, c2, c3, c4 = st.columns([1, 1, 1, 1.4])
    if c1.button("◀ Previous", key="prev_m", width="stretch"):
        st.session_state["anchor"] = m.start - timedelta(days=1)
        st.rerun()
    if c2.button("This month", key="today_m", width="stretch"):
        st.session_state["anchor"] = today
        st.rerun()
    if c3.button("Next ▶", key="next_m", width="stretch"):
        st.session_state["anchor"] = m.end + timedelta(days=1)
        st.rerun()
    picked = c4.date_input("Go to a date", value=anchor, min_value=view.first_day, max_value=view.last_day,
                           key=f"goto_{anchor.isoformat()}", label_visibility="collapsed", format="DD/MM/YYYY")
    if picked != anchor:
        st.session_state["anchor"] = picked
        st.rerun()

    other_list = others(view, ctx)
    leap = " · leap year (13 months)" if m.leap_year else ""
    bib = ""
    if view.kind != cv.FIXED:
        b = hn.BIBLICAL_MONTH[m.month]
        bib = (f"<div class='sl-bib'>First Temple usage: {bi(b[0], b[1])}"
               f"{' · ' + bi(b[2], b[3]) + ' (' + b[4] + ')' if b[2] else ''}</div>")
    st.html(f"<div class='sl-big'>{esc(m.name)} {m.year} <span class='sl-he'>{esc(m.name_he)} "
            f"{esc(fc.hebrew_numeral(m.year % 1000))}</span></div>{bib}"
            f"<div class='sl-muted'>{bi(view.kind, cv.KIND_HE[view.kind])} · {m.start:%d %b %Y} – {m.end:%d %b %Y} · {m.length} days{leap}</div>")

    days = [m.start + timedelta(days=i) for i in range(m.length)]
    have_sky = sky_ok()
    z = zmanim(place["lat"], place["lon"], place["tz"], m.start, m.end, ctx["candle"]) if have_sky else {}
    moon = moon_days(m.start, m.end, place["tz"]) if have_sky else {}
    hol = {}
    for h in view.holidays_between(m.start, m.end):
        hol.setdefault(h.date, []).append(h)

    def cell_lines(d):
        out = []
        hd_view = view.hdate(d)
        for other in other_list:
            oh = other.hdate(d)
            if oh is not None:
                differ = (oh.day, oh.month) != (hd_view.day, hd_view.month)
                out.append(f"<span class='sl-other'>{'≠ ' if differ else ''}{other.short}: {oh.day} {esc(oh.month_name)}</span>")
        for h in hol.get(d, []):
            out.append(hh.clickable(h.name, theme.chip(h.kind, h.name, h.hebrew),
                                    align_right=(d.weekday() in (3, 4, 5) and not device.phone())))
        if d.weekday() == 4 and z.get(d):
            out.append(f"<span class='sl-line'>Candles <b>{t12(z[d]['candle_lighting'])}</b></span>")
        if d.weekday() == 5:
            if z.get(d):
                out.append(f"<span class='sl-line'>Ends <b>{t12(z[d]['nightfall'])}</b></span>")
            p = view.parsha(d)
            if p and p[0]:
                out.append(f"<span class='sl-line'><b>{bi(p[0], p[1])}</b></span>")
        mi = moon.get(d)
        if mi and mi["event"]:
            out.append(f"<span class='sl-line'>{MOON_ICON[mi['event']]} {esc(mi['event'])} {mi['event_time']:%H:%M}</span>")
        return "".join(out)

    if device.phone():
        rows = []
        for d in days:
            h = view.hdate(d)
            cls = " sl-sat" if d.weekday() == 5 else ""
            cls += " sl-today" if d == today else ""
            rows.append(f"<tr><td class='{cls}' style='width:34%'><span class='sl-civ'>{h.day}</span> "
                        f"<span class='sl-he'>{esc(fc.hebrew_numeral(h.day))}</span><br>"
                        f"<span class='sl-muted'>{WEEK[(d.weekday() + 1) % 7][0]} {d:%d %b}</span></td>"
                        f"<td class='{cls}'>{cell_lines(d)}</td></tr>")
        st.html("<table class='sl-list'>" + "".join(rows) + "</table>")
    else:
        lead = (m.start.weekday() + 1) % 7   # Sunday first
        cells = ["<td class='sl-empty'></td>"] * lead
        for d in days:
            h = view.hdate(d)
            cls = []
            if d.weekday() == 5:
                cls.append("sl-sat")
            if d == today:
                cls.append("sl-today")
            civm = f"<span class='sl-civm'>{d:%b}</span>" if (d.day == 1 or d == m.start) else ""
            cells.append(f"<td class='{' '.join(cls)}'><span class='sl-civ'>{d.day}</span>{civm}"
                         f"<span class='sl-hd'>{esc(fc.hebrew_numeral(h.day))} <small>{h.day}</small></span>"
                         f"{cell_lines(d)}</td>")
        while len(cells) % 7:
            cells.append("<td class='sl-empty'></td>")
        rows = "".join("<tr>" + "".join(cells[i:i + 7]) + "</tr>" for i in range(0, len(cells), 7))
        st.html("<table class='sl-grid'><tr>" + "".join(f"<th>{w} <span class='sl-he-i'>{he}</span></th>" for w, he in WEEK)
                + "</tr>" + rows + "</table>")
    st.html(theme.legend() + "<div class='sl-muted' style='margin-top:.3rem'>Click a holiday's name for a short history "
            "of the day.</div>")

    # how the month began
    if view.kind == cv.FIXED:
        if have_sky:
            mi = molad_info(m.month, m.year)
            mt = mi["molad_traditional"]
            molad_local = mi["molad_utc"] + sl.JERUSALEM_MEAN_OFFSET
            diff = mi["molad_minus_true_h"]
            body = (f"<div>{bt('molad').capitalize()} (mean new moon) of {bi(m.name, m.name_he)}: <b>{molad_local:%A %d %b %Y}, "
                    f"{molad_local:%H:%M} and {mt['rem_parts']} parts</b> Jerusalem mean time "
                    f"<span class='sl-muted'>(traditional count: {mt['hours_from_6pm']} h {mt['parts']} parts after 6 pm)</span></div>"
                    f"<div>True new moon (JPL DE440s): <b>{mi['conjunction_utc'].astimezone(tz):%A %d %b %Y, %H:%M}</b> your time</div>"
                    f"<div class='sl-muted'>The molad is {abs(diff):.1f} hours {'after' if diff > 0 else 'before'} the true conjunction. "
                    "The fixed calendar uses the molad, never the observed Moon.</div>")
            st.html(card("How this month began · מולד החודש", body))
    elif view.kind == cv.PRETEMPLE:
        body = f"<div>{esc(m.note)}.</div>"
        mo = view.cal.get_month(m.year, m.month)
        if mo is not None and mo.conj_utc is not None:
            body += f"<div>In your time zone: <b>{mo.conj_utc.astimezone(tz):%A %d %b %Y, %H:%M}</b>.</div>"
        fstart = fc.to_gregorian(m.year, m.month, 1) if (m.month != fc.ADAR_II or fc.is_leap(m.year)) else None
        ostart = ctx["observed"].cal.get_month(m.year, m.month)
        cmp_rows = []
        if fstart:
            dd = (m.start - fstart).days
            cmp_rows.append(f"<tr><td>{bi('Fixed (rabbinic)', cv.KIND_HE[cv.FIXED])}</td><td>{fstart:%a %d %b %Y}</td><td>{'same day' if dd == 0 else f'{-dd:+d} days'}</td></tr>")
        if ostart:
            dd = (m.start - ostart.start).days
            cmp_rows.append(f"<tr><td>{bi('Observed (sighting)', cv.KIND_HE[cv.OBSERVED])}</td><td>{ostart.start:%a %d %b %Y}</td><td>{'same day' if dd == 0 else f'{-dd:+d} days'}</td></tr>")
        if cmp_rows:
            body += ("<table class='sl-table'><tr><th>Same month in</th><th>Day 1</th><th>Days after the Pre-Temple start</th></tr>"
                     + "".join(cmp_rows) + "</table>")
        body += ("<div class='sl-muted'>The month starts at the real conjunction, when the Moon is still invisible. "
                 "There is no molad, no sighting and no postponement.</div>")
        st.html(card("How this month began · המולד האמיתי", body))
    else:
        body = f"<div>{esc(m.note)}.</div>"
        evs = [m.start - timedelta(days=k) for k in (3, 2, 1, 0)]
        rows = []
        for e in evs:
            info = oc.evening_info(e)
            if info is None:
                continue
            if pd.isna(info["q"]):
                verdict = "Moon sets before the Sun or before conjunction"
                qtxt = "-"
            else:
                verdict = se.YALLOP_TEXT[info["yallop"]]
                qtxt = f"{info['q']:+.3f} ({info['yallop']})"
            rows.append(f"<tr><td>{e:%a %d %b}</td><td>{qtxt}</td><td>{info['lag_min']:.0f}</td>"
                        f"<td>{info['age_h']:.1f}</td><td>{info['arcl']:.1f}°</td><td>{esc(verdict)}</td></tr>")
        if rows:
            body += ("<table class='sl-table'><tr><th>Evening (Jerusalem)</th><th>Yallop q</th><th>Moonset lag (min)</th>"
                     "<th>Moon age (h)</th><th>Elongation</th><th>Verdict</th></tr>" + "".join(rows) + "</table>")
        crit = oc.CRITERIA[ctx["crit"]]
        body += f"<div class='sl-muted'>Rule in use: {esc(crit)}. Seen from {bt('Jerusalem')}.</div>"
        st.html(card("How this month began · קידוש החודש", body))


# ----------------------------------------------------------------------------------------------
# Year
# ----------------------------------------------------------------------------------------------
def year_picker(view, ctx, key: str) -> int:
    tz = ZoneInfo(ctx["place"]["tz"])
    today = datetime.now(tz).date()
    years = view.years()
    cur = view.year_of(today) or years[len(years) // 2]
    cur = min(max(cur, years[0]), years[-1])
    return st.selectbox("Hebrew year (AM)", years, index=years.index(cur), key=key,
                        format_func=lambda y: f"{y} ({y - 3761}–{y - 3760})")


def render_year(ctx):
    view, place = ctx["view"], ctx["place"]
    y = year_picker(view, ctx, "year_y")
    kinds = st.multiselect("Show", list(theme.KIND_LABEL), default=[k for k in theme.KIND_LABEL if k not in ("omer", "erev")],
                           format_func=lambda k: theme.KIND_LABEL[k], key="year_kinds")
    hol = [h for h in view.holidays_for_year(y) if h.kind in kinds]
    if not hol:
        st.info("Nothing to show for this year with these choices.")
        return
    have_sky = sky_ok()
    z = {}
    if have_sky:
        z = zmanim(place["lat"], place["lon"], place["tz"], hol[0].date - timedelta(days=1), hol[-1].date, ctx["candle"])
    rows, recs = [], []
    for h in hol:
        prev = z.get(h.date - timedelta(days=1), {})
        starts = t12(prev.get("sunset")) if (h.begins_evening_before and h.kind not in ("erev", "fast", "omer")) else ""
        if h.kind == "fast" and h.name != "Tisha B'Av":
            zz = z.get(h.date, {})
            starts = f"dawn {t12(zz.get('dawn'))}" if zz else ""
        rows.append(f"<tr><td>{h.date:%a %d %b %Y}</td><td>{hh.clickable(h.name, theme.chip(h.kind, h.name, h.hebrew))}"
                    f"{'<br><span class=sl-muted>' + esc(h.note) + '</span>' if h.note else ''}</td>"
                    f"<td>{esc(h.hdate) if h.hdate else ''}<br><span class='sl-he-i'>{esc(h.hdate.hebrew()) if h.hdate else ''}</span></td>"
                    f"<td>{esc(starts)}</td></tr>")
        recs.append({"date": h.date.isoformat(), "weekday": h.date.strftime("%A"), "holiday": h.name,
                     "hebrew_name": h.hebrew, "hebrew_date": str(h.hdate) if h.hdate else "",
                     "kind": theme.KIND_LABEL.get(h.kind, h.kind), "begins": starts, "note": h.note,
                     "calendar": view.kind})
    lm = "leap year, 13 months" if view.is_leap(y) else "12 months"
    extra = ""
    if view.kind == cv.FIXED:
        t = fc.year_type(y)
        extra = f" · {t['days']} days ({t['kind']}) · Rosh Hashanah on {t['rosh_hashanah_weekday']}"
    st.html(f"<div class='sl-big'>{y} <span class='sl-he'>{esc(fc.hebrew_numeral(y % 1000))}</span> — {bi(view.kind, cv.KIND_HE[view.kind])}</div><div class='sl-muted'>{lm}{extra}"
            f"{' · Israel scheme' if view.israel else ' · diaspora scheme (second festival days)'}</div>")
    st.html("<table class='sl-table'><tr><th>Date</th><th>Holiday</th><th>Hebrew date</th><th>Begins</th></tr>"
            + "".join(rows) + "</table>")
    df = pd.DataFrame(recs)
    c1, c2 = st.columns(2)
    c1.download_button("Download for your calendar app (.ics)", cv.to_ics(hol, f"{view.kind} {y}"),
                       file_name=f"sky_luach_{view.short.lower()}_{y}.ics", mime="text/calendar", width="stretch")
    c2.download_button("Download as a spreadsheet (.csv)", df.to_csv(index=False).encode("utf-8-sig"),
                       file_name=f"sky_luach_{view.short.lower()}_{y}.csv", mime="text/csv", width="stretch")
    st.caption("Click a holiday's name for a short history. Times in 'Begins' are sunset on the evening before at your "
               "place (fasts other than Tisha B'Av begin at dawn).")


# ----------------------------------------------------------------------------------------------
# Compare
# ----------------------------------------------------------------------------------------------
@st.cache_data(max_entries=8, show_spinner=False)
def pesach_series(kind, a, b, c):
    """Pesach (15 Nisan) of a calendar minus the fixed date, per year. kind 'obs' or 'pre'."""
    import pretemple_calendar as ptc
    o = oc.ObservedCalendar(a, b, c) if kind == "obs" else ptc.PreTempleCalendar(a, b, c)
    xs, ys = [], []
    for y in o.years():
        f = fc.to_gregorian(y, fc.NISAN, 15)
        ob = o.to_gregorian(y, fc.NISAN, 15)
        if ob:
            xs.append(f.year)
            ys.append((ob - f).days)
    return xs, ys


def render_compare(ctx):
    fixed, obs, pre = ctx["fixed"], ctx["observed"], ctx["pretemple"]
    st.html("<div class='sl-muted'>All three calendars side by side. The fixed calendar is shown with the Israel holiday "
            "scheme, so every calendar has one-day festivals. Differences are in days relative to the fixed calendar.</div>")
    common = [y for y in obs.years() if y in set(pre.years())]
    tz = ZoneInfo(ctx["place"]["tz"])
    cur = obs.year_of(datetime.now(tz).date()) or common[len(common) // 2]
    cur = min(max(cur, common[0]), common[-1])
    y = st.selectbox("Hebrew year (AM)", common, index=common.index(cur), key="cmp_y",
                     format_func=lambda y: f"{y} ({y - 3761}–{y - 3760})")
    cals = [("Observed", obs.cal), ("Pre-Temple", pre.cal)]

    def dfmt(d):
        return d.strftime("%a %d %b %Y") if d else "—"

    def dcell(d, ref):
        if d is None or ref is None:
            return "<td>—</td>"
        n = (d - ref).days
        txt = dfmt(d) + (f" <b>({n:+d})</b>" if n else "")
        return f"<td class='sl-diff'>{txt}</td>" if n else f"<td>{txt}</td>"

    def hol_date(cal, name, m, d):
        if name == "Shavuot":
            o16 = cal.to_gregorian(y, fc.NISAN, 16)
            return o16 + timedelta(days=49) if o16 else None
        mm = m if m is not None else (fc.ADAR_II if cal.is_leap(y) else fc.ADAR)
        return cal.to_gregorian(y, mm, d)

    head = ("<tr><th></th><th>" + bi("Fixed", cv.KIND_HE[cv.FIXED]) + "</th><th>" + bi("Observed", cv.KIND_HE[cv.OBSERVED])
            + "</th><th>" + bi("Pre-Temple", cv.KIND_HE[cv.PRETEMPLE]) + "</th></tr>")
    rows = []
    for name, m, d in oc.COMPARE_HOLIDAYS:
        mf = m if m is not None else (fc.ADAR_II if fc.is_leap(y) else fc.ADAR)
        f = fc.to_gregorian(y, mf, d)
        he = {"Rosh Hashanah": "ראש השנה", "Yom Kippur": "יום כיפור", "Sukkot I": "סוכות", "Chanukah (day 1)": "חנוכה",
              "Asara B'Tevet": "עשרה בטבת", "Tu BiShvat": "ט״ו בשבט", "Purim": "פורים", "Pesach I": "פסח",
              "Shavuot": "שבועות", "17 Tammuz": "שבעה עשר בתמוז", "Tisha B'Av (date)": "תשעה באב"}.get(name, "")
        rows.append(f"<tr><td>{hh.clickable(name, theme.chip('major', name, he))}</td><td>{dfmt(f)}</td>" +
                    "".join(dcell(hol_date(c, name, m, d), f) for _, c in cals) + "</tr>")
    st.html("<h4 style='margin:0'>Holidays · מועדים</h4><table class='sl-table'>" + head + "".join(rows) + "</table>")

    mrows = []
    for mth in fc.year_months(y) + ([fc.ADAR_II] if not fc.is_leap(y) and any(c.is_leap(y) for _, c in cals) else []):
        f = fc.to_gregorian(y, mth, 1) if (mth != fc.ADAR_II or fc.is_leap(y)) else None
        label = fc.month_name(mth, y) if f else "Adar II (not in the fixed calendar this year)"
        cells = ""
        for _, c in cals:
            om = c.get_month(y, mth)
            cells += dcell(om.start, f) if (om and f) else f"<td>{dfmt(om.start) if om else '—'}</td>"
        mrows.append(f"<tr><td>{bi(label, fc.month_name(mth, y, True) if f else 'אדר ב׳')}</td><td>{dfmt(f)}</td>{cells}</tr>")
    st.html("<h4 style='margin:.6rem 0 0 0'>First day of each month · ראשי חודשים</h4><table class='sl-table'>" + head
            + "".join(mrows) + "</table>")

    why = []
    lf = fc.is_leap(y)
    for nm, c in cals:
        if c.is_leap(y) != lf:
            why.append(f"{nm}: the leap month falls in a different year from the fixed calendar "
                       f"({'adds' if c.is_leap(y) else 'has no'} Adar II in {y}, the fixed calendar "
                       f"{'adds' if lf else 'does not'}), so the spring and summer holidays are about a month apart. "
                       "The fixed calendar's 19-year cycle uses a year about 6.6 minutes longer than the true solar "
                       "year, so its Pesach has drifted later against the equinox since the 4th century.")
    why.append("Observed months start 1–2 days after the true new moon, because the crescent can only be seen once "
               "the Moon has moved far enough from the Sun.")
    why.append("Pre-Temple Period months start at the true new moon. The fixed calendar starts from the molad, which is "
               "a mean new moon up to about 14 hours from the true one, and then applies the postponement rules "
               "(no Rosh Hashanah on Sunday, Wednesday or Friday, among others). So the two agree on the day about half "
               "the time and otherwise differ by 1–2 days.")
    st.html(card("Why they differ", "".join(f"<p>{esc(w)}</p>" for w in why)))

    fig, ax = plt.subplots(figsize=(9, 3.2) if not device.phone() else (5, 3.4), dpi=120)
    fig.patch.set_facecolor(theme.BG)
    ax.set_facecolor(theme.CARD)
    xo, yo = pesach_series("obs", ctx["crit"], ctx["eq"], ctx["nisan_day"])
    xp, yp = pesach_series("pre", ctx["pt_rule"], ctx["eq"], ctx["nisan_day"])
    ax.scatter(xo, yo, s=12, c=theme.OBS, label="Observed (sighting)", marker="o")
    ax.scatter(xp, [v + 0.0 for v in yp], s=10, c=theme.GOLD, label="Pre-Temple Period", marker="^")
    ax.axhline(0, color=theme.MUTED, lw=0.8)
    ax.set_xlabel("Year (CE)", color=theme.TEXT)
    ax.set_ylabel("Minus fixed date (days)", color=theme.TEXT)
    ax.set_title("First day of Pesach compared with the fixed calendar, 1850–2149", color=theme.TEXT, fontsize=11)
    ax.tick_params(colors=theme.TEXT)
    for sp in ax.spines.values():
        sp.set_color(theme.MUTED)
    leg = ax.legend(facecolor=theme.CARD, edgecolor=theme.MUTED, labelcolor=theme.TEXT, fontsize=8)
    fig.tight_layout()
    st.pyplot(fig, width="stretch")
    plt.close(fig)
    no = sum(1 for v in yo if abs(v) > 20)
    npre = sum(1 for v in yp if abs(v) > 20)
    st.caption(f"A month apart from the fixed Pesach (פסח): observed in {no} of {len(yo)} years, Pre-Temple Period in "
               f"{npre} of {len(yp)} years. Otherwise they are within a few days of the fixed date.")

    with st.expander("Sighting log for this year (observed calendar)"):
        rows = []
        o = obs.cal
        for mo in o.year_months(y):
            conj = mo.conj_utc.strftime("%d %b %Y %H:%M UT") if mo.conj_utc is not None else "—"
            rows.append({"month": o.month_label(mo.year, mo.month), "day 1": mo.start.isoformat(),
                         "days": mo.length, "true new moon": conj,
                         "sighting evening": mo.sighting_evening.isoformat() if mo.sighting_evening else "not seen (30th day)",
                         "Yallop q": None if mo.q is None else round(mo.q, 3), "zone": mo.yallop, "how": mo.reason})
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")


# ----------------------------------------------------------------------------------------------
# Cycles
# ----------------------------------------------------------------------------------------------
def render_cycles(ctx):
    fixed = ctx["fixed"]
    y = year_picker(fixed, ctx, "cyc_y")
    mp = fc.metonic_position(y)
    t = fc.year_type(y)
    sh = fc.shmita_position(y)
    sc = fc.solar_cycle_position(y)
    bh = [d for d in fc.birkat_hachamah_years(1850, 2149) if d.year >= y - 3761]
    cyc_html = "".join(
        f"<span class='sl-cycle {'leap' if k in mp['leap_years_in_cycle'] else 'common'}{' now' if k == mp['year_in_cycle'] else ''}'>{k}</span>"
        for k in range(1, 20))
    body = (f"<div>Year {y} is year <b>{mp['year_in_cycle']}</b> of 19 in small cycle ({bt('machzor katan')}) no. {mp['cycle']}. "
            f"Gold = leap years (3, 6, 8, 11, 14, 17, 19).</div><div style='margin:.4rem 0'>{cyc_html}</div>"
            f"<div>Year type (keviah): <b>{t['days']} days, {t['kind']}</b>, Rosh Hashanah on {t['rosh_hashanah_weekday']}, "
            f"Pesach on {t['pesach_weekday']}.</div>")
    st.html(card("The 19-year cycle · מחזור קטן", body))
    nxt = sh["next_shmita"]
    shm = (" — this is a shmita year" if sh["is_shmita"]
           else f"; next {bt('shmita')} year {nxt} ({nxt - 3761}–{nxt - 3760})")
    body = (f"<div>Sabbatical cycle: year <b>{sh['year_in_cycle']}</b> of 7{shm}.</div>"
            f"<div>Great solar cycle ({bt('machzor gadol')}): year <b>{sc['year_in_cycle']}</b> of 28 in cycle no. {sc['machzor_gadol']}.</div>")
    if bh:
        body += f"<div>Next {bt('Birkat HaChamah')} (blessing of the Sun): <b>{bh[0]:%A %d %B %Y}</b>.</div>"
    st.html(card("Sabbatical and solar cycles · שמיטה ומחזור גדול", body))

    if not sky_ok():
        return
    rows = []
    for m in fc.year_months(y):
        mi = molad_info(m, y)
        loc = mi["molad_utc"] + sl.JERUSALEM_MEAN_OFFSET
        rows.append({"month": fc.month_name(m, y), "חודש": fc.month_name(m, y, True), "molad (Jerusalem mean time)": loc.strftime("%a %d %b %Y %H:%M"),
                     "true new moon (UT)": mi["conjunction_utc"].strftime("%a %d %b %Y %H:%M"),
                     "molad − true (h)": round(mi["molad_minus_true_h"], 1)})
    df = pd.DataFrame(rows)
    st.html(card("Molad versus the true new moon · מולד ומולד אמיתי",
                 "<div class='sl-muted'>The molad advances by a fixed 29 d 12 h 793 parts. The real Moon speeds up and slows "
                 "down along its elliptical orbit, so the true conjunction (from JPL DE440s) can come up to about 14 hours "
                 "before or after the molad.</div>"))
    st.dataframe(df, hide_index=True, width="stretch")
    gy = y - 3760
    srows = []
    for r in seasons_info(gy):
        srows.append({"season": r["season"], "עונה": hn.SEASON_HE[r["season"]], "tekufah": r["tekufah"],
                      "תקופה": hn.TERMS[r["tekufah"]],
                      "true (UT)": r["true_utc"].strftime("%d %b %Y %H:%M"),
                      "Shmuel (UT)": r["shmuel_utc"].strftime("%d %b %Y %H:%M"),
                      "Shmuel − true (days)": round(r["shmuel_minus_true_d"], 2),
                      "Rav Adda (UT)": r["adda_utc"].strftime("%d %b %Y %H:%M"),
                      "Rav Adda − true (days)": round(r["adda_minus_true_d"], 2)})
    st.html(card(f"Tekufot versus the true equinoxes and solstices of {gy} · תקופות",
                 f"<div class='sl-muted'>The tekufah of {bt('Shmuel')} uses a year of exactly 365¼ days. It is used for the prayer "
                 "for rain (outside Israel) and for Birkat HaChamah, and it now runs about two weeks late. The tekufah of "
                 f"{bt('Rav Adda')} matches the fixed calendar's 19-year cycle and runs about a week late.</div>"))
    st.dataframe(pd.DataFrame(srows), hide_index=True, width="stretch")


# ----------------------------------------------------------------------------------------------
# How it works
# ----------------------------------------------------------------------------------------------
def render_about(ctx):
    path = os.path.join(HERE, "HOW_IT_WORKS.md")
    with open(path, encoding="utf-8") as f:
        st.markdown(f.read())
    st.markdown("### Holiday guide · מדריך המועדים")
    st.caption("The same short histories open when you click a holiday's name anywhere in the app.")
    for key, (title, he, text, src) in hh.H.items():
        with st.expander(f"{title} · {he}"):
            st.markdown(text)
            st.caption(f"Sources: {src}")
    try:
        lo, hi = se.ephemeris_range()
        _, _, name = se.load()
        st.caption(f"Ephemeris in use: {name}, valid {lo:%d %b %Y} – {hi:%d %b %Y}.")
    except Exception:
        st.caption("Ephemeris not loaded.")
