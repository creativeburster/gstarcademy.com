"""
Align KB rail + subnav to six lanes:
  Overview · Software · Terms · FAQ · Graph · Quiz

Run: python scripts/patch_kb_six_lane_nav.py
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

LANE_TARGETS: list[tuple[str, str, str]] = [
    ("overview", "knowledge-base", "Overview"),
    ("software", "kb-software", "Software"),
    ("terms", "kb-terms", "Terms"),
    ("faq", "kb-faq", "FAQ"),
    ("graph", "kb-graph", "Graph"),
    ("quiz", "quiz", "Quiz"),
]

SUBNAV_RE = re.compile(
    r'<nav[^>]*class="[^"]*kb-subnav[^"]*"[^>]*>\s*[\s\S]*?\s*</nav>',
    re.MULTILINE,
)

ACTIVE: dict[str, str] = {
    "knowledge-base.html": "overview",
    "knowledge-roadmap.html": "overview",
    "knowledge-domains.html": "overview",
    "knowledge-cax.html": "overview",
    "knowledge-curriculum.html": "overview",
    "kb-software.html": "software",
    "kb-terms.html": "terms",
    "knowledge-library.html": "terms",
    "knowledge-glossary.html": "terms",
    "kb-faq.html": "faq",
    "kb-graph.html": "graph",
}


def build_subnav(prefix: str, lane: str) -> str:
    lines = ['        <nav class="kb-subnav" aria-label="Knowledge base sections">']
    for key, slug, label in LANE_TARGETS:
        cls = "kb-subnav-link active" if lane == key else "kb-subnav-link"
        href = f"{prefix}{slug}" if prefix != "/" else f"/{slug}"
        lines.append(f'          <a class="{cls}" href="{href}">{label}</a>')
    lines.append("        </nav>")
    return "\n".join(lines)


def build_sidebar(prefix: str) -> str:
    prof = f"{prefix}kb/software/" if prefix != "/" else "./kb/software/"

    def link_href(slug: str) -> str:
        return f"{prefix}{slug}" if prefix != "/" else f"/{slug}"

    return (
        f'            <div class="kb-index-box">\n'
        f'              <strong class="kb-index-title">Six lanes</strong>\n'
        f'              <p class="meta kb-sidebar-taxonomy-note">\n'
        f"                Mirrors the top strip—taxonomy view of the same routes (expect overlap).\n"
        f"              </p>\n"
        f'              <a class="kb-index-link" href="{link_href("knowledge-base")}">Overview</a>\n'
        f'              <a class="kb-index-link" href="{link_href("kb-software")}">Software</a>\n'
        f'              <a class="kb-index-link" href="{link_href("kb-terms")}">Terms</a>\n'
        f'              <a class="kb-index-link" href="{link_href("kb-faq")}">FAQ</a>\n'
        f'              <a class="kb-index-link" href="{link_href("kb-graph")}">Graph</a>\n'
        f'              <a class="kb-index-link" href="{link_href("quiz")}">Quiz</a>\n'
        f'              <a class="kb-index-link" href="{prof}">Software profiles</a>\n'
        f'            </div>\n\n'
        f'            <div class="kb-nav-group">\n'
        f'              <button class="kb-nav-toggle" aria-expanded="true">Drill down</button>\n'
        f'              <div class="kb-nav-links">\n'
        f'                <a class="kb-side-link" href="{link_href("tutorials")}">Tutorial library</a>\n'
        f'                <a class="kb-side-link" href="{link_href("kb-terms")}">Term glossary (cards)</a>\n'
        f"              </div>\n"
        f'            </div>\n'
        f'            <div class="kb-nav-group">\n'
        f'              <button class="kb-nav-toggle" aria-expanded="true">Topics</button>\n'
        f'              <div class="kb-nav-links">\n'
        f'                <a class="kb-side-link" href="{link_href("knowledge-base")}">Hub overview</a>\n'
        f'                <a class="kb-side-link" href="{link_href("news")}">CAD news</a>\n'
        f"              </div>\n"
        f'            </div>\n'
        f'            <div class="kb-nav-group">\n'
        f'              <button class="kb-nav-toggle" aria-expanded="false">Meta</button>\n'
        f'              <div class="kb-nav-links kb-collapsed">\n'
        f'                <a class="kb-side-link" href="{link_href("knowledge-base")}#kb-about">About this hub</a>\n'
        f"              </div>\n"
        f"            </div>\n"
    )


def splice_sidebar(html: str, prefix: str) -> str:
    start = html.find('<div class="kb-index-box')
    stage = html.find('<div class="kb-stage">')
    if start < 0 or stage < 0:
        return html
    aside_close = html.rfind("</aside>", 0, stage)
    if aside_close < 0 or aside_close < start:
        return html
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
        prefix = "/"
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
