#!/usr/bin/env python3
"""
Fix nested <a> tags in concept pages.
Pattern: <a href="./X"><a href="./Y" style="...">text</a></a>
Fix to:  <a href="./Y" style="...">text</a>
(Keep the inner link, remove the outer wrapper)
"""
import re
from pathlib import Path

KB_CONCEPTS = Path(r"f:\gstarcademy\kb\concepts")

# Pattern: <a href="./slug1"><a href="./slug2" style="...">text</a></a>
# We want to keep only the inner <a> tag
pattern = re.compile(
    r'<a href="(\./[^"]+)">'        # outer <a> tag
    r'<a href="(\./[^"]+)"([^>]*)>'  # inner <a> tag with optional attributes
    r'(.*?)'                          # text content
    r'</a>'                           # closing inner
    r'</a>'                           # closing outer
)

fixed_count = 0
for f in KB_CONCEPTS.glob("*.html"):
    html = f.read_text(encoding="utf-8")
    new_html = pattern.sub(
        lambda m: f'<a href="{m.group(2)}"{m.group(3)}>{m.group(4)}</a>',
        html
    )
    if new_html != html:
        f.write_text(new_html, encoding="utf-8")
        fixed_count += 1
        print(f"  Fixed: {f.name}")

print(f"\nTotal: {fixed_count} files fixed")
