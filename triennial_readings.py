"""Ancient Land-of-Israel triennial Torah reading cycle (a stated reconstruction / model).

What it does
------------
``reading_for_shabbat(d, cal=None, start="nisan", length="3", division="accepted")``
returns the seder (or sedarim) of the Torah read on the Shabbat ``d`` under a *model* of
the triennial cycle practised in the Land of Israel in late antiquity, on the months of
an astronomical calendar of the app: ``observed_calendar.ObservedCalendar`` (first
visible crescent) or ``pretemple_calendar.PreTempleCalendar`` (true new moon).  ``cal``
defaults to an ObservedCalendar.  It returns ``None`` if ``d`` is not a Saturday, lies
outside the calendar's range (about 15/16 Mar 1850 - 10/11 Mar 2149), or falls before
the first modelled cycle begins.  Every result has ``model=True``.

The sedarim
-----------
data/readings/triennial_sedarim.json lists the Masoretic seder divisions of the Torah
with verse ranges:
* ``division="accepted"`` (default): 154 sedarim (Genesis 43, Exodus 29, Leviticus 23,
  Numbers 32, Deuteronomy 27), the division accepted in printed editions.  154 is the
  number usually given for the Torah sedarim (Jewish Encyclopedia, "Triennial Cycle").
* ``division="leningrad"``: 167 sedarim, the seder marks of the Leningrad Codex
  (B19a), which lists 167 sedarim at the end of the Torah.
Seder positions come from "Miqra according to the Masorah" (MAM, ed. Seth (Avi) Kadish,
Hebrew Wikisource, CC BY-SA 4.0), whose documentation notes record where the Leningrad
Codex, Sefer HaHilufim and the printed division differ.  Each seder runs to the verse
before the next one.

The schedule model (all choices are this module's, see "Uncertainties")
-----------------------------------------------------------------------
1. Ordinary Shabbat: one seder, in order, from Genesis 1:1 to the end of Deuteronomy.
2. Festival Shabbat (a Shabbat that is Rosh Hashanah, Yom Kippur, Sukkot I, a day of
   Chol HaMoed Sukkot / Hoshana Rabbah, Shemini Atzeret, any day of Pesach, or Shavuot
   in ``cal``): the festival reading named in Mishnah Megillah 3:5 replaces the seder
   and the cycle does not advance.  The Mishnah names incipits only; the verse extents
   used are the Masoretic paragraph from the incipit, or the whole of Leviticus 23 where
   the Mishnah names "the section of the appointed times" (stored in the data file).
3. The four special Shabbatot of Adar/Nisan (Mishnah Megillah 3:4): Shekalim (Shabbat on
   or before 1 Adar; in a leap year the second Adar), Zachor (Shabbat on or before 13
   Adar), Parah (the Shabbat before HaChodesh), HaChodesh (Shabbat on or before 1 Nisan),
   computed on the months of ``cal``.  The special section *replaces* the seder ("on the
   fifth they return to the order") and the cycle does not advance.
4. Rosh Chodesh, Chanukah and Purim falling on Shabbat are labelled but do not interrupt
   the cycle in this model.
5. Cycle windows (``length`` and ``start``):
   * ``length="3"`` (default): a new cycle begins every three years on the first ordinary
     Shabbat on or after 1 Nisan (``start="nisan"``, after Buechler) or 1 Tishrei
     (``start="tishrei"``).  The phase is anchored arbitrarily: Nisan cycles begin in
     years AM 5610 + 3k (the first in March 1850); Tishrei cycles in AM 5611 + 3k (the
     first in September 1850).
   * ``length="3.5"``: two cycles in each seven-year sabbatical (shemittah) cycle, after
     Naeh's proposal that the Torah was completed twice in seven years: one cycle begins
     on the first ordinary Shabbat on or after 1 Tishrei of the first year of the
     shemittah cycle (AM year % 7 == 1, e.g. 5783), the other on or after 1 Nisan of the
     fourth year (e.g. 5786).  ``start`` is ignored.
   Within a window with n ordinary Shabbatot and N sedarim: if n >= N the sedarim are read
   one per Shabbat and any Shabbatot left at the end of the window have no seder ("cycle
   complete"); if n < N the last N - n ordinary Shabbatot of the window read two
   consecutive sedarim each, so that every cycle is completed before the next begins.
6. Haftarot: none are given (``haftarah`` is always []).  The source used for the sedarim
   (MAM) gives no triennial haftarot, and the reconstructed lists of triennial haftarot
   were not available under an open licence.

Sources
-------
* Seder divisions: "Miqra according to the Masorah", Hebrew Wikisource,
  https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah, CC BY-SA 4.0;
  parsed edition B. Denckla, github.com/bdenckla/MAM-basics, MAM-parsed/plus (commit
  2a108647c4b17e587a00549eb9fa8de8958e0e3e).
* Mishnah Megillah 3:4-6 (four special Shabbatot; festival readings).
* A. Buechler, "The Reading of the Law and Prophets in a Triennial Cycle," Jewish
  Quarterly Review (old series) 5 (1893) 420-468 and 6 (1894) 1-73: a cycle begun on 1 Nisan.
* J. Mann, The Bible as Read and Preached in the Old Synagogue, vol. 1 (Cincinnati, 1940).
* J. Heinemann, "The Triennial Lectionary Cycle," Journal of Jewish Studies 19 (1968)
  41-48.
* S. Naeh, Tarbiz 67 (1997/98): the Torah completed twice in seven years.
* J. Jacobs, "Triennial Cycle," Jewish Encyclopedia (1906): 154 sedarim; Buechler's
  Nisan start; the possibility of a 3 1/2-year cycle.
* L. E. Moses, "Is there an Authentic Triennial Cycle of Torah Readings?" (Committee on
  Jewish Law and Standards of the Rabbinical Assembly, 1986-1990): the cycle was
  interrupted for the four special readings of Adar.

Uncertainties
-------------
There is no surviving calendar of the ancient cycle.  Scholars disagree on whether it
lasted three years or about three and a half (two cycles per shemittah), whether it began
in Nisan, in Tishrei or at no fixed date (Heinemann argued that practice was not uniform),
how many sedarim were used (141, 154 and 167 are all attested), how festivals and the
special Shabbatot interrupted it, and on which Shabbat any particular cycle began.  The
results are therefore an illustration of how such a cycle runs on an astronomical
calendar, not a record of what was read on a given date.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
from functools import lru_cache

import fixed_calendar as fc

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(_HERE, "data", "readings", "triennial_sedarim.json")
NISAN, TISHREI, SIVAN = 1, 7, 3

_FESTIVAL_OF = {  # holiday names used by observed/pretemple calendars -> festival_readings key
    "Rosh Hashanah": "Rosh Hashanah", "Rosh Hashanah I": "Rosh Hashanah", "Rosh Hashanah II": "Rosh Hashanah",
    "Yom Kippur": "Yom Kippur", "Sukkot I": "Sukkot I", "Hoshana Rabbah": "Sukkot Chol HaMoed",
    "Shemini Atzeret": "Shemini Atzeret", "Pesach I": "Pesach", "Pesach VII": "Pesach", "Shavuot": "Shavuot",
}
_FEST_EN = {"Pesach": "Shabbat during Pesach", "Shavuot": "Shavuot", "Rosh Hashanah": "Rosh Hashanah",
            "Yom Kippur": "Yom Kippur", "Sukkot I": "Sukkot I", "Sukkot Chol HaMoed": "Shabbat Chol HaMoed Sukkot",
            "Shemini Atzeret": "Shemini Atzeret"}


@lru_cache(maxsize=1)
def _data() -> dict:
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def sedarim(division: str = "accepted") -> list[dict]:
    return _data()["divisions"][division]


@lru_cache(maxsize=1)
def _default_cal():
    import observed_calendar
    return observed_calendar.ObservedCalendar()


def _sat_on_or_after(d: _dt.date) -> _dt.date:
    return d + _dt.timedelta((5 - d.weekday()) % 7)


def _sat_on_or_before(d: _dt.date) -> _dt.date:
    return d - _dt.timedelta((d.weekday() - 5) % 7)


class _CalInfo:
    """Classification of every Shabbat in a calendar's range (cached per calendar object)."""

    def __init__(self, cal):
        self.cal = cal
        years = list(cal.years() if callable(cal.years) else cal.years)
        self.first = cal.first_day() if callable(cal.first_day) else cal.first_day
        self.last = cal.last_day() if callable(cal.last_day) else cal.last_day
        self.fest: dict[_dt.date, tuple[str, str]] = {}    # date -> (festival key, calendar holiday name)
        self.four: dict[_dt.date, str] = {}
        self.labels: dict[_dt.date, list[str]] = {}
        for y in [years[0] - 1] + years + [years[-1] + 1]:
            try:
                hols = cal.holidays_for_year(y)
            except Exception:
                continue
            for h in hols:
                name = h.name
                key = _FESTIVAL_OF.get(name)
                if key is None and name.startswith("Pesach ") and "Chol HaMoed" in name:
                    key = "Pesach"
                if key is None and name.startswith("Sukkot ") and "Chol HaMoed" in name:
                    key = "Sukkot Chol HaMoed"
                if key and h.kind in ("major", "chol"):
                    self.fest[h.date] = (key, name)
                elif h.kind == "rosh_chodesh" or name.startswith(("Chanukah", "Purim", "Shushan Purim")):
                    self.labels.setdefault(h.date, []).append(name)
            self._four(y)

    def _g(self, y, m, d):
        try:
            return self.cal.to_gregorian(y, m, d)
        except Exception:
            return None

    def _four(self, y):
        try:
            months = [m.month for m in self.cal.year_months(y)]
        except Exception:
            return
        adar = 13 if 13 in months else 12
        a1, a13, n1 = self._g(y, adar, 1), self._g(y, adar, 13), self._g(y, NISAN, 1)
        if not (a1 and a13 and n1):
            return
        hach = _sat_on_or_before(n1)
        for dd, nm in ((_sat_on_or_before(a1), "Shabbat Shekalim"), (_sat_on_or_before(a13), "Shabbat Zachor"),
                       (hach - _dt.timedelta(7), "Shabbat Parah"), (hach, "Shabbat HaChodesh")):
            self.four[dd] = nm

    def ordinary(self, d: _dt.date) -> bool:
        return d not in self.fest and d not in self.four


