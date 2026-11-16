"""Samaritan Sabbath Torah readings for Sky Luach.

reading_for_shabbat(d, cal=None) -> dict | None
    d   : datetime.date (must be a Saturday)
    cal : samaritan_calendar.SamaritanCalendar (created on first use if omitted)
Returns None if d is not a Saturday or lies outside the calendar's table (1850-2149).
The dict follows the Sky Luach reading contract (tradition "samaritan", text "sp").

WHAT IS PUBLISHED (sources 1-3) AND WHAT IS INFERRED (marked model=True)
--------------------------------------------------------------------------
Published by the community:
* The 54 Samaritan weekly portions, with their verse ranges and the "additional verse" read
  with each, come from the community's Table of the weekly Parashot (source 1). Hebrew names come
  from the 2017 version of that table and are checked against the opening words of the
  Samaritan text. Together the 54 ranges cover all 5,954 verses of torah_sp.json.gz exactly once.
  50 of the 54 boundaries fall on a qissa (section) end of Ms. Nablus 6.
* The cycle starts and ends on the Sabbath after Shemini Atzeret, the Eighth Day of Assembly (source 2).
  The last portion, Ve-Haya ki Yavo'u, is read on the last ordinary Sabbath before Sukkot (source 3).
* The 2004-2006 community monthly calendars (source 3) give 84 dated Sabbaths. Rules a-f below are
  inferred from them:
  a. First month: the two Sabbaths on days 1-14 read Va-Yikra and Tsav. The Sabbath on days 15-21
     is the Sabbath of the Feast of Unleavened Bread and has no weekly portion.
  b. The seven Sabbaths of the Omer follow. Sabbaths 1-6 (Sea, Marah, Elim, Manna, Rock, Amalek)
     read the other six portions of Leviticus. The 7th Sabbath, the Sabbath of the Commandments
     (Devarim), has no portion. Shavuot is the next day.
  c. From the first Sabbath after Shavuot, Numbers and Deuteronomy are read in order, 17 portions,
     up to the last ordinary Sabbath before Sukkot.
  d. These Sabbaths have no weekly portion: the Feast of the Seventh Month (day 1) if it falls on a
     Sabbath; the Sabbath of the Selihot (the first Sabbath on days 2-9 of the seventh month); the
     Day of Atonement (day 10); the Sabbath of Sukkot (days 15-21); the Eighth Day of Assembly (day 22).
  e. From the Sabbath after the Eighth Day of Assembly to the last Sabbath before the next First
     Month, Genesis and Exodus are read, 29 portions.
  f. When a stretch has fewer Sabbaths than portions, adjacent portions are joined.
Inferred, not published (model):
* Which portions are joined, and how many. In 1850-2149 the winter stretch (e) needs 6 or 7 joins in
  common years and 2 or 3 in leap years. The Numbers-Deuteronomy stretch (c) needs 0-2 joins.
  - Common years, 7 joins: the joins of 2004-05 (source 3): Bereshit + Ve-Ha'adam Yada (that
    calendar prints only "Bereshit"; joining Ve-Ha'adam Yada to it is an assumption),
    Ve-Yada Adam + Ve-Ani Hineni, Va-Yissa + Va-Yakam, Va-Tetse + Va-Yeshev, Va-Yavo Yosef +
    Ve-Elle Shemot, El Shaddai + Ben Porat, Ha-Chodesh + Va-Yassa. 6 joins: the same joins
    without Bereshit + Ve-Ha'adam Yada (not attested).
  - Leap years: Ve-Ha'adam Yada + Ve-Yada Adam (attested 21 Oct 2006). The other one or two joins are
    not attested. The model takes the shortest of the 2004-05 pairs: El Shaddai + Ben Porat, then
    Va-Yavo Yosef + Ve-Elle Shemot (Genesis).
  - Numbers-Deuteronomy: 1 join = Ki Atem + Banim Atem (attested 26 Aug 2006). The second join is
    not attested; the model uses Shoftim + Ki Yikach.
* Special-Sabbath labels:
  - The "wonder" Sabbaths (the plagues) are counted back from the second Sabbath of the First
    Month (darkness), one plague per Sabbath. This matches all 7 dated wonder Sabbaths found
    (2004, 2006, 2015).
  - Rules d and e at their edges (a Sabbath on day 1 or day 22 of the seventh month) are not
    attested.
* Deviations from the community table:
  - Shoftim is taken to end at Deut 22:12 and Ki Yikach Ish Isha to start at 22:13, not 22:11/22:12.
    The portion's name is the opening of 22:13, and the manuscript's qissa ends after 22:12.
  - "Ki Tissa - Numbers 30:11-16" in the table is Exodus 30:11-16 (its Hebrew incipit is
    "כי תשא את ראש").
  - "Shemor - Exodus 20:8-12" is the Sabbath commandment. In the edition's numbering that is
    Exodus 20:7-10, and the Deuteronomy Shemor (Deut 5:12-15 in Masoretic numbering) is Deut 5:11-14.
    "Torah tsiva lanu Moshe..." is given as Deut 33:4. The table names only that verse's opening words.
* The edition's qissa sign falls inside Gen 8:21 ("...the pleasing odour: And the LORD said in his
  heart"). The table starts El Libo at 8:21 and ends Ve-Ani Hineni at 8:20; this module follows it.
* What is read on the Sabbaths that have no weekly portion is not documented in the sources used.
  For those Sabbaths torah is [].

HAFTARAH
Samaritans have no haftarah: their canon is the five books of the Torah only (source 4). So
haftarah is always [].

SOURCES
1. The Samaritans (community site, A. Sassoni ed.), "Table of the weekly Parashot (Portions of the
   week)", https://www.the-samaritans.net/table-weekly-parashot-portions-week/ (accessed 16 Nov 2026).
   Earlier versions: http://www.the-samaritans.com/calendar/Parashot.htm (Internet Archive,
   30 Oct 2004) and http://www.the-samaritans.com/calendar-2/ (Internet Archive, 6 Mar 2017, with
   Hebrew names and a glossary of special Sabbaths).
2. Israelite Samaritan Information Institute, "Sukkot", https://www.israelite-samaritans.com/religion/sukkah/
   (also published on TheTorah.com). Quote: "we do not begin and end our Torah reading cycle on Shemini Atzeret
   ... but on the Shabbat following Shemini Atzeret".
3. The-Samaritans.com monthly calendars, Apr 2004 - Dec 2006 (20 pages, e.g.
   http://www.the-samaritans.com/calendar/2006/SepOct06.htm), via the Internet Archive.
   Also the 2015 event pages "Sabbath Mofet ha-Kinnim / ha-Aareb / ha-Dabar".
4. M. Florentin and A. Tal, The Samaritan Pentateuch: An English Translation with a Parallel
   Annotated Hebrew Text (Cambridge: Open Book Publishers, 2024), https://doi.org/10.11647/OBP.0415.
   Source of the text and the qissa divisions; Samaritans hold the Pentateuch alone as scripture.
5. The month and festival dates come from Sky Luach's samaritan_calendar.py (its own model; see that
   module). In 17 of the 20 months of source 3 it starts the month on the same day as the community;
   in the other 3 it starts a day early. This changes none of the 84 dated readings (see
   docs/Samaritan_VALIDATION.md).

COVERAGE: every Saturday from 13 Apr 1850 to 14 Oct 2147. The last 77 Sabbaths of the calendar table
return None, because the next First Month is not in the table.
"""
from __future__ import annotations

