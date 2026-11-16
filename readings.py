"""
Shabbat Torah readings, in the version that belongs to each calendar's tradition.

    Fixed (rabbinic)            -> rabbinic_readings   (annual cycle, Masoretic text, JPS 1917 English)
    Observed, Early Temple      -> triennial_readings  (ancient Land-of-Israel triennial cycle; a reconstruction)
    Karaite                     -> karaite_readings    (Karaite divisions and haftarot; Masoretic text)
    Samaritan                   -> samaritan_readings  (Samaritan Sabbath portions; Samaritan Pentateuch)

Each module exposes reading_for_shabbat(d, cal=None, **opts) -> dict | None (see the module docstrings for
the rules and sources). Texts live in data/readings/*.json.gz as {"meta": {...}, "books": {book: {"c:v": {"he", "en"}}}}.
If a module or text file is missing the app simply shows no reading.
"""
from __future__ import annotations

import gzip
import html
import importlib
import json
import os
import re
from datetime import date, timedelta
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT_DIR = os.path.join(HERE, "data", "readings")
TEXT_FILES = {"mt": "torah_mt.json.gz", "sp": "torah_sp.json.gz"}
BOOK_HE = {"Genesis": "בראשית", "Exodus": "שמות", "Leviticus": "ויקרא", "Numbers": "במדבר", "Deuteronomy": "דברים"}
TRADITION_LABEL = {
    "rabbinic": ("Rabbinic annual cycle", "המחזור השנתי"),
    "triennial": ("Ancient Land-of-Israel triennial cycle (reconstruction)", "המחזור התלת-שנתי של ארץ ישראל"),
    "karaite": ("Karaite reading", "קריאת הקראים"),
    "samaritan": ("Samaritan reading", "קריאת השומרונים"),
}
# options for the triennial model, set from the Settings panel each run
TRIENNIAL_OPTS: dict = {"start": "nisan", "length": "3"}

TEXT_LABEL = {
    "mt": ("Masoretic text (Westminster Leningrad Codex) · English: JPS 1917", "נוסח המסורה"),
    "sp": ("Samaritan Pentateuch (MS Nablus 6) · English: Florentin & Tal 2024", "תורת השומרונים"),
}


def _module_for(kind: str):
    import calendars as cv
    name = {cv.FIXED: "rabbinic_readings", cv.OBSERVED: "triennial_readings", cv.PRETEMPLE: "triennial_readings",
            cv.KARAITE: "karaite_readings", cv.SAMARITAN: "samaritan_readings"}.get(kind)
    if not name:
        return None
    try:
        return importlib.import_module(name)
    except Exception:
        return None


def reading_for(view, d: date) -> dict | None:
    """The reading for Shabbat d in the tradition of the calendar view (None if unavailable)."""
    import calendars as cv
    if d.weekday() != 5:
        return None
    mod = _module_for(view.kind)
    if mod is None:
        return None
    try:
        if view.kind == cv.FIXED:
            return mod.reading_for_shabbat(d, None, israel=bool(view.israel))
        if view.kind in (cv.OBSERVED, cv.PRETEMPLE):
            return mod.reading_for_shabbat(d, getattr(view, "cal", None), **TRIENNIAL_OPTS)
        return mod.reading_for_shabbat(d, getattr(view, "cal", None))
    except Exception:
        return None


def available(view) -> bool:
    return _module_for(view.kind) is not None


@lru_cache(maxsize=2)
def load_text(key: str) -> dict | None:
    path = os.path.join(TEXT_DIR, TEXT_FILES.get(key, ""))
    if not os.path.exists(path):
        return None
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=8)
def _keys(key: str, book: str) -> tuple:
    t = load_text(key)
    return tuple(t["books"].get(book, {}).keys()) if t else ()


def _base(k: str) -> str:
    return re.sub(r"[a-z]+$", "", k)


def verses(key: str, book: str, frm: str, to: str) -> list[tuple[str, str, str]]:
    """[(ref, hebrew, english)] from verse frm to verse to inclusive (plus any lettered verses after `to`)."""
    t = load_text(key)
    ks = _keys(key, book)
    if not t or frm not in ks:
        return []
    i = ks.index(frm)
    j = max((n for n, k in enumerate(ks) if _base(k) == to), default=None)
    if j is None or j < i:
        return []
    b = t["books"][book]
    return [(k, b[k].get("he", ""), b[k].get("en", "")) for k in ks[i:j + 1]]


