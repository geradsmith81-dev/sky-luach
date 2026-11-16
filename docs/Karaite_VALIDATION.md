# Karaite Torah readings – validation

This note explains how the Karaite weekly Torah readings in Sky Luach (`karaite_readings.py`,
`data/readings/karaite_parashot.json`) were checked. All the numbers come from
`tools/validate_karaite_readings.py`, run on 16 Nov 2026.

## Summary

* The **list of portions and haftarot** comes from the Karaite Jews of America (KJA). It checks out
  against the Hebrew text and against an independent printed Karaite list from 1733.
* The **dates** (which portion falls on which Sabbath) are a **model**. They follow every rule we could
  find a source for, and they pass those rules in every year from 1850 to 2147. But no published,
  dated Karaite reading calendar could be found, so the dates have **not** been compared with what a
  Karaite synagogue actually read on a given Sabbath. Every reading the app shows is therefore marked
  as a model.

## 1. The portions (what is read)

| Check | Result |
|---|---|
| Portions in the KJA list | 54 |
| Verses covered, end to end, with no gap and no overlap | 5,847 of 5,847 verses in the Masoretic text file |
| Portion boundaries identical to the rabbinic ones (hebcal-leyning table) | 54 of 54 |
| Misprints in the KJA audio list, corrected from KJA's own commentary page for that portion | 9: Vayyera, Bo, Yitro, Ki Tissa, Shemini, Emor, Shelah, Re'eh, Haazinu |

The misprints are things like "Exodus 20:11" for Ki Tissa, where KJA's commentary page reads 30:11. Bo ends
at 13:16 and Beshalach starts at 13:17; the audio list has "13:6" and "13:7". Yitro ends at 20:23 in Hebrew
numbering, where the audio list has 20:26, the English numbering. So the Karaite portion boundaries
are the same as the rabbinic ones. Only the haftarot and the dates differ. Every correction is recorded
for its portion in `karaite_parashot.json` (field `correction`), together with the text exactly as KJA
printed it (field `kja_printed`).

Hebrew names: 49 are as printed on KJA's Torah Portions page. The other five (Ekev, Re'eh, Shofetim, Ki Tetze,
Haazinu) are missing from that page, so they are taken from the opening word(s) of the portion in the
Hebrew text.

## 2. The haftarot (prophetic readings)

The KJA haftarot were compared with the Karaite column of *Seder ha-Haftarot* (Kale, 1733), as tabulated by
A. Marsh (2015), Table 2. That table covers Bereshit to Masei only (43 portions).

| Result | Count |
|---|---|
| Same haftarah (or one of the 1733 alternatives) | 29 |
| Same first verse, different last verse | 10 (Lekh Lekha, Vayyera, Vayyetze, Mikketz, Vayigash, Vayikra, Tzav, Acharei Mot, Bechukotai, Shelah) |
| Different haftarah | 4 |

The four that differ:

| Portion | KJA (today) | Kale 1733 |
|---|---|---|
| Vaera | Isaiah 33:17-34:12, 35:10 | Isaiah 42:8-43:5 |
| Yitro | Isaiah 33:14-34:8 | Isaiah 33:13-34:8 |
| Tazria | 2 Kings 7:3-20 | Isaiah 66:7-66:24, 66:23 |
| Matot | Jeremiah 1:1-2:3 | 1 Samuel 1:1-2:10 |

In two of these, the 1733 list is the more likely reading:

* KJA gives Vaera the same haftarah as Vayyera (Isaiah 33:17).
* KJA's Yitro haftarah begins one verse after the 1733 one.

The app shows the KJA haftarah first. Where the 1733 list differs, its haftarah is shown second with the label
"Karaite (Kale 1733)". As a further cross-check, 20 of the 54 KJA
haftarot begin at the same verse as the rabbinic (Ashkenazi) haftarah. They are almost all in Numbers and
Deuteronomy (the Three Weeks and the seven "consolations"), so the Karaite list is not a copy of the rabbinic one.

## 3. The schedule (which Sabbath gets which portion)

### Rules with a source

| Rule | Source | Years that pass (of 297) |
|---|---|---|
| Vezot Haberakha ends the cycle and Bereshit begins it on Yom Simhat Torah (22nd of the seventh month); Bereshit is the first Sabbath after it | el-Kodsi (KJA site) | 297 |
| Naso on the Sabbath before Shavuot (Shavuot always on a Sunday) | Sar-Shalom 1994, p. 27 | 297 |
| Balak, Pinchas, Matot, Masei, Devarim on the Sabbaths of the mourning period, 9 Tammuz to 10 Av (4 or 5 Sabbaths), and no other portion in that period | KJA Torah Audio page; el-Kodsi | 297 |
| Haazinu on the Sabbath(s) between Yom Teruah and Sukkot | Sar-Shalom 1994, p. 19 | 297 (1 such Sabbath in 75 years, 2 in 222) |
| Va'etchanan on the first Sabbath after 10 Av (the first of seven consolation haftarot) | KJA haftarot | 297 |
| Every portion read exactly once in the year (Haazinu once or twice) | – | 297 |

