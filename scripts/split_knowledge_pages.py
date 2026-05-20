"""Split knowledge-base.html into multi-page KB (subnav = full page loads).

Run from repo root:
  py -3 scripts/split_knowledge_pages.py

Uses hard-coded line ranges (R_*) against the **pre-split** monolithic
knowledge-base.html. After the first run, knowledge-base.html is only the
overview page—restore the monolith from git (or a backup) before re-running,
or update R_* to match your source file.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "knowledge-base.html"
VER = "20260427kb12"

# 1-based inclusive line ranges from knowledge-base.html (current structure)
R_HOME = (132, 199)
R_FEATURE = (201, 214)
R_DAILY = (216, 222)
R_CAX = (224, 291)
R_LEARN = (293, 362)
R_LIBRARY = (364, 558)
R_CURRICULUM = (560, 615)
R_GRAPH = (617, 654)
R_CONCEPTS = (656, 671)
R_GLOSSARY = (673, 704)
R_SOFTWARE = (706, 725)
R_INSTR = (727, 754)
R_ABOUT = (756, 765)
R_RELATED = (767, 783)


def lines_slice(lines: list[str], start: int, end: int) -> str:
    return "".join(lines[start - 1 : end])


def fix_cross_links(html: str, *, library: bool = False) -> str:
    """Point in-page #kb-* anchors to split pages where sections moved."""
    if library:
        html = html.replace('href="#kb-glossary"', 'href="./knowledge-glossary.html"')
        html = html.replace('href="#kb-curriculum"', 'href="./knowledge-curriculum.html"')
        html = html.replace('href="#kb-cax"', 'href="./knowledge-cax.html"')
        html = html.replace('href="#kb-self-study"', 'href="./knowledge-roadmap.html"')
    return html


def overview_main(lines: list[str]) -> str:
    h = lines_slice(lines, *R_HOME)
    h = h.replace('href="#kb-curriculum"', 'href="./knowledge-curriculum.html"')
    h = h.replace('href="#kb-concepts"', 'href="./kb-terms.html"')
    h = h.replace('href="#kb-glossary"', 'href="./knowledge-glossary.html"')
    h = h.replace('href="#kb-instructors"', 'href="./knowledge-domains.html"')
    h = h.replace('href="#kb-graph"', 'href="./kb-graph.html"')
    h = h.replace('href="#kb-self-study"', 'href="./knowledge-roadmap.html"')
    h = h.replace('href="#kb-pdf-library"', 'href="./knowledge-library.html"')
    h = h.replace('href="#kb-software"', 'href="./kb-software.html"')
    h = h.replace('href="#kb-about"', 'href="#kb-about"')
    body = h + lines_slice(lines, *R_FEATURE) + lines_slice(lines, *R_DAILY)
    body = body.replace('href="#kb-graph"', 'href="./kb-graph.html"')
    body = body.replace('href="#kb-glossary"', 'href="./knowledge-glossary.html"')
    body += lines_slice(lines, *R_ABOUT)
    rel = lines_slice(lines, *R_RELATED)
    rel = rel.replace('href="#kb-cax"', 'href="./knowledge-cax.html"')
    rel = rel.replace('href="#kb-self-study"', 'href="./knowledge-roadmap.html"')
    rel = rel.replace('href="#kb-pdf-library"', 'href="./knowledge-library.html"')
    body += rel
    return body


def graph_inject_filters(graph_html: str, concepts_tag_lines: str) -> str:
    """Insert tag-filter row under graph section head for knowledge.js graph tinting."""
    needle = '<span class="section-note">Interactive</span>\n              </div>\n'
    if needle not in graph_html:
        raise SystemExit("graph_html: expected Interactive section-note block missing")
    insert = (
        needle
        + "              <div class=\"kb-tag-cloud kb-graph-filters\" aria-label=\"Filter graph by tag\">\n"
        + concepts_tag_lines
        + "              </div>\n"
    )
    return graph_html.replace(needle, insert, 1)


