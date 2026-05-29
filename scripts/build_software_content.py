"""Build per-software KB content from data/sw/*.json.

For each software JSON, this script renders:
  - kb/software/<slug>.html       — deep software profile page
  - kb/concepts/<term-slug>.html  — one page per term
  - kb/vendors/<vendor-slug>.html — vendor masthead (idempotent merge)

It also rewrites blocks marked by AUTO-GEN sentinels in:
  - kb-faq.html      (FAQ sections, one per software)
  - knowledge.js     (graph nodes + links — appended sets)
  - kb-terms.html    (alphabetical term index)
  - sitemap.xml      (URL entries)

Run from repo root:
  python scripts/build_software_content.py

Content is original commentary by Gstarcademy editors; this script only assembles
the static HTML. Every concept page emits:
  - Article + DefinedTerm + BreadcrumbList JSON-LD (E-E-A-T compliant)
  - Author + Reviewer byline (from data/editorial.json)
  - "Sources & further reading" outbound link list
  - "Related concepts" + "Related software" + "Related FAQs" internal clusters
"""
from __future__ import annotations

import html as _html
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "sw"
EDITORIAL_PATH = ROOT / "data" / "editorial.json"
CONCEPTS_DIR = ROOT / "kb" / "concepts"
SOFTWARE_DIR = ROOT / "kb" / "software"
VENDORS_DIR = ROOT / "kb" / "vendors"
SITE_URL = "https://learncad.io"
CSS_VER = "v9_concept_visibility"

CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)
SOFTWARE_DIR.mkdir(parents=True, exist_ok=True)
VENDORS_DIR.mkdir(parents=True, exist_ok=True)


def esc(s: str) -> str:
    return _html.escape(s or "", quote=True)


def md_inline(s: str) -> str:
    """Tiny inline markdown: **bold**, *italic*, `code`, [text](url)."""
    if not s:
        return ""
    out = esc(s)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def paragraphs(text: str) -> str:
    """Convert prose with blank-line paragraphs into <p> blocks."""
    if not text:
        return ""
    blocks = re.split(r"\n\s*\n", text.strip())
    return "\n".join(f"<p>{md_inline(b.strip())}</p>" for b in blocks)


def bullet_list(items: list[str]) -> str:
    if not items:
        return ""
    lis = "\n".join(f"<li>{md_inline(x)}</li>" for x in items)
    return f"<ul>{lis}</ul>"


def fonts_block(relpath: str) -> str:
    css = f'{relpath}styles.css?v={CSS_VER}'
    return f"""<link rel="preload" href="{css}" as="style" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />
    <link rel="stylesheet" href="{css}" />"""


def topbar_html(relpath: str, page: str = "knowledge") -> str:
    return f"""<div class="header-stack">
      <aside class="site-notice" id="site-notice" data-notice-id="global-v2" aria-label="Announcement">
        <div class="site-notice-inner container">
          <p class="site-notice-text">
            Tip: open the <a class="site-notice-link" href="{relpath}tutorials.html">tutorial library</a> to filter by software, task, level, and source—then follow outbound links to the originals.
          </p>
          <button type="button" class="site-notice-close" aria-label="Dismiss announcement">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      </aside>
      <header class="topbar">
        <div class="container topbar-inner">
          <a class="brand" href="{relpath}index.html">
            <span class="brand-badge">GC</span>
            <span>Gstarcademy</span>
          </a>
          <button class="hamburger" aria-label="Toggle navigation menu" aria-expanded="false">
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
          </button>
          <nav class="nav">
            <div class="nav-header">
              <button class="nav-close" aria-label="Close navigation menu">
                <span class="nav-close-icon">×</span>
              </button>
            </div>
            <a class="nav-link" data-nav="home" href="{relpath}index.html">Home</a>
            <a class="nav-link{' active' if page=='knowledge' else ''}" data-nav="knowledge" href="{relpath}knowledge-base.html">Wiki</a>
            <a class="nav-link" data-nav="tutorials" href="{relpath}tutorials.html">Tutorials</a>
            <a class="nav-link" data-nav="news" href="{relpath}news.html">News</a>
            <a class="nav-link" data-nav="about" href="{relpath}about.html">About</a>
          </nav>
        </div>
        <div class="nav-overlay" aria-hidden="true"></div>
      </header>
    </div>"""


def footer_html(relpath: str) -> str:
    return f"""<footer class="footer site-footer">
      <div class="container site-footer-inner">
        <div class="site-footer-brand">
          <p class="site-footer-tagline">Gstarcademy</p>
          <p class="site-footer-desc">CAD knowledge base and tutorial navigation. We link to high-quality, curated external CAD sources for AEC, MFG, and Civil Engineering professionals.</p>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Software Hubs</h4>
          <ul class="site-footer-links">
            <li><a href="{relpath}kb/software/autocad.html">AutoCAD Guide</a></li>
            <li><a href="{relpath}kb/software/revit.html">Revit Guide</a></li>
            <li><a href="{relpath}kb/software/fusion-360.html">Fusion 360</a></li>
            <li><a href="{relpath}kb/software/civil-3d.html">Civil 3D Guide</a></li>
            <li><a href="{relpath}kb/software/solidworks.html">SOLIDWORKS</a></li>
            <li><a href="{relpath}kb/software/catia.html">CATIA Guide</a></li>
            <li><a href="{relpath}kb/software/gstarcad.html">GstarCAD</a></li>
            <li><a href="{relpath}kb/software/inventor.html">Autodesk Inventor</a></li>
          </ul>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Technical Core</h4>
          <ul class="site-footer-links">
            <li><a href="{relpath}kb/concepts/intelligent-objects.html">2D Drafting</a></li>
            <li><a href="{relpath}kb/concepts/bim.html">BIM Coordination</a></li>
            <li><a href="{relpath}kb/concepts/parametric-constraints.html">Parametrics</a></li>
            <li><a href="{relpath}kb/concepts/command-alias.html">Command Line</a></li>
            <li><a href="{relpath}kb/concepts/drawing-merge.html">Drawing Merge</a></li>
            <li><a href="{relpath}kb/concepts/dwg-compare.html">DWG Compare</a></li>
            <li><a href="{relpath}kb/concepts/layer.html">Layer Strategy</a></li>
            <li><a href="{relpath}kb/concepts/xref.html">Xrefs &amp; Blocks</a></li>
          </ul>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Structured Learn</h4>
          <ul class="site-footer-links">
            <li><a href="{relpath}tutorials.html">Tutorial Library</a></li>
            <li><a href="{relpath}knowledge-base.html">Knowledge Center</a></li>
            <li><a href="{relpath}kb-graph.html">Interactive Graph</a></li>
            <li><a href="{relpath}knowledge-domains.html">Domain Map</a></li>
            <li><a href="{relpath}kb-software.html">Software Index</a></li>
            <li><a href="{relpath}kb-terms.html">CAD Glossary</a></li>
            <li><a href="{relpath}kb-faq.html">Technical FAQ</a></li>
          </ul>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Company &amp; Legal</h4>
          <ul class="site-footer-links">
            <li><a href="{relpath}about.html">About Project</a></li>
            <li><a href="{relpath}contact.html">Contact Us</a></li>
            <li><a href="{relpath}privacy.html">Privacy Policy</a></li>
            <li><a href="{relpath}terms.html">Terms of Use</a></li>
            <li><a href="{relpath}legal.html">Copyright &amp; Disclaimer</a></li>
          </ul>
        </div>
      </div>
      <div class="container site-footer-bottom">
        <p>© <span id="footer-year"></span> Gstarcademy. All rights reserved.</p>
      </div>
    </footer>"""


