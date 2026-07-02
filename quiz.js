// --- Phase P1: Duolingo-style Isolated CAD Quiz Challenge Engine ---
(function() {
  'use strict';

  // 1. 测验题库定义 (微课化重构：每个职业方向为 1 个 Unit，包含 3 节循序渐进的 Lesson)
  const QUIZ_DATABASE = {
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
,
        {
          id: 4,
          title: "Lesson 4: Advanced Coordination",
          desc: "Federated Models, Level of Information Need, & Digital Twin Handover",
          questions: [
              {
                type: "single",
                nodeId: "bim",
                slug: "federated-model-concept",
                difficulty: "intermediate",
                question: "What distinguishes a 'federated model' from a single integrated BIM file in multi-discipline projects?",
                options: [
                  "A federated model overlays separate discipline-specific files (Arch, Struct, MEP) in a viewer without merging them into one editable database.",
                  "A federated model merges all disciplines into one Revit file editable by everyone simultaneously.",
                  "A federated model is a 2D PDF overlay of scanned architectural blueprints.",
                  "Federation refers to printing multiple sets of drawings and stapling them together.",
                ],
                correctIdx: 0,
                why: "Federation keeps each discipline's model authoritative and independent. Navisworks, Solibri, or BIMcollab Zoom combine them for coordination without data loss.",
                pitfall: "Never try to combine all disciplines into one working file. This causes file corruption, worksharing conflicts, and ownership confusion."
              },
              {
                type: "single",
                nodeId: "bim",
                slug: "loin-iso-7817",
                difficulty: "advanced",
                question: "Under ISO 19650 / ISO 7817, what does 'Level of Information Need' (LOIN) replace in modern BIM specifications?",
                options: [
                  "LOIN replaces the ambiguous LOD scale by explicitly defining required geometry detail, alphanumeric data, and documentation for each deliverable purpose.",
                  "LOIN replaces the project schedule Gantt chart with a new timeline format.",
                  "LOIN eliminates the need for IFC data exchange between BIM platforms.",
                  "LOIN replaces building codes with a single international regulation.",
                ],
                correctIdx: 0,
                why: "LOIN separates geometric detail, information (data properties), and documentation needs per purpose, avoiding the one-number-fits-all confusion of LOD 100-500.",
                pitfall: "LOIN must be defined per information delivery milestone and purpose. Requesting maximum LOIN globally wastes modeling effort on elements not yet relevant."
              },
              {
                type: "single",
                nodeId: "ifc",
                slug: "ifc4-vs-ifc2x3",
                difficulty: "intermediate",
                question: "What is the primary technical improvement of IFC4 over IFC2x3 for model exchange?",
                options: [
                  "IFC4 adds parametric geometry representation (CSG trees, swept solids), improved property set definitions, and MVD (Model View Definition) certification framework.",
                  "IFC4 reduces file size by converting all geometry to JPEG images.",
                  "IFC4 removes support for MEP systems to simplify the schema.",
                  "IFC4 only works with Autodesk products while IFC2x3 is vendor-neutral.",
                ],
                correctIdx: 0,
                why: "IFC4 enables richer geometry transfer (tessellated + CSG + swept), better property inheritance, and certifiable MVDs (Reference View, Design Transfer View).",
                pitfall: "Not all BIM software fully supports IFC4 export. Verify receiver software compatibility before switching from IFC2x3 Coordination View 2.0."
              },
              {
                type: "single",
                nodeId: "clash",
                slug: "clash-tolerance-zones",
                difficulty: "advanced",
                question: "When setting up clash detection in Navisworks, why is defining tolerance zones (clearance values) per discipline pairing essential?",
                options: [
                  "Different systems require different minimum clearances (e.g., 150mm around hot pipes, 50mm for cable trays, 25mm for structural), so one global tolerance creates false positives or misses real conflicts.",
                  "Tolerance zones make the software render clashes in different colors for aesthetic reports.",
                  "Tolerance zones are required by Navisworks licensing agreements to function.",
                  "All systems require the same 0mm tolerance because any physical overlap is unacceptable.",
                ],
                correctIdx: 0,
                why: "Maintenance access, insulation thickness, and thermal expansion require discipline-specific clearances. A hot steam pipe needs more clearance than a cold water pipe.",
                pitfall: "Document your tolerance rationale in the BEP. When stakeholders question why 500 'clashes' were marked approved, the tolerance documentation justifies the decision."
              },
              {
                type: "multiple",
                nodeId: "bim",
                slug: "digital-twin-data-sources",
                difficulty: "advanced",
                question: "Which of the following data sources feed into an operational Digital Twin after construction handover? (Select all correct)",
                options: [
                  "IoT sensor streams (temperature, occupancy, energy meters)",
                  "As-built BIM model geometry and asset metadata (COBie)",
                  "Maintenance management system (CMMS) work orders and schedules",
                  "The original architect's hand-sketched concept napkin drawings",
                ],
                correctIndices: [0, 1, 2],
                why: "Digital Twins combine the as-built BIM (static geometry/data), live IoT feeds (dynamic state), and maintenance records (operational history) for facility optimization.",
                pitfall: "A Digital Twin without live data connections is just a 3D viewer. Ensure IoT infrastructure and API integrations are specified in the BEP from design phase."
              }
          ]
        },
        {
          id: 5,
          title: "Lesson 5: Quality & Compliance",
          desc: "Model Checking, BCF Workflows, & Regulatory Compliance in BIM",
          questions: [
              {
                type: "single",
                nodeId: "bim",
                slug: "solibri-rule-checking",
                difficulty: "intermediate",
                question: "What is the primary purpose of rule-based model checking tools (like Solibri Model Checker) in BIM quality assurance?",
                options: [
                  "Automatically validating BIM models against predefined rules (fire egress distances, accessibility compliance, naming conventions) without manual visual inspection.",
                  "Rendering photorealistic images of the building for client presentations.",
                  "Compressing BIM files to reduce server storage costs.",
                  "Converting Revit files to AutoCAD DWG format for 2D drafting teams.",
                ],
                correctIdx: 0,
                why: "Rule-based checkers encode building codes, employer requirements, and project standards into automated validation passes that catch errors humans would miss.",
                pitfall: "Rule sets must be configured per project. Default rulesets catch generic issues but miss project-specific requirements (client naming, room numbering, custom parameters)."
              },
              {
                type: "single",
                nodeId: "bim",
                slug: "bcf-issue-tracking",
                difficulty: "intermediate",
                question: "How does BCF (BIM Collaboration Format) improve coordination issue tracking compared to email or spreadsheet methods?",
                options: [
                  "BCF embeds viewpoint camera positions, element GUIDs, and markup annotations so issues link directly to the 3D model location, enabling precise one-click navigation to problems.",
                  "BCF compresses all project emails into a single searchable PDF document.",
                  "BCF replaces the BIM model with a simplified wireframe for faster loading.",
                  "BCF is an encrypted messaging protocol that prevents unauthorized access to project chat.",
                ],
                correctIdx: 0,
                why: "BCF topics carry spatial context (camera, selected elements, screenshots) making issues unambiguous. Any BCF-compatible tool (Solibri, Revit, BIMcollab) can open and respond.",
                pitfall: "Always set the 'assigned to' field and due date in BCF topics. Unassigned issues get lost in large projects with hundreds of open coordination items."
              },
              {
                type: "single",
                nodeId: "revit",
                slug: "workset-best-practices",
                difficulty: "intermediate",
                question: "In Revit worksharing, what is the recommended strategy for organizing worksets in a multi-user central model?",
                options: [
                  "Organize worksets by building system (Exterior Shell, Interior Partitions, MEP, Structure, Site) so teams can take ownership of logical groupings without blocking others.",
                  "Create one workset per user so each person's elements are isolated.",
                  "Put all elements in a single workset and rely on element-level checkout for control.",
                  "Create worksets by floor level only, ignoring discipline separation.",
                ],
                correctIdx: 0,
                why: "System-based worksets let teams selectively close (unload) other disciplines for performance while maintaining clear ownership boundaries for synchronized editing.",
                pitfall: "Never put Levels, Grids, or Shared Coordinates in a user-owned workset. These project-wide datums must always be available to all team members."
              },
              {
                type: "multiple",
                nodeId: "bim",
                slug: "bim-regulatory-compliance",
                difficulty: "advanced",
                question: "Which of the following building compliance checks can be automated through BIM model rule validation? (Select all correct)",
                options: [
                  "Fire egress distance and corridor width verification",
                  "Accessibility (ADA/DDA) door width and ramp gradient checks",
                  "Structural load-bearing capacity calculations (requires separate FEA)",
                  "Room area minimum requirements per building code occupancy type",
                ],
                correctIndices: [0, 1, 3],
                why: "Geometric checks (distances, widths, areas, slopes) can be automated from BIM data. Structural capacity requires separate engineering analysis software.",
                pitfall: "Model checking validates geometry and metadata, not engineering. A room that meets area requirements may still fail structurally. Always pair BIM checks with engineering sign-off."
              },
              {
                type: "single",
                nodeId: "shared-coords",
                slug: "point-cloud-registration",
                difficulty: "advanced",
                question: "When registering multiple point cloud scans into a unified coordinate system, what does 'target-based registration' provide over 'cloud-to-cloud' registration?",
                options: [
                  "Surveyed targets with known coordinates provide absolute accuracy referenced to the project coordinate system, while cloud-to-cloud only achieves relative alignment between scans.",
                  "Target-based registration is faster because it processes fewer data points.",
                  "Cloud-to-cloud registration requires special hardware that target-based does not.",
                  "Target-based registration only works indoors while cloud-to-cloud works anywhere.",
                ],
                correctIdx: 0,
                why: "Surveyed targets (checkerboards/spheres) with known XYZ coordinates tie the point cloud to the project datum. Without targets, scans align to each other but may drift from true coordinates.",
                pitfall: "Place registration targets with clear sight lines from multiple scan positions. Targets visible from only one scan position cannot contribute to registration accuracy."
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
            },
            {
              type: "single",
              nodeId: "parametrics",
              slug: "feature-tree-order",
              difficulty: "beginner",
              question: "Why does the order of features in a parametric feature tree matter for design stability?",
              options: [
                "Features are evaluated sequentially; later features depend on the geometry created by earlier ones, so reordering can break references.",
                "Feature order only affects the display color sequence in the graphics viewport.",
                "Feature trees are always recalculated in random order by the solver.",
                "Feature order is cosmetic and has no effect on model geometry."
              ],
              correctIdx: 0,
              why: "Parametric solvers evaluate features top-to-bottom. A fillet referencing an edge created by a later feature will fail if moved above it.",
              pitfall: "Plan your modeling sequence before starting. Retrofitting features into the middle of a mature tree often cascades rebuild errors."
            },
            {
              type: "single",
              nodeId: "solidworks",
              slug: "solidworks-design-table",
              difficulty: "beginner",
              question: "In SOLIDWORKS, what is the relationship between Design Tables and Configurations?",
              options: [
                "A Design Table is an Excel spreadsheet that drives multiple Configurations by mapping dimension values to configuration names in rows and columns.",
                "Design Tables replace the feature tree entirely with a flat list of coordinates.",
                "Design Tables are used exclusively for rendering material assignments.",
                "Configurations are created manually and cannot be controlled by external data."
              ],
              correctIdx: 0,
              why: "Design Tables provide a spreadsheet interface to create and manage large families of configurations (e.g., bolt sizes M4 through M20) efficiently.",
              pitfall: "Column headers in Design Tables must exactly match dimension names including the feature reference (e.g., 'D1@Boss-Extrude1'). Typos silently fail."
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
            },
            {
              type: "single",
              nodeId: "brep",
              slug: "nurbs-vs-brep",
              difficulty: "beginner",
              question: "What is the relationship between NURBS surfaces and B-Rep solid models in CAD kernels?",
              options: [
                "B-Rep uses NURBS surfaces as the geometric definition of faces, combined with topological data (edges, vertices) to define the solid boundary.",
                "NURBS and B-Rep are competing formats that cannot coexist in the same model.",
                "B-Rep stores only mesh triangles; NURBS is used exclusively for rendering.",
                "NURBS defines 2D curves only; B-Rep handles all 3D geometry independently."
              ],
              correctIdx: 0,
              why: "B-Rep topology (faces, edges, vertices) references NURBS surface equations for exact geometry. The topology defines how surfaces connect; NURBS defines their shape.",
              pitfall: "Importing STEP files with trimmed NURBS surfaces can introduce gap tolerances. Always run a geometry heal check after import."
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
            },
            {
              type: "single",
              nodeId: "assembly",
              slug: "gdt-datums",
              difficulty: "beginner",
              question: "In GD&T (Geometric Dimensioning and Tolerancing), what is the primary function of establishing Datum features?",
              options: [
                "Datums define the reference coordinate system from which all geometric tolerances and measurements are taken, ensuring consistent inspection.",
                "Datums set the rendering viewpoint for 3D model screenshots.",
                "Datums control the order of features in the parametric feature tree.",
                "Datums specify the material grade for structural steel beams."
              ],
              correctIdx: 0,
              why: "Datums establish the measurement framework. A positional tolerance of 0.1mm references specific Datum planes (A, B, C) to define where that tolerance is measured from.",
              pitfall: "Datum order matters (primary A, secondary B, tertiary C). Swapping datum priority changes the entire tolerance zone orientation."
            },
            {
              type: "single",
              nodeId: "solidworks",
              slug: "sheet-metal-k-factor",
              difficulty: "beginner",
              question: "In sheet metal design, what does the K-factor represent and why is it critical for flat pattern accuracy?",
              options: [
                "K-factor defines the position of the neutral axis within the bend thickness, determining how much material stretches during bending to calculate correct flat pattern dimensions.",
                "K-factor measures the hardness of the metal sheet material.",
                "K-factor sets the number of bends allowed per part.",
                "K-factor controls the rendering color of bent edges in the 3D view."
              ],
              correctIdx: 0,
              why: "The neutral axis shifts during bending. K-factor (0 to 1) locates it within the material thickness, directly affecting the Bend Allowance calculation for flat patterns.",
              pitfall: "K-factor varies by material, thickness, and bend radius. Using a generic K-factor for all materials produces inaccurate flat patterns and fabrication rejects."
            }
          ]
        }
,
        {
          id: 4,
          title: "Lesson 4: Manufacturing Integration",
          desc: "Sheet Metal Design, Weldments, & DFM Analysis",
          questions: [
              {
                type: "single",
                nodeId: "solidworks",
                slug: "sheet-metal-bend-relief",
                difficulty: "intermediate",
                question: "In SOLIDWORKS sheet metal design, what is the purpose of 'bend relief' cuts at the junction of bends and flat faces?",
                options: [
                  "Bend reliefs prevent material tearing and cracking at the intersection of a bend and an adjacent flat region by providing a controlled stress relief notch.",
                  "Bend reliefs increase the visual appeal of the final painted product.",
                  "Bend reliefs reduce the weight of the sheet metal part for aerospace applications.",
                  "Bend reliefs allow laser cutting machines to operate at higher speeds.",
                ],
                correctIdx: 0,
                why: "Without relief cuts, the material at bend-to-flat transitions experiences uncontrolled deformation, causing tears in ductile metals and cracks in brittle ones.",
                pitfall: "Match relief type (rectangular, obround, tear) to your fabrication shop's capabilities. Some shops cannot produce obround reliefs with basic press brakes."
              },
              {
                type: "single",
                nodeId: "solidworks",
                slug: "weldment-profiles",
                difficulty: "intermediate",
                question: "In SOLIDWORKS Weldments, what is the role of 'structural member profiles' when building welded frame structures?",
                options: [
                  "Profiles are 2D cross-sections (I-beam, C-channel, tube, angle) swept along 3D sketch paths to generate structural members with correct material properties.",
                  "Profiles are rendering textures applied to solid bodies for photorealistic visualization.",
                  "Profiles define the chemical composition of welding rod filler materials.",
                  "Profiles set the machine feed rate for CNC cutting operations.",
                ],
                correctIdx: 0,
                why: "Weldment profiles contain geometry from steel supplier catalogs (AISC, DIN, JIS). SOLIDWORKS sweeps them along skeleton paths and auto-generates trim/cope joints at intersections.",
                pitfall: "Verify profile dimensions match your actual supplier stock. Library profiles may differ from regional steel suppliers by 1-2mm, causing fit issues."
              },
              {
                type: "single",
                nodeId: "assembly",
                slug: "dfm-design-for-manufacturing",
                difficulty: "advanced",
                question: "What does SOLIDWORKS DFMXpress analyze when running a Design for Manufacturability check on a machined part?",
                options: [
                  "It checks for features that are difficult or impossible to machine: deep narrow slots, thin walls, sharp internal corners, inaccessible holes, and draft angles insufficient for molding.",
                  "It verifies that the part weighs less than the maximum shipping limit.",
                  "It checks that all dimensions are expressed in metric units rather than imperial.",
                  "It ensures the file size is small enough to email to suppliers.",
                ],
                correctIdx: 0,
                why: "DFMXpress flags manufacturing challenges early in design (e.g., a 2mm-wide 50mm-deep slot requires special EDM tooling). Catching these before shop drawings saves rework costs.",
                pitfall: "DFMXpress uses generic rules. For specialized processes (5-axis machining, Swiss-type turning), configure custom rules or consult your machinist directly."
              },
              {
                type: "multiple",
                nodeId: "mbd",
                slug: "step-ap242-capabilities",
                difficulty: "advanced",
                question: "Which of the following data types can STEP AP242 carry that STEP AP203/AP214 cannot? (Select all correct)",
                options: [
                  "3D PMI annotations (GD&T semantic data attached to geometry)",
                  "Tessellated (mesh) geometry alongside exact B-Rep",
                  "Saved viewpoints and cross-section definitions for PMI consumption",
                  "Complete project email archives and meeting minutes",
                ],
                correctIndices: [0, 1, 2],
                why: "AP242 extends STEP for MBD workflows: semantic PMI, tessellated representations for visualization, and saved views. Earlier APs carry only geometry and basic metadata.",
                pitfall: "Not all CAM/CMM software reads AP242 PMI semantically. Verify your downstream toolchain before mandating AP242 as the only delivery format."
              },
              {
                type: "single",
                nodeId: "parametrics",
                slug: "global-variables-equations",
                difficulty: "intermediate",
                question: "In SOLIDWORKS, how do Global Variables and Equations improve parametric design intent?",
                options: [
                  "They create named parameters (e.g., 'WallThickness=3mm') that drive multiple dimensions via formulas, so changing one variable updates the entire model consistently.",
                  "They translate dimension text into different languages for international drawings.",
                  "They encrypt dimension values so competitors cannot reverse-engineer the design.",
                  "They replace the feature tree with a flat list of numerical coordinates.",
                ],
                correctIdx: 0,
                why: "Global Variables create single-source-of-truth parameters. Link cavity depth, wall thickness, and draft angle to variables so changing 'Material_Thickness' updates everything.",
                pitfall: "Circular references (Variable A depends on B which depends on A) cause solver failures. Map your equation dependency graph before building complex linked dimensions."
              }
          ]
        },
        {
          id: 5,
          title: "Lesson 5: Advanced Analysis",
          desc: "FEA Best Practices, Fatigue Analysis, & Topology Optimization",
          questions: [
              {
                type: "single",
                nodeId: "solidworks",
                slug: "fea-boundary-conditions",
                difficulty: "advanced",
                question: "Why do incorrect boundary conditions in FEA produce more dangerous errors than mesh quality issues?",
                options: [
                  "Boundary conditions define the physical reality (how loads enter and supports hold the part). Wrong BCs produce plausible-looking but completely wrong stress distributions that pass visual inspection.",
                  "Boundary conditions only affect rendering colors, not stress calculations.",
                  "Mesh quality always dominates accuracy regardless of boundary conditions.",
                  "Boundary conditions are optional metadata that simulation solvers ignore.",
                ],
                correctIdx: 0,
                why: "A perfectly meshed model with wrong fixtures (e.g., fixed when it should be pinned) produces incorrect stress paths. The results look legitimate but predict failure locations wrongly.",
                pitfall: "Always validate FEA boundary conditions against physical reality. If uncertain, run sensitivity studies: how much does stress change if a fixed support becomes a frictionless one?"
              },
              {
                type: "single",
                nodeId: "solidworks",
                slug: "fatigue-sn-curve",
                difficulty: "advanced",
                question: "In mechanical fatigue analysis, what does an S-N curve (Wohler curve) represent?",
                options: [
                  "The relationship between cyclic stress amplitude (S) and the number of cycles to failure (N), used to predict component lifespan under repeated loading.",
                  "The relationship between static stress and material density for weight optimization.",
                  "The relationship between surface roughness and cutting speed in CNC machining.",
                  "The relationship between assembly bolt torque and clamp force in fastener design.",
                ],
                correctIdx: 0,
                why: "S-N curves define material endurance limits. Below the endurance limit stress, a component theoretically survives infinite cycles. Above it, the curve predicts cycle-to-failure count.",
                pitfall: "S-N data from handbooks assumes polished test specimens. Real parts have surface finish, size effects, and stress concentrations that require correction factors (Marin equation)."
              },
              {
                type: "single",
                nodeId: "brep",
                slug: "topology-optimization-goal",
                difficulty: "advanced",
                question: "What is the primary engineering goal of topology optimization in mechanical design?",
                options: [
                  "Finding the optimal material distribution within a design space that minimizes weight while satisfying stress, displacement, and frequency constraints under given loads.",
                  "Optimizing the topology (network configuration) of electrical circuit board traces.",
                  "Finding the fastest CNC toolpath by optimizing tool approach angles.",
                  "Optimizing the order of features in the parametric feature tree for rebuild speed.",
                ],
                correctIdx: 0,
                why: "Topology optimization removes material from low-stress regions while preserving load paths. The result is an organic-looking structure that's lightweight yet stiff under specified loads.",
                pitfall: "Raw topology optimization results are rarely directly manufacturable. Post-process the organic shape into producible geometry (smooth surfaces, add draft, remove undercuts) before detailing."
              },
              {
                type: "multiple",
                nodeId: "assembly",
                slug: "fea-element-types",
                difficulty: "intermediate",
                question: "Which FEA element types are commonly used for structural analysis of mechanical parts? (Select all correct)",
                options: [
                  "Tetrahedral solid elements (for complex 3D geometry)",
                  "Shell elements (for thin-walled structures like enclosures and sheet metal)",
                  "Beam elements (for structural frames and trusses)",
                  "Pixel elements (for 2D image rendering of stress plots)",
                ],
                correctIndices: [0, 1, 2],
                why: "Tet solids capture 3D stress states; shells are efficient for thin structures (plate bending); beams model frames. 'Pixel elements' do not exist in FEA.",
                pitfall: "Using solid elements on thin sheet metal (thickness < 1/10 of other dimensions) requires many through-thickness elements. Switch to shell elements for 10-100x faster solutions."
              },
              {
                type: "single",
                nodeId: "parametrics",
                slug: "design-study-optimization",
                difficulty: "intermediate",
                question: "In SOLIDWORKS Simulation, what does a 'Design Study' (parametric optimization) allow you to achieve?",
                options: [
                  "Automatically varying design dimensions within specified ranges to find the combination that minimizes weight while keeping stress below the yield limit.",
                  "Studying the visual appearance of different paint colors on the product surface.",
                  "Comparing render quality between different GPU hardware configurations.",
                  "Tracking design revision history for PDM compliance documentation.",
                ],
                correctIdx: 0,
                why: "Design Studies automate what-if analysis: define parameters (wall thickness, rib height), constraints (max stress, max deflection), and goals (minimize mass). The solver finds the optimum.",
                pitfall: "Design studies with too many variables (>10) and wide ranges require excessive computation. Start with sensitivity studies to identify the 3-4 most influential parameters first."
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
            },
            {
              type: "single",
              nodeId: "terrain",
              slug: "breaklines-tin",
              difficulty: "beginner",
              question: "Why are breaklines essential when constructing TIN surfaces for civil design?",
              options: [
                "Breaklines enforce hard edges (ridges, ditches, retaining walls) in the triangulation, preventing the TIN from smoothing across distinct grade changes.",
                "Breaklines add color coding to surface triangles for visual clarity.",
                "Breaklines compress the file size of large survey datasets.",
                "Breaklines convert TIN surfaces into flat 2D contour PDFs."
              ],
              correctIdx: 0,
              why: "Without breaklines, TIN triangulation interpolates smoothly between points, missing sharp grade transitions like curbs, ditches, and wall footings.",
              pitfall: "Ensure breaklines do not cross each other at conflicting elevations; crossing breaklines at different heights create surface artifacts and incorrect grading."
            },
            {
              type: "single",
              nodeId: "alignment",
              slug: "superelevation-design",
              difficulty: "beginner",
              question: "What does superelevation represent in highway alignment design?",
              options: [
                "The intentional banking (cross-slope tilting) of the road surface on horizontal curves to counteract centrifugal force and improve vehicle safety.",
                "The vertical height of overhead bridge structures above the road surface.",
                "The elevation difference between the road centerline and the property boundary.",
                "The maximum speed limit posted on highway curve warning signs."
              ],
              correctIdx: 0,
              why: "Superelevation tilts the road surface on curves so gravity and friction together counteract centrifugal force, reducing skidding risk at design speed.",
              pitfall: "Transition lengths between normal crown and full superelevation must be gradual. Abrupt superelevation changes cause driver discomfort and drainage pooling."
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
            },
            {
              type: "single",
              nodeId: "corridor",
              slug: "corridor-targets",
              difficulty: "beginner",
              question: "In Civil 3D corridor modeling, what is the purpose of assigning 'Targets' to subassembly parameters?",
              options: [
                "Targets dynamically link subassembly parameters (like daylight slope or lane width) to external objects such as surfaces, alignments, or offsets, enabling adaptive corridor geometry.",
                "Targets set the background color of the corridor visualization.",
                "Targets define the construction schedule timeline for the project.",
                "Targets specify which users have permission to edit the corridor model."
              ],
              correctIdx: 0,
              why: "Without targets, subassemblies use fixed values. By targeting the existing ground surface, a daylight subassembly automatically extends its slope until it intersects the terrain.",
              pitfall: "Verify target assignments at every region break. Missing targets cause subassemblies to extend infinitely or collapse to zero width."
            },
            {
              type: "single",
              nodeId: "corridor",
              slug: "pipe-network-parts-list",
              difficulty: "beginner",
              question: "In Civil 3D pipe network design, what role does the Parts List play?",
              options: [
                "The Parts List defines the catalog of available pipe sizes, materials, and structure types that can be placed in the network, enforcing design standards.",
                "The Parts List generates construction cost estimates for the entire project.",
                "The Parts List controls the display color of pipes in plan view.",
                "The Parts List sets the maximum number of pipes allowed in a single drawing."
              ],
              correctIdx: 0,
              why: "Parts Lists tie pipe networks to standard catalogs (e.g., HDPE 300mm, concrete manholes). Pipe sizes and structure dimensions come from the catalog, not manual entry.",
              pitfall: "Ensure the Parts List matches local municipal standards before design. Using a mismatched catalog means redesigning the entire network at review."
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
            },
            {
              type: "single",
              nodeId: "grading",
              slug: "grading-criteria",
              difficulty: "beginner",
              question: "In site grading design, what determines the choice between 'Grade to Surface' and 'Grade to Distance' criteria?",
              options: [
                "'Grade to Surface' extends slopes until they meet an existing terrain surface (daylight), while 'Grade to Distance' extends slopes a fixed horizontal distance regardless of terrain.",
                "'Grade to Surface' applies only to parking lots; 'Grade to Distance' applies only to highways.",
                "'Grade to Surface' uses metric units; 'Grade to Distance' uses imperial units.",
                "Both options produce identical results and are interchangeable."
              ],
              correctIdx: 0,
              why: "Grade to Surface is used when fill slopes must tie into existing ground (variable distance). Grade to Distance is used for fixed-width features like sidewalks.",
              pitfall: "When using Grade to Surface, verify the target surface extends beyond the grading footprint. Missing surface data causes grading objects to fail silently."
            },
            {
              type: "single",
              nodeId: "landxml",
              slug: "quantity-takeoff-surfaces",
              difficulty: "beginner",
              question: "How are earthwork quantity takeoffs typically calculated in civil infrastructure projects?",
              options: [
                "By comparing the existing ground surface against the proposed design surface using composite volume calculations (Average End Area or prismoidal methods).",
                "By counting the number of contour lines on a printed topographic map.",
                "By weighing soil samples collected from each grid point on the site.",
                "By measuring the perimeter boundary length of the site footprint."
              ],
              correctIdx: 0,
              why: "Volume between two TIN surfaces (existing vs. proposed) is calculated using computational geometry methods, giving accurate cut and fill quantities for each station range.",
              pitfall: "Always define a boundary for volume calculations. Without boundaries, the engine computes volumes over the entire surface extents, including areas outside the project limits."
            }
          ]
        }
,
        {
          id: 4,
          title: "Lesson 4: Earthwork & Utilities",
          desc: "Grading Optimization, Pipe Networks, & Quantity Takeoff",
          questions: [
              {
                type: "single",
                nodeId: "grading",
                slug: "grading-balance",
                difficulty: "intermediate",
                question: "What does 'cut-fill balance' mean in civil earthwork grading, and why is it a design optimization target?",
                options: [
                  "Achieving roughly equal volumes of earth excavated (cut) and earth placed (fill) minimizes hauling costs and eliminates the need to import or export soil from the site.",
                  "Cutting and filling are aesthetic landscaping terms for creating visual slopes.",
                  "Cut-fill balance means the site is perfectly flat with zero elevation change.",
                  "It refers to balancing the weight of construction equipment on both sides of the site.",
                ],
                correctIdx: 0,
                why: "Importing soil or disposing of excess is expensive. Civil designers adjust proposed grades to balance cut and fill volumes, minimizing truck haul cycles and tipping fees.",
                pitfall: "Balance volume alone isn't sufficient. Consider haul distance (mass-haul diagram) — balanced volumes with long haul distances can cost more than slight imbalance with short hauls."
              },
              {
                type: "single",
                nodeId: "corridor",
                slug: "pipe-network-design",
                difficulty: "intermediate",
                question: "In Civil 3D pipe network design, what determines the invert elevation of a gravity sewer pipe at each structure?",
                options: [
                  "Minimum cover depth requirements, pipe slope (gradient for self-cleansing velocity), and downstream connection point elevation — all ensuring gravity flow without pumping.",
                  "The aesthetic preference of the landscape architect for manhole positioning.",
                  "The color coding standard for different utility types.",
                  "The maximum pipe diameter available from the local supplier.",
                ],
                correctIdx: 0,
                why: "Gravity sewers must maintain minimum slope (e.g., 1:80 for 150mm pipes) for self-cleansing velocity while respecting minimum cover (e.g., 900mm) below finished ground.",
                pitfall: "Flat sites with long sewer runs may require deep excavation at the downstream end. Check against maximum trench depth limits and consider pump stations early in design."
              },
              {
                type: "single",
                nodeId: "terrain",
                slug: "volume-surface-comparison",
                difficulty: "intermediate",
                question: "In Civil 3D, how is earthwork volume calculated between an existing ground surface and a proposed design surface?",
                options: [
                  "Creating a 'volume surface' (TIN-to-TIN comparison) that calculates the prismoidal difference between existing and proposed triangulated surfaces across the site.",
                  "Manually counting contour lines and multiplying by a fixed depth factor.",
                  "Exporting both surfaces to Excel and subtracting cell values.",
                  "Measuring the distance between two random survey points on each surface.",
                ],
                correctIdx: 0,
                why: "Volume surfaces compare every triangle pair between the two TINs. Civil 3D computes composite volumes (average-end-area or prismoidal) and reports cut/fill per station range.",
                pitfall: "Volume accuracy depends on TIN density. Sparse survey points produce triangles that span real terrain undulations, underestimating actual earthwork volumes."
              },
              {
                type: "multiple",
                nodeId: "landxml",
                slug: "utility-design-factors",
                difficulty: "advanced",
                question: "Which factors must a civil engineer consider when designing underground utility pipe networks? (Select all correct)",
                options: [
                  "Minimum depth of cover to protect against traffic loading and frost penetration",
                  "Pipe gradient sufficient for self-cleansing velocity in gravity systems",
                  "Clearance separation distances between parallel utilities (gas, electric, water, sewer)",
                  "The RGB color values assigned to pipe layers in the CAD drawing",
                ],
                correctIndices: [0, 1, 2],
                why: "Cover depth, gradient, and utility separations are engineering requirements driven by codes (ASCE, local standards). Layer colors are drafting conventions, not design constraints.",
                pitfall: "Always check local utility clearance requirements. National codes give minimums, but utility companies often mandate greater separations in their connection agreements."
              },
              {
                type: "single",
                nodeId: "grading",
                slug: "stormwater-detention-sizing",
                difficulty: "advanced",
                question: "What is the primary engineering purpose of stormwater detention basins in civil site design?",
                options: [
                  "Temporarily storing runoff from developed impervious surfaces and releasing it at a controlled rate that does not exceed pre-development peak flow, preventing downstream flooding.",
                  "Creating decorative ponds for aesthetic landscaping in residential developments.",
                  "Providing fire-fighting water supply reservoirs for emergency services.",
                  "Collecting sediment from construction sites during the building phase only.",
                ],
                correctIdx: 0,
                why: "Development increases impervious area (roofs, roads), accelerating runoff peaks. Detention ponds attenuate the peak by temporarily storing volume and releasing it slowly through an orifice.",
                pitfall: "Size detention for multiple storm return periods (2yr, 10yr, 100yr). A pond sized only for the 10-year storm may be inadequate during extreme events, causing downstream flooding."
              }
          ]
        },
        {
          id: 5,
          title: "Lesson 5: Data Exchange & Construction",
          desc: "LandXML/IFC Export, Machine Control, & As-Built Documentation",
          questions: [
              {
                type: "single",
                nodeId: "landxml",
                slug: "landxml-export-purpose",
                difficulty: "intermediate",
                question: "What is the primary purpose of exporting Civil 3D designs to LandXML format?",
                options: [
                  "Enabling vendor-neutral exchange of civil engineering data (surfaces, alignments, parcels, pipe networks) between different software platforms and machine control systems.",
                  "Compressing 3D terrain models into smaller files for email transfer.",
                  "Converting civil designs into architectural Revit building models.",
                  "Generating photorealistic renderings of road surfaces with realistic textures.",
                ],
                correctIdx: 0,
                why: "LandXML is the civil engineering equivalent of IFC. It carries alignments, profiles, cross-sections, surfaces, and parcels in a schema that other civil software (12d, Bentley) can import.",
                pitfall: "LandXML doesn't carry all Civil 3D data. Pipe networks, pressure networks, and some corridor subtleties may be lost or simplified in the export."
              },
              {
                type: "single",
                nodeId: "corridor",
                slug: "machine-control-models",
                difficulty: "advanced",
                question: "How do GNSS-based machine control systems use Civil 3D design surfaces during construction grading?",
                options: [
                  "The design surface is loaded into the machine's onboard computer, which compares real-time blade/bucket position (via GNSS) against the target elevation, guiding the operator to cut/fill to design grades automatically.",
                  "Machine control sends email alerts to the engineer when the machine moves.",
                  "The machine automatically downloads software updates from Civil 3D during operation.",
                  "GNSS coordinates are used only for tracking fuel consumption, not guiding earthwork.",
                ],
                correctIdx: 0,
                why: "Machine control eliminates manual grade stakes. The operator sees real-time cut/fill indicators on a cabin display, achieving design grades within ±20mm without survey crew intervention.",
                pitfall: "Export machine control surfaces at sufficient TIN density. Over-simplified TINs create flat triangle planes between points, causing the machine to grade incorrect intermediate elevations."
              },
              {
                type: "single",
                nodeId: "alignment",
                slug: "horizontal-curve-design",
                difficulty: "intermediate",
                question: "In road alignment design, what is the purpose of a transition curve (clothoid/spiral) between a straight (tangent) and a circular curve?",
                options: [
                  "Providing a gradual change in curvature (from zero to the circular curve radius) so drivers experience smooth lateral acceleration transition, improving safety and comfort.",
                  "Making the road alignment look more aesthetically pleasing on plan drawings.",
                  "Reducing the total length of road to save construction material costs.",
                  "Allowing vehicles to reach higher speeds in the circular curve section.",
                ],
                correctIdx: 0,
                why: "Without transitions, drivers experience a sudden lateral force change at tangent-to-curve junctions. Spirals ramp up curvature (and superelevation) gradually, matching vehicle dynamics.",
                pitfall: "Spiral length must match superelevation development length. If the spiral is too short, the road surface cannot transition from normal crown to full banking within the available distance."
              },
              {
                type: "multiple",
                nodeId: "terrain",
                slug: "as-built-survey-methods",
                difficulty: "intermediate",
                question: "Which surveying methods are commonly used to capture as-built conditions for comparison against design models? (Select all correct)",
                options: [
                  "Total station spot measurements at critical design points (inverts, top-of-curb, edge-of-pavement)",
                  "Terrestrial LiDAR scanning for comprehensive 3D surface capture",
                  "Drone photogrammetry for rapid large-area topographic mapping",
                  "Manual tape measurement from property boundary fences",
                ],
                correctIndices: [0, 1, 2],
                why: "Total stations provide point accuracy at key locations; LiDAR gives dense 3D coverage; drones efficiently map large sites. Tape measurements from fences lack precision for engineering verification.",
                pitfall: "Choose the survey method matching required accuracy: total station for mm-precision pipe inverts, drone photogrammetry for ±30mm surface grades over large areas."
              },
              {
                type: "single",
                nodeId: "landxml",
                slug: "construction-staking",
                difficulty: "intermediate",
                question: "What information does a construction staking report from Civil 3D provide to field crews?",
                options: [
                  "Station/offset coordinates, cut/fill depths from proposed design surface, and alignment geometry data that field crews use to set grade stakes and guide earthwork operations.",
                  "Material purchase orders for concrete and asphalt suppliers.",
                  "Employee attendance records for site workers.",
                  "Weather forecasts for optimal construction scheduling.",
                ],
                correctIdx: 0,
                why: "Staking reports translate design geometry into field-usable data: station numbers, offsets from centerline, and excavation/fill depths relative to survey benchmarks.",
                pitfall: "Verify the report coordinate system matches field survey equipment settings. Datum mismatches between design coordinates and field instruments cause systematic elevation errors."
              }
          ]
        }
      ]
    },
    draft: {
      trackTitle: "2D Drafting Specialist",
      trackBadge: "📐 2D Draft",
      nodesToMaster: ["layers", "xrefs", "pgp", "annotative", "viewport", "purge", "draft-lisp", "draft-plot", "draft-std", "draft-ssm", "draft-attr", "draft-dynblk"],
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
            },
            {
              type: "single",
              nodeId: "layers",
              slug: "layer-filters-cad",
              difficulty: "beginner",
              question: "In large multi-discipline DWG files, what is the primary benefit of creating Layer Filters?",
              options: [
                "Layer Filters group layers by name pattern, discipline, or property, allowing draftsmen to quickly isolate and manage relevant layers from hundreds of available layers.",
                "Layer Filters increase the rendering speed of 3D perspective views.",
                "Layer Filters automatically translate layer names into multiple languages.",
                "Layer Filters encrypt layer data to prevent unauthorized access."
              ],
              correctIdx: 0,
              why: "In production drawings with 200+ layers, filters (e.g., show only layers starting with 'M-' for mechanical) make layer management practical.",
              pitfall: "Name-based filters only work if layer naming follows a consistent convention. Inconsistent naming renders filters useless."
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
            },
            {
              type: "single",
              nodeId: "annotative",
              slug: "dimension-styles-cad",
              difficulty: "beginner",
              question: "Why is it important to define and use named Dimension Styles rather than overriding individual dimensions?",
              options: [
                "Named Dimension Styles ensure all dimensions in a drawing share consistent formatting (text height, arrow size, tolerances), and global changes propagate by updating the style definition.",
                "Dimension Styles are required for exporting to PDF format.",
                "Individual dimension overrides are not supported in any CAD platform.",
                "Dimension Styles control the layer assignments of all geometry objects."
              ],
              correctIdx: 0,
              why: "Dimension Styles act like CSS for dimensions. Changing the style updates every dimension using it, ensuring uniformity across hundreds of sheets.",
              pitfall: "Dimension overrides (right-click > properties on individual dims) are invisible in the style manager and create inconsistencies that are hard to diagnose."
            },
            {
              type: "single",
              nodeId: "viewport",
              slug: "dwg-compare-tool",
              difficulty: "beginner",
              question: "What is the primary use case for the DWG Compare tool in production drafting workflows?",
              options: [
                "Automatically highlighting geometric differences between two revisions of the same drawing, enabling draftsmen to quickly identify what changed between versions.",
                "Comparing rendering quality between different graphics card drivers.",
                "Measuring the file size difference between compressed and uncompressed DWG files.",
                "Comparing construction cost estimates between two project proposals."
              ],
              correctIdx: 0,
              why: "DWG Compare overlays two drawing versions and color-codes additions, deletions, and modifications, making revision review systematic rather than visual guesswork.",
              pitfall: "Ensure both DWG files use the same coordinate system and units before comparing; misaligned origins will flag every entity as 'changed'."
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
            },
            {
              type: "single",
              nodeId: "purge",
              slug: "etransmit-cad",
              difficulty: "beginner",
              question: "Why should draftsmen use eTransmit (or Pack-and-Go) when delivering DWG files to external consultants?",
              options: [
                "eTransmit packages the DWG file together with all dependent files (Xrefs, fonts, plot styles, images) and converts paths to relative, ensuring the recipient can open the drawing without missing references.",
                "eTransmit encrypts the drawing database to prevent unauthorized edits.",
                "eTransmit converts DWG files to PDF format for email delivery.",
                "eTransmit removes all layers to reduce the file size for transmission."
              ],
              correctIdx: 0,
              why: "Without eTransmit, recipients often see 'missing Xref' or 'missing font' warnings because dependent files were not included or paths are absolute.",
              pitfall: "Always include plot style tables (CTB/STB) in the transmittal package. Missing plot styles cause incorrect line weights and colors when the recipient plots."
            },
            {
              type: "single",
              nodeId: "layers",
              slug: "audit-recover-cad",
              difficulty: "beginner",
              question: "When a DWG file becomes corrupted (crashes on open, missing objects), what is the recommended recovery procedure?",
              options: [
                "Use the RECOVER command to open and repair the file, then run AUDIT to fix remaining database errors, and finally PURGE to remove orphaned objects.",
                "Rename the file extension from .dwg to .bak and reopen it.",
                "Delete the file and redraw all content from memory.",
                "Convert the file to PDF and then back to DWG to clean corrupted data."
              ],
              correctIdx: 0,
              why: "RECOVER reads the raw DWG database and rebuilds corrupted structures. AUDIT fixes logical errors. Together they salvage most data from damaged files.",
              pitfall: "Always work on a copy when recovering. If RECOVER fails, try inserting the corrupted file as a block into a new drawing to extract salvageable geometry."
            }
          ]
        }
