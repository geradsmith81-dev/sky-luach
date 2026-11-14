"""
An observational ("Temple-period style") Hebrew calendar reconstructed from NASA JPL astronomy.

Rules (each is a modelling choice, shown in the app):
1. The day begins at sunset in Jerusalem.
2. A month has 29 or 30 days. On the evening that ends day 29, if the young crescent is
   predicted visible from Jerusalem by the chosen criterion, the next day is 1st of the new
   month; otherwise day 30 is added and the month ends regardless (Mishnah Rosh Hashanah 2;
   a month never exceeds 30 days).
3. Leap month (Adar II): Nisan is the first month in which the spring equinox falls no later
   than day 15 (Rambam, Kiddush HaChodesh 4:2: if the tekufah of Nisan would fall on the 16th of
   Nisan or later, the year is intercalated). The day limit and the equinox (true JPL equinox,
   tekufah of Shmuel, or of Rav Adda) can be changed.
4. Holidays fall on their biblical/rabbinic dates in these months, one day each (as in the Land
   of Israel); Shavuot is the 50th day counted from 16 Nisan, so it may fall on 5, 6 or 7 Sivan.
5. None of the fixed calendar's postponement rules (lo ADU rosh, molad zaken, ...) apply.

Precomputed tables in data/ (built by tools/build_tables.py from de440s.bsp):
  crescents_jerusalem.csv.gz  crescent parameters for evenings around every new moon
  seasons.csv                 equinoxes and solstices
"""
from __future__ import annotations

import bisect
import math
import os
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache

import pandas as pd

import fixed_calendar as fc
from fixed_calendar import (NISAN, IYYAR, SIVAN, TAMMUZ, AV, ELUL, TISHREI, MARHESHVAN, KISLEV,
                            TEVET, SHEVAT, ADAR, ADAR_II, Holiday, HDate)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CRESCENT_FILE = os.path.join(DATA, "crescents_jerusalem.csv.gz")
SEASONS_FILE = os.path.join(DATA, "seasons.csv")

CRITERIA = {
    "yallop_B": "Yallop zone A or B: naked eye in perfect conditions (q > -0.014)",
    "yallop_A": "Yallop zone A only: easily visible (q > +0.216)",
    "yallop_C": "Yallop A-C: includes 'may need optical aid to find' (q > -0.160)",
    "odeh_A": "Odeh 2004 zone A: visible to the naked eye (V >= 5.65)",
}
EQUINOX_SOURCES = {
    "true": "True spring equinox (JPL)",
    "shmuel": "Tekufah of Shmuel (365 1/4-day year)",
    "adda": "Tekufah of Rav Adda (19-year cycle year)",
}
ORDER = [NISAN, IYYAR, SIVAN, TAMMUZ, AV, ELUL, TISHREI, MARHESHVAN, KISLEV, TEVET, SHEVAT, ADAR, ADAR_II]


def _visible(row, criterion: str) -> bool:
    q, v = row["q"], row["v"]
    if criterion == "yallop_A":
        return q > 0.216
    if criterion == "yallop_B":
        return q > -0.014
    if criterion == "yallop_C":
        return q > -0.160
    if criterion == "odeh_A":
        return v >= 5.65
    raise ValueError(criterion)


# ----------------------------------------------------------------------------------------------
# tables
# ----------------------------------------------------------------------------------------------
def build_tables(start: date = date(1850, 1, 1), end: date = date(2150, 1, 10)) -> None:
    """Compute the precomputed tables from the JPL ephemeris (about 1 minute)."""
    import sky_engine as se
    os.makedirs(DATA, exist_ok=True)
    df = se.crescent_table(start, end)
    df.to_csv(CRESCENT_FILE, index=False, compression="gzip")
    rows = []
    for t, k in se.seasons(start, end):
        # the Hebrew (sunset-to-sunset) day in Jerusalem containing the event
        local = t + timedelta(hours=2)  # Israel standard time is close enough for the date
        d = local.date()
        _, sets = se.sun_events(se.JERUSALEM["lat"], se.JERUSALEM["lon"],
                                datetime(d.year, d.month, d.day, tzinfo=timezone.utc) - timedelta(hours=2),
                                datetime(d.year, d.month, d.day, tzinfo=timezone.utc) + timedelta(hours=22))
        sunset = sets[0]
        heb_day = d if t < sunset else d + timedelta(days=1)
        rows.append({"utc": t.isoformat(), "kind": k, "name": se.SEASON_NAMES[k],
                     "jerusalem_sunset_utc": sunset.isoformat(), "hebrew_day": heb_day.isoformat()})
    pd.DataFrame(rows).to_csv(SEASONS_FILE, index=False)


