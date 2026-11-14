"""
The fixed (rabbinic, "Hillel II") Hebrew calendar.

Pure arithmetic, no astronomy: mean lunar month (molad) of 29 d 12 h 793 parts, the 19-year
cycle of leap years, and the four postponement rules (dehiyyot). The arithmetic follows
E. M. Reingold & N. Dershowitz, *Calendrical Calculations* (Cambridge UP), using "fixed day
numbers" (RD), which are the same as Python's date.toordinal().

Months are numbered as in the Torah and in Calendrical Calculations:
Nisan=1 ... Elul=6, Tishrei=7 ... Shevat=11, Adar (Adar I in a leap year)=12, Adar II=13.
The year number changes on 1 Tishrei.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from functools import lru_cache
import math

NISAN, IYYAR, SIVAN, TAMMUZ, AV, ELUL = 1, 2, 3, 4, 5, 6
TISHREI, MARHESHVAN, KISLEV, TEVET, SHEVAT, ADAR, ADAR_II = 7, 8, 9, 10, 11, 12, 13

HEBREW_EPOCH = -1373427  # RD of 1 Tishrei AM 1 (Julian 7 Oct 3761 BCE)
PARTS_PER_DAY = 25920      # 24 h x 1080 parts
LUNATION_PARTS = 765433    # 29 d 12 h 793 p
MONTH_DAYS = LUNATION_PARTS / PARTS_PER_DAY  # 29.530594 days

MONTH_NAMES = {
    NISAN: "Nisan", IYYAR: "Iyyar", SIVAN: "Sivan", TAMMUZ: "Tammuz", AV: "Av", ELUL: "Elul",
    TISHREI: "Tishrei", MARHESHVAN: "Cheshvan", KISLEV: "Kislev", TEVET: "Tevet",
    SHEVAT: "Shevat", ADAR: "Adar", ADAR_II: "Adar II",
}
MONTH_NAMES_HE = {
    NISAN: "ניסן", IYYAR: "אייר", SIVAN: "סיון", TAMMUZ: "תמוז", AV: "אב", ELUL: "אלול",
    TISHREI: "תשרי", MARHESHVAN: "חשון", KISLEV: "כסלו", TEVET: "טבת", SHEVAT: "שבט",
    ADAR: "אדר", ADAR_II: "אדר ב׳",
}
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Shabbat", "Sunday"]  # date.weekday()


def month_name(m: int, year: int | None = None, hebrew: bool = False) -> str:
    """Adar is called 'Adar I' in a leap year."""
    if m == ADAR and year is not None and is_leap(year):
        return "אדר א׳" if hebrew else "Adar I"
    return (MONTH_NAMES_HE if hebrew else MONTH_NAMES)[m]


# ----------------------------------------------------------------------------------------------
# core arithmetic
# ----------------------------------------------------------------------------------------------
def is_leap(year: int) -> bool:
    """Years 3, 6, 8, 11, 14, 17 and 19 of each 19-year cycle have 13 months."""
    return (7 * year + 1) % 19 < 7


def last_month_of_year(year: int) -> int:
    return ADAR_II if is_leap(year) else ADAR


def months_elapsed(year: int) -> int:
    """Lunations from the molad of creation (BaHaRaD) to the molad of Tishrei of `year`."""
    return (235 * year - 234) // 19


def molad_parts(month: int, year: int) -> int:
    """Molad of a month in parts (1/1080 hour) counted from midnight beginning RD 0,
    in Jerusalem local mean time. BaHaRaD = Sunday 11:11:20 pm (5 h 204 p after 6 pm)."""
    y = year + 1 if month < TISHREI else year
    elapsed = month - TISHREI + months_elapsed(y)
    return HEBREW_EPOCH * PARTS_PER_DAY - 876 + elapsed * LUNATION_PARTS


def molad(month: int, year: int) -> float:
    """Molad as a fractional RD moment (Jerusalem local mean time, day begins at midnight)."""
    return molad_parts(month, year) / PARTS_PER_DAY


def molad_traditional(month: int, year: int) -> dict:
    """Molad in the traditional notation: weekday, hours counted from 6 pm, parts."""
    p = molad_parts(month, year) + 6 * 1080  # shift so that the 'day' starts at 6 pm
    day, rem = divmod(p, PARTS_PER_DAY)
    hours, parts = divmod(rem, 1080)
    wd = date.fromordinal(int(day)).weekday()
    return {"weekday": WEEKDAYS[wd], "hours_from_6pm": hours, "parts": parts,
            "minutes": parts // 18, "rem_parts": parts % 18}


def _elapsed_days(year: int) -> int:
    """Days from the epoch to 1 Tishrei before the year-length corrections
    (includes molad zaken and lo ADU rosh)."""
    me = months_elapsed(year)
    parts_elapsed = 12084 + 13753 * me
    days = 29 * me + parts_elapsed // 25920
    return days + 1 if (3 * (days + 1)) % 7 < 3 else days


@lru_cache(maxsize=None)
def _year_length_correction(year: int) -> int:
    """GaTaRaD and BeTU'TaKPaT: keep year lengths in {353,354,355,383,384,385}."""
    ny0, ny1, ny2 = _elapsed_days(year - 1), _elapsed_days(year), _elapsed_days(year + 1)
    if ny2 - ny1 == 356:
        return 2
    if ny1 - ny0 == 382:
        return 1
    return 0


