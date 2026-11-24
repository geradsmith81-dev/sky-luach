# Sky Luach · לוח השמים

Five calendars of the Jewish and Samaritan traditions (**fixed, observed, Early Temple Period, Karaite and Samaritan**) from NASA JPL astronomy (DE440s via Skyfield).

- **Fixed (rabbinic) · הלוח הקבוע:** the calendar used today (molad, 19-year cycle, postponements), with holidays, fasts, the weekly Torah portion, and Israel or diaspora custom. For 1850–2149 it was checked day by day against pyluach and convertdate, with 0 differences.
- **Observed (sighting) · קידוש החודש על פי הראייה:** a Temple-period reconstruction. Months begin at the first crescent predicted visible from Jerusalem (Yallop or Odeh criteria), and the leap month follows the spring equinox (Rambam, *Kiddush HaChodesh* 4:2).
- **Early Temple Period · לוח תקופת המקדש הקדומה:** months begin at the true astronomical new moon, counted from year 1. It is an astronomical ideal for comparison, not a documented historical calendar.
- **Karaite · לוח הקראים:** months from the sighted crescent (the observed calendar's chain), the barley (aviv) year modelled by the spring equinox, biblical festivals one day each, Shavuot always on a Sunday, and the Karaite fasts.
- **Samaritan · לוח השומרונים:** months from the true new moon at Mount Gerizim (sunset day boundary), the First Month after 11 March (Julian), and the year number advancing at the Sixth Month. It matches 14 of 14 published community dates from 2001 to 2026 (see docs/VALIDATION.md).
- **Traditions · זרמים:** a diagram of the branches of Judaism with the calendar and festival-day custom of each, and buttons that switch to it. The fixed calendar adds a one-day-everywhere (Reform) scheme and Sigd, the Beta Israel festival.
- **Torah reading · קריאת התורה:** on the Today page, the full Shabbat reading in Hebrew and English. Each calendar uses its own tradition: the rabbinic annual cycle, the ancient triennial cycle, the Karaite portions, or the Samaritan portions read from the Samaritan Pentateuch.
- **Hillula days · ימי הילולא:** 36 anniversaries of great tzaddikim, from Moses and Rabbi Shimon bar Yochai to the Baba Sali. Each is a clickable chip with a short history and sources, shown in the fixed, observed and Early Temple calendars.
- **Finds your location** automatically (asks the browser once) and gives **a short history of every holiday** when you click its name.
- **Pages:** Today, Month, Year & holidays (with .ics and .csv downloads), Compare, Cycles, How it works.
- **Design:** proper nouns also appear in Hebrew letters, and the look follows First Temple period art.

See `HOW_IT_WORKS.md` for the rules and sources, and `docs/VALIDATION.md` for the checks.

## Put it online (GitHub + Streamlit Community Cloud)

1. On github.com, create a new **public** repository named `sky-luach`.
2. Choose **Add file → Upload files** and drag in *everything in this folder*. Upload the `assets`, `data`, `docs`, `ephem` and `tools` folders as folders.
3. Browsers often skip the hidden `.streamlit` folder. If it is missing after the upload, choose **Add file → Create new file**, type the name `.streamlit/config.toml`, and paste the *contents* of `config.toml for GitHub (paste).txt` (not its file name). Use that file, not a copy of the desktop settings: it leaves out the this-computer-only address.
4. At https://share.streamlit.io choose **Create app**, select the repository, branch `main` and file `app.py`. Under **Advanced settings** pick **Python 3.12**, then **Deploy**.
5. The first start downloads the NASA JPL file (32.7 MB), which takes about a minute.

## Run locally

Install the exact, checksum-verified versions the app was tested with (Python 3.12 or newer):

```
python -m venv .venv
.venv\Scripts\python -m pip install --require-hashes --only-binary ":all:" -r requirements.txt
.venv\Scripts\python -m streamlit run app.py --server.address 127.0.0.1
```

`requirements.in` lists the direct components; `requirements.txt` is the full lock with SHA-256
hashes (generated with `uv pip compile requirements.in --universal --python-version 3.12
--generate-hashes --only-binary :all:`). The same lock serves Streamlit Community Cloud.

## Dates and data

Dates run from 1850 to 2149. Put de440.bsp in `ephem/` to extend the times and moon phases to 1550–2650; the observed calendar's tables then need rebuilding with `python tools/build_tables.py`.

The Paleo-Hebrew font is Noto Sans Phoenician, © The Noto Project Authors, under the SIL Open Font License (`assets/NotoSansPhoenician_OFL.txt`).

## License

Sky Luach is released under the [MIT License](LICENSE), © 2026 Gerad Smith. Bundled third-party material keeps its own terms; see [THIRD_PARTY.md](THIRD_PARTY.md). This includes the Torah texts for the Shabbat readings: the Masoretic text and JPS 1917 translation (public domain), and the Samaritan Pentateuch of Florentin & Tal (CC BY-NC 4.0, non-commercial). These include the Noto Sans Phoenician font (SIL Open Font License, `assets/NotoSansPhoenician_OFL.txt`), the NASA JPL DE440s ephemeris, and the GeoNames town list (CC BY 4.0).

## Security and privacy

- The Windows desktop copy of Sky Luach listens on this computer only (127.0.0.1). "Share on this network.bat" can open it to the local network, protected by a new password each time; only the person at the computer sees Quit and data-clearing controls.
- The desktop copy keeps its data and logs in `%LOCALAPPDATA%\SkyLuach`, checks its program files against `MANIFEST.sha256` at every start, and each release publishes SHA-256 checksums of its zips in `SHA256SUMS.txt`.
- All components are pinned to exact versions and installed with `--require-hashes`.
- The desktop-only code (`desktop.py`) does nothing on a hosted copy: no Quit button is shown there.
- The app stores nothing about its visitors: location, town searches and settings live only in the open browser session. On the desktop copy, the only stored file is a downloaded copy of the JPL ephemeris, and only if the shipped `ephem/de440s.bsp` is missing.