import datetime as _dt
from functools import lru_cache

PORTIONS = [
    ('bereshit', 'Bereshit', 'בראשית', 'Barashet', 'Genesis', '1:1', '3:24', 80, ('shemor_ex',)),
    ('vehaadam', "Ve'Ha'adam Yada", 'והאדם ידע', "Wa'adam yada", 'Genesis', '4:1', '4:24', 24, ('shemor_ex',)),
    ('veyada', "Ve'Yada Adam", 'וידע אדם', 'Wyada adam', 'Genesis', '4:25', '6:16', 50, ('shemor_ex',)),
    ('vaani', "Ve'Ani Hineni", 'ואני הנני', 'Wani innani', 'Genesis', '6:17', '8:20', 50, ('shemor_ex',)),
    ('ellibo', 'El Libo', 'אל לבו', 'Al libbo', 'Genesis', '8:21', '11:32', 95, ('shemor_ex',)),
    ('lechlecha', 'Lech Lecha', 'לך לך', 'Lik lak', 'Genesis', '12:1', '16:16', 99, ('shemor_ex',)),
    ('vayehiavram', "Va'Yehi Avram", 'ויהי אברם', "Way'i abram", 'Genesis', '17:1', '20:18', 116, ('shemor_ex',)),
    ('vehashempakad', "Ve'Hashem Pakad", 'ויהוה פקד', 'Wshema fakad', 'Genesis', '21:1', '23:20', 78, ('shemor_ex',)),
    ('veavrahamzaken', "Ve'Avraham Zaken", 'ואברהם זקן', "Wab'raam zaqen", 'Genesis', '24:1', '25:18', 85, ('shemor_ex',)),
    ('veeletoldot', "Ve'Elle Toldot Yitschak", 'ואלה תולדת יצחק', 'Willa tuldat', 'Genesis', '25:19', '28:22', 119, ('shemor_ex',)),
    ('vayissa', "Va'Yissa Yaakov", 'וישא יעקב', "Wyissa ya'qob", 'Genesis', '29:1', '31:16', 97, ('shemor_ex',)),
    ('vayakam', "Va'Yakam Yaakov", 'ויקם יעקב', "Wyaqam ya'qob", 'Genesis', '31:17', '33:20', 91, ('shemor_ex',)),
    ('vatetse', "Va'Tetse Dina", 'ותצא דינה', 'Wtissa dina', 'Genesis', '34:1', '36:43', 103, ('shemor_ex',)),
    ('vayeshev', "Va'Yeshev Yaakov", 'וישב יעקב', "Wyashab ya'qob", 'Genesis', '37:1', '38:30', 66, ('shemor_ex',)),
    ('veyosefhurad', "Ve'Yosef Hurad", 'ויוסף הורד', 'Wyusef uwwared', 'Genesis', '39:1', '41:49', 95, ('shemor_ex',)),
    ('veleyosef', "Ve'le Yosef Yuldu", 'וליוסף ילדו', 'Walyusef yelidu', 'Genesis', '41:50', '43:25', 71, ('shemor_ex',)),
    ('vayavoyosef', "Va'Yavo Yosef", 'ויבא יוסף', 'Wyaba yusef', 'Genesis', '43:26', '46:7', 78, ('shemor_ex',)),
    ('veeleshemot_g', "Ve'Elle Shemot (Genesis)", 'ואלה שמות', 'Willa shemot', 'Genesis', '46:8', '48:2', 60, ('shemor_ex',)),
    ('elshaddai', 'El Shaddai', 'אל שדי', 'Il shiddi', 'Genesis', '48:3', '49:21', 41, ('shemor_ex',)),
    ('benporat', 'Ben Porat', 'בן פרת', 'Ban farat', 'Genesis', '49:22', '50:26', 38, ('torahtsiva', 'shemor_ex')),
    ('veeleshemot', "Ve'Elle Shemot", 'ואלה שמות', 'Willa shemot', 'Exodus', '1:1', '7:7', 161, ('shemor_ex',)),
    ('kiyedaber', 'Ki Yedaber', 'כי ידבר', 'Ki yedabber', 'Exodus', '7:8', '11:10', 152, ('shemor_ex',)),
    ('hachodesh', "Ha'Chodesh Haze", 'החדש הזה', "Aa'desh azze", 'Exodus', '12:1', '15:21', 125, ('kitissa',)),
    ('vayassa', "Va'Yassa Moshe", 'ויסע משה', 'Wayassa mushi', 'Exodus', '15:22', '18:27', 95, ('shemor_ex',)),
    ('bachodesh', "Ba'Chodesh Ha'Shelishi", 'בחדש השלישי', 'Baadesh asshelishi', 'Exodus', '19:1', '24:18', 182, ('veata',)),
    ('vayikchu', "Va'Yikchu Li Teruma", 'ויקחו לי תרומה', 'Wyiqqau li teruma', 'Exodus', '25:1', '28:43', 152, ('veata',)),
    ('vezehadavar', "Ve'Ze Ha'Davar", 'וזה הדבר', 'Wze addebar', 'Exodus', '29:1', '31:17', 91, ('veshamru',)),
    ('vayiten', "Va'Yiten El Moshe", 'ויתן אל משה', 'Wyitten al mushi', 'Exodus', '31:18', '36:19', 149, ('kedoshim',)),
    ('vayaas', "Va'Yaas et Ha'Kerashim", 'ויעש את הקרשים', 'Wyash it aqqerashem', 'Exodus', '36:20', '40:38', 161, ('torahtsiva',)),
    ('vayikra', "Va'Yikra El Moshe", 'ויקרא אל משה', 'Wyikra al mushi', 'Leviticus', '1:1', '5:26', 111, ('moadei',)),
    ('tsav', 'Tsav et Aharon', 'צו את אהרן', 'Sabi it aarron', 'Leviticus', '6:1', '9:21', 118, ('moadei',)),
    ('vayissaaharon', "Va'Yissa Aharon", 'וישא אהרן', 'Wyissha aarron', 'Leviticus', '9:22', '13:28', 106, ('vesafartem',)),
    ('veish', "Ve'Ish o Isha", 'ואיש או אשה', 'Wish u issha', 'Leviticus', '13:29', '15:33', 121, ('vesafartem',)),
    ('acharei', 'Acharei Mot', 'אחרי מות', "Aa'uri mot", 'Leviticus', '16:1', '19:8', 88, ('vesafartem',)),
    ('uvekatsirchem', "U've'Katsirchem", 'ובקצירכם', "Waf'qaserkimma", 'Leviticus', '19:9', '22:33', 113, ('vesafartem',)),
    ('moadei', 'Moadei', 'מועדי', 'Muwwedi', 'Leviticus', '23:1', '26:2', 124, ('shivaa',)),
    ('imbechukotai', "Im Be'Chukotai", 'אם בחקותי', 'Am baqquti', 'Leviticus', '26:3', '27:34', 78, ('torahtsiva', 'shivaa')),
    ('bemidbar', "Be'Midbar Sinai", 'במדבר סיני', 'Bamadbar sini', 'Numbers', '1:1', '3:51', 139, ('daberaharon',)),
    ('naso', 'Naso et Rosh', 'נשא את ראש', 'Nasha it reosh', 'Numbers', '4:1', '6:21', 102, ('daberaharon',)),
    ('daber', 'Daber el Aharon', 'דבר אל אהרן', 'Dabber al aarron', 'Numbers', '6:22', '12:16d', 238, ('tsavnum',)),
    ('shelach', 'Shelach Lecha', 'שלח לך', 'Shalla lak', 'Numbers', '13:1', '15:41', 127, ('tsavnum',)),
    ('vayikach', "Va'Yikach Korach", 'ויקח קרח', 'Wyiqqa qara', 'Numbers', '16:1', '20:13i', 139, ('tsavnum',)),
    ('vayishlach', "Va'Yishlach Moshe", 'וישלח משה', 'Wyeshalla mushi', 'Numbers', '20:14', '25:9', 163, ('tsavnum',)),
    ('pinchas', 'Pinchas', 'פינחס', 'Finaas', 'Numbers', '25:10', '31:31', 222, ('shemor_dt',)),
    ('vayehihamalkoach', "Va'Yehi Ha'Malkoach", 'ויהי המלקח', 'Wyai ammalqa', 'Numbers', '31:32', '36:13', 197, ('torahtsiva', 'shemor_dt')),
    ('eleh', "Elle Ha'Devarim", 'אלה הדברים', 'Illa addebarem', 'Deuteronomy', '1:1', '4:4', 119, ('shemor_dt',)),
    ('reu', "Re'u Limadti", 'ראו למדתי', 'Reu lammidtti', 'Deuteronomy', '4:5', '6:25', 107, ('kitissa',)),
    ('kiyeviacha', 'Ki Yeviacha', 'כי יביאך', 'Ki yibbiyak', 'Deuteronomy', '7:1', '11:30', 127, ('vayishkon',)),
    ('kiatem', 'Ki Atem', 'כי אתם', 'Ki attima', 'Deuteronomy', '11:31', '13:19', 52, ('vayishkon',)),
    ('banim', 'Banim Atem', 'בנים אתם', 'Banem attima', 'Deuteronomy', '14:1', '16:17', 69, ('vayishkon',)),
    ('shoftim', "Shoftim ve'Shotrim", 'שפטים ושוטרים', 'Shufatem wshutarem', 'Deuteronomy', '16:18', '22:12', 123, ('vayishkon',)),
    ('kiyikach', 'Ki Yikach Ish Isha', 'כי יקח איש אשה', 'Ki yiqqa ish issha', 'Deuteronomy', '22:13', '26:15', 99, ('vayishkon',)),
    ('hayom', "Ha'Yom Ha'Ze", 'היום הזה', 'Ayyom aazze', 'Deuteronomy', '26:16', '29:28', 127, ('vayishkon',)),
    ('vehaya', "Ve'Haya Ki Yavo'u", 'והיה כי יבאו', 'Weeyya ki yibbiyak', 'Deuteronomy', '30:1', '34:12', 141, ('torahtsiva',)),
]
ADDITIONAL = {
    'shemor_ex': ('Shamor (Exodus 20, Sabbath commandment)', 'Exodus', '20:7', '20:10'),
    'kitissa': ('Ki Tissa (Exodus 30:11-16)', 'Exodus', '30:11', '30:16'),
    'veata': ('Ve-Atta Daber (Exodus 31:12-17)', 'Exodus', '31:12', '31:17'),
    'veshamru': ('Ve-Shamru (Exodus 31:16-17)', 'Exodus', '31:16', '31:17'),
    'kedoshim': ('Kedoshim (Leviticus 19:1-8)', 'Leviticus', '19:1', '19:8'),
    'moadei': ('Moadei (Leviticus 23:1-8)', 'Leviticus', '23:1', '23:8'),
    'vesafartem': ('U-Sefartem (Leviticus 23:15-22)', 'Leviticus', '23:15', '23:22'),
    'shivaa': ("Shiv'a Shavu'ot (Deuteronomy 16:9-12)", 'Deuteronomy', '16:9', '16:12'),
    'daberaharon': ('Daber el Aharon (Numbers 6:22-27)', 'Numbers', '6:22', '6:27'),
    'tsavnum': ('Tsav (Numbers 28:1-10)', 'Numbers', '28:1', '28:10'),
    'shemor_dt': ('Shamor (Deuteronomy 5, Sabbath commandment)', 'Deuteronomy', '5:11', '5:14'),
    'vayishkon': ('Va-Yishkon Yisrael (Deuteronomy 33:24-29)', 'Deuteronomy', '33:24', '33:29'),
    'torahtsiva': ('Torah Tsiva Lanu Moshe (Deuteronomy 33:4)', 'Deuteronomy', '33:4', '33:4'),
}

