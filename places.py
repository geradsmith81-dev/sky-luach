"""Place search (GeoNames cities with 15,000+ people, via geonamescache) with time zones."""
from __future__ import annotations

import unicodedata
from functools import lru_cache

from hebrew_names import hebrew_place_name

PRESETS = [
    {"name": "Jerusalem", "he": "ירושלים", "country": "IL", "lat": 31.7683, "lon": 35.2137, "tz": "Asia/Jerusalem"},
    {"name": "Tel Aviv", "he": "תל אביב-יפו", "country": "IL", "lat": 32.0809, "lon": 34.7806, "tz": "Asia/Jerusalem"},
    {"name": "Haifa", "he": "חיפה", "country": "IL", "lat": 32.8184, "lon": 34.9885, "tz": "Asia/Jerusalem"},
    {"name": "New York", "he": "ניו יורק", "country": "US", "lat": 40.7128, "lon": -74.0060, "tz": "America/New_York"},
    {"name": "Los Angeles", "he": "לוס אנג׳לס", "country": "US", "lat": 34.0522, "lon": -118.2437, "tz": "America/Los_Angeles"},
    {"name": "Chicago", "he": "שיקגו", "country": "US", "lat": 41.8781, "lon": -87.6298, "tz": "America/Chicago"},
    {"name": "London", "he": "לונדון", "country": "GB", "lat": 51.5074, "lon": -0.1278, "tz": "Europe/London"},
    {"name": "Paris", "he": "פריז", "country": "FR", "lat": 48.8566, "lon": 2.3522, "tz": "Europe/Paris"},
    {"name": "Toronto", "he": "טורונטו", "country": "CA", "lat": 43.6532, "lon": -79.3832, "tz": "America/Toronto"},
    {"name": "Buenos Aires", "he": "בואנוס איירס", "country": "AR", "lat": -34.6037, "lon": -58.3816, "tz": "America/Argentina/Buenos_Aires"},
    {"name": "Johannesburg", "he": "יוהנסבורג", "country": "ZA", "lat": -26.2041, "lon": 28.0473, "tz": "Africa/Johannesburg"},
    {"name": "Melbourne", "he": "מלבורן", "country": "AU", "lat": -37.8136, "lon": 144.9631, "tz": "Australia/Melbourne"},
]


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


@lru_cache(maxsize=1)
def _cities() -> list[dict]:
    try:
        import geonamescache
    except ImportError:
        return []
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    states = gc.get_us_states()
    out = []
    for c in gc.get_cities().values():
        cc = c["countrycode"]
        region = states.get(c.get("admin1code", ""), {}).get("name", "") if cc == "US" else ""
        out.append({"name": c["name"], "country": cc,
                    "country_name": countries.get(cc, {}).get("name", cc), "region": region,
                    "lat": float(c["latitude"]), "lon": float(c["longitude"]), "tz": c["timezone"],
                    "pop": int(c["population"]), "key": _norm(c["name"]),
                    "he": hebrew_place_name(c.get("alternatenames", [])),
                    "alt": "|" + "|".join(_norm(a) for a in c.get("alternatenames", []) if a) + "|"})
    out.sort(key=lambda r: -r["pop"])
    return out


def search(query: str, limit: int = 12) -> list[dict]:
    """Exact name matches first, then alternate names, then prefixes; larger cities first."""
    q = _norm(query)
    if not q:
        return []
    cities = _cities()
    exact = [c for c in cities if c["key"] == q]
    alt = [c for c in cities if c["key"] != q and f"|{q}|" in c["alt"]]
    pref = [c for c in cities if c["key"] != q and c["key"].startswith(q) and f"|{q}|" not in c["alt"]]
    seen, out = set(), []
    for c in exact + alt + pref:
        k = (c["name"], c["country"], round(c["lat"], 2))
        if k not in seen:
            seen.add(k)
            out.append(c)
        if len(out) >= limit:
            break
    return out


def label(p: dict) -> str:
    parts = [p["name"]]
    if p.get("region"):
        parts.append(p["region"])
    parts.append(p.get("country_name") or p.get("country", ""))
    return ", ".join(x for x in parts if x)
