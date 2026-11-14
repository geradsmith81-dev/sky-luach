"""
Branches of Judaism (and the Samaritans), and the calendar each one keeps.

The diagram follows the structure of a widely shared mind map of the branches (Samaritan, Karaite,
Orthodoxy, Masorti/Conservative -> Reconstructionist, Reform, small modern groups, Beta Israel,
Messianic Judaism). It is redrawn here from scratch in the app's own style - no image is copied.
"""
from __future__ import annotations

import html
import math

import ornaments as orn

IVORY = "#f3e9d2"
MUTED = "#dccdab"
GOLD = "#e8bd5c"
CEDAR = "#1a120c"
PANEL = "#2a1d13"

# calendar keys used in the table -> (label, Hebrew)
CAL = {
    "samaritan": ("Samaritan calendar", "לוח השומרונים"),
    "karaite": ("Karaite calendar", "לוח הקראים"),
    "fixed2": ("Fixed calendar · two festival days outside Israel", "הלוח הקבוע · יום טוב שני"),
    "fixed1": ("Fixed calendar · one day everywhere", "הלוח הקבוע · יום אחד"),
    "fixedmix": ("Fixed calendar · practice varies", "הלוח הקבוע"),
    "beta": ("Fixed calendar + Sigd (today); own lunar reckoning in Ethiopia", "הלוח הקבוע וסיגד"),
    "messianic": ("Fixed calendar, mostly", "הלוח הקבוע"),
}

TAG = {"samaritan": "Samaritan calendar", "karaite": "Karaite calendar", "fixed2": "Fixed · 2 days outside Israel",
       "fixed1": "Fixed · one day", "fixedmix": "Fixed · practice varies", "beta": "Fixed + Sigd",
       "messianic": "Fixed (mostly)"}
TAG_X = 975

# (name, Hebrew, short description, colour, calendar key, note on festival days, sub-branches)
# sub-branch: (name, Hebrew, short description, calendar key, note)
BRANCHES = [
    ("Samaritan", "שומרונים", "Torah (Samaritan Pentateuch) and Samaritan oral tradition", "#c08a4e", "samaritan",
     "Their own calculated calendar, set by the priests; festivals one day; pilgrimages to Mount Gerizim; "
     "Shavuot always on a Sunday. Festivals often fall a month after the Jewish dates.", []),
    ("Karaite", "קראים", "Written Torah only; rejects the rabbinic Oral Torah", "#e3994a", "karaite",
     "Months from the sighted crescent, the year from the barley (aviv) in the Land of Israel; biblical "
     "festivals one day each; Shavuot on a Sunday; no Chanukah.", []),
    ("Orthodoxy", "אורתודוקסיה", "Torah given by God; halakha binding", "#b097e0", "fixed2",
     "Fixed rabbinic calendar; one festival day in Israel, two outside Israel (Yom Tov Sheni).",
     [("Modern Orthodox", "אורתודוקסיה מודרנית", "", "fixed2", ""),
      ("Chasidim", "חסידים", "", "fixed2", ""),
      ("Haredi (Yeshivish)", "חרדים (ישיבתיים)", "", "fixed2", ""),
      ("Yemenite Orthodox", "תימנים", "", "fixed2", "")]),
    ("Masorti / Conservative", "יהדות מסורתית", "Torah inspired by God; halakha observed", "#ec6f68",
     "fixed2", "Fixed calendar; most congregations outside Israel keep two days; a one-day option has been "
     "accepted by the movement's law committee, and some congregations follow it.",
     [("Reconstructionist", "יהדות רקונסטרוקציונית", "", "fixed1", "most congregations keep one day")]),
    ("Reform", "יהדות רפורמית", "Torah inspired by God; halakha not binding", "#4fb8c4", "fixed1",
     "Fixed calendar; one day for each festival, including (in most congregations) Rosh Hashanah.", []),
    ("Small modern groups", "זרמים קטנים", "", "#8fa8ec", "fixedmix", "",
     [("Humanistic", "יהדות הומניסטית", "non-theistic", "fixed1", "cultural observance, one day"),
      ("Classical Reform", "רפורמה קלאסית", "religion rather than ethnicity", "fixed1", "one day"),
      ("Neolog", "ניאולוגים", "Hungarian, moderately traditional", "fixed2", "second days kept, as in the diaspora"),
      ("Jewish Renewal", "התחדשות יהודית", "counter-cultural, spiritual", "fixedmix", "varies; often one day"),
      ("Jewish Science", "מדע יהודי", "counterpart to Christian Science", "fixedmix", "follows Reform-style practice")]),
    ("Beta Israel (Ethiopia)", "ביתא ישראל", "Orit (Ge'ez Octateuch) and priestly (qessotch) tradition", "#ee9fbd",
     "beta", "In Ethiopia a lunar calendar of their own, with festivals such as Sigd; in Israel today mostly the "
     "fixed rabbinic calendar, with Sigd on 29 Marcheshvan (a state holiday since 2008).", []),
    ("Messianic Judaism", "יהדות משיחית", "heterodox; regarded by Jewish denominations as a form of Christianity",
     "#6fc283", "messianic", "Most congregations use the fixed rabbinic calendar; a few follow sighted-moon or "
     "Karaite-style reckoning.", []),
]


