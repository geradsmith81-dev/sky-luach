"""Checks for karaite_readings.py; prints a JSON summary. Run from the repo root:
python tools/validate_karaite_readings.py"""
import gzip, json, os, re, sys
from collections import Counter
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fixed_calendar as fc
import karaite_calendar as kc
import karaite_readings as kr

R = {}
data = kr._data()["parashot"]
mt = json.load(gzip.open("data/readings/torah_mt.json.gz", "rt", encoding="utf-8"))["books"]

# 1. data: tiling
R["portions"] = len(data)
R["verses_covered"] = sum(p["verses"] for p in data)
R["verses_in_text"] = sum(len(v) for v in mt.values())
R["misprints_corrected"] = [p["name_en"] for p in data if re.search(r"prints|omits|ends at", p["correction"])]

# 2. boundaries vs hebcal-leyning (rabbinic) table
rl = json.load(open("data/readings/rabbinic_leyning.json", encoding="utf-8"))["parshiyot"]
rab = sorted([(v["num"], k, v) for k, v in rl.items() if isinstance(v, dict) and isinstance(v.get("num"), int)
              and v["num"] <= 54], key=lambda x: x[0])
assert [n for n, _, _ in rab] == list(range(1, 55)), "rabbinic table not 54 single portions"
bm, bd = 0, []
hm_ash = []
def start(s):
    m = re.match(r"(.+?)\s+(\d+):(\d+)", s.replace("I Kings", "1 Kings").replace("II Kings", "2 Kings")
                 .replace("I Samuel", "1 Samuel").replace("II Samuel", "2 Samuel"))
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else None
for (n, k, v), p in zip(rab, data):
    fk = v["fullkriyah"]
    if (fk["1"][0], fk["7"][1]) == (p["from"], p["to"]):
        bm += 1
    else:
        bd.append([k, fk["1"][0], fk["7"][1], p["from"], p["to"]])
    h = v.get("haft")
    h = h[0] if isinstance(h, list) else h
    if isinstance(h, dict) and start(f'{h["k"]} {h["b"]}') == start(p["haftarah"]):
        hm_ash.append(p["name_en"])
R["boundaries_same_as_rabbinic"] = bm
R["boundaries_different"] = bd
R["haftarah_same_start_as_ashkenazi"] = [len(hm_ash), hm_ash]

# 3. KJA haftarot vs Kale 1733
ex, st, diff = [], [], []
for p in data:
    k = p["haftarah_kale_1733"]
    if not k:
        continue
    opts = [o.replace(" ", "") for o in k.split(" or ")]
    if p["haftarah"].replace(" ", "") in opts:
        ex.append(p["name_en"])
    elif start(p["haftarah"]) in [start(o) for o in k.split(" or ")]:
        st.append(p["name_en"])
    else:
        diff.append([p["name_en"], p["haftarah"], k])
R["kale_compared"] = len(ex) + len(st) + len(diff)
R["kale_exact"] = [len(ex), ex]
R["kale_same_start_other_end"] = [len(st), st]
R["kale_different"] = [len(diff), diff]

