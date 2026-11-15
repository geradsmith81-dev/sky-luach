# Sky Luach · לוח השמים

Five calendars of the Jewish and Samaritan traditions (**fixed, observed, Early Temple Period, Karaite and Samaritan**) from NASA JPL astronomy (DE440s via Skyfield).

- **Fixed (rabbinic) · הלוח הקבוע:** the calendar used today (molad, 19-year cycle, postponements), with holidays, fasts, the weekly Torah portion, and Israel or diaspora custom. For 1850–2149 it was checked day by day against pyluach and convertdate, with 0 differences.
- **Observed (sighting) · קידוש החודש על פי הראייה:** a Temple-period reconstruction. Months begin at the first crescent predicted visible from Jerusalem (Yallop or Odeh criteria), and the leap month follows the spring equinox (Rambam, *Kiddush HaChodesh* 4:2).
- **Early Temple Period · לוח תקופת המקדש הקדומה:** months begin at the true astronomical new moon, counted from year 1. It is an astronomical ideal for comparison, not a documented historical calendar.
- **Karaite · לוח הקראים:** months from the sighted crescent (the observed calendar's chain), the barley (aviv) year modelled by the spring equinox, biblical festivals one day each, Shavuot always on a Sunday, and the Karaite fasts.
- **Samaritan · לוח השומרונים:** months from the true new moon at Mount Gerizim (sunset day boundary), the First Month after 11 March (Julian), and the year number advancing at the Sixth Month. It matches 14 of 14 published community dates from 2001 to 2026 (see docs/VALIDATION.md).
- **Traditions · זרמים:** a diagram of the branches of Judaism with the calendar and festival-day custom of each, and buttons that switch to it. The fixed calendar adds a one-day-everywhere (Reform) scheme and Sigd, the Beta Israel festival.
- **Finds your location** automatically (asks the browser once) and gives **a short history of every holiday** when you click its name.
- **Pages:** Today, Month, Year & holidays (with .ics and .csv downloads), Compare, Cycles, How it works.
- **Design:** proper nouns also appear in Hebrew letters, and the look follows First Temple period art.

See `HOW_IT_WORKS.md` for the rules and sources, and `docs/VALIDATION.md` for the checks.

## Put it online (GitHub + Streamlit Community Cloud)

1. On github.com, create a new **public** repository named `sky-luach`.
2. Choose **Add file → Upload files** and drag in *everything in this folder*. Upload the `assets`, `data`, `docs`, `ephem` and `tools` folders as folders.
3. Browsers often skip the hidden `.streamlit` folder. If it is missing after the upload, choose **Add file → Create new file**, type the name `.streamlit/config.toml`, and paste the *contents* of `config.toml for GitHub (paste).txt` (not its file name).
4. At https://share.streamlit.io choose **Create app**, select the repository, branch `main` and file `app.py`. Under **Advanced settings** pick **Python 3.12**, then **Deploy**.
5. The first start downloads the NASA JPL file (32.7 MB), which takes about a minute.

## Run it on a computer

```
pip install -r requirements.txt
streamlit run app.py
```

Dates run from 1850 to 2149. Put de440.bsp in `ephem/` to extend the times and moon phases to 1550–2650; the observed calendar's tables then need rebuilding with `python tools/build_tables.py`.

The Paleo-Hebrew font is Noto Sans Phoenician, © The Noto Project Authors, under the SIL Open Font License (`assets/NotoSansPhoenician_OFL.txt`).

## License

Sky Luach is released under the [MIT License](LICENSE), © 2026 Gerad Smith. Bundled third-party material keeps its own terms; see [THIRD_PARTY.md](THIRD_PARTY.md). These include the Noto Sans Phoenician font (SIL Open Font License, `assets/NotoSansPhoenician_OFL.txt`), the NASA JPL DE440s ephemeris, and the GeoNames town list (CC BY 4.0).
