#!/usr/bin/env python3
"""
Generate FAQ pages for common CAD questions — targets "how to X in [Software]" searches.
"""

import os
from datetime import date

TODAY = date.today().isoformat()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'faq')
os.makedirs(OUTPUT_DIR, exist_ok=True)

FAQS = [
    # AutoCAD FAQs
    {"slug": "how-to-scale-in-autocad", "title": "How to Scale Objects in AutoCAD", "desc": "Step-by-step guide to scaling objects in AutoCAD using SCALE command, reference scaling, and viewport scale settings.", "software": "AutoCAD", "sw_slug": "autocad",
     "questions": [("How do I scale an object in AutoCAD?", "Use the SCALE command (SC shortcut): select objects, pick a base point, then enter a scale factor (2 = double size, 0.5 = half). For reference scaling, use the Reference option to specify a known dimension and its desired new size."), ("How do I set the drawing scale in AutoCAD?", "Drawing scale is set per viewport in paper space. Double-click inside a viewport, zoom to fit, then set the VP scale from the status bar dropdown (1:100, 1:50, etc.). Lock the viewport to prevent accidental changes."), ("Why are my dimensions wrong after scaling?", "If you scale annotative objects, their size changes relative to paper space. Use annotative dimensions with the correct annotation scale to maintain proper text height regardless of viewport scale.")]},
    {"slug": "how-to-print-autocad", "title": "How to Print/Plot in AutoCAD", "desc": "Complete guide to plotting in AutoCAD: page setup, plot styles (CTB/STB), PDF output, and batch plotting multiple layouts.", "software": "AutoCAD", "sw_slug": "autocad",
     "questions": [("How do I print to PDF in AutoCAD?", "Use PLOT command > select DWG to PDF.pc3 as the printer > choose paper size > set plot area (Layout or Window) > select plot style table > Preview > OK. For multi-sheet PDFs, use PUBLISH command."), ("What is the difference between CTB and STB plot styles?", "CTB (Color Table Based) maps line appearance by color number — all red objects print the same. STB (Style Table Based) assigns plot styles by name independent of color. STB is more flexible for complex projects; CTB is simpler for small teams."), ("How do I batch plot multiple drawings?", "Use PUBLISH command or Sheet Set Manager. PUBLISH lets you add multiple DWG files and their layouts to a batch list, then plot all at once to DWF, PDF, or paper. Sheet Set Manager automates this for organized projects.")]},
    {"slug": "how-to-create-blocks-autocad", "title": "How to Create and Use Blocks in AutoCAD", "desc": "Complete guide to AutoCAD blocks: creation, insertion, attributes, dynamic blocks, and block libraries for reusable content.", "software": "AutoCAD", "sw_slug": "autocad",
     "questions": [("How do I create a block in AutoCAD?", "Use BLOCK command (B shortcut): name the block, select objects, pick an insertion base point, and choose whether to convert/retain/delete the original objects. The block is stored in the current drawing. Use WBLOCK to save as a separate .dwg file for use in other drawings."), ("How do I add attributes to a block?", "Before creating the block, use ATTDEF to place attribute definitions (tag, prompt, default value) alongside the geometry. When you create the block including these ATTDEF objects, they become fillable fields on insertion. Use EATTEXT or DATAEXTRACTION to export attribute data to tables."), ("What are dynamic blocks?", "Dynamic blocks contain parameters (distances, angles, flip states) and actions (stretch, rotate, array) that let users modify instances without exploding. Created in the Block Editor (BEDIT), they reduce library size dramatically — one dynamic door block replaces 50 fixed-size blocks.")]},
    {"slug": "how-to-use-xrefs-autocad", "title": "How to Use External References (Xrefs) in AutoCAD", "desc": "Guide to AutoCAD Xrefs: attaching, overlaying, clipping, managing paths, and resolving common Xref issues.", "software": "AutoCAD", "sw_slug": "autocad",
     "questions": [("What is an Xref in AutoCAD?", "An External Reference (Xref) is another DWG file displayed inside your current drawing without increasing file size. Changes to the source file update automatically. Use Xrefs for site plans, backgrounds, title blocks, and multi-discipline coordination."), ("Attach vs Overlay — what's the difference?", "Attach: the xref appears in any drawing that references YOUR drawing (nested). Overlay: the xref only appears in the current drawing, not when your drawing is itself xref'd elsewhere. Use Overlay for consultant drawings to avoid circular references."), ("How do I fix 'Xref not found' errors?", "Open the External References palette (XREF command). Unresolved xrefs show a broken path. Right-click > Select New Path > navigate to the file. Use relative paths (./subfolder/file.dwg) for project portability, or set PROJECTNAME and search paths for team environments.")]},
    {"slug": "autocad-keyboard-shortcuts", "title": "AutoCAD Keyboard Shortcuts & Command Aliases", "desc": "Essential AutoCAD keyboard shortcuts and command aliases for faster drafting: navigation, drawing, editing, and annotation shortcuts.", "software": "AutoCAD", "sw_slug": "autocad",
     "questions": [("What are the most important AutoCAD shortcuts?", "Essential aliases: L (Line), C (Circle), REC (Rectangle), TR (Trim), EX (Extend), O (Offset), M (Move), CO (Copy), RO (Rotate), MI (Mirror), SC (Scale), E (Erase), Z (Zoom), P (Pan), DI (Distance), AR (Array), H (Hatch), DIM (Dimension)."), ("How do I customize command aliases?", "Edit the acad.pgp file (ALIASEDIT command or Express Tools > ALIASEDIT). Add entries like: ZZ, *ZOOM or FF, *FILLET. Restart AutoCAD for changes to take effect. Back up your custom PGP file for use across machines."), ("What function keys do in AutoCAD?", "F1: Help, F2: Text window, F3: OSNAP toggle, F5: Isoplane cycle, F7: Grid, F8: Ortho, F9: Snap, F10: Polar tracking, F11: Object snap tracking, F12: Dynamic input. F3 and F8 are the most frequently toggled during drafting.")]},

    # SOLIDWORKS FAQs
    {"slug": "how-to-create-assembly-solidworks", "title": "How to Create an Assembly in SOLIDWORKS", "desc": "Step-by-step guide to creating SOLIDWORKS assemblies: inserting components, applying mates, and managing assembly structure.", "software": "SOLIDWORKS", "sw_slug": "solidworks",
     "questions": [("How do I start a new assembly?", "File > New > Assembly. Insert the first component (base/fixture part) — it's automatically fixed in place. Then Insert Components for additional parts. Use mates to constrain their relative positions and degrees of freedom."), ("What mates should I use?", "Standard mates: Coincident (faces/planes touching), Concentric (aligned cylinders), Distance (specific gap), Parallel, Perpendicular, Tangent. Advanced: Width (center between faces), Path (follow a curve), Profile Center. Mechanical: Gear, Rack-Pinion, Cam."), ("How do I fix 'over-defined' assembly errors?", "Over-defined means conflicting mates — the component can't satisfy all constraints simultaneously. Right-click the component > View Mates to see which mates conflict. Delete or suppress the redundant mate. Use MateXpert for diagnosis.")]},
    {"slug": "how-to-create-drawing-solidworks", "title": "How to Create Drawings in SOLIDWORKS", "desc": "Guide to SOLIDWORKS drawings: creating views, adding dimensions, annotations, BOM tables, and preparing for manufacturing.", "software": "SOLIDWORKS", "sw_slug": "solidworks",
     "questions": [("How do I create a drawing from a part?", "File > Make Drawing From Part/Assembly. Choose a template (A3, A4, etc.). Drag standard views (Front, Top, Right) from the View Palette, or use Insert > Drawing View > Standard 3 View. Add detail views, section views, and isometric views as needed."), ("How do I add dimensions to a drawing?", "Use Insert > Model Items to import dimensions from the 3D model (driven dimensions). For additional annotation, use Smart Dimension (sketch dimensions), or Insert > Annotations for GD&T, surface finish, weld symbols, and notes."), ("How do I add a BOM to an assembly drawing?", "Insert > Tables > Bill of Materials. Select the assembly view. Choose BOM type (Top-level, Indented, Parts-only). Configure columns (part number, description, quantity, material). Balloon the view with Insert > Annotations > Auto Balloon.")]},
    {"slug": "solidworks-file-formats", "title": "SOLIDWORKS File Formats Explained", "desc": "Guide to SOLIDWORKS file types: SLDPRT, SLDASM, SLDDRW, eDrawings, and export formats (STEP, IGES, STL, PDF).", "software": "SOLIDWORKS", "sw_slug": "solidworks",
     "questions": [("What are the main SOLIDWORKS file types?", "SLDPRT = Part file (single component), SLDASM = Assembly file (multiple parts constrained together), SLDDRW = Drawing file (2D documentation). Supporting: SLDDRT (drawing template), SLDLFP (library feature part), SLDPRT (sheet format)."), ("What format should I use for 3D printing?", "Export as STL (tessellated mesh) for FDM/SLA printers, or 3MF (newer, includes color/material info). Set resolution appropriately — Coarse for quick checks, Fine for production. Check for non-manifold geometry before export."), ("What format for sharing with non-SOLIDWORKS users?", "STEP (.stp) is the universal choice for 3D data exchange. Use AP214 for visual properties. For viewing-only, eDrawings (.eprt/.easm) is free to view. For 2D drawings, export to PDF with embedded 3D (File > Save As > PDF with 3D option).")]},

    # Revit FAQs
    {"slug": "how-to-create-family-revit", "title": "How to Create Custom Families in Revit", "desc": "Guide to creating parametric Revit families: templates, reference planes, parameters, types, and best practices.", "software": "Revit", "sw_slug": "revit",
     "questions": [("How do I start creating a family?", "File > New > Family. Choose the appropriate template: Generic Model, Door, Window, Furniture, etc. The template determines the family category, which controls visibility, scheduling, and behavior. Start with reference planes to define the parametric skeleton."), ("How do parameters work in families?", "Parameters drive dimensions and properties. Instance parameters vary per-placed-element (e.g., a specific door's fire rating). Type parameters are shared across all instances of the same type (e.g., standard door width). Create parameters in Family Types dialog and associate them with dimensions/constraints."), ("What makes a good Revit family?", "Good families: use reference planes for all geometry control, have clear parameter naming, flex correctly when parameters change, include correct connectors (MEP), are the right category, and have appropriate detail levels (coarse/medium/fine).")]},
    {"slug": "how-to-create-sheets-revit", "title": "How to Create Sheets & Manage Views in Revit", "desc": "Guide to Revit documentation: creating sheets, placing views, title blocks, sheet lists, and drawing management.", "software": "Revit", "sw_slug": "revit",
     "questions": [("How do I create a sheet in Revit?", "View > Sheet > New Sheet. Select a title block family. Then drag views from the Project Browser onto the sheet. Views can only be placed on one sheet — if already placed, you'll see (Sheet: A101) next to the view name."), ("How do I organize sheet numbering?", "Right-click the sheet > Properties > Sheet Number. Follow your firm's numbering convention (e.g., A-101 for architecture, S-101 for structural). Use the Sheet Issues/Revisions tool for revision tracking and clouding."), ("How do I create a sheet list/index?", "View > Schedules > Sheet List. This auto-generates a table of all sheets with number, name, and revision info. Place it on a cover sheet. Filter and sort columns to match your project requirements.")]},

    # Fusion 360 FAQs
    {"slug": "how-to-export-stl-fusion-360", "title": "How to Export STL from Fusion 360 for 3D Printing", "desc": "Step-by-step guide to exporting STL files from Fusion 360 with optimal settings for FDM, SLA, and SLS 3D printing.", "software": "Fusion 360", "sw_slug": "fusion-360",
     "questions": [("How do I export an STL in Fusion 360?", "Right-click the body/component in the browser > Save As STL (or File > 3D Print). Set refinement: Low (fast, rough), Medium (balanced), High (smooth, larger file). Choose unit (mm recommended). Click OK and save to your desired location."), ("What settings for FDM vs SLA printing?", "FDM: Medium refinement is usually sufficient since layer lines dominate surface quality. SLA: Use High refinement — the printer can reproduce fine mesh detail. For both: ensure your model is watertight (no open surfaces or non-manifold edges)."), ("How do I fix non-manifold errors?", "In Fusion 360, run Inspect > Section Analysis to check for gaps. Use Repair Body (Mesh workspace) for imported meshes. For native bodies, ensure all surfaces form a closed solid — check the body icon shows 'Solid Body' not 'Surface Body' in the browser.")]},
    {"slug": "fusion-360-vs-solidworks-which-better", "title": "Fusion 360 vs SOLIDWORKS — Which Should You Learn?", "desc": "Detailed comparison of Fusion 360 and SOLIDWORKS for students, hobbyists, and professionals choosing their first MCAD platform.", "software": "Fusion 360", "sw_slug": "fusion-360",
     "questions": [("Which is better for beginners?", "Fusion 360 has a lower entry barrier: free for personal use, cloud-based (no install), integrated CAD/CAM/CAE. SOLIDWORKS has a steeper learning curve but is the industry standard for mechanical engineering jobs. Learn Fusion 360 to start quickly; learn SOLIDWORKS if you're targeting manufacturing employment."), ("Can I switch between them later?", "Yes. Core parametric modeling concepts (sketch constraints, features, assemblies) are transferable. The workflow and UI differ, but an experienced Fusion user can become productive in SOLIDWORKS within 2-4 weeks, and vice versa. STEP files transfer geometry between them."), ("Which has better job prospects?", "SOLIDWORKS dominates manufacturing job listings (5-10x more openings than Fusion 360 specifically). However, Fusion 360 skills are increasingly valued at startups, hardware companies, and design consultancies. Learning both maximizes employability.")]},

    # GstarCAD FAQs  
    {"slug": "how-to-migrate-autocad-to-gstarcad", "title": "How to Migrate from AutoCAD to GstarCAD", "desc": "Step-by-step migration guide from AutoCAD to GstarCAD: DWG compatibility, command mapping, LISP migration, and customization transfer.", "software": "GstarCAD", "sw_slug": "gstarcad",
     "questions": [("Can GstarCAD open AutoCAD files?", "Yes, GstarCAD natively reads and writes DWG/DXF files (all versions from R2.5 to latest). No conversion needed — open AutoCAD files directly. Fonts, linetypes, blocks, and xrefs transfer seamlessly. SHX fonts and CTB/STB plot styles are also compatible."), ("Do AutoCAD LISP routines work in GstarCAD?", "Most AutoLISP/Visual LISP routines run without modification in GstarCAD. Complex LISP using undocumented AutoCAD internal functions may need minor adjustment. Test your critical routines before deploying; GstarCAD provides LISP debugging tools for troubleshooting."), ("How much does switching save?", "GstarCAD offers perpetual licenses at roughly 1/3 to 1/5 of AutoCAD's annual subscription cost. For a 10-seat firm, switching can save $15,000-25,000/year while maintaining DWG workflow continuity. Multi-year ROI is significant for firms not using AutoCAD-exclusive vertical tools.")]},
    {"slug": "gstarcad-system-requirements", "title": "GstarCAD System Requirements & Performance Tips", "desc": "GstarCAD hardware requirements, performance optimization settings, and tips for handling large DWG files efficiently.", "software": "GstarCAD", "sw_slug": "gstarcad",
     "questions": [("What are GstarCAD's minimum system requirements?", "Minimum: Windows 7/10/11, 2GB RAM, 2GB disk, 1024x768 display. Recommended: 8GB+ RAM, SSD storage, dedicated GPU (OpenGL 3.3+). GstarCAD is notably lighter than AutoCAD — it runs well on hardware that AutoCAD struggles with."), ("How to speed up large file handling?", "Enable hardware acceleration (GRAPHICSCONFIG), use layer freezing for unused content, set SELECTIONPREVIEW to 0 for complex selections, reduce VIEWRES for initial display, and use PURGE regularly to remove unused objects bloating memory."), ("Does it support multi-monitor setups?", "Yes, GstarCAD supports multi-monitor workflows. Drag toolbars, palettes, and command line to secondary monitors. Use WSCURRENT to save and restore workspace configurations for different monitor arrangements.")]},

    # Civil 3D FAQs
    {"slug": "how-to-create-surface-civil-3d", "title": "How to Create a Surface in Civil 3D", "desc": "Guide to creating TIN surfaces in Civil 3D from points, contours, DEM files, and survey data with proper boundary and breakline configuration.", "software": "Civil 3D", "sw_slug": "civil-3d",
     "questions": [("How do I create a surface from survey points?", "Prospector > Surfaces > right-click > Create Surface. Choose TIN type, name it (e.g., 'EG - Existing Ground'). Under the surface, expand Definition > Point Groups > right-click > Add. Select your survey point group. The surface triangulates automatically."), ("How do I add breaklines?", "Breaklines force the TIN to follow known linear features (road edges, ditches, retaining walls). Under Definition > Breaklines > right-click > Add. Select polylines representing the features. Choose Standard or Wall type depending on whether there's a vertical face."), ("How do I set surface boundaries?", "Under Definition > Boundaries > right-click > Add. Select a closed polyline defining the surface extent. Choose Outer (clips everything outside), Hide (hides inside), or Show (shows only inside). Boundaries prevent triangulation across voids and define the surface edge.")]},
    {"slug": "how-to-create-alignment-civil-3d", "title": "How to Create an Alignment in Civil 3D", "desc": "Guide to creating horizontal alignments in Civil 3D: tangent-curve geometry, design criteria, and alignment labels.", "software": "Civil 3D", "sw_slug": "civil-3d",
     "questions": [("How do I create a road centerline alignment?", "Home tab > Create Alignment > From Objects (convert existing polyline) or Create Design Alignment. For design alignments, use the Alignment Layout Tools toolbar to place tangent lines and then insert curves (Free/Fixed/Floating) between them."), ("How do I set design speeds and standards?", "In alignment properties > Design Criteria tab, select a design criteria file (AASHTO, country-specific). Set the design speed. Civil 3D then validates your horizontal curves against minimum radius and superelevation requirements, flagging violations."), ("How do I add stations and labels?", "Alignments have automatic stationing. Add labels: select alignment > right-click > Edit Alignment Labels. Add Major/Minor Station labels, Geometry Point labels (PC, PT, PI), and Station Equation labels as needed.")]},

    # Blender FAQs
    {"slug": "blender-for-cad-users", "title": "Blender for CAD Users — Key Differences & Tips", "desc": "Guide for CAD professionals learning Blender: navigation differences, precision tools, unit setup, and CAD-to-Blender workflow.", "software": "Blender", "sw_slug": "blender",
     "questions": [("How is Blender different from CAD software?", "Blender is a polygonal/SubD modeler, not parametric. There's no feature history tree — edits are destructive. Precision comes from typed input (G then X then 10 = move 10 units in X) rather than constraint-driven sketches. Blender excels at organic/visual work; CAD excels at engineering precision."), ("How do I set up precise measurements?", "Edit > Preferences > Scene > Units: set to Metric, scale 0.001 (millimeters). Enable 'Length' display. Use N-panel (sidebar) for exact transform values. Type dimensions during operations: S, X, 2, Enter = scale 2x in X. Use the MeasureIt add-on for on-screen dimensions."), ("How do I import CAD files into Blender?", "Export from CAD as STEP, OBJ, or FBX. In Blender: File > Import. For STEP files, use the CAD Sketcher or built-in STEP importer (Blender 4.0+). FBX/OBJ lose parametric data but preserve mesh geometry. For BIM: use BlenderBIM with IFC files.")]},

    # FreeCAD FAQs
    {"slug": "freecad-vs-fusion-360", "title": "FreeCAD vs Fusion 360 — Free CAD Options Compared", "desc": "Comparing the two most popular free CAD options: FreeCAD (open-source) vs Fusion 360 (freemium). Features, limitations, and best use cases.", "software": "FreeCAD", "sw_slug": "freecad",
     "questions": [("Which is truly free?", "FreeCAD is 100% free, open-source (LGPL), no restrictions, no internet required, forever. Fusion 360 has a free 'Personal Use' tier with limitations: no full CAM, limited file exports, requires Autodesk account, features can change. For commercial use without licensing risk, FreeCAD wins."), ("Which has better modeling?", "Fusion 360 has a more polished, stable parametric modeling experience and better assembly tools. FreeCAD's Part Design is capable but has known issues with the Topological Naming Problem (features break when base sketch changes). FreeCAD 1.0+ addresses this significantly."), ("Which is better for 3D printing?", "Both work well. FreeCAD has the Mesh Design workbench for STL manipulation and Part Design for solid modeling. Fusion 360 has integrated slicing preview and direct export to 3MF. FreeCAD's advantage: Python scripting for parametric model generation (batch-create variations). Fusion's advantage: smoother UX and cloud rendering.")]},

    # General CAD FAQs
    {"slug": "how-to-choose-cad-software", "title": "How to Choose CAD Software — Decision Framework", "desc": "Framework for choosing the right CAD software: budget, industry, skill level, collaboration needs, and platform requirements.", "software": "Multi-platform", "sw_slug": "autocad",
     "questions": [("What factors should I consider?", "Industry standard in your field, budget (subscription vs perpetual vs free), platform needs (Windows/Mac/Linux/Cloud), collaboration features (team size, cloud sharing), learning curve, job market demand, and file format requirements from your clients/partners."), ("Should I learn free software or paid?", "If you're a student: learn both — FreeCAD/Blender for personal projects, and get educational licenses for industry-standard tools (Fusion 360 free tier, SOLIDWORKS student, AutoCAD educational). If professional: learn what your industry uses, supplementing with free tools for personal work."), ("Can I use multiple CAD programs together?", "Absolutely. Common combos: AutoCAD for 2D documentation + Revit for BIM; SOLIDWORKS for MCAD + Fusion 360 for CAM; Rhino/Grasshopper for conceptual design + Revit for documentation. Use neutral formats (STEP, IFC, DXF) to transfer between them.")]},
    {"slug": "cad-career-paths", "title": "CAD Career Paths — Roles, Skills & Salary Ranges", "desc": "Career guide for CAD professionals: job roles (drafter, designer, BIM manager, CAE analyst), required skills, and industry salary expectations.", "software": "Multi-platform", "sw_slug": "autocad",
     "questions": [("What CAD careers are available?", "CAD Drafter/Technician (entry), Design Engineer (mid), Senior Designer/Lead (senior), BIM Manager/Coordinator (BIM), CAE Analyst (simulation), CAD Manager (IT/standards), Application Engineer (vendor side), and Computational Design Specialist (parametric/generative)."), ("What certifications matter?", "Autodesk Certified Professional (ACP) for AutoCAD/Revit/Inventor, SOLIDWORKS CSWA/CSWP/CSWE progression, Siemens NX Associate/Specialist, and PTC Creo certification. For BIM: buildingSMART Professional Certification, BIM Level 2 qualifications (UK)."), ("What salary can I expect?", "Varies by region. US ranges: CAD Drafter $40-60K, Design Engineer $65-95K, BIM Manager $85-130K, CAE Analyst $80-120K, Computational Designer $90-150K. Add 20-40% for senior/lead roles. Specialized skills (CFD, generative design) command premium rates.")]},
    {"slug": "cad-file-management-best-practices", "title": "CAD File Management Best Practices", "desc": "Best practices for organizing CAD files: folder structures, naming conventions, version control, backup strategies, and team collaboration.", "software": "Multi-platform", "sw_slug": "autocad",
     "questions": [("What folder structure should I use?", "Project-based hierarchy: /ProjectName/01-Incoming/02-Working/03-Output/04-Archive. Within Working: separate by discipline (Arch, Struct, MEP) and type (Models, Drawings, References). Include a README or project standards document."), ("What naming convention is best?", "Format: [ProjectCode]-[Discipline]-[Type]-[Zone]-[Level]-[Description]-[Rev]. Example: PRJ001-A-DWG-Z01-L02-FloorPlan-RevC.dwg. Avoid spaces (use hyphens/underscores). Include revision in filename OR use PDM revision tracking — never both."), ("How should I handle backups?", "3-2-1 rule: 3 copies, 2 different media, 1 offsite. Automate daily backups of project folders. For PDM-managed files, the vault handles versioning. For file-based workflows, use automated backup tools with versioned snapshots (not just mirrors).")]},
    {"slug": "cad-collaboration-remote-teams", "title": "CAD Collaboration for Remote & Distributed Teams", "desc": "Strategies for remote CAD collaboration: cloud platforms, file sharing, real-time co-editing, and communication workflows.", "software": "Multi-platform", "sw_slug": "onshape",
     "questions": [("What tools enable remote CAD collaboration?", "Cloud-native: Onshape, Fusion 360 (real-time co-editing). Cloud storage: BIM 360/ACC (Revit), GrabCAD (SOLIDWORKS). File-based: SharePoint/OneDrive with strict check-out protocols. Communication: Slack/Teams channels per project, scheduled design reviews via screen share."), ("How do we avoid file conflicts?", "Option 1: PDM system (SOLIDWORKS PDM, Vault, ProjectWise) with check-in/check-out. Option 2: Cloud-native platform (Onshape, Fusion) with concurrent editing. Option 3: Discipline-based file splitting + scheduled sync meetings. Never use generic cloud sync (Dropbox) for active CAD files without a PDM layer."), ("How to do design reviews remotely?", "Use native review tools: BIM 360 model review, Fusion 360 shared links, eDrawings markup. For presentations: screen share with annotating (Zoom/Teams). For async: BCF (BIM Collaboration Format) for issue tracking, or PDF markups with comment round-trips.")]},

    # Additional targeted pages
    {"slug": "autocad-vs-autocad-lt", "title": "AutoCAD vs AutoCAD LT — Differences & Which to Buy", "desc": "Complete comparison of AutoCAD full version vs LT: 3D capabilities, customization, LISP support, pricing, and decision criteria.", "software": "AutoCAD", "sw_slug": "autocad",
     "questions": [("What features does AutoCAD LT lack?", "LT removes: all 3D modeling/rendering, AutoLISP/VBA programming, network licensing, Express Tools (though some are now included), action recording, CAD standards checking, and .NET API access. LT is strictly for 2D drafting and annotation."), ("Is LT worth the savings?", "AutoCAD LT costs about 60% of full AutoCAD. If you only do 2D drafting with no scripting needs and no 3D, LT is sufficient. But if you use ANY LISP routines, need 3D for visualization, or want Express Tools, full AutoCAD is worth the premium."), ("Should I consider alternatives instead of LT?", "If budget is the primary concern: GstarCAD, ZWCAD, and BricsCAD offer full 2D+3D+LISP capabilities at similar or lower cost than AutoCAD LT, with perpetual licensing options. They read/write native DWG and support most AutoLISP routines.")]},
    {"slug": "revit-vs-autocad-which-to-learn", "title": "Revit vs AutoCAD — Which Should Architects Learn?", "desc": "Comparison of Revit and AutoCAD for architecture students and professionals: when to use each, skill value, and career implications.", "software": "Revit", "sw_slug": "revit",
     "questions": [("Do I still need AutoCAD if I learn Revit?", "Yes, for most architecture careers you need both. Revit for new BIM projects, AutoCAD for 2D details, site plans, renovation as-builts, and working with consultants who use DWG. The BIM mandate is growing but hasn't fully replaced AutoCAD in practice."), ("Which is harder to learn?", "Revit has a steeper initial curve because you're learning BIM methodology simultaneously — understanding families, parameters, levels, and information management. AutoCAD is conceptually simpler (draw lines) but mastery (productivity, standards, customization) takes equally long."), ("Which has better job prospects?", "Both are essential. Revit skills are increasingly required (most architecture job listings mention it). AutoCAD is assumed as baseline. Having both makes you significantly more employable than either alone. Add Rhino/Grasshopper for computational design roles.")]},
]


