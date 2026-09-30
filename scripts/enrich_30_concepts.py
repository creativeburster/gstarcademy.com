"""Enrich the 30 recently added engineering standard & modeling concept pages.
Adds:
- Section 3: Engineering Application & Practical CAD/BIM Workflows (Detailed operations, parameters, commands)
- Section 4: Quality Control & Common Failure Modes (Checklist, troubleshooting, best practices)
This brings all 30 pages from ~125 words up to 400-500 words, eliminating thin content.
"""
from pathlib import Path
from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parents[1]
CONCEPTS_DIR = REPO_ROOT / "kb" / "concepts"

ENRICHMENTS = {
    "annotative-scaling-model-paper-space": {
        "sec3_title": "3. CAD Implementation & Workflow Commands",
        "sec3_content": """
<p>To implement annotative scaling in production drawings:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Annotation Scale Synchronization:</strong> Set the active drawing scale via the status bar scale menu (or system variable <code>CANNOSCALE</code>) before drafting text, dimensions, or hatches.</li>
  <li><strong>Viewport Assignment:</strong> When selecting a layout viewport, specify the exact engineering scale (e.g., 1:50 or 1:100). The CAD display engine dynamically scales annotative objects to preserve paper-space text height (typically 2.5mm or 3.0mm).</li>
  <li><strong>Multi-Scale Grips:</strong> When multiple scales are assigned to a single note, clicking the annotative text displays multiple ghosted boundary outlines, enabling draftsmen to reposition annotations per viewport without affecting other sheets.</li>
</ul>""",
        "sec4_title": "4. Quality Control & Scale List Bloat Prevention",
        "sec4_content": """
<p>A frequent error in multi-user environments is leaving <code>ANNOAUTOSCALE</code> enabled (set to 4). This automatically appends every encountered viewport scale to all annotative objects, inflating drawing file sizes and causing severe freeze lags during save operations. Production standard operating procedures mandate setting <code>ANNOAUTOSCALE</code> to 1 (or 0) and regularly executing the <code>-SCALELISTEDIT</code> command (using the <code>Reset</code> option) to purge unused scales.</p>"""
    },
    "b-rep-boundary-representation": {
        "sec3_title": "3. Geometric Modeling Engine Workflows",
        "sec3_content": """
<p>In boundary representation kernels such as Parasolid, ACIS, and Open CASCADE, 3D solids are evaluated through a two-tiered data structure:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Topological Graph:</strong> A hierarchical connectivity network containing Shells, Faces, Loops, Edges, and Vertices. The loop topology defines the trimming boundaries for each parametric face.</li>
  <li><strong>Geometric Embedding:</strong> Exact underlying mathematical representations, including NURBS spline surfaces, analytical cylinders, tori, and planar equations tied to vertices and edges.</li>
  <li><strong>Euler Operators:</strong> Kernel operations preserve topological Euler-Poincaré invariants (V - E + F - (L - F) - 2(S - G) = 0) during Boolean unions, cuts, and sweeps, ensuring closed 2-manifold volumes.</li>
</ul>""",
        "sec4_title": "4. Robustness Challenges & Non-Manifold Geometry",
        "sec4_content": """
<p>Modeling failures during complex fillets, lofts, or Boolean subtractions typically occur when geometry produces non-manifold conditions, such as two solid regions touching along a zero-thickness edge or vertex. In enterprise CAD/CAM data exchange, healing algorithms in STEP import modules re-stitch adjacent trimmed edges within an allowable numerical tolerance (typically 0.001mm to 0.01mm) to reconstruct a valid closed solid.</p>"""
    },
    "bcf-3-0-topic-management": {
        "sec3_title": "3. OpenBIM Coordination & REST API Integration",
        "sec3_content": """
<p>BCF (BIM Collaboration Format) 3.0 replaces unwieldy static PDF clash dossiers with lightweight XML/JSON issue payloads. Key technical mechanisms include:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Orthogonal & Perspective Viewpoint Cameras:</strong> Captures exact focal position, target direction, up-vector, and field of view, enabling any connected authoring software to reproduce the exact designer viewpoint with one click.</li>
  <li><strong>Component GUID Identification:</strong> Issues record specific <code>IfcGuid</code> references for colliding or queried elements, automatically isolating and highlighting target geometry in Revit, GstarCAD Architecture, or ArchiCAD.</li>
  <li><strong>RESTful Cloud Synchronization:</strong> BCF-API enables real-time synchronization between coordination platforms (e.g., BIMcollab, Revizto) and desktop CAD/BIM tools.</li>
</ul>""",
        "sec4_title": "4. Project Governance & Status Lifecycle",
        "sec4_content": """
<p>Effective BCF governance enforces structured status progressions: Open &rarr; In Progress &rarr; Resolved &rarr; Verified &rarr; Closed. Coordination managers must prevent subcontractors from marking issues as 'Closed' without attaching an updated BCF viewpoint demonstrating clearance. Maintaining strict topic typing (Clash, Inquiry, Request for Information) keeps team task backlogs organized throughout project construction phases.</p>"""
    },
    "cde-common-data-environment-iso-19650": {
        "sec3_title": "3. Information Container States & Metadata Gates",
        "sec3_content": """
<p>Under ISO 19650-1 and 19650-2, the Common Data Environment is structured around four distinct information states with formalized transition gateways:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Work in Progress (WIP):</strong> Private working area for individual task teams. Model containers undergo internal checks before approval.</li>
  <li><strong>Shared:</strong> Information verified and released for multi-disciplinary coordination, reference, and design development.</li>
  <li><strong>Published:</strong> Contractual deliverables approved by the appointing party for statutory approvals, procurement, and physical construction.</li>
  <li><strong>Archived:</strong> Permanent historical record of all completed milestones and operational as-built facility data.</li>
</ul>""",
        "sec4_title": "4. Access Security & Audit Trail Governance",
        "sec4_content": """
<p>A compliant CDE mandates immutable versioning, automated audit logs, and status code tracking (e.g., S1 for coordination, S3 for review, A for construction). Enterprise implementations must guard against common anti-patterns, such as team members sharing unapproved WIP drawings via unmanaged consumer cloud drives, which introduces uncoordinated geometric changes into structural steel fabrication.</p>"""
    },
    "clash-detection-hard-soft-clearance": {
        "sec3_title": "3. Coordination Matrix & Tolerance Rules",
        "sec3_content": """
<p>Modern clash detection engines (e.g., Navisworks, Solibri, BIM Track) evaluate 3D federated models against specialized test matrices:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Hard Clash Detection:</strong> Identifies volumetric intersections between solid geometries (e.g., a 200mm drainage pipe passing through a prestressed concrete girder).</li>
  <li><strong>Soft (Clearance) Clash Detection:</strong> Enforces spatial buffer envelopes around elements, ensuring adequate room for pipe insulation, valve turning handles, and maintenance access.</li>
  <li><strong>Time (4D) Clashes:</strong> Analyzes spatial conflicts where temporary construction equipment (scaffolding, cranes) intersects structural members scheduled for installation at the same date.</li>
</ul>""",
        "sec4_title": "4. Filtering Strategies & Avoiding False Positives",
        "sec4_content": """
<p>Setting clash tolerances to 0.00mm generates thousands of false positives caused by coplanar drywall finishes and structural slabs. Best practices mandate setting an initial tolerance threshold (e.g., 5mm to 10mm) and applying exclusion rules to ignore penetration sleeves, insulation touching hangers, and fixtures contained entirely within their host wall assemblies.</p>"""
    },
    "csg-constructive-solid-geometry": {
        "sec3_title": "3. Tree Evaluation & Computational Principles",
        "sec3_content": """
<p>Constructive Solid Geometry builds complex shapes through binary trees where terminal leaf nodes represent primitive shapes (cubes, cylinders, spheres, cones) and internal nodes represent Boolean operations (Union, Difference, Intersection):</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Ray-Casting & Volumetric Queries:</strong> CSG trees allow instant point-in-solid and ray-intersection tests without explicitly generating all boundary surface meshes.</li>
  <li><strong>Boundary Evaluation:</strong> Modern CAD kernels convert CSG histories into B-Rep representations so that edge fillets, draft angles, and chamfers can be applied to the resulting intersection curves.</li>
  <li><strong>Parametric Re-evaluation:</strong> Modifying primitive dimensions recalculates the CSG tree deterministically, updating the physical model volume.</li>
</ul>""",
        "sec4_title": "4. Modeling Performance & Numerical Stability",
        "sec4_content": """
<p>Deeply nested CSG trees containing hundreds of successive Boolean operations can degrade CAD regeneration performance. In production modeling, designers should consolidate simple Boolean patterns into single sketched extrusions with multi-contour profiles, avoiding degenerate coplanar Boolean operations that lead to zero-thickness calculation exceptions.</p>"""
    },
    "datum-reference-frame-setup": {
        "sec3_title": "3. 3-2-1 Fixture Alignment & Mathematical Restraint",
        "sec3_content": """
<p>A Datum Reference Frame establishes a rigid Cartesian coordinate system (X, Y, Z axes and planes) to lock all 6 spatial degrees of freedom (3 translations, 3 rotations):</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Primary Datum (3 Points):</strong> Restricts 2 rotational axes and 1 translational axis, establishing the orientation of the primary plane.</li>
  <li><strong>Secondary Datum (2 Points):</strong> Restricts 1 rotational axis and 1 translational axis, oriented perpendicular to the primary datum.</li>
  <li><strong>Tertiary Datum (1 Point):</strong> Restricts the final translational degree of freedom, locating the coordinate origin.</li>
</ul>""",
        "sec4_title": "4. Quality Inspection & Physical Fixturing",
        "sec4_content": """
<p>Datums should always be assigned to physically functional mating features. Selecting flexible, thin sheet metal flanges as primary datums introduces severe measurement instability on Coordinate Measuring Machines (CMM). When datum features have significant form variation, datum target areas or pins (e.g., [A1], [A2], [A3]) must be explicitly specified per ASME Y14.5.</p>"""
    },
    "dwg-audit-purge-drawing-recovery": {
        "sec3_title": "3. Database Maintenance Commands & Protocol",
        "sec3_content": """
<p>Enterprise CAD drawings often accumulate corrupt entity pointer records and orphaned metadata. The standard hygiene workflow includes:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>AUDIT Command:</strong> Scans the active DWG object database, detects invalid pointer handles, and automatically repairs dangling references with the <code>Y</code> fix option.</li>
  <li><strong>-PURGE (Command-Line):</strong> Run with the <code>RegApps</code> (Registered Applications) option to eliminate zombie application dictionary headers left by third-party plugins.</li>
  <li><strong>OVERKILL:</strong> Deletes duplicate overlapping lines, arcs, and polylines, combining collinear segments to optimize vector draw pipelines.</li>
</ul>""",
        "sec4_title": "4. DGN LineStyle Bloat & Disaster Recovery",
        "sec4_content": """
<p>Importing MicroStation DGN files frequently infects DWG drawings with hundreds of thousands of hidden line-style dictionaries, causing 2MB drawings to balloon into 80MB files. Running dedicated DGN purge routines or invoking <code>WBLOCK</code> to export only valid model space entities strips corrupted tables and restores instant zoom and save response times.</p>"""
    },
    "ecad-mcad-codesign-idx-protocol": {
        "sec3_title": "3. Incremental Collaboration via ProStep IDX",
        "sec3_content": """
<p>The ProStep EDMD (ECAD/MCAD Data Exchange) XML schema standardizes incremental collaborative workflows between electrical PCB tools (Altium, Cadence) and mechanical CAD systems (SolidWorks, Creo, NX):</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Baseline & Incremental Changes:</strong> Instead of re-importing massive 3D models upon every design tweak, IDX communicates only moved component centroids, modified board outlines, and altered keep-out zones.</li>
  <li><strong>Accept / Reject Messaging:</strong> Electrical and mechanical engineers review proposed component shifts interactively, approving or rejecting changes with embedded engineering notes.</li>
  <li><strong>3D Component Heights:</strong> Maps precise component bounding heights to prevent collisions with metal chassis covers and thermal heatsinks.</li>
</ul>""",
        "sec4_title": "4. Coordinate Origin Alignment & Keep-Out Zones",
        "sec4_content": """
<p>A primary failure point in ECAD-MCAD collaboration is misaligned coordinate origins. Teams must establish a shared physical mounting hole or board corner as the master 0,0,0 reference. Mechanical designers must explicitly define Z-direction keep-out volumes around connectors to prevent electrical trace routing in high-stress assembly zones.</p>"""
    },
    "first-angle-vs-third-angle-projection": {
        "sec3_title": "3. Orthographic Layout Rules & Projection Symbols",
        "sec3_content": """
<p>Standard engineering drawings employ orthographic projection to map 3D features onto 2D drawing sheets without distortion:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>First Angle Projection (ISO / European Convention):</strong> The object rests between the observer and the projection plane. Looking from the front, the view from the left is drawn on the right; the view from above is drawn on the bottom.</li>
  <li><strong>Third Angle Projection (ASME / North American Convention):</strong> The projection plane rests between the observer and the object. The view from the right is placed on the right; the top view is placed directly above the front view.</li>
  <li><strong>Title Block Projection Cone:</strong> Drawings must prominently feature the truncated cone projection symbol in the title block to prevent shop-floor machinists from inverting the view orientation.</li>
</ul>""",
        "sec4_title": "4. Manufacturing Pitfalls & Rejection Risks",
        "sec4_content": """
<p>Failing to verify the projection angle before fabricating asymmetric parts can result in 100% scrap rates, producing mirrored parts that cannot be installed into final assemblies. Quality inspection procedures must always cross-reference the title block projection symbol against the CAD model orientation.</p>"""
    },
    "geometric-dimensioning-tolerancing-asme-y14-5": {
        "sec3_title": "3. Feature Control Frames & Tolerance Categories",
        "sec3_content": """
<p>ASME Y14.5 groups geometric tolerances into five distinct functional categories indicated by universal drafting symbols:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Form Tolerances:</strong> Straightness, Flatness, Circularity, and Cylindricity (evaluated without reference to datums).</li>
  <li><strong>Orientation Tolerances:</strong> Perpendicularity, Parallelism, and Angularity (referenced to datums).</li>
  <li><strong>Location Tolerances:</strong> Position, Concentricity, and Symmetry (controlling feature spacing and alignment).</li>
  <li><strong>Runout & Profile:</strong> Circular/Total Runout and Profile of a Line/Surface, controlling complex geometry envelopes.</li>
</ul>""",
        "sec4_title": "4. Drawing Review Checklist & Shop-Floor Verification",
        "sec4_content": """
<p>When authoring GD&T callouts in GstarCAD or AutoCAD, ensure that all basic dimensions (enclosed in rectangular boxes) link to true datum features. Common errors include placing datum symbols on non-repeatable surfaces or applying Maximum Material Condition modifiers to runout or form callouts where size compensation is mathematically invalid.</p>"""
    },
    "ifc-4-3-infrastructure-entities": {
        "sec3_title": "3. Infrastructure Entities & Alignment Mathematics",
        "sec3_content": """
<p>buildingSMART IFC 4.3 expands openBIM from architectural buildings to civil and transportation infrastructure:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>IfcAlignment:</strong> Encapsulates continuous mathematical alignment curves, combining horizontal tangents/spirals/arcs with vertical parabolic crest/sag profiles.</li>
  <li><strong>Domain Entities:</strong> Introduces specialized subclasses including <code>IfcRoad</code>, <code>IfcRailway</code>, <code>IfcBridge</code>, <code>IfcMarineFacility</code>, and <code>IfcEarthworks</code>.</li>
  <li><strong>Dynamic Cross-Sections:</strong> Supports alignment-based linear referencing, extruding parameterized bridge decks or pavement layers along the 3D curve.</li>
</ul>""",
        "sec4_title": "4. Software Interoperability & Export Best Practices",
        "sec4_content": """
<p>When exporting road or rail projects from Civil 3D or specialized civil suites to IFC 4.3, configure model view definitions to preserve alignment entity curves rather than decomposing geometry into faceted triangular meshes. Ensure all spatial structural components reference proper infrastructure spatial hierarchies.</p>"""
    },
    "iso-128-technical-drawings-rules": {
        "sec3_title": "3. Line Types, Weights & Engineering Application",
        "sec3_content": """
<p>ISO 128 defines standardized graphical representations across all mechanical and civil engineering drawings:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Continuous Thick Lines (Type 01.2):</strong> Visible outlines and structural edges (typically 0.50mm or 0.70mm).</li>
  <li><strong>Dashed Narrow Lines (Type 02.1):</strong> Hidden contours and concealed features (typically 0.25mm or 0.35mm).</li>
  <li><strong>Long-Dashed Dotted Narrow Lines (Type 04.1):</strong> Axes of symmetry, pitch circles, and movement trajectories.</li>
  <li><strong>Continuous Narrow with Zigzags (Type 01.1):</strong> Interrupted views and long-break boundaries.</li>
</ul>""",
        "sec4_title": "4. Plot Style Governance & Sheet Uniformity",
        "sec4_content": """
<p>Maintain enterprise CAD standards by linking ISO 128 line weights directly to drawing layer conventions through standardized CTB or STB plot style tables. Avoid overriding line weights on individual entity properties, which complicates multi-sheet drafting updates and creates unreadable micro-lineweights on PDF exports.</p>"""
    },
    "level-of-development-lod-bim": {
        "sec3_title": "3. BIMForum LOD Framework Progression",
        "sec3_content": """
<p>The Level of Development (LOD) framework standardizes model completeness across project milestones:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>LOD 100 (Conceptual):</strong> Schematic 3D masses conveying overall spatial volume, orientation, and cost metrics.</li>
  <li><strong>LOD 200 (Approximate Geometry):</strong> Generic systems or assemblies with approximate size, shape, and location.</li>
  <li><strong>LOD 300 (Design Coordination):</strong> Specific architectural/structural elements suitable for regulatory submittals and trade coordination.</li>
  <li><strong>LOD 350 (Field Interfaces):</strong> Includes interface connections, embeds, and support brackets necessary to resolve cross-trade clashes.</li>
  <li><strong>LOD 400 (Fabrication):</strong> Precise shop fabrication assemblies with weld preparations, bolt patterns, and assembly sequencing.</li>
</ul>""",
        "sec4_title": "4. Contractual Governance & Model Bloat Avoidance",
        "sec4_content": """
<p>A frequent contracting trap is demanding global LOD 400 or 500 across an entire project. This drastically inflates authoring costs, multiplies file sizes, and overwhelms coordinator workstations. BIM Execution Plans must define an LOD progression matrix that assigns high LOD only to critical congested zones (e.g., MEP plant rooms).</p>"""
    },
    "maximum-material-condition-mmc": {
        "sec3_title": "3. Bonus Tolerance Calculation & Functional Gaging",
        "sec3_content": """
<p>Maximum Material Condition specifies the boundary where a feature contains the maximum amount of material within its size limits (smallest hole or largest pin):</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Virtual Condition Envelope:</strong> Outer boundary calculated as MMC Size + Positional Tolerance for pins, or MMC Size - Positional Tolerance for holes.</li>
  <li><strong>Bonus Tolerance Growth:</strong> When a produced hole is manufactured larger than its minimum MMC diameter, the extra diameter difference is added directly to the allowable geometric positional tolerance.</li>
  <li><strong>Hard Gage Verification:</strong> MMC allows physical go/no-go hard functional attribute gages to inspect parts instantly without CMM numerical scanning.</li>
</ul>""",
        "sec4_title": "4. Inappropriate Application & Design Cautions",
        "sec4_content": """
<p>Never specify MMC on press-fit dowel pin holes or precision alignment pilot bores where location must be maintained regardless of hole diameter. Using MMC in press-fit applications will allow loose alignment centers, causing mechanical gear mesh binding and bearing failures.</p>"""
    },
    "mesh-smoothing-subdivision-surfaces": {
        "sec3_title": "3. Catmull-Clark Subdivision & Polygonal Modeling",
        "sec3_content": """
<p>Subdivision surface algorithms iteratively refine coarse polygonal control cages into smooth, organic limit surfaces:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Catmull-Clark Algorithm:</strong> Computes face points, edge points, and updated vertex positions, converting arbitrary quad/triangle cages into smooth quad-dominant B-spline limit surfaces.</li>
  <li><strong>Edge Creasing & Weighting:</strong> Assigns sharpness weights to control edges, allowing designers to retain hard mechanical ridges and sharp chamfers within organic sculptured geometry.</li>
  <li><strong>CAD Kernel Translation:</strong> Specialized reverse-engineering modules convert dense subdivision limit meshes into analytic NURBS surface patches for downstream CNC milling and tooling.</li>
</ul>""",
        "sec4_title": "4. Mesh Topology Quality & Pole Governance",
        "sec4_content": """
<p>When modeling organic consumer goods, avoid placing 5-edge or 3-edge vertices (poles) directly along high-curvature highlight areas. Poor subdivision topology produces visible surface pinching and wavy reflection lines on rendered consumer products.</p>"""
    },
    "nurbs-degree-continuity-g0-g1-g2-g3": {
        "sec3_title": "3. Geometric Continuity Hierarchy & Evaluation",
        "sec3_content": """
<p>Surface continuity governs how adjacent patches meet and reflect light across their shared boundary curves:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>G0 (Positional Continuity):</strong> Patches share a coincident edge boundary with no gap, but can exhibit a sharp angle or crease.</li>
  <li><strong>G1 (Tangency Continuity):</strong> Surface normal vectors align along the seam, producing a smooth transition with no crease (visible as a sharp kink in zebra reflection stripes).</li>
  <li><strong>G2 (Curvature Continuity):</strong> Normal vectors and radii of curvature match continuously across the boundary, yielding seamless reflection highlights mandatory for automotive Class-A surfaces.</li>
  <li><strong>G3 (Torsion / Acceleration Continuity):</strong> The rate of curvature change is continuous, eliminating microscopic highlight acceleration shifts.</li>
</ul>""",
        "sec4_title": "4. Real-Time Inspection & Zebra Diagnostic Analysis",
        "sec4_content": """
<p>In high-end industrial design, always activate dynamic Zebra stripe shaders in the CAD viewport. Discontinuous zebra stripes indicate G0 gaps; sharp zigzag breaks indicate G1 tangency; smooth continuous zebra ribbons confirm true G2/G3 curvature compliance.</p>"""
    },
    "open-design-alliance-drawing-sdk": {
        "sec3_title": "3. Native DWG/DXF Architecture & Cross-Platform Engines",
        "sec3_content": """
<p>The Open Design Alliance (ODA) develops independent SDKs that provide full read/write/render access to native DWG and DXF formats:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Drawing SDK (formerly Teigha / OpenDWG):</strong> Parses object database hierarchies, block records, layer tables, and extended entity data (xdata) without requiring Autodesk runtime engines.</li>
  <li><strong>Multi-Platform Support:</strong> Powers native DWG processing across Windows, Linux, macOS, iOS, Android, and WebAssembly cloud microservices.</li>
  <li><strong>Custom Object Enablers:</strong> Decodes complex proxy objects generated by specialized AEC, Mechanical, and Civil desktop software.</li>
</ul>""",
        "sec4_title": "4. Third-Party ISV Integration & Licensing Protocol",
        "sec4_content": """
<p>CAD developers integrating ODA SDKs must handle custom object enablers and non-standard geometric dictionaries carefully. Unhandled proxy entities can be converted into static proxy graphics if proper third-party module handlers are not registered before saving.</p>"""
    },
    "ordinate-dimensioning-baseline-drafting": {
        "sec3_title": "3. CNC Manufacturing & Datum Origin Workflows",
        "sec3_content": """
<p>Ordinate dimensioning measures perpendicular X and Y distances from a designated datum origin (0,0):</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Elimination of Clutter:</strong> Replaces tangled chains of dimension extension lines with clean single-line leader callouts along sheet metal plates and CNC hole patterns.</li>
  <li><strong>Direct Machine Tool Matching:</strong> The drawing datum origin aligns directly with the machine tool's Part Work Coordinate System (e.g., G54 origin), allowing CNC operators to verify drill coordinates instantly.</li>
  <li><strong>Zero Cumulative Error:</strong> Because every coordinate references the common origin, manufacturing tolerance errors never accumulate across hole arrays.</li>
</ul>""",
        "sec4_title": "4. Origin Placement & Orthogonal Verification",
        "sec4_content": """
<p>Before placing ordinate dimensions with the <code>DIMORDINATE</code> command, use the <code>UCS</code> command to relocate the user coordinate system origin to the primary manufacturing datum corner. Failure to reset the UCS will measure coordinates from arbitrary global space coordinates.</p>"""
    },
    "p-and-id-piping-instrumentation-diagram": {
        "sec3_title": "3. Schematic Symbology & ISA 5.1 Standards",
        "sec3_content": """
<p>Piping and Instrumentation Diagrams (P&ID) serve as the functional blueprint for chemical, energy, and water treatment processing plants:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Equipment Identifiers:</strong> Pumps, heat exchangers, pressure vessels, and tanks are tagged with standardized alphanumeric codes (e.g., P-101A for a slurry pump).</li>
  <li><strong>Piping Line Service Codes:</strong> Specifies nominal pipe size, process fluid code, piping specification class, and insulation thickness (e.g., 6"-PW-1002-1CS150-H).</li>
  <li><strong>Instrument Bubbles:</strong> Standard ISA 5.1 circles and squares indicate whether instrumentation (e.g., Pressure Indicator Controller - PIC) is field-mounted or displayed in the central distributed control system (DCS).</li>
</ul>""",
        "sec4_title": "4. 2D-to-3D Piping Verification & Line List Consistency",
        "sec4_content": """
<p>In modern industrial engineering, intelligent P&ID databases feed directly into 3D plant modeling software. Discrepancies between P&ID line lists and 3D piping routing must be caught through automated line-list audits before spool fabrication begins.</p>"""
    },
    "parasolid-vs-acis-kernel": {
        "sec3_title": "3. Architectural Comparison of Commercial Kernels",
        "sec3_content": """
<p>Parasolid (Siemens) and ACIS (Spatial/Dassault Systèmes) represent the foundational 3D geometric modeling engines powering global engineering software:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Parasolid (.x_t / .x_b):</strong> Powers NX, SolidWorks, Solid Edge, and Mastercam. Known for exceptional numerical stability in complex multi-face variable fillets, sheet metal unbending, and high-performance Boolean operations.</li>
  <li><strong>ACIS (.sat / .sab):</strong> Powers AutoCAD, GstarCAD 3D, SpaceClaim, and BricsCAD. Utilizes a C++ object-oriented architecture optimized for flexible hybrid surface-solid modeling and cellular topology.</li>
  <li><strong>Neutral Translation:</strong> Translating geometry between Parasolid and ACIS engines is best accomplished via ISO STEP AP242 to minimize edge tolerance stitching errors.</li>
</ul>""",
        "sec4_title": "4. Kernel Imprecision & Direct Translation Healing",
        "sec4_content": """
<p>Directly converting between .x_t and .sat files can introduce microscopic vertex tolerance gaps (e.g., 0.005mm) where face boundaries do not evaluate to identical parametric curves. Enterprise CAD workflows apply automated edge stitching and tolerance healing routines upon geometry import.</p>"""
    },
    "point-cloud-decimation-registration": {
        "sec3_title": "3. Registration Algorithms & Spatial Voxel Grid Filtering",
        "sec3_content": """
<p>Terrestrial and mobile LiDAR scanners produce billions of spatial coordinate points requiring structured processing before CAD import:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Target-Based & Cloud-to-Cloud Alignment:</strong> Coarse registration uses surveyed spherical targets; fine alignment uses the Iterative Closest Point (ICP) algorithm to minimize Euclidean point-to-plane deviations.</li>
  <li><strong>Spatial Voxel Grid Decimation:</strong> Replaces random point thinning with uniform 3D cubic voxel filters (e.g., 10mm cubes), retaining one representative point per voxel to normalize density across near and far scan fields.</li>
  <li><strong>Feature Extraction:</strong> Edge-detection filters identify planes, cylinders, and curb feature lines for automated As-Built model reconstruction.</li>
</ul>""",
        "sec4_title": "4. Registration Errors & Hardware Acceleration",
        "sec4_content": """
<p>Never import raw un-decimated scan clouds containing hundreds of millions of points directly into standard drafting viewports. This exhausts workstation GPU VRAM and causes viewport frame rates to drop below 5 FPS. Always index point clouds into structured octree formats (e.g., RCP/RCS or LAS/E57) with level-of-detail culling enabled.</p>"""
    },
    "runout-circular-and-total-tolerance": {
        "sec3_title": "3. Dial Indicator Verification & Mechanical Function",
        "sec3_content": """
<p>Runout tolerances control the composite variation of rotating rotational surfaces relative to a datum axis:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Circular Runout (Single Arrow):</strong> Evaluates individual 2D cross-sectional circular elements as the part is rotated 360 degrees about its datum axis, controlling circularity and coaxiality.</li>
  <li><strong>Total Runout (Double Arrow):</strong> Measures the full 3D surface simultaneously as the indicator traverses axially while the part rotates, controlling circularity, straightness, coaxiality, angularity, and taper.</li>
  <li><strong>Dial Indicator Setup:</strong> The physical inspection setup mounts a dial indicator perpendicular to the rotating shaft supported on datum centers.</li>
</ul>""",
        "sec4_title": "4. Functional Allocation & Manufacturing Costs",
        "sec4_content": """
<p>Specifying Total Runout on non-critical spacer sleeves unnecessarily inflates grinding costs. Reserve Total Runout for high-speed transmission shafts, turbine rotors, and bearing journals where dynamic centrifugal unbalance causes severe vibration and premature bearing destruction.</p>"""
    },
    "sheet-metal-k-factor-bend-allowance": {
        "sec3_title": "3. Neutral Axis Physics & Flat Blank Formulas",
        "sec3_content": """
<p>When sheet metal bends, compressive stresses deform the inner radius while tensile stresses stretch the outer radius:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>K-Factor Definition:</strong> The ratio of the neutral axis position (t) to total material thickness (T): <code>K = t / T</code>. Typical air-bending K-factors range from 0.33 to 0.45.</li>
  <li><strong>Bend Allowance (BA) Formula:</strong> <code>BA = &pi; * (R + K * T) * (&theta; / 180)</code>, calculating the arc length along the unstretched neutral layer.</li>
  <li><strong>Bend Deduction (BD):</strong> The amount subtracted from the sum of the flange lengths to calculate the precise flat blank cutting pattern.</li>
</ul>""",
        "sec4_title": "4. Press Brake Tooling & Empirical Calibration",
        "sec4_content": """
<p>Using CAD default K-factors (such as 0.50) without calibration results in flat blanks that are consistently 1-2mm too long when bent on shop-floor press brakes. Quality managers must run physical bend coupon tests for each specific material gauge, V-die opening width, and punch radius to establish verified bend tables.</p>"""
    },
    "step-ap242-semantic-pmi": {
        "sec3_title": "3. Model-Based Definition & Digital Thread Integration",
        "sec3_content": """
<p>ISO 10303-242 (STEP AP242) standardizes Model-Based Definition (MBD) for downstream digital manufacturing:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Semantic PMI Data Structures:</strong> Embeds GD&T feature control frames, datums, and surface finishes as machine-readable digital entities rather than dumb graphical vector polylines.</li>
  <li><strong>Automated CMM Programming:</strong> Inspection software parses the semantic STEP model to generate automated coordinate measuring probe paths with zero human transcription errors.</li>
  <li><strong>Feature-Based CAM Toolpaths:</strong> CNC CAM software reads semantic hole tolerances directly, automatically selecting appropriate drilling or reaming tool sizes.</li>
</ul>""",
        "sec4_title": "4. Downstream Reader Compatibility & Archive Validation",
        "sec4_content": """
<p>Ensure that downstream suppliers have certified STEP AP242 semantic readers before discontinuing 2D inspection drawings. Validating neutral STEP models against native CAD geometry with automated 3D comparison tools ensures that complex surface trims and annotations translate faithfully.</p>"""
    },
    "surface-roughness-symbols-iso-1302": {
        "sec3_title": "3. Surface Texture Parameters & Drawing Annotation",
        "sec3_content": """
<p>ISO 1302 and ASME B46.1 specify standardized graphical symbols and parameters to control surface finishes on machined components:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Ra (Roughness Average):</strong> The arithmetic mean deviation of the assessed surface profile heights from the center line.</li>
  <li><strong>Rz (Maximum Peak-to-Valley Height):</strong> Measures the vertical distance between the highest peak and deepest valley within a sampling length, catching sharp scratches that cause seal leaks.</li>
  <li><strong>Machining Method Specifiers:</strong> Checkmark symbols specify whether material removal is mandatory (machined), prohibited (cast/forged), or optional.</li>
</ul>""",
        "sec4_title": "4. Tribological Failures & Over-Specification Costs",
        "sec4_content": """
<p>Demanding unnecessarily fine finishes (e.g., Ra 0.2&mu;m where Ra 1.6&mu;m is functional) forces shops into secondary cylindrical grinding or lapping operations, multiplying component manufacturing costs 4x to 8x. However, on hydraulic piston rods, relying solely on Ra without specifying Rz can permit sharp valley grooves that shred rubber lip seals.</p>"""
    },
    "tolerances-limits-and-fits-iso-286": {
        "sec3_title": "3. Hole-Basis & Shaft-Basis Fit Categories",
        "sec3_content": """
<p>ISO 286 provides a standardized system of fundamental tolerance grades (IT01 to IT18) and fundamental deviations (letters A-ZC for holes, a-zc for shafts):</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Clearance Fits (e.g., H7/g6, H7/f7):</strong> Guarantees positive clearance between mating parts for sliding shafts, rotating bearings, and free axial guides.</li>
  <li><strong>Transition Fits (e.g., H7/k6, H7/m6):</strong> May produce slight clearance or slight interference, used for precision rigid location with light mallet assembly.</li>
  <li><strong>Interference Fits (e.g., H7/p6, H7/s6):</strong> Guarantees negative clearance, creating heavy friction joints for press-fit bushings and gears requiring thermal shrink fitting.</li>
</ul>""",
        "sec4_title": "4. Hole-Basis System Standard Operating Procedure",
        "sec4_content": """
<p>Standard manufacturing practice dictates using the Hole-Basis system (specifying hole tolerance H7), because standard reamers, drills, and plug gages are manufactured to fixed H sizes. Shafts can be turned and ground flexibly to arbitrary tolerance classes on standard lathes.</p>"""
    },
    "topological-naming-problem": {
        "sec3_title": "3. Parametric Dependency Graphs & Reference Failures",
        "sec3_content": """
<p>The Topological Naming Problem occurs in feature-based parametric CAD engines when internal face/edge indices change after upstream edits:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Entity Numbering Instability:</strong> If an engineer edits Feature 1 to add a chamfer, the solid modeler re-indexes all adjacent faces (e.g., Face14 becomes Face16).</li>
  <li><strong>Dangling Child Features:</strong> Downstream sketches, fillets, or mates referencing the original internal face handle lose their parent anchor, triggering rebuild errors.</li>
  <li><strong>Persistent Naming Mechanisms:</strong> Modern kernels use geometric history tracking and local adjacency tracking to resolve persistent naming across regenerations.</li>
</ul>""",
        "sec4_title": "4. Modeling Defensive Strategies",
        "sec4_content": """
<p>To insulate models against TNP failures: attach sketches to primary datum planes and master coordinate systems rather than model faces; centralize core dimensions in top-level skeleton sketches; and apply fillets and cosmetic chamfers at the very bottom of the feature tree.</p>"""
    },
    "true-position-tolerance-hole-patterns": {
        "sec3_title": "3. Cylindrical Tolerance Zones & True Position Math",
        "sec3_content": """
<p>True Position per ASME Y14.5 replaces legacy rectangular plus-minus coordinate tolerance zones with cylindrical tolerance fields:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>57% Extra Usable Area:</strong> A cylindrical tolerance zone (&empty; 0.28mm) circumscribes a square &plusmn;0.10mm box, providing 57% more allowable manufacturing zone without reducing functional clearance.</li>
  <li><strong>True Position Formula:</strong> <code>Position Deviation = 2 * &radic;((X_actual - X_basic)&sup2; + (Y_actual - Y_basic)&sup2;)</code>.</li>
  <li><strong>Pattern Composite Callouts:</strong> Dual-tier feature control frames control pattern location relative to external datums in the top tier, while tightly controlling hole-to-hole spacing in the lower tier.</li>
</ul>""",
        "sec4_title": "4. Functional Assembly Verification",
        "sec4_content": """
<p>When inspecting multi-hole flange patterns, coordinate deviation must be evaluated simultaneously across all holes when Maximum Material Condition is invoked. Inspecting holes individually on calipers masks collective pattern rotation errors that cause assembly bolt jamming.</p>"""
    },
    "welding-symbols-iso-2553": {
        "sec3_title": "3. Arrow Side, Other Side & Dual Reference Lines",
        "sec3_content": """
<p>ISO 2553 defines a rigorous graphical shorthand to communicate weld types, sizes, and inspection requirements on fabrication drawings:</p>
<ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
  <li><strong>Arrow Side vs. Other Side:</strong> Weld symbols placed on the solid reference line apply to the side pointed to by the arrow; symbols placed on the dashed identification line apply to the opposite side.</li>
  <li><strong>Fillet Weld Dimensions:</strong> Leg length is designated with prefix 'z' (e.g., z8), while design throat thickness is designated with prefix 'a' (e.g., a6).</li>
  <li><strong>Peripheral & Field Welds:</strong> A circle at the reference line elbow indicates an all-around weld; a black flag symbol indicates an on-site field weld.</li>
</ul>""",
        "sec4_title": "4. Structural Safety & Drawing Ambiguity Risks",
        "sec4_content": """
<p>Confusing throat thickness ('a') with leg length ('z') will undersize the physical weld by approximately 30%, risking catastrophic structural joint failure under dynamic fatigue loads. Quality assurance protocols mandate verifying that fabricators interpret dual reference lines according to the specified ISO 2553 standard version.</p>"""
    }
}

