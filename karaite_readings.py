"""
Karaite weekly Torah readings for Sky Luach (Karaite calendar).

reading_for_shabbat(d, cal=None) -> dict | None gives the portion read on a Sabbath in the app's Karaite
calendar (karaite_calendar.KaraiteCalendar: Jerusalem-crescent months, equinox stand-in for the aviv,
one-day festivals, Shavuot always on a Sunday). The text shown is the Masoretic text (text = "mt").

WHAT IS SOURCED
1. Portions and haftarot. The 54 portions, their verse ranges and their haftarot follow the list of the
   Karaite Jews of America (Egyptian Karaite tradition) [KJA-A], with the verse ranges checked against the
   KJA commentary page of each portion [KJA-P]. The portion boundaries are the same as the rabbinic ones
   (54 of 54 match the hebcal-leyning table); the haftarot are mostly different. The haftarot are compared
   with an older printed Karaite list, Seder ha-Haftarot (Kale, 1733) [KALE]; where KALE differs it is
   offered as a second haftarah. Data: data/readings/karaite_parashot.json (tools/build_karaite_parashot.py).
2. The year's cycle ends and begins on Yom Simhat Torah, the 22nd of the seventh month (Shemini Atzeret):
   Vezot Haberakha is read and Bereshit is begun from a second scroll [ELK].
3. Naso is always read on the Sabbath before Shavuot, i.e. on the eve of the Sunday Shavuot [SAR, p. 27].
4. Balak, Pinhas, Matot, Masei and Devarim are the portions of the mourning period before the destruction
   of the Temple, read with a special haftarah melody [KJA-A]. On "the Saturdays from the 9th of Tammuz
   until the 10th of Av, four or five special prayers are read" [ELK]. This module therefore puts those
   portions on the Sabbaths from 9 Tammuz to 10 Av inclusive (4 or 5 Sabbaths in every year).
5. Haazinu is read on both Sabbaths between Yom Teruah and Sukkot [SAR, p. 19].
6. The haftarot of Va'etchanan..Nitzavim [KJA-A] are the seven "consolation" readings of Isaiah, which
   implies seven Sabbaths from 10 Av to Yom Teruah - the usual count in this calendar (280 of 297 years).

WHAT IS A MODEL (model = True on every result)
* The months themselves are the app's astronomical crescent model, and the year start uses the equinox in
  place of the aviv inspection; a real Karaite year can differ by a day per month or by a whole month.
* Combining rules are NOT documented in the sources found. This module fills each stretch between anchors
  as follows (stretch: portions -> Sabbaths available in 5611-5907):
  - Bereshit..Bamidbar (34 portions) between Simhat Torah and the Naso Sabbath, skipping the festival
    Sabbath of Unleavened Bread (29-31 Sabbaths in a common year, 34-35 in a leap year).
    Join, in this order, Tazria+Metzora, Acharei Mot+Kedoshim, Behar+Bechukotai, Vayakhel+Pekudei
    (the pairs the rabbinic calendar joins); if still too many portions, join the shortest adjacent pair of
    single portions (by verse count). If there is one Sabbath too many (19 leap years in 297), Tetzaveh is
    read over two Sabbaths, split at Exodus 29:1, after a historical (non-Karaite) custom of halving
    portions in leap years described by Sar-Shalom [SAR, p. 21]; a second spare Sabbath would split Ki Tissa
    at 32:15 (does not occur in 5611-5907).
  - Beha'alotekha..Chukat between Shavuot and 9 Tammuz (4 Sabbaths, 3 in 19 years). With 3 Sabbaths,
    Chukat is read with Balak (Chukat-Balak, a rabbinic pair) on the first Sabbath of the mourning period.
  - Balak..Devarim from 9 Tammuz to 10 Av: 5 Sabbaths -> one each; 4 Sabbaths -> Matot-Masei joined.
  - Va'etchanan..Vayelech from 11 Av to the eve of Yom Teruah: 8 Sabbaths -> one each; 7 -> Nitzavim-Vayelech
    joined; 6 (3 years) -> also the shortest adjacent pair of single portions.
* When two portions are read together, every haftarah of both is listed; which one is read is not
  documented. A split second half gets no haftarah.
* Festival Sabbaths (Yom Teruah, Yom Kippur, Sukkot 15-21 Tishrei, Unleavened Bread 15-21 Nisan) pause the
  weekly cycle. Their Karaite Torah reading is not in the sources used, so "torah" is empty and the
  festival is named in "special". On a Sabbath that is Yom Simhat Torah (22 Tishrei) Vezot Haberakha is
  given, with the beginning of Bereshit mentioned in the note (its extent is not given in the source).
* No maftir: no Karaite maftir is documented in the sources, so "maftir" is always [].

SOURCES
[KJA-A] Karaite Jews of America, "Torah Audio - Karaite Parashiot and Haftarot",
        https://karaites.org/torah-audio/ (read 16 Nov 2026).
[KJA-P] Karaite Jews of America, "Torah Portions" and the per-portion commentary pages,
        https://karaites.org/torah-portions/ (read 16 Nov 2026).
[ELK]   Mourad el-Kodsi, The Karaite Jews of Egypt from 1882-1985 (title as given on the KJA page), sections
        "Yom Simhat Torah" and "Days of Fasting and Mourning", as reproduced ("pages copied and scanned") by the KJA at
        https://karaites.org/karaite-customs-and-traditons/ (read 16 Nov 2026).
[SAR]   Rahamim Sar-Shalom, "Parashat ha-shavua - mi-minhagim shonim le-minhag ahid", Shana be-Shana 5754
        (1994), https://www.daat.ac.il/daat/kitveyet/shana/sarshalom-2.pdf (page numbers of that PDF).
[KALE]  Seder ha-Haftarot, Kale (Gozleve) 1733, Karaite column as tabulated in Aaron Marsh, "The Sequential
        Triennial Cycle: A History and Guide to its Modern Use", Master's project, Academy for Jewish
        Religion, 2015, Table 2, pp. 36-38.

KNOWN UNCERTAINTIES
* No published dated Karaite schedule (a calendar listing the portion of each Sabbath) was found, so the
  dates are not checked against one; see Karaite_VALIDATION.md.
* Many Karaite synagogues began the annual cycle in Nisan before the 15th century [Karaite Korner, Bible FAQ, https://www.karaite-korner.org/bible_faq.shtml];
  this module follows the present KJA practice (cycle ends and begins on 22 Tishrei).
* KJA-A gives Vaera the same haftarah as Vayyera; KALE gives Isaiah 42:8-43:5. Both are offered.
"""
from __future__ import annotations

