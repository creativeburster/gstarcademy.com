#!/usr/bin/env python3
"""Check for broken internal links in concept pages, correctly handling extensionless URLs."""
import re, os
from pathlib import Path
from collections import Counter

KB_CONCEPTS = Path(r"f:\gstarcademy\kb\concepts")

NAV_PREFIXES = {'../../knowledge-base', '../../tutorials', '../../news', '../../about',
                '../../kb-terms', '../../editorial-process'}

broken_concept_links = Counter()
broken_software_links = Counter()

for f in KB_CONCEPTS.glob("*.html"):
    html = f.read_text(encoding="utf-8")
    links = re.findall(r'href="(\.\./[^"]+|\./[^"]+)"', html)
    for link in links:
        if link.startswith('#') or link.startswith('http'):
            continue
        if any(link.startswith(nav) for nav in NAV_PREFIXES):
            continue
        base_link = link.split('#')[0]
        if not base_link:
            continue
        # Try both: exact path, and path + .html
        target = (f.parent / base_link).resolve()
        target_html = Path(str(target) + '.html')
        if not os.path.exists(str(target)) and not target_html.exists():
            if base_link.startswith('./'):
                broken_concept_links[base_link] += 1
            elif base_link.startswith('../software/'):
                broken_software_links[base_link] += 1

print(f"Broken concept-to-concept links: {len(broken_concept_links)} unique targets")
for target, count in broken_concept_links.most_common(30):
    print(f"  {count:4d}x  {target}")

print(f"\nBroken concept-to-software links: {len(broken_software_links)} unique targets")
for target, count in broken_software_links.most_common(20):
    print(f"  {count:4d}x  {target}")
