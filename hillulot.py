"""
Hillula days (יום הילולא): the anniversaries of the passing of great righteous figures (tzaddikim).

The word comes from the Zohar (Idra Zuta), which describes the death of Rabbi Shimon bar Yochai as a
wedding celebration (hillula), the soul's union with its source. Visiting graves and festive gatherings on
these days are strong customs among Sephardi and Mizrahi Jews (above all Moroccan Jews) and in the Chasidic
world; other communities mark some of them in study and prayer.

Rules used here
* Each day is kept on its Hebrew date, from sunset to sunset, and is never moved for Shabbat.
* A figure who died in a known year is shown only in later years.
* Adar in a leap year: a death in the Adar of an ordinary year (or a traditional Adar date) is shown in
  Adar I, the Ashkenazi custom (Rema, Orach Chayim 568:7); Sephardim keep it in Adar II. A death in Adar II
  is kept in Adar II in leap years and in Adar otherwise.
* The biblical dates follow the list of fasts for the righteous in the Shulchan Aruch (Orach Chayim 580:2),
  the Torah itself (Aaron), the Talmud (Moses, David) or long tradition (Rachel, Rabbi Meir, Rabbi Shimon bar
  Yochai, Rabbi Yehuda HaNasi).
* Shown in the fixed, observed and Early Temple Period calendars. Karaites and Samaritans do not keep them.
"""
from __future__ import annotations

from dataclasses import dataclass

import fixed_calendar as fc
from fixed_calendar import (NISAN, IYYAR, SIVAN, TAMMUZ, AV, ELUL, TISHREI, MARHESHVAN, KISLEV, TEVET, SHEVAT,
                            ADAR, ADAR_II)


@dataclass(frozen=True)
class Tzaddik:
    key: str
    month: int
    day: int
    name: str          # English, as shown on the chip after "Hillula: "
    he: str            # Hebrew
    died_am: int | None
    era: str           # dates of life, CE
    text: str
    sources: str


