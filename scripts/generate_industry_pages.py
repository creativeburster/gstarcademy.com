#!/usr/bin/env python3
"""
Generate industry/use-case pages targeting "best CAD for X" and workflow queries.
"""

import os
from datetime import date

TODAY = date.today().isoformat()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'guides')
os.makedirs(OUTPUT_DIR, exist_ok=True)

GUIDES = [
    # Best-software-for pages
    {"slug": "best-cad-architecture", "title": "Best CAD Software for Architecture in 2026", "desc": "Compare the top CAD and BIM software for architects: Revit, ArchiCAD, Vectorworks, SketchUp, and Rhino. Features, pricing, and workflow recommendations.", "category": "Architecture", "software": [("revit", "Revit"), ("archicad", "ArchiCAD"), ("vectorworks", "Vectorworks"), ("sketchup", "SketchUp"), ("rhinoceros", "Rhino")]},
    {"slug": "best-cad-mechanical-design", "title": "Best CAD Software for Mechanical Design in 2026", "desc": "Top MCAD software for product development and mechanical engineering: SOLIDWORKS, Creo, NX, Inventor, and Fusion 360 compared.", "category": "Mechanical Engineering", "software": [("solidworks", "SOLIDWORKS"), ("creo-parametric", "Creo Parametric"), ("siemens-nx", "Siemens NX"), ("inventor", "Inventor"), ("fusion-360", "Fusion 360")]},
    {"slug": "best-cad-civil-engineering", "title": "Best CAD Software for Civil Engineering in 2026", "desc": "Compare civil infrastructure design tools: Civil 3D, MicroStation, OpenRoads Designer, and more. Alignments, corridors, grading, and pipe network capabilities.", "category": "Civil Engineering", "software": [("civil-3d", "Civil 3D"), ("microstation", "MicroStation"), ("openroads", "OpenRoads Designer")]},
    {"slug": "best-free-cad-software", "title": "Best Free CAD Software in 2026 — Open Source & Freemium", "desc": "Top free CAD software for students, hobbyists, and professionals on a budget: FreeCAD, Blender, SketchUp Free, Onshape Free, and DraftSight.", "category": "Free & Open Source", "software": [("freecad", "FreeCAD"), ("blender", "Blender"), ("sketchup", "SketchUp Free"), ("onshape", "Onshape Free")]},
    {"slug": "best-cad-3d-printing", "title": "Best CAD Software for 3D Printing in 2026", "desc": "Top modeling software for 3D printing and additive manufacturing: Fusion 360, FreeCAD, Blender, SOLIDWORKS, and Rhino with mesh preparation workflows.", "category": "3D Printing", "software": [("fusion-360", "Fusion 360"), ("freecad", "FreeCAD"), ("blender", "Blender"), ("solidworks", "SOLIDWORKS"), ("rhinoceros", "Rhino")]},
    {"slug": "best-cad-interior-design", "title": "Best CAD Software for Interior Design in 2026", "desc": "Compare CAD tools for interior designers: SketchUp, Revit, Vectorworks, AutoCAD, and 3ds Max for space planning, rendering, and documentation.", "category": "Interior Design", "software": [("sketchup", "SketchUp"), ("revit", "Revit"), ("vectorworks", "Vectorworks"), ("autocad", "AutoCAD"), ("3dsmax", "3ds Max")]},
    {"slug": "best-cad-automotive", "title": "Best CAD Software for Automotive Design in 2026", "desc": "Top CAD platforms for automotive engineering: CATIA, NX, SOLIDWORKS, Creo, and Alias compared for body design, chassis, and powertrain development.", "category": "Automotive", "software": [("catia", "CATIA"), ("siemens-nx", "Siemens NX"), ("solidworks", "SOLIDWORKS"), ("creo-parametric", "Creo Parametric")]},
    {"slug": "best-cad-aerospace", "title": "Best CAD Software for Aerospace Engineering in 2026", "desc": "Compare aerospace-grade CAD/CAE platforms: CATIA, NX, Creo, SOLIDWORKS, and ABAQUS for airframe design, simulation, and certification workflows.", "category": "Aerospace", "software": [("catia", "CATIA"), ("siemens-nx", "Siemens NX"), ("creo-parametric", "Creo"), ("abaqus", "ABAQUS")]},
    {"slug": "best-cad-students", "title": "Best CAD Software for Students in 2026", "desc": "Top free and discounted CAD software for engineering students: educational licenses, free tiers, and open-source alternatives for learning.", "category": "Education", "software": [("fusion-360", "Fusion 360"), ("solidworks", "SOLIDWORKS"), ("freecad", "FreeCAD"), ("onshape", "Onshape"), ("autocad", "AutoCAD")]},
    {"slug": "best-cad-product-design", "title": "Best CAD Software for Product Design in 2026", "desc": "Compare product design tools for consumer electronics, furniture, and industrial design: SOLIDWORKS, Fusion 360, Rhino, and Onshape evaluated.", "category": "Product Design", "software": [("solidworks", "SOLIDWORKS"), ("fusion-360", "Fusion 360"), ("rhinoceros", "Rhino"), ("onshape", "Onshape")]},
    {"slug": "best-cad-mep-engineering", "title": "Best CAD Software for MEP Engineering in 2026", "desc": "Compare MEP design tools: Revit MEP, AutoCAD MEP, MagiCAD, and DDS-CAD for HVAC, plumbing, and electrical system modeling.", "category": "MEP Engineering", "software": [("revit", "Revit MEP"), ("autocad", "AutoCAD MEP"), ("allplan", "Allplan")]},
    {"slug": "best-cad-landscape-architecture", "title": "Best CAD Software for Landscape Architecture in 2026", "desc": "Top tools for landscape architects: Vectorworks Landmark, Civil 3D, SketchUp, and Rhino with Lands Design compared for site planning and terrain modeling.", "category": "Landscape Architecture", "software": [("vectorworks", "Vectorworks Landmark"), ("civil-3d", "Civil 3D"), ("sketchup", "SketchUp"), ("rhinoceros", "Rhino")]},
    {"slug": "best-cad-furniture-design", "title": "Best CAD Software for Furniture Design in 2026", "desc": "Compare CAD tools for furniture makers and woodworkers: SketchUp, Fusion 360, SOLIDWORKS, Rhino, and FreeCAD for joinery, CNC, and rendering.", "category": "Furniture Design", "software": [("sketchup", "SketchUp"), ("fusion-360", "Fusion 360"), ("solidworks", "SOLIDWORKS"), ("rhinoceros", "Rhino"), ("freecad", "FreeCAD")]},
    {"slug": "best-cad-jewelry-design", "title": "Best CAD Software for Jewelry Design in 2026", "desc": "Top 3D modeling tools for jewelry CAD: Rhino with Matrix/RhinoGold, ZBrush, Fusion 360, and Blender for ring, pendant, and gemstone modeling.", "category": "Jewelry Design", "software": [("rhinoceros", "Rhino + Matrix"), ("blender", "Blender"), ("fusion-360", "Fusion 360")]},
    {"slug": "best-cad-game-development", "title": "Best 3D Modeling Software for Game Development in 2026", "desc": "Compare game-ready 3D tools: Blender, 3ds Max, Maya, ZBrush, and SketchUp for environment art, character modeling, and asset optimization.", "category": "Game Development", "software": [("blender", "Blender"), ("3dsmax", "3ds Max"), ("sketchup", "SketchUp")]},
    # Workflow / How-to pages
    {"slug": "dwg-vs-rvt-vs-ifc", "title": "DWG vs RVT vs IFC — File Format Comparison for AEC", "desc": "Understand the differences between DWG, RVT, and IFC file formats in architecture and construction. When to use each format and interoperability considerations.", "category": "File Formats", "software": [("autocad", "AutoCAD (DWG)"), ("revit", "Revit (RVT)")]},
    {"slug": "parametric-vs-direct-modeling", "title": "Parametric vs Direct Modeling — When to Use Each Approach", "desc": "Understand the differences between parametric (history-based) and direct modeling approaches in CAD. Learn when each method excels and which software supports both.", "category": "Methodology", "software": [("solidworks", "SOLIDWORKS"), ("siemens-nx", "NX Synchronous"), ("creo-parametric", "Creo"), ("bricscad", "BricsCAD")]},
    {"slug": "bim-vs-cad", "title": "BIM vs CAD — What's the Difference and When to Switch", "desc": "Understand the fundamental differences between BIM and traditional CAD drafting. Learn when to transition from 2D CAD to BIM and what the migration involves.", "category": "Methodology", "software": [("autocad", "AutoCAD"), ("revit", "Revit"), ("archicad", "ArchiCAD")]},
    {"slug": "cloud-cad-vs-desktop", "title": "Cloud CAD vs Desktop CAD — Pros, Cons & Best Options in 2026", "desc": "Compare cloud-native CAD platforms (Onshape, Fusion 360) with traditional desktop installations (SOLIDWORKS, AutoCAD). Performance, collaboration, and security considerations.", "category": "Methodology", "software": [("onshape", "Onshape"), ("fusion-360", "Fusion 360"), ("solidworks", "SOLIDWORKS"), ("autocad", "AutoCAD")]},
    {"slug": "autocad-alternatives", "title": "AutoCAD Alternatives — 10 DWG-Compatible CAD Programs in 2026", "desc": "The best AutoCAD alternatives that read and write DWG natively: GstarCAD, ZWCAD, BricsCAD, DraftSight, ARES Commander, and more compared on features and pricing.", "category": "Alternatives", "software": [("gstarcad", "GstarCAD"), ("zwcad", "ZWCAD"), ("bricscad", "BricsCAD"), ("draftsight", "DraftSight"), ("ares-commander", "ARES Commander")]},
    {"slug": "solidworks-alternatives", "title": "SOLIDWORKS Alternatives — Best MCAD Options in 2026", "desc": "Top alternatives to SOLIDWORKS for mechanical design: Fusion 360, Onshape, Inventor, Creo, Solid Edge, FreeCAD, and IronCAD compared on capability and cost.", "category": "Alternatives", "software": [("fusion-360", "Fusion 360"), ("onshape", "Onshape"), ("inventor", "Inventor"), ("creo-parametric", "Creo"), ("solid-edge", "Solid Edge"), ("freecad", "FreeCAD")]},
    {"slug": "revit-alternatives", "title": "Revit Alternatives — BIM Software Options in 2026", "desc": "Best alternatives to Revit for building information modeling: ArchiCAD, Allplan, Vectorworks, BricsCAD BIM, and BlenderBIM compared on openBIM support and workflow.", "category": "Alternatives", "software": [("archicad", "ArchiCAD"), ("allplan", "Allplan"), ("vectorworks", "Vectorworks"), ("bricscad", "BricsCAD BIM")]},
    {"slug": "cad-system-requirements-2026", "title": "CAD System Requirements 2026 — Hardware Guide", "desc": "Minimum and recommended PC specs for running AutoCAD, Revit, SOLIDWORKS, and other CAD software in 2026. CPU, GPU, RAM, and storage recommendations by software.", "category": "Hardware", "software": [("autocad", "AutoCAD"), ("revit", "Revit"), ("solidworks", "SOLIDWORKS"), ("3dsmax", "3ds Max")]},
    {"slug": "cad-file-formats-guide", "title": "CAD File Formats Explained — DWG, STEP, IGES, IFC & More", "desc": "Complete guide to CAD file formats: DWG, DXF, STEP, IGES, IFC, 3DM, SAT, STL, and proprietary formats. Understand when to use each and interoperability tips.", "category": "File Formats", "software": [("autocad", "AutoCAD"), ("solidworks", "SOLIDWORKS"), ("revit", "Revit"), ("freecad", "FreeCAD")]},
    {"slug": "cad-collaboration-tools", "title": "CAD Collaboration Tools & Workflows in 2026", "desc": "Compare CAD collaboration solutions: cloud platforms, PDM/PLM systems, BIM servers, and real-time co-editing tools for distributed engineering teams.", "category": "Collaboration", "software": [("onshape", "Onshape"), ("fusion-360", "Fusion 360"), ("solidworks", "SOLIDWORKS PDM")]},
    {"slug": "cad-automation-scripting", "title": "CAD Automation & Scripting Guide — AutoLISP, Python, Dynamo & More", "desc": "Overview of CAD automation options: AutoLISP, Python, VBA, Dynamo, Grasshopper, iLogic, and journal files. Choose the right scripting approach for your software.", "category": "Scripting", "software": [("autocad", "AutoCAD"), ("revit", "Revit"), ("solidworks", "SOLIDWORKS"), ("rhinoceros", "Rhino"), ("freecad", "FreeCAD")]},
    {"slug": "cad-certification-guide", "title": "CAD Certification Guide 2026 — Vendor Exams & Career Value", "desc": "Complete guide to CAD certifications: Autodesk Certified Professional, SOLIDWORKS CSWA/CSWP, Siemens NX certification, and their career impact.", "category": "Career", "software": [("autocad", "AutoCAD"), ("revit", "Revit"), ("solidworks", "SOLIDWORKS"), ("siemens-nx", "NX")]},
    {"slug": "from-autocad-to-revit", "title": "Migrating from AutoCAD to Revit — Complete Transition Guide", "desc": "Step-by-step guide for AutoCAD users transitioning to Revit BIM. Covers mindset shift, key differences, reusable skills, and learning timeline expectations.", "category": "Migration", "software": [("autocad", "AutoCAD"), ("revit", "Revit")]},
    {"slug": "from-autocad-to-gstarcad", "title": "Migrating from AutoCAD to GstarCAD — Compatibility Guide", "desc": "How to switch from AutoCAD to GstarCAD with minimal disruption. DWG compatibility, command mapping, LISP migration, and license cost savings explained.", "category": "Migration", "software": [("autocad", "AutoCAD"), ("gstarcad", "GstarCAD")]},
    {"slug": "from-solidworks-to-fusion-360", "title": "Migrating from SOLIDWORKS to Fusion 360 — What Changes", "desc": "Guide for SOLIDWORKS users moving to Fusion 360. Covers differences in modeling approach, data management, collaboration, and feature mapping.", "category": "Migration", "software": [("solidworks", "SOLIDWORKS"), ("fusion-360", "Fusion 360")]},
]


