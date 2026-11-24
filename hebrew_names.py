"""Hebrew spellings of the proper nouns shown in the app, and a Paleo-Hebrew transliterator."""
from __future__ import annotations

import html

import fixed_calendar as fc

PARSHA_HE = [
    "בראשית", "נח", "לך לך", "וירא", "חיי שרה", "תולדות", "ויצא", "וישלח", "וישב", "מקץ", "ויגש", "ויחי",
    "שמות", "וארא", "בא", "בשלח", "יתרו", "משפטים", "תרומה", "תצוה", "כי תשא", "ויקהל", "פקודי",
    "ויקרא", "צו", "שמיני", "תזריע", "מצורע", "אחרי מות", "קדושים", "אמור", "בהר", "בחקתי",
    "במדבר", "נשא", "בהעלתך", "שלח", "קרח", "חקת", "בלק", "פינחס", "מטות", "מסעי",
    "דברים", "ואתחנן", "עקב", "ראה", "שופטים", "כי תצא", "כי תבוא", "נצבים", "וילך", "האזינו", "וזאת הברכה",
]
assert len(PARSHA_HE) == len(fc.PARSHIYOT) == 54

# date.weekday(): Monday=0 ... Sunday=6
WEEKDAY_HE = ["יום שני", "יום שלישי", "יום רביעי", "יום חמישי", "יום שישי", "שבת", "יום ראשון"]
WEEKDAY_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Shabbat", "Sunday"]
GRID_WEEK = [("Sun", "א׳"), ("Mon", "ב׳"), ("Tue", "ג׳"), ("Wed", "ד׳"), ("Thu", "ה׳"), ("Fri", "ו׳"), ("Shabbat", "שבת")]

TERMS = {
    "Fixed (rabbinic)": "הלוח הקבוע",
    "Observed (sighting)": "קידוש החודש על פי הראייה",
    "Early Temple Period": "לוח תקופת המקדש הקדומה",
    "true new moon": "המולד האמיתי",
    "Sky Luach": "לוח השמים",
    "Jerusalem": "ירושלים",
    "Temple Mount": "הר הבית",
    "Israel": "ארץ ישראל",
    "molad": "מולד",
    "tekufah": "תקופה",
    "Tekufat Nisan": "תקופת ניסן", "Tekufat Tammuz": "תקופת תמוז",
    "Tekufat Tishrei": "תקופת תשרי", "Tekufat Tevet": "תקופת טבת",
    "Shmuel": "שמואל", "Rav Adda": "רב אדא", "Hillel II": "הלל השני", "Rambam": "רמב״ם",
    "Mishnah": "משנה", "Sanhedrin": "סנהדרין",
    "machzor katan": "מחזור קטן", "machzor gadol": "מחזור גדול", "shmita": "שמיטה",
    "Birkat HaChamah": "ברכת החמה", "keviah": "קביעות", "Shabbat": "שבת", "Havdalah": "הבדלה",
    "candle lighting": "הדלקת נרות", "Torah portion": "פרשת השבוע", "Omer": "עומר",
    "sha'ah zmanit": "שעה זמנית", "Rosh Chodesh": "ראש חודש", "Pesach": "פסח", "Shavuot": "שבועות",
    "Yallop": "יאלופ", "Odeh": "עודה", "aviv": "אביב",
}
KIND_HE = {
    "major": "יום טוב", "fast": "תענית", "chol": "חול המועד", "minor": "מועד", "rosh_chodesh": "ראש חודש",
    "modern": "יום לאומי", "special_shabbat": "שבת מיוחדת", "erev": "ערב חג", "omer": "ספירת העומר", "hillula": "הילולא",
}
SEASON_HE = {"Vernal equinox": "שוויון האביב", "Summer solstice": "היום הארוך",
             "Autumnal equinox": "שוויון הסתיו", "Winter solstice": "הלילה הארוך"}

# First Temple usage: months are counted from the spring (Exod 12:2); four carry older names.
BIBLICAL_MONTH = {
    fc.NISAN: ("1st month", "החדש הראשון", "Aviv", "חדש האביב", "Exod 13:4"),
    fc.IYYAR: ("2nd month", "החדש השני", "Ziv", "ירח זו", "1 Kgs 6:1, 37"),
    fc.SIVAN: ("3rd month", "החדש השלישי", "", "", ""),
    fc.TAMMUZ: ("4th month", "החדש הרביעי", "", "", ""),
    fc.AV: ("5th month", "החדש החמישי", "", "", ""),
    fc.ELUL: ("6th month", "החדש הששי", "", "", ""),
    fc.TISHREI: ("7th month", "החדש השביעי", "Ethanim", "ירח האיתנים", "1 Kgs 8:2"),
    fc.MARHESHVAN: ("8th month", "החדש השמיני", "Bul", "ירח בול", "1 Kgs 6:38"),
    fc.KISLEV: ("9th month", "החדש התשיעי", "", "", ""),
    fc.TEVET: ("10th month", "החדש העשירי", "", "", ""),
    fc.SHEVAT: ("11th month", "החדש עשתי עשר", "", "", ""),
    fc.ADAR: ("12th month", "החדש שנים עשר", "", "", ""),
    fc.ADAR_II: ("added month", "חדש העבור", "", "", ""),
}


def parsha_he(indices: list[int]) -> str:
    return "–".join(PARSHA_HE[i] for i in indices)


def term(en: str) -> str:
    return TERMS.get(en, "")


def bi(en: str, he: str, cls: str = "sl-he-i") -> str:
    """'English <hebrew>' as HTML; the Hebrew is isolated so it reads right-to-left inside English text."""
    if not he:
        return html.escape(en)
    return f"{html.escape(en)} <span class='{cls}' lang='he' dir='rtl'>{html.escape(he)}</span>"


def bt(en: str) -> str:
    """bi() for a term in TERMS."""
    return bi(en, TERMS.get(en, ""))


# ---- Paleo-Hebrew (Unicode Phoenician block; same 22 letters) ----
_SQUARE = "אבגדהוזחטיכלמנסעפצקרשת"
_FINALS = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}


def paleo(text: str) -> str:
    """Letter-for-letter transliteration of square Hebrew into Paleo-Hebrew letters
    (U+10900-U+10915); spaces become the word-divider dot used in Iron Age inscriptions."""
    out = []
    for ch in text:
        ch = _FINALS.get(ch, ch)
        i = _SQUARE.find(ch)
        if i >= 0:
            out.append(chr(0x10900 + i))
        elif ch == " ":
            out.append(chr(0x1091F))   # Phoenician word separator
        elif "\u0591" <= ch <= "\u05C7" or ch in "״׳":
            continue                   # vowel points and punctuation: not used in the old script
        else:
            out.append(ch)
    return "".join(out)


def hebrew_place_name(alternates: list[str]) -> str:
    """Best Hebrew-script name among GeoNames alternate names. GeoNames mixes Hebrew and Yiddish
    spellings without language tags, so: prefer unpointed forms, then the fewest alef/ayin used
    as vowels (Yiddish marks vowels with them), then the longest form."""
    def is_heb(a):
        return a and any("\u05d0" <= c <= "\u05ea" for c in a) and not any("a" <= c.lower() <= "z" for c in a)
    cands = [a for a in (alternates or []) if is_heb(a)]
    if not cands:
        return ""
    plain = [a for a in cands if not any("\u0591" <= c <= "\u05c7" for c in a)]
    pool = plain or cands
    def score(a):
        yid = sum(a[1:].count(x) for x in "אע") + 3 * sum(a.count(x) for x in "װױײ")
        return (yid, -len(a))
    return min(pool, key=score)
