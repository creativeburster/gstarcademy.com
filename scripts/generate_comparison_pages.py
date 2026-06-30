#!/usr/bin/env python3
"""
Generate CAD software comparison pages (X vs Y).

Each comparison page targets "Software A vs Software B" search intent,
providing structured comparison content with proper SEO signals.
"""

import os
import json
from datetime import date

TODAY = date.today().isoformat()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'compare')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Software data: slug, display name, category, key strengths, pricing tier, typical user
SOFTWARE = [
    # DWG-CAD Family
    {"slug": "autocad", "name": "AutoCAD", "category": "DWG-CAD", "focus": "2D/3D drafting", "pricing": "Subscription ($1,865/yr)", "user": "Architects, engineers, drafters", "strengths": ["Industry standard DWG format", "Extensive command ecosystem", "AutoLISP/VBA scripting", "Massive third-party plugin library"]},
    {"slug": "gstarcad", "name": "GstarCAD", "category": "DWG-CAD", "focus": "2D/3D drafting", "pricing": "Perpetual + subscription options", "user": "Cost-conscious firms, government, education", "strengths": ["DWG-native compatibility", "Ultra-low memory footprint", "Fast file open speed", "AutoLISP & .NET API support", "Perpetual licensing available"]},
    {"slug": "zwcad", "name": "ZWCAD", "category": "DWG-CAD", "focus": "2D/3D drafting", "pricing": "Perpetual + subscription", "user": "SMBs, education, government", "strengths": ["DWG-native editing", "Smart Voice annotation", "Flexible API (LISP, .NET, ZRX)", "Low system requirements"]},
    {"slug": "bricscad", "name": "BricsCAD", "category": "DWG-CAD", "focus": "2D/3D + BIM", "pricing": "Perpetual licenses", "user": "Multi-discipline firms", "strengths": ["DWG-native with BIM capabilities", "AI-assisted modeling", "Sheet metal + mechanical", "Perpetual licensing"]},
    {"slug": "draftsight", "name": "DraftSight", "category": "DWG-CAD", "focus": "2D drafting", "pricing": "Subscription", "user": "SOLIDWORKS ecosystem users", "strengths": ["Part of Dassault ecosystem", "DWG/DXF native", "Batch processing tools", "3D modeling capabilities"]},
    {"slug": "ares-commander", "name": "ARES Commander", "category": "DWG-CAD", "focus": "Cross-platform DWG", "pricing": "Subscription + perpetual", "user": "Cross-platform teams", "strengths": ["Trinity concept (Desktop+Touch+Kudo)", "Cross-platform (Win/Mac/Linux)", "DWG-native editing", "Cloud collaboration"]},

    # BIM Family
    {"slug": "revit", "name": "Revit", "category": "BIM", "focus": "Building Information Modeling", "pricing": "Subscription ($2,835/yr)", "user": "Architects, structural engineers, MEP", "strengths": ["Industry-standard BIM", "Parametric families", "Multi-discipline coordination", "Dynamo visual scripting"]},
    {"slug": "archicad", "name": "ArchiCAD", "category": "BIM", "focus": "Architectural BIM", "pricing": "Subscription + perpetual", "user": "Architects, small practices", "strengths": ["OpenBIM/IFC native", "Morph modeling tool", "Teamwork server", "Algorithmic design (Param-O)"]},
    {"slug": "allplan", "name": "Allplan", "category": "BIM", "focus": "AEC BIM", "pricing": "Subscription", "user": "Structural engineers, precast", "strengths": ["Precast concrete detailing", "Reinforcement modeling", "Bridge/infrastructure BIM", "openBIM certified"]},
    {"slug": "vectorworks", "name": "Vectorworks", "category": "BIM", "focus": "Design + BIM", "pricing": "Subscription + perpetual", "user": "Architects, landscape architects", "strengths": ["Integrated 2D/3D/BIM", "Landscape architecture", "Entertainment design", "Marionette scripting"]},

    # MCAD Family
    {"slug": "solidworks", "name": "SOLIDWORKS", "category": "MCAD", "focus": "Mechanical 3D CAD", "pricing": "Perpetual + subscription", "user": "Product designers, mechanical engineers", "strengths": ["Parametric solid modeling", "Simulation integrated", "PDM/PLM ecosystem", "Massive user community"]},
    {"slug": "catia", "name": "CATIA", "category": "MCAD", "focus": "Advanced surface/solid", "pricing": "Enterprise licensing", "user": "Aerospace, automotive OEMs", "strengths": ["Class-A surfacing", "Large assembly performance", "Systems engineering", "3DEXPERIENCE platform"]},
    {"slug": "creo-parametric", "name": "Creo Parametric", "category": "MCAD", "focus": "Mechanical CAD", "pricing": "Subscription", "user": "Discrete manufacturing", "strengths": ["Parametric & direct modeling", "Generative design", "AR/IoT integration", "Windchill PLM integration"]},
    {"slug": "siemens-nx", "name": "Siemens NX", "category": "MCAD", "focus": "Advanced mechanical", "pricing": "Enterprise licensing", "user": "Aerospace, automotive, industrial", "strengths": ["Synchronous technology", "Integrated CAM", "Convergent modeling", "Teamcenter integration"]},
    {"slug": "fusion-360", "name": "Fusion 360", "category": "MCAD", "focus": "Cloud CAD/CAM", "pricing": "Subscription ($545/yr)", "user": "Startups, makers, students", "strengths": ["Cloud-native collaboration", "Integrated CAD/CAM/CAE", "Generative design", "Accessible pricing"]},
    {"slug": "inventor", "name": "Inventor", "category": "MCAD", "focus": "Mechanical design", "pricing": "Subscription", "user": "Manufacturing engineers", "strengths": ["iLogic automation", "Frame generator", "Tube & pipe routing", "Vault integration"]},
    {"slug": "solid-edge", "name": "Solid Edge", "category": "MCAD", "focus": "Mechanical design", "pricing": "Subscription + perpetual", "user": "Mid-market manufacturing", "strengths": ["Synchronous technology", "Convergent modeling", "Integrated simulation", "Cloud collaboration"]},
    {"slug": "onshape", "name": "Onshape", "category": "MCAD", "focus": "Cloud-native CAD", "pricing": "Subscription ($1,500/yr)", "user": "Distributed teams, education", "strengths": ["Fully cloud-native", "Real-time collaboration", "Version control built-in", "No file management"]},

    # Visualization
    {"slug": "blender", "name": "Blender", "category": "Visualization", "focus": "3D creation suite", "pricing": "Free & open-source", "user": "Artists, architects, game devs", "strengths": ["Cycles/EEVEE renderers", "Sculpting + animation", "Open-source community", "BlenderBIM add-on"]},
    {"slug": "3dsmax", "name": "3ds Max", "category": "Visualization", "focus": "3D visualization", "pricing": "Subscription", "user": "Viz artists, game devs, architects", "strengths": ["Arnold renderer", "Polygonal modeling", "Animation tools", "MAXScript automation"]},
    {"slug": "sketchup", "name": "SketchUp", "category": "Visualization", "focus": "Conceptual 3D", "pricing": "Freemium + subscription", "user": "Architects, interior designers", "strengths": ["Intuitive push-pull", "3D Warehouse models", "Quick conceptual design", "Extension ecosystem"]},
    {"slug": "rhinoceros", "name": "Rhino", "category": "Visualization", "focus": "NURBS modeling", "pricing": "Perpetual ($995)", "user": "Industrial designers, architects", "strengths": ["NURBS precision", "Grasshopper parametric", "SubD modeling", "Plugin ecosystem (V-Ray, etc.)"]},

    # Civil
    {"slug": "civil-3d", "name": "Civil 3D", "category": "Civil", "focus": "Civil infrastructure", "pricing": "Subscription", "user": "Civil engineers, land surveyors", "strengths": ["Corridor modeling", "Grading tools", "Pipe networks", "Survey data management"]},
    {"slug": "microstation", "name": "MicroStation", "category": "Civil", "focus": "Infrastructure design", "pricing": "Subscription", "user": "DOTs, infrastructure firms", "strengths": ["DGN format", "Large model handling", "iTwin platform", "ProjectWise integration"]},

    # Simulation
    {"slug": "ansys-mechanical", "name": "ANSYS Mechanical", "category": "Simulation", "focus": "Structural FEA", "pricing": "Enterprise licensing", "user": "Simulation engineers", "strengths": ["Advanced FEA solver", "Multi-physics coupling", "Parametric studies", "HPC scaling"]},
    {"slug": "abaqus", "name": "ABAQUS", "category": "Simulation", "focus": "FEA/explicit dynamics", "pricing": "Enterprise licensing", "user": "Aerospace, automotive R&D", "strengths": ["Explicit dynamics", "Non-linear analysis", "UMAT subroutines", "Contact mechanics"]},

    # Open Source
    {"slug": "freecad", "name": "FreeCAD", "category": "Open-Source", "focus": "Parametric 3D", "pricing": "Free & open-source", "user": "Hobbyists, students, SMBs", "strengths": ["Fully open-source", "Workbench architecture", "Python scripting", "Active community"]},
]

