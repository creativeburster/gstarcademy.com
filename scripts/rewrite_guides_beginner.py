#!/usr/bin/env python3
"""
Rewrite all guide pages to use beginner-level language and framing.
Focus: CAD beginners choosing their first software or learning basics.
"""

import os
from datetime import date

TODAY = date.today().isoformat()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'guides')

GUIDES = [
    {"slug": "best-cad-architecture", "title": "Best CAD Software for Architecture Beginners in 2026",
     "desc": "New to architectural CAD? Compare beginner-friendly options: SketchUp, Revit, ArchiCAD, and Vectorworks — ease of learning, free versions, and first-project recommendations.",
     "category": "Architecture",
     "software": [("sketchup", "SketchUp"), ("revit", "Revit"), ("archicad", "ArchiCAD"), ("vectorworks", "Vectorworks")],
     "intro": "Starting your architecture CAD journey can feel overwhelming with so many software options. This guide is written for complete beginners — no prior CAD experience needed. We'll help you pick the right tool based on how easy it is to learn, whether it has a free version, and what kind of projects you want to create.",
     "factors": ["Learning curve — how quickly can a beginner become productive?", "Cost — is there a free or student version available?", "Community resources — are there plenty of beginner tutorials on YouTube?", "Job relevance — will employers value this skill?", "Project type — are you designing houses, interiors, or commercial buildings?"],
     "sw_notes": [
         ("SketchUp", "Easiest to learn (1-2 weeks for basics). Free web version available. Excellent for quick 3D visualization and early design concepts. Huge YouTube tutorial community. Start here if you've never used CAD before."),
         ("Revit", "Industry standard for professional architecture (BIM). Steeper learning curve (1-3 months). Free for students. Essential for career in architecture firms. Start here if you're studying architecture."),
         ("ArchiCAD", "Strong BIM tool with a more intuitive interface than Revit. Free student version. Popular in Europe. Good balance between ease of use and professional capability."),
         ("Vectorworks", "Excellent for design-focused architects. More creative freedom than Revit. Free student version. Popular with smaller firms and design-oriented practices."),
     ],
     "recommendation": "Complete beginners: Start with SketchUp Free to learn 3D thinking. Architecture students: Get the free Revit student license and invest in learning it — it's what firms use. Creative designers: Try ArchiCAD or Vectorworks for a balance of usability and power."},

    {"slug": "best-cad-mechanical-design", "title": "Best CAD Software for Mechanical Design Beginners in 2026",
     "desc": "Starting mechanical CAD? Compare beginner-friendly 3D modeling tools: Fusion 360, SOLIDWORKS, FreeCAD, and Onshape — free options, learning resources, and first-part tutorials.",
     "category": "Mechanical Engineering",
     "software": [("fusion-360", "Fusion 360"), ("solidworks", "SOLIDWORKS"), ("freecad", "FreeCAD"), ("onshape", "Onshape")],
     "intro": "Want to design mechanical parts, products, or machines in 3D? This guide helps complete beginners choose their first CAD software. We focus on ease of learning, free availability, and which software will serve you best as you grow.",
     "factors": ["Free access — can you learn without paying?", "Learning curve — how quickly can you make your first part?", "Career value — which software do employers want on your resume?", "Community — are there free tutorials and forums for beginners?", "3D printing ready — can you easily export for manufacturing?"],
     "sw_notes": [
         ("Fusion 360", "Best starting point for most beginners. Free for personal/hobbyist use. Cloud-based (no powerful PC needed). Includes CAD + CAM + simulation in one tool. Excellent Autodesk learning resources and YouTube tutorials."),
         ("SOLIDWORKS", "Industry standard for mechanical engineering jobs. Steeper learning curve but most requested in job listings. Free for students (through university). Investment pays off for career in manufacturing/product design."),
         ("FreeCAD", "100% free and open-source. No account required. Runs on Windows/Mac/Linux. Learning curve is moderate. Best choice if you want zero cost and no restrictions."),
         ("Onshape", "Free tier available. Runs entirely in browser (no install). Real-time collaboration. Great for learning parametric modeling concepts that transfer to any CAD tool."),
     ],
     "recommendation": "Hobbyists and makers: Start with Fusion 360 Free — easiest path to 3D printing and CNC. Engineering students: Get SOLIDWORKS through your university for career advantage. Budget-conscious: FreeCAD costs nothing and teaches solid parametric fundamentals."},

    {"slug": "best-cad-civil-engineering", "title": "Best CAD Software for Civil Engineering Beginners in 2026",
     "desc": "New to civil engineering CAD? Learn about Civil 3D, MicroStation, and AutoCAD — what each does, how to get started, and which to learn first as a student or entry-level engineer.",
     "category": "Civil Engineering",
     "software": [("civil-3d", "Civil 3D"), ("autocad", "AutoCAD"), ("microstation", "MicroStation")],
     "intro": "Civil engineering CAD involves designing roads, sites, utilities, and infrastructure. If you're just starting out — whether as a student or transitioning into the field — this guide explains which software does what and where to begin your learning journey.",
     "factors": ["What type of civil work interests you (roads, sites, utilities)?", "Is there a free student version?", "What do employers in your region typically use?", "How steep is the learning curve for a beginner?", "Does it build on AutoCAD basics you may already know?"],
     "sw_notes": [
         ("Civil 3D", "The go-to for road design, site grading, and utility networks in North America. Built on AutoCAD, so AutoCAD skills transfer directly. Free for students. Learn this if targeting transportation or land development careers."),
         ("AutoCAD", "Foundation for all 2D civil drafting. Simpler than Civil 3D but essential to learn first. Free for students. Most civil engineers start here before specializing."),
         ("MicroStation", "Common in DOT (Department of Transportation) projects and large infrastructure. Dominant in some regions (UK, parts of US). Learning curve similar to AutoCAD."),
     ],
     "recommendation": "Start with AutoCAD basics (2-4 weeks), then move to Civil 3D for specialization. Students: get free Autodesk student licenses for both. If your target employer uses MicroStation, learn that instead — ask during informational interviews."},

    {"slug": "best-free-cad-software", "title": "Best Free CAD Software for Beginners in 2026",
     "desc": "Want to learn CAD without spending money? Complete guide to free options: FreeCAD, Blender, Fusion 360 Free, SketchUp Free, and Onshape — what each is best for and how to start.",
     "category": "Free & Open Source",
     "software": [("freecad", "FreeCAD"), ("blender", "Blender"), ("fusion-360", "Fusion 360 Free"), ("sketchup", "SketchUp Free"), ("onshape", "Onshape Free")],
     "intro": "You don't need to spend hundreds on software to start learning CAD. Several excellent options are completely free — whether open-source or freemium tiers from major vendors. Here's what each free option is best for and how to get started today.",
     "factors": ["Completely free vs free with limitations?", "What do you want to design (buildings, parts, art, prints)?", "Does it require a powerful computer?", "Are there enough beginner tutorials available?", "Can you grow with it or will you need to switch later?"],
     "sw_notes": [
         ("FreeCAD", "Fully free, open-source, no limitations. Best for: mechanical parts, 3D printing, parametric modeling. Works on any OS. Active community. Moderate learning curve."),
         ("Blender", "Fully free, open-source. Best for: artistic 3D modeling, rendering, animation, game assets. NOT ideal for engineering precision, but excellent for organic shapes and visualization."),
         ("Fusion 360 Free", "Free for personal/hobby use. Best for: mechanical design, 3D printing, CNC machining. Cloud-based. Professional-quality tool with generous free tier. Requires Autodesk account."),
         ("SketchUp Free", "Free web version. Best for: architectural concepts, interior design, quick 3D sketches. Easiest to learn of all CAD tools. Limited export options in free version."),
         ("Onshape Free", "Free tier (public documents). Best for: parametric modeling practice, collaboration. Runs in browser. Professional CAD with training videos built in."),
     ],
     "recommendation": "For mechanical parts/3D printing: Fusion 360 Free or FreeCAD. For buildings/interiors: SketchUp Free. For artistic/organic modeling: Blender. For learning parametric CAD fundamentals: Onshape Free."},

    {"slug": "best-cad-3d-printing", "title": "Best Free CAD Software for 3D Printing Beginners in 2026",
     "desc": "New to 3D printing? Learn which free CAD software to use for designing printable objects: Fusion 360, FreeCAD, Blender, and TinkerCAD — from simple to advanced.",
     "category": "3D Printing",
     "software": [("fusion-360", "Fusion 360"), ("freecad", "FreeCAD"), ("blender", "Blender")],
     "intro": "Got a 3D printer (or access to one) and want to design your own objects instead of downloading files? This guide covers the best free software for beginners, from drag-and-drop simple to full parametric modeling.",
     "factors": ["How complex are the objects you want to create?", "Do you need precise measurements or is 'close enough' fine?", "Are you designing functional parts or artistic pieces?", "How much time are you willing to invest in learning?", "Do you need to modify downloaded STL files?"],
     "sw_notes": [
         ("Fusion 360", "Best all-around choice for 3D printing beginners who want precision. Free for personal use. Excellent STL export. Built-in mesh repair. Great YouTube tutorials from makers. Handles both simple and complex designs."),
         ("FreeCAD", "Fully free, no limitations. Good for precise mechanical parts. Steeper learning curve than Fusion but no account required. Active 3D printing community with tutorials."),
         ("Blender", "Best for organic/artistic shapes (figurines, sculptures, vases). Free and powerful. Less ideal for precise mechanical parts with specific dimensions. Huge tutorial community."),
     ],
     "recommendation": "Complete beginners: Start with TinkerCAD (free, browser-based, drag-and-drop) for your first few prints. Ready to level up: Move to Fusion 360 Free for parametric precision. Making art/figures: Use Blender. Need zero-cost with full power: FreeCAD."},

    {"slug": "best-cad-interior-design", "title": "Best CAD Software for Interior Design Beginners in 2026",
     "desc": "Starting interior design? Learn which software beginners should use: SketchUp, Planner 5D, Revit, and Vectorworks — from room layouts to 3D walkthroughs.",
     "category": "Interior Design",
     "software": [("sketchup", "SketchUp"), ("revit", "Revit"), ("vectorworks", "Vectorworks")],
     "intro": "Want to design room layouts, visualize furniture arrangements, or create client presentations? This guide helps interior design beginners pick the right tool based on skill level, budget, and project type.",
     "factors": ["Are you doing this as a hobby or studying professionally?", "Do you need photorealistic renderings for clients?", "Is free software sufficient for your needs?", "How quickly do you need to become productive?", "Do you need floor plans, 3D views, or both?"],
     "sw_notes": [
         ("SketchUp", "Easiest to learn, most popular for interior design beginners. Free web version. Excellent furniture libraries (3D Warehouse). Quick to produce 3D room visualizations. Most interior design YouTubers teach this."),
         ("Revit", "For professional interior design firms. Creates construction-ready documents. Material schedules, furniture schedules auto-generated. Free for students. Steeper learning curve but industry-standard."),
         ("Vectorworks", "Strong for design-focused interior work. Good rendering built in. Free student version. Popular in smaller design studios that value aesthetics over documentation volume."),
     ],
     "recommendation": "Hobbyists and side projects: SketchUp Free. Interior design students: SketchUp for quick work + Revit for professional skills. Professional path: Learn SketchUp first (1 week), then transition to Revit or Vectorworks for your career."},

    {"slug": "best-cad-automotive", "title": "CAD for Automotive Design — What Beginners Should Know",
     "desc": "Interested in automotive CAD? Learn what software the industry uses, what beginners should start with, and how to build skills toward a car design career.",
     "category": "Automotive",
     "software": [("solidworks", "SOLIDWORKS"), ("fusion-360", "Fusion 360"), ("blender", "Blender")],
     "intro": "Dreaming of designing cars? The automotive industry uses specialized (expensive) tools like CATIA and NX. But as a beginner, you can build foundational CAD skills with accessible software first, then specialize later.",
     "factors": ["Are you interested in exterior styling or mechanical engineering?", "Do you have access to student software licenses?", "Are you in an engineering program or self-teaching?", "What's your timeline (hobby exploration vs career goal)?"],
     "sw_notes": [
         ("SOLIDWORKS", "Best beginner-friendly path to automotive mechanical engineering (chassis, engine parts, fixtures). Free for students through universities. Skills directly transfer to entry-level auto industry jobs."),
         ("Fusion 360", "Free for personal use. Good for learning 3D modeling fundamentals. Surface modeling capabilities for exterior concepts. Great first step before expensive industry tools."),
         ("Blender", "Free. Excellent for automotive exterior concept visualization and rendering. Many car modeling tutorials on YouTube. Not used for engineering but great for design presentation."),
     ],
     "recommendation": "Engineering students: Start with SOLIDWORKS or Fusion 360 for mechanical components. Design/styling enthusiasts: Start with Blender for exterior visualization. Know that industry tools (CATIA, NX) come later in your career — employers train you on their specific toolset."},

    {"slug": "best-cad-aerospace", "title": "CAD for Aerospace — What Students Should Learn First",
     "desc": "Pursuing aerospace engineering? Learn which CAD skills to develop as a student: SOLIDWORKS for fundamentals, then CATIA/NX for industry specialization.",
     "category": "Aerospace",
     "software": [("solidworks", "SOLIDWORKS"), ("fusion-360", "Fusion 360"), ("freecad", "FreeCAD")],
     "intro": "Aerospace companies use enterprise CAD tools (CATIA, NX, Creo). But as a student or early-career engineer, you should focus on learning transferable CAD fundamentals first. Here's the practical path.",
     "factors": ["Are you still in university or early career?", "Does your program provide specific software access?", "Are you targeting structures, propulsion, or systems?", "Do you need CFD/FEA or just geometry modeling?"],
     "sw_notes": [
         ("SOLIDWORKS", "Most common in aerospace university programs. Free through student license. Excellent for learning parametric modeling, assemblies, and drawings. Skills transfer to CATIA (same company). Best first step."),
         ("Fusion 360", "Free for students/personal use. Good for individual projects and prototyping. Integrated simulation for basic stress analysis. Cloud-based convenience."),
         ("FreeCAD", "Free alternative if your university doesn't provide SOLIDWORKS. Open-source FEM workbench for basic structural analysis. Good for self-study."),
     ],
     "recommendation": "University students: Use whatever your program provides (usually SOLIDWORKS or NX). Self-learners: Start with Fusion 360 Free. The key insight: aerospace employers will train you on their specific tool (CATIA/NX/Creo) — your job is to demonstrate strong parametric modeling fundamentals."},

    {"slug": "best-cad-students", "title": "Best Free CAD Software for Students in 2026 — Complete Guide",
     "desc": "Student looking for free CAD software? Get free professional licenses from Autodesk, SOLIDWORKS, Siemens — plus open-source alternatives. Complete access guide.",
     "category": "Education",
     "software": [("fusion-360", "Fusion 360"), ("solidworks", "SOLIDWORKS"), ("freecad", "FreeCAD"), ("onshape", "Onshape"), ("autocad", "AutoCAD")],
     "intro": "As a student, you have access to professional CAD software for FREE that normally costs thousands per year. This guide shows you exactly how to get legal student licenses, plus which software to prioritize based on your major.",
     "factors": ["What's your field of study?", "Does your university have specific software partnerships?", "Do you need it for coursework or personal projects?", "Windows, Mac, or Chromebook?", "Do you want cloud-based or installed software?"],
     "sw_notes": [
         ("Fusion 360", "Free for students (verify with .edu email). Cloud-based. Works on Windows and Mac. Covers mechanical design, electronics, CAM, and simulation. Best all-in-one for engineering students."),
         ("SOLIDWORKS", "Free through many universities (check with your department). Industry standard for mechanical engineering. Windows only. Career-critical for MECH/MFG majors."),
         ("FreeCAD", "Free for everyone, always. No email verification needed. Linux/Mac/Windows. Best for students on Chromebooks (via Linux) or those wanting true open-source."),
         ("Onshape", "Free education plan. Browser-based (works on anything). Real-time collaboration for team projects. Teaches modern cloud-CAD concepts."),
         ("AutoCAD", "Free for students (Autodesk Education). Essential for civil engineering and architecture students. Learn 2D drafting fundamentals here."),
     ],
     "recommendation": "Architecture: AutoCAD + Revit (free student). Mechanical: SOLIDWORKS (university) + Fusion 360 (personal). Civil: AutoCAD + Civil 3D. Electrical: Fusion 360 Electronics. Any major: Start with Onshape (zero friction, browser-based) to learn CAD thinking."},

    {"slug": "best-cad-product-design", "title": "Best CAD Software for Product Design Beginners in 2026",
     "desc": "Want to design consumer products? Compare beginner-friendly tools: Fusion 360, SOLIDWORKS, Onshape, and Rhino — which to learn first for product/industrial design.",
     "category": "Product Design",
     "software": [("fusion-360", "Fusion 360"), ("solidworks", "SOLIDWORKS"), ("onshape", "Onshape"), ("rhinoceros", "Rhino")],
     "intro": "Product design combines engineering precision with aesthetic form. Whether you want to design phone cases, furniture, kitchen tools, or electronics enclosures, you need CAD software that handles both organic shapes and precise dimensions.",
     "factors": ["Are you more engineering-focused or design/aesthetics-focused?", "Do you need to prepare files for manufacturing?", "Is free software sufficient?", "Do you want to do your own rendering/visualization?", "How quickly do you need to be productive?"],
     "sw_notes": [
         ("Fusion 360", "Best starting point for product design beginners. Free personal license. Handles both precision parts and freeform surfaces. Built-in rendering. Direct path to 3D printing and CNC manufacturing."),
         ("SOLIDWORKS", "Industry standard for manufactured products. More precise engineering controls. Free for students. Best for career in product development at established companies."),
         ("Onshape", "Free tier available. Browser-based. Excellent for learning parametric design. Good for collaboration on team projects. Professional workflow without the install."),
         ("Rhino", "Best for complex organic surfaces (shoes, bottles, jewelry, furniture). Student license affordable. Grasshopper plugin for parametric/generative design. Less engineering-focused."),
     ],
     "recommendation": "Engineering-focused (functional products): Fusion 360 → SOLIDWORKS. Design-focused (aesthetics, form): Rhino + Blender for rendering. All-around beginners: Start with Fusion 360 Free — it covers the widest ground with the lowest barrier."},

    {"slug": "best-cad-mep-engineering", "title": "CAD for MEP Engineering — Beginner's Guide",
     "desc": "New to MEP (mechanical, electrical, plumbing) design? Learn which CAD/BIM tools to study, what MEP engineers actually do in CAD, and how to start building skills.",
     "category": "MEP Engineering",
     "software": [("revit", "Revit MEP"), ("autocad", "AutoCAD MEP")],
     "intro": "MEP (Mechanical, Electrical, Plumbing) engineers design building services — HVAC ducts, plumbing pipes, electrical systems. If you're starting in this field, here's what software to learn and how to begin.",
     "factors": ["Are you studying HVAC, electrical, or plumbing specifically?", "Does your employer or program specify software?", "Do you need BIM (3D coordinated) or 2D drafting?", "What's your AutoCAD comfort level?"],
     "sw_notes": [
         ("Revit MEP", "Industry standard for BIM-based MEP design. Creates 3D coordinated models of ducts, pipes, and conduit. Used for clash detection with architecture and structure. Free for students. THE skill to have for MEP careers."),
         ("AutoCAD MEP", "For firms still doing 2D-based MEP design (smaller projects, renovations). Familiar if you know basic AutoCAD. Being phased out in favor of Revit on new projects."),
     ],
     "recommendation": "Students entering MEP: Learn Revit MEP — it's where the industry is heading. Start with basic Revit (architecture views) to understand the interface, then specialize in MEP systems. AutoCAD basics are helpful but not the priority for new professionals."},

    {"slug": "best-cad-landscape-architecture", "title": "CAD for Landscape Architecture Beginners",
     "desc": "Starting landscape architecture? Learn which CAD tools beginners should study: SketchUp for visualization, Civil 3D for grading, and Vectorworks for design-build.",
     "category": "Landscape Architecture",
     "software": [("sketchup", "SketchUp"), ("civil-3d", "Civil 3D"), ("vectorworks", "Vectorworks")],
     "intro": "Landscape architecture combines artistic site design with technical grading, planting plans, and drainage engineering. Different software handles different aspects — here's how to navigate as a beginner.",
     "factors": ["Are you focused on design (planting, hardscape) or engineering (grading, drainage)?", "Is a free tool sufficient for learning?", "What does your program teach?", "Do you need 3D visualization for client presentations?"],
     "sw_notes": [
         ("SketchUp", "Best for 3D site visualization and concept presentations. Easy to learn. Free web version. Add-ons for landscape design. Great for communicating design intent to clients."),
         ("Civil 3D", "For technical site work: grading, drainage, earthwork calculations. Free for students. Essential if you work on site engineering aspects. Built on AutoCAD."),
         ("Vectorworks Landmark", "All-in-one landscape architecture tool. BIM-capable. Plant databases, irrigation design, hardscape detailing. Free for students. Popular in landscape-specific firms."),
     ],
     "recommendation": "Start with SketchUp for 3D thinking (week 1-2). Add AutoCAD for 2D plan production. Then specialize: Vectorworks Landmark for design-focused firms, or Civil 3D for engineering-focused site work."},

    {"slug": "best-cad-furniture-design", "title": "Best CAD Software for Furniture Design Beginners",
     "desc": "Want to design furniture? Compare beginner-friendly CAD tools for woodworkers and furniture makers: SketchUp, Fusion 360, FreeCAD — from simple sketches to CNC-ready files.",
     "category": "Furniture Design",
     "software": [("sketchup", "SketchUp"), ("fusion-360", "Fusion 360"), ("freecad", "FreeCAD")],
     "intro": "Whether you're a hobbyist woodworker wanting to plan projects or a furniture design student, CAD software helps you visualize, refine, and produce accurate cut lists and joinery details.",
     "factors": ["Hand tools or CNC/machine fabrication?", "Simple projects (shelves, tables) or complex joinery?", "Need renderings for client approval?", "Budget: free tools only or willing to invest?", "Do you need cut lists and material optimization?"],
     "sw_notes": [
         ("SketchUp", "Most popular among woodworkers. Easy to learn. Free web version. Huge furniture design community. Plugins for cut lists, joinery, and rendering. Start here."),
         ("Fusion 360", "Best for CNC-furniture and complex parametric designs. Free for personal use. T-spline surfaces for organic furniture forms. Direct CAM output for CNC routing."),
         ("FreeCAD", "Free, open-source. Good for precise joinery modeling. Steeper curve than SketchUp but fully capable for furniture. No cost, ever."),
     ],
     "recommendation": "Hand-tool woodworkers: SketchUp Free for planning. CNC furniture makers: Fusion 360 for design-to-manufacture. Budget-conscious: SketchUp Free → FreeCAD as you advance."},

    {"slug": "best-cad-jewelry-design", "title": "CAD for Jewelry Design Beginners",
     "desc": "Interested in jewelry CAD? Learn which free and affordable tools beginners use for ring, pendant, and gemstone modeling: Blender, Fusion 360, and Rhino basics.",
     "category": "Jewelry Design",
     "software": [("blender", "Blender"), ("fusion-360", "Fusion 360"), ("rhinoceros", "Rhino")],
     "intro": "Jewelry CAD lets you design rings, pendants, bracelets, and earrings in 3D before casting or 3D printing them in wax/resin. The industry uses specialized tools (RhinoGold, MatrixGold), but beginners can start free.",
     "factors": ["Are you designing for 3D printing/casting or hand fabrication?", "Simple bands/pendants or complex gem settings?", "Budget: can you invest in specialized jewelry plugins?", "Are organic or geometric designs your style?"],
     "sw_notes": [
         ("Blender", "Free. Excellent for organic jewelry forms (skulls, animals, flowing shapes). Many jewelry-specific YouTube tutorials. Export to STL for wax printing. Best free starting point for artistic jewelry."),
         ("Fusion 360", "Free personal use. Good for precise geometric designs (bezels, prong settings). Parametric control for sizing rings across finger sizes. Direct 3D print export."),
         ("Rhino", "Industry standard when paired with MatrixGold plugin. Student license affordable. Most professional jewelry CAD houses use Rhino. Learn this for career in jewelry trade."),
     ],
     "recommendation": "Hobby/artistic jewelry: Start with Blender (free, excellent organic forms). Precision/commercial: Start with Fusion 360 Free, then consider Rhino + MatrixGold when you're ready to go professional."},

    {"slug": "best-cad-game-development", "title": "Best 3D Modeling Software for Game Dev Beginners",
     "desc": "Want to make 3D game assets? Beginner's guide to Blender (free), SketchUp, and the modeling pipeline — from first mesh to game engine import.",
     "category": "Game Development",
     "software": [("blender", "Blender"), ("sketchup", "SketchUp")],
     "intro": "Game development needs 3D models (characters, environments, props) created outside the game engine, then imported. Here's what free tools beginners use and how the pipeline works.",
     "factors": ["Characters, environments, or props?", "Stylized (low-poly) or realistic?", "Which game engine (Unity, Unreal, Godot)?", "Are you working alone or on a team?", "Do you want to sculpt or hard-surface model?"],
     "sw_notes": [
         ("Blender", "The clear winner for beginners. Completely free. Modeling, sculpting, texturing, rigging, and animation in one tool. Exports to all game engines. Massive tutorial ecosystem. Used by indie and AAA studios."),
         ("SketchUp", "Quick for blockout/prototyping environments. Easy to learn. Good for architectural game assets (buildings, interiors). Limited for characters or organic shapes."),
     ],
     "recommendation": "Start with Blender — it's free, industry-accepted, and covers the entire 3D game art pipeline. Follow a beginner course (Blender Guru, Grant Abbitt) and you'll be making game-ready assets within a month."},

    # Keep methodology/workflow guides but make them beginner-friendly
    {"slug": "dwg-vs-rvt-vs-ifc", "title": "DWG vs RVT vs IFC — File Formats Explained for Beginners",
     "desc": "Confused by CAD file formats? Simple explanation of DWG (AutoCAD), RVT (Revit), and IFC (universal BIM) — what each is, when you'll encounter them, and how to handle them.",
     "category": "File Formats",
     "software": [("autocad", "AutoCAD (DWG)"), ("revit", "Revit (RVT)")],
     "intro": "You'll encounter many file formats in CAD. The three most important in architecture/engineering are DWG, RVT, and IFC. Here's a plain-English explanation of what each is and when you'll need them.",
     "factors": ["DWG = AutoCAD's format. The most common 2D/3D drawing file. Almost universal.", "RVT = Revit's format. Contains a complete building information model. Only opens in Revit.", "IFC = Universal BIM format. Any BIM software can open it. Used for sharing between different programs."],
     "sw_notes": [
         ("AutoCAD (DWG)", "DWG files contain geometry (lines, arcs, text) in 2D or 3D. They're the most widely exchanged CAD file type. Almost every CAD program can open DWG. You'll see these everywhere."),
         ("Revit (RVT)", "RVT files contain an entire building model with intelligent objects (walls know they're walls, doors know their fire rating). Much richer data than DWG but only works in Revit."),
     ],
     "recommendation": "Rule of thumb: DWG for 2D drawings and simple 3D. RVT when working in Revit teams. IFC when sharing BIM models between different software (e.g., architect uses Revit, structural engineer uses Tekla). Don't stress about this early — you'll learn naturally as you work."},

    {"slug": "parametric-vs-direct-modeling", "title": "Parametric vs Direct Modeling — Beginner's Explanation",
     "desc": "Two ways to model in CAD: parametric (history-based) and direct (push-pull). What each means, which software uses which, and which beginners should learn first.",
     "category": "Methodology",
     "software": [("solidworks", "SOLIDWORKS"), ("fusion-360", "Fusion 360"), ("onshape", "Onshape")],
     "intro": "CAD software uses two main approaches to 3D modeling. Understanding this helps you choose software and know what to expect when learning. Here's the difference in plain language.",
     "factors": ["Parametric = every step is recorded. Change a dimension → everything updates automatically.", "Direct = push, pull, move faces freely. No history. Quick edits but no automatic updates.", "Most modern software offers both (Fusion 360, NX, Creo, BricsCAD).", "Beginners should start with parametric — it teaches better design habits.", "Direct modeling is faster for one-off modifications and imported geometry."],
     "sw_notes": [
         ("SOLIDWORKS", "Primarily parametric. Every feature (extrude, cut, fillet) is in a history tree. Change a sketch dimension and everything rebuilds. The standard teaching approach for engineering CAD."),
         ("Fusion 360", "Both parametric AND direct. You can switch between timeline (parametric) and direct editing. Great for learning both approaches in one tool."),
         ("Onshape", "Parametric with history. Similar to SOLIDWORKS in approach. Good for learning parametric fundamentals with free access."),
     ],
     "recommendation": "Learn parametric modeling first — it teaches you to think about design intent and relationships. Start with Fusion 360 or Onshape (free) and follow their built-in tutorials."},

    {"slug": "bim-vs-cad", "title": "BIM vs CAD — What's the Difference? (Simple Explanation)",
     "desc": "BIM and CAD — what's the difference? Simple explanation for beginners: CAD draws lines, BIM creates intelligent building models. When to use each and how they work together.",
     "category": "Methodology",
     "software": [("autocad", "AutoCAD (CAD)"), ("revit", "Revit (BIM)")],
     "intro": "You'll hear 'CAD' and 'BIM' used constantly in architecture and engineering. They're related but different. Here's the simplest possible explanation.",
     "factors": ["CAD = Computer-Aided Design. You draw lines, shapes, and annotations. Like a digital drafting board.", "BIM = Building Information Modeling. You place intelligent objects (walls, doors, windows) that 'know' what they are.", "CAD is older and simpler. BIM is newer and more powerful for buildings.", "Most firms use BOTH — CAD for quick details, BIM for the main model.", "Learning order: AutoCAD basics first, then Revit for BIM."],
     "sw_notes": [
         ("AutoCAD (CAD)", "The classic CAD tool. You draw lines, rectangles, circles. A wall is just two parallel lines — the software doesn't know it's a wall. Fast and flexible but less intelligent. Still used for details, site plans, and simple projects."),
         ("Revit (BIM)", "A wall in Revit IS a wall object — it has height, material, fire rating, cost. Change the floor plan and the sections, elevations, and schedules update automatically. More setup time but huge efficiency for complex buildings."),
     ],
     "recommendation": "Students should learn BOTH. Start with AutoCAD (simpler, teaches spatial thinking), then add Revit (teaches BIM methodology). Most jobs require both. The industry is moving toward BIM for all new buildings, but CAD isn't going away."},

    {"slug": "cloud-cad-vs-desktop", "title": "Cloud CAD vs Desktop CAD — Which is Better for Beginners?",
     "desc": "Should you use cloud CAD (Onshape, Fusion 360) or desktop CAD (SOLIDWORKS, AutoCAD)? Beginner's comparison of convenience, cost, and learning experience.",
     "category": "Methodology",
     "software": [("onshape", "Onshape"), ("fusion-360", "Fusion 360"), ("solidworks", "SOLIDWORKS")],
     "intro": "Some CAD software runs in your browser (cloud), while others require installation on your computer (desktop). For beginners, this choice affects your learning experience more than you might think.",
     "factors": ["Cloud: works on any computer/tablet with internet. No install. Auto-saves.", "Desktop: needs a decent Windows PC. More features. Works offline.", "Cloud is easier to start (zero setup) but needs internet.", "Desktop is more powerful but requires hardware investment.", "Skills transfer between both — the modeling concepts are the same."],
     "sw_notes": [
         ("Onshape", "Cloud-native. Runs in any browser. Zero install. Free education tier. Real-time collaboration (like Google Docs for CAD). Best for getting started instantly with zero friction."),
         ("Fusion 360", "Hybrid — installs locally but syncs to cloud. Works offline. Free personal license. More features than Onshape's free tier. Good middle ground."),
         ("SOLIDWORKS", "Desktop only. Windows only. Needs a capable PC. Industry standard for jobs. Free through universities. Learn this for career, not for convenience."),
     ],
     "recommendation": "Just want to learn NOW with zero barriers: Onshape (open browser, start modeling). Have a decent PC and want career skills: Fusion 360 or SOLIDWORKS. The underlying skills transfer between all of them."},

    {"slug": "autocad-alternatives", "title": "Cheaper Alternatives to AutoCAD for Beginners in 2026",
     "desc": "AutoCAD too expensive? Learn about affordable alternatives that read DWG files: GstarCAD, ZWCAD, BricsCAD, DraftSight, and free options for learning 2D CAD.",
     "category": "Alternatives",
     "software": [("gstarcad", "GstarCAD"), ("bricscad", "BricsCAD"), ("draftsight", "DraftSight"), ("freecad", "FreeCAD")],
     "intro": "AutoCAD is expensive (~$1,800/year). If you're a student, you get it free. But if you're a hobbyist, freelancer, or from a small firm, these alternatives work with the same DWG files at a fraction of the cost.",
     "factors": ["All alternatives listed here can open and save DWG files.", "Most use the same commands as AutoCAD (LINE, CIRCLE, TRIM, etc.).", "Some offer perpetual licenses (pay once, own forever) vs AutoCAD's subscription.", "Free student: just get AutoCAD Education — it's free and full-featured.", "Professionals saving money: BricsCAD and GstarCAD are proven alternatives."],
     "sw_notes": [
         ("GstarCAD", "~1/3 the cost of AutoCAD. Perpetual license available. DWG-native. Same commands. Supports AutoLISP scripts. Best value for firms switching from AutoCAD. Very similar workflow — minimal retraining."),
         ("BricsCAD", "DWG-compatible + has 3D/BIM capabilities. Perpetual license. AI tools (Blockify, Propagate). One-time cost. Good for firms wanting DWG compatibility plus future BIM capability."),
         ("DraftSight", "From Dassault (SOLIDWORKS company). DWG-compatible. Professional tier has 3D. Clean interface. Good for SOLIDWORKS shops that also need 2D drafting."),
         ("FreeCAD", "Completely free. Can import/export DXF and some DWG. Not a direct AutoCAD replacement (different interface) but capable for 2D drafting and 3D modeling at zero cost."),
     ],
     "recommendation": "Students: use free AutoCAD Education. Hobbyists: FreeCAD or LibreCAD (free). Small firms: GstarCAD or BricsCAD for DWG compatibility at lower cost. The commands you learn in any DWG-based tool transfer to AutoCAD if needed later."},

    {"slug": "solidworks-alternatives", "title": "Free Alternatives to SOLIDWORKS for Beginners",
     "desc": "Can't afford SOLIDWORKS? Learn free alternatives for 3D mechanical CAD: Fusion 360 Free, FreeCAD, Onshape Free — how they compare and which to start with.",
     "category": "Alternatives",
     "software": [("fusion-360", "Fusion 360"), ("onshape", "Onshape"), ("freecad", "FreeCAD")],
     "intro": "SOLIDWORKS costs ~$4,000-8,000 and requires Windows. If you can't access it through school, here are free alternatives that teach the same parametric modeling fundamentals.",
     "factors": ["All three alternatives below are free and teach parametric modeling.", "Skills learned in any parametric CAD transfer to SOLIDWORKS.", "If your university offers SOLIDWORKS — use it. It's the career standard.", "These alternatives are NOT 'lesser' — they're fully capable for learning."],
     "sw_notes": [
         ("Fusion 360", "Free for personal use. Closest workflow to SOLIDWORKS for beginners. Sketch → Extrude → Pattern workflow is nearly identical. Best free alternative for learning skills that transfer to SOLIDWORKS jobs."),
         ("Onshape", "Free tier available. Browser-based. Created by former SOLIDWORKS developers — similar workflow intentionally. Excellent built-in tutorials. No install needed."),
         ("FreeCAD", "Fully free, open-source. More rough around the edges UI-wise but fully capable Part Design workbench. Zero restrictions. Community-driven documentation."),
     ],
     "recommendation": "Best SOLIDWORKS skill-transfer: Fusion 360 Free or Onshape. Zero friction start: Onshape (just open browser). Zero cost + zero restrictions: FreeCAD. Once you know parametric modeling in any tool, SOLIDWORKS becomes easy to pick up if you get access later."},

    {"slug": "revit-alternatives", "title": "Free Alternatives to Revit for BIM Beginners",
     "desc": "Learning BIM but can't access Revit? Free alternatives: BlenderBIM, FreeCAD BIM, and affordable options like ArchiCAD and BricsCAD BIM.",
     "category": "Alternatives",
     "software": [("blender", "BlenderBIM"), ("freecad", "FreeCAD BIM"), ("archicad", "ArchiCAD"), ("bricscad", "BricsCAD BIM")],
     "intro": "Revit is the BIM industry standard, but it's expensive and Windows-only. If you're exploring BIM concepts without access to Revit, here are alternatives.",
     "factors": ["Revit Education is FREE for students — check first!", "BIM concepts transfer between tools (the methodology matters more than the software).", "BlenderBIM is fully free and open-source BIM.", "ArchiCAD and BricsCAD have affordable student licenses."],
     "sw_notes": [
         ("BlenderBIM", "Completely free, open-source. Full IFC (open BIM) authoring in Blender. Unconventional interface for BIM users but fully capable. Best free BIM tool available. Works on all platforms."),
         ("FreeCAD BIM", "Free, open-source. BIM workbench for basic building modeling and IFC export. More experimental than BlenderBIM but integrated with FreeCAD's parametric modeling."),
         ("ArchiCAD", "Professional BIM tool. Free for students (25 license). More intuitive than Revit for beginners. Strong in Europe and parts of Asia. Excellent learning option."),
         ("BricsCAD BIM", "DWG-based BIM. AI-powered classification. Affordable perpetual license. Good option for firms familiar with AutoCAD wanting to add BIM."),
     ],
     "recommendation": "Students: Get free Revit Education or free ArchiCAD student license — learn the professional tools while they're free. Self-learners without student access: BlenderBIM for full free BIM capability."},

    {"slug": "cad-system-requirements-2026", "title": "What Computer Do I Need for CAD? (Beginner's Hardware Guide 2026)",
     "desc": "Worried your computer can't run CAD? Simple hardware guide for beginners — minimum specs, what actually matters, and budget recommendations for students.",
     "category": "Hardware",
     "software": [("fusion-360", "Fusion 360"), ("solidworks", "SOLIDWORKS"), ("revit", "Revit"), ("blender", "Blender")],
     "intro": "Good news: you don't need an expensive workstation to start learning CAD. Here's what actually matters hardware-wise for beginners, and some budget-friendly options.",
     "factors": ["Cloud CAD (Onshape, SketchUp Free) runs on ANY computer with a browser.", "Most CAD software runs fine on a mid-range laptop from the last 3-4 years.", "RAM matters most — aim for 16GB (8GB absolute minimum).", "A dedicated GPU helps but isn't required for learning.", "SSD storage makes everything faster — avoid mechanical hard drives."],
     "sw_notes": [
         ("Fusion 360", "Runs well on modest hardware. 8GB RAM works for simple parts. Mac and Windows. Cloud processing handles heavy tasks (rendering, simulation) on their servers."),
         ("SOLIDWORKS", "Windows only. Needs 16GB RAM, dedicated GPU recommended. Most demanding on hardware. But learning with simple parts (under 100 features) works fine on mid-range laptops."),
         ("Revit", "Windows only. 16GB RAM minimum for real projects. Learning with small models works on less. SSD strongly recommended."),
         ("Blender", "Runs on anything (Windows/Mac/Linux). Very light for modeling. Only needs a good GPU for rendering — but you don't need to render while learning."),
     ],
     "recommendation": "Starting out? Use cloud CAD (Onshape, SketchUp Free) on whatever you have. Buying a laptop for CAD? Get: 16GB RAM, SSD, Intel i5/AMD Ryzen 5 or better, dedicated GPU nice-to-have. Budget ~$700-1000 for a capable CAD laptop. Don't overspend — the learning happens between your ears, not in the hardware."},

    {"slug": "cad-file-formats-guide", "title": "CAD File Formats Explained Simply — DWG, STEP, STL & More",
     "desc": "Confused by CAD file formats? Beginner-friendly guide to DWG, DXF, STEP, STL, OBJ, and IFC — what each is for, when you'll need them, and which software uses which.",
     "category": "File Formats",
     "software": [("autocad", "AutoCAD"), ("solidworks", "SOLIDWORKS"), ("fusion-360", "Fusion 360")],
     "intro": "There are dozens of CAD file formats. As a beginner, here are the ones that actually matter and what each is used for — explained without jargon.",
     "factors": ["DWG/DXF = 2D drawings (AutoCAD world)", "STEP/IGES = sharing 3D models between different software", "STL/3MF = 3D printing", "IFC = sharing BIM building models", "Each software has its own native format too (SLDPRT, FCStd, F3D, etc.)"],
     "sw_notes": [
         ("AutoCAD", "Native: DWG. Also uses DXF (interchange), DWF (lightweight viewing). Export to PDF for sharing drawings."),
         ("SOLIDWORKS", "Native: SLDPRT (part), SLDASM (assembly), SLDDRW (drawing). Export STEP for sharing 3D, STL for printing, PDF for 2D."),
         ("Fusion 360", "Native: F3D (cloud). Export STEP for sharing, STL/3MF for printing, DXF for laser cutting."),
     ],
     "recommendation": "Don't memorize all formats. Just remember: save in native format for your own work. Export STEP to share 3D models with others. Export STL for 3D printing. Export PDF for 2D drawings. That's 90% of what beginners need."},

    {"slug": "cad-collaboration-tools", "title": "How to Collaborate on CAD Projects — Beginner's Guide",
     "desc": "Need to work on CAD with classmates or colleagues? Simple guide to sharing files, collaborating in real-time, and managing versions without losing work.",
     "category": "Collaboration",
     "software": [("onshape", "Onshape"), ("fusion-360", "Fusion 360")],
     "intro": "Working on a CAD project with others (classmates, team members)? Here's how to share work without overwriting each other's changes or losing files.",
     "factors": ["Simplest: use cloud CAD (Onshape/Fusion 360) — everyone sees the same model.", "File-based: share via Google Drive/Dropbox with a naming convention.", "NEVER have two people edit the same file at the same time (unless using cloud CAD).", "Version naming: ProjectName_v01, ProjectName_v02, etc.", "Export STEP/PDF for review — don't send your native CAD files to non-CAD users."],
     "sw_notes": [
         ("Onshape", "Built for collaboration. Multiple people edit the same document simultaneously (like Google Docs). Version control built in. Free education plan. Best for team projects."),
         ("Fusion 360", "Cloud storage with sharing links. Team members can view and comment. One editor at a time per file. Forking and merging for parallel work."),
     ],
     "recommendation": "Student team projects: Use Onshape Free (everyone edits in browser, no install conflicts). Solo with occasional sharing: Fusion 360 shared links. Just need someone to review: Export STEP + screenshots."},

    {"slug": "cad-automation-scripting", "title": "Introduction to CAD Scripting & Automation for Beginners",
     "desc": "Interested in automating CAD tasks? Beginner's introduction to scripting: what's possible, which languages each software uses, and how to write your first script.",
     "category": "Scripting",
     "software": [("autocad", "AutoCAD (LISP)"), ("freecad", "FreeCAD (Python)"), ("rhinoceros", "Rhino (Grasshopper)")],
     "intro": "Once you're comfortable with basic CAD, scripting lets you automate repetitive tasks. This is an introduction — you don't need programming experience to understand the concepts, but you'll need some to write scripts.",
     "factors": ["Scripting = telling the CAD software what to do with text commands instead of clicking.", "Each software has its own scripting language (unfortunately, not universal).", "Start simple: record a macro of actions you repeat frequently.", "Python is the most transferable language across CAD platforms.", "Grasshopper (Rhino) is visual scripting — no code typing required."],
     "sw_notes": [
         ("AutoCAD (LISP)", "AutoCAD uses AutoLISP — a specialized language. Good for: automating drawing tasks, batch processing files, custom commands. Start by recording Action Macros (no coding needed)."),
         ("FreeCAD (Python)", "FreeCAD uses Python — the most popular programming language. Great for: learning to code + learning CAD automation simultaneously. Python skills transfer to data science, web dev, etc."),
         ("Rhino (Grasshopper)", "Grasshopper is VISUAL scripting (connect boxes with wires). No typing code. Great for: parametric design, generative patterns, complex geometry. Architect/designer-friendly."),
     ],
     "recommendation": "Never coded before? Start with Grasshopper in Rhino (visual, immediate results) or FreeCAD Python console (transferable language). Already code? Look at your CAD tool's API documentation. Just want quick automation? Use macro recording (available in AutoCAD, SOLIDWORKS, etc.) — zero programming needed."},

    {"slug": "cad-certification-guide", "title": "Are CAD Certifications Worth It? (Student & Beginner Guide)",
     "desc": "Thinking about getting CAD certified? Honest guide for beginners: which certifications exist, what they actually prove, and whether employers care.",
     "category": "Career",
     "software": [("autocad", "AutoCAD ACP"), ("solidworks", "SOLIDWORKS CSWA"), ("revit", "Revit ACP")],
     "intro": "CAD vendors offer certification exams. But are they worth your time and money as a beginner? Here's an honest breakdown from the hiring perspective.",
     "factors": ["Certifications prove baseline competency — not mastery.", "They're most valuable for entry-level candidates with no work experience.", "A portfolio of projects often impresses employers more.", "Many certifications are free or cheap for students.", "Don't pursue certification before you're comfortable with the basics."],
     "sw_notes": [
         ("AutoCAD ACP", "Autodesk Certified Professional. Costs ~$175. Tests practical AutoCAD skills. Worth it if applying for drafting positions and have no work experience yet. Listed on resumes for entry-level roles."),
         ("SOLIDWORKS CSWA", "Certified SOLIDWORKS Associate. Entry-level exam. ~$99 (often free through universities). Tests basic modeling skills. Good for mechanical engineering students applying for internships."),
         ("Revit ACP", "Autodesk Certified Professional for Revit. Tests BIM modeling skills. Useful for architecture students entering job market. Shows you've invested in learning the tool."),
     ],
     "recommendation": "Students with no experience: Yes, get CSWA or ACP — it's a resume differentiator for your first job/internship. Working professionals: your portfolio and work history matter more. Don't pay for certification if your university offers free vouchers — ask your department."},

    {"slug": "from-autocad-to-revit", "title": "Switching from AutoCAD to Revit — Beginner's Transition Guide",
     "desc": "Know AutoCAD and need to learn Revit? What transfers, what's completely different, and a realistic timeline for becoming productive in BIM.",
     "category": "Migration",
     "software": [("autocad", "AutoCAD"), ("revit", "Revit")],
     "intro": "Many beginners learn AutoCAD first, then need Revit for BIM projects. Good news: some skills transfer. Bad news: the mindset is fundamentally different. Here's what to expect.",
     "factors": ["What transfers: general computer literacy, spatial thinking, understanding of drawing conventions.", "What doesn't transfer: the workflow. Revit is NOT 'AutoCAD with BIM on top.' It's a completely different approach.", "The biggest shift: in AutoCAD you DRAW lines. In Revit you PLACE intelligent objects.", "Timeline: expect 2-4 weeks to feel comfortable, 2-3 months to be productive.", "Don't try to use Revit like AutoCAD (detail lines everywhere) — learn the Revit way."],
     "sw_notes": [
         ("AutoCAD", "What you know: commands, coordinate input, layers, blocks, plotting. These concepts exist in Revit but work differently. Your spatial reasoning and precision habits transfer well."),
         ("Revit", "New concepts to learn: Families (like smart blocks), Levels/Grids (project skeleton), Views (not viewports), Parameters (dimensions that update everything). Start with the Revit basics course on LinkedIn Learning or Autodesk tutorials."),
     ],
     "recommendation": "Don't abandon AutoCAD — you'll still need it for details and site work. Add Revit on top. Start with a structured tutorial (not random YouTube videos) to learn the methodology correctly from day one. Practice by modeling a simple building you know well (your house, your school)."},

    {"slug": "from-autocad-to-gstarcad", "title": "Switching from AutoCAD to GstarCAD — What's Different?",
     "desc": "Considering GstarCAD as an AutoCAD alternative? What beginners and small firms need to know: command compatibility, DWG support, and what (little) changes.",
     "category": "Migration",
     "software": [("autocad", "AutoCAD"), ("gstarcad", "GstarCAD")],
     "intro": "GstarCAD is designed as a cost-effective AutoCAD alternative. If you know AutoCAD (or are learning it), switching to GstarCAD is remarkably easy. Here's what stays the same and what's different.",
     "factors": ["Same commands: LINE, CIRCLE, TRIM, OFFSET, HATCH — all work identically.", "Same file format: opens and saves DWG natively. Your drawings work perfectly.", "Same interface layout: ribbon tabs, command line, properties panel — all familiar.", "LISP routines: most AutoLISP scripts run without modification.", "What's different: some advanced features, plugin availability, and the price (much lower)."],
     "sw_notes": [
         ("AutoCAD", "What you know transfers almost 100% to GstarCAD. Same keyboard shortcuts, same concepts, same file format. If you can use AutoCAD, you can use GstarCAD immediately."),
         ("GstarCAD", "1/3-1/5 the cost of AutoCAD. Perpetual license option (pay once). Lighter on system resources. Very similar UI. Main limitation: fewer third-party plugins (most major verticals are available though)."),
     ],
     "recommendation": "If you're learning: the skills are identical — learn on whichever you have access to. If your firm is considering switching: the transition is nearly painless. Test your LISP routines and any specialized plugins first, but the core workflow needs zero retraining."},

    {"slug": "from-solidworks-to-fusion-360", "title": "SOLIDWORKS vs Fusion 360 — Differences for Beginners",
     "desc": "Coming from SOLIDWORKS to Fusion 360 (or vice versa)? Key differences in workflow, file management, and features explained simply for learners.",
     "category": "Migration",
     "software": [("solidworks", "SOLIDWORKS"), ("fusion-360", "Fusion 360")],
     "intro": "SOLIDWORKS and Fusion 360 are both parametric CAD tools that work similarly at their core. If you know one, learning the other is much easier than starting from scratch.",
     "factors": ["Both use: sketch → extrude → pattern workflow. Core modeling is very similar.", "File management: SOLIDWORKS uses local files. Fusion 360 uses cloud (Data Panel).", "Assembly: SOLIDWORKS has mates. Fusion 360 has joints. Same concept, different names.", "Fusion 360 adds CAM and PCB design built in. SOLIDWORKS needs add-ins for those.", "SOLIDWORKS is Windows-only. Fusion 360 works on Mac and Windows."],
     "sw_notes": [
         ("SOLIDWORKS", "Feature tree (left panel), PropertyManager (right panel), sketch relations, mates for assembly. Files saved locally. More features for advanced surfacing and simulation."),
         ("Fusion 360", "Timeline (bottom), Design workspace, sketch constraints, joints for assembly. Files saved to cloud. Integrated CAD+CAM+CAE in one tool. Free for personal use."),
     ],
     "recommendation": "The core skills transfer directly. What you learned about sketching, constraints, features, and assemblies works the same way in both. Give yourself 1-2 weeks to adjust to the different UI, and you'll be productive. Don't try to make one tool work like the other — learn each on its own terms."},
]


