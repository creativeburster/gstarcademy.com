# scratch/cleanup_dangling.py
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "sw"
CONCEPTS_DIR = ROOT / "kb" / "concepts"

# 1. Collect all active term slugs
active_slugs = set()
for p in DATA_DIR.glob("*.json"):
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    for t in data.get("terms", []):
        active_slugs.add(t["slug"])

print(f"Total active slugs in database: {len(active_slugs)}")

# 2. Collect all HTML files in concepts directory
deleted_count = 0
for html_path in CONCEPTS_DIR.glob("*.html"):
    slug = html_path.stem
    if slug not in active_slugs:
        # Check if it was a custom named page that doesn't follow terms (e.g. non-term pages, wait, all concepts are terms)
        # In this project, all files in kb/concepts/ represent terms. Let's verify.
        # Yes, kb/concepts/ has one file per term slug.
        # Let's delete the dangling file!
        print(f"🗑️ Deleting dangling concept page: {html_path.name}")
        html_path.unlink()
        deleted_count += 1

print(f"🎉 Cleaned up {deleted_count} dangling HTML pages!")
