"""Short histories of the holidays, opened by clicking a holiday's name.

Each entry: title, Hebrew title, a few sentences of history, and the main sources. Where an
archaeological link is debated, the text says so.
"""
from __future__ import annotations

import html

H = {
    "rosh_hashanah": ("Rosh Hashanah", "ראש השנה",
        "The Torah sets the first day of the seventh month as a day of rest marked by trumpet blasts (Yom Teruah). "
        "The name Rosh Hashanah, 'head of the year', first appears in the Mishnah, which lists it among four new "
        "years and makes it the day of judgment for the world. Its prayers of Kingship, Remembrance and Shofar "
        "blasts are already set out in the Mishnah. Two days were kept even in the Land of Israel from early "
        "times, because witnesses to the new moon could arrive late. The tashlich custom at a river is first "
        "recorded in late-medieval Germany.",
        "Lev 23:23–25; Num 29:1–6; Ezek 40:1; Mishnah Rosh Hashanah 1:1–2, 4:5"),
    "tzom_gedaliah": ("Tzom Gedaliah", "צום גדליה",
        "After Jerusalem fell in 586 BCE, Nebuchadnezzar appointed Gedaliah son of Ahikam governor of Judah, "
        "based at Mizpah. His murder by Ishmael son of Nethaniah led the remaining Judeans to flee to Egypt. "
        "Zechariah's 'fast of the seventh month' is understood as this fast, and the rabbis set it on 3 Tishrei. "
        "Mizpah is usually identified with Tell en-Nasbeh, which flourished in the 6th century BCE. A seal "
        "impression from Lachish reading 'Gedalyahu who is over the house' has been linked to him, but the "
        "identification is debated.",
        "2 Kgs 25:22–26; Jer 40–41; Zech 7:5, 8:19; Talmud Rosh Hashanah 18b"),
    "yom_kippur": ("Yom Kippur", "יום כיפור",
        "The Day of Atonement falls on the tenth of the seventh month, a day of fasting ('afflicting the soul') and "
        "complete rest. In the Temple the high priest entered the Holy of Holies, and of two goats one was "
        "offered and one sent 'to Azazel' in the wilderness. The Mishnah tractate Yoma describes the Second "
        "Temple rite in detail. After 70 CE the day became one of prayer and repentance; the Avodah poem still "
        "retells the Temple service, and Kol Nidre dates from the geonic period. The Mishnah also remembers it "
        "as a joyful day on which young women danced in the vineyards.",
        "Lev 16; 23:26–32; Num 29:7–11; Mishnah Yoma; Mishnah Taanit 4:8"),
    "sukkot": ("Sukkot", "סוכות",
        "Sukkot began as the autumn harvest festival, the 'Feast of Ingathering'. The Torah adds dwelling in "
        "booths in memory of the wilderness, and the four species. Solomon dedicated the Temple at this feast in "
        "the month of Ethanim, and Nehemiah describes the booths being renewed after the return from Babylon. "
        "In the Second Temple it was the great pilgrimage feast, with the water libation and the night-long joy "
        "of the Water-Drawing. Coins of both Jewish revolts show the lulav and etrog, and a Bar Kokhba letter "
        "from the Judean Desert asks for palm branches and citrons for the festival.",
        "Exod 23:16; Lev 23:33–43; Deut 16:13–15; 1 Kgs 8:2; Neh 8:13–18; Mishnah Sukkah 4–5"),
    "hoshana_rabbah": ("Hoshana Rabbah", "הושענא רבה",
        "On the seventh day of Sukkot the Temple altar was circled seven times with willow branches while "
        "'Hosha-na' ('save, please') was chanted; on the other days of the festival it was circled once. "
        "The custom of beating willow branches is called in the Talmud a 'custom of the prophets'. Medieval "
        "Kabbalah made the day the final sealing of the year's judgment, with an all-night study vigil.",
        "Mishnah Sukkah 4:5–6; Talmud Sukkah 44a"),
    "shemini_atzeret": ("Shemini Atzeret", "שמיני עצרת",
        "The 'Eighth Day of Assembly' follows the seven days of Sukkot. The Torah treats it as a separate holy "
        "day, with no booths or four species. The rabbis began the prayer for rain on this day, marking the "
        "start of the rainy season in the Land of Israel. In Israel it is also Simchat Torah.",
        "Lev 23:36, 39; Num 29:35–38; Mishnah Taanit 1:1–2"),
    "simchat_torah": ("Simchat Torah", "שמחת תורה",
        "Simchat Torah is not in the Bible. It grew up in Babylonia, where the Torah was read through in one "
        "year, while the Land of Israel used a cycle of about three years. Finishing Deuteronomy and starting "
        "Genesis again became a celebration in the geonic and early medieval periods. Dancing processions "
        "(hakafot) with all the Torah scrolls are documented from the 16th century. Outside Israel it falls on "
        "the day after Shemini Atzeret.",
        "Talmud Megillah 29b (the two reading cycles); geonic and medieval custom"),
    "chanukah": ("Chanukah", "חנוכה",
        "Chanukah ('dedication') marks the rededication of the Temple altar by Judah Maccabee on 25 Kislev "
        "164 BCE. Three years earlier the Seleucid king Antiochus IV had defiled the Temple. The books of "
        "Maccabees describe an eight-day festival modelled on Sukkot, and Josephus calls it 'Lights'. The story "
        "of the single cruse of oil that lasted eight days comes later, from the Babylonian Talmud.",
        "1 Macc 4:36–59; 2 Macc 10:1–8; Josephus, Antiquities 12.316–325; Talmud Shabbat 21b"),
    "asara_btevet": ("Asara B'Tevet", "עשרה בטבת",
        "On the tenth of the tenth month Nebuchadnezzar of Babylon began the siege of Jerusalem, in 589/588 "
        "BCE. Two and a half years later the city fell and the First Temple was destroyed. Zechariah lists it as "
        "the 'fast of the tenth month'. In 1949 Israel's Chief Rabbinate made it a day of Kaddish for Holocaust "
        "victims whose date of death is unknown.",
        "2 Kgs 25:1; Jer 52:4; Ezek 24:1–2; Zech 8:19"),
    "tu_bishvat": ("Tu BiShvat", "ט״ו בשבט",
        "The Mishnah names the 15th of Shevat as the 'new year for trees', following the school of Hillel. "
        "It is the cut-off date for counting a tree's age and for its tithes. Kabbalists in 16th–17th-century "
        "Safed gave it a fruit-eating ritual, the Tu BiShvat seder, printed in the 18th century. From the late "
        "19th century the Zionist movement made it a day of tree planting in the Land of Israel.",
        "Mishnah Rosh Hashanah 1:1; Pri Etz Hadar (1728)"),
    "purim_katan": ("Purim Katan", "פורים קטן",
        "In a leap year Purim is kept in the second Adar, the one next to Nisan, linking the two redemptions of "
        "Purim and Passover. The 14th and 15th of the first Adar remain minor days of joy, with no Megillah "
        "reading and no fasting.",
        "Mishnah Megillah 1:4; Talmud Megillah 6b"),
    "taanit_esther": ("Ta'anit Esther", "תענית אסתר",
        "The Book of Esther tells of a three-day fast before Esther went to the king, and later speaks of fasts "
        "and lamentations. A fast on 13 Adar, the day the Jews of Persia fought their enemies, is first recorded "
        "in the geonic period (8th century CE). When the 13th is a Shabbat it is moved back to Thursday.",
        "Esth 4:16, 9:1, 9:31; She'iltot of Rav Ahai"),
    "purim": ("Purim", "פורים",
        "The Book of Esther is set at the Persian court of King Ahasuerus, often identified with Xerxes I "
        "(486–465 BCE). It tells how Haman's lot (pur) fixed a day to destroy the Jews, and how Esther and "
        "Mordecai turned it around. Esther 9 sets the festival: feasting, gifts of food to friends and gifts to "
        "the poor. The Mishnah adds the reading of the scroll. French excavations at Susa uncovered the Persian "
        "palace of Darius I and Xerxes. A Persian-period name Marduka in administrative texts from Persepolis has "
        "been compared to Mordecai, but the link is uncertain.",
        "Esther 3, 9:17–32; Mishnah Megillah 1–2"),
    "shushan_purim": ("Shushan Purim", "שושן פורים",
        "In Susa (Shushan) the fighting lasted a day longer, so its Jews celebrated on the 15th. The Mishnah "
        "applies this to cities walled since the days of Joshua; today Jerusalem keeps Purim on 15 Adar.",
        "Esth 9:18–19; Mishnah Megillah 1:1"),
    "taanit_bechorot": ("Ta'anit Bechorot", "תענית בכורות",
        "First-born sons fast on the eve of Passover in thanks for the sparing of Israel's first-born in Egypt. "
        "The custom is first mentioned in the post-talmudic tractate Soferim. Most first-born are released from "
        "the fast by attending a siyum, a celebration of finishing a tractate of Talmud.",
        "Exod 12:29, 13:2, 13:15; Tractate Soferim 21:3"),
    "pesach": ("Pesach (Passover)", "פסח",
        "Pesach joins two biblical feasts. One is the Passover offering, slaughtered on the afternoon of 14 Nisan "
        "and eaten that night in memory of the Exodus. The other is the seven-day Feast of Unleavened Bread at the "
        "start of the barley harvest, in the 'month of Aviv'. Kings Hezekiah and Josiah held national Passovers "
        "in Jerusalem. The 'Passover Papyrus' from Elephantine in Egypt (419 BCE) instructs the Jewish garrison "
        "there on the festival's dates. After 70 CE the Seder and the Haggadah replaced the offering. The "
        "Samaritans still slaughter the Passover lambs on Mount Gerizim.",
        "Exod 12–13; Lev 23:4–8; Deut 16:1–8; 2 Kgs 23:21–23; 2 Chr 30; Mishnah Pesachim 10"),
    "pesach_sheni": ("Pesach Sheni", "פסח שני",
        "The 'second Passover' on 14 Iyyar was a second chance for anyone ritually impure or far away on 14 Nisan. "
        "Hezekiah's great Passover was held in the second month for this reason. Today it is a minor day, when "
        "some eat matzah.",
        "Num 9:1–14; 2 Chr 30:2–3, 15"),
    "omer": ("Counting the Omer", "ספירת העומר",
        "The Torah commands bringing a sheaf (omer) of the first barley 'on the morrow after the Sabbath' of "
        "Passover, then counting seven weeks to Shavuot. The rabbis read 'Sabbath' as the first day of the "
        "festival, so the count starts on 16 Nisan. The Boethusians, and later the Karaites, counted from the "
        "Sunday instead. The weeks later became a time of semi-mourning for Rabbi Akiva's students. This app's "
        "observed and Pre-Temple calendars count Shavuot from 16 Nisan, following the rabbinic reading.",
        "Lev 23:9–16; Deut 16:9–10; Mishnah Menachot 10; Talmud Menachot 65a–66a; Yevamot 62b"),
    "lag_baomer": ("Lag BaOmer", "ל״ג בעומר",
        "The 33rd day of the Omer (18 Iyyar) breaks the mourning of the counting weeks. The Talmud says Rabbi "
        "Akiva's students died between Passover and Shavuot, and medieval sources say the dying stopped on this "
        "day. Kabbalistic tradition made it the anniversary of Rabbi Shimon bar Yochai, and since the 16th century "
        "crowds have gone to his tomb at Meron, with bonfires. Modern Zionism also linked the day to the Bar "
        "Kokhba revolt.",
        "Talmud Yevamot 62b; medieval and Safed customs"),
    "shavuot": ("Shavuot", "שבועות",
        "Shavuot, the 'Feast of Weeks', is the wheat harvest festival. It falls on the 50th day of the Omer count "
        "and brings two loaves of new wheat and the first fruits to the Temple. The Torah gives it no fixed date, "
        "only the count. In this app's observed calendar it can therefore fall on 5, 6 or 7 Sivan. Rabbinic "
        "tradition, and earlier the Book of Jubilees, connect it with the covenant at Sinai in the third month. "
        "The all-night study vigil (Tikkun Leil Shavuot) began among the 16th-century Safed kabbalists, and the "
        "Book of Ruth is read.",
        "Exod 19:1, 23:16, 34:22; Lev 23:15–21; Num 28:26; Mishnah Bikkurim 3; Talmud Pesachim 68b"),
    "tzom_tammuz": ("Tzom Tammuz (17 Tammuz)", "שבעה עשר בתמוז",
        "The Mishnah lists five disasters on this day: Moses broke the tablets, the daily offering stopped, the "
        "city walls were breached, Apostomos burned a Torah scroll, and an idol was set up in the Temple. The "
        "breach of 17 Tammuz is the Roman one of 70 CE; for the Babylonian siege Jeremiah gives 9 Tammuz. It is "
        "Zechariah's 'fast of the fourth month' and opens the Three Weeks of mourning before Tisha B'Av.",
        "Jer 39:2, 52:6–7; Zech 8:19; Mishnah Taanit 4:6"),
    "tisha_bav": ("Tisha B'Av", "תשעה באב",
        "Tisha B'Av mourns the destruction of both Temples: by Babylon in 586 BCE and by Rome in 70 CE. The Bible "
        "dates the first to the 7th or 10th of Av, and the rabbis set the fast on the 9th. The Mishnah adds "
        "later disasters, including the fall of Betar in 135 CE. Lamentations is read. Archaeology has found "
        "both destructions: the burnt Babylonian-era houses and arrowheads in the City of David, and the 'Burnt "
        "House' of 70 CE in the Jewish Quarter. The Arch of Titus in Rome shows the Temple menorah carried in "
        "triumph.",
        "2 Kgs 25:8–9; Jer 52:12–13; Lamentations; Mishnah Taanit 4:6; Josephus, Jewish War 6"),
    "tu_bav": ("Tu B'Av", "ט״ו באב",
        "The Mishnah says there were no days as joyful as 15 Av and Yom Kippur, when the young women of Jerusalem "
        "went out in borrowed white clothes to dance in the vineyards. The Talmud gives several reasons for the "
        "day, among them the end of the wood offering for the altar. In modern Israel it has become a day of "
        "love.",
        "Mishnah Taanit 4:8; Talmud Taanit 30b–31a"),
    "rosh_chodesh": ("Rosh Chodesh", "ראש חודש",
        "The new moon was a biblical festival, with its own offerings and trumpet blasts. Saul held a new-moon "
        "feast, and Amos's merchants could not trade on it. In Second Temple times the Sanhedrin declared the new "
        "month on the testimony of witnesses who had seen the crescent. Beacon fires on the Mount of Olives then "
        "spread the news; the Mishnah describes the procedure. This app's observed calendar models that "
        "procedure. Tradition gives Rosh Chodesh as a special day to women.",
        "Num 10:10, 28:11–15; 1 Sam 20:5, 18–34; Amos 8:5; Mishnah Rosh Hashanah 1–2"),
    "yom_hashoah": ("Yom HaShoah", "יום השואה",
        "Holocaust and Heroism Remembrance Day was set by the Knesset in 1951 on 27 Nisan. That date falls after "
        "Passover and within the weeks of the Warsaw Ghetto Uprising, which began on 19 April 1943, the eve of "
        "Passover. A law of 1959 fixed its observance, and a siren stops the country for two minutes.",
        "Knesset resolution 1951; Martyrs' and Heroes' Remembrance Day Law 1959"),
    "yom_hazikaron": ("Yom HaZikaron", "יום הזיכרון",
        "Israel's Memorial Day for fallen soldiers, and in recent decades also for victims of terror. A 1963 "
        "law placed it on the day before Independence Day, linking sacrifice and statehood. Sirens sound in "
        "the evening and in the morning.",
        "Memorial Day Law 1963"),
    "yom_haatzmaut": ("Yom HaAtzmaut", "יום העצמאות",
        "On 5 Iyyar 5708 (14 May 1948) David Ben-Gurion read the Declaration of Independence of the State of "
        "Israel in Tel Aviv. The day is kept on its Hebrew date. It moves when that date would run into "
        "Shabbat, or (since 2004) when it falls on a Monday.",
        "Declaration of the Establishment of the State of Israel, 1948"),
    "yom_yerushalayim": ("Yom Yerushalayim", "יום ירושלים",
        "Jerusalem Day marks 28 Iyyar 5727 (7 June 1967), when Israeli forces took the Old City and the Western "
        "Wall during the Six-Day War. The day was declared in 1968 and fixed in law in 1998.",
        "Jerusalem Day Law 1998"),
    "shabbat_shuvah": ("Shabbat Shuvah", "שבת שובה",
        "The Shabbat between Rosh Hashanah and Yom Kippur is named after its prophetic reading, 'Return, O "
        "Israel' (Hosea 14:2). It was traditionally the day of a rabbi's great sermon on repentance.",
        "Hos 14:2–10"),
    "shabbat_shekalim": ("Shabbat Shekalim", "שבת שקלים",
        "Read on or before 1 Adar. The Torah passage on the half-shekel each Israelite gave recalls the yearly "
        "Temple tax. The Mishnah says that collecting it was announced on 1 Adar, ready for the new Temple year "
        "beginning in Nisan.",
        "Exod 30:11–16; Mishnah Shekalim 1:1"),
    "shabbat_zachor": ("Shabbat Zachor", "שבת זכור",
        "On the Shabbat before Purim the command to 'remember (zachor) what Amalek did' is read. Haman is called "
        "'the Agagite', linking him to Agag, king of Amalek.",
        "Deut 25:17–19; 1 Sam 15; Esth 3:1"),
    "shabbat_parah": ("Shabbat Parah", "שבת פרה",
        "The law of the red heifer (parah adumah), whose ashes purified from contact with the dead, is read "
        "before Nisan. Every pilgrim had to be pure to eat the Passover offering.",
        "Num 19"),
    "shabbat_hachodesh": ("Shabbat HaChodesh", "שבת החודש",
        "On or before 1 Nisan, Exodus 12 is read: 'This month shall be for you the beginning of months.' The "
        "rabbis read this verse as the command to sanctify each new month, the basis of the whole Jewish "
        "calendar. The fixed and observed calendars in this app are two answers to it.",
        "Exod 12:1–20; Talmud Rosh Hashanah 22a"),
    "shabbat_hagadol": ("Shabbat HaGadol", "שבת הגדול",
        "The 'Great Shabbat' before Passover is probably named after its prophetic reading about 'the great day "
        "of the Lord' (Malachi 3). Medieval commentators also explain it by the Passover lambs. Those were set "
        "aside on 10 Nisan, which in the Exodus year they reckoned to have been a Sabbath.",
        "Mal 3:4–24; Exod 12:3; Tosafot to Shabbat 87b"),
    "shabbat_chazon": ("Shabbat Chazon", "שבת חזון",
        "On the Shabbat before Tisha B'Av, Isaiah 1 is read: 'The vision (chazon) of Isaiah'. It is the last of "
        "three prophetic readings of rebuke in the weeks of mourning.",
        "Isa 1:1–27"),
    "shabbat_nachamu": ("Shabbat Nachamu", "שבת נחמו",
        "On the Shabbat after Tisha B'Av, Isaiah 40 is read: 'Comfort, comfort my people'. It is the first of "
        "seven prophetic readings of consolation leading to Rosh Hashanah.",
        "Isa 40:1–26"),
}