def generate_guide_page(guide):
    g = guide
    canonical = f"https://gstarcademy.com/kb/guides/{g['slug']}"
    
    # Software links
    sw_links = ""
    for slug, name in g["software"]:
        sw_links += f'<a href="../software/{slug}" style="display:inline-flex;align-items:center;gap:6px;padding:8px 14px;background:var(--ink-surface-2);border:1px solid var(--ink-line);border-radius:8px;text-decoration:none;color:var(--ink-text);font-size:13px;font-weight:500;">{name}</a>\n'
    
    # Factors as list
    factors_html = ""
    for f in g["factors"]:
        factors_html += f'<li style="margin-bottom:8px;">{f}</li>\n'
    
    # Software notes
    sw_notes_html = ""
    for name, note in g["sw_notes"]:
        sw_notes_html += f'''<div style="margin-bottom:16px;padding:16px 20px;background:var(--ink-surface-2);border:1px solid var(--ink-line);border-radius:10px;">
          <h3 style="margin:0 0 8px;font-size:0.95rem;">{name}</h3>
          <p style="margin:0;font-size:14px;line-height:1.7;">{note}</p>
        </div>\n'''
    
    html = f'''<!doctype html>
<html lang="en">
  <head>
    <link rel="preconnect" href="https://www.googletagmanager.com" />
    <link rel="dns-prefetch" href="https://www.googletagmanager.com" />
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}};window.gtag=gtag;window.addEventListener('load',function(){{const i=()=>{{const s=document.createElement('script');s.src='https://www.googletagmanager.com/gtag/js?id=G-ZV3YR72933';s.async=true;document.head.appendChild(s);gtag('js',new Date());gtag('config','G-ZV3YR72933');}};'requestIdleCallback' in window?requestIdleCallback(i):setTimeout(i,1);}});</script>
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
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://gstarcademy.com/"}},{{"@type":"ListItem","position":2,"name":"Knowledge Base","item":"https://gstarcademy.com/knowledge-base"}},{{"@type":"ListItem","position":3,"name":"Beginner Guides","item":"https://gstarcademy.com/kb/guides/"}},{{"@type":"ListItem","position":4,"name":"{g['title']}","item":"{canonical}"}}]}}</script>
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

    <main class="container" style="margin-top:32px;max-width:920px;">
      <nav class="kb-faq-breadcrumbs" aria-label="Breadcrumb">
        <a href="../../">Home</a> /
        <a href="../../knowledge-base">Knowledge Base</a> /
        <a href="./">Beginner Guides</a> /
        <span aria-current="page">{g['category']}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom:28px;">
          <span class="chip pill-warn">Beginner Guide &middot; {g['category']}</span>
          <h1 style="margin-top:12px;">{g['title']}</h1>
          <p class="hero-sub">{g['desc']}</p>
        </header>

        <div class="ink-byline" role="contentinfo">
          <span><strong>By</strong> Gstarcademy Editorial Team</span>
          <span><strong>Updated</strong> <time datetime="{TODAY}">{TODAY}</time></span>
          <span><a href="../../editorial-process">Editorial process</a></span>
        </div>

        <section class="kb-concept-section">
          <h2>Who This Guide Is For</h2>
          <p>{g['intro']}</p>
        </section>

        <section class="kb-concept-section">
          <h2>Software Covered</h2>
          <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px;">
            {sw_links}
          </div>
        </section>

        <section class="kb-concept-section">
          <h2>Key Things to Consider</h2>
          <ul style="list-style:none;padding:0;">
            {factors_html}
          </ul>
        </section>

        <section class="kb-concept-section">
          <h2>Your Options Explained</h2>
          {sw_notes_html}
        </section>

        <section class="kb-concept-section">
          <h2>Our Recommendation</h2>
          <div style="padding:16px 20px;background:var(--accent-bg, #f0f9ff);border:1px solid var(--accent, #0284c7);border-radius:10px;">
            <p style="margin:0;font-size:14px;line-height:1.8;font-weight:500;">{g['recommendation']}</p>
          </div>
        </section>

        <section class="kb-concept-section" style="margin-top:32px;">
          <h2>Next Steps</h2>
          <p>Ready to start learning? Check out our <a href="../learning-paths/">structured learning paths</a> for step-by-step beginner courses in each software. Or browse the <a href="../faq/">FAQ section</a> for answers to common "how do I..." questions.</p>
        </section>

        <aside style="margin-top:32px;padding:20px 24px;background:var(--ink-surface-2);border:1px solid var(--ink-line);border-radius:14px;">
          <p style="font-size:12px;font-weight:600;margin:0 0 4px;">Gstarcademy Editorial Team</p>
          <p style="font-size:11px;color:var(--ink-text-soft);margin:0;">Written for beginners with no prior CAD experience. <a href="../../editorial-process" style="color:var(--accent);">Editorial guidelines</a>. Last updated: <time datetime="{TODAY}">{TODAY}</time></p>
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
    by_cat = {}
    for g in GUIDES:
        cat = g["category"]
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(g)
    
    links = ""
    for cat, guides in sorted(by_cat.items()):
        links += f'<h3 style="margin-top:20px;">{cat}</h3><ul style="list-style:none;padding:0;">\n'
        for g in guides:
            links += f'<li style="margin-bottom:8px;"><a href="./{g["slug"]}" style="color:var(--accent);font-weight:500;">{g["title"]}</a><br><span style="font-size:12px;color:var(--ink-text-soft);">{g["desc"][:100]}...</span></li>\n'
        links += '</ul>\n'
    
    html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CAD Beginner Guides — Choose the Right Software | Gstarcademy</title>
    <meta name="description" content="Beginner-friendly guides to choosing CAD software: by industry, budget, and project type. Written for complete beginners with no prior experience." />
    <link rel="canonical" href="https://gstarcademy.com/kb/guides/" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="stylesheet" href="../../styles.min.css" />
  </head>
  <body>
    <div class="page-shell"><header class="topbar"><div class="container topbar-inner"><a class="brand" href="../../"><span class="brand-badge">GC</span><span>Gstarcademy</span></a><nav class="nav"><a class="nav-link" href="../../">Home</a><a class="nav-link active" href="../../knowledge-base">Wiki</a><a class="nav-link" href="../../tutorials">Tutorials</a><a class="nav-link" href="../../news">News</a><a class="nav-link" href="../../about">About</a></nav></div></header></div>
    <main class="container" style="margin-top:32px;max-width:920px;">
      <h1>Beginner Guides</h1>
      <p style="color:var(--ink-text-soft);font-size:15px;">No prior CAD experience needed. These guides help you choose the right software and get started learning.</p>
      {links}
    </main>
    <footer class="footer site-footer"><div class="container site-footer-bottom"><p>&copy; Gstarcademy.</p></div></footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    print(f"Rewriting {len(GUIDES)} guide pages as beginner-friendly content...")
    for g in GUIDES:
        html = generate_guide_page(g)
        filepath = os.path.join(OUTPUT_DIR, f"{g['slug']}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    generate_index()
    print(f"Done! Rewrote {len(GUIDES)} guides + index as beginner-level content")


if __name__ == '__main__':
    main()
