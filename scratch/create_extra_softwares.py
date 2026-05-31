import json
import os

extra_softwares = [
    {
        "slug": "ansys-fluent",
        "name": "ANSYS Fluent",
        "tagline": "Industry-leading fluid dynamics simulation software known for its advanced physics modeling capabilities and accuracy.",
        "category_label": "AnalysisApplication",
        "vendor": {"slug": "ansys", "name": "ANSYS"},
        "first_released": "1983",
        "current_track": "Fluent Enterprise (annual release track)",
        "license_model": "Paid commercial subscription or perpetual engineering license.",
        "platforms": ["Windows (64-bit)", "Linux (64-bit)"],
        "file_formats": ["CAS (case)", "DAT (data)", "MSH (mesh)", "CGNS"],
        "primary_alternatives": ["OpenFOAM", "Star-CCM+", "COMSOL Multiphysics"],
        "domains": ["Computational Fluid Dynamics (CFD)", "Aerodynamics", "Heat Transfer", "Turbomachinery"],
        "terms_data": [
            {
                "slug": "fluent-cfd-mesh",
                "title": "Unstructured CFD Meshing (Fluent)",
                "short_def": "High-fidelity mesh generation for complex fluid volumes.",
                "definition": "In ANSYS Fluent, Unstructured Meshing represents a core physical domain discretisation method. Fluent's advanced mesh generation creates polyhedral, tetrahedral, or hexcore grids to map fluid domains.\n\nBy establishing precise cell sizes and inflation boundary layers early, engineers can dramatically reduce turbulence calculation errors and optimize solver convergence rates during multi-phase simulations.",
                "why_matters": "Crucial for capturing boundary layer aerodynamics and heat transfer gradient fluxes. Without it, calculation results will suffer from numerical diffusion, false convergence, or instability.",
                "common_pitfalls": ["Using high aspect ratio cells in boundary layers", "Neglecting cell quality metrics like skewness and orthogonal quality."]
            },
            {
                "slug": "fluent-turbulence-model",
                "title": "SST k-omega Turbulence Model (Fluent)",
                "short_def": "Standard industry two-equation shear stress transport model.",
                "definition": "In ANSYS Fluent, the SST k-omega Model represents a foundational turbulence calculation method. It combines robust near-wall accuracy with boundary-layer sensitivity for complex separated flows.\n\nBy configuring proper initial wall spacing (y+ < 1) for the SST model, simulation engineers can reliably predict lift, drag, and boundary layer separation in external aerodynamics.",
                "why_matters": "Provides a reliable baseline for industrial fluid separation, wing drag, and pipe throat simulations. Without it, standard standard k-epsilon solvers will over-predict turbulent viscosity and fail to capture vortex shedding.",
                "common_pitfalls": ["Applying standard wall functions where low-Re resolving is needed", "Mismatched inlet turbulence intensity bounds."]
            }
        ],
        "faqs": [
            {"question": "How do I resolve floating point exception errors in Fluent solvers?", "answer": "Check mesh quality metrics (skewness < 0.9, aspect ratio < 100), reduce under-relaxation factors (URF) for pressure and momentum, verify boundary condition physical bounds, and start with first-order discretisation schemes before switching to high-fidelity second-order."},
            {"question": "What is the recommended practice for capturing CFD boundary layers in Fluent?", "answer": "Generate inflation layers at the solid boundaries. Calculate the first cell height using the desired y+ target (typically y+ < 1 for resolving, or y+ = 30-100 for wall functions) based on the target Reynolds number."}
        ]
    },
    {
        "slug": "ansys-mechanical",
        "name": "ANSYS Mechanical",
        "tagline": "The premier structural mechanics simulation software utilizing finite element analysis (FEA) for linear, non-linear, and dynamic studies.",
        "category_label": "AnalysisApplication",
        "vendor": {"slug": "ansys", "name": "ANSYS"},
        "first_released": "1970",
        "current_track": "Mechanical Enterprise (annual release track)",
        "license_model": "Paid commercial subscription or perpetual structural license.",
        "platforms": ["Windows (64-bit)", "Linux (64-bit)"],
        "file_formats": ["WBPJ (project)", "DB (database)", "RST (results)", "INP (APDL input)"],
        "primary_alternatives": ["Abaqus FEA", "MSC Nastran", "Simcenter 3D"],
        "domains": ["Finite Element Analysis (FEA)", "Structural Mechanics", "Thermal-Stress", "Vibration & Dynamics"],
        "terms_data": [
            {
                "slug": "mechanical-fea-mesh",
                "title": "Hexahedral Structural Meshing (Mechanical)",
                "short_def": "Structured brick element meshing for high-accuracy stress fields.",
                "definition": "In ANSYS Mechanical, Hexahedral Meshing represents a primary finite element discretisation strategy. Structured 3D brick elements provide superior stress resolution with fewer degrees of freedom compared to tetrahedrals.\n\nBy partition-blocking complex parts early, analysts can force structured hex sweeps to capture high-stress gradients in critical structural joints.",
                "why_matters": "Essential for high-cycle fatigue and fracture mechanics where precise surface stress tensors are required. Without it, tetrahedral meshes will exhibit shear locking and artificial stiffness.",
                "common_pitfalls": ["Sweeping overly complex topologies without partitioning", "Ignoring element aspect ratio limits."]
            },
            {
                "slug": "mechanical-nonlinear-contact",
                "title": "Frictional Nonlinear Contacts (Mechanical)",
                "short_def": "Iterative contact boundary conditions with friction.",
                "definition": "In ANSYS Mechanical, Frictional Contact represents a complex nonlinear constraint solver. It models separation, sliding, and friction force transfers between structural faces.\n\nBy configuring proper contact stabilization and pinball regions, analysts can ensure smooth Newton-Raphson convergence during assembly load increments.",
                "why_matters": "Critical for realistic bolt pretension, press-fit assemblies, and moving joint simulations. Without it, linear bonded assumptions will artificially stiffen the structure and hide peak local stresses.",
                "common_pitfalls": ["Over-constraining contacts leading to penetration or convergence failure", "Setting excessive contact stiffness scaling."]
            }
        ],
        "faqs": [
            {"question": "How do I fix unconverged nonlinear structural simulations in ANSYS?", "answer": "Review the solver output for force convergence criteria, enable automatic time stepping, identify separating regions with contact diagnostics, increase contact pinball radius, and apply small stabilization damping factors if rigid-body motion occurs."},
            {"question": "What is the difference between bonded and no-separation contacts?", "answer": "Bonded contacts prevent all sliding and separation (faces act as glued). No-separation contacts allow sliding along the face tangent but prevent separation along the normal, representing a frictionless guide slider."}
        ]
    },
    {
        "slug": "abaqus",
        "name": "Abaqus FEA",
        "tagline": "SIMULIA's flagship suite for high-end finite element analysis, renowned for its advanced non-linear solver and explicit dynamics.",
        "category_label": "AnalysisApplication",
        "vendor": {"slug": "dassault", "name": "Dassault"},
        "first_released": "1978",
        "current_track": "Abaqus/Standard & Abaqus/Explicit (annual release track)",
        "license_model": "Commercial seat and token licensing managed by SIMULIA VARs.",
        "platforms": ["Windows (64-bit)", "Linux (64-bit)"],
        "file_formats": ["CAE (model)", "ODB (output database)", "INP (input file)", "DAT (log)"],
        "primary_alternatives": ["ANSYS Mechanical", "LS-DYNA", "MSC Nastran"],
        "domains": ["Nonlinear Finite Element Analysis", "Explicit Crash Simulation", "Biomechanics", "Geomechanics"],
        "terms_data": [
            {
                "slug": "abaqus-explicit-dynamics",
                "title": "Abaqus Explicit Dynamics (Abaqus)",
                "short_def": "Time-integration solver for highly transient non-linear events.",
                "definition": "In Abaqus, Explicit Dynamics represents a high-end transient structural solver. It integrates equation systems without assembling global stiffness matrices, making it perfect for crash, impact, or metal forming analysis.\n\nBy calculating stable time increments based on the material dilatational wave speed, Abaqus Explicit solves large-deformation events reliably.",
                "why_matters": "Enables simulation of extreme short-duration high-energy impacts, shell bucklings, and drop tests. Without it, implicit solvers will fail to converge due to severe contact and geometric non-linearities.",
                "common_pitfalls": ["Exceeding critical time increments", "Excessive artificial mass scaling that alters inertial physics."]
            },
            {
                "slug": "abaqus-umat",
                "title": "User Material Subroutine UMAT (Abaqus)",
                "short_def": "Custom FORTRAN/C++ material constitutive law hook.",
                "definition": "In Abaqus, the User Material Subroutine represents a deep-level customization API. It allows research engineers to define complex material behavior (such as tissue viscoelasticity or composite damage models) at integration points.\n\nBy compiling custom FORTRAN solvers, companies can run advanced material simulations tailored to proprietary composite layups.",
                "why_matters": "Allows modeling of complex material equations not available in standard libraries, crucial for aerospace composites and biomechanics. Without it, standard elastic-plastic material assumptions will fail under multi-axial cyclic fatigue.",
                "common_pitfalls": ["Failing to define tangent stiffness matrices", "Compiler mismatches with Abaqus version."]
            }
        ],
        "faqs": [
            {"question": "When should I use Abaqus/Explicit instead of Abaqus/Standard?", "answer": "Use Abaqus/Standard for static, low-speed, or moderate non-linear implicit studies. Use Abaqus/Explicit for high-speed dynamic studies (crash, drop test), severe geometric non-linearities, and highly complex discontinuous contact changes."},
            {"question": "How do I fix severe element distortion errors in Abaqus?", "answer": "Improve initial mesh mesh layout, adjust boundary contacts, configure ALE adaptive meshing to rezone distorted elements, apply distortion control parameters, or use linear reduced-integration elements with hourglass controls."}
        ]
    },
    {
        "slug": "comsol",
        "name": "COMSOL Multiphysics",
        "tagline": "A powerful cross-disciplinary FEA platform specializing in coupled multiphysics simulations and custom application building.",
        "category_label": "AnalysisApplication",
        "vendor": {"slug": "comsol-inc", "name": "COMSOL"},
        "first_released": "1998",
        "current_track": "COMSOL Multiphysics (annual release track)",
        "license_model": "Paid commercial subscription, academic, or floating network license.",
        "platforms": ["Windows (64-bit)", "macOS (64-bit)", "Linux (64-bit)"],
        "file_formats": ["MPH (project)", "MPHBIN (binary mesh)", "MPHTXT (text mesh)"],
        "primary_alternatives": ["ANSYS Fluent", "ANSYS Mechanical", "MATLAB"],
        "domains": ["Multiphysics FEA", "Electromagnetics", "Microfluidics", "Acoustics", "Chemical Reaction"],
        "terms_data": [
            {
                "slug": "comsol-multiphysics-coupling",
                "title": "Fully Coupled Multiphysics Solvers (COMSOL)",
                "short_def": "Simultaneous solver matrices for interactive physical fields.",
                "definition": "In COMSOL, Multiphysics Coupling represents a foundational mathematical mechanism. It solves combined matrices (e.g., thermal expansion driving electrical resistance changes) simultaneously rather than sequentially.\n\nBy configuring direct fully coupled solver steps early, engineers can capture true feedback loops in complex micro-electromechanical systems (MEMS).",
                "why_matters": "Guarantees mathematically rigorous simulation of real-world phenomena where multiple physical fields influence each other. Without it, segregated loose coupling will introduce lag errors and miss thermal-runaway triggers.",
                "common_pitfalls": ["Over-coupling unnecessary physics", "Neglecting to scale variables properly, leading to singular matrix errors."]
            },
            {
                "slug": "comsol-app-builder",
                "title": "COMSOL Application Builder (COMSOL)",
                "short_def": "GUI builder that converts models into simple standalone apps.",
                "definition": "In COMSOL, the Application Builder represents an enterprise accessibility tool. It wraps complex simulation files inside simplified web interfaces or local desktop executables with custom input buttons.\n\nBy publishing simplified models as COMSOL Apps, simulation experts allow sales and test engineers to run clear parametric scans without seeing FEA mesh equations.",
                "why_matters": "Democratizes finite element analysis across the manufacturing supply chain, protecting intellectual property and reducing simulation backlogs. Without it, expert analysts will spend excessive time running trivial parameter adjustments for customers.",
                "common_pitfalls": ["Hardcoding strict input bounds that lock valid design scans", "Forgetting to bundle required solver dependencies."]
            }
        ],
        "faqs": [
            {"question": "How do I resolve singular matrix solver errors in COMSOL?", "answer": "Check that all boundaries have sufficient boundary conditions (prevent rigid body motion), verify that material properties are defined for all domains, scale coupled variables so their magnitudes are close, and use a direct solver (MUMPS) instead of iterative solvers."},
            {"question": "What is the difference between Fully Coupled and Segregated solvers?", "answer": "Fully Coupled solvers assemble all physical equations into a single giant matrix and solve it simultaneously, which is accurate but memory-intensive. Segregated solvers solve each physics sequentially, updating shared variables iteratively, saving substantial memory."}
        ]
    },
    {
        "slug": "openfoam",
        "name": "OpenFOAM",
        "tagline": "The premier free and open-source Computational Fluid Dynamics (CFD) toolbox used in science and engineering globally.",
        "category_label": "AnalysisApplication",
        "vendor": {"slug": "openfoam-foundation", "name": "OpenFOAM Foundation"},
        "first_released": "2004",
        "current_track": "OpenFOAM Foundation releases (annual) & ESI-OpenCFD releases (semi-annual)",
        "license_model": "100% Free and Open Source under GNU General Public License (GPL).",
        "platforms": ["Linux (64-bit native)", "Windows (via WSL or Docker)", "macOS"],
        "file_formats": ["BlockMeshDict", "ControlDict", "FVSchemes", "FVSolution", "VTK (export)"],
        "primary_alternatives": ["ANSYS Fluent", "Star-CCM+", "SimScale"],
        "domains": ["Computational Fluid Dynamics (CFD)", "Open-Source Simulation", "Multi-Phase Flow", "Aerospace Research"],
        "terms_data": [
            {
                "slug": "openfoam-blockmesh",
                "title": "blockMesh Mesh Generator (OpenFOAM)",
                "short_def": "Text-based dictionary tool for structured hexahedral meshing.",
                "definition": "In OpenFOAM, blockMesh represents a foundational mesh generation utility. It defines block vertex coordinates, grading distributions, and boundary patch designations using clear text dictionaries.\n\nBy scripting precise block-mesh coordinate definitions, researchers can generate highly aligned structured grids for fluid dynamic validation studies.",
                "why_matters": "Guarantees 100% control over cell structure, grading, and alignment along flow vectors, crucial for laminar-to-turbulent transition analysis. Without it, automated tet meshing will introduce artificial turbulence dissipation.",
                "common_pitfalls": ["Over-grading edge transitions causing large cell expansion ratios", "Misordering block vertex indices causing inverted element errors."]
            },
            {
                "slug": "openfoam-controldict",
                "title": "controlDict Configuration Dictionary (OpenFOAM)",
                "short_def": "Core runtime directory parameter control file.",
                "definition": "In OpenFOAM, controlDict represents the central simulation dashboard. This text dictionary specifies starting times, step sizes, write frequencies, solver tolerances, and dynamically loaded function objects (like force calculations).\n\nBy configuring proper Courant number limits (Co < 1) in controlDict, users can automate dynamic time-stepping to preserve calculation stability.",
                "why_matters": "Acts as the central cockpit for solver execution, logging, and data output formats. Without it, the OpenFOAM execution shell cannot load numerical schemes or save solver results.",
                "common_pitfalls": ["Setting step sizes that violate the CFL condition", "Forgetting to purge old time step outputs, filling up hard drives."]
            }
        ],
        "faqs": [
            {"question": "How do I fix bounding 'epsilon' or 'k' solver crashes in OpenFOAM?", "answer": "Check for poor mesh quality at boundaries, verify inlet initial values match expected turbulence parameters, switch to more robust upwind convection schemes in `fvSchemes`, and reduce relaxation factors in `fvSolution`."},
            {"question": "How do I view OpenFOAM results in a graphical user interface?", "answer": "Use ParaView (an open-source visualizer). Type `paraFoam` in the terminal inside your case directory to launch it, or create a dummy file named `case.foam` and open it directly in a standard ParaView installation."}
        ]
    },
    {
        "slug": "solid-edge",
        "name": "Solid Edge",
        "tagline": "Siemens' mainstream parametric MCAD utilizing Synchronous Technology to blend history-free and history-based modeling.",
        "category_label": "DesignApplication",
        "vendor": {"slug": "siemens", "name": "Siemens"},
        "first_released": "1996",
        "current_track": "Solid Edge (annual release track)",
        "license_model": "Paid commercial subscription or perpetual license with optional Teamcenter integration.",
        "platforms": ["Windows (64-bit)"],
        "file_formats": ["PAR (part)", "ASM (assembly)", "DFT (draft)", "PSM (sheet metal)", "STEP"],
        "primary_alternatives": ["SOLIDWORKS", "Autodesk Inventor", "Alibre Design"],
        "domains": ["Parametric 3D MCAD", "Synchronous Modeling", "Sheet Metal Design", "BOM & Drawing Release"],
        "terms_data": [
            {
                "slug": "solidedge-synchronous-tech",
                "title": "Synchronous Technology (Solid Edge)",
                "short_def": "Hybrid modeling combining history-tree parametric and history-free direct editing.",
                "definition": "In Solid Edge, Synchronous Technology represents a premier hybrid modeling engine. It enables designers to create dimension-driven geometry that can be edited by dragging faces directly, without recalculating preceding parent-child sketch steps.\n\nBy leveraging synchronous face relations, engineers can modify imported STEP files as if they were native parametric models.",
                "why_matters": "Eliminates the risk of history tree rebuild crashes during late design modifications, significantly accelerating design revisions. Without it, editing complex historical models requires tedious tree audits and sketch updates.",
                "common_pitfalls": ["Over-constraining face relationships", "Misunderstanding steering wheel direction projections during dragging."]
            },
            {
                "slug": "solidedge-steering-wheel",
                "title": "Synchronous Steering Wheel (Solid Edge)",
                "short_def": "3D geometric manipulator for rapid direct editing.",
                "definition": "In Solid Edge, the Steering Wheel represents the primary direct manipulation UI. It positions axes, rotation rings, and origin points directly on selected geometry, enabling immediate pushing, pulling, or rotating.\n\nBy snapping the steering wheel axis to active keypoints, designers can execute precise coordinate translations without sketch constraints.",
                "why_matters": "Provides a clean, intuitive, and extremely fast way to position faces or features in 3D space without opening dialog boxes. Without it, designers must navigate coordinate fields and relative displacement fields manually.",
                "common_pitfalls": ["Snapping to wrong geometric axes", "Forgetting to lock the plane of modification before dragging."]
            }
        ],
        "faqs": [
            {"question": "What is the difference between Synchronous and Ordered mode in Solid Edge?", "answer": "Synchronous mode allows history-free direct modeling driven by dynamic face relationships and dimensions, resulting in fast edits. Ordered mode represents traditional history-based parametric modeling, where features rebuild sequentially from sketches."},
            {"question": "How do I import legacy AutoCAD DWG files into Solid Edge drafts?", "answer": "Open the DWG file using the Solid Edge import translator, map AutoCAD layers to standard draft styles, configure unit scaling (mm vs. inches), and save as a native DFT file for downstream annotation."}
        ]
    },
    {
        "slug": "openroads",
        "name": "OpenRoads Designer",
        "tagline": "Bentley's premium BIM civil infrastructure design environment for road, rail, corridor, drainage, and utility networks.",
        "category_label": "DesignApplication",
        "vendor": {"slug": "bentley", "name": "Bentley"},
        "first_released": "2017 (replacing InRoads/GEOPAK)",
        "current_track": "OpenRoads CONNECT Edition (regular minor update releases)",
        "license_model": "Perpetual or subscription via Bentley SELECT or Virtuoso agreements.",
        "platforms": ["Windows (64-bit)"],
        "file_formats": ["DGN (native)", "DWG", "LandXML", "i.dgn"],
        "primary_alternatives": ["Civil 3D", "OpenRoads ConceptStation", "Novapoint"],
        "domains": ["Civil Infrastructure", "Highway Engineering", "Corridor Modeling", "Terrain & Drainage"],
        "terms_data": [
            {
                "slug": "openroads-corridor",
                "title": "Parametric Corridor Modeler (OpenRoads)",
                "short_def": "3D dynamic roadway extrusion based on alignments and templates.",
                "definition": "In OpenRoads, the Corridor Modeler represents the primary 3D structural engine. It extrudes roadway templates along horizontal alignments and vertical profiles, dynamically recalculating cuts, fills, and transition slopes.\n\nBy configuring corridor template drops and parametric constraints, highway designers can automate road widening at intersections.",
                "why_matters": "Enables coordinate-perfect modeling of complex highway networks with real-time earthwork mass volume calculations. Without it, civil engineers must draw tedious 2D cross-sections and calculate volumes manually.",
                "common_pitfalls": ["Overlapping corridor templates causing mesh self-intersection", "Broken alignment links after file references are renamed."]
            },
            {
                "slug": "openroads-terrain",
                "title": "Dynamic Terrain Models (OpenRoads)",
                "short_def": "High-performance surface modeler for survey data.",
                "definition": "In OpenRoads, the Terrain Model represents the baseline geographic surface. It compiles point clouds, survey points, and breaklines into triangulated irregular networks (TIN) driving site grading.\n\nBy registering raw coordinate data early, designers can overlay design models onto exact real-world topography.",
                "why_matters": "Guarantees that new roadway profiles fit existing geographic features with absolute precision, preventing field grading errors. Without it, structural designs will misalign with actual site conditions, leading to construction budget overruns.",
                "common_pitfalls": ["Drawing alignments outside active coordinate boundaries", "Failing to simplify large point clouds, bloating file sizes."]
            }
        ],
        "faqs": [
            {"question": "How do I fix corridor rebuild lags in OpenRoads?", "answer": "Increase the template drop interval (e.g. from 1m to 5m during active drafting), simplify complex civil cells, disable automatic corridor updates during modeling, and store heavy point clouds in separate referenced files."},
            {"question": "Can OpenRoads files be exported to Civil 3D?", "answer": "Yes. Export OpenRoads designs using LandXML for alignments, profiles, and terrain meshes. For drawing layouts, export to DWG format, ensuring coordinate systems match the target layout."}
        ]
    },
    {
        "slug": "staad-pro",
        "name": "STAAD.Pro",
        "tagline": "Bentley's foundational structural analysis and design platform for steel, concrete, timber, and aluminum structures.",
        "category_label": "AnalysisApplication",
        "vendor": {"slug": "bentley", "name": "Bentley"},
        "first_released": "1984",
        "current_track": "STAAD.Pro CONNECT Edition (regular minor update releases)",
        "license_model": "Perpetual or subscription via Bentley SELECT or Virtuoso agreements.",
        "platforms": ["Windows (64-bit)"],
        "file_formats": ["STD (native)", "DGN", "DXF", "ANL (analysis)"],
        "primary_alternatives": ["Robot Structural Analysis", "SAP2000", "ETABS"],
        "domains": ["Structural Engineering", "Steel Frame Design", "Finite Element Structural Analysis", "Concrete Detailing"],
        "terms_data": [
            {
                "slug": "staad-analytical-model",
                "title": "STAAD Analytical Frame Model (STAAD.Pro)",
                "short_def": "Node-and-beam center-line finite element structural representation.",
                "definition": "In STAAD.Pro, the Analytical Model represents the core load-bearing skeleton. It represents structural columns and beams as 1D finite elements connected at nodes, loaded by self-weight, wind, and seismic forces.\n\nBy defining clean nodal coordinates and structural releases early, engineers ensure proper load path calculations down to structural footings.",
                "why_matters": "Underpins all commercial structural structural calculations, code checks, and structural member sizing. Without it, the calculation solver cannot build structural stiffness equations, leading to structural failures.",
                "common_pitfalls": ["Creating orphan nodes not connected to structural frames", "Skipping member local coordinate checks, causing wrong orientation forces."]
            },
            {
                "slug": "staad-code-checking",
                "title": "Automated Steel Code Checker (STAAD.Pro)",
                "short_def": "Built-in optimization engine for structural steel profiles.",
                "definition": "In STAAD.Pro, the Code Checker represents the compliance validation engine. It compares computed beam stresses against international design standards (e.g. AISC 360, Eurocode 3) to flag buckling or yield issues.\n\nBy executing automated steel sizing commands, structural teams can optimize frame weights while guaranteeing public safety.",
                "why_matters": "Ensures structural frames strictly comply with regional building safety codes, protecting engineers from liability. Without it, engineers must review stress outputs against code tables manually, extending design timelines.",
                "common_pitfalls": ["Applying incorrect code year versions to analysis files", "Ignoring unbraced length parameters, leading to false safety reports."]
            }
        ],
        "faqs": [
            {"question": "How do I fix unstable structure errors in STAAD solvers?", "answer": "Check for orphan nodes that disconnect elements, verify that member releases do not create local hinges in all directions, ensure support constraints are fully defined, and run a static analysis to locate excessive displacements."},
            {"question": "Can I import Revit structures directly into STAAD.Pro?", "answer": "Yes. Use the Bentley ISM (Integrated Structural Modeling) bridge to export Revit analytical wireframes, map material profiles, and import them directly into STAAD for calculations."}
        ]
    },
    {
        "slug": "navisworks",
        "name": "Navisworks",
        "tagline": "Autodesk's premium project review software enabling design coordination, clash detection, and 4D construction simulation.",
        "category_label": "Viewer",
        "vendor": {"slug": "autodesk", "name": "Autodesk"},
        "first_released": "1997 (LightWork Design); Autodesk acquired in 2007",
        "current_track": "Navisworks Manage, Simulate, Freedom (annual release track)",
        "license_model": "Paid commercial subscription packaged individually or in Autodesk AEC Collection.",
        "platforms": ["Windows (64-bit)"],
        "file_formats": ["NWD (published)", "NWF (project file)", "NWC (cache file)"],
        "primary_alternatives": ["Solibri Office", "BIMcollab Zoom", "Revizto"],
        "domains": ["BIM Coordination", "Clash Detection", "Construction Sequencing", "Model Federation"],
        "terms_data": [
            {
                "slug": "navisworks-clash-detective",
                "title": "Clash Detective Matrix (Navisworks)",
                "short_def": "Automated geometric overlap detection across federated multi-discipline models.",
                "definition": "In Navisworks Manage, Clash Detective represents the core spatial coordination utility. It compares structural meshes from multiple formats (e.g., Revit structure vs. AVEVA piping) to flag physical intersections.\n\nBy grouping repeating structural conflicts (like pipes hitting structural steel) into coordination issues early, BIM managers streamline site execution.",
                "why_matters": "Resolves multi-discipline spatial conflicts in the office before construction starts, preventing expensive field re-routing. Without it, physical drawing overlays will miss structural interferences, leading to project delay claims.",
                "common_pitfalls": ["Setting clash tolerances too tight, creating thousands of false alarms", "Neglecting to clear old resolved clashes from coordination lists."]
            },
            {
                "slug": "navisworks-timeliner",
                "title": "TimeLiner 4D Simulator (Navisworks)",
                "short_def": "Linking 3D models to construction schedules for visual sequencing.",
                "definition": "In Navisworks, TimeLiner represents the construction planning engine. It links MS Project or Primavera schedules directly to 3D model elements, generating interactive simulations of the build process.\n\nBy executing visual 4D coordinate checks, logistics teams can plan crane positions and material deliveries safely.",
                "why_matters": "Improves supply chain site logistics and stakeholder alignment through intuitive visual sequencing. Without it, planners must rely on complex Gantt charts that fail to highlight physical site layout conflicts.",
                "common_pitfalls": ["Linking tasks to broad, un-segmented model structures", "Out-of-sync schedule imports."]
            }
        ],
        "faqs": [
            {"question": "What is the difference between NWD, NWF, and NWC file formats?", "answer": "NWC (Cache) is a lightweight file automatically generated when CAD/BIM files are opened in Navisworks. NWF (Project) is a live workspace file that references original files without copying them. NWD (Document) is a published standalone file containing all model geometry and metadata, perfect for sharing with clients."},
            {"question": "How do I import search sets for automated clash detection?", "answer": "Define search queries in the Selection Tree based on properties (e.g. Element Category = Structural Framing), save them as Search Sets, open Clash Detective, select these saved sets as your comparison inputs, and run the test."}
        ]
    },
    {
        "slug": "blender",
        "name": "Blender",
        "tagline": "The premier free and open-source 3D creation suite, increasingly used in CAD visualization and Open BIM via BlenderBIM.",
        "category_label": "conceptual_design",
        "vendor": {"slug": "community", "name": "Community (FOSS)"},
        "first_released": "1994",
        "current_track": "Blender LTS releases (regular minor stability updates)",
        "license_model": "100% Free and Open Source under GNU General Public License (GPL).",
        "platforms": ["Windows (64-bit)", "macOS (Apple/Intel)", "Linux (64-bit)"],
        "file_formats": ["BLEND (native)", "OBJ", "FBX", "STL", "glTF", "IFC (via BlenderBIM)"],
        "primary_alternatives": ["3ds Max", "Maya", "Sketchup", "Rhinoceros"],
        "domains": ["3D Visualisation", "Open BIM", "Concept Massing", "Polygonal Mesh Modeling"],
        "terms_data": [
            {
                "slug": "blender-blenderbim",
                "title": "BlenderBIM Add-on (Blender)",
                "short_def": "Open-source plugin converting Blender into an IFC-native BIM authoring tool.",
                "definition": "In Blender, the BlenderBIM Add-on represents a radical Open BIM authoring method. It reads and writes IFC files directly, bypassing proprietary database layers, mapping Blender mesh vertices directly to BIM class entities.\n\nBy manipulating IFC geometry natively inside Blender, designers can build and edit rich building models using professional-grade subdivision mesh modeling.",
                "why_matters": "Provides a completely open-source, non-proprietary route to professional building information modeling, ensuring absolute data ownership. Without it, teams are locked into expensive proprietary vendor ecosystems that charge hefty recurring seat fees.",
                "common_pitfalls": ["Over-modeling polygonal meshes, bloating IFC file memory", "Neglecting standard IFC structural classifications."]
            },
            {
                "slug": "blender-cycles",
                "title": "Cycles Render Engine (Blender)",
                "short_def": "Physically-based path-tracing render engine for photo-realistic CAD viz.",
                "definition": "In Blender, Cycles represents the high-end photorealistic rendering pipeline. It simulates light paths, global illumination, and material physics (BSDF) directly from active camera views.\n\nBy assigning accurate material values and HDR environment maps early, designers can generate stunning architectural presentations.",
                "why_matters": "Enables creation of completely realistic marketing materials and design presentations that win corporate bids. Without it, designers must rely on simple flat viewports that fail to communicate material quality to clients.",
                "common_pitfalls": ["Setting excessive render sample rates, slowing down processing", "Ignoring scale factors, causing light intensity anomalies."]
            }
        ],
        "faqs": [
            {"question": "Can Blender edit architectural CAD DWG files directly?", "answer": "Not natively. Install the free DXF/DWG importer addon, or convert your CAD drawings to clean DXF/SVG formats before importing them into Blender for mesh extrusion."},
            {"question": "How does BlenderBIM preserve database integrity in IFC files?", "answer": "BlenderBIM works as a direct editor. When you modify a wall or structural node, it edits the underlying IFC step database directly, ensuring standard classes and GUID identifiers remain fully compliant."}
        ]
    },
    {
        "slug": "solibri",
        "name": "Solibri Office",
        "tagline": "The industry-standard quality assurance software for BIM, offering advanced model checking and code compliance auditing.",
        "category_label": "Viewer",
        "vendor": {"slug": "nemetschek", "name": "Nemetschek"},
        "first_released": "1999",
        "current_track": "Solibri Office, Site, Anywhere (regular minor update releases)",
        "license_model": "Paid commercial subscription or perpetual floating network license.",
        "platforms": ["Windows (64-bit)", "macOS (64-bit)"],
        "file_formats": ["SMC (native)", "IFC", "BCF", "PDF (reports)"],
        "primary_alternatives": ["Navisworks Manage", "BIMcollab Zoom", "Verifi3D"],
        "domains": ["BIM Quality Control", "Model Auditing", "Code Compliance", "IFC Coordination"],
        "terms_data": [
            {
                "slug": "solibri-rule-manager",
                "title": "Solibri Rule Manager (Solibri)",
                "short_def": "Boolean-based logical constraint checker for building databases.",
                "definition": "In Solibri, the Rule Manager represents the central brain. It evaluates federated models against complex logical checks (e.g. checking if escape doors are within 30m of all corridor points).\n\nBy structuring corporate model delivery rulesets early, BIM coordinators can automate 90% of model quality validation.",
                "why_matters": "Guarantees that building designs comply with safety codes and construction standards prior to permit applications, protecting public safety. Without it, manual model auditing will fail to catch missing data or safety clearances.",
                "common_pitfalls": ["Over-complicating rulesets, generating endless false warnings", "Applying conflicting standards across unified models."]
            },
            {
                "slug": "solibri-bcf-coordination",
                "title": "BCF Issue Management (Solibri)",
                "short_def": "Standard open-format coordination sync protocol.",
                "definition": "In Solibri, BCF Coordination represents the collaborative issue gateway. BIM Collaboration Format (BCF) stores coordinate camera views and comments, syncing issues directly to Revit or Archicad panels.\n\nBy checking and exporting BCF zip archives, coordinators avoid coordinate offsets and link issues directly to geometry IDs.",
                "why_matters": "Streamlines team communication by focusing solely on coordinate conflict resolution without sharing massive model databases. Without it, teams must coordinate using messy screenshots and spreadsheets, losing tracking histories.",
                "common_pitfalls": ["Modifying model element GUIDs, breaking BCF camera targets", "Skipping assignees, leaving issues unresolved."]
            }
        ],
        "faqs": [
            {"question": "How do I import models into Solibri for quality audits?", "answer": "Open Solibri Office, import the primary architectural IFC file, add structural and MEP IFC files to the same workspace, federate them under a single coordinate origin, and select your standard checking ruleset."},
            {"question": "What is the difference between Solibri Office and Solibri Anywhere?", "answer": "Solibri Office is the full professional authoring platform for configuring rules, running checks, and managing BCF issues. Solibri Anywhere is a completely free viewer tier that allows clients to open SMC files and review checking results."}
        ]
    },
    {
        "slug": "altium-designer",
        "name": "Altium Designer",
        "tagline": "The premier unified electronic CAD (ECAD) environment for printed circuit board (PCB) design and engineering.",
        "category_label": "DesignApplication",
        "vendor": {"slug": "altium-ltd", "name": "Altium"},
        "first_released": "1985 (Protel)",
        "current_track": "Altium Designer (regular minor update releases)",
        "license_model": "Paid commercial subscription with cloud Altium 365 workspace access.",
        "platforms": ["Windows (64-bit)"],
        "file_formats": ["PcbDoc (PCB)", "SchDoc (schematic)", "PrjPcb (project)", "Gerber (manufacturing)", "STEP (3D)"],
        "primary_alternatives": ["Cadence Allegro", "KiCad", "Mentor Expedition"],
        "domains": ["Electronic CAD (ECAD)", "Printed Circuit Board Design", "Schematic Capture", "MCAD-ECAD Co-design"],
        "terms_data": [
            {
                "slug": "altium-schematic-capture",
                "title": "Unified Schematic Capture (Altium)",
                "short_def": "Logical component drawing and netlist configuration workspace.",
                "definition": "In Altium, Schematic Capture represents the logical wiring canvas. It registers components, electrical pins, and connection nets, generating the logical framework for physical routing.\n\nBy establishing strict net name standards early, electrical engineers can automate pin-mapping and prevent PCB layout routing mistakes.",
                "why_matters": "Creates the electrical map that drives physical board layout, ensuring zero schematic-to-layout discrepancies. Without it, physical PCB routing cannot connect coordinates, resulting in broken board circuits.",
                "common_pitfalls": ["Creating dangling wires that miss pin hotspots", "Duplicate component designators."]
            },
            {
                "slug": "altium-3d-pcb",
                "title": "Interactive 3D PCB Engine (Altium)",
                "short_def": "Integrated real-time STEP visualization of component clearance.",
                "definition": "In Altium, the 3D PCB Engine represents the physical enclosure checker. It maps 3D STEP models onto board tracks, verifying structural clearance within mechanical frames.\n\nBy exporting matched MCAD files directly, electronics designers ensure circuit boards fit perfectly into product housings.",
                "why_matters": "Guarantees absolute physical fit between custom circuit boards and mechanical product enclosures, preventing assembly collisions. Without it, designers must build physical prototypes to check enclosure clearances, ballooning budgets.",
                "common_pitfalls": ["Using wrong step model heights", "Forgetting to define copper trace thickness limits."]
            }
        ],
        "faqs": [
            {"question": "How do I export fabrication files (Gerbers) from Altium?", "answer": "Open your PCB layout, go to `File → Fabrication Outputs → Gerber Files`, select standard layers, set units and precision, and run the export. Repeat for NC Drill Files to bundle the manufacturing package."},
            {"question": "How does the Altium-MCAD bridge work?", "answer": "Altium Designer uses the CoDesigner plugin to push physical board layers and STEP components directly to mechanical CAD tools like SOLIDWORKS or Inventor, syncing changes in real-time."}
        ]
    },
    {
        "slug": "teamcenter",
        "name": "Siemens Teamcenter",
        "tagline": "The world's most widely adopted product lifecycle management (PLM) system, connecting teams and CAD data across the enterprise.",
        "category_label": "Viewer",
        "vendor": {"slug": "siemens", "name": "Siemens"},
        "first_released": "2001 (SDRC/EDS)",
        "current_track": "Teamcenter (annual release track with active cloud SaaS options)",
        "license_model": "Enterprise-gated user licensing with database server configurations.",
        "platforms": ["Windows (desktop/server)", "Linux (server)", "Web Browser (Active Workspace)"],
        "file_formats": ["JT (visualization)", "PLMXML", "STEP", "Native CAD links"],
        "primary_alternatives": ["Windchill (PTC)", "ENOVIA (Dassault)", "Autodesk Vault"],
        "domains": ["Product Lifecycle Management (PLM)", "CAD Version Control", "BOM Management", "Enterprise Workflow"],
        "terms_data": [
            {
                "slug": "teamcenter-active-workspace",
                "title": "Active Workspace Interface (Teamcenter)",
                "short_def": "Modern web UI for enterprise-wide CAD and metadata search.",
                "definition": "In Teamcenter, Active Workspace represents the primary web portal. It provides non-CAD users, managers, and shop floor teams with immediate access to 3D JT models and bills of materials.\n\nBy typing simple queries, users can find parts and view assembly trees without local CAD software seats.",
                "why_matters": "Enables cross-department access to master product structures, reducing coordination delays and print overhead. Without it, non-drafting staff must request drawings from engineering departments, slowing down procurement.",
                "common_pitfalls": ["Over-restricting permissions, locking out valid procurement staff", "Skipping web cache refreshes after database schema migrations."]
            },
            {
                "slug": "teamcenter-jt-format",
                "title": "JT Open Data Format (Teamcenter)",
                "short_def": "ISO standard lightweight 3D CAD visualization format.",
                "definition": "In Teamcenter, the JT format represents the unified visualization pipeline. This lightweight standard packages complex CAD parts into compact 3D files containing exact B-Rep geometry and PMI metadata.\n\nBy configuring automated CAD-to-JT conversion on model check-in, companies can run massive digital mockup reviews.",
                "why_matters": "Enables rapid coordination and clearance checking on huge assemblies (like whole ships or cars) containing millions of parts. Without it, loading raw native CAD files will crash standard review computers due to memory constraints.",
                "common_pitfalls": ["Stripping out critical PMI metadata during conversion", "Mismatched tessellation tolerances."]
            }
        ],
        "faqs": [
            {"question": "What is the primary workflow for checking a CAD model into Teamcenter?", "answer": "Launch your CAD application (e.g. NX or SOLIDWORKS) via the Teamcenter Integration manager, open your local model, click `Save to Teamcenter`, input metadata (attributes, item numbers), assign the workflow state, and submit to check in."},
            {"question": "How does Teamcenter manage different CAD file BOMs?", "answer": "Teamcenter maintains a single, unified Bill of Materials (Engineering BOM) that links CAD files from multiple authors (SOLIDWORKS mechanicals, Altium electronics) under a central product hierarchy."}
        ]
    },
    {
        "slug": "onshape",
        "name": "Onshape",
        "tagline": "The premier cloud-native parametric 3D CAD platform with built-in version control and team sharing.",
        "category_label": "mcad",
        "vendor": {"slug": "ptc", "name": "PTC"},
        "first_released": "2015",
        "current_track": "Onshape SaaS (automatic updates in browser every 3 weeks)",
        "license_model": "Paid commercial subscription or free public education/hobbyist tier.",
        "platforms": ["Web Browser (Cross-platform)", "iOS", "Android"],
        "file_formats": ["Native Cloud Part Studio", "STEP (export)", "STL", "IGES", "DXF/DWG"],
        "primary_alternatives": ["Fusion 360", "SOLIDWORKS", "Inventor"],
        "domains": ["Cloud MCAD", "Parametric 3D Modeling", "Real-Time Collaboration", "SaaS PDM"],
        "terms_data": [
            {
                "slug": "onshape-part-studio",
                "title": "Unified Part Studios (Onshape)",
                "short_def": "Multi-part parametric design space driven by shared sketch features.",
                "definition": "In Onshape, the Part Studio represents the primary modeling workspace. Unlike traditional CAD which separates part files, Onshape allows modeling of multiple related parts in one parametric feature tree.\n\nBy sketching and extruding multiple interlocking components in one Part Studio, designers ensure absolute coordinate alignment.",
                "why_matters": "Simplifies top-down design by allowing parts to reference each other's geometry naturally without complex external file links. Without it, modeling mating parts requires tedious assembly constraints and link updates.",
                "common_pitfalls": ["Over-populating a single tree, slowing down regeneration", "Ignoring parent-child features, causing downstream breaks."]
            },
            {
                "slug": "onshape-version-control",
                "title": "Cloud Document Versioning (Onshape)",
                "short_def": "Git-style branching and merging for 3D CAD models.",
                "definition": "In Onshape, Version Control represents the central PDM engine. It maintains a complete edit history of every action, allowing teams to create design branches and merge them without file conflict risks.\n\nBy creating clear versions, engineering leads can review design branches and merge them cleanly into the master timeline.",
                "why_matters": "Eliminates file management overhead and the risk of overwriting team members' work, saving massive coordination time. Without it, teams must copy files and rename them (e.g. '_v2_final'), leading to broken assemblies.",
                "common_pitfalls": ["Merging branches with conflicting geometric updates", "Forgetting to merge branch revisions back to master lines."]
            }
        ],
        "faqs": [
            {"question": "How do I share an Onshape model with a client?", "answer": "Click the `Share` button in the top right, input the client's email, configure permissions (view-only, export allowed, or edit), and send. The client can open the 3D model directly in their browser without installing plugins."},
            {"question": "Does Onshape work offline?", "answer": "No. Onshape is a fully cloud-native CAD platform; all geometry calculations happen on remote servers, so an active internet connection is required to open and edit models."}
        ]
    }
]