@lru_cache(maxsize=None)
def new_year(year: int) -> int:
    """RD of 1 Tishrei of `year`."""
    return HEBREW_EPOCH + _elapsed_days(year) + _year_length_correction(year)


def days_in_year(year: int) -> int:
    return new_year(year + 1) - new_year(year)


def long_marheshvan(year: int) -> bool:
    return days_in_year(year) in (355, 385)


def short_kislev(year: int) -> bool:
    return days_in_year(year) in (353, 383)


def last_day_of_month(month: int, year: int) -> int:
    if month in (IYYAR, TAMMUZ, ELUL, TEVET, ADAR_II):
        return 29
    if month == ADAR and not is_leap(year):
        return 29
    if month == MARHESHVAN and not long_marheshvan(year):
        return 29
    if month == KISLEV and short_kislev(year):
        return 29
    return 30


def year_months(year: int) -> list[int]:
    """Months of a Hebrew year in calendar order (Tishrei first)."""
    return list(range(TISHREI, last_month_of_year(year) + 1)) + list(range(NISAN, TISHREI))


@lru_cache(maxsize=None)
def _month_start(year: int, month: int) -> int:
    rd = new_year(year)
    for m in year_months(year):
        if m == month:
            return rd
        rd += last_day_of_month(m, year)
    raise ValueError(f"month {month} not in year {year}")


def to_rd(year: int, month: int, day: int) -> int:
    return _month_start(year, month) + day - 1


def to_gregorian(year: int, month: int, day: int) -> date:
    return date.fromordinal(to_rd(year, month, day))


@dataclass(frozen=True)
class HDate:
    year: int
    month: int
    day: int
    leap: bool | None = None   # set by the observational calendar; None = fixed-calendar rule

    def _is_leap(self) -> bool:
        return is_leap(self.year) if self.leap is None else self.leap

    @property
    def month_name(self) -> str:
        if self.month == ADAR and self._is_leap():
            return "Adar I"
        return MONTH_NAMES[self.month]

    @property
    def month_name_he(self) -> str:
        if self.month == ADAR and self._is_leap():
            return "אדר א׳"
        return MONTH_NAMES_HE[self.month]

    def __str__(self) -> str:
        return f"{self.day} {self.month_name} {self.year}"

    def hebrew(self) -> str:
        return f"{hebrew_numeral(self.day)} {self.month_name_he} {hebrew_numeral(self.year % 1000)}"


def from_rd(rd: int) -> HDate:
    approx = math.floor((rd - HEBREW_EPOCH) / (35975351 / 98496)) + 1
    year = approx - 1
    while new_year(year + 1) <= rd:
        year += 1
    month = TISHREI if rd < to_rd(year, NISAN, 1) else NISAN
    while rd > to_rd(year, month, last_day_of_month(month, year)):
        month += 1
    return HDate(year, month, rd - to_rd(year, month, 1) + 1)


def from_gregorian(d: date) -> HDate:
    return from_rd(d.toordinal())


