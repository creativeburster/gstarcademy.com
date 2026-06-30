#!/usr/bin/env python3
"""
Generate learning path / beginner guide pages for major CAD software.
Each page targets "[Software] learning path" / "[Software] beginner guide" search intent.
"""

import os
from datetime import date

TODAY = date.today().isoformat()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'learning-paths')
os.makedirs(OUTPUT_DIR, exist_ok=True)

PATHS = [
    {
        "slug": "autocad-beginner",
        "software": "AutoCAD",
        "sw_slug": "autocad",
        "title": "AutoCAD Beginner Learning Path",
        "desc": "Structured 6-week AutoCAD learning path for beginners. Master 2D drafting fundamentals, layers, blocks, dimensions, and plotting with step-by-step milestones.",
        "duration": "6 weeks",
        "level": "Beginner to Intermediate",
        "prereqs": "Basic computer literacy, understanding of technical drawings",
        "stages": [
            {"name": "Week 1: Interface & Navigation", "topics": ["AutoCAD workspace layout", "Command line basics", "Navigation (zoom, pan, orbit)", "File management (DWG, DWT)"], "concepts": ["dynamic-input", "dwg-file-format"]},
            {"name": "Week 2: Basic Drawing", "topics": ["Line, circle, arc, polyline", "Object snaps and tracking", "Coordinate systems (absolute, relative, polar)", "Construction geometry"], "concepts": ["annotative-objects"]},
            {"name": "Week 3: Editing & Modifying", "topics": ["Move, copy, rotate, mirror", "Trim, extend, offset, fillet", "Array (rectangular, polar, path)", "Grips editing"], "concepts": ["dynamic-blocks-autocad"]},
            {"name": "Week 4: Organization", "topics": ["Layer management", "Properties and match", "Block creation and insertion", "External references (Xrefs)"], "concepts": ["layers-gstarcad", "attributes-blocks", "xref-autocad"]},
            {"name": "Week 5: Annotation", "topics": ["Dimensions (linear, aligned, angular)", "Text styles and multiline text", "Hatching and gradients", "Leaders and tables"], "concepts": ["annotative-objects"]},
            {"name": "Week 6: Output & Productivity", "topics": ["Paper space and viewports", "Page setup and plotting", "PDF export", "AutoLISP introduction"], "concepts": ["paper-space-autocad", "autolisp"]},
        ],
    },
    {
        "slug": "gstarcad-beginner",
        "software": "GstarCAD",
        "sw_slug": "gstarcad",
        "title": "GstarCAD Beginner Learning Path",
        "desc": "Complete GstarCAD learning guide from zero to productive. Covers the DWG-native workflow, performance-optimized drafting, and API scripting for beginners.",
        "duration": "5 weeks",
        "level": "Beginner to Intermediate",
        "prereqs": "Basic computer literacy",
        "stages": [
            {"name": "Week 1: Getting Started", "topics": ["GstarCAD interface overview", "Quick properties and command line", "Drawing setup (units, limits)", "Template creation"], "concepts": ["ai-tools-gstarcad"]},
            {"name": "Week 2: Core Drawing", "topics": ["Basic geometry commands", "Object snaps and polar tracking", "Precision input methods", "Drawing techniques for speed"], "concepts": ["3d-operations-gstarcad"]},
            {"name": "Week 3: Editing & Layers", "topics": ["Modify commands (trim, offset, fillet)", "Layer management and filters", "Block library workflow", "Design center usage"], "concepts": ["layers-gstarcad"]},
            {"name": "Week 4: Annotation & Output", "topics": ["Dimension styles", "Text and tables", "Plotting and PDF output", "Batch plot utility"], "concepts": ["annotative-objects-gstarcad"]},
            {"name": "Week 5: Scripting & Customization", "topics": ["AutoLISP basics in GstarCAD", "CUI customization", "Tool palettes", ".NET plugin introduction"], "concepts": ["autolisp-gstarcad"]},
        ],
    },
    {
        "slug": "revit-beginner",
        "software": "Revit",
        "sw_slug": "revit",
        "title": "Revit Beginner Learning Path",
        "desc": "8-week structured Revit learning path. Go from zero BIM knowledge to creating coordinated building models with families, views, sheets, and collaboration workflows.",
        "duration": "8 weeks",
        "level": "Beginner to Intermediate",
        "prereqs": "Basic understanding of building construction, architectural drawings",
        "stages": [
            {"name": "Week 1-2: BIM Fundamentals", "topics": ["BIM vs CAD concepts", "Revit interface and project browser", "Levels and grids", "Basic wall, floor, roof creation"], "concepts": ["revit-term-1"]},
            {"name": "Week 3-4: Building Elements", "topics": ["Doors and windows", "Stairs and railings", "Curtain walls", "Component families"], "concepts": ["revit-term-2"]},
            {"name": "Week 5-6: Documentation", "topics": ["Views, plans, sections", "Dimension and annotation", "Schedules and quantities", "Sheet composition"], "concepts": ["revit-term-3"]},
            {"name": "Week 7-8: Collaboration", "topics": ["Worksharing and central models", "Design options", "Linked models", "Export to IFC and DWG"], "concepts": ["revit-term-4", "revit-term-5"]},
        ],
    },
    {
        "slug": "solidworks-beginner",
        "software": "SOLIDWORKS",
        "sw_slug": "solidworks",
        "title": "SOLIDWORKS Beginner Learning Path",
        "desc": "6-week SOLIDWORKS learning path for mechanical design beginners. Master sketching, part modeling, assemblies, and drawings with practical exercises.",
        "duration": "6 weeks",
        "level": "Beginner to Intermediate",
        "prereqs": "Basic understanding of mechanical engineering drawings",
        "stages": [
            {"name": "Week 1: Sketching", "topics": ["Sketch entities and constraints", "Dimensions and relations", "Sketch patterns", "Sketch best practices"], "concepts": ["solidworks-term-1"]},
            {"name": "Week 2: Part Modeling", "topics": ["Extrude, revolve, sweep, loft", "Fillets and chamfers", "Shell and draft", "Reference geometry"], "concepts": ["solidworks-term-2", "solidworks-term-3"]},
            {"name": "Week 3: Advanced Features", "topics": ["Patterns (linear, circular)", "Configurations", "Design tables", "Multi-body parts"], "concepts": ["solidworks-term-4"]},
            {"name": "Week 4: Assemblies", "topics": ["Mates and constraints", "Sub-assemblies", "Interference detection", "Exploded views"], "concepts": ["solidworks-term-5", "solidworks-term-6"]},
            {"name": "Week 5: Drawings", "topics": ["Drawing views", "Dimensions and annotations", "Bill of materials", "Drawing templates"], "concepts": ["solidworks-term-7"]},
            {"name": "Week 6: Simulation Basics", "topics": ["Static analysis setup", "Mesh control", "Interpreting results", "Design validation"], "concepts": ["solidworks-term-8", "solidworks-term-9"]},
        ],
    },
    {
        "slug": "fusion-360-beginner",
        "software": "Fusion 360",
        "sw_slug": "fusion-360",
        "title": "Fusion 360 Beginner Learning Path",
        "desc": "5-week Fusion 360 learning path covering cloud-native CAD fundamentals, parametric modeling, assembly design, rendering, and basic CAM toolpaths.",
        "duration": "5 weeks",
        "level": "Beginner to Intermediate",
        "prereqs": "Basic computer skills, Autodesk account",
        "stages": [
            {"name": "Week 1: Cloud Workspace", "topics": ["Data panel and projects", "Design timeline", "Sketch constraints", "Parametric dimensions"], "concepts": ["constraints-fusion"]},
            {"name": "Week 2: Solid Modeling", "topics": ["Extrude, revolve, sweep", "Direct modeling (push/pull)", "Sculpt (T-splines)", "Component vs body"], "concepts": ["fusion-360-term-1", "fusion-360-term-2"]},
            {"name": "Week 3: Assembly & Motion", "topics": ["Joints and as-built joints", "Motion studies", "Contact sets", "Interference checking"], "concepts": ["fusion-360-term-3"]},
            {"name": "Week 4: Rendering & Drawing", "topics": ["Materials and appearances", "Scene setup and rendering", "2D drawing creation", "Export formats"], "concepts": ["fusion-360-term-4"]},
            {"name": "Week 5: CAM & Manufacturing", "topics": ["Setup and stock definition", "2D toolpaths (contour, pocket)", "3D toolpaths (adaptive)", "Post-processing and NC code"], "concepts": ["fusion-360-term-5", "fusion-360-term-6"]},
        ],
    },
    {
        "slug": "blender-beginner",
        "software": "Blender",
        "sw_slug": "blender",
        "title": "Blender Beginner Learning Path",
        "desc": "4-week Blender learning path for CAD professionals. Learn polygonal modeling, materials, Cycles rendering, and architectural visualization in the free open-source 3D suite.",
        "duration": "4 weeks",
        "level": "Beginner",
        "prereqs": "Basic 3D spatial understanding",
        "stages": [
            {"name": "Week 1: Interface & Navigation", "topics": ["Viewport navigation", "Object vs Edit mode", "Selection and transforms", "Modifier stack basics"], "concepts": ["blender-cycles"]},
            {"name": "Week 2: Modeling", "topics": ["Mesh primitives", "Extrude, loop cut, bevel", "Subdivision surfaces", "Boolean operations"], "concepts": ["3dsmax-polygonal-modeling"]},
            {"name": "Week 3: Materials & Lighting", "topics": ["Shader editor nodes", "PBR materials", "HDRI lighting", "Cycles vs EEVEE"], "concepts": ["blender-cycles"]},
            {"name": "Week 4: Rendering & Output", "topics": ["Camera setup", "Render settings optimization", "Compositing basics", "Export for CAD (FBX, OBJ, glTF)"], "concepts": ["3dsmax-arnold-renderer"]},
        ],
    },
    {
        "slug": "civil-3d-beginner",
        "software": "Civil 3D",
        "sw_slug": "civil-3d",
        "title": "Civil 3D Beginner Learning Path",
        "desc": "8-week Civil 3D learning path for civil engineering students and professionals. Master surfaces, alignments, profiles, corridors, and pipe networks.",
        "duration": "8 weeks",
        "level": "Beginner to Intermediate",
        "prereqs": "AutoCAD basics, civil engineering fundamentals",
        "stages": [
            {"name": "Week 1-2: Points & Surfaces", "topics": ["Point groups and import", "Surface creation (TIN)", "Surface editing and analysis", "Contour display"], "concepts": ["surfaces-civil-3d"]},
            {"name": "Week 3-4: Alignments & Profiles", "topics": ["Horizontal alignments", "Profile views", "Vertical alignment design", "Superelevation"], "concepts": ["alignments-civil-3d"]},
            {"name": "Week 5-6: Corridors", "topics": ["Assembly creation", "Corridor modeling", "Corridor surfaces", "Quantity takeoff"], "concepts": ["corridors-civil-3d", "assemblies-civil-3d"]},
            {"name": "Week 7-8: Grading & Pipes", "topics": ["Grading objects", "Pipe networks", "Pressure pipe networks", "Plan production"], "concepts": ["grading-civil-3d", "pipe-networks-civil-3d"]},
        ],
    },
    {
        "slug": "freecad-beginner",
        "software": "FreeCAD",
        "sw_slug": "freecad",
        "title": "FreeCAD Beginner Learning Path",
        "desc": "4-week FreeCAD learning path for beginners. Learn parametric modeling, Part Design workbench, assemblies, and technical drawings in the free open-source CAD platform.",
        "duration": "4 weeks",
        "level": "Beginner",
        "prereqs": "Basic computer skills",
        "stages": [
            {"name": "Week 1: Getting Started", "topics": ["Workbench concept", "Navigation and views", "Document structure", "Sketch constraints"], "concepts": ["addon-manager", "bim-workbench"]},
            {"name": "Week 2: Part Design", "topics": ["Sketcher workbench", "Pad, pocket, revolve", "Fillets and chamfers", "Boolean operations"], "concepts": ["fem-workbench", "path-workbench"]},
            {"name": "Week 3: Assembly & TechDraw", "topics": ["Assembly workbenches (A2plus/Assembly4)", "TechDraw for 2D documentation", "Dimensions and annotations", "Export to PDF/DXF"], "concepts": ["assembly-workbenches-fc", "techdraw-workbench"]},
            {"name": "Week 4: Scripting & BIM", "topics": ["Python macro basics", "Custom object creation", "BIM workbench intro", "IFC export"], "concepts": ["bim-workbench", "draft-workbench"]},
        ],
    },
    {
        "slug": "archicad-beginner",
        "software": "ArchiCAD",
        "sw_slug": "archicad",
        "title": "ArchiCAD Beginner Learning Path",
        "desc": "6-week ArchiCAD learning path for architecture students. Master BIM modeling, smart building elements, documentation, and IFC-based collaboration.",
        "duration": "6 weeks",
        "level": "Beginner to Intermediate",
        "prereqs": "Basic architectural drawing knowledge",
        "stages": [
            {"name": "Week 1: Basics", "topics": ["Project setup and templates", "Navigation and views", "Story structure", "Basic tools overview"], "concepts": ["archicad-term-1"]},
            {"name": "Week 2: Building Elements", "topics": ["Walls, slabs, roofs", "Doors and windows", "Columns and beams", "Object tool (GDL)"], "concepts": ["archicad-term-2"]},
            {"name": "Week 3: Modeling", "topics": ["Morph tool", "Complex profiles", "Curtain wall system", "Shell tool"], "concepts": ["archicad-term-3"]},
            {"name": "Week 4: Documentation", "topics": ["Floor plans and sections", "Elevations and 3D documents", "Dimensions and labels", "Zone stamps"], "concepts": ["archicad-term-1"]},
            {"name": "Week 5: Schedules & Visualization", "topics": ["Interactive schedules", "Materials and surfaces", "CineRender basics", "BIMx export"], "concepts": ["archicad-term-2"]},
            {"name": "Week 6: Collaboration", "topics": ["Teamwork setup", "Hotlinked modules", "IFC export/import", "Publisher sets"], "concepts": ["archicad-term-3"]},
        ],
    },
    {
        "slug": "rhinoceros-beginner",
        "software": "Rhino",
        "sw_slug": "rhinoceros",
        "title": "Rhino (Rhinoceros) Beginner Learning Path",
        "desc": "5-week Rhino learning path covering NURBS geometry, surface modeling, Grasshopper parametric design, and rendering workflows for architects and industrial designers.",
        "duration": "5 weeks",
        "level": "Beginner to Intermediate",
        "prereqs": "Basic 3D spatial understanding",
        "stages": [
            {"name": "Week 1: NURBS Fundamentals", "topics": ["Points, curves, surfaces", "Degree and control points", "Curve editing tools", "Surface from curves"], "concepts": ["rhinoceros-term-1"]},
            {"name": "Week 2: Surface Modeling", "topics": ["Loft, sweep, revolve", "Network surface", "Blend and match surfaces", "Trimming and splitting"], "concepts": ["rhinoceros-term-1"]},
            {"name": "Week 3: Solids & SubD", "topics": ["Boolean operations", "SubD modeling", "Mesh tools", "Analysis tools (curvature, zebra)"], "concepts": ["rhinoceros-term-2"]},
            {"name": "Week 4: Grasshopper Intro", "topics": ["Visual programming basics", "Data trees", "Parametric geometry", "Basic plugins (Ladybug, Kangaroo)"], "concepts": ["rhinoceros-term-2"]},
            {"name": "Week 5: Rendering & Output", "topics": ["V-Ray / Cycles setup", "Materials and lighting", "2D drawing production (Make2D)", "Export for fabrication"], "concepts": ["rhinoceros-term-1"]},
        ],
    },
    {
        "slug": "sketchup-beginner",
        "software": "SketchUp",
        "sw_slug": "sketchup",
        "title": "SketchUp Beginner Learning Path",
        "desc": "3-week SketchUp learning path for quick conceptual 3D modeling. Learn push-pull geometry, components, materials, and presentation techniques.",
        "duration": "3 weeks",
        "level": "Beginner",
        "prereqs": "Basic computer skills",
        "stages": [
            {"name": "Week 1: Core Tools", "topics": ["Push/pull paradigm", "Drawing and inference", "Groups and components", "Orbit, zoom, pan"], "concepts": []},
            {"name": "Week 2: Modeling Techniques", "topics": ["Follow-me tool", "Solid tools", "3D Warehouse usage", "Section planes"], "concepts": []},
            {"name": "Week 3: Presentation", "topics": ["Materials and textures", "Scenes and animation", "Layout for 2D docs", "Extensions ecosystem"], "concepts": []},
        ],
    },
    {
        "slug": "catia-beginner",
        "software": "CATIA",
        "sw_slug": "catia",
        "title": "CATIA Beginner Learning Path",
        "desc": "8-week CATIA V5/3DEXPERIENCE learning path for aerospace and automotive engineers. Master part design, surface modeling, assembly design, and drafting.",
        "duration": "8 weeks",
        "level": "Beginner to Intermediate",
        "prereqs": "Engineering drawing fundamentals, basic 3D concepts",
        "stages": [
            {"name": "Week 1-2: Part Design", "topics": ["Sketcher constraints", "Pad, pocket, shaft", "Dress-up features", "Boolean operations"], "concepts": ["catia-term-1"]},
            {"name": "Week 3-4: Surface Design", "topics": ["Wireframe and surface workbench", "Fill, blend, sweep", "Surface analysis (curvature)", "Hybrid design methodology"], "concepts": ["catia-term-2"]},
            {"name": "Week 5-6: Assembly", "topics": ["Product structure", "Constraints (fix, offset, angle)", "Assembly features", "Interference analysis"], "concepts": ["catia-term-3"]},
            {"name": "Week 7-8: Drafting & Advanced", "topics": ["Drawing generation", "Annotations and GD&T", "Knowledge Advisor basics", "Design tables"], "concepts": ["catia-term-4", "catia-term-5"]},
        ],
    },
    {
        "slug": "siemens-nx-beginner",
        "software": "Siemens NX",
        "sw_slug": "siemens-nx",
        "title": "Siemens NX Beginner Learning Path",
        "desc": "8-week Siemens NX learning path for product development engineers. Cover synchronous technology, part modeling, assembly, drafting, and basic simulation.",
        "duration": "8 weeks",
        "level": "Beginner to Intermediate",
        "prereqs": "Mechanical engineering fundamentals",
        "stages": [
            {"name": "Week 1-2: Basics & Sketching", "topics": ["NX interface and roles", "Sketch constraints", "Feature-based modeling", "Expressions and parameters"], "concepts": ["assembly-constraints-nx"]},
            {"name": "Week 3-4: Solid Modeling", "topics": ["Extrude, revolve, sweep", "Synchronous technology", "Direct editing", "Pattern and mirror features"], "concepts": ["pmi-nx"]},
            {"name": "Week 5-6: Assembly", "topics": ["Assembly constraints", "WAVE geometry linker", "Arrangement and positioning", "Clash detection"], "concepts": ["assembly-constraints-nx"]},
            {"name": "Week 7-8: Drafting & PMI", "topics": ["Drawing views", "PMI annotations (3D)", "Dimension and tolerancing", "Sheet metal design basics"], "concepts": ["pmi-nx", "direct-edit-nx"]},
        ],
    },
    {
        "slug": "bricscad-beginner",
        "software": "BricsCAD",
        "sw_slug": "bricscad",
        "title": "BricsCAD Beginner Learning Path",
        "desc": "5-week BricsCAD learning path covering DWG-native drafting, 3D direct modeling, BIM workflows, and AI-assisted design features.",
        "duration": "5 weeks",
        "level": "Beginner to Intermediate",
        "prereqs": "Basic drafting knowledge (AutoCAD experience helpful)",
        "stages": [
            {"name": "Week 1: DWG Drafting", "topics": ["Interface familiar to AutoCAD users", "Drawing and editing commands", "Layers and properties", "Command line and quad cursor"], "concepts": ["bricscad-term-1"]},
            {"name": "Week 2: Blocks & References", "topics": ["Block creation and insertion", "Dynamic blocks", "External references", "Sheet sets"], "concepts": ["bricscad-term-2"]},
            {"name": "Week 3: 3D Modeling", "topics": ["Direct modeling paradigm", "Push/pull 3D editing", "AI-assisted modeling", "Solid and surface tools"], "concepts": ["bricscad-term-3"]},
            {"name": "Week 4: BIM Mode", "topics": ["BIM classification", "IFC import/export", "Propagate and composition", "BIM project browser"], "concepts": ["bricscad-term-4"]},
            {"name": "Week 5: Automation", "topics": ["LISP scripting", "BRX SDK basics", "Mechanical components", "Sheet metal design"], "concepts": ["bricscad-term-5", "bricscad-term-6"]},
        ],
    },
]


