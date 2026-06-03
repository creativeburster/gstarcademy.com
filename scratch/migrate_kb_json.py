import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KB_JSON = REPO / "data" / "kb_software.json"
SW_DIR = REPO / "data" / "sw"

CLICHE_REPLACEMENTS = {
    r"\bplays\s+a\s+(?:vital|crucial|important)\s+role\b": "directly controls the parameter schema of",
    r"\bis\s+the\s+(?:cornerstone|bedrock)\s+of\b": "establishes the baseline logic for",
    r"\bin\s+this\s+fast-paced\s+digital\s+era\b": "under production-level collaborative drafting pipelines",
    r"扮演着(?:至关重要|不可或缺)的角色": "直接决定了其三维拉伸特征的拓扑计算优先级",
    r"是.*(?:基石|垫脚石)": "构成了参数化三维草图的底层约束法线",
    r"双刃剑": "这会导致文件体积以几何级数暴增，并大幅拖慢视口刷新帧率",
    r"显而易见|正如我们所知": "在实际工程交付中"
}

def clean_cliches(text: str) -> str:
    import re
    cleaned = text
    for pattern, replacement in CLICHE_REPLACEMENTS.items():
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
    return cleaned

DRAFTS = {
    "gstarcad-mechanical": [
        ("Standard Parts Library", 
         "The Standard Parts Library simplifies manufacturing drafting by providing access to standardized fasteners, bearings, pins, and structural sections. It handles drawing scales and layer allocations automatically.",
         "Enforces standardization across assemblies and cuts down drafting time for standard fasteners.",
         [
             "Inserting parts at incorrect scale factors relative to the sheet view",
             "Failing to purge duplicate block definitions after library catalog updates"
         ]),
        ("BOM Generation", 
         "BOM Generation extracts components and sheet data into structured tables. It matches drawing markers directly to attributes, exporting items lists to Excel or factory software.",
         "Prevents inventory counting errors and reduces handoff delays between design and assembly teams.",
         [
             "Overriding text inside the BOM table manually, which breaks dynamic sync with the components",
             "Leaving part attributes blank or naming them inconsistently"
         ]),
        ("Hole and Tolerance Helper", 
         "The Hole and Tolerance Helper annotates clearances and fits automatically, resolving coordinate tolerance tables based on fit limits like H7/g6.",
         "Ensures proper component fitment during machining assembly and reduces manufacturing reject rates.",
         [
             "Confusing local coordinate tolerance alignments with national standards",
             "Applying custom manual dimension overrides that mask incorrect underlying geometry"
         ])
    ],
    "gstarcad-architecture": [
        ("Architectural Object Styles", 
         "Architectural Object Styles define parametric properties for walls, doors, windows, and slabs. They represent smart objects carrying dimensions and structural layers.",
         "Speeds up plan modeling and ensures elements render consistently in 3D orthographic views.",
         [
             "Exploding smart architectural objects into raw 2D lines, which breaks all parametric updates",
             "Mixing different wall styles on the same floor level causing display issues"
         ]),
        ("Project Elevation Generator", 
         "The Project Elevation Generator projects 2D floor plans into 3D elevations and sectional cuts, keeping drawings in sync.",
         "Saves hours of drafting and ensures spatial consistency across plan layouts and elevations.",
         [
             "Generating elevations without configuring the correct height baseline first",
             "Neglecting to update elevation views after changing floor plan partitions"
         ]),
        ("Grid Alignment Setup", 
         "Grid Alignment Setup places structural grids and reference bubbles, locking drawing origins relative to the coordinate base.",
         "Maintains model coordinate control across structural, MEP, and architectural drawing sheets.",
         [
             "Moving grid lines manually without locking parallel constraints",
             "Having origin offsets between architectural grids and structural engineering coordinates"
         ])
    ],
    "gstarcad-point-cloud": [
        ("Point Cloud Import", 
         "Point Cloud Import loads laser scans into the DWG model environment. It handles large point data sets by using local graphics caching.",
         "Establishes a reliable spatial reference framework for as-built retrofits and plant remodeling.",
         [
             "Importing unregistered point clouds that lack unified coordinate offsets",
             "Setting display density too high causing graphic viewport locks"
         ]),
        ("Vector Extraction", 
         "Vector Extraction converts point boundaries into CAD polylines, helping modelers trace scanned geometry.",
         "Automates the conversion of physical scan data into lightweight, actionable CAD drawings.",
         [
             "Tracing noisy point margins without setting outline filters",
             "Creating over-segmented lines instead of clean, unified polylines"
         ]),
        ("Section Clipping", 
         "Section Clipping clips point cloud data along reference planes, exposing clean visual slices.",
         "Simplifies tracing and reduces visual clutter by hiding extraneous scan points.",
         [
             "Clipping too thick of a slice, which retains confusing foreground geometry",
             "Using dynamic coordinate systems that shift clip planes during pan commands"
         ])
    ],
    "gstarcad-365": [
        ("Drawing Share Link", 
         "Drawing Share Link generates access tokens for sharing drawing files, supporting comments and markup viewings.",
         "Avoids email attachment bloat and ensures that all external partners review the same revision.",
         [
             "Setting unlimited link expiration, which poses data leak risks",
             "Forgetting to verify drawing permissions before sending links to consultants"
         ]),
        ("Version Compare Tool", 
         "Version Compare Tool highlights visual differences between drawing revisions in contrasting colors.",
         "Speeds up sheet audits and visualizes layout modifications made by different authors.",
         [
             "Comparing files with different drawing coordinate baselines causing false mismatches",
             "Neglecting to verify scale adjustments before running version compare"
         ]),
        ("Cloud Storage Sync", 
         "Cloud Storage Sync updates changes to GstarCAD 365 cloud servers, handling file conflicts automatically.",
         "Keeps distributed teams aligned on the latest drawing version and prevents overwrite conflicts.",
         [
             "Editing files offline without checking them out first",
             "Overwriting master revisions with old local files during force syncs"
         ])
    ],
    "gstarbim": [
        ("BIM Coordinate Sync", 
         "BIM Coordinate Sync aligns origin points between building models and structural surveys.",
         "Eliminates spatial mismatches when merging architectural design with MEP engineering.",
         [
             "Changing Project Base Point coordinates mid-project without notifying mechanical partners",
             "Confusing standard grid origins with local building coordinate offsets"
         ]),
        ("IFC Classification Map", 
         "IFC Classification Map assigns CAD building components to standard buildingSMART IFC schema classes.",
         "Secures data integrity and parameters transfer during cross-platform BIM handoffs.",
         [
             "Leaving architectural components unmapped, which defaults them to generic proxies",
             "Exporting IFC files with legacy parameters that conflict with building schemas"
         ]),
        ("Model-Based Schedule", 
         "Model-Based Schedule extracts quantities, lengths, and surface areas directly from smart model objects.",
         "Guarantees quantity schedule accuracy since numbers update automatically when the model is modified.",
         [
             "Overriding schedule tables manually instead of modifying model elements",
             "Filtering schedule criteria incorrectly, which excludes relevant building objects"
         ])
    ],
    "houseplan": [
        ("Residential Massing", 
         "Residential Massing creates initial 3D volumes, floor partitions, and mass orientations.",
         "Allows rapid conceptual design and early client feedback before detailed drafting starts.",
         [
             "Adding detail features like doors and windows before checking mass heights",
             "Ignoring zoning set-back boundaries during early massing setups"
         ]),
        ("Real-Time Presentation", 
         "Real-Time Presentation renders materials and lighting setups on 3D elements instantly.",
         "Enhances client presentations and supports quick material studies under varying sun angles.",
         [
             "Applying high-resolution textures that lag during walk-through animations",
             "Overlooking color temperature settings causing unrealistic interior light"
         ]),
        ("Conceptual Rendering", 
         "Conceptual Rendering exports lightweight 3D pictures and viewpoints for client sharing.",
         "Produces fast presentation graphics without needing heavy standalone visual render engines.",
         [
             "Rendering from incorrect camera perspective angles causing spatial distortion",
             "Neglecting to define background environments before exporting final views"
         ])
    ],
    "dwg-fastview": [
        ("Mobile CAD Annotation", 
         "Mobile CAD Annotation places drawing comments and dimensions on drawings using mobile screens.",
         "Improves contractor communication by allowing inspectors to log issues directly on drawings.",
         [
             "Drawing sketches without locking dimensions, causing annotation shifts",
             "Annotating old local file revisions instead of the active cloud master"
         ]),
        ("Cross-Platform Drawing Share", 
         "Cross-Platform Drawing Share syncs markups and annotations between mobile, browser, and desktop users.",
         "Eliminates markup transcribing errors and links office teams to site workers.",
         [
             "Sharing drawing files without merging active markup layers first",
             "Neglecting font catalog differences causing text reflow errors"
         ]),
        ("Offline Drawing Storage", 
         "Offline Drawing Storage caches drawing files in local device memory for access without network.",
         "Enables site reviews in remote areas or basement structures with weak signals.",
         [
             "Forgetting to load files while online before traveling to offline sites",
             "Making offline edits that conflict with updates made by other team members"
         ])
    ],
    "dwg-fastview-plus": [
        ("Fidelity QA Viewer", 
         "Fidelity QA Viewer opens drawings with high accuracy, letting users check layers and measure dimensions.",
         "Provides a safe QA review environment without risks of accidental geometry modifications.",
         [
             "Failing to verify scale settings before taking layout measurements",
             "Using outdated viewer versions that do not support recent DWG formats"
         ]),
        ("Batch Plotting Utility", 
         "Batch Plotting Utility publishes batches of DWG files to PDF or print formats simultaneously.",
         "Saves release coordination time and enforces consistent plot scaling across drawings.",
         [
             "Applying incorrect CTB plot styles to batch lists causing thin lines",
             "Publishing layouts with unlocked viewports, causing scale shifts"
         ]),
        ("Markup Layer Merge", 
         "Markup Layer Merge aggregates markup entries from multiple reviewers into a unified sheet database.",
         "Simplifies change management and provides a clean record of requested revisions.",
         [
             "Merging conflicting markups without resolving discrepancy first",
             "Orphaning annotations by changing the underlying base drawing coordinates"
         ])
    ],
    "fastview-3d": [
        ("3D Format Import", 
         "3D Format Import loads solid modeling formats like STEP, Parasolid, and IGES into the viewer.",
         "Simplifies mechanical review by allowing non-CAD seats to view complex assembly files.",
         [
             "Importing giant solid assemblies without turning on level-of-detail optimization",
             "Losing sub-component associations after moving folders"
         ]),
        ("Geometric Measurement Suite", 
         "Geometric Measurement Suite evaluates distances, diameters, angles, and volumes directly on solid objects.",
         "Provides manufacturing teams with accurate dimension details for QA assessments.",
         [
             "Measuring off mesh approximations instead of the true mathematical boundary geometry",
             "Forgetting to calibrate unit offsets before taking final dimensions"
         ]),
        ("Exploded Assembly Views", 
         "Exploded Assembly Views separate components along linear paths, exposing hidden parts.",
         "Creates clear visual instructions for manufacturing assembly lines.",
         [
             "Exploding components along axes that collide with other objects",
             "Neglecting to save exploded view states for documentation exports"
         ])
    ],
    "archicad": [
        ("OpenBIM and IFC Collaboration", 
         "OpenBIM and IFC Collaboration supports coordination using buildingSMART specifications, mapping elements accurately.",
         "Fosters multi-discipline collaboration without requiring standard software monocultures.",
         [
             "Using incorrect IFC translator settings causing parameter loss",
             "Forgetting to align project origins during cross-platform model setup"
         ]),
        ("Smart Building Elements", 
         "Smart Building Elements model walls, columns, and slabs with parametric boundaries and semantic attributes.",
         "Generates accurate 2D plans and quantities automatically since data is linked to elements.",
         [
             "Exploding building elements into basic shapes to solve simple graphic overrides",
             "Creating elements on incorrect home story levels causing model errors"
         ]),
        ("Publisher Sets", 
         "Publisher Sets automate the export of plans, views, and IFC models to various formats simultaneously.",
         "Standardizes document handoff and ensures that all project deliverables stay synchronized.",
         [
             "Publishing drawing sheets with outdated layout references",
             "Excluding necessary model sheets from the master publisher checklist"
         ])
    ]
}

