# Sky Luach — validation report

Generated 2026-11-13 with Skyfield 1.54, ephemeris JPL DE440s, pyluach 2.3.0, convertdate 2.5.1.

## 1. Fixed (Hillel II) calendar — checked against two independent libraries

| Check | Span | Items | Mismatches |
|---|---|---|---|
| Hebrew date of every civil day vs **pyluach** | 1 Jan 1850 – 31 Dec 2149 | 109,573 days | **0** |
| Hebrew date of every civil day vs **convertdate** | same | 109,573 days | **0** |
| Round trip Hebrew → civil → Hebrew | same | 109,573 days | **0** |
| Weekly Torah portion on every Shabbat vs pyluach (Israel and diaspora) | AM 5611–5909 | 31,210 Shabbat readings | **0** |
| Festivals, Chol HaMoed and the five fasts (incl. Shabbat postponements) vs pyluach, Israel scheme | 1850–2149 | 11,509 holiday-days | **0** |
| Same, diaspora scheme (second festival days) | 1850–2149 | 12,409 holiday-days | **0** |
| Molad of every month (weekday, hour, parts) vs pyluach | AM 5610–5910 | 3,723 months | **0** |

Not covered by pyluach, checked by hand instead:

- Israeli national days, including the postponement rules: Yom HaAtzmaut 27 Apr 2004 (first year of the Monday rule), 14 May 2024 and 1 May 2025; Yom HaShoah 24 Apr 2025. All match.
- Birkat HaChamah, from the tekufah of Shmuel: the engine gives 11 dates in 1850–2149: 07 Apr 1869, 07 Apr 1897, 08 Apr 1925, 08 Apr 1953, 08 Apr 1981, 08 Apr 2009, 08 Apr 2037, 08 Apr 2065, 08 Apr 2093, 09 Apr 2121, 09 Apr 2149. Five of them (8 Apr 1925, 1953, 1981, 2009 and 2037) were checked against recorded observances and match. The others follow from the same 28-year arithmetic. The move from 7 to 8 to 9 April comes from the Gregorian calendar leaving out the leap days of 1900 and 2100. Tekufat Nisan 5769 is computed at 6 pm on Tuesday 7 Apr 2009, the start of Wednesday, as tradition requires.

## 2. Astronomy — checked against NASA JPL Horizons

Twelve evenings were sampled evenly from 1850 to 2150. At each crescent "best time" in Jerusalem, Horizons gave airless topocentric altitude and azimuth for the Sun and Moon, from which ARCV and ARCL were rebuilt.

| Evening (Jerusalem) | ARCV diff (″) | ARCL diff (″) | Sunset diff (s) |
|---|---|---|---|
| 1850-01-13 | -0.00 | +0.07 | +0.02 |
| 1876-11-17 | -0.03 | +0.03 | +0.02 |
| 1904-02-19 | +0.16 | +0.03 | +0.02 |
| 1931-01-19 | -0.08 | +0.16 | +0.02 |
| 1958-07-17 | -0.10 | +0.11 | +0.02 |
| 1985-08-18 | +0.32 | -0.24 | +0.55 |
| 2013-03-14 | +0.05 | -0.23 | +0.21 |
| 2040-09-08 | +0.24 | +0.46 | -0.13 |
| 2068-02-06 | +4.43 | +4.79 | -0.11 |
| 2095-07-04 | +7.79 | +11.50 | -0.07 |
| 2122-10-02 | +12.95 | +20.48 | -0.04 |
| 2150-01-01 | +31.77 | +36.97 | +0.11 |

- **1850–2040:** ARCV and ARCL agree within 0.46″, which is the table's rounding (0.0001° = 0.36″).
- **After 2040:** differences grow to 37″ by 2150. This is not an ephemeris error. Future ΔT (the slowing of Earth's rotation) is unknown, and Skyfield and Horizons extrapolate it differently. The Moon moves about 0.5″ per second, so a gap of a few tens of seconds in ΔT shifts it by tens of arcseconds. That is about 0.01°, far too small to change a visibility verdict.
- **Sunset:** Horizons puts the Sun's centre at −0.833° (the standard sunset definition) within 0.55 s of the app's sunset time on every sample evening.
- **New moons:** at the app's conjunction instants, Horizons' geocentric Moon−Sun ecliptic longitude is 0.00–0.01″, i.e. under 0.1 s of time.

## 3. Observational calendar — internal checks (rules as modelled; default: Yallop B, true equinox, equinox ≤ 15 Nisan)

- 298 complete years (AM 5611–5908). Every year has 12 or 13 months, and 110 have 13.
- Month lengths: 1736 of 29 days and 1962 of 30 days (53.1% long months; the mean synodic month of 29.53 days implies about 53%).
- Shavuot (50th day of the Omer) falls on 5 Sivan in 45 years, 6 Sivan in 222 years, 7 Sivan in 31 years.
- 1 Tishrei (observed) minus 1 Tishrei (fixed), in days: {-30: 11, -29: 20, -28: 34, -27: 9, 0: 34, 1: 117, 2: 69, 3: 4}. A value near 0 to +2 means the month is the same and begins 0–2 days later than the fixed calendar, because first visibility comes after the conjunction and the molad. Values near −30 mean the observed year has already intercalated relative to the fixed one. With the true equinox this happens in about a quarter of years, because the fixed calendar's year is the year of Rav Adda (365.2468 d), longer than the tropical year (365.2422 d). Since Hillel II it has drifted about 7 days against the equinox.


## 3b. Early Temple Period calendar (true new moon) — checks

- The month starts were computed twice, once from the app's Jerusalem table and once directly from the JPL ephemeris. The day-1 dates are identical for all 3,711 true new moons (1850–2150).
- The equinox rule gives 298 complete years (AM 5611–5908), of which 110 have 13 months. Months: 1,736 of 29 days and 1,962 of 30 days.
- The 19-year-cycle rule gives 299 complete years, with leap years identical to the fixed calendar in every year. Its Pesach falls on the fixed date in 137 years, 1 day earlier in 60, 1 day later in 100 and 2 days later in 2.
- New-month start minus fixed-calendar start, over all 3,711 months: −2 d: 124; −1 d: 1,164; same day: 1,790; +1 d: 622; +2 d: 11.
- New-month start minus observed start: −2 d: 292; −1 d: 2,956; same day: 450.
- Molad minus true conjunction, 3,709 months: mean +2.00 h, standard deviation 7.51 h, range −12.3 to +16.3 h.
- Rosh Hashanah weekdays in 299 years: Saturday 52, Thursday 49, Tuesday 46, Monday 45, Wednesday 38, Sunday 37, Friday 32. The fixed calendar allows only Monday, Tuesday, Thursday and Saturday.

## 4. What is *not* validated

- The crescent criteria come from published models: Yallop 1997, NAO Technical Note 69; Odeh 2004, *Experimental Astronomy* 18:39–64. Their formulas are implemented as published, but the app has not been tested against a sighting record for Jerusalem. Real sightings also depend on weather, haze, observer skill and practice. The observational calendar is therefore a reasoned reconstruction, not a record of any historical or present-day practice.
- The leap-month rule (equinox no later than 15 Nisan, after Rambam, Kiddush HaChodesh 4:2) stands in for the *aviv* (barley ripeness) and the other considerations the Sanhedrin weighed. Those cannot be computed.
- The Early Temple Period calendar is an astronomical ideal. No historical source documents a conjunction-based Jewish calendar.
- Dates outside 1850–2149 need the larger de440.bsp (1550–2650) in the ephem folder. The precomputed crescent tables would then also need rebuilding (tools/build_tables.py).