import json
import os
from datetime import date, timedelta
from functools import lru_cache

import fixed_calendar as fc

_HERE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_HERE, "data", "readings", "karaite_parashot.json")
TISHREI, NISAN, SIVAN, TAMMUZ, AV = 7, 1, 3, 4, 5

# index (0-based) of portions
BERESHIT, TETZAVEH, KI_TISSA, VAYAKHEL, TAZRIA, ACHAREI, BEHAR, BAMIDBAR, NASO = 0, 19, 20, 21, 26, 28, 31, 33, 34
BEHAALOTEKHA, CHUKAT, BALAK, MATOT, DEVARIM, VAETCHANAN, NITZAVIM, VAYELECH, HAAZINU, VEZOT = 35, 38, 39, 41, 43, 44, 50, 51, 52, 53
_PAIRS_A = [TAZRIA, ACHAREI, BEHAR, VAYAKHEL]          # first index of each preferred pair
_SPLITS = [(TETZAVEH, "29:1"), (KI_TISSA, "32:15")]      # (portion, first verse of part 2)

_cal = None


def _default_cal():
    global _cal
    if _cal is None:
        import karaite_calendar
        _cal = karaite_calendar.KaraiteCalendar()
    return _cal


@lru_cache(maxsize=1)
def _data():
    with open(_DATA, encoding="utf-8") as f:
        return json.load(f)


def _P(i):
    return _data()["parashot"][i]


def _sabbaths(a: date, b: date) -> list[date]:
    """Saturdays with a <= d <= b."""
    d = a + timedelta(days=(5 - a.weekday()) % 7)
    out = []
    while d <= b:
        out.append(d)
        d += timedelta(days=7)
    return out


def _shavuot(cal, y):
    n15 = cal.to_gregorian(y, NISAN, 15)
    wave = next(n15 + timedelta(days=k) for k in range(7) if (n15 + timedelta(days=k)).weekday() == fc.SUNDAY)
    return wave + timedelta(days=49)