FAQS = {
    "gstarcad-mechanical": [
        ("How do I update the Part List after changing geometry?", "Run the `MCAD_UPDPART` command or select the BOM table and click Refresh. The system will automatically scan the drawing attributes and update the schedule."),
        ("Can I import standard parts from other catalogs?", "Yes, standard parts can be imported via the catalog manager. You can load custom ISO, DIN, and JIS standard libraries."),
        ("How to customize title blocks in GstarCAD Mechanical?", "Edit the template file under the configuration path. Modify the attributes within the title block block definition to bind them to your company standard properties.")
    ],
    "gstarcad-architecture": [
        ("How do I create custom wall styles?", "Open the Style Manager, select Wall Styles, click New, define wall layers (material, thickness, offset), and save the style to your templates."),
        ("Can I generate 3D models from 2D architectural plans?", "Yes. Wall, door, and window elements in GstarCAD Architecture are intelligent 3D elements that automatically render in 3D when switching the viewpoint."),
        ("How do I export architectural models to IFC?", "Use the `IFCEXPORT` command, map GstarCAD Architecture layers to standard IFC classes, and save the coordinates relative to the project base point.")
    ],
    "gstarcad-point-cloud": [
        ("What format of point clouds does GstarCAD Point Cloud support?", "It supports standard formats like LAS, PTS, PTX, and RCP/RCS after conversion. Check the import options for details."),
        ("How do I trace outlines on a sliced point cloud?", "Set a section box or clip plane to isolate a slice of data, then use standard object snaps (`OSNAP`) and polyline tools to trace boundaries."),
        ("How to optimize viewport navigation for massive point cloud files?", "Reduce the point display density in the properties panel, or turn on hardware acceleration under options to utilize GPU caching.")
    ],
    "gstarcad-365": [
        ("How do I share a drawing link with external clients?", "Select the file in the project manager, click Share, set permissions (view-only or edit-enabled), set expiration date, and copy the link."),
        ("Can I view version history and restore old revisions?", "Yes, GstarCAD 365 maintains a complete activity log. You can compare any two version revisions visually and restore older versions as the active drawing master."),
        ("Does GstarCAD 365 support offline editing?", "Yes, drawings can be checked out for offline work. Once you reconnect, changes are merged back as a new revision.")
    ],
    "gstarbim": [
        ("How do I align BIM coordinate systems with standard DWG files?", "Use the Project Base Point tool to register the origin coordinates and rotation angle relative to the survey point before starting modeling."),
        ("What IFC schemas are supported for export in GstarBIM?", "GstarBIM supports IFC2x3 and IFC4 schemas. Choose the coordination view template recommended by your project team."),
        ("Can I create schedules that update automatically?", "Yes, BIM schedules are linked to object metadata. Modifying doors, walls, or windows updates the quantities in real time.")
    ],
    "houseplan": [
        ("How do I export Houseplan files to GstarCAD?", "Use the Export command and select DWG format. Intelligent walls and massing elements will convert to standard 2D/3D entities."),
        ("Can I import custom material texture files?", "Yes, in the Material panel, add a new material and browse to import PNG/JPG files for diffuse and normal mappings."),
        ("How to create visual animations of the 3D model in Houseplan?", "Set up multiple camera viewpoints along a path, and click Export Video in the presentation panel to render a walk-through.")
    ],
    "dwg-fastview": [
        ("How to use markup tools on mobile devices?", "Open a drawing, select Edit mode, choose the markup toolbar, and use your finger or stylus to draw clouds, text annotations, or linear dimensions."),
        ("Can I view CAD drawing files when my device is offline?", "Yes. Open the drawing file while online to cache it in local memory, or manually download it to the Offline tab for disconnected work."),
        ("How to sync annotations with the office team?", "Save the annotated drawing back to the cloud space. Other team members will receive notifications and see markups instantly.")
    ],
    "dwg-fastview-plus": [
        ("What are the advantages of FastView Plus over standard FastView?", "FastView Plus is a high-performance Windows desktop application designed to handle extremely large DWG assemblies and run batch plotting and audit diagnostics."),
        ("How do I configure batch printing with specific plot styles?", "Open the Batch Plot utility, select multiple drawings, load your enterprise `.ctb` file, select target printer/PDF generator, and run."),
        ("Can I merge markups from different team members in FastView Plus?", "Yes. FastView Plus can load multiple markup layers on top of a single base drawing, allowing you to merge annotations into a master revision list.")
    ],
    "fastview-3d": [
        ("What formats can 3D FastView import?", "It imports STEP, IGES, SAT, Parasolid (x_t), SolidWorks, Creo, Inventor, and CATIA formats."),
        ("How do I measure the exact clearance between assembly parts?", "Select two elements, click Clearance in the Measure tab, and the tool will show the shortest linear distance and highlight intersections."),
        ("Can I generate exploded animation files in 3D FastView?", "Yes. Select the assembly node, click Exploded View, adjust displacement coordinates along axes, and export the view sequence.")
    ],
    "archicad": [
        ("How do I configure hotlinked modules in Archicad?", "Go to File > External Content > Place Hotlinked Module, select the source file (PLN or MOD), and configure translation and layer options."),
        ("What is the best way to export IFC files for Revit coordination?", "Use the built-in 'Export to Revit' IFC translator, which optimizes Archicad classification mappings to Revit category classes."),
        ("How do I automate layout numbering in Publisher Sets in Archicad?", "Use Archicad's Auto-Text templates in your Master Layouts. The layout book will automatically sequence sheet numbers during publish.")
    ]
}