def _t(x, y, text, size=15, color=IVORY, weight="normal", anchor="start", he=False, italic=False):
    fam = ("'Frank Ruehl CLM','David','Times New Roman',serif" if he
           else "'Palatino Linotype',Palatino,'Book Antiqua',Georgia,serif")
    extra = " direction='rtl'" if he else ""
    st = " font-style='italic'" if italic else ""
    return (f"<text x='{x:.1f}' y='{y:.1f}' font-family=\"{fam}\" font-size='{size}' fill='{color}' "
            f"font-weight='{weight}' text-anchor='{anchor}'{extra}{st}>{html.escape(text)}</text>")


def diagram_svg() -> str:
    """The branch mind map, redrawn: root cartouche at left, curved branches, calendar tags."""
    W = 1200
    rows = []            # (y, level, item)
    y = 46
    for b in BRANCHES:
        rows.append((y, 0, b))
        y += 50 if not b[6] else 40
        for sb in b[6]:
            rows.append((y, 1, sb, b))
            y += 34
        if b[6]:
            y += 14
    H = y + 24
    rx, ry = 92, H / 2
    out = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}'>",
           f"<rect x='0' y='0' width='{W}' height='{H}' rx='14' fill='{PANEL}'/>",
           f"<rect x='4' y='4' width='{W - 8}' height='{H - 8}' rx='11' fill='none' stroke='{GOLD}' stroke-opacity='.45'/>"]
    branch_end = {}
    for r in rows:
        yy, lvl = r[0], r[1]
        if lvl == 0:
            name, he, desc, col, cal, note, subs = r[2]
            x0, x1 = 230, 580
            # tapering ribbon from the root to the label underline
            sy = ry + (yy - ry) * 0.12          # spread the roots along the cartouche
            sx = rx + 62
            out.append(f"<path d='M{sx},{sy - 9} C{sx + 70},{sy - 9} {x0 - 100},{yy + 3} {x0},{yy + 3} "
                       f"L{x0},{yy + 8} C{x0 - 100},{yy + 8} {sx + 70},{sy + 9} {sx},{sy + 9} Z' "
                       f"fill='{col}' fill-opacity='.9'/>")
            out.append(f"<rect x='{x0}' y='{yy + 3}' width='{x1 - x0}' height='4' rx='2' fill='{col}'/>")
            out.append(_t(x0 + 6, yy - 4, name, 17, IVORY, "bold"))
            out.append(_t(x1 - 4, yy - 4, he, 17, GOLD, anchor="end", he=True))
            if desc:
                out.append(_t(x0 + 6, yy + 22, desc, 12.5, MUTED, italic=True))
            branch_end[name] = (x1, yy + 5, col)
            if not subs:
                out.append(f"<line x1='{x1 + 8}' y1='{yy + 5}' x2='{TAG_X - 10}' y2='{yy + 5}' stroke='{GOLD}' "
                           f"stroke-opacity='.5' stroke-dasharray='2 5'/>")
                out.append(_t(TAG_X, yy + 10, TAG[cal], 15, GOLD, "bold"))
        else:
            name, he, desc, cal, note = r[2]
            parent = r[3]
            px, py, col = branch_end[parent[0]]
            x0, x1 = px + 45, px + 345
            out.append(f"<path d='M{px},{py} C{px + 30},{py} {x0 - 30},{yy + 5} {x0},{yy + 5}' fill='none' "
                       f"stroke='{col}' stroke-width='3'/>")
            out.append(f"<rect x='{x0}' y='{yy + 3}' width='{x1 - x0}' height='3' rx='1.5' fill='{col}'/>")
            label = name + (f" — {desc}" if desc else "")
            out.append(_t(x0 + 4, yy - 3, label, 14, IVORY))
            out.append(f"<line x1='{x1 + 8}' y1='{yy + 5}' x2='{TAG_X - 10}' y2='{yy + 5}' stroke='{GOLD}' "
                       f"stroke-opacity='.5' stroke-dasharray='2 5'/>")
            out.append(_t(TAG_X, yy + 9, TAG[cal], 14, GOLD))
    # root cartouche
    out.append(f"<ellipse cx='{rx}' cy='{ry}' rx='80' ry='40' fill='{CEDAR}' stroke='{GOLD}' stroke-width='2.5'/>")
    out.append(_t(rx, ry - 3, "Judaism", 20, IVORY, "bold", "middle"))
    out.append(_t(rx, ry + 21, "יהדות", 18, GOLD, anchor="middle", he=True))
    out.append(_t(TAG_X, 26, "Calendar kept · הלוח", 13, MUTED, italic=True))
    out.append(_t(W - 16, H - 12, "Redrawn after a popular mind map of the branches; Samaritans are Israelites "
                  "but not Jews in their own view.", 10.5, MUTED, anchor="end", italic=True))
    out.append("</svg>")
    return "".join(out)


def diagram_uri() -> str:
    return orn.data_uri(diagram_svg())
