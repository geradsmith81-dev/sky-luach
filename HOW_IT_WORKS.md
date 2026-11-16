## How Sky Luach works · איך זה עובד

Sky Luach (לוח השמים) shows five calendars of the Jewish and Samaritan traditions side by side. Use the switch at the top of every page to change between them.

### 1. The fixed calendar · הלוח הקבוע

This is the calendar Jewish communities use today. Tradition credits it to Hillel II (הלל השני), about 359 CE. It is pure arithmetic and never looks at the sky.

- **Molad (מולד).** Each month starts from a *mean* new moon. Successive molads are exactly 29 days, 12 hours and 793 parts apart (a part, *chelek*, is 1/1080 hour). The count starts from the molad of Creation, "BaHaRaD".
- **The 19-year cycle (מחזור קטן).** Years 3, 6, 8, 11, 14, 17 and 19 of each cycle have a second Adar, which keeps Pesach (פסח) in spring.
- **Postponements (דחיות).** Rosh Hashanah (ראש השנה) never falls on a Sunday, Wednesday or Friday (*lo ADU rosh*). It is also moved when the molad falls at noon or later (*molad zaken*), and in two rarer cases (*GaTaRaD*, *BeTUTaKPaT*).
- **Holidays.** You can choose the Israel custom (ארץ ישראל), the diaspora custom with second festival days (Orthodox and most Conservative congregations), or one day everywhere with a one-day Rosh Hashanah (Reform and many Reconstructionist congregations). Sigd (סיגד), the Beta Israel festival on 29 Marcheshvan, can be shown or hidden. Fasts that would fall on Shabbat (שבת) are moved as tradition prescribes. The weekly Torah portion (פרשת השבוע) follows the standard rules for joining portions.
- **Accuracy.** The arithmetic follows Reingold & Dershowitz, *Calendrical Calculations*. For every day from 1850 to 2149 it matches two independent programs (pyluach and convertdate), with zero differences in dates, holidays, Torah portions and molads. See docs/VALIDATION.md.

### 2. The observed calendar · קידוש החודש על פי הראייה

This is a reconstruction of how the calendar worked while the Sanhedrin (סנהדרין) sanctified months on the testimony of witnesses (Mishnah, *Rosh Hashanah* 1–2). It is computed from NASA JPL astronomy.

1. **The day begins at sunset in Jerusalem (ירושלים).**
2. **New months.** On the evening that ends day 29 of a month, the app works out whether the young crescent would be visible from Jerusalem. If it would, the next day is the 1st of the new month. If not, the month gets a 30th day and the new month begins after it, because a month never has more than 30 days.
3. **Crescent visibility.** The app uses a published criterion. The default is Yallop (יאלופ, 1997), zone A or B: visible to the naked eye in a clear sky. The alternatives are a stricter Yallop A, a looser Yallop C, and the criterion of Odeh (עודה, 2004). The calculation uses the Moon's height above the Sun at the "best time", 4/9 of the way from sunset to moonset, and the width of the lit crescent.
4. **The leap month.** Nisan (ניסן) is the first month in which the spring equinox falls no later than the 15th day. This follows Rambam (רמב״ם), *Kiddush HaChodesh* 4:2: if the *tekufah* would fall on 16 Nisan or later, a second Adar was added. You can use the true equinox from JPL, or the traditional tekufah of Shmuel (שמואל) or of Rav Adda (רב אדא).
5. **Festivals.** Festivals fall on their biblical dates in these months, one day each. Shavuot (שבועות) is counted as the 50th day from the Omer (עומר) offering on 16 Nisan, so it can fall on 5, 6 or 7 Sivan.
6. **Month names.** The months also carry their First Temple-period names. In the Bible, months are counted from the spring ("the first month", Exod 12:2), and four have names older than the Babylonian ones used today: Aviv (אביב, Exod 13:4), Ziv (זו, 1 Kgs 6:1, 37), Ethanim (האיתנים, 1 Kgs 8:2) and Bul (בול, 1 Kgs 6:38).