SIDEBAR = f"""      <aside class="kb-sidebar kb-sidebar--portal" id="kb-rail" aria-label="Knowledge base navigation">
        <div class="kb-rail-toolbar">
          <span class="kb-rail-toolbar-label" id="kb-rail-label">Navigation</span>
          <button
            type="button"
            class="kb-rail-toggle"
            id="kb-rail-toggle"
            aria-labelledby="kb-rail-label"
            aria-controls="kb-rail"
            aria-expanded="true"
            title="Hide navigation (wider reading)"
          >
            <span class="kb-rail-toggle-icon" aria-hidden="true">◀</span>
            <span class="kb-sr-only">Collapse navigation sidebar</span>
          </button>
        </div>
        <label class="kb-sr-only" for="kb-sidebar-search">Search knowledge base</label>
        <input
          type="search"
          id="kb-sidebar-search"
          class="kb-portal-search"
          placeholder="Search titles &amp; terms…"
          autocomplete="off"
        />

            <div class="kb-index-box">
              <strong class="kb-index-title">Core Index</strong>
              <p class="meta kb-sidebar-taxonomy-note">
                Topics can overlap—like tag-like lenses and category-like buckets on the same idea.
              </p>
              <a class="kb-index-link" href="./knowledge-base.html">Overview</a>
              <a class="kb-index-link" href="./knowledge-cax.html">CAD / CAE / CAM</a>
              <a class="kb-index-link" href="./kb-terms.html#kb-term-jump">Terms <span>40+</span></a>
              <a class="kb-index-link" href="./knowledge-domains.html">Domain tracks</a>
              <a class="kb-index-link" href="./kb-graph.html">Knowledge graph</a>
              <a class="kb-index-link" href="./kb-software.html">Software map</a>
              <a class="kb-index-link" href="./kb-vendors.html">Vendor docs</a>
            </div>

            <div class="kb-nav-group">
              <button class="kb-nav-toggle" aria-expanded="true">Maps &amp; lanes</button>
              <div class="kb-nav-links">
                <a class="kb-side-link" href="./knowledge-cax.html">CAD · CAE · CAM</a>
                <a class="kb-side-link" href="./kb-graph.html">Knowledge graph</a>
              </div>
            </div>
            <div class="kb-nav-group">
              <button class="kb-nav-toggle" aria-expanded="true">Topics</button>
              <div class="kb-nav-links">
                <a class="kb-side-link" href="./kb-terms.html#kb-term-jump">Terms</a>
                <a class="kb-side-link" href="./kb-software.html">Software map</a>
                <a class="kb-side-link" href="./kb-vendors.html">Vendor docs (official)</a>
                <a class="kb-side-link" href="./knowledge-domains.html">Domains &amp; industries</a>
              </div>
            </div>
            <div class="kb-nav-group">
              <button class="kb-nav-toggle" aria-expanded="false">Meta</button>
              <div class="kb-nav-links kb-collapsed">
                <a class="kb-side-link" href="./knowledge-base.html#kb-about">About this hub</a>
              </div>
            </div>
      </aside>
"""


def subnav(active: str) -> str:
    orphans = {"learn", "library", "curriculum"}
    key_active = "__none__" if active in orphans else active

    def item(key: str, href: str, label: str) -> str:
        cls = (
            ' class="kb-subnav-link active"'
            if key == key_active and key_active != "__none__"
            else ' class="kb-subnav-link"'
        )
        return f'          <a{cls} href="{href}">{label}</a>\n'

    return (
        '        <nav class="kb-subnav" aria-label="Knowledge base sections">\n'
        + item("overview", "./knowledge-base.html", "Overview")
        + item("cax", "./knowledge-cax.html", "CAx")
        + item("concepts", "./kb-terms.html", "Terms")
        + item("graph", "./kb-graph.html", "Graph")
        + item("software", "./kb-software.html", "Software")
        + item("vendor", "./kb-vendors.html", "Vendor hubs")
        + item("domains", "./knowledge-domains.html", "Domains")
        + "        </nav>\n"
    )


def head_block(*, title: str, canonical: str, description: str, ld_url: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta
      name="description"
      content="{description}"
    />
    <meta name="robots" content="index,follow,max-image-preview:large" />
    <link rel="canonical" href="{canonical}" />
    <link
      rel="icon"
      type="image/svg+xml"
      href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3C/svg%3E"
    />
    <link rel="shortcut icon" href="data:image/x-icon;," />
    <link rel="apple-touch-icon" href="data:image/png;," />
    <link rel="preload" href="./styles.css?v={VER}" as="style" />
    <link rel="stylesheet" href="./styles.css?v={VER}" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": "CAD Knowledge Base",
        "url": "{ld_url}",
        "description": "{description}"
      }}
    </script>
  </head>
  <body data-page="knowledge">
    <header class="topbar">
      <div class="container topbar-inner">
        <a class="brand" href="./index.html">
          <span class="brand-badge">LC</span>
          <span>LearnCAD</span>
        </a>
        <nav class="nav">
          <a class="nav-link" data-nav="home" href="./index.html">Home</a>
          <a class="nav-link" data-nav="knowledge" href="./knowledge-base.html">Knowledge Base</a>
          <a class="nav-link" data-nav="tutorials" href="./tutorials.html">Tutorials</a>
          <a class="nav-link" data-nav="news" href="./news.html">News</a>
          <a class="nav-link" data-nav="about" href="./about.html">About</a>
        </nav>
      </div>
    </header>

    <div class="kb-app" id="kb-app">