@lru_cache(maxsize=1)
def crescents() -> pd.DataFrame:
    if not os.path.exists(CRESCENT_FILE):
        build_tables()
    df = pd.read_csv(CRESCENT_FILE, compression="gzip")
    for c in ("conj_utc", "sunset_utc", "moonset_utc", "best_utc"):
        df[c] = pd.to_datetime(df[c], utc=True, format="ISO8601")
    df["evening"] = pd.to_datetime(df["evening"]).dt.date
    return df


@lru_cache(maxsize=1)
def season_table() -> pd.DataFrame:
    if not os.path.exists(SEASONS_FILE):
        build_tables()
    df = pd.read_csv(SEASONS_FILE)
    df["utc"] = pd.to_datetime(df["utc"], utc=True, format="ISO8601")
    df["hebrew_day"] = pd.to_datetime(df["hebrew_day"]).dt.date
    return df


@lru_cache(maxsize=1)
def _evening_index():
    df = crescents()
    idx = {e: i for i, e in enumerate(df["evening"])}
    conj_dates = sorted({c.date() for c in df["conj_utc"].dt.to_pydatetime()})
    return idx, conj_dates


def evening_info(evening: date) -> dict | None:
    """Crescent parameters on the evening of `evening` (None if the table does not cover it)."""
    idx, _ = _evening_index()
    i = idx.get(evening)
    if i is None:
        return None
    return crescents().iloc[i].to_dict()


def visible_on(evening: date, criterion: str) -> tuple[bool, dict | None]:
    info = evening_info(evening)
    if info is not None:
        if pd.isna(info["q"]):
            return False, info
        return _visible(info, criterion), info
    # not in the table: either a well-grown Moon (> 3 days after conjunction) or an old Moon
    _, conj_dates = _evening_index()
    j = bisect.bisect_right(conj_dates, evening) - 1
    if j >= 0 and (evening - conj_dates[j]).days >= 3:
        return True, None
    return False, None


# ----------------------------------------------------------------------------------------------
# months and years
# ----------------------------------------------------------------------------------------------
@dataclass
class ObsMonth:
    year: int          # AM year (changes at Tishrei)
    month: int         # fixed_calendar month number
    start: date        # Gregorian date of day 1 (daytime)
    length: int
    sighting_evening: date | None   # evening the crescent was (predicted) seen, or None if month completed to 30 days
    reason: str
    q: float | None
    v: float | None
    yallop: str
    conj_utc: datetime | None

    @property
    def name(self) -> str:
        if self.month == ADAR and self.leap:
            return "Adar I"
        return fc.MONTH_NAMES[self.month]

    leap: bool = False

    @property
    def end(self) -> date:
        return self.start + timedelta(days=self.length - 1)


@lru_cache(maxsize=8)
def month_chain(criterion: str = "yallop_B") -> list[tuple[date, date | None, str, float | None, float | None, str, object]]:
    """Successive month starts: (day-1 date, sighting evening or None, reason, q, v, zone, conj)."""
    df = crescents()
    first_conj = df["conj_utc"].iloc[0]
    sub = df[(df["conj_utc"] == first_conj)]
    start = None
    for _, r in sub.iterrows():
        if not pd.isna(r["q"]) and _visible(r, criterion):
            start = r["evening"] + timedelta(days=1)
            break
    if start is None:
        start = sub["evening"].iloc[-1] + timedelta(days=1)
    chain = [(start, start - timedelta(days=1), "first sighting", None, None, "", first_conj)]
    last_evening = df["evening"].iloc[-1]
    d1 = start
    while True:
        eve29 = d1 + timedelta(days=28)
        if eve29 > last_evening:
            break
        vis, info = visible_on(eve29, criterion)
        q = None if info is None or pd.isna(info["q"]) else float(info["q"])
        v = None if info is None or pd.isna(info["v"]) else float(info["v"])
        zone = info["yallop"] if info is not None else ""
        conj = info["conj_utc"] if info is not None else None
        if vis:
            d1 = d1 + timedelta(days=29)
            chain.append((d1, eve29, "crescent seen on the evening ending day 29", q, v, zone, conj))
        else:
            d1 = d1 + timedelta(days=30)
            info30 = evening_info(d1 - timedelta(days=1))
            conj30 = info30["conj_utc"] if info30 is not None else conj
            chain.append((d1, None, "not seen on the 29th evening: month completed to 30 days", q, v, zone, conj30))
    return chain