def ref_text(rng: dict) -> str:
    a, b = rng["from"], rng["to"]
    ca, cb = a.split(":")[0], b.split(":")[0]
    end = b.split(":")[1] if ca == cb else b
    return f"{rng['book']} {a}–{end}"


def refs_text(rngs: list[dict]) -> str:
    return "; ".join(ref_text(r) for r in rngs)


def _section(key: str, rngs: list[dict], phone: bool) -> tuple[str, int]:
    out, n = [], 0
    for r in rngs:
        vs = verses(key, r["book"], r["from"], r["to"])
        if not vs:
            continue
        out.append(f"<div class='sl-read-ref'>{html.escape(ref_text(r))} · "
                   f"<span lang='he' dir='rtl'>{BOOK_HE.get(r['book'], '')}</span></div>")
        cls = "sl-read sl-read-phone" if phone else "sl-read"
        rows = []
        for ref, he, en in vs:
            n += 1
            rows.append(f"<div class='sl-vrow'><div class='sl-ven'><span class='sl-vnum'>{html.escape(ref)}</span> "
                        f"{html.escape(en)}</div><div class='sl-vhe' lang='he' dir='rtl'>{html.escape(he)}</div></div>")
        out.append(f"<div class='{cls}'>" + "".join(rows) + "</div>")
    return "".join(out), n


def render_html(rd: dict, phone: bool = False) -> str:
    """Heading, references and the full text (Hebrew and English side by side) for a reading."""
    key = rd.get("text", "mt")
    t = load_text(key)
    trad = TRADITION_LABEL.get(rd.get("tradition"), ("", ""))
    head = (f"<div class='sl-big'>{html.escape(rd.get('name_en', ''))} "
            f"<span class='sl-he' lang='he' dir='rtl'>{html.escape(rd.get('name_he', ''))}</span></div>"
            f"<div class='sl-muted'>{html.escape(trad[0])} · <span lang='he' dir='rtl'>{trad[1]}</span>"
            + (f" · {html.escape(rd['special'])}" if rd.get("special") else "") + "</div>")
    if rd.get("torah"):
        lines = [f"<div><b>Torah:</b> {html.escape(refs_text(rd['torah']))}</div>"]
    else:
        lines = ["<div><b>Festival Sabbath.</b> The weekly cycle pauses. The festival's own Torah reading in this "
                 "tradition is not documented in the sources this app uses, so no text is shown.</div>"]
    extra_lab = ("Additional verse", "תוספת") if rd.get("tradition") == "samaritan" else ("Maftir", "מפטיר")
    if rd.get("maftir"):
        lines.append(f"<div><b>{extra_lab[0]}:</b> {html.escape(refs_text(rd['maftir']))}</div>")
    for h in rd.get("haftarah", []):
        lines.append(f"<div><b>Haftarah ({html.escape(h.get('label', ''))}):</b> {html.escape(h.get('ref', ''))}</div>")
    if not rd.get("haftarah") and rd.get("tradition") == "samaritan":
        lines.append("<div class='sl-muted'>No haftarah: the Samaritan scriptures are the Torah alone.</div>")
    note = ""
    if rd.get("model"):
        note += "<div class='sl-muted'><b>Modelled schedule:</b> reconstructed from published sources, not an official list.</div>"
    if rd.get("note"):
        note += f"<div class='sl-muted'>{html.escape(rd['note'])}</div>"
    if t is None:
        return head + "".join(lines) + note + "<div class='sl-muted'>The text file for this reading is not installed.</div>"
    body, n1 = _section(key, rd.get("torah", []), phone)
    if rd.get("maftir"):
        mb, n2 = _section(key, rd["maftir"], phone)
        body += f"<div class='sl-read-ref'><b>{extra_lab[0]} · {extra_lab[1]}</b></div>" + mb
    src = TEXT_LABEL.get(key, ("", ""))
    meta = t.get("meta", {})
    credit = (f"<div class='sl-muted' style='margin-top:.5rem'>{html.escape(src[0])}. "
              f"{html.escape(meta.get('attribution', ''))}"
              + (f" Licence: {html.escape(meta['license'])}." if meta.get("license") else "") + "</div>")
    return head + "".join(lines) + note + body + credit


def shabbatot(start: date, n: int) -> list[date]:
    s = start + timedelta(days=(5 - start.weekday()) % 7)
    return [s + timedelta(days=7 * i) for i in range(n)]
