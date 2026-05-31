# scratch/check_placeholders.py
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "sw"

for p in DATA_DIR.glob("*.json"):
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    placeholders = [t["title"] for t in data.get("terms", []) if "concept" in t["title"].lower()]
    if placeholders:
        print(f"{p.name}: {len(placeholders)} placeholders, e.g., {placeholders[:3]}")