def author_jsonld(editorial: dict) -> dict:
    """Default Article author + reviewer schema fragment."""
    team = {t["id"]: t for t in editorial["editorial_team"]}
    return {
        "author": {
            "@type": "Organization",
            "name": team["lc-editorial"]["name"],
            "url": team["lc-editorial"]["url"],
        },
        "publisher": {
            "@type": "Organization",
            "name": editorial["publisher"]["name"],
            "url": editorial["publisher"]["url"],
            "logo": {
                "@type": "ImageObject",
                "url": editorial["publisher"]["logo"],
            },
        },
    }


def reviewer_jsonld(editorial: dict, reviewer_id: str) -> dict | None:
    team = {t["id"]: t for t in editorial["editorial_team"]}
    rev = team.get(reviewer_id)
    if not rev:
        return None
    return {
        "@type": "Person",
        "name": rev["name"],
        "jobTitle": rev["role"],
        "url": rev["url"],
    }


def open_graph(title: str, desc: str, url: str, kind: str = "article") -> str:
    return (
        f'<meta property="og:type" content="{kind}" />\n'
        f'    <meta property="og:title" content="{esc(title)}" />\n'
        f'    <meta property="og:description" content="{esc(desc)}" />\n'
        f'    <meta property="og:url" content="{esc(url)}" />\n'
        f'    <meta property="og:site_name" content="Gstarcademy" />\n'
        f'    <meta name="twitter:card" content="summary_large_image" />\n'
        f'    <meta name="twitter:title" content="{esc(title)}" />\n'
        f'    <meta name="twitter:description" content="{esc(desc)}" />\n'
    )


def breadcrumb_jsonld(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": url,
            }
            for i, (name, url) in enumerate(items)
        ],
    }


def get_relevant_faqs(term: dict, software: dict) -> list[dict]:
    """Select up to 3 relevant FAQs for the concept, filling with general ones if needed."""
    faqs = software.get("faqs", [])
    if not faqs:
        return []
        
    title_lower = term["title"].lower()
    slug_words = term["slug"].replace("-", " ").lower().split()
    
    matches = []
    for q in faqs:
        q_text = (q["question"] + " " + q["answer"]).lower()
        if title_lower in q_text:
            matches.append(q)
            continue
        word_match = False
        for word in slug_words:
            if len(word) > 3 and word in q_text:
                word_match = True
                break
        if word_match:
            matches.append(q)
            
    unique_matches = []
    seen = set()
    for q in matches:
        if q["question"] not in seen:
            seen.add(q["question"])
            unique_matches.append(q)
            
    for q in faqs:
        if len(unique_matches) >= 3:
            break
        if q["question"] not in seen:
            seen.add(q["question"])
            unique_matches.append(q)
            
    return unique_matches[:3]


def render_faq_accordion(relevant_faqs: list[dict], sw_name: str) -> str:
    """Render interactive details/summary blocks for relevant FAQs."""
    if not relevant_faqs:
        return ""
        
    items = []
    for q in relevant_faqs:
        items.append(f"""
        <details class="kb-concept-faq-item" style="margin: 12px 0; padding: 16px 20px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 12px; transition: border-color 0.2s ease;">
          <summary style="cursor:pointer; font-weight:600; color: var(--ink-text); outline: none; list-style: none;">
            <span style="color: var(--ink-focus); margin-right: 8px;">❓</span> {esc(q['question'])}
          </summary>
          <div style="margin-top: 12px; color: var(--ink-text-soft); line-height: 1.6; font-size: 14.5px;">
            {paragraphs(q['answer'])}
          </div>
        </details>
        """)
        
    return f"""
    <section class="kb-concept-section" style="margin-top: 40px; border-top: 1px solid var(--ink-line); padding-top: 32px;">
      <h2 style="font-size: 1.5rem; color: var(--ink-text); margin-bottom: 12px;">Relevant {sw_name} FAQs</h2>
      <p class="meta" style="margin-bottom: 18px;">Direct answers from our technical editorial desk concerning related workflows.</p>
      {"".join(items)}
    </section>
    """


def render_spotlight_card(software: dict) -> str:
    """Render an ecosystem spotlight card linking software and vendor."""
    sw_name = esc(software["name"])
    sw_slug = software["slug"]
    vendor_name = esc(software["vendor"]["name"])
    vendor_slug = software["vendor"]["slug"]
    tagline = esc(software.get("tagline", ""))
    summary = esc(software.get("summary", ""))
    
    return f"""
    <section class="kb-concept-section" style="margin-top: 40px; border-top: 1px solid var(--ink-line); padding-top: 32px;">
      <div class="kb-spotlight-card" style="background: linear-gradient(135deg, var(--ink-surface-2) 0%, var(--ink-surface-1) 100%); border: 1px solid var(--ink-line); border-radius: 16px; padding: 24px; display: flex; flex-direction: column; gap: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 20px;">🛡️</span>
          <h3 style="margin: 0; font-size: 1.25rem; color: var(--ink-text); font-weight: 700;">{sw_name} Ecosystem Context</h3>
        </div>
        <p style="margin: 0; color: var(--ink-text-soft); line-height: 1.6; font-size: 14.5px;">
          This concept is a core structural element of the <strong>{sw_name}</strong> drafting and engineering environment developed by <strong>{vendor_name}</strong>. {tagline} {summary}
        </p>
        <div style="display: flex; gap: 16px; margin-top: 8px; flex-wrap: wrap;">
          <a href="../software/{sw_slug}.html" style="background: var(--ink-text); color: var(--ink-bg); padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 13.5px; transition: opacity 0.2s ease;">
            Explore {sw_name} Profile ›
          </a>
          <a href="../vendors/{vendor_slug}.html" style="background: transparent; color: var(--ink-text); border: 1px solid var(--ink-line); padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 13.5px; transition: background 0.2s ease;">
            About {vendor_name} ›
          </a>
        </div>
      </div>
    </section>
    """