,
        {
          id: 4,
          title: "Lesson 4: Automation & Standards",
          desc: "AutoLISP Basics, Plot Styles (CTB/STB), & Drawing Standards Audit",
          questions: [
              {
                type: "single",
                nodeId: "draft-lisp",
                slug: "autolisp-defun-basics",
                difficulty: "intermediate",
                question: "In AutoLISP programming for AutoCAD, what does the (defun C:MYCOMMAND () ...) syntax create?",
                options: [
                  "A custom AutoCAD command named MYCOMMAND that users can type at the command line, executing the LISP function body when invoked.",
                  "A system variable that permanently modifies AutoCAD's source code.",
                  "A compiled executable (.exe) file that runs outside of AutoCAD.",
                  "A macro that records mouse movements for playback in video tutorials.",
                ],
                correctIdx: 0,
                why: "The C: prefix tells AutoLISP to register the function as a command-line command. Users type MYCOMMAND at the prompt and the LISP code executes within the current drawing session.",
                pitfall: "LISP commands defined with C: are session-only unless loaded via acad.lsp or a startup suite. Restarting AutoCAD without auto-loading loses custom commands."
              },
              {
                type: "single",
                nodeId: "draft-plot",
                slug: "ctb-vs-stb-plot-styles",
                difficulty: "intermediate",
                question: "What is the fundamental difference between CTB (Color-dependent) and STB (Named) plot style tables in AutoCAD?",
                options: [
                  "CTB maps plot output (lineweight, screening) based on object color numbers (1-255), while STB assigns named styles independently of color, giving more flexibility.",
                  "CTB files are newer and recommended; STB is a deprecated legacy format.",
                  "CTB controls 3D rendering materials; STB controls 2D line colors.",
                  "There is no difference; they are interchangeable synonyms.",
                ],
                correctIdx: 0,
                why: "CTB forces the old convention of 'color = lineweight' (red = 0.5mm, yellow = 0.25mm). STB decouples print appearance from display color, useful for colored model-space backgrounds.",
                pitfall: "Converting a drawing from CTB to STB mode is irreversible per drawing. Always keep a backup before running CONVERTPSTYLES, especially on shared project files."
              },
              {
                type: "single",
                nodeId: "draft-std",
                slug: "cad-standards-audit",
                difficulty: "intermediate",
                question: "What does the AutoCAD STANDARDS command (CAD Standards Checker) validate in a drawing file?",
                options: [
                  "It compares layers, dimension styles, text styles, and linetypes in the current drawing against a standards file (.dws), flagging non-compliant deviations.",
                  "It checks that the drawing file size is below a specified maximum.",
                  "It verifies that all geometry is drawn to 1:1 scale in model space.",
                  "It validates that the license subscription is current and paid.",
                ],
                correctIdx: 0,
                why: "DWS standards files encode your office layer naming, colors, linetypes, and dimension style settings. The checker reports violations (wrong layer names, non-standard text heights).",
                pitfall: "Standards checking doesn't auto-fix problems. It reports violations that must be resolved manually. Run checks regularly during drafting, not just before final submission."
              },
              {
                type: "multiple",
                nodeId: "draft-lisp",
                slug: "autolisp-common-functions",
                difficulty: "advanced",
                question: "Which of the following are valid AutoLISP functions for interacting with drawing entities? (Select all correct)",
                options: [
                  "(entget ename) — retrieves the DXF data list of an entity",
                  "(ssget) — creates a selection set of entities via user pick or filter",
                  "(command \"LINE\" pt1 pt2 \"\") — executes an AutoCAD command programmatically",
                  "(compile-shader \"vertex.glsl\") — compiles GPU rendering shaders",
                ],
                correctIndices: [0, 1, 2],
                why: "entget reads entity data, ssget builds selection sets, and (command ...) drives AutoCAD commands from LISP. GPU shader compilation is not a LISP function.",
                pitfall: "Using (command ...) inside event reactors or in-progress commands causes re-entrancy issues. Use (entmake) or (vla-*) methods instead for programmatic entity creation."
              },
              {
                type: "single",
                nodeId: "draft-std",
                slug: "template-dwt-strategy",
                difficulty: "beginner",
                question: "Why should a drafting team use a standardized DWT (drawing template) file for all new projects?",
                options: [
                  "DWT files pre-configure layer standards, dimension styles, text styles, title blocks, page setups, and units — ensuring every new drawing starts compliant without manual setup.",
                  "DWT files are required by AutoCAD's license agreement for commercial use.",
                  "DWT files compress drawings to reduce file size by 50%.",
                  "DWT files prevent users from creating new layers or modifying existing objects.",
                ],
                correctIdx: 0,
                why: "Templates eliminate setup repetition and enforce standards from the first keystroke. Without templates, each drafter creates different layer names and dimension styles.",
                pitfall: "Version-control your DWT files. When standards change (new layer naming, updated title block), distribute the updated template AND communicate changes to all team members."
              }
          ]
        },
        {
          id: 5,
          title: "Lesson 5: Advanced Documentation",
          desc: "Sheet Set Manager, Fields & Attributes, & Dynamic Block Parameters",
          questions: [
              {
                type: "single",
                nodeId: "draft-ssm",
                slug: "sheet-set-manager",
                difficulty: "intermediate",
                question: "What problem does Sheet Set Manager (SSM) solve for multi-drawing construction document sets in AutoCAD?",
                options: [
                  "SSM organizes drawings across multiple DWG files into a single project tree, automating sheet numbering, title block fields, and batch publishing without manually opening each file.",
                  "SSM merges all project drawings into one large DWG file for simpler management.",
                  "SSM is a cloud storage service for backing up AutoCAD files.",
                  "SSM converts all drawings to PDF format and deletes the original DWG files.",
                ],
                correctIdx: 0,
                why: "SSM lets you manage 200+ sheets across dozens of DWG files as one logical set. Sheet numbers, revision dates, and drawing titles auto-populate from SSM properties into title block fields.",
                pitfall: "SSM requires consistent layout naming and title block field definitions across all project DWG files. Retrofitting SSM onto legacy drawings without standardized title blocks fails."
              },
              {
                type: "single",
                nodeId: "draft-attr",
                slug: "block-attributes-extraction",
                difficulty: "intermediate",
                question: "How do block attributes enable automated data extraction (schedules, BOMs) from AutoCAD drawings?",
                options: [
                  "Attributes store structured text data (part number, material, cost) inside block references. DATAEXTRACTION command queries all instances and exports tabulated data to Excel or AutoCAD tables.",
                  "Attributes are visual decorations that cannot be queried or exported.",
                  "Attributes only work in 3D models, not 2D drawings.",
                  "DATAEXTRACTION reads drawing file metadata but cannot access block attribute values.",
                ],
                correctIdx: 0,
                why: "Each block instance carries attribute values (like a mini database record). DATAEXTRACTION scans all blocks matching a filter and produces a schedule without manual counting.",
                pitfall: "Define attribute tags consistently (PART_NO not PartNo, Part-No, etc.). Inconsistent naming prevents accurate filtering and extraction across drawing sets."
              },
              {
                type: "single",
                nodeId: "draft-dynblk",
                slug: "dynamic-block-visibility-states",
                difficulty: "advanced",
                question: "In AutoCAD dynamic blocks, what do 'Visibility States' allow a single block definition to achieve?",
                options: [
                  "Multiple visual representations (e.g., plan view, side view, simplified view) within one block, switchable via a properties dropdown without needing separate block definitions.",
                  "Animated transitions between block states for presentation purposes.",
                  "Automatic color changes based on the time of day in the drawing.",
                  "Password-protecting certain block geometries from unauthorized editing.",
                ],
                correctIdx: 0,
                why: "Visibility states pack multiple representations into one intelligent block. A door block could show: plan/elevation/3D/fire-rated variants, all switchable from the Properties palette.",
                pitfall: "Too many visibility states in one block bloat file size and confuse users. Limit to 5-8 meaningful states. For fundamentally different objects, use separate block definitions."
              },
              {
                type: "multiple",
                nodeId: "draft-dynblk",
                slug: "dynamic-block-parameters",
                difficulty: "advanced",
                question: "Which parameter types can be added to AutoCAD dynamic blocks to create intelligent, adjustable geometry? (Select all correct)",
                options: [
                  "Linear parameter (stretches geometry along an axis)",
                  "Rotation parameter (rotates geometry around a base point)",
                  "Lookup parameter (maps a table of preset values to other parameters)",
                  "Weather parameter (changes block appearance based on outdoor temperature)",
                ],
                correctIndices: [0, 1, 2],
                why: "Linear, Rotation, Lookup (plus Point, Polar, Flip, Alignment, Visibility) are valid dynamic block parameters. Weather integration doesn't exist in AutoCAD blocks.",
                pitfall: "Always pair parameters with actions (Stretch, Move, Rotate, Scale). A parameter without an associated action does nothing when the user grips the block."
              },
              {
                type: "single",
                nodeId: "draft-std",
                slug: "field-codes-autocad",
                difficulty: "intermediate",
                question: "What are 'Fields' in AutoCAD text and how do they differ from static text?",
                options: [
                  "Fields are dynamic text placeholders that auto-update their displayed value based on drawing properties (filename, date, sheet number, object properties, plot scale) without manual editing.",
                  "Fields are encrypted text strings that cannot be read by other CAD software.",
                  "Fields are fixed labels that must be manually updated each time a drawing is revised.",
                  "Fields only work inside table cells and cannot be used in title blocks or annotations.",
                ],
                correctIdx: 0,
                why: "Fields pull live data from the drawing database: %<\AcVar Filename>% shows the current filename, %<\AcVar Date>% shows today's date. They update on save, plot, or regeneration.",
                pitfall: "Fields display '####' or stale values if the background update setting (FIELDEVAL) is disabled. Ensure FIELDEVAL includes 'on plot' for title blocks to show current data when printing."
              }
          ]
        }
      ]
    },

    sim: {
      trackTitle: "Simulation / CAE Analyst",
      trackBadge: "🔬 CAE",
      nodesToMaster: ["fea-basics", "meshing", "cfd", "thermal", "optimization"],
      lessons: [
        {
          id: 1,
          title: "Lesson 1: FEA Fundamentals",
          desc: "Finite Element Method, Element Types, & Boundary Conditions",
          questions: [
            {
              type: "single",
              nodeId: "fea-basics",
              slug: "fea-discretization",
              difficulty: "beginner",
              question: "What is the fundamental principle behind the Finite Element Method (FEM)?",
              options: [
                "Dividing a continuous geometry into discrete small elements, solving equilibrium equations at each element, and assembling results to approximate the global behavior.",
                "Drawing stress contour lines manually on printed cross-section drawings.",
                "Measuring physical prototype strain using only analog dial indicators.",
                "Replacing all CAD geometry with simplified 2D wireframe sketches."
              ],
              correctIdx: 0,
              why: "FEM discretizes continuous domains into elements with nodes. Each element has simple shape functions; assembling all element stiffness matrices yields the global system of equations.",
              pitfall: "FEA results are approximations. Always validate with hand calculations or experimental data for critical load cases before using results for design decisions."
            },
            {
              type: "single",
              nodeId: "fea-basics",
              slug: "element-types-comparison",
              difficulty: "beginner",
              question: "When should a structural analyst choose solid (3D) elements over shell (2D) elements in FEA?",
              options: [
                "When the component has significant through-thickness stress variation or complex 3D geometry that cannot be represented as a surface with uniform thickness.",
                "Solid elements should always be used because they are more accurate in every situation.",
                "Shell elements are obsolete and no longer supported in modern FEA software.",
                "Solid elements are used for thermal analysis only; shell elements handle all structural loads."
              ],
              correctIdx: 0,
              why: "Shell elements assume plane-stress through thickness and are efficient for thin-walled structures. Solid elements capture 3D stress states needed for thick or complex geometries.",
              pitfall: "Using solid elements on thin-walled structures requires many elements through the thickness, dramatically increasing solve time without improving accuracy over shells."
            },
            {
              type: "single",
              nodeId: "fea-basics",
              slug: "boundary-conditions-fea",
              difficulty: "beginner",
              question: "Why is correct boundary condition (BC) definition the most critical step in setting up an FEA simulation?",
              options: [
                "Boundary conditions define how the model is supported and loaded; incorrect BCs produce mathematically valid but physically meaningless results.",
                "Boundary conditions only affect the visual display of the deformed shape plot.",
                "Boundary conditions are automatically determined by the FEA solver from the geometry.",
                "Boundary conditions set the mesh density and element type selection."
              ],
              correctIdx: 0,
              why: "The solver faithfully computes results for whatever BCs you define. An over-constrained model shows artificially low stress; an under-constrained model has rigid-body motion errors.",
              pitfall: "Avoid fully fixing all degrees of freedom at supports unless the real structure is truly rigid there. Over-constraining introduces unrealistic stress concentrations."
            },
            {
              type: "single",
              nodeId: "meshing",
              slug: "mesh-quality-metrics",
              difficulty: "beginner",
              question: "What mesh quality metric indicates that an element is too distorted for reliable FEA results?",
              options: [
                "High aspect ratio (long, thin elements), high skewness (deviation from ideal shape), or Jacobian values below acceptable thresholds indicate poor element quality.",
                "Elements with more than 4 nodes are always considered poor quality.",
                "Mesh quality is measured only by the total number of elements in the model.",
                "Dark-colored elements in the visualization indicate poor mesh quality."
              ],
              correctIdx: 0,
              why: "Distorted elements have poor shape functions that introduce numerical errors. Aspect ratio, skewness, and Jacobian ratios quantify how far an element deviates from its ideal shape.",
              pitfall: "Check mesh quality metrics before solving. A single highly distorted element near a stress concentration can corrupt results in the entire surrounding region."
            },
            {
              type: "multiple",
              nodeId: "fea-basics",
              slug: "fea-analysis-types",
              difficulty: "beginner",
              question: "Which of the following are standard analysis types available in structural FEA software? (Select all correct)",
              options: [
                "Linear static analysis (small deformation, linear material)",
                "Modal analysis (natural frequency and mode shapes)",
                "Nonlinear analysis (large deformation, contact, plasticity)",
                "Autonomous vehicle navigation path planning"
              ],
              correctIndices: [0, 1, 2],
              why: "Linear static, modal, and nonlinear analyses are core structural FEA capabilities. Vehicle navigation is a robotics/AI problem, not structural simulation.",
              pitfall: "Start with linear static analysis. Only add nonlinear effects (contact, large deformation, plasticity) when the linear results indicate they are necessary."
            }
          ]
        },
        {
          id: 2,
          title: "Lesson 2: CFD & Thermal",
          desc: "Computational Fluid Dynamics, Heat Transfer, & Turbulence Models",
          questions: [
            {
              type: "single",
              nodeId: "cfd",
              slug: "cfd-reynolds-number",
              difficulty: "beginner",
              question: "Why is the Reynolds number the first parameter a CFD analyst should calculate before setting up a simulation?",
              options: [
                "Reynolds number determines whether the flow is laminar or turbulent, which dictates the choice of turbulence model, mesh resolution requirements, and solver settings.",
                "Reynolds number sets the color scale of velocity contour plots.",
                "Reynolds number is only relevant for incompressible water simulations.",
                "Reynolds number determines the maximum number of mesh cells allowed in the model."
              ],
              correctIdx: 0,
              why: "Re = (density x velocity x length) / viscosity. Low Re means laminar flow (no turbulence model needed); high Re means turbulent flow requiring appropriate modeling.",
              pitfall: "Using a laminar solver for high-Reynolds-number flows produces completely wrong results. Always estimate Re before choosing solver settings."
            },
            {
              type: "single",
              nodeId: "cfd",
              slug: "turbulence-models-selection",
              difficulty: "beginner",
              question: "When would an engineer select the k-epsilon turbulence model over the k-omega SST model in CFD?",
              options: [
                "k-epsilon performs well for fully turbulent free-stream flows away from walls, while k-omega SST is preferred when accurate near-wall boundary layer resolution is critical.",
                "k-epsilon is newer and always more accurate than k-omega SST.",
                "k-omega SST can only be used for gas flows; k-epsilon handles all fluid types.",
                "Both models produce identical results regardless of the flow conditions."
              ],
              correctIdx: 0,
              why: "k-omega SST blends k-omega (accurate near walls) with k-epsilon (stable in free stream), making it the default choice for most engineering applications.",
              pitfall: "Verify y+ values at walls match the turbulence model requirements. k-omega SST with wall functions needs y+ around 30-300; resolving the boundary layer needs y+ < 1."
            },
            {
              type: "single",
              nodeId: "thermal",
              slug: "conjugate-heat-transfer",
              difficulty: "beginner",
              question: "What defines a Conjugate Heat Transfer (CHT) simulation?",
              options: [
                "Simultaneously solving heat conduction through solid domains and convective heat transfer in adjacent fluid domains, with thermal coupling at the solid-fluid interface.",
                "Running separate thermal and flow simulations independently without data exchange.",
                "Simulating heat transfer only through radiation between two distant surfaces.",
                "Calculating the thermal expansion of a solid without considering fluid cooling effects."
              ],
              correctIdx: 0,
              why: "CHT couples the solid conduction equation with the fluid energy equation at shared interfaces, capturing the interaction between cooling fluid flow and component heating.",
              pitfall: "Ensure the mesh at the solid-fluid interface is conformal (matching nodes). Non-conformal interfaces require interpolation that can introduce thermal energy imbalance."
            },
            {
              type: "single",
              nodeId: "thermal",
              slug: "transient-vs-steady-state",
              difficulty: "beginner",
              question: "When should a thermal simulation be run as transient rather than steady-state?",
              options: [
                "When the temperature distribution changes over time (e.g., startup, shutdown, cyclic loading), and the time-dependent thermal response is needed for design decisions.",
                "Transient simulations should always be used because they are more accurate.",
                "Transient analysis is only available for 2D models; 3D models must use steady-state.",
                "Steady-state analysis cannot model any form of heat transfer."
              ],
              correctIdx: 0,
              why: "Steady-state finds the equilibrium temperature distribution. Transient analysis tracks how temperature evolves over time, which matters for thermal shock, cycling, and startup.",
              pitfall: "Transient simulations require appropriate time step sizes. Too large a time step misses rapid temperature changes; too small wastes computation time."
            },
            {
              type: "multiple",
              nodeId: "cfd",
              slug: "cfd-post-processing-checks",
              difficulty: "beginner",
              question: "Which post-processing checks should a CFD analyst perform to verify simulation validity? (Select all correct)",
              options: [
                "Monitor residual convergence to ensure equations are solved to acceptable tolerance",
                "Check mass and energy conservation across inlet and outlet boundaries",
                "Perform mesh independence study by comparing results at different mesh densities",
                "Verify the simulation by checking if velocity contours look aesthetically pleasing"
              ],
              correctIndices: [0, 1, 2],
              why: "Residual convergence, conservation checks, and mesh independence are standard validation practices. Visual aesthetics alone do not indicate numerical accuracy.",
              pitfall: "Converged residuals alone do not guarantee accurate results. Always check physical conservation balances and compare against experimental data when available."
            }
          ]
        },
        {
          id: 3,
          title: "Lesson 3: Optimization & Best Practices",
          desc: "Topology Optimization, Design Studies, & Solver Performance",
          questions: [
            {
              type: "single",
              nodeId: "optimization",
              slug: "topology-optimization",
              difficulty: "beginner",
              question: "What is the primary engineering purpose of topology optimization in structural design?",
              options: [
                "Determining the optimal material distribution within a design space to minimize weight while satisfying stress, displacement, and manufacturing constraints.",
                "Automatically generating photorealistic renderings of structural components.",
                "Sorting the feature tree operations into the most efficient rebuild order.",
                "Converting mesh elements into NURBS surfaces for CAD export."
              ],
              correctIdx: 0,
              why: "Topology optimization iteratively removes material from low-stress regions, producing organic-looking structures that are structurally efficient for the defined load cases.",
              pitfall: "Topology optimization results require interpretation and redesign. The raw optimized shape is not directly manufacturable without smoothing and feature reconstruction."
            },
            {
              type: "single",
              nodeId: "optimization",
              slug: "design-of-experiments",
              difficulty: "beginner",
              question: "In simulation-driven design, what is the purpose of a Design of Experiments (DOE) study?",
              options: [
                "Systematically varying design parameters (dimensions, materials, loads) across a structured matrix to understand how each parameter affects performance metrics.",
                "Randomly changing all parameters simultaneously to find the single best design.",
                "Running the same simulation repeatedly with identical inputs to check reproducibility.",
                "Documenting the experimental test plan for physical prototype testing only."
              ],
              correctIdx: 0,
              why: "DOE uses structured parameter combinations (Latin Hypercube, Full Factorial) to efficiently map the design space, revealing parameter sensitivity and interaction effects.",
              pitfall: "Full factorial DOE becomes computationally prohibitive with many parameters. Use Latin Hypercube or response surface methods for 5+ parameter studies."
            },
            {
              type: "single",
              nodeId: "meshing",
              slug: "adaptive-mesh-refinement",
              difficulty: "beginner",
              question: "What is adaptive mesh refinement (AMR) and when should it be used?",
              options: [
                "AMR automatically refines the mesh in regions of high solution gradient (stress concentration, flow separation) during or between solver iterations, improving accuracy where it matters most.",
                "AMR uniformly doubles the mesh density across the entire model after each solve.",
                "AMR reduces mesh density everywhere to speed up computation time.",
                "AMR only applies to 2D simulations and cannot be used in 3D models."
              ],
              correctIdx: 0,
              why: "AMR concentrates computational resources where the solution changes rapidly, achieving higher accuracy in critical regions without the cost of globally fine meshes.",
              pitfall: "Set AMR convergence criteria carefully. Without limits, AMR can refine indefinitely at singularities (sharp corners), consuming all available memory."
            },
            {
              type: "single",
              nodeId: "optimization",
              slug: "fatigue-analysis-sn",
              difficulty: "beginner",
              question: "In mechanical fatigue analysis, what does an S-N curve represent?",
              options: [
                "The relationship between applied stress amplitude (S) and the number of cycles to failure (N) for a given material, used to predict component fatigue life.",
                "The relationship between simulation speed and the number of mesh nodes.",
                "The signal-to-noise ratio in vibration measurement instruments.",
                "The surface roughness (S) versus nominal thickness (N) for sheet metal parts."
              ],
              correctIdx: 0,
              why: "S-N curves (Wohler curves) are the foundation of fatigue design. They define how many load cycles a material can withstand at each stress level before cracking.",
              pitfall: "S-N curves from material databases assume polished specimens. Apply surface finish, size, and reliability correction factors for real-world components."
            },
            {
              type: "multiple",
              nodeId: "meshing",
              slug: "solver-performance-tips",
              difficulty: "beginner",
              question: "Which strategies effectively reduce FEA solver computation time without significantly sacrificing accuracy? (Select all correct)",
              options: [
                "Using symmetry boundary conditions to model only half or quarter of symmetric geometries",
                "Applying submodeling to refine only the critical region using boundary conditions from a coarser global model",
                "Simplifying geometry by removing small fillets, holes, and features far from the region of interest",
                "Reducing the number of load cases by ignoring the most critical loading scenario"
              ],
              correctIndices: [0, 1, 2],
              why: "Symmetry, submodeling, and geometry simplification are standard efficiency techniques. Ignoring critical load cases compromises the entire analysis purpose.",
              pitfall: "When using symmetry, verify the loading and boundary conditions are truly symmetric. Asymmetric loads on a symmetric geometry still require a full model."
            }
          ]
        }
,
        {
          id: 4,
          title: "Lesson 4: CFD & Thermal",
          desc: "Turbulence Modeling, Conjugate Heat Transfer, & Mesh Independence",
          questions: [
              {
                type: "single",
                nodeId: "sim-cfd",
                slug: "rans-turbulence-models",
                difficulty: "intermediate",
                question: "In CFD (Computational Fluid Dynamics), what do RANS turbulence models (k-epsilon, k-omega SST) approximate?",
                options: [
                  "They solve time-averaged Navier-Stokes equations with modeled turbulent viscosity, predicting mean flow behavior without resolving individual turbulent eddies.",
                  "They calculate exact positions of every fluid molecule for perfect accuracy.",
                  "They only work for incompressible laminar flow in straight pipes.",
                  "They replace the need for any computational mesh or spatial discretization.",
                ],
                correctIdx: 0,
                why: "RANS models are practical engineering tools: they decompose velocity into mean + fluctuation, model the fluctuation effects via turbulent viscosity, and solve for the mean flow field.",
                pitfall: "k-epsilon struggles with separation, adverse pressure gradients, and swirl. Use k-omega SST for external aerodynamics and flows with boundary layer separation."
              },
              {
                type: "single",
                nodeId: "sim-thermal",
                slug: "conjugate-heat-transfer",
                difficulty: "advanced",
                question: "What distinguishes conjugate heat transfer (CHT) analysis from a simple convection boundary condition?",
                options: [
                  "CHT simultaneously solves fluid flow AND solid conduction in one coupled simulation, computing heat flux across solid-fluid interfaces without prescribing a convection coefficient.",
                  "CHT only models radiation heat transfer between surfaces.",
                  "CHT is a simplified 1D analytical calculation, not a numerical simulation.",
                  "CHT replaces the energy equation with a constant temperature assumption.",
                ],
                correctIdx: 0,
                why: "In CHT, the solver calculates local heat transfer coefficients from the resolved flow field. This captures effects like recirculation zones with poor cooling that a prescribed 'h' would miss.",
                pitfall: "CHT requires fine boundary layer mesh on solid-fluid interfaces (y+ ≈ 1 for accurate heat flux). Coarse meshes at walls produce wrong temperature predictions."
              },
              {
                type: "single",
                nodeId: "sim-mesh",
                slug: "yplus-wall-treatment",
                difficulty: "advanced",
                question: "In CFD wall-bounded flows, what does the y+ (y-plus) value of the first cell represent?",
                options: [
                  "A non-dimensional wall distance indicating whether the first mesh cell resolves the viscous sublayer (y+ ≈ 1) or relies on wall functions (y+ = 30-300) for near-wall turbulence modeling.",
                  "The total number of mesh cells in the simulation domain.",
                  "The percentage of convergence achieved by the solver.",
                  "The physical height in millimeters of the tallest cell in the mesh.",
                ],
                correctIdx: 0,
                why: "y+ determines wall treatment validity. Low-Re models need y+ ≈ 1 (resolving viscous sublayer). Standard wall functions need y+ = 30-300. Between 5-30 is a 'buffer zone' where neither is accurate.",
                pitfall: "Check y+ AFTER running the simulation (it depends on local flow conditions). If y+ falls in the buffer zone (5-30), refine or coarsen the boundary layer mesh accordingly."
              },
              {
                type: "multiple",
                nodeId: "sim-cfd",
                slug: "cfd-convergence-indicators",
                difficulty: "intermediate",
                question: "Which indicators confirm that a steady-state CFD simulation has converged to a reliable solution? (Select all correct)",
                options: [
                  "Residuals (continuity, momentum, energy) have dropped by 3-4+ orders of magnitude and stabilized",
                  "Monitored quantities (drag force, outlet temperature, pressure drop) have reached steady values",
                  "Mass/energy imbalance between inlet and outlet is below 0.1%",
                  "The simulation has run for exactly 1000 iterations regardless of residual behavior",
                ],
                correctIndices: [0, 1, 2],
                why: "Convergence requires all three: low residuals, stable monitors, and conservation balance. A fixed iteration count guarantees nothing about solution quality.",
                pitfall: "Some flows are inherently unsteady (vortex shedding, separation bubbles). Forcing steady-state convergence on unsteady physics produces oscillating residuals and wrong predictions."
              },
              {
                type: "single",
                nodeId: "sim-mesh",
                slug: "mesh-independence-study",
                difficulty: "intermediate",
                question: "What is the purpose of a mesh independence (grid convergence) study in CFD/FEA?",
                options: [
                  "Systematically refining the mesh until key output quantities (stress, pressure drop, heat transfer) change by less than a threshold (typically 1-2%), proving results are not artifacts of mesh resolution.",
                  "Testing whether the simulation runs on different computer hardware configurations.",
                  "Verifying that the mesh file format is compatible with multiple CFD software packages.",
                  "Checking that the mesh generation software license is valid.",
                ],
                correctIdx: 0,
                why: "Without mesh independence, results may be mesh-dependent — refining could change the answer significantly. Three mesh levels (coarse, medium, fine) with consistent results confirm grid independence.",
                pitfall: "Only compare results at identical monitoring locations. Global averages can appear converged while local values (peak stress, recirculation zone size) still change with refinement."
              }
          ]
        },
        {
          id: 5,
          title: "Lesson 5: Structural Dynamics & Optimization",
          desc: "Modal Analysis, Explicit Dynamics, & Design Optimization Loops",
          questions: [
              {
                type: "single",
                nodeId: "sim-modal",
                slug: "modal-analysis-purpose",
                difficulty: "intermediate",
                question: "What does modal analysis determine about a mechanical structure, and why is it critical for vibration design?",
                options: [
                  "Modal analysis finds the natural frequencies and mode shapes of a structure, identifying resonance risks where operating frequencies could excite destructive vibrations.",
                  "Modal analysis calculates the maximum static load a structure can bear before yielding.",
                  "Modal analysis measures the acoustic noise level produced by the structure during operation.",
                  "Modal analysis determines the thermal expansion coefficient of materials under heating.",
                ],
                correctIdx: 0,
                why: "Every structure has natural frequencies. If an excitation source (motor RPM, wind gust frequency) matches a natural frequency, resonance amplifies vibration, causing fatigue or failure.",
                pitfall: "Always check the first 10-20 modes. Higher modes with less mass participation can still be excited by harmonic content in broadband excitation sources."
              },
              {
                type: "single",
                nodeId: "sim-explicit",
                slug: "explicit-vs-implicit-dynamics",
                difficulty: "advanced",
                question: "When should an engineer use explicit dynamics (LS-DYNA, Abaqus Explicit) instead of implicit static/dynamic analysis?",
                options: [
                  "For very short-duration high-speed events (crash, impact, blast, metal forming) where time steps are microseconds and large deformations/contact dominate the physics.",
                  "For steady-state thermal analysis of building HVAC systems.",
                  "For calculating bolt pretension in a flanged connection under static pressure.",
                  "For modal analysis of a bridge deck under pedestrian walking loads.",
                ],
                correctIdx: 0,
                why: "Explicit solvers advance time using tiny stable steps without solving large equation systems. This excels at crash (milliseconds), forming (contact changes every step), and blast (pressure waves).",
                pitfall: "Explicit time step is limited by the smallest element (Courant condition). One tiny element in a large model forces globally small time steps, dramatically increasing solve time."
              },
              {
                type: "single",
                nodeId: "sim-opt",
                slug: "parametric-vs-topology-opt",
                difficulty: "intermediate",
                question: "What is the key difference between parametric optimization and topology optimization in structural design?",
                options: [
                  "Parametric optimization varies dimensions of a fixed shape (wall thickness, rib height), while topology optimization freely redistributes material, potentially creating entirely new shapes with holes and branches.",
                  "Parametric optimization uses FEA while topology optimization uses hand calculations.",
                  "Topology optimization only works for plastic materials, not metals.",
                  "They are identical methods with different names used by different software vendors.",
                ],
                correctIdx: 0,
                why: "Parametric optimization searches within a design space defined by parameters. Topology optimization has no preconceived shape — it discovers the optimal load paths from scratch.",
                pitfall: "Topology results often require manufacturing interpretation. An optimal topology may include undercuts, enclosed voids, or thin bridges that are impractical for CNC machining or casting."
              },
              {
                type: "multiple",
                nodeId: "sim-modal",
                slug: "vibration-mitigation-strategies",
                difficulty: "advanced",
                question: "Which engineering strategies can shift a structure's natural frequencies away from operating excitation frequencies? (Select all correct)",
                options: [
                  "Adding stiffeners or ribs to increase structural stiffness (raises natural frequency)",
                  "Adding mass dampers or tuned mass absorbers (shifts/splits modes)",
                  "Changing material to one with higher stiffness-to-weight ratio (E/rho)",
                  "Painting the structure a different color to change its acoustic properties",
                ],
                correctIndices: [0, 1, 2],
                why: "Natural frequency depends on stiffness and mass (f ∝ √(k/m)). Stiffening raises frequency; adding dampers splits modes; material E/rho ratio directly affects wave speed.",
                pitfall: "Simply adding mass lowers frequency — but may move it toward a different excitation source. Always map ALL excitation frequencies before deciding which direction to shift modes."
              },
              {
                type: "single",
                nodeId: "sim-opt",
                slug: "design-of-experiments-doe",
                difficulty: "intermediate",
                question: "In simulation-driven design, what does Design of Experiments (DOE) methodology provide?",
                options: [
                  "A structured sampling strategy (Latin Hypercube, full factorial) that efficiently explores the design space, identifying which parameters most influence performance with minimum simulation runs.",
                  "A laboratory testing protocol for physical prototype destructive testing.",
                  "A project management timeline for scheduling engineering resources.",
                  "An accounting spreadsheet for tracking simulation software license costs.",
                ],
                correctIdx: 0,
                why: "DOE minimizes the number of expensive simulations needed to understand parameter sensitivity. A 5-parameter study with 3 levels per parameter needs 243 runs with full factorial but only ~25 with Latin Hypercube.",
                pitfall: "DOE results are only valid within the sampled range. Extrapolating surrogate models beyond the DOE bounds can predict physically impossible (negative thickness) or catastrophically wrong results."
              }
          ]
        }
      ]
    },

    viz: {
      trackTitle: "3D Visualization Specialist",
      trackBadge: "🎨 Viz",
      nodesToMaster: ["materials", "lighting", "camera", "rendering", "post-process"],
      lessons: [
        {
          id: 1,
          title: "Lesson 1: Materials & Textures",
          desc: "PBR Materials, UV Mapping, & Texture Resolution",
          questions: [
            {
              type: "single",
              nodeId: "materials",
              slug: "pbr-workflow",
              difficulty: "beginner",
              question: "What is the core principle of Physically Based Rendering (PBR) materials?",
              options: [
                "PBR materials use physics-based equations to calculate light interaction (reflection, refraction, absorption), producing consistent and realistic results under any lighting condition.",
                "PBR materials require hand-painting every shadow and highlight onto texture maps.",
                "PBR only works with exterior daylight scenes and cannot render interior spaces.",
                "PBR replaces all geometry with photographic images mapped onto flat planes."
              ],
              correctIdx: 0,
              why: "PBR separates material properties (base color, metalness, roughness) from lighting, ensuring materials look correct whether lit by sun, studio lights, or HDR environments.",
              pitfall: "Avoid setting metalness to values between 0 and 1 for real materials. In PBR, materials are either metallic (1.0) or dielectric (0.0); in-between values are physically incorrect."
            },
            {
              type: "single",
              nodeId: "materials",
              slug: "texture-resolution-selection",
              difficulty: "beginner",
              question: "How should a visualization artist determine the appropriate texture resolution for a material?",
              options: [
                "Based on the texel density: the texture resolution should provide sufficient pixels per meter of surface area at the expected camera distance, typically 10-20 pixels per centimeter for close-up objects.",
                "Always use the maximum resolution (8K) for every material to ensure quality.",
                "Texture resolution should match the monitor resolution regardless of object distance.",
                "Lower resolution textures are always preferred because they render faster."
              ],
              correctIdx: 0,
              why: "Texel density matches pixel coverage to viewing conditions. A distant building facade needs lower resolution than a close-up countertop material.",
              pitfall: "Over-resolution textures waste VRAM and slow rendering without visible quality improvement. Match texture resolution to the largest on-screen pixel coverage."
            },
            {
              type: "single",
              nodeId: "materials",
              slug: "normal-vs-displacement",
              difficulty: "beginner",
              question: "What is the practical difference between Normal maps and Displacement maps in architectural visualization?",
              options: [
                "Normal maps simulate surface detail by perturbing lighting calculations without changing geometry; Displacement maps physically modify the mesh surface, creating real geometric depth visible in silhouettes.",
                "Normal maps and Displacement maps produce identical results in all rendering engines.",
                "Normal maps are used for metallic materials; Displacement maps are used for wood only.",
                "Displacement maps can only be applied in 2D rendering workflows."
              ],
              correctIdx: 0,
              why: "Normal maps are fast but fake depth (silhouettes remain flat). Displacement maps create real geometry, producing correct shadows, occlusion, and parallax at the cost of higher polygon count.",
              pitfall: "Displacement maps require sufficient mesh subdivision to capture the detail. Without enough geometry, displacement looks blocky and stepped."
            },
            {
              type: "single",
              nodeId: "materials",
              slug: "ior-glass-materials",
              difficulty: "beginner",
              question: "Why is the Index of Refraction (IOR) setting critical when creating glass and water materials?",
              options: [
                "IOR determines how much light bends when passing through the material, directly affecting transparency, reflection intensity, and the visual appearance of thick glass, water pools, and gemstones.",
                "IOR only affects the color tint of transparent materials.",
                "IOR is a rendering speed optimization parameter with no visual effect.",
                "IOR must always be set to 1.0 for all transparent materials."
              ],
              correctIdx: 0,
              why: "Glass IOR is 1.52, water is 1.33, diamond is 2.42. Incorrect IOR makes glass look like plastic or water look like air. PBR renderers calculate Fresnel reflections from IOR.",
              pitfall: "For architectural glass, also model the glass thickness. Single-surface glass without thickness misses the refraction offset visible in real thick glazing panels."
            },
            {
              type: "multiple",
              nodeId: "materials",
              slug: "pbr-texture-maps",
              difficulty: "beginner",
              question: "Which texture maps are part of a standard PBR metallic-roughness material workflow? (Select all correct)",
              options: [
                "Base Color (Albedo) map defining surface color without lighting information",
                "Roughness map controlling microsurface smoothness (shiny vs. matte)",
                "Normal map adding surface detail without extra geometry",
                "Ambient light temperature map setting the room thermostat value"
              ],
              correctIndices: [0, 1, 2],
              why: "Base Color, Roughness, and Normal maps are core PBR texture channels. Room temperature is a physical property unrelated to material rendering.",
              pitfall: "Ensure Base Color maps do not contain baked lighting or shadows. PBR relies on the renderer calculating lighting; pre-baked shadows create incorrect double-lighting."
            }
          ]
        },
        {
          id: 2,
          title: "Lesson 2: Lighting & Camera",
          desc: "HDRI Environments, Three-Point Lighting, & Camera Settings",
          questions: [
            {
              type: "single",
              nodeId: "lighting",
              slug: "hdri-environment-lighting",
              difficulty: "beginner",
              question: "Why are HDRI (High Dynamic Range Image) environment maps the preferred lighting method for product and architectural visualization?",
              options: [
                "HDRIs capture real-world light intensity across the full dynamic range, providing physically accurate ambient illumination, reflections, and soft shadows from a single image.",
                "HDRIs are smaller in file size than standard JPG images.",
                "HDRIs can only be used in exterior scenes and do not work for interior rendering.",
                "HDRIs replace all material textures in the scene with environment colors."
              ],
              correctIdx: 0,
              why: "HDRIs store brightness values far beyond the 0-255 range of standard images. This extended range drives realistic exposure, light falloff, and specular reflections.",
              pitfall: "Rotate the HDRI to align the dominant light source (sun) with the intended shadow direction. The default orientation rarely matches the desired lighting angle."
            },
            {
              type: "single",
              nodeId: "lighting",
              slug: "three-point-lighting",
              difficulty: "beginner",
              question: "In the three-point lighting setup for product visualization, what is the specific role of the fill light?",
              options: [
                "The fill light softens shadows created by the key light by providing lower-intensity illumination from the opposite side, controlling the shadow density and contrast ratio.",
                "The fill light is the brightest light in the scene and defines the primary shadow direction.",
                "The fill light is placed directly behind the product to create a silhouette effect.",
                "The fill light is only used in outdoor scenes and has no role in studio setups."
              ],
              correctIdx: 0,
              why: "Key light establishes the dominant direction and shadows. Fill light (typically 1/2 to 1/4 key intensity) lifts shadow areas to control the contrast ratio.",
              pitfall: "Do not make the fill light as bright as the key light. Equal-intensity front lighting produces flat, shadowless renders that lack dimensionality."
            },
            {
              type: "single",
              nodeId: "camera",
              slug: "camera-focal-length",
              difficulty: "beginner",
              question: "How does camera focal length affect architectural interior visualization renders?",
              options: [
                "Shorter focal lengths (wide-angle, 18-24mm) capture more of the room but introduce perspective distortion; longer focal lengths (50-85mm) produce more natural proportions but show less of the space.",
                "Focal length only affects the brightness of the render output.",
                "All architectural renders should use a 200mm telephoto lens for realism.",
                "Focal length has no effect on perspective; it only changes the zoom level."
              ],
              correctIdx: 0,
              why: "Wide angles exaggerate spatial depth (rooms look larger) but distort edges. Standard focal lengths (35-50mm) balance spatial coverage with natural-looking proportions.",
              pitfall: "Avoid extreme wide-angle lenses (below 18mm) for interior visualization. The barrel distortion makes straight walls appear curved and rooms look unrealistically large."
            },
            {
              type: "single",
              nodeId: "camera",
              slug: "exposure-settings-render",
              difficulty: "beginner",
              question: "In physically-based rendering, what three camera parameters control exposure?",
              options: [
                "Aperture (f-stop), shutter speed, and ISO sensitivity work together to control how much light reaches the virtual sensor, just as in physical photography.",
                "Resolution, anti-aliasing samples, and output file format.",
                "Material reflectivity, scene polygon count, and GPU memory.",
                "Render engine version, operating system, and monitor calibration."
              ],
              correctIdx: 0,
              why: "PBR cameras simulate real photography exposure. Lower f-stop = more light + shallower DOF. Slower shutter = more light + motion blur. Higher ISO = more light + noise.",
              pitfall: "When adjusting exposure, change one parameter at a time. Compensating aperture changes with ISO changes simultaneously makes it impossible to isolate the visual effect."
            },
            {
              type: "multiple",
              nodeId: "lighting",
              slug: "gi-algorithms",
              difficulty: "beginner",
              question: "Which of the following are Global Illumination (GI) algorithms used in rendering engines? (Select all correct)",
              options: [
                "Path Tracing (unbiased Monte Carlo light transport simulation)",
                "Irradiance Cache / Light Cache (interpolated indirect illumination)",
                "Photon Mapping (two-pass method storing photon energy hits)",
                "Gouraud Shading (per-vertex color interpolation for real-time display)"
              ],
              correctIndices: [0, 1, 2],
              why: "Path Tracing, Irradiance Cache, and Photon Mapping are GI techniques for computing indirect light bounces. Gouraud shading is a real-time display technique, not a GI algorithm.",
              pitfall: "Path tracing produces the most accurate results but requires many samples to reduce noise. Use denoising algorithms to achieve clean results at practical sample counts."
            }
          ]
        },
        {
          id: 3,
          title: "Lesson 3: Rendering & Post-Production",
          desc: "Render Settings, Denoising, & Compositing Workflows",
          questions: [
            {
              type: "single",
              nodeId: "rendering",
              slug: "sampling-noise-tradeoff",
              difficulty: "beginner",
              question: "What is the relationship between render sample count and image noise in path-traced rendering?",
              options: [
                "Higher sample counts reduce noise by averaging more random light paths per pixel, but render time increases linearly with sample count; halving noise requires quadrupling samples.",
                "Sample count only affects render resolution, not image quality.",
                "Lower sample counts always produce cleaner images because they avoid light path interference.",
                "Sample count is fixed by the rendering engine and cannot be adjusted by the user."
              ],
              correctIdx: 0,
              why: "Monte Carlo path tracing convergence follows the inverse square root law. Doubling quality (halving noise) requires 4x the samples and thus 4x the render time.",
              pitfall: "Use AI denoising (Intel OIDN, NVIDIA OptiX) to achieve clean results at lower sample counts. Modern denoisers can produce production-quality results at 1/4 the traditional sample count."
            },
            {
              type: "single",
              nodeId: "rendering",
              slug: "render-passes-compositing",
              difficulty: "beginner",
              question: "Why do production visualization studios render separate passes (diffuse, reflection, shadow, depth) instead of a single beauty image?",
              options: [
                "Separate passes allow post-production adjustment of individual components (brighten reflections, soften shadows, add depth-of-field) without re-rendering the entire scene.",
                "Rendering passes is faster than rendering a single combined image.",
                "Separate passes are required because rendering engines cannot combine lighting effects.",
                "Passes are only useful for animation and serve no purpose in still image production."
              ],
              correctIdx: 0,
              why: "Multi-pass rendering gives compositors control. Adjusting reflection intensity in Photoshop takes seconds; re-rendering the entire scene to adjust reflections takes hours.",
              pitfall: "Ensure all passes are rendered with the same camera, resolution, and sample settings. Mismatched passes produce visible compositing artifacts at edges."
            },
            {
              type: "single",
              nodeId: "post-process",
              slug: "color-management-aces",
              difficulty: "beginner",
              question: "Why is ACES (Academy Color Encoding System) recommended for architectural visualization color management?",
              options: [
                "ACES provides a scene-referred, wide-gamut color space that preserves the full dynamic range of rendered data through the entire pipeline from rendering to final display output.",
                "ACES reduces the file size of rendered images by compressing color data.",
                "ACES is only used in film production and has no benefit for architectural rendering.",
                "ACES automatically color-corrects renders to match the client's monitor calibration."
              ],
              correctIdx: 0,
              why: "ACES separates the rendering color space from the display color space. This preserves highlight and shadow detail that would be clipped in standard sRGB workflows.",
              pitfall: "When using ACES, ensure texture inputs are converted to the correct ACES color space (ACEScg for linear data, sRGB for display-referred textures like base color maps)."
            },
            {
              type: "single",
              nodeId: "post-process",
              slug: "chromatic-aberration-lens",
              difficulty: "beginner",
              question: "In post-production for photorealistic visualization, what effect does adding subtle chromatic aberration achieve?",
              options: [
                "It simulates the color fringing at high-contrast edges caused by real camera lenses failing to focus all wavelengths at the same point, adding photographic realism.",
                "It converts the entire image to black and white for artistic effect.",
                "It increases the resolution of the rendered image beyond the original pixel count.",
                "It removes all lens distortion to produce perfectly straight lines."
              ],
              correctIdx: 0,
              why: "Real lenses have imperfections. Subtle chromatic aberration, vignetting, and lens distortion make CG images feel like photographs rather than computer graphics.",
              pitfall: "Apply lens effects subtly. Excessive chromatic aberration or bloom makes renders look artificial rather than photographic. Less is more for realism."
            },
            {
              type: "multiple",
              nodeId: "rendering",
              slug: "gpu-vs-cpu-rendering",
              difficulty: "beginner",
              question: "Which statements about GPU rendering versus CPU rendering are correct? (Select all correct)",
              options: [
                "GPU renderers (like NVIDIA OptiX, Redshift) are significantly faster for path tracing due to massive parallel processing cores",
                "CPU renderers (like Arnold CPU, V-Ray CPU) typically handle more complex scenes because system RAM is larger than VRAM",
                "Hybrid rendering uses both CPU and GPU resources to balance speed and scene complexity",
                "GPU rendering always produces more accurate results than CPU rendering regardless of the algorithm"
              ],
              correctIndices: [0, 1, 2],
              why: "GPUs excel at parallel computation (speed). CPUs handle larger scenes (more RAM). Hybrid rendering leverages both. Accuracy depends on the algorithm, not the processor type.",
              pitfall: "GPU rendering is limited by VRAM. Scenes exceeding available VRAM either fail or fall back to slower out-of-core rendering. Monitor VRAM usage during test renders."
            }
          ]
        }
,
        {
          id: 4,
          title: "Lesson 4: Lighting & Environment",
          desc: "HDRI Lighting, Sun Studies, & Interior Lighting Strategies",
          questions: [
              {
                type: "single",
                nodeId: "lighting",
                slug: "hdri-image-based-lighting",
                difficulty: "intermediate",
                question: "Why do visualization artists use HDRI (High Dynamic Range Image) environment maps instead of simple background colors for lighting?",
                options: [
                  "HDRI maps contain actual luminance data spanning many orders of magnitude, providing physically accurate illumination, reflections, and color bleeding from real-world environments.",
                  "HDRIs are smaller files that render faster than solid color backgrounds.",
                  "HDRIs only affect the background image, not the lighting of objects in the scene.",
                  "HDRIs are required by rendering software licenses to produce any output.",
                ],
                correctIdx: 0,
                why: "HDRIs encode real-world brightness ratios (sunlit areas 100,000x brighter than shadows). This creates natural lighting, soft shadows, and environment reflections that flat colors cannot provide.",
                pitfall: "Low-resolution HDRIs produce blurry reflections on glossy surfaces. Use 4K+ resolution HDRIs for scenes with reflective materials (chrome, glass, water)."
              },
              {
                type: "single",
                nodeId: "lighting",
                slug: "three-point-lighting",
                difficulty: "beginner",
                question: "In product visualization, what is the purpose of a classic three-point lighting setup (key, fill, rim)?",
                options: [
                  "Key light provides main illumination direction; fill light softens shadows on the opposite side; rim/back light separates the subject from the background by edge-highlighting the silhouette.",
                  "Three identical lights pointed at the same spot create the brightest possible illumination.",
                  "Three lights are the minimum required by rendering engines to calculate any shadows.",
                  "The three lights correspond to red, green, and blue color channels for white balance.",
                ],
                correctIdx: 0,
                why: "Three-point lighting creates depth perception in 2D images. The key establishes mood/direction, fill controls shadow density/contrast, and rim adds dimensional separation.",
                pitfall: "Don't use three-point lighting dogmatically. Moody automotive renders may use only key + rim (no fill) for dramatic contrast. Let the creative intent drive the setup."
              },
              {
                type: "single",
                nodeId: "lighting",
                slug: "interior-artificial-lighting",
                difficulty: "intermediate",
                question: "When rendering architectural interiors, why is accurate IES photometric data important for artificial light sources?",
                options: [
                  "IES profiles define the real-world light distribution pattern (beam angle, intensity falloff, asymmetry) of specific luminaires, producing physically accurate illumination matching manufacturer specifications.",
                  "IES files make lights render faster by reducing calculation complexity.",
                  "IES data is only used for exterior street lighting, not interior design.",
                  "IES profiles add decorative lens flare effects to light fixtures.",
                ],
                correctIdx: 0,
                why: "Each luminaire has a unique distribution (narrow spot, wide flood, asymmetric wall-wash). IES data from manufacturers ensures rendered lighting matches what will be installed, validating design decisions.",
                pitfall: "Verify IES file units (candela vs. lumens) and coordinate orientation. Some manufacturer IES files use non-standard orientations that produce rotated or inverted light patterns."
              },
              {
                type: "multiple",
                nodeId: "lighting",
                slug: "global-illumination-methods",
                difficulty: "advanced",
                question: "Which rendering algorithms compute global illumination (indirect light bounces) in architectural visualization? (Select all correct)",
                options: [
                  "Path tracing (Monte Carlo random ray sampling)",
                  "Photon mapping (two-pass: photon emission + gathering)",
                  "Irradiance caching (interpolating indirect illumination between sample points)",
                  "Flat shading (no lighting calculation, only base color display)",
                ],
                correctIndices: [0, 1, 2],
                why: "Path tracing, photon mapping, and irradiance caching all compute multi-bounce indirect illumination. Flat shading displays unlit base color with no GI calculation.",
                pitfall: "Irradiance caching is fast but can miss small-scale color bleeding (colored glass caustics). Switch to brute-force path tracing for scenes where subtle indirect effects are critical."
              },
              {
                type: "single",
                nodeId: "camera",
                slug: "sun-study-animation",
                difficulty: "beginner",
                question: "What does a sun study (solar analysis) animation reveal about a building design?",
                options: [
                  "How sunlight and shadows move across the building and surrounding context throughout the day and year, informing facade orientation, shading device design, and daylighting performance.",
                  "How the building's structural loads change with temperature across seasons.",
                  "The chemical degradation rate of exterior paint under UV exposure.",
                  "The electricity generation capacity of solar panels on the roof.",
                ],
                correctIdx: 0,
                why: "Sun studies visualize solar access for daylighting, identify overshadowing of neighbors, validate shading device effectiveness, and inform passive solar design decisions.",
                pitfall: "Set correct geographic coordinates and true north orientation. A 10-degree north error dramatically changes shadow patterns, especially at high latitudes or during winter months."
              }
          ]
        },
        {
          id: 5,
          title: "Lesson 5: Post-Processing & Delivery",
          desc: "Compositing, Color Management, & Real-Time Visualization",
          questions: [
              {
                type: "single",
                nodeId: "post-process",
                slug: "render-passes-compositing",
                difficulty: "intermediate",
                question: "Why do professional visualization artists render separate passes (diffuse, reflection, shadow, Z-depth) instead of a single combined beauty image?",
                options: [
                  "Separate passes allow post-production adjustment of individual lighting components (brighten reflections, soften shadows, adjust depth-of-field) without re-rendering the entire scene.",
                  "Separate passes are required because rendering software cannot combine all effects simultaneously.",
                  "Separate passes reduce the total file size compared to a single combined image.",
                  "Separate passes are only used in film VFX, never in architectural visualization.",
                ],
                correctIdx: 0,
                why: "Compositing passes in Photoshop/Nuke gives artistic control after the expensive render phase. Adjust shadow intensity, add fog via Z-depth, tweak reflections — all without waiting for another render.",
                pitfall: "Render passes in linear color space (32-bit EXR), not sRGB 8-bit. Compositing in sRGB produces incorrect blending, banding, and clipped highlights."
              },
              {
                type: "single",
                nodeId: "post-process",
                slug: "color-management-aces",
                difficulty: "advanced",
                question: "What problem does ACES (Academy Color Encoding System) solve in a visualization pipeline?",
                options: [
                  "ACES provides a scene-referred linear color space with wide gamut that preserves all captured/rendered color data through the pipeline, with standardized transforms for display on different devices.",
                  "ACES compresses image files to reduce storage requirements.",
                  "ACES is a camera brand that produces the sharpest photographs.",
                  "ACES converts all images to grayscale for structural analysis.",
                ],
                correctIdx: 0,
                why: "Without ACES, textures in different color spaces (sRGB photos, raw HDRIs, Rec.709 video) produce inconsistent results. ACES linearizes everything into one interchange space for predictable compositing.",
                pitfall: "Apply ACES input transforms (IDTs) to all texture maps. A sRGB texture loaded without IDT into an ACES pipeline appears washed out because the renderer double-linearizes it."
              },
              {
                type: "single",
                nodeId: "rendering",
                slug: "realtime-vs-offline-rendering",
                difficulty: "beginner",
                question: "What is the fundamental tradeoff between real-time rendering (Unreal Engine, Twinmotion) and offline path tracing (V-Ray, Corona)?",
                options: [
                  "Real-time renders approximate lighting with rasterization tricks for interactive framerates; offline path tracers simulate physically accurate light transport but require minutes-to-hours per frame.",
                  "Real-time rendering produces higher quality results than offline rendering.",
                  "Offline rendering cannot display any image until the entire animation is complete.",
                  "Real-time rendering requires a constant internet connection while offline works locally.",
                ],
                correctIdx: 0,
                why: "Real-time uses screen-space reflections, pre-baked lightmaps, and ray-traced approximations for 30-60fps. Offline traces billions of rays for ground-truth GI, caustics, and subsurface scattering.",
                pitfall: "Real-time 'ray tracing' (RTX) is limited in bounce count and sample quality. Marketing claims of 'ray traced' real-time don't equal offline quality for architectural still images."
              },
              {
                type: "multiple",
                nodeId: "rendering",
                slug: "denoising-techniques",
                difficulty: "intermediate",
                question: "Which denoising approaches are used to clean up Monte Carlo noise in path-traced renders? (Select all correct)",
                options: [
                  "AI/ML denoisers (Intel OIDN, NVIDIA OptiX) trained on clean/noisy image pairs",
                  "Non-local means filtering using auxiliary buffers (normals, albedo, depth) to preserve edges",
                  "Simply increasing render samples until noise is imperceptible (brute force)",
                  "Applying JPEG compression to hide noise artifacts in the lossy encoding",
                ],
                correctIndices: [0, 1, 2],
                why: "AI denoisers, non-local means, and brute-force sampling all reduce noise legitimately. JPEG compression introduces its own block artifacts without actually improving the underlying render quality.",
                pitfall: "AI denoisers can hallucinate or smear fine detail (fabric weave, distant text). Always compare denoised output against a high-sample reference to verify no detail loss."
              },
              {
                type: "single",
                nodeId: "camera",
                slug: "360-panorama-rendering",
                difficulty: "intermediate",
                question: "What camera type and projection must be used to render a 360-degree interactive panorama for VR viewing?",
                options: [
                  "A spherical (equirectangular) camera that captures the full 360x180 degree environment, output as a 2:1 aspect ratio image that maps to a sphere for VR headset or web viewer display.",
                  "A standard perspective camera rotated 4 times at 90-degree intervals and stitched together.",
                  "A fisheye lens with 180-degree field of view, which covers the full sphere.",
                  "Any camera type works for VR — the VR software automatically fills in missing angles.",
                ],
                correctIdx: 0,
                why: "Equirectangular projection maps the full sphere onto a flat rectangle (like a world map). VR viewers inverse-project this back onto a sphere surrounding the viewer for immersive 360 viewing.",
                pitfall: "Render equirectangular panoramas at 8K+ resolution (8192x4096 minimum). Each viewer direction only samples a small region of the image, so visible resolution per eye is much lower than total pixel count."
              }
          ]
        }
      ]
    },
    placement: {
      trackTitle: "Placement Test",
      trackBadge: "🏆 Placement",
      drawCount: 12,
      questions: [
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-bim-clash",
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
              difficulty: "beginner",
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
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-fea-mesh",
              difficulty: "beginner",
          question: "In Finite Element Analysis (FEA), why is mesh convergence testing essential before accepting simulation results?",
          options: [
            "Mesh convergence verifies that results are independent of mesh density by iteratively refining until stress values stabilize, confirming numerical accuracy.",
            "Mesh convergence testing is only needed for 2D simulations.",
            "Mesh convergence speeds up the solver by reducing the total number of elements.",
            "Mesh convergence applies only to thermal simulations, not structural."
          ],
          correctIdx: 0,
          why: "Without convergence testing, results may change significantly with different mesh sizes, indicating the solution is mesh-dependent and unreliable.",
          pitfall: "Watch for stress singularities at sharp corners that prevent convergence. Model realistic fillets to avoid mathematically infinite stress concentrations."
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-cfd-turbulence",
              difficulty: "beginner",
          question: "In CFD simulation, what determines whether to use a laminar or turbulent flow solver?",
          options: [
            "The Reynolds number of the flow: low Re indicates laminar flow, high Re indicates turbulent flow requiring a turbulence model like k-omega SST or k-epsilon.",
            "Turbulent solvers should always be used regardless of flow conditions.",
            "The choice depends on the color scheme preferred for velocity contour plots.",
            "Laminar solvers are for gases only; turbulent solvers are for liquids only."
          ],
          correctIdx: 0,
          why: "Reynolds number is the dimensionless ratio of inertial to viscous forces. It determines the flow regime and thus the appropriate solver configuration.",
          pitfall: "Using a laminar solver for high-Reynolds-number turbulent flows produces physically incorrect results. Always estimate Re first."
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-pbr-materials",
              difficulty: "beginner",
          question: "In Physically Based Rendering (PBR), what do the Metalness and Roughness parameters control?",
          options: [
            "Metalness determines whether light is reflected as colored specular (metal=1) or white specular with diffuse color (metal=0); Roughness controls microsurface smoothness from mirror-like (0) to matte (1).",
            "Metalness sets the weight of the object; Roughness sets the polygon count.",
            "Both parameters only affect how the material appears in wireframe mode.",
            "Metalness and Roughness are interchangeable and produce the same visual effect."
          ],
          correctIdx: 0,
          why: "PBR separates materials into metallic conductors and dielectric insulators. Roughness controls the spread of specular reflections on both types.",
          pitfall: "Real-world metals have base colors from their Fresnel reflectance curves (gold is yellow, copper is reddish). Do not use pure white as the base color for metals."
        },
        {
          type: "single",
          nodeId: "placement",
          slug: "placement-render-passes",
              difficulty: "beginner",
          question: "Why do visualization studios render separate passes (diffuse, reflection, depth, shadow) rather than a single composite image?",
          options: [
            "Separate passes enable non-destructive post-production adjustments — brightening reflections, adding depth-of-field blur, or softening shadows — without re-rendering the entire scene.",
            "Rendering separate passes is faster than rendering a single combined image.",
            "Separate passes are only useful for film VFX and have no application in architecture.",
            "Rendering engines cannot combine multiple light effects into a single output."
          ],
          correctIdx: 0,
          why: "Multi-pass rendering separates light components for compositing flexibility. Adjusting a reflection pass in Photoshop takes seconds versus hours of re-rendering.",
          pitfall: "Always render passes at the same resolution and sample count. Mismatched settings cause visible edge artifacts when compositing."
        }
      ]
    }
  }  // 2. 状态机与游戏数据初始化
  let state = {
    activeTrack: "",
    activeLessonId: null, // 当前小课 ID (1, 2, 3)，如果是定级测试则为 null
    questions: [],
    currentIndex: 0,
    hearts: 3,
    xpTotal: 0,
    perfectRun: true,
    selectedOptionIdx: -1,
    selectedIndices: [], // 用于存储多选题选中的索引
    streakCount: 0
  };

  // 3. 元素选择器
  const selectionScreen = document.getElementById("quiz-selection-screen");
  const activeScreen = document.getElementById("quiz-active-screen");
  const resultScreen = document.getElementById("quiz-result-screen");
  const lessonsScreen = document.getElementById("quiz-lessons-screen");
  
  const questionTitle = document.getElementById("quiz-question-title");
  const optionsWrapper = document.getElementById("quiz-options-wrapper");
  const trackBadge = document.getElementById("quiz-track-badge");
  const questionProgress = document.getElementById("quiz-question-progress");
  const progressBar = document.getElementById("quiz-progress-bar");
  const heartsContainer = document.getElementById("quiz-hearts-container");

  const feedbackBanner = document.getElementById("quiz-feedback-banner");
  const feedbackStatus = document.getElementById("quiz-feedback-status");
  const explanationBody = document.getElementById("quiz-explanation-body");
  const btnContinue = document.getElementById("quiz-btn-continue");
  const btnSubmit = document.getElementById("quiz-submit-btn");

  const successView = document.getElementById("quiz-success-view");
  const failureView = document.getElementById("quiz-failure-view");
  const resultXp = document.getElementById("result-xp");
  const resultStatus = document.getElementById("result-status");

  const globalStreakBadge = document.getElementById("global-streak-badge");
  const globalStreakCount = document.getElementById("global-streak-count");

  // 判断小课是否已解锁
  function isLessonUnlocked(trackKey, lessonId) {
    if (lessonId === 1) return true;
    
    let progress = {};
    try {
      progress = JSON.parse(localStorage.getItem("gstarcademy_lessons_progress")) || {};
    } catch (_) {}
    
    const trackProgress = progress[trackKey] || [];
    return trackProgress.includes(lessonId - 1);
  }

  // 显示小课关卡中心
  function showLessonsScreen(trackKey) {
    state.activeTrack = trackKey;
    state.activeLessonId = null;

    if (selectionScreen) selectionScreen.style.display = "none";
    if (activeScreen) activeScreen.style.display = "none";
    if (resultScreen) resultScreen.style.display = "none";
    if (lessonsScreen) lessonsScreen.style.display = "block";

    const track = QUIZ_DATABASE[trackKey];
    
    const unitTitleEl = document.getElementById("lessons-unit-title");
    const unitSubtitleEl = document.getElementById("lessons-unit-subtitle");
    if (unitTitleEl) {
      unitTitleEl.textContent = `Unit: ${track.trackTitle}`;
    }
    if (unitSubtitleEl) {
      unitSubtitleEl.textContent = "Complete each bite-sized lesson sequentially to master this career track and unlock all roadmap nodes!";
    }

    renderLessonsList(trackKey);
  }

  // 渲染小课关卡中心解锁列表
  function renderLessonsList(trackKey) {
    const cardsWrapper = document.getElementById("lessons-cards-wrapper");
    if (!cardsWrapper) return;

    cardsWrapper.innerHTML = "";

    const track = QUIZ_DATABASE[trackKey];
    const lessons = track.lessons;

    let progress = {};
    try {
      progress = JSON.parse(localStorage.getItem("gstarcademy_lessons_progress")) || {};
    } catch (_) {}

    const trackProgress = progress[trackKey] || [];

    lessons.forEach(lesson => {
      const lessonId = lesson.id;
      let status = "locked"; // "locked", "active", "completed"

      if (trackProgress.includes(lessonId)) {
        status = "completed";
      } else if (lessonId === 1 || trackProgress.includes(lessonId - 1)) {
        status = "active";
      }

      const card = document.createElement("div");
      card.className = "lesson-portal-card";
      if (status === "completed") {
        card.classList.add("completed");
      } else if (status === "active") {
        card.classList.add("active-lesson");
      } else {
        card.classList.add("locked");
      }

      let statusTagHtml = "";
      let buttonText = "";
      let buttonClass = "";
      let buttonAttrs = "";

      if (status === "completed") {
        statusTagHtml = `<span class="lesson-status-tag completed">Passed ✅</span>`;
        buttonText = "Review";
        buttonClass = "btn";
      } else if (status === "active") {
        statusTagHtml = `<span class="lesson-status-tag active">Active 🟢</span>`;
        buttonText = "Start";
        buttonClass = "btn btn-primary";
      } else {
        statusTagHtml = `<span class="lesson-status-tag locked">Locked 🔒</span>`;
        buttonText = "Locked 🔒";
        buttonClass = "btn";
        buttonAttrs = "disabled";
      }

      card.innerHTML = `
        <div class="lesson-card-meta">
          <div class="lesson-card-badge">${status === "completed" ? "✓" : lessonId}</div>
          <div class="lesson-card-info">
            <h4>${lesson.title} ${statusTagHtml}</h4>
            <p class="meta">${lesson.desc}</p>
          </div>
        </div>
        <button type="button" class="${buttonClass}" ${buttonAttrs} onclick="window.location.href='?track=${trackKey}&lesson=${lessonId}'">${buttonText}</button>
      `;

      cardsWrapper.appendChild(card);
    });
  }

  // 4. 入口分析 & 初始化
  function init() {
    initStreakBadge();

    const params = new URLSearchParams(window.location.search);
    const trackParam = params.get("track");
    const lessonParam = params.get("lesson");

    if (trackParam) {
      if (trackParam === "placement") {
        startQuiz("placement");
      } else if (trackParam === "mistake") {
        let mistakes = [];
        try {
          mistakes = JSON.parse(localStorage.getItem("gstarcademy_mistakes")) || [];
        } catch (_) {}
        if (mistakes.length === 0) {
          window.location.href = "quiz";
        } else {
          startQuiz("mistake");
        }
      } else if (QUIZ_DATABASE[trackParam]) {
        if (lessonParam) {
          const lessonId = parseInt(lessonParam, 10);
          if ([1, 2, 3].includes(lessonId)) {
            if (isLessonUnlocked(trackParam, lessonId)) {
              startQuiz(trackParam, lessonId);
            } else {
              window.location.href = `quiz?track=${trackParam}`;
            }
          } else {
            window.location.href = `quiz?track=${trackParam}`;
          }
        } else {
          showLessonsScreen(trackParam);
        }
      } else {
        showSelectionScreen();
      }
    } else {
      showSelectionScreen();
    }
  }

  // 5. 连胜（Streak）计数器与主栏显示
  function initStreakBadge() {
    let streak = 0;
    try {
      streak = parseInt(localStorage.getItem("gstarcademy_streak_v1") || "0", 10);
    } catch (_) {}

    // Verify streak date validity (within 36 hours since last check, otherwise reset if too long)
    try {
      const lastCompletedStr = localStorage.getItem("gstarcademy_last_quiz_completed_date");
      if (lastCompletedStr && streak > 0) {
        const lastDate = new Date(lastCompletedStr);
        const today = new Date();
        // Calculate difference in hours
        const diffHours = (today.getTime() - lastDate.getTime()) / (1000 * 60 * 60);
        if (diffHours > 36) {
          // Streak broken
          streak = 0;
          localStorage.setItem("gstarcademy_streak_v1", "0");
        }
      }
    } catch (_) {}

    state.streakCount = streak;

    if (streak > 0) {
      if (globalStreakBadge) globalStreakBadge.style.display = "inline-flex";
      if (globalStreakCount) globalStreakCount.textContent = streak;
    }
  }

  // 触发每日打卡升级
  function triggerDailyStreakUpdate() {
    const todayStr = new Date().toDateString();
    let lastCompletedStr = "";
    try {
      lastCompletedStr = localStorage.getItem("gstarcademy_last_quiz_completed_date") || "";
    } catch (_) {}

    if (lastCompletedStr !== todayStr) {
      // It's a new day! Verify if it was yesterday
      let isYesterday = false;
      if (lastCompletedStr) {
        const lastDate = new Date(lastCompletedStr);
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        isYesterday = lastDate.toDateString() === yesterday.toDateString();
      }

      if (isYesterday || lastCompletedStr === "") {
        state.streakCount += 1;
      } else {
        state.streakCount = 1; // broken yesterday, reset to 1 today
      }

      try {
        localStorage.setItem("gstarcademy_streak_v1", String(state.streakCount));
        localStorage.setItem("gstarcademy_last_quiz_completed_date", todayStr);
      } catch (_) {}

      // Update badge
      if (globalStreakBadge) globalStreakBadge.style.display = "inline-flex";
      if (globalStreakCount) globalStreakCount.textContent = state.streakCount;
    }
  }

  // 显示路线选择主卡，并更新进度管家面板
  function showSelectionScreen() {
    if (selectionScreen) selectionScreen.style.display = "block";
    if (activeScreen) activeScreen.style.display = "none";
    if (resultScreen) resultScreen.style.display = "none";
    if (lessonsScreen) lessonsScreen.style.display = "none";
    
    // 初始化/更新进度管家数据
    updateBackupManager();
    // 初始化/更新错题本卡片
    updateMistakeCard();
    // 渲染可视化仪表盘
    renderDashboardStats();
  }

  // 渲染/动画化可视化熟练度图谱面板
  function renderDashboardStats() {
    let masteredProgress = { bim: [], mcad: [], civil: [], draft: [] };
    try {
      masteredProgress = JSON.parse(localStorage.getItem("gstarcademy_roadmap_progress")) || {
        bim: [], mcad: [], civil: [], draft: []
      };
    } catch (_) {}

    // 补全结构安全防护
    ["bim", "mcad", "civil", "draft"].forEach(t => {
      if (!masteredProgress[t]) masteredProgress[t] = [];
    });

    const tracks = ["bim", "mcad", "civil", "draft"];
    tracks.forEach(tKey => {
      const count = Math.min(masteredProgress[tKey].length, 5); // 上限 5
      const pct = Math.round((count / 5) * 100);

      // 找到对应的 DOM
      const ringFill = document.getElementById(`ring-fill-${tKey}`);
      const ringText = document.getElementById(`ring-text-${tKey}`);
      const statDesc = document.getElementById(`stat-desc-${tKey}`);

      if (statDesc) {
        statDesc.textContent = `${count} / 5 Lit`;
      }
      if (ringText) {
        ringText.textContent = `${pct}%`;
      }

      if (ringFill) {
        // 圆环周长为 157 (2 * PI * 25)
        const strokeOffset = 157 - (157 * pct) / 100;
        // 延迟触发动画以实现动效
        setTimeout(() => {
          ringFill.style.strokeDashoffset = String(strokeOffset);
        }, 100);
      }
    });
  }

  // 初始化/更新进度管家数据及事件绑定
  let backupInitialized = false;
  function updateBackupManager() {
    const statXpEl = document.getElementById("backup-stat-xp");
    const statStreakEl = document.getElementById("backup-stat-streak");
    const statNodesEl = document.getElementById("backup-stat-nodes");
    const codeInput = document.getElementById("backup-code-input");
    const btnCopy = document.getElementById("btn-copy-backup");
    const importInput = document.getElementById("import-code-input");
    const btnImport = document.getElementById("btn-import-backup");
    const msgEl = document.getElementById("backup-message");

    if (!statXpEl || !codeInput) return;

    // 1. 读取 localStorage 数据
    let totalXp = 0;
    try {
      totalXp = parseInt(localStorage.getItem("gstarcademy_total_xp") || "0", 10);
    } catch (_) {}

    let streak = state.streakCount;

    let nodeCount = 0;
    try {
      const progressData = JSON.parse(localStorage.getItem("gstarcademy_roadmap_progress")) || {};
      Object.keys(progressData).forEach(trackKey => {
        if (Array.isArray(progressData[trackKey])) {
          nodeCount += progressData[trackKey].length;
        }
      });
    } catch (_) {}

    // 2. 更新面板数值
    statXpEl.textContent = `${totalXp} XP`;
    statStreakEl.textContent = `🔥 ${streak} Days`;
    statNodesEl.textContent = `${nodeCount} / 20`;

    // 3. 生成 Base64 进度恢复码
    const backupData = {
      version: 1,
      timestamp: Date.now(),
      data: {
        totalXp: totalXp,
        streak: streak,
        lastDate: localStorage.getItem("gstarcademy_last_quiz_completed_date") || "",
        roadmapProgress: localStorage.getItem("gstarcademy_roadmap_progress") || "{}",
        conceptMastery: localStorage.getItem("gstarcademy_concept_mastery") || "[]",
        lessonsProgress: localStorage.getItem("gstarcademy_lessons_progress") || "{}"
      }
    };

    try {
      const jsonStr = JSON.stringify(backupData);
      // 使用 btoa 加密
      const base64Code = btoa(unescape(encodeURIComponent(jsonStr)));
      codeInput.value = base64Code;
    } catch (err) {
      codeInput.value = "生成失败";
      console.error("Backup code generation error:", err);
    }

    // 4. 事件绑定 (只需绑定一次)
    if (!backupInitialized) {
      backupInitialized = true;

      // 复制按钮
      if (btnCopy) {
        btnCopy.addEventListener("click", () => {
          if (codeInput.value && codeInput.value !== "生成失败") {
            // 复制到剪贴板
            navigator.clipboard.writeText(codeInput.value).then(() => {
              showBackupMessage("📋 Progress recovery code copied to clipboard!", "success");
            }).catch(() => {
              // 兼容方案
              codeInput.select();
              document.execCommand("copy");
              showBackupMessage("📋 Progress recovery code selected and copied!", "success");
            });
          }
        });
      }

      // 导入按钮
      if (btnImport) {
        btnImport.addEventListener("click", () => {
          const rawCode = importInput.value.trim();
          if (!rawCode) {
            showBackupMessage("❌ Please enter a valid recovery code.", "error");
            return;
          }

          try {
            // 解密 Base64
            const jsonStr = decodeURIComponent(escape(atob(rawCode)));
            const parsed = JSON.parse(jsonStr);

            // 基础校验
            if (!parsed || parsed.version !== 1 || !parsed.data) {
              showBackupMessage("❌ Invalid recovery code format or version mismatch.", "error");
              return;
            }

            const data = parsed.data;

            // 写入 localStorage
            if (data.totalXp !== undefined) {
              localStorage.setItem("gstarcademy_total_xp", String(data.totalXp));
            }
            if (data.streak !== undefined) {
              localStorage.setItem("gstarcademy_streak_v1", String(data.streak));
            }
            if (data.lastDate !== undefined) {
              localStorage.setItem("gstarcademy_last_quiz_completed_date", data.lastDate);
            }
            if (data.roadmapProgress !== undefined) {
              localStorage.setItem("gstarcademy_roadmap_progress", data.roadmapProgress);
            }
            if (data.conceptMastery !== undefined) {
              localStorage.setItem("gstarcademy_concept_mastery", data.conceptMastery);
            }
            if (data.lessonsProgress !== undefined) {
              localStorage.setItem("gstarcademy_lessons_progress", data.lessonsProgress);
            }

            showBackupMessage("🎉 Progress restored successfully! Reloading...", "success");
            
            // 延迟刷新
            setTimeout(() => {
              location.reload();
            }, 1500);

          } catch (err) {
            showBackupMessage("❌ Restore failed. Recovery code is invalid or corrupted.", "error");
            console.error("Import error:", err);
          }
        });
      }
    }

    function showBackupMessage(msg, type) {
      if (msgEl) {
        msgEl.textContent = msg;
        msgEl.className = `backup-message ${type}`;
        msgEl.style.display = "block";
        
        // 5秒后自动隐藏
        setTimeout(() => {
          msgEl.style.display = "none";
        }, 5000);
      }
    }
  }

  // 数组打乱辅助函数 (Fisher-Yates)
  function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }

  // 开始测试
  function startQuiz(trackKey, lessonId) {
    const track = QUIZ_DATABASE[trackKey];
    state.activeTrack = trackKey;
    state.activeLessonId = lessonId || null;

    let totalPool = [];
    let countToDraw = 5;

    if (trackKey === "placement") {
      totalPool = track.questions;
      countToDraw = track.drawCount || 10;
    } else if (trackKey === "mistake") {
      let mistakes = [];
      try {
        mistakes = JSON.parse(localStorage.getItem("gstarcademy_mistakes")) || [];
      } catch (_) {}
      totalPool = findMistakeQuestions(mistakes);
      countToDraw = totalPool.length;
    } else {
      const lesson = track.lessons[lessonId - 1];
      totalPool = lesson.questions;
      countToDraw = Math.min(3, totalPool.length);
    }

    const shuffledPool = shuffleArray([...totalPool]);
    
    // 2. 截取并深拷贝抽出来的题目，避免直接修改破坏 QUIZ_DATABASE 内存
    state.questions = shuffledPool.slice(0, countToDraw).map(q => {
      const qCopy = {
        nodeId: q.nodeId,
        slug: q.slug,
        difficulty: "beginner",
        question: q.question,
        options: [...q.options],
        correctIdx: q.correctIdx,
        correctIndices: q.correctIndices ? [...q.correctIndices] : undefined,
        why: q.why,
        pitfall: q.pitfall,
        type: q.type || "single"
      };

      // 3. 对这道题目的选项进行随机打乱，并重写正确答案索引
      if (qCopy.type === "multiple" || qCopy.correctIndices) {
        const correctTexts = qCopy.correctIndices.map(idx => qCopy.options[idx]);
        qCopy.options = shuffleArray([...qCopy.options]);
        qCopy.correctIndices = correctTexts.map(text => qCopy.options.indexOf(text));
      } else {
        const correctText = qCopy.options[qCopy.correctIdx];
        qCopy.options = shuffleArray([...qCopy.options]);
        qCopy.correctIdx = qCopy.options.indexOf(correctText);
      }

      return qCopy;
    });

    state.currentIndex = 0;
    state.hearts = 3;
    state.xpTotal = 0;
    state.perfectRun = true;
    state.selectedOptionIdx = -1;
    state.selectedIndices = [];

    if (selectionScreen) selectionScreen.style.display = "none";
    if (lessonsScreen) lessonsScreen.style.display = "none";
    if (activeScreen) activeScreen.style.display = "block";
    if (resultScreen) resultScreen.style.display = "none";

    if (trackBadge) {
      if (trackKey === "placement") {
        trackBadge.textContent = track.trackBadge;
        trackBadge.className = "badge badge-paid";
      } else if (trackKey === "mistake") {
        trackBadge.textContent = "🔴 Mistake Review";
        trackBadge.className = "badge badge-paid";
      } else {
        trackBadge.textContent = `${track.trackBadge} - L${lessonId}`;
        trackBadge.className = "badge " + (trackKey === "bim" ? "badge-free" : trackKey === "mcad" ? "badge-paid" : "badge-free");
      }
    }

    renderQuestion();
  }

  // 渲染题目
  function renderQuestion() {
    // Hide feedback banner
    feedbackBanner.classList.remove("show");

    const q = state.questions[state.currentIndex];
    
    // Progress
    questionProgress.textContent = `Question ${state.currentIndex + 1} of ${state.questions.length}`;
    const pct = Math.round((state.currentIndex / state.questions.length) * 100);
    progressBar.style.width = `${pct}%`;

    // Render Hearts
    renderHearts();

    // Set Text
    questionTitle.textContent = q.question;
    optionsWrapper.innerHTML = "";
    state.selectedOptionIdx = -1;
    state.selectedIndices = [];

    // 针对多选题，判断是否要展示 Submit 按钮
    const isMultiple = q.type === "multiple" || !!q.correctIndices;
    if (btnSubmit) {
      btnSubmit.style.display = isMultiple ? "block" : "none";
      btnSubmit.disabled = true;
    }

    // Build Options
    q.options.forEach((opt, idx) => {
      const keys = ["A", "B", "C", "D"];
      const btn = document.createElement("button");
      btn.className = "quiz-option-btn";
      if (isMultiple) {
        btn.classList.add("multiple-choice-btn");
      }
      btn.type = "button";
      btn.innerHTML = `
        <span class="quiz-option-key">${keys[idx]}</span>
        <span class="quiz-option-text">${opt}</span>
      `;

      btn.addEventListener("click", () => {
        if (state.selectedOptionIdx !== -1) return; // Answer locked
        if (isMultiple) {
          if (state.selectedIndices.includes(idx)) {
            state.selectedIndices = state.selectedIndices.filter(i => i !== idx);
            btn.classList.remove("selected");
          } else {
            state.selectedIndices.push(idx);
            btn.classList.add("selected");
          }
          if (btnSubmit) {
            btnSubmit.disabled = state.selectedIndices.length === 0;
          }
        } else {
          selectOption(idx, btn);
        }
      });

      optionsWrapper.appendChild(btn);
    });
  }

  // 渲染爱心列表
  function renderHearts() {
    heartsContainer.innerHTML = "";
    for (let i = 0; i < 3; i++) {
      const span = document.createElement("span");
      span.className = "quiz-heart" + (i >= state.hearts ? " broken" : "");
      span.innerHTML = i >= state.hearts ? "🖤" : "❤️";
      heartsContainer.appendChild(span);
    }
  }

  // 选项选中即时校验
  function selectOption(selectedIdx, btnEl) {
    state.selectedOptionIdx = selectedIdx;
    
    // Highlight selected
    btnEl.classList.add("selected");

    const q = state.questions[state.currentIndex];
    const isCorrect = selectedIdx === q.correctIdx;

    const allBtns = optionsWrapper.querySelectorAll(".quiz-option-btn");
    
    // Disable all options
    allBtns.forEach(btn => btn.classList.add("disabled"));

    if (isCorrect) {
      btnEl.classList.add("correct");
      state.xpTotal += 10;
      
      // Bottom banner green
      feedbackStatus.innerHTML = "🎉 Correct! +10 XP";
      feedbackStatus.className = "quiz-feedback-status ok";
      feedbackBanner.className = "quiz-feedback-bar show correct-bar";
      explanationBody.innerHTML = `<strong>Why it matters:</strong> ${q.why}`;
    } else {
      btnEl.classList.add("incorrect");
      state.perfectRun = false;
      state.hearts -= 1;
      
      // Shake hearts
      heartsContainer.classList.add("quiz-heart-shake");
      setTimeout(() => heartsContainer.classList.remove("quiz-heart-shake"), 400);

      // Highlight the correct one
      allBtns[q.correctIdx].classList.add("correct");

      // Redraw hearts
      renderHearts();

      // Bottom banner red
      feedbackStatus.innerHTML = "💔 Incorrect";
      feedbackStatus.className = "quiz-feedback-status err";
      feedbackBanner.className = "quiz-feedback-bar show incorrect-bar";
      explanationBody.innerHTML = `<strong>Common Pitfall:</strong> ${q.pitfall}<br><small style="opacity:0.8; display:block; margin-top:4px;">Correct Answer: ${q.options[q.correctIdx]}</small>`;
    }
  }

  // 点击“继续”推进状态
  btnContinue.addEventListener("click", () => {
    // Hide feedback banner
    feedbackBanner.classList.remove("show");

    if (state.hearts <= 0) {
      showFailureScreen();
      return;
    }

    state.currentIndex += 1;

    if (state.currentIndex >= state.questions.length) {
      showSuccessScreen();
    } else {
      renderQuestion();
    }
  });

  // 显示挑战失败卡片
  function showFailureScreen() {
    activeScreen.style.display = "none";
    resultScreen.style.display = "block";
    successView.style.display = "none";
    failureView.style.display = "block";

    const failureSecondaryBtn = failureView.querySelector('.btn:not(.btn-primary)');

    if (state.activeTrack === "placement") {
      const fTitle = failureView.querySelector('.hero-title');
      const fMeta = failureView.querySelector('.meta');
      const fBtn = failureView.querySelector('button');
      
      if (fTitle) {
        fTitle.textContent = "Placement Test Failed";
        fTitle.style.color = "#ef4444";
      }
      if (fMeta) {
        fMeta.textContent = "You ran out of lives or scored below 80%. Don't give up! Try starting with the core lessons to build up your skills.";
      }
      if (fBtn) {
        fBtn.textContent = "🔁 Retry Placement Test";
      }
      if (failureSecondaryBtn) {
        failureSecondaryBtn.textContent = "📚 Browse Wiki";
        failureSecondaryBtn.href = "knowledge-base";
      }
    } else if (state.activeTrack === "mistake") {
      const fTitle = failureView.querySelector('.hero-title');
      const fMeta = failureView.querySelector('.meta');
      const fBtn = failureView.querySelector('button');
      if (fTitle) {
        fTitle.textContent = "Review Failed";
        fTitle.style.color = "#ef4444";
      }
      if (fMeta) {
        fMeta.textContent = "You ran out of lives in this review session. Don't worry, try again to clear your mistakes!";
      }
      if (fBtn) {
        fBtn.textContent = "🔁 Retry Mistakes";
      }
      if (failureSecondaryBtn) {
        failureSecondaryBtn.textContent = "📋 Back to Tracks";
        failureSecondaryBtn.href = "quiz";
      }
    } else {
      // 恢复普通失败文案
      const fTitle = failureView.querySelector('.hero-title');
      const fMeta = failureView.querySelector('.meta');
      const fBtn = failureView.querySelector('button');
      if (fTitle) {
        fTitle.textContent = "Lesson Failed";
        fTitle.style.color = "#ef4444";
      }
      if (fMeta) {
        fMeta.textContent = "You ran out of lives in this challenge. Reviewing the atomic concepts in our Wiki will help you conquer it next time!";
      }
      if (fBtn) {
        fBtn.textContent = "🔁 Retry Lesson";
      }
      if (failureSecondaryBtn) {
        failureSecondaryBtn.textContent = "📋 Back to Unit Portal";
        failureSecondaryBtn.href = `?track=${state.activeTrack}`;
      }
    }
  }

  // 显示挑战成功结算卡片并写 LocalStorage
  function showSuccessScreen() {
    if (state.activeTrack === "mistake") {
      successView.style.display = "block";
      failureView.style.display = "none";

      triggerDailyStreakUpdate();

      // 错题消灭战通关固定得 +20 XP
      const finalXp = 20;
      resultXp.textContent = `+${finalXp} XP`;
      resultStatus.textContent = state.perfectRun ? "Perfect Run!" : "Passed";
      resultStatus.style.color = state.perfectRun ? "#eab308" : "#10b981";

      let currentTotalXp = 0;
      try {
        currentTotalXp = parseInt(localStorage.getItem("gstarcademy_total_xp") || "0", 10);
      } catch (_) {}
      currentTotalXp += finalXp;
      try {
        localStorage.setItem("gstarcademy_total_xp", String(currentTotalXp));
      } catch (_) {}

      // 更新文案
      const sTitle = successView.querySelector('.hero-title');
      const sMetaList = successView.querySelectorAll('p.meta');
      const successPrimaryBtn = successView.querySelector('.btn-primary');
      const successSecondaryBtn = successView.querySelector('.btn:not(.btn-primary)');

      if (sTitle) {
        sTitle.textContent = "Mistakes Cleared!";
        sTitle.style.color = "#10b981";
      }
      if (sMetaList && sMetaList[0]) {
        sMetaList[0].textContent = "Great job! You have successfully resolved your historically incorrect questions, solidifying your CAD skills.";
      }
      if (sMetaList && sMetaList[1]) {
        sMetaList[1].innerHTML = "🎯 <strong>Mistake Book Updated:</strong> Correct answers have been removed from your mistake list. Keep your record clean!";
      }

      if (successPrimaryBtn) {
        successPrimaryBtn.textContent = "📋 Back to Tracks";
        successPrimaryBtn.href = "quiz";
      }
      if (successSecondaryBtn) {
        successSecondaryBtn.textContent = "🗺️ View Learning Map";
        successSecondaryBtn.href = "knowledge-roadmap";
      }
      
      activeScreen.style.display = "none";
      resultScreen.style.display = "block";
      return;
    }

    // 如果是定级测试，但答对题目少于 8 题，重定向到 Failure 页！
    if (state.activeTrack === "placement" && state.xpTotal < 80) {
      showFailureScreen();
      return;
    }

    activeScreen.style.display = "none";
    resultScreen.style.display = "block";
    
    // 动态重写 successView 内部的文案和按钮
    const sTitle = successView.querySelector('.hero-title');
    const sMetaList = successView.querySelectorAll('p.meta');
    const successPrimaryBtn = successView.querySelector('.btn-primary');
    const successSecondaryBtn = successView.querySelector('.btn:not(.btn-primary)');
    
    if (state.activeTrack === "placement") {
      successView.style.display = "block";
      failureView.style.display = "none";

      triggerDailyStreakUpdate();

      const finalXp = 150;
      resultXp.textContent = `+${finalXp} XP`;
      resultStatus.textContent = "Expert";
      resultStatus.style.color = "#ca8a04";

      // 累加并存入全局总经验值
      let currentTotalXp = 0;
      try {
        currentTotalXp = parseInt(localStorage.getItem("gstarcademy_total_xp") || "0", 10);
      } catch (_) {}
      currentTotalXp += finalXp;
      try {
        localStorage.setItem("gstarcademy_total_xp", String(currentTotalXp));
      } catch (_) {}

      // 批量点亮所有 20 个技能节点
      const allTracks = ["bim", "mcad", "civil", "draft"];
      let masteredProgress = {};
      try {
        masteredProgress = JSON.parse(localStorage.getItem("gstarcademy_roadmap_progress")) || {};
      } catch (_) {}

      allTracks.forEach(tKey => {
        masteredProgress[tKey] = QUIZ_DATABASE[tKey].nodesToMaster;
      });

      try {
        localStorage.setItem("gstarcademy_roadmap_progress", JSON.stringify(masteredProgress));
      } catch (_) {}

      // 批量点亮 wiki 概念
      let masteredConcepts = [];
      try {
        masteredConcepts = JSON.parse(localStorage.getItem("gstarcademy_concept_mastery")) || [];
      } catch (_) {}

      allTracks.forEach(tKey => {
        QUIZ_DATABASE[tKey].lessons.forEach(lesson => {
          lesson.questions.forEach(q => {
            if (q.slug && !masteredConcepts.includes(q.slug)) {
              masteredConcepts.push(q.slug);
            }
          });
        });
      });
      QUIZ_DATABASE.placement.questions.forEach(q => {
        if (q.slug && !masteredConcepts.includes(q.slug)) {
          masteredConcepts.push(q.slug);
        }
      });

      try {
        localStorage.setItem("gstarcademy_concept_mastery", JSON.stringify(masteredConcepts));
      } catch (_) {}

      if (sTitle) {
        sTitle.textContent = "Placement Test Passed!";
        sTitle.style.color = "#ca8a04";
      }
      if (sMetaList && sMetaList[0]) {
        sMetaList[0].textContent = "Great job! You've successfully passed the comprehensive placement test, demonstrating strong CAD competency.";
      }
      if (sMetaList && sMetaList[1]) {
        sMetaList[1].innerHTML = "🎯 <strong>Roadmap Synced:</strong> Congratulations! All 20 skill nodes across all 4 pathways have been fully lit up!";
      }

      if (successPrimaryBtn) {
        successPrimaryBtn.textContent = "🗺️ View Learning Map";
        successPrimaryBtn.href = "knowledge-roadmap";
      }
      if (successSecondaryBtn) {
        successSecondaryBtn.textContent = "🔄 Try Other Pathways";
        successSecondaryBtn.href = "quiz";
      }

    } else {
      // 普通小课 (Lesson 1 / 2 / 3) 挑战成功
      successView.style.display = "block";
      failureView.style.display = "none";

      triggerDailyStreakUpdate();

      // Lesson 1/2 通关得 +20 XP，Lesson 3 通关得 +30 XP
      const finalXp = state.activeLessonId === 3 ? 30 : 20;
      resultXp.textContent = `+${finalXp} XP`;
      resultStatus.textContent = state.perfectRun ? "Perfect Run!" : "Passed";
      resultStatus.style.color = state.perfectRun ? "#eab308" : "#10b981";

      let currentTotalXp = 0;
      try {
        currentTotalXp = parseInt(localStorage.getItem("gstarcademy_total_xp") || "0", 10);
      } catch (_) {}
      currentTotalXp += finalXp;
      try {
        localStorage.setItem("gstarcademy_total_xp", String(currentTotalXp));
      } catch (_) {}

      // 更新小课通关纪录
      let lessonsProgress = {};
      try {
        lessonsProgress = JSON.parse(localStorage.getItem("gstarcademy_lessons_progress")) || {};
      } catch (_) {}
      if (!lessonsProgress[state.activeTrack]) {
        lessonsProgress[state.activeTrack] = [];
      }
      if (!lessonsProgress[state.activeTrack].includes(state.activeLessonId)) {
        lessonsProgress[state.activeTrack].push(state.activeLessonId);
      }
      try {
        localStorage.setItem("gstarcademy_lessons_progress", JSON.stringify(lessonsProgress));
      } catch (_) {}

      const track = QUIZ_DATABASE[state.activeTrack];
      const lesson = track.lessons[state.activeLessonId - 1];

      // 点亮该小课对应的概念 Wiki
      let masteredConcepts = [];
      try {
        masteredConcepts = JSON.parse(localStorage.getItem("gstarcademy_concept_mastery")) || [];
      } catch (_) {}
      lesson.questions.forEach(q => {
        if (q.slug && !masteredConcepts.includes(q.slug)) {
          masteredConcepts.push(q.slug);
        }
      });
      try {
        localStorage.setItem("gstarcademy_concept_mastery", JSON.stringify(masteredConcepts));
      } catch (_) {}

      // 特殊处理 Lesson 3 (终极小课) 通关：单元整体点亮，同步路线图 5 个节点
      if (state.activeLessonId === 3) {
        let masteredProgress = {};
        try {
          masteredProgress = JSON.parse(localStorage.getItem("gstarcademy_roadmap_progress")) || {};
        } catch (_) {}
        
        if (!masteredProgress[state.activeTrack]) {
          masteredProgress[state.activeTrack] = [];
        }

        track.nodesToMaster.forEach(nodeId => {
          if (!masteredProgress[state.activeTrack].includes(nodeId)) {
            masteredProgress[state.activeTrack].push(nodeId);
          }
        });

        try {
          localStorage.setItem("gstarcademy_roadmap_progress", JSON.stringify(masteredProgress));
        } catch (_) {}

        if (sTitle) {
          sTitle.textContent = "Unit Completed!";
          sTitle.style.color = "#10b981";
        }
        if (sMetaList && sMetaList[0]) {
          sMetaList[0].textContent = `Congratulations! You have successfully completed all lessons for the ${track.trackTitle} track.`;
        }
        if (sMetaList && sMetaList[1]) {
          sMetaList[1].innerHTML = "🎯 <strong>Roadmap Synced:</strong> Congratulations! All 5 core nodes on the skill map have been lit up and added to your concept library.";
        }

        if (successPrimaryBtn) {
          successPrimaryBtn.textContent = "🗺️ View Learning Map";
          successPrimaryBtn.href = "knowledge-roadmap";
        }
        if (successSecondaryBtn) {
          successSecondaryBtn.textContent = "🔄 Try Other Pathways";
          successSecondaryBtn.href = "quiz";
        }
      } else {
        // Lesson 1 或 2 通关
        if (sTitle) {
          sTitle.textContent = "Lesson Completed!";
          sTitle.style.color = "#10b981";
        }
        if (sMetaList && sMetaList[0]) {
          sMetaList[0].textContent = `Congratulations on passing ${lesson.title}! You have mastered the core concepts of this lesson.`;
        }
        if (sMetaList && sMetaList[1]) {
          sMetaList[1].innerHTML = "🎯 <strong>Next Lesson Unlocked:</strong> Continue to the next challenge, or finish the unit to light up the skill tree!";
        }

        if (successPrimaryBtn) {
          successPrimaryBtn.textContent = "➡️ Continue";
          successPrimaryBtn.href = `?track=${state.activeTrack}&lesson=${state.activeLessonId + 1}`;
        }
        if (successSecondaryBtn) {
          successSecondaryBtn.textContent = "📋 Back to Unit Portal";
          successSecondaryBtn.href = `?track=${state.activeTrack}`;
        }
      }
    }
  }

  // 6. Keyboard Shortcuts Support (A, B, C, D to select, Enter / Space to continue)
  window.addEventListener("keydown", (e) => {
    // If active quiz screen is hidden, ignore
    if (activeScreen.style.display === "none") return;

    const key = e.key.toUpperCase();

    // Option select (A, B, C, D)
    if (state.selectedOptionIdx === -1) {
      if (key === "A") selectShortcutOption(0);
      else if (key === "B") selectShortcutOption(1);
      else if (key === "C") selectShortcutOption(2);
      else if (key === "D") selectShortcutOption(3);
      else if (e.key === "Enter") {
        const q = state.questions[state.currentIndex];
        const isMultiple = q && (q.type === "multiple" || !!q.correctIndices);
        if (isMultiple && btnSubmit && !btnSubmit.disabled && btnSubmit.style.display !== "none") {
          btnSubmit.click();
        }
      }
    } else {
      // Continue (Enter)
      if (e.key === "Enter") {
        btnContinue.click();
      }
    }
  });

  function selectShortcutOption(idx) {
    const btns = optionsWrapper.querySelectorAll(".quiz-option-btn");
    if (btns && btns[idx]) {
      btns[idx].click();
    }
  }

  // 多选题校验与提交
  if (btnSubmit) {
    btnSubmit.addEventListener("click", () => {
      if (state.selectedOptionIdx !== -1) return; // 已经回答过了
      if (state.selectedIndices.length === 0) return; // 必须至少选一个
      
      // 标记为已答
      state.selectedOptionIdx = 999;
      verifyMultipleChoice();
    });
  }

  // 多选题校验
  function verifyMultipleChoice() {
    const q = state.questions[state.currentIndex];
    const allBtns = optionsWrapper.querySelectorAll(".quiz-option-btn");
    
    // 禁用所有选项
    allBtns.forEach(btn => btn.classList.add("disabled"));
    if (btnSubmit) btnSubmit.style.display = "none"; // 隐藏提交按钮

    const userAnswers = [...state.selectedIndices].sort((a, b) => a - b);
    const correctAnswers = [...q.correctIndices].sort((a, b) => a - b);
    
    const isCorrect = userAnswers.length === correctAnswers.length && 
                      userAnswers.every((val, idx) => val === correctAnswers[idx]);

    // 渲染 UI 反馈
    allBtns.forEach((btn, idx) => {
      const isUserSelected = userAnswers.includes(idx);
      const isTargetCorrect = correctAnswers.includes(idx);

      if (isUserSelected && isTargetCorrect) {
        btn.classList.add("correct");
        btn.classList.add("selected");
      } else if (isUserSelected && !isTargetCorrect) {
        btn.classList.add("incorrect");
        btn.classList.add("selected");
      } else if (!isUserSelected && isTargetCorrect) {
        // 用户漏选了的正确项，标绿提示
        btn.classList.add("correct");
      }
    });

    if (isCorrect) {
      state.xpTotal += 10;
      removeMistake(q.slug);
      
      feedbackStatus.innerHTML = "🎉 Correct! +10 XP";
      feedbackStatus.className = "quiz-feedback-status ok";
      feedbackBanner.className = "quiz-feedback-bar show correct-bar";
      explanationBody.innerHTML = `<strong>Why it matters:</strong> ${q.why}`;
    } else {
      state.perfectRun = false;
      state.hearts -= 1;
      collectMistake(q.slug);

      // Shake hearts
      heartsContainer.classList.add("quiz-heart-shake");
      setTimeout(() => heartsContainer.classList.remove("quiz-heart-shake"), 400);

      // Redraw hearts
      renderHearts();

      feedbackStatus.innerHTML = "💔 Incorrect";
      feedbackStatus.className = "quiz-feedback-status err";
      feedbackBanner.className = "quiz-feedback-bar show incorrect-bar";
      
      const correctTexts = q.correctIndices.map(idx => q.options[idx]).join(", ");
      explanationBody.innerHTML = `<strong>Common Pitfall:</strong> ${q.pitfall}<br><small style="opacity:0.8; display:block; margin-top:4px;">Correct Answers: ${correctTexts}</small>`;
    }
  }

  // 错题收集与清除
  function collectMistake(slug) {
    if (!slug) return;
    let mistakes = [];
    try {
      mistakes = JSON.parse(localStorage.getItem("gstarcademy_mistakes")) || [];
    } catch (_) {}
    if (!mistakes.includes(slug)) {
      mistakes.push(slug);
      try {
        localStorage.setItem("gstarcademy_mistakes", JSON.stringify(mistakes));
      } catch (_) {}
    }
    updateMistakeCard();
  }

  function removeMistake(slug) {
    if (!slug) return;
    let mistakes = [];
    try {
      mistakes = JSON.parse(localStorage.getItem("gstarcademy_mistakes")) || [];
    } catch (_) {}
    if (mistakes.includes(slug)) {
      mistakes = mistakes.filter(s => s !== slug);
      try {
        localStorage.setItem("gstarcademy_mistakes", JSON.stringify(mistakes));
      } catch (_) {}
    }
    updateMistakeCard();
  }

  function updateMistakeCard() {
    const card = document.getElementById("mistake-review-card");
    const badge = document.getElementById("mistake-count-badge");
    if (!card || !badge) return;

    let mistakes = [];
    try {
      mistakes = JSON.parse(localStorage.getItem("gstarcademy_mistakes")) || [];
    } catch (_) {}

    if (mistakes.length > 0) {
      card.style.display = "flex";
      badge.textContent = mistakes.length;
    } else {
      card.style.display = "none";
    }
  }

  function findMistakeQuestions(mistakeSlugs) {
    const pool = [];
    const tracks = ["bim", "mcad", "civil", "draft"];
    tracks.forEach(tKey => {
      QUIZ_DATABASE[tKey].lessons.forEach(lesson => {
        lesson.questions.forEach(q => {
          if (mistakeSlugs.includes(q.slug)) {
            pool.push(q);
          }
        });
      });
    });
    // placement
    QUIZ_DATABASE.placement.questions.forEach(q => {
      if (mistakeSlugs.includes(q.slug)) {
        pool.push(q);
      }
    });
    return pool;
  }

  // Hook initial boot
  init();

})();
