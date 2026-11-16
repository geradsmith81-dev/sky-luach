"""
Build data/readings/karaite_parashot.json - the Karaite weekly Torah portions and haftarot.

Run from the repo root:  python tools/build_karaite_parashot.py
Needs data/readings/torah_mt.json.gz (to check the verse ranges and to read five Hebrew incipits).

Sources (transcribed 16 Nov 2026):
  KJA-A  Karaite Jews of America, "Torah Audio - Karaite Parashiot and Haftarot", https://karaites.org/torah-audio/
         (portion and haftarah of each parasha, Egyptian Karaite tradition, recordings by Hazan Rotem Cohen).
  KJA-P  Karaite Jews of America, "Torah Portions" index and the per-portion commentary pages,
         https://karaites.org/torah-portions/ (Hebrew names; verse range of each portion).
  KALE   Seder ha-Haftarot (Kale [Gozleve/Yevpatoria], 1733), Karaite column as tabulated in
         Aaron Marsh, "The Sequential Triennial Cycle: A History and Guide to its Modern Use",
         Master's project, Academy for Jewish Religion, 2015, Table 2, pp. 36-38 (Bereshit to Masei only).
Where the KJA-A list has an evident misprint the KJA-P commentary page is followed; every such case is
recorded in "correction".
"""
import gzip, json, os, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = {"Gen": "Genesis", "Ex": "Exodus", "Lev": "Leviticus", "Num": "Numbers", "Deut": "Deuteronomy"}

# Hebrew names as printed on the KJA Torah Portions page (NFC-normalised).
HE_KJA = {"Bereshit": "בְּרֵאשִׁית", "Noah": "נֹחַ", "Lekh Lekha": "לֶךְ לְךָ", "Vayyera": "וַיֵּרָא", "Hayyei Sarah": "חַיֵּי שָׂרָה", "Toledot": "תּוֹלְדֹת", "Vayyetze": "וַיֵּצֵא", "Vayishlach": "וַיִּשְׁלַח", "Vayeshev": "וַיֵּשֶׁב", "Mikketz": "מִקֵּץ", "Vayigash": "וַיִּגַּשׁ", "Vayechi": "וַיְחִי", "Shemot": "שְׁמוֹת", "Vaera": "וָאֵרָא", "Bo": "בֹּא", "Beshalach": "בְּשַׁלַּח", "Yitro": "יִתְרוֹ", "Mishpatim": "מִשְׁפָּטִים", "Terumah": "תְּרוּמָה", "Tetzaveh": "תְּצַוֶּה", "Ki Tissa": "כִּי תִשָּׂא", "Vayakhel": "וַיַּקְהֵל", "Pekudei": "פְּקוּדֵי", "Vayikra": "וַיִּקְרָא", "Tzav": "צַו", "Shemini": "שְׁמִינִי", "Tazria": "תַּזְרִיעַ", "Metzora": "מְצֹרָע", "Acharei Mot": "אַחֲרֵי מוֹת", "Kedoshim": "קְדֹשִׁים", "Emor": "אֱמֹר", "Behar Sinai": "בְּהַר סִינַי", "Bechukotai": "בְּחֻקֹּתַי", "Bamidbar": "בְּמִדְבַּר", "Nasso": "נָשֹׂא", "Beha’alotekha": "בְּהַעֲלֹתְךָ", "Shelah": "שְׁלַח", "Korach": "קֹרַח", "Chukat": "חֻקַּת", "Balak": "בָּלָק", "Pinchas": "פִּינְחָס", "Matot": "מַטּוֹת", "Masei": "מַסְעֵי", "Devarim": "דְּבָרִים", "Va’etchanan": "וָאֶתְחַנַּן", "Ki Tavo": "כִּי תָבוֹא", "Nitzavim": "נִצָּבִים", "Vayelech": "וַיֵּלֶךְ", "Vezot Haberacha": "וְזֹאת הַבְּרָכָה"}