def _fit(units, n, pairs=(), allow_split=False):
    """Fit a list of units (each a list of (portion, part)) into n Sabbaths. Returns (units, rules used)."""
    units = [list(u) for u in units]
    rules = []
    single = lambda u: len(u) == 1 and u[0][1] is None
    for p in pairs:
        if len(units) <= n:
            break
        for k in range(len(units) - 1):
            if single(units[k]) and units[k][0][0] == p and single(units[k + 1]):
                units[k:k + 2] = [units[k] + units[k + 1]]
                rules.append("pair")
                break
    while len(units) > n:
        best = None
        for k in range(len(units) - 1):
            if single(units[k]) and single(units[k + 1]):
                v = _P(units[k][0][0])["verses"] + _P(units[k + 1][0][0])["verses"]
                if best is None or v < best[0]:
                    best = (v, k)
        if best is None:
            raise ValueError("cannot fit portions")
        k = best[1]
        units[k:k + 2] = [units[k] + units[k + 1]]
        rules.append("shortest")
    if allow_split:
        for p, _ in _SPLITS:
            if len(units) >= n:
                break
            k = next(k for k, u in enumerate(units) if u == [(p, None)])
            units[k:k + 1] = [[(p, 1)], [(p, 2)]]
            rules.append("split")
    if len(units) != n:
        raise ValueError(f"{len(units)} units for {n} Sabbaths")
    return units, rules


@lru_cache(maxsize=512)
def _year_schedule(y: int, cal_id: int) -> dict:
    """Schedule of the reading year that starts after 22 Tishrei of year y and ends on 22 Tishrei of y+1."""
    cal = _CALS[cal_id]
    g = cal.to_gregorian
    st, nxt = g(y, TISHREI, 22), g(y + 1, TISHREI, 22)
    shav, tam9, av10, yt = _shavuot(cal, y), g(y, TAMMUZ, 9), g(y, AV, 10), g(y + 1, TISHREI, 1)
    fest = {}
    for k in range(15, 22):
        fest[g(y, NISAN, k)] = ("Feast of Unleavened Bread (Chag HaMatzot)", "חג המצות")
    fest[yt] = ("Yom Teruah", "יום תרועה")
    fest[g(y + 1, TISHREI, 10)] = ("Yom Kippur", "יום הכפורים")
    for k in range(15, 22):
        fest[g(y + 1, TISHREI, k)] = ("Sukkot", "חג הסוכות")
    sched = {}
    for d in _sabbaths(st + timedelta(days=1), nxt):
        if d in fest:
            sched[d] = ("festival", fest[d], [])
    seg = lambda a, b: [d for d in _sabbaths(a, b) if d not in fest]
    A = seg(st + timedelta(days=1), shav - timedelta(days=1))
    naso_day, A = A[-1], A[:-1]
    B = seg(shav + timedelta(days=1), tam9 - timedelta(days=1))
    W = seg(tam9, av10)
    D = seg(av10 + timedelta(days=1), yt - timedelta(days=1))
    E = seg(yt + timedelta(days=1), nxt - timedelta(days=1))
    one = lambda a, b: [[(i, None)] for i in range(a, b + 1)]
    ua, ra = _fit(one(BERESHIT, BAMIDBAR), len(A), _PAIRS_A, allow_split=True)
    ub = one(BEHAALOTEKHA, CHUKAT)
    uw = one(BALAK, DEVARIM)
    rb = []
    if len(B) < len(ub):                    # Chukat moves into the mourning period as Chukat-Balak
        ub = ub[:-1]
        uw[0] = [(CHUKAT, None)] + uw[0]
        rb = ["chukat-balak"]
    ub, rb2 = _fit(ub, len(B))
    uw, rw = _fit(uw, len(W), [MATOT])
    ud, rd = _fit(one(VAETCHANAN, VAYELECH), len(D), [NITZAVIM])
    for days, units, rules in ((A, ua, ra), (B, ub, rb + rb2), (W, uw, rw), (D, ud, rd)):
        for d, u in zip(days, units):
            sched[d] = ("cycle", u, rules)
    sched[naso_day] = ("cycle", [(NASO, None)], ["anchor"])
    for d in E:
        sched[d] = ("cycle", [(HAAZINU, None)], ["anchor"])
    if nxt.weekday() == 5:
        sched[nxt] = ("simhat", None, [])
    return sched


_CALS: dict[int, object] = {}


def _ref(p, part=None):
    if part == 1:
        z = next(s for q, s in _SPLITS if q == p["num"] - 1)
        ch, v = map(int, z.split(":"))
        keys = list(_mt_keys(p["book"]))
        to = keys[keys.index(z) - 1]
        return {"book": p["book"], "from": p["from"], "to": to}
    if part == 2:
        z = next(s for q, s in _SPLITS if q == p["num"] - 1)
        return {"book": p["book"], "from": z, "to": p["to"]}
    return {"book": p["book"], "from": p["from"], "to": p["to"]}