T = [
    Tzaddik("miriam", NISAN, 10, "Miriam the Prophetess", "מרים הנביאה", None, "biblical",
            "Sister of Moses and Aaron, she led the women in song and dance after the crossing of the Sea. She "
            "died at Kadesh in the wilderness, and the rabbis taught that the well which followed Israel was given "
            "in her merit and vanished at her death. The Shulchan Aruch lists 10 Nisan among the days on which the "
            "pious fasted for the death of the righteous.",
            "Exod 15:20–21; Num 20:1–2; Talmud Ta'anit 9a; Shulchan Aruch OC 580:2"),
    Tzaddik("joshua", NISAN, 26, "Joshua son of Nun", "יהושע בן נון", None, "biblical",
            "Moses' attendant and successor, who led Israel across the Jordan and into the land. He was buried at "
            "Timnath-serah in the hill country of Ephraim. Many identify the place with Kifl Haris in Samaria, "
            "where thousands of pilgrims gather at night on his yahrzeit. The date comes from the Shulchan Aruch's "
            "list of fasts for the righteous.",
            "Josh 24:29–30; Judg 2:8–9; Shulchan Aruch OC 580:2"),
    Tzaddik("samuel", IYYAR, 28, "Samuel the Prophet", "שמואל הנביא", None, "biblical",
            "The last of the judges, who anointed both Saul and David. The Bible says he was buried in his home "
            "town, Ramah. Since the Middle Ages tradition has placed his tomb at Nebi Samwil, on the hill north "
            "of Jerusalem, which became a pilgrimage site on this date.",
            "1 Sam 25:1, 28:3; Shulchan Aruch OC 580:2"),
    Tzaddik("aaron", AV, 1, "Aaron the Priest", "אהרן הכהן", None, "biblical",
            "The only yahrzeit stated in the Torah itself: Aaron, the first high priest, died on Mount Hor 'in the "
            "fortieth year after the Israelites had come out of the land of Egypt, on the first day of the fifth "
            "month'. All Israel mourned him for thirty days. The Mishnah remembers him as one who loved peace and "
            "pursued peace.",
            "Num 20:22–29, 33:38–39; Mishnah Avot 1:12"),
    Tzaddik("moses", ADAR, 7, "Moses our Teacher", "משה רבנו", None, "biblical",
            "The Talmud derives from the verses that Moses was born and died on 7 Adar. 'No one knows his burial "
            "place to this day', so the day has no grave pilgrimage. Instead, burial societies (chevra kadisha) "
            "traditionally fast on it and hold their annual feast. Customs differ on which Adar keeps it in a leap "
            "year.",
            "Deut 34:5–8; Talmud Kiddushin 38a, Megillah 13b; Shulchan Aruch OC 580:2"),
    Tzaddik("rachel", MARHESHVAN, 11, "Rachel our Mother", "רחל אמנו", None, "biblical",
            "Jacob's beloved wife died giving birth to Benjamin and was buried 'on the way to Ephrath, that is "
            "Bethlehem'. Jeremiah's image of 'Rachel weeping for her children' made her the mother who prays for "
            "the exiles. On this date, fixed by later tradition, tens of thousands visit Rachel's Tomb at the "
            "entrance to Bethlehem, a domed building of the Ottoman period that Moses Montefiore restored in 1841.",
            "Gen 35:16–20; Jer 31:15–17"),
    Tzaddik("david", SIVAN, 6, "King David", "דוד המלך", None, "biblical",
            "The Jerusalem Talmud records that David died on Shavuot. This is one reason the Book of Ruth, which ends "
            "with his genealogy, is read on the festival. The traditional tomb on Mount Zion is a medieval "
            "identification, first described in the 12th century; the Bible places his burial in the City of "
            "David.",
            "1 Kgs 2:10; Ruth 4:17–22; Jerusalem Talmud Chagigah 2:3, Beitzah 2:4"),
    Tzaddik("rabbi_meir", IYYAR, 14, "Rabbi Meir Baal HaNes", "רבי מאיר בעל הנס", None, "2nd century",
            "A leading sage of the 2nd century, a student of Rabbi Akiva and husband of the learned Beruriah. The "
            "Talmud says that an anonymous statement in the Mishnah follows Rabbi Meir. He is called 'master of "
            "the miracle' after a Talmudic story in which he rescued his sister-in-law from captivity in Rome. "
            "Crowds gather at his tomb above the hot springs of Tiberias on Pesach Sheni, the traditional date.",
            "Talmud Sanhedrin 86a, Avodah Zarah 18a–b, Eruvin 13b"),
    Tzaddik("rashbi", IYYAR, 18, "Rabbi Shimon bar Yochai", "רבי שמעון בר יוחאי", None, "2nd century",
            "A student of Rabbi Akiva who, the Talmud relates, hid from the Romans in a cave with his son for "
            "thirteen years. Kabbalists attribute the Zohar to him. The Zohar's account of his death as a wedding "
            "feast gave the hillula its name. Since the 16th century, when the circle of the Ari in Safed celebrated "
            "it, Lag BaOmer has been kept as his hillula at Meron, with bonfires, music and the first haircut of "
            "three-year-old boys.",
            "Talmud Shabbat 33b; Zohar III, Idra Zuta 287b–296b; Chaim Vital, Sha'ar HaKavanot"),
    Tzaddik("rabbi", KISLEV, 15, "Rabbi Yehuda HaNasi", "רבי יהודה הנשיא", None, "c. 135–217",
            "The Patriarch who edited the Mishnah around 200 CE, known simply as 'Rabbi'. The Talmud says he was "
            "buried at Beit She'arim in the Lower Galilee. Excavations there by Benjamin Mazar and Nahman Avigad "
            "uncovered a great necropolis of the 2nd–4th centuries. Catacomb 14, with inscriptions naming Rabbi "
            "Shimon and Rabbi Gamaliel (both names of his sons), has been proposed as his family's tomb, though "
            "the identification is debated. 15 Kislev is the traditional date.",
            "Talmud Ketubot 103a–104a; N. Avigad, Beth She'arim III (1976); B. Mazar, Beth She'arim I (1973)"),
    Tzaddik("rashi", TAMMUZ, 29, "Rashi", "רש״י", 4865, "1040–1105",
            "Rabbi Shlomo Yitzchaki of Troyes in Champagne. His commentaries on the Bible and the Talmud are printed "
            "in almost every edition, and his Torah commentary is the earliest dated Hebrew printed book (Reggio di "
            "Calabria, 1475). He explained difficult words in Old French written in Hebrew letters, which makes his "
            "work a source for the history of French.",
            "A. Grossman, Rashi (2012)"),
    Tzaddik("rambam", TEVET, 20, "Maimonides (Rambam)", "הרמב״ם", 4965, "1138–1204",
            "Rabbi Moses ben Maimon, born in Córdoba, later court physician in Fustat (Old Cairo). He wrote the "
            "Mishneh Torah, the first complete code of Jewish law, and the Guide for the Perplexed. His Laws of the "
            "Sanctification of the Month set out the rules this app follows for the fixed and observed calendars. "
            "Tradition holds that he was buried in Tiberias.",
            "Maimonides, Mishneh Torah, Kiddush HaChodesh; H. Davidson, Moses Maimonides (2005)"),
    Tzaddik("karo", NISAN, 13, "Rabbi Yosef Karo", "רבי יוסף קארו", 5335, "1488–1575",
            "Born in Iberia before the expulsion, he settled in Safed, where he wrote the Beit Yosef and its "
            "summary, the Shulchan Aruch (Venice, 1565). With the Rema's Ashkenazi glosses, the Shulchan Aruch "
            "became the standard code of Jewish law. He is buried in the old cemetery of Safed.",
            "Shulchan Aruch; R. J. Z. Werblowsky, Joseph Karo, Lawyer and Mystic (1962)"),
    Tzaddik("ari", AV, 5, "The Ari (Rabbi Isaac Luria)", "האר״י הקדוש", 5332, "1534–1572",
            "Born in Jerusalem and raised in Egypt, he came to Safed in about 1570 and taught there for only two "
            "years before dying in an epidemic. His teachings on creation, exile and repair (tikkun), written down "
            "by his student Chaim Vital, shaped all later Kabbalah, and the Kabbalat Shabbat service grew up in "
            "his circle. His grave in Safed is visited all year.",
            "Chaim Vital, Etz Chaim; L. Fine, Physician of the Soul, Healer of the Cosmos (2003)"),
    Tzaddik("or_hachaim", TAMMUZ, 15, "The Or HaChaim (Rabbi Chaim ibn Attar)", "האור החיים הקדוש", 5503, "1696–1743",
            "Born in Salé, Morocco, he led a group of students to Jerusalem in 1742 and died there the next year. "
            "His Torah commentary, Or HaChaim, is studied widely by both Moroccan and Chasidic Jews. Tradition says "
            "the Baal Shem Tov held him in the highest esteem. He is buried on the Mount of Olives.",
            "Chaim ibn Attar, Or HaChaim (Venice, 1742)"),
    Tzaddik("ramchal", IYYAR, 26, "The Ramchal (Rabbi Moshe Chaim Luzzatto)", "הרמח״ל", 5506, "1707–1746",
            "A poet, dramatist and kabbalist from Padua whose mystical writings drew the opposition of the Venetian "
            "rabbis. He moved to Amsterdam and then to Acre, where he died of plague. His ethical guide, Mesillat "
            "Yesharim ('The Path of the Upright'), became a classic of the Musar movement. Tradition places his "
            "grave in Tiberias.",
            "Luzzatto, Mesillat Yesharim (Amsterdam, 1740); J. Garb, Kabbalist in the Heart of the Storm (2014)"),
    Tzaddik("besht", SIVAN, 6, "The Baal Shem Tov", "הבעל שם טוב", 5520, "c. 1700–1760",
            "Rabbi Israel ben Eliezer, healer and teacher of Medzhybizh in Podolia (now Ukraine), and the founder "
            "of Chasidism. He taught that God can be served with joy in every act. He died on the first day of "
            "Shavuot, so his yahrzeit and King David's fall on the same day. His teachings survive through his "
            "disciples' books and the stories of Shivchei HaBesht (1815). Pilgrims visit his grave in Medzhybizh.",
            "Ya'akov Yosef of Polonne, Toldot Ya'akov Yosef (1780); M. Rosman, Founder of Hasidism (1996)"),
    Tzaddik("maggid", KISLEV, 19, "The Maggid of Mezritch", "המגיד ממזריטש", 5533, "d. 1772",
            "Rabbi Dov Ber, the Baal Shem Tov's successor, who made Chasidism an organised movement. His disciples "
            "carried it across Ukraine, Poland and Belarus. Chabad also keeps 19 Kislev as the day its founder, the "
            "Maggid's student Rabbi Shneur Zalman, was freed from prison in 1798.",
            "Dov Ber, Maggid Devarav le-Ya'akov (1781)"),
    Tzaddik("elimelech", ADAR, 21, "Rabbi Elimelech of Lizhensk", "רבי אלימלך מליזנסק", 5547, "1717–1787",
            "A disciple of the Maggid of Mezritch whose book Noam Elimelech (1788) set out the role of the tzaddik "
            "as the spiritual leader of his community. Thousands of Chasidim travel each year to his grave in "
            "Leżajsk, south-eastern Poland, on his yahrzeit.",
            "Elimelech of Lizhensk, Noam Elimelech (Lviv, 1788)"),
    Tzaddik("rashash", SHEVAT, 10, "The Rashash (Rabbi Shalom Sharabi)", "הרש״ש", 5537, "1720–1777",
            "Born in Yemen, he reached Jerusalem by way of India, Baghdad and Damascus. There he became head of the "
            "Beit El yeshiva of kabbalists. His prayer book of kabbalistic intentions (kavanot) is still used there "
            "and in Sephardi kabbalist circles. He is buried on the Mount of Olives. Most sources give 1777, "
            "following his gravestone; a few give 1782.",
            "Sharabi, Nahar Shalom; Siddur HaRashash"),
    Tzaddik("gra", TISHREI, 19, "The Vilna Gaon", "הגאון מווילנא", 5558, "1720–1797",
            "Rabbi Eliyahu ben Shlomo Zalman of Vilna, the leading scholar of Lithuanian Jewry. His commentaries "
            "range over the whole of rabbinic literature, and he led the opposition to Chasidism. He died during "
            "Sukkot. From 1808 his students, the Perushim, settled in Safed and Jerusalem.",
            "I. Etkes, The Gaon of Vilna (2002)"),
    Tzaddik("berditchev", TISHREI, 25, "Rabbi Levi Yitzchak of Berditchev", "רבי לוי יצחק מברדיטשוב", 5570, "1740–1809",
            "A disciple of the Maggid of Mezritch, remembered as the 'defender of Israel', who argued with God in "
            "prayer on behalf of his people. His Torah commentary is Kedushat Levi. Yiddish songs and stories about "
            "him are still sung and told.",
            "Levi Yitzchak, Kedushat Levi (1798)"),
    Tzaddik("chatam_sofer", TISHREI, 25, "The Chatam Sofer (Rabbi Moshe Sofer)", "החתם סופר", 5600, "1762–1839",
            "Rabbi of Pressburg (Bratislava) and head of its great yeshiva. He led traditional opposition to the "
            "Reform movement with the motto 'the new is forbidden by the Torah'. His grave survives in the "
            "underground Chatam Sofer Memorial, built when the rest of the old cemetery was destroyed.",
            "Moshe Sofer, She'elot u-Teshuvot Chatam Sofer"),
    Tzaddik("nachman", TISHREI, 18, "Rabbi Nachman of Breslov", "רבי נחמן מברסלב", 5571, "1772–1810",
            "Great-grandson of the Baal Shem Tov, a teacher of personal prayer (hitbodedut), joy and faith, and "
            "author of Likutei Moharan and the mystical Tales (Sippurei Ma'asiyot). He died during Sukkot in Uman, "
            "Ukraine. Tens of thousands of his followers travel there every Rosh Hashanah, at his request.",
            "Nachman of Breslov, Likutei Moharan; A. Green, Tormented Master (1979)"),
    Tzaddik("alter_rebbe", TEVET, 24, "Rabbi Shneur Zalman of Liadi", "רבי שניאור זלמן מליאדי (בעל התניא)", 5573, "1745–1812",
            "Founder of Chabad Chasidism and author of the Tanya (1796/97) and the Shulchan Aruch HaRav. He died in "
            "the village of Piena while fleeing Napoleon's advance into Russia, and was buried in Hadiach "
            "(Ukraine).",
            "Shneur Zalman of Liadi, Likutei Amarim (Tanya); I. Etkes, Rabbi Shneur Zalman of Liady (2015)"),
    Tzaddik("pinto", ELUL, 26, "Rabbi Haim Pinto", "רבי חיים פינטו", 5605, "1743–1845",
            "Chief rabbi of Essaouira (Mogador), Morocco, from a celebrated family of rabbis. His hillula is one of "
            "the great Moroccan pilgrimages. Every year Jews from Morocco, Israel, France and the Americas gather "
            "at his tomb in the old Jewish cemetery of Essaouira.",
            "Diarna archive, 'Tomb of Rabbi Haim Pinto, Essaouira'"),
    Tzaddik("abir_yaakov", TEVET, 20, "Rabbi Yaakov Abuhatzeira (Abir Yaakov)", "רבי יעקב אביחצירא", 5640, "1806–1880",
            "A kabbalist and scholar of the Tafilalt region of Morocco, author of many works. He died at Damanhur "
            "in Egypt on his way to the Land of Israel, and his tomb there was long a pilgrimage site. He was the "
            "grandfather of the Baba Sali. His yahrzeit falls on the same day as Maimonides'.",
            "Yaakov Abuhatzeira, Pituchei Chotam"),
    Tzaddik("salanter", SHEVAT, 25, "Rabbi Yisrael Salanter", "רבי ישראל סלנטר", 5643, "1809–1883",
            "Rabbi Yisrael Lipkin of Salant, founder of the Musar movement, which taught daily study of ethics and "
            "self-examination in the Lithuanian yeshivot. He died in Königsberg.",
            "I. Etkes, Rabbi Israel Salanter and the Mussar Movement (1993)"),
    Tzaddik("ben_ish_chai", ELUL, 13, "The Ben Ish Chai (Rabbi Yosef Chaim)", "הבן איש חי", 5669, "1835–1909",
            "The great sage of Baghdad, whose Ben Ish Chai sets out Jewish law in sermons arranged by the weekly "
            "Torah portion. It remains a standard guide for Iraqi and other Sephardi communities.",
            "Yosef Chaim, Ben Ish Chai"),
    Tzaddik("chofetz_chaim", ELUL, 24, "The Chofetz Chaim (Rabbi Yisrael Meir Kagan)", "החפץ חיים", 5693, "1838–1933",
            "A sage of Radun (now Belarus). His first book, Chafetz Chaim (1873), on the laws against gossip and "
            "slander, gave him his name. His Mishnah Berurah became the standard Ashkenazi guide to daily "
            "practice.",
            "Kagan, Chafetz Chaim (1873); Mishnah Berurah (1884–1907)"),
    Tzaddik("rav_kook", ELUL, 3, "Rav Kook (Rabbi Avraham Yitzchak HaKohen Kook)", "הרב אברהם יצחק הכהן קוק", 5695, "1865–1935",
            "The first Ashkenazi Chief Rabbi of Mandatory Palestine (from 1921). He was a mystic and thinker who saw "
            "the Zionist return as part of redemption. His thought shapes religious Zionism to this day. He is "
            "buried on the Mount of Olives.",
            "Kook, Orot (1920); Y. Mirsky, Rav Kook (2014)"),
    Tzaddik("rayatz", SHEVAT, 10, "Rabbi Yosef Yitzchak Schneersohn", "רבי יוסף יצחק שניאורסון (הריי״צ)", 5710, "1880–1950",
            "The sixth Lubavitcher Rebbe. The Soviets arrested him in 1927 for keeping Jewish life going in Russia "
            "and freed him on 12 Tammuz. He escaped Warsaw in 1940 and rebuilt Chabad in Brooklyn. His successor "
            "formally accepted the leadership on this day a year after his death.",
            "A. C. Glitzenstein, Sefer HaToldot: Rabbi Yosef Yitzchak"),
    Tzaddik("baba_sali", SHEVAT, 4, "The Baba Sali (Rabbi Yisrael Abuhatzeira)", "הבבא סאלי", 5744, "1889–1984",
            "A kabbalist from the Tafilalt in Morocco, renowned for his blessings. He moved to Israel in 1964 and "
            "settled in Netivot. His hillula there draws enormous crowds and is one of the largest gatherings in "
            "Israel.",
            "Y. Bilu and E. Ben-Ari, 'The Making of Modern Saints', American Ethnologist 19 (1992)"),
    Tzaddik("feinstein", ADAR_II, 13, "Rabbi Moshe Feinstein", "רבי משה פיינשטיין", 5746, "1895–1986",
            "Born in Belarus, he emigrated in 1937 and headed the Mesivtha Tifereth Jerusalem yeshiva on New York's Lower East Side. His responsa, Igrot "
            "Moshe, answered the questions of modern life and made him the leading halakhic authority of American "
            "Jewry. He died on the Fast of Esther and is buried in Jerusalem.",
            "Feinstein, Igrot Moshe (1959–)"),
    Tzaddik("rebbe", TAMMUZ, 3, "The Lubavitcher Rebbe (Rabbi Menachem Mendel Schneerson)", "הרבי מליובאוויטש", 5754, "1902–1994",
            "The seventh Lubavitcher Rebbe, leader of Chabad from 1950. He built its worldwide network of emissaries "
            "and outreach. Tens of thousands visit his resting place, the Ohel, in Queens, New York, on Gimmel "
            "Tammuz (3 Tammuz).",
            "S. Heilman and M. Friedman, The Rebbe (2010); J. Telushkin, Rebbe (2014)"),
    Tzaddik("ovadia", MARHESHVAN, 3, "Rabbi Ovadia Yosef", "רבי עובדיה יוסף", 5774, "1920–2013",
            "Born in Baghdad and raised in Jerusalem, he was Sephardi Chief Rabbi of Israel (1973–1983) and author "
            "of the responsa Yabia Omer and Yechaveh Da'at. He worked to restore pride in Sephardi tradition and "
            "was the spiritual leader of the Shas party. His funeral was among the largest in Israel's history.",
            "Ovadia Yosef, Yabia Omer; Yechaveh Da'at"),
]
BY_KEY = {t.key: t for t in T}
KIND = "hillula"