def generate_faq_page(faq):
    f = faq
    canonical = f"https://gstarcademy.com/kb/faq/{f['slug']}"
    
    qa_html = ""
    schema_qa = []
    for q, a in f["questions"]:
        qa_html += f'''
        <div style="margin-bottom: 20px; padding: 20px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 12px;">
          <h3 style="margin: 0 0 10px; font-size: 0.95rem; font-weight: 700; color: var(--ink-text);">{q}</h3>
          <p style="margin: 0; font-size: 14px; line-height: 1.7; color: var(--ink-text);">{a}</p>
        </div>'''
        schema_qa.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a[:500]}"}}}}')
    
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
      <nav class="kb-faq-breadcrumbs" aria-label="Breadcrumb">
        <a href="../../">Home</a> /
        <a href="../../knowledge-base">Knowledge Base</a> /
        <a href="./">FAQ</a> /
        <span aria-current="page">{f['software']}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 28px;">
          <span class="chip pill-warn">FAQ &middot; {f['software']}</span>
          <h1 style="margin-top: 12px;">{f['title']}</h1>
          <p class="hero-sub">{f['desc']}</p>
        </header>

        <div class="ink-byline" role="contentinfo">
          <span><strong>By</strong> Gstarcademy Editorial Team</span>
          <span><strong>Updated</strong> <time datetime="{TODAY}">{TODAY}</time></span>
        </div>

        <section class="kb-concept-section">
          {qa_html}
        </section>

        <section class="kb-concept-section" style="margin-top: 32px;">
          <h2>Learn More</h2>
          <p>For deeper coverage, explore our <a href="../software/{f['sw_slug']}">{f['software']} knowledge base</a>, <a href="../learning-paths/">learning paths</a>, and <a href="../compare/">software comparisons</a>.</p>
        </section>

        <aside style="margin-top: 32px; padding: 20px 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 14px;">
          <p style="font-size: 12px; font-weight: 600; margin: 0 0 4px;">Gstarcademy Editorial Team</p>
          <p style="font-size: 11px; color: var(--ink-text-soft); margin: 0;">Last updated: <time datetime="{TODAY}">{TODAY}</time></p>
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