Range: the reading years 5611–5907 (1850-10-05 to 2147-10-14), 15,499 Sabbaths in all.
Of these, 669 are festival Sabbaths: Yom Teruah, Yom Kippur, Sukkot, and the
Feast of Unleavened Bread. On those the weekly cycle pauses. Our sources do not give the Karaite festival
Torah reading, so the app shows the festival name with no text. No rule failed in any year.

### Rules that are a model (no source found)

No source we found says how Karaites join or split portions to fit a year. The app joins portions in these
cases:

| What the app does | Number of years (of 297) |
|---|---|
| Nitzavim-Vayelech together (7 Sabbaths after 10 Av, the usual case) | 283 |
| Tazria-Metzora, Acharei Mot-Kedoshim, Behar-Bechukotai together (common years) | 187 each |
| Vayakhel-Pekudei together | 170 |
| Matot-Masei together (only 4 Sabbaths of mourning) | 149 |
| Chukat-Balak together (only 3 Sabbaths between Shavuot and 9 Tammuz) | 19 |
| Tetzaveh read over two Sabbaths, split at Exodus 29:1 (leap years with one Sabbath to spare) | 19 |
| Tzav-Shemini together (one more join needed; shortest neighbouring pair) | 3 |
| Shofetim-Ki Tetze together (only 6 Sabbaths after 10 Av) | 3 |

The first five pairs are the ones the rabbinic calendar joins. The Tetzaveh split follows an old custom
of halving portions in leap years, which Sar-Shalom describes (p. 21); it is a rabbinic custom, not a
Karaite one. When two portions are read together, the app lists both haftarot and says it is not known
which one is read.

### How often the Karaite reading matches the rabbinic one

On 14,370 Sabbaths both calendars read a weekly portion. On 8,386
of them (58%), the Karaite model reads the same
portion as the rabbinic calendar of the Land of Israel. On the rest it differs. The main reasons are that
Karaite months begin at the visible new moon, that Karaite leap years are not the rabbinic ones, and that
Naso and the Three-Weeks portions are fixed to different days. This figure only describes the difference;
it is not a test of correctness.

### Published dated Karaite schedules: none found

We looked for a Karaite calendar that lists the portion for each Sabbath. We checked the KJA website and its
public Google Calendar (it lists services but not portions), searches in English and Hebrew, the
Open Siddur Project (it blocks automated access), and the scanned Karaite prayer books on archive.org
(Vilna 1891/1892; N. Gordon 2002). We found no dated schedule, so the dates could not be checked against
real practice. If you can get a Karaite synagogue calendar (for example from the Karaite Jews of America or
the Karaite community in Israel), the script can compare it date by date.

## 4. Technical contract

* Gives no reading for a day that is not a Saturday: yes.
* Gives no reading outside the calendar's range (1700, 2300): yes.
* Result has exactly the agreed fields: yes.
* Every verse reference exists in `torah_mt.json.gz`: yes (no failures).

## 5. Sample year: reading year 5786 (October 2025 – October 2026), as the model gives it