# (English name, KJA-P key or None, book, from, to, KJA-A torah as printed, KJA-A haftarah as printed,
#  haftarah used, correction note)
ROWS = [
("Bereshit","Bereshit","Gen","1:1","6:8","Genesis 1:1 – 6:8","Isaiah 65:17 – 66:13","Isaiah 65:17-66:13",""),
("Noah","Noah","Gen","6:9","11:32","Genesis 6:9 – 11:32","Isaiah 54:9 – 55:12","Isaiah 54:9-55:12",""),
("Lekh Lekha","Lekh Lekha","Gen","12:1","17:27","Genesis 12:1-17:27","Joshua 24:3 – 24:18","Joshua 24:3-18",""),
("Vayyera","Vayyera","Gen","18:1","22:24","Genesis:18:1-22:24","33:17 – 35:10","Isaiah 33:17-35:10","KJA-A omits the book of the haftarah; Isaiah supplied (KALE gives Isaiah 33:17-34:12, 35:10 for this portion)."),
("Hayyei Sarah","Hayyei Sarah","Gen","23:1","25:18","Genesis 23:1-25:18","Isaiah 51:2-51:22","Isaiah 51:2-22",""),
("Toledot","Toledot","Gen","25:19","28:9","Genesis 25:19-28:9","Isaiah 65:23-66:18","Isaiah 65:23-66:18",""),
("Vayyetze","Vayyetze","Gen","28:10","32:3","Genesis 28:10-32:3","Hosea 11:7-13:5","Hosea 11:7-13:5",""),
("Vayishlach","Vayishlach","Gen","32:4","36:43","Genesis 32:4-36:43","Ovadiah 1:1-21","Obadiah 1:1-21",""),
("Vayeshev","Vayeshev","Gen","37:1","40:23","Genesis 37:1-40:23","Isaiah 32:18-33:22","Isaiah 32:18-33:22",""),
("Mikketz","Mikketz","Gen","41:1","44:17","Genesis 41:1-44:17","Isaiah 29:7-24","Isaiah 29:7-24",""),
("Vayigash","Vayigash","Gen","44:18","47:27","Genesis 44:18-47:27","Joshua 14:6-14:15","Joshua 14:6-15",""),
("Vayechi","Vayechi","Gen","47:28","50:26","Genesis 47:28-50:26","2 Kings: 13:14-14:7","2 Kings 13:14-14:7",""),
("Shemot","Shemot","Ex","1:1","6:1","Exodus 1:1-6:1","Isaiah 27:6-28:13","Isaiah 27:6-28:13",""),
("Vaera","Vaera","Ex","6:2","9:35","Ex. 6:2-9:35","Isaiah 33:17-34:12, 35:10","Isaiah 33:17-34:12, 35:10","KJA-A gives the same haftarah as for Vayyera; KALE gives Isaiah 42:8-43:5 for Vaera."),
("Bo","Bo","Ex","10:1","13:16","Exodus 10:1-13:6","Isaiah 34:11-35:10","Isaiah 34:11-35:10","KJA-A prints Exodus 10:1-13:6 and Beshalach 13:7-; KJA-P gives Ex. 10:1-13:16 and 13:17-17:16, used here."),
("Beshalach","Beshalach","Ex","13:17","17:16","Exodus 13:7-17:16","Joshua 24:7-24:26","Joshua 24:7-26","See Bo."),
("Yitro","Yitro","Ex","18:1","20:23","Exodus 18:1 – 20:26","Isaiah 33:14 – 34:8","Isaiah 33:14-34:8","KJA-A ends at 20:26 (English verse numbering of Exodus 20); in Hebrew numbering the chapter ends at 20:23. KJA-P's first section starts at Ex. 18:1 (its heading misprints 17:1)."),
("Mishpatim","Mishpatim","Ex","21:1","24:18","Exodus 21:1-24:18","Isaiah 56:1-57:2","Isaiah 56:1-57:2",""),
("Terumah","Terumah","Ex","25:1","27:19","Exodus 25:1-27:19","Isaiah 60:17-61:9","Isaiah 60:17-61:9",""),
("Tetzaveh","Tetzaveh","Ex","27:20","30:10","Exodus 27:20-30:10","Jeremiah 11:16-12:15","Jeremiah 11:16-12:15",""),
("Ki Tissa","Ki Tissa","Ex","30:11","34:35","Exodus 20:11-34:35","Isaiah 43:7-44:5","Isaiah 43:7-44:5","KJA-A prints 20:11 (misprint); KJA-P gives Ex. 30:11-34:35."),
("Vayakhel","Vayakhel","Ex","35:1","38:20","Exodus 35:1-38:20","1 Kings 8:1-8:19","1 Kings 8:1-19",""),
("Pekudei","Pekudei","Ex","38:21","40:38","Exodus 38:21-40:38","Jeremiah 30:18-31:13","Jeremiah 30:18-31:13",""),
("Vayikra","Vayikra","Lev","1:1","5:26","Leviticus 1:1-5:26","Isaiah 43:21-44:23","Isaiah 43:21-44:23",""),
("Tzav","Tzav","Lev","6:1","8:36","Leviticus 6:1-8:36","Malachi 3:4-3:24, 3:23","Malachi 3:4-24, 3:23","Verse 3:23 is repeated after the end of the book."),
("Shemini","Shemini","Lev","9:1","11:47","Leviticus 9:11-11:47","Ezekiel 43:27 – 44:16","Ezekiel 43:27-44:16","KJA-A prints 9:11 (misprint); KJA-P gives Lev. 9:1-11:47."),
("Tazria","Tazria","Lev","12:1","13:59","Leviticus 12:1-13:59","2 Kings 7:3-7:20","2 Kings 7:3-20","KALE gives Isaiah 66:7-24, 66:23 for Tazria."),
("Metzora","Metzora","Lev","14:1","15:33","Leviticus 14:1-15:33","2 Kings 7:3-18","2 Kings 7:3-18",""),
("Acharei Mot","Acharei Mot","Lev","16:1","18:30","Leviticus 16:1-18:30","Ezekiel 22:1-16","Ezekiel 22:1-16",""),
("Kedoshim","Kedoshim","Lev","19:1","20:27","Leviticus 19:1-20:27","Isaiah 4:3-5:16","Isaiah 4:3-5:16",""),
("Emor","Emor","Lev","21:1","24:23","Leviticus 21:1-24:3","Ezekiel 44:25-45:11","Ezekiel 44:25-45:11","KJA-A prints 24:3 (misprint); KJA-P gives Lev. 21:1-24:23."),
("Behar Sinai","Behar Sinai","Lev","25:1","26:2","Leviticus 25:1-26:2","Isaiah 24:2-23","Isaiah 24:2-23",""),
("Bechukotai","Bechukotai","Lev","26:3","27:34","Leviticus 26:3-27:34","Isaiah 1:19-2:11","Isaiah 1:19-2:11",""),
("Bamidbar","Bamidbar","Num","1:1","4:20","Numbers 1:1-4:20","Hosea 2:1-2:22","Hosea 2:1-22",""),
("Nasso","Nasso","Num","4:21","7:89","Numbers 4:21-7:89","Judges 13:2-13:24","Judges 13:2-24",""),
("Beha'alotekha","Beha’alotekha","Num","8:1","12:16","Numbers 8:1-12:16","Zechariah 2:14-4:7","Zechariah 2:14-4:7",""),
("Shelah","Shelah","Num","13:1","15:41","Numbers 13:1-15:31","Joshua 2:1-16","Joshua 2:1-16","KJA-A prints 15:31; KJA-P gives Num. 13:1-15:41 (end of chapter 15)."),
("Korach","Korach","Num","16:1","18:32","Numbers 16:1-18:32","Hosea 10:2-11:9","Hosea 10:2-11:9",""),
("Chukat","Chukat","Num","19:1","22:1","Numbers 19:1-22:1","Judges 11:1-11:17","Judges 11:1-17",""),
("Balak","Balak","Num","22:2","25:9","Numbers 22:2 – 25:9","Micah 5:6-6:8","Micah 5:6-6:8",""),
("Pinchas","Pinchas","Num","25:10","30:1","Numbers 25:10 – 30:1","Malachai 2:5-3:3","Malachi 2:5-3:3",""),
("Matot","Matot","Num","30:2","32:42","Numbers 30:2-32:42","Jeremiah 1:1-2:3","Jeremiah 1:1-2:3","KALE gives 1 Samuel 1:1-2:10 for Matot."),
("Masei","Masei","Num","33:1","36:13","Numbers 33:1-36:13","Joshua 20:1-20:9","Joshua 20:1-9",""),
("Devarim","Devarim","Deut","1:1","3:22","Deuteronomy 1:1-3:22","Isaiah 1:1-1:27","Isaiah 1:1-27",""),
("Va'etchanan","Va’etchanan","Deut","3:23","7:11","Deuteronomy 3:23-7:11","Isaiah 40:1-40:22","Isaiah 40:1-22",""),
("Ekev",None,"Deut","7:12","11:25","Deuteronomy 7:12-11:25","Isaiah 49:14-50:5","Isaiah 49:14-50:5",""),
("Re'eh",None,"Deut","11:26","16:17","Deuteronomy 11:26-16-17","Isaiah 54:11–56:1","Isaiah 54:11-56:1","KJA-A prints 16-17 for 16:17."),
("Shofetim",None,"Deut","16:18","21:9","Deuteronomy 16:18-21:9","Isaiah 51:12–52:8","Isaiah 51:12-52:8",""),
("Ki Tetze",None,"Deut","21:10","25:19","Deuteronomy 21:10 – 25:19","Isaiah 54:1-54:17","Isaiah 54:1-17",""),
("Ki Tavo","Ki Tavo","Deut","26:1","29:8","Deuteronomy 26:1-29:8","Isaiah 60:1–60:16","Isaiah 60:1-16",""),
("Nitzavim","Nitzavim","Deut","29:9","30:20","Deuteronomy 29:9-30:20","Isaiah 61:10–63:1","Isaiah 61:10-63:1",""),
("Vayelech","Vayelech","Deut","31:1","31:30","Deuteronomy 31:1-30","Isaiah 55:6-56:8","Isaiah 55:6-56:8",""),
("Haazinu",None,"Deut","32:1","32:52","Deuteronomy 32:1-32","Hosea 14:2–14:10","Hosea 14:2-10","KJA-A prints 32:1-32; the portion runs to the end of chapter 32 (32:52), before Vezot Haberacha at 33:1."),
("Vezot Haberacha","Vezot Haberacha","Deut","33:1","34:12","Deuteronomy 33:1-34:12","Joshua 1:1-1:10","Joshua 1:1-10",""),
]

