#!/usr/bin/env python3
"""Expand quiz.js by adding Lessons 4 and 5 to each of the 6 career tracks,
   plus a difficulty field to all questions (existing and new).
"""
import re

# New lessons to insert for each track
NEW_LESSONS = {
    "bim": [
        {
            "id": 4,
            "title": "Lesson 4: Advanced Coordination",
            "desc": "Federated Models, Level of Information Need, & Digital Twin Handover",
            "questions": [
                {
                    "type": "single",
                    "nodeId": "bim",
                    "slug": "federated-model-concept",
                    "difficulty": "intermediate",
                    "question": "What distinguishes a 'federated model' from a single integrated BIM file in multi-discipline projects?",
                    "options": [
                        "A federated model overlays separate discipline-specific files (Arch, Struct, MEP) in a viewer without merging them into one editable database.",
                        "A federated model merges all disciplines into one Revit file editable by everyone simultaneously.",
                        "A federated model is a 2D PDF overlay of scanned architectural blueprints.",
                        "Federation refers to printing multiple sets of drawings and stapling them together."
                    ],
                    "correctIdx": 0,
                    "why": "Federation keeps each discipline's model authoritative and independent. Navisworks, Solibri, or BIMcollab Zoom combine them for coordination without data loss.",
                    "pitfall": "Never try to combine all disciplines into one working file. This causes file corruption, worksharing conflicts, and ownership confusion."
                },
                {
                    "type": "single",
                    "nodeId": "bim",
                    "slug": "loin-iso-7817",
                    "difficulty": "advanced",
                    "question": "Under ISO 19650 / ISO 7817, what does 'Level of Information Need' (LOIN) replace in modern BIM specifications?",
                    "options": [
                        "LOIN replaces the ambiguous LOD scale by explicitly defining required geometry detail, alphanumeric data, and documentation for each deliverable purpose.",
                        "LOIN replaces the project schedule Gantt chart with a new timeline format.",
                        "LOIN eliminates the need for IFC data exchange between BIM platforms.",
                        "LOIN replaces building codes with a single international regulation."
                    ],
                    "correctIdx": 0,
                    "why": "LOIN separates geometric detail, information (data properties), and documentation needs per purpose, avoiding the one-number-fits-all confusion of LOD 100-500.",
                    "pitfall": "LOIN must be defined per information delivery milestone and purpose. Requesting maximum LOIN globally wastes modeling effort on elements not yet relevant."
                },
                {
                    "type": "single",
                    "nodeId": "ifc",
                    "slug": "ifc4-vs-ifc2x3",
                    "difficulty": "intermediate",
                    "question": "What is the primary technical improvement of IFC4 over IFC2x3 for model exchange?",
                    "options": [
                        "IFC4 adds parametric geometry representation (CSG trees, swept solids), improved property set definitions, and MVD (Model View Definition) certification framework.",
                        "IFC4 reduces file size by converting all geometry to JPEG images.",
                        "IFC4 removes support for MEP systems to simplify the schema.",
                        "IFC4 only works with Autodesk products while IFC2x3 is vendor-neutral."
                    ],
                    "correctIdx": 0,
                    "why": "IFC4 enables richer geometry transfer (tessellated + CSG + swept), better property inheritance, and certifiable MVDs (Reference View, Design Transfer View).",
                    "pitfall": "Not all BIM software fully supports IFC4 export. Verify receiver software compatibility before switching from IFC2x3 Coordination View 2.0."
                },
                {
                    "type": "single",
                    "nodeId": "clash",
                    "slug": "clash-tolerance-zones",
                    "difficulty": "advanced",
                    "question": "When setting up clash detection in Navisworks, why is defining tolerance zones (clearance values) per discipline pairing essential?",
                    "options": [
                        "Different systems require different minimum clearances (e.g., 150mm around hot pipes, 50mm for cable trays, 25mm for structural), so one global tolerance creates false positives or misses real conflicts.",
                        "Tolerance zones make the software render clashes in different colors for aesthetic reports.",
                        "Tolerance zones are required by Navisworks licensing agreements to function.",
                        "All systems require the same 0mm tolerance because any physical overlap is unacceptable."
                    ],
                    "correctIdx": 0,
                    "why": "Maintenance access, insulation thickness, and thermal expansion require discipline-specific clearances. A hot steam pipe needs more clearance than a cold water pipe.",
                    "pitfall": "Document your tolerance rationale in the BEP. When stakeholders question why 500 'clashes' were marked approved, the tolerance documentation justifies the decision."
                },
                {
                    "type": "multiple",
                    "nodeId": "bim",
                    "slug": "digital-twin-data-sources",
                    "difficulty": "advanced",
                    "question": "Which of the following data sources feed into an operational Digital Twin after construction handover? (Select all correct)",
                    "options": [
                        "IoT sensor streams (temperature, occupancy, energy meters)",
                        "As-built BIM model geometry and asset metadata (COBie)",
                        "Maintenance management system (CMMS) work orders and schedules",
                        "The original architect's hand-sketched concept napkin drawings"
                    ],
                    "correctIndices": [0, 1, 2],
                    "why": "Digital Twins combine the as-built BIM (static geometry/data), live IoT feeds (dynamic state), and maintenance records (operational history) for facility optimization.",
                    "pitfall": "A Digital Twin without live data connections is just a 3D viewer. Ensure IoT infrastructure and API integrations are specified in the BEP from design phase."
                }
            ]
        },
        {
            "id": 5,
            "title": "Lesson 5: Quality & Compliance",
            "desc": "Model Checking, BCF Workflows, & Regulatory Compliance in BIM",
            "questions": [
                {
                    "type": "single",
                    "nodeId": "bim",
                    "slug": "solibri-rule-checking",
                    "difficulty": "intermediate",
                    "question": "What is the primary purpose of rule-based model checking tools (like Solibri Model Checker) in BIM quality assurance?",
                    "options": [
                        "Automatically validating BIM models against predefined rules (fire egress distances, accessibility compliance, naming conventions) without manual visual inspection.",
                        "Rendering photorealistic images of the building for client presentations.",
                        "Compressing BIM files to reduce server storage costs.",
                        "Converting Revit files to AutoCAD DWG format for 2D drafting teams."
                    ],
                    "correctIdx": 0,
                    "why": "Rule-based checkers encode building codes, employer requirements, and project standards into automated validation passes that catch errors humans would miss.",
                    "pitfall": "Rule sets must be configured per project. Default rulesets catch generic issues but miss project-specific requirements (client naming, room numbering, custom parameters)."
                },
                {
                    "type": "single",
                    "nodeId": "bim",
                    "slug": "bcf-issue-tracking",
                    "difficulty": "intermediate",
                    "question": "How does BCF (BIM Collaboration Format) improve coordination issue tracking compared to email or spreadsheet methods?",
                    "options": [
                        "BCF embeds viewpoint camera positions, element GUIDs, and markup annotations so issues link directly to the 3D model location, enabling precise one-click navigation to problems.",
                        "BCF compresses all project emails into a single searchable PDF document.",
                        "BCF replaces the BIM model with a simplified wireframe for faster loading.",
                        "BCF is an encrypted messaging protocol that prevents unauthorized access to project chat."
                    ],
                    "correctIdx": 0,
                    "why": "BCF topics carry spatial context (camera, selected elements, screenshots) making issues unambiguous. Any BCF-compatible tool (Solibri, Revit, BIMcollab) can open and respond.",
                    "pitfall": "Always set the 'assigned to' field and due date in BCF topics. Unassigned issues get lost in large projects with hundreds of open coordination items."
                },
                {
                    "type": "single",
                    "nodeId": "revit",
                    "slug": "workset-best-practices",
                    "difficulty": "intermediate",
                    "question": "In Revit worksharing, what is the recommended strategy for organizing worksets in a multi-user central model?",
                    "options": [
                        "Organize worksets by building system (Exterior Shell, Interior Partitions, MEP, Structure, Site) so teams can take ownership of logical groupings without blocking others.",
                        "Create one workset per user so each person's elements are isolated.",
                        "Put all elements in a single workset and rely on element-level checkout for control.",
                        "Create worksets by floor level only, ignoring discipline separation."
                    ],
                    "correctIdx": 0,
                    "why": "System-based worksets let teams selectively close (unload) other disciplines for performance while maintaining clear ownership boundaries for synchronized editing.",
                    "pitfall": "Never put Levels, Grids, or Shared Coordinates in a user-owned workset. These project-wide datums must always be available to all team members."
                },
                {
                    "type": "multiple",
                    "nodeId": "bim",
                    "slug": "bim-regulatory-compliance",
                    "difficulty": "advanced",
                    "question": "Which of the following building compliance checks can be automated through BIM model rule validation? (Select all correct)",
                    "options": [
                        "Fire egress distance and corridor width verification",
                        "Accessibility (ADA/DDA) door width and ramp gradient checks",
                        "Structural load-bearing capacity calculations (requires separate FEA)",
                        "Room area minimum requirements per building code occupancy type"
                    ],
                    "correctIndices": [0, 1, 3],
                    "why": "Geometric checks (distances, widths, areas, slopes) can be automated from BIM data. Structural capacity requires separate engineering analysis software.",
                    "pitfall": "Model checking validates geometry and metadata, not engineering. A room that meets area requirements may still fail structurally. Always pair BIM checks with engineering sign-off."
                },
                {
                    "type": "single",
                    "nodeId": "shared-coords",
                    "slug": "point-cloud-registration",
                    "difficulty": "advanced",
                    "question": "When registering multiple point cloud scans into a unified coordinate system, what does 'target-based registration' provide over 'cloud-to-cloud' registration?",
                    "options": [
                        "Surveyed targets with known coordinates provide absolute accuracy referenced to the project coordinate system, while cloud-to-cloud only achieves relative alignment between scans.",
                        "Target-based registration is faster because it processes fewer data points.",
                        "Cloud-to-cloud registration requires special hardware that target-based does not.",
                        "Target-based registration only works indoors while cloud-to-cloud works anywhere."
                    ],
                    "correctIdx": 0,
                    "why": "Surveyed targets (checkerboards/spheres) with known XYZ coordinates tie the point cloud to the project datum. Without targets, scans align to each other but may drift from true coordinates.",
                    "pitfall": "Place registration targets with clear sight lines from multiple scan positions. Targets visible from only one scan position cannot contribute to registration accuracy."
                }
            ]
        }
    ],
    "mcad": [
        {
            "id": 4,
            "title": "Lesson 4: Manufacturing Integration",
            "desc": "Sheet Metal Design, Weldments, & DFM Analysis",
            "questions": [
                {
                    "type": "single",
                    "nodeId": "solidworks",
                    "slug": "sheet-metal-bend-relief",
                    "difficulty": "intermediate",
                    "question": "In SOLIDWORKS sheet metal design, what is the purpose of 'bend relief' cuts at the junction of bends and flat faces?",
                    "options": [
                        "Bend reliefs prevent material tearing and cracking at the intersection of a bend and an adjacent flat region by providing a controlled stress relief notch.",
                        "Bend reliefs increase the visual appeal of the final painted product.",
                        "Bend reliefs reduce the weight of the sheet metal part for aerospace applications.",
                        "Bend reliefs allow laser cutting machines to operate at higher speeds."
                    ],
                    "correctIdx": 0,
                    "why": "Without relief cuts, the material at bend-to-flat transitions experiences uncontrolled deformation, causing tears in ductile metals and cracks in brittle ones.",
                    "pitfall": "Match relief type (rectangular, obround, tear) to your fabrication shop's capabilities. Some shops cannot produce obround reliefs with basic press brakes."
                },
                {
                    "type": "single",
                    "nodeId": "solidworks",
                    "slug": "weldment-profiles",
                    "difficulty": "intermediate",
                    "question": "In SOLIDWORKS Weldments, what is the role of 'structural member profiles' when building welded frame structures?",
                    "options": [
                        "Profiles are 2D cross-sections (I-beam, C-channel, tube, angle) swept along 3D sketch paths to generate structural members with correct material properties.",
                        "Profiles are rendering textures applied to solid bodies for photorealistic visualization.",
                        "Profiles define the chemical composition of welding rod filler materials.",
                        "Profiles set the machine feed rate for CNC cutting operations."
                    ],
                    "correctIdx": 0,
                    "why": "Weldment profiles contain geometry from steel supplier catalogs (AISC, DIN, JIS). SOLIDWORKS sweeps them along skeleton paths and auto-generates trim/cope joints at intersections.",
                    "pitfall": "Verify profile dimensions match your actual supplier stock. Library profiles may differ from regional steel suppliers by 1-2mm, causing fit issues."
                },
                {
                    "type": "single",
                    "nodeId": "assembly",
                    "slug": "dfm-design-for-manufacturing",
                    "difficulty": "advanced",
                    "question": "What does SOLIDWORKS DFMXpress analyze when running a Design for Manufacturability check on a machined part?",
                    "options": [
                        "It checks for features that are difficult or impossible to machine: deep narrow slots, thin walls, sharp internal corners, inaccessible holes, and draft angles insufficient for molding.",
                        "It verifies that the part weighs less than the maximum shipping limit.",
                        "It checks that all dimensions are expressed in metric units rather than imperial.",
                        "It ensures the file size is small enough to email to suppliers."
                    ],
                    "correctIdx": 0,
                    "why": "DFMXpress flags manufacturing challenges early in design (e.g., a 2mm-wide 50mm-deep slot requires special EDM tooling). Catching these before shop drawings saves rework costs.",
                    "pitfall": "DFMXpress uses generic rules. For specialized processes (5-axis machining, Swiss-type turning), configure custom rules or consult your machinist directly."
                },
                {
                    "type": "multiple",
                    "nodeId": "mbd",
                    "slug": "step-ap242-capabilities",
                    "difficulty": "advanced",
                    "question": "Which of the following data types can STEP AP242 carry that STEP AP203/AP214 cannot? (Select all correct)",
                    "options": [
                        "3D PMI annotations (GD&T semantic data attached to geometry)",
                        "Tessellated (mesh) geometry alongside exact B-Rep",
                        "Saved viewpoints and cross-section definitions for PMI consumption",
                        "Complete project email archives and meeting minutes"
                    ],
                    "correctIndices": [0, 1, 2],
                    "why": "AP242 extends STEP for MBD workflows: semantic PMI, tessellated representations for visualization, and saved views. Earlier APs carry only geometry and basic metadata.",
                    "pitfall": "Not all CAM/CMM software reads AP242 PMI semantically. Verify your downstream toolchain before mandating AP242 as the only delivery format."
                },
                {
                    "type": "single",
                    "nodeId": "parametrics",
                    "slug": "global-variables-equations",
                    "difficulty": "intermediate",
                    "question": "In SOLIDWORKS, how do Global Variables and Equations improve parametric design intent?",
                    "options": [
                        "They create named parameters (e.g., 'WallThickness=3mm') that drive multiple dimensions via formulas, so changing one variable updates the entire model consistently.",
                        "They translate dimension text into different languages for international drawings.",
                        "They encrypt dimension values so competitors cannot reverse-engineer the design.",
                        "They replace the feature tree with a flat list of numerical coordinates."
                    ],
                    "correctIdx": 0,
                    "why": "Global Variables create single-source-of-truth parameters. Link cavity depth, wall thickness, and draft angle to variables so changing 'Material_Thickness' updates everything.",
                    "pitfall": "Circular references (Variable A depends on B which depends on A) cause solver failures. Map your equation dependency graph before building complex linked dimensions."
                }
            ]
        },
        {
            "id": 5,
            "title": "Lesson 5: Advanced Analysis",
            "desc": "FEA Best Practices, Fatigue Analysis, & Topology Optimization",
            "questions": [
                {
                    "type": "single",
                    "nodeId": "solidworks",
                    "slug": "fea-boundary-conditions",
                    "difficulty": "advanced",
                    "question": "Why do incorrect boundary conditions in FEA produce more dangerous errors than mesh quality issues?",
                    "options": [
                        "Boundary conditions define the physical reality (how loads enter and supports hold the part). Wrong BCs produce plausible-looking but completely wrong stress distributions that pass visual inspection.",
                        "Boundary conditions only affect rendering colors, not stress calculations.",
                        "Mesh quality always dominates accuracy regardless of boundary conditions.",
                        "Boundary conditions are optional metadata that simulation solvers ignore."
                    ],
                    "correctIdx": 0,
                    "why": "A perfectly meshed model with wrong fixtures (e.g., fixed when it should be pinned) produces incorrect stress paths. The results look legitimate but predict failure locations wrongly.",
                    "pitfall": "Always validate FEA boundary conditions against physical reality. If uncertain, run sensitivity studies: how much does stress change if a fixed support becomes a frictionless one?"
                },
                {
                    "type": "single",
                    "nodeId": "solidworks",
                    "slug": "fatigue-sn-curve",
                    "difficulty": "advanced",
                    "question": "In mechanical fatigue analysis, what does an S-N curve (Wohler curve) represent?",
                    "options": [
                        "The relationship between cyclic stress amplitude (S) and the number of cycles to failure (N), used to predict component lifespan under repeated loading.",
                        "The relationship between static stress and material density for weight optimization.",
                        "The relationship between surface roughness and cutting speed in CNC machining.",
                        "The relationship between assembly bolt torque and clamp force in fastener design."
                    ],
                    "correctIdx": 0,
                    "why": "S-N curves define material endurance limits. Below the endurance limit stress, a component theoretically survives infinite cycles. Above it, the curve predicts cycle-to-failure count.",
                    "pitfall": "S-N data from handbooks assumes polished test specimens. Real parts have surface finish, size effects, and stress concentrations that require correction factors (Marin equation)."
                },
                {
                    "type": "single",
                    "nodeId": "brep",
                    "slug": "topology-optimization-goal",
                    "difficulty": "advanced",
                    "question": "What is the primary engineering goal of topology optimization in mechanical design?",
                    "options": [
                        "Finding the optimal material distribution within a design space that minimizes weight while satisfying stress, displacement, and frequency constraints under given loads.",
                        "Optimizing the topology (network configuration) of electrical circuit board traces.",
                        "Finding the fastest CNC toolpath by optimizing tool approach angles.",
                        "Optimizing the order of features in the parametric feature tree for rebuild speed."
                    ],
                    "correctIdx": 0,
                    "why": "Topology optimization removes material from low-stress regions while preserving load paths. The result is an organic-looking structure that's lightweight yet stiff under specified loads.",
                    "pitfall": "Raw topology optimization results are rarely directly manufacturable. Post-process the organic shape into producible geometry (smooth surfaces, add draft, remove undercuts) before detailing."
                },
                {
                    "type": "multiple",
                    "nodeId": "assembly",
                    "slug": "fea-element-types",
                    "difficulty": "intermediate",
                    "question": "Which FEA element types are commonly used for structural analysis of mechanical parts? (Select all correct)",
                    "options": [
                        "Tetrahedral solid elements (for complex 3D geometry)",
                        "Shell elements (for thin-walled structures like enclosures and sheet metal)",
                        "Beam elements (for structural frames and trusses)",
                        "Pixel elements (for 2D image rendering of stress plots)"
                    ],
                    "correctIndices": [0, 1, 2],
                    "why": "Tet solids capture 3D stress states; shells are efficient for thin structures (plate bending); beams model frames. 'Pixel elements' do not exist in FEA.",
                    "pitfall": "Using solid elements on thin sheet metal (thickness < 1/10 of other dimensions) requires many through-thickness elements. Switch to shell elements for 10-100x faster solutions."
                },
                {
                    "type": "single",
                    "nodeId": "parametrics",
                    "slug": "design-study-optimization",
                    "difficulty": "intermediate",
                    "question": "In SOLIDWORKS Simulation, what does a 'Design Study' (parametric optimization) allow you to achieve?",
                    "options": [
                        "Automatically varying design dimensions within specified ranges to find the combination that minimizes weight while keeping stress below the yield limit.",
                        "Studying the visual appearance of different paint colors on the product surface.",
                        "Comparing render quality between different GPU hardware configurations.",
                        "Tracking design revision history for PDM compliance documentation."
                    ],
                    "correctIdx": 0,
                    "why": "Design Studies automate what-if analysis: define parameters (wall thickness, rib height), constraints (max stress, max deflection), and goals (minimize mass). The solver finds the optimum.",
                    "pitfall": "Design studies with too many variables (>10) and wide ranges require excessive computation. Start with sensitivity studies to identify the 3-4 most influential parameters first."
                }
            ]
        }
    ],
    "civil": [
        {
            "id": 4,
            "title": "Lesson 4: Earthwork & Utilities",
            "desc": "Grading Optimization, Pipe Networks, & Quantity Takeoff",
            "questions": [
                {
                    "type": "single",
                    "nodeId": "grading",
                    "slug": "grading-balance",
                    "difficulty": "intermediate",
                    "question": "What does 'cut-fill balance' mean in civil earthwork grading, and why is it a design optimization target?",
                    "options": [
                        "Achieving roughly equal volumes of earth excavated (cut) and earth placed (fill) minimizes hauling costs and eliminates the need to import or export soil from the site.",
                        "Cutting and filling are aesthetic landscaping terms for creating visual slopes.",
                        "Cut-fill balance means the site is perfectly flat with zero elevation change.",
                        "It refers to balancing the weight of construction equipment on both sides of the site."
                    ],
                    "correctIdx": 0,
                    "why": "Importing soil or disposing of excess is expensive. Civil designers adjust proposed grades to balance cut and fill volumes, minimizing truck haul cycles and tipping fees.",
                    "pitfall": "Balance volume alone isn't sufficient. Consider haul distance (mass-haul diagram) — balanced volumes with long haul distances can cost more than slight imbalance with short hauls."
                },
                {
                    "type": "single",
                    "nodeId": "corridor",
                    "slug": "pipe-network-design",
                    "difficulty": "intermediate",
                    "question": "In Civil 3D pipe network design, what determines the invert elevation of a gravity sewer pipe at each structure?",
                    "options": [
                        "Minimum cover depth requirements, pipe slope (gradient for self-cleansing velocity), and downstream connection point elevation — all ensuring gravity flow without pumping.",
                        "The aesthetic preference of the landscape architect for manhole positioning.",
                        "The color coding standard for different utility types.",
                        "The maximum pipe diameter available from the local supplier."
                    ],
                    "correctIdx": 0,
                    "why": "Gravity sewers must maintain minimum slope (e.g., 1:80 for 150mm pipes) for self-cleansing velocity while respecting minimum cover (e.g., 900mm) below finished ground.",
                    "pitfall": "Flat sites with long sewer runs may require deep excavation at the downstream end. Check against maximum trench depth limits and consider pump stations early in design."
                },
                {
                    "type": "single",
                    "nodeId": "terrain",
                    "slug": "volume-surface-comparison",
                    "difficulty": "intermediate",
                    "question": "In Civil 3D, how is earthwork volume calculated between an existing ground surface and a proposed design surface?",
                    "options": [
                        "Creating a 'volume surface' (TIN-to-TIN comparison) that calculates the prismoidal difference between existing and proposed triangulated surfaces across the site.",
                        "Manually counting contour lines and multiplying by a fixed depth factor.",
                        "Exporting both surfaces to Excel and subtracting cell values.",
                        "Measuring the distance between two random survey points on each surface."
                    ],
                    "correctIdx": 0,
                    "why": "Volume surfaces compare every triangle pair between the two TINs. Civil 3D computes composite volumes (average-end-area or prismoidal) and reports cut/fill per station range.",
                    "pitfall": "Volume accuracy depends on TIN density. Sparse survey points produce triangles that span real terrain undulations, underestimating actual earthwork volumes."
                },
                {
                    "type": "multiple",
                    "nodeId": "landxml",
                    "slug": "utility-design-factors",
                    "difficulty": "advanced",
                    "question": "Which factors must a civil engineer consider when designing underground utility pipe networks? (Select all correct)",
                    "options": [
                        "Minimum depth of cover to protect against traffic loading and frost penetration",
                        "Pipe gradient sufficient for self-cleansing velocity in gravity systems",
                        "Clearance separation distances between parallel utilities (gas, electric, water, sewer)",
                        "The RGB color values assigned to pipe layers in the CAD drawing"
                    ],
                    "correctIndices": [0, 1, 2],
                    "why": "Cover depth, gradient, and utility separations are engineering requirements driven by codes (ASCE, local standards). Layer colors are drafting conventions, not design constraints.",
                    "pitfall": "Always check local utility clearance requirements. National codes give minimums, but utility companies often mandate greater separations in their connection agreements."
                },
                {
                    "type": "single",
                    "nodeId": "grading",
                    "slug": "stormwater-detention-sizing",
                    "difficulty": "advanced",
                    "question": "What is the primary engineering purpose of stormwater detention basins in civil site design?",
                    "options": [
                        "Temporarily storing runoff from developed impervious surfaces and releasing it at a controlled rate that does not exceed pre-development peak flow, preventing downstream flooding.",
                        "Creating decorative ponds for aesthetic landscaping in residential developments.",
                        "Providing fire-fighting water supply reservoirs for emergency services.",
                        "Collecting sediment from construction sites during the building phase only."
                    ],
                    "correctIdx": 0,
                    "why": "Development increases impervious area (roofs, roads), accelerating runoff peaks. Detention ponds attenuate the peak by temporarily storing volume and releasing it slowly through an orifice.",
                    "pitfall": "Size detention for multiple storm return periods (2yr, 10yr, 100yr). A pond sized only for the 10-year storm may be inadequate during extreme events, causing downstream flooding."
                }
            ]
        },
        {
            "id": 5,
            "title": "Lesson 5: Data Exchange & Construction",
            "desc": "LandXML/IFC Export, Machine Control, & As-Built Documentation",
            "questions": [
                {
                    "type": "single",
                    "nodeId": "landxml",
                    "slug": "landxml-export-purpose",
                    "difficulty": "intermediate",
                    "question": "What is the primary purpose of exporting Civil 3D designs to LandXML format?",
                    "options": [
                        "Enabling vendor-neutral exchange of civil engineering data (surfaces, alignments, parcels, pipe networks) between different software platforms and machine control systems.",
                        "Compressing 3D terrain models into smaller files for email transfer.",
                        "Converting civil designs into architectural Revit building models.",
                        "Generating photorealistic renderings of road surfaces with realistic textures."
                    ],
                    "correctIdx": 0,
                    "why": "LandXML is the civil engineering equivalent of IFC. It carries alignments, profiles, cross-sections, surfaces, and parcels in a schema that other civil software (12d, Bentley) can import.",
                    "pitfall": "LandXML doesn't carry all Civil 3D data. Pipe networks, pressure networks, and some corridor subtleties may be lost or simplified in the export."
                },
                {
                    "type": "single",
                    "nodeId": "corridor",
                    "slug": "machine-control-models",
                    "difficulty": "advanced",
                    "question": "How do GNSS-based machine control systems use Civil 3D design surfaces during construction grading?",
                    "options": [
                        "The design surface is loaded into the machine's onboard computer, which compares real-time blade/bucket position (via GNSS) against the target elevation, guiding the operator to cut/fill to design grades automatically.",
                        "Machine control sends email alerts to the engineer when the machine moves.",
                        "The machine automatically downloads software updates from Civil 3D during operation.",
                        "GNSS coordinates are used only for tracking fuel consumption, not guiding earthwork."
                    ],
                    "correctIdx": 0,
                    "why": "Machine control eliminates manual grade stakes. The operator sees real-time cut/fill indicators on a cabin display, achieving design grades within ±20mm without survey crew intervention.",
                    "pitfall": "Export machine control surfaces at sufficient TIN density. Over-simplified TINs create flat triangle planes between points, causing the machine to grade incorrect intermediate elevations."
                },
                {
                    "type": "single",
                    "nodeId": "alignment",
                    "slug": "horizontal-curve-design",
                    "difficulty": "intermediate",
                    "question": "In road alignment design, what is the purpose of a transition curve (clothoid/spiral) between a straight (tangent) and a circular curve?",
                    "options": [
                        "Providing a gradual change in curvature (from zero to the circular curve radius) so drivers experience smooth lateral acceleration transition, improving safety and comfort.",
                        "Making the road alignment look more aesthetically pleasing on plan drawings.",
                        "Reducing the total length of road to save construction material costs.",
                        "Allowing vehicles to reach higher speeds in the circular curve section."
                    ],
                    "correctIdx": 0,
                    "why": "Without transitions, drivers experience a sudden lateral force change at tangent-to-curve junctions. Spirals ramp up curvature (and superelevation) gradually, matching vehicle dynamics.",
                    "pitfall": "Spiral length must match superelevation development length. If the spiral is too short, the road surface cannot transition from normal crown to full banking within the available distance."
                },
                {
                    "type": "multiple",
                    "nodeId": "terrain",
                    "slug": "as-built-survey-methods",
                    "difficulty": "intermediate",
                    "question": "Which surveying methods are commonly used to capture as-built conditions for comparison against design models? (Select all correct)",
                    "options": [
                        "Total station spot measurements at critical design points (inverts, top-of-curb, edge-of-pavement)",
                        "Terrestrial LiDAR scanning for comprehensive 3D surface capture",
                        "Drone photogrammetry for rapid large-area topographic mapping",
                        "Manual tape measurement from property boundary fences"
                    ],
                    "correctIndices": [0, 1, 2],
                    "why": "Total stations provide point accuracy at key locations; LiDAR gives dense 3D coverage; drones efficiently map large sites. Tape measurements from fences lack precision for engineering verification.",
                    "pitfall": "Choose the survey method matching required accuracy: total station for mm-precision pipe inverts, drone photogrammetry for ±30mm surface grades over large areas."
                },
                {
                    "type": "single",
                    "nodeId": "landxml",
                    "slug": "construction-staking",
                    "difficulty": "intermediate",
                    "question": "What information does a construction staking report from Civil 3D provide to field crews?",
                    "options": [
                        "Station/offset coordinates, cut/fill depths from proposed design surface, and alignment geometry data that field crews use to set grade stakes and guide earthwork operations.",
                        "Material purchase orders for concrete and asphalt suppliers.",
                        "Employee attendance records for site workers.",
                        "Weather forecasts for optimal construction scheduling."
                    ],
                    "correctIdx": 0,
                    "why": "Staking reports translate design geometry into field-usable data: station numbers, offsets from centerline, and excavation/fill depths relative to survey benchmarks.",
                    "pitfall": "Verify the report coordinate system matches field survey equipment settings. Datum mismatches between design coordinates and field instruments cause systematic elevation errors."
                }
            ]
        }
    ],
    "draft": [
        {
            "id": 4,
            "title": "Lesson 4: Automation & Standards",
            "desc": "AutoLISP Basics, Plot Styles (CTB/STB), & Drawing Standards Audit",
            "questions": [
                {
                    "type": "single",
                    "nodeId": "draft-lisp",
                    "slug": "autolisp-defun-basics",
                    "difficulty": "intermediate",
                    "question": "In AutoLISP programming for AutoCAD, what does the (defun C:MYCOMMAND () ...) syntax create?",
                    "options": [
                        "A custom AutoCAD command named MYCOMMAND that users can type at the command line, executing the LISP function body when invoked.",
                        "A system variable that permanently modifies AutoCAD's source code.",
                        "A compiled executable (.exe) file that runs outside of AutoCAD.",
                        "A macro that records mouse movements for playback in video tutorials."
                    ],
                    "correctIdx": 0,
                    "why": "The C: prefix tells AutoLISP to register the function as a command-line command. Users type MYCOMMAND at the prompt and the LISP code executes within the current drawing session.",
                    "pitfall": "LISP commands defined with C: are session-only unless loaded via acad.lsp or a startup suite. Restarting AutoCAD without auto-loading loses custom commands."
                },
                {
                    "type": "single",
                    "nodeId": "draft-plot",
                    "slug": "ctb-vs-stb-plot-styles",
                    "difficulty": "intermediate",
                    "question": "What is the fundamental difference between CTB (Color-dependent) and STB (Named) plot style tables in AutoCAD?",
                    "options": [
                        "CTB maps plot output (lineweight, screening) based on object color numbers (1-255), while STB assigns named styles independently of color, giving more flexibility.",
                        "CTB files are newer and recommended; STB is a deprecated legacy format.",
                        "CTB controls 3D rendering materials; STB controls 2D line colors.",
                        "There is no difference; they are interchangeable synonyms."
                    ],
                    "correctIdx": 0,
                    "why": "CTB forces the old convention of 'color = lineweight' (red = 0.5mm, yellow = 0.25mm). STB decouples print appearance from display color, useful for colored model-space backgrounds.",
                    "pitfall": "Converting a drawing from CTB to STB mode is irreversible per drawing. Always keep a backup before running CONVERTPSTYLES, especially on shared project files."
                },
                {
                    "type": "single",
                    "nodeId": "draft-std",
                    "slug": "cad-standards-audit",
                    "difficulty": "intermediate",
                    "question": "What does the AutoCAD STANDARDS command (CAD Standards Checker) validate in a drawing file?",
                    "options": [
                        "It compares layers, dimension styles, text styles, and linetypes in the current drawing against a standards file (.dws), flagging non-compliant deviations.",
                        "It checks that the drawing file size is below a specified maximum.",
                        "It verifies that all geometry is drawn to 1:1 scale in model space.",
                        "It validates that the license subscription is current and paid."
                    ],
                    "correctIdx": 0,
                    "why": "DWS standards files encode your office layer naming, colors, linetypes, and dimension style settings. The checker reports violations (wrong layer names, non-standard text heights).",
                    "pitfall": "Standards checking doesn't auto-fix problems. It reports violations that must be resolved manually. Run checks regularly during drafting, not just before final submission."
                },
                {
                    "type": "multiple",
                    "nodeId": "draft-lisp",
                    "slug": "autolisp-common-functions",
                    "difficulty": "advanced",
                    "question": "Which of the following are valid AutoLISP functions for interacting with drawing entities? (Select all correct)",
                    "options": [
                        "(entget ename) — retrieves the DXF data list of an entity",
                        "(ssget) — creates a selection set of entities via user pick or filter",
                        "(command \"LINE\" pt1 pt2 \"\") — executes an AutoCAD command programmatically",
                        "(compile-shader \"vertex.glsl\") — compiles GPU rendering shaders"
                    ],
                    "correctIndices": [0, 1, 2],
                    "why": "entget reads entity data, ssget builds selection sets, and (command ...) drives AutoCAD commands from LISP. GPU shader compilation is not a LISP function.",
                    "pitfall": "Using (command ...) inside event reactors or in-progress commands causes re-entrancy issues. Use (entmake) or (vla-*) methods instead for programmatic entity creation."
                },
                {
                    "type": "single",
                    "nodeId": "draft-std",
                    "slug": "template-dwt-strategy",
                    "difficulty": "beginner",
                    "question": "Why should a drafting team use a standardized DWT (drawing template) file for all new projects?",
                    "options": [
                        "DWT files pre-configure layer standards, dimension styles, text styles, title blocks, page setups, and units — ensuring every new drawing starts compliant without manual setup.",
                        "DWT files are required by AutoCAD's license agreement for commercial use.",
                        "DWT files compress drawings to reduce file size by 50%.",
                        "DWT files prevent users from creating new layers or modifying existing objects."
                    ],
                    "correctIdx": 0,
                    "why": "Templates eliminate setup repetition and enforce standards from the first keystroke. Without templates, each drafter creates different layer names and dimension styles.",
                    "pitfall": "Version-control your DWT files. When standards change (new layer naming, updated title block), distribute the updated template AND communicate changes to all team members."
                }
            ]
        },
        {
            "id": 5,
            "title": "Lesson 5: Advanced Documentation",
            "desc": "Sheet Set Manager, Fields & Attributes, & Dynamic Block Parameters",
            "questions": [
                {
                    "type": "single",
                    "nodeId": "draft-ssm",
                    "slug": "sheet-set-manager",
                    "difficulty": "intermediate",
                    "question": "What problem does Sheet Set Manager (SSM) solve for multi-drawing construction document sets in AutoCAD?",
                    "options": [
                        "SSM organizes drawings across multiple DWG files into a single project tree, automating sheet numbering, title block fields, and batch publishing without manually opening each file.",
                        "SSM merges all project drawings into one large DWG file for simpler management.",
                        "SSM is a cloud storage service for backing up AutoCAD files.",
                        "SSM converts all drawings to PDF format and deletes the original DWG files."
                    ],
                    "correctIdx": 0,
                    "why": "SSM lets you manage 200+ sheets across dozens of DWG files as one logical set. Sheet numbers, revision dates, and drawing titles auto-populate from SSM properties into title block fields.",
                    "pitfall": "SSM requires consistent layout naming and title block field definitions across all project DWG files. Retrofitting SSM onto legacy drawings without standardized title blocks fails."
                },
                {
                    "type": "single",
                    "nodeId": "draft-attr",
                    "slug": "block-attributes-extraction",
                    "difficulty": "intermediate",
                    "question": "How do block attributes enable automated data extraction (schedules, BOMs) from AutoCAD drawings?",
                    "options": [
                        "Attributes store structured text data (part number, material, cost) inside block references. DATAEXTRACTION command queries all instances and exports tabulated data to Excel or AutoCAD tables.",
                        "Attributes are visual decorations that cannot be queried or exported.",
                        "Attributes only work in 3D models, not 2D drawings.",
                        "DATAEXTRACTION reads drawing file metadata but cannot access block attribute values."
                    ],
                    "correctIdx": 0,
                    "why": "Each block instance carries attribute values (like a mini database record). DATAEXTRACTION scans all blocks matching a filter and produces a schedule without manual counting.",
                    "pitfall": "Define attribute tags consistently (PART_NO not PartNo, Part-No, etc.). Inconsistent naming prevents accurate filtering and extraction across drawing sets."
                },
                {
                    "type": "single",
                    "nodeId": "draft-dynblk",
                    "slug": "dynamic-block-visibility-states",
                    "difficulty": "advanced",
                    "question": "In AutoCAD dynamic blocks, what do 'Visibility States' allow a single block definition to achieve?",
                    "options": [
                        "Multiple visual representations (e.g., plan view, side view, simplified view) within one block, switchable via a properties dropdown without needing separate block definitions.",
                        "Animated transitions between block states for presentation purposes.",
                        "Automatic color changes based on the time of day in the drawing.",
                        "Password-protecting certain block geometries from unauthorized editing."
                    ],
                    "correctIdx": 0,
                    "why": "Visibility states pack multiple representations into one intelligent block. A door block could show: plan/elevation/3D/fire-rated variants, all switchable from the Properties palette.",
                    "pitfall": "Too many visibility states in one block bloat file size and confuse users. Limit to 5-8 meaningful states. For fundamentally different objects, use separate block definitions."
                },
                {
                    "type": "multiple",
                    "nodeId": "draft-dynblk",
                    "slug": "dynamic-block-parameters",
                    "difficulty": "advanced",
                    "question": "Which parameter types can be added to AutoCAD dynamic blocks to create intelligent, adjustable geometry? (Select all correct)",
                    "options": [
                        "Linear parameter (stretches geometry along an axis)",
                        "Rotation parameter (rotates geometry around a base point)",
                        "Lookup parameter (maps a table of preset values to other parameters)",
                        "Weather parameter (changes block appearance based on outdoor temperature)"
                    ],
                    "correctIndices": [0, 1, 2],
                    "why": "Linear, Rotation, Lookup (plus Point, Polar, Flip, Alignment, Visibility) are valid dynamic block parameters. Weather integration doesn't exist in AutoCAD blocks.",
                    "pitfall": "Always pair parameters with actions (Stretch, Move, Rotate, Scale). A parameter without an associated action does nothing when the user grips the block."
                },
                {
                    "type": "single",
                    "nodeId": "draft-std",
                    "slug": "field-codes-autocad",
                    "difficulty": "intermediate",
                    "question": "What are 'Fields' in AutoCAD text and how do they differ from static text?",
                    "options": [
                        "Fields are dynamic text placeholders that auto-update their displayed value based on drawing properties (filename, date, sheet number, object properties, plot scale) without manual editing.",
                        "Fields are encrypted text strings that cannot be read by other CAD software.",
                        "Fields are fixed labels that must be manually updated each time a drawing is revised.",
                        "Fields only work inside table cells and cannot be used in title blocks or annotations."
                    ],
                    "correctIdx": 0,
                    "why": "Fields pull live data from the drawing database: %<\\AcVar Filename>% shows the current filename, %<\\AcVar Date>% shows today's date. They update on save, plot, or regeneration.",
                    "pitfall": "Fields display '####' or stale values if the background update setting (FIELDEVAL) is disabled. Ensure FIELDEVAL includes 'on plot' for title blocks to show current data when printing."
                }
            ]
        }
    ],
    "sim": [
        {
            "id": 4,
            "title": "Lesson 4: CFD & Thermal",
            "desc": "Turbulence Modeling, Conjugate Heat Transfer, & Mesh Independence",
            "questions": [
                {
                    "type": "single",
                    "nodeId": "sim-cfd",
                    "slug": "rans-turbulence-models",
                    "difficulty": "intermediate",
                    "question": "In CFD (Computational Fluid Dynamics), what do RANS turbulence models (k-epsilon, k-omega SST) approximate?",
                    "options": [
                        "They solve time-averaged Navier-Stokes equations with modeled turbulent viscosity, predicting mean flow behavior without resolving individual turbulent eddies.",
                        "They calculate exact positions of every fluid molecule for perfect accuracy.",
                        "They only work for incompressible laminar flow in straight pipes.",
                        "They replace the need for any computational mesh or spatial discretization."
                    ],
                    "correctIdx": 0,
                    "why": "RANS models are practical engineering tools: they decompose velocity into mean + fluctuation, model the fluctuation effects via turbulent viscosity, and solve for the mean flow field.",
                    "pitfall": "k-epsilon struggles with separation, adverse pressure gradients, and swirl. Use k-omega SST for external aerodynamics and flows with boundary layer separation."
                },
                {
                    "type": "single",
                    "nodeId": "sim-thermal",
                    "slug": "conjugate-heat-transfer",
                    "difficulty": "advanced",
                    "question": "What distinguishes conjugate heat transfer (CHT) analysis from a simple convection boundary condition?",
                    "options": [
                        "CHT simultaneously solves fluid flow AND solid conduction in one coupled simulation, computing heat flux across solid-fluid interfaces without prescribing a convection coefficient.",
                        "CHT only models radiation heat transfer between surfaces.",
                        "CHT is a simplified 1D analytical calculation, not a numerical simulation.",
                        "CHT replaces the energy equation with a constant temperature assumption."
                    ],
                    "correctIdx": 0,
                    "why": "In CHT, the solver calculates local heat transfer coefficients from the resolved flow field. This captures effects like recirculation zones with poor cooling that a prescribed 'h' would miss.",
                    "pitfall": "CHT requires fine boundary layer mesh on solid-fluid interfaces (y+ ≈ 1 for accurate heat flux). Coarse meshes at walls produce wrong temperature predictions."
                },
                {
                    "type": "single",
                    "nodeId": "sim-mesh",
                    "slug": "yplus-wall-treatment",
                    "difficulty": "advanced",
                    "question": "In CFD wall-bounded flows, what does the y+ (y-plus) value of the first cell represent?",
                    "options": [
                        "A non-dimensional wall distance indicating whether the first mesh cell resolves the viscous sublayer (y+ ≈ 1) or relies on wall functions (y+ = 30-300) for near-wall turbulence modeling.",
                        "The total number of mesh cells in the simulation domain.",
                        "The percentage of convergence achieved by the solver.",
                        "The physical height in millimeters of the tallest cell in the mesh."
                    ],
                    "correctIdx": 0,
                    "why": "y+ determines wall treatment validity. Low-Re models need y+ ≈ 1 (resolving viscous sublayer). Standard wall functions need y+ = 30-300. Between 5-30 is a 'buffer zone' where neither is accurate.",
                    "pitfall": "Check y+ AFTER running the simulation (it depends on local flow conditions). If y+ falls in the buffer zone (5-30), refine or coarsen the boundary layer mesh accordingly."
                },
                {
                    "type": "multiple",
                    "nodeId": "sim-cfd",
                    "slug": "cfd-convergence-indicators",
                    "difficulty": "intermediate",
                    "question": "Which indicators confirm that a steady-state CFD simulation has converged to a reliable solution? (Select all correct)",
                    "options": [
                        "Residuals (continuity, momentum, energy) have dropped by 3-4+ orders of magnitude and stabilized",
                        "Monitored quantities (drag force, outlet temperature, pressure drop) have reached steady values",
                        "Mass/energy imbalance between inlet and outlet is below 0.1%",
                        "The simulation has run for exactly 1000 iterations regardless of residual behavior"
                    ],
                    "correctIndices": [0, 1, 2],
                    "why": "Convergence requires all three: low residuals, stable monitors, and conservation balance. A fixed iteration count guarantees nothing about solution quality.",
                    "pitfall": "Some flows are inherently unsteady (vortex shedding, separation bubbles). Forcing steady-state convergence on unsteady physics produces oscillating residuals and wrong predictions."
                },
                {
                    "type": "single",
                    "nodeId": "sim-mesh",
                    "slug": "mesh-independence-study",
                    "difficulty": "intermediate",
                    "question": "What is the purpose of a mesh independence (grid convergence) study in CFD/FEA?",
                    "options": [
                        "Systematically refining the mesh until key output quantities (stress, pressure drop, heat transfer) change by less than a threshold (typically 1-2%), proving results are not artifacts of mesh resolution.",
                        "Testing whether the simulation runs on different computer hardware configurations.",
                        "Verifying that the mesh file format is compatible with multiple CFD software packages.",
                        "Checking that the mesh generation software license is valid."
                    ],
                    "correctIdx": 0,
                    "why": "Without mesh independence, results may be mesh-dependent — refining could change the answer significantly. Three mesh levels (coarse, medium, fine) with consistent results confirm grid independence.",
                    "pitfall": "Only compare results at identical monitoring locations. Global averages can appear converged while local values (peak stress, recirculation zone size) still change with refinement."
                }
            ]
        },
        {
            "id": 5,
            "title": "Lesson 5: Structural Dynamics & Optimization",
            "desc": "Modal Analysis, Explicit Dynamics, & Design Optimization Loops",
            "questions": [
                {
                    "type": "single",
                    "nodeId": "sim-modal",
                    "slug": "modal-analysis-purpose",
                    "difficulty": "intermediate",
                    "question": "What does modal analysis determine about a mechanical structure, and why is it critical for vibration design?",
                    "options": [
                        "Modal analysis finds the natural frequencies and mode shapes of a structure, identifying resonance risks where operating frequencies could excite destructive vibrations.",
                        "Modal analysis calculates the maximum static load a structure can bear before yielding.",
                        "Modal analysis measures the acoustic noise level produced by the structure during operation.",
                        "Modal analysis determines the thermal expansion coefficient of materials under heating."
                    ],
                    "correctIdx": 0,
                    "why": "Every structure has natural frequencies. If an excitation source (motor RPM, wind gust frequency) matches a natural frequency, resonance amplifies vibration, causing fatigue or failure.",
                    "pitfall": "Always check the first 10-20 modes. Higher modes with less mass participation can still be excited by harmonic content in broadband excitation sources."
                },
                {
                    "type": "single",
                    "nodeId": "sim-explicit",
                    "slug": "explicit-vs-implicit-dynamics",
                    "difficulty": "advanced",
                    "question": "When should an engineer use explicit dynamics (LS-DYNA, Abaqus Explicit) instead of implicit static/dynamic analysis?",
                    "options": [
                        "For very short-duration high-speed events (crash, impact, blast, metal forming) where time steps are microseconds and large deformations/contact dominate the physics.",
                        "For steady-state thermal analysis of building HVAC systems.",
                        "For calculating bolt pretension in a flanged connection under static pressure.",
                        "For modal analysis of a bridge deck under pedestrian walking loads."
                    ],
                    "correctIdx": 0,
                    "why": "Explicit solvers advance time using tiny stable steps without solving large equation systems. This excels at crash (milliseconds), forming (contact changes every step), and blast (pressure waves).",
                    "pitfall": "Explicit time step is limited by the smallest element (Courant condition). One tiny element in a large model forces globally small time steps, dramatically increasing solve time."
                },
                {
                    "type": "single",
                    "nodeId": "sim-opt",
                    "slug": "parametric-vs-topology-opt",
                    "difficulty": "intermediate",
                    "question": "What is the key difference between parametric optimization and topology optimization in structural design?",
                    "options": [
                        "Parametric optimization varies dimensions of a fixed shape (wall thickness, rib height), while topology optimization freely redistributes material, potentially creating entirely new shapes with holes and branches.",
                        "Parametric optimization uses FEA while topology optimization uses hand calculations.",
                        "Topology optimization only works for plastic materials, not metals.",
                        "They are identical methods with different names used by different software vendors."
                    ],
                    "correctIdx": 0,
                    "why": "Parametric optimization searches within a design space defined by parameters. Topology optimization has no preconceived shape — it discovers the optimal load paths from scratch.",
                    "pitfall": "Topology results often require manufacturing interpretation. An optimal topology may include undercuts, enclosed voids, or thin bridges that are impractical for CNC machining or casting."
                },
                {
                    "type": "multiple",
                    "nodeId": "sim-modal",
                    "slug": "vibration-mitigation-strategies",
                    "difficulty": "advanced",
                    "question": "Which engineering strategies can shift a structure's natural frequencies away from operating excitation frequencies? (Select all correct)",
                    "options": [
                        "Adding stiffeners or ribs to increase structural stiffness (raises natural frequency)",
                        "Adding mass dampers or tuned mass absorbers (shifts/splits modes)",
                        "Changing material to one with higher stiffness-to-weight ratio (E/rho)",
                        "Painting the structure a different color to change its acoustic properties"
                    ],
                    "correctIndices": [0, 1, 2],
                    "why": "Natural frequency depends on stiffness and mass (f ∝ √(k/m)). Stiffening raises frequency; adding dampers splits modes; material E/rho ratio directly affects wave speed.",
                    "pitfall": "Simply adding mass lowers frequency — but may move it toward a different excitation source. Always map ALL excitation frequencies before deciding which direction to shift modes."
                },
                {
                    "type": "single",
                    "nodeId": "sim-opt",
                    "slug": "design-of-experiments-doe",
                    "difficulty": "intermediate",
                    "question": "In simulation-driven design, what does Design of Experiments (DOE) methodology provide?",
                    "options": [
                        "A structured sampling strategy (Latin Hypercube, full factorial) that efficiently explores the design space, identifying which parameters most influence performance with minimum simulation runs.",
                        "A laboratory testing protocol for physical prototype destructive testing.",
                        "A project management timeline for scheduling engineering resources.",
                        "An accounting spreadsheet for tracking simulation software license costs."
                    ],
                    "correctIdx": 0,
                    "why": "DOE minimizes the number of expensive simulations needed to understand parameter sensitivity. A 5-parameter study with 3 levels per parameter needs 243 runs with full factorial but only ~25 with Latin Hypercube.",
                    "pitfall": "DOE results are only valid within the sampled range. Extrapolating surrogate models beyond the DOE bounds can predict physically impossible (negative thickness) or catastrophically wrong results."
                }
            ]
        }
    ],
    "viz": [
        {
            "id": 4,
            "title": "Lesson 4: Lighting & Environment",
            "desc": "HDRI Lighting, Sun Studies, & Interior Lighting Strategies",
            "questions": [
                {
                    "type": "single",
                    "nodeId": "lighting",
                    "slug": "hdri-image-based-lighting",
                    "difficulty": "intermediate",
                    "question": "Why do visualization artists use HDRI (High Dynamic Range Image) environment maps instead of simple background colors for lighting?",
                    "options": [
                        "HDRI maps contain actual luminance data spanning many orders of magnitude, providing physically accurate illumination, reflections, and color bleeding from real-world environments.",
                        "HDRIs are smaller files that render faster than solid color backgrounds.",
                        "HDRIs only affect the background image, not the lighting of objects in the scene.",
                        "HDRIs are required by rendering software licenses to produce any output."
                    ],
                    "correctIdx": 0,
                    "why": "HDRIs encode real-world brightness ratios (sunlit areas 100,000x brighter than shadows). This creates natural lighting, soft shadows, and environment reflections that flat colors cannot provide.",
                    "pitfall": "Low-resolution HDRIs produce blurry reflections on glossy surfaces. Use 4K+ resolution HDRIs for scenes with reflective materials (chrome, glass, water)."
                },
                {
                    "type": "single",
                    "nodeId": "lighting",
                    "slug": "three-point-lighting",
                    "difficulty": "beginner",
                    "question": "In product visualization, what is the purpose of a classic three-point lighting setup (key, fill, rim)?",
                    "options": [
                        "Key light provides main illumination direction; fill light softens shadows on the opposite side; rim/back light separates the subject from the background by edge-highlighting the silhouette.",
                        "Three identical lights pointed at the same spot create the brightest possible illumination.",
                        "Three lights are the minimum required by rendering engines to calculate any shadows.",
                        "The three lights correspond to red, green, and blue color channels for white balance."
                    ],
                    "correctIdx": 0,
                    "why": "Three-point lighting creates depth perception in 2D images. The key establishes mood/direction, fill controls shadow density/contrast, and rim adds dimensional separation.",
                    "pitfall": "Don't use three-point lighting dogmatically. Moody automotive renders may use only key + rim (no fill) for dramatic contrast. Let the creative intent drive the setup."
                },
                {
                    "type": "single",
                    "nodeId": "lighting",
                    "slug": "interior-artificial-lighting",
                    "difficulty": "intermediate",
                    "question": "When rendering architectural interiors, why is accurate IES photometric data important for artificial light sources?",
                    "options": [
                        "IES profiles define the real-world light distribution pattern (beam angle, intensity falloff, asymmetry) of specific luminaires, producing physically accurate illumination matching manufacturer specifications.",
                        "IES files make lights render faster by reducing calculation complexity.",
                        "IES data is only used for exterior street lighting, not interior design.",
                        "IES profiles add decorative lens flare effects to light fixtures."
                    ],
                    "correctIdx": 0,
                    "why": "Each luminaire has a unique distribution (narrow spot, wide flood, asymmetric wall-wash). IES data from manufacturers ensures rendered lighting matches what will be installed, validating design decisions.",
                    "pitfall": "Verify IES file units (candela vs. lumens) and coordinate orientation. Some manufacturer IES files use non-standard orientations that produce rotated or inverted light patterns."
                },
                {
                    "type": "multiple",
                    "nodeId": "lighting",
                    "slug": "global-illumination-methods",
                    "difficulty": "advanced",
                    "question": "Which rendering algorithms compute global illumination (indirect light bounces) in architectural visualization? (Select all correct)",
                    "options": [
                        "Path tracing (Monte Carlo random ray sampling)",
                        "Photon mapping (two-pass: photon emission + gathering)",
                        "Irradiance caching (interpolating indirect illumination between sample points)",
                        "Flat shading (no lighting calculation, only base color display)"
                    ],
                    "correctIndices": [0, 1, 2],
                    "why": "Path tracing, photon mapping, and irradiance caching all compute multi-bounce indirect illumination. Flat shading displays unlit base color with no GI calculation.",
                    "pitfall": "Irradiance caching is fast but can miss small-scale color bleeding (colored glass caustics). Switch to brute-force path tracing for scenes where subtle indirect effects are critical."
                },
                {
                    "type": "single",
                    "nodeId": "camera",
                    "slug": "sun-study-animation",
                    "difficulty": "beginner",
                    "question": "What does a sun study (solar analysis) animation reveal about a building design?",
                    "options": [
                        "How sunlight and shadows move across the building and surrounding context throughout the day and year, informing facade orientation, shading device design, and daylighting performance.",
                        "How the building's structural loads change with temperature across seasons.",
                        "The chemical degradation rate of exterior paint under UV exposure.",
                        "The electricity generation capacity of solar panels on the roof."
                    ],
                    "correctIdx": 0,
                    "why": "Sun studies visualize solar access for daylighting, identify overshadowing of neighbors, validate shading device effectiveness, and inform passive solar design decisions.",
                    "pitfall": "Set correct geographic coordinates and true north orientation. A 10-degree north error dramatically changes shadow patterns, especially at high latitudes or during winter months."
                }
            ]
        },
        {
            "id": 5,
            "title": "Lesson 5: Post-Processing & Delivery",
            "desc": "Compositing, Color Management, & Real-Time Visualization",
            "questions": [
                {
                    "type": "single",
                    "nodeId": "post-process",
                    "slug": "render-passes-compositing",
                    "difficulty": "intermediate",
                    "question": "Why do professional visualization artists render separate passes (diffuse, reflection, shadow, Z-depth) instead of a single combined beauty image?",
                    "options": [
                        "Separate passes allow post-production adjustment of individual lighting components (brighten reflections, soften shadows, adjust depth-of-field) without re-rendering the entire scene.",
                        "Separate passes are required because rendering software cannot combine all effects simultaneously.",
                        "Separate passes reduce the total file size compared to a single combined image.",
                        "Separate passes are only used in film VFX, never in architectural visualization."
                    ],
                    "correctIdx": 0,
                    "why": "Compositing passes in Photoshop/Nuke gives artistic control after the expensive render phase. Adjust shadow intensity, add fog via Z-depth, tweak reflections — all without waiting for another render.",
                    "pitfall": "Render passes in linear color space (32-bit EXR), not sRGB 8-bit. Compositing in sRGB produces incorrect blending, banding, and clipped highlights."
                },
                {
                    "type": "single",
                    "nodeId": "post-process",
                    "slug": "color-management-aces",
                    "difficulty": "advanced",
                    "question": "What problem does ACES (Academy Color Encoding System) solve in a visualization pipeline?",
                    "options": [
                        "ACES provides a scene-referred linear color space with wide gamut that preserves all captured/rendered color data through the pipeline, with standardized transforms for display on different devices.",
                        "ACES compresses image files to reduce storage requirements.",
                        "ACES is a camera brand that produces the sharpest photographs.",
                        "ACES converts all images to grayscale for structural analysis."
                    ],
                    "correctIdx": 0,
                    "why": "Without ACES, textures in different color spaces (sRGB photos, raw HDRIs, Rec.709 video) produce inconsistent results. ACES linearizes everything into one interchange space for predictable compositing.",
                    "pitfall": "Apply ACES input transforms (IDTs) to all texture maps. A sRGB texture loaded without IDT into an ACES pipeline appears washed out because the renderer double-linearizes it."
                },
                {
                    "type": "single",
                    "nodeId": "rendering",
                    "slug": "realtime-vs-offline-rendering",
                    "difficulty": "beginner",
                    "question": "What is the fundamental tradeoff between real-time rendering (Unreal Engine, Twinmotion) and offline path tracing (V-Ray, Corona)?",
                    "options": [
                        "Real-time renders approximate lighting with rasterization tricks for interactive framerates; offline path tracers simulate physically accurate light transport but require minutes-to-hours per frame.",
                        "Real-time rendering produces higher quality results than offline rendering.",
                        "Offline rendering cannot display any image until the entire animation is complete.",
                        "Real-time rendering requires a constant internet connection while offline works locally."
                    ],
                    "correctIdx": 0,
                    "why": "Real-time uses screen-space reflections, pre-baked lightmaps, and ray-traced approximations for 30-60fps. Offline traces billions of rays for ground-truth GI, caustics, and subsurface scattering.",
                    "pitfall": "Real-time 'ray tracing' (RTX) is limited in bounce count and sample quality. Marketing claims of 'ray traced' real-time don't equal offline quality for architectural still images."
                },
                {
                    "type": "multiple",
                    "nodeId": "rendering",
                    "slug": "denoising-techniques",
                    "difficulty": "intermediate",
                    "question": "Which denoising approaches are used to clean up Monte Carlo noise in path-traced renders? (Select all correct)",
                    "options": [
                        "AI/ML denoisers (Intel OIDN, NVIDIA OptiX) trained on clean/noisy image pairs",
                        "Non-local means filtering using auxiliary buffers (normals, albedo, depth) to preserve edges",
                        "Simply increasing render samples until noise is imperceptible (brute force)",
                        "Applying JPEG compression to hide noise artifacts in the lossy encoding"
                    ],
                    "correctIndices": [0, 1, 2],
                    "why": "AI denoisers, non-local means, and brute-force sampling all reduce noise legitimately. JPEG compression introduces its own block artifacts without actually improving the underlying render quality.",
                    "pitfall": "AI denoisers can hallucinate or smear fine detail (fabric weave, distant text). Always compare denoised output against a high-sample reference to verify no detail loss."
                },
                {
                    "type": "single",
                    "nodeId": "camera",
                    "slug": "360-panorama-rendering",
                    "difficulty": "intermediate",
                    "question": "What camera type and projection must be used to render a 360-degree interactive panorama for VR viewing?",
                    "options": [
                        "A spherical (equirectangular) camera that captures the full 360x180 degree environment, output as a 2:1 aspect ratio image that maps to a sphere for VR headset or web viewer display.",
                        "A standard perspective camera rotated 4 times at 90-degree intervals and stitched together.",
                        "A fisheye lens with 180-degree field of view, which covers the full sphere.",
                        "Any camera type works for VR — the VR software automatically fills in missing angles."
                    ],
                    "correctIdx": 0,
                    "why": "Equirectangular projection maps the full sphere onto a flat rectangle (like a world map). VR viewers inverse-project this back onto a sphere surrounding the viewer for immersive 360 viewing.",
                    "pitfall": "Render equirectangular panoramas at 8K+ resolution (8192x4096 minimum). Each viewer direction only samples a small region of the image, so visible resolution per eye is much lower than total pixel count."
                }
            ]
        }
    ]
}