_BY_ID = {p[0]: p for p in PORTIONS}
_ORDER = [p[0] for p in PORTIONS]
GEN_EXOD = _ORDER[:29]
LEVITICUS = _ORDER[29:37]
NUM_DEUT = _ORDER[37:]

# joins (first id of a join -> ids joined), per number of joins needed
_JOINS_WINTER = {
    7: [("bereshit", "vehaadam"), ("veyada", "vaani"), ("vayissa", "vayakam"), ("vatetse", "vayeshev"),
        ("vayavoyosef", "veeleshemot_g"), ("elshaddai", "benporat"), ("hachodesh", "vayassa")],
    6: [("veyada", "vaani"), ("vayissa", "vayakam"), ("vatetse", "vayeshev"),
        ("vayavoyosef", "veeleshemot_g"), ("elshaddai", "benporat"), ("hachodesh", "vayassa")],
    3: [("vehaadam", "veyada"), ("elshaddai", "benporat"), ("vayavoyosef", "veeleshemot_g")],
    2: [("vehaadam", "veyada"), ("elshaddai", "benporat")],
    1: [("vehaadam", "veyada")],
    0: [],
}
_JOINS_SUMMER = {0: [], 1: [("kiatem", "banim")], 2: [("kiatem", "banim"), ("shoftim", "kiyikach")]}
_ATTESTED = {("bereshit", "vehaadam"): False, ("vehaadam", "veyada"): True, ("veyada", "vaani"): True,
             ("vayissa", "vayakam"): True, ("vatetse", "vayeshev"): True, ("vayavoyosef", "veeleshemot_g"): True,
             ("elshaddai", "benporat"): True, ("hachodesh", "vayassa"): True, ("kiatem", "banim"): True,
             ("shoftim", "kiyikach"): False}

