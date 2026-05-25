import os

# Ensure kb/concepts directory exists
os.makedirs('kb/concepts', exist_ok=True)

TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} · CAD Concepts · Gstarcademy</title>
    <meta name="description" content="{description}" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="stylesheet" href="../../styles.css?v=20260506" />
  </head>
  <body data-page="knowledge" class="page-kb-concepts">
    <div class="header-stack">
      <aside
        class="site-notice"
        id="site-notice"
        data-notice-id="global-v2"
        aria-label="Announcement"
      >
        <div class="site-notice-inner container">
          <p class="site-notice-text">
            Tip: open the
            <a class="site-notice-link" href="../../tutorials">tutorial library</a>
            to filter by software, task, level, and source—then follow outbound links to the originals.
          </p>
          <button type="button" class="site-notice-close" aria-label="Dismiss announcement">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      </aside>
      <header class="topbar">
        <div class="container topbar-inner">
          <a class="brand" href="../../index">
            <span class="brand-badge">GC</span>
            <span>Gstarcademy</span>
          </a>
          <nav class="nav">
            <a class="nav-link" href="../../index">Home</a>
            <a class="nav-link" href="../../knowledge-base">Knowledge Base</a>
            <a class="nav-link" href="../../tutorials">Tutorials</a>
            <a class="nav-link" href="../../news">News</a>
          </nav>
        </div>
      </header>
    </div>

    <main class="container" style="margin-top: 32px; max-width: 900px;">
      <nav class="kb-faq-breadcrumbs" aria-label="Breadcrumb">
        <a href="../../index">Home</a> /
        <a href="../../knowledge-base">Knowledge Base</a> /
        <a href="../../kb-terms">Terms</a> /
        <span aria-current="page">{title}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 40px; border-bottom: 1px solid #e2e8f0; padding-bottom: 24px;">
          <span class="chip" style="margin-bottom: 12px; background: #e0f2fe; color: #0369a1; border-color: #bae6fd;">{category}</span>
          <h1 style="font-size: 2.5rem; margin-bottom: 12px; color: #0f172a;">{title}</h1>
          <p class="hero-sub" style="font-size: 1.2rem; color: #475569;">
            {sub_title}
          </p>
        </header>

        <section class="kb-concept-section" style="margin-bottom: 48px;">
          <h2 style="font-size: 1.5rem; margin-bottom: 16px; color: #1e293b; border-left: 4px solid #38bdf8; padding-left: 12px;">Core Concepts</h2>
          <p style="line-height: 1.7; color: #334155; font-size: 1.05rem;">
            {core_content}
          </p>
        </section>

        <section class="kb-concept-section" style="margin-bottom: 48px; background: #f8fafc; padding: 24px; border-radius: 16px; border: 1px solid #e2e8f0;">
          <h2 style="font-size: 1.3rem; margin-bottom: 16px; color: #1e293b;">Key Advantages & Applications</h2>
          <ul style="display: grid; gap: 12px; padding-left: 20px; color: #475569;">
            {key_points}
          </ul>
        </section>

        <section class="kb-concept-section" style="margin-bottom: 48px;">
          <h2 style="font-size: 1.5rem; margin-bottom: 16px; color: #1e293b;">Industry Best Practices</h2>
          <p class="meta" style="color: #475569; line-height: 1.6;">{best_practices}</p>
        </section>
      </article>
    </main>

    <footer class="footer site-footer">
      <div class="container">
        <p>© 2026 Gstarcademy · Knowledge Base</p>
      </div>
    </footer>
    <script src="../../app.js" defer></script>
  </body>
