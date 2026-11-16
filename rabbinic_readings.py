"""Rabbinic (annual-cycle) Shabbat Torah readings and haftarot for Sky Luach.

What it does
------------
``reading_for_shabbat(d, cal=None, israel=True)`` returns the Torah reading, maftir and
haftarot (Ashkenazi and Sephardi) for the Shabbat ``d`` according to the fixed rabbinic
calendar (Hillel II), for 1 Jan 1850 - 31 Dec 2149, in the Land of Israel
(``israel=True``) or the diaspora (``israel=False``).  It returns ``None`` when ``d`` is not
a Saturday or lies outside that range.  ``cal`` is accepted for a uniform interface with
the other reading modules and is ignored: the rabbinic schedule is always computed on the
fixed calendar (``fixed_calendar``).

Rules
-----
1. Which portion (parashah, or a combined pair such as Vayakhel-Pekudei) is read on a
   Shabbat comes from ``fixed_calendar.parshiyot_for_year`` - the app's existing schedule
   (Israel and diaspora), which was validated separately.  A Shabbat with no portion is a
   festival Shabbat.
2. Verse ranges of the seven aliyot and the regular maftir of each portion, and the regular
   haftarot, come from the hebcal-leyning table ``aliyot.json``.  For a combined pair the
   haftarah is that of the second portion, except Nitzavim-Vayeilech (Nitzavim) and
   Achrei Mot-Kedoshim (its own entry), as in hebcal-leyning.
3. Special readings follow the decision procedure of hebcal-leyning
   (``specialReadings.ts``, ``getLeyningKeyForEvent.ts``), applied to dates computed by
   ``fixed_calendar``:
   * Shabbat Shuvah (Shabbat between 3 and 9 Tishrei): haftarah "Shabbat Shuva (with
     Vayeilech / Ha'azinu)".
   * Shabbat Chanukah (25 Kislev - 2/3 Tevet): Chanukah maftir for that day from Numbers 7
     and haftarah Zechariah 2:14-4:7 (1 Kings 7:40-50 on the second Shabbat, day 8);
     on Shabbat Rosh Chodesh Tevet the seventh aliyah is the Rosh Chodesh reading
     (Num 28:9-15) and the maftir is the Chanukah reading.
   * The four parshiyot - Shekalim (Shabbat on or before 1 Adar / Adar II), Zachor
     (Shabbat before Purim), Parah (Shabbat before HaChodesh), HaChodesh (Shabbat on or
     before 1 Nisan) - with their maftir and haftarah; Shekalim or HaChodesh falling on
     Rosh Chodesh add the Rosh Chodesh reading as the seventh aliyah.
   * Shabbat HaGadol (Shabbat before Pesach): haftarah Malachi 3:4-24.
   * When no special haftarah has been set by the above: Pinchas after 17 Tammuz takes
     Jeremiah 1:1-2:3; Shabbat Rosh Chodesh (day 30 or 1) takes maftir Num 28:9-15 and
     haftarah Isaiah 66 (Masei / Matot-Masei have their own Rosh Chodesh form);
     Ki Teitzei on 14 Elul adds the third haftarah of consolation; Kedoshim on 26/28 Nisan
     or 6 Iyyar takes Amos 9:7-15 (Sephardi Ezekiel 20:2-20); and outside Av a Shabbat on
     the eve of Rosh Chodesh is Shabbat Machar Chodesh (1 Samuel 20:18-42).
   * Shabbat Chazon (Devarim, Isaiah 1) and Shabbat Nachamu (Va'etchanan, Isaiah 40) are
     labelled; their haftarot are the regular haftarot of those portions.
   * Festival Shabbatot use the festival readings in ``holiday-readings.json``:
     Rosh Hashanah I, Yom Kippur, Sukkot I, Shabbat Chol HaMoed Sukkot (maftir of the
     Chol HaMoed day: Israel day = Tishrei day - 15, diaspora = Tishrei day - 16),
     Shemini Atzeret (diaspora) or Shemini Atzeret-Simchat Torah (Israel), Pesach I,
     Shabbat Chol HaMoed Pesach, Pesach VII, Pesach VIII (diaspora), Shavuot II (diaspora).
4. Haftarah labels: "Ashkenazi" and "Sephardi" when hebcal-leyning gives a separate
   Sephardi haftarah; otherwise a single entry labelled "Ashkenazi and Sephardi".
   (Chabad and other local customs that hebcal-leyning also lists are not shown.)

Sources
-------
* hebcal-leyning: Hebcal Jewish calendar project, "@hebcal/leyning" v10.1.0, GitHub
  repository hebcal/hebcal-leyning, commit dc3e46a15ccf4e1bdc9802e32d7c807ffb8065b5
  (fetched 16 Nov 2026), files src/aliyot.json, src/holiday-readings.json,
  src/numverses.json and the logic in src/specialReadings.ts and
  src/getLeyningKeyForEvent.ts.  BSD 2-Clause License, Copyright (c) 2020, hebcal.
  The tables are shipped unchanged in data/readings/rabbinic_leyning.json together with
  the licence text.
* Calendar dates: Sky Luach ``fixed_calendar`` (Hillel II calendar: molad, 19-year
  cycle, dehiyyot).

Known uncertainties
-------------------
* Customs differ between communities (Ashkenazi, Sephardi, Chabad, Yemenite, Italian,
  ...).  Only the Ashkenazi and Sephardi haftarot of hebcal-leyning are given; some
  communities differ on, e.g., Shabbat HaGadol on the eve of Pesach, Shabbat Machar
  Chodesh coinciding with Chanukah, or the Shabbat Shuvah haftarah.
* Shushan Purim on Shabbat (Purim Meshulash) concerns Jerusalem and walled cities only;
  it is reported in ``note`` (Israel schedule) and does not change the reading returned.
* Verse numbers follow the standard Jewish (and JPS 1917) versification used by
  data/readings/torah_mt.json.gz.
* Validation: the full output for every Shabbat 1850-2149, Israel and diaspora, was
  compared with the reference implementation (@hebcal/leyning ``getLeyningOnDate``);
  see Rabbinic_VALIDATION.md.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
from functools import lru_cache

import fixed_calendar as fc

try:  # Hebrew portion names already used by the app
    from hebrew_names import PARSHA_HE as _PARSHA_HE
except Exception:  # pragma: no cover
    _PARSHA_HE = None

FIRST_DATE = _dt.date(1850, 1, 1)
LAST_DATE = _dt.date(2149, 12, 31)
BOOK = ["", "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]
_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(_HERE, "data", "readings", "rabbinic_leyning.json")

# ---------------------------------------------------------------- display names
_SPECIAL_NAMES = {  # hebcal key -> (English label, Hebrew label)
    "Rosh Hashana I (on Shabbat)": ("Rosh Hashanah I", "ראש השנה א׳"),
    "Yom Kippur (on Shabbat)": ("Yom Kippur", "יום כיפור"),
    "Sukkot I (on Shabbat)": ("Sukkot I", "סוכות א׳"),
    "Sukkot Shabbat Chol ha-Moed": ("Shabbat Chol HaMoed Sukkot", "שבת חול המועד סוכות"),
    "Shmini Atzeret (on Shabbat)": ("Shemini Atzeret", "שמיני עצרת"),
    "Simchat Torah (on Shabbat)": ("Shemini Atzeret - Simchat Torah", "שמיני עצרת - שמחת תורה"),
    "Pesach I (on Shabbat)": ("Pesach I", "פסח א׳"),
    "Pesach Shabbat Chol ha-Moed": ("Shabbat Chol HaMoed Pesach", "שבת חול המועד פסח"),
    "Pesach VII (on Shabbat)": ("Pesach VII", "שביעי של פסח"),
    "Pesach VIII (on Shabbat)": ("Pesach VIII", "אחרון של פסח"),
    "Shavuot II (on Shabbat)": ("Shavuot II", "שבועות ב׳"),
    "Shabbat Shuva": ("Shabbat Shuvah", "שבת שובה"),
    "Shabbat Shekalim": ("Shabbat Shekalim", "שבת שקלים"),
    "Shabbat Shekalim (on Rosh Chodesh)": ("Shabbat Shekalim; Rosh Chodesh", "שבת שקלים, ראש חודש"),
    "Shabbat Zachor": ("Shabbat Zachor", "שבת זכור"),
    "Shabbat Parah": ("Shabbat Parah", "שבת פרה"),
    "Shabbat HaChodesh": ("Shabbat HaChodesh", "שבת החודש"),
    "Shabbat HaChodesh (on Rosh Chodesh)": ("Shabbat HaChodesh; Rosh Chodesh", "שבת החודש, ראש חודש"),
    "Shabbat HaGadol": ("Shabbat HaGadol", "שבת הגדול"),
    "Shabbat Rosh Chodesh": ("Shabbat Rosh Chodesh", "שבת ראש חודש"),
    "Masei on Shabbat Rosh Chodesh": ("Shabbat Rosh Chodesh", "שבת ראש חודש"),
    "Matot-Masei on Shabbat Rosh Chodesh": ("Shabbat Rosh Chodesh", "שבת ראש חודש"),
    "Shabbat Rosh Chodesh Chanukah": ("Shabbat Chanukah; Rosh Chodesh", "שבת חנוכה, ראש חודש"),
    "Shabbat Machar Chodesh": ("Shabbat Machar Chodesh", "שבת מחר חודש"),
    "Pinchas occurring after 17 Tammuz": ("First Shabbat of the Three Weeks", "שבת ראשונה של בין המצרים"),
    "Ki Teitzei with 3rd Haftarah of Consolation": ("Ki Teitzei with the 3rd haftarah of consolation",
                                                     "כי תצא עם הפטרת נחמה שלישית"),
    "Kedoshim following Special Shabbat": ("", ""),
}

_BOOK_HE_NOTE = {"Song of Songs": "Song of Songs", "Ecclesiastes": "Ecclesiastes", "Ruth": "Ruth"}


@lru_cache(maxsize=1)
def _data() -> dict:
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- verse helpers
def _cv(s: str) -> tuple[int, int]:
    c, v = s.split(":")
    return int(c), int(v)


def _next_verse(book: str, ref: str) -> str:
    c, v = _cv(ref)
    nv = _data()["chapter_verses"][book]
    return f"{c + 1}:1" if v >= nv[c] else f"{c}:{v + 1}"


def _merge(ranges: list[tuple[str, str, str]]) -> list[dict]:
    """Merge consecutive (book, from, to) ranges that are contiguous or overlapping."""
    out: list[list[str]] = []
    for k, b, e in ranges:
        if out and out[-1][0] == k:
            pk, pb, pe = out[-1]
            if _cv(b) <= _cv(_next_verse(k, pe)) and _cv(b) >= _cv(pb):
                if _cv(e) > _cv(pe):
                    out[-1][2] = e
                continue
        out.append([k, b, e])
    return [{"book": k, "from": b, "to": e} for k, b, e in out]


def _book_display(k: str) -> str:
    if k.startswith("II "):
        return "2 " + k[3:]
    if k.startswith("I "):
        return "1 " + k[2:]
    return k


def _fmt_haft(parts) -> str:
    if isinstance(parts, dict):
        parts = [parts]
    out, prev = [], None
    for p in parts:
        k, b, e = p["k"], p["b"], p["e"]
        cb, _ = _cv(b)
        ce, ve = _cv(e)
        rng = b if b == e else (f"{b}-{ve}" if cb == ce else f"{b}-{e}")
        out.append(rng if k == prev else f"{_book_display(k)} {rng}")
        prev = k
    return "; ".join(out)


def _as_list(h):
    if h is None:
        return None
    return [dict(x) for x in (h if isinstance(h, list) else [h])]


# ---------------------------------------------------------------- lookups
def _festival(key: str) -> dict | None:
    fest = _data()["festivals"]
    src = fest.get(key)
    if src is None:
        return None
    if src.get("alias"):
        src = fest[src["key"]]
    src = json.loads(json.dumps(src))
    for grp in ("fullkriyah", "alt"):
        for a in (src.get(grp) or {}).values():
            if isinstance(a.get("k"), int):
                a["k"] = BOOK[a["k"]]
    return src


def _parsha_aliyot(name: str) -> dict:
    raw = _data()["parshiyot"][name]
    book = BOOK[raw["book"]]
    return {n: {"k": book, "b": src[0], "e": src[1]} for n, src in raw["fullkriyah"].items()}


def _haftara_key(parsha: list[str]) -> str:
    if len(parsha) == 2 and parsha[0] == "Achrei Mot":
        return "-".join(parsha)
    if len(parsha) == 1 or parsha[0] == "Nitzavim":
        return parsha[0]
    return parsha[1]


def _is_rc(day: int) -> bool:
    return day in (1, 30)


def _event_keys(hd: fc.HDate, rd: int, parsha_name: str, israel: bool) -> list[str]:
    """hebcal-leyning keys of events (other than Rosh Chodesh) on a portion Shabbat."""
    keys: list[str] = []
    y, m, day = hd.year, hd.month, hd.day
    # Shabbat Shuvah
    if m == fc.TISHREI and 3 <= day <= 9:
        keys.append(f"Shabbat Shuva (with {parsha_name})")
    # Chanukah: day n = days since 24 Kislev (1..8)
    n = rd - fc.to_rd(y, fc.KISLEV, 24)
    if 1 <= n <= 8:
        keys.append("Shabbat Rosh Chodesh Chanukah" if _is_rc(day) else f"Chanukah Day {n} (on Shabbat)")
    # four parshiyot and Shabbat HaGadol (dates from fixed_calendar)
    for h in fc.special_shabbatot_for_year(y):
        if h.date.toordinal() != rd:
            continue
        nm = {"Shabbat Shekalim": "Shabbat Shekalim", "Shabbat Zachor": "Shabbat Zachor",
              "Shabbat Parah": "Shabbat Parah", "Shabbat HaChodesh": "Shabbat HaChodesh",
              "Shabbat HaGadol": "Shabbat HaGadol"}.get(h.name)
        if nm:
            if nm in ("Shabbat Shekalim", "Shabbat HaChodesh") and _is_rc(day):
                nm += " (on Rosh Chodesh)"
            keys.append(nm)
    return keys


def _festival_key(hd: fc.HDate, israel: bool) -> tuple[str, int | None]:
    m, day = hd.month, hd.day
    if m == fc.TISHREI:
        if day == 1:
            return "Rosh Hashana I (on Shabbat)", None
        if day == 10:
            return "Yom Kippur (on Shabbat)", None
        if day == 15:
            return "Sukkot I (on Shabbat)", None
        if 16 <= day <= 21:
            chm = day - 15 if israel else day - 16
            if chm >= 1:
                return "Sukkot Shabbat Chol ha-Moed", chm
            return "Sukkot II", None
        if day == 22:
            return ("Simchat Torah (on Shabbat)" if israel else "Shmini Atzeret (on Shabbat)"), None
    if m == fc.NISAN:
        if day == 15:
            return "Pesach I (on Shabbat)", None
        if day == 21:
            return "Pesach VII (on Shabbat)", None
        if day == 22 and not israel:
            return "Pesach VIII (on Shabbat)", None
        if 16 <= day <= 20:
            return ("Pesach Shabbat Chol ha-Moed" if (israel or day >= 17) else "Pesach II"), None
    if m == fc.SIVAN:
        if day == 6:
            return "Shavuot I", None
        if day == 7 and not israel:
            return "Shavuot II (on Shabbat)", None
    raise ValueError(f"no festival reading known for Shabbat {hd} (israel={israel})")


def leyning_raw(d: _dt.date, israel: bool = True) -> dict | None:
    """hebcal-style intermediate result (used by the validation script):
    {"key", "parsha" (list or None), "aliyot" {num: {k,b,e}}, "haft" [..], "seph" [..]|None,
     "reasons" [keys], "megillah"}"""
    if d.weekday() != 5 or not (FIRST_DATE <= d <= LAST_DATE):
        return None
    rd = d.toordinal()
    hd = fc.from_gregorian(d)
    idx = fc.parshiyot_for_year(hd.year, israel).get(rd)
    if idx is None:  # safety: look in the neighbouring year table
        idx = fc.parshiyot_for_year(hd.year - 1, israel).get(rd, [])
    if not idx:  # festival Shabbat
        key, chm = _festival_key(hd, israel)
        src = _festival(key)
        fk = dict(src.get("fullkriyah") or {})
        if key == "Sukkot Shabbat Chol ha-Moed" and chm:
            fk["M"] = fk[f"M-day{chm}"]
        fk = {n: a for n, a in fk.items() if not n.startswith("M-day")}
        return {"key": key, "parsha": None, "aliyot": fk, "haft": _as_list(src.get("haft")),
                "seph": _as_list(src.get("seph")), "reasons": [key], "megillah": src.get("megillah"),
                "hd": hd}

    parsha = [fc.PARSHIYOT[i] for i in idx]
    pname = "-".join(parsha)
    aliyot = _parsha_aliyot(pname)
    hk = _haftara_key(parsha)
    praw = _data()["parshiyot"][hk]
    haft, seph = _as_list(praw.get("haft")), _as_list(praw.get("seph"))
    reasons: list[str] = []
    special_haft = False

    def handle(key: str):
        nonlocal aliyot, haft, seph, special_haft
        sp = _festival(key)
        if not sp:
            return
        if isinstance(sp.get("il"), bool) and sp["il"] != israel:
            return
        used = False
        if sp.get("haft") and not special_haft:
            haft, seph, special_haft, used = _as_list(sp["haft"]), _as_list(sp.get("seph")), True, True
        if sp.get("fullkriyah"):
            al = json.loads(json.dumps(aliyot))
            spk = sp["fullkriyah"]
            if "7" in spk:
                a6, a7 = al["6"], al.pop("7")
                al["6"] = {"k": a6["k"], "b": a6["b"], "e": a7["e"]}
                al["7"] = dict(spk["7"])
            if "M" in spk:
                al["M"] = dict(spk["M"])
            aliyot, used = al, True
        if used or sp.get("note"):
            reasons.append(key)

    for key in _event_keys(hd, rd, pname, israel):
        handle(key)
    day = hd.day
    if not special_haft:
        if pname == "Pinchas" and day > 17:
            handle("Pinchas occurring after 17 Tammuz")
        elif _is_rc(day):
            handle(f"{pname} on Shabbat Rosh Chodesh" if pname in ("Masei", "Matot-Masei")
                   else "Shabbat Rosh Chodesh")
        elif pname == "Ki Teitzei" and day == 14:
            handle("Ki Teitzei with 3rd Haftarah of Consolation")
        elif pname == "Kedoshim" and day in (26, 28, 6):
            handle("Kedoshim following Special Shabbat")
        elif hd.month != fc.AV:
            tomorrow = fc.from_rd(rd + 1).day
            if tomorrow in (30, 1):
                handle("Shabbat Machar Chodesh")
    for a in aliyot.values():
        for kk in ("p", "v", "reason"):
            a.pop(kk, None)
    return {"key": pname, "parsha": parsha, "aliyot": aliyot, "haft": haft, "seph": seph,
            "reasons": reasons, "megillah": None, "hd": hd}


def _order(n: str) -> tuple:
    return (1, 0) if n == "M" else (0, int(n))


def reading_for_shabbat(d: _dt.date, cal=None, israel: bool = True, **opts) -> dict | None:
    """Rabbinic Shabbat reading for ``d`` (see module docstring).  ``cal`` is ignored."""
    raw = leyning_raw(d, israel)
    if raw is None:
        return None
    hd = raw["hd"]
    nums = sorted((n for n in raw["aliyot"] if n != "M"), key=_order)
    torah = _merge([(raw["aliyot"][n]["k"], raw["aliyot"][n]["b"], raw["aliyot"][n]["e"]) for n in nums])
    maftir = ([{"book": raw["aliyot"]["M"]["k"], "from": raw["aliyot"]["M"]["b"], "to": raw["aliyot"]["M"]["e"]}]
              if "M" in raw["aliyot"] else [])
    haft = []
    if raw["haft"]:
        a = _fmt_haft(raw["haft"])
        s = _fmt_haft(raw["seph"]) if raw["seph"] else a
        haft = ([{"label": "Ashkenazi and Sephardi", "ref": a}] if s == a else
                [{"label": "Ashkenazi", "ref": a}, {"label": "Sephardi", "ref": s}])

    specials_en, specials_he, notes = [], [], []
    if raw["parsha"] is None:
        name_en, name_he = _SPECIAL_NAMES.get(raw["key"], (raw["key"], raw["key"]))
        specials_en.append(name_en)
        specials_he.append(name_he)
        if raw["key"] == "Sukkot I (on Shabbat)" and israel:
            notes.append("Ecclesiastes is read today (Ashkenazi custom in Israel).")
        elif raw["megillah"]:
            notes.append(f"{raw['megillah']} is also read (Ashkenazi custom).")
    else:
        name_en = raw["key"]
        idx = [fc.PARSHIYOT.index(p) for p in raw["parsha"]]
        name_he = "-".join(_PARSHA_HE[i] for i in idx) if _PARSHA_HE else name_en
        for k in raw["reasons"]:
            if k.startswith("Shabbat Shuva"):
                k = "Shabbat Shuva"
            if k.startswith("Chanukah Day"):
                n = k.split()[2]
                en, he = f"Shabbat Chanukah (day {n})", f"שבת חנוכה (יום {fc.hebrew_numeral(int(n))})"
            else:
                en, he = _SPECIAL_NAMES.get(k, (k, k))
            if en:
                specials_en.append(en)
                specials_he.append(he)
        for h in fc.special_shabbatot_for_year(hd.year):
            if h.date == d and h.name in ("Shabbat Chazon", "Shabbat Nachamu"):
                specials_en.append(h.name)
                specials_he.append(h.hebrew)
        if raw["parsha"] == ["Beshalach"]:
            specials_en.append("Shabbat Shirah")
            specials_he.append("שבת שירה")
        if israel and hd.month in (fc.ADAR, fc.ADAR_II) and hd.day == 15 and \
                hd.month == (fc.ADAR_II if fc.is_leap(hd.year) else fc.ADAR):
            notes.append("Shushan Purim falls on this Shabbat: in Jerusalem and walled cities the maftir is "
                         "Exodus 17:8-16 with the haftarah of Shabbat Zachor.")
    notes.append("Readings from the hebcal-leyning tables (BSD licence); local customs vary in places.")
    return {
        "date": d.isoformat(),
        "tradition": "rabbinic",
        "name_en": name_en,
        "name_he": name_he,
        "torah": torah,
        "maftir": maftir,
        "haftarah": haft,
        "special": "; ".join(specials_en),
        "special_he": "; ".join(s for s in specials_he if s),
        "text": "mt",
        "model": False,
        "note": " ".join(notes),
    }
