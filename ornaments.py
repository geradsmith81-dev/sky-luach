"""Decorative SVG ornaments after Iron Age II (First Temple period) art of Israel and Judah.

* proto-Aeolic ("volute") capital - the stone capitals of royal buildings at Samaria, Megiddo,
  Hazor, Ramat Rahel and Jerusalem (City of David): two volutes curling out from a central triangle
  under a flat abacus.
* palmette - the 'tree of life' palmette of the Samaria and Nimrud ivories.
* pomegranate - the rows of pomegranates on the capitals of the bronze pillars Jachin and Boaz
  (1 Kings 7:18-20) and on the high priest's robe (Exodus 28:33-34); cf. the small ivory pomegranate.
* rosette - the rosette seal impressions on Judahite storage-jar handles (late 7th c. BCE) and the
  'open flowers' carved in the Temple (1 Kings 6:18, 29).
All are drawn here from simple geometry (no copied images).
"""
from __future__ import annotations

import base64
import math

GOLD = "#e2b552"
BRONZE = "#b8834a"
IVORY = "#f3e9d2"
TEKHELET = "#3f6aa8"
ARGAMAN = "#7a3a6e"
SCARLET = "#b23a32"
CEDAR = "#1a120c"


def _spiral(cx, cy, r0, r1, turns, a0, clockwise=True):
    pts = []
    n = int(60 * turns)
    for i in range(n + 1):
        t = i / n
        r = r0 + (r1 - r0) * t
        a = a0 + (2 * math.pi * turns * t) * (1 if clockwise else -1)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def capital_svg(w=120, h=84, color=GOLD, fill=None) -> str:
    """Proto-Aeolic capital: abacus, two volutes, central triangle, stem bands."""
    sw = 4.2
    left = _spiral(31, 40, 24, 3.5, 1.6, -math.pi / 2, clockwise=False)
    right = _spiral(89, 40, 24, 3.5, 1.6, -math.pi / 2, clockwise=True)
    tri = "60,18 43,70 77,70"
    body = (
        f"<rect x='6' y='6' width='108' height='9' rx='1.5' fill='{color}'/>"
        f"<polyline points='{left}' fill='none' stroke='{color}' stroke-width='{sw}' stroke-linecap='round'/>"
        f"<polyline points='{right}' fill='none' stroke='{color}' stroke-width='{sw}' stroke-linecap='round'/>"
        f"<circle cx='31' cy='40' r='3.4' fill='{color}'/><circle cx='89' cy='40' r='3.4' fill='{color}'/>"
        f"<polygon points='{tri}' fill='{fill or color}' stroke='{color}' stroke-width='2'/>"
        f"<rect x='38' y='72' width='44' height='4' fill='{color}'/>"
        f"<rect x='42' y='78' width='36' height='4' fill='{color}'/>"
    )
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 84' width='{w}' height='{h}'>{body}</svg>"


def palmette(cx, base_y, size=1.0, color=GOLD, accent=TEKHELET) -> str:
    """Fan of leaves rising from a pair of small volutes (Samaria-ivory palmette)."""
    out = []
    for k in range(-3, 4):
        a = math.radians(-90 + k * 19)
        L = (17 - abs(k) * 1.4) * size
        x2, y2 = cx + L * math.cos(a), base_y - 4 * size + L * math.sin(a)
        mx, my = cx + 0.55 * L * math.cos(a), base_y - 4 * size + 0.55 * L * math.sin(a)
        rot = math.degrees(a)
        out.append(f"<ellipse cx='{mx:.1f}' cy='{my:.1f}' rx='{0.5 * L:.1f}' ry='{2.3 * size:.1f}' "
                   f"transform='rotate({rot:.1f} {mx:.1f} {my:.1f})' fill='{color}'/>")
    s = size
    out.append(f"<path d='M{cx - 9 * s:.1f},{base_y:.1f} q{4 * s:.1f},{-8 * s:.1f} {9 * s:.1f},{-4 * s:.1f} "
               f"q{5 * s:.1f},{-4 * s:.1f} {9 * s:.1f},{4 * s:.1f}' fill='none' stroke='{accent}' stroke-width='{2.2 * s:.1f}'/>")
    out.append(f"<circle cx='{cx - 9 * s:.1f}' cy='{base_y:.1f}' r='{1.8 * s:.1f}' fill='{accent}'/>")
    out.append(f"<circle cx='{cx + 9 * s:.1f}' cy='{base_y:.1f}' r='{1.8 * s:.1f}' fill='{accent}'/>")
    return "".join(out)


def pomegranate(cx, cy, r=6.0, color=SCARLET, crown=GOLD) -> str:
    return (f"<line x1='{cx}' y1='{cy + r}' x2='{cx}' y2='{cy + r + 5}' stroke='{crown}' stroke-width='1.6'/>"
            f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{color}'/>"
            f"<polygon points='{cx - 3.4},{cy - r + 1} {cx - 3.8},{cy - r - 4.5} {cx - 1.4},{cy - r - 1.6} "
            f"{cx},{cy - r - 5.2} {cx + 1.4},{cy - r - 1.6} {cx + 3.8},{cy - r - 4.5} {cx + 3.4},{cy - r + 1}' fill='{crown}'/>")


def frieze_tile_svg(h=34) -> str:
    """One repeat of the frieze: palmette, pomegranate, on a lily-work (chain) band."""
    w = 64
    body = (
        palmette(16, 27, 0.95) + pomegranate(48, 17, 5.6) +
        f"<line x1='0' y1='31' x2='{w}' y2='31' stroke='{BRONZE}' stroke-width='1.6'/>"
        f"<path d='M0,31 q8,-5 16,0 q8,5 16,0 q8,-5 16,0 q8,5 16,0' fill='none' stroke='{GOLD}' stroke-width='1.1' opacity='0.8'/>"
    )
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 34' width='{w}' height='{h}'>{body}</svg>"


def rosette_svg(size=28, petals=12, color=GOLD, center=SCARLET) -> str:
    c = 50
    out = []
    for k in range(petals):
        a = 360 * k / petals
        out.append(f"<ellipse cx='{c}' cy='{c - 25}' rx='7.5' ry='20' transform='rotate({a:.1f} {c} {c})' fill='{color}'/>")
    out.append(f"<circle cx='{c}' cy='{c}' r='10' fill='{center}' stroke='{color}' stroke-width='3'/>")
    out.append(f"<circle cx='{c}' cy='{c}' r='47' fill='none' stroke='{color}' stroke-width='3'/>")
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' width='{size}' height='{size}'>{''.join(out)}</svg>"


def data_uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")
