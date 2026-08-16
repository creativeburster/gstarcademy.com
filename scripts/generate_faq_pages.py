#!/usr/bin/env python3
"""
Generate comprehensive, in-depth FAQ pages for common CAD questions.
Each page provides step-by-step instructions, command syntax, troubleshooting tables,
multi-software cross references, and best practice checklists to eliminate thin content.
"""

import os
from datetime import date

TODAY = date.today().isoformat()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'faq')
os.makedirs(OUTPUT_DIR, exist_ok=True)

FAQS = [
    # AutoCAD FAQs
    {
        "slug": "how-to-scale-in-autocad",
        "title": "How to Scale Objects in AutoCAD: Reference, Viewport & Base Point Guide",
        "desc": "Master scaling in AutoCAD with step-by-step methods: standard factor scaling, reference length alignment, viewport scale setup in paper space, and annotative dimension control.",
        "software": "AutoCAD",
        "sw_slug": "autocad",
        "quick_answer": "To scale an object uniformly in AutoCAD: enter SCALE (shortcut SC), select target entities, click a base point, and enter a numeric factor (e.g. 2 for 200%, 0.5 for 50%). For precise fitting without manual math, use the Reference (R) sub-option.",
        "steps": [
            {
                "title": "Method 1: Factor-Based Scaling (Standard SC Command)",
                "content": "Type <code>SC</code> or <code>SCALE</code> in the command line and hit Enter. Select the objects you wish to resize and press Enter. Click to specify the base point—this point remains stationary while surrounding geometry expands or contracts. Type your scaling factor (e.g., <code>0.25</code> to reduce to one-quarter size, or <code>4</code> to quadruple size) and confirm with Enter."
            },
            {
                "title": "Method 2: Reference Scaling (Match Exact Target Dimensions)",
                "content": "When you need an unknown length to match an exact target measurement (e.g., an imported raster floor plan or DWG block), start the <code>SCALE</code> command and pick your base point. Type <code>R</code> (Reference) and Enter. Pick the two endpoints of the existing segment, then enter the desired true length (or click a second point in your drawing). AutoCAD computes the exact ratio instantly without rounding errors."
            },
            {
                "title": "Method 3: Viewport & Paper Space Scale Setup",
                "content": "Never scale model geometry just to fit a title block. Keep all 1:1 true-scale geometry in Model Space. Switch to your Layout tab (Paper Space), select or create a Viewport (<code>MVIEW</code>), and set the viewport scale from the status bar dropdown (e.g., <code>1:50</code>, <code>1:100</code>, or <code>1/4\" = 1'-0\"</code>). Lock the viewport display immediately to prevent accidental zoom changes."
            }
        ],
        "troubleshooting": [
            ("Dimensions show incorrect values after scaling", "Check whether your dimension style is Annotative. If annotative scaling is disabled, dimensions reflect resized geometry directly. Turn on Annotative property in DIMSTYLE so text height adjusts relative to paper space."),
            ("Geometry distorts along only one axis (X or Y)", "The standard SCALE command is strictly isotropic (uniform XYZ). Non-uniform scaling requires creating a Block (<code>B</code>) and inserting it with separate X, Y, Z scale multipliers in the Properties palette (<code>Ctrl+1</code>)."),
            ("Hatch patterns disappear or become solid", "Scaling up or down affects hatch density. Adjust the <code>HPSCALE</code> variable or select the hatch and modify 'Scale' in the Hatch Editor ribbon to prevent dense solid fills or sparse empty voids.")
        ],
        "multi_cad_tips": "In GstarCAD and ZWCAD, the <code>SCALE</code> command, Reference option (<code>R</code>), and Viewport scaling operate identically with full DWG command alias compatibility. In SOLIDWORKS, sketch geometry scaling is handled via 'Scale Entities' in the Sketch toolbar or parametric equations.",
        "best_practices": [
            "Always keep raw architectural and mechanical drawings drawn at 1:1 scale in Model Space.",
            "Utilize the Reference (R) option whenever scaling scanned raster underlays or PDF imports.",
            "Lock paper space viewports immediately after setting standard scale factors.",
            "Use Annotative text and dimension styles to prevent text distortion across multiple viewport scales."
        ],
        "related_concepts": [
            ("annotative-objects", "Annotative Scaling & Text Management"),
            ("dynamic-blocks-autocad", "Dynamic Blocks & Scaling Actions"),
            ("paper-space-autocad", "Paper Space Layouts & Viewports"),
            ("dwg-file-format", "DWG Coordinate & Unit Systems")
        ]
    },
    {
        "slug": "how-to-print-autocad",
        "title": "How to Print and Plot in AutoCAD: CTB, STB, PDF Output & Batch Publishing",
        "desc": "Complete guide to AutoCAD plotting: page setup configurations, CTB vs STB plot style tables, vector PDF export, and batch plotting multiple drawing sheets with Sheet Set Manager.",
        "software": "AutoCAD",
        "sw_slug": "autocad",
        "quick_answer": "To plot a clean drawing to PDF in AutoCAD: Press Ctrl+P (or type PLOT), select 'AutoCAD PDF (General Documentation).pc3', choose your paper size (e.g., ISO A1 or ANSI D), set Plot Area to 'Layout' or 'Window', select your monochrome.ctb plot style table, and verify via Preview before printing.",
        "steps": [
            {
                "title": "Step 1: Page Setup Configuration",
                "content": "Right-click your layout tab and open the <b>Page Setup Manager</b>. Select Modify to lock in standard plotter presets. Choose <code>AutoCAD PDF (General Documentation).pc3</code> or your network plotter. Set the Paper Size (e.g., ARCH D 24x36 in or ISO A1 594x841 mm). Set Plot Area to <i>Layout</i> for 1:1 paper space sheets, and ensure Plot Scale is fixed at <code>1:1</code> (1 mm = 1 unit or 1 inch = 1 unit)."
            },
            {
                "title": "Step 2: Assigning and Managing Plot Styles (CTB vs STB)",
                "content": "In the top right of the Plot dialog, select your Plot Style Table. For color-dependent plotting (<b>CTB</b>), assign line weights and screening by AutoCAD color index (e.g., Color 1 Red = 0.18mm, Color 7 White = 0.50mm, monochrome.ctb for solid black lines). For named plot styles (<b>STB</b>), styles are assigned directly to layers or objects regardless of display color."
            },
            {
                "title": "Step 3: Generating High-Fidelity Searchable PDFs",
                "content": "Click <b>PDF Options</b> in the Plot dialog. Ensure 'Capture fonts used in the drawing' and 'Include layer information' are enabled. This ensures that TrueType text remains searchable and selectable in Adobe Acrobat and Bluebeam Revu, and allows recipients to toggle CAD layers on and off directly in the PDF."
            },
            {
                "title": "Step 4: Batch Plotting Multi-Sheet Sets (PUBLISH Command)",
                "content": "To export an entire drawing set (20+ sheets) at once, enter <code>PUBLISH</code>. Load all target DWG files and layout tabs, select 'Publish to: PDF', apply Page Setup overrides to ensure consistent plotting parameters, and click Publish. Alternatively, manage project-wide multi-sheet submissions through the <b>Sheet Set Manager</b> (<code>SSM</code>)."
            }
        ],
        "troubleshooting": [
            ("Lineweights appear too thick or muddy in print", "Check the 'Plot object lineweights' and 'Plot with plot styles' checkboxes in the Plot dialog. Ensure your viewport lineweight scale is not compounding object lineweights. Verify that CTB line weight assignments match title block standards."),
            ("PDF text is converted to graphical outlines and is not searchable", "AutoCAD SHX fonts cannot be embedded as live vector text in PDFs and are turned into geometry. Switch annotations to standard TrueType fonts (such as Arial, Inter, or Roboto), or enable 'Convert text to geometry' settings wisely."),
            ("Missing custom CTB plot style files when opening external files", "Place shared <code>.ctb</code> files in the AutoCAD Printer Support File Path (Options > Files > Printer Support File Path > Plot Style Table Search Path), or type <code>STYLESMANAGER</code> to open the directory directly.")
        ],
        "multi_cad_tips": "GstarCAD and ZWCAD fully support all AutoCAD CTB and STB files, PC3 configurations, and the PUBLISH batch plotting engine without any format translation. GstarCAD includes an ultra-fast multi-core PDF printer engine that accelerates large sheet sets.",
        "best_practices": [
            "Standardize Page Setups in your seed drawing templates (.DWT) so all new sheets inherit correct plot configurations.",
            "Always inspect drawing outputs in the full-screen 'Preview' window before executing the physical plot.",
            "Use eTransmit when sending drawings to external partners so custom CTB plot styles and font files travel together.",
            "Set PDF vector resolution to at least 600 DPI (1200 DPI for dense schematics) to guarantee razor-sharp lines."
        ],
        "related_concepts": [
            ("paper-space-autocad", "Paper Space Layout Design"),
            ("layers-gstarcad", "Layer Color & Lineweight Standards"),
            ("dwg-file-format", "DWG Sheet Set Packaging & eTransmit"),
            ("construction-documentation", "Construction Document Standards")
        ]
    },
    {
        "slug": "how-to-create-blocks-autocad",
        "title": "How to Create and Manage Blocks in AutoCAD: Attributes, Dynamic Actions & Libraries",
        "desc": "Step-by-step masterclass on AutoCAD blocks: internal block creation (B), external library export (WBLOCK), parametric dynamic blocks, and automated attribute extraction.",
        "software": "AutoCAD",
        "sw_slug": "autocad",
        "quick_answer": "To create a reusable block in AutoCAD: draw your component on Layer 0, type BLOCK (shortcut B), enter a descriptive name, select a logical insertion Base Point (e.g., midpoint or center), select the geometry, and choose 'Convert to Block'. Use WBLOCK to save the block as a standalone external DWG.",
        "steps": [
            {
                "title": "Step 1: Drawing Geometry on Layer 0 for Dynamic Inheritance",
                "content": "Best practice is to draw all block sub-entities on <b>Layer 0</b> with Color, Linetype, and Lineweight set to <code>ByLayer</code>. When inserted into a project drawing, the block will dynamically inherit the layer color, linetype, and visibility of whichever target layer you place it on."
            },
            {
                "title": "Step 2: Internal Block Definition (B Command)",
                "content": "Type <code>B</code> or <code>BLOCK</code>. Give the block a standardized name (e.g., <code>ELEC_PANEL_100A</code> or <code>DOOR_SINGLE_900MM</code>). Click 'Pick point' to assign the insertion base point—never leave it at default (0,0,0) as this makes placement awkward. Click 'Select objects', choose your geometry, choose 'Convert to block', and confirm."
            },
            {
                "title": "Step 3: Adding Fillable Text with Attribute Definitions (ATTDEF)",
                "content": "Before finalizing a title block or tag, type <code>ATTDEF</code>. Define the Attribute Tag (e.g., <code>ROOM_NAME</code>), Prompt (e.g., <code>Enter Room Name:</code>), and default value. Place the text marker next to your geometry. When creating the block, include the attribute definitions in your selection. When inserted, AutoCAD automatically prompts users to fill in data."
            },
            {
                "title": "Step 4: Authoring Dynamic Blocks (BEDIT)",
                "content": "Double-click any block to launch the <b>Block Editor</b> (<code>BEDIT</code>). Use the Authoring Palettes to assign Parameters (such as Linear, Visibility, or Alignment) and pair them with Actions (such as Stretch, Rotate, Array, or Flip). A single dynamic door block can replace dozens of static doors by offering width stretches and swing flip states."
            },
            {
                "title": "Step 5: Exporting External Block Libraries (WBLOCK)",
                "content": "To use your block across multiple drawings, type <code>WBLOCK</code> (Write Block). Select 'Block' from the source menu and specify a file destination in your company's central CAD content library. Team members can now insert the block via the <b>Blocks Palette</b> (<code>INSERT</code>) or <b>Design Center</b> (<code>ADC</code>)."
            }
        ],
        "troubleshooting": [
            ("Block colors do not change when changing layers", "Entities inside the block were drawn on a specific layer (e.g., Layer 'Walls') or had hardcoded color overrides. Open the block in <code>BEDIT</code>, select all entities, set Layer to '0' and Color to 'ByLayer', then save and close."),
            ("Block inserts miles away from cursor", "The insertion base point was left at coordinates (0,0,0) rather than on the geometry itself. Open <code>BEDIT</code>, use the <code>BASE</code> command or move geometry to origin (0,0), and save."),
            ("Attributes do not update after editing block definition", "After modifying attribute definitions in Block Editor, run the <code>ATTSYNC</code> or <code>BATTMAN</code> command in model space to synchronize existing block instances with the updated definition.")
        ],
        "multi_cad_tips": "Dynamic blocks authored in AutoCAD function with full visibility states and stretch grips in GstarCAD and BricsCAD. GstarCAD also features a native Dynamic Block Editor and unique tools like 'Batch Block Replace' and 'Block Quantity Takeoff'.",
        "best_practices": [
            "Always author standard component geometry on Layer 0 with ByLayer properties.",
            "Establish strict, structured naming conventions (e.g., [Discipline]_[Category]_[Descriptor]_[Size]).",
            "Use WBLOCK to curate centralized network libraries rather than copying and pasting from old drawings.",
            "Run ATTSYNC whenever attribute positions, font styles, or tags are revised in the Block Editor."
        ],
        "related_concepts": [
            ("dynamic-blocks-autocad", "Dynamic Blocks & Parametric Actions"),
            ("attributes-blocks", "Block Attributes & Data Extraction"),
            ("layers-gstarcad", "Layer 0 Standards & Hierarchy"),
            ("cad-file-management-best-practices", "CAD Library Management")
        ]
    },
    {
        "slug": "how-to-use-xrefs-autocad",
        "title": "How to Use External References (Xrefs) in AutoCAD: Attach, Overlay & Path Management",
        "desc": "Master external references (Xrefs) in AutoCAD: multi-disciplinary team collaboration, Attach vs Overlay differences, relative path resolution, clipping boundaries, and binding workflows.",
        "software": "AutoCAD",
        "sw_slug": "autocad",
        "quick_answer": "To link a background DWG in AutoCAD: Type XREF (or XR), click 'Attach DWG', choose your file, select Reference Type ('Overlay' is recommended to prevent circular nesting), set Path Type to 'Relative Path', check 'Uniform Scale = 1.0', and click OK to position the reference.",
        "steps": [
            {
                "title": "Step 1: The External References Manager (XR Palette)",
                "content": "Type <code>XREF</code> or <code>XR</code> to open the palette. Click the top-left icon dropdown and choose <b>Attach DWG</b> (or Attach Image, PDF, DGN, Point Cloud). Locate your base file (e.g., <code>ARCH_LEVEL_01_BASE.dwg</code>)."
            },
            {
                "title": "Step 2: Attach vs. Overlay — Critical Strategic Choice",
                "content": "<b>Attach</b> means the Xref will follow your drawing as a nested reference if your file is subsequently xref'd by someone else. <b>Overlay</b> (strongly recommended for consultant files) ensures the background is visible only in your drawing and does NOT propagate into downstream drawings, preventing circular reference errors."
            },
            {
                "title": "Step 3: Setting Coordinate Alignment & Relative Paths",
                "content": "In collaborative workflows, ensure 'Insertion Point: Specify on-screen' is UNCHECKED, with X=0, Y=0, Z=0 and Scale=1.0. This ensures architectural, structural, and MEP files align to shared world project coordinates (WCS). Always select <b>Relative Path</b> (e.g., <code>.\\Ref\\Base.dwg</code>) so drawings remain linked when project folders move across servers or cloud drives."
            },
            {
                "title": "Step 4: Clipping and Fading Backgrounds (XCLIP & XDWGFADECTL)",
                "content": "To focus on a specific building zone, type <code>XCLIP</code>, select the reference, choose 'New boundary', and draw a rectangular or polygonal crop area. Use the system variable <code>XDWGFADECTL</code> (default 50) to fade background xrefs on-screen so your active work stands out with visual clarity."
            }
        ],
        "troubleshooting": [
            ("Xref Status shows 'Not Found' or 'Unresolved'", "The linked file was renamed, moved, or the absolute drive path changed. Select the missing item in the XREF palette, look at 'Saved Path' in the bottom pane, click '...' and remap to the new location. Then right-click > Path > Make Relative."),
            ("Circular Reference Warning on file load", "A file references another file that in turn references the first file. Change the Reference Type from <code>Attach</code> to <code>Overlay</code> in both files to break the infinite loading loop."),
            ("Layers inside the Xref keep reverting to original colors after reopening", "Check the <code>VISRETAIN</code> system variable. Setting <code>VISRETAIN = 1</code> tells AutoCAD to preserve your local layer color, visibility, and linetype overrides for xref layers across sessions.")
        ],
        "multi_cad_tips": "GstarCAD and ZWCAD manage Xrefs with complete DWG compatibility. GstarCAD includes an optimized 'Xref Manager' that supports background multithreaded loading and in-place reference editing via <code>REFEDIT</code>.",
        "best_practices": [
            "Default to Overlay instead of Attach unless intentionally designing a hierarchical master drawing.",
            "Always store project files on shared servers using Relative Paths, never hardcoded C:\\ drive paths.",
            "Set VISRETAIN to 1 to preserve customized discipline layer overrides.",
            "Use eTransmit when archiving or sharing project bundles to automatically package all external dependencies."
        ],
        "related_concepts": [
            ("dwg-file-format", "DWG Architecture & Dependency Trees"),
            ("layers-gstarcad", "Xref Layer Overrides & Filters"),
            ("construction-documentation", "Multi-Disciplinary Model Coordination"),
            ("cad-file-management-best-practices", "Project Folder Structure Standards")
        ]
    },
    {
        "slug": "autocad-keyboard-shortcuts",
        "title": "Essential AutoCAD Keyboard Shortcuts, Function Keys & Command Aliases",
        "desc": "Comprehensive guide to essential AutoCAD keyboard shortcuts: core 2D drafting aliases, modifier keys, F1-F12 function toggles, and step-by-step PGP customization for drafting speed.",
        "software": "AutoCAD",
        "sw_slug": "autocad",
        "quick_answer": "Top AutoCAD shortcuts: L (Line), PL (Polyline), C (Circle), REC (Rectangle), M (Move), CO (Copy), RO (Rotate), TR (Trim), EX (Extend), O (Offset), F (Fillet), SC (Scale), MI (Mirror), H (Hatch), B (Block), XR (Xref), Ctrl+1 (Properties), and F3/F8 (OSNAP/ORTHO).",
        "steps": [
            {
                "title": "1. Essential 2D Geometry Creation Aliases",
                "content": "<code>L</code>: Line | <code>PL</code>: Polyline | <code>C</code>: Circle | <code>A</code>: Arc | <code>REC</code>: Rectangle | <code>EL</code>: Ellipse | <code>POL</code>: Polygon | <code>H</code>: Hatch | <code>REG</code>: Region | <code>T</code> or <code>MT</code>: Multiline Text."
            },
            {
                "title": "2. Primary Precision Modification Commands",
                "content": "<code>M</code>: Move | <code>CO</code> / <code>CP</code>: Copy | <code>RO</code>: Rotate | <code>TR</code>: Trim | <code>EX</code>: Extend | <code>O</code>: Offset | <code>F</code>: Fillet (use R=0 to join corners) | <code>CHA</code>: Chamfer | <code>MI</code>: Mirror | <code>SC</code>: Scale | <code>S</code>: Stretch | <code>J</code>: Join | <code>X</code>: Explode."
            },
            {
                "title": "3. Function Key Hardware Toggles (F1 - F12)",
                "content": "<b>F1</b>: Help | <b>F2</b>: Command History Window | <b>F3</b>: Object Snap (OSNAP) On/Off | <b>F5</b>: Isoplane Toggle | <b>F7</b>: Grid Display | <b>F8</b>: Ortho Mode (constrain 90°) | <b>F9</b>: Snap to Grid | <b>F10</b>: Polar Tracking | <b>F11</b>: Object Snap Tracking | <b>F12</b>: Dynamic Input."
            },
            {
                "title": "4. Customizing Your acad.pgp Command Aliases",
                "content": "To edit shortcuts, type <code>ALIASEDIT</code> (Express Tools) or open <code>acad.pgp</code> directly (Manage tab > Edit Aliases). Scroll to the bottom and append custom aliases (e.g., <code>QQ, *PURGE</code> or <code>FF, *FILLET</code>). Save the text file and run <code>REINIT</code> (check PGP file box) to load new hotkeys immediately without restarting AutoCAD."
            }
        ],
        "troubleshooting": [
            ("Command line does not appear when typing", "Dynamic Input might be off or the command window was closed. Press <code>Ctrl+9</code> to toggle the Command Line window back on. Press <code>F12</code> to enable dynamic heads-up typing."),
            ("Custom PGP shortcuts stopped working after upgrade", "New CAD versions install a fresh default PGP file. Always maintain a backup copy of your customized aliases section and paste them at the very bottom of the new version's PGP file."),
            ("ESC key doesn't cancel stubborn commands", "If a macro or AutoLISP routine is trapped in a loop, press <code>Ctrl+C</code> or <code>ESC</code> multiple times. Check your CUI macro button assignments if a command continually relaunches.")
        ],
        "multi_cad_tips": "GstarCAD and ZWCAD support full PGP alias mapping (<code>gcad.pgp</code> / <code>zwcad.pgp</code>) with 100% AutoCAD shortcut compatibility. You can directly import your AutoCAD PGP file into GstarCAD using the Customize dialog.",
        "best_practices": [
            "Keep your left hand on the keyboard and right hand on the mouse for maximum drafting velocity.",
            "Customize single-letter or double-letter aliases for commands you invoke more than 20 times per hour.",
            "Master F3 (OSNAP), F8 (ORTHO), and F10 (Polar Tracking) for high-precision vector drafting.",
            "Use Spacebar or Right-Click as an instantaneous Enter confirmation."
        ],
        "related_concepts": [
            ("dynamic-input", "Dynamic Input & Cursor Heads-Up Drafting"),
            ("autolisp", "AutoLISP Customization & Automation"),
            ("layers-gstarcad", "Layer Management Hotkeys"),
            ("cad-career-paths", "CAD Drafter Productivity Best Practices")
        ]
    },
    # SOLIDWORKS FAQs
    {
        "slug": "how-to-create-assembly-solidworks",
        "title": "How to Create an Assembly in SOLIDWORKS: Mates, Degrees of Freedom & Best Practices",
        "desc": "Comprehensive SOLIDWORKS assembly guide: inserting base parts, applying standard/advanced/mechanical mates, managing degrees of freedom, and troubleshooting over-defined mate conflicts.",
        "software": "SOLIDWORKS",
        "sw_slug": "solidworks",
        "quick_answer": "To build a robust SOLIDWORKS assembly: Open File > New > Assembly. Drop your foundational base component directly onto the Origin (0,0,0) to lock it in space (Fixed). Insert secondary components and apply standard mates (Coincident, Concentric, Distance) to constrain required Degrees of Freedom (DOF).",
        "steps": [
            {
                "title": "Step 1: Grounding the Base Component at Origin",
                "content": "When inserting the first component into a new assembly, click the green checkmark in the PropertyManager without clicking in the graphics viewport. This automatically aligns the component origin with the assembly origin and marks it as <b>(f) Fixed</b>. A properly grounded base part is crucial for assembly stability."
            },
            {
                "title": "Step 2: Applying Standard Geometric Mates",
                "content": "Click <b>Mate</b> (paperclip icon) or press <code>S</code>. Select two entity faces, axes, or planes. Apply standard mates: <b>Concentric</b> (align cylinder centerlines), <b>Coincident</b> (align flat faces), <b>Parallel</b>, or <b>Distance</b>. Aim to remove degrees of freedom systematically without redundant constraints."
            },
            {
                "title": "Step 3: Utilizing Advanced & Mechanical Mates",
                "content": "Under Advanced Mates, use <b>Width</b> to center a tab between two clevis ears in a single mate. Use <b>Path Mate</b> or <b>Linear Coupler</b> for mechanism kinematics. Under Mechanical Mates, choose <b>Gear</b>, <b>Rack & Pinion</b>, or <b>Screw</b> to simulate mechanical power transmission."
            },
            {
                "title": "Step 4: Checking Degrees of Freedom & Interference Detection",
                "content": "Go to the Evaluate tab and run <b>Interference Detection</b> to verify clearances between adjacent solids before releasing parts for CNC or mold tooling. In the FeatureManager tree, components marked with <code>(-)</code> have unconstrained degrees of freedom."
            }
        ],
        "troubleshooting": [
            ("Over-defined assembly error (red/yellow mate alerts)", "Conflicting mates prevent geometric solution. Right-click the red component, select <b>View Mates</b>, or launch <b>MateXpert</b>. Suppress or delete redundant concentric/coincident mates one by one to find the conflict."),
            ("Component moves unexpectedly when dragging", "The part has free degrees of freedom. Right-click the part > 'Show DOF' or test by dragging with the left mouse button. Apply an additional angle, parallel, or distance mate to lock orientation."),
            ("Large assembly performance is sluggish", "Turn on <b>Large Assembly Settings</b> (Tools > Options). Set lightweight mode for components, turn off RealView Graphics and ambient occlusion, and use Defeature or SpeedPak for complex vendor sub-assemblies.")
        ],
        "multi_cad_tips": "Parametric assembly mating principles in SOLIDWORKS translate directly to Autodesk Inventor (Joints/Constraints), PTC Creo, and Onshape. Neutral STEP AP242 and Parasolid (.x_t) files transfer assembly component structures reliably.",
        "best_practices": [
            "Always fix the primary chassis or base part to the assembly origin.",
            "Prefer mating to principal datum planes (Front/Top/Right) where possible rather than fragile chamfered faces.",
            "Use Sub-Assemblies to organize logical subsystems and maintain clean top-level BOM hierarchies.",
            "Run Collision Detection and Interference Detection regularly during design development."
        ],
        "related_concepts": [
            ("solidworks-term-5", "SOLIDWORKS Assembly Mates & Topologies"),
            ("bottom-up-design", "Bottom-Up vs Top-Down Assembly Strategy"),
            ("solidworks-file-formats", "SLDPRT, SLDASM & Neutral Formats"),
            ("quality-assurance-cad", "Interference Detection & QA Workflows")
        ]
    },
    {
        "slug": "how-to-create-drawing-solidworks",
        "title": "How to Create Manufacturing Drawings in SOLIDWORKS: Views, GD&T, BOM & Detailing",
        "desc": "Step-by-step SOLIDWORKS 2D detailing guide: standard orthographic views, section and detail cuts, model item annotations, GD&T symbols, and automated Bill of Materials tables.",
        "software": "SOLIDWORKS",
        "sw_slug": "solidworks",
        "quick_answer": "To create a manufacturing drawing in SOLIDWORKS: Open your 3D part or assembly, click File > Make Drawing from Part/Assembly, select a drawing template (e.g. ISO A2 or ANSI B), drag standard views from the View Palette, use 'Model Items' to auto-import driving dimensions, and add GD&T tolerances.",
        "steps": [
            {
                "title": "Step 1: Selecting Sheet Format & View Layout",
                "content": "Choose File > Make Drawing from Part/Assembly. Select your company drawing template with pre-configured title block, projection angle (First Angle for ISO/Europe, Third Angle for ANSI/US), and sheet scale. Drag the <b>Front View</b> from the View Palette onto the sheet; projected Top and Right views follow automatically."
            },
            {
                "title": "Step 2: Section, Detail & Auxiliary Views",
                "content": "From the View Layout tab, select <b>Section View</b> to cut through internal cavities, bore holes, and O-ring grooves. Use <b>Detail View</b> to create an enlarged circular callout (e.g., 2:1 or 4:1 scale) of intricate thread reliefs and chamfers. Add an isometric shaded view in the upper-right corner for visual clarity."
            },
            {
                "title": "Step 3: Model Items vs. Smart Dimensions",
                "content": "Click <b>Model Items</b> on the Annotation tab to import dimensions directly from the 3D parametric sketches. These driving dimensions automatically update whenever 3D part geometry changes. Use <b>Smart Dimension</b> for reference dimensions, noting them with parentheses (e.g., <code>(50.0)</code>)."
            },
            {
                "title": "Step 4: GD&T, Surface Finish & Weld Symbols",
                "content": "Apply <b>Datum Feature</b> symbols to primary locating faces. Use the <b>Geometric Tolerance</b> tool to specify position, flatness, perpendicularity, and runout controls with appropriate material condition modifiers (MMC/LMC) per ASME Y14.5 or ISO 1101 standards."
            },
            {
                "title": "Step 5: Bill of Materials (BOM) & Auto Ballooning",
                "content": "For assemblies, go to Insert > Tables > <b>Bill of Materials</b>. Choose Parts-only or Indented BOM. SOLIDWORKS generates a live table linked to custom part properties (Part Number, Material, Description). Click <b>Auto Balloon</b> to label every item number cleanly."
            }
        ],
        "troubleshooting": [
            ("Dimensions turn olive green or dangling (yellow)", "The edge or vertex that the dimension was referencing was modified or deleted in the 3D model. Reattach the dangling dimension by dragging its attachment handle to the new valid edge or face."),
            ("Title block text is uneditable", "Title blocks are stored in the Sheet Format layer. Right-click anywhere on the drawing sheet and select <b>Edit Sheet Format</b>. Modify title block text and revision blocks, then right-click > 'Edit Sheet' to return."),
            ("Drawing views display coarse or faceted circles", "Go to Tools > Options > Document Properties > Image Quality. Increase the 'Shaded and draft quality' slider to High for smooth circular geometry.")
        ],
        "multi_cad_tips": "SOLIDWORKS drawing sheets (.SLDDRW) can be batch-exported to DWG/DXF for legacy CAM or to vector PDF with embedded 3D layers for vendor quoting.",
        "best_practices": [
            "Store company title blocks and border parameters in standardized .SLDDRT sheet formats.",
            "Always link title block fields (Author, Material, Mass, Date) to 3D model custom properties.",
            "Maintain strict GD&T standards (ASME Y14.5M / ISO 1101) to eliminate ambiguous manufacturing tolerances.",
            "Perform a drawing check against model revisions prior to PDF release."
        ],
        "related_concepts": [
            ("solidworks-term-7", "SOLIDWORKS 2D Detailing & Standards"),
            ("construction-documentation", "Engineering Drawing Standards & Practices"),
            ("solidworks-file-formats", "SLDDRW & DXF Export Workflows"),
            ("quality-assurance-cad", "Drawing Quality Control Checklists")
        ]
    },
    {
        "slug": "solidworks-file-formats",
        "title": "SOLIDWORKS File Formats Guide: SLDPRT, SLDASM, SLDDRW & Neutral CAD Exports",
        "desc": "Complete reference guide to SOLIDWORKS proprietary file formats (SLDPRT, SLDASM, SLDDRW) and neutral export standards (STEP, IGES, Parasolid, STL, 3MF, DWG) for manufacturing and collaboration.",
        "software": "SOLIDWORKS",
        "sw_slug": "solidworks",
        "quick_answer": "SOLIDWORKS uses three core native file types: .SLDPRT (individual 3D parts), .SLDASM (assemblies with mate relationships), and .SLDDRW (2D manufacturing drawings). For vendor collaboration and CNC manufacturing, export to STEP AP214/AP242, Parasolid (.x_t), or STL/3MF for 3D printing.",
        "steps": [
            {
                "title": "1. Native SOLIDWORKS Document Formats",
                "content": "<b>.SLDPRT</b>: Stores 3D solid and surface features, sketch history, material properties, and configurations. <b>.SLDASM</b>: References external part files and contains mate constraints, exploded views, and assembly BOM structures. <b>.SLDDRW</b>: 2D drawing sheets referencing parts/assemblies for shop floor fabrication."
            },
            {
                "title": "2. High-Fidelity Neutral Formats for CNC & Tooling (STEP & Parasolid)",
                "content": "<b>STEP (.step / .stp)</b>: The universal ISO standard. Use <b>AP214</b> for basic color and layer retention, or <b>AP242</b> for Model-Based Definition (MBD) including 3D GD&T and PMI. <b>Parasolid (.x_t / .x_b)</b>: The native geometric modeling kernel of SOLIDWORKS, NX, and Onshape, delivering 100% loss-free solid geometry transfer without tolerance stitching issues."
            },
            {
                "title": "3. Additive Manufacturing & 3D Printing Formats (STL vs. 3MF)",
                "content": "<b>STL (.stl)</b>: Legacy triangulated surface mesh format. Always adjust Export Options (Set Deviation to <0.02 mm and Angle to <5°) to avoid faceted cylindrical prints. <b>3MF (.3mf)</b>: Modern XML-based standard containing unit data, multi-material assignments, color texture maps, and full assembly structures."
            },
            {
                "title": "4. Lightweight Collaboration & Viewing Formats (eDrawings & 3D PDF)",
                "content": "<b>eDrawings (.eprt / .easm / .edrw)</b>: Compressed lightweight viewer files with built-in measurement, dynamic cross-sectioning, and markup tools. Recipient only needs the free eDrawings Viewer. <b>3D PDF</b>: Standard PDF containing interactive 3D solid models viewable in Adobe Acrobat Reader."
            }
        ],
        "troubleshooting": [
            ("Imported STEP file appears as 'Surface Bodies' with gaps instead of a Solid", "The export tolerance in the originating system was too loose. In SOLIDWORKS, run <b>Import Diagnostics</b> (right-click imported body > Import Diagnostics > Heal All), or use 'Knit Surface' with 'Try to form solid' enabled."),
            ("Cannot open newer SOLIDWORKS files in older software version", "SOLIDWORKS files are not backwards compatible across major release years (e.g., SW2024 files cannot be opened in SW2022 directly). To share with older versions, export as <b>Parasolid (.x_t)</b> or <b>STEP (.step)</b>."),
            ("Assembly opens with missing components (Suppressed / Cannot Locate)", "SOLIDWORKS .SLDASM files only link to .SLDPRT files by file path; they do not embed them. Always use <b>Pack and Go</b> (File > Pack and Go) to bundle the assembly and all referenced parts into a single folder or zip file.")
        ],
        "multi_cad_tips": "SOLIDWORKS 3D Interconnect allows native opening of Inventor (.ipt), Creo (.prt), CATIA (.CATPart), and Solid Edge files directly without translating to neutral formats, preserving live links to native edits.",
        "best_practices": [
            "Use Pack and Go whenever sharing or archiving multi-part assemblies to avoid broken file references.",
            "Export to STEP AP242 when sending parts to CNC machine shops to retain exact B-Rep definitions.",
            "Adopt 3MF format over legacy STL for 3D printing workflows to eliminate unit scaling errors.",
            "Set Parasolid version export to N-1 or N-2 when transferring to older downstream CAM systems."
        ],
        "related_concepts": [
            ("cad-file-formats-guide", "Universal CAD File Format Master Guide"),
            ("cad-file-management-best-practices", "File Management, PDM & Revision Control"),
            ("bottom-up-design", "Assembly Reference Architecture"),
            ("step-file-exchange", "STEP AP214 vs AP242 Standards")
        ]
    },
    # Revit FAQs
    {
        "slug": "how-to-create-family-revit",
        "title": "How to Create Custom Parametric Families in Revit: Reference Planes, Parameters & Categories",
        "desc": "Master custom Revit family creation (RFA): choosing templates, establishing reference plane frameworks, driving dimensions with Type vs Instance parameters, and BIM scheduling.",
        "software": "Revit",
        "sw_slug": "revit",
        "quick_answer": "To build a parametric Revit family: Open File > New > Family, select the correct Family Template (e.g. Metric Generic Model or Window), establish your geometric skeleton with Reference Planes (RP), assign Type/Instance Parameters to aligned dimensions, model solid geometry locked to the planes, and test by 'flexing' parameters.",
        "steps": [
            {
                "title": "Step 1: Selecting the Right Family Template (.RFT)",
                "content": "Navigate to File > New > Family. The template defines the <b>Family Category</b> (e.g., Doors, Mechanical Equipment, Casework, Lighting Fixtures) and hosting behavior (Wall-hosted, Ceiling-hosted, Face-based, or Free-standing). Choosing the correct category is critical because it controls subcategories, line styles, view cut behavior, and BIM scheduling."
            },
            {
                "title": "Step 2: Constructing the Reference Plane Skeleton",
                "content": "Before creating any solid geometry, draw <b>Reference Planes</b> (shortcut <code>RP</code>) in plan and elevation views. Add dimensions (<code>DI</code>) between reference planes, apply the Equality constraint (<code>EQ</code>) to keep objects centered, and create overall width/depth/height dimensions."
            },
            {
                "title": "Step 3: Creating Type vs. Instance Parameters",
                "content": "Select a dimension and click 'Create Parameter' in the ribbon. Choose between: <b>Type Parameter</b> (value applies to all instances of that family catalog type, ideal for standard manufactured sizes) or <b>Instance Parameter</b> (value can vary independently per placed element in the model, ideal for custom lengths or clearance heights)."
            },
            {
                "title": "Step 4: Modeling Geometry & Locking to Planes",
                "content": "Create solid geometry using <b>Extrusion</b>, <b>Blend</b>, <b>Revolve</b>, <b>Sweep</b>, or <b>Swept Blend</b>. Align (<code>AL</code>) the solid faces to the reference planes and click the padlock icon to lock them. Never lock geometry to other geometry—always lock to Reference Planes."
            },
            {
                "title": "Step 5: Flexing the Model & Loading into Project",
                "content": "Open the <b>Family Types</b> dialog. Change parameter values (e.g., width from 900mm to 1200mm, height from 2100mm to 2400mm) and click Apply to 'flex' the model. If geometry breaks or throws constraints errors, fix the misaligned sketch locks. Click 'Load into Project' once verified."
            }
        ],
        "troubleshooting": [
            ("Constraints not satisfied / Over-constrained family error", "Multiple conflicting dimensions or sketches were locked to different planes. Delete locks on sketch boundaries and verify that dimensions only drive Reference Planes, not raw geometry edges."),
            ("Family does not cut properly in floor plan views", "Some Revit categories (such as Furniture, Specialty Equipment, Plumbing Fixtures) are non-cuttable and always display in projection. If section cut representation is needed, switch category to Generic Model or Casework in Family Category and Parameters."),
            ("Parameters do not appear in project schedules", "You used local Family Parameters instead of <b>Shared Parameters</b>. Shared Parameters reference a central GUID text file, allowing custom properties (e.g., Manufacturer, Fire Rating, Warranty Date) to appear in project-wide schedules and tag families.")
        ],
        "multi_cad_tips": "Revit families (.RFA) can be exported to standard IFC 4x3 classification classes or 3D DWG blocks. In Archicad and Allplan, equivalent parametric objects are authored using GDL scripts or SmartParts.",
        "best_practices": [
            "Follow the golden rule: Skeleton (Ref Planes) -> Parameters (Dims) -> Geometry (Extrusions) -> Flex (Test).",
            "Use Shared Parameters for all attributes that must be scheduled in BIM or tagged in sheet drawings.",
            "Keep nested family geometry clean and avoid over-modeling high-polygon details (such as screw threads) that bloat RVT project file sizes.",
            "Establish distinct Coarse, Medium, and Fine visibility graphics settings for fast viewport rendering."
        ],
        "related_concepts": [
            ("bim-workbench", "BIM Parameter Standardization & Scheduling"),
            ("revit-vs-autocad-which-to-learn", "Revit BIM vs AutoCAD 2D Workflows"),
            ("construction-documentation", "Revit BIM Documentation Standards"),
            ("quality-assurance-cad", "BIM Model Quality Control & Auditing")
        ]
    },
    {
        "slug": "how-to-create-sheets-revit",
        "title": "How to Create Sheets, Views & Drawing Sets in Revit: Viewports, Title Blocks & Revisions",
        "desc": "Complete Revit documentation guide: creating title block sheets, placing and scaling floor plan/section views, managing sheet numbering conventions, and automated revision tracking.",
        "software": "Revit",
        "sw_slug": "revit",
        "quick_answer": "To create a sheet in Revit: Right-click 'Sheets (all)' in the Project Browser > New Sheet, select your company Title Block family (e.g., A1 Metric), drag desired views (Floor Plans, Elevations, Sections) from the Project Browser onto the sheet, and organize view titles.",
        "steps": [
            {
                "title": "Step 1: Creating a New Sheet and Loading Title Blocks",
                "content": "In the Project Browser, right-click <b>Sheets</b> and choose <b>New Sheet</b>. Choose an existing title block family or click Load to import a custom corporate title block (.RFA). Set sheet properties in the Properties palette: Sheet Number (e.g., <code>A-101</code>), Sheet Name (e.g., <code>GROUND FLOOR PLAN</code>), Drawn By, and Checked By."
            },
            {
                "title": "Step 2: Placing Views and Managing Viewport Scales",
                "content": "Drag any plan, section, callout, or 3D view directly from the Project Browser onto the sheet area. Click to place. The Viewport Scale is controlled by the source view properties (e.g., 1:100 or 1:50). Note: A standard Revit model view can only be placed on ONE sheet at a time; to place the same view on multiple sheets, right-click the view > <b>Duplicate as a Dependent</b>."
            },
            {
                "title": "Step 3: Configuring View Titles and Grid Alignment",
                "content": "Click the placed viewport to adjust its position. Click the View Title line independently to move it or adjust its length. Use Viewport Guide Grids (View tab > <b>Guide Grid</b>) to align floor plans, grids, and title blocks across consecutive sheets identically."
            },
            {
                "title": "Step 4: Managing Sheet Lists & Automated Revisions",
                "content": "Create an automated drawing index: Go to View > Schedules > <b>Sheet List</b>. Add Sheet Number, Sheet Name, Current Revision, and Issue Date. Use the <b>Sheet Issues/Revisions</b> dialog (View tab) to log Delta Revisions (Add / Cloud / Issue), which automatically updates revision tables in title blocks."
            }
        ],
        "troubleshooting": [
            ("Error: 'View is already placed on Sheet A-102'", "Revit enforces a strict rule that model views can only exist on a single sheet. To show the same view on another sheet, right-click the view in Project Browser > Duplicate View > <b>Duplicate as a Dependent</b> or <b>Duplicate with Detailing</b>."),
            ("Floor plan view boundaries overlap the entire sheet", "The view's Crop Region is too large or unclipped. Open the source view, check 'Crop View' and 'Crop Region Visible' in Properties, and drag the rectangular crop boundary handles tight around your building geometry."),
            ("Grid lines and level markers disappear on sheets", "Ensure Grid 3D extents intersect the view's cut plane, or adjust the Crop Region to include grid heads. Check Visibility/Graphic Overrides (<code>VG</code>) > Annotation Categories to confirm Grids are turned on.")
        ],
        "multi_cad_tips": "Revit sheets can be batch-exported to PDF or multi-layer DWG files using custom Layer Export Mapping (File > Export > CAD Formats > DWG > Export Setup).",
        "best_practices": [
            "Use View Templates to enforce consistent scale, detail level, and category visibility across all plan sheets.",
            "Establish strict Sheet Numbering conventions (e.g., Disciplinary Prefix-Level-SheetType: A-101, M-201, S-301).",
            "Leverage Guide Grids to ensure identical viewport placement and alignment across multi-story buildings.",
            "Track project milestones with the integrated Sheet Issues/Revisions tool for automated title block updates."
        ],
        "related_concepts": [
            ("how-to-create-family-revit", "Revit Family Creation & Parameters"),
            ("construction-documentation", "Construction Document Package Production"),
            ("revit-vs-autocad-which-to-learn", "Revit BIM vs AutoCAD Detailing"),
            ("cad-file-management-best-practices", "BIM Project Organization & Standards")
        ]
    },
    # Fusion 360 FAQs
    {
        "slug": "how-to-export-stl-fusion-360",
        "title": "How to Export STL & 3MF from Fusion 360 for 3D Printing: Resolution, Mesh & Repair",
        "desc": "Complete guide to exporting 3D print files from Fusion 360: STL vs 3MF comparisons, mesh refinement parameters, unit scaling fix, and non-manifold solid repair.",
        "software": "Fusion 360",
        "sw_slug": "fusion-360",
        "quick_answer": "To export an STL or 3MF in Fusion 360: In the Browser tree, right-click your Body or Component > select 'Save As Mesh'. Select 3MF (recommended) or STL format, set Refinement to 'High' (or Custom: Normal Deviation 0.01mm), choose Millimeter units, and save to your drive or send directly to your slicer (Bambu Studio, Cura, PrusaSlicer).",
        "steps": [
            {
                "title": "Step 1: Choosing 'Save As Mesh' vs Legacy 3D Print Tool",
                "content": "Right-click the target solid body or top-level component in the Browser tree and click <b>Save As Mesh</b>. Alternatively, use the Utilities tab > Make > <b>3D Print</b>. Saving at the component level preserves multi-body relative positioning."
            },
            {
                "title": "Step 2: STL vs. 3MF — The Modern Standard",
                "content": "Choose <b>3MF (.3mf)</b> whenever supported by your slicer (Bambu Studio, OrcaSlicer, PrusaSlicer, Cura). 3MF files contain exact physical units, individual multi-body components, color information, and significantly smaller file sizes. Choose <b>STL (Binary)</b> for older legacy 3D printers and CAM software."
            },
            {
                "title": "Step 3: Configuring Mesh Refinement & Tolerances",
                "content": "In the Refinement dropdown: <b>Medium</b> is suitable for flat mechanical brackets. <b>High</b> is required for curved organic shapes, ball joints, and fine threads. For master precision: select <b>Custom</b> and set Surface Deviation to <code>0.005 mm</code> and Normal Deviation to <code>5.0 deg</code> to eliminate polygon facet lines."
            },
            {
                "title": "Step 4: Verifying Watertight Manifold Geometry",
                "content": "Before sending to slice, inspect the Browser icon for your part: it must show a solid cylinder icon (Solid Body), not an orange open-envelope icon (Surface Body). Switch to the <b>Mesh tab</b> > Modify > <b>Repair Mesh</b> to automatically stitch open boundaries or remove self-intersections."
            }
        ],
        "troubleshooting": [
            ("Model imports 10x or 1000x too small into Slicer (e.g. millimeters vs meters)", "Fusion 360 exported in centimeters or inches while the slicer defaults to millimeters. In the Save As Mesh dialog, explicitly verify that 'Unit Type' is set to <b>Millimeter</b>, not 'Document Units'."),
            ("Curved surfaces appear faceted / blocky after 3D printing", "The export refinement was set to Low or Medium. Re-export the mesh with Refinement set to <b>High</b> or Custom (Maximum Edge Length < 2mm, Normal Deviation < 5°)."),
            ("Slicer displays 'Non-manifold edges / Model has holes' warning", "The 3D model contains zero-thickness geometry or unstitched surfaces. In Fusion 360, use <code>Inspect > Section Analysis</code> to locate hollow interior voids, then combine bodies with <code>Combine > Join</code>.")
        ],
        "multi_cad_tips": "In SOLIDWORKS and Inventor, STL/3MF export options are configured in File > Save As > Options (Tessellation Resolution). Fusion 360's integrated Manufacture / Additive workspace also allows direct slicing and G-code generation.",
        "best_practices": [
            "Prefer 3MF over STL for additive manufacturing to maintain multi-body and unit integrity.",
            "Always inspect and repair non-manifold surfaces in the Mesh workspace before exporting.",
            "Set Refinement to High on round bearing journals, gears, and threads to avoid geometric flats.",
            "Organize functional mechanisms into distinct components before exporting complete assemblies."
        ],
        "related_concepts": [
            ("constraints-fusion", "Fusion 360 Parametric Modeling & Constraints"),
            ("fusion-360-vs-solidworks-which-better", "Fusion 360 vs SOLIDWORKS Feature Matrix"),
            ("cad-file-formats-guide", "STL, 3MF & STEP Format Deep Dive"),
            ("quality-assurance-cad", "Additive Manufacturing CAD Quality Checklists")
        ]
    },
    {
        "slug": "fusion-360-vs-solidworks-which-better",
        "title": "Fusion 360 vs SOLIDWORKS: Comprehensive CAD/CAM Comparison & Career Guide",
        "desc": "In-depth comparison between Autodesk Fusion 360 and Dassault Systèmes SOLIDWORKS: parametric modeling, cloud collaboration, CAM, FEA simulation, pricing, and job market demand.",
        "software": "Fusion 360",
        "sw_slug": "fusion-360",
        "quick_answer": "Choose Fusion 360 for fast prototyping, integrated CAD/CAM/CAE, cloud collaboration, startups, and hobbyists on a budget. Choose SOLIDWORKS for mainstream industrial manufacturing, heavy machinery engineering, complex large assemblies (10,000+ parts), and standard enterprise engineering job roles.",
        "steps": [
            {
                "title": "1. Modeling Architecture & Large Assembly Handling",
                "content": "<b>Fusion 360</b> uses a top-down, multi-body component design workspace where parts and assemblies coexist in a single file (.F3D) with timeline history. It excels at agile prototyping up to ~1,000 parts. <b>SOLIDWORKS</b> uses a strict file-linked architecture (.SLDPRT, .SLDASM) with specialized tools (SpeedPak, Large Assembly Mode) capable of handling massive industrial assemblies with 20,000+ components."
            },
            {
                "title": "2. Integrated CAM, CNC & Additive Manufacturing",
                "content": "<b>Fusion 360</b> includes best-in-class 2.5D, 3-axis, and 5-axis CAM milling toolpaths (derived from HSMWorks) and additive manufacturing slicers natively in its core subscription. <b>SOLIDWORKS</b> includes basic SOLIDWORKS CAM Standard, but advanced multi-axis CNC or specialized toolpath generation requires paid add-ons (like CAMWorks or Mastercam)."
            },
            {
                "title": "3. Simulation & Finite Element Analysis (CAE)",
                "content": "<b>Fusion 360</b> offers cloud-based FEA simulation (Static Stress, Modal Frequencies, Thermal, Non-linear Event Simulation, Generative Design) using cloud tokens. <b>SOLIDWORKS Simulation</b> runs locally on workstation hardware, offering deep structural, fatigue, drop test, and computational fluid dynamics (Flow Simulation) modules."
            },
            {
                "title": "4. Pricing, Licensing & Total Cost of Ownership",
                "content": "<b>Fusion 360</b>: Annual SaaS subscription (~$680/year), free tier for hobbyists/personal use, and generous startup discounts. <b>SOLIDWORKS</b>: Traditional desktop perpetual licenses (~$4,000 - $8,000 upfront + annual maintenance) or 3DEXPERIENCE SOLIDWORKS subscriptions."
            }
        ],
        "troubleshooting": [
            ("Transferring projects between Fusion 360 and SOLIDWORKS", "Use neutral <b>STEP AP242</b> or <b>Parasolid (.x_t)</b> format. Feature history trees will not translate into editable sketches, but direct modeling tools in both programs allow push-pull modifications on imported solids."),
            ("Cloud storage vs Local LAN security concerns", "Fusion 360 stores project data in the Autodesk Construction Cloud (with local offline cache). Enterprise defense and IT policies requiring air-gapped on-premise servers usually mandate SOLIDWORKS with local PDM Vault.")
        ],
        "multi_cad_tips": "Skills in parametric sketch constraints, feature hierarchy (Extrude, Revolve, Sweep, Loft), and assembly mates transfer 90% between Fusion 360, SOLIDWORKS, Autodesk Inventor, and Onshape.",
        "best_practices": [
            "Learn Fusion 360 for rapid hardware prototyping, 3D printing, and integrated CNC manufacturing.",
            "Master SOLIDWORKS if your career goal is mechanical engineering in automotive, aerospace, or industrial machinery.",
            "Maintain clean parametric sketch constraints (fully defined sketches) in both software to prevent timeline corruption."
        ],
        "related_concepts": [
            ("how-to-export-stl-fusion-360", "Fusion 360 3D Printing & Mesh Workflows"),
            ("how-to-create-assembly-solidworks", "SOLIDWORKS Assembly Mates & Structures"),
            ("cad-career-paths", "Mechanical CAD Career & Certification Guide"),
            ("bottom-up-design", "Top-Down vs Bottom-Up Assembly Paradigms")
        ]
    },
    # GstarCAD FAQs
    {
        "slug": "how-to-migrate-autocad-to-gstarcad",
        "title": "How to Migrate from AutoCAD to GstarCAD: DWG Compatibility, LISP & Command Migration",
        "desc": "Complete enterprise migration guide from AutoCAD to GstarCAD: 100% DWG native file opening, UI customization, AutoLISP/VBA script porting, and cost-benefit analysis.",
        "software": "GstarCAD",
        "sw_slug": "gstarcad",
        "quick_answer": "Migrating from AutoCAD to GstarCAD requires zero file conversion: GstarCAD opens and saves DWG/DXF files natively from AutoCAD R2.5 through 2026. Command names, aliases, ribbon layouts, CTB plot styles, and 95%+ of AutoLISP routines execute identically without code changes.",
        "steps": [
            {
                "title": "Step 1: Direct DWG/DXF File Opening & Integrity Verification",
                "content": "Install GstarCAD and open existing DWG drawings directly. GstarCAD uses the Open Design Alliance (ODA) certified DWG kernel, ensuring full fidelity for 2D geometry, 3D ACIS solids, dynamic blocks, associative dimensions, and external references (Xrefs) without translation."
            },
            {
                "title": "Step 2: Importing Plot Styles (.CTB/.STB) & Templates (.DWT)",
                "content": "Copy your company's <code>.ctb</code> plot style tables and <code>.dwt</code> seed templates into GstarCAD's support directory, or use <code>OPTIONS</code> > Files tab to add your shared network drive search paths. Type <code>STYLESMANAGER</code> to open the plot style folder directly."
            },
            {
                "title": "Step 3: Migrating AutoLISP, DCL Dialogs & Custom Scripts",
                "content": "Load your custom AutoLISP scripts via <code>APPLOAD</code>. GstarCAD includes Visual LISP compatibility and an integrated LISP IDE for debugging. Most VLX and LSP files execute with zero syntax modifications. Add frequent tools to the Startup Suite for automated session loading."
            },
            {
                "title": "Step 4: Transferring Custom Tool Palettes & PGP Aliases",
                "content": "Import your <code>acad.pgp</code> shortcut file directly into GstarCAD (or edit <code>gcad.pgp</code>). Custom Tool Palettes (.XTP) and CUI customization files can be imported via the Customize User Interface (<code>CUI</code>) dialog."
            }
        ],
        "troubleshooting": [
            ("Custom ObjectARX / C++ plugins do not load", "ObjectARX plugins compiled for AutoCAD (.arx) require recompilation using the GstarCAD GRX SDK (compatible C++ API headers). Contact your plugin vendor or recompile in Visual Studio using GRX libraries."),
            ("Fonts or special characters display as question marks (???)", "Missing specialized SHX fonts. Copy your architectural or engineering SHX font library into GstarCAD's <code>Fonts</code> directory (e.g., <code>C:\\Program Files\\Gstarsoft\\GstarCAD\\Fonts</code>) and type <code>REGEN</code>.")
        ],
        "multi_cad_tips": "GstarCAD offers unique productivity tools not found in standard AutoCAD, including Magnifier, QR Code / Barcode generator, Free Scale, and Batch Plotting.",
        "best_practices": [
            "Test critical AutoLISP and batch automation routines in a sandbox environment before company-wide rollout.",
            "Centralize CTB plot styles, standard templates, and SHX fonts on a shared network drive.",
            "Take advantage of GstarCAD's perpetual licensing model to eliminate recurring subscription overhead."
        ],
        "related_concepts": [
            ("gstarcad-system-requirements", "GstarCAD Hardware & Performance Guide"),
            ("autolisp-gstarcad", "AutoLISP in GstarCAD & Migration Guide"),
            ("layers-gstarcad", "GstarCAD Layer & Drafting Standards"),
            ("cad-file-management-best-practices", "CAD Standards & Network Setup")
        ]
    },
    {
        "slug": "gstarcad-system-requirements",
        "title": "GstarCAD System Requirements, Hardware Optimization & Performance Guide",
        "desc": "Official hardware requirements and performance tuning for GstarCAD: CPU, GPU, RAM, multi-threading settings, and graphics optimization for large DWG files.",
        "software": "GstarCAD",
        "sw_slug": "gstarcad",
        "quick_answer": "Minimum requirements: Windows 11/10/8, 64-bit multi-core CPU (2.5 GHz+), 4 GB RAM, 2 GB disk space. Recommended for large drawings & 3D: Intel Core i7 / AMD Ryzen 7 (3.5 GHz+), 16 GB+ DDR4/DDR5 RAM, NVMe SSD, and dedicated NVIDIA GeForce/RTX or AMD Radeon GPU (4GB+ VRAM, OpenGL 4.2+).",
        "steps": [
            {
                "title": "1. Minimum vs. Recommended Hardware Specifications",
                "content": "<b>Operating System</b>: Windows 11, Windows 10 (64-bit). <b>Processor</b>: 3.0 GHz+ Intel Core i5/i7 or AMD Ryzen 5/7 with high single-thread clock speed. <b>Memory (RAM)</b>: 8 GB for standard 2D drafting; 16 GB to 32 GB for 100MB+ large DWG files with dense Xrefs. <b>Storage</b>: High-speed NVMe PCIe SSD. <b>Graphics</b>: Dedicated GPU with DirectX 11 / OpenGL 4.2 support."
            },
            {
                "title": "2. Enabling Hardware Acceleration (GRAPHICSCONFIG)",
                "content": "Type <code>GRAPHICSCONFIG</code> in the GstarCAD command line. Ensure <b>Hardware Acceleration</b> is enabled. This offloads anti-aliasing, pan/zoom rasterization, and 3D shade rendering directly to the dedicated GPU, boosting framerates on dense vector drawings."
            },
            {
                "title": "3. Multi-Core CPU & Display Variable Optimization",
                "content": "GstarCAD features a multi-core computing engine. Set <code>WHIPTHREAD = 3</code> to distribute both redraw and regeneration calculations across all available CPU cores. Set <code>SELECTIONPREVIEW = 0</code> on ultra-dense drawings to prevent cursor hovering lag."
            },
            {
                "title": "4. Managing Large Drawing Memory Footprint",
                "content": "Regularly run <code>PURGE</code> (shortcut <code>PU</code>) to clear unused blocks, layers, and linetypes. Use <code>AUDIT</code> to fix internal database pointer errors. For large Xref structures, enable Demand Loading (<code>XLOADCTL = 2</code>) to load only visible layers into RAM."
            }
        ],
        "troubleshooting": [
            ("Graphics stutter or black screen when panning across large drawings", "Integrated Intel HD graphics driver conflict. In Windows Graphics Settings, force GstarCAD (<code>gcad.exe</code>) to run on 'High Performance' dedicated NVIDIA/AMD graphics card. Update GPU display drivers to the latest studio/gaming release."),
            ("Drawing open time is slow over network shares", "Antivirus software is scanning external Xrefs on read. Add the project network folder and GstarCAD executable to your Antivirus real-time scan exclusion list.")
        ],
        "multi_cad_tips": "GstarCAD requires approximately 50% less RAM and disk space than AutoCAD, enabling fluid performance on standard office laptops and legacy workstation hardware.",
        "best_practices": [
            "Install GstarCAD and active project files on an NVMe SSD for instant file read/write times.",
            "Enable Hardware Acceleration and multi-core processing (WHIPTHREAD = 3).",
            "Maintain clean DWG databases using AUDIT and PURGE routines before archiving."
        ],
        "related_concepts": [
            ("how-to-migrate-autocad-to-gstarcad", "AutoCAD to GstarCAD Migration Guide"),
            ("dwg-file-format", "DWG File Format Architecture & Optimization"),
            ("layers-gstarcad", "Layer Management & View Optimization"),
            ("cad-file-management-best-practices", "CAD Workstation Setup & IT Standards")
        ]
    },
    # Civil 3D FAQs
    {
        "slug": "how-to-create-surface-civil-3d",
        "title": "How to Create and Edit Surfaces in Civil 3D: TIN, Point Groups, Breaklines & Boundaries",
        "desc": "Master Autodesk Civil 3D surface modeling: TIN surface creation, importing survey point groups, adding breaklines for sharp terrain features, boundary clipping, and volume calculations.",
        "software": "Civil 3D",
        "sw_slug": "civil-3d",
        "quick_answer": "To build a TIN surface in Civil 3D: Open the Toolspace > Prospector tab > right-click 'Surfaces' > Create Surface. Name your surface (e.g., 'EG - Existing Ground'), expand Definition, right-click 'Point Groups' > Add your survey point group. Add Breaklines to lock road edges and retaining walls, and add an Outer Boundary to clip voids.",
        "steps": [
            {
                "title": "Step 1: Creating the Base TIN Surface",
                "content": "In the Prospector palette, right-click <b>Surfaces</b> and choose <b>Create Surface</b>. Set Surface Type to <b>TIN Surface</b> (Triangulated Irregular Network). Specify the layer, name it (e.g., <code>EG_Topographic</code>), and select a Surface Style (e.g., <code>Contours 1m and 5m (Background)</code>)."
            },
            {
                "title": "Step 2: Adding Point Groups & Survey Data",
                "content": "Expand your new surface under Prospector > Definition. Right-click <b>Point Groups</b> and click <b>Add</b>. Select your imported survey group (e.g., <code>_All Points</code> or <code>Ground_Shots</code>). Civil 3D creates Delaunay triangulation lines connecting the 3D coordinate points instantly."
            },
            {
                "title": "Step 3: Defining Linear Breaklines (Curbs, Ditches & Walls)",
                "content": "TIN algorithms can inappropriately triangulate across ridges or stream beds. Expand Definition > right-click <b>Breaklines</b> > Add. Select 3D polylines or feature lines representing road crowns, curbs, retaining walls, or ditch inverts. Breaklines force TIN edges to follow exact linear physical features."
            },
            {
                "title": "Step 4: Applying Outer and Hide Boundaries",
                "content": "Under Definition, right-click <b>Boundaries</b> > Add. Select a closed polyline around your project survey limits. Choose Type: <b>Outer</b> to clip unwanted long triangular slivers around the periphery, or Type: <b>Hide</b> to exclude building footprints or water bodies."
            }
        ],
        "troubleshooting": [
            ("Triangulation connects across empty concave spaces (flat false triangles)", "Add an Outer Boundary or adjust the maximum triangle length: Right-click Surface > Surface Properties > Definition tab > Build > Set 'Use Maximum Triangle Length' to Yes and specify a maximum length (e.g., 30m)."),
            ("Crossing Breaklines Error in Event Viewer", "Two breaklines cross each other at differing elevations, creating mathematical ambiguity. In the Event Viewer, zoom to the conflict coordinate and adjust feature line vertex elevations to snap to a shared elevation node.")
        ],
        "multi_cad_tips": "Civil 3D surfaces can be exported to LandXML (.xml) for use in Bentley OpenRoads, Carlson Civil, 12d Model, or machine control GPS excavators (Trimble / Topcon).",
        "best_practices": [
            "Keep raw survey data separate in dedicated point groups before surface integration.",
            "Always utilize standard Breaklines for all known grade breaks and hard landscape features.",
            "Use LandXML for cross-platform terrain data exchange with zero geometric loss."
        ],
        "related_concepts": [
            ("how-to-create-alignment-civil-3d", "Civil 3D Alignments & Corridor Design"),
            ("stormwater-management", "Stormwater Drainage & Catchment Modeling"),
            ("road-design-standards", "Civil Highway & Grading Standards"),
            ("quality-assurance-cad", "Survey QA & Terrain Model Validation")
        ]
    },
    {
        "slug": "how-to-create-alignment-civil-3d",
        "title": "How to Create Alignments & Profiles in Civil 3D: Horizontal Geometry & Stationing",
        "desc": "Complete Civil 3D alignment design tutorial: creating horizontal alignments from objects, tangent-curve layout tools, design speed criteria (AASHTO), and automated station labeling.",
        "software": "Civil 3D",
        "sw_slug": "civil-3d",
        "quick_answer": "To create a road centerline alignment in Civil 3D: Home tab > Create Design > Alignment > select 'Alignment Creation Tools' (or 'Create Alignment from Objects'). Define alignment name, type (Centerline), design speed, and design criteria file (AASHTO). Use tangent-tangent and curve tools to place your geometry.",
        "steps": [
            {
                "title": "Step 1: Alignment Creation Tools & Settings",
                "content": "From the Home tab, click <b>Alignment</b> > <b>Alignment Creation Tools</b>. Name the alignment (e.g., <code>Main_Street_CL</code>), set Type to <b>Centerline</b>, choose an Alignment Style, and select an Alignment Label Set (Major/Minor Stations + Geometry Points)."
            },
            {
                "title": "Step 2: Assigning Design Speed & AASHTO Criteria",
                "content": "In the Design Criteria tab, check 'Use criteria-based design'. Select your local standard design file (e.g., <code>AASHTO 2018 Imperial/Metric.xml</code>) and specify the minimum Design Speed (e.g., <code>60 km/h</code>). Civil 3D will automatically validate curve radii and superelevation rates."
            },
            {
                "title": "Step 3: Drawing Tangents and Free Spirals / Curves",
                "content": "In the Alignment Layout Tools toolbar, select <b>Tangent-Tangent (With Curves)</b> or place tangents first and use <b>Free Curve Filament Between Two Entities (Radius)</b>. Civil 3D dynamically keeps curves tangent to adjoining straight lines as vertex handles move."
            },
            {
                "title": "Step 4: Stationing & Station Equation Management",
                "content": "Labels generate automatically along the alignment. To adjust start station (e.g., starting at Station <code>10+000</code>), right-click Alignment > Alignment Properties > <b>Station Control</b> tab and update the Reference Station value."
            }
        ],
        "troubleshooting": [
            ("Warning warning glyph (exclamation triangle) appears on curves", "The curve radius violates minimum design criteria for the assigned design speed under AASHTO rules. Click the curve > open the Alignment Grid View (Panorama) to inspect the violation and increase curve radius."),
            ("Alignment station numbers are running backwards", "The polyline was drawn in reverse direction. Select Alignment > click <b>Reverse Direction</b> in the Alignment ribbon context tab.")
        ],
        "multi_cad_tips": "Alignments serve as the mathematical spine for Civil 3D Corridors, Profiles, Assemblies, Cross Sections, and Pipe Networks.",
        "best_practices": [
            "Always activate criteria-based design to catch minimum curve radius violations early.",
            "Use Free Curves (tangent to two entities) rather than fixed static radius arcs for smooth roadway transitions.",
            "Lock alignment stationing before generating detailed cross-section volumes."
        ],
        "related_concepts": [
            ("how-to-create-surface-civil-3d", "Civil 3D Terrain Surface Modeling"),
            ("road-design-standards", "AASHTO & Eurocode Road Geometric Standards"),
            ("traffic-engineering-cad", "Traffic Markings & Highway Planning"),
            ("construction-documentation", "Civil Engineering Plan & Profile Production")
        ]
    },
    # Blender FAQs
    {
        "slug": "blender-for-cad-users",
        "title": "Blender for CAD & BIM Users: Precision Modeling, Units, Modifiers & CAD Imports",
        "desc": "Essential guide for CAD/BIM engineers transitioning to Blender: precision snapping, metric unit setup, non-destructive modifiers, STEP/IFC import addons, and mesh cleanup.",
        "software": "Blender",
        "sw_slug": "blender",
        "quick_answer": "Blender is a polygonal mesh/SubD modeler, whereas CAD uses parametric mathematical B-Rep (NURBS) geometry. To use Blender for precision CAD work: set Scene Units to Metric (scale 0.001 for mm), enable MeasureIt and CAD Sketcher addons, use absolute numeric transform typing (e.g., G > X > 50), and import CAD files via STEP or BlenderBIM (IFC).",
        "steps": [
            {
                "title": "1. Fundamental Paradigm: Mesh vs. Parametric B-Rep",
                "content": "CAD software (AutoCAD, SOLIDWORKS, Revit) stores surfaces as mathematically precise NURBS equations and solid bodies (B-Rep). <b>Blender</b> stores shapes as polygonal meshes (vertices, edges, faces). Edits in Blender are topology-focused, enabling photorealistic rendering, VFX, and organic sculpting that CAD systems struggle to execute."
            },
            {
                "title": "2. Setting Up Metric Precision Units & Snapping",
                "content": "In Properties > <b>Scene Properties > Units</b>: Set Unit System to <b>Metric</b>, Unit Scale to <code>0.001</code>, and Length to <b>Millimeters</b>. Enable Edge Length display in Viewport Overlays. Turn on Snapping (magnet icon) set to <b>Vertex</b> and <b>Increment</b> for grid-aligned precision."
            },
            {
                "title": "3. Precision Numeric Input & CAD Sketcher Addon",
                "content": "During any transformation, type exact coordinates: <code>G</code> (Grab/Move) then <code>X</code> then <code>25.4</code> moves an entity exactly 25.4 mm along X. Install the open-source <b>CAD Sketcher</b> (Solvespace-based) addon to bring true constraint-based 2D sketching (coincident, tangent, dimensional constraints) directly inside Blender."
            },
            {
                "title": "4. Importing CAD (STEP) & BIM (IFC) Files",
                "content": "Use the free <b>STEP Importer</b> addon to import STEP AP214/AP242 assemblies with automatic adaptive tessellation. For architecture and BIM, install <b>BlenderBIM</b> to natively author and edit building models using open-standard IFC files without losing parametric properties."
            }
        ],
        "troubleshooting": [
            ("Imported CAD models show dark, smeared shading glitches", "Normal vectors are inverted or custom split normals are corrupt. Select the mesh > Edit Mode > press <code>Shift+N</code> (Recalculate Outside Normals). In Object Data Properties > Geometry Data, click 'Clear Custom Split Normals Data' and enable 'Auto Smooth'."),
            ("Boolean modifier fails or creates non-manifold holes", "Blender's default Fast Boolean solver struggles with coplanar faces. Switch the Boolean modifier solver option from 'Fast' to <b>'Exact'</b> and ensure intersecting meshes are completely manifold (closed solids).")
        ],
        "multi_cad_tips": "Blender is the ultimate visualization and animation companion to CAD: model technical geometry in SOLIDWORKS/Revit, export to STEP/IFC, and render photorealistic marketing visuals in Blender Cycles.",
        "best_practices": [
            "Set Scene Units to Millimeters before importing CAD geometry to prevent scale mismatches.",
            "Apply Scale (Ctrl+A > Apply All Transforms) on all meshes before adding Bevel or Boolean modifiers.",
            "Use BlenderBIM for open-source native IFC building documentation.",
            "Clean imported CAD mesh topology with 'Merge by Distance' (shortcut M) to remove duplicate vertices."
        ],
        "related_concepts": [
            ("cad-file-formats-guide", "CAD Formats vs Polygonal Meshes (STEP, OBJ, STL)"),
            ("bim-workbench", "OpenBIM & BlenderBIM Integration"),
            ("generative-ai-cad", "3D Visualization & Computational Rendering"),
            ("quality-assurance-cad", "Mesh Quality & Topology Optimization")
        ]
    },
    # FreeCAD FAQs
    {
        "slug": "freecad-vs-fusion-360",
        "title": "FreeCAD vs Fusion 360: Open-Source vs Freemium Parametric CAD Comparison",
        "desc": "Comprehensive comparison between FreeCAD (open-source) and Autodesk Fusion 360: Part Design workbenches, Topological Naming, offline privacy, CAM, Python scripting, and commercial use licensing.",
        "software": "FreeCAD",
        "sw_slug": "freecad",
        "quick_answer": "FreeCAD is 100% free, open-source (LGPL), runs completely offline on Windows/macOS/Linux, and has zero commercial restrictions. Fusion 360 is a cloud-connected freemium commercial tool with a polished UI, integrated multi-axis CAM, cloud rendering, and generative design, but limits its free tier for commercial use.",
        "steps": [
            {
                "title": "1. Licensing, Privacy & Commercial Freedom",
                "content": "<b>FreeCAD</b> is free forever under the LGPL open-source license. You can use it commercially without paying subscription fees, and your files (.FCStd) live 100% locally on your machine with zero cloud dependency. <b>Fusion 360</b>'s free 'Personal Use' tier restricts active documents (max 10 editable files), disables rapid tool changes in CAM, and prohibits commercial monetization."
            },
            {
                "title": "2. Parametric Modeling & Topological Naming Resolution",
                "content": "Both tools use standard parametric feature trees (Sketch -> Pad/Extrude -> Fillet). FreeCAD historically faced the 'Topological Naming Problem' (editing an early sketch could break downstream fillet references). The landmark <b>FreeCAD 1.0</b> release integrates topological naming algorithms directly into the core, delivering enterprise stability comparable to commercial CAD."
            },
            {
                "title": "3. Python Automation & Modular Workbenches",
                "content": "FreeCAD is built on top of the OpenCASCADE geometric kernel and has deep, complete Python API integration. Every button click corresponds to a Python command. Users can author custom workbenches, automated parametric part generators, and custom GUI tools with ease."
            },
            {
                "title": "4. CAM, FEA Simulation & Technical Drafting",
                "content": "FreeCAD includes the <b>CAM Workbench</b> (formerly Path) for G-code milling, the <b>FEM Workbench</b> (powered by CalculiX and Elmer) for structural and thermal analysis, and the <b>TechDraw Workbench</b> for generating 2D manufacturing drawings to ISO/ASME standards."
            }
        ],
        "troubleshooting": [
            ("FreeCAD sketch shows 'Under-constrained (N degrees of freedom)'", "Open the Sketcher Solver message pane. Add geometric constraints (Horizontal, Vertical, Coincident, Tangent) and dimensional constraints until the solver displays 'Fully constrained sketch' (lines turn green)."),
            ("Exporting files from FreeCAD to 3D printing slicers", "Select the final Pad or Revolution feature in the tree (not the raw sketch) > File > Export > <b>STL Mesh (*.stl)</b> or <b>3MF (*.3mf)</b>. Adjust mesh deviation in Edit > Preferences > Import-Export > Mesh Formats.")
        ],
        "multi_cad_tips": "FreeCAD natively imports and exports STEP, IGES, DXF, SVG, IFC, OBJ, STL, and CSG files, making it a powerful neutral format translator for engineering teams.",
        "best_practices": [
            "Upgrade to FreeCAD 1.0+ to benefit from integrated topological naming fixes.",
            "Always achieve a green 'Fully Constrained' status in Sketcher before extruding features.",
            "Reference datum planes and datum lines rather than solid faces for maximum parametric resilience.",
            "Use TechDraw for standard 2D drawings and BOM tables."
        ],
        "related_concepts": [
            ("how-to-export-stl-fusion-360", "Fusion 360 3D Printing & Parametric Modeling"),
            ("cad-file-formats-guide", "Open Source vs Proprietary CAD Standards"),
            ("bottom-up-design", "Parametric Feature Tree Best Practices"),
            ("autolisp", "CAD Scripting: Python vs AutoLISP")
        ]
    },
    # General & Career FAQs
    {
        "slug": "how-to-choose-cad-software",
        "title": "How to Choose the Right CAD Software: Decision Matrix by Industry & Budget",
        "desc": "Comprehensive CAD selection framework for students, engineers, and firms: mechanical (MCAD), architectural (BIM), civil, electrical (ECAD), licensing models, and software comparisons.",
        "software": "Multi-platform",
        "sw_slug": "autocad",
        "quick_answer": "Select CAD software based on your discipline: for 2D Drafting & General AEC, choose AutoCAD or cost-effective GstarCAD; for Building Architecture & BIM, choose Revit or Archicad; for Mechanical Engineering & Product Design, choose SOLIDWORKS, Inventor, or Fusion 360; for Civil Infrastructure, choose Civil 3D; for Open-Source/Hobbyists, choose FreeCAD or Blender.",
        "steps": [
            {
                "title": "1. Mechanical Engineering & Product Design (MCAD)",
                "content": "If designing machinery, consumer electronics, sheet metal parts, or injection-molded products, choose parametric solid modelers: <b>SOLIDWORKS</b> (industry standard), <b>Autodesk Inventor</b>, <b>PTC Creo</b>, <b>Siemens NX</b> (aerospace/automotive), or <b>Fusion 360</b> (startups/rapid prototyping)."
            },
            {
                "title": "2. Architecture, Engineering & Construction (AEC / BIM)",
                "content": "For 2D floor plans, details, and site plans: <b>AutoCAD</b> and <b>GstarCAD</b>. For full Building Information Modeling (BIM) with parametric components, multi-disciplinary clash coordination, and scheduling: <b>Autodesk Revit</b>, <b>Graphisoft Archicad</b>, <b>Nemetschek Allplan</b>, or <b>Vectorworks</b>."
            },
            {
                "title": "3. Civil Engineering, Surveying & Infrastructure",
                "content": "For road geometric design, digital terrain models (DTM), pipeline utilities, and earthwork grading: <b>Autodesk Civil 3D</b>, <b>Bentley OpenRoads / MicroStation</b>, or <b>12d Model</b>."
            },
            {
                "title": "4. Budget, Hardware & Licensing Model Considerations",
                "content": "Evaluate whether your organization requires <b>Subscription SaaS</b> (AutoCAD, Revit, Fusion) or <b>Perpetual Ownership</b> (GstarCAD, ZWCAD, BricsCAD) to reduce software overhead. Consider whether team members work on local high-spec workstations or need cloud collaboration."
            }
        ],
        "troubleshooting": [
            ("Working with clients who use different CAD platforms", "Establish a strict <b>Neutral File Exchange protocol</b>: use <b>STEP AP242</b> or <b>Parasolid (.x_t)</b> for 3D mechanical models, <b>IFC 4x3</b> for BIM architectural models, and <b>DWG/DXF</b> (saved to AutoCAD 2018 format) for 2D engineering drawings.")
        ],
        "multi_cad_tips": "Most professional engineering consultancies utilize a multi-CAD hybrid stack: Revit/Archicad for BIM + GstarCAD/AutoCAD for fast 2D detailing + SOLIDWORKS for custom fabricated hardware.",
        "best_practices": [
            "Align software choices with industry job market demand in your specific geographic territory.",
            "Calculate Total Cost of Ownership (TCO) including software licenses, workstation hardware, and training.",
            "Verify neutral format compatibility (STEP, IFC, DWG) before signing client contracts."
        ],
        "related_concepts": [
            ("cad-career-paths", "CAD Industry Career Roles & Salaries"),
            ("cad-file-management-best-practices", "Multi-CAD File Exchange Standards"),
            ("revit-vs-autocad-which-to-learn", "Revit vs AutoCAD Decision Guide"),
            ("fusion-360-vs-solidworks-which-better", "Fusion 360 vs SOLIDWORKS Matrix")
        ]
    },
    {
        "slug": "cad-career-paths",
        "title": "CAD Career Paths: Roles, Required Skills, Industry Certifications & Salaries",
        "desc": "Complete CAD career roadmap: drafter vs designer vs BIM manager vs CAE simulation specialist roles, software proficiencies, industry certifications, and international salary benchmarks.",
        "software": "Multi-platform",
        "sw_slug": "autocad",
        "quick_answer": "Top CAD careers span: CAD Drafter/Technician (entry: 2D/3D documentation), Design Engineer (mechanical/civil product development), BIM Coordinator/Manager (AEC digital twins & clash detection), and Computational Design Specialist (Grasshopper/Dynamo parametric algorithms). Professional certifications (Autodesk ACP, SOLIDWORKS CSWA/CSWP) boost hiring velocity.",
        "steps": [
            {
                "title": "1. CAD Drafter / Drafting Technician (Entry to Mid Level)",
                "content": "<b>Role</b>: Converting sketches and engineering calculations into clean, standards-compliant 2D shop drawings and 3D models. <b>Core Tools</b>: AutoCAD, GstarCAD, basic SOLIDWORKS or Revit. <b>Typical Salary</b>: $45,000 – $65,000 / year."
            },
            {
                "title": "2. Mechanical Design Engineer / Product Designer (Mid to Senior)",
                "content": "<b>Role</b>: Conceptualizing functional machinery, performing tolerance stack-up analysis, DFM (Design for Manufacturing), and FEA simulation. <b>Core Tools</b>: SOLIDWORKS, Inventor, Creo, NX, GD&T (ASME Y14.5). <b>Typical Salary</b>: $70,000 – $105,000 / year."
            },
            {
                "title": "3. BIM Coordinator & BIM Manager (AEC Specialist)",
                "content": "<b>Role</b>: Managing building information models across disciplines, conducting Navisworks clash detection, maintaining BEP (BIM Execution Plans), and enforcing ISO 19650 standards. <b>Core Tools</b>: Revit, Navisworks, ACC/BIM 360, Solibri, IFC. <b>Typical Salary</b>: $85,000 – $135,000 / year."
            },
            {
                "title": "4. High-Value Industry Certifications",
                "content": "<b>Autodesk Certified Professional (ACP)</b> in AutoCAD, Revit, or Civil 3D. <b>Dassault Systèmes SOLIDWORKS</b> progression: CSWA (Associate), CSWP (Professional), and CSWE (Expert). <b>buildingSMART</b> Professional Certification for openBIM ISO 19650 compliance."
            }
        ],
        "troubleshooting": [
            ("Transitioning from 2D drafting to high-paying BIM or 3D engineering roles", "Build a portfolio featuring 3 complete end-to-end projects: (1) A coordinated multi-discipline BIM building model with sheets and schedules, (2) A complex mechanical assembly with complete GD&T manufacturing drawings, and (3) An automated script (AutoLISP or Dynamo/Python).")
        ],
        "multi_cad_tips": "Engineers who master both 2D DWG production efficiency and 3D parametric BIM/MCAD systems command a 20-30% salary premium in consulting engineering firms.",
        "best_practices": [
            "Build a digital portfolio showcasing clean drawing sheets, GD&T callouts, and parametric assemblies.",
            "Obtain recognized vendor certifications (CSWP, ACP) to validate professional competency.",
            "Learn scripting (AutoLISP, Python, Dynamo) to automate repetitive engineering tasks."
        ],
        "related_concepts": [
            ("how-to-choose-cad-software", "CAD Software Decision Framework"),
            ("construction-documentation", "Professional Drawing Quality Standards"),
            ("bim-workbench", "BIM Management & Coordination"),
            ("autolisp", "CAD Scripting & Automation Skills")
        ]
    },
    {
        "slug": "cad-file-management-best-practices",
        "title": "CAD File Management Best Practices: Folder Structures, Naming & Revision Control",
        "desc": "Enterprise CAD data management guide: standardized project directory trees, ISO 19650 naming conventions, Xref reference mapping, PDM vaults, and 3-2-1 backup strategies.",
        "software": "Multi-platform",
        "sw_slug": "autocad",
        "quick_answer": "Implement a 4-tier project folder structure (/01-Incoming, /02-WIP, /03-Shared, /04-Published/Archive), adopt strict ISO 19650 naming conventions (Project-Discipline-Zone-Level-Type-Role-Number), enforce Relative Paths for all external references, and back up data using the 3-2-1 rule (3 copies, 2 media, 1 offsite).",
        "steps": [
            {
                "title": "1. Standardized 4-Tier Project Folder Structure",
                "content": "Maintain a standardized project skeleton across all servers: <code>/01_INCOMING</code> (vendor/client source files, read-only), <code>/02_WIP_WORKING</code> (live editable engineering files subdivided by discipline), <code>/03_SHARED_COORDINATION</code> (clean background bases and Xrefs), and <code>/04_PUBLISHED_OUTPUT</code> (official issued PDF/DWG packages with revision timestamps)."
            },
            {
                "title": "2. Systematic File Naming Conventions (ISO 19650 / National CAD Standard)",
                "content": "Never name files 'Draft_Final_v2_final.dwg'. Follow a deterministic schema: <code>[ProjectCode]-[Originator]-[Volume/Zone]-[Level]-[DocType]-[Discipline]-[Number]-[Rev]</code>. Example: <code>PRJ101-ARC-BLD01-L02-DR-A-0102-RevB.dwg</code>. Use hyphens, never spaces or special characters."
            },
            {
                "title": "3. Reference File Management & Relative Paths",
                "content": "Always store external references (Xrefs, raster images, point clouds) inside a subfolder relative to host drawings (e.g. <code>.\\Xref\\Arch_Base.dwg</code>). Avoid absolute drive letters (e.g. <code>D:\\Project...</code>) which break when colleagues access files from different network mappings."
            },
            {
                "title": "4. Enterprise PDM Vaults & 3-2-1 Backup Strategy",
                "content": "For multi-user teams, implement Product Data Management (PDM) software (such as SOLIDWORKS PDM, Autodesk Vault, or BIM 360/ACC) for check-in/check-out version locking. For file-based systems, follow the <b>3-2-1 Backup Rule</b>: 3 copies of data, on 2 different media types, with 1 copy stored securely offsite or in cloud backup."
            }
        ],
        "troubleshooting": [
            ("Overwriting colleague's work on shared network drives", "Traditional network folders lack live co-authoring file locks. Implement a check-out protocol or deploy PDM/Vault systems where files are explicitly checked out with ownership badges before editing."),
            ("Missing font or plot style when opening old project archives", "Always package completed drawing milestones using <b>eTransmit</b> in AutoCAD/GstarCAD or <b>Pack and Go</b> in SOLIDWORKS to bundle all fonts, CTB plot styles, Xrefs, and image dependencies into a self-contained archive.")
        ],
        "multi_cad_tips": "Cloud-native CAD tools like Onshape and Autodesk Fusion 360 feature integrated cloud version trees with continuous auto-save and branching, eliminating traditional file loss risks.",
        "best_practices": [
            "Enforce standardized project folder templates (.zip archive) for all new project kick-offs.",
            "Use eTransmit / Pack and Go for all milestone client deliveries and final project archiving.",
            "Conduct automated nightly incremental backups and weekly off-site snapshot backups.",
            "Establish strict file naming conventions and prohibit spaces in filenames."
        ],
        "related_concepts": [
            ("how-to-use-xrefs-autocad", "AutoCAD Xref Path Management & Relative Links"),
            ("solidworks-file-formats", "SOLIDWORKS Pack and Go Workflows"),
            ("construction-documentation", "AEC Drawing Numbering & Revision Systems"),
            ("quality-assurance-cad", "CAD Standards & Audit Compliance")
        ]
    },
    {
        "slug": "cad-collaboration-remote-teams",
        "title": "CAD Collaboration for Remote & Distributed Teams: Cloud PDM, Co-Authoring & Review Tools",
        "desc": "Complete remote CAD collaboration playbook: cloud-native platforms (Onshape, Fusion), BIM collaboration (Autodesk Construction Cloud, BCF), PDM VPN optimization, and async design review.",
        "software": "Multi-platform",
        "sw_slug": "onshape",
        "quick_answer": "Enable effective remote CAD collaboration by choosing the right architecture: Cloud-Native CAD (Onshape / Fusion 360) for real-time concurrent editing, Cloud BIM Hubs (Autodesk Construction Cloud / BIM 360) for multi-firm architectural coordination, or Cloud PDM Vaults (SOLIDWORKS PDM with Web2/VPN) with disciplined check-in/check-out protocols.",
        "steps": [
            {
                "title": "1. Cloud-Native Real-Time Co-Authoring (Onshape & Fusion 360)",
                "content": "Cloud-native CAD runs in browser/cloud environments, allowing multiple engineers to work simultaneously on the same assembly with live cursor presence, instant revision histories, and zero file sync conflicts. Changes update instantly across global engineering teams."
            },
            {
                "title": "2. AEC & BIM Remote Coordination (ACC & OpenBIM BCF)",
                "content": "For Revit and Civil 3D projects, use <b>Autodesk Construction Cloud (ACC)</b> for Cloud Worksharing, allowing architects, structural engineers, and MEP contractors to synchronize local worksets to a central cloud model. Use <b>BIM Collaboration Format (BCF)</b> for open-standard, cross-platform issue tracking across Solibri, Archicad, and Revit."
            },
            {
                "title": "3. Remote PDM Vaults & Network Latency Optimization",
                "content": "When using traditional file-based CAD (SOLIDWORKS, Inventor, AutoCAD) over remote VPNs, never open CAD files directly across a high-latency network share. Use a PDM system with <b>Local Caching</b>: files download to local SSDs during check-out, and only compressed delta changes are uploaded upon check-in."
            },
            {
                "title": "4. Asynchronous Design Review & Markup Protocols",
                "content": "Conduct remote design reviews using lightweight collaborative viewers (eDrawings, Autodesk Viewer, Bluebeam Revu Studio Sessions). Markup vector PDFs with standardized comment statuses (Accepted, Rejected, Completed) and track action items in weekly coordination standups."
            }
        ],
        "troubleshooting": [
            ("Extreme lag and crashing when opening DWG/CAD files over corporate VPN", "Direct Windows SMB file sharing over high-latency VPN connections causes network timeouts. Switch to a PDM local caching vault or use remote desktop streaming (HP Anyware, Parsec for Teams, or Azure Virtual Desktop)."),
            ("Version collision when two remote drafters edit the same DWG file", "Break master drawings into separate Xref modules by zone/floor, or utilize cloud check-out locking to ensure only one author has write permission at any given time.")
        ],
        "multi_cad_tips": "Modern collaborative web viewers support over 60+ CAD file formats (DWG, RVT, STEP, SLDASM, IFC), allowing non-CAD stakeholders and project managers to inspect 3D models and measure dimensions without installing heavy CAD desktop software.",
        "best_practices": [
            "Never open live CAD files directly across remote VPN network drives without a local caching PDM client.",
            "Adopt BCF (BIM Collaboration Format) for structured clash issue management between disciplines.",
            "Use cloud-based markup tools (Bluebeam Studio / Autodesk Viewer) for clear asynchronous design reviews."
        ],
        "related_concepts": [
            ("cad-file-management-best-practices", "CAD Data Governance & Folder Schemes"),
            ("how-to-use-xrefs-autocad", "Xref Modular Drawing Strategy"),
            ("bim-workbench", "BIM Cloud Worksharing & Coordination"),
            ("quality-assurance-cad", "Design Review & Audit Protocols")
        ]
    },
    {
        "slug": "autocad-vs-autocad-lt",
        "title": "AutoCAD vs AutoCAD LT: Feature Comparison, 3D, LISP Scripting & Value Analysis",
        "desc": "Detailed comparison of full AutoCAD vs AutoCAD LT: 3D solid modeling, AutoLISP scripting, specialized toolsets, network licensing, pricing, and alternative DWG platforms.",
        "software": "AutoCAD",
        "sw_slug": "autocad",
        "quick_answer": "AutoCAD LT is restricted to 2D drafting and annotation with limited scripting. Full AutoCAD includes 3D modeling and rendering, full AutoLISP/VBA/.NET API programming, specialized industry toolsets (Architecture, MEP, Electrical, Mechanical), and action recording. If you need 3D or custom LISP automations, full AutoCAD or perpetual alternatives (GstarCAD) are essential.",
        "steps": [
            {
                "title": "1. 2D Drafting vs. 3D Solid Modeling",
                "content": "<b>AutoCAD LT</b> provides complete 2D drawing, editing, dimensioning, and plotting capabilities identical to full AutoCAD. However, LT contains zero 3D modeling tools—no 3D solid primitives (Box, Cylinder), no Boolean operations (Union, Subtract), no 3D orbit, and no photorealistic rendering."
            },
            {
                "title": "2. Programming & Customization APIs (AutoLISP, .NET, ARX)",
                "content": "Full AutoCAD supports <b>AutoLISP</b>, <b>Visual LISP</b>, <b>VBA</b>, <b>.NET (C#/VB)</b>, and <b>ObjectARX (C++)</b> for building enterprise custom commands and automated workflows. AutoCAD LT recently added basic AutoLISP support, but lacks ARX, .NET, and advanced API capabilities required for third-party industry plugins."
            },
            {
                "title": "3. Specialized Toolsets Included with Full AutoCAD",
                "content": "Since Autodesk consolidated AutoCAD subscriptions, full AutoCAD licenses include 7 specialized industry toolsets: <b>Architecture</b>, <b>Mechanical</b>, <b>Electrical</b>, <b>MEP</b>, <b>Plant 3D</b>, <b>Map 3D</b>, and <b>Raster Design</b>. AutoCAD LT does not include any specialized toolsets."
            },
            {
                "title": "4. Pricing & High-Value Alternatives (GstarCAD / BricsCAD)",
                "content": "AutoCAD costs ~$1,975/year, while AutoCAD LT costs ~$505/year. For firms needing full 2D+3D+AutoLISP capabilities without steep annual subscription fees, alternative DWG platforms like <b>GstarCAD</b> and <b>BricsCAD</b> provide perpetual licenses with full DWG and LISP compatibility at a fraction of the cost."
            }
        ],
        "troubleshooting": [
            ("Opening a 3D DWG file in AutoCAD LT", "AutoCAD LT can view existing 3D wireframes and shaded models in read-only projection, but users cannot edit 3D solid geometry, push/pull faces, or perform Boolean operations without full AutoCAD.")
        ],
        "multi_cad_tips": "GstarCAD Professional includes full 2D drafting, 3D ACIS solid modeling, AutoLISP/GRX APIs, and dynamic blocks under a perpetual license, serving as a powerful drop-in replacement for both AutoCAD LT and full AutoCAD.",
        "best_practices": [
            "Choose AutoCAD LT only if your scope is strictly 2D drafting with no third-party plugin requirements.",
            "Choose full AutoCAD or GstarCAD if your workflow relies on custom AutoLISP scripts or 3D solid operations.",
            "Calculate multi-year ROI comparing annual subscription software against perpetual license options."
        ],
        "related_concepts": [
            ("how-to-migrate-autocad-to-gstarcad", "AutoCAD to GstarCAD Migration Guide"),
            ("autolisp", "AutoLISP Scripting & Productivity Tools"),
            ("how-to-choose-cad-software", "CAD Software Selection Framework"),
            ("cad-career-paths", "CAD Drafter vs Design Engineer Tools")
        ]
    },
    {
        "slug": "revit-vs-autocad-which-to-learn",
        "title": "Revit vs AutoCAD for Architecture & Construction: BIM vs 2D Drafting Career Guide",
        "desc": "In-depth guide comparing Revit (BIM) and AutoCAD (2D/3D CAD) for architects and engineers: drawing vs modeling workflows, parametric schedules, learning curve, and job market demand.",
        "software": "Revit",
        "sw_slug": "revit",
        "quick_answer": "AutoCAD is a generic 2D/3D drafting tool based on lines, arcs, and text—ideal for details, schematic layouts, civil site plans, and shop drawings. Revit is an intelligent Building Information Modeling (BIM) platform where you assemble real-world parametric objects (walls, doors, ductwork) that automatically generate coordinated plans, sections, elevations, and quantity schedules.",
        "steps": [
            {
                "title": "1. Core Philosophy: Drawing Lines vs. Building Digital Twins",
                "content": "In <b>AutoCAD</b>, you draw 2D vector lines that represent walls. If you move a wall in a floor plan, you must manually update the corresponding section, elevation, and door schedule. In <b>Revit</b>, you place an intelligent 3D Wall element; moving it in floor plan automatically updates all elevations, sections, 3D views, and material takeoffs simultaneously."
            },
            {
                "title": "2. Coordination & Multi-Discipline Clash Detection",
                "content": "Revit integrates architectural, structural, and MEP engineering in a single parametric environment. Clashes (such as an HVAC duct intersecting a steel beam) are identified immediately in 3D, preventing expensive rework during site construction. AutoCAD requires manual Xref overlay comparisons."
            },
            {
                "title": "3. Learning Curve & Productivity Progression",
                "content": "AutoCAD has a gentle initial learning curve (master basic drawing commands in 2-3 weeks). Revit has a steeper initial learning curve (learning BIM concepts, family creation, view templates, and parameters takes 2-3 months), but delivers 3x to 5x higher documentation productivity on large building projects once mastered."
            },
            {
                "title": "4. Industry Demand & Career Value",
                "content": "BIM mandates (ISO 19650) in government and commercial construction make <b>Revit</b> skills mandatory for modern architecture, structural engineering, and MEP consulting firms. <b>AutoCAD</b> remains an essential baseline tool for 2D detailing, renovation as-builts, civil site planning, and manufacturing fabrication."
            }
        ],
        "troubleshooting": [
            ("Should architecture students learn AutoCAD or Revit first?", "Learn both: start with AutoCAD for 2-3 weeks to understand technical drafting fundamentals, coordinate geometry, and layer standards; then transition to Revit as your primary design and BIM portfolio tool.")
        ],
        "multi_cad_tips": "A standard architectural workflow is hybrid: master building models and floor plans are created in Revit, and legacy manufacturer details or municipal site plans are linked as 2D DWGs.",
        "best_practices": [
            "Master Revit if your target career is Architectural Design, Structural Engineering, or BIM Management.",
            "Maintain AutoCAD proficiency for 2D detail libraries, DWG consultant coordination, and civil site plans.",
            "Build a portfolio highlighting coordinated multi-view Revit BIM projects with live schedules."
        ],
        "related_concepts": [
            ("how-to-create-family-revit", "Revit Parametric Family Creation Guide"),
            ("how-to-create-sheets-revit", "Revit Sheet Composition & Documentation"),
            ("bim-workbench", "BIM Standards & Level of Development (LOD)"),
            ("cad-career-paths", "AEC & BIM Coordinator Career Roadmap")
        ]
    }
]

