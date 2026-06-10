"""
Loader for the DSA problem bank stored in Data_Layer/static_questions/dsa/.

Each problem is a JSON file (see two_sum.json for the shape). This module just
reads them off disk; later you can swap this for a DB-backed loader without
touching the UI.
"""

import json
from pathlib import Path

# Frontend/problems.py -> parents[1] is the project root (Mock_Interview_project)
DSA_DIR = Path(__file__).resolve().parents[2] / "Data_Layer" / "static_questions" / "dsa"


def load_dsa_problems() -> list:
    """Return every DSA problem as a list of dicts, sorted by difficulty then title."""
    order = {"Easy": 0, "Medium": 1, "Hard": 2}
    problems = []
    for path in sorted(DSA_DIR.glob("*.json")):
        with open(path, encoding="utf-8") as fh:
            problems.append(json.load(fh))
    problems.sort(key=lambda p: (order.get(p.get("difficulty"), 99), p.get("title", "")))
    return problems


def filter_problems(problems: list, area: str = None, difficulty: str = None) -> list:
    """Narrow the bank by area and/or difficulty. None means 'any'."""
    out = problems
    if area:
        out = [p for p in out if p.get("area") == area]
    if difficulty:
        out = [p for p in out if p.get("difficulty") == difficulty]
    return out