# KALE (Karaite column of Marsh 2015, Table 2), by position 0..42 (Bereshit..Masei); not tabulated after Masei.
KALE = ["Isaiah 65:17-66:13","Isaiah 54:9-55:12","Joshua 24:3-23","Isaiah 33:17-34:12, 35:10","Isaiah 51:2-22",
 "Isaiah 65:23-66:18","Hosea 11:7-12:12 or Hosea 12:13-14:10","Obadiah 1:1-21","Isaiah 32:18-33:22","Isaiah 29:7-30:3",
 "Joshua 14:6-15:6","2 Kings 13:14-14:7","Isaiah 26:7-27:6 or Isaiah 27:6-28:13","Isaiah 42:8-43:5","Isaiah 34:11-35:10",
 "Joshua 24:7-26","Isaiah 33:13-34:8","Isaiah 56:1-57:2 or Isaiah 56:1-57:14","Isaiah 60:17-61:9","Jeremiah 11:16-12:15",
 "Isaiah 43:7-44:5","1 Kings 8:1-19","Jeremiah 30:18-31:13","Isaiah 43:21-44:22","Malachi 3:4-24",
 "Ezekiel 43:27-44:16 or Ezekiel 43:27-44:24","Isaiah 66:7-66:24, 66:23","2 Kings 7:1-18 or 2 Kings 7:3-18","Ezekiel 22:1-22",
 "Isaiah 4:3-5:16","Ezekiel 44:25-45:11","Isaiah 24:2-23 or Jeremiah 16:19-17:14","Isaiah 1:19-2:17","Hosea 2:1-22",
 "Judges 13:2-24 or Hosea 4:14-6:2","Zechariah 2:14-4:7","Joshua 2:1-15 or Joshua 2:1-24","Hosea 10:2-11:9",
 "Judges 11:1-17 or Judges 11:1-25","Micah 5:6-6:8","Malachi 2:5-3:3","1 Samuel 1:1-2:10","Joshua 20:1-9 or Ezekiel 46:24-47:21"]