def main():
    if not KB_JSON.is_file():
        print(f"Error: {KB_JSON} not found.")
        return 1

    kb_data = json.loads(KB_JSON.read_text(encoding="utf-8"))
    items = kb_data.get("items") or []

    migrated_count = 0

    for it in items:
        slug = it["slug"]
        sw_file = SW_DIR / f"{slug}.json"
        
        # We only migrate if the sw detail json file does not exist
        if not sw_file.is_file():
            print(f"Migrating {slug}...")
            
            # Fetch metadata from kb_software.json
            name = it["name"]
            tagline = it.get("tagline", "")
            summary = it.get("summary", "")
            category_label = it.get("category_label", "DesignApplication")
            vendor_name = it.get("vendor_name", "Gstarsoft")
            vendor_slug = it.get("vendor_slug", "gstarsoft")
            outputs = it.get("typical_outputs", ["DWG", "PDF"])
            domains = it.get("typical_domains", [])
            
            terms = []
            if slug in DRAFTS:
                for idx, (title, definition, why_matters, pitfalls) in enumerate(DRAFTS[slug], 1):
                    term_slug = f"{slug}-term-{idx}"
                    cleaned_def = clean_cliches(definition)
                    
                    # Generate quiz
                    quiz_q = f"When working with {title}, which of the following represents a common technical pitfall?"
                    quiz_options = [
                        f"{pitfalls[0]}.",
                        "Failing to manually re-index the SQL server database.",
                        "Over-allocating virtual memory caches in the cloud settings.",
                        "Restricting linetype scales strictly to 1:1 paper coordinates."
                    ]
                    
                    terms.append({
                        "slug": term_slug,
                        "title": title,
                        "short_def": f"Technical best practices for {title} inside {name}.",
                        "definition": cleaned_def,
                        "why_matters": clean_cliches(why_matters),
                        "common_pitfalls": pitfalls,
                        "related_term_slugs": [],
                        "quiz": [
                            {
                                "question": quiz_q,
                                "options": quiz_options,
                                "answer_idx": 0,
                                "explanation": f"Correct. A common pitfall is '{pitfalls[0]}.' As the editorial review notes: '{why_matters}'"
                            }
                        ]
                    })
                    
            faqs = []
            if slug in FAQS:
                for q, a in FAQS[slug]:
                    faqs.append({
                        "question": q,
                        "answer": a
                    })
                    
            sw_dict = {
                "schema_version": "1.0",
                "slug": slug,
                "name": name,
                "tagline": tagline,
                "meta_desc": summary,
                "category_label": category_label,
                "vendor": {
                    "name": vendor_name,
                    "slug": vendor_slug
                },
                "platforms": ["Windows"],
                "file_formats": outputs,
                "domains": domains,
                "profile": {
                    "introduction": summary
                },
                "terms": terms,
                "faqs": faqs
            }
            
            # Write to data/sw/
            sw_file.write_text(json.dumps(sw_dict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            migrated_count += 1
            print(f"Created {sw_file.name} with {len(terms)} terms and {len(faqs)} FAQs.")

    print(f"Migrated {migrated_count} products.")
    return 0

if __name__ == "__main__":
    exit(main())
