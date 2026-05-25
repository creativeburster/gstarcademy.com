#!/usr/bin/env python3
"""
Idempotently patch every site HTML page so it has the unified mobile-friendly
top navigation:

  - hamburger trigger button
  - nav-header (with nav-close ×) inside <nav class="nav">
  - nav-overlay before </header>
  - "Knowledge Base" -> "Wiki" rename for the data-nav="knowledge" link
    (and other ad-hoc rewrites the trae agent already shipped for index.html)

This works as a post-processor: regenerators (e.g. build_software_content.py)
may emit nav HTML without these elements; running this script restores them.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HAMBURGER_BLOCK = """          <button class="hamburger" aria-label="Toggle navigation menu" aria-expanded="false">
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
          </button>
"""

HAMBURGER_RE_FULL = re.compile(
    r'\s*<button class="hamburger"[^>]*>\s*'
    r'(?:<span class="hamburger-line"></span>\s*){3}'
    r'</button>\s*',
    re.DOTALL,
)

NAV_HEADER_BLOCK = """            <div class="nav-header">
              <button class="nav-close" aria-label="Close navigation menu">
                <span class="nav-close-icon">×</span>
              </button>
            </div>
"""

OVERLAY_BLOCK = '          <div class="nav-overlay" aria-hidden="true"></div>\n'


# Match a <nav class="nav">...</nav> block (non-greedy) inside a topbar.
NAV_BLOCK_RE = re.compile(
    r'(<nav\s+class="nav"\s*>)(.*?)(</nav>)',
    flags=re.DOTALL,
)

# Match the closing </header> (only the first occurrence in the file).
HEADER_CLOSE_RE = re.compile(r'(\s*)</header>')

# Match the brand <a class="brand">...</a> block (first occurrence).
BRAND_CLOSE_RE = re.compile(
    r'(<a\s+class="brand"[^>]*>.*?</a>)',
    flags=re.DOTALL,
)


def patch_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    # 1) "Knowledge Base" -> "Wiki" in the nav link only (not in titles / body).
    # We target the exact link text inside a <a ... data-nav="knowledge" ...>...</a>.
    text = re.sub(
        r'(<a[^>]*data-nav="knowledge"[^>]*>)\s*Knowledge Base\s*(</a>)',
        r'\1Wiki\2',
        text,
    )

    # 2) Ensure exactly one hamburger button sits between the brand and the nav.
    #    a) Find the topbar block (header.topbar … </header>).
    m_topbar = re.search(r'<header class="topbar"[^>]*>(.*?)</header>', text, re.DOTALL)
    if m_topbar:
        topbar_block = m_topbar.group(0)
        nav_open_idx = topbar_block.find('<nav class="nav"')
        nav_close_idx = topbar_block.find('</nav>')
        if nav_open_idx != -1 and nav_close_idx != -1:
            # b) Strip any hamburger buttons that were misplaced INSIDE the nav block.
            inside_nav = topbar_block[nav_open_idx:nav_close_idx]
            cleaned_inside = HAMBURGER_RE_FULL.sub('', inside_nav)
            # c) Determine if a hamburger exists outside the nav already.
            before_nav = topbar_block[:nav_open_idx]
            has_outside_hamburger = '<button class="hamburger"' in before_nav
            # d) Build the new topbar block with hamburger before nav.
            insert_block = '' if has_outside_hamburger else HAMBURGER_BLOCK
            new_topbar = (
                before_nav
                + insert_block
                + cleaned_inside
                + topbar_block[nav_close_idx:]
            )
            if new_topbar != topbar_block:
                text = text.replace(topbar_block, new_topbar, 1)

    # 3) Inject nav-header (with × close button) at top of <nav class="nav"> ... </nav>.
    if 'class="nav-header"' not in text:
        def _inject_nav_header(match: re.Match[str]) -> str:
            opening = match.group(1)
            inner = match.group(2)
            closing = match.group(3)
            return f"{opening}\n{NAV_HEADER_BLOCK.rstrip()}\n{inner.lstrip()}{closing}"
        text = NAV_BLOCK_RE.sub(_inject_nav_header, text, count=1)

    # 4) Add nav-overlay before the first </header> if missing.
    if 'class="nav-overlay"' not in text:
        def _inject_overlay(match: re.Match[str]) -> str:
            indent = match.group(1)
            return f"\n{OVERLAY_BLOCK}{indent}</header>"
        text = HEADER_CLOSE_RE.sub(_inject_overlay, text, count=1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def iter_html_files(root: Path):
    skip_dirs = {".git", "node_modules", "scratch", "scripts", "PDF", "__pycache__"}
    for dirpath, dirnames, filenames in os.walk(root):
        # Mutate in place to prune walk.
        dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith(".")]
        for name in filenames:
            if name.endswith(".html"):
                yield Path(dirpath) / name


def main() -> int:
    changed = 0
    skipped = 0
    for p in iter_html_files(ROOT):
        text = p.read_text(encoding="utf-8", errors="replace")
        if "<header class=\"topbar\"" not in text and "<header class='topbar'" not in text:
            # Page doesn't render the main topbar (rare static fragments). Skip.
            skipped += 1
            continue
        if patch_html(p):
            changed += 1
            print(f"patched {p.relative_to(ROOT)}")
    print(f"\n{changed} files patched, {skipped} non-topbar files skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
