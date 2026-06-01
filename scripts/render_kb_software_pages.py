"""
Render static KB software profile pages from data/kb_software.json.

Usage (from repo root):
  python scripts/render_kb_software_pages.py
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data" / "kb_software.json"
OUT_DIR = REPO / "kb" / "software"
CSS_VER = "20260427kb12"
SITE = "https://learncad.io"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def sidebar_block() -> str:
    return """
            <div class="kb-index-box">
              <strong class="kb-index-title">Six lanes</strong>
              <p class="meta kb-sidebar-taxonomy-note">
                Mirrors the top strip—taxonomy view of the same routes (expect overlap).
              </p>
              <a class="kb-index-link" href="../../knowledge-base.html">Overview</a>
              <a class="kb-index-link" href="../../kb-vendors.html">Vendors</a>
              <a class="kb-index-link" href="../../kb-software.html">Software</a>
              <a class="kb-index-link" href="../../kb-terms.html">Terms</a>
              <a class="kb-index-link" href="../../kb-faq.html">FAQ</a>
              <a class="kb-index-link" href="../../kb-graph.html">Graph</a>
              <a class="kb-index-link" href="./index.html">Software profiles</a>
            </div>

            <div class="kb-nav-group">
              <button class="kb-nav-toggle" aria-expanded="true">Drill down</button>
              <div class="kb-nav-links">
                <a class="kb-side-link" href="../../tutorials.html">Tutorial library</a>
                <a class="kb-side-link" href="../../knowledge-glossary.html">Term glossary (cards)</a>
              </div>
            </div>
            <div class="kb-nav-group">
              <button class="kb-nav-toggle" aria-expanded="true">Topics</button>
              <div class="kb-nav-links">
                <a class="kb-side-link" href="../../knowledge-base.html">Hub overview</a>
                <a class="kb-side-link" href="../../news.html">CAD news</a>
              </div>
            </div>
            <div class="kb-nav-group">
              <button class="kb-nav-toggle" aria-expanded="false">Meta</button>
              <div class="kb-nav-links kb-collapsed">
                <a class="kb-side-link" href="../../knowledge-base.html#kb-about">About this hub</a>
              </div>
            </div>"""


def page_shell(
    title: str,
    description: str,
    canonical_suffix: str,
    json_ld: str,
    main_html: str,
) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <!-- Google tag (gtag.js) - Performance Optimized Loading -->
    <link rel="preconnect" href="https://www.googletagmanager.com" />
    <link rel="dns-prefetch" href="https://www.googletagmanager.com" />
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      window.gtag = gtag;
      window.addEventListener('load', function() {{
        const initGtag = () => {{
          const script = document.createElement('script');
          script.src = 'https://www.googletagmanager.com/gtag/js?id=G-ZV3YR72933';
          script.async = true;
          document.head.appendChild(script);
          gtag('js', new Date());
          gtag('config', 'G-ZV3YR72933');
        }};
        if ('requestIdleCallback' in window) {{
          requestIdleCallback(initGtag);
        }} else {{
          setTimeout(initGtag, 1);
        }}
      }});
    </script>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}" />
    <meta name="robots" content="index,follow,max-image-preview:large" />
    <link rel="canonical" href="{esc(canonical_suffix)}" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="preload" href="../../styles.css?v={CSS_VER}" as="style" />
    <link rel="stylesheet" href="../../styles.css?v={CSS_VER}" />
    <script type="application/ld+json">
{json_ld}
    </script>
  </head>
  <body data-page="knowledge">
    <header class="topbar">
      <div class="container topbar-inner">
        <a class="brand" href="../../index.html">
          <span class="brand-badge">GC</span>
          <span>Gstarcademy</span>
        </a>
        <nav class="nav">
          <a class="nav-link" data-nav="home" href="../../index.html">Home</a>
          <a class="nav-link" data-nav="knowledge" href="../../knowledge-base.html">Knowledge Base</a>
          <a class="nav-link" data-nav="tutorials" href="../../tutorials.html">Tutorials</a>
          <a class="nav-link" data-nav="news" href="../../news.html">News</a>
          <a class="nav-link" data-nav="about" href="../../about.html">About</a>
        </nav>
      </div>
    </header>

    <div class="kb-app" id="kb-app">
      <aside class="kb-sidebar kb-sidebar--portal" id="kb-rail" aria-label="Knowledge base navigation">
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
{sidebar_block()}
      </aside>
      <div class="kb-stage">
        <nav class="kb-subnav" aria-label="Knowledge base sections">
          <a class="kb-subnav-link" href="../../knowledge-base.html">Overview</a>
          <a class="kb-subnav-link" href="../../kb-vendors.html">Vendors</a>
          <a class="kb-subnav-link active" href="../../kb-software.html">Software</a>
          <a class="kb-subnav-link" href="../../kb-terms.html">Terms</a>
          <a class="kb-subnav-link" href="../../kb-faq.html">FAQ</a>
          <a class="kb-subnav-link" href="../../kb-graph.html">Graph</a>
        </nav>
        <div class="kb-stage-scroll">
          <div class="kb-main kb-main--portal">
{main_html}
          </div>
        </div>
      </div>
    </div>

    <footer class="footer site-footer">
      <div class="container site-footer-inner">
        <div class="site-footer-brand">
          <p class="site-footer-tagline">Gstarcademy</p>
          <p class="site-footer-desc">CAD knowledge base and tutorial navigation. We link to original sources and do not host third-party videos.</p>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Learn</h4>
          <ul class="site-footer-links">
            <li><a href="../../tutorials.html">Tutorials</a></li>
            <li><a href="../../knowledge-base.html">Knowledge base</a></li>
            <li><a href="../../tutorials.html">Tutorial library</a></li>
            <li><a href="../../news.html">CAD news</a></li>
          </ul>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Site</h4>
          <ul class="site-footer-links">
            <li><a href="../../about.html">About</a></li>
            <li><a href="../../contact.html">Contact</a></li>
          </ul>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Legal</h4>
          <ul class="site-footer-links">
            <li><a href="../../privacy.html">Privacy policy</a></li>
            <li><a href="../../terms.html">Terms of use</a></li>
            <li><a href="../../legal.html">Copyright &amp; disclaimer</a></li>
          </ul>
        </div>
      </div>
      <div class="container site-footer-bottom">
        <p>© <span id="footer-year"></span> Gstarcademy. All rights reserved.</p>
      </div>
    </footer>
    <script src="../../app.js" defer></script>
    <script src="../../knowledge.js?v={CSS_VER}" defer></script>
  </body>
</html>
"""


