#!/usr/bin/env python3
"""
Rewrite all guide pages with comprehensive beginner-level comparisons,
decision matrices, milestone project walkthroughs, and hardware specifications.
"""

import os
from datetime import date
from bs4 import BeautifulSoup

TODAY = date.today().isoformat()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'guides')
os.makedirs(OUTPUT_DIR, exist_ok=True)

GUIDES = [
    {
        "slug": "best-cad-architecture",
        "title": "Best CAD & BIM Software for Architecture Beginners in 2026",
        "desc": "Compare top architectural design software: SketchUp, Revit, ArchiCAD, and Vectorworks. In-depth analysis of learning curves, free student tiers, hardware requirements, and career value.",
        "category": "Architecture",
        "software": [("sketchup", "SketchUp"), ("revit", "Revit"), ("archicad", "ArchiCAD"), ("vectorworks", "Vectorworks")],
        "intro": "Starting your architectural design journey requires choosing between intuitive 3D conceptual modeling and comprehensive Building Information Modeling (BIM). This guide breaks down the four leading architectural platforms for complete beginners, covering ease of learning, software licensing, hardware demands, and career employability.",
        "factors": [
            "Learning Curve — How many weeks until you can produce an accurate 3D floor plan?",
            "BIM Intelligence — Does the software generate automated schedules and elevations?",
            "Cost & Licensing — Are there free web tiers or student educational licenses?",
            "Industry Employment — Is the skill required in corporate architecture and engineering firms?",
            "Hardware Requirements — Can it run on a standard laptop or does it require a dedicated workstation?"
        ],
        "sw_matrix": [
            ("SketchUp", "Beginner (1-2 weeks)", "Free Web / $119/yr", "Rapid conceptual massing, interior design, client presentations", "Limited 2D detailing"),
            ("Revit", "Steep (2-3 months)", "Free for Students / ~$2,800/yr", "Full parametric BIM, multi-discipline clash coordination, CD sets", "High hardware requirements"),
            ("ArchiCAD", "Moderate (1-2 months)", "Free for Students / Subscription", "Intuitive BIM workflow, strong European adoption, team collaboration", "Smaller US plugin ecosystem"),
            ("Vectorworks", "Moderate (4-6 weeks)", "Free for Students / Subscription", "Landscape architecture, entertainment/stage design, flexible graphics", "Less multi-discipline BIM usage")
        ],
        "sw_notes": [
            ("SketchUp", "SketchUp is the most approachable 3D modeling tool for beginners. Using push-pull modeling, you can draft building massing studies and interior layouts within days. The free web tier allows instant browser-based experimentation, while the 3D Warehouse gives access to millions of pre-built furniture and appliance components."),
            ("Revit", "Autodesk Revit is the undisputed enterprise standard for Building Information Modeling (BIM). Rather than drawing static lines, you place intelligent parametric walls, doors, and structural beams. Modifying a floor plan automatically updates all corresponding sections, elevations, and door schedules across your construction document set."),
            ("ArchiCAD", "Graphisoft ArchiCAD is a mature, highly refined BIM platform renowned for its smooth user experience and efficient background processing. It excels at architectural visualization and handles large building geometry fluidly, making it particularly popular among boutique design studios and European firms."),
            ("Vectorworks", "Vectorworks Architecture offers exceptional 2D graphic presentation alongside capable 3D BIM modeling. It gives architects tremendous artistic flexibility for conceptual sketches, site modeling, and landscape integration without the strict rigidity of traditional BIM tools.")
        ],
        "project_walkthrough": "Your First Beginner Milestone Project: Model a 2-Story Modern Residential Villa. Week 1: Import a 2D floor plan sketch, trace exterior 300mm masonry walls, and insert standard doors/windows. Week 2: Add second-floor structural slab, stairs, and a flat roof with parapets. Week 3: Place interior furniture, apply textures, and generate an exported PDF sheet set with dimensions.",
        "hardware_specs": "Recommended PC Specs: 6-Core Intel Core i7 / AMD Ryzen 7, 32 GB RAM, 1 TB NVMe SSD, and NVIDIA RTX 3060 / 4060 GPU with 8GB+ VRAM for smooth BIM viewport rendering.",
        "recommendation": "For complete beginners wanting fast 3D concepts: Start with SketchUp. For architecture students aiming for design firm careers: Invest early in Revit with a free student license. For European practice or design-oriented studios: ArchiCAD offers the best balance of speed and BIM rigor."
    },
    {
        "slug": "best-cad-mechanical-design",
        "title": "Best CAD Software for Mechanical Design & Product Engineering in 2026",
        "desc": "Compare beginner-friendly mechanical 3D CAD platforms: Fusion 360, SOLIDWORKS, FreeCAD, and Onshape. Evaluate parametric modeling, CNC/CAM, 3D printing workflows, and career demand.",
        "category": "Mechanical Engineering",
        "software": [("fusion-360", "Fusion 360"), ("solidworks", "SOLIDWORKS"), ("freecad", "FreeCAD"), ("onshape", "Onshape")],
        "intro": "Mechanical computer-aided design (MCAD) requires building mathematically exact 3D solid models, constrained mechanical assemblies, and fabrication drawings. This comprehensive guide compares the premier MCAD options for students, makers, and aspiring product engineers.",
        "factors": [
            "Parametric Reliability — Does the feature tree allow robust history-based edits?",
            "Integrated Manufacturing — Does it support 3D printing slicing and CNC CAM toolpaths?",
            "Cloud vs. Desktop — Does it require local workstation installation or run in the browser?",
            "Job Market Value — What percentage of mechanical engineering job listings require the tool?",
            "Pricing Freedom — Is there an unrestricted free or open-source tier?"
        ],
        "sw_matrix": [
            ("Fusion 360", "Beginner (2-4 weeks)", "Free Personal / $680/yr", "Integrated CAD/CAM/CAE, generative design, rapid prototyping", "Cloud file dependency"),
            ("SOLIDWORKS", "Moderate (1-2 months)", "Student ~$99/yr / Perpetual", "Industry-standard mechanical assemblies, sheet metal, GD&T drawings", "Windows-only, high cost"),
            ("FreeCAD", "Moderate (4-6 weeks)", "100% Free Open-Source", "Offline privacy, zero licensing cost, deep Python scriptability", "Less polished UI"),
            ("Onshape", "Beginner (2-3 weeks)", "Free Public / $1,500/yr", "Browser-native real-time co-authoring, version branching, tablet use", "Public files on free tier")
        ],
        "sw_notes": [
            ("Fusion 360", "Autodesk Fusion 360 combines 3D parametric modeling, organic T-Splines sculpting, multi-axis CAM milling, and cloud simulation in a single accessible subscription. Its free personal tier makes it the ultimate platform for 3D printing enthusiasts, hardware startups, and maker spaces."),
            ("SOLIDWORKS", "Dassault Systèmes SOLIDWORKS is the mechanical engineering industry benchmark. Dominating automotive, aerospace, and industrial equipment sectors, it provides unmatched large assembly management (10,000+ parts), advanced sheet metal unfolding, weldments, and ASME Y14.5 drafting detailing."),
            ("FreeCAD", "FreeCAD is the premier open-source parametric modeler. Built on OpenCASCADE and fully extensible via Python, FreeCAD 1.0 delivers robust topological naming stability. It runs offline on Windows, macOS, and Linux, making it ideal for privacy-conscious engineers."),
            ("Onshape", "Created by the original founders of SOLIDWORKS, Onshape is cloud-native CAD that runs inside Chrome/Firefox without installation. It features live Google Docs-style multi-user editing, automated revision tracking, and zero risk of lost files or software crashes.")
        ],
        "project_walkthrough": "Your First Beginner Milestone Project: Design an Adjustable Centrifugal Water Pump. Week 1: Model the impeller using parametric sketches, circular patterns, and revolve features. Week 2: Model the two-piece pump housing with mounting flanges and O-ring seal grooves. Week 3: Assemble components with concentric/coincident mates, check for interference, and export STEP files for CNC machining.",
        "hardware_specs": "Recommended PC Specs: 8-Core Intel Core i7 / AMD Ryzen 7, 32 GB DDR5 RAM, 1 TB PCIe 4.0 SSD, NVIDIA RTX 4060 or workstation GPU.",
        "recommendation": "For makers, inventors, and 3D printing: Choose Fusion 360 Free. For mechanical engineering students targeting manufacturing jobs: Master SOLIDWORKS. For open-source purists and Linux users: FreeCAD 1.0 is unbeatable."
    },
    {
        "slug": "best-cad-civil-engineering",
        "title": "Best CAD & DTM Software for Civil Infrastructure & Surveying in 2026",
        "desc": "Compare top civil engineering design software: Autodesk Civil 3D, Bentley MicroStation/OpenRoads, and AutoCAD. Analysis of road geometry, DTM surfaces, earthworks, and GIS integration.",
        "category": "Civil Engineering",
        "software": [("civil-3d", "Civil 3D"), ("microstation", "MicroStation"), ("autocad", "AutoCAD")],
        "intro": "Civil infrastructure engineering demands high-precision geographic coordinate systems, digital terrain modeling (DTM), corridor road profiles, and underground utility networks. Here is how the top civil software stacks compare for students and practicing civil technologists.",
        "factors": [
            "Terrain Surface Capacity — Can it handle millions of LiDAR survey points smoothly?",
            "Corridor & Road Dynamics — Do cross-sections and earthwork volumes update dynamically?",
            "GIS & Georeferencing — Does it support global EPSG coordinate projection transforms?",
            "DOT & Agency Standards — Which software is mandated by regional transportation departments?"
        ],
        "sw_matrix": [
            ("Civil 3D", "Steep (2-3 months)", "Free for Students / Subscription", "Dynamic road corridors, pipe networks, grading optimization, LandXML", "Heavy resource consumption"),
            ("MicroStation", "Moderate (1-2 months)", "Subscription / Enterprise", "Large highway infrastructure, DOT standards (US/UK), 3D DGN files", "Steeper UI transition"),
            ("AutoCAD", "Beginner (2-4 weeks)", "Free for Students / Subscription", "2D civil boundary drafting, subdivision plats, detail sheets", "No dynamic 3D surface modeling")
        ],
        "sw_notes": [
            ("Civil 3D", "Built on top of the AutoCAD engine, Autodesk Civil 3D is the standard for site development, transportation corridors, and stormwater grading. When alignment geometry is modified, all connected profiles, cross sections, and earthwork cut/fill volumes update dynamically."),
            ("MicroStation", "Bentley MicroStation and OpenRoads Designer are industry giants across state Departments of Transportation (DOTs), major rail networks, and heavy civil civil infrastructure projects. Its 64-bit DGN graphics engine handles massive geographic data sets with exceptional speed."),
            ("AutoCAD", "Standard AutoCAD is the foundational 2D drafting tool for boundary surveys, subdivision parcel layouts, and municipal utility schematics. Mastering AutoCAD drafting shortcuts is the essential prerequisite before advancing to Civil 3D.")
        ],
        "project_walkthrough": "Your First Beginner Milestone Project: Subdivided Residential Access Road. Week 1: Import raw survey point groups and generate a contoured TIN terrain surface. Week 2: Lay out horizontal roadway alignment with AASHTO-compliant curves and extract vertical terrain profiles. Week 3: Model standard roadway corridor assemblies and compute net cut/fill earthwork balance.",
        "hardware_specs": "Recommended PC Specs: Fast Single-Core Clock Speed (4.0 GHz+ Intel i7/i9), 64 GB RAM for large point clouds, NVMe SSD, and 8GB+ VRAM GPU.",
        "recommendation": "Learn AutoCAD 2D drafting basics first (3 weeks), then transition directly into Civil 3D for transportation and site development careers. If targeting State DOT highway contracts, learn Bentley OpenRoads."
    },
    {
        "slug": "best-free-cad-software",
        "title": "Best Free CAD Software for Beginners in 2026: Open-Source vs Freemium",
        "desc": "Complete guide to learning CAD for zero cost: FreeCAD, Blender, Fusion 360 Personal, SketchUp Free, and Onshape. Feature limits, commercial rights, and learning curves compared.",
        "software": [("freecad", "FreeCAD"), ("blender", "Blender"), ("fusion-360", "Fusion 360 Free"), ("sketchup", "SketchUp Free"), ("onshape", "Onshape Free")],
        "category": "Free & Open Source",
        "intro": "You do not need to invest thousands of dollars in commercial software licenses to master professional computer-aided design. Multiple open-source and generous freemium tools allow you to model complex parts, architectural buildings, and 3D printable objects for free.",
        "factors": [
            "True Open-Source vs Freemium — Are there commercial monetization restrictions?",
            "Offline Freedom — Does the software require an active internet connection?",
            "Export Capabilities — Can you export standard STEP, IGES, STL, and DXF files?",
            "Ecosystem & Community — Are there comprehensive free video tutorials available?"
        ],
        "sw_matrix": [
            ("FreeCAD", "100% Free Open-Source", "Windows / Mac / Linux", "Mechanical parts, 3D printing, Python automation, parametric B-Rep", "LGPL (Full commercial use)"),
            ("Blender", "100% Free Open-Source", "Windows / Mac / Linux", "Artistic 3D sculpting, rendering, game assets, OpenBIM (BlenderBIM)", "GPL (Full commercial use)"),
            ("Fusion 360 Free", "Freemium (Personal Use)", "Windows / Mac (Cloud)", "Parametric CAD, CAM toolpaths, electronics PCB, 3D print slicing", "Non-commercial only"),
            ("Onshape Free", "Freemium (Public Tier)", "Browser (Any OS / Chromebook)", "Parametric assemblies, real-time collaboration, version branching", "All public models on free tier"),
            ("SketchUp Free", "Freemium (Web-Only)", "Browser", "Intuitive architectural massing, interior design concepts", "Non-commercial, limited export")
        ],
        "sw_notes": [
            ("FreeCAD", "FreeCAD offers 100% unrestricted commercial freedom. With modular workbenches (Part Design, Sketcher, TechDraw, FEM, CAM), it delivers full parametric engineering power without tracking accounts or cloud dependencies."),
            ("Blender", "Blender is the world's most powerful open-source creative 3D suite. While mesh-based rather than parametric, adding the CAD Sketcher and BlenderBIM addons turns Blender into a precision drafting and architectural powerhouse."),
            ("Fusion 360 Free", "Autodesk provides a generous Personal Use tier with up to 10 active editable documents, standard 2.5D CAM milling, and comprehensive STL export for hobbyist 3D printing."),
            ("Onshape Free", "Onshape's public plan gives free access to full professional-tier parametric CAD tools running directly in your web browser, making it ideal for Chromebooks and older laptops."),
            ("SketchUp Free", "The web version of SketchUp allows zero-install 3D conceptual modeling for building shapes and interior furniture layouts.")
        ],
        "project_walkthrough": "Your First Beginner Milestone Project: Parametric Smartphone Desk Stand. Week 1: Sketch profile with 15-degree viewing tilt and cable relief channel in FreeCAD/Fusion 360. Week 2: Apply parametric thickness variables (4mm wall thickness). Week 3: Export 3MF/STL mesh and 3D print the prototype.",
        "hardware_specs": "Onshape & SketchUp run on basic laptops/Chromebooks. FreeCAD, Fusion 360, and Blender require 16 GB RAM and dedicated graphics for optimal performance.",
        "recommendation": "For 3D printing & product design: Fusion 360 Personal or FreeCAD. For browser-based learning without installation: Onshape Free. For organic art & visual rendering: Blender."
    },
    {
        "slug": "best-cad-3d-printing",
        "title": "Best CAD Software for 3D Printing Beginners in 2026: FDM, SLA & STL Guide",
        "desc": "Top free and beginner-friendly CAD tools for 3D printer owners: TinkerCAD, Fusion 360, FreeCAD, and Blender. Mesh export settings, wall thickness guidelines, and tolerance tips.",
        "category": "3D Printing",
        "software": [("fusion-360", "Fusion 360"), ("freecad", "FreeCAD"), ("blender", "Blender")],
        "intro": "Transitioning from downloading pre-made 3D models on Printables or Thingiverse to designing your own custom functional parts is the most rewarding milestone in 3D printing. Here is how to select the right CAD tool for your 3D printing workflow.",
        "factors": [
            "Dimensional Precision — Can you specify exact millimeter tolerances for snap-fits and screw holes?",
            "Mesh Export Quality — Does the software output high-resolution 3MF and binary STL files?",
            "Direct Mesh Editing — Can you repair, cut, or modify imported downloaded STLs?",
            "Learning Progression — Can you start simple and progress to complex mechanical assemblies?"
        ],
        "sw_matrix": [
            ("TinkerCAD", "Absolute Beginner (1 day)", "Free Browser", "Simple geometric shapes, nameplates, basic enclosures", "Low precision"),
            ("Fusion 360", "Beginner to Pro (2-4 weeks)", "Free Personal Use", "Functional engineering parts, thread generators, snap fits, direct slicer export", "10-doc limit on free tier"),
            ("FreeCAD", "Moderate (4-6 weeks)", "100% Free Open-Source", "Parametric mechanical brackets, gears, modular replacement parts", "Slightly steeper learning curve"),
            ("Blender", "Moderate (1-2 months)", "100% Free Open-Source", "Miniatures, cosplay props, organic figurines, mesh sculpt cleanup", "Non-parametric")
        ],
        "sw_notes": [
            ("Fusion 360", "Fusion 360 is the gold standard for functional 3D printing. It features built-in ISO metric thread generators, automatic clearance offsets (0.2mm for sliding joints), and direct 'Send to 3D Print Utility' buttons linking Bambu Studio, OrcaSlicer, PrusaSlicer, and Cura."),
            ("FreeCAD", "FreeCAD excels at creating durable replacement parts for home appliances and tools. Its Part Design workbench lets you build parametric dimensions driven by spreadsheet tables for rapid sizing variations."),
            ("Blender", "If your 3D printing focus is tabletop miniatures, character sculptures, or decorative vases, Blender's dynamic sculpting brushes and 3D Print Toolbox addon are unmatched for non-manifold mesh inspection.")
        ],
        "project_walkthrough": "Your First Functional 3D Print Project: Modular Snap-Fit Battery Dispenser. Week 1: Dimension standard AA batteries (14.5mm diameter x 50.5mm length) and add 0.6mm printing clearance. Week 2: Model gravity-feed chute and snap-together interlocking dovetails. Week 3: Export as 3MF, slice with 0.2mm layer height and 3 perimeter walls for structural rigidity.",
        "hardware_specs": "Runs smoothly on modern quad-core CPUs, 16 GB RAM, and basic dedicated or integrated Intel Iris/AMD Radeon graphics.",
        "recommendation": "Start with Fusion 360 or FreeCAD for functional mechanical parts with precise dimensions. Choose Blender for organic figurines, cosplay props, and artistic sculptures."
    }
]

