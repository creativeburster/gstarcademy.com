"""
Inject Open Graph + Twitter Card meta tags + Organization JSON-LD into all
root-level HTML pages that lack them.

E-E-A-T hardening: every page should have author/publisher context, OG cards,
and structured data so search engines and social previews work.

Idempotent: safe to re-run.
"""

from __future__ import annotations
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://learncad.io"

# Pages handled by build_software_content.py — skip them here.
SKIP_PATTERNS = ["kb/concepts/", "kb/software/", "kb/vendors/", "kb/pilot/"]

# Map page basename → (og_type, og_title_suffix)
PAGE_META = {
    "index.html": ("website", None),
    "about.html": ("article", "About LearnCAD"),
    "contact.html": ("article", "Contact LearnCAD"),
    "knowledge-base.html": ("article", "CAD Knowledge Base — Overview"),
    "kb-software.html": ("article", "CAD Software Profiles"),
    "kb-terms.html": ("article", "CAD Terminology Index"),
    "kb-faq.html": ("article", "CAD FAQs by Software"),
    "kb-graph.html": ("article", "CAD Knowledge Graph"),
    "kb-vendors.html": ("article", "CAD Vendors"),
    "tutorials.html": ("article", "CAD Tutorials"),
    "tutorial-detail.html": ("article", "Tutorial Detail"),
    "news.html": ("article", "CAD News"),
    "topic.html": ("article", "Topic"),
    "knowledge-cax.html": ("article", "CAD/CAE/CAM Family"),
    "knowledge-curriculum.html": ("article", "CAD Curriculum"),
    "knowledge-domains.html": ("article", "CAD Domains"),
    "knowledge-glossary.html": ("article", "CAD Glossary"),
    "knowledge-learn.html": ("article", "Learn CAD"),
    "knowledge-library.html": ("article", "CAD Library"),
    "knowledge-roadmap.html": ("article", "CAD Roadmap"),
    "editorial-process.html": ("article", "Editorial Process & Sources"),
    "legal.html": ("article", "Legal — Copyright & Disclaimer"),
    "privacy.html": ("article", "Privacy Policy"),
    "terms.html": ("article", "Terms of Use"),
}


def extract_meta(html: str, name: str) -> str | None:
    """Extract the content of <meta name|property="..."> tag."""
    pattern = re.compile(
        r'<meta\s+(?:name|property)="' + re.escape(name) + r'"\s+content="([^"]*)"',
        re.IGNORECASE,
    )
    m = pattern.search(html)
    if m:
        return m.group(1)
    return None


def extract_title(html: str) -> str | None:
    m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip()
    return None


def extract_canonical(html: str) -> str | None:
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', html, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def build_og_block(html: str, basename: str) -> str:
    og_type, _suffix = PAGE_META.get(basename, ("article", None))
    title = extract_title(html) or "LearnCAD"
    description = extract_meta(html, "description") or "LearnCAD — structured CAD knowledge base and tutorial navigation."
    canonical = extract_canonical(html) or f"/{basename}"
    if canonical.startswith("/"):
        canonical_url = f"{SITE_URL}{canonical}"
    elif canonical.startswith("http"):
        canonical_url = canonical
    else:
        canonical_url = f"{SITE_URL}/{canonical.lstrip('./')}"

    # Strip trailing site brand from title for cleaner OG
    og_title = title
    for sep in [" · LearnCAD", " — LearnCAD", " - LearnCAD", " | LearnCAD"]:
        if sep in og_title:
            og_title = og_title.split(sep, 1)[0]
            break

    block = (
        f'<meta property="og:type" content="{og_type}" />\n'
        f'    <meta property="og:title" content="{_escape(og_title)}" />\n'
        f'    <meta property="og:description" content="{_escape(description)}" />\n'
        f'    <meta property="og:url" content="{canonical_url}" />\n'
        f'    <meta property="og:site_name" content="LearnCAD" />\n'
        f'    <meta name="twitter:card" content="summary_large_image" />\n'
        f'    <meta name="twitter:title" content="{_escape(og_title)}" />\n'
        f'    <meta name="twitter:description" content="{_escape(description)}" />'
    )
    return block, canonical_url, og_title, description


