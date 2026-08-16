#!/usr/bin/env python3
"""
Generate comprehensive, in-depth CAD Learning Path pages.
Each page includes week-by-week curriculum, practical hands-on drawing assignments,
command mastery checklists, self-assessment quiz links, and capstone portfolio projects.
"""

import os
from datetime import date
from bs4 import BeautifulSoup

TODAY = date.today().isoformat()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'learning-paths')
os.makedirs(OUTPUT_DIR, exist_ok=True)

PATHS = [
    {
        "slug": "autocad-beginner",
        "software": "AutoCAD",
        "sw_slug": "autocad",
        "title": "AutoCAD Beginner to Professional 6-Week Learning Path",
        "desc": "Structured 6-week AutoCAD learning path. Master 2D drafting fundamentals, geometric constraints, layer governance, dynamic blocks, annotative dimensions, and paper space plotting with hands-on weekly milestones.",
        "duration": "6 weeks (6-8 hours / week)",
        "level": "Beginner to Intermediate",
        "prereqs": "Basic computer literacy and foundational understanding of engineering geometry.",
        "capstone": "Complete Architectural & Mechanical Drawing Package: Author a 3-sheet A1 construction document set including ground floor plan with dynamic door/window blocks, section detail with hatch materials, and title block with automated attribute fields.",
        "stages": [
            {
                "name": "Week 1: Interface Mastery, Navigation & Coordinate Geometry",
                "topics": ["AutoCAD workspace customization & Ribbon/Command bar setup", "Precision coordinate systems (Absolute, Relative Cartesian @X,Y, Polar @Dist<Angle)", "Viewport navigation (Pan, Zoom Extents/Window, CleanScreen)", "Drawing units setup (UNITS, LIMITS) & seed template initialization (.DWT)"],
                "assignment": "Draw a precise mechanical spacer plate using polar coordinates with exact vertex snaps (Endpoint, Midpoint, Center).",
                "commands": "L, PL, C, REC, UNITS, LIMITS, OSNAP, DYNMODE",
                "concepts": ["dynamic-input", "dwg-file-format"]
            },
            {
                "name": "Week 2: Advanced 2D Geometry & Object Snap Tracking",
                "topics": ["Complex polylines, arcs, splines, and construction lines (XLINE)", "Object Snap Tracking (F11) and Polar Tracking (F10) angles", "Parametric geometric constraints (Coincident, Tangent, Concentric, Parallel)", "Boundary creation (BOUNDARY) and Region analysis (MASSPROP)"],
                "assignment": "Construct a multi-curved transmission gear silhouette with tangent fillets and polar pitch circle layout.",
                "commands": "ARC, SPLINE, XLINE, FILLET, CHAMFER, CONSTRAINTSETTINGS",
                "concepts": ["annotative-objects"]
            },
            {
                "name": "Week 3: Precision Modification & Transform Operations",
                "topics": ["Transform tools: Move, Copy, Rotate with Reference angle, Mirror", "Trimming, Extending, Offsetting, and Stretching geometry (STRETCH crossing window)", "Associative rectangular, polar, and path arrays (ARRAY)", "Grips editing and multi-functional vertex modification"],
                "assignment": "Build an architectural staircase with 18 uniform treads and circular handrail balusters using rectangular and polar arrays.",
                "commands": "M, CO, RO, MI, TR, EX, O, S, ARRAY, JOIN, EXPLODE",
                "concepts": ["dynamic-blocks-autocad"]
            },
            {
                "name": "Week 4: Layer Governance, Lineweights & Block Libraries",
                "topics": ["National CAD Standard (NCS) layer hierarchies (Layer naming, colors, linetypes)", "Layer States Manager and Layer Freeze/Lock in Viewports", "Internal Block creation (BLOCK) on Layer 0 with ByLayer attributes", "Dynamic Blocks with stretch parameters, visibility states, and WBLOCK library export"],
                "assignment": "Create a standardized office furniture block library with dynamic stretch actions for desks (1200-1800mm).",
                "commands": "LAYER, LAYTRANS, BLOCK, WBLOCK, BEDIT, ATTDEF, BATTMAN",
                "concepts": ["layers-gstarcad", "attributes-blocks", "how-to-create-blocks-autocad"]
            },
            {
                "name": "Week 5: Annotative Scaling, Hatching & Tabular Data",
                "topics": ["Annotative dimension styles (DIMSTYLE) across multiple scales (1:50, 1:100)", "Multiline text (MTEXT), leader styles (MLEADER), and spell check", "Associative Hatching (HATCH) with custom scale, pattern origins, and gradient fills", "Table creation (TABLE) and field codes linked to object properties"],
                "assignment": "Fully dimension a residential floor plan with room area tags, section callout symbols, and a live door/window schedule table.",
                "commands": "DIMSTYLE, DIMLINEAR, DIMALIGNED, MTEXT, MLEADER, HATCH, TABLE",
                "concepts": ["annotative-objects", "how-to-scale-in-autocad"]
            },
            {
                "name": "Week 6: Paper Space Layouts, Sheet Sets & Batch PDF Publishing",
                "topics": ["Model space vs Paper space layout concepts (TILEMODE)", "Creating and scaling viewports (MVIEW, VP Scale locking)", "Page Setup Manager & CTB monochrome/color-dependent plot style tables", "Multi-sheet batch publishing (PUBLISH) and eTransmit archive packaging"],
                "assignment": "Assemble and publish a 3-sheet vector PDF submission package at 1:50 scale with border title blocks and locked viewports.",
                "commands": "LAYOUT, MVIEW, PAGESETUP, PLOT, PUBLISH, ETRANSMIT, SSM",
                "concepts": ["paper-space-autocad", "how-to-print-autocad", "how-to-use-xrefs-autocad"]
            }
        ]
    },
    {
        "slug": "gstarcad-beginner",
        "software": "GstarCAD",
        "sw_slug": "gstarcad",
        "title": "GstarCAD Beginner to Advanced 5-Week Mastery Path",
        "desc": "Complete 5-week GstarCAD learning curriculum. Master DWG-native high-speed drafting, dynamic blocks, layer management, AutoLISP customization, and multi-sheet batch plotting.",
        "duration": "5 weeks (5-7 hours / week)",
        "level": "Beginner to Intermediate",
        "prereqs": "Basic computer literacy and willingness to learn standard DWG drafting practices.",
        "capstone": "Produce a complete industrial machinery foundation layout with dynamic components, bill of materials table, and automated LISP script routine.",
        "stages": [
            {
                "name": "Week 1: Interface Optimization & Core DWG Setup",
                "topics": ["GstarCAD workspace configuration (Ribbon vs Classic Interface)", "Hardware graphics acceleration setup (GRAPHICSCONFIG)", "Drawing setup (UNITS, LIMITS, Grid snap)", "Quick Properties and heads-up dynamic cursor drafting"],
                "assignment": "Draw an accurate structural anchor plate with counterbored holes and centerlines.",
                "commands": "UNITS, GRAPHICSCONFIG, LINE, CIRCLE, RECTANG, DYNMODE",
                "concepts": ["gstarcad-system-requirements", "how-to-migrate-autocad-to-gstarcad"]
            },
            {
                "name": "Week 2: Precision 2D Construction & Layer Strategy",
                "topics": ["Object snap modes (Center, Quadrant, Tangent, Perpendicular)", "Modify tools (Offset, Trim, Fillet, Chamfer, Mirror)", "Layer management, color coding by lineweight, and layer filters", "Design Center and Tool Palette integration"],
                "assignment": "Draft a multi-room commercial layout with designated architectural, electrical, and furniture layers.",
                "commands": "OFFSET, TRIM, EXTEND, FILLET, LAYER, ADCENTER, TOOLPALETTES",
                "concepts": ["layers-gstarcad"]
            },
            {
                "name": "Week 3: Blocks, Dynamic Parameters & Quantity Takeoff",
                "topics": ["Block creation on Layer 0 with ByLayer attributes", "Authoring Dynamic Blocks with visibility states and stretch actions", "GstarCAD unique tools: Free Scale, Magnifier, and Barcode generator", "Block data extraction to Excel / CSV tables"],
                "assignment": "Create a dynamic electrical receptacle block with single/duplex/GFCI visibility states and extract component quantities.",
                "commands": "BLOCK, WBLOCK, BEDIT, ATTDEF, EATTEXT, FREESCALE",
                "concepts": ["attributes-blocks", "dynamic-blocks-autocad"]
            },
            {
                "name": "Week 4: Annotations, Tables & Multi-Sheet Plotting",
                "topics": ["Annotative text and dimension styles (Linear, Aligned, Radius)", "Table creation and live mathematical spreadsheet formulas", "Paper space layout viewports and scale locking", "Batch Plotting multi-drawing DWG files to unified PDF packages"],
                "assignment": "Publish an annotated manufacturing assembly drawing with balloon callouts and a linked BOM parts list.",
                "commands": "DIMSTYLE, MTEXT, TABLE, MVIEW, PAGESETUP, BATCHPLOT",
                "concepts": ["annotative-objects-gstarcad", "how-to-print-autocad"]
            },
            {
                "name": "Week 5: AutoLISP Scripting & Enterprise Workflow Automation",
                "topics": ["AutoLISP syntax fundamentals (defun, setq, getpoint, command)", "Loading custom LSP/VLX routines via APPLOAD and Startup Suite", "Custom command aliases in gcad.pgp", "Migrating legacy AutoCAD toolbars and menu macros to GstarCAD"],
                "assignment": "Write a custom AutoLISP routine that automatically draws a standardized labeled rectangle with user-prompted length and width.",
                "commands": "APPLOAD, VLIDE, ALIASEDIT, CUI, REINIT",
                "concepts": ["autolisp-gstarcad", "autolisp"]
            }
        ]
    },
    {
        "slug": "revit-beginner",
        "software": "Revit",
        "sw_slug": "revit",
        "title": "Revit Architecture BIM 8-Week Professional Learning Path",
        "desc": "Comprehensive 8-week Autodesk Revit BIM curriculum. Progress from basic BIM concepts to multi-story building models, parametric family authoring, construction sheets, and IFC collaboration.",
        "duration": "8 weeks (8-10 hours / week)",
        "level": "Beginner to Advanced",
        "prereqs": "Understanding of architectural drawing conventions and building construction systems.",
        "capstone": "Full BIM Digital Twin: Model a 3-story commercial office building complete with curtain wall facade, egress stairs, structural framing, HVAC coordination, and live quantity takeoff schedules.",
        "stages": [
            {
                "name": "Week 1-2: BIM Fundamentals, Levels, Grids & Core Enclosures",
                "topics": ["BIM methodology vs traditional 2D CAD (Parameters & digital twins)", "Revit project browser, view controls, and visual styles", "Establishing Building Levels and Column Grids", "Basic multi-layer exterior walls, interior partitions, and floor slabs"],
                "assignment": "Construct the structural grid and exterior shell for a 2-story commercial pavilion with accurate finish materials.",
                "commands": "LL (Level), GR (Grid), WA (Wall), FL (Floor), AL (Align)",
                "concepts": ["revit-vs-autocad-which-to-learn", "bim-workbench"]
            },
            {
                "name": "Week 3-4: Doors, Windows, Curtain Walls, Roofs & Stairs",
                "topics": ["Placing hosted components (Doors, Windows, Openings)", "Curtain wall systems: Grids, Mullions, and Custom Glazing panels", "Roofs by Footprint, Roofs by Extrusion, and soffit/fascia trims", "Component-based stairs, railings, and multi-landing egress stairs"],
                "assignment": "Model a double-height glazed entrance atrium with custom aluminum mullions and a feature steel spiral staircase.",
                "commands": "DR (Door), WN (Window), CW (Curtain Wall), ROOF, STAIR",
                "concepts": ["construction-documentation"]
            },
            {
                "name": "Week 5-6: Parametric Family Authoring & Shared Parameters",
                "topics": ["Family Editor templates (.RFT) and Category behavior", "Reference Planes skeleton (RP), EQ constraints, and driving dimensions", "Type vs Instance parameters and Shared Parameters (.TXT file)", "Flexing geometry, formula equations, and subcategories for line control"],
                "assignment": "Build a fully parametric casework kitchen cabinet with selectable door styles, width options, and material parameters.",
                "commands": "RP (Ref Plane), DI (Dimension), EQ, FAMILYTYPES, LOADPROJECT",
                "concepts": ["how-to-create-family-revit"]
            },
            {
                "name": "Week 7-8: View Templates, Sheet Documentation & Collaboration",
                "topics": ["View Templates, Graphic Overrides (VG), and Crop regions", "Room tags, Color Fill Schemes, and Door/Window Schedules", "Creating Sheets, title blocks, and viewport guide grids", "Worksharing (Central Model, Worksets) and exporting to IFC / DWG"],
                "assignment": "Assemble a complete 6-sheet architectural permit package with plans, elevations, wall sections, and room finish schedules.",
                "commands": "VG (Visibility/Graphics), RT (Room Tag), SHEET, SCHEDULE, WORKSETS",
                "concepts": ["how-to-create-sheets-revit", "cad-collaboration-remote-teams"]
            }
        ]
    },
    {
        "slug": "solidworks-beginner",
        "software": "SOLIDWORKS",
        "sw_slug": "solidworks",
        "title": "SOLIDWORKS Mechanical Design 6-Week Professional Learning Path",
        "desc": "In-depth 6-week SOLIDWORKS curriculum for mechanical engineering students and product designers. Master parametric sketching, 3D solids, complex assemblies, GD&T drawings, and FEA simulation.",
        "duration": "6 weeks (7-9 hours / week)",
        "level": "Beginner to Intermediate",
        "prereqs": "Familiarity with mechanical engineering drawings and basic manufacturing processes.",
        "capstone": "Design an Industrial Gearbox Reducer: Model high-precision gears, shafts, bearings, and split housing; apply assembly mates; conduct motion collision analysis; and produce full ASME Y14.5 manufacturing drawings with GD&T.",
        "stages": [
            {
                "name": "Week 1: Parametric 2D Sketching & Constraint Discipline",
                "topics": ["Sketch plane selection (Front, Top, Right) and sketch tools", "Geometric relations (Coincident, Tangent, Concentric, Symmetric, Collinear)", "Smart Dimensions, driven vs driving dimensions, and design intent", "Solving under-constrained sketches to achieve green 'Fully Defined' status"],
                "assignment": "Sketch a fully constrained connecting rod cross-section profile with tangent radii and symmetry relations.",
                "commands": "Line, Circle, Arc, Smart Dimension, Add Relation, Fully Defined Sketch",
                "concepts": ["fusion-360-vs-solidworks-which-better"]
            },
            {
                "name": "Week 2: Core 3D Features (Extrude, Revolve, Sweep & Loft)",
                "topics": ["Boss/Base Extrude with draft angles and thin-feature options", "Revolved Boss/Base and Revolved Cuts around centerlines", "Sweep along guide curves and Loft between non-parallel profiles", "Applied features: Fillets (constant/variable radius), Chamfers, and Shell"],
                "assignment": "Model a cast aluminum valve body with internal fluid passageways and mounting bolt flanges.",
                "commands": "Extrude, Revolve, Sweep, Loft, Shell, Fillet, Chamfer",
                "concepts": ["bottom-up-design"]
            },
            {
                "name": "Week 3: Advanced Features, Patterns, Configurations & Tables",
                "topics": ["Linear and Circular component patterns with feature skipping", "Hole Wizard for standard metric (ISO) and imperial tapped holes", "Part Configurations and Design Tables (Excel-driven geometry)", "Multi-body part modeling and direct Boolean operations (Combine)"],
                "assignment": "Create a standard fastener catalog part with 12 distinct metric screw configurations driven by a Design Table.",
                "commands": "Hole Wizard, Linear Pattern, Circular Pattern, Configuration Manager, Combine",
                "concepts": ["quality-assurance-cad"]
            },
            {
                "name": "Week 4: Bottom-Up & Top-Down Assembly Modeling",
                "topics": ["Inserting components and fixing base grounding parts", "Standard mates (Coincident, Concentric, Distance, Parallel)", "Advanced mates (Width, Path, Limit) and Mechanical mates (Gear, Cam)", "Interference Detection, Clearance Verification, and Exploded Views"],
                "assignment": "Assemble a 4-bar linkage mechanism with crank handle and run motion simulation to detect pinch points.",
                "commands": "Insert Component, Mate, Width Mate, Gear Mate, Interference Detection, Exploded View",
                "concepts": ["how-to-create-assembly-solidworks"]
            },
            {
                "name": "Week 5: 2D Detailing, GD&T Tolerancing & BOM Tables",
                "topics": ["Drawing sheet formats (.SLDDRT) and projection angles (1st vs 3rd Angle)", "Standard orthographic, section, detail, and auxiliary views", "Importing driving model dimensions (Model Items) vs Smart Dimensions", "Geometric Dimensioning & Tolerancing (GD&T per ASME Y14.5) and Bill of Materials (BOM)"],
                "assignment": "Produce a complete shop drawing for a machined drive shaft with runout and positional tolerances.",
                "commands": "Make Drawing, Model Items, Section View, Detail View, Geometric Tolerance, Bill of Materials",
                "concepts": ["how-to-create-drawing-solidworks", "solidworks-file-formats"]
            },
            {
                "name": "Week 6: FEA Stress Analysis, Sheet Metal & CAM Export",
                "topics": ["SOLIDWORKS SimulationXpress (fixtures, loads, von Mises stress, Factor of Safety)", "Sheet metal base flanges, edge flanges, and flat pattern unfolding", "3D printing mesh export (3MF / STL resolution tuning)", "Pack and Go archive bundling and STEP AP242 vendor exchange"],
                "assignment": "Perform static stress simulation on a crane lifting bracket to verify a minimum 2.5 Factor of Safety.",
                "commands": "SimulationXpress, Sheet Metal, Flat Pattern, Save As 3MF, Pack and Go",
                "concepts": ["quality-assurance-cad", "cad-file-management-best-practices"]
            }
        ]
    }
]

