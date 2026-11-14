"""
The Samaritan (Israelite Samaritan) calendar - a calculated lunisolar calendar.

The Samaritan priestly family computes the calendar ("Ishban Kashta", the true calculation); the full
method is kept within that family. This module follows the published reconstruction of
E. M. Reingold & N. Dershowitz, *Calendrical Calculations* (4th ed., 2018), "modern calculation":

* A month begins on the day of the true (geocentric) conjunction of Sun and Moon. Two versions of the
  day rule are offered:
    'sunset' (default): the Samaritan day (sunset to sunset at Mount Gerizim) that contains the
             conjunction is day 1. This is this app's calibration against published community dates
             (see Validation below); it is not a published Samaritan rule.
    'noon':  Reingold & Dershowitz's published rule - the day of the conjunction if it falls at or
             before apparent noon at Mount Gerizim (32.1994 N, 35.2728 E), else the following day.
             It misses 5 of the 14 dates: the 14th is a day late in 2016, 2025 and 2026 (and the 2026
             pilgrimage with it), and in 2025 that pushes Shavuot a full week late (8 June for 1 June).
* The First Month (Abib) is the first month whose conjunction falls after noon of 11 March in the
  Julian calendar (24 March Gregorian in 1900-2099). A thirteenth month is added before it when needed.
* Optional (off by default): a "Passover sacrifice never before 8 April" floor, sometimes quoted for the
  community. When on, a year whose 14th would fall earlier is intercalated. It changes 10 of the
  years 1850-2150 and contradicts a published date (the Sixth Month of 3640 began 19 Aug 2001),
  so it is off by default.

Validation (sunset rule, no floor): 14 of 14 published community dates - 14th of the First Month
2016-04-20, 2017-04-10, 2018-04-29, 2019-04-18, 2020-05-06, 2024-04-22, 2025-04-11, 2026-04-30;
closing pilgrimage (21st) 2026-05-07; Shavuot 2017-06-04, 2025-06-01; Sixth Month 2001-08-19 and
2026-09-11; Seventh Month 2026-10-11. The noon rule gives 9 of 14. (In 2026 the sacrifice ceremony
itself was brought forward to 10 April because of the war; the calendar date was 30 April.)
* Years are counted from the entry into Canaan; the year number advances at the Sixth Month
  (year 3640 began 19 Aug 2001; year 3656 in 2017).

Conjunctions come from NASA JPL DE440s (stored in data/crescents_jerusalem.csv.gz); apparent noon uses
the NOAA equation-of-time formula (accurate to well under a minute).
"""
from __future__ import annotations

import bisect
import math
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache

import fixed_calendar as fc
import observed_calendar as oc
from fixed_calendar import Holiday, HDate

GERIZIM = {"name": "Mount Gerizim", "lat": 32.1994, "lon": 35.2728, "elev": 881.0}
ORDINAL = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth",
           "Eleventh", "Twelfth", "Thirteenth"]
ORDINAL_HE = ["החדש הראשון", "החדש השני", "החדש השלישי", "החדש הרביעי", "החדש החמישי", "החדש הששי",
              "החדש השביעי", "החדש השמיני", "החדש התשיעי", "החדש העשירי", "החדש עשתי עשר",
              "החדש שנים עשר", "החדש השלשה עשר"]


def equation_of_time_min(d: date) -> float:
    """Apparent minus mean solar time in minutes (NOAA approximation)."""
    n = d.timetuple().tm_yday
    g = 2 * math.pi / 365.0 * (n - 1)
    return 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                     - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))


def apparent_local(t_utc: datetime) -> datetime:
    """UTC instant -> local apparent (sundial) time at Mount Gerizim, as a naive datetime."""
    lmt = t_utc.replace(tzinfo=None) + timedelta(hours=GERIZIM["lon"] / 15.0)
    return lmt + timedelta(minutes=equation_of_time_min(lmt.date()))


def solar_declination_deg(d: date) -> float:
    n = d.timetuple().tm_yday
    g = 2 * math.pi / 365.0 * (n - 1)
    return math.degrees(0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
                        + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))


def sunset_apparent_hours(d: date) -> float:
    """Apparent solar time of sunset at Gerizim (Sun's upper limb, standard refraction), NOAA formulas."""
    phi = math.radians(GERIZIM["lat"])
    dec = math.radians(solar_declination_deg(d))
    cos_h = (math.sin(math.radians(-0.833)) - math.sin(phi) * math.sin(dec)) / (math.cos(phi) * math.cos(dec))
    return 12.0 + math.degrees(math.acos(max(-1.0, min(1.0, cos_h)))) / 15.0