# Define comparison pairs (high search volume combinations)
COMPARISONS = [
    # DWG-CAD vs DWG-CAD
    ("autocad", "gstarcad"), ("autocad", "zwcad"), ("autocad", "bricscad"),
    ("autocad", "draftsight"), ("autocad", "ares-commander"),
    ("gstarcad", "zwcad"), ("gstarcad", "bricscad"), ("gstarcad", "ares-commander"),
    ("zwcad", "bricscad"), ("bricscad", "ares-commander"),
    # BIM vs BIM
    ("revit", "archicad"), ("revit", "allplan"), ("revit", "vectorworks"),
    ("archicad", "allplan"), ("archicad", "vectorworks"),
    # MCAD vs MCAD
    ("solidworks", "catia"), ("solidworks", "creo-parametric"), ("solidworks", "siemens-nx"),
    ("solidworks", "fusion-360"), ("solidworks", "inventor"), ("solidworks", "onshape"),
    ("solidworks", "solid-edge"),
    ("catia", "siemens-nx"), ("catia", "creo-parametric"),
    ("creo-parametric", "siemens-nx"), ("fusion-360", "onshape"),
    ("fusion-360", "inventor"), ("inventor", "solid-edge"),
    ("siemens-nx", "solid-edge"),
    # Cross-category (high search volume)
    ("autocad", "revit"), ("autocad", "solidworks"), ("autocad", "sketchup"),
    ("revit", "archicad"), ("revit", "sketchup"),
    ("solidworks", "fusion-360"), ("solidworks", "freecad"),
    ("blender", "3dsmax"), ("blender", "sketchup"), ("blender", "rhinoceros"),
    ("sketchup", "rhinoceros"), ("rhinoceros", "solidworks"),
    ("autocad", "microstation"), ("civil-3d", "microstation"),
    ("autocad", "freecad"), ("fusion-360", "freecad"),
    ("solidworks", "catia"), ("ansys-mechanical", "abaqus"),
    # GstarCAD cross-category
    ("gstarcad", "autocad"), ("gstarcad", "draftsight"),
    # Additional high-value
    ("onshape", "solidworks"), ("catia", "inventor"),
    ("3dsmax", "sketchup"), ("blender", "freecad"),
    ("autocad", "fusion-360"), ("revit", "allplan"),
]