def render_knowledge_tree(term: dict, software: dict, related_terms: list[str], all_terms_index: dict[str, str]) -> str:
    """Render a structured Tree Navigation mapping global, local, and sibling nodes."""
    sw_name = esc(software["name"])
    sw_slug = software["slug"]
    vendor_name = esc(software["vendor"]["name"])
    vendor_slug = software["vendor"]["slug"]
    title = esc(term["title"])
    
    if related_terms:
        items = []
        for s in related_terms:
            label = all_terms_index.get(s) or s.replace("-", " ").title()
            items.append(f'<a href="./{s}.html" style="color: var(--ink-text); text-decoration: underline; font-weight: 500;">{esc(label)}</a>')
        leaves = " · ".join(items)
    else:
        leaves = f'<span style="color: var(--ink-text-muted); font-style: italic;">Detailed sibling terms defined on the <a href="../software/{sw_slug}.html" style="color: var(--ink-text);">{sw_name} software page</a>.</span>'
        
    return f"""
    <section class="kb-concept-section" style="margin-top: 40px; border-top: 1px solid var(--ink-line); padding-top: 32px;">
      <div class="kb-tree-navigator" style="background: var(--ink-surface-1); border: 1px solid var(--ink-line); border-radius: 16px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);">
        <h3 style="margin-top: 0; margin-bottom: 20px; font-size: 1.25rem; color: var(--ink-text); display: flex; align-items: center; gap: 8px; font-weight: 700;">
          <span>🌳</span> CAD Knowledge Tree Navigation
        </h3>
        <div style="display: flex; flex-direction: column; gap: 16px; border-left: 2px dashed var(--ink-line); padding-left: 20px; margin-left: 10px;">
          
          <div class="kb-tree-level" style="position: relative;">
            <div style="position: absolute; left: -26px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--ink-text); border: 2px solid var(--ink-bg);"></div>
            <strong style="color: var(--ink-text); font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 4px;">Trunk (主干 — Global Foundations)</strong>
            <div style="font-size: 14.5px; color: var(--ink-text-soft);">
              <a href="../../knowledge-base.html" style="color: var(--ink-text); text-decoration: underline; font-weight: 500;">Wiki Home</a> · 
              <a href="../../kb-terms.html" style="color: var(--ink-text); text-decoration: underline; font-weight: 500;">Glossary Index</a> · 
              <a href="../../kb-graph.html" style="color: var(--ink-text); text-decoration: underline; font-weight: 500;">Interactive Graph</a>
            </div>
          </div>
          
          <div class="kb-tree-level" style="position: relative;">
            <div style="position: absolute; left: -26px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--ink-text); border: 2px solid var(--ink-bg);"></div>
            <strong style="color: var(--ink-text); font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 4px;">Branch (枝干 — Software &amp; Vendor)</strong>
            <div style="font-size: 14.5px; color: var(--ink-text-soft);">
              <a href="../software/{sw_slug}.html" style="color: var(--ink-text); text-decoration: underline; font-weight: 500;">{sw_name} Profile</a> · 
              <a href="../vendors/{vendor_slug}.html" style="color: var(--ink-text); text-decoration: underline; font-weight: 500;">{vendor_name} Ecosystem</a>
            </div>
          </div>
          
          <div class="kb-tree-level" style="position: relative;">
            <div style="position: absolute; left: -26px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--ink-focus); border: 2px solid var(--ink-bg);"></div>
            <strong style="color: var(--ink-text); font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 4px;">Leaf (树叶 — Current Node &amp; Sibling Terms)</strong>
            <div style="font-size: 14.5px; color: var(--ink-text-soft);">
              <span style="background: var(--ink-surface-2); color: var(--ink-text); padding: 2px 8px; border-radius: 4px; font-weight: 600; border: 1px solid var(--ink-line); font-size: 13.5px; display: inline-block; margin-bottom: 6px;">
                🍃 Active: {title}
              </span>
              <div style="margin-top: 4px;">
                {leaves}
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </section>
    """


def autolink_string(text: str, candidates: list[tuple[str, str]], linked: set[str]) -> str:
    """Recursively search and autolink the first occurrence of terms, avoiding nested tags."""
    if not text:
        return ""
    for name, url in candidates:
        if name in linked:
            continue
        escaped_name = re.escape(name)
        pattern = r'\b' + escaped_name + r'\b'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start, end = match.span()
            matched_str = text[start:end]
            link_html = f'<a href="{url}">{matched_str}</a>'
            linked.add(name)
            
            before = autolink_string(text[:start], candidates, linked)
            after = autolink_string(text[end:], candidates, linked)
            
            return before + link_html + after
    return text


def apply_autolinks(html_content: str, software_list: list[dict], all_terms_index: dict[str, str], current_slug: str) -> str:
    """Parse HTML content, separating tags and plain text, and apply link triggers securely.
    Only processes the <body> portion of the HTML to avoid corrupting <head> elements like title, meta, or script JSON-LD.
    """
    if "</head>" in html_content:
        head, body = html_content.split("</head>", 1)
    else:
        head = ""
        body = html_content

    candidates = []
    for sw in software_list:
        candidates.append((sw["name"], f"../software/{sw['slug']}.html"))
    for slug, title in all_terms_index.items():
        if slug != current_slug and len(title) >= 3:
            candidates.append((title, f"./{slug}.html"))
            
    candidates.sort(key=lambda x: len(x[0]), reverse=True)
    parts = re.split(r'(<[^>]+>)', body)
    
    linked = set()
    in_anchor = False
    
    for idx in range(len(parts)):
        part = parts[idx]
        if part.startswith('<'):
            tag_lower = part.lower()
            if '<a ' in tag_lower or '<a>' in tag_lower:
                in_anchor = True
            elif '</a>' in tag_lower:
                in_anchor = False
        else:
            if not in_anchor:
                parts[idx] = autolink_string(part, candidates, linked)
                
    body_linked = "".join(parts)
    if head:
        return head + "</head>" + body_linked
    return body_linked


