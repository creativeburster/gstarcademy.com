import re, collections
from pathlib import Path

phrasings = [
    "is a fundamental design mechanism",
    "serves as a key modeling principle",
    "functions as an essential workflow component",
    "acts as a core structural element",
    "operates as a primary design driver",
    "constitutes a critical modeling concept",
    "forms an integral part of the design workflow",
    "provides a foundational technical capability",
    "represents a key engineering principle",
    "serves as a central modeling mechanism",
    "is an essential design tool",
    "functions as a core engineering concept",
    "acts as a fundamental modeling element",
    "provides a key technical foundation",
    "operates as a central design principle",
]

counts = collections.Counter()
for f in Path(r"f:\gstarcademy\kb\concepts").glob("*.html"):
    html = f.read_text(encoding="utf-8")
    for p in phrasings:
        if p in html:
            counts[p] += 1

for p, c in counts.most_common():
    print(f"  {c:3d}  {p}")
print(f"\nTotal: {sum(counts.values())} occurrences across {len(phrasings)} phrasings")