# Deduplicate (A vs B == B vs A)
seen = set()
unique_comparisons = []
for a, b in COMPARISONS:
    key = tuple(sorted([a, b]))
    if key not in seen:
        seen.add(key)
        unique_comparisons.append((a, b))

SW_MAP = {s["slug"]: s for s in SOFTWARE}


def generate_comparison_page(slug_a, slug_b):
    """Generate a comparison page HTML."""
    a = SW_MAP[slug_a]
    b = SW_MAP[slug_b]
    
    page_slug = f"{slug_a}-vs-{slug_b}"
    title = f"{a['name']} vs {b['name']} — Feature Comparison & Differences | Gstarcademy"
    description = f"Detailed comparison of {a['name']} and {b['name']}: pricing, features, use cases, and performance differences. Find which {a['category']} software fits your workflow."
    canonical = f"https://gstarcademy.com/kb/compare/{page_slug}"
    
    # Determine comparison context
    same_category = a["category"] == b["category"]
    category_label = a["category"] if same_category else f"{a['category']} / {b['category']}"
    
    # Build strengths comparison rows
    def strength_rows(sw):
        return "\n".join(f'                      <li>{s}</li>' for s in sw["strengths"])
    
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
    <title>{title}</title>
    <meta name="description" content="{description}" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <link rel="canonical" href="{canonical}" />
    <meta property="og:image" content="https://gstarcademy.com/images/og-default.webp" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{a['name']} vs {b['name']} — Software Comparison" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:site_name" content="Gstarcademy" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{a['name']} vs {b['name']} — Software Comparison" />
    <meta name="twitter:description" content="{description}" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="preload" href="../../styles.min.css" as="style" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />
    <link rel="stylesheet" href="../../styles.min.css" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{a['name']} vs {b['name']}","description":"{description}","url":"{canonical}","datePublished":"{TODAY}","dateModified":"{TODAY}","inLanguage":"en","isPartOf":{{"@type":"WebSite","name":"Gstarcademy","url":"https://gstarcademy.com"}},"mainEntityOfPage":"{canonical}","author":{{"@type":"Organization","name":"Gstarcademy Editorial Team","url":"https://gstarcademy.com/about"}},"publisher":{{"@type":"Organization","name":"Gstarcademy","url":"https://gstarcademy.com/","logo":{{"@type":"ImageObject","url":"https://gstarcademy.com/favicon.svg"}}}}}}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://gstarcademy.com/"}},{{"@type":"ListItem","position":2,"name":"Knowledge Base","item":"https://gstarcademy.com/knowledge-base"}},{{"@type":"ListItem","position":3,"name":"Comparisons","item":"https://gstarcademy.com/kb/compare/"}},{{"@type":"ListItem","position":4,"name":"{a['name']} vs {b['name']}","item":"{canonical}"}}]}}</script>
    <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{{"@type": "Question", "name": "What is the main difference between {a['name']} and {b['name']}?", "acceptedAnswer": {{"@type": "Answer", "text": "{a['name']} focuses on {a['focus']} and is primarily used by {a['user']}. {b['name']} focuses on {b['focus']} and is primarily used by {b['user']}. They differ in pricing model, feature depth, and target workflow."}}}}, {{"@type": "Question", "name": "Is {a['name']} or {b['name']} better for beginners?", "acceptedAnswer": {{"@type": "Answer", "text": "The better choice depends on your industry and budget. {a['name']} ({a['pricing']}) is standard in {a['category']} workflows, while {b['name']} ({b['pricing']}) offers {b['strengths'][0].lower()}. Consider which ecosystem your team or employer uses."}}}}, {{"@type": "Question", "name": "Can {a['name']} files be opened in {b['name']}?", "acceptedAnswer": {{"@type": "Answer", "text": "File interoperability depends on the format. {'Both support DWG natively, so files transfer directly.' if 'DWG' in str(a.get('strengths','')) and 'DWG' in str(b.get('strengths','')) else 'Standard exchange formats like STEP, IGES, IFC, or DXF enable cross-software file sharing, though some parametric data may be lost in translation.'}"}}}}]}}</script>
  </head>
  <body>
    <div class="page-shell">
      <aside class="env-banner" role="alert" aria-live="polite" hidden>
        <div class="container env-banner-inner">
          <span class="env-banner-text" id="env-banner-msg"></span>
          <button class="env-banner-close" aria-label="Dismiss">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      </aside>
      <header class="topbar">
        <div class="container topbar-inner">
          <a class="brand" href="../../">
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
                <span class="nav-close-icon">\u00d7</span>
              </button>
            </div>
            <a class="nav-link" data-nav="home" href="../../">Home</a>
            <a class="nav-link active" data-nav="knowledge" href="../../knowledge-base">Wiki</a>
            <a class="nav-link" data-nav="tutorials" href="../../tutorials">Tutorials</a>
            <a class="nav-link" data-nav="news" href="../../news">News</a>
            <a class="nav-link" data-nav="about" href="../../about">About</a>
          </nav>
        </div>
        <div class="nav-overlay" aria-hidden="true"></div>
      </header>
    </div>

    <main class="container" style="margin-top: 32px; max-width: 920px;">
      <nav class="kb-faq-breadcrumbs" aria-label="Breadcrumb">
        <a href="../../">Home</a> /
        <a href="../../knowledge-base">Knowledge Base</a> /
        <a href="./">Comparisons</a> /
        <span aria-current="page">{a['name']} vs {b['name']}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 28px;">
          <span class="chip pill-warn">Software Comparison \u00b7 {category_label}</span>
          <h1 style="margin-top: 12px;">{a['name']} vs {b['name']}</h1>
          <p class="hero-sub">A structured comparison of {a['name']} and {b['name']} for professionals evaluating {a['category'] if same_category else 'CAD'} software options.</p>
        </header>

        <div class="ink-byline" role="contentinfo">
          <span><strong>By</strong> Gstarcademy Editorial Team</span>
          <span><strong>Updated</strong> <time datetime="{TODAY}">{TODAY}</time></span>
          <span><a href="../../editorial-process">Editorial process</a></span>
        </div>

        <section class="kb-concept-section">
          <h2>Overview</h2>
          <p><strong><a href="../software/{slug_a}">{a['name']}</a></strong> and <strong><a href="../software/{slug_b}">{b['name']}</a></strong> are both established tools in the {category_label} space, but they serve different market segments and design philosophies. This comparison breaks down their key differences to help you make an informed decision.</p>
          <p>{a['name']} is focused on <em>{a['focus']}</em> and is primarily used by {a['user']}. {b['name']} focuses on <em>{b['focus']}</em> and targets {b['user']}. Understanding these distinctions is critical before committing to a software ecosystem that may define your workflow for years.</p>
        </section>

        <section class="kb-concept-section">
          <h2>Quick Comparison Table</h2>
          <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 16px;">
              <thead>
                <tr style="background: var(--ink-surface-2); border-bottom: 2px solid var(--ink-line);">
                  <th style="padding: 12px 16px; text-align: left; font-weight: 700;">Criteria</th>
                  <th style="padding: 12px 16px; text-align: left; font-weight: 700;">{a['name']}</th>
                  <th style="padding: 12px 16px; text-align: left; font-weight: 700;">{b['name']}</th>
                </tr>
              </thead>
              <tbody>
                <tr style="border-bottom: 1px solid var(--ink-line);">
                  <td style="padding: 10px 16px; font-weight: 600;">Primary Focus</td>
                  <td style="padding: 10px 16px;">{a['focus']}</td>
                  <td style="padding: 10px 16px;">{b['focus']}</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--ink-line); background: var(--ink-surface-2);">
                  <td style="padding: 10px 16px; font-weight: 600;">Pricing</td>
                  <td style="padding: 10px 16px;">{a['pricing']}</td>
                  <td style="padding: 10px 16px;">{b['pricing']}</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--ink-line);">
                  <td style="padding: 10px 16px; font-weight: 600;">Target Users</td>
                  <td style="padding: 10px 16px;">{a['user']}</td>
                  <td style="padding: 10px 16px;">{b['user']}</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--ink-line); background: var(--ink-surface-2);">
                  <td style="padding: 10px 16px; font-weight: 600;">Category</td>
                  <td style="padding: 10px 16px;">{a['category']}</td>
                  <td style="padding: 10px 16px;">{b['category']}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section class="kb-concept-section">
          <h2>{a['name']} — Key Strengths</h2>
          <p>{a['name']} ({a['pricing']}) excels in {a['focus']} workflows. It is the preferred choice for {a['user']} who need:</p>
          <ul>
{strength_rows(a)}
          </ul>
          <p>Learn more: <a href="../software/{slug_a}">{a['name']} software profile \u2192</a></p>
        </section>

        <section class="kb-concept-section">
          <h2>{b['name']} — Key Strengths</h2>
          <p>{b['name']} ({b['pricing']}) excels in {b['focus']} workflows. It is the preferred choice for {b['user']} who need:</p>
          <ul>
{strength_rows(b)}
          </ul>
          <p>Learn more: <a href="../software/{slug_b}">{b['name']} software profile \u2192</a></p>
        </section>

        <section class="kb-concept-section">
          <h2>When to Choose {a['name']}</h2>
          <p>Choose {a['name']} if your primary requirements include:</p>
          <ul>
            <li>Your team or industry standard is built around the {a['category']} ecosystem</li>
            <li>You need {a['strengths'][0].lower()} as a core capability</li>
            <li>Your workflow involves {a['focus']} as the primary design activity</li>
            <li>Budget allows for {a['pricing'].lower()} pricing</li>
          </ul>
        </section>

        <section class="kb-concept-section">
          <h2>When to Choose {b['name']}</h2>
          <p>Choose {b['name']} if your primary requirements include:</p>
          <ul>
            <li>Your team or industry standard is built around the {b['category']} ecosystem</li>
            <li>You need {b['strengths'][0].lower()} as a core capability</li>
            <li>Your workflow involves {b['focus']} as the primary design activity</li>
            <li>Budget allows for {b['pricing'].lower()} pricing</li>
          </ul>
        </section>

        <section class="kb-concept-section">
          <h2>File Compatibility &amp; Interoperability</h2>
          <p>When evaluating {a['name']} vs {b['name']}, file exchange is a key consideration:</p>
          <ul>
            <li><strong>Native formats:</strong> Each software uses its own native file format optimized for internal performance</li>
            <li><strong>Exchange formats:</strong> {'DWG/DXF files can be shared directly between both platforms' if a['category'] == 'DWG-CAD' and b['category'] == 'DWG-CAD' else 'Standard exchange formats (STEP, IGES, IFC, DXF) enable cross-software workflows'}</li>
            <li><strong>Data loss considerations:</strong> Parametric history, custom properties, and software-specific features may not transfer between platforms</li>
            <li><strong>Collaboration strategy:</strong> For mixed environments, establish a neutral exchange format protocol early in the project lifecycle</li>
          </ul>
        </section>

        <section class="kb-concept-section">
          <h2>Verdict &amp; Recommendation</h2>
          <p>Both {a['name']} and {b['name']} are capable tools with distinct advantages. The right choice depends on your specific context:</p>
          <ul>
            <li><strong>For {a['user'].split(',')[0].strip().lower()}:</strong> {a['name']} offers a mature ecosystem with {a['strengths'][0].lower()}</li>
            <li><strong>For {b['user'].split(',')[0].strip().lower()}:</strong> {b['name']} provides {b['strengths'][0].lower()} as its primary differentiator</li>
            <li><strong>For teams transitioning:</strong> Consider trial periods with both and evaluate based on your actual project files and workflows</li>
          </ul>
          <p>We recommend testing both platforms with your actual production files before committing to a multi-year licensing decision.</p>
        </section>

        <section style="margin-top: 36px; padding: 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 16px;">
          <h2 style="font-size: 1.3rem; font-weight: 700; color: var(--ink-text); margin-bottom: 12px;">&#128279; Related Comparisons</h2>
          <div style="display: flex; flex-wrap: wrap; gap: 8px;">'''
    
    # Add links to related comparisons
    related = []
    for ca, cb in unique_comparisons:
        if (ca, cb) == (slug_a, slug_b):
            continue
        if ca == slug_a or cb == slug_a or ca == slug_b or cb == slug_b:
            related.append((ca, cb))
    
    for ca, cb in related[:8]:
        na = SW_MAP[ca]["name"]
        nb = SW_MAP[cb]["name"]
        html += f'\n            <a href="./{ca}-vs-{cb}" style="display: inline-block; padding: 8px 14px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 8px; text-decoration: none; color: var(--ink-text); font-size: 13px; font-weight: 500;">{na} vs {nb}</a>'
    
    html += f'''
          </div>
        </section>

        <aside style="margin-top: 32px; padding: 20px 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 14px; display: flex; gap: 16px; align-items: flex-start; flex-wrap: wrap;" aria-label="Editorial information">
          <div style="flex: 1; min-width: 200px;">
            <p style="font-size: 12px; font-weight: 600; color: var(--ink-text); margin: 0 0 4px;">Written by Gstarcademy Editorial Team</p>
            <p style="font-size: 11px; color: var(--ink-text-soft); margin: 0;">Technically reviewed by domain specialists. Content follows our <a href="../../editorial-process" style="color: var(--accent); text-decoration: underline;">editorial guidelines</a>.</p>
          </div>
          <div style="text-align: right; min-width: 140px;">
            <p style="font-size: 11px; color: var(--ink-text-soft); margin: 0;">Last updated</p>
            <time datetime="{TODAY}" style="font-size: 12px; font-weight: 600; color: var(--ink-text);">{TODAY}</time>
          </div>
        </aside>

        <p class="meta" style="margin-top: 36px; font-size: 12px;">Article text is original editorial content by Gstarcademy. Software names and trademarks belong to their respective owners. Pricing information is approximate and subject to change; verify with vendor for current rates.</p>
      </article>
    </main>

    <footer class="footer site-footer">
      <div class="container site-footer-inner">
        <div class="site-footer-brand">
          <p class="site-footer-tagline">Gstarcademy</p>
          <p class="site-footer-desc">CAD knowledge base and tutorial navigation.</p>
        </div>
      </div>
      <div class="container site-footer-bottom">
        <p>\u00a9 <span id="footer-year"></span> Gstarcademy. All rights reserved.</p>
      </div>
    </footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    
    return page_slug, html