| Sabbath | Karaite date | Reading | Haftarah (KJA) |
|---|---|---|---|
| 2025-10-18 | 25 Tishrei | Bereshit | Isaiah 65:17-66:13 |
| 2025-10-25 | 2 Cheshvan | Noah | Isaiah 54:9-55:12 |
| 2025-11-01 | 9 Cheshvan | Lekh Lekha | Joshua 24:3-18 |
| 2025-11-08 | 16 Cheshvan | Vayyera | Isaiah 33:17-35:10 |
| 2025-11-15 | 23 Cheshvan | Hayyei Sarah | Isaiah 51:2-22 |
| 2025-11-22 | 30 Cheshvan | Toledot | Isaiah 65:23-66:18 |
| 2025-11-29 | 7 Kislev | Vayyetze | Hosea 11:7-13:5 |
| 2025-12-06 | 14 Kislev | Vayishlach | Obadiah 1:1-21 |
| 2025-12-13 | 21 Kislev | Vayeshev | Isaiah 32:18-33:22 |
| 2025-12-20 | 28 Kislev | Mikketz | Isaiah 29:7-24 |
| 2025-12-27 | 6 Tevet | Vayigash | Joshua 14:6-15 |
| 2026-01-03 | 13 Tevet | Vayechi | 2 Kings 13:14-14:7 |
| 2026-01-10 | 20 Tevet | Shemot | Isaiah 27:6-28:13 |
| 2026-01-17 | 27 Tevet | Vaera | Isaiah 33:17-34:12, 35:10 |
| 2026-01-24 | 4 Shevat | Bo | Isaiah 34:11-35:10 |
| 2026-01-31 | 11 Shevat | Beshalach | Joshua 24:7-26 |
| 2026-02-07 | 18 Shevat | Yitro | Isaiah 33:14-34:8 |
| 2026-02-14 | 25 Shevat | Mishpatim | Isaiah 56:1-57:2 |
| 2026-02-21 | 3 Adar | Terumah | Isaiah 60:17-61:9 |
| 2026-02-28 | 10 Adar | Tetzaveh | Jeremiah 11:16-12:15 |
| 2026-03-07 | 17 Adar | Ki Tissa | Isaiah 43:7-44:5 |
| 2026-03-14 | 24 Adar | Vayakhel-Pekudei | 1 Kings 8:1-19; Jeremiah 30:18-31:13 |
| 2026-03-21 | 1 Nisan | Vayikra | Isaiah 43:21-44:23 |
| 2026-03-28 | 8 Nisan | Tzav | Malachi 3:4-24, 3:23 |
| 2026-04-04 | 15 Nisan | Sabbath of Feast of Unleavened Bread (Chag HaMatzot) | – |
| 2026-04-11 | 22 Nisan | Shemini | Ezekiel 43:27-44:16 |
| 2026-04-18 | 29 Nisan | Tazria-Metzora | 2 Kings 7:3-20; 2 Kings 7:3-18 |
| 2026-04-25 | 7 Iyyar | Acharei Mot-Kedoshim | Ezekiel 22:1-16; Isaiah 4:3-5:16 |
| 2026-05-02 | 14 Iyyar | Emor | Ezekiel 44:25-45:11 |
| 2026-05-09 | 21 Iyyar | Behar Sinai-Bechukotai | Isaiah 24:2-23; Isaiah 1:19-2:11 |
| 2026-05-16 | 28 Iyyar | Bamidbar | Hosea 2:1-22 |
| 2026-05-23 | 6 Sivan | Nasso | Judges 13:2-24 |
| 2026-05-30 | 13 Sivan | Beha'alotekha | Zechariah 2:14-4:7 |
| 2026-06-06 | 20 Sivan | Shelah | Joshua 2:1-16 |
| 2026-06-13 | 27 Sivan | Korach | Hosea 10:2-11:9 |
| 2026-06-20 | 4 Tammuz | Chukat | Judges 11:1-17 |
| 2026-06-27 | 11 Tammuz | Balak | Micah 5:6-6:8 |
| 2026-07-04 | 18 Tammuz | Pinchas | Malachi 2:5-3:3 |
| 2026-07-11 | 25 Tammuz | Matot | Jeremiah 1:1-2:3 |
| 2026-07-18 | 3 Av | Masei | Joshua 20:1-9 |
| 2026-07-25 | 10 Av | Devarim | Isaiah 1:1-27 |
| 2026-08-01 | 17 Av | Va'etchanan | Isaiah 40:1-22 |
| 2026-08-08 | 24 Av | Ekev | Isaiah 49:14-50:5 |
| 2026-08-15 | 1 Elul | Re'eh | Isaiah 54:11-56:1 |
| 2026-08-22 | 8 Elul | Shofetim | Isaiah 51:12-52:8 |
| 2026-08-29 | 15 Elul | Ki Tetze | Isaiah 54:1-17 |
| 2026-09-05 | 22 Elul | Ki Tavo | Isaiah 60:1-16 |
| 2026-09-12 | 29 Elul | Nitzavim-Vayelech | Isaiah 61:10-63:1; Isaiah 55:6-56:8 |
| 2026-09-19 | 7 Tishrei | Haazinu | Hosea 14:2-10 |
| 2026-09-26 | 14 Tishrei | Haazinu | Hosea 14:2-10 |
| 2026-10-03 | 21 Tishrei | Sabbath of Sukkot | – |

## Sources

* Karaite Jews of America, "Torah Audio – Karaite Parashiot and Haftarot", https://karaites.org/torah-audio/ , and
  "Torah Portions" with the commentary page for each portion, https://karaites.org/torah-portions/ (read 16 Nov 2026).
* Mourad el-Kodsi, *The Karaite Jews of Egypt from 1882–1985* (title as given on the KJA page), pages reproduced on
  https://karaites.org/karaite-customs-and-traditons/ .
* Rahamim Sar-Shalom, "Parashat ha-shavua – mi-minhagim shonim le-minhag ahid", *Shana be-Shana* 5754 (1994),
  https://www.daat.ac.il/daat/kitveyet/shana/sarshalom-2.pdf .
* *Seder ha-Haftarot* (Kale, 1733), Karaite column in Aaron Marsh, *The Sequential Triennial Cycle: A History and Guide
  to its Modern Use*, Master's project, Academy for Jewish Religion, 2015, Table 2, pp. 36–38.
* Rabbinic comparison: hebcal-leyning tables (BSD 2-Clause), `data/readings/rabbinic_leyning.json`; the app's
  `fixed_calendar.parshiyot_for_year(year, israel=True)`.