def ld_software_application(item: dict) -> str:
    desc = ((item.get("tagline") or "") + " " + (item.get("summary") or "")).strip()
    blob: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": item["name"],
        "applicationCategory": "DesignApplication",
        "description": desc[:500],
        "url": f"{SITE}/kb/software/{item['slug']}.html",
        "brand": {"@type": "Brand", "name": item.get("vendor_name") or ""},
    }
    raw = json.dumps(blob, ensure_ascii=False, indent=2)
    return "\n".join("      " + line for line in raw.split("\n"))


def render_detail(item: dict) -> str:
    slug = item["slug"]
    name = item["name"]
    q = item.get("tutorial_search_q") or name
    outputs = item.get("typical_outputs") or []
    domains = item.get("typical_domains") or []
    terms = item.get("related_term_slugs") or []
    vendor = item.get("vendor_name") or ""
    cat = item.get("category_label") or ""
    outputs_li = "".join(f"              <li>{esc(x)}</li>\n" for x in outputs)
    domains_li = "".join(f"              <li>{esc(x)}</li>\n" for x in domains)
    terms_html = ", ".join(esc(t) for t in terms) if terms else "—"

    vendor_docs = '<a href="../../kb-vendors.html#kb-vendor-docs">Vendor documentation hubs</a>'

    main = f"""
            <article class="kb-section kb-anchor-target" data-kb-profile-slug="{esc(slug)}">
              <nav class="meta kb-breadcrumbs" aria-label="Breadcrumb" style="margin-bottom: 14px">
                <a href="../../index.html">Home</a>
                <span aria-hidden="true"> · </span>
                <a href="../../knowledge-base.html">Knowledge base</a>
                <span aria-hidden="true"> · </span>
                <a href="../../kb-software.html">Software</a>
                <span aria-hidden="true"> · </span>
                <span aria-current="page">{esc(name)}</span>
              </nav>

              <div class="kb-section-head">
                <h1 style="margin: 0">{esc(name)}</h1>
                <span class="section-note">{esc(cat)}</span>
              </div>
              <p class="meta" style="margin-top: 6px"><strong>{esc(vendor)}</strong> · status: {esc(str(item.get("status") or "draft"))}</p>

              <p class="meta" style="margin-top: 12px; max-width: 52rem">{esc(item.get("tagline") or "")}</p>

              <div class="panel" style="margin-top: 16px">
                <h3 class="panel-title">Overview</h3>
                <p style="margin: 10px 0 0 0; max-width: 52rem; line-height: 1.6">{esc(item.get("summary") or "")}</p>
              </div>

              <div class="panel" style="margin-top: 14px">
                <h3 class="panel-title">Typical outputs &amp; exchange</h3>
                <ul style="margin: 10px 0 0 18px">{outputs_li}</ul>
              </div>

              <div class="panel" style="margin-top: 14px">
                <h3 class="panel-title">Where it commonly shows up</h3>
                <ul style="margin: 10px 0 0 18px">{domains_li}</ul>
              </div>

              <div class="panel" style="margin-top: 14px">
                <h3 class="panel-title">Drill down</h3>
                <p class="meta" style="margin-top: 8px">
                  <strong>Tutorials:</strong>
                  <a href="../../tutorials.html">Open tutorial discovery</a>
                  <span class="meta"> — try keyword “{esc(q)}” in filters or search when available.</span>
                </p>
                <p class="meta" style="margin-top: 10px">
                  <strong>Related glossary keys (anchors TBD):</strong> {terms_html}
                </p>
                <p class="meta" style="margin-top: 10px">
                  <strong>OEM / official tree:</strong> {vendor_docs}
                </p>
              </div>
            </article>
"""

    canon = f"{SITE}/kb/software/{slug}.html"
    desc = (item.get("tagline") or "")[:155]
    json_ld = ld_software_application(item)

    return page_shell(
        title=f"{name} · Software profile · CAD Knowledge Base",
        description=desc,
        canonical_suffix=canon,
        json_ld=json_ld,
        main_html=main,
    )


