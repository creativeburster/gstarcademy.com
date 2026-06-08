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
          title: "Lesson 1: 热身测验 (Warmup)",
          desc: "BIM 核心范式、LOD 精度等级、协作流程与标准",
          questions: [
            {
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
            }
          ]
        },
        {
          id: 2,
          title: "Lesson 2: 核心概念 (Core Concepts)",
          desc: "Autodesk Revit 族系统、多学科共享坐标系与三维扫描对齐",
          questions: [
            {
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
            }
          ]
        },
        {
          id: 3,
          title: "Lesson 3: 实操避坑 (Common Pitfalls)",
          desc: "Navisworks 碰撞检测、IFC 格式导出设置与 4D/5D 工程模拟",
          questions: [
            {
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
          title: "Lesson 1: 热身测验 (Warmup)",
          desc: "MCAD 几何约束意图、SOLIDWORKS 配置管理与 PDM 版本控制",
          questions: [
            {
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
              nodeId: "solidworks",
              slug: "solidworks",
              question: "In SOLIDWORKS, when you need to create multiple physical variations of a part (such as a screw with different lengths) in a single file, what feature should you deploy?",
              options: [
                "Configurations Manager",
                "Command Alias (PGP)",
                "External Reference links",
                "Plot CTB Style scales"
              ],
              correctIdx: 0,
              why: "Configurations in SOLIDWORKS manage part dimensions, suppressed states, and metadata variables, letting a designer keep a whole product family in one source file.",
              pitfall: "Suppressing features in configurations can sometimes break child dependencies. Carefully check downstream features when adding variations."
            },
            {
              nodeId: "parametrics",
              slug: "product-data-management",
              question: "In Product Data Management (PDM) version control, what represents the primary difference between checking out and checking in a part file?",
              options: [
                "Check-out locks the file for editing by the user; Check-in releases the lock and saves a new version to the vault.",
                "Check-out exports the model to 2D paper sheets; Check-in compiles sheet scales to PDF.",
                "Check-out deletes the local workspace; Check-in creates online database backups.",
                "Check-out runs FEA structural tests; Check-in runs CNC toolpath codes."
              ],
              correctIdx: 0,
              why: "PDM vaulting prevents multiple designers from overwriting the same assembly file concurrently by locking files during edit cycles.",
              pitfall: "Never work on assembly files locally outside the PDM workflow; it creates broken reference links and duplicates revision history."
            },
            {
              nodeId: "parametrics",
              slug: "gd-t-tolerances",
              question: "What represents the core advantage of Geometric Dimensioning and Tolerancing (GD&T) according to ASME Y14.5 compared to coordinate tolerance?",
              options: [
                "It uses cylindrical tolerance zones to capture true functional mating clearance, saving cost by expanding scrap limits.",
                "It automatically draws auxiliary views for paper drafting packages.",
                "It limits geometry design to flat orthogonal planes.",
                "It encrypts solid model geometry so competitors cannot copy design configurations."
              ],
              correctIdx: 0,
              why: "GD&T focuses on functional mating interfaces (like datums and MMC). Cylindrical tolerance zones offer 57% more tolerance area than old coordinate square zones.",
              pitfall: "Avoid over-specifying tight location tolerances on non-mating features; this increases manufacturing inspection costs with zero benefit."
            }
          ]
        },
        {
          id: 2,
          title: "Lesson 2: 核心概念 (Core Concepts)",
          desc: "B-Rep 拓扑边界表达、三维装配自由度约束与 FEA 有限元分析网格收敛",
          questions: [
            {
              nodeId: "brep",
              slug: "intelligent-objects",
              question: "MCAD systems primarily represent solid geometry using B-Rep (Boundary Representation). What represents the core mathematical model of B-Rep?",
              options: [
                "Defining models using a dense cloud of coordinate points captured by lasers.",
                "Defining models via topological elements (vertices, edges, faces) bounded by mathematical surfaces.",
                "Approximating solid shapes using thousands of flat triangular pixels (STL mesh).",
                "Using static image arrays to paint simulated highlights on flat drawings."
              ],
              correctIdx: 1,
              why: "B-Rep represents solids by defining their boundaries. Faces, edges, and vertices connect topologically, backed by exact CAD math (NURBS, analytic planes).",
              pitfall: "Operations that create 'zero-thickness geometry' violate B-Rep topology rules, causing boolean unions and extrudes to fail."
            },
            {
              nodeId: "assembly",
              slug: "skeleton-creo",
              question: "When designing assemblies in mechanical CAD, what is the primary role of assembly mates / constraints?",
              options: [
                "To calculate the manufacturing price of steel raw materials based on weight.",
                "To constrain the relative degrees of freedom between component coordinate coordinate planes.",
                "To automatically record custom macro scripts for drawing layout plots.",
                "To check if the spelling of coordinate labels matches standard ISO terms."
              ],
              correctIdx: 1,
              why: "Mates align parts together in 3D assembly coordinates by locking mechanical degrees of freedom (e.g. coaxial shafts, coincident faces).",
              pitfall: "Mating to chamfers or draft angles can cause mate solver failures when part dimensions shift. Prefer mating to primary reference planes."
            },
            {
              nodeId: "parametrics",
              slug: "finite-element-analysis",
              question: "In Finite Element Analysis (FEA), what represents the primary purpose of conducting a 'Mesh Convergence Study'?",
              options: [
                "To verify that stress results are independent of element size by refining the mesh until results stabilize.",
                "To test if the CAD workstation has sufficient graphics cards to run fluid animations.",
                "To convert B-Rep solid models into simple flat drawing viewports.",
                "To check if material price estimates match the factory inventory database."
              ],
              correctIdx: 0,
              why: "Mesh convergence ensures that your FEA mathematical solution has stabilized and is not displaying artificial stresses caused by coarse mesh elements.",
              pitfall: "Do not blindly accept stress results from a single coarse default mesh; always refine mesh at critical fillet radii to check for convergence."
            }
          ]
        },
        {
          id: 3,
          title: "Lesson 3: 实操避坑 (Common Pitfalls)",
          desc: "模型定义 MBD 标准化、模具拔模检测与钣金展平 K-Factor 计算",
          questions: [
            {
              nodeId: "mbd",
              slug: "model-based-definition-solidworks",
              question: "What is the ultimate goal of adopting Model-Based Definition (MBD) in modern manufacturing?",
              options: [
                "Replacing CAD models with digital photos of hand-drawn drafting sheets.",
                "Embedding PMI (Product Manufacturing Info, GD&T) directly in the 3D model, eliminating separate 2D drawings.",
                "Training generative AI models to create CAD models without human supervision.",
                "Converting all files to HTML documents for simple browser editing."
              ],
              correctIdx: 1,
              why: "MBD makes the 3D CAD model the single source of truth. Dim, tolerances, and surface finish annotations reside inside the 3D model database for downstream CAM ingestion.",
              pitfall: "Adopting MBD requires a supplier chain capable of reading annotated 3D formats (like STEP AP242). Verify supplier capabilities before dropping 2D."
            },
            {
              nodeId: "parametrics",
              slug: "draft-angles-parting-lines",
              question: "When designing plastic injection molded parts in MCAD, why are draft angles essential on vertical faces?",
              options: [
                "To allow the solidified plastic part to eject cleanly from the mold cavity without drag marks or damage.",
                "To reduce the weight of steel material needed to build the model.",
                "To ensure the model configuration matches the 2D plot CTB layout.",
                "To force the extruder to heat raw plastic faster."
              ],
              correctIdx: 0,
              why: "Draft angles taper vertical walls so that as the mold opens, the part separates instantly from metal mold walls, preventing scraping.",
              pitfall: "Failing to check draft angles on textured surfaces will cause drag marks. Heavy textures require greater draft angles (typically 1 to 1.5 degrees per 0.02mm texture depth)."
            },
            {
              nodeId: "parametrics",
              slug: "k-factor-sheet-metal",
              question: "When designing sheet metal parts in MCAD, how does the K-Factor govern the flat pattern calculation?",
              options: [
                "It represents the ratio of the neutral sheet axis offset to the total sheet metal thickness during bending.",
                "It is a safety factor calculating load failure points in FEA stress zones.",
                "It is a scale factor adjusting print layouts to match standard paper sizes.",
                "It specifies the ratio of copper to steel used in assembly mating."
              ],
              correctIdx: 0,
              why: "K-Factor locates the neutral axis (the layer that neither stretches nor compresses during a bend), which is critical to calculate exact flat blank lengths.",
              pitfall: "Using a default K-Factor (like 0.5) for all materials and tooling will result in incorrect flat layouts. Verify actual bend deduction with shop trials."
            }
          ]
        }
      ]
    },
    civil: {
      trackTitle: "Civil Infrastructure",
      trackBadge: "🏗️ Civil",
      nodesToMaster: ["surfaces", "civil3d", "alignments", "corridors", "landxml"],
      lessons: [
        {
          id: 1,
          title: "Lesson 1: 热身测验 (Warmup)",
          desc: "TIN 地形表面模型、Civil 3D 软件架构与 COGO 点 Description Key 自动处理",
          questions: [
            {
              nodeId: "surfaces",
              slug: "surfaces-civil-3d",
              question: "In civil engineering CAD, what represents the primary geometry configuration of a TIN Surface?",
              options: [
                "A grid of horizontal contours calculated solely from PDF underlays.",
                "A network of non-overlapping triangles connecting surveyor survey points.",
                "A series of curved splines representing underground pipe trajectories.",
                "A database storing text listings of land parcel ownership records."
              ],
              correctIdx: 1,
              why: "TIN (Triangulated Irregular Network) surfaces model 3D topography by connecting coordinate points. They calculate cut/fill earthworks and model drainage paths.",
              pitfall: "Ensure breaklines are added to TIN surfaces at curbs and retaining walls, or triangulation will cut across slopes inaccurately."
            },
            {
              nodeId: "civil3d",
              slug: "civil-3d",
              question: "Autodesk Civil 3D is widely used for infrastructure design. What represents its fundamental architecture?",
              options: [
                "It is a database extension that runs in standard web browsers without local installs.",
                "It is built directly on the AutoCAD drafting engine, adding dynamic, object-oriented land objects.",
                "It is a standalone simulation engine designed to replace steel structure design.",
                "It is a lightweight drawing viewer optimized for mobile devices without edit tools."
              ],
              correctIdx: 1,
              why: "Civil 3D leverages standard DWG geometry commands but layers smart parametric civil objects (alignments, parcels, surfaces) on top of the AutoCAD core.",
              pitfall: "Civil 3D objects require specific object-enablers to display correctly when drawing files are opened in basic AutoCAD seats."
            },
            {
              nodeId: "surfaces",
              slug: "point-groups-civil",
              question: "In survey coordinate databases, what represents the primary benefit of deploying Description Key Sets?",
              options: [
                "Automatically assigning symbols, layer assignments, and label formats to COGO points upon import.",
                "Translating standard coordinate labels into alternative language files.",
                "Encrypting TIN surfaces to prevent editing by structural subconsultants.",
                "Reducing the coordinate precision of survey points to save PC memory."
              ],
              correctIdx: 0,
              why: "Description Keys read surveyor code tags (like 'LP' for Light Pole) and map them to standard symbols, scales, and layers instantly.",
              pitfall: "Failing to standardize description keys across field crews will result in manual point sorting, wasting coordinator hours."
            }
          ]
        },
        {
          id: 2,
          title: "Lesson 2: 核心概念 (Core Concepts)",
          desc: "道路平纵曲线关联设计、重力流管网规则与放坡组 (Grading Group) 动态平衡",
          questions: [
            {
              nodeId: "alignments",
              slug: "profiles-civil-3d",
              question: "What represents the difference between an Alignment and a Profile in civil design?",
              options: [
                "An alignment controls text fonts, while a profile controls printer plot scales.",
                "An alignment defines the horizontal centerline (X,Y path), while a profile defines the vertical elevation changes (Z coordinates).",
                "An alignment plots site boundaries, while a profile catalogs soil moisture tests.",
                "An alignment is used in AEC BIM, while a profile is reserved for mechanical MCAD."
              ],
              correctIdx: 1,
              why: "Alignments establish the linear trajectory of roads/pipes horizontally. Profiles show elevation grids along that alignment to design slopes and vertical curves.",
              pitfall: "Alignments and profiles are dynamically linked. Modifying horizontal alignment coordinates will automatically adjust vertical profile views."
            },
            {
              nodeId: "civil3d",
              slug: "storm-pipe-networks",
              question: "When designing gravity pipe networks in Civil 3D, what governs the slope and elevation calculation of pipes?",
              options: [
                "Rules-based profiles checking minimum/maximum cover depths and slope parameters.",
                "The rendering speed of graphics cards processing water flow animations.",
                "The absolute size of external references linked to standard sheet layouts.",
                "The coordinate projection scale adjusting UTM grids to localized paper sizes."
              ],
              correctIdx: 0,
              why: "Civil gravity networks use design rules to verify that pipe slopes stay within limits and that vertical clearance depths below surfaces are satisfied.",
              pitfall: "Double-check structure connection offsets; if structure depths are set too shallow, pipes will project above ground contours."
            },
            {
              nodeId: "surfaces",
              slug: "grading-groups-civil",
              question: "In Civil site modeling, how does a Grading Group dynamically compute cut and fill earthworks?",
              options: [
                "It projects dynamic slope slopes from feature lines to target a surface, calculating volume balances.",
                "It automatically prints sheet layouts for surveyor field handoffs.",
                "It runs traffic simulation scenes to verify road alignment lanes.",
                "It translates coordinate points into simple contour line drawings."
              ],
              correctIdx: 0,
              why: "Grading Groups project slopes (e.g. 3:1 cut/fill) from a control line to meet a target surface, generating a dynamic 3D surface for volume calculation.",
              pitfall: "Ensure feature lines inside grading groups have no crossing horizontal lines, as these create modeling gaps and crash volume solvers."
            }
          ]
        },
        {
          id: 3,
          title: "Lesson 3: 实操避坑 (Common Pitfalls)",
          desc: "道路装配部件目标映射、GPS 数字化施工 LandXML 导出与土方量核算",
          questions: [
            {
              nodeId: "corridors",
              slug: "subassembly-civil-3d",
              question: "When modeling a road Corridor in Civil 3D, what three primary elements must you bring together?",
              options: [
                "Line weights, paper space sheets, and printer CTB configurations.",
                "A horizontal alignment, a vertical profile, and a cross-section assembly.",
                "A site parcel layout, an IFC file, and a database of material costs.",
                "A point cloud scan, a structural FEA grid, and a PDF coordinate underlay."
              ],
              correctIdx: 1,
              why: "Corridors sweep a dynamic cross-section (assembly) along a horizontal track (alignment) and vertical guideline (profile), calculating precise daylighting and earthworks.",
              pitfall: "If corridor parameters are not set with correct targets (e.g. targeting the existing surface), grading slopes won't daylight correctly."
            },
            {
              nodeId: "landxml",
              slug: "pressure-networks-civil-3d",
              question: "How does exporting site data to LandXML format help in the site construction phase?",
              options: [
                "It automatically registers drawings with state land coordinate databases.",
                "It translates surfaces and alignments to GPS-guided machine grading equipment directly on site.",
                "It compresses drawing images so they can be sent via text messages.",
                "It converts all 3D geometry into simple spreadsheets for tax audits."
              ],
              correctIdx: 1,
              why: "LandXML is a lightweight open standard. It permits surveyors and machine operators to transfer coordinate paths and terrains straight to machinery control cabinets.",
              pitfall: "Verify coordinate projections (UTM, state planes) before exporting LandXML; wrong scale scale parameters will offset machinery positions."
            },
            {
              nodeId: "alignments",
              slug: "average-end-area-earthworks",
              question: "How is the Average End Area method used to estimate road corridor volumes?",
              options: [
                "It averages the cross-sectional cut/fill areas of adjacent stations and multiplies by the distance between them.",
                "It averages the elevation heights of TIN surfaces inside site parcels.",
                "It counts the number of surveyor survey coordinate points inside a grid.",
                "It divides the total LandXML file size by the corridor centerline length."
              ],
              correctIdx: 0,
              why: "This standard method interpolates volume between design stations. Volume = (Area1 + Area2) / 2 * Distance.",
              pitfall: "Average End Area overestimate volume along sharp curves. Use composite surface volume checks for high-accuracy payouts."
            }
          ]
        }
      ]
    },
    draft: {
      trackTitle: "2D Drafting Specialist",
      trackBadge: "📐 2D Draft",
      nodesToMaster: ["layer", "xref", "alias", "plot", "merge"],
      lessons: [
        {
          id: 1,
          title: "Lesson 1: 热身测验 (Warmup)",
          desc: "2D 图层状态管理、PGP 快捷键命令别名与 AutoLISP 脚本自动定制",
          questions: [
            {
              nodeId: "layer",
              slug: "layer",
              question: "In native DWG systems (like AutoCAD/GstarCAD), what represents the utility of Layer States?",
              options: [
                "To trace lines automatically from scanned PDF drawings.",
                "To save and instantly toggle color, linetype, and visibility properties of layers.",
                "To monitor the memory consumption of system variable files.",
                "To export the drawing direct to steel manufacture systems."
              ],
              correctIdx: 1,
              why: "Layer States save current layer status configurations. This lets designers switch between viewing electrical layouts, HVAC lines, or base architectural walls with one click.",
              pitfall: "Layer States capture snapshot settings. If you add new layers later, make sure to update your saved Layer States to manage their visibility."
            },
            {
              nodeId: "alias",
              slug: "command-alias",
              question: "What is a command alias (configured via acad.pgp or gcad.pgp) in classic CAD drafting?",
              options: [
                "An alternative name for a CAD seat license assigned to a user.",
                "A keyboard shortcut (like 'L' for LINE) that lets draftsmen launch commands from the console.",
                "A coordinate point offset parameter used during circular arrays.",
                "A security encryption key used to protect coordinate databases."
              ],
              correctIdx: 1,
              why: "Aliases enable high-speed keyboard input. Professional draftsmen rely on muscle memory and keyboard shortcut commands to minimize viewport mouse navigation.",
              pitfall: "When migrating to alternative CAD platforms, export and map your custom PGP file to preserve your productivity shortcuts."
            },
            {
              nodeId: "alias",
              slug: "autolisp-scripts",
              question: "What represents the primary power of writing AutoLISP scripts (.lsp) in native CAD drafting workflows?",
              options: [
                "Automating repetitive drafting actions and geometry creation by executing custom CAD command scripts.",
                "Increasing the rendering resolution of 3D solids inside viewports.",
                "Translating drawing text blocks into alternative international languages.",
                "Encrypting drawings so only registered site owners can open them."
              ],
              correctIdx: 0,
              why: "LISP allows draftsmen to write custom macros and shortcuts, interacting directly with the CAD drawing database to streamline production tasks.",
              pitfall: "Always test LISP commands in clean viewports; poorly written LISP routines can freeze drawing sessions and cause unsaved data loss."
            }
          ]
        },
        {
          id: 2,
          title: "Lesson 2: 核心概念 (Core Concepts)",
          desc: "外部参照 Xref 协同管理、图纸视口比例打印与动态块参数设计",
          questions: [
            {
              nodeId: "xref",
              slug: "xref",
              question: "What is the key technical difference between inserting an External Reference (Xref) and inserting a Block in a drawing?",
              options: [
                "Blocks can handle color parameters, whereas Xrefs are strictly monochrome.",
                "Blocks embed geometry databases directly inside the drawing, while Xrefs link to external files, keeping files lightweight and collaborative.",
                "Xrefs are only used on mobile viewer apps, whereas Blocks require desktop CAD.",
                "Xrefs can run automated LISP scripts, while Blocks are purely static shapes."
              ],
              correctIdx: 1,
              why: "Xrefs reference external files dynamically. When the external file changes, the changes automatically show in the master drawing. Blocks merge geometry permanently.",
              pitfall: "Relative paths are preferred for Xrefs. Absolute paths will break when files are shared or moved to different servers."
            },
            {
              nodeId: "plot",
              slug: "plot-style",
              question: "What is the difference between Model Space and Paper Space in classic CAD layout design?",
              options: [
                "Model Space is used in AEC coordination, whereas Paper Space is strictly for MCAD.",
                "Model Space is where you draw the 1:1 scale geometries, and Paper Space layouts are used to scale, annotate, and print sheets.",
                "Model Space limits drawing to 2D lines, while Paper Space supports 3D parametric solids.",
                "Model Space is saved locally, while Paper Space layouts require cloud database syncing."
              ],
              correctIdx: 1,
              why: "Draw once at full scale in Model Space. Then create Paper Space layouts to manage scale viewports, add border templates, and set up print plot scaling.",
              pitfall: "Never draw primary geometry inside Paper Space layouts. Keep geometry in Model Space and use viewports to look at it."
            },
            {
              nodeId: "alias",
              slug: "dynamic-blocks",
              question: "What is the key structural benefit of defining Dynamic Blocks in 2D design libraries?",
              options: [
                "Adding custom parameters (Linear, Lookup) and actions (Stretch, Array) so a single block can adjust geometry dynamically.",
                "Connecting the drawing coordinate system directly to active GPS satellites.",
                "Enabling the block to run structural FEA simulations in paper space layouts.",
                "Compressing file size so DWG drawings can be read on basic mobile viewers."
              ],
              correctIdx: 0,
              why: "Dynamic blocks consolidate CAD libraries. A single door block can stretch, mirror, and scale to dozens of sizes, replacing hundreds of static blocks.",
              pitfall: "Overloading a single block with too many overlapping actions makes editing complex. Keep dynamic behaviors focused and clean."
            }
          ]
        },
        {
          id: 3,
          title: "Lesson 3: 实操避坑 (Common Pitfalls)",
          desc: "DWG 图纸版本图层差异比对、多视口下注释性比例 (Annotative) 缩放与冲突消解",
          questions: [
            {
              nodeId: "merge",
              slug: "drawing-merge",
              question: "When using DWG Compare in GstarCAD / AutoCAD, how does the rendering screen display differences?",
              options: [
                "It automatically repairs all coordinate alignment errors without user input.",
                "It overlays the two drawing versions in a unified viewport, using distinct colors to show additions, deletions, and unchanged items.",
                "It lists coordinate differences as a text table of math formulas.",
                "It turns off all layers except the coordinate differences."
              ],
              correctIdx: 1,
              why: "DWG Compare runs differences checking on entities. By color-coding version changes, reviewers quickly audit what background wall lines or coordinate references moved.",
              pitfall: "Proxy objects and custom third-party objects may fail to diff cleanly. Explode or bind external coordinate objects prior to comparison."
            },
            {
              nodeId: "alias",
              slug: "annotative-scaling",
              question: "Why is setting text and dimensions to 'Annotative' preferred in multi-scale layouts?",
              options: [
                "It automatically scales text heights and dimension labels to display consistently across viewports of different scales.",
                "It translates all drawing labels into standard coordinates for CNC.",
                "It encrypts drawing annotations to prevent layout edits.",
                "It enables rendering engines to compile auxiliary viewport lines."
              ],
              correctIdx: 0,
              why: "Annotative objects automatically scale their heights according to viewport scales (e.g. 1:50 vs 1:100), ensuring paper printed text remains readable.",
              pitfall: "Ensure you add the relevant annotation scales to objects before plotting, or the text might vanish in specific viewports."
            }
          ]
        }
      ]
    },
    placement: {
      trackTitle: "Placement Test",
      trackBadge: "🏆 Placement",
      nodesToMaster: [],
      drawCount: 10,
      questions: [
        {
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
          nodeId: "placement",
          slug: "placement-draft-xrefs",
          question: "Why is referencing drawings via Xrefs (External References) preferred over copying static blocks in multi-designer floor layouts?",
          options: [
            "Xrefs reference external files dynamically, ensuring background changes are updated automatically while keeping the master file size lightweight.",
            "Xrefs support custom colors, whereas blocks are strictly monochrome.",
            "Xrefs permit scripts automation, while blocks are static drawing shapes.",
            "Xrefs are optimized for browser viewers, whereas blocks require desktop seats."
          ],
          correctIdx: 0,
          why: "Xrefs enable real-time collaboration. When the architect moves a wall in the base plan, the structural engineer sees it immediately without importing files.",
          pitfall: "Prefer relative path references for Xrefs. Absolute paths will break when files are migrated to cloud servers or shared with clients."
        },
        {
          nodeId: "placement",
          slug: "placement-draft-spaces",
          question: "What represents the golden rule for separating Model Space and Paper Space in classic 2D CAD production?",
          options: [
            "Drawing all design geometry at 1:1 scale in Model Space, and using Viewports in Paper Space to organize annotation tags and print sheet layouts.",
            "Using Model Space strictly for BIM coordination, while Paper Space is reserved for MCAD layouts.",
            "Drafting only 3D solids in Model Space, while 2D lines are drawn in Paper Space.",
            "Saving Model Space on local hard drives, while Paper Space layouts require cloud servers."
          ],
          correctIdx: 0,
          why: "Model Space is the infinite virtual drafting room. Paper space layouts contain standard borders and use viewports to frame and scale the drawing for plots.",
          pitfall: "Never draw building geometry in Paper Space layouts; this detaches details from coordinates, ruining coordinates alignment."
        },
        {
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
  };

  // 2. 状态机与游戏数据初始化
  let state = {
    activeTrack: "",
    activeLessonId: null, // 当前小课 ID (1, 2, 3)，如果是定级测试则为 null
    questions: [],
    currentIndex: 0,
    hearts: 3,
    xpTotal: 0,
    perfectRun: true,
    selectedOptionIdx: -1,
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
      unitSubtitleEl.textContent = "依次完成以下小课以解锁该职业路径的技能树节点并获取经验值！";
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
        statusTagHtml = `<span class="lesson-status-tag completed">已通关 ✅</span>`;
        buttonText = "重新挑战";
        buttonClass = "btn";
      } else if (status === "active") {
        statusTagHtml = `<span class="lesson-status-tag active">可开始 🟢</span>`;
        buttonText = "开始挑战";
        buttonClass = "btn btn-primary";
      } else {
        statusTagHtml = `<span class="lesson-status-tag locked">已锁闭 🔒</span>`;
        buttonText = "已锁闭 🔒";
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

    if (trackParam && QUIZ_DATABASE[trackParam]) {
      if (trackParam === "placement") {
        startQuiz("placement");
      } else {
        if (lessonParam) {
          const lessonId = parseInt(lessonParam, 10);
          if ([1, 2, 3].includes(lessonId)) {
            if (isLessonUnlocked(trackParam, lessonId)) {
              startQuiz(trackParam, lessonId);
            } else {
              window.location.href = `quiz.html?track=${trackParam}`;
            }
          } else {
            window.location.href = `quiz.html?track=${trackParam}`;
          }
        } else {
          showLessonsScreen(trackParam);
        }
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
    
    // 初始化/更新进度管家数据
    updateBackupManager();
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
    statStreakEl.textContent = `🔥 ${streak} 天`;
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
              showBackupMessage("📋 进度恢复码已成功复制到剪贴板！请妥善保存。", "success");
            }).catch(() => {
              // 兼容方案
              codeInput.select();
              document.execCommand("copy");
              showBackupMessage("📋 进度恢复码已选择并复制！", "success");
            });
          }
        });
      }

      // 导入按钮
      if (btnImport) {
        btnImport.addEventListener("click", () => {
          const rawCode = importInput.value.trim();
          if (!rawCode) {
            showBackupMessage("❌ 请先输入有效的进度恢复码。", "error");
            return;
          }

          try {
            // 解密 Base64
            const jsonStr = decodeURIComponent(escape(atob(rawCode)));
            const parsed = JSON.parse(jsonStr);

            // 基础校验
            if (!parsed || parsed.version !== 1 || !parsed.data) {
              showBackupMessage("❌ 无效的恢复码，版本不匹配或格式有误。", "error");
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

            showBackupMessage("🎉 进度恢复成功！页面即将刷新加载最新数据...", "success");
            
            // 延迟刷新
            setTimeout(() => {
              location.reload();
            }, 1500);

          } catch (err) {
            showBackupMessage("❌ 还原失败，恢复码无效或已损坏，请确保复制完整。", "error");
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
        question: q.question,
        options: [...q.options],
        correctIdx: q.correctIdx,
        why: q.why,
        pitfall: q.pitfall
      };

      // 3. 对这道题目的选项进行随机打乱，并重写正确答案索引
      const correctText = qCopy.options[qCopy.correctIdx];
      qCopy.options = shuffleArray([...qCopy.options]);
      qCopy.correctIdx = qCopy.options.indexOf(correctText);

      return qCopy;
    });

    state.currentIndex = 0;
    state.hearts = 3;
    state.xpTotal = 0;
    state.perfectRun = true;
    state.selectedOptionIdx = -1;

    if (selectionScreen) selectionScreen.style.display = "none";
    if (lessonsScreen) lessonsScreen.style.display = "none";
    if (activeScreen) activeScreen.style.display = "block";
    if (resultScreen) resultScreen.style.display = "none";

    if (trackBadge) {
      if (trackKey === "placement") {
        trackBadge.textContent = track.trackBadge;
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

    // Build Options
    q.options.forEach((opt, idx) => {
      const keys = ["A", "B", "C", "D"];
      const btn = document.createElement("button");
      btn.className = "quiz-option-btn";
      btn.type = "button";
      btn.innerHTML = `
        <span class="quiz-option-key">${keys[idx]}</span>
        <span class="quiz-option-text">${opt}</span>
      `;

      btn.addEventListener("click", () => {
        if (state.selectedOptionIdx !== -1) return; // Answer locked
        selectOption(idx, btn);
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
        fTitle.textContent = "定级未通过";
        fTitle.style.color = "#ef4444";
      }
      if (fMeta) {
        fMeta.textContent = "您在定级测试中生命值耗尽，或者正确率未达到 80%。别灰心！从基础单项测验开始，能帮您快速查漏补缺。";
      }
      if (fBtn) {
        fBtn.textContent = "🔁 重新定级测试";
      }
      if (failureSecondaryBtn) {
        failureSecondaryBtn.textContent = "📚 浏览 Wiki";
        failureSecondaryBtn.href = "knowledge-base.html";
      }
    } else {
      // 恢复普通失败文案
      const fTitle = failureView.querySelector('.hero-title');
      const fMeta = failureView.querySelector('.meta');
      const fBtn = failureView.querySelector('button');
      if (fTitle) {
        fTitle.textContent = "挑战失败";
        fTitle.style.color = "#ef4444";
      }
      if (fMeta) {
        fMeta.textContent = "您在本次挑战中生命值已耗尽。没关系，多在 Wiki 中学习原子概念，下次一定能成功！";
      }
      if (fBtn) {
        fBtn.textContent = "🔁 重新开始本课";
      }
      if (failureSecondaryBtn) {
        failureSecondaryBtn.textContent = "📋 返回关卡中心";
        failureSecondaryBtn.href = `?track=${state.activeTrack}`;
      }
    }
  }

  // 显示挑战成功结算卡片并写 LocalStorage
  function showSuccessScreen() {
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
        sTitle.textContent = "定级通关成功！";
        sTitle.style.color = "#ca8a04";
      }
      if (sMetaList && sMetaList[0]) {
        sMetaList[0].textContent = "太棒了！您成功通过了综合入学定级测验，证明了自己深厚的 CAD 实战经验。";
      }
      if (sMetaList && sMetaList[1]) {
        sMetaList[1].innerHTML = "🎯 <strong>路线图点亮：</strong> 恭喜！全站所有 4 大职业路径共 20 个技能节点已被全部同步点亮！";
      }

      if (successPrimaryBtn) {
        successPrimaryBtn.textContent = "🗺️ 查看技能地图";
        successPrimaryBtn.href = "knowledge-roadmap.html";
      }
      if (successSecondaryBtn) {
        successSecondaryBtn.textContent = "🔄 挑战其他职业路径";
        successSecondaryBtn.href = "quiz.html";
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
          sTitle.textContent = "单元通关成功！";
          sTitle.style.color = "#10b981";
        }
        if (sMetaList && sMetaList[0]) {
          sMetaList[0].textContent = `恭喜！您已成功通关 ${track.trackTitle} 的全部课程！`;
        }
        if (sMetaList && sMetaList[1]) {
          sMetaList[1].innerHTML = "🎯 <strong>技能树已点亮：</strong> 恭喜！本单元在技能地图上的 5 个核心节点已被全部点亮，并同步更新至您的 Wiki 概念库中！";
        }

        if (successPrimaryBtn) {
          successPrimaryBtn.textContent = "🗺️ 查看技能地图";
          successPrimaryBtn.href = "knowledge-roadmap.html";
        }
        if (successSecondaryBtn) {
          successSecondaryBtn.textContent = "🔄 挑战其他职业路径";
          successSecondaryBtn.href = "quiz.html";
        }
      } else {
        // Lesson 1 或 2 通关
        if (sTitle) {
          sTitle.textContent = "小课挑战成功！";
          sTitle.style.color = "#10b981";
        }
        if (sMetaList && sMetaList[0]) {
          sMetaList[0].textContent = `恭喜通关 ${lesson.title}！您已经掌握了本小课的核心概念。`;
        }
        if (sMetaList && sMetaList[1]) {
          sMetaList[1].innerHTML = "🎯 <strong>下一课已解锁：</strong> 继续挑战下一课，完整通关本单元以点亮技能树！";
        }

        if (successPrimaryBtn) {
          successPrimaryBtn.textContent = "➡️ 继续下一课";
          successPrimaryBtn.href = `?track=${state.activeTrack}&lesson=${state.activeLessonId + 1}`;
        }
        if (successSecondaryBtn) {
          successSecondaryBtn.textContent = "📋 返回关卡中心";
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

  // Hook initial boot
  init();

})();