OMER = [("Sabbath of the Sea", "שבת הים"), ("Sabbath of Marah", "שבת מרה"), ("Sabbath of Elim", "שבת אילים"),
        ("Sabbath of the Manna", "שבת המן"), ("Sabbath of the Rock", "שבת הצור"),
        ("Sabbath of Amalek", "שבת עמלק"), ("Sabbath of the Commandments (Devarim)", "שבת הדברים")]
WONDERS = [("blood", "הדם"), ("frogs", "הצפרדע"), ("lice", "הכנים"), ("swarms", "הערב"), ("pestilence", "הדבר"),
           ("boils", "השחין"), ("hail", "הברד"), ("locusts", "הארבה"), ("darkness", "החשך")]
ORD = ["", "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth",
       "Eleventh", "Twelfth", "Thirteenth"]

NOTE_BASE = ("Samaritan weekly portion from the community's table of portions. The date it is read is "
             "inferred from the community's dated calendars for 2004-2006 (see the module notes). "
             "The maftir slot shows the 'additional verse' the table pairs with the portion. "
             "Samaritans read no haftarah.")

_CAL = None


def _calendar(cal):
    global _CAL
    if cal is not None:
        return cal
    if _CAL is None:
        import samaritan_calendar
        _CAL = samaritan_calendar.SamaritanCalendar()
    return _CAL