def year_type(year: int) -> dict:
    """Keviah: weekday of Rosh Hashanah, length class and weekday of the first day of Pesach."""
    n = days_in_year(year)
    kind = {353: "deficient", 354: "regular", 355: "complete",
            383: "deficient", 384: "regular", 385: "complete"}[n]
    rh = date.fromordinal(new_year(year)).weekday()
    pesach = to_gregorian(year, NISAN, 15).weekday()
    return {"days": n, "leap": is_leap(year), "kind": kind,
            "rosh_hashanah_weekday": WEEKDAYS[rh], "pesach_weekday": WEEKDAYS[pesach]}


# ----------------------------------------------------------------------------------------------
# traditional cycles
# ----------------------------------------------------------------------------------------------
def metonic_position(year: int) -> dict:
    """Machzor katan: 19-year cycle number and the year's place in it."""
    cycle, pos = divmod(year - 1, 19)
    return {"cycle": cycle + 1, "year_in_cycle": pos + 1, "leap": is_leap(year),
            "leap_years_in_cycle": [3, 6, 8, 11, 14, 17, 19]}


def shmita_position(year: int) -> dict:
    """Sabbatical cycle in the standard modern reckoning: AM years divisible by 7 are shmita
    years (e.g. 5775, 5782, 5789)."""
    pos = year % 7 or 7
    return {"year_in_cycle": pos, "is_shmita": pos == 7,
            "next_shmita": year + (7 - pos) if pos != 7 else year}


# Molad of Nisan of AM 1 (year 1 is not a leap year: Tishrei + 6 lunations).
def _molad_nisan_year1_parts() -> int:
    return molad_parts(NISAN, 1)


TEKUFAH_SHMUEL_YEAR_PARTS = 365 * PARTS_PER_DAY + 6 * 1080  # 365.25 days
TEKUFAH_ADDA_YEAR_PARTS = 235 * LUNATION_PARTS // 19         # 365 d 5 h 997 p 48 m (exact /19)


def tekufah_shmuel(year_of_nisan: int, season: int = 0) -> float:
    """Tekufah of Shmuel (Rambam, Kiddush HaChodesh 9:3): the first tekufat Nisan was
    7 d 9 h 642 p before the molad of Nisan of year 1; each year is 365 1/4 days, each season
    91 d 7 1/2 h. `year_of_nisan` is the Hebrew year whose Nisan the tekufah precedes/falls in;
    season 0=Nisan (spring), 1=Tammuz, 2=Tishrei, 3=Tevet (of the following Gregorian winter).
    Returns a fractional RD moment, Jerusalem local mean time."""
    first = _molad_nisan_year1_parts() - (7 * PARTS_PER_DAY + 9 * 1080 + 642)
    p = first + (year_of_nisan - 1) * TEKUFAH_SHMUEL_YEAR_PARTS + season * TEKUFAH_SHMUEL_YEAR_PARTS // 4
    return p / PARTS_PER_DAY


def tekufah_adda(year_of_nisan: int, season: int = 0) -> float:
    """Tekufah of Rav Adda (Rambam, Kiddush HaChodesh 10:3): the first tekufat Nisan was
    9 h 642 p before the molad of Nisan of year 1; year = 235/19 mean months."""
    first = _molad_nisan_year1_parts() - (9 * 1080 + 642)
    p = first + (year_of_nisan - 1) * TEKUFAH_ADDA_YEAR_PARTS + season * TEKUFAH_ADDA_YEAR_PARTS / 4
    return p / PARTS_PER_DAY


def birkat_hachamah_years(start_greg: int, end_greg: int) -> list[date]:
    """Birkat HaChamah: when tekufat Nisan of Shmuel falls at 6 pm (start of a Wednesday);
    this happens every 28 years (machzor gadol). Returns the Wednesday morning of the blessing."""
    out = []
    for hy in range(start_greg + 3760 - 1, end_greg + 3761 + 1):
        t = tekufah_shmuel(hy)
        local = t + 0.25  # shift: day starts at 6 pm
        day = math.floor(local + 1e-9)
        frac = local - day
        if abs(frac) < 1e-6 and date.fromordinal(day).weekday() == 2:
            d = date.fromordinal(day)
            if start_greg <= d.year <= end_greg:
                out.append(d)
    return out