</html>
"""

CONCEPTS_DATA = [
    {
        "filename": "catia-gsd.html",
        "title": "CATIA GSD (Generative Shape Design)",
        "description": "Explore CATIA Generative Shape Design (GSD), the industry standard for aerospace and automotive class-A surfacing.",
        "category": "Surfacing",
        "sub_title": "Industrial-grade class-A surface design and advanced geometric shapes.",
        "core_content": "<strong>Generative Shape Design (GSD)</strong> provides an extensive set of tools for creating wireframe and surface geometries. It allows designers to build highly complex, organic shapes suitable for aerospace, automotive, and high-tech product design. Surfacing in GSD supports associative links, ensuring that any modifications to base curves automatically propagate through parent surfaces.",
        "key_points": "<li><strong>Class-A Precision:</strong> Perfect curvature continuity (G0 to G3) essential for reflection and aerodynamics.</li><li><strong>Generative History:</strong> Every surface point and curve is parametrical, allowing quick scaling and morphing.</li><li><strong>Robust Healing:</strong> Built-in diagnostic tools to check and heal surface gaps, cracks, and tangent defects.</li>",
        "best_practices": "Always construct surfaces using primary wireframe skeletons. Minimize multi-section surfaces where simple sweeps can achieve the same geometry to avoid control-point congestion."
    },
    {
        "filename": "solidworks-pdm.html",
        "title": "SOLIDWORKS PDM",
        "description": "Learn about SOLIDWORKS Product Data Management (PDM) for file versioning, secure check-in/out, and collaborative workflows.",
        "category": "Data Management",
        "sub_title": "Secure data management, revision control, and automated team collaboration.",
        "core_content": "<strong>SOLIDWORKS PDM (Product Data Management)</strong> is a centralized database-driven solution that helps design teams manage their CAD files. By utilizing a local 'Vault' paradigm, it prevents accidental data loss, overwrites, and manages drawing revisions through secure check-in/check-out permissions.",
        "key_points": "<li><strong>Revision Control:</strong> Automatically increments drawing revisions based on engineering workflow approvals.</li><li><strong>Where Used Tracking:</strong> Instantly check which assemblies contain a specific part before making major geometry changes.</li><li><strong>BOM Synchronization:</strong> Translates CAD custom properties into exact bill-of-materials exports.</li>",
        "best_practices": "Ensure all designers complete daily check-ins. Never reference files outside the local PDM vault to avoid breaking external assembly links."
    },
    {
        "filename": "3dexperience-platform.html",
        "title": "3DEXPERIENCE Platform",
        "description": "Understand Dassault Systemes 3DEXPERIENCE, a unified cloud portal connecting CAD, PLM, and multi-discipline engineering.",
        "category": "Cloud Platform",
        "sub_title": "Unified enterprise environment for CAD, simulation, and business innovation.",
        "core_content": "The <strong>3DEXPERIENCE Platform</strong> represents Dassault Systemes' vision for enterprise data collaboration. It bridges traditional desktop CAD (SOLIDWORKS, CATIA) with advanced cloud PLM (ENOVIA) and simulation (SIMULIA), providing a single source of truth accessible from any web browser.",
        "key_points": "<li><strong>Zero File Local Storage:</strong> Models are stored as structured database objects rather than vulnerable local flat files.</li><li><strong>Real-time Dashboards:</strong> Instant project health checks, task assignments, and 3D playbacks for non-CAD stakeholders.</li><li><strong>Scalable Roles:</strong> Dynamically add simulation, governance, or manufacturing packages to active user seats.</li>",
        "best_practices": "Use the collaborative space feature to organize files by project division. Clean up orphan revisions and cache databases regularly for quick synchronization."
    },
    {
        "filename": "catia-caa-sdk.html",
        "title": "CATIA CAA C++ SDK",
        "description": "Deep dive into Component Application Architecture (CAA), the native C++ APIs to customize and extend CATIA's core engine.",
        "category": "SDK & Customization",
        "sub_title": "High-performance enterprise API hooks for custom feature definitions.",
        "core_content": "The <strong>Component Application Architecture (CAA)</strong> is the native C++ API framework for CATIA. It provides developers deep access to the product structure, geometrical modeler, and UI engine, enabling the creation of custom features, commands, and heavy-duty extensions that behave like out-of-the-box workbenches.",
        "key_points": "<li><strong>Deep Modeler Access:</strong> Direct control over topological operators and B-Rep structures.</li><li><strong>Extension Framework:</strong> Add custom features that participate natively in the update cycle.</li><li><strong>Enterprise Integration:</strong> Link CATIA modeling events directly with external ERP or custom PDM databases.</li>",
        "best_practices": "Maintain a strict development build environment aligned with Dassault's exact compiler recommendations. Leverage standard interface definitions to prevent regression bugs."
    },
    {
        "filename": "solidworks-api.html",
        "title": "SOLIDWORKS API",
        "description": "Learn to use the SOLIDWORKS VBA and .NET APIs to automate repetitive modeling, drawing generation, and ERP exports.",
        "category": "SDK & Customization",
        "sub_title": "VBA, VB.NET, and C# automation for repetitive modeling tasks.",
        "core_content": "The <strong>SOLIDWORKS API (Application Programming Interface)</strong> is a powerful COM-based programming interface. Using languages like VBA, VB.NET, or C#, engineers can automate daily drafting operations, auto-generate standard parts from configurations, and write direct exporters to manufacturing systems.",
        "key_points": "<li><strong>Macro Recording:</strong> Instantly capture user interface clicks into editable VBA macro code.</li><li><strong>Document Traversal:</strong> Scan through complex assemblies to modify model parameters on the fly.</li><li><strong>Custom Task Panes:</strong> Embed proprietary tools directly inside the SOLIDWORKS user interface panel.</li>",
        "best_practices": "Keep macros modular. When writing high-throughput assembly traversers, always disable screen updates and set components to lightweight mode to boost speed."
    },
    {
        "filename": "catia-fbd.html",
        "title": "CATIA Feature-Based Design",
        "description": "Understand Feature-Based Design (FBD) parameters, update cycles, and parent-child dependencies in CATIA V5/V6.",
        "category": "Solid Modeling",
        "sub_title": "Parametric history, features, and strict geometrical parent-child trees.",
        "core_content": "<strong>Feature-Based Design (FBD)</strong> in CATIA is built on strict parametric principles. Unlike traditional direct modelers, every element (sketches, pads, pockets) exists as a node in the specification tree. The geometry updates sequentially, ensuring design intent is strictly maintained according to parent-child links.",
        "key_points": "<li><strong>Strict Spec Tree:</strong> Clear chronological history of how the solid is constructed.</li><li><strong>Parameters & Formulas:</strong> Link dimensions directly to spreadsheet variables or conditional equations.</li><li><strong>Regeneration Control:</strong> Manual or automatic update triggers to handle heavy parametric calculations.</li>",
        "best_practices": "Establish clean naming conventions for your tree nodes. Avoid daisy-chaining references; always tie geometric features to stable datum planes."
    },
    {
        "filename": "solidworks-configurations.html",
        "title": "SOLIDWORKS Configurations",
        "description": "Master SOLIDWORKS configurations, design tables, and instance properties to model complex standard part families.",
        "category": "Solid Modeling",
        "sub_title": "Managing multiple part sizes, materials, and display states in one file.",
        "core_content": "<strong>SOLIDWORKS Configurations</strong> allow designers to create and manage multiple variations of a part or assembly within a single document. Instead of creating distinct files for minor dimensional changes, you can suppress features, adjust dimensions, and swap properties per configuration.",
        "key_points": "<li><strong>Design Tables:</strong> Drive configuration parameters directly using embedded Excel spreadsheets.</li><li><strong>Display States:</strong> Toggle custom visual appearances and component visibility without altering active geometric metadata.</li><li><strong>Assembly Instances:</strong> Choose different configurations for repeated fasteners to keep tree structures clean.</li>",
        "best_practices": "Keep your default configuration generic. Suppress highly detailed cosmetic features in simplified configurations to improve downstream assembly performance."
    },
    {
        "filename": "enovia-plm.html",
        "title": "ENOVIA PLM",
        "description": "Learn about ENOVIA PLM, the enterprise product life cycle backbone of Dassault Systemes for BOM and change control.",
        "category": "Data Management",
        "sub_title": "Product lifecycle management, engineering bill of materials (EBOM), and change orders.",
        "core_content": "<strong>ENOVIA PLM</strong> is the central business process orchestrator in the Dassault Systemes ecosystem. It governs the entire product life cycle from conceptual design, collaborative BOM management, and strict engineering change operations (ECOs) down to shop-floor handoffs.",
        "key_points": "<li><strong>Enterprise EBOM:</strong> Centralized BOM management decoupled from CAD-specific file configurations.</li><li><strong>Change Management:</strong> Enforces formal change actions (CO, CA) with sign-off loops across corporate departments.</li><li><strong>Multi-CAD Integrations:</strong> Bridges CATIA, SOLIDWORKS, and non-DS CAD data in one unified system.</li>",
        "best_practices": "Map CAD custom properties strictly to ENOVIA attributes prior to publishing. Enforce a robust classification system to avoid duplicating parts."
    },
    {
        "filename": "simulia-abaqus.html",
        "title": "SIMULIA Abaqus FEA",
        "description": "Explore SIMULIA Abaqus for advanced nonlinear finite element analysis, structural integrity, and dynamic loading simulation.",
        "category": "Simulation & CAE",
        "sub_title": "Industry-leading nonlinear finite element analysis and structural solver.",
        "core_content": "<strong>SIMULIA Abaqus FEA</strong> is an advanced suite for finite element analysis. It is globally recognized for its exceptional capability to handle highly nonlinear structural problems, including complex contact, plastic deformation, material failure, and dynamic impact events.",
        "key_points": "<li><strong>Nonlinear Solver:</strong> Master class handling of geometric, material, and boundary nonlinearities.</li><li><strong>Abaqus/Explicit:</strong> Specialized solver for transient dynamic events like crashworthiness and drop tests.</li><li><strong>Co-Simulation:</strong> Couple electromagnetic, fluid, and structural analyses for multiphysics fidelity.</li>",
        "best_practices": "Start with a simplified 2D or symmetric model to validate boundaries. Mesh critical zones finely while utilizing structural transitions to keep solve times reasonable."
    },
    {
        "filename": "delmia-digital-mfg.html",
        "title": "DELMIA Digital Manufacturing",
        "description": "Master DELMIA Digital Manufacturing to simulate production lines, assembly ergonomics, and robot operations.",
        "category": "Manufacturing & CAM",
        "sub_title": "Digital factory simulation, line balancing, and automated robotic assembly.",
        "core_content": "<strong>DELMIA Digital Manufacturing</strong> bridges the gap between engineering design and actual production. It allows manufacturers to virtually build their production lines, analyze assembly feasibility, optimize throughput, and simulate robotic operations before investing in physical tooling.",
        "key_points": "<li><strong>Robot Programming:</strong> Offline programming (OLP) and collision checks for multi-axis robot workcells.</li><li><strong>Ergonomics Simulation:</strong> Assess human operator comfort and reach limits using realistic digital mannequins.</li><li><strong>Process Planning:</strong> Link structural CAD assemblies directly to the Manufacturing BOM (MBOM) and assembly instructions.</li>",
        "best_practices": "Maintain a standardized library of robotic arms and tooling fixtures. Synchronize the cycle times with DELMIA simulation runs to avoid bottle-necks on the actual plant floor."
    },
    {
        "filename": "draftsight-professional.html",
        "title": "DraftSight Professional",
        "description": "Learn about DraftSight, the highly compatible 2D DWG drafting tool from Dassault Systemes for AutoCAD alternatives.",
        "category": "2D Drafting",
        "sub_title": "Highly compatible and cost-effective 2D DWG drafting software.",
        "core_content": "<strong>DraftSight Professional</strong> is Dassault Systemes' professional 2D drafting alternative. Supporting native DWG file handling, it offers AutoCAD users a familiar user interface, full command line compatibility, and advanced APIs for LISP/C++ automation.",
        "key_points": "<li><strong>Native DWG Support:</strong> Seamlessly open, edit, and save DWG files without importing or format loss.</li><li><strong>Familiar Interface:</strong> Traditional workspace options minimize employee retraining times.</li><li><strong>Smart Block Conversion:</strong> Easily translate dynamic blocks and scripts into the DraftSight format.</li>",
        "best_practices": "Set up your custom system paths for DWG template files. Back up your command aliases to ease user onboarding during transition cycles."
    },
    {
        "filename": "catia-v5-v6-hybrid.html",
        "title": "CATIA V5-V6 Hybrid Workflows",
        "description": "Understand file-based V5 and database-based V6/3DEXPERIENCE interoperability and data translation best practices.",
        "category": "Solid Modeling",
        "sub_title": "Bridging traditional file-based CAD with modern database-driven PLM.",
        "core_content": "As companies transition, managing co-existence between <strong>CATIA V5</strong> (file-based) and <strong>CATIA V6 / 3DEXPERIENCE</strong> (database-driven) is a critical challenge. Hybrid workflows enable teams to link, exchange, and revise designs across both platforms without losing parametric fidelity.",
        "key_points": "<li><strong>Data Translation:</strong> Direct downstream transfer of specification tree structures from V5 to V6.</li><li><strong>Collaborative Workspaces:</strong> Check in V5 files directly into ENOVIA databases for coordination.</li><li><strong>3D XML Handoffs:</strong> Lightweight spatial sharing of master assemblies for review without exposing IP.</li>",
        "best_practices": "Verify boundary representation (B-Rep) face IDs when translating files back to V5 to prevent downstream model features from losing their reference edges."
    },
    {
        "filename": "solidworks-weldments.html",
        "title": "SOLIDWORKS Weldments",
        "description": "Learn SOLIDWORKS Weldments for steel frames, structural members, cut lists, and structural frame drawings.",
        "category": "Solid Modeling",
        "sub_title": "Structural steel framing, trim-extend operations, and automated cut lists.",
        "core_content": "<strong>SOLIDWORKS Weldments</strong> is a specialized solid modeling module designed for steel framing and structural shapes. By projecting standardized structural profiles along simple 2D or 3D sketch skeletons, it automates weldment design, corner trimming, and structural drawings.",
        "key_points": "<li><strong>Profile Library:</strong> Extensible library of international standards (ISO, ANSI, DIN) for beams and pipes.</li><li><strong>Automatic Cut Lists:</strong> Instantly generate manufacturing lists containing exact lengths, angles, and quantities.</li><li><strong>Joint Management:</strong> Automated trim, extend, and miter-cut tools for clean frame corners.</li>",
        "best_practices": "Always construct structural frame skeletons using a single master 3D sketch. Organize weldment features chronologically to avoid rebuild loops."
    },
    {
        "filename": "solidworks-sheetmetal.html",
        "title": "SOLIDWORKS Sheet Metal",
        "description": "Understand SOLIDWORKS sheet metal design, K-factors, bend tables, and flat pattern exports for manufacturing.",
        "category": "Solid Modeling",
        "sub_title": "Flat pattern flattening, K-factors, and precision bend calculations.",
        "core_content": "The <strong>SOLIDWORKS Sheet Metal</strong> workbench allows engineers to design sheet metal enclosures and stampings. It calculates material stretch during bending based on material-specific K-Factors or Bend Tables, ensuring that flat patterns correspond exactly to the finished physical bent part.",
        "key_points": "<li><strong>Flat Pattern Generation:</strong> Instant folding and unfolding of parts to verify mechanical clearance.</li><li><strong>Forming Tools:</strong> Easily drag and drop standard louvers, ribs, and lance punches onto solid sheet faces.</li><li><strong>DXF Exports:</strong> Streamlined direct exports of flat profiles for CNC laser and waterjet cutters.</li>",
        "best_practices": "Consult with your manufacturing supplier to input their actual K-factor parameters. Avoid tight bends that exceed material elongation limits."
    },
    {
        "filename": "catia-part-design.html",
        "title": "CATIA Part Design",
        "description": "Explore CATIA Part Design: robust solid modeling, boolean operations, sketchers, and parametric tree management.",
        "category": "Solid Modeling",
        "sub_title": "High-fidelity parametric part modeling, spec trees, and boolean operations.",
        "core_content": "<strong>CATIA Part Design</strong> is the cornerstone of mechanical part design in CATIA. Utilizing sketches, pads, shafts, and dress-up features, it enables engineers to build stable solid parts with rich parametric intelligence, suited for high-reliability manufacturing sectors.",
        "key_points": "<li><strong>Sketcher Constraints:</strong> Rigorous geometric sketch validation to prevent under-constrained features.</li><li><strong>Boolean Modeler:</strong> Execute advanced union, intersection, and subtraction operations across distinct solid bodies.</li><li><strong>Contextual Features:</strong> Create associative drafts and fillets linked to parent face boundaries.</li>",
        "best_practices": "Keep sketches simple and fully constrained. Use coordinate systems instead of absolute part origins to ensure excellent model portability."
    },
    {
        "filename": "catia-assembly-design.html",
        "title": "CATIA Assembly Design",
        "description": "Master CATIA Assembly Design for high-component count products, kinematic joints, and collision diagnostics.",
        "category": "Solid Modeling",
        "sub_title": "Rigid constraint management, kinematics, and large assembly coordination.",
        "core_content": "<strong>CATIA Assembly Design</strong> provides the tools to assemble, analyze, and manage thousands of individual parts. It uses rigid assembly constraints (coincidence, contact, offset) to locate components in 3D space, and offers clash diagnostics to prevent hardware assembly conflicts.",
        "key_points": "<li><strong>Multi-Level Tree:</strong> Intuitive sub-assembly hierarchy suited for heavy complex machinery.</li><li><strong>Clash Analysis:</strong> Instant spatial clash and clearance detection between parts in real-time.</li><li><strong>Flexible Assemblies:</strong> Define kinetic joints to simulate and verify moving mechanical assemblies.</li>",
        "best_practices": "Anchor the primary structural part of the assembly first. Load sub-assemblies in visualization mode to preserve CPU resources during checkouts."
    },
    {
        "filename": "solidworks-edrawings.html",
        "title": "SOLIDWORKS eDrawings",
        "description": "Understand eDrawings for sharing high-fidelity, lightweight CAD file previews, markup, and VR reviews.",
        "category": "Data Management",
        "sub_title": "Lightweight CAD viewer and collaborative review for cross-functional teams.",
        "core_content": "<strong>eDrawings</strong> is a lightweight, high-fidelity CAD visualization utility. It allows engineers to publish compressed CAD assemblies and drawings that can be easily shared, reviewed, and marked up by project managers, purchasing teams, and shop-floor technicians without high-end CAD seats.",
        "key_points": "<li><strong>Self-Contained Previews:</strong> Embedded model geometries allow full pan, zoom, and section cuts in email-friendly files.</li><li><strong>Interactive Markups:</strong> Draw redlines, add text comments, and measure 3D coordinates directly.</li><li><strong>AR & VR Support:</strong> View assemblies at 1:1 scale using mobile cameras and VR headsets.</li>",
        "best_practices": "Enable measurement protection when sending models to external partners. Combine multi-sheet drawings into a single eDrawings package for client reviews."
    },
    {
        "filename": "3dexperience-collaborative-sharing.html",
        "title": "3DEXPERIENCE Collaborative Sharing",
        "description": "Learn how 3DEXPERIENCE Collaborative Sharing coordinates user roles, workspaces, and real-time co-authoring.",
        "category": "Cloud Platform",
        "sub_title": "Real-time design co-authoring and permission governance in the cloud.",
        "core_content": "<strong>Collaborative Sharing</strong> is the foundation of 3DEXPERIENCE team coordination. It replaces traditional file servers with digital 'Spaces', where designers can co-author parts, manage tasks, and govern model access through robust role-based permissions.",
        "key_points": "<li><strong>Active Reservation:</strong> Lock parts in-work to notify the team that you are actively modifying geometry.</li><li><strong>Share to 3DPlay:</strong> Instantly share interactive 3D models with procurement or suppliers without emailing source files.</li><li><strong>Integrated Lifecycles:</strong> Directly request approvals and trigger ECO checks from the active CAD interface.</li>",
        "best_practices": "Structure workspace access roles (Reader, Author, Leader) clearly at the start of each project. Use tag tags to filter and search items inside big spaces."
    },
    {
        "filename": "solidworks-simulation.html",
        "title": "SOLIDWORKS Simulation",
        "description": "Master SOLIDWORKS Simulation: FEA solvers, static stress analysis, fatigue, and mesh tuning within the CAD interface.",
        "category": "Simulation & CAE",
        "sub_title": "CAD-integrated FEA for stress, displacement, and factor of safety.",
        "core_content": "<strong>SOLIDWORKS Simulation</strong> is a design-validation tool integrated directly into the SOLIDWORKS modeler. It allows designers to apply static and dynamic loads, structural constraints, and evaluate stress, deflection, and factor-of-safety parameters before manufacturing prototype parts.",
        "key_points": "<li><strong>Integrated Workflow:</strong> Instantly switch between the modeling tree and the simulation tree.</li><li><strong>Contact Formulations:</strong> Simulate real-world interactions using bonded, sliding, and shrinkage fits.</li><li><strong>Mesh Optimization:</strong> Automatically refine meshes on critical stress concentrations using h-adaptive mesh algorithms.</li>",
        "best_practices": "Verify displacement results first to ensure boundaries behave realistically. Use simplified beam elements for frame weldments to drastically cut solver runtime."
    },
    {
        "filename": "catia-composites-design.html",
        "title": "CATIA Composites Design",
        "description": "Explore CATIA Composites Design for composite layup, ply books, draping simulation, and core sample diagnostics.",
        "category": "Surfacing",
        "sub_title": "Composite ply layup, draping simulation, and advanced materials engineering.",
        "core_content": "<strong>CATIA Composites Design</strong> is a dedicated workbench tailored for aerospace and marine composite structural engineering. It manages the entire process from structural surface zones, ply draping simulation, to exporting flat patterns for carbon-fiber laser projection systems.",
        "key_points": "<li><strong>Draping Simulation:</strong> Predict fiber deformation and warp shear over highly curved surfaces before layups.</li><li><strong>Ply Table Generation:</strong> Automatically generate exact ply books, sequencing charts, and engineering layups.</li><li><strong>Core Samples:</strong> Extract precise material core thickness profiles at any physical point on the composite shell.</li>",
        "best_practices": "Ensure the underlying mold surface is completely healed and continuous. Define clear fiber orientation reference axes to maintain ply structural alignment."
    }
]

for item in CONCEPTS_DATA:
    filepath = f"kb/concepts/{item['filename']}"
    content = TEMPLATE.format(
        title=item['title'],
        description=item['description'],
        category=item['category'],
        sub_title=item['sub_title'],
        core_content=item['core_content'],
        key_points=item['key_points'],
        best_practices=item['best_practices']
    )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {filepath}")