def add_difficulty_to_existing(content):
    """Add difficulty: 'beginner' to all existing questions that don't have it."""
    # Add difficulty field after slug field for existing questions
    pattern = r'(slug: "[^"]+",)\n(\s+question:)'
    replacement = r'\1\n              difficulty: "beginner",\n\2'
    return re.sub(pattern, replacement, content)


def format_question(q, indent=14):
    """Format a question dict as JavaScript source."""
    sp = " " * indent
    lines = []
    lines.append(f"{sp}{{")
    lines.append(f'{sp}  type: "{q["type"]}",')
    lines.append(f'{sp}  nodeId: "{q["nodeId"]}",')
    lines.append(f'{sp}  slug: "{q["slug"]}",')
    lines.append(f'{sp}  difficulty: "{q["difficulty"]}",')
    
    # Escape question text
    qtext = q["question"].replace('"', '\\"')
    lines.append(f'{sp}  question: "{qtext}",')
    
    lines.append(f'{sp}  options: [')
    for opt in q["options"]:
        opt_escaped = opt.replace('"', '\\"')
        lines.append(f'{sp}    "{opt_escaped}",')
    lines.append(f'{sp}  ],')
    
    if q.get("image"):
        img = q["image"].replace("\\", "\\\\").replace('"', '\\"')
        img = img.replace("\n", " ").replace("\r", " ")
        lines.append(f'{sp}  image: "{img}",')

    if q["type"] in ("single", "image"):
        lines.append(f'{sp}  correctIdx: {q["correctIdx"]},')
    else:
        lines.append(f'{sp}  correctIndices: {q["correctIndices"]},')
    
    why_escaped = q["why"].replace('"', '\\"')
    lines.append(f'{sp}  why: "{why_escaped}",')
    pitfall_escaped = q["pitfall"].replace('"', '\\"')
    lines.append(f'{sp}  pitfall: "{pitfall_escaped}"')
    lines.append(f"{sp}}}")
    return "\n".join(lines)