def _sabbaths(a, b):
    d = a + _dt.timedelta(days=(5 - a.weekday()) % 7)
    out = []
    while d < b:
        out.append(d)
        d += _dt.timedelta(days=7)
    return out


def _group(ids, joins):
    """Split the ordered portion ids into reading units, applying the joins."""
    first = {a: b for a, b in joins}
    units, i = [], 0
    while i < len(ids):
        u = [ids[i]]
        while u[-1] in first and i + 1 < len(ids) and ids[i + 1] == first[u[-1]]:
            i += 1
            u.append(ids[i])
        units.append(u)
        i += 1
    return units


def _unit_entry(unit, attested):
    ps = [_BY_ID[x] for x in unit]
    torah = []
    for p in ps:
        if torah and torah[-1]["book"] == p[4]:
            torah[-1]["to"] = p[6]
        else:
            torah.append({"book": p[4], "from": p[5], "to": p[6]})
    adds = []
    for p in ps:
        for a in p[8]:
            if a not in adds:
                adds.append(a)
    maftir = [{"book": ADDITIONAL[a][1], "from": ADDITIONAL[a][2], "to": ADDITIONAL[a][3]} for a in adds]
    note = NOTE_BASE
    if len(unit) > 1:
        note += (" These portions are read together this week. Joins seen in the community calendars are "
                 "attested; this one is " + ("attested." if attested else "a model choice (not attested)."))
    return {"name_en": " + ".join(p[1] for p in ps), "name_he": " + ".join(p[2] for p in ps),
            "torah": torah, "maftir": maftir, "portions": unit,
            "additional": [ADDITIONAL[a][0] for a in adds], "note": note}