_RULES = [
    ("Erev Rosh Hashanah", "rosh_hashanah"), ("Rosh Hashanah", "rosh_hashanah"),
    ("Tzom Gedaliah", "tzom_gedaliah"), ("Erev Yom Kippur", "yom_kippur"), ("Yom Kippur", "yom_kippur"),
    ("Erev Sukkot", "sukkot"), ("Sukkot", "sukkot"), ("Hoshana Rabbah", "hoshana_rabbah"),
    ("Shemini Atzeret", "shemini_atzeret"), ("Simchat Torah", "simchat_torah"), ("Chanukah", "chanukah"),
    ("Asara B'Tevet", "asara_btevet"), ("Tu BiShvat", "tu_bishvat"), ("Purim Katan", "purim_katan"),
    ("Shushan Purim Katan", "purim_katan"), ("Ta'anit Esther", "taanit_esther"), ("Shushan Purim", "shushan_purim"),
    ("Purim", "purim"), ("Ta'anit Bechorot", "taanit_bechorot"), ("Pesach Sheni", "pesach_sheni"),
    ("Erev Pesach", "pesach"), ("Pesach", "pesach"), ("Omer day", "omer"), ("Lag BaOmer", "lag_baomer"),
    ("Erev Shavuot", "shavuot"), ("Shavuot", "shavuot"), ("Tzom Tammuz", "tzom_tammuz"), ("17 Tammuz", "tzom_tammuz"),
    ("Tisha B'Av", "tisha_bav"), ("Tu B'Av", "tu_bav"), ("Rosh Chodesh", "rosh_chodesh"),
    ("Yom HaShoah", "yom_hashoah"), ("Yom HaZikaron", "yom_hazikaron"), ("Yom HaAtzmaut", "yom_haatzmaut"),
    ("Yom Yerushalayim", "yom_yerushalayim"), ("Shabbat Shuvah", "shabbat_shuvah"),
    ("Shabbat Shekalim", "shabbat_shekalim"), ("Shabbat Zachor", "shabbat_zachor"), ("Shabbat Parah", "shabbat_parah"),
    ("Shabbat HaChodesh", "shabbat_hachodesh"), ("Shabbat HaGadol", "shabbat_hagadol"),
    ("Shabbat Chazon", "shabbat_chazon"), ("Shabbat Nachamu", "shabbat_nachamu"),
]


def key_for(name: str) -> str | None:
    """The history entry for a holiday name as the calendars produce it."""
    for prefix, key in _RULES:
        if name.startswith(prefix):
            return key
    return None


def body_html(key: str) -> str:
    title, he, text, src = H[key]
    return (f"<div class='sl-pop-title'>{html.escape(title)} <span class='sl-he-i' lang='he' dir='rtl'>"
            f"{html.escape(he)}</span></div><div class='sl-pop-text'>{html.escape(text)}</div>"
            f"<div class='sl-pop-src'>Sources: {html.escape(src)}</div>")


def clickable(name: str, chip_html: str, align_right: bool = False) -> str:
    """Wrap a holiday chip so that clicking it opens the holiday's history (no JavaScript needed)."""
    key = key_for(name)
    if key is None:
        return chip_html
    cls = "sl-pop sl-pop-r" if align_right else "sl-pop"
    return (f"<details class='{cls}'><summary title='Click for the history of this day'>{chip_html}</summary>"
            f"<div class='sl-popbody'>{body_html(key)}</div></details>")
