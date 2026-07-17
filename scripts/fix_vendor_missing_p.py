#!/usr/bin/env python3
"""Fix missing closing </p> tag in vendor pages after template replacement."""
import re
from pathlib import Path

VENDORS_DIR = Path(r"f:\gstarcademy\kb\vendors")
FIXED_FILES = ["alibre", "allplan", "altium-ltd", "community", "comsol-inc",
               "freecad-community", "graebert", "ironcad", "mcneel",
               "openfoam-foundation", "vectorworks"]

for stem in FIXED_FILES:
    filepath = VENDORS_DIR / f"{stem}.html"
    html = filepath.read_text(encoding="utf-8")
    # Fix: lines where <p> is followed by content but no </p> before <h2>Learning Resources
    # Pattern: "...collaboration.\n        <h2>Learning Resources" should be "...collaboration.</p>\n        <h2>Learning Resources"
    fixed = re.sub(r'(\.\s*)\n(\s*<h2>Learning Resources)', r'\1</p>\n\2', html)
    if fixed != html:
        filepath.write_text(fixed, encoding="utf-8")
        print(f"  Fixed </p>: {stem}.html")
    else:
        print(f"  OK: {stem}.html")
