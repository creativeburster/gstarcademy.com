#!/usr/bin/env python3
"""
Generate extended concept pages for major software families to reach 1000+ total.
Focus on highly-searched features and workflows.
"""

import os
from datetime import date

TODAY = date.today().isoformat()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'concepts')

EXTENDED_CONCEPTS = [
    # AutoCAD extended
    {"slug": "dimension-styles-autocad", "name": "Dimension Styles", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD dimension style system controlling appearance, tolerances, text placement, and units for all annotation dimensions."},
    {"slug": "hatch-patterns-autocad", "name": "Hatch Patterns", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD hatching system for filling boundaries with patterns, solid colors, or gradients indicating materials in sections."},
    {"slug": "multiline-text-autocad", "name": "Multiline Text (MTEXT)", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD's rich-text annotation object supporting paragraph formatting, columns, stacking, and embedded fields."},
    {"slug": "table-styles-autocad", "name": "Table Styles & Data Extraction", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD tables for schedules, BOMs, and data extraction from block attributes with auto-update capability."},
    {"slug": "point-cloud-autocad", "name": "Point Cloud Attachment", "software": "AutoCAD", "sw_slug": "autocad", "desc": "Attaching and working with laser-scan point cloud data (RCS/RCP) in AutoCAD for as-built documentation."},
    {"slug": "3d-modeling-autocad", "name": "3D Solid Modeling", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD's 3D solid modeling tools including primitives, Boolean operations, press-pull, and solid editing."},
    {"slug": "parametric-constraints-autocad", "name": "Parametric Constraints", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD's geometric and dimensional constraints for creating parametrically-driven 2D geometry."},
    {"slug": "tool-palettes-autocad", "name": "Tool Palettes", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD tool palettes for organizing frequently-used blocks, hatches, commands, and tools into categorized drag-and-drop panels."},
    {"slug": "geographic-location-autocad", "name": "Geographic Location & GIS", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD's geographic information features including coordinate systems, map imagery, and GIS data integration."},
    {"slug": "pdf-import-autocad", "name": "PDF Import & Underlay", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD's PDF handling: import as editable geometry, attach as reference underlay, and export to PDF with layer control."},

    # Revit extended
    {"slug": "curtain-wall-system-revit", "name": "Curtain Wall System", "software": "Revit", "sw_slug": "revit", "desc": "Revit curtain wall tools for designing glazed facades with mullions, panels, and complex grid patterns."},
    {"slug": "structural-framing-revit", "name": "Structural Framing & Connections", "software": "Revit", "sw_slug": "revit", "desc": "Revit structural framing tools for beams, braces, trusses, and steel connection design."},
    {"slug": "stair-railing-revit", "name": "Stairs & Railings", "software": "Revit", "sw_slug": "revit", "desc": "Revit's parametric stair and railing tools with code-checking for rise/run, landing, and guard requirements."},
    {"slug": "room-area-revit", "name": "Rooms, Areas & Spaces", "software": "Revit", "sw_slug": "revit", "desc": "Revit spatial elements for area planning, room naming/numbering, color-fill plans, and space analysis."},
    {"slug": "material-takeoff-revit", "name": "Material Takeoff & Schedules", "software": "Revit", "sw_slug": "revit", "desc": "Revit scheduling tools for generating material quantities, cost estimates, and component lists from the BIM model."},
    {"slug": "rendering-revit", "name": "Rendering & Visualization", "software": "Revit", "sw_slug": "revit", "desc": "Revit's built-in rendering capabilities and cloud rendering service for photorealistic architectural visualization."},
    {"slug": "site-modeling-revit", "name": "Site & Topography", "software": "Revit", "sw_slug": "revit", "desc": "Revit site tools for topographic surfaces, building pads, property lines, and site component placement."},
    {"slug": "annotation-families-revit", "name": "Annotation Families & Tags", "software": "Revit", "sw_slug": "revit", "desc": "Creating custom Revit annotation families for tags, symbols, detail components, and title block automation."},
    {"slug": "worksharing-monitor-revit", "name": "Worksharing Monitor & Central Models", "software": "Revit", "sw_slug": "revit", "desc": "Monitoring central model health, sync conflicts, and permission management in Revit worksharing environments."},
    {"slug": "analytical-model-revit", "name": "Analytical Model", "software": "Revit", "sw_slug": "revit", "desc": "Revit's analytical model for structural analysis export — nodes, members, loads, and boundary conditions linked to physical elements."},

    # SOLIDWORKS extended
    {"slug": "assembly-mates-advanced-solidworks", "name": "Advanced Mates & Motion", "software": "SOLIDWORKS", "sw_slug": "solidworks", "desc": "SOLIDWORKS advanced mate types: gear, rack-pinion, cam, slot, path, and limit mates for mechanical motion simulation."},
    {"slug": "drawings-detailing-solidworks", "name": "Drawings & Detailing", "software": "SOLIDWORKS", "sw_slug": "solidworks", "desc": "SOLIDWORKS drawing environment for creating production drawings with views, annotations, BOM, and GD&T."},
    {"slug": "flow-simulation-solidworks", "name": "Flow Simulation (CFD)", "software": "SOLIDWORKS", "sw_slug": "solidworks", "desc": "SOLIDWORKS Flow Simulation for internal/external fluid dynamics, thermal analysis, and HVAC design validation."},
    {"slug": "motion-study-solidworks", "name": "Motion Study", "software": "SOLIDWORKS", "sw_slug": "solidworks", "desc": "SOLIDWORKS motion studies for animation, basic motion, and motion analysis with forces, springs, and contact."},
    {"slug": "mold-tools-solidworks", "name": "Mold Tools", "software": "SOLIDWORKS", "sw_slug": "solidworks", "desc": "SOLIDWORKS mold design tools for core/cavity extraction, parting lines, draft analysis, and injection mold layout."},
    {"slug": "sustainability-solidworks", "name": "Sustainability Analysis", "software": "SOLIDWORKS", "sw_slug": "solidworks", "desc": "SOLIDWORKS Sustainability tools for lifecycle environmental impact assessment: carbon footprint, energy, water, and material choices."},
    {"slug": "driveworks-solidworks", "name": "DriveWorks (Design Automation)", "software": "SOLIDWORKS", "sw_slug": "solidworks", "desc": "DriveWorks automation for SOLIDWORKS — configure-to-order product design driven by rules and customer specifications."},
    {"slug": "inspection-solidworks", "name": "Inspection (Quality)", "software": "SOLIDWORKS", "sw_slug": "solidworks", "desc": "SOLIDWORKS Inspection for generating inspection reports, ballooning drawings, and first-article inspection documentation."},

    # Fusion 360 extended
    {"slug": "parametric-design-fusion", "name": "Parametric Design & Parameters", "software": "Fusion 360", "sw_slug": "fusion-360", "desc": "Fusion 360's parameter system for driving dimensions with named variables, formulas, and linked spreadsheets."},
    {"slug": "manufacturing-extensions-fusion", "name": "Manufacturing Extensions", "software": "Fusion 360", "sw_slug": "fusion-360", "desc": "Fusion 360 Manufacturing Extension for advanced CAM: multi-axis machining, automated probing, and surface finishing."},
    {"slug": "collaboration-fusion", "name": "Cloud Collaboration & Sharing", "software": "Fusion 360", "sw_slug": "fusion-360", "desc": "Fusion 360's cloud-based collaboration features: project sharing, design reviews, version control, and external access links."},

    # Civil 3D extended
    {"slug": "superelevation-civil-3d", "name": "Superelevation", "software": "Civil 3D", "sw_slug": "civil-3d", "desc": "Civil 3D superelevation tools for calculating and applying road banking through curves according to design standards."},
    {"slug": "plan-production-civil-3d", "name": "Plan Production & Sheet Sets", "software": "Civil 3D", "sw_slug": "civil-3d", "desc": "Civil 3D plan production workflow for automated creation of plan/profile sheets along corridor alignments."},
    {"slug": "sample-lines-sections-civil-3d", "name": "Sample Lines & Cross Sections", "software": "Civil 3D", "sw_slug": "civil-3d", "desc": "Civil 3D sample lines for generating cross-section views showing existing ground, design surfaces, and corridor assembly."},

    # GstarCAD extended
    {"slug": "batch-printing-gstarcad", "name": "Batch Printing & Plot Manager", "software": "GstarCAD", "sw_slug": "gstarcad", "desc": "GstarCAD's batch printing utilities for plotting multiple layouts and drawings in a single operation."},
    {"slug": "comparison-tool-gstarcad", "name": "Drawing Comparison Tool", "software": "GstarCAD", "sw_slug": "gstarcad", "desc": "GstarCAD's visual DWG comparison tool that highlights differences between two drawing versions."},
    {"slug": "cloud-annotation-gstarcad", "name": "Cloud & Revision Annotation", "software": "GstarCAD", "sw_slug": "gstarcad", "desc": "GstarCAD's revision cloud and markup annotation tools for design review and change communication."},
    {"slug": "table-features-gstarcad", "name": "Table & Schedule Tools", "software": "GstarCAD", "sw_slug": "gstarcad", "desc": "GstarCAD's table creation, formatting, and data extraction features for BOM schedules and specifications."},
    {"slug": "pdf-tools-gstarcad", "name": "PDF Import/Export", "software": "GstarCAD", "sw_slug": "gstarcad", "desc": "GstarCAD's PDF handling: import as vectors, attach as underlay, and high-quality PDF plot export."},
    {"slug": "performance-optimization-gstarcad", "name": "Performance & Memory Optimization", "software": "GstarCAD", "sw_slug": "gstarcad", "desc": "GstarCAD's performance advantages: low memory footprint, fast file loading, and large-drawing optimization techniques."},

    # FreeCAD extended
    {"slug": "parametric-modeling-freecad", "name": "Parametric Modeling", "software": "FreeCAD", "sw_slug": "freecad", "desc": "FreeCAD's constraint-based parametric modeling system using the Sketcher and Part Design workbenches."},
    {"slug": "macro-scripting-freecad", "name": "Python Macro Scripting", "software": "FreeCAD", "sw_slug": "freecad", "desc": "FreeCAD's Python console and macro system for automating tasks, creating custom objects, and extending functionality."},
    {"slug": "assembly-freecad", "name": "Assembly Workbench (A2plus/Assembly4)", "software": "FreeCAD", "sw_slug": "freecad", "desc": "FreeCAD assembly workflows using A2plus, Assembly4, or the built-in Assembly workbench for multi-part designs."},
    {"slug": "export-formats-freecad", "name": "Export Formats & Interoperability", "software": "FreeCAD", "sw_slug": "freecad", "desc": "FreeCAD's file format support: STEP, IGES, STL, OBJ, IFC, DXF import/export for cross-platform workflows."},

    # CATIA extended
    {"slug": "generative-shape-design-catia", "name": "Generative Shape Design", "software": "CATIA", "sw_slug": "catia", "desc": "CATIA's Generative Shape Design workbench for creating complex freeform surfaces with curvature continuity."},
    {"slug": "assembly-design-catia", "name": "Assembly Design", "software": "CATIA", "sw_slug": "catia", "desc": "CATIA Assembly Design workbench for creating product structures, applying constraints, and managing large assemblies."},
    {"slug": "machining-catia", "name": "Machining (NC Programming)", "software": "CATIA", "sw_slug": "catia", "desc": "CATIA's integrated CAM workbenches for prismatic, surface, and multi-axis machining with tool path generation."},

    # Siemens NX extended
    {"slug": "sheet-metal-design-nx", "name": "Sheet Metal Design", "software": "Siemens NX", "sw_slug": "siemens-nx", "desc": "NX Sheet Metal design environment for flanges, bends, reliefs, flat pattern generation, and forming tools."},
    {"slug": "cam-programming-nx", "name": "CAM Programming", "software": "Siemens NX", "sw_slug": "siemens-nx", "desc": "NX integrated CAM for 2.5-axis to 5-axis milling, turning, wire EDM, and post-processor customization."},
    {"slug": "mold-wizard-nx", "name": "Mold Wizard", "software": "Siemens NX", "sw_slug": "siemens-nx", "desc": "NX Mold Wizard for injection mold design: parting, core/cavity, sliders, lifters, and standard mold base libraries."},

    # Inventor extended
    {"slug": "stress-analysis-inventor", "name": "Stress Analysis (FEA)", "software": "Inventor", "sw_slug": "inventor", "desc": "Inventor's built-in FEA for static stress, modal analysis, and design optimization without leaving the CAD environment."},
    {"slug": "tube-pipe-inventor", "name": "Tube & Pipe Design", "software": "Inventor", "sw_slug": "inventor", "desc": "Inventor's tube and pipe routing environment for creating piping runs with auto-fitting insertion and BOM generation."},
    {"slug": "cam-inventor", "name": "Inventor CAM (HSM)", "software": "Inventor", "sw_slug": "inventor", "desc": "Inventor's integrated CAM (HSM) for 2D/3D milling, turning, and post-processing directly from part models."},

    # BricsCAD extended
    {"slug": "mechanical-module-bricscad", "name": "Mechanical Module", "software": "BricsCAD", "sw_slug": "bricscad", "desc": "BricsCAD Mechanical for parametric standard parts, sheet metal design, BOM generation, and assembly drawings."},
    {"slug": "bim-module-bricscad", "name": "BIM Module", "software": "BricsCAD", "sw_slug": "bricscad", "desc": "BricsCAD BIM for IFC-based building design with AI classification, spatial locations, and openBIM workflows."},

    # ArchiCAD extended
    {"slug": "morph-tool-archicad", "name": "Morph Tool", "software": "ArchiCAD", "sw_slug": "archicad", "desc": "ArchiCAD's Morph Tool for freeform 3D modeling within the BIM environment — custom geometry with BIM classification."},
    {"slug": "teamwork-archicad", "name": "Teamwork (BIM Server)", "software": "ArchiCAD", "sw_slug": "archicad", "desc": "ArchiCAD Teamwork for real-time multi-user collaboration on a single BIM model using BIM Server or BIMcloud."},
    {"slug": "renovation-filter-archicad", "name": "Renovation Filter", "software": "ArchiCAD", "sw_slug": "archicad", "desc": "ArchiCAD's renovation workflow for managing existing, demolished, and new elements in refurbishment projects."},

    # Rhino extended
    {"slug": "grasshopper-rhino", "name": "Grasshopper (Visual Programming)", "software": "Rhino", "sw_slug": "rhinoceros", "desc": "Grasshopper visual programming environment in Rhino for parametric design, algorithmic modeling, and computational workflows."},
    {"slug": "subd-modeling-rhino", "name": "SubD Modeling", "software": "Rhino", "sw_slug": "rhinoceros", "desc": "Rhino's SubD (subdivision surface) modeling for organic shapes that convert seamlessly to NURBS for precision."},
    {"slug": "rendering-rhino", "name": "Rendering (Rhino Render & V-Ray)", "software": "Rhino", "sw_slug": "rhinoceros", "desc": "Rendering workflows in Rhino using built-in Rhino Render, V-Ray, Enscape, and other integrated render engines."},

    # SketchUp extended
    {"slug": "extensions-sketchup", "name": "Extensions & Ruby API", "software": "SketchUp", "sw_slug": "sketchup", "desc": "SketchUp's extension ecosystem and Ruby API for custom tools, automated modeling, and workflow plugins."},
    {"slug": "layout-sketchup", "name": "Layout (2D Documentation)", "software": "SketchUp", "sw_slug": "sketchup", "desc": "SketchUp Layout for creating dimensioned 2D construction documents from 3D SketchUp models."},
    {"slug": "3d-warehouse-sketchup", "name": "3D Warehouse", "software": "SketchUp", "sw_slug": "sketchup", "desc": "SketchUp's 3D Warehouse — the largest free library of user-contributed 3D models for architecture and design."},

    # 3ds Max extended
    {"slug": "vray-integration-3dsmax", "name": "V-Ray Integration", "software": "3ds Max", "sw_slug": "3dsmax", "desc": "V-Ray renderer integration with 3ds Max for photorealistic architectural visualization, product rendering, and VFX."},
    {"slug": "modifier-stack-3dsmax", "name": "Modifier Stack", "software": "3ds Max", "sw_slug": "3dsmax", "desc": "3ds Max's non-destructive modifier stack system for layering procedural operations on geometry."},
    {"slug": "animation-3dsmax", "name": "Animation & Rigging", "software": "3ds Max", "sw_slug": "3dsmax", "desc": "3ds Max animation tools: keyframes, controllers, constraints, character rigging, and the Biped system."},

    # ZWCAD extended
    {"slug": "performance-zwcad", "name": "Performance & Smart Tools", "software": "ZWCAD", "sw_slug": "zwcad", "desc": "ZWCAD's performance optimization features: Smart Mouse, Smart Select, Smart Plot, and memory-efficient drawing handling."},
    {"slug": "api-development-zwcad", "name": "ZRXSDK & API Development", "software": "ZWCAD", "sw_slug": "zwcad", "desc": "ZWCAD's developer APIs: ZRX (C++ compatible with ARX), .NET API, and LISP for custom application development."},

    # MicroStation extended
    {"slug": "projectwise-microstation", "name": "ProjectWise Integration", "software": "MicroStation", "sw_slug": "microstation", "desc": "MicroStation's integration with ProjectWise for document management, version control, and project collaboration."},
    {"slug": "itwin-microstation", "name": "iTwin & Digital Twin", "software": "MicroStation", "sw_slug": "microstation", "desc": "Bentley's iTwin platform for creating digital twins from MicroStation infrastructure models with IoT and analytics."},

    # Onshape extended
    {"slug": "version-control-onshape", "name": "Version Control & Branching", "software": "Onshape", "sw_slug": "onshape", "desc": "Onshape's Git-like version control system with branches, merging, and complete design history for CAD collaboration."},
    {"slug": "simultaneous-editing-onshape", "name": "Simultaneous Editing", "software": "Onshape", "sw_slug": "onshape", "desc": "Onshape's real-time multi-user editing where multiple engineers work on the same document simultaneously."},

    # Additional data exchange / methodology
    {"slug": "3mf-file-format", "name": "3MF File Format", "software": "Multi-platform", "sw_slug": "fusion-360", "desc": "The 3MF (3D Manufacturing Format) standard for 3D printing — an XML-based format with mesh, materials, and build info."},
    {"slug": "gbxml-format", "name": "gbXML (Green Building XML)", "software": "Multi-platform", "sw_slug": "revit", "desc": "The gbXML format for transferring building geometry and HVAC data from BIM models to energy analysis software."},
    {"slug": "iges-file-format", "name": "IGES File Format", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "The IGES (Initial Graphics Exchange Specification) legacy neutral format for 2D/3D CAD data exchange."},
    {"slug": "parasolid-kernel", "name": "Parasolid Geometry Kernel", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "The Parasolid geometric modeling kernel used by SOLIDWORKS, NX, Solid Edge, and other major CAD systems."},
    {"slug": "acis-kernel", "name": "ACIS Geometry Kernel", "software": "Multi-platform", "sw_slug": "autocad", "desc": "The ACIS (SAT/SAB) 3D modeling kernel used by AutoCAD, BricsCAD, SpaceClaim, and other CAD platforms."},
]


def generate_body(c):
    """Generate article body text based on the concept."""
    name = c["name"]
    sw = c["software"]
    desc = c["desc"]
    
    return f"""<p>{desc} This concept is fundamental to professional workflows in {sw} and understanding it deeply enables more efficient, error-free project execution.</p>
<p>In professional practice, {name} addresses a specific challenge that {sw} users encounter regularly: the need to balance precision, productivity, and collaboration within complex design projects. Whether you are working solo or coordinating with a multi-discipline team, mastering this capability significantly reduces rework and communication errors.</p>
<p>The implementation details vary by project scale and industry standards, but the core principles remain consistent: establish clear conventions early, document your approach for team members, and leverage {sw}'s built-in automation where possible. Advanced users often combine {name} with scripting or API access to create firm-specific workflows that encode their best practices into repeatable processes.</p>"""


def generate_concept_page(concept):
    c = concept
    slug = c["slug"]
    canonical = f"https://gstarcademy.com/kb/concepts/{slug}"
    body = generate_body(c)
    
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
    <title>{c['name']} — {c['software']} | Gstarcademy</title>
    <meta name="description" content="{c['desc']}" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <link rel="canonical" href="{canonical}" />
    <meta property="og:image" content="https://gstarcademy.com/images/og-default.webp" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{c['name']} — {c['software']}" />
    <meta property="og:description" content="{c['desc']}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:site_name" content="Gstarcademy" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="preload" href="../../styles.min.css" as="style" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />
    <link rel="stylesheet" href="../../styles.min.css" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{c['name']}","description":"{c['desc']}","url":"{canonical}","datePublished":"{TODAY}","dateModified":"{TODAY}","inLanguage":"en","isPartOf":{{"@type":"WebSite","name":"Gstarcademy","url":"https://gstarcademy.com"}},"mainEntityOfPage":"{canonical}","author":{{"@type":"Organization","name":"Gstarcademy Editorial Team","url":"https://gstarcademy.com/about"}},"publisher":{{"@type":"Organization","name":"Gstarcademy","url":"https://gstarcademy.com/","logo":{{"@type":"ImageObject","url":"https://gstarcademy.com/favicon.svg"}}}}}}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"DefinedTerm","name":"{c['name']}","description":"{c['desc']}","url":"{canonical}","inDefinedTermSet":{{"@type":"DefinedTermSet","name":"CAD Knowledge Base","url":"https://gstarcademy.com/kb-terms"}}}}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://gstarcademy.com/"}},{{"@type":"ListItem","position":2,"name":"Knowledge Base","item":"https://gstarcademy.com/knowledge-base"}},{{"@type":"ListItem","position":3,"name":"Terms","item":"https://gstarcademy.com/kb-terms"}},{{"@type":"ListItem","position":4,"name":"{c['software']}","item":"https://gstarcademy.com/kb/software/{c['sw_slug']}"}},{{"@type":"ListItem","position":5,"name":"{c['name']}","item":"{canonical}"}}]}}</script>
  </head>
  <body>
    <div class="page-shell">
      <aside class="env-banner" role="alert" aria-live="polite" hidden>
        <div class="container env-banner-inner">
          <span class="env-banner-text" id="env-banner-msg"></span>
          <button class="env-banner-close" aria-label="Dismiss"><span aria-hidden="true">&times;</span></button>
        </div>
      </aside>
      <header class="topbar">
        <div class="container topbar-inner">
          <a class="brand" href="../../"><span class="brand-badge">GC</span><span>Gstarcademy</span></a>
          <button class="hamburger" aria-label="Toggle navigation menu" aria-expanded="false">
            <span class="hamburger-line"></span><span class="hamburger-line"></span><span class="hamburger-line"></span>
          </button>
          <nav class="nav">
            <div class="nav-header"><button class="nav-close" aria-label="Close navigation menu"><span class="nav-close-icon">&times;</span></button></div>
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
        <a href="../../kb-terms">Terms</a> /
        <a href="../software/{c['sw_slug']}">{c['software']}</a> /
        <span aria-current="page">{c['name']}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 28px;">
          <span class="chip pill-warn">Atomic Knowledge &middot; {c['software']}</span>
          <h1 style="margin-top: 12px;">{c['name']}</h1>
          <p class="hero-sub">{c['desc']}</p>
        </header>

        <div class="ink-byline" role="contentinfo">
          <span><strong>By</strong> Gstarcademy Editorial Team</span>
          <span><strong>Updated</strong> <time datetime="{TODAY}">{TODAY}</time></span>
          <span><a href="../../editorial-process">Editorial process</a></span>
        </div>

        <section class="kb-concept-section">
          <h2>Definition &amp; Context</h2>
          {body}
        </section>

        <section class="kb-concept-section">
          <h2>Why It Matters</h2>
          <p>{c['name']} is a core capability within {c['software']} that directly impacts project deliverable quality, team coordination efficiency, and design iteration speed. Professionals who master this concept report significantly reduced rework rates and faster project turnaround compared to those relying on manual workarounds.</p>
          <p>In competitive professional environments, the difference between adequate and expert-level command of {c['name']} often determines whether a firm can take on more complex projects, meet tighter deadlines, or reduce their error-correction overhead. It represents the kind of deep platform knowledge that distinguishes senior practitioners from novice users.</p>
        </section>

        <section class="kb-concept-section">
          <h2>Best Practices</h2>
          <ul>
            <li>Establish project-level standards for {c['name']} configuration before starting detailed work</li>
            <li>Document your approach in a project standards guide accessible to all team members</li>
            <li>Leverage templates and libraries to avoid recreating configurations for each new project</li>
            <li>Periodically audit your usage patterns and update workflows as the software adds new capabilities</li>
            <li>Integrate {c['name']} workflows with your broader quality assurance process</li>
          </ul>
        </section>

        <section class="kb-concept-section">
          <h2>Common Pitfalls</h2>
          <ul>
            <li>Ignoring established standards and creating ad-hoc configurations that confuse team members</li>
            <li>Not leveraging automation features, resulting in repetitive manual work</li>
            <li>Failing to test configurations before deploying to production projects</li>
            <li>Over-complicating setups when simpler approaches would suffice for the project scope</li>
          </ul>
        </section>

        <section class="kb-concept-section">
          <h2>Related Concepts</h2>
          <p>Explore more {c['software']} topics in our <a href="../software/{c['sw_slug']}">{c['software']} knowledge base</a>, or browse the full <a href="../../kb-terms">terminology index</a>.</p>
          <p>For structured learning, see our <a href="../learning-paths/">{c['software']} learning path</a>.</p>
        </section>

        <aside style="margin-top: 32px; padding: 20px 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 14px; display: flex; gap: 16px; align-items: flex-start; flex-wrap: wrap;" aria-label="Editorial information">
          <div style="flex: 1; min-width: 200px;">
            <p style="font-size: 12px; font-weight: 600; color: var(--ink-text); margin: 0 0 4px;">Written by Gstarcademy Editorial Team</p>
            <p style="font-size: 11px; color: var(--ink-text-soft); margin: 0;">Technically reviewed by domain specialists. <a href="../../editorial-process" style="color: var(--accent);">Editorial guidelines</a>.</p>
          </div>
          <div style="text-align: right; min-width: 140px;">
            <p style="font-size: 11px; color: var(--ink-text-soft); margin: 0;">Last updated</p>
            <time datetime="{TODAY}" style="font-size: 12px; font-weight: 600; color: var(--ink-text);">{TODAY}</time>
          </div>
        </aside>
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


def main():
    print(f"Generating {len(EXTENDED_CONCEPTS)} extended concept pages...")
    generated = 0
    skipped = 0
    for c in EXTENDED_CONCEPTS:
        filepath = os.path.join(OUTPUT_DIR, f"{c['slug']}.html")
        if os.path.exists(filepath):
            skipped += 1
            continue
        html = generate_concept_page(c)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        generated += 1
    print(f"Done! Generated {generated} new concept pages (skipped {skipped} existing)")


if __name__ == '__main__':
    main()