def generate_path_page(path_data):
    """Generate a learning path HTML page."""
    p = path_data
    canonical = f"https://gstarcademy.com/kb/learning-paths/{p['slug']}"
    
    # Build stages HTML
    stages_html = ""
    for i, stage in enumerate(p["stages"], 1):
        topics_li = "\n".join(f'              <li>{t}</li>' for t in stage["topics"])
        concepts_links = ""
        if stage.get("concepts"):
            links = " ".join(
                f'<a href="../concepts/{c}" style="display: inline-block; padding: 4px 10px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 6px; font-size: 12px; text-decoration: none; color: var(--ink-text); font-weight: 500;">{c}</a>'
                for c in stage["concepts"]
            )
            concepts_links = f'\n              <p style="margin-top: 12px; font-size: 12px; color: var(--ink-text-soft);"><strong>Related concepts:</strong></p>\n              <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px;">{links}</div>'
        
        stages_html += f'''
        <div style="margin-bottom: 24px; padding: 20px 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 14px; border-left: 4px solid var(--accent);">
          <h3 style="margin: 0 0 12px; font-size: 1rem; font-weight: 700; color: var(--ink-text);">Stage {i}: {stage["name"]}</h3>
          <ul style="margin: 0; padding-left: 20px; font-size: 14px; line-height: 1.8;">
{topics_li}
          </ul>{concepts_links}
        </div>'''

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
    <title>{p['title']} | Gstarcademy</title>
    <meta name="description" content="{p['desc']}" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <link rel="canonical" href="{canonical}" />
    <meta property="og:image" content="https://gstarcademy.com/images/og-default.webp" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{p['title']}" />
    <meta property="og:description" content="{p['desc']}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:site_name" content="Gstarcademy" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{p['title']}" />
    <meta name="twitter:description" content="{p['desc']}" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="preload" href="../../styles.min.css" as="style" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />
    <link rel="stylesheet" href="../../styles.min.css" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Course","name":"{p['title']}","description":"{p['desc']}","provider":{{"@type":"Organization","name":"Gstarcademy","url":"https://gstarcademy.com"}},"educationalLevel":"{p['level']}","timeRequired":"P{p['duration'].split()[0]}W","url":"{canonical}"}}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://gstarcademy.com/"}},{{"@type":"ListItem","position":2,"name":"Knowledge Base","item":"https://gstarcademy.com/knowledge-base"}},{{"@type":"ListItem","position":3,"name":"Learning Paths","item":"https://gstarcademy.com/kb/learning-paths/"}},{{"@type":"ListItem","position":4,"name":"{p['title']}","item":"{canonical}"}}]}}</script>
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
        <a href="./">Learning Paths</a> /
        <span aria-current="page">{p['software']}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 28px;">
          <span class="chip pill-warn">Learning Path &middot; {p['software']}</span>
          <h1 style="margin-top: 12px;">{p['title']}</h1>
          <p class="hero-sub">{p['desc']}</p>
        </header>

        <div class="ink-byline" role="contentinfo">
          <span><strong>By</strong> Gstarcademy Editorial Team</span>
          <span><strong>Updated</strong> <time datetime="{TODAY}">{TODAY}</time></span>
          <span><a href="../../editorial-process">Editorial process</a></span>
        </div>

        <section class="kb-concept-section">
          <h2>Path Overview</h2>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-top: 16px;">
            <div style="padding: 16px; background: var(--ink-surface-2); border-radius: 10px; text-align: center;">
              <p style="font-size: 20px; font-weight: 800; color: var(--accent); margin: 0;">{p['duration']}</p>
              <p style="font-size: 12px; color: var(--ink-text-soft); margin: 4px 0 0;">Duration</p>
            </div>
            <div style="padding: 16px; background: var(--ink-surface-2); border-radius: 10px; text-align: center;">
              <p style="font-size: 20px; font-weight: 800; color: var(--accent); margin: 0;">{len(p['stages'])}</p>
              <p style="font-size: 12px; color: var(--ink-text-soft); margin: 4px 0 0;">Stages</p>
            </div>
            <div style="padding: 16px; background: var(--ink-surface-2); border-radius: 10px; text-align: center;">
              <p style="font-size: 20px; font-weight: 800; color: var(--accent); margin: 0;">{p['level'].split(' to ')[0]}</p>
              <p style="font-size: 12px; color: var(--ink-text-soft); margin: 4px 0 0;">Start Level</p>
            </div>
          </div>
          <p style="margin-top: 16px;"><strong>Prerequisites:</strong> {p['prereqs']}</p>
          <p>This structured learning path for <a href="../software/{p['sw_slug']}">{p['software']}</a> is designed to take you from {p['level'].split(' to ')[0].lower()} to {p['level'].split(' to ')[-1].lower()} level through progressive stages. Each stage builds on the previous one, so follow them in order for best results.</p>
        </section>

        <section class="kb-concept-section">
          <h2>Learning Stages</h2>
          {stages_html}
        </section>

        <section class="kb-concept-section">
          <h2>Tips for Success</h2>
          <ul>
            <li><strong>Practice daily:</strong> Even 30 minutes of hands-on practice is more effective than hours of passive watching</li>
            <li><strong>Use real projects:</strong> Apply each stage's skills to a personal or work project immediately</li>
            <li><strong>Join communities:</strong> {p['software']} forums and Discord/Reddit communities accelerate learning through peer support</li>
            <li><strong>Review our tutorials:</strong> Visit the <a href="../../tutorials">tutorial library</a> for curated video content matching each stage</li>
          </ul>
        </section>

        <section class="kb-concept-section">
          <h2>Next Steps After Completion</h2>
          <p>Once you complete this path, consider:</p>
          <ul>
            <li>Exploring advanced {p['software']} features through our <a href="../software/{p['sw_slug']}">{p['software']} knowledge articles</a></li>
            <li>Taking vendor certification exams to validate your skills</li>
            <li>Contributing to your team's template and standards library</li>
            <li>Exploring related software through our <a href="../compare/">comparison guides</a></li>
          </ul>
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

        <p class="meta" style="margin-top: 36px; font-size: 12px;">Learning path curated by Gstarcademy Editorial Team. Software names and trademarks belong to their respective owners.</p>
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
        <p>&copy; <span id="footer-year"></span> Gstarcademy. All rights reserved.</p>
      </div>
    </footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    return html


