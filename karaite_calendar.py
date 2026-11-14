"""
The Karaite calendar (לוח הקראים).

Karaite Jews keep the biblical calendar as they read it, without the rabbinic fixed calendar:

* A month begins on the evening the new crescent is seen from the Land of Israel; a month is never
  longer than 30 days. Here this is the same Jerusalem crescent chain as the app's observed calendar
  (same visibility criterion), so the months are identical to the observed calendar's.
* The year begins with the month of the aviv - the ripening barley in the Land of Israel. Barley cannot
  be computed from an ephemeris, so this model uses the observed calendar's spring-equinox rule as a
  stated stand-in. In a real year the barley inspection can differ by a month.
* Festivals are kept one day each, as the Torah gives them. There is no Chanukah, no Tu BiShvat,
  no Lag BaOmer. Purim is kept (14 and 15 of the last Adar).
* The Omer is waved on the Sunday that falls during the Feast of Unleavened Bread (the "morrow after
  the Sabbath" read as the weekly Sabbath), so Shavuot, 50 days later, is always a Sunday.
* Fasts of the destruction follow the biblical dates: 10th of the 10th month, 9th of the 4th month,
  7th and 10th of the 5th month, and 24th of the 7th month (Neh 9:1). They are not moved for Shabbat
  in this model.
"""
from __future__ import annotations

from datetime import timedelta

import fixed_calendar as fc
import observed_calendar as oc
from fixed_calendar import HDate, Holiday, TISHREI, TEVET, ADAR, ADAR_II, NISAN, TAMMUZ, AV


class KaraiteCalendar(oc.ObservedCalendar):
    """Observed months (Jerusalem crescent) with the Karaite festival and fast cycle."""

    def holidays_for_year(self, year: int, rosh_chodesh: bool = True, omer: bool = False) -> list[Holiday]:
        H: list[Holiday] = []
        if not self.year_complete(year):
            return H
        adar = ADAR_II if self.is_leap(year) else ADAR

        def add(m, d, name, he, kind, note=""):
            gd = self.to_gregorian(year, m, d)
            if gd is not None:
                H.append(Holiday(gd, name, he, kind, HDate(year, m, d, self.is_leap(year)), note))

        add(TISHREI, 1, "Yom Teruah (Day of Shouting)", "יום תרועה", "major",
            "one day; Karaites do not call it Rosh Hashanah - the year begins in spring")
        add(TISHREI, 10, "Yom Kippur", "יום הכפורים", "major")
        add(TISHREI, 15, "Sukkot I", "חג הסוכות", "major")
        for d in range(16, 22):
            add(TISHREI, d, f"Sukkot {d - 14} (Chol HaMoed)", "חול המועד סוכות", "chol")
        add(TISHREI, 22, "Shemini Atzeret", "שמיני עצרת", "major", "the eighth day")
        add(TISHREI, 24, "Karaite fast of the 7th month", "צום החדש השביעי", "fast", "Neh 9:1")
        add(TEVET, 10, "Karaite fast of the 10th month", "צום העשירי", "fast", "2 Kgs 25:1")
        add(adar, 14, "Purim", "פורים", "minor", "kept 14 and 15 of the last Adar")
        add(adar, 15, "Purim (day 2)", "פורים", "minor")
        add(NISAN, 14, "Erev Pesach (Passover)", "פסח", "erev", "the Passover is at evening on the 14th")
        add(NISAN, 15, "Chag HaMatzot I (Pesach)", "חג המצות", "major")
        for d in range(16, 21):
            add(NISAN, d, f"Chag HaMatzot {d - 14}", "חג המצות", "chol")
        add(NISAN, 21, "Chag HaMatzot VII (Pesach)", "חג המצות", "major")
        n15 = self.to_gregorian(year, NISAN, 15)
        if n15:
            wave = next(n15 + timedelta(days=k) for k in range(7) if (n15 + timedelta(days=k)).weekday() == fc.SUNDAY)
            H.append(Holiday(wave, "Yom Hanafat HaOmer (Waving of the Omer)", "יום הנפת העומר", "minor",
                             self.from_gregorian(wave), "the Sunday during the Feast of Unleavened Bread"))
            shav = wave + timedelta(days=49)
            hd = self.from_gregorian(shav)
            H.append(Holiday(shav, "Shavuot (Chag HaShavuot)", "חג השבועות", "major", hd,
                             "always a Sunday: the 50th day from the waving of the Omer"
                             + (f" ({hd.day} {hd.month_name})" if hd else "")))
            if omer:
                for i in range(49):
                    od = wave + timedelta(days=i)
                    H.append(Holiday(od, f"Omer day {i + 1}", "ספירת העומר", "omer", self.from_gregorian(od)))
        add(TAMMUZ, 9, "Karaite fast of the 4th month", "צום הרביעי", "fast", "Jer 39:2, 52:6")
        add(AV, 7, "Karaite fast of the 5th month (7 Av)", "צום החמישי", "fast", "2 Kgs 25:8")
        add(AV, 10, "Karaite fast of the 5th month (10 Av)", "צום החמישי", "fast", "Jer 52:12")
        if rosh_chodesh:
            for om in self.year_months(year):
                m = om.month
                if m == TISHREI:
                    continue
                he = "אדר א׳" if (m == ADAR and self.is_leap(year)) else fc.MONTH_NAMES_HE[m]
                H.append(Holiday(om.start, f"Rosh Chodesh {self.month_label(year, m)}",
                                 f"ראש חודש {he}", "rosh_chodesh", HDate(year, m, 1, self.is_leap(year)),
                                 "one day: the day after the crescent was seen"))
        H.sort(key=lambda h: (h.date, fc._KIND_ORDER.get(h.kind, 9)))
        return H
