# Third-party material in Sky Luach

Sky Luach's own code and the data tables it generates (`data/crescents_jerusalem.csv.gz`, `data/seasons.csv`) are under the MIT License in `LICENSE`. The items below are not covered by that license. They keep their own terms.

| Item | Where | Source and terms |
|---|---|---|
| Noto Sans Phoenician font | `assets/NotoSansPhoenician-Regular.ttf` | © The Noto Project Authors. SIL Open Font License 1.1; full text in `assets/NotoSansPhoenician_OFL.txt`. |
| NASA JPL planetary ephemeris DE440s | `ephem/de440s.bsp` (bundled in the desktop package; downloaded on first start otherwise) | Produced by the Solar System Dynamics group, Jet Propulsion Laboratory, and distributed freely by JPL. Reference: R. S. Park, W. M. Folkner, J. G. Williams and D. H. Boggs, "The JPL Planetary and Lunar Ephemerides DE440 and DE441", *Astronomical Journal* 161:105 (2021). |
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