def _month_for(t: Tzaddik, leap: bool) -> int:
    if t.month == ADAR_II:
        return ADAR_II if leap else ADAR
    if t.month == ADAR:
        return ADAR          # Adar I in a leap year (Rema); Adar in an ordinary year
    return t.month


def chip_name(t: Tzaddik) -> str:
    return f"Hillula: {t.name}"


def for_year(year: int, to_greg, is_leap, make_hdate) -> list:
    """Holiday objects for Hebrew `year` using the calendar's own conversion functions."""
    from fixed_calendar import Holiday
    out = []
    leap = is_leap(year)
    for t in T:
        if t.died_am is not None and year <= t.died_am:
            continue
        m = _month_for(t, leap)
        g = to_greg(year, m, t.day)
        if g is None:
            continue
        note = t.era if t.era != "biblical" else "biblical"
        if leap and t.month == ADAR:
            note += "; leap year: shown in Adar I (Ashkenazi custom), Sephardim keep it in Adar II"
        out.append(Holiday(g, chip_name(t), f"הילולת {t.he}", KIND, make_hdate(year, m, t.day), note))
    return out


def history_entries() -> tuple[dict, list]:
    """(entries for holiday_history.H, prefix rules) so every hillula chip opens its short history."""
    H, rules = {}, []
    for t in T:
        k = f"hillula_{t.key}"
        H[k] = (f"Hillula of {t.name}" + (f" ({t.era})" if t.era != "biblical" else ""), f"הילולת {t.he}",
                t.text, t.sources)
        rules.append((chip_name(t), k))
    return H, rules