def generate_faq_page(faq):
    f = faq
    canonical = f"https://gstarcademy.com/kb/faq/{f['slug']}"
    
    # 1. Quick Answer Card
    quick_answer_html = f'''
    <div style="margin-bottom: 28px; padding: 22px 24px; background: var(--ink-surface-2, #f5f6f8); border-left: 4px solid var(--accent, #0066cc); border-radius: 8px;">
      <h2 style="margin: 0 0 10px; font-size: 1.05rem; font-weight: 700; color: var(--ink-text);">⚡ Quick Answer / Key Takeaway</h2>
      <p style="margin: 0; font-size: 15px; line-height: 1.7; color: var(--ink-text);">{f['quick_answer']}</p>
    </div>'''
    
    # 2. Detailed Step-by-Step Instructions
    steps_html = ""
    for idx, s in enumerate(f['steps'], 1):
        steps_html += f'''
        <div style="margin-bottom: 24px; padding: 20px; background: var(--ink-surface); border: 1px solid var(--ink-line); border-radius: 12px;">
          <h3 style="margin: 0 0 12px; font-size: 1.0rem; font-weight: 700; color: var(--ink-text);">{s['title']}</h3>
          <p style="margin: 0; font-size: 14.5px; line-height: 1.75; color: var(--ink-text);">{s['content']}</p>
        </div>'''
    
    # 3. Troubleshooting & Failure Scenarios Table
    trouble_html = ""
    if "troubleshooting" in f and f["troubleshooting"]:
        rows = ""
        for issue, fix in f["troubleshooting"]:
            rows += f'''
            <tr style="border-bottom: 1px solid var(--ink-line);">
              <td style="padding: 12px 16px; font-weight: 600; vertical-align: top; color: var(--ink-text); width: 35%;">{issue}</td>
              <td style="padding: 12px 16px; vertical-align: top; color: var(--ink-text); line-height: 1.6;">{fix}</td>
            </tr>'''
        trouble_html = f'''
        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Common Issues &amp; Troubleshooting Guide</h2>
          <div style="overflow-x: auto; margin-top: 16px;">
            <table style="width: 100%; border-collapse: collapse; background: var(--ink-surface); border: 1px solid var(--ink-line); border-radius: 8px; font-size: 14px;">
              <thead>
                <tr style="background: var(--ink-surface-2); border-bottom: 2px solid var(--ink-line); text-align: left;">
                  <th style="padding: 12px 16px; font-weight: 700;">Common Failure / Problem</th>
                  <th style="padding: 12px 16px; font-weight: 700;">Root Cause &amp; Recommended Solution</th>
                </tr>
              </thead>
              <tbody>
                {rows}
              </tbody>
            </table>
          </div>
        </section>'''

    # 4. Multi-CAD Tips
    multi_cad_html = ""
    if "multi_cad_tips" in f and f["multi_cad_tips"]:
        multi_cad_html = f'''
        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Cross-CAD Compatibility &amp; Alternatives</h2>
          <p style="font-size: 14.5px; line-height: 1.75; color: var(--ink-text);">{f['multi_cad_tips']}</p>
        </section>'''

    # 5. Best Practices Checklist
    bp_html = ""
    if "best_practices" in f and f["best_practices"]:
        bp_items = "".join([f'<li style="margin-bottom: 10px; line-height: 1.6;">{bp}</li>' for bp in f["best_practices"]])
        bp_html = f'''
        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Engineering Best Practices Checklist</h2>
          <ul style="padding-left: 20px; font-size: 14.5px; color: var(--ink-text);">
            {bp_items}
          </ul>
        </section>'''

    # 6. Related Concepts
    rel_html = ""
    if "related_concepts" in f and f["related_concepts"]:
        rel_links = ""
        for cslug, ctitle in f["related_concepts"]:
            rel_links += f'<li style="margin-bottom: 8px;"><a href="../concepts/{cslug}" style="color: var(--accent); font-weight: 600;">{ctitle}</a></li>'
        rel_html = f'''
        <section class="kb-concept-section" style="margin-top: 36px;">
          <h2>Related Concepts &amp; Further Learning</h2>
          <ul style="list-style: none; padding: 0; font-size: 14.5px;">
            {rel_links}
          </ul>
        </section>'''

    # JSON-LD Schema
    schema_qa = [f'{{"@type":"Question","name":"{f["title"]}","acceptedAnswer":{{"@type":"Answer","text":"{f["quick_answer"][:500]}"}}}}']
    for s in f["steps"]:
        schema_qa.append(f'{{"@type":"Question","name":"{s["title"]}","acceptedAnswer":{{"@type":"Answer","text":"{s["content"][:400]}"}}}}')
    faq_schema = ",".join(schema_qa)

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
    <title>{f['title']} | Gstarcademy</title>
    <meta name="description" content="{f['desc']}" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <link rel="canonical" href="{canonical}" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{f['title']}" />
    <meta property="og:description" content="{f['desc']}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:site_name" content="Gstarcademy" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="preload" href="../../styles.min.css" as="style" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />
    <link rel="stylesheet" href="../../styles.min.css" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_schema}]}}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://gstarcademy.com/"}},{{"@type":"ListItem","position":2,"name":"Knowledge Base","item":"https://gstarcademy.com/knowledge-base"}},{{"@type":"ListItem","position":3,"name":"FAQ","item":"https://gstarcademy.com/kb/faq/"}},{{"@type":"ListItem","position":4,"name":"{f['title']}","item":"{canonical}"}}]}}</script>
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
        <a href="./" style="color: var(--ink-text-soft);">FAQ</a> /
        <span aria-current="page" style="color: var(--ink-text);">{f['software']}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 28px;">
          <span class="chip pill-warn">How-To &amp; FAQ &middot; {f['software']}</span>
          <h1 style="margin-top: 12px; font-size: 2.1rem; line-height: 1.25;">{f['title']}</h1>
          <p class="hero-sub" style="font-size: 16px; line-height: 1.6; color: var(--ink-text-soft);">{f['desc']}</p>
        </header>

        <div class="ink-byline" role="contentinfo" style="margin-bottom: 24px; font-size: 13px; color: var(--ink-text-soft); display: flex; gap: 16px; border-bottom: 1px solid var(--ink-line); padding-bottom: 12px;">
          <span><strong>Author:</strong> Gstarcademy Engineering Editorial Board</span>
          <span><strong>Updated:</strong> <time datetime="{TODAY}">{TODAY}</time></span>
        </div>

        {quick_answer_html}

        <section class="kb-concept-section">
          <h2>Step-by-Step Instructions &amp; Commands</h2>
          {steps_html}
        </section>

        {trouble_html}
        {multi_cad_html}
        {bp_html}
        {rel_html}

        <aside style="margin-top: 48px; padding: 20px 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 14px;">
          <p style="font-size: 13px; font-weight: 700; margin: 0 0 6px; color: var(--ink-text);">Gstarcademy Technical Review Committee</p>
          <p style="font-size: 12px; color: var(--ink-text-soft); margin: 0; line-height: 1.5;">This technical answer was authored and verified by CAD application engineers. Content is updated regularly to align with modern AutoCAD, GstarCAD, SOLIDWORKS, Revit, and Fusion 360 releases.</p>
        </aside>
      </article>
    </main>

    <footer class="footer site-footer" style="margin-top: 60px;">
      <div class="container site-footer-inner">
        <div class="site-footer-brand"><p class="site-footer-tagline">Gstarcademy</p><p class="site-footer-desc">CAD Knowledge Base &amp; Tutorial Hub for Architecture, Engineering, and Manufacturing professionals.</p></div>
      </div>
      <div class="container site-footer-bottom"><p>&copy; <span id="footer-year"></span> Gstarcademy. All rights reserved.</p></div>
    </footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    return html