def _equinox_hebrew_days(source: str) -> dict[int, date]:
    """Gregorian year -> Hebrew (sunset-based) day containing the spring equinox/tekufah."""
    out = {}
    if source == "true":
        st = season_table()
        for _, r in st[st["kind"] == 0].iterrows():
            out[r["utc"].year] = r["hebrew_day"]
        return out
    for gy in range(1849, 2152):
        hy = gy + 3760  # Hebrew year whose Nisan falls in spring of gy
        moment = fc.tekufah_shmuel(hy) if source == "shmuel" else fc.tekufah_adda(hy)
        out[gy] = date.fromordinal(math.floor(moment + 0.25))  # traditional day starts 6 pm
    return out


@lru_cache(maxsize=32)
def calendar(criterion: str = "yallop_B", equinox: str = "true", nisan_day: int = 15) -> list[ObsMonth]:
    """All complete months of the observational calendar, with names and AM years."""
    chain = month_chain(criterion)
    starts = [c[0] for c in chain]
    eq = _equinox_hebrew_days(equinox)
    nisan_starts = []
    for gy in sorted(eq):
        e = eq[gy]
        cand = [s for s in starts if e - timedelta(days=75) <= s <= e + timedelta(days=30)]
        ok = [s for s in cand if e <= s + timedelta(days=nisan_day - 1)]
        if ok:
            nisan_starts.append(ok[0])
    months: list[ObsMonth] = []
    for a, b in zip(nisan_starts, nisan_starts[1:]):
        ia, ib = starts.index(a), starts.index(b)
        n = ib - ia
        if n not in (12, 13):
            raise RuntimeError(f"year from {a} has {n} months")
        gy = a.year
        for k in range(n):
            s, eve, reason, q, v, zone, conj = chain[ia + k]
            length = (starts[ia + k + 1] - s).days
            m = ORDER[k]
            am = gy + 3760 if m < TISHREI else gy + 3761
            months.append(ObsMonth(am, m, s, length, eve, reason, q, v, zone,
                                   conj.to_pydatetime() if hasattr(conj, "to_pydatetime") else conj,
                                   leap=(n == 13)))
    return months


@lru_cache(maxsize=32)
def _index(criterion, equinox, nisan_day):
    ms = calendar(criterion, equinox, nisan_day)
    return [m.start for m in ms], {(m.year, m.month): m for m in ms}