RULES = {
    "sunset": "The Samaritan day (sunset to sunset) that contains the conjunction is day 1 "
              "(matches all 14 published dates checked, 2001-2026)",
    "noon": "Reingold & Dershowitz: day of the conjunction if at or before apparent noon, else the next day "
            "(matches 9 of 14)",
}


def month_start_for_conjunction(t_utc: datetime, rule: str = "sunset") -> date:
    """First day of the month (Gregorian daytime date) for a conjunction at t_utc."""
    la = apparent_local(t_utc)
    h = la.hour + la.minute / 60 + la.second / 3600
    cut = 12.0 if rule == "noon" else sunset_apparent_hours(la.date())
    return la.date() if h <= cut else la.date() + timedelta(days=1)


def julian_to_gregorian(y: int, m: int, d: int) -> date:
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    jdn = d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - 32083
    return date.fromordinal(jdn - 1721425)


def noon_utc_at_gerizim(d: date) -> datetime:
    """UTC instant of apparent noon at Gerizim on civil date d."""
    lmt_noon = datetime(d.year, d.month, d.day, 12) - timedelta(minutes=equation_of_time_min(d))
    return (lmt_noon - timedelta(hours=GERIZIM["lon"] / 15.0)).replace(tzinfo=timezone.utc)


@dataclass
class SamMonth:
    year: int          # Samaritan year (from the entry into Canaan)
    month: int         # 1..12, 13 = intercalary month (before the First Month)
    start: date
    length: int
    conj_utc: datetime
    leap: bool

    @property
    def name(self) -> str:
        return f"{ORDINAL[self.month - 1]} Month"

    @property
    def name_he(self) -> str:
        return ORDINAL_HE[self.month - 1]

    @property
    def end(self) -> date:
        return self.start + timedelta(days=self.length - 1)


@lru_cache(maxsize=1)
def conjunctions() -> list[datetime]:
    df = oc.crescents()
    return sorted({c.to_pydatetime() for c in df["conj_utc"]})


@lru_cache(maxsize=8)
def calendar(april8_floor: bool = False, rule: str = "sunset") -> list[SamMonth]:
    conj = conjunctions()
    starts = [month_start_for_conjunction(c, rule) for c in conj]
    first_months = []
    for gy in range(1850, 2151):
        noon = noon_utc_at_gerizim(julian_to_gregorian(gy, 3, 11))
        i = bisect.bisect_left(conj, noon)
        if i >= len(conj):
            break
        if april8_floor and starts[i] + timedelta(days=13) < date(gy, 4, 8):
            i += 1
        if i < len(conj):
            first_months.append(i)
    months: list[SamMonth] = []
    for a, b in zip(first_months, first_months[1:]):
        n = b - a
        if n not in (12, 13):
            raise RuntimeError(f"Samaritan year from {starts[a]} has {n} months")
        gy = starts[a].year
        for k in range(n):
            i = a + k
            if i + 1 >= len(starts):
                break
            m = k + 1 if k < 12 else 13
            year = gy + 1638 + (1 if m >= 6 else 0)
            months.append(SamMonth(year, m, starts[i], (starts[i + 1] - starts[i]).days, conj[i], n == 13))
    return months


def _shavuot(first_15: date) -> date:
    """Sunday after the Sabbath that falls within the Feast of Unleavened Bread (15th-21st), + 49 days."""
    for k in range(7):
        d = first_15 + timedelta(days=k)
        if d.weekday() == 5:
            return d + timedelta(days=1 + 49)
    raise AssertionError