def solar_cycle_position(year: int) -> dict:
    """Machzor gadol (28-year solar cycle) counted so that Birkat HaChamah falls in year 1."""
    pos = (year - 1) % 28 + 1  # AM 5769 (2009) -> (5768 % 28) + 1 = 1
    return {"year_in_cycle": pos, "machzor_gadol": (year - 1) // 28 + 1}


# ----------------------------------------------------------------------------------------------
# holidays
# ----------------------------------------------------------------------------------------------
@dataclass
class Holiday:
    date: date
    name: str
    hebrew: str
    kind: str          # 'major' (work forbidden), 'minor', 'fast', 'chol', 'rosh_chodesh', 'modern',
                       # 'special_shabbat', 'erev', 'omer'
    hdate: HDate | None = None
    note: str = ""
    begins_evening_before: bool = True

    def as_dict(self) -> dict:
        return {"date": self.date, "name": self.name, "hebrew": self.hebrew, "kind": self.kind,
                "hebrew_date": str(self.hdate) if self.hdate else "", "note": self.note}


SHABBAT = 5  # date.weekday() of Saturday
FRIDAY, THURSDAY, SUNDAY, MONDAY = 4, 3, 6, 0


def _h(year, month, day, name, he, kind, note="", evening=True) -> Holiday:
    g = to_gregorian(year, month, day)
    return Holiday(g, name, he, kind, HDate(year, month, day), note, evening)


def holidays_for_year(year: int, israel: bool = False, modern: bool = True,
                      special_shabbatot: bool = True, rosh_chodesh: bool = True,
                      omer: bool = False, sigd: bool = False, one_day_rh: bool = False) -> list[Holiday]:
    """All holidays from 1 Tishrei to 29 Elul of Hebrew `year`.

    sigd: add the Beta Israel festival of Sigd (29 Marcheshvan; Thursday 27 Marcheshvan when the 29th is
          Shabbat, as observed in Israel).
    one_day_rh: Rosh Hashanah of one day only (the Reform custom; use with israel=True for the
          'one day everywhere' scheme).
    """
    H: list[Holiday] = []
    add = H.append
    adar = ADAR_II if is_leap(year) else ADAR

    # --- Tishrei
    add(_h(year - 1, ELUL, 29, "Erev Rosh Hashanah", "ערב ראש השנה", "erev", evening=False))
    if one_day_rh:
        add(_h(year, TISHREI, 1, "Rosh Hashanah", "ראש השנה", "major", "one day (Reform custom)"))
    else:
        add(_h(year, TISHREI, 1, "Rosh Hashanah I", "ראש השנה א׳", "major"))
        add(_h(year, TISHREI, 2, "Rosh Hashanah II", "ראש השנה ב׳", "major"))
    g = 3 if to_gregorian(year, TISHREI, 3).weekday() != SHABBAT else 4
    add(_h(year, TISHREI, g, "Tzom Gedaliah", "צום גדליה", "fast",
           "postponed from Shabbat" if g == 4 else "", evening=False))
    add(_h(year, TISHREI, 9, "Erev Yom Kippur", "ערב יום כיפור", "erev", evening=False))
    add(_h(year, TISHREI, 10, "Yom Kippur", "יום כיפור", "major"))
    add(_h(year, TISHREI, 14, "Erev Sukkot", "ערב סוכות", "erev", evening=False))
    add(_h(year, TISHREI, 15, "Sukkot I", "סוכות א׳", "major"))
    if israel:
        for d in range(16, 21):
            add(_h(year, TISHREI, d, f"Sukkot {d - 14} (Chol HaMoed)", "חול המועד סוכות", "chol"))
    else:
        add(_h(year, TISHREI, 16, "Sukkot II", "סוכות ב׳", "major"))
        for d in range(17, 21):
            add(_h(year, TISHREI, d, f"Sukkot {d - 14} (Chol HaMoed)", "חול המועד סוכות", "chol"))
    add(_h(year, TISHREI, 21, "Hoshana Rabbah", "הושענא רבה", "chol"))
    if israel:
        add(_h(year, TISHREI, 22, "Shemini Atzeret / Simchat Torah", "שמיני עצרת / שמחת תורה", "major"))
    else:
        add(_h(year, TISHREI, 22, "Shemini Atzeret", "שמיני עצרת", "major"))
        add(_h(year, TISHREI, 23, "Simchat Torah", "שמחת תורה", "major"))

    # --- Marcheshvan: Sigd (Beta Israel), 50 days after Yom Kippur
    if sigd:
        sd = 29 if to_gregorian(year, MARHESHVAN, 29).weekday() != SHABBAT else 27
        add(_h(year, MARHESHVAN, sd, "Sigd", "סיגד", "minor",
               "Beta Israel festival, 50 days after Yom Kippur; an Israeli state holiday since 2008"
               + ("; moved to Thursday (29 Marcheshvan is Shabbat)" if sd == 27 else ""), evening=False))

    # --- Kislev / Tevet: Chanukah, 25 Kislev for 8 days (candles from the evening before)
    for i in range(8):
        rd = to_rd(year, KISLEV, 25) + i
        add(Holiday(date.fromordinal(rd), f"Chanukah: {i + 1} candle{'s' if i else ''} (day {i + 1})",
                    "חנוכה", "minor", from_rd(rd), "candles lit the evening before"))
    add(_h(year, TEVET, 10, "Asara B'Tevet", "עשרה בטבת", "fast", evening=False))

    # --- Shevat / Adar
    add(_h(year, SHEVAT, 15, "Tu BiShvat", "ט״ו בשבט", "minor"))
    if is_leap(year):
        add(_h(year, ADAR, 14, "Purim Katan", "פורים קטן", "minor"))
        add(_h(year, ADAR, 15, "Shushan Purim Katan", "שושן פורים קטן", "minor"))
    e = 13 if to_gregorian(year, adar, 13).weekday() != SHABBAT else 11
    add(_h(year, adar, e, "Ta'anit Esther", "תענית אסתר", "fast",
           "moved to Thursday (13 Adar is Shabbat)" if e == 11 else "", evening=False))
    add(_h(year, adar, 14, "Purim", "פורים", "minor"))
    add(_h(year, adar, 15, "Shushan Purim", "שושן פורים", "minor", "Purim in Jerusalem"))

    # --- Nisan: Pesach
    b = 14 if to_gregorian(year, NISAN, 14).weekday() != SHABBAT else 12
    add(_h(year, NISAN, b, "Ta'anit Bechorot", "תענית בכורות", "fast",
           "moved to Thursday (14 Nisan is Shabbat)" if b == 12 else "", evening=False))
    add(_h(year, NISAN, 14, "Erev Pesach", "ערב פסח", "erev", evening=False))
    add(_h(year, NISAN, 15, "Pesach I", "פסח א׳", "major"))
    if israel:
        for d in range(16, 21):
            add(_h(year, NISAN, d, f"Pesach {d - 14} (Chol HaMoed)", "חול המועד פסח", "chol"))
        add(_h(year, NISAN, 21, "Pesach VII", "שביעי של פסח", "major"))
    else:
        add(_h(year, NISAN, 16, "Pesach II", "פסח ב׳", "major"))
        for d in range(17, 21):
            add(_h(year, NISAN, d, f"Pesach {d - 14} (Chol HaMoed)", "חול המועד פסח", "chol"))
        add(_h(year, NISAN, 21, "Pesach VII", "שביעי של פסח", "major"))
        add(_h(year, NISAN, 22, "Pesach VIII", "אחרון של פסח", "major"))

    # --- Omer, Lag BaOmer, Shavuot
    add(_h(year, IYYAR, 14, "Pesach Sheni", "פסח שני", "minor"))
    add(_h(year, IYYAR, 18, "Lag BaOmer", "ל״ג בעומר", "minor"))
    add(_h(year, SIVAN, 5, "Erev Shavuot", "ערב שבועות", "erev", evening=False))
    add(_h(year, SIVAN, 6, "Shavuot I" if not israel else "Shavuot", "שבועות", "major"))
    if not israel:
        add(_h(year, SIVAN, 7, "Shavuot II", "שבועות ב׳", "major"))
    if omer:
        start = to_rd(year, NISAN, 16)
        for i in range(49):
            add(Holiday(date.fromordinal(start + i), f"Omer day {i + 1}", "ספירת העומר", "omer",
                        from_rd(start + i), "counted the evening before"))

    # --- summer fasts
    t = 17 if to_gregorian(year, TAMMUZ, 17).weekday() != SHABBAT else 18
    add(_h(year, TAMMUZ, t, "Tzom Tammuz (17 Tammuz)", "שבעה עשר בתמוז", "fast",
           "postponed from Shabbat" if t == 18 else "", evening=False))
    a = 9 if to_gregorian(year, AV, 9).weekday() != SHABBAT else 10
    add(_h(year, AV, a, "Tisha B'Av", "תשעה באב", "fast",
           "postponed from Shabbat" if a == 10 else ""))
    add(_h(year, AV, 15, "Tu B'Av", "ט״ו באב", "minor"))

    # --- Rosh Chodesh
    if rosh_chodesh:
        for m in year_months(year):
            if m == TISHREI:
                continue
            prev = m - 1 if m not in (NISAN, TISHREI) else None
            if m == NISAN:
                prev = last_month_of_year(year)
            nm = month_name(m, year)
            if prev is not None and last_day_of_month(prev, year) == 30:
                add(_h(year, prev, 30, f"Rosh Chodesh {nm} (day 1)", f"ראש חודש {month_name(m, year, True)}",
                       "rosh_chodesh"))
                add(_h(year, m, 1, f"Rosh Chodesh {nm} (day 2)", f"ראש חודש {month_name(m, year, True)}",
                       "rosh_chodesh"))
            else:
                add(_h(year, m, 1, f"Rosh Chodesh {nm}", f"ראש חודש {month_name(m, year, True)}", "rosh_chodesh"))

    # --- modern Israeli days (dates as observed in Israel)
    if modern:
        H.extend(modern_days(year))

    # --- special Shabbatot
    if special_shabbatot:
        H.extend(special_shabbatot_for_year(year))

    H.sort(key=lambda h: (h.date, _KIND_ORDER.get(h.kind, 9)))
    return H


_KIND_ORDER = {"major": 0, "fast": 1, "chol": 2, "minor": 3, "modern": 4, "rosh_chodesh": 5,
               "special_shabbat": 6, "erev": 7, "omer": 8}


def modern_days(year: int) -> list[Holiday]:
    """Israeli national days with the Knesset/Chief Rabbinate postponement rules."""
    out = []
    greg = to_gregorian(year, NISAN, 1).year
    # Yom HaShoah 27 Nisan (since 1951): Friday -> Thursday 26; Sunday -> Monday 28 (since 1997)
    if greg >= 1951:
        d = 27
        wd = to_gregorian(year, NISAN, 27).weekday()
        if wd == FRIDAY:
            d = 26
        elif wd == SUNDAY and greg >= 1997:
            d = 28
        out.append(_h(year, NISAN, d, "Yom HaShoah", "יום השואה", "modern", "Holocaust Remembrance Day"))
    # Yom HaZikaron / Yom HaAtzmaut (5 Iyyar, since 1949)
    if greg >= 1949:
        wd5 = to_gregorian(year, IYYAR, 5).weekday()
        if wd5 == FRIDAY:
            atz = 4
        elif wd5 == SHABBAT:
            atz = 3
        elif wd5 == MONDAY and greg >= 2004:
            atz = 6
        else:
            atz = 5
        out.append(_h(year, IYYAR, atz - 1, "Yom HaZikaron", "יום הזיכרון", "modern", "Memorial Day"))
        out.append(_h(year, IYYAR, atz, "Yom HaAtzmaut", "יום העצמאות", "modern", "Independence Day"))
    # Yom Yerushalayim 28 Iyyar (since 1968)
    if greg >= 1968:
        out.append(_h(year, IYYAR, 28, "Yom Yerushalayim", "יום ירושלים", "modern", "Jerusalem Day"))
    return out


def _shabbat_on_or_before(rd: int) -> int:
    return rd - ((date.fromordinal(rd).weekday() - SHABBAT) % 7)


def special_shabbatot_for_year(year: int) -> list[Holiday]:
    out = []
    adar = ADAR_II if is_leap(year) else ADAR

    def add(rd, name, he, note=""):
        out.append(Holiday(date.fromordinal(rd), name, he, "special_shabbat", from_rd(rd), note))

    rh_next = new_year(year + 1)
    add(_shabbat_on_or_before(to_rd(year, TISHREI, 9)), "Shabbat Shuvah", "שבת שובה")
    shekalim = _shabbat_on_or_before(to_rd(year, adar, 1))
    add(shekalim, "Shabbat Shekalim", "שבת שקלים")
    add(_shabbat_on_or_before(to_rd(year, adar, 13)), "Shabbat Zachor", "שבת זכור")
    hachodesh = _shabbat_on_or_before(to_rd(year, NISAN, 1))
    add(hachodesh - 7, "Shabbat Parah", "שבת פרה")
    add(hachodesh, "Shabbat HaChodesh", "שבת החודש")
    add(_shabbat_on_or_before(to_rd(year, NISAN, 14)), "Shabbat HaGadol", "שבת הגדול")
    chazon = _shabbat_on_or_before(to_rd(year, AV, 9))
    add(chazon, "Shabbat Chazon", "שבת חזון")
    add(chazon + 7, "Shabbat Nachamu", "שבת נחמו")
    return [h for h in out if new_year(year) <= h.date.toordinal() < rh_next]


def holidays_between(start: date, end: date, **kw) -> list[Holiday]:
    """Holidays with start <= date <= end."""
    y0 = from_gregorian(start).year
    y1 = from_gregorian(end).year
    out = []
    for y in range(y0, y1 + 1):
        out.extend(h for h in holidays_for_year(y, **kw) if start <= h.date <= end)
    return out


# ----------------------------------------------------------------------------------------------
# weekly Torah portions
# ----------------------------------------------------------------------------------------------
PARSHIYOT = [
    "Bereshit", "Noach", "Lech-Lecha", "Vayera", "Chayei Sara", "Toldot", "Vayetzei", "Vayishlach",
    "Vayeshev", "Miketz", "Vayigash", "Vayechi", "Shemot", "Vaera", "Bo", "Beshalach", "Yitro",
    "Mishpatim", "Terumah", "Tetzaveh", "Ki Tisa", "Vayakhel", "Pekudei", "Vayikra", "Tzav",
    "Shmini", "Tazria", "Metzora", "Achrei Mot", "Kedoshim", "Emor", "Behar", "Bechukotai",
    "Bamidbar", "Nasso", "Beha'alotcha", "Sh'lach", "Korach", "Chukat", "Balak", "Pinchas",
    "Matot", "Masei", "Devarim", "Vaetchanan", "Eikev", "Re'eh", "Shoftim", "Ki Teitzei",
    "Ki Tavo", "Nitzavim", "Vayeilech", "Ha'azinu", "Vezot Haberakhah",
]
P = {name: i for i, name in enumerate(PARSHIYOT)}


def _is_festival_shabbat(rd: int, israel: bool) -> bool:
    """True if a Shabbat falls on a festival or chol hamoed (no weekly portion is read)."""
    h = from_rd(rd)
    m, d = h.month, h.day
    if m == TISHREI and (d in (1, 2, 10) or 15 <= d <= (22 if israel else 23)):
        return True
    if m == NISAN and 15 <= d <= (21 if israel else 22):
        return True
    if m == SIVAN and (d == 6 or (d == 7 and not israel)):
        return True
    return False


def _fill(shabbatot: list[int], first: int, last: int, pairs_priority: list[int]) -> dict[int, list[int]]:
    """Assign portions first..last to the given Shabbatot, combining pairs (each pair given by
    the index of its first portion) in priority order until the count fits."""
    n_read = last - first + 1
    need = n_read - len(shabbatot)
    if need < 0 or need > len(pairs_priority):
        raise ValueError("portion count does not fit")
    combined = set(pairs_priority[:need])
    out, i = {}, first
    for rd in shabbatot:
        if i in combined:
            out[rd] = [i, i + 1]
            i += 2
        else:
            out[rd] = [i]
            i += 1
    assert i == last + 1
    return out


@lru_cache(maxsize=None)
def parshiyot_for_year(year: int, israel: bool = False) -> dict[int, list[int]]:
    """Map RD of each Shabbat in Hebrew `year` -> list of portion indices read on it
    (empty list for festival Shabbatot)."""
    start, end = new_year(year), new_year(year + 1) - 1
    first_sat = _shabbat_on_or_before(start + 6)
    sats = list(range(first_sat, end + 1, 7))
    result = {rd: [] for rd in sats}
    regular = [rd for rd in sats if not _is_festival_shabbat(rd, israel)]

    # Tishrei before Simchat Torah: Vayeilech (if left over from last year) then Ha'azinu
    simchat = to_rd(year, TISHREI, 22 if israel else 23)
    pre = [rd for rd in regular if rd < simchat]
    rh_wd = date.fromordinal(start).weekday()
    portions = ([P["Vayeilech"]] if rh_wd in (MONDAY, 1) else []) + [P["Ha'azinu"]]
    assert len(pre) == len(portions), (year, len(pre), portions)
    for rd, p in zip(pre, portions):
        result[rd] = [p]

    leap = is_leap(year)
    pesach = to_rd(year, NISAN, 15)
    shavuot = to_rd(year, SIVAN, 6)
    tisha = to_rd(year, AV, 9)
    seg_p = [rd for rd in regular if simchat < rd < pesach]
    seg_s = [rd for rd in regular if pesach < rd < shavuot]
    seg_t = [rd for rd in regular if shavuot < rd <= tisha]
    seg_r = [rd for rd in regular if rd > tisha]

    # Bereshit ... before Pesach: Tzav (regular years) / Metzora (leap years) is read last
    anchor = P["Metzora"] if leap else P["Tzav"]
    n_p = anchor - P["Bereshit"] + 1
    if len(seg_p) > n_p:   # an extra Shabbat before Pesach: carry on reading
        anchor += len(seg_p) - n_p
    pri_p = [P["Vayakhel"]] if not leap else []
    result.update(_fill(seg_p, P["Bereshit"], anchor, pri_p))
    # after Pesach ... Bamidbar (normally read on the Shabbat before Shavuot). In leap years only
    # Behar-Bechukotai may be joined. A surplus Shabbat (e.g. in Israel when the diaspora's
    # 8th day of Pesach is a Shabbat) carries the reading on to Nasso before Shavuot.
    pri_s = [P["Behar"]] if leap else [p for p in (P["Tazria"], P["Achrei Mot"], P["Behar"]) if p > anchor]
    last_s = P["Bamidbar"]
    n_s = last_s - anchor
    if len(seg_s) > n_s:
        last_s += len(seg_s) - n_s
    result.update(_fill(seg_s, anchor + 1, last_s, pri_s))
    # after Shavuot ... Devarim (read on the Shabbat on or before 9 Av)
    result.update(_fill(seg_t, last_s + 1, P["Devarim"], [P["Matot"], P["Chukat"]]))
    # after 9 Av ... Nitzavim (+ Vayeilech unless next Rosh Hashanah is Monday or Tuesday)
    next_rh_wd = date.fromordinal(new_year(year + 1)).weekday()
    last = P["Nitzavim"] if next_rh_wd in (MONDAY, 1) else P["Vayeilech"]
    result.update(_fill(seg_r, P["Vaetchanan"], last, [P["Nitzavim"]]))
    return result


def parsha_on(d: date, israel: bool = False) -> str | None:
    """Name of the portion(s) read on the Shabbat `d` (None if not a Shabbat, '' on a festival)."""
    if d.weekday() != SHABBAT:
        return None
    y = from_gregorian(d).year
    idx = parshiyot_for_year(y, israel).get(d.toordinal(), [])
    return "-".join(PARSHIYOT[i] for i in idx)


def upcoming_parsha(d: date, israel: bool = False) -> tuple[date, str]:
    """The next Shabbat on or after d that has a weekly reading."""
    rd = d.toordinal() + ((SHABBAT - d.weekday()) % 7)
    for _ in range(10):
        name = parsha_on(date.fromordinal(rd), israel)
        if name:
            return date.fromordinal(rd), name
        rd += 7
    return date.fromordinal(rd), ""


# ----------------------------------------------------------------------------------------------
# Hebrew numerals
# ----------------------------------------------------------------------------------------------
_ONES = ["", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט"]
_TENS = ["", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ"]
_HUNDREDS = ["", "ק", "ר", "ש", "ת", "תק", "תר", "תש", "תת", "תתק"]


def hebrew_numeral(n: int) -> str:
    """Gematria with geresh/gershayim; 15 and 16 as ט״ו / ט״ז."""
    if n <= 0:
        return str(n)
    s = _HUNDREDS[(n % 1000) // 100]
    rest = n % 100
    if rest == 15:
        s += "טו"
    elif rest == 16:
        s += "טז"
    else:
        s += _TENS[rest // 10] + _ONES[rest % 10]
    if len(s) == 1:
        return s + "׳"
    return s[:-1] + "״" + s[-1]