def render_concept(term: dict, software: dict, editorial: dict, all_terms_index: dict[str, str]) -> str:
    """Render a single concept term HTML page."""
    title = term["title"]
    slug = term["slug"]
    url = f"{SITE_URL}/kb/concepts/{slug}.html"
    short = term.get("short_def", "")
    desc = term.get("meta_desc") or short or title
    reviewer = reviewer_jsonld(editorial, term.get("reviewer_id", software.get("default_reviewer_id", "lc-editorial")))
    last_reviewed = term.get("last_reviewed") or software.get("last_reviewed") or editorial["default_last_reviewed"]
    published = term.get("date_published") or last_reviewed

    article_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "url": url,
        "datePublished": published,
        "dateModified": last_reviewed,
        "inLanguage": "en",
        "isPartOf": {"@type": "WebSite", "name": "Gstarcademy", "url": SITE_URL},
        "mainEntityOfPage": url,
        **author_jsonld(editorial),
    }
    if reviewer:
        article_ld["reviewedBy"] = reviewer

    definedterm_ld = {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": title,
        "description": short or desc,
        "url": url,
        "inDefinedTermSet": {
            "@type": "DefinedTermSet",
            "name": "CAD Knowledge Base",
            "url": f"{SITE_URL}/kb-terms.html",
        },
    }

    bc = breadcrumb_jsonld([
        ("Home", f"{SITE_URL}/index.html"),
        ("Knowledge Base", f"{SITE_URL}/knowledge-base.html"),
        ("Terms", f"{SITE_URL}/kb-terms.html"),
        (title, url),
    ])

    # Related links
    related_terms = term.get("related_term_slugs") or []
    related_links_html = ""
    if related_terms:
        items = []
        for s in related_terms:
            label = all_terms_index.get(s) or s.replace("-", " ").title()
            items.append(f'<li><a href="./{s}.html">{esc(label)}</a></li>')
        related_links_html = f"""
        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Related concepts</h2>
          <ul class="ink-source-list">{''.join(items)}</ul>
        </section>"""

    # Sources
    sources = term.get("sources") or []
    sources_html = ""
    if sources:
        lis = "\n".join(
            f'<li><a href="{esc(s["url"])}" rel="noopener noreferrer nofollow" target="_blank">{esc(s["label"])}</a> · <span class="meta">{esc(s.get("publisher",""))}</span></li>'
            for s in sources
        )
        sources_html = f"""
        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Sources &amp; further reading</h2>
          <ul class="ink-source-list">{lis}</ul>
        </section>"""

    # Body sections
    body_parts = []
    if term.get("definition"):
        body_parts.append(f"""
        <section class="kb-concept-section">
          <h2>Definition</h2>
          {paragraphs(term['definition'])}
        </section>""")
    if term.get("why_matters"):
        body_parts.append(f"""
        <section class="kb-concept-section">
          <h2>Why it matters</h2>
          {paragraphs(term['why_matters'])}
        </section>""")
    if term.get("how_it_works"):
        body_parts.append(f"""
        <section class="kb-concept-section">
          <h2>How it works in practice</h2>
          {paragraphs(term['how_it_works'])}
        </section>""")
    if term.get("common_pitfalls"):
        if isinstance(term["common_pitfalls"], list):
            body_parts.append(f"""
        <section class="kb-concept-section">
          <h2>Common pitfalls</h2>
          {bullet_list(term['common_pitfalls'])}
        </section>""")
        else:
            body_parts.append(f"""
        <section class="kb-concept-section">
          <h2>Common pitfalls</h2>
          {paragraphs(term['common_pitfalls'])}
        </section>""")
    if term.get("learn_next"):
        body_parts.append(f"""
        <section class="kb-concept-section">
          <h2>What to learn next</h2>
          {paragraphs(term['learn_next'])}
        </section>""")

    sw_name = esc(software["name"])
    sw_slug = software["slug"]
    chip = f'<span class="chip pill-warn">Atomic Knowledge · {sw_name}</span>'

    byline = f"""<div class="ink-byline" role="contentinfo">
          <span><strong>By</strong> {esc(editorial['editorial_team'][0]['name'])}</span>
          <span><strong>Reviewed by</strong> {esc(reviewer['name']) if reviewer else 'Gstarcademy Editorial Team'}</span>
          <span><strong>Last reviewed</strong> <time datetime="{last_reviewed}">{last_reviewed}</time></span>
          <span><a href="../../about.html#editorial-process">Editorial process</a></span>
        </div>"""

    faq_accordion_html = render_faq_accordion(get_relevant_faqs(term, software), sw_name)
    spotlight_card_html = render_spotlight_card(software)
    knowledge_tree_html = render_knowledge_tree(term, software, related_terms, all_terms_index)

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(title)} · {sw_name} · CAD Knowledge Base · Gstarcademy</title>
    <meta name="description" content="{esc(desc)}" />
    <link rel="canonical" href="{url}" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    {open_graph(title, desc, url)}
    {fonts_block('../../')}
    <script type="application/ld+json">{json.dumps(article_ld, ensure_ascii=False, separators=(',', ':'))}</script>
    <script type="application/ld+json">{json.dumps(definedterm_ld, ensure_ascii=False, separators=(',', ':'))}</script>
    <script type="application/ld+json">{json.dumps(bc, ensure_ascii=False, separators=(',', ':'))}</script>
  </head>
  <body data-page="knowledge" class="page-kb-concepts">
    {topbar_html('../../')}

    <main class="container" style="margin-top: 32px; max-width: 920px;">
      <nav class="kb-faq-breadcrumbs" aria-label="Breadcrumb">
        <a href="../../index.html">Home</a> /
        <a href="../../knowledge-base.html">Knowledge Base</a> /
        <a href="../../kb-terms.html">Terms</a> /
        <a href="../software/{sw_slug}.html">{sw_name}</a> /
        <span aria-current="page">{esc(title)}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 28px;">
          {chip}
          <h1 style="margin-top: 12px;">{esc(title)}</h1>
          <p class="hero-sub">{esc(short)}</p>
        </header>

        {byline}

        {''.join(body_parts)}

        {spotlight_card_html}

        {faq_accordion_html}

        {knowledge_tree_html}

        {sources_html}

        <p class="meta" style="margin-top: 36px; font-size: 12px;">{esc(editorial['license_note'])}</p>
      </article>
    </main>

    {footer_html('../../')}
    <script src="../../app.js?v={CSS_VER}" defer></script>
  </body>