def generate_index():
    """Generate learning paths index page."""
    links = "\n".join(
        f'        <a href="./{p["slug"]}" style="display: block; padding: 20px 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 14px; text-decoration: none; color: var(--ink-text); margin-bottom: 12px;"><strong style="font-size: 1rem;">{p["software"]} Learning Path</strong><br><span style="font-size: 13px; color: var(--ink-text-soft);">{p["duration"]} &middot; {p["level"]}</span></a>'
        for p in PATHS
    )
    
    html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CAD Learning Paths — Structured Study Guides by Software | Gstarcademy</title>
    <meta name="description" content="Structured learning paths for AutoCAD, GstarCAD, Revit, SOLIDWORKS, Fusion 360, Blender, Civil 3D, FreeCAD, and more. Follow step-by-step stages from beginner to intermediate." />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <link rel="canonical" href="https://gstarcademy.com/kb/learning-paths/" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="CAD Learning Paths" />
    <meta property="og:description" content="Structured learning paths for CAD software." />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="preload" href="../../styles.min.css" as="style" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />
    <link rel="stylesheet" href="../../styles.min.css" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"CAD Learning Paths","description":"Structured study guides by software.","url":"https://gstarcademy.com/kb/learning-paths/"}}</script>
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
        <a href="../../">Home</a> / <a href="../../knowledge-base">Knowledge Base</a> / <span aria-current="page">Learning Paths</span>
      </nav>
      <h1 style="margin-top: 16px;">CAD Learning Paths</h1>
      <p style="font-size: 15px; color: var(--ink-text-soft); margin-bottom: 32px;">Structured study guides for {len(PATHS)} major CAD platforms. Each path provides progressive stages with clear milestones, helping you build skills systematically.</p>
      <div>
{links}
      </div>
    </main>
    <footer class="footer site-footer">
      <div class="container site-footer-inner">
        <div class="site-footer-brand"><p class="site-footer-tagline">Gstarcademy</p></div>
      </div>
      <div class="container site-footer-bottom"><p>&copy; <span id="footer-year"></span> Gstarcademy. All rights reserved.</p></div>
    </footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    print(f"Generating {len(PATHS)} learning path pages...")
    for p in PATHS:
        html = generate_path_page(p)
        filepath = os.path.join(OUTPUT_DIR, f"{p['slug']}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Generated: {p['slug']}")
    
    generate_index()
    print(f"\n Done! Generated {len(PATHS)} learning path pages + index")


if __name__ == '__main__':
    main()
