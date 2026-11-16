# Samaritan readings: validation report

> **Update (16 Nov 2026), after this report was written.** The month-start check below led to a change in
> `samaritan_calendar.py`. The app's default rule is no longer the sunset day boundary. The month now begins on the
> day of the conjunction if it falls by 15:00 sundial time at Mount Gerizim, otherwise the next day.
> With that rule the 20 community month starts of 2004-2006 all match (20 of 20); the sunset rule gets 17 of 20
> and the noon rule 16 of 20. `docs/samaritan_month_starts_check.csv` now has one column per rule
> (`start_afternoon`, `start_sunset`, `start_noon` and their `diff_` columns).
> The dated Sabbath readings are unchanged by the new rule (83 of 84). The "sunset rule, 17 of 20" figures below
> describe the old default. See `docs/VALIDATION.md`, section 3d, for the combined table (34 of 34 with the 15:00 rule).


This report covers the Samaritan Torah text (`data/readings/torah_sp.json.gz`), the list of section ends
(`data/readings/sp_qissot.json`), and the Sabbath reading schedule (`samaritan_readings.py`).
It lists what was checked, against what, and the results.

## 1. The text: Samaritan Pentateuch (Florentin & Tal 2024)

**Source.** Moshe Florentin and Abraham Tal, *The Samaritan Pentateuch: An English Translation with a Parallel
Annotated Hebrew Text* (Open Book Publishers 2024, https://doi.org/10.11647/OBP.0415). Licence CC BY-NC 4.0,
as stated on the book's copyright page. The Hebrew follows Ms. Nablus 6 (1204 CE). The text was taken from the
publisher's PDF in the Internet Archive item c626ab74-3df2-4291-a871-030f76c129b5 (1,126 pages; text pages 104–913).

**How it was extracted.** Each page has two columns. The Hebrew text and the English translation are told apart by
font and size. Running heads, page numbers and the footnotes at the foot of the page use other sizes, so they are
left out, and so are the endnotes. In the PDF the Hebrew words come out in reverse order. The program rebuilt them
letter by letter, from right to left by position on the page. The book's own verse numbers split the text into verses.

**Verse counts against the Masoretic Text.** The Masoretic count comes from the Westminster Leningrad Codex
(openscriptures/morphhb).

| Book | Samaritan verses | of which Samaritan additions (e.g. 7:18a) | Masoretic verses | Masoretic verse numbers not used in the Samaritan file |
|---|---|---|---|---|
| Genesis | 1536 | 3 | 1533 | — |
| Exodus | 1268 | 70 | 1213 | 20:23, 20:24, 20:25, 20:26, 29:21, 30:1, 30:2, 30:3, 30:4, 30:5, 30:6, 30:7, 30:8, 30:9, 30:10 |
| Leviticus | 859 | 0 | 859 | — |
| Numbers | 1327 | 38 | 1289 | — |
| Deuteronomy | 964 | 11 | 959 | 5:30, 5:31, 5:32, 5:33, 34:2, 34:3 |
| **Total** | **5954** | **122** | **5853** | |

All of these differences are expected:

- **Additions** (122 verses with letter suffixes). Examples are the expanded plague stories (Exod 7:18a–c, 7:29a–d,
  8:19a–d, 9:5a–e, 9:19a–g, 10:2a–d) and the Mount Gerizim commandment after the Ten Commandments (Exod 20:13a–g).
  There are also other harmonising additions, many of them repeating Deuteronomy. Examples are Exod 18:24a–g,
  20:17a–i; Num 10:10a–c, 12:16a–d, 13:33a–g, 20:13a–i; Deut 2:7a–c, 5:17a–h; and Gen 30:36a–c.
- **Moved passages.** The incense altar (Exod 30:1–10) stands after Exod 26:35 as 26:35a–j, and Exod 29:21 stands
  after 29:28 as 29:28a. The Samaritan Pentateuch puts them there.
- **Different verse numbering.** In Exodus 20 and Deuteronomy 5 the edition counts "I am..." and "You shall have
  no other gods" as one verse, so Exodus 20 ends at verse 22 (Masoretic 26) and Deuteronomy 5 at verse 29
  (Masoretic 33). Deut 34:1–3 is one verse in the Samaritan text.
- **Known Samaritan readings, checked by eye:**
  - Deut 27:4 reads בהרגריזים, "on Mount Gerizim", where the Masoretic Text has Ebal.
  - Exod 20:13a–g has the command to set up stones and build an altar on "Mount Gerizim" (בהר גריזים).
  - Gen 5:28 gives Lamech's age as 53, the Samaritan chronology.

**Spot checks against page images (16 verses).** Gen 1:1, 1:5, 1:11, 1:14, 6:16, 6:19, 6:20; Exod 18:24e,
20:6, 20:7, 20:13a–c; Lev 9:2; Deut 5:5, 5:6, 34:10, 34:11. Each was compared word for word, in both columns, with
a picture of the page. All 16 agree.

**Automatic check of every verse.** Each Samaritan Hebrew verse was compared with the Masoretic consonants of the
same verse. Exodus 20 and Deuteronomy 5 were left out because their numbering differs. Over 5,781 verses the average
word agreement is 0.90. Only 26 verses score below 0.5. The 30 lowest were read one by one; every one is a real
Samaritan difference (different spelling, an extra "and", a rearranged passage), not an extraction error. If the
Hebrew words had stayed reversed, the reversed order would score higher. It scores higher in only 2 verses (Exod 26:3,
Num 15:12), and only because the same words repeat there.

**Defects found and fixed.**

1. Exod 18:24g: the edition does not print the number 24g in the English column. The English was split at
   "And he took the heads of their tribes..." to match the Hebrew 24g.
2. Deut 5:7: the edition prints the verse number 7 twice. Both parts are kept as one verse, 5:7.
3. The font in the PDF stores ligatures (fi, ff, fl, ffi, ffl) as odd symbols. They were turned back into letters.
4. Words split by a hyphen at a line end were rejoined: 829 joined, 77 hyphens kept (compounds such as
   "man-servant", numbers such as "twenty-two", place names such as "Bit-el").
5. Scribal colophons at the end of each book (the count of sections) were taken out of the last verse.

Passages that could not be extracted cleanly: **none** (0 verses). Every verse has both Hebrew and English. No
verse has stray footnote text or verse numbers in it.

**What the Hebrew does and does not have.** It has no vowel points: the Samaritan manuscript has none, and
Samaritan tradition does not write them. A colon at the end of a verse marks the end of a section (*qiṣṣa*).
A full stop inside a verse is the editors' mark for a Samaritan pause. The edition's red and italic marking of
differences from the Masoretic Text is not kept.

**Sections (*qiṣṣot*).** 966 section ends were found: Gen 251, Exod 200, Lev 136, Num 217, Deut 162.
The manuscript's own end-of-book notes give Exod 200 (match), Lev 134 (2 more found) and Num 218 (1 fewer found).
In 26 places the section sign stands inside a verse; these are listed in `sp_qissot.json`.

## 2. The Sabbath reading schedule

**Sources.**

- (1) The community's *Table of the weekly Parashot*: 54 portions with verse ranges and the "additional verse"
  read with each. It is online at the-samaritans.net (2026), with versions in the Internet Archive from 2004
  and 2017; the 2017 version has the Hebrew names.
- (2) The Israelite Samaritan Information Institute: the cycle begins and ends on the Sabbath after Shemini Atzeret.
- (3) The-Samaritans.com monthly calendars for Apr 2004 – Dec 2006 (20 months, via the Internet Archive). These
  give **84 dated Sabbaths** with their portions and special names. Also three 2015 event pages for "wonder"
  Sabbaths.
- (4) Samaritans do not read a haftarah. Their canon is the five books of Moses only, so haftarah is always empty.

**The portion table against the text.** The 54 ranges cover all 5,954 verses of the Samaritan file exactly once,
with no gaps and no overlaps. 50 of the 54 portion boundaries fall on a section end of the manuscript. Of the
other 4:

- Gen 8:20/21: the section sign stands inside 8:21; the table's split is kept.
- Deut 22:11/12: this module moves the split to 22:12/13. The portion "Ki Yikach Ish Isha" is named from the
  words of 22:13, and the manuscript's section ends after 22:12.

Two more points about the table:

- Each portion's Hebrew name was checked against the opening words of the Samaritan text: 54 of 54 agree, allowing
  for spelling.
- The table's "Ki Tissa – Numbers 30:11-16" is read as **Exodus** 30:11-16; its Hebrew opening words are
  "כי תשא את ראש".

**Rules taken from the dated calendars.**

- **First Month.** Leviticus starts on the first Sabbath of the First Month. The Sabbath during the Feast of
  Unleavened Bread has no portion. The six Sabbaths of the Omer read the rest of Leviticus. The 7th Omer Sabbath,
  the "Sabbath of the Commandments", has no portion.
- **Summer.** Numbers and Deuteronomy are read straight through after Shavuot.
- **Seventh Month.** The Sabbath of the Selihot, the Day of Atonement and the Sabbath of Sukkot have no portion.
- **Winter.** Genesis begins on the Sabbath after the Eighth Day of Assembly, and Exodus is finished by the
  First Month.

**Result against the 84 dated Sabbaths (2004–2006): 83 match, 1 does not.**

- All 84 agree on whether there is a portion at all, and in 83 the portion or joined portions are the same.
- All 16 named Omer and wonder labels match (Sea, Marah, Elim, Manna, Rock, Amalek, locusts, darkness, in 2004
  and 2006). All 9 portion-less Sabbaths match: Unleavened Bread, Commandments, Selihot, Sukkot, and the Day of
  Atonement on a Sabbath (2004).
- The one mismatch is 6 Nov 2004. The calendar prints just "Bereshit". The model reads Bereshit + Ve-Ha'adam Yada,
  because in 2004–05 Ve-Ha'adam Yada is not listed on any Sabbath, so it must have been read with a neighbour.
- The three 2015 wonder Sabbaths also match: lice 21 Mar, swarms 28 Mar, pestilence 4 Apr.

The 84 rows are in `samaritan_dated_check.csv`.

**What is a model (not established), and how often it matters (1850–2147, 297 years).**

- **Winter joins.** Common years need 6 joins (37 years) or 7 joins (151 years). The 7 joins are those printed in
  the 2004–05 calendar; for 6 joins the assumed Bereshit + Ve-Ha'adam Yada join is dropped.
- **Leap years** need 2 joins (48 years) or 3 joins (61 years). Only one is attested: Ve-Ha'adam Yada +
  Ve-Yada Adam (21 Oct 2006). The model adds El Shaddai + Ben Porat, then Va-Yavo Yosef + Ve-Elle Shemot.
  These are the shortest pairs that were joined in 2004–05. In those years the Sabbaths between the first
  unattested join and the end of Exodus may be one week off.
- **Numbers–Deuteronomy** needs 0 joins (74 years), 1 join (126 years) or 2 joins (97 years). The first join,
  Ki Atem + Banim Atem, is attested (26 Aug 2006). The second, Shoftim + Ki Yikach, is a model choice.
- **Wonder Sabbaths.** The rule (count back nine Sabbaths from the second Sabbath of the First Month) fits all
  7 dated examples. It is still an inference.
- **Edge cases not seen in the data.** These are a Sabbath on the Feast of the Seventh Month or on the Eighth Day
  of Assembly, and what is read on the portion-less Sabbaths. In all of them the module gives no Torah range.
- Every result therefore carries `model: True`.

**The app's Samaritan calendar against the same 2004–2006 calendars.** This is a side result for
`samaritan_calendar.py`, which this track did not change. The month starts were rebuilt from every day of each
monthly calendar.

| Calendar page | Month | Community start | App start | |
|---|---|---|---|---|
| AprilMay04.htm | The First Month | 2004-04-20 | 2004-04-19 | app 1 day earlier |
| MayJune04.htm | The Second Month | 2004-05-19 | 2004-05-19 | ✓ |
| JuneJuly04.htm | The Third Month | 2004-06-18 | 2004-06-18 | ✓ |
| JulyAug04.htm | The Fourth Month | 2004-07-17 | 2004-07-17 | ✓ |
| AugSep04.htm | The Fifth Month | 2004-08-16 | 2004-08-16 | ✓ |
| OctNov04.htm | The Seventh Month | 2004-10-14 | 2004-10-14 | ✓ |
| NovDec04.htm | The Eighth Month | 2004-11-13 | 2004-11-12 | app 1 day earlier |
| Dec04Jan05.htm | The Ninth Month | 2004-12-12 | 2004-12-12 | ✓ |
| Janfeb05.htm | The Tenth Month | 2005-01-10 | 2005-01-10 | ✓ |
| FebMar05.htm | The Eleventh Month | 2005-02-09 | 2005-02-09 | ✓ |
| MarApr05.htm | The T welfth Month | 2005-03-10 | 2005-03-10 | ✓ |
| MarchApril06.htm | The First Month | 2006-03-29 | 2006-03-29 | ✓ |
| AprilMay06.htm | The Second Month | 2006-04-28 | 2006-04-28 | ✓ |
| MayJune06.htm | The Third Month | 2006-05-27 | 2006-05-27 | ✓ |
| JuneJuly06.htm | The Fourth Month | 2006-06-26 | 2006-06-25 | app 1 day earlier |
| JulyAug06.htm | The Fifth Month | 2006-07-25 | 2006-07-25 | ✓ |
| AugSep06.htm | The Sixth Month | 2006-08-24 | 2006-08-24 | ✓ |
| SepOct06.htm | The Seventh Month | 2006-09-22 | 2006-09-22 | ✓ |
| OctNov06.htm | The Eighth Month | 2006-10-22 | 2006-10-22 | ✓ |
| NovDec06.htm | The Ninth Month | 2006-11-21 | 2006-11-21 | ✓ |

The app's default (sunset) rule gets 17 of 20 month starts right. In the other 3 (1st month 2004, 8th month 2004,
4th month 2006) it starts the month a day early. Reingold & Dershowitz's noon rule gets 16 of 20, and its misses
fall in different months. Because of the 2004 miss, the app puts the 2004 Passover sacrifice on 2 May, while the
community calendar gives 3 May. None of the 84 reading assignments changes.

Also checked:

- 2015: the 13th month began 20 Mar, the First Month 19 Apr, and the Passover sacrifice was on 2 May. The
  community's event pages give the same three dates as the app.
- The eight 2026 festival dates listed on the-samaritans.net all agree: 6th month 11 Sep, 7th month 11 Oct,
  Atonement 20 Oct, Sukkot 25 Oct, Sabbath of Sukkot 31 Oct, Shemini Atzeret 1 Nov, 8th month 9 Nov,
  9th month 9 Dec.

**Coverage.** The module gives a reading for every Saturday from 13 Apr 1850 to 14 Oct 2147: 15,524 Sabbaths.
It returns None for the last 77 Sabbaths of the calendar table, because the next First Month is not in the table.

**A source that was not used.** The community's online calendar app (sam-calendar.the-samaritans.net) computes
weekly portions too, but it stores its data in a deliberately scrambled form. It was not decoded, and nothing
was compared against it.
