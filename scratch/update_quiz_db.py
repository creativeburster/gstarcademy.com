import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
quiz_js_path = os.path.join(ROOT_DIR, "quiz.js")

with open(quiz_js_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "  const QUIZ_DATABASE = {"
end_marker = "  // 2. 状态机与游戏数据初始化"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_db_str = """  const QUIZ_DATABASE = {
    bim: {
      trackTitle: "BIM Coordinator",
      trackBadge: "🏢 BIM",
      nodesToMaster: ["bim", "revit", "shared-coords", "clash", "ifc"],
      lessons: [
        {
          id: 1,
          title: "Lesson 1: Warmup",
          desc: "BIM Paradigms, LOD Standards, & CDE Workflow",
          questions: [
            {
              type: "single",
              nodeId: "bim",
              slug: "bim",
              question: "BIM (Building Information Modeling) compared to traditional 2D drafting represents a fundamental paradigm shift. What is its core technical characteristic?",
              options: [
                "Replacing geometric lines with smart, parametric objects mapped to a relational database.",
                "Utilizing faster graphics acceleration cards to render simple drawing files.",
                "Replacing all keyboards with mouse drag-and-drop actions for sketching.",
                "Creating flattened PDF files that cannot be edited by subcontractors."
              ],
              correctIdx: 0,
              why: "BIM shifts drafting from drawing simple 2D lines to placing intelligent object elements (walls, ducts) containing rich physical and functional metadata.",
              pitfall: "Do not confuse BIM with simple 3D modeling. A pure 3D drawing without attached data attributes is not a true BIM database."
            },
            {
              type: "single",
              nodeId: "bim",
              slug: "lod-bim",
              question: "In BIM specifications, Level of Development (LOD) defines the clarity of model elements. What is the fundamental difference between LOD 300 and LOD 400?",
              options: [
                "LOD 300 contains approximate sizing for aesthetic design, while LOD 400 includes precise fabrication, assembly, and installation details.",
                "LOD 300 is rendered in grayscale, whereas LOD 400 must have textured colors.",
                "LOD 300 runs on local PCs, while LOD 400 requires cloud database servers.",
                "LOD 300 represents 2D schematic layouts, while LOD 400 represents 3D views."
              ],
              correctIdx: 0,
              why: "LOD 300 model elements are suitable for construction design with specific size, shape, and location. LOD 400 adds precise shop drawing and fabrication-level detailing.",
              pitfall: "Avoid demanding LOD 400/500 globally across the whole project in contract terms; this creates massive file bloat and wastes coordinator hours."
            },
            {
              type: "single",
              nodeId: "bim",
              slug: "common-data-environment",
              question: "A Common Data Environment (CDE) is defined under ISO 19650 for BIM projects. What represents its primary information flow strategy?",
              options: [
                "Separating information into Work in Progress (WIP), Shared, Published, and Archived states with structured sign-offs.",
                "Hosting all files on a single open-source folder without permission restriction.",
                "Automatically deleting all drawing revisions after 30 days to save server storage.",
                "Restricting file formats strictly to PDF to prevent editing by structural consultants."
              ],
              correctIdx: 0,
              why: "CDE manages information flow states. Teams work privately in WIP, share approved files in Shared, publish contractual sets in Published, and store records in Archived.",
              pitfall: "Always establish clear gates and metadata approvals before moving a model from WIP to Shared, otherwise coordinated errors proliferate."
            },
            {
              type: "single",
              nodeId: "bim",
              slug: "cobie-data-standard",
              question: "What represents the primary industry purpose of the COBie (Construction Operations Building Information Exchange) standard?",
              options: [
                "Providing a structured spreadsheet-like format to deliver asset and maintenance metadata to facility managers.",
                "Establishing an online licensing store to buy Revit families and scripts.",
                "Compressing DWG coordinates down to tiny vector lines for email handoffs.",
                "Encrypting BIM models so unauthorized subcontractors cannot view parameters."
              ],
              correctIdx: 0,
              why: "COBie captures equipment lists, product data sheets, warranties, and space coordinates at handover, letting facility managers load asset management software directly.",
              pitfall: "Define COBie parameters early in the project. Trying to populate asset data sheets at 100% construction completion is extremely expensive."
            },
            {
              type: "single",
              nodeId: "bim",
              slug: "bim-execution-plan",
              question: "What represents the primary technical role of a BIM Execution Plan (BEP) in a collaborative construction project?",
              options: [
                "Governing and defining the overall project team responsibilities, software versions, information delivery cycle, and coordination protocols.",
                "Listing the financial payroll details of structural subcontractors.",
                "Running automatic laser scans on site without operator supervision.",
                "Compressing 3D geometric coordinate meshes into 2D drawing blocks."
              ],
              correctIdx: 0,
              why: "A BEP governs the information management details of the project, aligning all parties on tools, protocols, and coordination schedules before work begins.",
              pitfall: "Do not treat BEP as a static contractual file. It must be updated iteratively as new sub-designers onboard to avoid software conflicts."
            },
            {
              type: "multiple",
              nodeId: "bim",
              slug: "bim-open-standards-iso",
              question: "Which of the following data exchange formats are defined by buildingSMART as vendor-neutral open standards for openBIM coordination? (Select all correct)",
              options: [
                "IFC (Industry Foundation Classes) for geometric and metadata exchange",
                "BCF (BIM Collaboration Format) for coordination clash tagging",
                "COBie (Construction Operations Building Information Exchange) for facility asset handovers",
                "NWD (Navisworks Document) proprietary review files"
              ],
              correctIndices: [0, 1, 2],
              why: "IFC, BCF, and COBie are buildingSMART certified open standards. NWD is a proprietary Autodesk format.",
              pitfall: "Always specify the required IFC Schema (e.g., IFC4 Reference View) in the BEP, as wrong export configurations will strip custom parameters."
            }
          ]
        },
        {
          id: 2,
          title: "Lesson 2: Core Concepts",
          desc: "Revit Family System, Shared Coordinates, & Scan-to-BIM",
          questions: [
            {
              type: "single",
              nodeId: "revit",
              slug: "revit",
              question: "When coordinating models in Autodesk Revit, what is the primary structural role of a 'Family' (.rfa)?",
              options: [
                "A temporary annotation note used to highlight drawing mistakes.",
                "A reusable component containing parametric geometry and metadata definitions.",
                "A software script used to import building permit approvals.",
                "An archive file format used to zip and email backup folders."
              ],
              correctIdx: 1,
              why: "Revit families are the building blocks of BIM models. They represent parametric components (like windows, air terminals) that scale and adjust based on parameters.",
              pitfall: "Avoid loading too many high-polygon nested families, as they dramatically increase file size and degrade project pan/zoom performance."
            },
            {
              type: "single",
              nodeId: "shared-coords",
              slug: "shared-coordinates-revit",
              question: "Why is establishing 'Shared Coordinates' critical in a multi-disciplinary BIM coordination pipeline?",
              options: [
                "It permits all team members to use the same software login credentials.",
                "It forces all text annotations to use the same font and size across companies.",
                "It aligns independent architectural, structural, and MEP models in a unified global coordinate system.",
                "It locks the files so only the chief coordinator can modify drawing dimensions."
              ],
              correctIdx: 2,
              why: "Shared Coordinates create a common origin point, allowing models created by different disciplines (structural engineers, architects) to compile and coordinate seamlessly without geometric shift.",
              pitfall: "Never manually drag misaligned models into position. Always bind and sync coordinate systems through Acquire/Publish coordinates."
            },
            {
              type: "single",
              nodeId: "bim",
              slug: "scan-to-bim-point-cloud",
              question: "When implementing Scan-to-BIM workflows, why is matching the survey target/control point network critical when importing point clouds?",
              options: [
                "It registers the point cloud to the identical real-world site coordinate system, preventing misalignment with the design model.",
                "It compresses the laser point cloud files so they can be loaded on basic mobile devices.",
                "It automatically converts raw point cloud dots into editable parametric Revit doors and windows.",
                "It clears system RAM so rendering programs can paint lighting reflections."
              ],
              correctIdx: 0,
              why: "Aligning point clouds to survey control targets ensures the scanned 'as-built' geometry overlays exactly on the design coordinate origin.",
              pitfall: "Never manually align point clouds by eye. A minor rotation offset can result in major coordinate errors at the far ends of a large warehouse site."
            },
            {
              type: "single",
              nodeId: "revit",
              slug: "revit-parameter-types",
              question: "In Autodesk Revit, what is the primary structural difference between 'Project Parameters' and 'Shared Parameters'?",
              options: [
                "Project Parameters can appear in schedules but not in tags; Shared Parameters can appear in both schedules and drawing annotation tags.",
                "Project Parameters are stored in the cloud; Shared Parameters are stored on local PCs.",
                "Project Parameters control wall lengths; Shared Parameters control door colors only.",
                "Project Parameters are read-only; Shared Parameters are editable by all trades."
              ],
              correctIdx: 0,
              why: "Shared Parameters are stored in an external text file (.txt) with unique GUIDs, allowing them to appear in drawing labels and tags, unlike Project parameters.",
              pitfall: "Never edit the Shared Parameter TXT file manually in Notepad; doing so can corrupt parameters GUID links, breaking schedules."
            },
            {
              type: "multiple",
              nodeId: "shared-coords",
              slug: "shared-coordinates-setup-actions",
              question: "Which of the following actions are standard Revit workflows for coordinating model alignment? (Select all correct)",
              options: [
                "Acquiring coordinates from a linked survey CAD or Revit file",
                "Publishing coordinates to linked structural or MEP sub-files",
                "Manually dragging and rotating linked models visually to match geometric lines",
                "Specifying coordinate parameters directly at a known Point based on survey markers"
              ],
              correctIndices: [0, 1, 3],
              why: "Acquire, Publish, and Specify Coordinates are Revit's coordinate control tools. Manual shifts create misalignment errors.",
              pitfall: "Avoid manually dragging survey coordinate points after coordinates have been established; this shifts coordinate systems."
            }
          ]
        },
        {
          id: 3,
          title: "Lesson 3: Common Pitfalls",
          desc: "Navisworks Clashes, IFC Settings, & 4D/5D Simulation",
          questions: [
            {
              type: "single",
              nodeId: "clash",
              slug: "navisworks-clash-detection",
              question: "In Navisworks Clash Detective, what is the primary benefit of performing 'Clash Detection' before site construction?",
              options: [
                "It automatically recalculates structural calculations to verify steel loads.",
                "It identifies spatial intersections and physical conflicts between MEP pipes and structural concrete.",
                "It runs rendering scenes to select aesthetic wall paint colors for clients.",
                "It prints out physical paper copies of sheet lists for foreman logs."
              ],
              correctIdx: 1,
              why: "Clash Detection flags physical clashes (e.g. an HVAC duct passing through a structural steel beam) digitally, letting teams solve routing conflicts in office coordinates rather than paying for field rebuilds.",
              pitfall: "Set realistic clearance tolerances in Navisworks; setting tolerance too tight (e.g. 0mm) creates thousands of false-positive warnings."
            },
            {
              type: "single",
              nodeId: "ifc",
              slug: "ifc-export-revit",
              question: "What is the primary industry purpose of exporting coordinates and metadata to IFC (Industry Foundation Classes) format?",
              options: [
                "To encrypt drawing databases so competitors cannot steal geometry secrets.",
                "To enable open-standard data exchange between competing BIM platforms (Revit, Bentley, ArchiCAD).",
                "To compress the file size down to under 1 Megabyte for mobile browsing.",
                "To automatically generate invoice bills for structural material purchases."
              ],
              correctIdx: 1,
              why: "IFC is a neutral, open standard for BIM. It permits teams using different design platforms to share rich coordinate and metadata assets without vendor-lock.",
              pitfall: "Check your Model View Definition (MVD) configuration when exporting IFC; selecting the wrong MVD can drop parameter metadata fields."
            },
            {
              type: "single",
              nodeId: "bim",
              slug: "4d-construction-simulation",
              question: "What defines 4D and 5D BIM integrations in virtual design and construction (VDC) workflows?",
              options: [
                "4D adds construction schedule time to elements; 5D links model elements to cost and budget databases.",
                "4D represents four-dimensional hyper-spheres; 5D represents five-dimensional matrix render engines.",
                "4D refers to high-speed render refresh rates; 5D refers to smell and touch VR simulations.",
                "4D is for mobile layout checking; 5D is for cloud database backup transfers."
              ],
              correctIdx: 0,
              why: "4D binds BIM objects to CPM project schedules (like Primavera/MS Project) to simulate staging. 5D connects quantities from elements to cost estimate databases.",
              pitfall: "Do not attempt 4D/5D simulation on unstructured models. Objects must be grouped and named consistently to map cleanly to WBS schedule tasks."
            },
            {
              type: "single",
              nodeId: "clash",
              slug: "navisworks-search-sets-clash",
              question: "Why are 'Search Sets' preferred over 'Selection Sets' when setting up clash detection runs in Navisworks?",
              options: [
                "Search Sets dynamically update to include new model elements based on search criteria; Selection Sets are static lists of specific elements.",
                "Search Sets compress files better, while Selection Sets slow down CPU speeds.",
                "Search Sets are only compatible with Revit, while Selection Sets work with all CADs.",
                "Search Sets encrypt model data, preventing edits by structural teams."
              ],
              correctIdx: 0,
              why: "Search Sets query database parameters dynamically. When updated model files are loaded, new items matching the query are automatically checked.",
              pitfall: "Ensure parameter naming is standardized in CAD/BIM authors, otherwise Search Sets queries will miss elements, leading to undetected clashes."
            },
            {
              type: "multiple",
              nodeId: "ifc",
              slug: "ifc-schema-mvd-options",
              question: "When configuring IFC exports for cross-disciplinary coordination, which Model View Definitions (MVDs) are buildingSMART standards? (Select all correct)",
              options: [
                "IFC2x3 Coordination View 2.0",
                "IFC4 Reference View",
                "IFC4 Design Transfer View",
                "IFC2x3 Graphic JPG Rendering View"
              ],
              correctIndices: [0, 1, 2],
              why: "Coordination View 2.0, Reference View, and Design Transfer View are buildingSMART certified MVDs. JPG views are rendering standards, not BIM IFC standards.",
              pitfall: "Always test IFC exports with model checkers before project handoffs to ensure the MVD did not drop custom metadata parameters."
            }
          ]
        }
      ]
    },
    mcad: {
      trackTitle: "Mechanical Design Engineer",
      trackBadge: "⚙️ MCAD",
      nodesToMaster: ["parametrics", "solidworks", "brep", "assembly", "mbd"],
      lessons: [
        {
          id: 1,
          title: "Lesson 1: Warmup",
          desc: "Geometric Constraints, SOLIDWORKS Configurations, & PDM",
          questions: [
            {
              type: "single",
              nodeId: "parametrics",
              slug: "parametric-constraints",
              question: "In parametric sketch design, what is the core purpose of defining geometric constraints (e.g., Tangent, Concentric, Parallel)?",
              options: [
                "To specify the color values used when sending drawing files to CAM.",
                "To lock and govern geometric relationships, ensuring changes preserve design intent.",
                "To limit the speed of the CPU when rendering complex surface fillets.",
                "To restrict drawing models to 2D projections without 3D depth parameters."
              ],
              correctIdx: 1,
              why: "Geometric constraints define the structural rules of design. If a circle is constrained as Tangent to a line, it remains tangent even when you modify dimensions.",
              pitfall: "Avoid over-constraining sketches. Redundant constraints cause solver conflicts and regeneration errors in feature trees."
            },
            {
              type: "single",
              nodeId: "solidworks",
              slug: "solidworks-configurations",
              question: "In SOLIDWORKS, what represents the primary assembly-level benefit of creating part 'Configurations'?",
              options: [
                "Allowing multiple design variations (different sizes, features, or materials) to exist in a single CAD model file.",
                "Encrypting drawings so structural subconsultants cannot load model parameters.",
                "Increasing the screen rendering frame rate of complex assembly views.",
                "Translating dimension values into multiple language text annotations."
              ],
              correctIdx: 0,
              why: "Configurations allow variations of a part (e.g., standard M6 bolt vs M8 bolt) to live in one file, keeping assemblies uncluttered and lightweight.",
              pitfall: "Avoid changing configuration names after referencing them in parent assembly files, as this can break references."
            },
            {
              type: "single",
              nodeId: "solidworks",
              slug: "solidworks-pdm-vault",
              question: "When multiple mechanical engineers collaborate on a large machine assembly in SOLIDWORKS PDM, what is the purpose of the 'Check-Out' operation?",
              options: [
                "Locking the part file so only the checker can edit it, preventing concurrent modification overrides.",
                "Zipping the assembly files into an email folder to send to structural clients.",
                "Exporting coordinates straight to 3D printers without mesh verification.",
                "Deleting previous drawing revisions from the central server vault."
              ],
              correctIdx: 0,
              why: "Check-out acts as a write-lock, giving the user exclusive rights to modify a part file, while other team members see the latest read-only version.",
              pitfall: "Never modify local files without checking them out first. Changes made outside checkout will be overwritten on next vault sync."
            },
            {
              type: "multiple",
              nodeId: "parametrics",
              slug: "solidworks-fully-defined-circle",
              question: "In parametric sketch design, which dimensions or constraints are needed to make a circle fully defined (green/black)? (Select all correct)",
              options: [
                "Diameter or radius dimension",
                "Horizontal distance (X coordinate) from center to origin",
                "Vertical distance (Y coordinate) from center to origin",
                "Drawing view scale factor"
              ],
              correctIndices: [0, 1, 2],
              why: "A circle requires size (diameter) and position (X and Y coordinates) to be fully defined. View scale is an output parameter, not a sketch constraint.",
              pitfall: "Avoid leaving sketch entities under-defined (blue), as they can shift unpredictably when parent features are modified."
            }
          ]
        },
        {
          id: 2,
          title: "Lesson 2: Core Concepts",
          desc: "B-Rep Modelling, Assembly Constraints, & 3D MBD",
          questions: [
            {
              type: "single",
              nodeId: "brep",
              slug: "boundary-representation",
              question: "In solid modeling kernels (like Parasolid or ACIS), what defines Boundary Representation (B-Rep) geometry?",
              options: [
                "Storing 3D solids by mapping their boundary topological elements (faces, edges, vertices) connected to geometric surfaces and curves.",
                "Splitting 3D parts into millions of tiny grid points for fluid dynamics checks.",
                "Creating 2D flat drawings and scanning them to generate solid meshes.",
                "Encrypting structural parameters to protect model security properties."
              ],
              correctIdx: 0,
              why: "B-Rep represents solids mathematically through topology (faces/edges) linked to geometric shapes (cylinders/lines), permitting exact coordinate calculations.",
              pitfall: "B-Rep files can suffer from 'topological naming problems' during model updates. Editing early features can break subsequent edge fillets."
            },
            {
              type: "single",
              nodeId: "assembly",
              slug: "assembly-mating-constraints",
              question: "Why is utilizing concentric, coincident, and distance mates critical when designing large assemblies in SOLIDWORKS?",
              options: [
                "It coordinates drawing scales, making prints match paper sizes.",
                "It restricts parts from rotating so that assemblies remain static during structural scans.",
                "It restricts degrees of freedom (DOF) between parts, reflecting physical assembly fit.",
                "It encrypts components coordinates to prevent coordinate leakage."
              ],
              correctIdx: 2,
              why: "Assembly mates restrict mechanical DOF (translation/rotation), allowing CAD tools to calculate kinematic movements and assembly clearances.",
              pitfall: "Over-constraining assemblies with conflicting mates creates mate errors, slowing down model calculation times."
            },
            {
              type: "single",
              nodeId: "mbd",
              slug: "model-based-definition",
              question: "What is the primary technical goal of adopting Model-Based Definition (MBD) in modern manufacturing CAD?",
              options: [
                "Attaching all Product Manufacturing Information (PMI, GD&T, and finishes) directly in the 3D model, eliminating the need for 2D drawings.",
                "Converting 3D parts to flat 2D PDF sketches to print on site plans.",
                "Sending parts design directly to structural coordinate check files.",
                "Limiting parts design to 3D rendering viewports on mobile devices."
              ],
              correctIdx: 0,
              why: "MBD turns the 3D model into the single source of truth. Software (like CAM/CMM) can read the PMI metadata directly, eliminating drafting overhead.",
              pitfall: "Adopting MBD requires a supply chain capable of reading STEP AP242 or native PMI. Do not drop 2D drawings if suppliers cannot read PMI."
            },
            {
              type: "multiple",
              nodeId: "mbd",
              slug: "mbd-pmi-components",
              question: "Which of the following manufacturing parameters are directly embedded in a 3D model when using Model-Based Definition (MBD)? (Select all correct)",
              options: [
                "GD&T (Geometric Dimensioning and Tolerancing) annotations",
                "Surface roughness/finish specifications",
                "Thread and fastener data specifications",
                "Supplier bank routing coordinates"
              ],
              correctIndices: [0, 1, 2],
              why: "GD&T, surface finish, and thread specs are core Product Manufacturing Information (PMI) embedded in MBD models. Supplier financials are not CAD metadata.",
              pitfall: "Ensure downstream CNC and CMM software can interpret semantic PMI; graphical-only PMI cannot be read automatically by machining tools."
            }
          ]
        },
        {
          id: 3,
          title: "Lesson 3: Common Pitfalls",
          desc: "Mesh FEA Convergence, Clearance Mates, & Tolerance Stack-up",
          questions: [
            {
              type: "single",
              nodeId: "solidworks",
              slug: "mesh-convergence-fea",
              question: "When conducting Finite Element Analysis (FEA) on a mechanical bracket, what is 'Mesh Convergence'?",
              options: [
                "Iteratively refining mesh sizing until the resulting stress values stabilize, ensuring the simulation results are mathematically independent of grid sizing.",
                "Merging two independent mesh networks to compile structural coordinate files.",
                "Compressing mesh nodes down to tiny vectors to fit in email attachments.",
                "Converting high-polygon CAD models into flat JPEG rendering drawings."
              ],
              correctIdx: 0,
              why: "Mesh convergence ensures accuracy. If stress values continue to jump drastically as mesh density increases, the FEA results are not mathematically converged.",
              pitfall: "Beware of stress singularities at sharp internal corners; infinite stress will result. Always model realistic fillets to avoid false singularities."
            },
            {
              type: "single",
              nodeId: "assembly",
              slug: "tolerance-stack-up",
              question: "In assembly manufacturing, what is 'Tolerance Stack-up analysis'?",
              options: [
                "Calculating cumulative dimensional tolerances across multiple mating parts to ensure components fit together without assembly interference.",
                "Measuring coordinate alignments in structural link files.",
                "Increasing structural sheet counts to accommodate revision listings.",
                "Encrypting dimension parameters to secure layout coordinate files."
              ],
              correctIdx: 0,
              why: "Every part has manufacturing variation. Stack-up analysis calculates worst-case or statistical tolerances to prevent assembly failures.",
              pitfall: "Avoid simple worst-case calculations on assemblies with many parts; this leads to over-designed, expensive tolerances. Use RSS (Root Sum Squares) statistical analysis."
            },
            {
              type: "multiple",
              nodeId: "assembly",
              slug: "interference-fit-causes",
              question: "In mechanical design, which of the following physical factors are common causes of assembly interference? (Select all correct)",
              options: [
                "Tolerance stack-up cumulative deviations",
                "Material thermal expansion under high operating temperatures",
                "Incorrect thread pitch or dimension matching between mating fasteners",
                "Missing CAD rendering scene texture files"
              ],
              correctIndices: [0, 1, 2],
              why: "Tolerance deviations, thermal expansion, and thread mismatches cause real assembly interference. Missing rendering textures only affect visuals, not geometry.",
              pitfall: "Perform clearance verification check runs under simulated operating temperatures if components utilize materials with varying thermal coefficients."
            }
          ]
        }
      ]
    },
    civil: {
      trackTitle: "Civil Infrastructure Specialist",
      trackBadge: "🏗️ Civil",
      nodesToMaster: ["terrain", "corridor", "alignment", "grading", "landxml"],
      lessons: [
        {
          id: 1,
          title: "Lesson 1: Warmup",
          desc: "TIN Surfaces, Horizontal Alignments, & Profile Grids",
          questions: [
            {
              type: "single",
              nodeId: "terrain",
              slug: "tin-surfaces-civil",
              question: "In infrastructure CAD (like Civil 3D), how is a Triangulated Irregular Network (TIN) Surface created?",
              options: [
                "By connecting height survey points in a network of non-overlapping triangles to model irregular ground levels.",
                "By drawing flat contour curves copied from paper plans.",
                "By writing coordinates lists on spreadsheet log databases.",
                "By exporting 2D text descriptions to structural databases."
              ],
              correctIdx: 0,
              why: "TIN surfaces offer exact mathematical representations of irregular ground surfaces, permitting Civil tools to calculate slopes and cut/fill volumes.",
              pitfall: "Always add breaklines along retaining walls and ditches, otherwise triangulation will inaccurately smooth out distinct grade changes."
            },
            {
              type: "single",
              nodeId: "alignment",
              slug: "horizontal-alignment-centerline",
              question: "Why is a 'Horizontal Alignment' critical in road and highway infrastructure projects?",
              options: [
                "It specifies the coordinate centerline (X-Y) of the road path, serving as the baseline for stations, corridor offsets, and profiles.",
                "It defines coordinate scales used to print drawings on sheets.",
                "It records soil moisture readings for environmental reports.",
                "It locks coordinate files so only coordinate checkers can edit layout parameters."
              ],
              correctIdx: 0,
              why: "Alignments establish the linear referencing system. Stationing (e.g. Sta 10+00) allows designers to coordinate coordinates, pipe outfalls, and lane widths.",
              pitfall: "Avoid editing alignments horizontally without locking station offsets; shifting centerlines can dislocate roadside structures."
            },
            {
              type: "multiple",
              nodeId: "terrain",
              slug: "civil-surface-data-sources",
              question: "In Civil 3D, which of the following data sources can be used to construct a TIN surface? (Select all correct)",
              options: [
                "COGO Points (Coordinate Geometry survey points)",
                "Contour lines with elevation properties",
                "Point cloud survey files",
                "Standard 2D text annotation strings without elevation data"
              ],
              correctIndices: [0, 1, 2],
              why: "COGO points, contour lines, and point clouds contain elevation data. Flat 2D text strings do not have height data to build a TIN surface.",
              pitfall: "Filter out redundant survey point clouds before building TIN surfaces; excessive density causes severe file size and rendering lag."
            }
          ]
        },
        {
          id: 2,
          title: "Lesson 2: Core Concepts",
          desc: "Vertical Profiles, Corridor Assemblies, & Cut & Fill Volumes",
          questions: [
            {
              type: "single",
              nodeId: "alignment",
              slug: "vertical-profile-grid",
              question: "How are Horizontal Alignments dynamically linked to Vertical Profiles in Civil 3D?",
              options: [
                "Shifting the horizontal centerline coordinates automatically recalculates and updates vertical elevations displayed in the profile viewport grid.",
                "Profiles control drawing text scales; alignments govern boundary offsets.",
                "Alignments govern structural walls; profiles gov structural coordinate checks.",
                "Profiles govern MCAD parameters; alignments govern civil coordinates."
              ],
              correctIdx: 0,
              why: "Civil 3D maintains dynamic links. Since the profile represents the elevation along the alignment path, modifying the horizontal centerline shifts the profile projection.",
              pitfall: "Always lock design vertical grade points to stations to ensure horizontal centerline shifts do not dislocate bridges."
            },
            {
              type: "single",
              nodeId: "corridor",
              slug: "corridor-assemblies",
              question: "What is the primary role of a 'Corridor Assembly' in road design workflows?",
              options: [
                "A template defining the road cross-section (lanes, curbs, sub-base, shoulders) swept along alignments to build 3D road volumes.",
                "A temporary drawing block representing construction warning signs.",
                "A script used to calculate tax invoices for highway materials.",
                "A coordinates filter used to compress surveying metadata lists."
              ],
              correctIdx: 0,
              why: "Assemblies combine subassemblies (lanes, curbs) to define the road shape. Sweeping this shape along alignments and profiles builds the 3D corridor database.",
              pitfall: "Verify target parameters for subassemblies; failing to assign targets (like daylighting to surface) results in roads suspended in mid-air."
            },
            {
              type: "multiple",
              nodeId: "corridor",
              slug: "earthwork-surface-comparisons",
              question: "When calculating earthwork cut and fill volumes for a new highway corridor, which surfaces must be compared? (Select all correct)",
              options: [
                "Existing Ground (EG) TIN Surface representing original site levels",
                "Proposed finished grading corridor surface (FG Surface)",
                "Sub-grade datum surface representing excavation levels under pavement",
                "Revit structural columns coordinate boundaries"
              ],
              correctIndices: [0, 1, 2],
              why: "EG, FG, and Sub-grade datum surfaces are compared to calculate cut/fill volumes. Revit columns are not used in civil site volume calculations.",
              pitfall: "Ensure boundary regions are locked in the volume properties, otherwise the volume engine will calculate outside site limits."
            }
          ]
        },
        {
          id: 3,
          title: "Lesson 3: Common Pitfalls",
          desc: "Grading Feature Lines, LandXML Transfers, & GIS Alignment",
          questions: [
            {
              type: "single",
              nodeId: "grading",
              slug: "grading-feature-lines",
              question: "When modeling site grading (e.g., retention ponds), what is the function of 'Feature Lines'?",
              options: [
                "3D vector lines containing elevations used as grading footprints and breaklines to build TIN grading surfaces.",
                "2D drawing lines used to frame print borders in Paper space.",
                "Text properties used to name different soil parameters.",
                "Coordinates filters used to encrypt surveying points logs."
              ],
              correctIdx: 0,
              why: "Feature lines hold exact X, Y, and Z elevations. They govern grading slopes (e.g., target a surface at 3:1 slope) and serve as breaklines for surface models.",
              pitfall: "Avoid overlapping feature lines in the same site footprint; conflicting elevation endpoints at intersections cause grading solver errors."
            },
            {
              type: "single",
              nodeId: "landxml",
              slug: "landxml-exchange-format",
              question: "Why is utilizing LandXML preferred for transferring civil models (surfaces, alignments, points) to construction field surveyors?",
              options: [
                "It is a neutral, open XML format that field GPS hardware and machine control systems can read directly, preventing file conversion errors.",
                "It compresses drawings down to tiny JPEG rendering icons for mobile browsers.",
                "It encrypts surveying data to protect coordinate security parameters.",
                "It automatically calculates labor costs for bulldozer crews."
              ],
              correctIdx: 0,
              why: "LandXML is open-standard. Surveyors and bulldozer machine control systems read LandXML directly to guide grading blades on site without CAD conversions.",
              pitfall: "Check your project unit settings (International Foot vs US Survey Foot) when exporting LandXML; minor scale offsets can cause significant alignment shifts."
            },
            {
              type: "multiple",
              nodeId: "terrain",
              slug: "civil-gis-alignments",
              question: "When importing civil CAD models into GIS platforms (such as ArcGIS Pro), which parameters are critical for correct alignment? (Select all correct)",
              options: [
                "EPSG Geodetic Coordinate reference system code",
                "Feature attribute metadata tables",
                "Geometric vector boundaries and shapes",
                "CAD software user license login parameters"
              ],
              correctIndices: [0, 1, 2],
              why: "EPSG codes, attribute tables, and vector shapes are critical to align and database CAD elements in GIS. CAD license login data is not geo-metadata.",
              pitfall: "Validate coordinate references before export; importing CAD models without EPSG codes will place the model in the middle of the ocean."
            }
          ]
        }
      ]
    },
    draft: {
      trackTitle: "2D Drafting Specialist",
      trackBadge: "📐 2D Draft",
      nodesToMaster: ["layers", "xrefs", "pgp", "annotative", "viewport", "purge"],
      lessons: [
        {
          id: 1,
          title: "Lesson 1: Warmup",
          desc: "Layer Strategies, External References (Xrefs), & keyboard PGP",
          questions: [
            {
              type: "single",
              nodeId: "layers",
              slug: "layer-strategies-cad",
              question: "In production drafting, why is utilizing standard naming conventions (like AIA CAD Standards) for 'Layers' critical?",
              options: [
                "To control geometry visibility, colors, and line weights across disciplines, preventing plot mismatches.",
                "To speed up the network file transfer rate when emailing files.",
                "To convert 2D lines into solid 3D coordinate model objects.",
                "To encrypt drawing files so structural coordinators cannot print sheets."
              ],
              correctIdx: 0,
              why: "Layers control display properties. Standardized layers ensure structural plans hide architectural grid annotations uniformly during plotting.",
              pitfall: "Avoid drawing everything on Layer 0; Layer 0 possesses unique block creation characteristics and makes visibility filters useless."
            },
            {
              type: "single",
              nodeId: "xrefs",
              slug: "xrefs-external-references",
              question: "Why is referencing drawing files via Xrefs preferred over copying static blocks in floor layouts?",
              options: [
                "Xrefs link background plans dynamically, updating changes automatically while keeping the drawing file lightweight.",
                "Xrefs support custom colors, whereas blocks are strictly monochrome.",
                "Xrefs permit LISP scripts automation, while blocks are static shapes.",
                "Xrefs are optimized for mobile viewers, whereas blocks require desktop seats."
              ],
              correctIdx: 0,
              why: "Xrefs allow concurrent work. When the base plan is modified, mechanical draftsmen referencing that base see the change instantly on reload.",
              pitfall: "Prefer relative path references for Xrefs. Absolute paths will break when files are migrated to cloud servers or shared with clients."
            },
            {
              type: "single",
              nodeId: "pgp",
              slug: "pgp-aliases-cad",
              question: "In native DWG programs (AutoCAD/GstarCAD), what is the function of the acad.pgp or gcad.pgp configuration files?",
              options: [
                "Mapping single or double-letter keyboard shortcuts to system commands to boost drafting speed.",
                "Storing coordinates parameters used in coordinate transformation matrix operations.",
                "Assigning user licenses to authorized drafter accounts.",
                "Restricting file access permissions for external subcontractors."
              ],
              correctIdx: 0,
              why: "PGP aliases enable keyboard-driven speed drafting, letting draftsmen execute commands with one hand while the other hand controls the mouse.",
              pitfall: "Document custom pgp shortcuts before upgrading CAD software, otherwise custom overrides may be lost during installation."
            },
            {
              type: "multiple",
              nodeId: "xrefs",
              slug: "xref-management-best-practices",
              question: "When sending coordinates and drawings containing Xrefs to structural consultants, which actions are recommended? (Select all correct)",
              options: [
                "Use 'Overlay' reference attachment type to prevent circular nesting errors",
                "Organize reference files in a relative directory folder structure",
                "Bind Xrefs using the 'Insert' option if delivering a self-contained static DWG archive",
                "Rename xref base files randomly to hide design revisions"
              ],
              correctIndices: [0, 1, 2],
              why: "Overlay type, relative paths, and Bind-Insert are standard practices for error-free Xref delivery. Random renaming breaks link associations.",
              pitfall: "Never use 'Attach' reference types for background layouts, as this creates circular reference dependencies that crash sessions."
            }
          ]
        },
        {
          id: 2,
          title: "Lesson 2: Core Concepts",
          desc: "Annotative Scales, Viewport Property Overrides, & DWG Audit",
          questions: [
            {
              type: "single",
              nodeId: "annotative",
              slug: "annotative-scales-cad",
              question: "What is the primary technical benefit of defining text and dimensions as 'Annotative' in CAD?",
              options: [
                "Annotative objects automatically scale their size based on the viewport scale, ensuring labels remain readable across different view layouts.",
                "Annotative objects automatically translate text annotations into coordinate files.",
                "Annotative objects encrypt drawings dimensions so layout checkers cannot alter values.",
                "Annotative objects convert 2D annotations into 3D Revit coordinates."
              ],
              correctIdx: 0,
              why: "Annotative scales manage annotation size. A note will print at 2.5mm height on paper whether the viewport scale is 1:50 or 1:100.",
              pitfall: "Avoid adding too many annotation scale factors to objects; this causes 'annotation scale bloat' and slows model open speeds."
            },
            {
              type: "single",
              nodeId: "viewport",
              slug: "viewport-overrides-layout",
              question: "In Paper Space layouts, how are Viewport Layer Overrides utilized?",
              options: [
                "They let designers assign unique colors, line weights, and display overrides to layers inside a specific viewport without altering global layers.",
                "They lock the drawing coordinates to protect data layout safety.",
                "They convert architectural viewports into structural coordinate views.",
                "They automatically delete old revisions inside viewport boundaries."
              ],
              correctIdx: 0,
              why: "Viewport overrides let designers present different layouts. A layer can plot in color on one layout and in grayscale on another layout.",
              pitfall: "Avoid manual line properties overrides (e.g. override color directly on object); this bypasses viewport overrides, breaking controls."
            },
            {
              type: "multiple",
              nodeId: "viewport",
              slug: "viewport-overrides-properties",
              question: "Which Layer properties can be controlled independently for individual viewports in Paper Space? (Select all correct)",
              options: [
                "VP Freeze (freezes the layer inside a specific viewport)",
                "VP Color (overrides the layer plot color per viewport)",
                "VP Linetype (overrides the layer linetype per viewport)",
                "Global Delete (removes the layer from the entire drawing)"
              ],
              correctIndices: [0, 1, 2],
              why: "VP Freeze, VP Color, and VP Linetype are viewport-specific overrides. Global Delete is a global database change, not a viewport property override.",
              pitfall: "Ensure drawing objects are set to 'ByLayer' properties, otherwise object-level overrides will block viewport-level property overrides."
            }
          ]
        },
        {
          id: 3,
          title: "Lesson 3: Common Pitfalls",
          desc: "Model vs Paper Space, Attributed Blocks, & DWG Purge",
          questions: [
            {
              type: "single",
              nodeId: "purge",
              slug: "dwg-purge-database",
              question: "Why is executing the PURGE command critical before finalizing and issuing CAD drawings?",
              options: [
                "It deletes unused block definitions, layers, and line types, significantly reducing DWG file size.",
                "It recalculates coordinates alignments to fix survey errors.",
                "It prints drawing lists onto central spreadsheet registers.",
                "It converts 2D drawings into 3D models."
              ],
              correctIdx: 0,
              why: "PURGE scans the DWG database, removing unreferenced definitions (blocks, layers) to optimize file storage and speed up project open times.",
              pitfall: "Purge cannot remove elements currently in use. If a block refuses to purge, search for hidden references or empty block entities."
            },
            {
              type: "single",
              nodeId: "viewport",
              slug: "model-vs-paper-space",
              question: "What represents the golden rule of separation between Model Space and Paper Space?",
              options: [
                "Draw all building geometry at 1:1 scale in Model Space; draw title borders, sheet layouts, and viewport frames in Paper Space.",
                "Draw architectural lines in Model Space; draw structural lines in Paper Space.",
                "Draw 3D geometry in Model Space; draw 2D layout projections in Paper Space.",
                "Save Model Space on local drives; Paper Space layouts are strictly on servers."
              ],
              correctIdx: 0,
              why: "Model space is the virtual CAD environment. Paper space layouts represent printed sheets and use viewports to frame and scale the model geometry.",
              pitfall: "Never draw building floor plans directly in Paper Space layouts; doing so disconnects plans from model coordinates, ruining coordinate alignments."
            },
            {
              type: "multiple",
              nodeId: "purge",
              slug: "attributed-block-elements",
              question: "When creating an Attributed Block in CAD to export BOM schedules, which definitions are required? (Select all correct)",
              options: [
                "Attribute Tag (the unique database parameter variable name)",
                "Attribute Prompt (the description text shown to the draftsman)",
                "Default attribute value",
                "CAD rendering texture file path"
              ],
              correctIndices: [0, 1, 2],
              why: "Tag, Prompt, and Default value are core attributes definitions. Texture files are rendering properties, not attributed block metadata.",
              pitfall: "Avoid using blank spaces in Attribute Tags (e.g. use 'DOOR_WIDTH' instead of 'DOOR WIDTH'), as spaces break BOM data table extraction scripts."
            }
          ]
        }
      ]
    },
    placement: {
      trackTitle: "Placement Test",
      trackBadge: "🏆 Placement",
      drawCount: 10,
      questions: [
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-bim-clash",
          question: "In a collaborative BIM project, which of the following is the standard workflow to identify geometric and spatial conflicts between different design disciplines (e.g., structural steel and MEP piping)?",
          options: [
            "Exporting models in IFC/NWC format and running Clash Detection tolerance checking inside Navisworks.",
            "Manually drawing 2D lines across architectural plans to measure physical clearance.",
            "Sending building materials details to structural engineers via spreadsheets.",
            "Rendering 3D scenes in standard browsers to check lighting reflections."
          ],
          correctIdx: 0,
          why: "Clash Detection in Navisworks flags spatial conflicts digitally early on, saving high field rework costs during site construction.",
          pitfall: "Do not manually check coordinate clashes by eyeball; coordinate coordinates shift and structural changes can make manuals obsolete."
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-bim-lod",
          question: "According to BIM specifications, what does LOD 400 represent compared to LOD 300?",
          options: [
            "Detailed fabrication, shop assembly, and installation instructions, rather than general layout and location intent.",
            "Utilizing monochrome wireframe rendering instead of photorealistic colors.",
            "Deploying local PC servers instead of high-speed cloud databases.",
            "Applying flat 2D projection sketches instead of 3D volumetric coordinates."
          ],
          correctIdx: 0,
          why: "LOD 300 defines approximate elements with general size and orientation. LOD 400 includes exact fabrication detailing suitable for site installers.",
          pitfall: "Avoid requiring LOD 400 across all MEP pipes in contract documents; this creates massive file bloat and wastes coordinator time."
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-mcad-constraints",
          question: "When building a parametric 3D CAD model, what is the primary role of geometric constraints (like Tangency or Concentricity)?",
          options: [
            "To capture and enforce design intent so that changing dimensions preserves correct geometric relationships.",
            "To limit the regeneration speed of complex feature trees.",
            "To define color properties of raw steel materials for CAM plots.",
            "To block the model from being edited by structural subconsultants."
          ],
          correctIdx: 0,
          why: "Geometric constraints ensure elements scale logically. If two cylinders are Concentric, they stay aligned even when diameter dimensions shift.",
          pitfall: "Do not over-constrain sketches; redundant constraints trigger solver conflicts and prevent feature tree regeneration."
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-mcad-mbd",
          question: "What is the ultimate technical goal of adopting Model-Based Definition (MBD) in mechanical design workflows?",
          options: [
            "Embedding all Product Manufacturing Information (PMI, GD&T, and finishes) directly in the 3D model, eliminating the need for separate 2D drawings.",
            "Replacing 3D solid models with high-resolution digital photographs of prototype components.",
            "Enabling CAM software to cut materials without human coordinator supervision.",
            "Converting CAD files to simple HTML sheets for browser viewings."
          ],
          correctIdx: 0,
          why: "MBD turns the 3D model into the single source of truth, letting downstream manufacturing software read annotations directly.",
          pitfall: "Ensure your supply chain is capable of reading STEP AP242 / native PMI data formats before completely dropping 2D drawing deliverables."
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-civil-tin",
          question: "In site terrain design, how does a Triangulated Irregular Network (TIN) surface represent the topographic model?",
          options: [
            "By connecting survey coordinate points in a dynamic network of non-overlapping triangles to calculate slope and drainage volumes.",
            "By rendering static horizontal contour lines copied from PDF sheets.",
            "By plotting spline lines representing underground pipeline trajectories.",
            "By logging a text table cataloging land parcel owners."
          ],
          correctIdx: 0,
          why: "TIN surfaces offer exact mathematical representations of irregular ground surfaces, which is critical to calculate earthwork volumes.",
          pitfall: "Always add breaklines at retaining walls and ditches, otherwise triangulation will inaccurately smooth slopes."
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-civil-alignments",
          question: "In infrastructure CAD (like Civil 3D), how are Horizontal Alignments dynamically linked to Vertical Profiles?",
          options: [
            "Alignments govern the horizontal X-Y centerline, and any coordinate changes instantly adjust the vertical elevation Z viewports in the profile grid.",
            "Profiles manage text label fonts, while alignments control printed scale styles.",
            "Alignments project site boundaries, while profiles record soil moisture data sheets.",
            "Profiles are used in building coordinate BIM, while alignments are strictly MCAD."
          ],
          correctIdx: 0,
          why: "Alignments and profiles are dynamically connected. Shifting a road path horizontally automatically adjusts the elevations displayed on the profile viewport.",
          pitfall: "Verify vertical clearances along alignments; structural pipe depths must remain below frost elevations."
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-draft-aliases",
          question: "In standard drafting systems (AutoCAD/GstarCAD), what is the function of the acad.pgp or gcad.pgp configuration files?",
          options: [
            "Mapping custom single or double-letter keyboard shortcuts to complex system commands to boost drafting speed.",
            "Storing coordinate systems parameters used in coordinate matrix operations.",
            "Assigning system access licenses to authorized user accounts.",
            "Restricting drawing files access to project coordinators only."
          ],
          correctIdx: 0,
          why: "Command aliases enable keyboard-driven speed drafting, letting draftsmen invoke commands with one hand on the keyboard and one on the mouse.",
          pitfall: "Always document custom pgp overrides so backups can be restored cleanly during platform migrations."
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-draft-xrefs",
          question: "Why is referencing drawings via Xrefs (External References) preferred over copying static blocks in multi-designer floor layouts?",
          options: [
            "Xrefs reference external files dynamically, ensuring background changes are updated automatically while keeping the master file size lightweight.",
            "Xrefs support custom colors, whereas blocks are strictly monochrome.",
            "Xrefs permit LISP scripts automation, while blocks are static drawing shapes.",
            "Xrefs are optimized for mobile viewers, whereas blocks require desktop seats."
          ],
          correctIdx: 0,
          why: "Xrefs enable real-time collaboration. When the architect moves a wall in the base plan, the structural engineer sees it immediately without importing files.",
          pitfall: "Prefer relative path references for Xrefs. Absolute paths will break when files are migrated to cloud servers or shared with clients."
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-draft-spaces",
          question: "What represents the golden rule for separating Model Space and Paper Space in classic 2D CAD production?",
          options: [
            "Drawing all design geometry at 1:1 scale in Model Space, and using Viewports in Paper Space to organize annotation tags and print sheet layouts.",
            "Using Model Space strictly for BIM coordination, while Paper Space is reserved for MCAD layouts.",
            "Drafting only 3D solids in Model Space, while 2D lines are drawn in Paper Space.",
            "Saving Model Space on local drives, while Paper Space layouts require cloud servers."
          ],
          correctIdx: 0,
          why: "Model Space is the infinite virtual drafting room. Paper space layouts contain standard borders and use viewports to frame and scale the geometry.",
          pitfall: "Never draw building geometry in Paper Space layouts; this detaches details from coordinates, ruining coordinates alignment."
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-draft-lisp",
          question: "What is the primary purpose of writing and loading AutoLISP (.lsp) routines in native DWG drafting applications?",
          options: [
            "Writing custom macro procedures to automate repetitive database geometry tasks and batch printing commands.",
            "Boosting the screen rendering speed of dense point clouds.",
            "Translating drawing text annotations into international language sheets.",
            "Encrypting drawing files databases to prevent unauthorized edits."
          ],
          correctIdx: 0,
          why: "LISP routines access the drawing database directly, letting draftsmen create custom utilities, automate repetitive offsets, and coordinate data exports.",
          pitfall: "Test custom LISP tools in empty drawings first; infinite loop bugs in LISP scripts will freeze sessions and cause unsaved data loss."
        }
      ]
    }
  }"""

    # 拼接新内容
    new_content = content[:start_idx] + new_db_str + content[end_idx:]
    with open(quiz_js_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully replaced QUIZ_DATABASE in quiz.js")
else:
    print("Error: start or end marker not found in quiz.js")