</html>
"""


def render_software_profile(sw: dict, editorial: dict, all_terms_index: dict[str, str]) -> str:
    """Render a deep software profile page."""
    name = sw["name"]
    slug = sw["slug"]
    url = f"{SITE_URL}/kb/software/{slug}.html"
    desc = sw.get("meta_desc") or sw.get("tagline") or name
    last_reviewed = sw.get("last_reviewed") or editorial["default_last_reviewed"]
    reviewer = reviewer_jsonld(editorial, sw.get("default_reviewer_id", "lc-editorial"))

    bc = breadcrumb_jsonld([
        ("Home", f"{SITE_URL}/index.html"),
        ("Knowledge Base", f"{SITE_URL}/knowledge-base.html"),
        ("Software", f"{SITE_URL}/kb-software.html"),
        (name, url),
    ])

    sw_ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "applicationCategory": sw.get("category_label", "DesignApplication"),
        "operatingSystem": ", ".join(sw.get("platforms", []) or ["Windows"]),
        "url": url,
        "description": desc,
        "brand": {"@type": "Brand", "name": sw["vendor"]["name"]},
    }
    article_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{name} — software profile, learning path, ecosystem",
        "description": desc,
        "url": url,
        "datePublished": sw.get("date_published") or last_reviewed,
        "dateModified": last_reviewed,
        "inLanguage": "en",
        "mainEntityOfPage": url,
        **author_jsonld(editorial),
    }
    if reviewer:
        article_ld["reviewedBy"] = reviewer

    profile = sw.get("profile", {})

    def section(title: str, key: str) -> str:
        body = profile.get(key)
        if not body:
            return ""
        return f"""
        <section class="kb-concept-section">
          <h2>{esc(title)}</h2>
          {paragraphs(body)}
        </section>"""

    learning_path_html = ""
    if profile.get("recommended_learning_path"):
        steps = "\n".join(
            f'<li><strong>{esc(step["stage"])}.</strong> {md_inline(step["focus"])}</li>'
            for step in profile["recommended_learning_path"]
        )
        learning_path_html = f"""
        <section class="kb-concept-section">
          <h2>Recommended learning path</h2>
          <ol class="ink-source-list">{steps}</ol>
        </section>"""

    fact_rows = []
    if sw.get("vendor"):
        fact_rows.append(("Vendor", f'<a href="../vendors/{sw["vendor"]["slug"]}.html">{esc(sw["vendor"]["name"])}</a>'))
    if sw.get("first_released"):
        fact_rows.append(("First released", esc(sw["first_released"])))
    if sw.get("current_track"):
        fact_rows.append(("Current release track", esc(sw["current_track"])))
    if sw.get("license_model"):
        fact_rows.append(("Licensing model", esc(sw["license_model"])))
    if sw.get("platforms"):
        fact_rows.append(("Platforms", ", ".join(esc(p) for p in sw["platforms"])))
    if sw.get("file_formats"):
        fact_rows.append(("Native / common formats", ", ".join(esc(f) for f in sw["file_formats"])))
    if sw.get("domains"):
        fact_rows.append(("Typical domains", ", ".join(esc(d) for d in sw["domains"])))
    if sw.get("primary_alternatives"):
        fact_rows.append(("Common alternatives", ", ".join(esc(a) for a in sw["primary_alternatives"])))

    fact_html = ""
    if fact_rows:
        rows = "\n".join(
            f'<tr><th scope="row" style="text-align:left; padding:8px 14px 8px 0; color:var(--ink-text-muted); font-weight:600; font-size:13px; vertical-align:top;">{k}</th><td style="padding:8px 0; color:var(--ink-text);">{v}</td></tr>'
            for k, v in fact_rows
        )
        fact_html = f"""
        <section class="kb-concept-section">
          <h2>At a glance</h2>
          <table style="width:100%; border-collapse: collapse; font-size:14.5px;">
            <tbody>{rows}</tbody>
          </table>
        </section>"""

    # Terms grid
    terms = sw.get("terms", [])
    terms_html = ""
    if terms:
        cards = "\n".join(
            f"""<a class="card" href="../concepts/{esc(t['slug'])}.html" style="display:block; padding:18px 20px;">
              <h3>{esc(t['title'])}</h3>
              <p class="meta">{esc(t.get('short_def', ''))}</p>
            </a>"""
            for t in terms
        )
        terms_html = f"""
        <section class="kb-concept-section">
          <h2>Core terminology &amp; workflows ({len(terms)})</h2>
          <p class="meta">Atomic concepts our editors broke out from official documentation and real practice. Each is a standalone, linkable definition with sources.</p>
          <div class="grid grid-2" style="gap:14px; margin-top:14px;">{cards}</div>
        </section>"""

    faqs = sw.get("faqs", [])
    faq_html = ""
    if faqs:
        items = "\n".join(
            f"""<details style="margin: 10px 0; padding: 14px 18px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 12px;">
              <summary style="cursor:pointer; font-weight:600; color: var(--ink-text);">{esc(q['question'])}</summary>
              <div style="margin-top:10px; color:var(--ink-text-soft);">{paragraphs(q['answer'])}</div>
            </details>"""
            for q in faqs
        )
        faq_html = f"""
        <section class="kb-concept-section">
          <h2>Frequently asked questions ({len(faqs)})</h2>
          {items}
          <p class="meta" style="margin-top:14px;"><a href="../../kb-faq.html#{slug}">All {name} FAQs ›</a></p>
        </section>"""

    sources = sw.get("sources", [])
    sources_html = ""
    if sources:
        lis = "\n".join(
            f'<li><a href="{esc(s["url"])}" rel="noopener noreferrer nofollow" target="_blank">{esc(s["label"])}</a> · <span class="meta">{esc(s.get("publisher",""))}</span></li>'
            for s in sources
        )
        sources_html = f"""
        <section class="kb-concept-section">
          <h2>Sources &amp; further reading</h2>
          <ul class="ink-source-list">{lis}</ul>
        </section>"""

    byline = f"""<div class="ink-byline">
      <span><strong>By</strong> {esc(editorial['editorial_team'][0]['name'])}</span>
      <span><strong>Reviewed by</strong> {esc(reviewer['name']) if reviewer else 'Gstarcademy Editorial Team'}</span>
      <span><strong>Last reviewed</strong> <time datetime="{last_reviewed}">{last_reviewed}</time></span>
      <span><a href="../../about.html#editorial-process">Editorial process</a></span>
    </div>"""

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(name)} — software profile, learning path, ecosystem · Gstarcademy</title>
    <meta name="description" content="{esc(desc)}" />
    <link rel="canonical" href="{url}" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    {open_graph(name + ' — software profile', desc, url)}
    {fonts_block('../../')}
    <script type="application/ld+json">{json.dumps(sw_ld, ensure_ascii=False, separators=(',', ':'))}</script>
    <script type="application/ld+json">{json.dumps(article_ld, ensure_ascii=False, separators=(',', ':'))}</script>
    <script type="application/ld+json">{json.dumps(bc, ensure_ascii=False, separators=(',', ':'))}</script>
  </head>
  <body data-page="knowledge" class="page-kb-software">
    {topbar_html('../../')}

    <main class="container" style="margin-top: 24px; max-width: 1100px;">
      <nav class="kb-faq-breadcrumbs" aria-label="Breadcrumb">
        <a href="../../index.html">Home</a> /
        <a href="../../knowledge-base.html">Knowledge Base</a> /
        <a href="../../kb-software.html">Software</a> /
        <span aria-current="page">{esc(name)}</span>
      </nav>

      <section class="hero hero-premium" style="margin-top: 20px;">
        <div class="hero-inner">
          <span class="eyebrow">Software profile · {esc(sw['vendor']['name'])}</span>
          <h1 class="hero-title">{esc(name)}</h1>
          <p class="hero-sub">{esc(sw.get('tagline', desc))}</p>
        </div>
      </section>

      <article class="kb-concept-detail">
        {byline}

        {fact_html}
        {section('What it is', 'what_it_is')}
        {section('Where it is used', 'where_used')}
        {section('Learning curve and getting started', 'learning_curve')}
        {section('Licensing reality', 'licensing_reality')}
        {section('Ecosystem and extensions', 'ecosystem')}
        {section('Common pitfalls and misconceptions', 'common_pitfalls')}
        {section('When to use vs. alternatives', 'when_to_use_vs_alternative')}
        {learning_path_html}

        {terms_html}
        {faq_html}
        {sources_html}

        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Continue exploring</h2>
          <ul class="ink-source-list">
            <li><a href="../vendors/{sw['vendor']['slug']}.html">{esc(sw['vendor']['name'])} — vendor profile</a></li>
            <li><a href="../../kb-graph.html">Open the {esc(name)} cluster in the knowledge graph</a></li>
            <li><a href="../../tutorials.html">Find tutorials on {esc(name)}</a></li>
            <li><a href="../../kb-terms.html">All CAD terms</a></li>
          </ul>
        </section>

        <p class="meta" style="margin-top: 28px; font-size: 12px;">{esc(editorial['license_note'])}</p>
      </article>
    </main>

    {footer_html('../../')}
    <script src="../../app.js?v={CSS_VER}" defer></script>
  </body>
</html>
"""


