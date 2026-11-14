"""Colours, fonts and ornament for a theme drawn from First Temple period (Iron Age II) art.

Palette: cedar panelling (1 Kgs 6:15-18), carved ivory (Samaria ivories, 1 Kgs 22:39, Amos 3:15), gold leaf,
bronze (Jachin and Boaz), and the Tabernacle colours tekhelet (blue), argaman (purple) and
tola'at shani (scarlet), Exod 26:1. Ornaments: see ornaments.py.

Every text colour has at least 7:1 contrast (WCAG AAA) on its background: ivory 12.3-15.3:1,
muted/gold/link/olive 8.4-13.1:1, holiday chips (cedar ink on pastel) 10.9-14.5:1, white on argaman 7.9:1.
"""
import base64
import html
import os

import streamlit as st

import hebrew_names as hn
import ornaments as orn

HERE = os.path.dirname(os.path.abspath(__file__))

BG = "#1a120c"          # cedar
CARD = "#2a1d13"        # cedar panel
SIDEBAR = "#221810"
SHABBAT_BG = "#1c2740"  # deep tekhelet
TEXT = "#f3e9d2"        # ivory
MUTED = "#dccdab"
GOLD = "#e8bd5c"
LINK = "#a9c9f0"        # light tekhelet
OBS = "#cfe0a0"         # olive
INK = "#1a120c"
ARGAMAN = "#7a3a6e"
TEKHELET = "#3f6aa8"
SCARLET = "#b23a32"
BRONZE = "#b8834a"

CHIP = {
    "major": "#e9c46a", "fast": "#cfc6b4", "chol": "#efe3c8", "minor": "#bcd39a",
    "rosh_chodesh": "#b3cdee", "modern": "#a8dbd6", "special_shabbat": "#ddbfd6",
    "erev": "#e0d6c4", "omer": "#e3d38f",
}
KIND_LABEL = {
    "major": "Festival (no work)", "fast": "Fast", "chol": "Chol HaMoed", "minor": "Minor holiday",
    "rosh_chodesh": "Rosh Chodesh", "modern": "Israeli national day", "special_shabbat": "Special Shabbat",
    "erev": "Eve", "omer": "Omer count",
}


def _font_face() -> str:
    path = os.path.join(HERE, "assets", "NotoSansPhoenician-Regular.ttf")
    try:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        return ("@font-face { font-family: 'PaleoHebrew'; "
                f"src: url(data:font/ttf;base64,{b64}) format('truetype'); }}")
    except OSError:
        return ""


FRIEZE = orn.data_uri(orn.frieze_tile_svg())
ROSETTE = orn.data_uri(orn.rosette_svg(40))

SERIF = "'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, 'Times New Roman', serif"
HEB = "'Frank Ruehl CLM', 'Frank Ruhl Libre', 'David', 'Taamey Frank CLM', 'Times New Roman', serif"