# 4. schedule over all covered reading years
cal = kc.KaraiteCalendar()
years = [y for y in range(5400, 6200) if cal.year_complete(y) and cal.year_complete(y + 1)]
R["years"] = [years[0], years[-1], len(years)]
fails = Counter(); patterns = Counter(); rules = Counter(); haaz = Counter(); nsab = 0; nfest = 0
first = last = None
for y in years:
    rs = kr.year_readings(y, cal)
    nsab += len(rs); nfest += sum(1 for r in rs if r["torah"] == [])
    first = first or rs[0]["date"]; last = rs[-1]["date"]
    seen = Counter()
    for r in rs:
        if r["special"] or not r["torah"]:
            continue
        for t in r["torah"]:
            i = next(i for i, p in enumerate(data) if p["book"] == t["book"] and p["from"] <= t["from"] and
                     (data[i + 1]["book"] != t["book"] or True) and p["book"] == t["book"] and
                     list(mt[p["book"]]).index(p["from"]) <= list(mt[t["book"]]).index(t["from"]) <= list(mt[p["book"]]).index(p["to"]))
            if t["from"] == data[i]["from"]:
                seen[i] += 1
        if "-" in r["name_en"] and "(part" not in r["name_en"]:
            patterns[r["name_en"]] += 1
        if "(part" in r["name_en"]:
            patterns[r["name_en"].split(" (")[0] + " split"] += 1
    haaz[seen[kr.HAAZINU]] += 1
    for i in range(0, kr.HAAZINU):
        if seen[i] != 1:
            fails[f"portion {i} read {seen[i]} times"] += 1
    if seen[kr.HAAZINU] < 1:
        fails["no Haazinu"] += 1
    sched = {date.fromisoformat(r["date"]): r for r in rs}
    shav = kr._shavuot(cal, y)
    if sched.get(shav - timedelta(days=1), {}).get("name_en") != "Nasso":
        fails["Naso not on Sabbath before Shavuot"] += 1
    t9, a10 = cal.to_gregorian(y, 4, 9), cal.to_gregorian(y, 5, 10)
    for d, r in sched.items():
        names = r["name_en"].split("-")
        if any(n in ("Balak", "Pinchas", "Matot", "Masei", "Devarim") for n in names) and not (t9 <= d <= a10):
            fails["mourning portion outside 9 Tammuz-10 Av"] += 1
        if t9 <= d <= a10 and not any(n in ("Balak", "Pinchas", "Matot", "Masei", "Devarim") for n in names):
            fails["other portion inside 9 Tammuz-10 Av"] += 1
    st22 = cal.to_gregorian(y, 7, 22)
    b = min(d for d in sched if d > st22)
    if sched[b]["name_en"] != "Bereshit":
        fails["Bereshit not first Sabbath after 22 Tishrei"] += 1
    va = min(d for d in sched if d > a10)
    if not sched[va]["name_en"].startswith("Va'etchanan"):
        fails["Va'etchanan not first Sabbath after 10 Av"] += 1
    for r in rs:
        for t in r["torah"]:
            if t["from"] not in mt[t["book"]] or t["to"] not in mt[t["book"]]:
                fails["verse reference missing from text"] += 1
R["sabbaths"] = nsab; R["festival_sabbaths_without_reading"] = nfest; R["first_last"] = [first, last]
R["anchor_failures"] = dict(fails)
R["haazinu_sabbaths_per_year"] = dict(sorted(haaz.items()))
R["combination_patterns"] = dict(patterns.most_common())

# 5. contract
R["non_saturday_none"] = kr.reading_for_shabbat(date(2026, 11, 16)) is None
R["out_of_range_none"] = kr.reading_for_shabbat(date(1700, 1, 2)) is None and kr.reading_for_shabbat(date(2300, 1, 6)) is None
keys = {"date", "tradition", "name_en", "name_he", "torah", "maftir", "haftarah", "special", "text", "model", "note"}
r = kr.reading_for_shabbat(date(2026, 11, 14))
R["keys_ok"] = set(r) == keys

# 6. same portion as the rabbinic (Israel) calendar on the same Sabbath
same = tot = 0
cache = {}
for y in years:
    for r in kr.year_readings(y, cal):
        if not r["torah"] or r["special"]:
            continue
        d = date.fromisoformat(r["date"])
        hy = fc.from_gregorian(d).year
        if hy not in cache:
            cache[hy] = fc.parshiyot_for_year(hy, True)
        rab_i = cache[hy].get(d.toordinal())
        if not rab_i:
            continue
        tot += 1
        k_first = next(i for i, p in enumerate(data) if p["book"] == r["torah"][0]["book"] and p["from"] == r["torah"][0]["from"]) \
            if any(p["book"] == r["torah"][0]["book"] and p["from"] == r["torah"][0]["from"] for p in data) else None
        if k_first is not None and k_first == rab_i[0] and len(r["torah"]) == len(rab_i):
            same += 1
R["same_as_rabbinic_israel"] = [same, tot]
print(json.dumps(R, ensure_ascii=False, indent=1))