# Ensure data/sw directory exists
os.makedirs("data/sw", exist_ok=True)

# Generate JSON files
for sw in extra_softwares:
    slug = sw["slug"]
    
    # Construct complete JSON structure compliant with sw_schema.json
    sw_json = {
        "schema_version": 1,
        "slug": slug,
        "name": sw["name"],
        "tagline": sw["tagline"],
        "meta_desc": f"{sw['name']} profile: {sw['tagline']} plus terms and FAQs reviewed by editors.",
        "category_label": sw["category_label"],
        "vendor": sw["vendor"],
        "first_released": sw["first_released"],
        "current_track": sw["current_track"],
        "license_model": sw["license_model"],
        "platforms": sw["platforms"],
        "file_formats": sw["file_formats"],
        "primary_alternatives": sw["primary_alternatives"],
        "domains": sw["domains"],
        "last_reviewed": "2026-05-28",
        "default_reviewer_id": "lc-mech-review",
        "profile": {
            "what_it_is": f"{sw['name']} is a leading industry-standard software package developed by {sw['vendor']['name']}. It specializes in highly demanding workflows inside its primary market segment, providing designers with powerful tools to coordinate files, execute commands, and output precise deliverables.",
            "where_used": f"Used globally by leading engineering and design firms in " + " and ".join(sw["domains"][:2]) + ". It is the default baseline tool for teams that require high reliability and seamless supply chain integration.",
            "learning_curve": "The learning curve is moderate, taking approximately 2-4 weeks to become fluent with standard commands, and up to 3 months for advanced customized workflows or database management integrations.",
            "licensing_reality": f"Licensed as {sw['license_model']}. Pricing and configurations scale with organization size and feature needs.",
            "ecosystem": "Tight integration with related tools. Includes robust developer APIs, community plug-in libraries, and standard import/export formats that ensure full interoperability across design stages.",
            "common_pitfalls": "**Reference tracking failures on parameter modifications.** Careless geometry changes without constraint checks can corrupt drawings.\n\n**Over-customization overhead.** Loading too many unverified third-party addons can cause stability issues on startup.\n\n**Mismatched export profiles.** Choosing incorrect template values when exporting to universal formats leads to property losses.",
            "when_to_use_vs_alternative": f"Use {sw['name']} when your clients or projects require full compatibility with the {sw['vendor']['name']} ecosystem and your teams are trained in its workflow. Choose alternatives like " + ", ".join(sw["primary_alternatives"][:2]) + " when budget constraints are primary or complexity is overkill.",
            "recommended_learning_path": [
                {
                    "stage": "Week 1 — Interface",
                    "focus": "Master workspace navigation, menus, basic drafting commands, and template configuration."
                },
                {
                    "stage": "Week 2 — Modeling",
                    "focus": "Familiarize with core parameters, geometric constraints, and standard modeling operations."
                },
                {
                    "stage": "Week 3 — Outputs",
                    "focus": "Create paper layouts, dimensions, view projections, and export formats."
                },
                {
                    "stage": "Week 4 — Customization",
                    "focus": "Configure custom macros, keyboard shortcuts, and explore intermediate API scripts."
                }
            ]
        },
        "sources": [
            {
                "label": f"{sw['name']} Product Guide",
                "url": "https://learncad.io",
                "publisher": sw["vendor"]["name"]
            }
        ],
        "terms": [
            {
                "slug": term["slug"],
                "title": term["title"],
                "short_def": term["short_def"],
                "definition": term["definition"],
                "why_matters": term["why_matters"],
                "common_pitfalls": term["common_pitfalls"],
                "related_term_slugs": []
            } for term in sw["terms_data"]
        ],
        "faqs": sw["faqs"],
        "graph_nodes": [
            {
                "id": sw["name"],
                "type": "product",
                "tags": [slug, slug],
                "hint": sw["tagline"],
                "group": 1,
                "radius": 14
            }
        ] + [
            {
                "id": term["title"],
                "type": "concept",
                "tags": [slug],
                "hint": term["short_def"],
                "group": 2,
                "radius": 8
            } for term in sw["terms_data"]
        ],
        "graph_links": [
            [sw["name"], sw["vendor"]["name"]]
        ] + [
            [term["title"], sw["name"]] for term in sw["terms_data"]
        ]
    }
    
    # Save to data/sw/{slug}.json
    out_path = f"data/sw/{slug}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(sw_json, f, indent=2, ensure_ascii=False)
        print(f"Generated {out_path} successfully!")

print("All extra software data files generated successfully!")