**Limits.** No formula can know the weather, the eyesight of witnesses, the state of the barley (the *aviv*), or the court's other considerations. Read this calendar as a reasoned model of how a sighting calendar behaves, not as a record of any particular year's practice, and not as a guide to practice today.

### 2b. The Early Temple Period calendar · לוח תקופת המקדש הקדומה

This calendar asks what the Jewish calendar would look like if it followed the true astronomical new moon from year 1.

1. **New months.** Each month begins at the **true new moon**: the moment the Moon passes the Sun (the geocentric conjunction), computed from NASA JPL DE440s. Day 1 starts at the first sunset in Jerusalem after that moment. There is no mean molad, no crescent sighting and no postponement rule, and months are 29 or 30 days.
2. **Counting from year 1.** Years are counted from AM 1. Because every month resets to the real Moon, the starting year changes only the year numbers, never a month boundary.
3. **The leap month.** You choose the rule in Settings:
   - the **spring equinox rule**, the same marker and Nisan day as the observed calendar (the default);
   - the **19-year cycle counted from AM 1**, which gives the fixed calendar's leap years combined with the real Moon.
4. **Holidays.** One day each. Shavuot is the 50th day from 16 Nisan.

**How it compares (1850–2149, 3,711 true new moons):**

- **With the fixed calendar:** the month starts on the same day 1,790 times, 1 day earlier 1,164 times, 2 days earlier 124 times, 1 day later 622 times and 2 days later 11 times. This has two causes: the molad runs a mean of 2.0 hours after the true new moon (range −12 to +16 hours), and the fixed calendar's postponement rules can move Rosh Hashanah.
- **With the observed calendar:** it is almost always 1–2 days earlier, because the conjunction comes before the crescent can be seen.
- **Weekdays:** Rosh Hashanah falls on any day of the week, including Sunday, Wednesday and Friday, which the fixed calendar never allows. Yom Kippur falls next to Shabbat (Friday or Sunday) in 70 of 299 years.
- **Leap years:** with the 19-year cycle, Pesach is never a month away from the fixed date. With the equinox rule, it is a month away in 65 of 298 years, about as often as in the observed calendar (74 of 298).
- **Drift of the molad:** the molad's mean month is about 0.46 seconds longer than the true one. You can see it creeping: the mean molad−conjunction offset is +1.81 h in 1850–1949, +2.00 h in 1950–2049 and +2.19 h in 2050–2149.

**A caution.** No archaeological or textual evidence shows that a conjunction-based calendar was used in ancient Israel or Judah. Biblical and rabbinic practice began the month with the first visible crescent; the Hebrew *chodesh* means "renewal". The name *Early Temple Period* is only a label for this astronomical ideal. It does not mean the calendar was used in the First Temple period, and it is not a reconstruction of documented practice. Its first month (Tishrei AM 1, autumn 3761 BCE) also lies outside DE440s. It would need the much larger DE441 file and an estimate of Earth's rotation 5,800 years ago, and that estimate is uncertain by more than enough to move a conjunction across sunset.

### 2c. The Karaite calendar · לוח הקראים

Karaite Jews (קראים) keep the calendar as they read it in the Bible, without the rabbinic fixed calendar.

- **Months.** A month begins when the new crescent is seen from the Land of Israel, and no month is longer than 30 days. The app uses the same Jerusalem crescent predictions as the observed calendar, so the months are the same.
- **The year.** The year begins with the month of the *aviv*, the ripening barley in the Land of Israel. Barley cannot be computed from an ephemeris, so the app uses the observed calendar's spring-equinox rule as a stand-in. In a real year the barley inspection can move the year by a month.
- **Festivals.** Each festival is kept for one day. There is no Chanukah, Tu BiShvat or Lag BaOmer. Purim is kept on 14 and 15 of the last Adar.
- **Shavuot.** The Omer is waved on the Sunday during the Feast of Unleavened Bread, because "the morrow after the sabbath" is read as the weekly Sabbath. Shavuot, 50 days later, is therefore always a Sunday.
- **Fasts.** The fasts of the destruction follow the biblical dates: 9 Tammuz, 7 and 10 Av, 24 Tishrei and 10 Tevet. They are not moved for Shabbat in this model.

