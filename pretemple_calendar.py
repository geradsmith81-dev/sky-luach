"""
The Pre-Temple Period calendar (לוח טרום המקדש): an astronomical ideal.

* Each month begins at the TRUE new moon: day 1 starts at the first sunset in Jerusalem after the
  geocentric conjunction computed from NASA JPL DE440s. No mean molad, no crescent sighting,
  no postponement rules. Months are 29 or 30 days.
* Years are counted from AM 1. Because every month resets to the real Moon, the starting year
  changes only the numbering, never a month boundary.
* Leap month, two choices:
    'equinox' - Nisan is the first month in which the spring equinox (or tekufah) falls no later
                than the chosen day of Nisan, as in the observed calendar;
    'cycle'   - the traditional 19-year cycle counted from AM 1 (years 3, 6, 8, 11, 14, 17, 19
                are leap years), i.e. the fixed calendar's leap years with the real Moon.
* Holidays: one day each, as in the observed calendar; Shavuot is the 50th day from 16 Nisan.

There is no archaeological or textual evidence that such a calendar was used in ancient Israel;
biblical and rabbinic practice began the month with the visible crescent. It is shown as an
astronomical reference point.

Uses the precomputed Jerusalem table (data/crescents_jerusalem.csv.gz), which holds every true
conjunction 1850-2150 and the Jerusalem sunsets around it, so it works without the ephemeris file.
"""
from __future__ import annotations

import bisect
from datetime import date, timedelta
from functools import lru_cache

import pandas as pd

import fixed_calendar as fc
import observed_calendar as oc
from fixed_calendar import TISHREI, ADAR, ADAR_II

LEAP_RULES = {
    "equinox": "Spring equinox rule (same marker and day as the observed calendar)",
    "cycle": "19-year cycle counted from AM 1 (the fixed calendar's leap years)",
}


@lru_cache(maxsize=1)
def month_starts() -> list[tuple[date, object, object]]:
    """(day-1 date, conjunction UTC, the Jerusalem sunset that begins day 1) for every true new moon."""
    df = oc.crescents()
    out = []
    for conj, grp in df.groupby("conj_utc", sort=True):
        after = grp[grp["sunset_utc"] > conj].sort_values("sunset_utc")
        if after.empty:
            continue
        r = after.iloc[0]
        out.append((r["evening"] + timedelta(days=1), conj.to_pydatetime(), r["sunset_utc"].to_pydatetime()))
    return out


def _make(starts, k, n_in_year, am, m, leap):
    s, conj, sunset = starts[k]
    length = (starts[k + 1][0] - s).days
    reason = "true new moon; day 1 begins at the first Jerusalem sunset after it"
    return oc.ObsMonth(am, m, s, length, None, reason, None, None, "", conj, leap=leap), sunset


@lru_cache(maxsize=16)
def calendar(rule: str = "equinox", equinox: str = "true", nisan_day: int = 15):
    starts = month_starts()
    sdates = [s[0] for s in starts]
    months, sunsets = [], {}
    if rule == "equinox":
        eq = oc._equinox_hebrew_days(equinox)
        nisan_idx = []
        for gy in sorted(eq):
            e = eq[gy]
            ok = [i for i, s in enumerate(sdates)
                  if e - timedelta(days=75) <= s <= e + timedelta(days=30) and e <= s + timedelta(days=nisan_day - 1)]
            if ok:
                nisan_idx.append(ok[0])
        for a, b in zip(nisan_idx, nisan_idx[1:]):
            n = b - a
            if n not in (12, 13):
                raise RuntimeError(f"year from {sdates[a]} has {n} months")
            gy = sdates[a].year
            for k in range(n):
                m = oc.ORDER[k]
                am = gy + 3760 if m < TISHREI else gy + 3761
                om, ss = _make(starts, a + k, n, am, m, n == 13)
                months.append(om)
                sunsets[om.start] = ss
    elif rule == "cycle":
        # name each true-new-moon month after the fixed-calendar month that starts nearest to it
        fixed = []
        for y in range(5609, 5912):
            for m in fc.year_months(y):
                fixed.append((fc.to_gregorian(y, m, 1), y, m))
        fixed.sort()
        fd = [f[0] for f in fixed]
        for k in range(len(starts) - 1):
            s = sdates[k]
            j = bisect.bisect_left(fd, s)
            cand = [i for i in (j - 1, j) if 0 <= i < len(fd)]
            i = min(cand, key=lambda i: abs((fd[i] - s).days))
            _, y, m = fixed[i]
            om, ss = _make(starts, k, 0, y, m, fc.is_leap(y))
            months.append(om)
            sunsets[om.start] = ss
        # keep only Nisan-to-Nisan complete stretches (drop partial ends)
        while months and months[0].month != fc.NISAN:
            months.pop(0)
    else:
        raise ValueError(rule)
    return months, sunsets


class PreTempleCalendar(oc.ObservedCalendar):
    """Same interface as ObservedCalendar (months, conversion, holidays)."""
    rh_note = "one day; the month begins at the true new moon"

    def __init__(self, rule: str = "equinox", equinox: str = "true", nisan_day: int = 15):
        self.rule, self.equinox, self.nisan_day = rule, equinox, nisan_day
        self.criterion = None
        self.months, self.sunset_of_start = calendar(rule, equinox, nisan_day)
        self._starts = [m.start for m in self.months]
        self._by = {(m.year, m.month): m for m in self.months}

    def holidays_for_year(self, year, rosh_chodesh=True, omer=False):
        H = super().holidays_for_year(year, rosh_chodesh=rosh_chodesh, omer=omer)
        for h in H:
            if h.name == "Rosh Hashanah":
                h.note = self.rh_note
        return H
