"""Apply v8 Deep Ink Engineering refresh to all HTML files.

- Bump CSS/JS cache query string v7_graph_fix -> v8_deep_ink
- Inject Google Fonts preconnect + Newsreader + Inter into <head>
- Idempotent: safe to re-run.

Run from repo root:
  python scripts/apply_v8_deep_ink.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OLD_VER = "v7_graph_fix"
NEW_VER = "v8_deep_ink"

# Pre-built Google Fonts block (preconnect + display=swap + only needed weights)
FONTS_BLOCK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
    '    <link rel="stylesheet"\n'
    '      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />'
)

FONT_MARKER = "fonts.googleapis.com/css2?family=Inter"


def patch(html: str) -> str:
    """Bump cache version + inject font block (if not already present)."""
    # Bump any old cache string variants seen in the repo
    out = html
    for old in (OLD_VER, "v6_faq_graph_perfection", "20260427kb12"):
        out = out.replace(f"?v={old}", f"?v={NEW_VER}")
    # Inject fonts block once
    if FONT_MARKER not in out:
        # Insert just before the styles.css <link rel="stylesheet"
        m = re.search(
            r'(\s*<link rel="stylesheet" href="[^"]*styles\.css[^"]*" />)',
            out,
        )
        if m:
            insert_at = m.start(1)
            block = "\n    " + FONTS_BLOCK
            out = out[:insert_at] + block + out[insert_at:]
    return out


def main() -> int:
    changed: list[Path] = []
    for path in ROOT.rglob("*.html"):
        # skip node_modules etc; this repo has none
        text = path.read_text(encoding="utf-8")
        new = patch(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed.append(path)
    print(f"Patched {len(changed)} html files")
    for p in changed:
        print(" -", p.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
