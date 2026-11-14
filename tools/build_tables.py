"""Rebuild data/crescents_jerusalem.csv.gz and data/seasons.csv from the JPL ephemeris.

Run from the app folder:  .venv\\Scripts\\python.exe tools\\build_tables.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import observed_calendar as oc  # noqa: E402

if __name__ == "__main__":
    oc.build_tables()
    print("written:", oc.CRESCENT_FILE, oc.SEASONS_FILE)