@lru_cache(maxsize=8)
def _mt_keys(book):
    import gzip
    with gzip.open(os.path.join(_HERE, "data", "readings", "torah_mt.json.gz"), "rt", encoding="utf-8") as f:
        return tuple(json.load(f)["books"][book].keys())


def _haftarot(unit):
    out = []
    multi = len({p for p, _ in unit}) > 1
    for p, part in unit:
        if part == 2:
            continue
        P = _P(p)
        tag = f" - for {P['name_en']}" if multi else ""
        out.append({"label": "Karaite (KJA)" + tag, "ref": P["haftarah"]})
        k = P.get("haftarah_kale_1733")
        if k and P["haftarah"].replace(" ", "") not in [o.replace(" ", "") for o in k.split(" or ")]:
            out.append({"label": "Karaite (Kale 1733)" + tag, "ref": k})
    return out


def reading_for_shabbat(d: date, cal=None, **opts) -> dict | None:
    """Karaite reading for the Sabbath d, or None if d is not a Saturday or outside the calendar's range."""
    if not isinstance(d, date) or d.weekday() != 5:
        return None
    cal = cal or _default_cal()
    _CALS[id(cal)] = cal
    hd = cal.from_gregorian(d)
    if hd is None:
        return None
    y = hd.year - 1 if (hd.month == TISHREI and hd.day <= 22) else hd.year
    if not (cal.year_complete(y) and cal.year_complete(y + 1)):
        return None
    try:
        kind, val, rules = _year_schedule(y, id(cal))[d]
    except (KeyError, ValueError, StopIteration):
        return None
    base = {"date": d.isoformat(), "tradition": "karaite", "maftir": [], "text": "mt", "model": True}
    if kind == "festival":
        en, he = val
        return {**base, "name_en": en, "name_he": he, "torah": [], "haftarah": [],
                "special": f"Sabbath of {en}",
                "note": ("Festival Sabbath: the weekly cycle pauses. The Karaite reading for this festival is not in "
                         "the sources used for this app." + (" Karaites read a lament for Moses after the haftarah on "
                         "the Sabbath of Sukkot (el-Kodsi)." if en == "Sukkot" else ""))}
    if kind == "simhat":
        P = _P(VEZOT)
        return {**base, "name_en": P["name_en"], "name_he": P["name_he"], "torah": [_ref(P)],
                "haftarah": _haftarot([(VEZOT, None)]), "special": "Yom Simhat Torah (Shemini Atzeret)",
                "note": ("On Yom Simhat Torah Vezot Haberakha completes the Torah and Bereshit is begun from a second "
                         "scroll (el-Kodsi); the length of the Bereshit reading is not given.")}
    names_en, names_he, torah = [], [], []
    for p, part in val:
        P = _P(p)
        suffix_en = {1: " (part 1)", 2: " (part 2)"}.get(part, "")
        suffix_he = {1: " (א)", 2: " (ב)"}.get(part, "")
        names_en.append(P["name_en"] + suffix_en)
        names_he.append(P["name_he"] + suffix_he)
        torah.append(_ref(P, part))
    notes = []
    if "anchor" in rules and val[0][0] == NASO:
        notes.append("Karaites always read Naso on the Sabbath before Shavuot, which they keep on a Sunday.")
    if BALAK <= val[0][0] <= DEVARIM or (len(val) > 1 and val[1][0] == BALAK):
        notes.append("A portion of the mourning period before the destruction of the Temple (9 Tammuz to 10 Av); "
                     "its haftarah is chanted in a special melody.")
    if len(val) > 1 and val[0][1] is None:
        notes.append("Read together this year to fit the year (model rule); which haftarah is read is not documented.")
    if val[0][1] is not None:
        notes.append("This portion is read over two Sabbaths this year (model rule for a year with a spare Sabbath).")
    if not notes:
        notes.append("Annual cycle as kept by the Karaite Jews of America; the placement of each portion is a model.")
    return {**base, "name_en": "-".join(names_en), "name_he": "-".join(names_he), "torah": torah,
            "haftarah": _haftarot(val), "special": "", "note": " ".join(notes)}


def year_readings(y: int, cal=None) -> list[dict]:
    """All Sabbath readings of the reading year that begins after 22 Tishrei of year y (for tables/tests)."""
    cal = cal or _default_cal()
    _CALS[id(cal)] = cal
    return [reading_for_shabbat(d, cal) for d in sorted(_year_schedule(y, id(cal)))]
