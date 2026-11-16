# Third-party material in Sky Luach

Sky Luach's own code (including the reading modules, except where noted) and the data tables it generates (`data/crescents_jerusalem.csv.gz`, `data/seasons.csv`) are under the MIT License in `LICENSE`. The items below are not covered by that license. They keep their own terms.

| Item | Where | Source and terms |
|---|---|---|
| Noto Sans Phoenician font | `assets/NotoSansPhoenician-Regular.ttf` | © The Noto Project Authors. SIL Open Font License 1.1; full text in `assets/NotoSansPhoenician_OFL.txt`. |
| NASA JPL planetary ephemeris DE440s | `ephem/de440s.bsp` (bundled in the desktop package; downloaded on first start otherwise) | Produced by the Solar System Dynamics group, Jet Propulsion Laboratory, and distributed freely by JPL. Reference: R. S. Park, W. M. Folkner, J. G. Williams and D. H. Boggs, "The JPL Planetary and Lunar Ephemerides DE440 and DE441", *Astronomical Journal* 161:105 (2021). |
| Hebrew Torah text | `data/readings/torah_mt.json.gz` | Westminster Leningrad Codex, via the Open Scriptures Hebrew Bible (github.com/openscriptures/morphhb). The text is in the public domain. |
| English Torah translation | `data/readings/torah_mt.json.gz` | *The Holy Scriptures According to the Masoretic Text* (Jewish Publication Society, 1917). Public domain. |
| Rabbinic reading tables | `data/readings/rabbinic_leyning.json`, `rabbinic_readings.py` | Ported from hebcal-leyning (github.com/hebcal/hebcal-leyning), BSD 2-Clause License, © 2020 hebcal; the licence text is in the data file's `meta`. |
| Triennial sedarim | `data/readings/triennial_sedarim.json` | Seder divisions from *Miqra according to the Masorah* (ed. Seth (Avi) Kadish, Hebrew Wikisource), **CC BY-SA 4.0**. This file may be reused only under that licence, with attribution. |
| Samaritan Pentateuch (Hebrew and English) | `data/readings/torah_sp.json.gz`, `data/readings/sp_qissot.json` | Moshe Florentin and Abraham Tal, *The Samaritan Pentateuch: An English Translation with a Parallel Annotated Hebrew Text* (Open Book Publishers, 2024), https://doi.org/10.11647/OBP.0415. **CC BY-NC 4.0: non-commercial use only.** |
| Karaite portions and haftarot | `data/readings/karaite_parashot.json` | Verse references as published by the Karaite Jews of America (karaites.org). These are factual references; no text is copied. |
| Samaritan Sabbath portions | `samaritan_readings.py` | Portion list and ranges as published by the Israelite Samaritan community (the-samaritans.net). These are factual references; no text is copied. |
| Town and city list | read at run time from the `geonamescache` package | Derived from GeoNames (geonames.org), licensed under Creative Commons Attribution 4.0. |

## Python packages

These are installed separately from PyPI (`requirements.txt`), not copied into this repository. Each has its own license:

- streamlit: Apache-2.0
- skyfield: MIT
- numpy: BSD-3-Clause
- pandas: BSD-3-Clause
- matplotlib: Matplotlib License (PSF-based)
- pillow: MIT-CMU (HPND)
- geonamescache: MIT
- tzdata: Apache-2.0

## Methods

The calendar arithmetic is implemented from published descriptions, and no code from those sources is included. The main sources are E. M. Reingold and N. Dershowitz, *Calendrical Calculations* (4th ed., 2018), Maimonides' *Kiddush HaChodesh*, Yallop (1997) and Odeh (2004). The full list is in `HOW_IT_WORKS.md` and `docs/VALIDATION.md`.

## Note on non-commercial material

The Samaritan Pentateuch files are licensed for non-commercial use only (CC BY-NC 4.0). Sky Luach is free and non-commercial. Anyone who reuses Sky Luach commercially must remove or replace those two files.