def render_vendor(vendor: dict, software_under_vendor: list[dict], editorial: dict) -> str:
    name = vendor["name"]
    slug = vendor["slug"]
    url = f"{SITE_URL}/kb/vendors/{slug}.html"
    desc = vendor.get("meta_desc") or vendor.get("tagline") or f"{name} — vendor profile, product portfolio, and ecosystem context."
    last_reviewed = vendor.get("last_reviewed") or editorial["default_last_reviewed"]
    reviewer = reviewer_jsonld(editorial, vendor.get("default_reviewer_id", "lc-editorial"))

    bc = breadcrumb_jsonld([
        ("Home", f"{SITE_URL}/index.html"),
        ("Knowledge Base", f"{SITE_URL}/knowledge-base.html"),
        ("Vendors", f"{SITE_URL}/kb-vendors.html"),
        (name, url),
    ])
    org_ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": name,
        "url": vendor.get("homepage", ""),
        "description": desc,
    }
    article_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{name} — vendor profile",
        "description": desc,
        "url": url,
        "datePublished": vendor.get("date_published") or last_reviewed,
        "dateModified": last_reviewed,
        "mainEntityOfPage": url,
        **author_jsonld(editorial),
    }
    if reviewer:
        article_ld["reviewedBy"] = reviewer

    profile = vendor.get("profile", {})

    def section(title: str, key: str) -> str:
        body = profile.get(key)
        if not body:
            return ""
        return f"""
        <section class="kb-concept-section">
          <h2>{esc(title)}</h2>
          {paragraphs(body)}
        </section>"""

    products_html = ""
    if software_under_vendor:
        cards = "\n".join(
            f"""<a class="card" href="../software/{esc(s['slug'])}.html" style="display:block; padding:18px 20px;">
              <h3>{esc(s['name'])}</h3>
              <p class="meta">{esc(s.get('tagline', ''))}</p>
            </a>"""
            for s in software_under_vendor
        )
        products_html = f"""
        <section class="kb-concept-section">
          <h2>Products in our knowledge base ({len(software_under_vendor)})</h2>
          <div class="grid grid-2" style="gap:14px; margin-top:14px;">{cards}</div>
        </section>"""

    sources = vendor.get("sources", [])
    sources_html = ""
    if sources:
        lis = "\n".join(
            f'<li><a href="{esc(s["url"])}" rel="noopener noreferrer nofollow" target="_blank">{esc(s["label"])}</a> · <span class="meta">{esc(s.get("publisher",""))}</span></li>'
            for s in sources
        )
        sources_html = f"""
        <section class="kb-concept-section">
          <h2>Sources</h2>
          <ul class="ink-source-list">{lis}</ul>
        </section>"""

    byline = f"""<div class="ink-byline">
      <span><strong>By</strong> {esc(editorial['editorial_team'][0]['name'])}</span>
      <span><strong>Reviewed by</strong> {esc(reviewer['name']) if reviewer else 'Gstarcademy Editorial Team'}</span>
      <span><strong>Last reviewed</strong> <time datetime="{last_reviewed}">{last_reviewed}</time></span>
      <span><a href="../../about.html#editorial-process">Editorial process</a></span>
    </div>"""

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(name)} — CAD vendor profile · Gstarcademy</title>
    <meta name="description" content="{esc(desc)}" />
    <link rel="canonical" href="{url}" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    {open_graph(name + ' — vendor profile', desc, url)}
    {fonts_block('../../')}
    <script type="application/ld+json">{json.dumps(org_ld, ensure_ascii=False, separators=(',', ':'))}</script>
    <script type="application/ld+json">{json.dumps(article_ld, ensure_ascii=False, separators=(',', ':'))}</script>
    <script type="application/ld+json">{json.dumps(bc, ensure_ascii=False, separators=(',', ':'))}</script>
  </head>
  <body data-page="knowledge" class="page-kb-vendors">
    {topbar_html('../../')}

    <main class="container" style="margin-top: 24px; max-width: 1080px;">
      <nav class="kb-faq-breadcrumbs" aria-label="Breadcrumb">
        <a href="../../index.html">Home</a> /
        <a href="../../knowledge-base.html">Knowledge Base</a> /
        <a href="../../kb-vendors.html">Vendors</a> /
        <span aria-current="page">{esc(name)}</span>
      </nav>

      <section class="hero hero-premium" style="margin-top: 20px;">
        <div class="hero-inner">
          <span class="eyebrow">Vendor profile</span>
          <h1 class="hero-title">{esc(name)}</h1>
          <p class="hero-sub">{esc(vendor.get('tagline', desc))}</p>
        </div>
      </section>

      <article class="kb-concept-detail">
        {byline}
        {section('Company snapshot', 'snapshot')}
        {section('Product portfolio', 'portfolio')}
        {section('Licensing &amp; subscription model', 'licensing')}
        {section('Ecosystem and partner network', 'ecosystem')}
        {section('Strategic position', 'positioning')}
        {section('What to watch', 'watchlist')}

        {products_html}
        {sources_html}

        <p class="meta" style="margin-top: 28px; font-size: 12px;">{esc(editorial['license_note'])}</p>
      </article>
    </main>

    {footer_html('../../')}
    <script src="../../app.js?v={CSS_VER}" defer></script>
  </body>