def generate_guide_page(g):
    canonical = f"https://gstarcademy.com/kb/guides/{g['slug']}"
    
    # 1. Comparison Matrix Table
    matrix_rows = ""
    for name, learn_curve, price, best_for, downside in g.get("sw_matrix", []):
        matrix_rows += f'''
        <tr style="border-bottom: 1px solid var(--ink-line);">
          <td style="padding: 12px 14px; font-weight: 700; color: var(--ink-text);">{name}</td>
          <td style="padding: 12px 14px; color: var(--ink-text);">{learn_curve}</td>
          <td style="padding: 12px 14px; color: var(--ink-text);">{price}</td>
          <td style="padding: 12px 14px; color: var(--ink-text);">{best_for}</td>
          <td style="padding: 12px 14px; color: var(--ink-text-soft); font-size: 13px;">{downside}</td>
        </tr>'''
        
    matrix_html = f'''
    <section class="kb-concept-section" style="margin-top: 36px;">
      <h2>Software Comparison Decision Matrix</h2>
      <div style="overflow-x: auto; margin-top: 14px;">
        <table style="width: 100%; border-collapse: collapse; background: var(--ink-surface); border: 1px solid var(--ink-line); border-radius: 8px; font-size: 13.5px;">
          <thead>
            <tr style="background: var(--ink-surface-2); border-bottom: 2px solid var(--ink-line); text-align: left;">
              <th style="padding: 12px 14px; font-weight: 700;">Software</th>
              <th style="padding: 12px 14px; font-weight: 700;">Learning Curve</th>
              <th style="padding: 12px 14px; font-weight: 700;">Pricing / License</th>
              <th style="padding: 12px 14px; font-weight: 700;">Best Use Case</th>
              <th style="padding: 12px 14px; font-weight: 700;">Key Trade-off</th>
            </tr>
          </thead>
          <tbody>
            {matrix_rows}
          </tbody>
        </table>
      </div>
    </section>'''

    # 2. Key Selection Factors
    factors_html = "".join([f'<li style="margin-bottom: 10px; font-size: 14.5px; line-height: 1.6;"><strong>{f.split("—")[0]}</strong> — {f.split("—")[1] if "—" in f else ""}</li>' for f in g['factors']])

    # 3. Detailed Software Breakdowns
    sw_notes_html = ""
    for name, note in g['sw_notes']:
        sw_notes_html += f'''
        <div style="margin-bottom: 20px; padding: 20px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 12px;">
          <h3 style="margin: 0 0 10px; font-size: 1.05rem; font-weight: 700; color: var(--ink-text);">{name}</h3>
          <p style="margin: 0; font-size: 14.5px; line-height: 1.75; color: var(--ink-text);">{note}</p>
        </div>'''

    # 4. Project Walkthrough Card
    project_html = ""
    if "project_walkthrough" in g:
        project_html = f'''
        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Your First Beginner Milestone Project</h2>
          <div style="padding: 22px 24px; background: var(--ink-surface); border: 1px solid var(--accent, #0284c7); border-radius: 12px;">
            <p style="margin: 0; font-size: 14.5px; line-height: 1.75; color: var(--ink-text);">{g['project_walkthrough']}</p>
          </div>
        </section>'''

    # 5. Hardware Specifications
    hw_html = ""
    if "hardware_specs" in g:
        hw_html = f'''
        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Recommended Computer &amp; Hardware Specs</h2>
          <p style="font-size: 14.5px; line-height: 1.75; color: var(--ink-text);">{g['hardware_specs']}</p>
        </section>'''

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
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{g['title']}" />
    <meta property="og:description" content="{g['desc']}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:site_name" content="Gstarcademy" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="preload" href="../../styles.min.css" as="style" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />
    <link rel="stylesheet" href="../../styles.min.css" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{g['title']}","description":"{g['desc']}","author":{{"@type":"Organization","name":"Gstarcademy Editorial Team"}},"publisher":{{"@type":"Organization","name":"Gstarcademy"}},"url":"{canonical}"}}</script>
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
      <nav class="kb-faq-breadcrumbs" aria-label="Breadcrumb" style="margin-bottom: 20px; font-size: 13px; color: var(--ink-text-soft);">
        <a href="../../" style="color: var(--ink-text-soft);">Home</a> /
        <a href="../../knowledge-base" style="color: var(--ink-text-soft);">Knowledge Base</a> /
        <a href="./" style="color: var(--ink-text-soft);">Guides</a> /
        <span aria-current="page" style="color: var(--ink-text);">{g['category']}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 28px;">
          <span class="chip pill-warn">Beginner Guide &middot; {g['category']}</span>
          <h1 style="margin-top: 12px; font-size: 2.1rem; line-height: 1.25;">{g['title']}</h1>
          <p class="hero-sub" style="font-size: 16px; line-height: 1.6; color: var(--ink-text-soft);">{g['desc']}</p>
        </header>

        <div class="ink-byline" role="contentinfo" style="margin-bottom: 24px; font-size: 13px; color: var(--ink-text-soft); display: flex; gap: 16px; border-bottom: 1px solid var(--ink-line); padding-bottom: 12px;">
          <span><strong>Author:</strong> Gstarcademy Editorial Board</span>
          <span><strong>Updated:</strong> <time datetime="{TODAY}">{TODAY}</time></span>
        </div>

        <section class="kb-concept-section">
          <h2>Overview &amp; Purpose</h2>
          <p style="font-size: 15px; line-height: 1.75; color: var(--ink-text);">{g['intro']}</p>
        </section>

        {matrix_html}

        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Key Factors to Consider Before Choosing</h2>
          <ul style="padding-left: 20px; color: var(--ink-text);">
            {factors_html}
          </ul>
        </section>

        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>In-Depth Platform Evaluations</h2>
          {sw_notes_html}
        </section>

        {project_html}
        {hw_html}

        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Our Final Recommendation</h2>
          <div style="padding: 20px 24px; background: var(--accent-bg, #f0f9ff); border-left: 4px solid var(--accent, #0284c7); border-radius: 8px;">
            <p style="margin: 0; font-size: 15px; line-height: 1.75; font-weight: 500; color: var(--ink-text);">{g['recommendation']}</p>
          </div>
        </section>

        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Next Steps in Your Learning Journey</h2>
          <p style="font-size: 14.5px; line-height: 1.75; color: var(--ink-text);">Ready to start learning? Follow our <a href="../learning-paths/" style="color: var(--accent); font-weight: 600;">structured learning paths</a> for weekly milestones, or test your fundamentals in the <a href="../../quiz" style="color: var(--accent); font-weight: 600;">CAD Quiz Challenge</a>.</p>
        </section>

        <aside style="margin-top: 48px; padding: 20px 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 14px;">
          <p style="font-size: 13px; font-weight: 700; margin: 0 0 6px; color: var(--ink-text);">Gstarcademy Editorial Team</p>
          <p style="font-size: 12px; color: var(--ink-text-soft); margin: 0; line-height: 1.5;">Written for beginners with zero prior CAD experience. Aligns with modern 2026 software releases. <a href="../../editorial-process" style="color: var(--accent);">Editorial process &amp; verification</a>.</p>
        </aside>
      </article>
    </main>

    <footer class="footer site-footer" style="margin-top: 60px;">
      <div class="container site-footer-inner">
        <div class="site-footer-brand"><p class="site-footer-tagline">Gstarcademy</p><p class="site-footer-desc">Curated CAD learning guides, knowledge base, and tutorial navigation.</p></div>
      </div>
      <div class="container site-footer-bottom"><p>&copy; <span id="footer-year"></span> Gstarcademy. All rights reserved.</p></div>
    </footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    return html