### 2d. The Samaritan calendar · לוח השומרונים

The Samaritans (שומרונים) are an Israelite community of Mount Gerizim and Holon. Their priests calculate the calendar, keep the full method within the priestly family, and publish it twice a year.

- **Months.** Each month begins on the day of the true new moon, computed from NASA JPL DE440s. If the new moon comes by 15:00 sundial time at Mount Gerizim, that day is the first of the month; if later, the next day is. This cut-off is the app's own calibration: published community dates require it to lie between 14:17 and 15:42. With it the app matches all 34 dates checked (2001–2026). Two other rules can be chosen in Settings: a sunset day boundary (31 of 34) and the published rule of Reingold & Dershowitz, with a noon cut-off (25 of 34).
- **The year.** The First Month is the first month to begin after 11 March in the Julian calendar (24 March today). Months are named by number. The year number counts from the entry into Canaan and advances at the Sixth Month: year 3665 began in September 2026.
- **Festivals.** The festivals are the Passover sacrifice on Mount Gerizim (14th of the First Month) and the Feast of Unleavened Bread (15th–21st). The others are Shavuot (always a Sunday), the Feast of the Seventh Month (the Samaritan New Year), the Day of Atonement, Tabernacles and the Eighth Day. Unleavened Bread, Shavuot and Tabernacles are pilgrimages up the mountain.
- **Optional floor.** A rule that the sacrifice is never before 8 April is sometimes quoted. It is off by default because it contradicts a published date (19 Aug 2001).

### 2e. Traditions · זרמים

The Traditions page redraws a well-known diagram of the branches of Judaism and shows which calendar each branch keeps. Most branches keep the fixed calendar and differ only in festival days. The Karaites and Samaritans keep their own calendars, and the buttons on that page switch the app to them.

### 3. The astronomy · האסטרונומיה

All positions come from NASA JPL's planetary ephemeris **DE440s**, the same file the other apps in this series use, computed with the Skyfield library. The file covers 1850–2149. Putting the larger de440.bsp in the *ephem* folder extends the times and moon phases to 1550–2650; the observed calendar's precomputed tables then also need rebuilding (tools\build_tables.py).

- **Sunrise and sunset** use the standard definition: the Sun's upper edge on a sea-level horizon, with normal refraction. **Nightfall** (צאת הכוכבים) is when the Sun is 8.5° below the horizon, the usual three-stars time. **Dawn** (עלות השחר) is at 16.1°.
- **New moons** are the true geocentric conjunctions. They match JPL Horizons to a small fraction of a second.
- The **Cycles** page compares the molad with the true new moon (they differ by up to about 14 hours). It also compares the tekufot of Shmuel and Rav Adda with the true equinoxes and solstices: Shmuel's now runs about two weeks late, Rav Adda's about a week.

### 4. Traditional cycles · מחזורים

- **Small cycle** (מחזור קטן): 19 years, with seven leap years.
- **Great cycle** (מחזור גדול): 28 years. Birkat HaChamah (ברכת החמה) is said when Shmuel's tekufah of Nisan returns to the start of a Wednesday; the next is on 8 April 2037.
- **Sabbatical cycle** (שמיטה): 7 years, by the modern reckoning (5782 and 5789 are shmita years).

### 4b. Your location and the holiday guide · מקום ומדריך המועדים

- **Location.** When the app opens it first guesses your place from your device's time zone. It then asks the device once for its position (GPS on a phone, Wi-Fi position on a computer); the browser shows its own permission prompt. Sunset and Shabbat times use your exact coordinates, named after the nearest town (with its Hebrew name when one is known). A place you choose yourself in Settings is never replaced. Press 📍 **Use my location** to ask again. Your position stays in this browser session and is not stored or sent anywhere else.
- **Holiday histories.** Click any holiday's name (in the month grid, the year list, "Coming up" or Compare) for a short history with its biblical, rabbinic and, where relevant, archaeological background. All the histories are also collected in the Holiday guide below.