def generate_guide_page(guide):
    g = guide
    canonical = f"https://gstarcademy.com/kb/guides/{g['slug']}"
    
    sw_links = "\n".join(
        f'            <a href="../software/{slug}" style="display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 8px; text-decoration: none; color: var(--ink-text); font-size: 13px; font-weight: 500;">{name}</a>'
        for slug, name in g["software"]
    )
    
    comparison_links = ""
    slugs = [s[0] for s in g["software"]]
    if len(slugs) >= 2:
        pairs = []
        for i in range(min(len(slugs), 4)):
            for j in range(i+1, min(len(slugs), 4)):
                pairs.append((slugs[i], slugs[j], g["software"][i][1], g["software"][j][1]))
        if pairs:
            comparison_links = '<h3 style="margin-top: 24px; font-size: 0.95rem; font-weight: 700;">Head-to-Head Comparisons</h3>\n<div style="display: flex; flex-wrap: wrap; gap: 8px;">\n'
            for sa, sb, na, nb in pairs[:6]:
                comparison_links += f'  <a href="../compare/{sa}-vs-{sb}" style="display: inline-block; padding: 6px 12px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 6px; font-size: 12px; text-decoration: none; color: var(--accent); font-weight: 500;">{na} vs {nb}</a>\n'
            comparison_links += '</div>'
    
    html = f'''<!doctype html>
<html lang="en">
  <head>
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
    <title>{g['title']} | Gstarcademy</title>
    <meta name="description" content="{g['desc']}" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <link rel="canonical" href="{canonical}" />
    <meta property="og:image" content="https://gstarcademy.com/images/og-default.webp" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{g['title']}" />
    <meta property="og:description" content="{g['desc']}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:site_name" content="Gstarcademy" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="preload" href="../../styles.min.css" as="style" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />
    <link rel="stylesheet" href="../../styles.min.css" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{g['title']}","description":"{g['desc']}","url":"{canonical}","datePublished":"{TODAY}","dateModified":"{TODAY}","inLanguage":"en","author":{{"@type":"Organization","name":"Gstarcademy Editorial Team","url":"https://gstarcademy.com/about"}},"publisher":{{"@type":"Organization","name":"Gstarcademy","url":"https://gstarcademy.com/"}}}}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://gstarcademy.com/"}},{{"@type":"ListItem","position":2,"name":"Knowledge Base","item":"https://gstarcademy.com/knowledge-base"}},{{"@type":"ListItem","position":3,"name":"Guides","item":"https://gstarcademy.com/kb/guides/"}},{{"@type":"ListItem","position":4,"name":"{g['title']}","item":"{canonical}"}}]}}</script>
  </head>
  <body>
    <div class="page-shell">
      <header class="topbar">
        <div class="container topbar-inner">
          <a class="brand" href="../../"><span class="brand-badge">GC</span><span>Gstarcademy</span></a>
          <nav class="nav">
            <a class="nav-link" href="../../">Home</a>
            <a class="nav-link active" href="../../knowledge-base">Wiki</a>
            <a class="nav-link" href="../../tutorials">Tutorials</a>
            <a class="nav-link" href="../../news">News</a>
            <a class="nav-link" href="../../about">About</a>
          </nav>
        </div>
      </header>
    </div>

    <main class="container" style="margin-top: 32px; max-width: 920px;">
      <nav class="kb-faq-breadcrumbs" aria-label="Breadcrumb">
        <a href="../../">Home</a> /
        <a href="../../knowledge-base">Knowledge Base</a> /
        <a href="./">Guides</a> /
        <span aria-current="page">{g['category']}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 28px;">
          <span class="chip pill-warn">Guide &middot; {g['category']}</span>
          <h1 style="margin-top: 12px;">{g['title']}</h1>
          <p class="hero-sub">{g['desc']}</p>
        </header>

        <div class="ink-byline" role="contentinfo">
          <span><strong>By</strong> Gstarcademy Editorial Team</span>
          <span><strong>Updated</strong> <time datetime="{TODAY}">{TODAY}</time></span>
          <span><a href="../../editorial-process">Editorial process</a></span>
        </div>

        <section class="kb-concept-section">
          <h2>Software Covered in This Guide</h2>
          <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px;">
{sw_links}
          </div>
        </section>

        <section class="kb-concept-section">
          <h2>Quick Summary</h2>
          <p>This guide helps you evaluate the best software options for <strong>{g['category'].lower()}</strong> workflows. Each tool has distinct strengths depending on your project scale, team size, budget, and industry requirements.</p>
          <p>Key factors to consider when choosing:</p>
          <ul>
            <li><strong>Project complexity:</strong> Simple conceptual design vs. detailed production documentation</li>
            <li><strong>Team collaboration:</strong> Solo practitioner vs. multi-discipline coordination</li>
            <li><strong>Budget constraints:</strong> Free/open-source vs. enterprise licensing</li>
            <li><strong>Industry standards:</strong> Required file formats and compliance (IFC, DWG, STEP)</li>
            <li><strong>Learning curve:</strong> Time available for training and existing skill sets</li>
          </ul>
        </section>

        <section class="kb-concept-section">
          <h2>Detailed Software Analysis</h2>'''
    
    for slug, name in g["software"]:
        html += f'''
          <div style="margin-top: 20px; padding: 20px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 12px;">
            <h3 style="margin: 0 0 8px; font-size: 1rem;"><a href="../software/{slug}" style="color: var(--accent); text-decoration: none; font-weight: 700;">{name}</a></h3>
            <p style="font-size: 14px; margin: 0; color: var(--ink-text-soft);">Visit the <a href="../software/{slug}">full {name} profile</a> for detailed feature documentation, API references, and concept articles.</p>
          </div>'''
    
    html += f'''
        </section>

        <section class="kb-concept-section">
          <h2>How to Decide</h2>
          <p>When selecting software for {g['category'].lower()}, we recommend:</p>
          <ol>
            <li><strong>Define your deliverables:</strong> What output formats does your client or downstream team require?</li>
            <li><strong>Evaluate ecosystem fit:</strong> Does the software integrate with your existing tools and processes?</li>
            <li><strong>Trial before committing:</strong> Most vendors offer free trials or educational licenses</li>
            <li><strong>Consider total cost:</strong> Factor in training time, hardware upgrades, and plugin costs beyond license fees</li>
            <li><strong>Check community support:</strong> Active forums, YouTube tutorials, and local user groups accelerate learning</li>
          </ol>
        </section>

        <section class="kb-concept-section">
          <h2>Related Resources</h2>
          {comparison_links}
          <h3 style="margin-top: 24px; font-size: 0.95rem; font-weight: 700;">Learning Paths</h3>
          <p>Start learning with our <a href="../learning-paths/">structured learning paths</a> for each software.</p>
        </section>

        <aside style="margin-top: 32px; padding: 20px 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 14px; display: flex; gap: 16px; align-items: flex-start; flex-wrap: wrap;" aria-label="Editorial information">
          <div style="flex: 1; min-width: 200px;">
            <p style="font-size: 12px; font-weight: 600; color: var(--ink-text); margin: 0 0 4px;">Written by Gstarcademy Editorial Team</p>
            <p style="font-size: 11px; color: var(--ink-text-soft); margin: 0;">Content follows our <a href="../../editorial-process" style="color: var(--accent); text-decoration: underline;">editorial guidelines</a>.</p>
          </div>
          <div style="text-align: right; min-width: 140px;">
            <p style="font-size: 11px; color: var(--ink-text-soft); margin: 0;">Last updated</p>
            <time datetime="{TODAY}" style="font-size: 12px; font-weight: 600; color: var(--ink-text);">{TODAY}</time>
          </div>
        </aside>

        <p class="meta" style="margin-top: 36px; font-size: 12px;">Guide curated by Gstarcademy Editorial Team. Software names and trademarks belong to their respective owners. Pricing is approximate; verify with vendors for current rates.</p>
      </article>
    </main>

    <footer class="footer site-footer">
      <div class="container site-footer-inner">
        <div class="site-footer-brand"><p class="site-footer-tagline">Gstarcademy</p><p class="site-footer-desc">CAD knowledge base and tutorial navigation.</p></div>
      </div>
      <div class="container site-footer-bottom"><p>&copy; <span id="footer-year"></span> Gstarcademy. All rights reserved.</p></div>
    </footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    return html


def generate_index():
    """Generate guides index."""
    categories = {}
    for g in GUIDES:
        cat = g["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(g)
    
    links = ""
    for cat, guides in sorted(categories.items()):
        links += f'<h3 style="margin-top: 20px; font-size: 0.95rem; font-weight: 700; color: var(--ink-text);">{cat}</h3>\n<div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px;">\n'
        for g in guides:
            links += f'  <a href="./{g["slug"]}" style="display: block; padding: 14px 20px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px; text-decoration: none; color: var(--ink-text);"><strong style="font-size: 14px;">{g["title"]}</strong><br><span style="font-size: 12px; color: var(--ink-text-soft);">{g["desc"][:100]}...</span></a>\n'
        links += '</div>\n'
    
    html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CAD Guides &amp; Best Software Recommendations | Gstarcademy</title>
    <meta name="description" content="Curated guides for choosing the best CAD software by industry, workflow, and budget. Recommendations for architecture, mechanical design, civil engineering, and more." />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <link rel="canonical" href="https://gstarcademy.com/kb/guides/" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="preload" href="../../styles.min.css" as="style" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />
    <link rel="stylesheet" href="../../styles.min.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="topbar">
        <div class="container topbar-inner">
          <a class="brand" href="../../"><span class="brand-badge">GC</span><span>Gstarcademy</span></a>
          <nav class="nav">
            <a class="nav-link" href="../../">Home</a>
            <a class="nav-link active" href="../../knowledge-base">Wiki</a>
            <a class="nav-link" href="../../tutorials">Tutorials</a>
            <a class="nav-link" href="../../news">News</a>
            <a class="nav-link" href="../../about">About</a>
          </nav>
        </div>
      </header>
    </div>
    <main class="container" style="margin-top: 32px; max-width: 920px;">
      <nav class="kb-faq-breadcrumbs" aria-label="Breadcrumb">
        <a href="../../">Home</a> / <a href="../../knowledge-base">Knowledge Base</a> / <span aria-current="page">Guides</span>
      </nav>
      <h1 style="margin-top: 16px;">CAD Guides &amp; Recommendations</h1>
      <p style="font-size: 15px; color: var(--ink-text-soft); margin-bottom: 32px;">{len(GUIDES)} curated guides to help you choose the right CAD software for your industry, workflow, and budget.</p>
      {links}
    </main>
    <footer class="footer site-footer">
      <div class="container site-footer-inner"><div class="site-footer-brand"><p class="site-footer-tagline">Gstarcademy</p></div></div>
      <div class="container site-footer-bottom"><p>&copy; <span id="footer-year"></span> Gstarcademy. All rights reserved.</p></div>
    </footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    print(f"Generating {len(GUIDES)} industry/guide pages...")
    for g in GUIDES:
        html = generate_guide_page(g)
        filepath = os.path.join(OUTPUT_DIR, f"{g['slug']}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    generate_index()
    print(f"Done! Generated {len(GUIDES)} guide pages + index")


if __name__ == '__main__':
    main()
