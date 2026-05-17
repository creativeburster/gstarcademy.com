import re

with open("kb-faq.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Inject tabs for SOLIDWORKS and CATIA into the tablist
tablist_needle = '<button type="button" class="kb-faq-tab" role="tab" aria-selected="false" data-kb-faq-filter="bentley">Bentley</button>'
tablist_replacement = (
    tablist_needle + "\n" +
    '                <button type="button" class="kb-faq-tab" role="tab" aria-selected="false" data-kb-faq-filter="solidworks">SOLIDWORKS</button>\n' +
    '                <button type="button" class="kb-faq-tab" role="tab" aria-selected="false" data-kb-faq-filter="catia">CATIA</button>'
)

if 'data-kb-faq-filter="solidworks"' not in content:
    content = content.replace(tablist_needle, tablist_replacement)
    print("Injected SOLIDWORKS & CATIA tabs.")
else:
    print("Tabs already exist or were injected.")

# 2. Prepare FAQ items to inject
NEW_FAQS = """
                <!-- SOLIDWORKS FAQs (10 Items) -->
                <article class="kb-faq-entry" data-kb-faq-topic="solidworks">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is the difference between SOLIDWORKS Desktop and 3DEXPERIENCE SOLIDWORKS?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · SOLIDWORKS Installation & Deployment</p>
                    <div class="kb-faq-answer">
                      <strong>SOLIDWORKS Desktop</strong> is local file-based, running fully on your Windows workstation. <strong>3DEXPERIENCE SOLIDWORKS</strong> is cloud-connected; it installs locally but saves files as secure database objects in the cloud (single source of truth) with built-in version control and role-based sharing.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="solidworks">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How do SOLIDWORKS Configurations manage multiple design variations efficiently?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · SOLIDWORKS Modeling Basics</p>
                    <div class="kb-faq-answer">
                      <strong>Configurations</strong> allow you to create multiple variations of a part or assembly model within a single document. You can suppress or resolve features, modify dimensions, and configure custom properties per instance, frequently managed using embedded Excel <strong>Design Tables</strong>.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="solidworks">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What are the best performance settings for large assemblies in SOLIDWORKS?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · SOLIDWORKS Large Assembly Administration</p>
                    <div class="kb-faq-answer">
                      For large assemblies: (1) Turn on <strong>Large Assembly Settings</strong>; (2) Use <strong>Lightweight</strong> mode to load components without loading feature tree data; (3) Disable <i>'Verification on rebuild'</i> under Performance Options; and (4) Verify that your graphics driver matches SOLIDWORKS certified versions.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="solidworks">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does SOLIDWORKS PDM protect against data overwrites in multi-user environments?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · SOLIDWORKS PDM Vault Guide</p>
                    <div class="kb-faq-answer">
                      SOLIDWORKS PDM uses a strict <strong>Check-Out / Check-In</strong> mechanism. When a designer checks out a file, it locks the master version in the SQL database vault and grants write-access to that user only. Other team members can only view a read-only local cache, preventing concurrent overwriting conflicts.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="solidworks">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does 'Large Design Review' (LDR) speed up loading of assemblies?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · SOLIDWORKS Large Assembly Guide</p>
                    <div class="kb-faq-answer">
                      <strong>Large Design Review (LDR)</strong> opens massive assemblies in seconds by only loading display graphics data (tessellated mesh) instead of solving deep parametric modeling history or geometric constraints. In LDR, you can still measure, view cross-sections, and execute edits like inserting components.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="solidworks">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is 'SpeedPak' configuration in SOLIDWORKS and when should I use it?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · SOLIDWORKS Performance Optimization</p>
                    <div class="kb-faq-answer">
                      <strong>SpeedPak</strong> creates a simplified graphical representation of an assembly without losing mates and drawing reference points. It deletes unnecessary faces and bodies from RAM cache, making it ideal for utilizing very complex sub-assemblies inside massive master layouts.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="solidworks">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How do I troubleshoot rebuild errors and resolve mate conflicts in SOLIDWORKS?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · SOLIDWORKS Assembly Debugging</p>
                    <div class="kb-faq-answer">
                      Use <strong>MateXpert</strong> to diagnose assembly conflicts. It isolates conflicting constraints and pinpoints redundant constraints. For part-level rebuild issues, step through features chronologically using the <strong>FeatureGoTo / Rollback bar</strong> to locate the precise parent reference loss.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="solidworks">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is the difference between System Options and Document Properties?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · SOLIDWORKS System Administration</p>
                    <div class="kb-faq-answer">
                      <strong>System Options</strong> control the global behavior of the application (e.g., file locations, performance options) and are saved in the Windows Registry. <strong>Document Properties</strong> control active drafting units, sheet scales, and dimension styles, and are saved directly within that specific template or file.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="solidworks">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does SOLIDWORKS manage sheet metal bend allowances and K-Factors?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · SOLIDWORKS Sheet Metal Manufacturing</p>
                    <div class="kb-faq-answer">
                      SOLIDWORKS calculates flat pattern expansion using the <strong>K-Factor</strong>, which is the ratio of the neutral sheet layer to total thickness. You can configure K-Factors, <strong>Bend Allowances</strong>, or custom <strong>Bend Tables</strong> provided by your manufacturing supplier to ensure extreme precision when unfolding parts.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="solidworks">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How do custom properties in SOLIDWORKS parts automate drawing title blocks?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · SOLIDWORKS Drawing Administration</p>
                    <div class="kb-faq-answer">
                      By defining <strong>Custom Properties</strong> (e.g., PartNo, Material, Revision) in the 3D model, you can link title block annotations directly using the syntax <code>$PRPSHEET:"Property_Name"</code>. When the part is swapped, the drawing annotations update automatically, eliminating manual entry mistakes.
                    </div>
                  </div>
                </article>

                <!-- CATIA FAQs (10 Items) -->
                <article class="kb-faq-entry" data-kb-faq-topic="catia">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>Why is CATIA GSD considered the gold standard for surface modeling?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · CATIA Generative Shape Design Guide</p>
                    <div class="kb-faq-answer">
                      <strong>Generative Shape Design (GSD)</strong> delivers uncompromising control over G0, G1, G2 (tangency), and G3 (curvature) continuous shapes. It easily manages dense mathematical wireframe skeletons and multi-section sweeps, which are essential for aerodynamic surface integrity in aerospace and automotive outer-mold-line designs.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="catia">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is the main difference between CATIA V5 and CATIA V6 (3DEXPERIENCE)?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · CATIA Infrastructure Migration</p>
                    <div class="kb-faq-answer">
                      CATIA V5 utilizes a traditional <strong>file-based storage paradigm</strong> (.CATPart, .CATProduct) stored locally or in basic PDM vaults. CATIA V6 (3DEXPERIENCE) uses a **database-driven architecture**, where models exist as structured metadata objects in the ENOVIA database, enabling massive real-time co-authoring without file locks.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="catia">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does CAA (Component Application Architecture) extend CATIA's core engine?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · CATIA CAA Developer Manual</p>
                    <div class="kb-faq-answer">
                      <strong>Component Application Architecture (CAA)</strong> is the native C++ API framework for Dassault Systemes products. Unlike lightweight script macros, CAA provides direct access to topological modeler operations and Specification Tree structures, allowing developers to create highly-optimized proprietary workbenches.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="catia">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does CATIA handle ultra-large assembly management and space coordination?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · CATIA Product Engineering Coordination</p>
                    <div class="kb-faq-answer">
                      CATIA coordinates massive digital mockups (DMU) by using <strong>Visualization Mode</strong> (loading lightweight cgr/3dxml representation) instead of Design Mode. Designers use the <strong>DMU Space Analysis</strong> workbench to perform real-time multi-gigabyte interference calculations and clearances.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="catia">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is a 'PowerCopy' in CATIA and how does it automate design patterns?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · CATIA Knowledge Advisor Guide</p>
                    <div class="kb-faq-answer">
                      A <strong>PowerCopy</strong> is a reusable set of spec-tree features (solids, surfaces, sketches, coordinate systems) that can be stored in a library template. When instantiated, it prompts the user to select new geometric inputs, adapting its rich parameter history to the local curvature seamlessly.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="catia">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How to control links in CATIA's Multi-Model link (MML) system?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · CATIA Assembly & Part Linking</p>
                    <div class="kb-faq-answer">
                      Use the <strong>Edit Links</strong> dialog to inspect external geometric publications. For safe collaborative modeling, check the options <i>'Keep link with selected object'</i> and enforce <strong>Publications</strong> on shared parent sketch boundaries to prevent downstream parent loss.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="catia">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What are the best practices for Hybrid Design (Solid + Surface) in CATIA V5?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · CATIA Part Design Practices</p>
                    <div class="kb-faq-answer">
                      In <strong>Hybrid Design</strong> mode, wireframe and surface elements are stored directly inside the active <i>PartBody</i> along with solids. Best practices recommend separating them: construct complex surfaces in distinct <strong>Geometrical Sets</strong>, then perform boolean closes inside mechanical solid bodies.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="catia">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does CATIA's Composites Design workbench manage complex ply laying?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · CATIA Advanced Composites</p>
                    <div class="kb-faq-answer">
                      The <strong>Composites Design</strong> workbench allows engineers to define ply sequences, material orientations, and execute <strong>Draping Simulations</strong>. The draping solver projects composite warp and weft parameters onto curved surfaces, identifying zones of high shear strain prior to layup.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="catia">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is the role of ENOVIA inside a CATIA 3DEXPERIENCE workflow?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · 3DEXPERIENCE PLM Integration</p>
                    <div class="kb-faq-answer">
                      <strong>ENOVIA</strong> acts as the central data governance backbone. It manages user roles (Reader, Author, Leader), collaborative spaces, active checkouts (Locks), engineering changes, and structures the master <strong>Engineering Bill of Materials (EBOM)</strong> across enterprise divisions.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="catia">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does CATIA FT&A support Model-Based Definition (MBD)?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · CATIA Functional Tolerancing & Annotation</p>
                    <div class="kb-faq-answer">
                      <strong>Functional Tolerancing & Annotation (FT&A)</strong> embeds 3D GD&T annotations directly onto the surface faces of the solid model. By eliminating traditional 2D paper drawings, it supports <strong>Model-Based Definition (MBD)</strong>, allowing downstream manufacturing and inspection systems to parse product tolerancing directly.
                    </div>
                  </div>
                </article>

                <!-- Autodesk Additional FAQs (10 Items) -->
                <article class="kb-faq-entry" data-kb-faq-topic="autocad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is the difference between dynamic blocks and standard blocks in AutoCAD?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · AutoCAD Advanced Blocks</p>
                    <div class="kb-faq-answer">
                      Standard blocks are rigid collections of geometric entities. <strong>Dynamic Blocks</strong> contain smart parameters and actions (like stretch, flip, rotate, or lookup tables). This allows a single block definition to morph into various sizes or visual forms during drafting, reducing block library clutter.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="autocad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does 'Sheet Set Manager' (SSM) coordinate sheet properties globally?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · AutoCAD Sheet Set Management</p>
                    <div class="kb-faq-answer">
                      <strong>Sheet Set Manager (SSM)</strong> stores sheet metadata inside a central <code>.dst</code> file. By using <strong>Sheet Custom Fields</strong>, designers can automatically populate scales, project numbers, and titles across hundreds of sheets, ensuring instant updates across title blocks globally.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="autocad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How do I fix AutoCAD layout display performance and viewport lagging?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · AutoCAD Performance Diagnostics</p>
                    <div class="kb-faq-answer">
                      To optimize lag: (1) Ensure Hardware Acceleration is ON (<code>3DCONFIG</code>); (2) Toggle <code>LAYOUTREGENCTL</code> to 2 to cache layouts in RAM; (3) Clean nested blocks using <code>PURGE</code> and repair geometry database errors using <code>AUDIT</code>.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="autocad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What are AutoCAD 'Sysvars' and how do I back up a clean user profile?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · AutoCAD Settings & Profiles</p>
                    <div class="kb-faq-answer">
                      <strong>Sysvars (System Variables)</strong> are named variables controlling Snap settings, visual toggles, or command defaults (e.g., <code>PICKBOX</code>, <code>FILEDIA</code>). You can backup profiles via Options > Profiles > Export to save custom workspaces into an <code>.arg</code> file.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="revit">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How do 'Shared Parameters' differ from Project and Family Parameters in Revit?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · Revit Parameter Coordination</p>
                    <div class="kb-faq-answer">
                      Family Parameters only drive dimensions in specific family files. Project Parameters apply to chosen categories inside that project but cannot be exported to tags. <strong>Shared Parameters</strong> are defined in a external `.txt` file, allowing data sharing across families, project files, and scheduling tables.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="revit">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is 'Design Option' in Revit and how to manage design variants?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · Revit Design Management</p>
                    <div class="kb-faq-answer">
                      <strong>Design Options</strong> allow designers to model multiple alternative design studies within a single Revit model file. Active view instances can be assigned specific Design Option visibility, allowing seamless, side-by-side scheduling and drawing updates without model duplication.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="revit">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How to improve Revit model performance during worksharing synchronization?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · Revit BIM Management</p>
                    <div class="kb-faq-answer">
                      To optimize <i>'Sync with Central'</i>: (1) Ensure all links (CAD, PDFs) are set to **Overlay** instead of Attachment; (2) Close unneeded Worksets; (3) Clean up warnings (Manage > Review Warnings) because warning clutter slows down database solving cycles.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="civil3d">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How do 'Data Shortcuts' in Civil 3D manage terrain models?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                    </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · Civil 3D Project Coordination</p>
                    <div class="kb-faq-answer">
                      <strong>Data Shortcuts</strong> create references to geometric elements (like design surfaces, alignments, alignments, profiles) stored in separate master drawings. This allows a site grading specialist to work on a referenced surface without loading the entire survey database, reducing memory footprints.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="inventor">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does 'iLogic' in Inventor enable rule-based assembly automation?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · Inventor iLogic Customization</p>
                    <div class="kb-faq-answer">
                      <strong>iLogic</strong> embeds lightweight VB.NET code directly into parts or assemblies. Non-programmers can write simple rules (e.g., <i>'If length > 1000 then suppress Feature_A'</i>), which evaluate automatically during parametric parameter changes, enabling rapid product customization.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="fusion">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does Fusion manage cloud version history and branching?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · Fusion Cloud Integration</p>
                    <div class="kb-faq-answer">
                      Fusion saves all models in the Autodesk cloud. Each save generates a sequential **Version** node. Team members can create isolated branch sandbox environments to test assembly changes, and later execute formal merges back into the master timeline safely.
                    </div>
                  </div>
                </article>

                <!-- Gstarsoft Additional FAQs (11 Items) -->
                <article class="kb-faq-entry" data-kb-faq-topic="gstarcad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does GstarCAD 2026 optimize 'DWG Compare' performance?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · GstarCAD 2026 Release Notes</p>
                    <div class="kb-faq-answer">
                      In **GstarCAD 2026**, the DWG Compare engine utilizes enhanced multi-threading processing. It scans vector blocks and hatches in parallel, yielding up to a 40% speed improvement on complex site drawings with heavy external Xref coordinates.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="gstarcad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is the 'Parameters Manager' in GstarCAD and how does it drive constraints?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · GstarCAD Parametric Drafting</p>
                    <div class="kb-faq-answer">
                      The **Parameters Manager** is a centralized panel to manage geometric and dimensional constraint variables. Designers can define mathematical formulas (e.g., <code>Width * 0.75</code>) to drive sketch constraints, enabling reactive 2D parametric geometry updates.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="gstarcad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How to use 'Drawing Merge' to combine multiple DWGs into one master file?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · GstarCAD Project Collaboration</p>
                    <div class="kb-faq-answer">
                      Use the <code>DRAWINGMERGE</code> command. The wizard allows you to select multiple external drawing sheets, configure origin points, choose active layers, and merge them into a single Master DWG file with clash warnings.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="gstarcad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is 'GRX SDK' and how compatible is it with AutoCAD ObjectARX?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · GstarCAD Developer Reference</p>
                    <div class="kb-faq-answer">
                      The **GRX SDK** is the C++ development environment for GstarCAD. It provides high code-level parity with AutoCAD ObjectARX. Developers can port custom ARX plugins to GstarCAD with minimal changes to source files, retaining native performance.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="gstarcad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How to customize the Ribbon and Keyboard Shortcuts using GstarCAD's CUI editor?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · GstarCAD Workplace Customization</p>
                    <div class="kb-faq-answer">
                      Run the <code>CUI</code> command. This opens the Custom User Interface panel where you can drag and drop commands into the Ribbon tabs, define new shortcut keys, and export workspace profiles into a portable <code>.cuix</code> file.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="gstarcad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is the benefit of GstarCAD's 'SuperHatch' over standard patterns?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · GstarCAD Detailing Tips</p>
                    <div class="kb-faq-answer">
                      Unlike standard hatch patterns restricted to simple mathematical lines, **SuperHatch** allows designers to hatch selected boundaries using external images (.png/.jpg), complex block references, or external drawing files, enabling high-fidelity aesthetic hatches.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="gstarcad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does 'LISP Compatibility' in GstarCAD ease transition?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · GstarCAD Customization Support</p>
                    <div class="kb-faq-answer">
                      GstarCAD provides an outstanding built-in LISP interpreter supporting all standard VL-functions and DCL dialog boxes. Autolisp scripts written for other DWG editors run out-of-the-box in GstarCAD without compilation.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="gstarcad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How do I convert vectors from PDF drawings to editable DWG entities?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · GstarCAD PDF Integration</p>
                    <div class="kb-faq-answer">
                      Use the <code>PDFIMPORT</code> command. It parses vector pathways, text annotations, and layers directly from the PDF file, translating them back into native, editable DWG lines, arcs, and TrueType fonts.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="gstarcad">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is GstarCAD 'Data Link' and how to sync Excel tables in real-time?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · GstarCAD Advanced Table Tools</p>
                    <div class="kb-faq-answer">
                      **Data Link** (<code>DATALINK</code>) establishes an associative bidirectional link between a GstarCAD Table entity and an external Excel sheet. When you modify values in Excel, GstarCAD prompts you to update, updating table records automatically.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="fastview">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>How does 'DWG FastView markup' synchronize annotations between platforms?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · DWG FastView Cloud Services</p>
                    <div class="kb-faq-answer">
                      When a mobile or web reviewer places markups or dimensions on a drawing, the annotations are saved to a synchronized overlay database layer. The desktop GstarCAD client loads these overlay markups, keeping field and back-office teams perfectly coordinated.
                    </div>
                  </div>
                </article>

                <article class="kb-faq-entry" data-kb-faq-topic="fastview">
                  <button type="button" class="kb-faq-q-trigger">
                    <span class="kb-faq-qmark" aria-hidden="true">?</span>
                    <h3>What is 'GstarCAD 365' and how does it handle cloud-based co-editing?</h3>
                    <span class="kb-faq-toggle-ico" aria-hidden="true">＋</span>
                  </button>
                  <div class="kb-faq-a-body">
                    <p class="kb-faq-source">Source · Gstarsoft Cloud Collaboration</p>
                    <div class="kb-faq-answer">
                      **GstarCAD 365** is a collaborative SaaS ecosystem. Multiple registered users can log in, view, edit, and co-author identical DWG models in the cloud web portal, maintaining active lock boundaries on elements to prevent overlapping edits.
                    </div>
                  </div>
                </article>
"""

# 3. Inject new FAQs into the FAQ list
list_needle = '<section class="kb-faq-list" aria-label="Questions and answers" id="kb-faq-list">'
list_replacement = list_needle + NEW_FAQS

if 'data-kb-faq-topic="solidworks"' not in content:
    content = content.replace(list_needle, list_replacement)
    print("Injected all SOLIDWORKS, CATIA, and supplement FAQs.")
else:
    print("FAQs already exist or were injected.")

with open("kb-faq.html", "w", encoding="utf-8") as f:
    f.write(content)

print("FAQ enrichment complete!")