def enrich():
    updated = 0
    for slug, data in ENRICHMENTS.items():
        file_path = CONCEPTS_DIR / f"{slug}.html"
        if not file_path.exists():
            print(f"Warning: {file_path} not found!")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")
        article = soup.find("article", class_="kb-concept-detail")
        if not article:
            print(f"Warning: article not found in {file_path}")
            continue

        # Find existing sections
        sections = article.find_all("section", class_="kb-concept-section")
        if len(sections) >= 4:
            print(f"Already enriched: {slug}")
            continue

        # Locate insertion point before the cross-disciplinary resources section
        resource_sec = sections[-1] if sections else None

        new_sec3 = soup.new_tag("section", attrs={"class": "kb-concept-section"})
        new_sec3_h2 = soup.new_tag("h2")
        new_sec3_h2.string = data["sec3_title"]
        new_sec3.append(new_sec3_h2)
        sec3_soup = BeautifulSoup(data["sec3_content"], "html.parser")
        new_sec3.append(sec3_soup)

        new_sec4 = soup.new_tag("section", attrs={"class": "kb-concept-section"})
        new_sec4_h2 = soup.new_tag("h2")
        new_sec4_h2.string = data["sec4_title"]
        new_sec4.append(new_sec4_h2)
        sec4_soup = BeautifulSoup(data["sec4_content"], "html.parser")
        new_sec4.append(sec4_soup)

        if resource_sec:
            resource_sec.insert_before(new_sec3)
            resource_sec.insert_before(new_sec4)
        else:
            article.append(new_sec3)
            article.append(new_sec4)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        updated += 1
        print(f"Successfully enriched: {slug}.html")

    print(f"\nTotal concept pages enriched: {updated} / {len(ENRICHMENTS)}")

if __name__ == "__main__":
    enrich()
