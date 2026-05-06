"""One-off KB nav cleanup: strip top Learning Paths nav, CAx/Domains from KBchrome, Vendor hubs→Vendors."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Strip global topbar Learning Paths (all depth variants used in repo)
PATHS_NAV_LINE = re.compile(
    r"^[ \t]*<a class=\"nav-link\" data-nav=\"paths\" href=\"[^\"]+\">Learning Paths</a>\r?\n",
    re.MULTILINE,
)

HX = r"(?:\.\./)*(?:\./)?"  # matches ../../ or ./ before filename

# KB sidebar: remove CAx index line
RE_KB_IDX_CAX = re.compile(
    rf"^[ \t]*<a class=\"kb-index-link\" href=\"{HX}knowledge-cax\.html\">CAD / CAE / CAM</a>\r?\n",
    re.MULTILINE,
)
RE_KB_IDX_DOM = re.compile(
    rf"^[ \t]*<a class=\"kb-index-link\" href=\"{HX}knowledge-domains\.html\">Domain tracks</a>\r?\n",
    re.MULTILINE,
)

# Maps: remove CAD · CAE · CAM row
RE_MAPS_CAX = re.compile(
    rf"^[ \t]*<a class=\"kb-side-link\" href=\"{HX}knowledge-cax\.html\">CAD · CAE · CAM</a>\r?\n",
    re.MULTILINE,
)

# Topics: Domains row
RE_TOP_DOM = re.compile(
    rf"^[ \t]*<a class=\"kb-side-link\" href=\"{HX}knowledge-domains\.html\">Domains &amp; industries</a>\r?\n",
    re.MULTILINE,
)

# Subnav strip CAx And Domains link lines ONLY (anchor text constrained)
RE_SUB_CA = re.compile(
    rf"^[ \t]*<a class=\"kb-subnav-link[^\"]*\" href=\"{HX}knowledge-cax\.html\">CAx</a>\r?\n",
    re.MULTILINE,
)
RE_SUB_DOM = re.compile(
    rf"^[ \t]*<a class=\"kb-subnav-link[^\"]*\" href=\"{HX}knowledge-domains\.html\">Domains</a>\r?\n",
    re.MULTILINE,
)


def process(text: str) -> str:
    t = PATHS_NAV_LINE.sub("", text)
    t = RE_KB_IDX_CAX.sub("", t)
    t = RE_KB_IDX_DOM.sub("", t)
    t = RE_MAPS_CAX.sub("", t)
    t = RE_TOP_DOM.sub("", t)
    t = RE_SUB_CA.sub("", t)
    t = RE_SUB_DOM.sub("", t)
    # Label rename in subnav/kb-context (narrow: Vendor hubs as link text next to kb-subnav or vendor-docs)
    t = t.replace('href="./kb-vendors.html">Vendor hubs</', 'href="./kb-vendors.html">Vendors</')
    t = t.replace('href="../../kb-vendors.html">Vendor hubs</', 'href="../../kb-vendors.html">Vendors</')
    return t


def main() -> int:
    for path in sorted(ROOT.rglob("*.html")):
        raw = path.read_text(encoding="utf-8")
        new = process(raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            print("updated", path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