class ObservedCalendar:
    def __init__(self, criterion: str = "yallop_B", equinox: str = "true", nisan_day: int = 15):
        self.criterion, self.equinox, self.nisan_day = criterion, equinox, nisan_day
        self.months = calendar(criterion, equinox, nisan_day)
        self._starts, self._by = _index(criterion, equinox, nisan_day)

    # coverage
    @property
    def first_day(self) -> date:
        return self.months[0].start

    @property
    def last_day(self) -> date:
        return self.months[-1].end

    def covers(self, d: date) -> bool:
        return self.first_day <= d <= self.last_day

    def month_of(self, d: date) -> ObsMonth | None:
        if not self.covers(d):
            return None
        i = bisect.bisect_right(self._starts, d) - 1
        return self.months[i]

    def from_gregorian(self, d: date) -> HDate | None:
        m = self.month_of(d)
        if m is None:
            return None
        return HDate(m.year, m.month, (d - m.start).days + 1, self.is_leap(m.year))

    def get_month(self, year: int, month: int) -> ObsMonth | None:
        return self._by.get((year, month))

    def is_leap(self, year: int) -> bool:
        return (year, ADAR_II) in self._by

    def year_months(self, year: int) -> list[ObsMonth]:
        order = [TISHREI, MARHESHVAN, KISLEV, TEVET, SHEVAT, ADAR, ADAR_II, NISAN, IYYAR, SIVAN, TAMMUZ, AV, ELUL]
        return [self._by[(year, m)] for m in order if (year, m) in self._by]

    def to_gregorian(self, year: int, month: int, day: int) -> date | None:
        m = self._by.get((year, month))
        if m is None:
            return None
        return m.start + timedelta(days=day - 1)

    def month_label(self, year: int, month: int) -> str:
        if month == ADAR and self.is_leap(year):
            return "Adar I"
        return fc.MONTH_NAMES[month]

    def year_complete(self, year: int) -> bool:
        need = [TISHREI, ELUL]
        return all((year, m) in self._by for m in need)

    def years(self) -> list[int]:
        return sorted({y for (y, m) in self._by if self.year_complete(y)})

    # holidays
    def holidays_for_year(self, year: int, rosh_chodesh: bool = True, omer: bool = False) -> list[Holiday]:
        """Holidays from 1 Tishrei to the end of Elul of AM `year` (one day each, as in Israel)."""
        H: list[Holiday] = []
        if not self.year_complete(year):
            return H
        adar = ADAR_II if self.is_leap(year) else ADAR

        def g(y, m, d):
            return self.to_gregorian(y, m, d)

        def add(y, m, d, name, he, kind, note=""):
            gd = g(y, m, d)
            if gd is not None:
                H.append(Holiday(gd, name, he, kind, HDate(y, m, d, self.is_leap(y)), note))

        def wd(y, m, d):
            gd = g(y, m, d)
            return gd.weekday() if gd else None

        add(year, TISHREI, 1, "Rosh Hashanah", "ראש השנה", "major",
            "one day, as the Torah prescribes; a second day was added when witnesses arrived late")
        gd = 4 if wd(year, TISHREI, 3) == fc.SHABBAT else 3
        add(year, TISHREI, gd, "Tzom Gedaliah", "צום גדליה", "fast", "postponed from Shabbat" if gd == 4 else "")
        yk_note = ""
        if wd(year, TISHREI, 10) in (fc.FRIDAY, fc.SUNDAY):
            yk_note = "falls next to Shabbat - impossible in the fixed calendar"
        add(year, TISHREI, 10, "Yom Kippur", "יום כיפור", "major", yk_note)
        add(year, TISHREI, 15, "Sukkot I", "סוכות א׳", "major")
        for d in range(16, 21):
            add(year, TISHREI, d, f"Sukkot {d - 14} (Chol HaMoed)", "חול המועד סוכות", "chol")
        hr_note = "on Shabbat - avoided by the fixed calendar" if wd(year, TISHREI, 21) == fc.SHABBAT else ""
        add(year, TISHREI, 21, "Hoshana Rabbah", "הושענא רבה", "chol", hr_note)
        add(year, TISHREI, 22, "Shemini Atzeret", "שמיני עצרת", "major")
        start = g(year, KISLEV, 25)
        if start:
            for i in range(8):
                gd8 = start + timedelta(days=i)
                H.append(Holiday(gd8, f"Chanukah: {i + 1} candle{'s' if i else ''} (day {i + 1})", "חנוכה",
                                 "minor", self.from_gregorian(gd8), "candles lit the evening before"))
        tv = "on Shabbat - impossible in the fixed calendar" if wd(year, TEVET, 10) == fc.SHABBAT else ""
        add(year, TEVET, 10, "Asara B'Tevet", "עשרה בטבת", "fast", tv)
        add(year, SHEVAT, 15, "Tu BiShvat", "ט״ו בשבט", "minor")
        if self.is_leap(year):
            add(year, ADAR, 14, "Purim Katan", "פורים קטן", "minor")
        e = 11 if wd(year, adar, 13) == fc.SHABBAT else 13
        add(year, adar, e, "Ta'anit Esther", "תענית אסתר", "fast", "moved to Thursday" if e == 11 else "")
        add(year, adar, 14, "Purim", "פורים", "minor")
        add(year, adar, 15, "Shushan Purim", "שושן פורים", "minor")
        add(year, NISAN, 14, "Erev Pesach (Passover offering)", "ערב פסח", "erev")
        add(year, NISAN, 15, "Pesach I", "פסח א׳", "major")
        for d in range(16, 21):
            add(year, NISAN, d, f"Pesach {d - 14} (Chol HaMoed)", "חול המועד פסח", "chol",
                "Omer offering (first barley)" if d == 16 else "")
        add(year, NISAN, 21, "Pesach VII", "שביעי של פסח", "major")
        add(year, IYYAR, 14, "Pesach Sheni", "פסח שני", "minor")
        omer1 = g(year, NISAN, 16)
        if omer1:
            lag = omer1 + timedelta(days=32)
            H.append(Holiday(lag, "Lag BaOmer", "ל״ג בעומר", "minor", self.from_gregorian(lag), "33rd day of the Omer"))
            shav = omer1 + timedelta(days=49)
            hd = self.from_gregorian(shav)
            note = f"50th day of the Omer = {hd.day} {fc.MONTH_NAMES[hd.month]}" if hd else ""
            if hd and hd.day != 6:
                note += " (the fixed calendar always has 6 Sivan)"
            H.append(Holiday(shav, "Shavuot", "שבועות", "major", hd, note))
            if omer:
                for i in range(49):
                    od = omer1 + timedelta(days=i)
                    H.append(Holiday(od, f"Omer day {i + 1}", "ספירת העומר", "omer", self.from_gregorian(od)))
        t = 18 if wd(year, TAMMUZ, 17) == fc.SHABBAT else 17
        add(year, TAMMUZ, t, "Tzom Tammuz (17 Tammuz)", "שבעה עשר בתמוז", "fast", "postponed from Shabbat" if t == 18 else "")
        a = 10 if wd(year, AV, 9) == fc.SHABBAT else 9
        add(year, AV, a, "Tisha B'Av", "תשעה באב", "fast", "postponed from Shabbat" if a == 10 else "")
        add(year, AV, 15, "Tu B'Av", "ט״ו באב", "minor")
        if rosh_chodesh:
            for m in fc.year_months(year):
                om = self.get_month(year, m)
                if om is None or m == TISHREI:
                    continue
                nm = self.month_label(year, m)
                he = fc.MONTH_NAMES_HE[m]
                prev_end = om.start - timedelta(days=1)
                pm = self.month_of(prev_end)
                if pm is not None and pm.length == 30:
                    H.append(Holiday(prev_end, f"Rosh Chodesh {nm} (day 1)", f"ראש חודש {he}", "rosh_chodesh",
                                     self.from_gregorian(prev_end)))
                    H.append(Holiday(om.start, f"Rosh Chodesh {nm} (day 2)", f"ראש חודש {he}", "rosh_chodesh",
                                     HDate(year, m, 1, self.is_leap(year))))
                else:
                    H.append(Holiday(om.start, f"Rosh Chodesh {nm}", f"ראש חודש {he}", "rosh_chodesh",
                                     HDate(year, m, 1, self.is_leap(year))))
        H.sort(key=lambda h: (h.date, fc._KIND_ORDER.get(h.kind, 9)))
        return H

    def holidays_between(self, start: date, end: date, **kw) -> list[Holiday]:
        out = []
        for y in self.years():
            if fc.new_year(y) > end.toordinal() + 60 or fc.new_year(y + 1) < start.toordinal() - 60:
                continue
            out.extend(h for h in self.holidays_for_year(y, **kw) if start <= h.date <= end)
        return out


