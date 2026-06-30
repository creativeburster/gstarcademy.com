#!/usr/bin/env python3
"""
Generate additional concept pages for underrepresented software families.
Each page follows the existing concept-detail template with full E-E-A-T signals.
"""

import os
from datetime import date

TODAY = date.today().isoformat()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'concepts')

# New concepts to generate — these don't already exist
NEW_CONCEPTS = [
    # AutoCAD (currently has very few dedicated concept pages)
    {"slug": "action-recorder-autocad", "name": "Action Recorder", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD's macro tool that records command sequences for repeatable automation without scripting knowledge.", "family": "dwg-cad",
     "body": """<p>Action Recorder captures a sequence of AutoCAD commands, inputs, and coordinate picks, then saves them as an Action Macro (.actm file). You can replay the macro to repeat the same sequence on different geometry — for example, applying a standard annotation set to dozens of drawing sheets, batch-inserting blocks at predefined offsets, or running a consistent cleanup routine (purge + audit + save) across a batch of files.</p>
<p>Unlike AutoLISP or .NET, Action Recorder requires zero programming knowledge. You press Record, perform your workflow normally, then Stop. AutoCAD captures the command names, option keywords, coordinate points, and input values. On playback, you can mark certain inputs as "request user input" — pausing the macro for the operator to pick a point or type a value — making macros semi-interactive.</p>
<p>Limitations include: no conditional logic (if/then), no loops, no error handling. For complex automation, AutoLISP or .NET remains necessary. Action Macros are stored per-user profile unless exported and shared. They also cannot call other macros recursively.</p>"""},
    {"slug": "viewport-configuration-autocad", "name": "Viewport Configuration", "software": "AutoCAD", "sw_slug": "autocad", "desc": "Manage model space tiled viewports and paper space floating viewports for multi-view drafting in AutoCAD.", "family": "dwg-cad",
     "body": """<p>AutoCAD viewports come in two flavors: tiled viewports (model space) and floating viewports (paper space / layouts). Tiled viewports split the model-space drawing area into multiple simultaneous views — plan + elevation + isometric — for reference while drafting. Floating viewports in paper space are rectangular "windows" into model space placed on a printable sheet at specific scales.</p>
<p>Each layout viewport has independent layer visibility (VP Freeze), scale lock, annotation scale, and visual style. This means one sheet can show the same model from multiple angles and at different scales without duplicating geometry. The MVIEW command creates viewports; VPCLIP clips them to irregular shapes.</p>
<p>Best practices: lock viewport scale immediately after setting it (prevents accidental zoom changes); use annotative objects so text/dimensions auto-scale per viewport; name viewport layer configurations for consistency across sheets. For large projects with 50+ sheets, Sheet Set Manager (SSM) automates viewport creation from named views.</p>"""},
    {"slug": "express-tools-autocad", "name": "Express Tools", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD Express Tools — a curated collection of productivity utilities for text, blocks, layers, dimensions, and layout management.", "family": "dwg-cad",
     "body": """<p>Express Tools is a collection of ~80 utilities bundled with full AutoCAD (not LT) that extend core functionality: TEXTFIT scales text to fit between points, TCASE changes text case, BURST explodes blocks while retaining attribute values, GATTE changes attribute text globally, LMAN saves/restores layer states, ALIASEDIT manages command aliases, and SUPERHATCH fills regions with images or blocks.</p>
<p>These tools originated as bonus packs in the late 1990s, were later integrated into the main installer, and are now a required component many firms depend on. They install automatically with full AutoCAD but must be loaded explicitly via EXPRESSTOOLS command if they appear missing. Vertical products (Architecture, MEP) include them by default.</p>
<p>Key categories: Block tools (BURST, GATTE, NCopy), Text tools (ARCTEXT, TEXTFIT, TCASE, TEXTMASK), Layer tools (LAYWALK, LAYMRG, LAYISO), Layout tools (ALIGNSPACE, VPSCALE), and Draw tools (SUPERHATCH, BREAKLINE). While some have been absorbed into core AutoCAD over the years (e.g., layer isolation), most remain Express-only.</p>"""},
    {"slug": "data-link-autocad", "name": "Data Link", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD Data Link connects spreadsheet data (Excel/CSV) bidirectionally to drawing tables, enabling live schedule updates.", "family": "dwg-cad",
     "body": """<p>Data Link creates a live connection between an AutoCAD table object and an external data source — typically an Excel spreadsheet (.xlsx) or CSV file. Changes in Excel automatically propagate to the drawing table on file open or manual refresh (DATALINKUPDATE). Optionally, edits made in AutoCAD can write back to Excel (bidirectional mode).</p>
<p>This workflow is critical for construction documentation where equipment schedules, door/window schedules, and material lists are maintained in spreadsheets by non-CAD staff (procurement, PM) but must appear on drawings. Without Data Link, the drafter manually re-types changes — a major error source on large projects.</p>
<p>Setup: DATALINK command defines the source file, range, and update direction. Then TABLE → From Data Link inserts it. Formatting (font, color, borders) can be controlled from either the Excel cell style or the AutoCAD table style — choose one authority to avoid conflicts. Network paths work but require all users to have read access. For cloud-hosted Excel (SharePoint/OneDrive), the local sync path must be used.</p>"""},
    {"slug": "purge-audit-recover-autocad", "name": "Purge, Audit & Recover", "software": "AutoCAD", "sw_slug": "autocad", "desc": "AutoCAD file maintenance commands that remove unused objects, fix database errors, and recover corrupted drawings.", "family": "dwg-cad",
     "body": """<p>Three commands form AutoCAD's file-health toolkit: PURGE removes unused named objects (layers, blocks, linetypes, dimension styles, materials) that bloat file size; AUDIT scans the drawing database for internal inconsistencies and optionally fixes them; RECOVER opens a damaged .dwg and repairs structural corruption that prevents normal opening.</p>
<p>PURGE should be run periodically (especially before transmitting drawings) — a file that accumulates 500 unused block definitions from copy-paste operations can be 10x larger than necessary. Use -PURGE with the All option in scripts for batch cleanup. PURGE does not delete in-use objects, so it's always safe.</p>
<p>AUDIT checks the object hierarchy, entity ownership chains, and dictionary references. Run it when you encounter unexplained crashes, phantom objects, or selection-set anomalies. RECOVER is the last resort — it bypasses the normal file-open code path and rebuilds the database from raw binary. RECOVERALL extends this to all xrefs. After recovery, always AUDIT + PURGE the result and verify critical geometry wasn't lost.</p>"""},

    # Revit (currently very few dedicated pages)
    {"slug": "worksets-revit", "name": "Worksets", "software": "Revit", "sw_slug": "revit", "desc": "Revit worksharing worksets enable multiple team members to edit different parts of a central BIM model simultaneously.", "family": "bim-arch",
     "body": """<p>Worksets are Revit's collaboration mechanism for multi-user environments. When worksharing is enabled, the model is divided into worksets — named subsets of elements (e.g., "Architecture," "Structure," "MEP," "Site") — and stored as a central model on a shared server. Each team member creates a local copy, takes ownership of elements by editing them, and synchronizes changes back to central.</p>
<p>Unlike layer-based visibility in CAD, worksets provide ownership control: when User A edits a wall, that element is checked out (borrowed) and other users can't modify it until A syncs. This prevents conflicting edits. Worksets also control visibility and loading — you can close worksets you don't need, reducing memory usage in large models.</p>
<p>Best practices: create worksets by discipline or building zone (not by element type); sync frequently (every 30-60 minutes) to minimize conflicts; avoid editing elements in worksets you don't own; use worksharing display modes to see who owns what; establish a "last-to-leave" protocol for daily model reconciliation. Revit Server or BIM 360/ACC extends this workflow across WANs.</p>"""},
    {"slug": "view-templates-revit", "name": "View Templates", "software": "Revit", "sw_slug": "revit", "desc": "Revit view templates standardize graphics settings, visibility, and display parameters across project views for consistent documentation.", "family": "bim-arch",
     "body": """<p>A View Template is a saved collection of view properties — scale, detail level, visibility/graphics overrides, view filters, discipline, phase, crop region settings, and graphic display options — that can be applied to any view in one click. This ensures all floor plans look identical across sheets (same line weights, same category visibility, same filter colors) without manually configuring each view.</p>
<p>Templates can be "assigned" (permanently linked — changes to template auto-propagate to all views) or "applied once" (snapshot — applies settings but view can drift independently). Assigned templates enforce firm standards and prevent individual users from ad-hoc overriding graphics. The VG Overrides dialog shows which properties are template-controlled (greyed out).</p>
<p>Typical template set includes: Architectural Plan, Structural Plan, MEP Plan, Reflected Ceiling Plan, Coordination Model (all categories visible), Rendering View (materials on, detail off), and Presentation (custom line styles). Creating view templates early in a project saves exponential time as the drawing set grows from 50 to 500 sheets.</p>"""},
    {"slug": "adaptive-components-revit", "name": "Adaptive Components", "software": "Revit", "sw_slug": "revit", "desc": "Revit adaptive components are flexible parametric families that conform to complex geometry through placement points, enabling curtain panels and freeform facades.", "family": "bim-arch",
     "body": """<p>Adaptive components are a special family type in Revit designed for complex, non-standard geometry that must conform to varying host conditions. Unlike regular families (which have fixed insertion points), adaptive families have multiple adaptive points that can be placed independently — the geometry stretches, rotates, and scales between them.</p>
<p>Primary use cases: panelized curtain wall systems (each panel adapts to the quadrilateral formed by mullion intersections), complex roof cladding (panels that follow doubly-curved surfaces), repeating elements on freeform geometry (like parametric facade fins that vary in angle along a spline), and site-responsive installations.</p>
<p>Inside the Adaptive Component Family Editor, you place adaptive points, build reference planes and lines between them, and sketch/extrude geometry relative to those references. Parameters can drive dimensions based on point-to-point distances. When placed in a project via Divide Surface or manual point placement, each instance adapts to its local context. They're computationally heavier than standard families — use them only where regular families can't achieve the required form variation.</p>"""},
    {"slug": "design-options-revit", "name": "Design Options", "software": "Revit", "sw_slug": "revit", "desc": "Revit Design Options allow multiple design alternatives to coexist in a single model for comparison and client presentation.", "family": "bim-arch",
     "body": """<p>Design Options let you create alternative versions of part of a model within a single Revit file. A Design Option Set contains two or more options (e.g., "Lobby Layout A" vs "Lobby Layout B"). Only one option per set is "Primary" (shown by default in views) — the others are secondary and only visible when explicitly selected or through option-specific views.</p>
<p>This is invaluable during schematic design when the client hasn't decided between configurations: different facade treatments, two possible stair locations, or alternative MEP routing strategies. Without Design Options, you'd need separate files or duplicate views — both error-prone and hard to coordinate.</p>
<p>Elements belong to either the main model (visible always) or a specific option. When a decision is made, you "Accept Primary" to merge the chosen option into the main model and delete the alternatives. Limitations: elements in different option sets cannot reference each other; phasing and Design Options don't interact well; large option sets can confuse less-experienced team members. Use sparingly for truly undecided elements, not as a general versioning system — for that, use Revit's Save As or cloud model versioning.</p>"""},
    {"slug": "mep-systems-revit", "name": "MEP Systems", "software": "Revit", "sw_slug": "revit", "desc": "Revit MEP systems model building services (HVAC, plumbing, electrical) with connected components that calculate flow, pressure, and load.", "family": "bim-arch",
     "body": """<p>Revit MEP (Mechanical, Electrical, Plumbing) models building services as connected "systems" — not just geometry, but functional networks. A duct system knows its total airflow, a pipe system tracks pressure drops, and an electrical circuit sums connected loads. This enables engineers to validate designs against code requirements directly within the BIM model.</p>
<p>System types include: Supply Air, Return Air, Exhaust (HVAC duct), Hot Water Supply, Cold Water Supply, Sanitary, Storm (piping), Power, Lighting, Fire Alarm, Data (electrical). Each system connector on a family (the connection points on equipment, fittings, terminals) must match system type for routing to succeed.</p>
<p>Workflow: place equipment (AHUs, panels, fixtures) → connect with duct/pipe/conduit routing tools → assign to systems → run calculations (duct sizing, pipe sizing, panel schedules, voltage drop). Revit's built-in calculations are basic — many firms export to specialized tools (Trane Trace, HAP, SKM) for detailed engineering but keep the spatial coordination in Revit. Clash detection (via Navisworks or built-in Interference Check) is the primary coordination deliverable between MEP and architectural/structural models.</p>"""},

    # SOLIDWORKS additional concepts
    {"slug": "weldments-solidworks", "name": "Weldments", "software": "SOLIDWORKS", "sw_slug": "solidworks", "desc": "SOLIDWORKS Weldments environment for designing structural frames, generating cut lists, and creating weld bead annotations.", "family": "mcad-pro",
     "body": """<p>The Weldments environment in SOLIDWORKS is a specialized workflow for structural frame design (steel sections, tubing, channel, angle). Instead of modeling individual solid bodies for each structural member, you sketch the frame skeleton as a 3D wireframe (lines, arcs), then apply structural member profiles (W-beams, rectangular tubes, C-channels) along those sketch segments.</p>
<p>SOLIDWORKS automatically handles mitering at intersections, trimming overlapping members, and generating a cut list — a table that groups identical members by profile, length, and quantity. This cut list drives fabrication: each unique item is a distinct weld cut, and the list can be exported to ERP or sent directly to a saw operator.</p>
<p>Additional weldment features: gussets (triangular reinforcement plates), end caps (close open tube ends), weld beads (visual and symbolic representation of welds for documentation), and trim/extend operations on members. The structural profiles are stored in library files — firms customize these with their preferred suppliers' actual section dimensions. Drawing views automatically link to the cut list for BOM-accurate shop drawings.</p>"""},
    {"slug": "surfacing-techniques-solidworks", "name": "Surface Modeling", "software": "SOLIDWORKS", "sw_slug": "solidworks", "desc": "SOLIDWORKS surface modeling techniques for complex organic shapes, consumer products, and Class-A aesthetic surfaces.", "family": "mcad-pro",
     "body": """<p>Surface modeling in SOLIDWORKS creates zero-thickness NURBS surfaces that can later be trimmed, knitted, and thickened into solids. This approach is essential when solid features (extrude, loft) can't achieve the required shape complexity — think automotive body panels, consumer electronics housings, or ergonomic grips where curvature continuity (G2/G3) matters.</p>
<p>Key surface tools: Lofted Surface (blend between profiles with guide curves), Boundary Surface (higher-quality version with tangency/curvature control at all edges), Filled Surface (patch holes in a surface quilt), Swept Surface (profile along a path), and Offset Surface. The workflow typically involves building a surface quilt from multiple patches, then using Knit Surface + Thicken to convert to a solid body.</p>
<p>Quality analysis tools (Zebra stripes, Curvature combs, Deviation analysis) are critical for evaluating surface quality. G0 = positional continuity (touching), G1 = tangent (no crease), G2 = curvature (smooth reflections), G3 = rate-of-change (automotive A-Class). SOLIDWORKS excels at G2; for true G3 (Class-A), shops often use Rhino or CATIA ICEM Surf, then import the surface back for solid conversion.</p>"""},
    {"slug": "routing-solidworks", "name": "Routing (Piping, Tubing, Electrical)", "software": "SOLIDWORKS", "sw_slug": "solidworks", "desc": "SOLIDWORKS Routing add-in for 3D piping, tubing, wiring, and cable harness design within assembly context.", "family": "mcad-pro",
     "body": """<p>SOLIDWORKS Routing is a Premium-tier add-in that enables 3D design of piping systems, tubing runs, electrical cable harnesses, and conduit within assemblies. Routes are modeled as 3D sketches that follow connection points defined in component families (flanges, fittings, connectors). The system automatically inserts appropriate fittings (elbows, tees, reducers) based on route geometry and design rules.</p>
<p>The workflow: define connection points on equipment → start a route between two or more connection points → the route auto-generates with specified bend radii, minimum straight lengths, and fitting selections from a routing library. You can drag route segments to reroute around obstacles. The BOM auto-populates with fittings, pipe/tube lengths (including cut allowances), and cable specifications.</p>
<p>For electrical routing: harness design starts with a from-to list (which pin connects to which pin), then physical routing determines cable paths, bundle diameters, and connector sequences. The flattened harness drawing (a 2D representation of the 3D bundle) is the primary manufacturing deliverable — assembly technicians lay cables on a form board matching the flat pattern. Routing integrates with SOLIDWORKS Electrical for schematic-to-3D design synchronization.</p>"""},

    # Fusion 360 additional concepts
    {"slug": "mesh-modeling-fusion", "name": "Mesh Modeling (Mesh Environment)", "software": "Fusion 360", "sw_slug": "fusion-360", "desc": "Fusion 360's mesh workspace for editing triangulated meshes from 3D scans, converting to BRep, and preparing for reverse engineering.", "family": "mcad-pro",
     "body": """<p>Fusion 360's Mesh workspace handles triangulated mesh data (STL, OBJ, 3MF) that comes from 3D scanning, photogrammetry, or downloads from repositories like Thingiverse/GrabCAD. Unlike parametric BRep bodies, meshes are tessellated approximations — useful for organic shapes but difficult to edit with traditional CAD features.</p>
<p>Key capabilities: mesh repair (fill holes, remove self-intersections, smooth spikes), mesh reduction (reduce triangle count while preserving shape), mesh sectioning (cut planes to extract 2D profiles for re-modeling), and direct mesh boolean operations. The Convert Mesh to BRep command attempts to create a solid body from a watertight mesh — enabling standard Fusion operations on imported scan data.</p>
<p>Workflow for reverse engineering: import scan mesh → clean and repair → use mesh section planes to extract key profiles → sketch over profiles (Fit Curves to Section) → build parametric features following scan geometry → compare deviation between new BRep model and original mesh. This hybrid approach preserves design intent (parametric features) while matching the physical object's as-built geometry.</p>"""},
    {"slug": "simulation-fusion", "name": "Simulation (FEA & Thermal)", "software": "Fusion 360", "sw_slug": "fusion-360", "desc": "Fusion 360's integrated simulation environment for static stress, thermal, modal, and buckling analysis without leaving the design workspace.", "family": "mcad-pro",
     "body": """<p>Fusion 360's Simulation workspace provides cloud-computed Finite Element Analysis directly integrated with the design environment. Study types include: Static Stress (linear), Modal Frequencies (natural vibrations), Thermal (steady-state heat transfer), Thermal Stress (combined), Buckling (critical load factors), Nonlinear Static (large deformation, contact), and Event Simulation (drop test, impact).</p>
<p>Workflow: define materials (from extensive library) → apply constraints (fixed, pin, frictionless, prescribed displacement) → apply loads (force, pressure, moment, bearing, gravity, thermal) → mesh (auto or manual refinement) → solve (cloud compute) → interpret results (von Mises stress, displacement, factor of safety). The cloud solver eliminates local hardware limitations — complex studies that would take hours locally can run on powerful cloud instances.</p>
<p>Design validation approach: run simulation on your initial design → identify high-stress regions → modify geometry → re-run to verify improvement. Shape Optimization (topology/generative) goes further — you define keep/remove regions, loads, and constraints, then the solver generates an organic geometry that minimizes mass while meeting stress requirements. This result can be refined and manufactured via additive methods or used as a guide for traditional design.</p>"""},
    {"slug": "electronics-fusion", "name": "Electronics Design (PCB)", "software": "Fusion 360", "sw_slug": "fusion-360", "desc": "Fusion 360's integrated electronics design environment for schematic capture, PCB layout, and 3D board integration within mechanical assemblies.", "family": "mcad-pro",
     "body": """<p>Fusion 360 Electronics (formerly EAGLE integration) provides schematic capture and PCB layout directly within the Fusion environment, enabling seamless mechanical-electronic co-design. You design the circuit schematic, lay out the PCB, and the 3D board shape automatically appears in your mechanical assembly — including component heights for enclosure clearance checking.</p>
<p>The workflow bridges the traditional gap between ECAD and MCAD: mechanical engineers define the board outline and component keep-out zones in the 3D assembly → electronics engineers route traces within those constraints → changes sync bidirectionally. No more exporting STEP files of board outlines back and forth between separate tools.</p>
<p>Features include: multi-sheet schematic with hierarchical design, auto-router for PCB traces, design rule checking (DRC), extensive component libraries (with 3D models), copper pour, differential pair routing, and Gerber/ODB++ output for manufacturing. For complex high-speed designs, dedicated ECAD tools (Altium, KiCad, OrCAD) still dominate — but for IoT devices, consumer electronics prototypes, and maker projects, Fusion 360 Electronics eliminates tool-switching overhead.</p>"""},

    # Civil 3D additional concepts
    {"slug": "quantity-takeoff-civil-3d", "name": "Quantity Takeoff", "software": "Civil 3D", "sw_slug": "civil-3d", "desc": "Civil 3D quantity takeoff tools for earthwork volumes, material quantities, and cost estimation from corridor and grading models.", "family": "civil-infra",
     "body": """<p>Quantity Takeoff in Civil 3D computes material volumes and areas from corridor models, surfaces, and grading objects. The primary methods are: surface-to-surface volume comparison (cut/fill between existing ground and proposed design), corridor material volumes (computed from cross-section areas × station spacing using average-end-area or prismoidal methods), and grading volume tools (for pads and basins).</p>
<p>For corridor-based earthwork: Civil 3D generates sample lines at user-defined intervals along the alignment, extracts cross-sections showing existing ground and design surfaces, then calculates cut and fill volumes between stations. The Mass Haul diagram visualizes where material is removed (cut zones) and where it's placed (fill zones), optimizing haul distances and identifying borrow/waste requirements.</p>
<p>Pay item assignment connects quantities to cost codes: each material region (subgrade, base course, asphalt, topsoil) is tagged with a pay item number and unit rate. The Quantity Takeoff Report aggregates all pay items across the corridor for engineer's estimates and bid tabulations. For DOT projects, these reports directly feed into the contract documents specifying payment quantities for each work item.</p>"""},
    {"slug": "survey-database-civil-3d", "name": "Survey Database", "software": "Civil 3D", "sw_slug": "civil-3d", "desc": "Civil 3D Survey Database for importing, managing, and processing field survey data including points, figures, and networks.", "family": "civil-infra",
     "body": """<p>The Civil 3D Survey Database is a structured repository for field survey data — points (with coordinates, elevations, descriptions), figures (connected linework representing features like road edges, buildings, fences), observation data (angles, distances from total stations), and GPS observations. It separates raw field data from the design drawing, preventing accidental edits to survey control.</p>
<p>Import workflows support multiple formats: raw data collectors (Trimble DC, Leica GSI), point files (PNEZD CSV), LandXML, and direct database links to survey processing software. Figure prefix libraries auto-create linework from coded descriptions — surveyor enters "EP" (edge of pavement) as a point code, and Civil 3D automatically connects EP points into a polyline figure.</p>
<p>Survey network analysis performs least-squares adjustment on traverse observations, computing adjusted coordinates and reporting error ellipses. This validates field measurements before using them for design surfaces. The workflow: import raw observations → adjust network → generate adjusted points → create survey figures → build existing ground surface from points/figures → begin design on top of validated survey data.</p>"""},

    # BricsCAD additional
    {"slug": "ai-assisted-modeling-bricscad", "name": "AI-Assisted Modeling", "software": "BricsCAD", "sw_slug": "bricscad", "desc": "BricsCAD's AI-powered features including Blockify, Propagate, and intelligent copy that automate repetitive modeling tasks.", "family": "dwg-cad",
     "body": """<p>BricsCAD integrates machine-learning and pattern-recognition algorithms directly into the modeling workflow. Key AI features: BLOCKIFY scans a drawing and identifies repeated geometry that should be blocks — it groups identical patterns, creates block definitions, and replaces instances automatically. This can convert a legacy drawing with 500 copy-pasted chair geometries into 500 instances of a single chair block in seconds.</p>
<p>PROPAGATE watches your edits and applies similar changes throughout the model. If you modify one door opening (add a lintel, change the swing direction), BricsCAD identifies all similar door openings and offers to propagate the same modification — maintaining consistency without manual find-and-edit across a large floor plan.</p>
<p>In BricsCAD BIM, AI extends to classification: the BIMIFY command analyzes solid geometry and classifies elements as walls, slabs, columns, roofs, etc. based on shape, position, and relationship heuristics. A simple extruded box at the base of a building might be classified as a foundation wall; a thin horizontal slab at storey height becomes a floor. This accelerates the conversion of non-BIM 3D models into IFC-ready BIM models without manual element-by-element classification.</p>"""},

    # Blender additional
    {"slug": "geometry-nodes-blender", "name": "Geometry Nodes", "software": "Blender", "sw_slug": "blender", "desc": "Blender's node-based procedural geometry system for parametric modeling, scattering, instancing, and algorithmic design.", "family": "viz-render",
     "body": """<p>Geometry Nodes is Blender's procedural geometry system, introduced in version 2.92 and rapidly expanded since. It provides a node-based visual programming interface for creating, modifying, and instancing geometry procedurally — similar in concept to Houdini's node graph or Grasshopper in Rhino, but integrated into Blender's modifier stack.</p>
<p>Core capabilities: distribute points on surfaces (for vegetation scattering, crowd population, particle-like effects), instance geometry at points (place trees, rocks, buildings procedurally), mesh operations (subdivide, extrude, merge by distance), curve operations (resample, trim, fillet), attribute manipulation (store/read custom data per vertex/face/instance), and math/logic for conditional behaviors.</p>
<p>For CAD-adjacent workflows, Geometry Nodes enables: parametric architectural facades (panels that vary based on position), procedural urban layouts (roads + building footprints from rules), structural node visualization (generating beams between connection points), and landscape design (terrain-aware vegetation placement). Unlike traditional Blender modeling (manual mesh editing), Geometry Nodes are non-destructive and parameter-driven — changing one input value regenerates the entire result, making exploration rapid.</p>"""},
    {"slug": "blenderbim-addon", "name": "BlenderBIM Add-on", "software": "Blender", "sw_slug": "blender", "desc": "The BlenderBIM Add-on enables full IFC/openBIM authoring, viewing, and editing in Blender as a free alternative to proprietary BIM tools.", "family": "viz-render",
     "body": """<p>BlenderBIM (part of the IfcOpenShell project) transforms Blender into a fully-featured openBIM authoring tool capable of reading, writing, and editing IFC (Industry Foundation Classes) files directly. Unlike BIM tools that export to IFC as a secondary format, BlenderBIM works natively in IFC — every element you create has proper IFC classification, property sets, and relationships from the start.</p>
<p>Capabilities: author walls, slabs, columns, beams, doors, windows with proper IFC semantics; assign property sets (Pset_WallCommon, etc.); define spatial structure (IfcSite → IfcBuilding → IfcBuildingStorey); create schedules and quantity takeoffs from IFC properties; perform 4D/5D simulation (construction sequencing with time); and generate 2D documentation from 3D IFC models.</p>
<p>This is significant because it provides a completely free, open-source BIM workflow — no Revit or ArchiCAD license required. The trade-off: Blender's UI wasn't designed for BIM, so the workflow has a steeper learning curve for architectural professionals; fewer pre-built parametric families compared to commercial tools; and inter-firm collaboration typically still expects Revit RVT files. For openBIM-mandated projects (some Scandinavian countries, public sector), BlenderBIM is production-viable.</p>"""},

    # Additional GstarCAD concepts
    {"slug": "collaborative-design-gstarcad", "name": "Collaborative Design", "software": "GstarCAD", "sw_slug": "gstarcad", "desc": "GstarCAD's multi-user collaboration features including cloud sharing, markup tools, and DWG version management for team drafting.", "family": "dwg-cad",
     "body": """<p>GstarCAD provides several collaboration mechanisms for teams working on shared DWG projects: Xref-based workflows (attach drawings as external references for coordination without concurrent editing conflicts), DWG Compare (visual diff between drawing versions highlighting additions, deletions, and modifications), and markup/review tools for commenting without modifying the drawing itself.</p>
<p>GstarCAD 365 (the cloud-connected tier) adds online storage, browser-based viewing, and mobile access through DWG FastView — enabling field teams to view, measure, and annotate drawings on tablets without desktop CAD. Comments and markups sync back to the desktop users for resolution.</p>
<p>For larger teams, GstarCAD supports network licensing with floating seats (one license serves multiple users on rotation) and includes Sheet Set Manager for coordinating multi-sheet projects across drafters. The eTransmit function packages drawings with all dependencies (xrefs, fonts, plot styles) for reliable file transfer between offices. Unlike Revit's central model approach, GstarCAD collaboration is file-based — requiring human coordination protocols (file naming conventions, folder locking) for concurrent work on the same drawing.</p>"""},
    {"slug": "api-ecosystem-gstarcad", "name": "API & Plugin Ecosystem", "software": "GstarCAD", "sw_slug": "gstarcad", "desc": "GstarCAD's developer APIs including GRX (AutoCAD ARX-compatible), .NET, and LISP for custom tool and vertical application development.", "family": "dwg-cad",
     "body": """<p>GstarCAD provides three primary development APIs: GRX (C++ SDK compatible with AutoCAD's ObjectARX/ARX — allows direct porting of many ARX plugins), .NET API (C#/VB.NET access to the drawing database, UI customization, and command registration), and AutoLISP/Visual LISP (direct compatibility with AutoCAD LISP routines including DCL dialogs).</p>
<p>The GRX SDK is the differentiating factor — most alternative CAD platforms only offer .NET or proprietary APIs, meaning AutoCAD C++ plugins need complete rewrites. GstarCAD's GRX maintains similar class hierarchies (AcDb → GcDb, AcRx → GcRx) enabling mechanical porting of ObjectARX applications. This dramatically reduces the cost for vertical developers (electrical, structural, civil) to support GstarCAD alongside AutoCAD.</p>
<p>The plugin ecosystem includes vertical solutions for architecture (floor plans, elevations, BOM generation), mechanical design (parametric standard parts, tolerance analysis), civil engineering (road profiles, pipe networks), and surveying (point import, traverse calculation). Third-party developers publish through GstarCAD's extension center. For custom firm-specific automation, .NET with Visual Studio remains the most productive path — full access to the drawing database, ribbon UI, palettes, and Windows Forms/WPF for custom dialogs.</p>"""},

    # Onshape additional
    {"slug": "featurescript-onshape", "name": "FeatureScript", "software": "Onshape", "sw_slug": "onshape", "desc": "Onshape's open parametric modeling language that lets users create custom features, extending the CAD system with shareable reusable operations.", "family": "mcad-pro",
     "body": """<p>FeatureScript is Onshape's open-source programming language for defining custom parametric features. Unlike plugins that bolt onto a CAD system externally, FeatureScript features run inside Onshape's geometry kernel — they behave exactly like native features (extrude, fillet, etc.) with full parametric history, rollback, and update behavior. Every built-in Onshape feature is itself written in FeatureScript.</p>
<p>Use cases: industry-specific features (create a "Dovetail Joint" feature that generates the interlocking geometry from width/angle/depth parameters), design-rule-encoded features (a "Sheet Metal Bend" that automatically applies your firm's K-factor table), and workflow accelerators (a "Mounting Boss Pattern" that generates the boss array + holes + counterbores for a PCB mounting arrangement in one operation).</p>
<p>FeatureScript is shared through Onshape's document system — publish a custom feature and any Onshape user can add it to their toolbar. This creates a community-driven feature library (Onshape Feature Store) where engineers contribute and reuse specialized operations. The language includes access to topology queries, boolean operations, sketch geometry construction, and parametric dimension declaration. For engineers who also code, it provides unprecedented control over CAD behavior without reverse-engineering a closed API.</p>"""},

    # Additional cross-platform concepts
    {"slug": "step-file-format", "name": "STEP File Format (AP203/AP214)", "software": "Multi-platform", "sw_slug": "solidworks", "desc": "The STEP (ISO 10303) neutral file format for exchanging 3D CAD data between different systems while preserving geometry and product structure.", "family": "data-exchange",
     "body": """<p>STEP (Standard for the Exchange of Product model data, ISO 10303) is the most widely used neutral 3D CAD exchange format. Unlike proprietary formats (SLDPRT, CATPART, PRT), STEP files can be opened by virtually any professional CAD system. The two most common Application Protocols are AP203 (configuration-controlled 3D design) and AP214 (automotive design with colors and layers).</p>
<p>What STEP preserves: exact B-rep geometry (NURBS surfaces, trimming curves), solid body topology, assembly structure (component hierarchy), basic color/material assignments (AP214), and geometric tolerances (AP242). What it loses: parametric feature history (sketch constraints, extrude depths), in-context assembly references, proprietary features (sheet metal bend tables, routing), and simulation setups.</p>
<p>Best practices for exchange: export as AP214 (includes visual properties) or AP242 (adds PMI/GD&T); verify the export by reimporting into your own system and checking geometry integrity; for assemblies, maintain the component structure rather than exporting as a single solid; and include a PDF drawing as a visual reference since STEP has no guaranteed visual fidelity across importers. The receiving system should import STEP bodies as "dumb solids" and remodel critical features parametrically if future edits are needed.</p>"""},
    {"slug": "ifc-standard", "name": "IFC (Industry Foundation Classes)", "software": "Multi-platform", "sw_slug": "revit", "desc": "The IFC open standard (ISO 16739) for BIM data exchange, enabling interoperability between different building design platforms.", "family": "data-exchange",
     "body": """<p>IFC (Industry Foundation Classes, ISO 16739) is the open international standard for describing building and construction data. Unlike DWG or RVT, IFC is vendor-neutral — any BIM software can import and export IFC files for cross-platform coordination. The standard defines entity types (IfcWall, IfcSlab, IfcDoor, IfcSpace), property sets (Pset_WallCommon, Pset_DoorCommon), and relationships (containment, connection, decomposition).</p>
<p>IFC versions: IFC2x3 is still the most widely deployed (supported by all major BIM tools); IFC4 adds improved geometry kernels, property templates, and infrastructure entities; IFC4.3 extends to rail, road, bridge, and tunnel infrastructure. The buildingSMART alliance maintains the standard and certification program (IFC export/import conformance testing).</p>
<p>Practical considerations: IFC export quality varies wildly between authoring tools — some produce clean, well-classified models while others export geometrically correct but semantically poor data. Use Model View Definitions (MVDs) to specify which data should be included (Coordination View for clash detection, Design Transfer View for full model exchange). IFC files can be validated using tools like Solibri, BIMcollab, or the open-source IfcOpenShell library. For many public-sector projects globally, IFC delivery is now contractually required.</p>"""},
]


def generate_concept_page(concept):
    c = concept
    slug = c["slug"]
    canonical = f"https://gstarcademy.com/kb/concepts/{slug}"
    
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
          {c['body']}
        </section>

        <section class="kb-concept-section">
          <h2>Why It Matters</h2>
          <p>Understanding {c['name']} is essential for professionals working with {c['software']} because it directly impacts productivity, design quality, and team collaboration. Mastering this concept enables more efficient use of the software's capabilities and reduces common errors in professional workflows.</p>
        </section>

        <section class="kb-concept-section">
          <h2>Related Concepts</h2>
          <p>Explore more {c['software']} topics in our <a href="../software/{c['sw_slug']}">{c['software']} knowledge base</a>, or browse the full <a href="../../kb-terms">terminology index</a>.</p>
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
    print(f"Generating {len(NEW_CONCEPTS)} new concept pages...")
    generated = 0
    for c in NEW_CONCEPTS:
        filepath = os.path.join(OUTPUT_DIR, f"{c['slug']}.html")
        if os.path.exists(filepath):
            print(f"  Skipping {c['slug']} (already exists)")
            continue
        html = generate_concept_page(c)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        generated += 1
    print(f"Done! Generated {generated} new concept pages")


if __name__ == '__main__':
    main()