def generate_path_page(p):
    canonical = f"https://gstarcademy.com/kb/learning-paths/{p['slug']}"
    
    # Generate stages HTML
    stages_html = ""
    for idx, s in enumerate(p['stages'], 1):
        topics_li = "".join([f'<li style="margin-bottom: 6px; font-size: 14px; line-height: 1.6;">{t}</li>' for t in s['topics']])
        concept_links = ""
        if "concepts" in s:
            for c in s['concepts']:
                concept_links += f'<a href="../concepts/{c}" style="display: inline-block; padding: 4px 10px; font-size: 12px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 6px; text-decoration: none; color: var(--accent); margin-right: 6px; margin-top: 4px;">{c}</a>'

        stages_html += f'''
        <div style="margin-bottom: 28px; padding: 24px; background: var(--ink-surface); border: 1px solid var(--ink-line); border-radius: 14px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
            <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: var(--ink-text);">{s['name']}</h3>
            <span style="font-size: 12px; font-weight: 700; padding: 3px 10px; background: var(--accent-bg, #e0f2fe); color: var(--accent, #0284c7); border-radius: 20px;">Stage {idx}</span>
          </div>
          <p style="margin: 0 0 8px; font-size: 13px; font-weight: 700; text-transform: uppercase; color: var(--ink-text-soft);">Core Topics Covered:</p>
          <ul style="padding-left: 20px; color: var(--ink-text); margin-bottom: 16px;">
            {topics_li}
          </ul>
          <div style="margin-bottom: 16px; padding: 14px 16px; background: var(--ink-surface-2); border-left: 3px solid var(--accent, #0284c7); border-radius: 6px;">
            <p style="margin: 0; font-size: 13.5px; line-height: 1.6; color: var(--ink-text);"><strong>🛠️ Practical Hands-on Assignment:</strong> {s['assignment']}</p>
            <p style="margin: 6px 0 0; font-size: 12.5px; color: var(--ink-text-soft);"><strong>Key Commands / Tools:</strong> <code>{s.get('commands', 'Standard tools')}</code></p>
          </div>
          <div>
            <span style="font-size: 12px; font-weight: 600; color: var(--ink-text-soft); margin-right: 8px;">Recommended Concepts:</span>
            {concept_links}
          </div>
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
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{p['title']}" />
    <meta property="og:description" content="{p['desc']}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:site_name" content="Gstarcademy" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="preload" href="../../styles.min.css" as="style" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />
    <link rel="stylesheet" href="../../styles.min.css" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Course","name":"{p['title']}","description":"{p['desc']}","provider":{{"@type":"Organization","name":"Gstarcademy"}},"url":"{canonical}"}}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://gstarcademy.com/"}},{{"@type":"ListItem","position":2,"name":"Knowledge Base","item":"https://gstarcademy.com/knowledge-base"}},{{"@type":"ListItem","position":3,"name":"Learning Paths","item":"https://gstarcademy.com/kb/learning-paths/"}},{{"@type":"ListItem","position":4,"name":"{p['title']}","item":"{canonical}"}}]}}</script>
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
        <a href="./" style="color: var(--ink-text-soft);">Learning Paths</a> /
        <span aria-current="page" style="color: var(--ink-text);">{p['software']}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 28px;">
          <span class="chip pill-warn">Curriculum Roadmap &middot; {p['software']}</span>
          <h1 style="margin-top: 12px; font-size: 2.2rem; line-height: 1.25;">{p['title']}</h1>
          <p class="hero-sub" style="font-size: 16px; line-height: 1.6; color: var(--ink-text-soft);">{p['desc']}</p>
        </header>

        <div class="ink-byline" role="contentinfo" style="margin-bottom: 24px; font-size: 13px; color: var(--ink-text-soft); display: flex; gap: 16px; border-bottom: 1px solid var(--ink-line); padding-bottom: 12px;">
          <span><strong>Curriculum Director:</strong> Gstarcademy Engineering Editorial Board</span>
          <span><strong>Updated:</strong> <time datetime="{TODAY}">{TODAY}</time></span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 32px;">
          <div style="padding: 16px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px;">
            <span style="font-size: 12px; color: var(--ink-text-soft); text-transform: uppercase; font-weight: 700;">Duration</span>
            <p style="margin: 4px 0 0; font-size: 15px; font-weight: 700; color: var(--ink-text);">{p['duration']}</p>
          </div>
          <div style="padding: 16px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px;">
            <span style="font-size: 12px; color: var(--ink-text-soft); text-transform: uppercase; font-weight: 700;">Target Level</span>
            <p style="margin: 4px 0 0; font-size: 15px; font-weight: 700; color: var(--ink-text);">{p['level']}</p>
          </div>
          <div style="padding: 16px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px;">
            <span style="font-size: 12px; color: var(--ink-text-soft); text-transform: uppercase; font-weight: 700;">Self-Assessment</span>
            <p style="margin: 4px 0 0; font-size: 15px; font-weight: 700; color: var(--accent);"><a href="../../quiz" style="color: var(--accent); text-decoration: none;">Take CAD Quiz &rarr;</a></p>
          </div>
        </div>

        <section class="kb-concept-section">
          <h2>Prerequisites &amp; Setup Requirements</h2>
          <p style="font-size: 15px; line-height: 1.75; color: var(--ink-text);">{p['prereqs']}</p>
        </section>

        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Structured Learning Progression (Stage by Stage)</h2>
          {stages_html}
        </section>

        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Capstone Graduation Portfolio Project</h2>
          <div style="padding: 22px 24px; background: var(--accent-bg, #f0f9ff); border-left: 4px solid var(--accent, #0284c7); border-radius: 8px;">
            <p style="margin: 0; font-size: 15px; line-height: 1.75; font-weight: 500; color: var(--ink-text);">{p['capstone']}</p>
          </div>
        </section>

        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Next Steps &amp; Professional Certification</h2>
          <p style="font-size: 14.5px; line-height: 1.75; color: var(--ink-text);">Upon completing this learning path: review our <a href="../software/{p['sw_slug']}" style="color: var(--accent); font-weight: 600;">{p['software']} Documentation Hub</a>, test your retention with our interactive <a href="../../quiz" style="color: var(--accent); font-weight: 600;">CAD Certification Practice Quizzes</a>, or explore curated video courses in the <a href="../../tutorials" style="color: var(--accent); font-weight: 600;">Tutorials Directory</a>.</p>
        </section>

        <aside style="margin-top: 48px; padding: 20px 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 14px;">
          <p style="font-size: 13px; font-weight: 700; margin: 0 0 6px; color: var(--ink-text);">Gstarcademy Editorial Board</p>
          <p style="font-size: 12px; color: var(--ink-text-soft); margin: 0; line-height: 1.5;">Structured curriculum updated for 2026 industry standards. All registered trademarks belong to their respective holders.</p>
        </aside>
      </article>
    </main>

    <footer class="footer site-footer" style="margin-top: 60px;">
      <div class="container site-footer-inner">
        <div class="site-footer-brand"><p class="site-footer-tagline">Gstarcademy</p><p class="site-footer-desc">Professional CAD learning path guides and knowledge library.</p></div>
      </div>
      <div class="container site-footer-bottom"><p>&copy; <span id="footer-year"></span> Gstarcademy. All rights reserved.</p></div>
    </footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    return html

def main():
    import glob
    existing_files = glob.glob(os.path.join(OUTPUT_DIR, "*.html"))
    print(f"Enhancing {len(existing_files)} learning path pages in {OUTPUT_DIR}...")
    
    defined_slugs = {p["slug"] for p in PATHS}
    for p in PATHS:
        html = generate_path_page(p)
        with open(os.path.join(OUTPUT_DIR, f"{p['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(html)

    # For remaining learning path files, enrich them dynamically
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
            article = soup.find("article") or soup.find("main")
            if article:
                extra_sec = soup.new_tag("section", attrs={"class": "kb-concept-section", "style": "margin-top: 32px;"})
                ex_h2 = soup.new_tag("h2")
                ex_h2.string = "Capstone Project & Certification Milestones"
                ex_p1 = soup.new_tag("p")
                ex_p1.string = f"Completing this structured learning track requires producing a portfolio-grade capstone project: create full 2D production drawings with standard GD&T tolerances, build parametric multi-body assemblies, and pass self-assessment evaluation checkpoints in our CAD Quiz system."
                ex_p2 = soup.new_tag("p")
                ex_p2.string = f"Industry certifications (Autodesk ACP, SOLIDWORKS CSWP, buildingSMART openBIM) provide verified third-party validation of your software capabilities when applying for corporate design and engineering roles."
                extra_sec.append(ex_h2)
                extra_sec.append(ex_p1)
                extra_sec.append(ex_p2)
                article.append(extra_sec)
                
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(str(soup))

    print("Learning paths enhancement completed!")

if __name__ == "__main__":
    main()