### 4c. Shabbat Torah readings · קריאת התורה

On the Today page, choose **Torah reading · קריאת התורה** at the top. The app then shows the full text of a Shabbat's reading, Hebrew and English side by side, with the haftarah. You can pick this Shabbat or any of the surrounding weeks. Each calendar uses the reading of its own tradition:

- **Fixed (rabbinic):** the annual cycle of 54 portions, with the Israel or diaspora schedule set by your festival-day setting. It includes the special readings of festival Shabbatot, Rosh Chodesh, Chanukah and the four special Shabbatot, with Ashkenazi and Sephardi haftarot. Every Shabbat from 1850 to 2149 matches hebcal's open-source tables. The text is the Masoretic text (Westminster Leningrad Codex) with the Jewish Publication Society's 1917 English translation.
- **Observed and Early Temple Period:** the ancient triennial cycle of the Land of Israel (Talmud, *Megillah* 29b): about 154 short sections (*sedarim*), read one per Shabbat over three years or more. How the cycle began and how long it lasted are debated, so both are settings (Nisan or Tishrei; three or three and a half years). This schedule is a reconstruction.
- **Karaite:** the Karaite portions and haftarot as published by the Karaite Jews of America, on the Karaite calendar. The cycle starts after 22 Tishrei, Naso is read on the Sabbath before the Sunday Shavuot, and the mourning portions fall between 9 Tammuz and 10 Av. How portions are joined in a given year is the app's model, because no dated Karaite schedule was found.
- **Samaritan:** the Samaritan community's 54 Sabbath portions, read from the Samaritan Pentateuch. The text is MS Nablus 6 (1204 CE) in the edition and English translation of Moshe Florentin and Abraham Tal (2024). The Hebrew is unpointed, as in the manuscript, and it contains the Samaritan readings, such as the commandment about Mount Gerizim after the Ten Commandments. The schedule matches 83 of 84 dated Sabbaths in the community's 2004–2006 calendars. There is no haftarah: the Samaritan scriptures are the Torah alone.

### 5. The look of the app · עיצוב

The design draws on the art of the First Temple period (Iron Age II, about 1000–586 BCE) in Israel and Judah:

- **Proto-Aeolic (volute) capital.** Next to the title. Capitals of this kind stood on royal buildings at Samaria, Megiddo, Hazor, Ramat Rahel and the City of David.
- **Palmettes, pomegranates and lily-work.** The frieze. The palmette follows the Samaria ivories; the pomegranates recall the rows on the bronze pillars Jachin and Boaz (1 Kgs 7:18–20); the wavy chain stands for the lily-work.
- **Rosette.** Beside each heading. It follows the rosette seal impressions on Judahite jar handles (late 7th century BCE) and the "open flowers" carved in the Temple (1 Kgs 6:18, 29).
- **Colours.** Cedar panelling (1 Kgs 6), ivory (Amos 3:15) and gold leaf. Tekhelet blue marks Shabbat, with argaman purple and scarlet from the Tabernacle hangings (Exod 26:1).
- **Script.** The line under the title spells לוח השמים letter for letter in the Paleo-Hebrew script of the period, as on the Siloam tunnel inscription. Words are divided by dots, as in that inscription. The font is Noto Sans Phoenician (SIL Open Font License).

The ornaments are drawn from simple geometric shapes, as stylised evocations; they are not copies of particular objects.

### 6. Sources · מקורות

- E. M. Reingold & N. Dershowitz, *Calendrical Calculations* (Cambridge University Press).
- Maimonides (Rambam), *Mishneh Torah, Hilchot Kiddush HaChodesh*.
- B. D. Yallop, *A Method for Predicting the First Sighting of the New Crescent Moon*, NAO Technical Note 69 (1997).
- M. Sh. Odeh, "New criterion for lunar crescent visibility", *Experimental Astronomy* 18 (2004): 39–64.
- R. S. Park et al., "The JPL Planetary and Lunar Ephemerides DE440 and DE441", *Astronomical Journal* 161 (2021): 105.
- B. Rhodes, *Skyfield* (Python astronomy library).
