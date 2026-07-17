#!/usr/bin/env python3
"""Check for missing canonical, OG, and robots meta tags in concept pages."""
from pathlib import Path
import re

KB_CONCEPTS = Path(r"f:\gstarcademy\kb\concepts")

missing_canonical = []
missing_og = []
missing_robots = []
missing_desc = []

for f in KB_CONCEPTS.glob("*.html"):
    html = f.read_text(encoding="utf-8")
    if 'rel="canonical"' not in html:
        missing_canonical.append(f.name)
    if 'og:title' not in html:
        missing_og.append(f.name)
    if 'name="robots"' not in html:
        missing_robots.append(f.name)
    if 'name="description"' not in html:
        missing_desc.append(f.name)

print(f"Missing canonical: {len(missing_canonical)}")
if missing_canonical[:5]:
    print(f"  Examples: {missing_canonical[:5]}")
print(f"Missing OG title: {len(missing_og)}")
if missing_og[:5]:
    print(f"  Examples: {missing_og[:5]}")
print(f"Missing robots: {len(missing_robots)}")
if missing_robots[:5]:
    print(f"  Examples: {missing_robots[:5]}")
print(f"Missing description: {len(missing_desc)}")
if missing_desc[:5]:
    print(f"  Examples: {missing_desc[:5]}")
