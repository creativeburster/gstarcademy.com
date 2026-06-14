"""
Align KB rail + subnav to six lanes:
  Overview · Vendors · Software · Terms · FAQ · Graph

Run: python scripts/patch_kb_six_lane_nav.py
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

LANE_TARGETS: list[tuple[str, str, str]] = [
    ("overview", "knowledge-base.html", "Overview"),
    ("vendors", "kb-vendors.html", "Vendors"),
    ("software", "kb-software.html", "Software"),
    ("terms", "kb-terms.html", "Terms"),
    ("faq", "kb-faq.html", "FAQ"),
    ("graph", "kb-graph.html", "Graph"),
]

SUBNAV_RE = re.compile(
    r'<nav class="kb-subnav" aria-label="Knowledge base sections">\s*[\s\S]*?\s*</nav>',
    re.MULTILINE,
)

# Which lane gets .active (by path within repo)
ACTIVE: dict[str, str] = {}
for n in [
    "knowledge-base.html",
    "kb-vendors.html",
    "kb-software.html",
    "kb-terms.html",
    "kb-faq.html",
    "kb-graph.html",
]:
    k = n.split(".")[0].replace("knowledge-", "").replace("-", "_")
    if n == "knowledge-base.html":
        ACTIVE[n] = "overview"
    elif n == "kb-vendors.html":
        ACTIVE[n] = "vendors"
    elif n == "kb-software.html":
        ACTIVE[n] = "software"
    elif n == "kb-terms.html":
        ACTIVE[n] = "terms"
    elif n == "kb-faq.html":
        ACTIVE[n] = "faq"
    elif n == "kb-graph.html":
        ACTIVE[n] = "graph"

ACTIVE["knowledge-glossary.html"] = "terms"
ACTIVE["knowledge-library.html"] = "terms"
ACTIVE["knowledge-curriculum.html"] = "terms"
ACTIVE["knowledge-roadmap.html"] = "overview"
ACTIVE["knowledge-cax.html"] = "overview"
ACTIVE["knowledge-domains.html"] = "overview"


def build_subnav(prefix: str, lane: str) -> str:
    lines = ['        <nav class="kb-subnav" aria-label="Knowledge base sections">']
    for key, file, label in LANE_TARGETS:
        cls = "kb-subnav-link active" if lane == key else "kb-subnav-link"
        href = prefix + file
        lines.append(f'          <a class="{cls}" href="{href}">{label}</a>')
    lines.append("        </nav>")
    return "\n".join(lines)


def build_sidebar(prefix: str) -> str:
    prof = f"{prefix}kb/software/index.html"
    return (
        f'            <div class="kb-index-box">\n'
        f'              <strong class="kb-index-title">Six lanes</strong>\n'
        f'              <p class="meta kb-sidebar-taxonomy-note">\n'
        f"                Mirrors the top strip—taxonomy view of the same routes (expect overlap).\n"
        f"              </p>\n"
        f'              <a class="kb-index-link" href="{prefix}knowledge-base.html">Overview</a>\n'
        f'              <a class="kb-index-link" href="{prefix}kb-vendors.html">Vendors</a>\n'
        f'              <a class="kb-index-link" href="{prefix}kb-software.html">Software</a>\n'
        f'              <a class="kb-index-link" href="{prefix}kb-terms.html">Terms</a>\n'
        f'              <a class="kb-index-link" href="{prefix}kb-faq.html">FAQ</a>\n'
        f'              <a class="kb-index-link" href="{prefix}kb-graph.html">Graph</a>\n'
        f'              <a class="kb-index-link" href="{prof}">Software profiles</a>\n'
        f'            </div>\n\n'
        f'            <div class="kb-nav-group">\n'
        f'              <button class="kb-nav-toggle" aria-expanded="true">Drill down</button>\n'
        f'              <div class="kb-nav-links">\n'
        f'                <a class="kb-side-link" href="{prefix}tutorials.html">Tutorial library</a>\n'
        f'                <a class="kb-side-link" href="{prefix}kb-terms.html">Term glossary (cards)</a>\n'
        f"              </div>\n"
        f'            </div>\n'
        f'            <div class="kb-nav-group">\n'
        f'              <button class="kb-nav-toggle" aria-expanded="true">Topics</button>\n'
        f'              <div class="kb-nav-links">\n'
        f'                <a class="kb-side-link" href="{prefix}knowledge-base.html">Hub overview</a>\n'
        f'                <a class="kb-side-link" href="{prefix}news.html">CAD news</a>\n'
        f"              </div>\n"
        f'            </div>\n'
        f'            <div class="kb-nav-group">\n'
        f'              <button class="kb-nav-toggle" aria-expanded="false">Meta</button>\n'
        f'              <div class="kb-nav-links kb-collapsed">\n'
        f'                <a class="kb-side-link" href="{prefix}knowledge-base.html#kb-about">About this hub</a>\n'
        f"              </div>\n"
        f"            </div>\n"
    )


def splice_sidebar(html: str, prefix: str) -> str:
    start = html.find('<div class="kb-index-box')
    stage = html.find('<div class="kb-stage">')
    if start < 0 or stage < 0:
        raise ValueError("sidebar anchors missing")
    aside_close = html.rfind("</aside>", 0, stage)
    if aside_close < 0 or aside_close < start:
        raise ValueError("aside close missing before kb-stage")
    return html[:start] + build_sidebar(prefix) + html[aside_close:]


def process(path: Path) -> bool:
    rel_posix = path.relative_to(REPO).as_posix()
    if path.name == "index.html" and "kb/software" in rel_posix:
        key = "kb/software/index.html"
    elif path.parent.name == "software" and path.parent.parent.name == "kb":
        key = f"kb/software/{path.name}"
    else:
        key = path.name

    if "kb/software" in rel_posix:
        prefix = "../../"
        lane = "software"
    else:
        prefix = "./"
        lane = ACTIVE.get(key, ACTIVE.get(path.name, "overview"))

    text = path.read_text(encoding="utf-8")
    if "kb-subnav" not in text:
        return False

    t2 = SUBNAV_RE.sub(build_subnav(prefix, lane), text)
    t3 = splice_sidebar(t2, prefix)
    if t3 != text:
        path.write_text(t3, encoding="utf-8")
        return True
    return False


def main() -> int:
    files: list[Path] = []
    for p in sorted(REPO.glob("knowledge*.html")):
        files.append(p)
    for p in sorted(REPO.glob("kb-*.html")):
        files.append(p)
    ks = REPO / "kb" / "software"
    if ks.is_dir():
        files.extend(sorted(ks.glob("*.html")))

    n = 0
    for fp in files:
        try:
            if process(fp):
                n += 1
                print("+", fp.relative_to(REPO))
        except Exception as e:  # noqa: BLE001
            print("!", fp.relative_to(REPO), e)

    print("done,", n, "files updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