"""


FOOTER = f"""    <footer class="footer site-footer">
      <div class="container site-footer-inner">
        <div class="site-footer-brand">
          <p class="site-footer-tagline">LearnCAD</p>
          <p class="site-footer-desc">CAD knowledge base and tutorial navigation. We link to original sources and do not host third-party videos.</p>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Learn</h4>
          <ul class="site-footer-links">
            <li><a href="./tutorials.html">Tutorials</a></li>
            <li><a href="./knowledge-base.html">Knowledge base</a></li>
            <li><a href="./news.html">CAD news</a></li>
          </ul>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Site</h4>
          <ul class="site-footer-links">
            <li><a href="./about.html">About</a></li>
            <li><a href="./contact.html">Contact</a></li>
          </ul>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Legal</h4>
          <ul class="site-footer-links">
            <li><a href="./privacy.html">Privacy policy</a></li>
            <li><a href="./terms.html">Terms of use</a></li>
            <li><a href="./legal.html">Copyright &amp; disclaimer</a></li>
          </ul>
        </div>
      </div>
      <div class="container site-footer-bottom">
        <p>© <span id="footer-year"></span> LearnCAD. All rights reserved.</p>
      </div>
    </footer>
    <script src="./app.js" defer></script>
    <script src="./knowledge.js?v={VER}" defer></script>
  </body>
