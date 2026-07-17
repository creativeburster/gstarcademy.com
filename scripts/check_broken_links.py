#!/usr/bin/env python3
"""Check for broken internal links in concept pages."""
import re, os
from pathlib import Path

KB_CONCEPTS = Path(r"f:\gstarcademy\kb\concepts")
KB_DIR = Path(r"f:\gstarcademy\kb")

broken = []
checked = 0

for f in KB_CONCEPTS.glob("*.html"):
    html = f.read_text(encoding="utf-8")
    # Find relative links like href="./some-page" or href="../software/some-page"
    links = re.findall(r'href="(\.\./[^"]+|\./[^"]+)"', html)
    for link in links:
        # Skip fragment-only links and external links
        if link.startswith('#') or link.startswith('http'):
            continue
        # Resolve relative to the file
        target = (f.parent / link).resolve()
        # Strip fragment
        target_str = str(target).split('#')[0]
        if not os.path.exists(target_str):
            broken.append((f.name, link))

checked += 1

print(f"Checked {checked} files")
print(f"Broken links found: {len(broken)}")
if broken:
    # Show unique broken targets
    unique_targets = set(link for _, link in broken)
    print(f"Unique broken targets: {len(unique_targets)}")
    for fname, link in broken[:30]:
        print(f"  {fname} -> {link}")