def main():
    print(f"Generating {len(unique_comparisons)} comparison pages...")
    generated = 0
    
    for slug_a, slug_b in unique_comparisons:
        if slug_a not in SW_MAP or slug_b not in SW_MAP:
            print(f"  Skipping {slug_a} vs {slug_b} (missing data)")
            continue
        
        page_slug, html = generate_comparison_page(slug_a, slug_b)
        filepath = os.path.join(OUTPUT_DIR, f"{page_slug}.html")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        generated += 1
    
    # Generate index page
    generate_index()
    print(f"\n✅ Generated {generated} comparison pages + index")


def generate_index():
    """Generate the comparison index page."""
    categories = {}
    for slug_a, slug_b in unique_comparisons:
        if slug_a not in SW_MAP or slug_b not in SW_MAP:
            continue
        a, b = SW_MAP[slug_a], SW_MAP[slug_b]
        cat = a["category"] if a["category"] == b["category"] else "Cross-Category"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((slug_a, slug_b, a["name"], b["name"]))
    
    links_html = ""
    for cat, pairs in sorted(categories.items()):
        links_html += f'<h3 style="margin-top: 24px; font-size: 1rem; font-weight: 700;">{cat}</h3>\n<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px;">\n'
        for sa, sb, na, nb in pairs:
            links_html += f'  <a href="./{sa}-vs-{sb}" style="display: inline-block; padding: 8px 14px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 8px; text-decoration: none; color: var(--ink-text); font-size: 13px; font-weight: 500;">{na} vs {nb}</a>\n'
        links_html += '</div>\n'
    
    index_html = f'''<!doctype html>
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
    <title>CAD Software Comparisons — Head-to-Head Feature Analysis | Gstarcademy</title>
    <meta name="description" content="Compare CAD, BIM, and engineering software side by side. Detailed feature, pricing, and workflow comparisons for AutoCAD, SOLIDWORKS, Revit, GstarCAD, Fusion 360, and 25+ more tools." />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <link rel="canonical" href="https://gstarcademy.com/kb/compare/" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="CAD Software Comparisons" />
    <meta property="og:description" content="Compare CAD, BIM, and engineering software side by side." />
    <meta property="og:url" content="https://gstarcademy.com/kb/compare/" />
    <meta property="og:site_name" content="Gstarcademy" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="preload" href="../../styles.min.css" as="style" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />
    <link rel="stylesheet" href="../../styles.min.css" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"CAD Software Comparisons","description":"Head-to-head comparisons of CAD, BIM, and engineering software.","url":"https://gstarcademy.com/kb/compare/"}}</script>
  </head>
  <body>
    <div class="page-shell">
      <header class="topbar">
        <div class="container topbar-inner">
          <a class="brand" href="../../">
            <span class="brand-badge">GC</span>
            <span>Gstarcademy</span>
          </a>
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
        <span aria-current="page">Software Comparisons</span>
      </nav>

      <h1 style="margin-top: 16px;">CAD Software Comparisons</h1>
      <p style="font-size: 15px; color: var(--ink-text-soft); margin-bottom: 32px;">Side-by-side feature, pricing, and workflow comparisons across {len(unique_comparisons)} software pairings. Each comparison provides structured analysis to help you evaluate options for your specific needs.</p>

      {links_html}
    </main>

    <footer class="footer site-footer">
      <div class="container site-footer-inner">
        <div class="site-footer-brand">
          <p class="site-footer-tagline">Gstarcademy</p>
          <p class="site-footer-desc">CAD knowledge base and tutorial navigation.</p>
        </div>
      </div>
      <div class="container site-footer-bottom">
        <p>\u00a9 <span id="footer-year"></span> Gstarcademy. All rights reserved.</p>
      </div>
    </footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)


if __name__ == '__main__':
    main()
