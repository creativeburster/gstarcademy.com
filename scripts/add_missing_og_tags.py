#!/usr/bin/env python3
"""Add Open Graph + Twitter card tags to pages that lack them.

Idempotent: only touches files that have no `og:` tags. Derives values from the
page's existing <title>, meta description, and canonical URL, then inserts the
block right after the canonical <link> (matching the pattern used by pages that
already have OG tags).
"""

from __future__ import annotations

import html
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta\s+name="description"\s+content="(.*?)"\s*/?>', re.S)
CANON_RE = re.compile(r'(<link\s+rel="canonical"\s+href="(.*?)"\s*/?>)')


def _clean_title(raw: str) -> str:
    t = html.unescape(raw).strip()
    # Drop the " | Gstarcademy" site suffix for the social title.
    return re.sub(r"\s*\|\s*Gstarcademy\s*$", "", t).strip()


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "property=\"og:" in text:
        return False

    tm, dm, cm = TITLE_RE.search(text), DESC_RE.search(text), CANON_RE.search(text)
    if not (tm and cm):
        return False

    title = _clean_title(tm.group(1))
    desc = html.unescape(dm.group(1)).strip() if dm else title
    url = cm.group(2).strip()

    block = (
        f'{cm.group(1)}\n'
        f'    <meta property="og:type" content="article" />\n'
        f'    <meta property="og:title" content="{html.escape(title, quote=True)}" />\n'
        f'    <meta property="og:description" content="{html.escape(desc, quote=True)}" />\n'
        f'    <meta property="og:url" content="{html.escape(url, quote=True)}" />\n'
        f'    <meta property="og:site_name" content="Gstarcademy" />\n'
        f'    <meta name="twitter:card" content="summary_large_image" />'
    )
    text = text[: cm.start()] + block + text[cm.end():]
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for path in sorted(REPO.rglob("*.html")):
        if path.name == "offline.html":
            continue
        if process(path):
            changed += 1
            print(f"  + {path.relative_to(REPO)}")
    print(f"Added OG/Twitter tags to {changed} page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