class SamaritanCalendar:
    """Interface parallel to ObservedCalendar, for the pages."""

    def __init__(self, april8_floor: bool = False, rule: str = "sunset"):
        self.april8_floor, self.rule = april8_floor, rule
        self.months = calendar(april8_floor, rule)
        self._starts = [m.start for m in self.months]
        self._by = {(m.year, m.month): m for m in self.months}

    @property
    def first_day(self):
        return self.months[0].start

    @property
    def last_day(self):
        return self.months[-1].end

    def covers(self, d: date) -> bool:
        return self.first_day <= d <= self.last_day

    def month_of(self, d: date) -> SamMonth | None:
        if not self.covers(d):
            return None
        return self.months[bisect.bisect_right(self._starts, d) - 1]

    def from_gregorian(self, d: date):
        m = self.month_of(d)
        if m is None:
            return None
        return SamDate(m.year, m.month, (d - m.start).days + 1)

    def get_month(self, year: int, month: int) -> SamMonth | None:
        return self._by.get((year, month))

    # The app pages work in festival cycles: First Month of year y (months 1-5 carry the number y)
    # through the last month before the next First Month (months 6-12/13 carry y + 1).
    def cycle_months(self, y: int) -> list[SamMonth]:
        a = self._by.get((y, 1))
        b = self._by.get((y + 1, 1))
        if a is None or b is None:
            return []
        i, j = self.months.index(a), self.months.index(b)
        return self.months[i:j]

    def cycle_leap(self, y: int) -> bool:
        return len(self.cycle_months(y)) == 13

    def cycle_of(self, d: date) -> int | None:
        m = self.month_of(d)
        if m is None:
            return None
        return m.year if m.month <= 5 else m.year - 1

    def years(self) -> list[int]:
        """Cycle numbers (the year number carried by the First Month) fully inside the table."""
        return sorted(y for (y, m) in self._by if m == 1 and (y + 1, 1) in self._by)

    def is_leap(self, year: int) -> bool:
        return self.cycle_leap(year)

    def year_months(self, year: int) -> list[SamMonth]:
        return self.cycle_months(year)

    def to_gregorian(self, year: int, month: int, day: int) -> date | None:
        m = self._by.get((year, month))
        return m.start + timedelta(days=day - 1) if m else None

    def holidays_for_year(self, year: int, **kw) -> list[Holiday]:
        """Festivals of the spring-to-spring cycle whose First Month carries number `year`."""
        H = []

        def add(m, d, name, he, kind, note=""):
            g = self.to_gregorian(year, m, d)
            if g:
                H.append(Holiday(g, name, he, kind, SamDate(year, m, d), note))

        add(1, 1, "Samaritan First Month: head of the months", "ראש החדשים", "minor",
            "Exod 12:2 - the First Month, in spring; the year number itself advances at the Sixth Month")
        add(1, 14, "Passover sacrifice (Mount Gerizim)", "קרבן הפסח", "major", "offered at evening on the 14th")
        add(1, 15, "Feast of Unleavened Bread begins", "חג המצות", "major")
        for d in range(16, 21):
            add(1, d, f"Unleavened Bread, day {d - 14}", "חג המצות", "chol")
        add(1, 21, "Feast of Unleavened Bread (pilgrimage)", "חג המצות", "major", "first pilgrimage to Mount Gerizim")
        f15 = self.to_gregorian(year, 1, 15)
        if f15:
            sh = _shavuot(f15)
            sd = self.from_gregorian(sh)
            H.append(Holiday(sh, "Shavuot (pilgrimage)", "חג השבועות", "major", sd,
                             "always a Sunday: 50 days from the Sunday after the Sabbath of Unleavened Bread"))
        y7 = year + 1   # the Seventh Month carries the next year number
        for m, d, name, he, kind, note in [
            (7, 1, "Feast of the Seventh Month (Samaritan New Year)", "חג החדש השביעי", "major", ""),
            (7, 10, "Day of Atonement", "יום הכפורים", "major", ""),
            (7, 15, "Feast of Tabernacles (pilgrimage)", "חג הסוכות", "major", "third pilgrimage to Mount Gerizim"),
            (7, 22, "Eighth Day of Assembly", "שמיני עצרת", "major", "")]:
            g = self.to_gregorian(y7, m, d)
            if g:
                H.append(Holiday(g, name, he, kind, SamDate(y7, m, d), note))
        for d in range(16, 22):
            g = self.to_gregorian(y7, 7, d)
            if g:
                H.append(Holiday(g, f"Tabernacles, day {d - 14}", "חג הסוכות", "chol", SamDate(y7, 7, d)))
        H.sort(key=lambda h: h.date)
        return H

    def holidays_between(self, start: date, end: date, **kw) -> list[Holiday]:
        out = []
        for (y, m), mo in self._by.items():
            if m == 1 and mo.start <= end + timedelta(days=200) and mo.start >= start - timedelta(days=400):
                out.extend(h for h in self.holidays_for_year(y) if start <= h.date <= end)
        out.sort(key=lambda h: h.date)
        return out


@dataclass(frozen=True)
class SamDate:
    year: int
    month: int
    day: int

    @property
    def month_name(self) -> str:
        return f"{ORDINAL[self.month - 1]} Month"

    def __str__(self) -> str:
        return f"{self.day} {self.month_name} {self.year}"

    def hebrew(self) -> str:
        return f"{fc.hebrew_numeral(self.day)} ב{ORDINAL_HE[self.month - 1][1:]} {fc.hebrew_numeral(self.year % 1000)}"