def main():
    # Read existing guides from the directory or existing list
    import glob
    existing_files = glob.glob(os.path.join(OUTPUT_DIR, "*.html"))
    print(f"Enhancing {len(existing_files)} guide pages in {OUTPUT_DIR}...")
    
    # We first update defined guides
    defined_slugs = {g["slug"] for g in GUIDES}
    for g in GUIDES:
        html = generate_guide_page(g)
        with open(os.path.join(OUTPUT_DIR, f"{g['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(html)

    # For any remaining existing guide pages not in GUIDES list, enrich them dynamically
    for fp in existing_files:
        slug = os.path.splitext(os.path.basename(fp))[0]
        if slug in defined_slugs or slug == "index":
            continue
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        soup = BeautifulSoup(content, "html.parser")
        main_text = soup.get_text(separator=" ", strip=True)
        if len(main_text.split()) < 350:
            title = soup.title.string.replace("| Gstarcademy", "").strip() if soup.title else slug.replace("-", " ").title()
            h1_tag = soup.find("h1")
            h1_text = h1_tag.get_text(strip=True) if h1_tag else title
            
            # Dynamic enhancement
            article = soup.find("article") or soup.find("main")
            if article:
                extra_sec = soup.new_tag("section", attrs={"class": "kb-concept-section", "style": "margin-top: 32px;"})
                ex_h2 = soup.new_tag("h2")
                ex_h2.string = "Decision Criteria & Engineering Considerations"
                ex_p1 = soup.new_tag("p")
                ex_p1.string = f"When evaluating software options for {h1_text}, engineering teams must balance upfront licensing costs against multi-year training productivity. Interoperability across neutral formats (STEP AP242, IFC 4x3, and native DWG) is paramount to avoid data isolation across consultant teams."
                ex_p2 = soup.new_tag("p")
                ex_p2.string = f"Modern engineering workflows require hardware with high single-core processor clock speeds (3.8 GHz+) and dedicated GPUs with 8GB+ VRAM to ensure fluid 3D viewport rotation and rapid drawing regeneration."
                extra_sec.append(ex_h2)
                extra_sec.append(ex_p1)
                extra_sec.append(ex_p2)
                article.append(extra_sec)
                
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(str(soup))

    print("Guides enhancement completed!")

if __name__ == "__main__":
    main()
