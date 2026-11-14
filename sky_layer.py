"""
Astronomy shown alongside the calendars: true new moon vs. molad, true equinoxes/solstices vs.
the tekufot of Shmuel and Rav Adda, Moon phase per day.

The molad and the tekufot are reckoned in Jerusalem local mean time (traditional): UT + 2 h 20 m 56 s.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from functools import lru_cache

import fixed_calendar as fc
import sky_engine as se

JERUSALEM_MEAN_OFFSET = timedelta(hours=35.2354 / 15.0)  # 2 h 20 m 56 s


def rd_moment_to_utc(moment: float) -> datetime:
    """Fractional RD moment in Jerusalem local mean time -> UTC datetime."""
    local = datetime(1, 1, 1) + timedelta(days=moment - 1)
    return (local - JERUSALEM_MEAN_OFFSET).replace(tzinfo=timezone.utc)


def molad_utc(month: int, year: int) -> datetime:
    return rd_moment_to_utc(fc.molad(month, year))


@lru_cache(maxsize=512)
def _conj_near(day: date) -> tuple[datetime, ...]:
    return tuple(se.new_moons(day - timedelta(days=20), day + timedelta(days=20)))


def molad_vs_conjunction(month: int, year: int) -> dict:
    """The molad of a fixed-calendar month and the true (JPL) conjunction nearest to it."""
    m = molad_utc(month, year)
    conj = min(_conj_near(m.date()), key=lambda c: abs((c - m).total_seconds()))
    return {"molad_utc": m, "conjunction_utc": conj,
            "molad_minus_true_h": (m - conj).total_seconds() / 3600.0,
            "molad_traditional": fc.molad_traditional(month, year)}


def seasons_vs_tekufot(greg_year: int) -> list[dict]:
    """True equinoxes and solstices of a Gregorian year with the corresponding tekufot."""
    out = []
    for t, k in se.seasons(date(greg_year, 1, 1), date(greg_year + 1, 1, 1)):
        # tekufat Nisan of Hebrew year (greg_year + 3760); Tammuz/Tishrei/Tevet follow it
        hy = greg_year + 3760
        sh = rd_moment_to_utc(fc.tekufah_shmuel(hy, k))
        ad = rd_moment_to_utc(fc.tekufah_adda(hy, k))
        out.append({"season": se.SEASON_NAMES[k], "tekufah": se.TEKUFAH_NAMES[k], "true_utc": t,
                    "shmuel_utc": sh, "adda_utc": ad,
                    "shmuel_minus_true_d": (sh - t).total_seconds() / 86400.0,
                    "adda_minus_true_d": (ad - t).total_seconds() / 86400.0})
    return out


PHASE_NAMES = ["New moon", "First quarter", "Full moon", "Last quarter"]


def moon_phase_days(days: list[date], tzname: str) -> dict[date, dict]:
    """Moon illumination at local 8 pm and the principal phases (local dates) for each day."""
    from zoneinfo import ZoneInfo
    tz = ZoneInfo(tzname)
    when = [datetime(d.year, d.month, d.day, 20, tzinfo=tz).astimezone(timezone.utc) for d in days]
    illum = se.moon_illumination(when)
    elong = se.moon_elongation(when)
    out = {d: {"illum": float(i), "elong": float(e), "event": None, "event_time": None}
           for d, i, e in zip(days, illum, elong)}
    if days:
        for t, ph in se.moon_phase_events(min(days) - timedelta(days=1), max(days) + timedelta(days=2)):
            ld = t.astimezone(tz)
            if ld.date() in out:
                out[ld.date()]["event"] = PHASE_NAMES[ph]
                out[ld.date()]["event_time"] = ld
    return out
