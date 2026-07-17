#!/usr/bin/env python3
"""Check for duplicate canonical URLs across concept pages."""
import re
from pathlib import Path
from collections import Counter

KB_CONCEPTS = Path(r"f:\gstarcademy\kb\concepts")

canonicals = Counter()
for f in KB_CONCEPTS.glob("*.html"):
    html = f.read_text(encoding="utf-8")
    m = re.search(r'rel="canonical" href="([^"]+)"', html)
    if m:
        canonicals[m.group(1)] += 1

dupes = {url: count for url, count in canonicals.items() if count > 1}
if dupes:
    print(f"Duplicate canonical URLs found: {len(dupes)}")
    for url, count in sorted(dupes.items(), key=lambda x: -x[1]):
        print(f"  {count}x  {url}")
        # Find which files have this canonical
        for f in KB_CONCEPTS.glob("*.html"):
            html = f.read_text(encoding="utf-8")
            if url in html:
                print(f"    -> {f.name}")
else:
    print("No duplicate canonical URLs found.")
print(f"\nTotal canonical URLs: {len(canonicals)}")