CSS = f"""
<style>
{_font_face()}
.block-container, [data-testid="stMainBlockContainer"] {{ padding-top: 4.6rem; }}
[data-testid="stAppViewContainer"] {{ background:
   radial-gradient(ellipse at 50% -10%, rgba(232,189,92,.10), rgba(0,0,0,0) 55%), {BG}; }}
h1, h2, h3, h4 {{ font-family: {SERIF}; color: {GOLD}; }}
.sl-head {{ display:flex; align-items:center; gap: 14px; margin: .4rem 0 .2rem 0; }}
.sl-title {{ font-family: {SERIF}; font-size: 2.05rem; font-weight: 700; color: {GOLD}; line-height:1.1; }}
.sl-title .sl-he-i {{ font-size: 1.8rem; }}
.sl-paleo {{ font-family: 'PaleoHebrew', 'Segoe UI Historic', 'Noto Sans Phoenician', sans-serif;
            color: {MUTED}; font-size: 1.15rem; letter-spacing: .12em; direction: rtl; unicode-bidi: isolate; }}
.sl-paleo-note {{ color: {MUTED}; font-size: .78rem; }}
.sl-frieze {{ height: 34px; background-image: url("{FRIEZE}"); background-repeat: repeat-x;
             background-size: auto 34px; margin: .25rem 0 .7rem 0; opacity: .95; }}
.sl-sub {{ color: {MUTED}; margin-bottom: 0.4rem; }}
.sl-he, .sl-he-i {{ font-family: {HEB}; direction: rtl; unicode-bidi: isolate; }}
.sl-he {{ font-size: 1.35rem; color: {GOLD}; }}
.sl-he-i {{ color: {GOLD}; font-size: 1.04em; }}
.sl-card {{ background: {CARD}; border: 1px solid {BRONZE}; outline: 1px solid rgba(232,189,92,.35);
           outline-offset: -5px; border-radius: 4px; padding: .95rem 1.15rem; margin-bottom: .8rem; color: {TEXT}; }}
.sl-card h3 {{ font-family: {SERIF}; color: {GOLD}; margin: 0 0 .4rem 0; font-size: 1.08rem; font-weight: 700;
              padding-left: 26px; background: url("{ROSETTE}") no-repeat left center; background-size: 19px 19px; }}
.sl-big {{ font-family: {SERIF}; font-size: 1.55rem; font-weight: 700; color: {TEXT}; line-height: 1.25; }}
.sl-muted {{ color: {MUTED}; font-size: .92rem; }}
.sl-obs {{ color: {OBS}; }}
.sl-bib {{ color: {OBS}; font-size: .95rem; }}
.sl-grid {{ width: 100%; border-collapse: separate; border-spacing: 4px; table-layout: fixed; }}
.sl-grid th {{ font-family: {SERIF}; color: {GOLD}; font-weight: 700; font-size: .9rem; padding: 2px 4px; text-align: left;
              border-bottom: 2px solid {BRONZE}; }}
.sl-grid th .sl-he-i {{ font-size: .95rem; }}
.sl-grid td {{ background: {CARD}; border-radius: 3px; vertical-align: top; padding: 5px 6px;
              height: 108px; color: {TEXT}; border: 1px solid rgba(184,131,74,.45); }}
.sl-grid td.sl-empty {{ background: transparent; border: none; }}
.sl-grid td.sl-sat {{ background: {SHABBAT_BG}; border-color: rgba(63,106,168,.8); }}
.sl-grid td.sl-today {{ border: 2px solid {GOLD}; }}
.sl-civ {{ font-weight: 700; font-size: 1.05rem; color: {TEXT}; }}
.sl-civm {{ font-size: .78rem; color: {MUTED}; margin-left: 3px; }}
.sl-hd {{ float: right; text-align: right; font-family: {HEB}; font-size: 1.05rem; color: {GOLD}; }}
.sl-hd small {{ color: {MUTED}; font-size: .75rem; font-family: sans-serif; }}
.sl-other {{ font-size: .74rem; color: {OBS}; display: block; margin-top: 1px; }}
.sl-chip {{ display: inline-block; color: {INK}; border-radius: 3px; padding: 1px 6px; margin: 2px 2px 0 0;
           font-size: .76rem; font-weight: 600; line-height: 1.35; border: 1px solid rgba(26,18,12,.35); }}
.sl-chip .sl-he-i {{ color: {INK}; font-weight: 600; }}
.sl-line {{ font-size: .76rem; color: {MUTED}; display: block; margin-top: 2px; }}
.sl-line b {{ color: {TEXT}; }}
.sl-line .sl-he-i {{ font-size: .85rem; }}
.sl-list {{ width: 100%; border-collapse: collapse; }}
.sl-list td {{ border-bottom: 1px solid rgba(184,131,74,.4); padding: 7px 4px; vertical-align: top; color: {TEXT}; }}
.sl-list td.sl-sat {{ background: {SHABBAT_BG}; }}
.sl-list td.sl-today {{ outline: 2px solid {GOLD}; }}
.sl-legend span {{ margin-right: 6px; }}
.sl-table {{ width: 100%; border-collapse: collapse; font-size: .93rem; }}
.sl-table th {{ font-family: {SERIF}; color: {GOLD}; text-align: left; border-bottom: 2px solid {BRONZE}; padding: 5px 6px; }}
.sl-table td {{ color: {TEXT}; border-bottom: 1px solid rgba(184,131,74,.35); padding: 5px 6px; vertical-align: top; }}
.sl-table td.sl-diff {{ color: {GOLD}; font-weight: 700; }}
.sl-cycle {{ display: inline-block; width: 2.1rem; height: 2.1rem; line-height: 2.1rem; text-align: center;
            border-radius: 50%; margin: 2px; font-weight: 700; font-size: .9rem; }}
.sl-cycle.leap {{ background: {GOLD}; color: {INK}; }}
.sl-cycle.common {{ background: {CARD}; color: {TEXT}; border: 1px solid {BRONZE}; }}
.sl-cycle.now {{ outline: 3px solid {LINK}; outline-offset: 2px; }}
a {{ color: {LINK}; }}
@media (pointer: coarse) {{
  .sl-grid td {{ height: auto; min-height: 80px; }}
  div[data-testid="stRadio"] label {{ padding: 6px 4px; }}
  button {{ min-height: 44px; }}
}}
@media (max-width: 640px) {{
  .sl-title {{ font-size: 1.5rem; }} .sl-title .sl-he-i {{ font-size: 1.3rem; }}
  .sl-big {{ font-size: 1.28rem; }}
}}
</style>
"""


def apply():
    st.html(CSS)


def header(subtitle: str = ""):
    cap = orn.capital_svg(78, 55)
    paleo = hn.paleo("לוח השמים")
    st.html(f"<div class='sl-head'>{cap}<div><div class='sl-title'>Sky Luach "
            f"<span class='sl-he-i' lang='he' dir='rtl'>לוח השמים</span></div>"
            f"<div><span class='sl-paleo' title='לוח השמים in the Paleo-Hebrew script of the First Temple period "
            f"(as on the Siloam inscription)'>{paleo}</span> "
            f"<span class='sl-paleo-note'>· the Jewish calendar, fixed and observed, from NASA JPL astronomy</span></div>"
            f"</div></div><div class='sl-frieze' role='presentation'></div>")


def chip(kind: str, text: str, he: str = "") -> str:
    inner = html.escape(text)
    if he:
        inner += f" <span class='sl-he-i' lang='he' dir='rtl'>{html.escape(he)}</span>"
    return f"<span class='sl-chip' style='background:{CHIP.get(kind, '#e0d6c4')}'>{inner}</span>"


def legend() -> str:
    return "<div class='sl-legend'>" + "".join(chip(k, v, hn.KIND_HE.get(k, "")) for k, v in KIND_LABEL.items()) + "</div>"