def render_index(items: list[dict], base_path: str) -> str:
    rows = []
    for it in sorted(items, key=lambda x: x["name"].lower()):
        s = it["slug"]
        n = it["name"]
        v = it.get("vendor_name") or ""
        c = it.get("category_label") or ""
        rows.append(
            f"""            <tr>
              <td><a href="./{esc(s)}.html">{esc(n)}</a></td>
              <td>{esc(v)}</td>
              <td class="meta">{esc(c)}</td>
            </tr>"""
        )
    table = "\n".join(rows)

    main = f"""
            <div class="kb-section kb-anchor-target">
              <div class="kb-section-head">
                <h1 style="margin: 0">Software profiles</h1>
                <span class="section-note">Stable URLs for each product</span>
              </div>
              <p class="meta" style="margin-top: 10px; max-width: 52rem">
                Each row links to a lightweight <strong>product profile</strong> you can reference from terms and tutorial notes. Source data: <code>data/kb_software.json</code>. Regenerate with
                <code>python scripts/render_kb_software_pages.py</code>.
              </p>
              <p class="meta" style="margin-top: 8px">
                <a href="../../kb-software.html">← Software landscape (hub)</a>
              </p>

              <div class="panel" style="margin-top: 18px; overflow-x: auto">
                <table style="width: 100%; border-collapse: collapse">
                  <thead>
                    <tr>
                      <th style="text-align: left; padding: 8px">Product</th>
                      <th style="text-align: left; padding: 8px">Vendor</th>
                      <th style="text-align: left; padding: 8px">Lane</th>
                    </tr>
                  </thead>
                  <tbody>
{table}
                  </tbody>
                </table>
              </div>
            </div>
"""

    json_ld = f"""      {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "CAD software profiles",
        "url": "{SITE}{base_path}/index.html",
        "description": "Index of per-software knowledge base profile pages."
      }}"""

    return page_shell(
        title="Software profiles · CAD Knowledge Base",
        description="Index of per-software KB profiles with links to tutorials and vendor documentation hubs.",
        canonical_suffix=f"{SITE}{base_path}/index.html",
        json_ld=json_ld,
        main_html=main,
    )


def main() -> int:
    if not DATA.is_file():
        print(f"Missing {DATA}", file=sys.stderr)
        return 1
    doc = json.loads(DATA.read_text(encoding="utf-8"))
    items = doc.get("items")
    if not isinstance(items, list) or not items:
        print("Invalid items[] in kb_software.json", file=sys.stderr)
        return 1
    base_path = doc.get("base_path") or "/kb/software"

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    index_html = render_index(items, base_path)
    (OUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    for it in items:
        slug = it.get("slug")
        if not slug or not isinstance(slug, str):
            continue
        html_out = render_detail(it)
        (OUT_DIR / f"{slug}.html").write_text(html_out, encoding="utf-8")

    print(f"Wrote {len(items)} profiles + index under {OUT_DIR.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