def format_lesson(lesson, indent=8):
    """Format a lesson dict as JavaScript source."""
    sp = " " * indent
    lines = []
    lines.append(f"{sp}{{")
    lines.append(f'{sp}  id: {lesson["id"]},')
    lines.append(f'{sp}  title: "{lesson["title"]}",')
    lines.append(f'{sp}  desc: "{lesson["desc"]}",')
    lines.append(f'{sp}  questions: [')
    
    q_strs = []
    for q in lesson["questions"]:
        q_strs.append(format_question(q))
    lines.append(",\n".join(q_strs))
    
    lines.append(f'{sp}  ]')
    lines.append(f"{sp}}}")
    return "\n".join(lines)


def main():
    # Merge in the visual (看图识操作) + advanced text lessons
    try:
        from quiz_image_lessons import EXTRA_LESSONS
    except ImportError:
        import os, sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from quiz_image_lessons import EXTRA_LESSONS
    for tk, extra in EXTRA_LESSONS.items():
        NEW_LESSONS.setdefault(tk, []).extend(extra)

    with open("quiz.js", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Add difficulty field to existing questions
    content = add_difficulty_to_existing(content)
    
    # 2. Insert new lessons for each track, renumbering ids to follow the
    #    existing L1-L5 (so merged lessons become L6, L7, L8, ...).
    for track_key, lessons in NEW_LESSONS.items():
        # Determine the highest existing lesson id already in this track.
        tstart = content.index("\n    %s: {" % track_key)
        tclose = content.index("\n      ]\n    }", tstart)
        existing_ids = [int(x) for x in re.findall(r"\n          id: (\d+)", content[tstart:tclose])]
        base = (max(existing_ids) if existing_ids else 0) + 1

        for offset, lesson in enumerate(lessons):
            new_id = base + offset
            lesson["id"] = new_id
            lesson["title"] = re.sub(r"^Lesson \d+:", "Lesson %d:" % new_id, lesson["title"])

        new_lessons_text = "".join(",\n" + format_lesson(lesson) for lesson in lessons)

        # Insert just before the lessons-array close (the 6-space "      ]").
        content = content[:tclose] + new_lessons_text + content[tclose:]

    with open("quiz.js", "w", encoding="utf-8") as f:
        f.write(content)
    
    # Count new questions
    total_new = sum(len(q) for lessons in NEW_LESSONS.values() for q in [l["questions"] for l in lessons])
    print(f"Added {total_new} new questions across {sum(len(v) for v in NEW_LESSONS.values())} new lessons")
    print(f"Added difficulty tags to all existing questions")


if __name__ == "__main__":
    main()