# ----------------------------------------------------------------------------------------------
# comparison with the fixed calendar
# ----------------------------------------------------------------------------------------------
COMPARE_HOLIDAYS = [
    ("Rosh Hashanah", TISHREI, 1), ("Yom Kippur", TISHREI, 10), ("Sukkot I", TISHREI, 15),
    ("Chanukah (day 1)", KISLEV, 25), ("Asara B'Tevet", TEVET, 10), ("Tu BiShvat", SHEVAT, 15),
    ("Purim", None, 14), ("Pesach I", NISAN, 15), ("Shavuot", SIVAN, 6), ("17 Tammuz", TAMMUZ, 17),
    ("Tisha B'Av (date)", AV, 9),
]


def compare_year(year: int, obs: ObservedCalendar) -> list[dict]:
    """Holiday-by-holiday comparison for AM `year` (fixed Israel scheme vs observed)."""
    rows = []
    for name, m, d in COMPARE_HOLIDAYS:
        mf = m if m is not None else (ADAR_II if fc.is_leap(year) else ADAR)
        mo = m if m is not None else (ADAR_II if obs.is_leap(year) else ADAR)
        f = fc.to_gregorian(year, mf, d)
        if name == "Shavuot":
            o16 = obs.to_gregorian(year, NISAN, 16)
            o = o16 + timedelta(days=49) if o16 else None
        else:
            o = obs.to_gregorian(year, mo, d)
        rows.append({"holiday": name, "fixed": f, "observed": o,
                     "difference_days": (o - f).days if o else None})
    return rows


def compare_months(year: int, obs: ObservedCalendar) -> list[dict]:
    """First day of each month in both calendars for AM `year`."""
    rows = []
    for m in fc.year_months(year):
        f = fc.to_gregorian(year, m, 1)
        om = obs.get_month(year, m)
        rows.append({"month": fc.month_name(m, year), "fixed_start": f,
                     "observed_start": om.start if om else None,
                     "difference_days": (om.start - f).days if om else None,
                     "observed_length": om.length if om else None,
                     "fixed_length": fc.last_day_of_month(m, year)})
    if obs.is_leap(year) and not fc.is_leap(year):
        om = obs.get_month(year, ADAR_II)
        rows.append({"month": "Adar II (observed only)", "fixed_start": None, "observed_start": om.start,
                     "difference_days": None, "observed_length": om.length, "fixed_length": None})
    return rows