_INFO: dict[int, tuple[object, _CalInfo]] = {}


def _info(cal) -> _CalInfo:
    k = id(cal)
    if k not in _INFO or _INFO[k][0] is not cal:
        _INFO[k] = (cal, _CalInfo(cal))
    return _INFO[k][1]


def _first_ordinary_on_or_after(info: _CalInfo, d: _dt.date) -> _dt.date:
    s = _sat_on_or_after(d)
    while not info.ordinary(s):
        s += _dt.timedelta(7)
    return s


def _cycle_starts(info: _CalInfo, start: str, length: str) -> list[_dt.date]:
    cal = info.cal
    out = []
    for y in range(5600, 5920):
        if length == "3.5":
            if y % 7 == 1:
                g = info._g(y, TISHREI, 1)
            elif y % 7 == 4:
                g = info._g(y, NISAN, 1)
            else:
                continue
        elif start == "tishrei":
            if (y - 5611) % 3:
                continue
            g = info._g(y, TISHREI, 1)
        else:
            if (y - 5610) % 3:
                continue
            g = info._g(y, NISAN, 1)
        if g is not None and info.first <= g <= info.last:
            out.append(_first_ordinary_on_or_after(info, g))
    return sorted(out)


@lru_cache(maxsize=64)
def _window_plan(cal_id: int, start: str, length: str, division: str, w0: _dt.date, w1: _dt.date,
                 truncated: bool = False):
    """Assignments for the ordinary Shabbatot in [w0, w1): {date: [seder indices]}.
    ``truncated``: the window is cut off by the end of the calendar's data, so no end-of-cycle
    compression is applied (one seder per Shabbat)."""
    info = _INFO[cal_id][1]
    slots = []
    s = w0
    while s < w1:
        if info.ordinary(s):
            slots.append(s)
        s += _dt.timedelta(7)
    N, n = len(sedarim(division)), len(slots)
    plan = {}
    if n >= N or truncated:
        for i, s in enumerate(slots):
            plan[s] = [i] if i < N else []
    else:
        doubles = N - n
        idx = 0
        for i, s in enumerate(slots):
            k = 2 if i >= n - doubles else 1
            plan[s] = list(range(idx, idx + k))
            idx += k
    return plan, n, N