</html>
"""


def wrap_page(active: str, main_inner: str) -> str:
    return (
        head_block(
            title=PAGES[active][0],
            canonical=PAGES[active][1],
            description=PAGES[active][2],
            ld_url=PAGES[active][3],
        )
        + SIDEBAR
        + '      <div class="kb-stage">\n'
        + subnav(active)
        + '        <div class="kb-stage-scroll">\n'
        + '          <div class="kb-main kb-main--portal">\n'
        + main_inner
        + "          </div>\n        </div>\n      </div>\n    </div>\n\n"
        + FOOTER
    )


PAGES = {
    "overview": (
        "CAD Knowledge Base · Overview",
        "/knowledge-base.html",
        "CAD foundations hub—overview, quick links to structured literacy pages, glossary, and maps.",
        "https://learncad.io/knowledge-base.html",
    ),
    "cax": (
        "CAD Knowledge Base · CAD, CAE &amp; CAM",
        "/knowledge-cax.html",
        "CAD vs CAE vs CAM literacy primer and curated sources.",
        "https://learncad.io/knowledge-cax.html",
    ),
    "learn": (
        "CAD Knowledge Base · Self-study roadmap",
        "/knowledge-roadmap.html",
        "How to learn CAD on your own—tracks, tools, and practice loops.",
        "https://learncad.io/knowledge-roadmap.html",
    ),
    "library": (
        "CAD Knowledge Base · PDF reference library",
        "/knowledge-library.html",
        "Local PDF index, concept matrix, and drill-down notes (no full text republication).",
        "https://learncad.io/knowledge-library.html",
    ),
    "curriculum": (
        "CAD Knowledge Base · Curriculum map",
        "/knowledge-curriculum.html",
        "Six-stage CAD literacy curriculum for retention.",
        "https://learncad.io/knowledge-curriculum.html",
    ),
    "concepts": (
        "CAD Knowledge Base · Terms hub",
        "/kb-terms.html",
        "Terms hub—links to glossary, graph, learning paths, and domain tracks.",
        "https://learncad.io/kb-terms.html",
    ),
    "glossary": (
        "CAD Knowledge Base · Glossary",
        "/knowledge-glossary.html",
        "High-frequency CAD and BIM glossary terms with beginner-first filters.",
        "https://learncad.io/knowledge-glossary.html",
    ),
    "graph": (
        "CAD Knowledge Base · Knowledge graph",
        "/kb-graph.html",
        "Interactive beginner literacy graph for CAD topics.",
        "https://learncad.io/kb-graph.html",
    ),
    "software": (
        "CAD Knowledge Base · Software landscape",
        "/kb-software.html",
        "High-level map of common CAD-related tools (names only; verify licensing separately).",
        "https://learncad.io/kb-software.html",
    ),
    "domains": (
        "CAD Knowledge Base · Domains &amp; industries",
        "/knowledge-domains.html",
        "AEC, MFG, product design, and cross-platform literacy tracks.",
        "https://learncad.io/knowledge-domains.html",
    ),
}


def main() -> None:
    raw = SRC.read_text(encoding="utf-8")
    lines = raw.splitlines(keepends=True)

    concepts_tags = lines_slice(lines, 662, 669)

    graph_main = graph_inject_filters(lines_slice(lines, *R_GRAPH), concepts_tags)

    lib_main = fix_cross_links(lines_slice(lines, *R_LIBRARY), library=True)

    concepts_hub = lines_slice(lines, *R_CONCEPTS).replace(
        "<span class=\"section-note\">Click to filter</span>",
        "<span class=\"section-note\">Mental map · each topic opens in its own page</span>",
    )
    # Strip old tag-cloud block from sliced concepts; replace with hub tiles (maintain manually if re-splitting).
    concepts_hub = concepts_hub.split("<div class=\"kb-tag-cloud\">")[0].rstrip()
    concepts_hub += (
        '              <p class="meta" style="margin-top: 0; max-width: 52rem">\n'
        "                On this site, <strong>concepts</strong> are the big ideas—how 2D and 3D relate, what CAx stands for, how curriculum stages build on each other.\n"
        "                <strong>Term cards</strong> (Layer, Xref, BIM, …) live on the\n"
        '                <a href="./knowledge-glossary.html">glossary page</a> with filters. Use the tiles below to move without long in-page jumps.\n'
        "              </p>\n"
        '              <div class="kb-portal-quick-wrap" style="margin-top: 14px">\n'
        '                <h2 class="kb-portal-quick-heading">Jump in</h2>\n'
        '                <div class="kb-portal-quick-grid">\n'
        '                  <a class="kb-portal-tile" href="./knowledge-glossary.html">\n'
        '                    <span class="kb-portal-tile-emoji" aria-hidden="true">📇</span>\n'
        "                    <span>Glossary terms</span>\n"
        "                  </a>\n"
        '                  <a class="kb-portal-tile" href="./kb-graph.html">\n'
        '                    <span class="kb-portal-tile-emoji" aria-hidden="true">🕸️</span>\n'
        "                    <span>Knowledge graph</span>\n"
        "                  </a>\n"
        '                  <a class="kb-portal-tile" href="./knowledge-cax.html">\n'
        '                    <span class="kb-portal-tile-emoji" aria-hidden="true">⚙️</span>\n'
        "                    <span>CAx primer</span>\n"
        "                  </a>\n"
        '                  <a class="kb-portal-tile" href="./knowledge-domains.html">\n'
        '                    <span class="kb-portal-tile-emoji" aria-hidden="true">🏗️</span>\n'
        "                    <span>Domain tracks</span>\n"
        "                  </a>\n"
        '                  <a class="kb-portal-tile" href="./kb-software.html">\n'
        '                    <span class="kb-portal-tile-emoji" aria-hidden="true">🧰</span>\n'
        "                    <span>Software map</span>\n"
        "                  </a>\n"
        "                </div>\n"
        "              </div>\n"
        "            </div>\n"
    )

    glossary_tags = lines_slice(lines, 662, 669)
    glossary_main = lines_slice(lines, *R_GLOSSARY)
    glossary_main = glossary_main.replace(
        '<span class="section-note">Beginner-first</span>\n              </div>\n',
        '<span class="section-note">Filter by tag · pairs with the <a href="./kb-graph.html">knowledge graph</a></span>\n              </div>\n'
        '              <div class="kb-tag-cloud">\n'
        + glossary_tags
        + "              </div>\n",
        1,
    )

    pages_out = {
        "knowledge-base.html": wrap_page("overview", overview_main(lines)),
        "knowledge-cax.html": wrap_page("cax", lines_slice(lines, *R_CAX)),
        "knowledge-roadmap.html": wrap_page("learn", lines_slice(lines, *R_LEARN)),
        "knowledge-library.html": wrap_page("library", lib_main),
        "knowledge-curriculum.html": wrap_page("curriculum", lines_slice(lines, *R_CURRICULUM)),
        "kb-terms.html": wrap_page("concepts", concepts_hub),
        "knowledge-glossary.html": wrap_page("glossary", glossary_main),
        "kb-graph.html": wrap_page("graph", graph_main),
        "kb-software.html": wrap_page("software", lines_slice(lines, *R_SOFTWARE)),
        "knowledge-domains.html": wrap_page("domains", lines_slice(lines, *R_INSTR)),
    }

    for name, html in pages_out.items():
        (ROOT / name).write_text(html, encoding="utf-8")
        print("Wrote", name)

    # Fix JSON-LD description escaping for pages with & in title — optional; skip

    print("Done. Re-run if you change monolith line numbers.")


if __name__ == "__main__":
    main()