def _escape(s: str) -> str:
    return s.replace('"', "&quot;")


def build_jsonld(basename: str, canonical_url: str, og_title: str, description: str) -> str:
    """Build Organization + WebSite JSON-LD for index, Article JSON-LD for others."""
    publisher_json = (
        '"publisher":{"@type":"Organization","name":"LearnCAD","url":"https://learncad.io/",'
        '"logo":{"@type":"ImageObject","url":"https://learncad.io/favicon.svg"},'
        '"sameAs":["https://learncad.io/about.html"]}'
    )
    if basename == "index.html":
        organization = (
            '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization",'
            '"name":"LearnCAD","url":"https://learncad.io/",'
            '"logo":{"@type":"ImageObject","url":"https://learncad.io/favicon.svg"},'
            '"description":"LearnCAD is a structured CAD knowledge base and tutorial navigation site for AEC, MFG, and Civil Engineering professionals.",'
            '"sameAs":["https://learncad.io/about.html","https://learncad.io/editorial-process.html"]}</script>'
        )
        website = (
            '<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite",'
            '"name":"LearnCAD","url":"https://learncad.io/",'
            '"potentialAction":{"@type":"SearchAction",'
            '"target":{"@type":"EntryPoint","urlTemplate":"https://learncad.io/kb-terms.html?q={search_term_string}"},'
            '"query-input":"required name=search_term_string"}}</script>'
        )
        return f"    {organization}\n    {website}"

    article = (
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article",'
        f'"headline":"{_escape_json(og_title)}",'
        f'"description":"{_escape_json(description)}",'
        f'"url":"{canonical_url}",'
        '"datePublished":"2026-05-24","dateModified":"2026-05-24","inLanguage":"en",'
        '"mainEntityOfPage":"' + canonical_url + '",'
        '"author":{"@type":"Organization","name":"LearnCAD Editorial Team","url":"https://learncad.io/about.html"},'
        + publisher_json
        + "}</script>"
    )
    return f"    {article}"


def _escape_json(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def already_has_og(html: str) -> bool:
    return 'property="og:type"' in html


def already_has_jsonld(html: str) -> bool:
    return 'application/ld+json' in html


def patch_file(path: Path) -> bool:
    """Returns True if the file was modified."""
    html = path.read_text(encoding="utf-8")
    basename = path.name

    if basename not in PAGE_META:
        return False

    changed = False

    if not already_has_og(html):
        og_block, canonical_url, og_title, description = build_og_block(html, basename)
        # Insert before the existing canonical link or after the description meta.
        anchor = re.search(r'(<link\s+rel="canonical"[^>]*>)', html, re.IGNORECASE)
        if anchor:
            html = html.replace(anchor.group(1), anchor.group(1) + "\n    " + og_block, 1)
            changed = True
        else:
            # Insert before </head>
            html = html.replace("</head>", "    " + og_block + "\n  </head>", 1)
            changed = True
    else:
        # Pull info anyway for JSON-LD
        _, canonical_url, og_title, description = build_og_block(html, basename)

    if not already_has_jsonld(html):
        jsonld = build_jsonld(basename, canonical_url, og_title, description)
        html = html.replace("</head>", jsonld + "\n  </head>", 1)
        changed = True

    if changed:
        path.write_text(html, encoding="utf-8")
    return changed


def main() -> int:
    patched = 0
    skipped = 0
    for path in sorted(REPO_ROOT.glob("*.html")):
        # Skip pages handled by other generators
        if any(p in str(path) for p in SKIP_PATTERNS):
            continue
        if patch_file(path):
            patched += 1
            print(f"  patched: {path.name}")
        else:
            skipped += 1
    print(f"OG/JSON-LD inject: {patched} patched, {skipped} unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