def cycle_window(d: _dt.date, cal=None, start: str = "nisan", length: str = "3", division: str = "accepted"):
    """(window start, next window start, ordinary Shabbatot n, sedarim N) for date d, or None."""
    cal = cal or _default_cal()
    info = _info(cal)
    starts = _cycle_starts(info, start, length)
    prev = [s for s in starts if s <= d]
    nxt = [s for s in starts if s > d]
    if not prev:
        return None
    w0 = prev[-1]
    w1 = nxt[0] if nxt else info.last + _dt.timedelta(1)
    plan, n, N = _window_plan(id(cal), start, length, division, w0, w1, not nxt)
    return w0, w1, n, N, not nxt


def _rng(book, frm, to):
    return {"book": book, "from": frm, "to": to}


def reading_for_shabbat(d: _dt.date, cal=None, start: str = "nisan", length: str = "3",
                        division: str = "accepted", **opts) -> dict | None:
    """Triennial-cycle reading for the Shabbat ``d`` under the stated model (see module docstring)."""
    if d.weekday() != 5:
        return None
    cal = cal or _default_cal()
    if not cal.covers(d):
        return None
    info = _info(cal)
    win = cycle_window(d, cal, start, length, division)
    if win is None:
        return None
    w0, w1, n, N, truncated = win
    plan, _, _ = _window_plan(id(cal), start, length, division, w0, w1, truncated)
    labels = list(info.labels.get(d, []))
    data = _data()
    lenword = "about three and a half years (two cycles per sabbatical cycle)" if length == "3.5" else "three years"
    startword = "" if length == "3.5" else (" beginning in Tishrei" if start == "tishrei" else " beginning in Nisan")
    base_note = (f"Model: reconstructed Land-of-Israel triennial cycle ({N} Masoretic sedarim, one per Shabbat, "
                 f"cycle of {lenword}{startword}); the length, starting month and festival rules of the ancient cycle "
                 f"are disputed, so this shows how such a cycle would run, not a record of what was read.")
    out = {"date": d.isoformat(), "tradition": "triennial", "torah": [], "maftir": [], "haftarah": [],
           "text": "mt", "model": True}
    if d in info.fest:
        key, hname = info.fest[d]
        fr = data["festival_readings"][key]
        out.update(name_en=_FEST_EN[key], name_he=fr["he"], torah=[_rng(*t) for t in fr["torah"]],
                   special="; ".join([hname] + labels),
                   note="Festival reading after Mishnah Megillah 3:5 (verse extent is the model's); the cycle does not advance. "
                        + base_note)
        return out
    if d in info.four:
        nm = info.four[d]
        fr = data["four_parshiyot"][nm]
        out.update(name_en=nm, name_he=fr["he"], torah=[_rng(*t) for t in fr["torah"]],
                   special="; ".join([nm] + labels),
                   note="Special reading replaces the seder (Mishnah Megillah 3:4); the cycle does not advance. "
                        + base_note)
        return out
    idx = plan.get(d, [])
    seds = sedarim(division)
    if not idx:
        nxt = ("after the end of the calendar's data" if truncated else f"on {w1.isoformat()}")
        out.update(name_en="Cycle complete", name_he="סוף המחזור", special="; ".join(labels),
                   note=f"All sedarim of this cycle have been read; in this model the next cycle begins {nxt}. "
                        + base_note)
        return out
    ss = [seds[i] for i in idx]
    out["torah"] = [_rng(s["book"], s["from"], s["to"]) for s in ss]
    if len(ss) > 1 and ss[0]["book"] == ss[1]["book"]:
        out["torah"] = [_rng(ss[0]["book"], ss[0]["from"], ss[-1]["to"])]
    nums = [s["n"] for s in ss]
    lab = f"Seder {nums[0]}" if len(nums) == 1 else f"Sedarim {nums[0]}-{nums[-1]}"
    out["name_en"] = f"{lab} of {N} ({ss[0]['book']} {ss[0]['from']})"
    out["name_he"] = " / ".join(f"סדר {fc.hebrew_numeral(s['n'])}: {s['incipit_he']}" for s in ss)
    extra = []
    if idx[0] == 0:
        extra.append("Start of a new cycle")
    if idx[-1] == len(seds) - 1:
        extra.append("End of the cycle")
    if len(ss) > 1:
        extra.append("Two sedarim read together (model: end-of-cycle catch-up)")
    out["special"] = "; ".join(extra + labels)
    out["note"] = base_note + " No triennial haftarah is given (none in the source used)."
    return out
