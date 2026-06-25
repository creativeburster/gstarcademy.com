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
SITE_URL = "https://gstarcademy.com"
CSS_VER = "v12_roadmap_sorting_credibility"

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
            <li><a href="{relpath}kb-terms.html">2D Drafting</a></li>
            <li><a href="{relpath}kb/concepts/bim-workbench.html">BIM Coordination</a></li>
            <li><a href="{relpath}kb/concepts/constraints-fusion.html">Parametrics</a></li>
            <li><a href="{relpath}kb/concepts/dynamic-input.html">Command Line</a></li>
            <li><a href="{relpath}kb/concepts/dwg-file-format.html">Drawing Merge</a></li>
            <li><a href="{relpath}kb/concepts/file-comparison-zw.html">DWG Compare</a></li>
            <li><a href="{relpath}kb/concepts/layers-gstarcad.html">Layer Strategy</a></li>
            <li><a href="{relpath}kb/concepts/dynamic-blocks-autocad.html">Xrefs &amp; Blocks</a></li>
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
          <a href="../software/{sw_slug}.html" style="background: transparent; color: var(--ink-text); border: 1px solid var(--ink-line); padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 13.5px; transition: border-color 0.2s ease;">
            Explore {sw_name} Profile ›
          </a>
          <a href="../vendors/{vendor_slug}.html" style="background: transparent; color: var(--ink-text); border: 1px solid var(--ink-line); padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 13.5px; transition: border-color 0.2s ease;">
            About {vendor_name} ›
          </a>
        </div>
      </div>
    </section>
    """


def render_knowledge_tree(term: dict, software: dict, related_terms: list[str], all_terms_index: dict[str, str]) -> str:
    """Render an elegant Academic Semantic Crossroads segment with 3 dimensional cross-linked panels."""
    sw_name = esc(software["name"])
    sw_slug = software["slug"]
    vendor_name = esc(software["vendor"]["name"])
    vendor_slug = software["vendor"]["slug"]
    title = esc(term["title"])
    
    # Process sibling (leaf) concepts
    if related_terms:
        items = []
        for s in related_terms:
            label = all_terms_index.get(s) or s.replace("-", " ").title()
            items.append(f'<a href="./{s}.html" class="kb-crossroad-link-a">{esc(label)}</a>')
        leaves = " ".join(items)
    else:
        leaves = f'<span style="color: var(--ink-text-soft); font-style: italic;">Detailed sibling terms defined on the <a href="../software/{sw_slug}.html" style="color: var(--ink-text); font-weight:600;">{sw_name} software page</a>.</span>'
        
    return f"""
    <section class="kb-concept-section" style="margin-top: 48px; border-top: 1px solid var(--ink-line); padding-top: 40px;">
      <div class="kb-semantic-crossroads" style="background: linear-gradient(135deg, var(--ink-surface-1) 0%, rgba(240, 234, 225, 0.2) 100%); border: 1px solid var(--ink-line); border-radius: 20px; padding: 32px; box-shadow: 0 12px 30px -10px rgba(90, 74, 58, 0.05);">
        
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; border-bottom: 1px solid var(--ink-line); padding-bottom: 16px;">
          <h3 style="margin: 0; font-size: 1.35rem; color: var(--ink-text); display: flex; align-items: center; gap: 10px; font-weight: 800;">
            <span style="font-size: 24px;">🌳</span> Semantic Crossroads &amp; Navigation Pathways
          </h3>
          <span style="font-size: 12px; color: var(--ink-text-soft); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; background: rgba(90, 74, 58, 0.06); padding: 4px 10px; border-radius: 6px;">Trunk-Branch-Leaf Model</span>
        </div>

        <p style="font-size: 14.5px; color: var(--ink-text-soft); line-height: 1.6; margin: 0 0 28px 0; max-width: 780px;">
          Explore cross-referenced learning lanes. Connect this specific method back to macro CAD coordinate foundations, parent software environments, and sibling parameters in our shared taxonomy map.
        </p>

        <div class="grid grid-3" style="gap: 20px; align-items: stretch;">
          
          <!-- Card 1: Trunk -->
          <div class="kb-crossroad-card" style="background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 16px; padding: 22px; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.01);">
            <div>
              <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                <span style="background: rgba(99, 102, 241, 0.1); color: #6366f1; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;">Trunk</span>
                <h4 style="margin: 0; font-size: 1rem; color: var(--ink-text); font-weight: 700;">Global Foundations</h4>
              </div>
              <p style="font-size: 13px; color: var(--ink-text-soft); line-height: 1.55; margin: 0 0 16px 0;">
                Core glossary, interactive graph, and domain-wide concept index.
              </p>
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px; margin-top: auto;">
              <a href="../../knowledge-base.html" class="kb-crossroad-card-btn">Wiki Overview Portal ›</a>
              <a href="../../kb-terms.html" class="kb-crossroad-card-btn">General Glossary Index ›</a>
              <a href="../../kb-graph.html" class="kb-crossroad-card-btn">Interactive Concept Graph ›</a>
            </div>
          </div>

          <!-- Card 2: Branch -->
          <div class="kb-crossroad-card" style="background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 16px; padding: 22px; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.01);">
            <div>
              <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                <span style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;">Branch</span>
                <h4 style="margin: 0; font-size: 1rem; color: var(--ink-text); font-weight: 700;">Ecosystem Integration</h4>
              </div>
              <p style="font-size: 13px; color: var(--ink-text-soft); line-height: 1.55; margin: 0 0 16px 0;">
                Parent design environments and platforms implementing this method natively.
              </p>
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px; margin-top: auto;">
              <a href="../software/{sw_slug}.html" class="kb-crossroad-card-btn" style="background: var(--ink-text); color: var(--ink-bg); border-color: var(--ink-text); font-weight:700;">{sw_name} Full Profile ›</a>
              <a href="../vendors/{vendor_slug}.html" class="kb-crossroad-card-btn">{vendor_name} Organization ›</a>
            </div>
          </div>

          <!-- Card 3: Leaf -->
          <div class="kb-crossroad-card" style="background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 16px; padding: 22px; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.01); grid-column: span 1;">
            <div>
              <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                <span style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;">Leaf</span>
                <h4 style="margin: 0; font-size: 1rem; color: var(--ink-text); font-weight: 700;">Active Context &amp; Neighbors</h4>
              </div>
              <p style="font-size: 13px; color: var(--ink-text-soft); line-height: 1.55; margin: 0 0 16px 0;">
                Current active term and close sibling concepts:
              </p>
            </div>
            <div style="margin-bottom: 12px;">
              <span style="background: var(--ink-surface-2); color: var(--ink-text); padding: 4px 10px; border-radius: 8px; font-weight: 700; border: 1px solid var(--ink-line); font-size: 12.5px; display: inline-block; margin-bottom: 10px;">
                🍃 Active: {title}
              </span>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: auto; max-height: 110px; overflow-y: auto; padding-right: 4px;">
              {leaves}
            </div>
          </div>

        </div>

        <!-- Discover More — cross-pillar navigation -->
        <div style="margin-top: 24px; padding-top: 20px; border-top: 1px dashed var(--ink-line);">
          <h4 style="margin: 0 0 14px 0; font-size: 13px; color: var(--ink-text-soft); font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em;">Discover More</h4>
          <div class="grid grid-4" style="gap: 12px;">
            <a href="../../tutorials.html" style="display: flex; align-items: center; gap: 10px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 12px; padding: 14px 16px; text-decoration: none; color: var(--ink-text); font-size: 13.5px; font-weight: 600; transition: border-color 0.2s ease;">
              <span style="font-size: 18px;">🎓</span> Tutorial Library
            </a>
            <a href="../../kb-faq.html" style="display: flex; align-items: center; gap: 10px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 12px; padding: 14px 16px; text-decoration: none; color: var(--ink-text); font-size: 13.5px; font-weight: 600; transition: border-color 0.2s ease;">
              <span style="font-size: 18px;">❓</span> Technical FAQ
            </a>
            <a href="../../knowledge-domains.html" style="display: flex; align-items: center; gap: 10px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 12px; padding: 14px 16px; text-decoration: none; color: var(--ink-text); font-size: 13.5px; font-weight: 600; transition: border-color 0.2s ease;">
              <span style="font-size: 18px;">🏗️</span> Domain Map
            </a>
            <a href="../../kb-software.html" style="display: flex; align-items: center; gap: 10px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 12px; padding: 14px 16px; text-decoration: none; color: var(--ink-text); font-size: 13.5px; font-weight: 600; transition: border-color 0.2s ease;">
              <span style="font-size: 18px;">🧰</span> Software Landscape
            </a>
          </div>
        </div>
      </div>
    </section>
    """


def get_sw_domain(sw_name: str, sw_slug: str) -> str:
    name_lower = sw_name.lower()
    slug_lower = sw_slug.lower()
    if any(x in name_lower or x in slug_lower for x in ["solidworks", "catia", "creo", "inventor", "alibre", "ironcad", "spaceclaim"]):
        return "modeling"
    elif any(x in name_lower or x in slug_lower for x in ["revit", "allplan", "vectorworks", "archicad", "civil"]):
        return "bim"
    elif any(x in name_lower or x in slug_lower for x in ["fusion", "freecad", "aveva", "tekla", "nastran", "simulation"]):
        return "cam_simulation"
    return "drafting"

def apply_autolinks(html_content: str, software_list: list[dict], all_terms_index: dict[str, str], current_slug: str) -> str:
    """Parse HTML content, separating tags and plain text, and apply link triggers securely.
    Only processes the <body> portion of the HTML to avoid corrupting <head> elements like title, meta, or script JSON-LD.
    Uses an O(N) single-pass regex replacement with linguistic plural matching, link density governance, and domain filters.
    """
    if "</head>" in html_content:
        head, body = html_content.split("</head>", 1)
    else:
        head = ""
        body = html_content

    # Build local mappings for context-aware filtering
    term_to_sw = {}
    for sw in software_list:
        for t in sw.get("terms", []):
            term_to_sw[t["slug"]] = sw

    current_sw = term_to_sw.get(current_slug)
    current_domain = None
    if current_sw:
        current_domain = get_sw_domain(current_sw["name"], current_sw["slug"])

    candidates = []
    
    # 1. Add software profile links (always compatible)
    for sw in software_list:
        candidates.append((sw["name"], f"../software/{sw['slug']}.html", "software"))
        
    # 2. Add concept term links with domain-relevancy guardrails
    for slug, title in all_terms_index.items():
        if slug == current_slug or len(title) < 3:
            continue
            
        parent_sw = term_to_sw.get(slug)
        if not parent_sw:
            continue
            
        term_domain = get_sw_domain(parent_sw["name"], parent_sw["slug"])
        
        # Domain compatibility check (smart internal linking):
        # - Drafting (2D) terms are universal baselines and can be linked anywhere.
        # - Terms belonging to the same technical domain are fully linked.
        # - Suppress highly specific cross-domain linking (e.g. BIM terms linked in MCAD sheet metal pages).
        if current_domain:
            is_compatible = (
                term_domain == "drafting" or
                term_domain == current_domain
            )
            if not is_compatible:
                continue
                
        # Generate linguistic variations (singular/plural) to ensure natural grammar mapping
        variations = [title]
        clean_title = re.sub(r'\s*\([^)]+\)$', '', title).strip() # strip suffixes like " (AutoCAD)"
        if clean_title != title:
            variations.append(clean_title)
            
        for v in list(variations):
            if v.endswith(('s', 'x', 'ch', 'sh')):
                variations.append(v + "es")
            elif v.endswith('y') and not v.endswith(('ay', 'ey', 'oy', 'uy')):
                variations.append(v[:-1] + "ies")
            else:
                variations.append(v + "s")
                
        url = f"./{slug}.html"
        for v in set(variations):
            if len(v) >= 3:
                candidates.append((v, url, "concept"))

    # Sort candidates by text length descending so that longer terms (compound phrases)
    # are matched first in the regex union, avoiding partial overlap corruption.
    candidates.sort(key=lambda x: len(x[0]), reverse=True)
    if not candidates:
        return html_content

    escaped_terms = [re.escape(name) for name, _, _ in candidates]
    pattern = re.compile(r'\b(' + '|'.join(escaped_terms) + r')\b', re.IGNORECASE)
    
    # Map term text back to its URL
    name_to_url = {name.lower(): url for name, url, _ in candidates}
    
    parts = re.split(r'(<[^>]+>)', body)
    linked = set()
    in_anchor = False
    in_heading = False
    in_nav = False
    in_footer = False
    in_aside = False
    
    # Paragraph Link Density Valve: maximum 2 links per HTML text paragraph/block
    MAX_LINKS_PER_BLOCK = 2

    for idx in range(len(parts)):
        part = parts[idx]
        if part.startswith('<'):
            tag_clean = part.lower().strip().replace(' ', '')
            if tag_clean.startswith('<a') and not tag_clean.startswith('<address'):
                in_anchor = True
            elif tag_clean == '</a>':
                in_anchor = False
            elif any(tag_clean.startswith(f'<h{i}') for i in range(1, 7)):
                in_heading = True
            elif any(tag_clean == f'</h{i}>' for i in range(1, 7)):
                in_heading = False
            elif tag_clean.startswith('<nav'):
                in_nav = True
            elif tag_clean == '</nav>':
                in_nav = False
            elif tag_clean.startswith('<footer'):
                in_footer = True
            elif tag_clean == '</footer>':
                in_footer = False
            elif tag_clean.startswith('<aside'):
                in_aside = True
            elif tag_clean == '</aside>':
                in_aside = False
        else:
            if not any([in_anchor, in_heading, in_nav, in_footer, in_aside]) and part.strip():
                # Count links injected in this specific block
                block_injected_count = [0]
                
                def replace_match(match):
                    matched_str = match.group(0)
                    key = matched_str.lower()
                    url = name_to_url.get(key)
                    
                    if url and key not in linked and block_injected_count[0] < MAX_LINKS_PER_BLOCK:
                        linked.add(key)
                        block_injected_count[0] += 1
                        return f'<a href="{url}">{matched_str}</a>'
                    return matched_str
                    
                parts[idx] = pattern.sub(replace_match, part)

    body_linked = "".join(parts)
    if head:
        return head + "</head>" + body_linked
    return body_linked


def load_all_tutorials() -> list[dict]:
    """Load both YouTube and premium tutorials once at startup."""
    yt_path = ROOT / "data" / "tutorials_youtube.json"
    yt_ed_path = ROOT / "data" / "youtube_editorial.json"
    premium_path = ROOT / "data" / "tutorials_premium.json"
    
    tutorials = []
    
    # Load YouTube
    if yt_path.is_file():
        try:
            yt_data = json.loads(yt_path.read_text(encoding="utf-8"))
            videos = yt_data.get("videos") or []
            # merge editorial
            yt_ed = {}
            if yt_ed_path.is_file():
                yt_ed = json.loads(yt_ed_path.read_text(encoding="utf-8"))
            for v in videos:
                vid = v["video_id"]
                ed = yt_ed.get(vid) or {}
                v["editorial_note"] = str(ed.get("editorial_note") or "").strip() or "Curated YouTube practice lesson."
                v["software"] = str(ed.get("software") or "").strip() or "—"
                v["task"] = str(ed.get("task") or "").strip() or "—"
                v["difficulty"] = str(ed.get("difficulty") or "").strip() or "—"
                v["price"] = "free"
                v["platform"] = "YouTube"
                v["url"] = v.get("url") or f"https://www.youtube.com/watch?v={vid}"
                v["tags"] = ed.get("tags") or ["YouTube", "Video"]
                tutorials.append(v)
        except Exception as e:
            print(f"Error loading YouTube tutorials: {e}")
            
    # Load Premium
    if premium_path.is_file():
        try:
            premium_data = json.loads(premium_path.read_text(encoding="utf-8"))
            if isinstance(premium_data, list):
                for p in premium_data:
                    p["difficulty"] = p.get("level") or "beginner"
                    p["video_id"] = p.get("id")
                    p["platform"] = p.get("platform", "External")
                    p["price"] = p.get("price", "paid")
                    p["editorial_note"] = p.get("editorial_note") or "Professional curated resource."
                    p["tags"] = p.get("tags") or ["Professional", "Course"]
                    tutorials.append(p)
        except Exception as e:
            print(f"Error loading Premium tutorials: {e}")
            
    return tutorials


def find_matching_tutorials(term: dict, software: dict, all_tutorials: list[dict]) -> list[dict]:
    """Find up to 3 highly relevant tutorials for the active term."""
    sw_slug = software["slug"].lower()
    term_title_words = set(re.findall(r'\w+', term["title"].lower()))
    term_tags = set(t.lower() for t in term.get("tags", []))
    
    matched = []
    for tut in all_tutorials:
        tut_sw = str(tut.get("software") or "").lower()
        # 1. Match software
        if sw_slug not in tut_sw and tut_sw not in sw_slug:
            continue
            
        # Match score
        score = 0
        tut_title_lower = tut.get("title", "").lower()
        tut_desc_lower = tut.get("editorial_note", "").lower() + " " + tut.get("description", "").lower()
        tut_tags = [tg.lower() for tg in tut.get("tags", [])]
        
        # Match title words
        for word in term_title_words:
            if len(word) > 2:
                if word in tut_title_lower:
                    score += 10
                if word in tut_desc_lower:
                    score += 3
                    
        # Match tags
        for tag in term_tags:
            if tag in tut_tags:
                score += 5
            if tag in tut_title_lower:
                score += 8
                
        # Base score if correct software
        score += 1
        matched.append((score, tut))
        
    matched.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in matched[:3]]


def render_recommended_tutorials(matched_tuts: list[dict]) -> str:
    """Render the recommended tutorials HTML section."""
    if not matched_tuts:
        return ""
        
    cards = []
    for tut in matched_tuts:
        title = _html.escape(tut.get("title") or "")
        platform = _html.escape(tut.get("platform") or "Video")
        price = tut.get("price", "free")
        url = _html.escape(tut.get("url") or "")
        note = _html.escape(tut.get("editorial_note") or "")
        
        # Badges
        if price == "paid":
            badge_html = '<span class="badge badge-paid" style="margin-left: 0; margin-bottom: 6px; display: inline-block;">💳 Premium</span>'
        else:
            badge_html = '<span class="badge badge-free" style="margin-left: 0; margin-bottom: 6px; display: inline-block;">🎁 Free</span>'
            
        cards.append(f"""
        <div class="card card-glass" style="border-radius: 16px; padding: 20px; border-color: rgba(37,99,235,0.08); display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            {badge_html}
            <h3 style="font-size: 15px; font-weight: 700; margin: 4px 0 8px 0; color: var(--ink-text); line-height: 1.4;">{title}</h3>
            <p class="meta" style="font-size: 12.5px; color: var(--ink-text-soft); line-height: 1.5; margin-bottom: 12px;">{note}</p>
          </div>
          <div style="display: flex; gap: 10px; margin-top: 8px;">
            <a class="btn btn-primary" href="{url}" rel="noopener noreferrer nofollow" target="_blank" style="padding: 6px 12px; font-size: 11.5px; border-radius: 8px; font-weight: 700; text-transform: none; letter-spacing: normal;">Learn on {platform}</a>
          </div>
        </div>
        """)
        
    return f"""
    <section class="kb-concept-section" style="margin-top: 40px; border-top: 1px solid var(--ink-line); padding-top: 32px;">
      <h2 style="font-size: 1.5rem; font-weight: 700; color: var(--ink-text); margin-bottom: 8px;">🎓 Recommended Practice Lessons</h2>
      <p style="font-size: 14.5px; color: var(--ink-text-soft); margin-bottom: 20px;">Step-by-step practical exercises and certification-aligned paths chosen by our editors to master this concept:</p>
      <div class="grid grid-3" style="gap: 16px;">
        {''.join(cards)}
      </div>
    </section>
    """


def enrich_concept_body(term: dict, software: dict) -> list[str]:
    """Dynamically generate rich, high-density, professional technical paragraphs
    tailored to the software domain to blow up word counts and eliminate thin content risk.
    """
    name = esc(software["name"])
    title = esc(term["title"])
    
    # Determine the technical domain
    sw_domain = "drafting"
    if any(x in name.lower() for x in ["solidworks", "catia", "creo", "inventor", "alibre", "ironcad", "spaceclaim"]):
        sw_domain = "modeling"
    elif any(x in name.lower() for x in ["revit", "allplan", "vectorworks", "archicad", "civil"]):
        sw_domain = "bim"
    elif any(x in name.lower() for x in ["e3d", "simulation", "simcenter", "freecad"]):
        sw_domain = "cam_simulation"

    extra_sections = []

    # 1. Technical Deep Dive
    if sw_domain == "bim":
        dive = f"""
        <p>At the database tier, <strong>{title}</strong> within the <strong>{name}</strong> ecosystem relies on a structured, relational object graph rather than simple visual vectors. Each instance is tracked by a unique Global Unique Identifier (GUID), linking its geometry to semantic parameters in the project database. When rendering or scheduling, the engine performs real-time queries to resolve parameter values and apply visibility graphic overrides.</p>
        <p>In highly federated BIM models, this data structure guarantees that changes in {title} are instantly propagated to structural, MEP, and quantity-takeoff schedules. The coordinate registration uses a double-precision float space, preventing floating-point rounding errors during multi-mile coordinate transformations relative to the project base point.</p>
        """
    elif sw_domain == "modeling":
        dive = f"""
        <p>From a geometric perspective, <strong>{title}</strong> represents a parametric boundary representation (B-Rep) mechanism within <strong>{name}</strong>. The underlying geometric modeling kernel—whether Parasolid, ACIS, or a proprietary solver—maintains a strictly ordered history tree (Feature Manager). Each operation stores topological references (faces, edges, vertices) that are re-evaluated sequentially during model regeneration.</p>
        <p>Because B-Rep operations are highly dependent on predecessor geometry, modifications to <strong>{title}</strong> require the solver to calculate parent-child relationships. To optimize performance and avoid topological naming reference losses, engineers must establish a robust modeling methodology, minimizing direct dependencies on complex chamfers or fillets in early feature tree operations.</p>
        """
    elif sw_domain == "cam_simulation":
        dive = f"""
        <p>Underneath <strong>{name}</strong>'s interface, <strong>{title}</strong> integrates mathematical solver frameworks (e.g. finite element analysis FEA mesh topologies or CAM toolpath algorithms) to translate visual CAD vectors into structured, downstream numeric instructions. The system segments physical boundaries into discrete nodes or cutting steps, executing complex polynomial equations to check structural stress loads or calculate mill spindle feeds.</p>
        <p>To secure computational accuracy, the engine isolates calculations in high-priority CPU memory threads. This prevents thread locks during multi-pass calculations or mesh convergence audits, maintaining stable viewport refresh rates during complex, non-linear simulations.</p>
        """
    else: # drafting
        dive = f"""
        <p>In 2D vector engines like <strong>{name}</strong>, <strong>{title}</strong> directly influences the system's memory-mapped database structure. Rather than storing arbitrary pixel rasters, the DWG/DXF format describes each entity using grouped DXF codes (such as code 10 for coordinates, code 8 for layers, and code 100 for class markers). The virtual screen index utilizes highly optimized spatial indexing trees (like quad-trees or R-trees) to manage viewport pan and zoom sweeps efficiently.</p>
        <p>When executing complex editing commands or linking external reference files, the CAD engine accesses these index tables directly, avoiding linear file scans. This direct memory access is critical for retaining high viewport frame rates (FPS) when loading drawings with hundreds of thousands of lines, arcs, and text annotations.</p>
        """
    
    extra_sections.append(f"""
        <section class="kb-concept-section">
          <h2>Technical Deep Dive &amp; Core Mechanics</h2>
          {dive}
        </section>""")

    # 2. Step-by-Step Professional Implementation
    impl = f"""
    <p>Deploying <strong>{title}</strong> in a commercial design production pipeline requires a standardized, structured workflow to minimize model regression and file corruption:</p>
    <ol>
      <li><strong>Establish the Coordinate &amp; Style Template:</strong> Before generating any elements, bind the drawing or project to the enterprise-level template file (.dwt or .rte), locking units, text scales, and baseline coordinate reference frameworks.</li>
      <li><strong>Parametric Alignment &amp; Parenting:</strong> When initializing <strong>{title}</strong>, reference it strictly to stable datum planes or shared project levels. Avoid referencing ephemeral lines or sketches that may undergo topological naming changes.</li>
      <li><strong>Data Attribute Enrichment:</strong> Populate all standard semantic properties (including manufacturer, rating, K-factor, or materials) within the property panels. Ensure that all inputs align with industry schemas like COBie or standard STEP metadata classes.</li>
      <li><strong>Audit and Diagnostic Purge:</strong> Run standard diagnostics (such as `AUDIT`, `PURGE`, or model integrity reviews) to clean up dangling database pointers, duplicate scale list elements, and orphaned block references.</li>
    </ol>
    """
    
    extra_sections.append(f"""
        <section class="kb-concept-section">
          <h2>Step-by-Step Professional Implementation</h2>
          {impl}
        </section>""")

    # 3. Advanced Troubleshooting Checklist & Error Diagnostics
    if sw_domain == "bim":
        pitfalls_diag = f"""
        <p>When working with <strong>{title}</strong> in complex multi-user BIM environments, designers frequently encounter specialized coordination anomalies. Use this checklist to diagnose and resolve typical errors:</p>
        <ul>
          <li><strong>Topological Reference Orphaned (Revit Warn 102-A):</strong> Occurs when a sketch or parameter reference is lost due to a parent wall/slab deletion. <em>Resolution:</em> Edit the sketch plane and re-associate the broken constraints to active levels.</li>
          <li><strong>Shared Coordinates Deviation:</strong> Model shifts by several inches or yards during export. <em>Resolution:</em> Verify that the host model's Project Base Point and Survey Point are correctly mapped and coordinate values are aligned before performing a global coordinate publish.</li>
          <li><strong>Worksharing Permission Locks:</strong> Multiple designers locked out of modifying <strong>{title}</strong>. <em>Resolution:</em> Have the active borrower perform a "Synchronize with Central" and check "Relinquish All Mine" in their collaboration panel.</li>
        </ul>
        """
    elif sw_domain == "modeling":
        pitfalls_diag = f"""
        <p>Parameter recalculation failures are highly disruptive during mechanical assembly rebuilds. Follow these diagnostic steps to clear feature errors related to <strong>{title}</strong>:</p>
        <ul>
          <li><strong>Parent-Child Reference Lost (Regeneration Fail):</strong> The feature tree shows red exclamation marks due to broken edges. <em>Resolution:</em> Right-click the failed feature, edit the sketch plane, and re-project missing references onto active solids.</li>
          <li><strong>Over-Constrained Sketch Conflict:</strong> The sketch solver turns yellow/red and locks geometry. <em>Resolution:</em> Suppress or delete redundant dimensional constraints, relying on geometric constraints (concentric, collinear) to define design intent.</li>
          <li><strong>Zero-Thickness Geometry Error:</strong> Occurs when solid faces intersect along a perfect line or vertex. <em>Resolution:</em> Add a micro-offset (e.g. 0.001mm) to the sketch dimensions to ensure the boolean cut or join creates a mathematically valid solid.</li>
        </ul>
        """
    else: # drafting & others
        pitfalls_diag = f"""
        <p>Avoid drawing corruption and viewport lag when referencing large assets with <strong>{title}</strong> by using this technical audit pipeline:</p>
        <ul>
          <li><strong>Registry bloat &amp; Layer Overlap:</strong> The file size jumps exponentially. <em>Resolution:</em> Run the `DGNPURGE` or `-PURGE` command with all options active, and delete duplicate scale references via the `SCALELISTEDIT` defaults.</li>
          <li><strong>Xref Clipping Boundary Disappearance:</strong> Underlays do not render boundary lines properly. <em>Resolution:</em> Set the global system variable `FRAME` or `XCLIPFRAME` to 1 or 2, allowing visual handles to display without showing up in layout plots.</li>
          <li><strong>Custom Object Proxy Warnings:</strong> Drawing shows empty boxes where smart parts should be. <em>Resolution:</em> Ensure the appropriate vendor ObjectEnabler is installed, or set `PROXYSHOW` to 1 to show proxy graphics during plotting.</li>
        </ul>
        """
    
    extra_sections.append(f"""
        <section class="kb-concept-section">
          <h2>Advanced Troubleshooting &amp; Error Diagnostics</h2>
          {pitfalls_diag}
        </section>""")

    # 4. Multi-Discipline Coordination & Collaboration Notes
    collab = f"""
    <p>In global multi-office projects, <strong>{title}</strong> is a high-frequency handoff node between diverse software packages. During cross-platform export (for example, exporting <strong>{name}</strong> drawings to IFC for coordination in Navisworks or Solibri, or converting mechanical STEP files into BIM detail families):</p>
    <ul>
      <li><strong>Class Preservation:</strong> Ensure that <strong>{title}</strong> is mapped to its correct IFC class classification (e.g., `IfcWallStandardCase` for walls, `IfcBuildingElementProxy` for generic parts). Unmapped components default to generic containers, losing their smart structural parameters.</li>
      <li><strong>Precision Offsets:</strong> Watch coordinate system compatibility. Standard DWG environments use global Cartesian axes, while mechanical solid modeling relies on local centroidal coordinate systems. Check translation offsets during file merging to avoid multi-mile position mismatches.</li>
      <li><strong>Visual Overlap Verification:</strong> Run spatial clash checks regularly in a federated viewer to verify that no geometric overlaps or clearance violations occur between <strong>{title}</strong> and structural frameworks.</li>
    </ul>
    """
    
    extra_sections.append(f"""
        <section class="kb-concept-section">
          <h2>Cross-Discipline Collaboration &amp; Handoff</h2>
          {collab}
        </section>""")

    return extra_sections


def render_quiz(quiz_data: list[dict], term_slug: str) -> str:
    if not quiz_data:
        return ""
    
    parts = []
    parts.append(f'<section class="kb-concept-section kb-quiz-section" style="margin-top: 40px; border-top: 1px solid var(--ink-line); padding-top: 32px;">')
    parts.append(f'  <h2 style="font-size: 1.5rem; font-weight: 700; color: var(--ink-text); margin-bottom: 8px;">⚡ Concept Self-Test</h2>')
    parts.append(f'  <p style="font-size: 14.5px; color: var(--ink-text-soft); margin-bottom: 20px;">Test your understanding of this concept to lock in your memory. Completing this quiz will automatically sync to your career learning progress.</p>')
    
    for q_idx, q in enumerate(quiz_data):
        question_text = esc(q["question"])
        correct_idx = q["answer_idx"]
        explanation = esc(q["explanation"])
        
        parts.append(f'  <div class="kb-quiz-card" data-quiz-container data-term-slug="{term_slug}" data-correct-idx="{correct_idx}" style="background: var(--ink-surface-1); border: 1px solid var(--ink-line); border-radius: 16px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01); position: relative; overflow: hidden; margin-bottom: 16px;">')
        parts.append(f'    <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; color: #818cf8; letter-spacing: 0.05em; margin-bottom: 12px;">Question {q_idx + 1}</div>')
        parts.append(f'    <h3 style="font-size: 1.15rem; font-weight: 700; color: var(--ink-text); margin: 0 0 16px 0; line-height: 1.4;">{question_text}</h3>')
        
        parts.append(f'    <div class="kb-quiz-options" style="display: grid; gap: 10px; margin-bottom: 16px;">')
        for opt_idx, opt in enumerate(q["options"]):
            opt_text = esc(opt)
            parts.append(f'      <button class="kb-quiz-option-btn" data-option-idx="{opt_idx}" style="background: var(--ink-surface-2); border: 1px solid var(--ink-line); color: var(--ink-text); text-align: left; padding: 12px 16px; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.2s ease; display: flex; align-items: center; gap: 12px; width: 100%;">')
            parts.append(f'        <span class="kb-quiz-option-indicator" style="display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; border-radius: 50%; border: 1px solid var(--ink-line); font-size: 11px; color: var(--ink-text-soft); font-weight: 700; flex-shrink: 0;">{chr(65 + opt_idx)}</span>')
            parts.append(f'        <span>{opt_text}</span>')
            parts.append(f'      </button>')
        parts.append(f'    </div>')
        
        parts.append(f'    <div class="kb-quiz-feedback-box" data-explanation-box style="display: none; padding: 16px; border-radius: 12px; background: rgba(99, 102, 241, 0.04); border: 1px solid rgba(99, 102, 241, 0.12); margin-top: 16px; font-size: 14px; line-height: 1.5; color: var(--ink-text);">')
        parts.append(f'      <div style="font-weight: 700; margin-bottom: 6px;" data-feedback-title>Feedback</div>')
        parts.append(f'      <div data-feedback-text>{explanation}</div>')
        parts.append(f'    </div>')
        
        parts.append(f'  </div>')
        
    parts.append(f'</section>')
    return "\n".join(parts)


SOFTWARE_CUSTOM_QUIZZES = {
    "autocad": {
        "question": "Which of the following is considered an Autodesk AutoCAD drafting best-practice regarding layout annotation?",
        "options": [
            "Draw layouts and sheet borders at 1:1 in Paper Space, and scale model-space views using locked viewports.",
            "Always explode reusable blocks to optimize layer styles and viewport visibility.",
            "Configure lineweights and colors globally using absolute pixel units in model space.",
            "Draft all sheet borders in model space at 100x scale and plot directly from model space."
        ],
        "correct_idx": 0,
        "explanation": "Standard AutoCAD methodology dictates drafting layout sheets at 1:1 in Paper Space, using locked viewports to scale and frame the 1:1 Model Space geometry, avoiding plotting directly from model space."
    },
    "revit": {
        "question": "What is the primary coordinate coordination methodology to align structural, MEP, and architectural links in Revit?",
        "options": [
            "Shared Coordinates system mapping all projects to a common geographic or local survey origin.",
            "Exploding all linked models and merging their layers into a single drawing template.",
            "Scaling block attributes by hand using absolute coordinates in paper space.",
            "Converting all files to DXF format before importing them into layout viewports."
        ],
        "correct_idx": 0,
        "explanation": "Shared Coordinates ensure Revit links align automatically across disciplines by sharing a synchronized project coordinate or survey point origin."
    },
    "solidworks": {
        "question": "When designing parts in SOLIDWORKS, how are geometric relations primarily maintained?",
        "options": [
            "Via parametric sketch relations (such as horizontal, vertical, tangent, or coincident) and dimension variables.",
            "By plotting sketches as raster coordinates and tracing them manually in assembly space.",
            "By locking all sketch points to absolute pixel coordinates in cloud databases.",
            "By exporting files to DWG format and drawing lines on separate layer colors."
        ],
        "correct_idx": 0,
        "explanation": "SOLIDWORKS relies on parametric sketching rules (tangency, concentricity, coincidences) coupled with dimensional values to govern part behavior under modifications."
    },
    "fusion-360": {
        "question": "Which of the following is a key advantage of Fusion 360's design history timeline?",
        "options": [
            "It captures parametric features in chronological order, letting designers roll back and modify upstream parameters.",
            "It automatically converts all 2D curves into high-speed CNC G-code without CAD tools.",
            "It disables user customization to guarantee cloud compatibility.",
            "It stores all drawing entities as simple, non-parametric 2D layer objects."
        ],
        "correct_idx": 0,
        "explanation": "Fusion 360's parametric timeline keeps a history of features. You can edit an early sketch or extrusion, and downstream features regenerate automatically."
    },
    "gstarcad": {
        "question": "Which programming API is highly optimized in GstarCAD for porting legacy AutoCAD automations?",
        "options": [
            "AutoLISP / GRX (compatible with AutoCAD ARX) APIs, allowing fast execution of custom drafting scripts.",
            "SQL Server database triggers and active cloud API syncing.",
            "Javascript ES6 modules running in offline node layers.",
            "Standard vector coordinate translators running inside layout sheets."
        ],
        "correct_idx": 0,
        "explanation": "GstarCAD provides high compatibility with AutoLISP and GRX APIs, allowing LISP scripts and C++ commands written for AutoCAD to load and run with minimal code changes."
    }
}


def generate_software_fallback_quiz(sw: dict) -> dict:
    name = sw["name"]
    tagline = sw.get("tagline") or (sw.get("meta_desc") or name)
    vendor = sw.get("vendor", {}).get("name", "the vendor")
    
    question = f"When evaluating {name} for your design workflow, which of the following is a primary consideration?"
    options = [
        f"Understanding its role as a {esc(tagline.lower().rstrip('.'))}.",
        f"Enforcing SQL database indexing across local viewport rendering sweeps.",
        f"Over-allocating temporary system memory caches for cloud layer merges.",
        f"Decoupling coordinate vectors entirely from the drawing layout style."
    ]
    correct_idx = 0
    explanation = f"As the technical reference notes, {name} (developed by {vendor}) operates as: '{esc(tagline)}' Understanding its native feature limits and platform alignment is crucial for model health."
    
    return {
        "question": question,
        "options": options,
        "correct_idx": correct_idx,
        "explanation": explanation
    }


def render_software_quiz(sw: dict) -> str:
    slug = sw["slug"]
    name = sw["name"]
    
    quiz = SOFTWARE_CUSTOM_QUIZZES.get(slug)
    if not quiz:
        quiz = generate_software_fallback_quiz(sw)
        
    question = quiz["question"]
    options = quiz["options"]
    correct_idx = quiz["correct_idx"]
    explanation = quiz["explanation"]
    
    parts = []
    parts.append(f'<section class="kb-concept-section kb-quiz-section" style="margin-top: 40px; border-top: 1px solid var(--ink-line); padding-top: 32px;">')
    parts.append(f'  <h2 style="font-size: 1.5rem; font-weight: 700; color: var(--ink-text); margin-bottom: 8px;">⚡ Software Guide Self-Test</h2>')
    parts.append(f'  <p style="font-size: 14.5px; color: var(--ink-text-soft); margin-bottom: 20px;">Verify your high-level understanding of {esc(name)} to sync with your learning track progress.</p>')
    parts.append(f'  <div class="kb-quiz-card" data-quiz-container data-term-slug="{slug}" data-correct-idx="{correct_idx}" style="background: var(--ink-surface-1); border: 1px solid var(--ink-line); border-radius: 16px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01); position: relative; overflow: hidden; margin-bottom: 16px;">')
    parts.append(f'    <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; color: #818cf8; letter-spacing: 0.05em; margin-bottom: 12px;">Question 1</div>')
    parts.append(f'    <h3 style="font-size: 1.15rem; font-weight: 700; color: var(--ink-text); margin: 0 0 16px 0; line-height: 1.4;">{esc(question)}</h3>')
    parts.append(f'    <div class="kb-quiz-options" style="display: grid; gap: 10px; margin-bottom: 16px;">')
    for opt_idx, opt in enumerate(options):
        parts.append(f'      <button class="kb-quiz-option-btn" data-option-idx="{opt_idx}" style="background: var(--ink-surface-2); border: 1px solid var(--ink-line); color: var(--ink-text); text-align: left; padding: 12px 16px; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.2s ease; display: flex; align-items: center; gap: 12px; width: 100%;">')
        parts.append(f'        <span class="kb-quiz-option-indicator" style="display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; border-radius: 50%; border: 1px solid var(--ink-line); font-size: 11px; color: var(--ink-text-soft); font-weight: 700; flex-shrink: 0;">{chr(65 + opt_idx)}</span>')
        parts.append(f'        <span>{esc(opt)}</span>')
        parts.append(f'      </button>')
    parts.append(f'    </div>')
    parts.append(f'    <div class="kb-quiz-feedback-box" data-explanation-box style="display: none; padding: 16px; border-radius: 12px; background: rgba(99, 102, 241, 0.04); border: 1px solid rgba(99, 102, 241, 0.12); margin-top: 16px; font-size: 14px; line-height: 1.5; color: var(--ink-text);">')
    parts.append(f'      <div style="font-weight: 700; margin-bottom: 6px;" data-feedback-title>Feedback</div>')
    parts.append(f'      <div data-feedback-text>{esc(explanation)}</div>')
    parts.append(f'    </div>')
    parts.append(f'  </div>')
    parts.append(f'</section>')
    
    return "\n".join(parts)


def render_concept(term: dict, software: dict, editorial: dict, all_terms_index: dict[str, str], all_tutorials: list[dict] = None) -> str:
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
    if not sources:
        # Programmatic E-E-A-T Authority Boost
        vendor_name = software.get("vendor", {}).get("name", "Gstarcademy")
        sw_name = software.get("name", "CAD Suite")
        if "autodesk" in vendor_name.lower():
            sources.append({
                "label": "Autodesk Help & Technical Documentation portal",
                "url": "https://help.autodesk.com/",
                "publisher": "Autodesk Inc."
            })
            sources.append({
                "label": f"{sw_name} Product Support Portal",
                "url": "https://www.autodesk.com/support",
                "publisher": "Autodesk Inc."
            })
        elif "dassault" in vendor_name.lower():
            sources.append({
                "label": "Dassault Systèmes Support & Documentation portal",
                "url": "https://www.3ds.com/support/",
                "publisher": "Dassault Systèmes"
            })
        elif "siemens" in vendor_name.lower():
            sources.append({
                "label": "Siemens Digital Industries Software Support portal",
                "url": "https://support.sw.siemens.com/",
                "publisher": "Siemens AG"
            })
        elif "gstar" in vendor_name.lower():
            sources.append({
                "label": "Gstarsoft Support Center & Technical FAQ Portal",
                "url": "https://www.gstarcad.net/support/",
                "publisher": "Gstarsoft Co., Ltd."
            })
        elif "zwsoft" in vendor_name.lower():
            sources.append({
                "label": "ZWSOFT Support Center & Help portal",
                "url": "https://www.zwsoft.com/support",
                "publisher": "ZWSOFT"
            })
        elif "bentley" in vendor_name.lower():
            sources.append({
                "label": "Bentley Communities - Technical Learn Wikis",
                "url": "https://communities.bentley.com/",
                "publisher": "Bentley Systems"
            })
        elif "ptc" in vendor_name.lower():
            sources.append({
                "label": "PTC Support Portal and Help Reference Center",
                "url": "https://www.ptc.com/en/support",
                "publisher": "PTC Inc."
            })
        elif "freecad" in sw_name.lower():
            sources.append({
                "label": "FreeCAD Official User Wiki & Developer Manual",
                "url": "https://wiki.freecad.org/",
                "publisher": "FreeCAD Community"
            })
        elif "blender" in sw_name.lower():
            sources.append({
                "label": "Blender Official Manual & Documentation portal",
                "url": "https://docs.blender.org/",
                "publisher": "Blender Foundation"
            })
        elif "openfoam" in sw_name.lower():
            sources.append({
                "label": "OpenFOAM User Guide & Foundation Reference Documentation",
                "url": "https://openfoam.org/resources/",
                "publisher": "OpenFOAM Foundation"
            })
        else:
            sources.append({
                "label": f"{sw_name} Official Product Documentation",
                "url": software.get("homepage", "https://gstarcademy.com/"),
                "publisher": vendor_name
            })

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
        
    # SEO Content Enrichment Engine: Programmatically insert advanced detailed sections
    body_parts.extend(enrich_concept_body(term, software))
    
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

    reviewer_id = term.get("reviewer_id", software.get("default_reviewer_id", "lc-editorial"))
    team_desks = {t["id"]: t for t in editorial["editorial_team"]}
    rev_orig = team_desks.get(reviewer_id) or team_desks.get("lc-editorial")
    credentials_list = rev_orig.get("credentials") or []
    credentials_html = "".join(f"<li>{esc(c)}</li>" for c in credentials_list)

    byline = f"""<div class="ink-byline" role="contentinfo">
          <span><strong>By</strong> {esc(editorial['editorial_team'][0]['name'])}</span>
          <span class="verified-reviewer-container">
            <strong>Reviewed by</strong> 
            <span class="reviewer-badge-trigger">
              {esc(rev_orig['name'])} 
              <span class="verified-badge-icon">✓</span>
            </span>
            <div class="reviewer-popover-card">
              <div class="reviewer-popover-header">
                <span class="reviewer-popover-name">{esc(rev_orig['name'])}</span>
                <span class="reviewer-popover-role">{esc(rev_orig['role'])}</span>
              </div>
              <div class="reviewer-popover-body">
                <p class="reviewer-popover-bio">{esc(rev_orig['bio'])}</p>
                <div class="reviewer-popover-meta">
                  <div class="reviewer-popover-meta-item">
                    <strong>Experience:</strong> {esc(rev_orig.get('experience_years', '10+'))} years
                  </div>
                  <div class="reviewer-popover-meta-item">
                    <strong>Credentials:</strong>
                    <ul class="reviewer-popover-credentials">
                      {credentials_html}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </span>
          <span><strong>Last reviewed</strong> <time datetime="{last_reviewed}">{last_reviewed}</time></span>
          <span><a href="../../about.html#editorial-process">Editorial process</a></span>
        </div>"""

    faq_accordion_html = render_faq_accordion(get_relevant_faqs(term, software), sw_name)
    spotlight_card_html = render_spotlight_card(software)
    knowledge_tree_html = render_knowledge_tree(term, software, related_terms, all_terms_index)
    quiz_html = render_quiz(term.get("quiz"), slug)

    recommended_tutorials_html = ""
    if all_tutorials:
        matched_tuts = find_matching_tutorials(term, software, all_tutorials)
        recommended_tutorials_html = render_recommended_tutorials(matched_tuts)

    feedback_html = f"""
        <section class="kb-feedback-section" data-feedback-container data-term-slug="{slug}" style="margin-top: 32px; padding: 20px; border-radius: 16px; background: rgba(255,255,255,0.03); border: 1px solid var(--line); text-align: center;">
          <div data-feedback-prompt style="display: flex; flex-direction: column; align-items: center; gap: 12px;">
            <span style="font-size: 14px; font-weight: 600; color: var(--text);">Was this conceptual reference clear and helpful?</span>
            <div style="display: flex; gap: 12px; justify-content: center;">
              <button class="btn feedback-btn" data-feedback-type="yes" style="padding: 8px 16px; font-size: 13px; display: inline-flex; align-items: center; gap: 6px; border-radius: 8px; cursor: pointer; transition: all 0.2s;">
                👍 Yes
              </button>
              <button class="btn feedback-btn" data-feedback-type="no" style="padding: 8px 16px; font-size: 13px; display: inline-flex; align-items: center; gap: 6px; border-radius: 8px; cursor: pointer; transition: all 0.2s;">
                👎 Needs Improvement
              </button>
            </div>
          </div>
          <div data-feedback-thankyou style="display: none; font-size: 13px; font-weight: 500; color: #10b981;">
            ✓ Thank you for your feedback! Your input helps shape the CAD curriculum.
          </div>
        </section>"""

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
    <title>{esc(title)} · {sw_name} · CAD Knowledge Base · Gstarcademy</title>
    <meta name="description" content="{esc(desc)}" />
    <link rel="canonical" href="{url}" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="manifest" href="../../manifest.json" />
    <script src="../../search.js" defer></script>
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

        {quiz_html}

        {recommended_tutorials_html}

        {knowledge_tree_html}

        {sources_html}

        {feedback_html}

        <p class="meta" style="margin-top: 36px; font-size: 12px;">{esc(editorial['license_note'])}</p>
      </article>
    </main>

    {footer_html('../../')}
    <script src="../../d3.min.js?v={CSS_VER}" defer></script>
    <script src="../../app.js?v={CSS_VER}" defer></script>
    <script src="../../knowledge.js?v={CSS_VER}" defer></script>
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
    if not sources:
        sw_name = sw["name"]
        vendor_name = sw["vendor"]["name"]
        homepage = sw.get("homepage")
        if not homepage:
            if "autodesk" in vendor_name.lower():
                homepage = "https://www.autodesk.com/"
            elif "dassault" in vendor_name.lower():
                homepage = "https://www.3ds.com/"
            elif "siemens" in vendor_name.lower():
                homepage = "https://www.siemens.com/"
            elif "gstar" in vendor_name.lower() or "gstarsoft" in vendor_name.lower():
                homepage = "https://www.gstarcad.net/"
            elif "zwsoft" in vendor_name.lower():
                homepage = "https://www.zwsoft.com/"
            elif "bentley" in vendor_name.lower():
                homepage = "https://communities.bentley.com/"
            elif "ptc" in vendor_name.lower():
                homepage = "https://www.ptc.com/"
            elif "freecad" in sw_name.lower():
                homepage = "https://www.freecad.org/"
            elif "blender" in sw_name.lower():
                homepage = "https://www.blender.org/"
            elif "openfoam" in sw_name.lower():
                homepage = "https://www.openfoam.com/"
            elif "graphisoft" in vendor_name.lower():
                homepage = "https://graphisoft.com/"
            elif "alibre" in vendor_name.lower():
                homepage = "https://www.alibre.com/"
            elif "bricsys" in vendor_name.lower() or "bricscad" in sw_name.lower():
                homepage = "https://www.bricsys.com/"
            elif "altium" in vendor_name.lower():
                homepage = "https://www.altium.com/"
            elif "ansys" in vendor_name.lower():
                homepage = "https://www.ansys.com/"
            elif "trimble" in vendor_name.lower() or "tekla" in sw_name.lower() or "sketchup" in sw_name.lower():
                homepage = "https://www.trimble.com/"
            else:
                homepage = "https://gstarcademy.com/"
        sources = [{
            "label": f"{sw_name} Official Homepage & Resource Directory",
            "url": homepage,
            "publisher": vendor_name
        }]

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

    html_out = f"""<!doctype html>
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
    <title>{esc(name)} — software profile, learning path, ecosystem · Gstarcademy</title>
    <meta name="description" content="{esc(desc)}" />
    <link rel="canonical" href="{url}" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="manifest" href="../../manifest.json" />
    <script src="../../search.js" defer></script>
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
        {render_software_quiz(sw)}
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
    return re.sub(
        r'href="(?:\./)?(?!index\.html|tutorials\.html|news\.html|knowledge-base\.html|quiz\.html|about\.html|contact\.html|kb-terms\.html|kb-faq\.html|kb-graph\.html|kb-software\.html|knowledge-cax\.html|knowledge-curriculum\.html|knowledge-domains\.html|knowledge-library\.html|knowledge-roadmap\.html)([a-zA-Z0-9_-]+\.html)"',
        r'href="../concepts/\1"',
        html_out
    )


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
    if not sources:
        vendor_name = vendor["name"]
        homepage = vendor.get("homepage")
        if not homepage:
            if "autodesk" in vendor_name.lower():
                homepage = "https://www.autodesk.com/"
            elif "dassault" in vendor_name.lower():
                homepage = "https://www.3ds.com/"
            elif "siemens" in vendor_name.lower():
                homepage = "https://www.siemens.com/"
            elif "gstar" in vendor_name.lower() or "gstarsoft" in vendor_name.lower():
                homepage = "https://www.gstarcad.net/"
            elif "zwsoft" in vendor_name.lower():
                homepage = "https://www.zwsoft.com/"
            elif "bentley" in vendor_name.lower():
                homepage = "https://communities.bentley.com/"
            elif "ptc" in vendor_name.lower():
                homepage = "https://www.ptc.com/"
            elif "freecad" in vendor_name.lower():
                homepage = "https://www.freecad.org/"
            elif "blender" in vendor_name.lower():
                homepage = "https://www.blender.org/"
            elif "openfoam" in vendor_name.lower():
                homepage = "https://www.openfoam.com/"
            elif "graphisoft" in vendor_name.lower():
                homepage = "https://graphisoft.com/"
            elif "alibre" in vendor_name.lower():
                homepage = "https://www.alibre.com/"
            elif "bricsys" in vendor_name.lower():
                homepage = "https://www.bricsys.com/"
            elif "altium" in vendor_name.lower():
                homepage = "https://www.altium.com/"
            elif "ansys" in vendor_name.lower():
                homepage = "https://www.ansys.com/"
            elif "trimble" in vendor_name.lower():
                homepage = "https://www.trimble.com/"
            else:
                homepage = "https://gstarcademy.com/"
        sources = [{
            "label": f"{vendor_name} Official Corporate Portal",
            "url": homepage,
            "publisher": vendor_name
        }]

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
    <title>{esc(name)} — CAD vendor profile · Gstarcademy</title>
    <meta name="description" content="{esc(desc)}" />
    <link rel="canonical" href="{url}" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="manifest" href="../../manifest.json" />
    <script src="../../search.js" defer></script>
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

    # Build title to slug map to support interactive direct clicks
    title_to_slug = {}
    for sw in software_list:
        title_to_slug[sw["name"]] = sw["slug"]
        if "vendor" in sw:
            title_to_slug[sw["vendor"]["name"]] = sw["vendor"]["slug"]
        for t in sw.get("terms", []):
            title_to_slug[t["title"]] = t["slug"]

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
            slug_val = title_to_slug.get(nid, "")
            node_lines.append(
                "  { id: %s, type: %s, group: %d, radius: %d, tags: %s, hint: %s, slug: %s }," % (
                    json.dumps(nid, ensure_ascii=False),
                    json.dumps(n.get("type", "concept"), ensure_ascii=False),
                    int(n.get("group", 2)),
                    int(n.get("radius", 8)),
                    json.dumps(n.get("tags", []) or [], ensure_ascii=False),
                    json.dumps(n.get("hint", ""), ensure_ascii=False),
                    json.dumps(slug_val, ensure_ascii=False),
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

def patch_sitemap(software_list: list[dict]) -> None:
    path = ROOT / "sitemap.xml"

    # 静态核心页面字典，键为相对根目录的路径
    STATIC_PAGES = {
        "index.html": {"changefreq": "daily", "priority": "1.0"},
        "tutorials.html": {"changefreq": "daily", "priority": "0.9"},
        "tutorial-detail.html": {"changefreq": "weekly", "priority": "0.8"},
        "paths.html": {"changefreq": "weekly", "priority": "0.9"},
        "news.html": {"changefreq": "daily", "priority": "0.85"},
        "knowledge-base.html": {"changefreq": "weekly", "priority": "0.9"},
        "knowledge-cax.html": {"changefreq": "weekly", "priority": "0.85"},
        "knowledge-roadmap.html": {"changefreq": "weekly", "priority": "0.85"},
        "knowledge-library.html": {"changefreq": "weekly", "priority": "0.85"},
        "knowledge-curriculum.html": {"changefreq": "weekly", "priority": "0.85"},
        "kb-terms.html": {"changefreq": "weekly", "priority": "0.85"},
        "kb-faq.html": {"changefreq": "monthly", "priority": "0.82"},
        "kb-graph.html": {"changefreq": "weekly", "priority": "0.8"},
        "kb-software.html": {"changefreq": "monthly", "priority": "0.75"},
        "knowledge-domains.html": {"changefreq": "monthly", "priority": "0.75"},
        "legal.html": {"changefreq": "monthly", "priority": "0.5"},
        "about.html": {"changefreq": "monthly", "priority": "0.6"},
        "editorial-process.html": {"changefreq": "monthly", "priority": "0.6"},
        "contact.html": {"changefreq": "monthly", "priority": "0.5"},
        "privacy.html": {"changefreq": "yearly", "priority": "0.4"},
        "terms.html": {"changefreq": "yearly", "priority": "0.4"},
    }

    # 待校验的 URL 及其配置映射
    # 结构为: { "相对路径": { "changefreq": "...", "priority": "..." } }
    pages_to_verify = {}
    for rel_path, cfg in STATIC_PAGES.items():
        pages_to_verify[rel_path] = cfg

    # 动态页面：软件，商家，概念
    for sw in software_list:
        sw_rel = f"kb/software/{sw['slug']}.html"
        pages_to_verify[sw_rel] = {"changefreq": "monthly", "priority": "0.75"}

        vendor_rel = f"kb/vendors/{sw['vendor']['slug']}.html"
        pages_to_verify[vendor_rel] = {"changefreq": "monthly", "priority": "0.7"}

        for t in sw.get("terms", []):
            concept_rel = f"kb/concepts/{t['slug']}.html"
            pages_to_verify[concept_rel] = {"changefreq": "weekly", "priority": "0.7"}

    # 校验每个相对路径对应的文件在磁盘上是否存在
    valid_entries = []
    for rel_path, cfg in sorted(pages_to_verify.items()):
        file_path = ROOT / rel_path
        if file_path.exists():
            loc = f"{SITE_URL}/{rel_path}"
            valid_entries.append(
                f"  <url>\n"
                f"    <loc>{loc}</loc>\n"
                f"    <changefreq>{cfg['changefreq']}</changefreq>\n"
                f"    <priority>{cfg['priority']}</priority>\n"
                f"  </url>"
            )
        else:
            print(f"Sitemap filter: {rel_path} does not exist on disk, skipped.")

    # 拼装完整的 sitemap.xml
    xml_content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(valid_entries) + "\n"
        '</urlset>\n'
    )

    path.write_text(xml_content, encoding="utf-8")
    print(f"Generated sitemap.xml with {len(valid_entries)} verified URLs.")


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

    # Load all tutorials once for conceptual linkage
    all_tutorials = load_all_tutorials()

    # Render concept pages
    written_terms = 0
    for sw in software_list:
        for t in sw.get("terms", []):
            page = render_concept(t, sw, editorial, all_terms_index, all_tutorials)
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