def generate_index():
    by_sw = {}
    for f in FAQS:
        sw = f["software"]
        if sw not in by_sw:
            by_sw[sw] = []
        by_sw[sw].append(f)
    
    links = ""
    for sw, faqs in sorted(by_sw.items()):
        links += f'<h3 style="margin-top: 20px;">{sw}</h3><ul style="list-style: none; padding: 0;">\n'
        for f in faqs:
            links += f'<li style="margin-bottom: 8px;"><a href="./{f["slug"]}" style="color: var(--accent); font-weight: 500;">{f["title"]}</a></li>\n'
        links += '</ul>\n'
    
    html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CAD FAQ — Frequently Asked Questions | Gstarcademy</title>
    <meta name="description" content="Answers to common CAD questions: how-to guides for AutoCAD, SOLIDWORKS, Revit, Fusion 360, GstarCAD, and more." />
    <link rel="canonical" href="https://gstarcademy.com/kb/faq/" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="stylesheet" href="../../styles.min.css" />
  </head>
  <body>
    <div class="page-shell"><header class="topbar"><div class="container topbar-inner"><a class="brand" href="../../"><span class="brand-badge">GC</span><span>Gstarcademy</span></a><nav class="nav"><a class="nav-link" href="../../">Home</a><a class="nav-link active" href="../../knowledge-base">Wiki</a><a class="nav-link" href="../../tutorials">Tutorials</a><a class="nav-link" href="../../news">News</a><a class="nav-link" href="../../about">About</a></nav></div></header></div>
    <main class="container" style="margin-top: 32px; max-width: 920px;">
      <h1>CAD FAQ</h1>
      <p style="color: var(--ink-text-soft);">{len(FAQS)} frequently asked questions organized by software.</p>
      {links}
    </main>
    <footer class="footer site-footer"><div class="container site-footer-bottom"><p>&copy; Gstarcademy.</p></div></footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    print(f"Generating {len(FAQS)} FAQ pages...")
    for f in FAQS:
        html = generate_faq_page(f)
        filepath = os.path.join(OUTPUT_DIR, f"{f['slug']}.html")
        with open(filepath, 'w', encoding='utf-8') as fp:
            fp.write(html)
    generate_index()
    print(f"Done! Generated {len(FAQS)} FAQ pages + index")


if __name__ == '__main__':
    main()
