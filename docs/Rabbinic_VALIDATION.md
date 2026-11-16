# Torah readings – validation (rabbinic track)

Prepared 16 November 2026. This covers three things: the Hebrew–English Torah text, the
rabbinic (annual-cycle) Shabbat readings, and the model of the ancient triennial cycle.
Every number below was produced by running the code; nothing was typed in by hand.

## 1. The Torah text (`data/readings/torah_mt.json.gz`)

**Sources.** Hebrew: Westminster Leningrad Codex as published by the Open Scriptures Hebrew Bible
project (github.com/openscriptures/morphhb, `wlc/Gen.xml` … `wlc/Deut.xml`; public domain).
English: JPS 1917, *The Holy Scriptures According to the Masoretic Text* (public domain), in Sefaria's
digital edition from the Open Siddur Project (Sefaria-Export-Archive, commit ea008bc7a9; licence field
"Public Domain").

**How the Hebrew was cleaned.** Cantillation marks, meteg and paseq removed; vowels kept. Where the written and
the read forms differ (ketiv/qere, 67 places), the written form is shown in (round brackets) followed by the
pointed read form in [square brackets].

| Check | Result |
|---|---|
| Books | 5 (Genesis–Deuteronomy) |
| Verses per book | Genesis 1533, Exodus 1210, Leviticus 859, Numbers 1289, Deuteronomy 956 |
| Total verses | **5847** |
| Verses with both Hebrew and English | 5847 of 5847 (no empty entries) |
| Hebrew and English verse lists identical, chapter by chapter | yes, all 187 chapters |
| Chapter verse counts equal to hebcal-leyning's `numverses.json` | yes, all 187 chapters |
| Accent characters left in Hebrew | 0 |
| English/Hebrew length ratio (a shifted verse would show as an outlier) | every verse between 0.67 and 2.30 (median 1.25) |

**Why 5,847 and not 5,845.** The 5,845 figure is the medieval Masoretic summary note at the end of the Torah. Actual counts
differ slightly: printed Chumashim count 5,846 (Epstein & Greenberger, *Hakirah* 7). The raw Leningrad numbering has 5,853,
because it gives each of the short commandments "You shall not murder / commit adultery / steal / bear false witness" a
verse of its own (Exod 20:13–16, Deut 5:17–20). Those were joined into one verse (Exod 20:13, Deut 5:17), as in
standard Jewish editions and JPS 1917, which leaves 5,847. The remaining difference comes from Num 25:19
("And it came to pass after the plague,"). The Leningrad Codex has it as a verse of its own, while Sefaria's JPS starts
26:1 with those words. The English was split at "that the LORD" to match the Hebrew.

**Spot checks** (Hebrew and English read side by side):
Gen 1:1 (creation) ✓; Gen 32:1 (Laban rose early – the Hebrew numbering, = English 31:55) ✓; Exod 20:1–14 (Decalogue; 20:13
holds the four short commandments, 20:14 "You shall not covet") ✓; Lev 6:1 ("And the LORD spoke unto Moses") ✓;
Num 25:19 / 26:1 split ✓; Deut 23:1 ("A man shall not take his father's wife") ✓; Deut 34:12 (last verse) ✓.

## 2. Rabbinic Shabbat readings (`rabbinic_readings.py`)

**Sources.** Which portion is read: the app's own fixed-calendar schedule (`fixed_calendar.parshiyot_for_year`). Verse ranges,
maftir and haftarot: hebcal-leyning tables (BSD 2-Clause, v10.1.0, commit dc3e46a15c), shipped unchanged in
`data/readings/rabbinic_leyning.json`. The rules for special Shabbatot were ported from hebcal-leyning's source code.

**Check A – full comparison with the reference program.** The published `@hebcal/leyning` 10.1.0 package (with `@hebcal/core` 6.16.1)
was installed and run under Node.js. For **every Saturday from 5 Jan 1850 to 30 Dec 2149 (15653 Saturdays)**, Israel and
diaspora (**31306 Shabbat schedules**, i.e. the complete Hebrew years 5611–5909 plus the parts of 5610 and 5910 inside the range, in both schedules), the following were compared:
portion or festival, each of the 7 (or more) aliyah ranges, maftir, Ashkenazi haftarah and Sephardi haftarah.

| | Matches | Mismatches |
|---|---|---|
| All fields together | **31,306** | **0** |