def generate_index():
    by_sw = {}
    for f in FAQS:
        sw = f["software"]
        if sw not in by_sw:
            by_sw[sw] = []
        by_sw[sw].append(f)
    
    links = ""
    for sw, faqs in sorted(by_sw.items()):
        links += f'<div style="margin-bottom: 28px; padding: 20px; background: var(--ink-surface); border: 1px solid var(--ink-line); border-radius: 12px;">\n'
        links += f'<h2 style="margin: 0 0 14px; font-size: 1.25rem; color: var(--ink-text);">{sw} Technical Guides</h2>\n<ul style="list-style: none; padding: 0; margin: 0;">\n'
        for f in faqs:
            links += f'<li style="margin-bottom: 10px;"><a href="./{f["slug"]}" style="color: var(--accent); font-weight: 600; text-decoration: none;">{f["title"]}</a><p style="margin: 4px 0 0; font-size: 13px; color: var(--ink-text-soft);">{f["desc"]}</p></li>\n'
        links += '</ul></div>\n'
    
    html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CAD Technical FAQ &amp; How-To Guides | Gstarcademy</title>
    <meta name="description" content="In-depth technical answers and step-by-step CAD tutorials: AutoCAD, SOLIDWORKS, Revit, Fusion 360, GstarCAD, Civil 3D, and Blender." />
    <link rel="canonical" href="https://gstarcademy.com/kb/faq/" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="stylesheet" href="../../styles.min.css" />
  </head>
  <body>
    <div class="page-shell"><header class="topbar"><div class="container topbar-inner"><a class="brand" href="../../"><span class="brand-badge">GC</span><span>Gstarcademy</span></a><nav class="nav"><a class="nav-link" href="../../">Home</a><a class="nav-link active" href="../../knowledge-base">Wiki</a><a class="nav-link" href="../../tutorials">Tutorials</a><a class="nav-link" href="../../news">News</a><a class="nav-link" href="../../about">About</a></nav></div></header></div>
    <main class="container" style="margin-top: 32px; max-width: 920px;">
      <header style="margin-bottom: 32px;">
        <span class="chip pill-warn">Knowledge Base &middot; Q&amp;A</span>
        <h1 style="margin-top: 12px; font-size: 2.2rem;">CAD Technical FAQ &amp; Practical Guides</h1>
        <p style="color: var(--ink-text-soft); font-size: 16px; line-height: 1.6;">Comprehensive troubleshooting guides and step-by-step instructions for engineering and architecture software.</p>
      </header>
      {links}
    </main>
    <footer class="footer site-footer"><div class="container site-footer-bottom"><p>&copy; Gstarcademy. All rights reserved.</p></div></footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    print(f"Generating {len(FAQS)} comprehensive FAQ pages...")
    for f in FAQS:
        html = generate_faq_page(f)
        filepath = os.path.join(OUTPUT_DIR, f"{f['slug']}.html")
        with open(filepath, 'w', encoding='utf-8') as fp:
            fp.write(html)
    generate_index()
    print(f"Successfully generated {len(FAQS)} in-depth FAQ pages + index.html")


if __name__ == '__main__':
    main()