def _special(name_en, name_he, why):
    return {"name_en": name_en, "name_he": name_he, "torah": [], "maftir": [], "portions": [], "additional": [],
            "note": why + " The community calendars list no weekly portion for this Sabbath, and the sources "
                    "used do not say what is read."}


@lru_cache(maxsize=None)
def _cycle(c, cal_id):
    cal = _CALS[cal_id]
    months = cal.cycle_months(c)
    nxt = cal.cycle_months(c + 1)
    if not months:
        return None
    ms = {m.month: m for m in months}
    if 7 not in ms:
        return None
    m1, m7 = ms[1].start, ms[7].start
    m1n = nxt[0].start if nxt else None   # None: last cycle of the table, winter stretch not computable
    day = lambda m, n: m + _dt.timedelta(days=n - 1)
    sched, labels = {}, {}
    # ---- First Month and Omer (rules a, b)
    b1 = _sabbaths(m1, day(m1, 15))
    for s, pid in zip(b1, LEVITICUS[:2]):
        sched[s] = _unit_entry([pid], True)
    mats = _sabbaths(day(m1, 15), day(m1, 22))[0]
    sched[mats] = _special("Sabbath of the Feast of Unleavened Bread", "שבת מועד חג המצות",
                           "Sabbath within the seven days of Unleavened Bread.")
    omer = [mats + _dt.timedelta(days=7 * k) for k in range(1, 8)]
    for k, s in enumerate(omer):
        if k < 6:
            sched[s] = _unit_entry([LEVITICUS[2 + k]], True)
        else:
            sched[s] = _special("Sabbath of the Commandments (Devarim)", "שבת הדברים",
                                "Seventh Sabbath of the Omer, the week of the Revelation at Sinai; Shavuot is the next day.")
        labels.setdefault(s, []).append(OMER[k])
    shav = omer[-1] + _dt.timedelta(days=1)
    # ---- wonders: 9 Sabbaths ending with the 2nd Sabbath of the First Month
    w_end = b1[-1]
    for k in range(9):
        labels.setdefault(w_end - _dt.timedelta(days=7 * (8 - k)), []).append(
            ("Wonder of the " + WONDERS[k][0], "מופת " + WONDERS[k][1]))
    # ---- Numbers-Deuteronomy (rules c, d)
    sukk = day(m7, 15)
    spec = {}
    if m7.weekday() == 5:
        spec[m7] = _special("Feast of the Seventh Month", "מועד החדש השביעי", "Festival Sabbath.")
    sel = [s for s in _sabbaths(day(m7, 2), day(m7, 10)) if s not in spec]
    if sel:
        spec[sel[0]] = _special("Sabbath of the Selihot", "שבת הסליחות",
                                "First Sabbath of the ten days of pardon (Selihot).")
    yk = day(m7, 10)
    if yk.weekday() == 5:
        spec[yk] = _special("Day of Atonement", "יום הכפורים", "The Day of Atonement falls on this Sabbath.")
    summer = [s for s in _sabbaths(shav, sukk) if s not in spec]
    r = len(NUM_DEUT) - len(summer)
    joins = _JOINS_SUMMER.get(r)
    if joins is None:
        joins = []   # never happens in 1850-2149 (0-2 joins needed); no joins then
    units = _group(NUM_DEUT, joins or [])
    for s, u in zip(summer, units):
        sched[s] = _unit_entry(u, all(_ATTESTED.get(tuple(u[i:i + 2]), True) for i in range(len(u) - 1)))
    sched.update(spec)
    st = _sabbaths(sukk, day(m7, 22))
    for s in st:
        sched[s] = _special("Sabbath of the Feast of Tabernacles", "שבת מועד חג הסכות",
                            "Sabbath within the seven days of Sukkot.")
    sa = day(m7, 22)
    if sa.weekday() == 5:
        sched[sa] = _special("Eighth Day of Assembly", "שמיני עצרת", "Festival Sabbath.")
    # ---- Genesis-Exodus (rule e)
    winter = _sabbaths(sa + _dt.timedelta(days=1), m1n) if m1n else []
    r = len(GEN_EXOD) - len(winter)
    units = _group(GEN_EXOD, _JOINS_WINTER.get(r, []))
    for s, u in zip(winter, units):
        sched[s] = _unit_entry(u, all(_ATTESTED.get(tuple(u[i:i + 2]), True) for i in range(len(u) - 1)))
    # ---- new-moon label
    for m in months + list(nxt[:1]):
        if m.start.weekday() == 5:
            labels.setdefault(m.start, []).append(
                ("New Moon (Rosh Chodesh) of the " + ORD[m.month] + " Month", "ראש החדש"))
    return sched, labels, m1, m1n