This includes, among others, 1,054 Shabbat Rosh Chodesh readings, 762 Machar Chodesh, 164 Chanukah + Rosh Chodesh, 236 Shekalim/HaChodesh on
Rosh Chodesh, every Chol HaMoed Shabbat and every festival Shabbat (counts from the module's own output over the same range).

**Check B – which portion, against a second, independent program.** `pyluach` 2.3.0 computes the weekly portion with its own code.
Agreement with the app's schedule: **31,306 of 31,306** Shabbat schedules (0 differences).

**Check C – the portion boundaries against the manuscript itself.**
* The 54 portions, laid end to end, cover all 5,847 verses exactly once with no gaps: ✓.
* Within each portion the seven aliyot join without gaps: ✓ (0 gaps).
* Each combined pair (e.g. Vayakhel-Pekudei) runs from the start of the first portion to the end of the second: ✓ (7 of 7).
* 53 of the 54 portions begin where the Leningrad Codex has a paragraph break (open or closed section). The one that does not
  is Vayechi (Gen 47:28), the portion traditionally known as "closed", with no break before it. This is expected.

**Limits.** The verse ranges and haftarot come from one source (hebcal-leyning). Check A confirms that the app applies them
exactly as hebcal does, Check B confirms which portion is read, and Check C confirms the portion boundaries. The haftarah
references themselves were not checked against a second published list. Customs other than standard Ashkenazi and Sephardi
(Chabad, Yemenite, Italian, local variants) are not shown.

## 3. Ancient triennial cycle (`triennial_readings.py`, `data/readings/triennial_sedarim.json`)

**What is sourced and what is modelled.** The *sedarim* (the Masoretic divisions of the triennial cycle) are taken from
"Miqra according to the Masorah" (Hebrew Wikisource, CC BY-SA 4.0; parsed edition by B. Denckla). The *calendar of readings* is
a model. No ancient calendar survives, so every result carries `model = True`.

| Check | Result |
|---|---|
| Sedarim, accepted division | **154** (Genesis 43, Exodus 29, Leviticus 23, Numbers 32, Deuteronomy 27), the number usually given (Jewish Encyclopedia, "Triennial Cycle") |
| Seder numbers run 1, 2, 3 … in every book | yes, all 5 books |
| Average length | 38.0 verses (Wikipedia, "Seder (Bible)": about 38 for the Torah) |
| Sedarim, Leningrad division | **167**, the number in the Leningrad Codex's own list of sedarim at the end of the Torah (cited in MAM's notes) |
| Sedarim cover all 5,847 verses exactly once | yes, both divisions |
| Seder starts that are also paragraph breaks in the Leningrad Codex | 140 of 154 (sedarim are length-based, not topic-based, so some start mid-paragraph) |
| Festival and special readings (Mishnah Megillah 3:4–5): each of the 10 distinct incipits is a paragraph start in the Leningrad Codex | 10 of 10 |

**Running the model** (every Saturday in each calendar's range; 0 errors in all 12 combinations):

| Calendar | Cycle | Division | Covered | Complete cycles | Every seder read once, in order | Ordinary Shabbatot per cycle | Shabbatot with two sedarim per cycle | "Cycle complete" Shabbatot |
|---|---|---|---|---|---|---|---|---|
| Observed | 3 yr, nisan | accepted | 1850-03-16 – 2149-03-08 | 99 | 99/99 | 134–142 | 12–20 | 0 |
| Observed | 3 yr, nisan | leningrad | 1850-03-16 – 2149-03-08 | 99 | 99/99 | 134–142 | 25–33 | 0 |
| Observed | 3 yr, tishrei | accepted | 1850-09-14 – 2149-03-08 | 99 | 99/99 | 135–142 | 12–19 | 0 |
| Observed | 3 yr, tishrei | leningrad | 1850-09-14 – 2149-03-08 | 99 | 99/99 | 135–142 | 25–32 | 0 |
| Observed | 3.5 yr, — | accepted | 1851-04-05 – 2149-03-08 | 85 | 85/85 | 155–167 | 0–0 | 502 |
| Observed | 3.5 yr, — | leningrad | 1851-04-05 – 2149-03-08 | 85 | 85/85 | 155–167 | 3–12 | 0 |
| EarlyTemple | 3 yr, nisan | accepted | 1850-03-16 – 2149-03-08 | 99 | 99/99 | 134–142 | 12–20 | 0 |
| EarlyTemple | 3 yr, nisan | leningrad | 1850-03-16 – 2149-03-08 | 99 | 99/99 | 134–142 | 25–33 | 0 |
| EarlyTemple | 3 yr, tishrei | accepted | 1850-09-14 – 2149-03-08 | 99 | 99/99 | 134–142 | 12–20 | 0 |
| EarlyTemple | 3 yr, tishrei | leningrad | 1850-09-14 – 2149-03-08 | 99 | 99/99 | 134–142 | 25–33 | 0 |
| EarlyTemple | 3.5 yr, — | accepted | 1851-04-05 – 2149-03-08 | 85 | 85/85 | 154–166 | 0–0 | 452 |
| EarlyTemple | 3.5 yr, — | leningrad | 1851-04-05 – 2149-03-08 | 85 | 85/85 | 154–166 | 1–13 | 0 |

**What these numbers mean.** A three-year window holds only about 134–142 ordinary Shabbatot, because festival Shabbatot and the four
special Shabbatot of Adar interrupt the cycle. 154 sedarim therefore cannot be read one per Shabbat in exactly three years. The
model reads two sedarim together on the last 12–20 Shabbatot of each cycle. Two cycles in every seven years
(about 3½ years each) give 154–167 ordinary Shabbatot, which fits 154 sedarim with no doubling. This agrees with the long-standing
scholarly argument that the cycle actually ran for about three and a half years.

**Known uncertainties (also stated in the module).** Cycle length (3 vs about 3½ years), starting month (Nisan vs Tishrei vs no
fixed start), number of sedarim (141/154/167), how festivals and special Shabbatot interrupted the cycle, and which year a cycle
began. No triennial haftarot are given, because the source used does not list them.
