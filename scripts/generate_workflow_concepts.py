#!/usr/bin/env python3
"""
Generate additional workflow and terminology concept pages to reach 1000+ total.
These cover cross-platform CAD concepts and workflows.
"""

import os
from datetime import date

TODAY = date.today().isoformat()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'concepts')

WORKFLOW_CONCEPTS = [
    # General CAD/CAM/CAE concepts
    {"slug": "boolean-operations", "name": "Boolean Operations (Union, Subtract, Intersect)", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Boolean operations in CAD: union (add), subtract (cut), and intersect for combining solid bodies."},
    {"slug": "nurbs-surfaces", "name": "NURBS Surfaces", "software": "Multi-platform", "sw_slug": "rhinoceros", "desc": "Non-Uniform Rational B-Splines — the mathematical surface representation used by most CAD modeling kernels."},
    {"slug": "parametric-design-principles", "name": "Parametric Design Principles", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Core principles of parametric CAD: constraints, dimensions, feature history, and design intent capture."},
    {"slug": "gdt-geometric-tolerancing", "name": "GD&T (Geometric Dimensioning & Tolerancing)", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "ASME Y14.5 / ISO 1101 geometric tolerancing system for specifying form, orientation, and position tolerances."},
    {"slug": "design-for-manufacturing", "name": "Design for Manufacturing (DFM)", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "DFM principles in CAD: draft angles, wall thickness, undercuts, material selection, and manufacturing process awareness."},
    {"slug": "design-for-assembly", "name": "Design for Assembly (DFA)", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "DFA methodology in CAD: minimizing part count, self-locating features, and assembly sequence optimization."},
    {"slug": "finite-element-analysis", "name": "Finite Element Analysis (FEA) Fundamentals", "software": "Multi-platform", "sw_slug": "ansys-mechanical", "desc": "FEA basics: meshing, boundary conditions, solver types, convergence, and result interpretation for structural analysis."},
    {"slug": "cfd-fundamentals", "name": "CFD (Computational Fluid Dynamics) Basics", "software": "Multi-platform", "sw_slug": "ansys-mechanical", "desc": "CFD fundamentals for engineers: mesh generation, turbulence models, boundary conditions, and flow visualization."},
    {"slug": "topology-optimization", "name": "Topology Optimization & Generative Design", "software": "Multi-platform", "sw_slug": "fusion-360", "desc": "Topology optimization algorithms that remove material from a design space while maintaining structural requirements."},
    {"slug": "reverse-engineering-cad", "name": "Reverse Engineering in CAD", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Reverse engineering workflows: 3D scanning, point cloud processing, surface reconstruction, and parametric re-modeling."},
    {"slug": "plm-product-lifecycle", "name": "PLM (Product Lifecycle Management)", "software": "Multi-platform", "sw_slug": "siemens-nx", "desc": "PLM systems for managing product data, engineering changes, revision control, and cross-functional collaboration."},
    {"slug": "pdm-data-management", "name": "PDM (Product Data Management)", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "PDM systems for version control, file check-in/out, BOM management, and engineering release workflows."},
    {"slug": "bom-bill-of-materials", "name": "Bill of Materials (BOM)", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "BOM generation and management in CAD: engineering BOM vs manufacturing BOM, indented lists, and ERP integration."},
    {"slug": "drawing-standards-iso-asme", "name": "Drawing Standards (ISO vs ASME)", "software": "Multi-platform", "sw_slug": "autocad", "desc": "ISO 128/ISO 8015 vs ASME Y14 drawing standards: projection methods, dimensioning rules, and tolerancing conventions."},
    {"slug": "3d-printing-preparation", "name": "3D Print Preparation in CAD", "software": "Multi-platform", "sw_slug": "fusion-360", "desc": "Preparing CAD models for additive manufacturing: STL export, mesh repair, support structures, and build orientation."},
    {"slug": "cam-toolpath-fundamentals", "name": "CAM Toolpath Fundamentals", "software": "Multi-platform", "sw_slug": "fusion-360", "desc": "CNC machining toolpath types: contour, pocket, adaptive, 3D surface, and multi-axis strategies."},
    {"slug": "sheet-metal-design-principles", "name": "Sheet Metal Design Principles", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Sheet metal CAD fundamentals: bend radius, K-factor, relief types, flat pattern development, and DXF for laser cutting."},
    {"slug": "large-assembly-management", "name": "Large Assembly Management", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Techniques for working with large assemblies: lightweight mode, display states, simplified reps, and performance tuning."},
    {"slug": "coordinate-systems-cad", "name": "Coordinate Systems in CAD", "software": "Multi-platform", "sw_slug": "autocad", "desc": "World vs User coordinate systems, coordinate input methods, and coordinate system management across CAD platforms."},
    {"slug": "rendering-fundamentals", "name": "Rendering Fundamentals for CAD", "software": "Multi-platform", "sw_slug": "blender", "desc": "Rendering concepts for CAD visualization: ray tracing, PBR materials, HDRI lighting, and real-time vs offline rendering."},
    
    # BIM-specific concepts
    {"slug": "lod-level-of-development", "name": "LOD (Level of Development)", "software": "Multi-platform", "sw_slug": "revit", "desc": "BIM Level of Development framework (LOD 100-500) defining model detail and reliability at each project stage."},
    {"slug": "clash-detection-bim", "name": "Clash Detection in BIM", "software": "Multi-platform", "sw_slug": "revit", "desc": "Automated clash detection workflows for identifying spatial conflicts between building systems in BIM coordination."},
    {"slug": "4d-5d-bim", "name": "4D/5D BIM (Time & Cost)", "software": "Multi-platform", "sw_slug": "revit", "desc": "4D BIM (construction sequencing) and 5D BIM (cost estimation) for linking schedule and budget data to 3D models."},
    {"slug": "cde-common-data-environment", "name": "Common Data Environment (CDE)", "software": "Multi-platform", "sw_slug": "revit", "desc": "CDE platforms for BIM collaboration: shared repositories, approval workflows, and ISO 19650 compliance."},
    {"slug": "openbim-standards", "name": "openBIM & buildingSMART Standards", "software": "Multi-platform", "sw_slug": "archicad", "desc": "The openBIM movement: IFC, BCF, bSDD, and MVD standards for vendor-neutral BIM data exchange."},
    {"slug": "bim-execution-plan", "name": "BIM Execution Plan (BEP)", "software": "Multi-platform", "sw_slug": "revit", "desc": "BIM Execution Plans: defining model uses, LOD requirements, collaboration protocols, and deliverable specifications."},
    {"slug": "point-cloud-to-bim", "name": "Point Cloud to BIM (Scan-to-BIM)", "software": "Multi-platform", "sw_slug": "revit", "desc": "Scan-to-BIM workflows: laser scanning existing buildings, registering point clouds, and modeling BIM elements from scan data."},
    {"slug": "cobie-data", "name": "COBie (Construction Operations Building Information Exchange)", "software": "Multi-platform", "sw_slug": "revit", "desc": "COBie data standard for facility management handover: structured spreadsheet format linking BIM data to operations."},

    # Civil/Infrastructure concepts
    {"slug": "digital-terrain-model", "name": "Digital Terrain Model (DTM)", "software": "Multi-platform", "sw_slug": "civil-3d", "desc": "Digital Terrain Models: TIN surfaces, breaklines, contours, and terrain analysis for civil engineering design."},
    {"slug": "road-design-standards", "name": "Road Design Standards (AASHTO/Eurocode)", "software": "Multi-platform", "sw_slug": "civil-3d", "desc": "Highway geometric design standards: design speed, sight distance, horizontal/vertical curves, and cross-section elements."},
    {"slug": "stormwater-management", "name": "Stormwater Management Design", "software": "Multi-platform", "sw_slug": "civil-3d", "desc": "Stormwater design in civil CAD: pipe sizing, detention basins, rational method, and hydraulic modeling integration."},
    {"slug": "coordinate-reference-systems", "name": "Coordinate Reference Systems (CRS)", "software": "Multi-platform", "sw_slug": "civil-3d", "desc": "Geographic coordinate systems for civil engineering: UTM zones, state plane, datum transformations, and survey coordinates."},
    
    # Manufacturing/machining
    {"slug": "5-axis-machining", "name": "5-Axis CNC Machining", "software": "Multi-platform", "sw_slug": "siemens-nx", "desc": "5-axis simultaneous machining strategies: swarf cutting, multi-axis contouring, and collision avoidance in CAM."},
    {"slug": "post-processor-cam", "name": "Post Processors for CNC", "software": "Multi-platform", "sw_slug": "fusion-360", "desc": "CAM post processors: translating toolpath data into machine-specific G-code for CNC controllers."},
    {"slug": "fixture-design", "name": "Fixture & Jig Design", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Workholding fixture design principles in CAD: locating, clamping, supporting, and manufacturing accuracy."},
    {"slug": "injection-molding-design", "name": "Injection Molding Design Guidelines", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Designing plastic parts for injection molding: draft, wall thickness, ribs, bosses, gates, and sink marks."},
    {"slug": "casting-design", "name": "Casting Design for CAD", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Design for casting: draft angles, fillets, parting lines, core/cavity considerations, and shrinkage allowances."},
    {"slug": "weld-design-symbols", "name": "Weld Symbols & Joint Design", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "AWS A2.4 weld symbols in CAD drawings: joint types, groove geometry, weld sizing, and annotation standards."},

    # Collaboration & Data
    {"slug": "model-based-definition", "name": "Model-Based Definition (MBD)", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "MBD approach: embedding PMI (Product Manufacturing Information) in 3D models to replace traditional 2D drawings."},
    {"slug": "digital-twin-concept", "name": "Digital Twin in Engineering", "software": "Multi-platform", "sw_slug": "siemens-nx", "desc": "Digital twin technology: connecting CAD/BIM models to real-world sensor data for monitoring, simulation, and prediction."},
    {"slug": "generative-ai-cad", "name": "Generative AI in CAD", "software": "Multi-platform", "sw_slug": "fusion-360", "desc": "AI-assisted design in modern CAD: generative design, shape optimization, feature recognition, and automated drafting."},
    {"slug": "cloud-computing-cad", "name": "Cloud Computing for CAD/BIM", "software": "Multi-platform", "sw_slug": "onshape", "desc": "Cloud-native CAD platforms and cloud-compute rendering: benefits, limitations, and security considerations for engineering."},
    {"slug": "vr-ar-cad-review", "name": "VR/AR Design Review", "software": "Multi-platform", "sw_slug": "revit", "desc": "Virtual and augmented reality for CAD model review: immersive walkthroughs, on-site AR overlay, and collaborative VR sessions."},
    
    # More software-specific
    {"slug": "vault-autodesk", "name": "Autodesk Vault (PDM)", "software": "AutoCAD", "sw_slug": "autocad", "desc": "Autodesk Vault data management for AutoCAD, Inventor, and Revit: version control, lifecycle management, and BOM tracking."},
    {"slug": "3dexperience-platform", "name": "3DEXPERIENCE Platform", "software": "CATIA", "sw_slug": "catia", "desc": "Dassault's 3DEXPERIENCE cloud platform integrating CATIA, SOLIDWORKS, ENOVIA, SIMULIA for enterprise PLM."},
    {"slug": "windchill-ptc", "name": "Windchill PLM (PTC)", "software": "Creo Parametric", "sw_slug": "creo-parametric", "desc": "PTC Windchill product lifecycle management system integrated with Creo: change management, configuration control, and supply chain."},
    {"slug": "acc-bim-collaborate", "name": "Autodesk Construction Cloud (ACC)", "software": "Revit", "sw_slug": "revit", "desc": "ACC platform for BIM collaboration: cloud worksharing, model coordination, design review, and construction management."},
    {"slug": "enscape-realtime", "name": "Enscape Real-Time Rendering", "software": "Multi-platform", "sw_slug": "revit", "desc": "Enscape real-time visualization plugin for Revit, SketchUp, Rhino, and ArchiCAD: instant walkthroughs and VR export."},

    # DWG-specific workflows
    {"slug": "lisp-programming-cad", "name": "LISP Programming for CAD", "software": "Multi-platform", "sw_slug": "autocad", "desc": "AutoLISP/Visual LISP programming for CAD automation: syntax, functions, entity access, and dialog boxes."},
    {"slug": "net-api-cad", "name": ".NET API for CAD Development", "software": "Multi-platform", "sw_slug": "autocad", "desc": ".NET/C# plugin development for AutoCAD, GstarCAD, BricsCAD: database access, UI customization, and command creation."},
    {"slug": "vba-macro-cad", "name": "VBA Macros in CAD", "software": "Multi-platform", "sw_slug": "autocad", "desc": "Visual Basic for Applications (VBA) macro development for AutoCAD and other CAD platforms with ActiveX automation."},
    {"slug": "dynamo-visual-scripting", "name": "Dynamo Visual Scripting", "software": "Revit", "sw_slug": "revit", "desc": "Dynamo visual programming for Revit: node-based automation, parametric manipulation, and data-driven BIM workflows."},
    {"slug": "ilogic-automation", "name": "iLogic Design Automation", "software": "Inventor", "sw_slug": "inventor", "desc": "Inventor iLogic rules for design automation: conditional logic, parameter driving, and configure-to-order workflows."},

    # Additional workflow concepts
    {"slug": "version-control-cad", "name": "Version Control for CAD Files", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Version control approaches for CAD: PDM systems, Git-based solutions, naming conventions, and branching strategies."},
    {"slug": "template-library-management", "name": "Template & Library Management", "software": "Multi-platform", "sw_slug": "autocad", "desc": "Managing CAD template libraries: drawing templates, block libraries, family libraries, and content delivery strategies."},
    {"slug": "quality-assurance-cad", "name": "Quality Assurance in CAD", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "QA workflows for CAD deliverables: design reviews, model checking, drawing validation, and automated compliance tools."},
    {"slug": "interoperability-workflows", "name": "CAD Interoperability Workflows", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Cross-platform file exchange strategies: neutral formats, direct translators, and data validation for multi-tool environments."},

    # Software ecosystem concepts
    {"slug": "subscription-vs-perpetual", "name": "Subscription vs Perpetual Licensing", "software": "Multi-platform", "sw_slug": "autocad", "desc": "CAD software licensing models compared: subscription benefits, perpetual license advantages, and total cost of ownership analysis."},
    {"slug": "gpu-acceleration-cad", "name": "GPU Acceleration in CAD", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Graphics card utilization in CAD: certified GPUs, OpenGL vs DirectX, hardware rendering, and workstation recommendations."},
    {"slug": "workstation-hardware-cad", "name": "Workstation Hardware for CAD", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Hardware recommendations for CAD workstations: CPU selection, RAM sizing, GPU certification, and storage architecture."},
    {"slug": "cad-security-best-practices", "name": "CAD File Security & IP Protection", "software": "Multi-platform", "sw_slug": "autocad", "desc": "Protecting CAD intellectual property: file encryption, DRM, password protection, and secure file sharing for engineering data."},
    
    # Additional MCAD workflows
    {"slug": "multi-body-modeling", "name": "Multi-Body Part Modeling", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Multi-body design techniques: creating multiple solid bodies in one part file for complex components and weldments."},
    {"slug": "top-down-design", "name": "Top-Down Assembly Design", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Top-down design methodology in CAD: skeleton models, in-context editing, and layout-driven assembly workflows."},
    {"slug": "bottom-up-design", "name": "Bottom-Up Assembly Design", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Bottom-up assembly approach: designing individual parts first, then assembling with constraints/mates for modular products."},
    {"slug": "master-model-technique", "name": "Master Model Technique", "software": "Multi-platform", "sw_slug": "siemens-nx", "desc": "Master model methodology in NX and other MCAD: controlling downstream parts from a single reference geometry set."},
    {"slug": "kinematic-simulation", "name": "Kinematic Simulation in CAD", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "Assembly motion studies: kinematic chains, mechanism simulation, motion envelopes, and interference analysis over travel."},
    {"slug": "tolerance-stackup-analysis", "name": "Tolerance Stack-Up Analysis", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "1D and 3D tolerance stack-up analysis: worst-case, RSS, and Monte Carlo methods for assembly dimensional validation."},
    
    # Additional BIM/Arch concepts
    {"slug": "passive-house-design", "name": "Passive House Design in BIM", "software": "Multi-platform", "sw_slug": "revit", "desc": "BIM workflows for Passive House certification: thermal bridging analysis, PHPP integration, and envelope optimization."},
    {"slug": "energy-modeling-bim", "name": "Energy Modeling from BIM", "software": "Multi-platform", "sw_slug": "revit", "desc": "Using BIM models for energy simulation: gbXML export, thermal zones, HVAC modeling, and daylighting analysis."},
    {"slug": "acoustic-design-bim", "name": "Acoustic Design in BIM", "software": "Multi-platform", "sw_slug": "revit", "desc": "Acoustic performance modeling in BIM: room acoustics, sound insulation, and noise mapping integrated with building design."},
    {"slug": "fire-safety-bim", "name": "Fire Safety Design in BIM", "software": "Multi-platform", "sw_slug": "revit", "desc": "BIM for fire engineering: egress analysis, fire compartmentation, smoke control modeling, and code compliance verification."},
    {"slug": "prefabrication-bim", "name": "Prefabrication & Modular Design in BIM", "software": "Multi-platform", "sw_slug": "revit", "desc": "BIM for offsite construction: modular design, prefab panel detailing, logistics planning, and factory coordination."},
    {"slug": "facility-management-bim", "name": "Facility Management with BIM", "software": "Multi-platform", "sw_slug": "revit", "desc": "Using BIM models for facility operations: asset management, maintenance scheduling, space management, and renovation planning."},
    
    # Additional Civil concepts
    {"slug": "bridge-design-software", "name": "Bridge Design in CAD/BIM", "software": "Multi-platform", "sw_slug": "civil-3d", "desc": "Bridge design workflows: deck geometry, pier/abutment modeling, prestress layout, and structural analysis integration."},
    {"slug": "tunnel-design-bim", "name": "Tunnel Design in BIM", "software": "Multi-platform", "sw_slug": "civil-3d", "desc": "Tunnel BIM workflows: alignment-based modeling, lining design, geological integration, and TBM sequencing."},
    {"slug": "utility-network-design", "name": "Underground Utility Design", "software": "Multi-platform", "sw_slug": "civil-3d", "desc": "Utility network design in civil CAD: pipe sizing, manholes, trenchless methods, and utility conflict detection."},
    {"slug": "land-development-cad", "name": "Land Development & Subdivision", "software": "Multi-platform", "sw_slug": "civil-3d", "desc": "Subdivision design workflows: lot layout, road alignment, grading, utility routing, and municipal submission requirements."},
    {"slug": "construction-documentation", "name": "Construction Document Production", "software": "Multi-platform", "sw_slug": "revit", "desc": "CD production workflows: drawing set organization, cross-referencing, keynoting, and coordination between disciplines."},
    
    # Rendering & Viz specific
    {"slug": "pbr-materials", "name": "PBR Materials for CAD Visualization", "software": "Multi-platform", "sw_slug": "blender", "desc": "Physically-Based Rendering materials: roughness, metalness, normal maps, and material libraries for realistic CAD visualization."},
    {"slug": "hdri-lighting-cad", "name": "HDRI Lighting for CAD Rendering", "software": "Multi-platform", "sw_slug": "blender", "desc": "High Dynamic Range Image lighting for architectural and product visualization: studio setups, outdoor scenes, and color accuracy."},
    {"slug": "architectural-visualization", "name": "Architectural Visualization Workflow", "software": "Multi-platform", "sw_slug": "3dsmax", "desc": "End-to-end archviz workflow: model preparation, material assignment, lighting, rendering, and post-production."},
    {"slug": "product-visualization", "name": "Product Visualization & Photography", "software": "Multi-platform", "sw_slug": "blender", "desc": "Product rendering workflows: studio lighting, turntable animation, material accuracy, and marketing asset production."},
    
    # Simulation specific
    {"slug": "mesh-generation-fea", "name": "Mesh Generation for FEA", "software": "Multi-platform", "sw_slug": "ansys-mechanical", "desc": "FEA mesh generation: element types (tet/hex), mesh quality metrics, refinement strategies, and convergence studies."},
    {"slug": "contact-analysis-fea", "name": "Contact Analysis in FEA", "software": "Multi-platform", "sw_slug": "ansys-mechanical", "desc": "Contact modeling in structural FEA: contact types, friction, penetration tolerance, and solver convergence for assemblies."},
    {"slug": "fatigue-analysis", "name": "Fatigue Analysis in CAE", "software": "Multi-platform", "sw_slug": "ansys-mechanical", "desc": "Fatigue life prediction in CAE: S-N curves, strain-life approach, cycle counting, and critical plane methods."},
    {"slug": "thermal-analysis-cae", "name": "Thermal Analysis in CAE", "software": "Multi-platform", "sw_slug": "ansys-mechanical", "desc": "Thermal simulation: steady-state and transient heat transfer, convection, radiation, and thermal-structural coupling."},
    {"slug": "vibration-analysis", "name": "Vibration & Modal Analysis", "software": "Multi-platform", "sw_slug": "ansys-mechanical", "desc": "Modal and harmonic analysis: natural frequencies, mode shapes, forced response, and vibration isolation design."},
    {"slug": "crash-simulation", "name": "Crash & Impact Simulation", "software": "Multi-platform", "sw_slug": "abaqus", "desc": "Explicit dynamics for crash simulation: material failure, contact algorithms, airbag deployment, and occupant safety."},
    
    # Standards & Compliance
    {"slug": "iso-19650-bim", "name": "ISO 19650 BIM Information Management", "software": "Multi-platform", "sw_slug": "revit", "desc": "ISO 19650 framework for BIM information management: naming conventions, model production delivery tables, and CDE workflows."},
    {"slug": "bs-1192-bim-legacy", "name": "BS 1192 / PAS 1192 (Legacy BIM Standards)", "software": "Multi-platform", "sw_slug": "revit", "desc": "UK BIM standards history: BS 1192, PAS 1192 parts 2-5, and their transition to ISO 19650 international framework."},
    {"slug": "national-bim-standards", "name": "National BIM Standards & Mandates", "software": "Multi-platform", "sw_slug": "revit", "desc": "BIM mandates worldwide: UK Level 2, Singapore BIM Guide, Nordic openBIM requirements, and US GSA standards."},
]


def generate_body(c):
    name = c["name"]
    sw = c["software"]
    return f"""<p>{c['desc']} This concept is fundamental to modern engineering workflows and understanding it enables more efficient, higher-quality design output across projects of all scales.</p>
<p>In professional practice, {name} represents a critical competency that bridges theoretical knowledge with practical application. Whether working in {sw} or other platforms, the underlying principles remain consistent — making this knowledge transferable across your career.</p>
<p>Mastery of {name} typically distinguishes intermediate practitioners from advanced users. Organizations that invest in developing this capability across their teams report measurable improvements in design quality, reduced revision cycles, and better cross-disciplinary coordination.</p>"""


def generate_page(c):
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
    <title>{c['name']} | Gstarcademy</title>
    <meta name="description" content="{c['desc']}" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <link rel="canonical" href="{canonical}" />
    <meta property="og:image" content="https://gstarcademy.com/images/og-default.webp" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{c['name']}" />
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
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{c['name']}","description":"{c['desc']}","url":"{canonical}","datePublished":"{TODAY}","dateModified":"{TODAY}","inLanguage":"en","author":{{"@type":"Organization","name":"Gstarcademy Editorial Team","url":"https://gstarcademy.com/about"}},"publisher":{{"@type":"Organization","name":"Gstarcademy","url":"https://gstarcademy.com/"}}}}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"DefinedTerm","name":"{c['name']}","description":"{c['desc']}","url":"{canonical}","inDefinedTermSet":{{"@type":"DefinedTermSet","name":"CAD Knowledge Base","url":"https://gstarcademy.com/kb-terms"}}}}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://gstarcademy.com/"}},{{"@type":"ListItem","position":2,"name":"Knowledge Base","item":"https://gstarcademy.com/knowledge-base"}},{{"@type":"ListItem","position":3,"name":"Terms","item":"https://gstarcademy.com/kb-terms"}},{{"@type":"ListItem","position":4,"name":"{c['name']}","item":"{canonical}"}}]}}</script>
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
        <a href="../../kb-terms">Terms</a> /
        <span aria-current="page">{c['name']}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 28px;">
          <span class="chip pill-warn">Knowledge &middot; {c['software']}</span>
          <h1 style="margin-top: 12px;">{c['name']}</h1>
          <p class="hero-sub">{c['desc']}</p>
        </header>

        <div class="ink-byline" role="contentinfo">
          <span><strong>By</strong> Gstarcademy Editorial Team</span>
          <span><strong>Updated</strong> <time datetime="{TODAY}">{TODAY}</time></span>
          <span><a href="../../editorial-process">Editorial process</a></span>
        </div>

        <section class="kb-concept-section">
          <h2>Definition &amp; Overview</h2>
          {body}
        </section>

        <section class="kb-concept-section">
          <h2>Key Considerations</h2>
          <ul>
            <li>Understand the fundamental principles before diving into software-specific implementations</li>
            <li>Evaluate how this concept integrates with your existing workflows and team standards</li>
            <li>Consider scalability — approaches that work for small projects may not suit enterprise requirements</li>
            <li>Stay current with industry best practices as software capabilities evolve rapidly</li>
            <li>Document your implementation decisions for team knowledge sharing and onboarding</li>
          </ul>
        </section>

        <section class="kb-concept-section">
          <h2>Learn More</h2>
          <p>Explore related topics in our <a href="../../kb-terms">terminology index</a>, or find structured learning in our <a href="../learning-paths/">learning paths</a>. For software-specific guidance, visit the relevant <a href="../software/">software profiles</a>.</p>
        </section>

        <aside style="margin-top: 32px; padding: 20px 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 14px; display: flex; gap: 16px; align-items: flex-start; flex-wrap: wrap;">
          <div style="flex: 1; min-width: 200px;">
            <p style="font-size: 12px; font-weight: 600; margin: 0 0 4px;">Written by Gstarcademy Editorial Team</p>
            <p style="font-size: 11px; color: var(--ink-text-soft); margin: 0;"><a href="../../editorial-process" style="color: var(--accent);">Editorial guidelines</a></p>
          </div>
          <div style="text-align: right; min-width: 140px;">
            <time datetime="{TODAY}" style="font-size: 12px; font-weight: 600;">{TODAY}</time>
          </div>
        </aside>
      </article>
    </main>

    <footer class="footer site-footer">
      <div class="container site-footer-inner"><div class="site-footer-brand"><p class="site-footer-tagline">Gstarcademy</p></div></div>
      <div class="container site-footer-bottom"><p>&copy; <span id="footer-year"></span> Gstarcademy.</p></div>
    </footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    return html


def main():
    print(f"Generating {len(WORKFLOW_CONCEPTS)} workflow/general concept pages...")
    generated = 0
    for c in WORKFLOW_CONCEPTS:
        filepath = os.path.join(OUTPUT_DIR, f"{c['slug']}.html")
        if os.path.exists(filepath):
            continue
        html = generate_page(c)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        generated += 1
    print(f"Done! Generated {generated} pages")


if __name__ == '__main__':
    main()