_CALS = {}


def reading_for_shabbat(d, cal=None, **opts):
    """Samaritan Sabbath reading for date d (see module docstring); None if not a covered Saturday."""
    if not isinstance(d, _dt.date) or d.weekday() != 5:
        return None
    cal = _calendar(cal)
    _CALS[id(cal)] = cal
    try:
        c = cal.cycle_of(d)
    except Exception:
        c = None
    if c is None:
        return None
    got = _cycle(c, id(cal))
    if got is None:
        return None
    sched, labels, m1, m1n = got
    if d not in sched:
        return None
    e = dict(sched[d])
    lab = list(labels.get(d, []))
    nxt = _cycle(c + 1, id(cal))
    if nxt is not None:
        lab += [x for x in nxt[1].get(d, []) if x not in lab]
    special = "; ".join([e["name_en"]] if not e["torah"] else [])
    extra = "; ".join(x[0] for x in lab)
    special = "; ".join(x for x in [special, extra] if x)
    return {
        "date": d.isoformat(),
        "tradition": "samaritan",
        "name_en": e["name_en"],
        "name_he": e["name_he"],
        "torah": [dict(x) for x in e["torah"]],
        "maftir": [dict(x) for x in e["maftir"]],
        "haftarah": [],
        "special": special,
        "special_he": "; ".join(x[1] for x in lab),
        "text": "sp",
        "model": True,
        "note": e["note"],
        "portions": list(e["portions"]),
        "additional": list(e["additional"]),
    }


def portion_table():
    """The 54 portions: (id, name_en, name_he, samaritan transliteration, book, from, to, verses, additional ids)."""
    return list(PORTIONS)
