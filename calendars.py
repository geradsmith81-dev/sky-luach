"""One interface for the two calendars, used by the pages."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import fixed_calendar as fc
import hebrew_names as hn
import observed_calendar as oc
import pretemple_calendar as ptc
from fixed_calendar import HDate, Holiday

FIXED = "Fixed (rabbinic)"
OBSERVED = "Observed (sighting)"
PRETEMPLE = "Early Temple Period"
ALL = [FIXED, OBSERVED, PRETEMPLE]
KIND_HE = {FIXED: "הלוח הקבוע", OBSERVED: "קידוש החודש על פי הראייה", PRETEMPLE: "לוח תקופת המקדש הקדומה"}


@dataclass
class MonthInfo:
    year: int
    month: int
    name: str
    name_he: str
    start: date
    length: int
    leap_year: bool
    note: str = ""          # how the month began

    @property
    def end(self) -> date:
        return self.start + timedelta(days=self.length - 1)

    @property
    def title(self) -> str:
        return f"{self.name} {self.year}"


class FixedView:
    kind = FIXED
    short = "Fixed"

    def __init__(self, israel: bool, modern: bool, omer: bool):
        self.israel, self.modern, self.omer = israel, modern, omer

    def covers(self, d: date) -> bool:
        return date(1850, 1, 1) <= d <= date(2149, 12, 31)

    @property
    def first_day(self):
        return date(1850, 1, 1)

    @property
    def last_day(self):
        return date(2149, 12, 31)

    def hdate(self, d: date) -> HDate | None:
        return fc.from_gregorian(d)

    def month_at(self, d: date) -> MonthInfo:
        h = fc.from_gregorian(d)
        start = fc.to_gregorian(h.year, h.month, 1)
        return MonthInfo(h.year, h.month, fc.month_name(h.month, h.year), fc.month_name(h.month, h.year, True),
                         start, fc.last_day_of_month(h.month, h.year), fc.is_leap(h.year))

    def year_months(self, year: int) -> list[MonthInfo]:
        return [self.month_at(fc.to_gregorian(year, m, 1)) for m in fc.year_months(year)]

    def is_leap(self, year: int) -> bool:
        return fc.is_leap(year)

    def year_of(self, d: date) -> int:
        return fc.from_gregorian(d).year

    def holidays_for_year(self, year: int, rosh_chodesh=True, special=True) -> list[Holiday]:
        return fc.holidays_for_year(year, israel=self.israel, modern=self.modern,
                                    special_shabbatot=special, rosh_chodesh=rosh_chodesh, omer=self.omer)

    def holidays_between(self, start: date, end: date, rosh_chodesh=True, special=True) -> list[Holiday]:
        return fc.holidays_between(start, end, israel=self.israel, modern=self.modern,
                                   special_shabbatot=special, rosh_chodesh=rosh_chodesh, omer=self.omer)

    def parsha(self, d: date) -> tuple[str, str] | None:
        """(English, Hebrew) names of the weekly portion; None if not Shabbat; ('', '') on a festival."""
        if d.weekday() != fc.SHABBAT:
            return None
        idx = fc.parshiyot_for_year(fc.from_gregorian(d).year, self.israel).get(d.toordinal(), [])
        return "-".join(fc.PARSHIYOT[i] for i in idx), hn.parsha_he(idx)

    def years(self) -> list[int]:
        return list(range(fc.from_gregorian(self.first_day).year + 1, fc.from_gregorian(self.last_day).year))


class ObservedView:
    kind = OBSERVED
    short = "Observed"

    def __init__(self, criterion: str, equinox: str, nisan_day: int, omer: bool):
        self.cal = oc.ObservedCalendar(criterion, equinox, nisan_day)
        self.omer = omer
        self.israel = True

    def covers(self, d: date) -> bool:
        return self.cal.covers(d)

    @property
    def first_day(self):
        return self.cal.first_day

    @property
    def last_day(self):
        return self.cal.last_day

    def hdate(self, d: date) -> HDate | None:
        return self.cal.from_gregorian(d)

    def _info(self, m: oc.ObsMonth) -> MonthInfo:
        if m.sighting_evening is not None and m.q is not None:
            note = (f"Crescent predicted visible from Jerusalem on the evening of "
                    f"{m.sighting_evening:%a %d %b %Y} (Yallop q = {m.q:+.3f}, zone {m.yallop})")
        elif m.sighting_evening is not None:
            note = f"Crescent predicted visible from Jerusalem on the evening of {m.sighting_evening:%a %d %b %Y}"
        else:
            qtxt = f" (q = {m.q:+.3f}, zone {m.yallop})" if m.q is not None else ""
            note = ("Crescent not visible on the evening ending day 29" + qtxt +
                    ", so the previous month was completed to 30 days")
        he = fc.MONTH_NAMES_HE[m.month]
        if m.month == fc.ADAR and self.cal.is_leap(m.year):
            he = "אדר א׳"
        return MonthInfo(m.year, m.month, self.cal.month_label(m.year, m.month), he, m.start, m.length,
                         self.cal.is_leap(m.year), note)

    def month_at(self, d: date) -> MonthInfo | None:
        m = self.cal.month_of(d)
        return self._info(m) if m else None

    def year_months(self, year: int) -> list[MonthInfo]:
        return [self._info(m) for m in self.cal.year_months(year)]

    def is_leap(self, year: int) -> bool:
        return self.cal.is_leap(year)

    def year_of(self, d: date) -> int | None:
        h = self.cal.from_gregorian(d)
        return h.year if h else None

    def holidays_for_year(self, year: int, rosh_chodesh=True, special=True) -> list[Holiday]:
        return self.cal.holidays_for_year(year, rosh_chodesh=rosh_chodesh, omer=self.omer)

    def holidays_between(self, start: date, end: date, rosh_chodesh=True, special=True) -> list[Holiday]:
        return self.cal.holidays_between(start, end, rosh_chodesh=rosh_chodesh, omer=self.omer)

    def parsha(self, d: date):
        return None   # the annual reading cycle belongs to the fixed calendar

    def years(self) -> list[int]:
        return self.cal.years()


class PreTempleView(ObservedView):
    kind = PRETEMPLE
    short = "Early Temple"

    def __init__(self, rule: str, equinox: str, nisan_day: int, omer: bool):
        self.cal = ptc.PreTempleCalendar(rule, equinox, nisan_day)
        self.omer = omer
        self.israel = True

    def _info(self, m):
        info = super()._info(m)
        conj = m.conj_utc
        ss = self.cal.sunset_of_start.get(m.start)
        info.note = (f"True new moon (JPL DE440s) {conj:%a %d %b %Y, %H:%M} UT; day 1 began at the Jerusalem sunset of "
                     f"{(ss.date() if ss else m.start - timedelta(days=1)):%a %d %b %Y}"
                     + (f" ({ss:%H:%M} UT)" if ss else ""))
        return info


# ----------------------------------------------------------------------------------------------
def to_ics(holidays: list[Holiday], calname: str) -> str:
    """All-day iCalendar events (the Hebrew day starts the evening before; noted in each event)."""
    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace(";", r"\;").replace(",", r"\,").replace("\n", r"\n")

    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Sky Luach//Jewish calendar//EN",
             "CALSCALE:GREGORIAN", f"X-WR-CALNAME:{esc(calname)}"]
    stamp = date.today().strftime("%Y%m%dT000000Z")
    for h in holidays:
        slug = "".join(c for c in h.name.lower() if c.isalnum())[:40]
        desc = f"{h.hdate} ({calname})" if h.hdate else calname
        if h.begins_evening_before and h.kind not in ("erev",):
            desc += ". Begins at sunset the evening before."
        if h.note:
            desc += f" {h.note}."
        lines += ["BEGIN:VEVENT",
                  f"UID:{h.date:%Y%m%d}-{slug}-{'obs' if 'Observed' in calname else 'fix'}@sky-luach",
                  f"DTSTAMP:{stamp}",
                  f"DTSTART;VALUE=DATE:{h.date:%Y%m%d}",
                  f"DTEND;VALUE=DATE:{(h.date + timedelta(days=1)):%Y%m%d}",
                  f"SUMMARY:{esc(h.name)}",
                  f"DESCRIPTION:{esc(desc)}",
                  "TRANSP:TRANSPARENT", "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"