# Five portions are not on the KJA Torah Portions page: their Hebrew name is taken from the incipit in the text
# (word slice of the first verse).
INCIPIT = {"Ekev": (1, 2), "Re'eh": (0, 1), "Shofetim": (0, 1), "Ki Tetze": (0, 2), "Haazinu": (0, 1)}


def main():
    mt = json.load(gzip.open(os.path.join(ROOT, "data", "readings", "torah_mt.json.gz"), "rt", encoding="utf-8"))
    allv = [(b, k) for b in ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"] for k in mt["books"][b]]
    pos = {v: i for i, v in enumerate(allv)}
    out, prev = [], -1
    for i, (en, key, bk, a, z, raw_t, raw_h, haft, corr) in enumerate(ROWS):
        book = BOOK[bk]
        ia, iz = pos[(book, a)], pos[(book, z)]
        if ia != prev + 1:
            raise SystemExit(f"gap or overlap before {en}")
        prev = iz
        if key:
            he, he_src = unicodedata.normalize("NFC", HE_KJA[key]), "KJA-P"
        else:
            s, e = INCIPIT[en]
            w = mt["books"][book][a]["he"].replace("\u05be", " ").replace("\u05c3", "").split()
            he, he_src = " ".join(w[s:e]), f"incipit of {book} {a} (Masoretic text)"
        out.append({"num": i + 1, "name_en": en, "name_he": he, "name_he_source": he_src,
                    "book": book, "from": a, "to": z, "verses": iz - ia + 1,
                    "haftarah": haft, "haftarah_kale_1733": KALE[i] if i < len(KALE) else None,
                    "kja_printed": {"torah": raw_t, "haftarah": raw_h}, "correction": corr})
    if prev != len(allv) - 1:
        raise SystemExit("portions do not reach the end of Deuteronomy")
    doc = {"meta": {
        "title": "Karaite weekly Torah portions and haftarot (Egyptian Karaite tradition)",
        "source": ("KJA-A: Karaite Jews of America, 'Torah Audio - Karaite Parashiot and Haftarot', https://karaites.org/torah-audio/ ; "
                   "KJA-P: Karaite Jews of America, 'Torah Portions' and per-portion commentary pages, https://karaites.org/torah-portions/ ; "
                   "KALE: Seder ha-Haftarot (Kale, 1733), Karaite column as tabulated in A. Marsh, 'The Sequential Triennial Cycle: "
                   "A History and Guide to its Modern Use', Master's project, Academy for Jewish Religion, 2015, Table 2, pp. 36-38."),
        "license": ("Facts only (portion names, verse references); no text of the sources is reproduced beyond the short "
                    "reference strings in kja_printed. Compilation released with the app under the MIT licence."),
        "attribution": "Portion and haftarah list after the Karaite Jews of America (karaites.org).",
        "transcribed": "2026-11-16",
        "verse_numbering": "Hebrew (Masoretic) chapter:verse numbering, as in data/readings/torah_mt.json.gz.",
        "total_verses": prev + 1},
        "parashot": out}
    path = os.path.join(ROOT, "data", "readings", "karaite_parashot.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(f"wrote {path}: {len(out)} portions, {prev + 1} verses")


if __name__ == "__main__":
    main()
