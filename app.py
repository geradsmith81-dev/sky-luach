"""Sky Luach · לוח השמים — the Jewish calendars (fixed, observed, Early Temple, Karaite, Samaritan) from NASA JPL astronomy.

Run:  streamlit run app.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import streamlit as st  # noqa: E402

st.set_page_config(page_title="Sky Luach · לוח השמים", page_icon=os.path.join(HERE, "assets", "luach_icon.png"),
                   layout="wide", initial_sidebar_state="auto")

import desktop as dk  # noqa: E402  (desktop-only controls; inert on the hosted copy)

dk.require_password(st)

import calendars as cv  # noqa: E402
import device  # noqa: E402
import hebrew_names as hn  # noqa: E402
import observed_calendar as oc  # noqa: E402
import pretemple_calendar as ptc  # noqa: E402
import samaritan_calendar as smc  # noqa: E402
import readings as rdg  # noqa: E402
import pages  # noqa: E402
import locator  # noqa: E402
import places  # noqa: E402
import theme  # noqa: E402

theme.apply()
theme.header()

PAGES = {
    "Today": ("Today · היום", pages.render_today),
    "Month": ("Month · חודש", pages.render_month),
    "Year": ("Year & holidays · שנה ומועדים", pages.render_year),
    "Compare": ("Compare · השוואה", pages.render_compare),
    "Cycles": ("Cycles · מחזורים", pages.render_cycles),
    "Traditions": ("Traditions · זרמים", pages.render_traditions),
    "About": ("How it works · הסבר", pages.render_about),
}


@st.cache_resource(show_spinner="Building the observed calendar from the Jerusalem crescent table…", max_entries=12)
def observed_view(crit, eq, nd, omer, hillula=True):
    return cv.ObservedView(crit, eq, nd, omer, hillula)


@st.cache_resource(show_spinner="Building the Early Temple Period calendar from the true new moons…", max_entries=12)
def pretemple_view(rule, eq, nd, omer, hillula=True):
    return cv.PreTempleView(rule, eq, nd, omer, hillula)


@st.cache_resource(show_spinner="Building the Karaite calendar from the Jerusalem crescent table…", max_entries=12)
def karaite_view(crit, eq, nd, omer):
    return cv.KaraiteView(crit, eq, nd, omer)


@st.cache_resource(show_spinner="Building the Samaritan calendar from the true new moons at Mount Gerizim…", max_entries=8)
def samaritan_view(rule, floor):
    return cv.SamaritanView(rule, floor)


# ---------------------------------------------------------------- where the user is
def _browser_tz():
    try:
        return st.context.timezone
    except Exception:
        return None


if "place" not in st.session_state:
    guess = locator.place_from_timezone(_browser_tz())
    if guess is None:
        guess = dict(places.PRESETS[0], label="Jerusalem, Israel", src="default")
    st.session_state["place"] = guess
    st.session_state["place_src"] = guess["src"]


def _on_pick():
    v = st.session_state.get("locator")
    p = v.get("pick") if hasattr(v, "get") else getattr(v, "pick", None)
    if not isinstance(p, dict) or "lat" not in p:
        return
    try:
        lat, lon = float(p["lat"]), float(p["lon"])
    except (TypeError, ValueError):
        return
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return
    if p.get("auto") and st.session_state.get("place_src") == "manual":
        return   # the user already chose a place by hand: keep it
    acc = p.get("acc") if isinstance(p.get("acc"), (int, float)) else None
    st.session_state["place"] = locator.place_from_device(lat, lon, acc, _browser_tz())
    st.session_state["place_src"] = "gps"


def _set_manual(pl: dict):
    st.session_state["place"] = dict(pl, src="manual")
    st.session_state["place_src"] = "manual"


# ---------------------------------------------------------------- top switches
c1, c2 = st.columns([1.6, 2.0]) if not device.phone() else (st.container(), st.container())
with c1:
    cal = st.radio("Calendar · לוח", cv.ALL, key="cal", horizontal=True,
                   format_func=lambda k: f"{k} · {cv.KIND_HE[k]}",
                   help="Fixed: the rabbinic calendar of Hillel II, used by Jewish communities today. "
                        "Observed: months begin when the young crescent is (predicted) visible from Jerusalem, "
                        "and the leap month follows the spring equinox, as in the Second Temple period. "
                        "Early Temple Period: months begin at the true astronomical new moon (an astronomical "
                        "ideal, counted from year 1). Karaite: sighted crescent from the Land of Israel, the barley "
                        "(aviv) year, biblical festivals only. Samaritan: the priests' calculated calendar, months from "
                        "the true new moon at Mount Gerizim. See the Traditions page for who uses which.")
with c2:
    page = st.radio("Page", list(PAGES), key="page", horizontal=True, format_func=lambda k: PAGES[k][0],
                    label_visibility="collapsed" if not device.phone() else "visible")

_pl = st.session_state["place"]
_how = {"gps": "from your device", "timezone": "first guess from your time zone",
        "manual": "chosen by you", "default": "starting place"}.get(st.session_state.get("place_src"), "")
locator.show(f"📍 {_pl.get('label', _pl['name'])}" + (f" · {_pl['he']}" if _pl.get("he") else "") + f"  ({_how})",
             auto=st.session_state.get("place_src") in ("default", "timezone"), on_pick=_on_pick)

# ---------------------------------------------------------------- settings
device.switch()
panel = device.input_panel("Settings: place, holidays, sighting rules · הגדרות")
with panel:
    st.subheader("Your place · מקום")
    preset_names = [p["name"] for p in places.PRESETS]
    q = st.text_input("Search for a town or city", key="place_q", placeholder="e.g. Boulder, Haifa, Paris")
    if q.strip():
        res = places.search(q)
        if res:
            pick = st.selectbox("Matches", range(len(res)), key="place_pick",
                                format_func=lambda i: places.label(res[i]) + (f" · {res[i]['he']}" if res[i].get("he") else ""))
            if st.button("Use this place", key="place_use", width="stretch"):
                r = res[pick]
                _set_manual({"name": r["name"], "he": r.get("he", ""), "country": r["country"],
                             "lat": r["lat"], "lon": r["lon"], "tz": r["tz"], "label": places.label(r)})
                st.rerun()
        else:
            st.caption("No town of 15,000+ people by that name. Try a nearby city, or enter coordinates below.")
    pre = st.selectbox("…or a preset", ["—"] + preset_names, key="place_preset")
    if pre != "—" and st.session_state.get("_last_preset") != pre:
        st.session_state["_last_preset"] = pre
        p = dict(next(x for x in places.PRESETS if x["name"] == pre))
        p["label"] = places.label(p) if p.get("country_name") else f"{p['name']}"
        _set_manual(p)
        st.rerun()
    place = st.session_state["place"]
    place.setdefault("label", place["name"])
    with st.expander("Exact coordinates"):
        lat = st.number_input("Latitude (° north, negative = south)", -66.0, 66.0, float(place["lat"]), 0.0001,
                              format="%.4f", key=f"lat_{place['name']}_{place['lat']:.4f}")
        lon = st.number_input("Longitude (° east, negative = west)", -180.0, 180.0, float(place["lon"]), 0.0001,
                              format="%.4f", key=f"lon_{place['name']}_{place['lon']:.4f}")
        place = dict(place, lat=lat, lon=lon)
        st.caption(f"Time zone: {place['tz']}")
    st.caption(f"Using: {place['label']}" + (f" · {place['he']}" if place.get("he") else ""))

    st.subheader("Holidays · מועדים")
    scheme = st.selectbox("Festival days (fixed calendar)", list(cv.SCHEMES), format_func=lambda k: cv.SCHEMES[k],
                          index=0 if place.get("country") == "IL" else 1, key=f"scheme_{place['name']}",
                          help="Israel: one day per festival. Diaspora: Orthodox and most Conservative congregations "
                               "outside Israel add a second day (Yom Tov Sheni). One day everywhere: Reform and many "
                               "Reconstructionist congregations, with a one-day Rosh Hashanah.")
    israel = scheme != "diaspora"
    candle_default = 40 if place["name"] == "Jerusalem" else 18
    candle = st.number_input("Candle lighting: minutes before sunset", 0, 60, candle_default, 1,
                             key=f"candle_{place['name']}",
                             help="18 minutes is the common custom; Jerusalem custom is 40.")
    modern = st.toggle("Show Israeli national days", value=True, key="modern")
    hillula = st.toggle("Show hillula days · ימי הילולא", value=True, key="hillula",
                        help="Anniversaries of the passing of great tzaddikim, from Moses and Rabbi Shimon bar Yochai to "
                             "the Baba Sali. Click one for a short history. Shown in the fixed, observed and Early "
                             "Temple calendars.")
    sigd = st.toggle("Show Sigd · סיגד (Beta Israel; Israeli state holiday)", value=True, key="sigd")
    omer = st.toggle("Show the Omer count · ספירת העומר", value=False, key="omer")

    st.subheader("Sighting rules · קידוש החודש")
    st.caption("Used by the observed and Karaite calendars (and by the Early Temple Period calendar's equinox rule). "
               "For the Karaite calendar the spring marker stands in for the barley (aviv) inspection.")
    crit = st.selectbox("Crescent visibility from Jerusalem", list(oc.CRITERIA), key="crit",
                        format_func=lambda k: oc.CRITERIA[k])
    eq = st.selectbox("Spring marker for the leap month", list(oc.EQUINOX_SOURCES), key="eq",
                      format_func=lambda k: oc.EQUINOX_SOURCES[k])
    nisan_day = st.select_slider("The equinox must fall no later than this day of Nisan", [14, 15, 16], value=15,
                                 key="nisan_day",
                                 help="15 follows Rambam, Kiddush HaChodesh 4:2: if the tekufah would fall on 16 Nisan "
                                      "or later, the year was given a second Adar.")

    st.subheader("Early Temple Period · לוח תקופת המקדש הקדומה")
    pt_rule = st.selectbox("Leap month", list(ptc.LEAP_RULES), key="pt_rule", format_func=lambda k: ptc.LEAP_RULES[k],
                           help="Months always begin at the true new moon. This only decides which years get a "
                                "second Adar.")

    st.subheader("Ancient Torah reading cycle · המחזור התלת-שנתי")
    st.caption("Used by the Observed and Early Temple Period calendars: a reconstruction of the triennial cycle read "
               "in the Land of Israel in late antiquity (Talmud, Megillah 29b). Scholars disagree on both points below.")
    tri_start = st.selectbox("Cycle begins", ["nisan", "tishrei"], key="tri_start",
                             format_func=lambda k: {"nisan": "In Nisan (spring)", "tishrei": "In Tishrei (autumn)"}[k])
    tri_len = st.selectbox("Length of the cycle", ["3", "3.5"], key="tri_len",
                           format_func=lambda k: {"3": "Three years", "3.5": "Three and a half years (two per Sabbatical cycle)"}[k])
    rdg.TRIENNIAL_OPTS.update(start=tri_start, length=tri_len)

    st.subheader("Samaritan · לוח השומרונים")
    sam_rule = st.selectbox("Which day begins the month", list(smc.RULES), key="sam_rule",
                            format_func=lambda k: smc.RULES[k])
    sam_floor = st.toggle("Passover sacrifice never before 8 April", value=False, key="sam_floor",
                          help="A rule sometimes quoted for the community. Off by default: it contradicts the published "
                               "start of the Sixth Month on 19 Aug 2001.")

ctx = {
    "place": place, "candle": int(candle), "crit": crit, "eq": eq, "nisan_day": int(nisan_day), "pt_rule": pt_rule,
    "scheme": scheme, "scheme_key": f"scheme_{place['name']}",
    "fixed": cv.FixedView(israel, modern, omer, scheme=scheme, sigd=sigd, hillula=hillula),
    "observed": observed_view(crit, eq, int(nisan_day), omer, hillula),
    "pretemple": pretemple_view(pt_rule, eq, int(nisan_day), omer, hillula),
    "karaite": karaite_view(crit, eq, int(nisan_day), omer),
    "samaritan": samaritan_view(sam_rule, bool(sam_floor)),
}
ctx["view"] = {cv.FIXED: ctx["fixed"], cv.OBSERVED: ctx["observed"], cv.PRETEMPLE: ctx["pretemple"],
               cv.KARAITE: ctx["karaite"], cv.SAMARITAN: ctx["samaritan"]}[cal]

PAGES[page][1](ctx)

st.html("<div class='sl-frieze' role='presentation' style='margin-top:1.2rem'></div>"
        "<div class='sl-muted' style='font-size:.8rem'>Astronomy: NASA JPL DE440s via Skyfield. "
        "The observed, Karaite and Samaritan calendars are modelled reconstructions, not rulings for practice; "
        "follow your community's published calendar.</div>")

dk.desktop_controls(st)