</html>
"""


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


# -- knowledge.js graph patch ---------------------------------------------

NODES_START = "  /* AUTO-GEN sw-nodes START */"
NODES_END = "  /* AUTO-GEN sw-nodes END */"
LINKS_START = "  /* AUTO-GEN sw-links START */"
LINKS_END = "  /* AUTO-GEN sw-links END */"


def patch_graph(software_list: list[dict]) -> None:
    """Inject software-derived graph nodes/links into knowledge.js.

    We append after the current `nodes = [` and `links = [` arrays.
    Idempotent via AUTO-GEN sentinels. Deduplicates against pre-existing
    node IDs in knowledge.js so D3 doesn't fail on duplicate identifiers.
    """
    kj = ROOT / "knowledge.js"
    text = kj.read_text(encoding="utf-8")

    # Discover pre-existing node IDs (everything before AUTO-GEN block) so we
    # don't inject duplicates that break the D3 force layout.
    pre_text = text.split(NODES_START)[0] if NODES_START in text else text
    existing_ids = set(re.findall(r'{\s*id:\s*"([^"]+)"', pre_text))

    # Build node + link lines
    seen_ids: set[str] = set(existing_ids)
    node_lines = []
    link_lines = []
    for sw in software_list:
        for n in sw.get("graph_nodes", []):
            nid = n["id"]
            if nid in seen_ids:
                continue
            seen_ids.add(nid)
            tags = " ".join(n.get("tags", []) or [])
            node_lines.append(
                "  { id: %s, type: %s, group: %d, radius: %d, tags: %s, hint: %s }," % (
                    json.dumps(nid, ensure_ascii=False),
                    json.dumps(n.get("type", "concept"), ensure_ascii=False),
                    int(n.get("group", 2)),
                    int(n.get("radius", 8)),
                    json.dumps(n.get("tags", []) or [], ensure_ascii=False),
                    json.dumps(n.get("hint", ""), ensure_ascii=False),
                )
            )
        for src, dst in sw.get("graph_links", []):
            link_lines.append(
                "  [%s, %s]," % (
                    json.dumps(src, ensure_ascii=False),
                    json.dumps(dst, ensure_ascii=False),
                )
            )

    nodes_block = NODES_START + "\n" + "\n".join(node_lines) + "\n  " + NODES_END
    links_block = LINKS_START + "\n" + "\n".join(link_lines) + "\n  " + LINKS_END

    # Insert / replace inside the nodes array
    # The current file has: const nodes = [ ... ];  and  const links = [ ... ];
    def upsert(block_text: str, start_marker: str, end_marker: str, after_pattern: str) -> str:
        if start_marker in block_text and end_marker in block_text:
            # replace in place
            pattern = re.compile(
                re.escape(start_marker) + r"[\s\S]*?" + re.escape(end_marker)
            )
            new = nodes_block if start_marker is NODES_START else links_block
            return pattern.sub(lambda _m: new, block_text)
        # else inject just before the closing `];` of the target array
        m = re.search(after_pattern, block_text)
        if not m:
            return block_text
        insert_at = m.start()
        new = nodes_block if start_marker is NODES_START else links_block
        return block_text[:insert_at] + new + "\n" + block_text[insert_at:]

    # nodes array closer pattern (first occurrence after `const nodes = [`)
    text = upsert(
        text, NODES_START, NODES_END,
        after_pattern=r"\n  \];\s*\n\s*const links\s*=\s*\[",
    )
    # links array closer pattern (first `];` after `const links = [`)
    text = upsert(
        text, LINKS_START, LINKS_END,
        after_pattern=r"\n  \];\s*\n\s*const beginnerPath",
    )

    kj.write_text(text, encoding="utf-8")


# -- kb-faq.html patch ---------------------------------------------------

FAQ_START = "<!-- AUTO-GEN sw-faqs START -->"
FAQ_END = "<!-- AUTO-GEN sw-faqs END -->"
TAB_START = "<!-- AUTO-GEN sw-faq-tabs START -->"
TAB_END = "<!-- AUTO-GEN sw-faq-tabs END -->"


def patch_faq(software_list: list[dict]) -> None:
    faq_path = ROOT / "kb-faq.html"
    text = faq_path.read_text(encoding="utf-8")

    SLUG_TO_TOPIC = {
        "creo-parametric": "creo",
        "siemens-nx": "siemens",
        "microstation": "bentley",
        "autocad": "autocad",
        "revit": "revit",
        "fusion-360": "fusion",
        "inventor": "inventor",
        "civil-3d": "civil3d",
        "solidworks": "solidworks",
        "catia": "catia",
        "gstarcad": "gstarcad",
        "draftsight": "draftsight",
    }
    
    EXISTING_TOPICS = {
        "gstarcad", "fastview", "autocad", "revit", "civil3d", "inventor",
        "fusion", "draftsight", "creo", "siemens", "bentley", "solidworks", "catia"
    }

    # 1. Generate FAQ articles
    articles = []
    for sw in software_list:
        if not sw.get("faqs"):
            continue
        topic = SLUG_TO_TOPIC.get(sw["slug"], sw["slug"])
        for q in sw["faqs"]:
            articles.append(
                f"""                <article class="kb-faq-entry" data-kb-faq-topic="{esc(topic)}">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>{esc(q['question'])}</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · {esc(sw['name'])} Technical Reference</p>
                    <div class="kb-faq-answer">
                      {q['answer']}
                    </div>
                  </div>
                </article>"""
            )
            
    faq_block = FAQ_START + "\n" + "\n".join(articles) + "\n\n                " + FAQ_END

    if FAQ_START in text and FAQ_END in text:
        pattern = re.compile(re.escape(FAQ_START) + r"[\s\S]*?" + re.escape(FAQ_END))
        text = pattern.sub(lambda _m: faq_block, text)

    # 2. Generate Tab Buttons
    tabs = []
    for sw in software_list:
        topic = SLUG_TO_TOPIC.get(sw["slug"], sw["slug"])
        if topic not in EXISTING_TOPICS:
            # Avoid duplicate tab filters
            if topic not in [re.search(r'data-kb-faq-filter="([^"]*)"', t).group(1) for t in tabs if re.search(r'data-kb-faq-filter="([^"]*)"', t)]:
                tabs.append(
                    f'                <button type="button" class="kb-faq-tab" role="tab" aria-selected="false" data-kb-faq-filter="{esc(topic)}">{esc(sw["name"])}</button>'
                )
    
    tab_block = TAB_START + "\n" + "\n".join(tabs) + "\n                " + TAB_END

    if TAB_START in text and TAB_END in text:
        pattern = re.compile(re.escape(TAB_START) + r"[\s\S]*?" + re.escape(TAB_END))
        text = pattern.sub(lambda _m: tab_block, text)

    # Also emit a FAQPage JSON-LD encompassing all software FAQs (one combined entity per software)
    faqpages_ld = []
    for sw in software_list:
        if not sw.get("faqs"):
            continue
        faqpages_ld.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "name": f"{sw['name']} FAQs",
            "url": f"{SITE_URL}/kb-faq.html#{sw['slug']}",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q["question"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": q["answer"],
                    },
                }
                for q in sw["faqs"]
            ],
        })

    ld_block = "<!-- AUTO-GEN faq-jsonld START -->\n"
    for ld in faqpages_ld:
        ld_block += '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(",", ":")) + "</script>\n"
    ld_block += "<!-- AUTO-GEN faq-jsonld END -->"

    if "<!-- AUTO-GEN faq-jsonld START -->" in text:
        pattern = re.compile(
            r"<!-- AUTO-GEN faq-jsonld START -->[\s\S]*?<!-- AUTO-GEN faq-jsonld END -->"
        )
        text = pattern.sub(lambda _m: ld_block, text)
    else:
        # Insert before </head>
        text = text.replace("</head>", ld_block + "\n  </head>", 1)

    faq_path.write_text(text, encoding="utf-8")


# -- kb-terms.html patch -------------------------------------------------

TERMS_START = "<!-- AUTO-GEN sw-terms-index START -->"
TERMS_END = "<!-- AUTO-GEN sw-terms-index END -->"


def patch_terms_index(software_list: list[dict]) -> None:
    path = ROOT / "kb-terms.html"
    text = path.read_text(encoding="utf-8")

    # Aggregate all terms across software, group alphabetically
    rows: dict[str, list[tuple[str, str, str]]] = {}
    for sw in software_list:
        for t in sw.get("terms", []):
            initial = t["title"][0].upper()
            rows.setdefault(initial, []).append(
                (t["title"], t["slug"], sw["name"])
            )

    sections = []
    for letter in sorted(rows):
        items = sorted(rows[letter], key=lambda x: x[0].lower())
        lis = "\n".join(
            f'<li><a href="./kb/concepts/{esc(slug)}.html"><strong>{esc(title)}</strong></a> <span class="meta" style="font-size:12px;">({esc(swname)})</span></li>'
            for (title, slug, swname) in items
        )
        sections.append(
            f"""<section class="section" id="letter-{letter}" style="padding-top:8px;">
          <div class="section-head"><h2 class="section-title">{letter}</h2></div>
          <ul style="list-style:none; padding:0; margin:0; display:grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px 24px;">{lis}</ul>
        </section>"""
        )

    wrapper = (
        f'<section class="section" id="auto-generated-terms" style="margin-top: 56px;">\n'
        f'          <div class="section-head"><h2 class="section-title">Software-specific terminology</h2>'
        f'<span class="section-note">{sum(len(v) for v in rows.values())} terms · authored & reviewed by Gstarcademy editors</span></div>\n'
        f'          <p class="meta" style="margin-bottom: 18px;">Atomic concepts broken out per CAD product family. Each links to a dedicated page with definition, why-it-matters, common pitfalls, and sources.</p>\n'
        f"{chr(10).join(sections)}\n"
        f"        </section>"
    )
    block = TERMS_START + "\n" + wrapper + "\n        " + TERMS_END

    if TERMS_START in text and TERMS_END in text:
        pattern = re.compile(re.escape(TERMS_START) + r"[\s\S]*?" + re.escape(TERMS_END))
        text = pattern.sub(lambda _m: block, text)
    else:
        # Inject before the kb-main closing div
        anchor = '</div> <!-- End kb-main -->'
        if anchor in text:
            text = text.replace(anchor, block + "\n        " + anchor, 1)
        else:
            m = re.search(r"</main>", text)
            if m:
                text = text[: m.start()] + "      " + block + "\n    " + text[m.start():]

    path.write_text(text, encoding="utf-8")


# -- sitemap.xml patch ---------------------------------------------------

SITEMAP_START = "<!-- AUTO-GEN sw-sitemap START -->"
SITEMAP_END = "<!-- AUTO-GEN sw-sitemap END -->"


def patch_sitemap(software_list: list[dict]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")

    urls = []
    for sw in software_list:
        urls.append(f"{SITE_URL}/kb/software/{sw['slug']}.html")
        urls.append(f"{SITE_URL}/kb/vendors/{sw['vendor']['slug']}.html")
        for t in sw.get("terms", []):
            urls.append(f"{SITE_URL}/kb/concepts/{t['slug']}.html")
    urls = sorted(set(urls))

    entries = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n  </url>"
        for u in urls
    )
    block = SITEMAP_START + "\n" + entries + "\n  " + SITEMAP_END

    if SITEMAP_START in text and SITEMAP_END in text:
        pattern = re.compile(re.escape(SITEMAP_START) + r"[\s\S]*?" + re.escape(SITEMAP_END))
        text = pattern.sub(lambda _m: block, text)
    else:
        text = text.replace("</urlset>", "  " + block + "\n</urlset>", 1)

    path.write_text(text, encoding="utf-8")


# -- driver --------------------------------------------------------------

def main() -> int:
    editorial = json.loads(EDITORIAL_PATH.read_text(encoding="utf-8"))

    software_files = sorted(DATA_DIR.glob("*.json"))
    if not software_files:
        print("No software JSON found in data/sw/. Nothing to do.")
        return 0

    software_list: list[dict] = []
    for f in software_files:
        software_list.append(json.loads(f.read_text(encoding="utf-8")))

    # Build a global title index for cross-linking
    all_terms_index: dict[str, str] = {}
    for sw in software_list:
        for t in sw.get("terms", []):
            all_terms_index[t["slug"]] = t["title"]

    # Render concept pages
    written_terms = 0
    for sw in software_list:
        for t in sw.get("terms", []):
            page = render_concept(t, sw, editorial, all_terms_index)
            page = apply_autolinks(page, software_list, all_terms_index, t["slug"])
            out = CONCEPTS_DIR / f"{t['slug']}.html"
            if write_if_changed(out, page):
                written_terms += 1

    # Render software profile pages
    written_sw = 0
    for sw in software_list:
        page = render_software_profile(sw, editorial, all_terms_index)
        out = SOFTWARE_DIR / f"{sw['slug']}.html"
        if write_if_changed(out, page):
            written_sw += 1

    # Render vendor pages
    by_vendor: dict[str, list[dict]] = {}
    vendor_data: dict[str, dict] = {}
    for sw in software_list:
        v = sw["vendor"]
        by_vendor.setdefault(v["slug"], []).append(sw)
        if "profile" in v:
            vendor_data[v["slug"]] = v
    written_v = 0
    for vslug, vsw in by_vendor.items():
        vdata = vendor_data.get(vslug) or {
            "slug": vslug,
            "name": vsw[0]["vendor"]["name"],
            "tagline": vsw[0]["vendor"].get("name", ""),
            "profile": {},
        }
        if "name" not in vdata:
            vdata["name"] = vsw[0]["vendor"]["name"]
        page = render_vendor(vdata, vsw, editorial)
        out = VENDORS_DIR / f"{vslug}.html"
        if write_if_changed(out, page):
            written_v += 1

    # Patch shared files
    patch_graph(software_list)
    patch_faq(software_list)
    patch_terms_index(software_list)
    patch_sitemap(software_list)

    print(
        f"Rendered: {written_terms} concept pages, {written_sw} software profiles, "
        f"{written_v} vendor pages. Patched: knowledge.js, kb-faq.html, kb-terms.html, sitemap.xml."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
