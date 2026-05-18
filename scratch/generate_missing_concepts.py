import os

root_dir = r'f:\CAD-tutorial'
concepts_dir = os.path.join(root_dir, 'kb', 'concepts')
os.makedirs(concepts_dir, exist_ok=True)

# Missing concepts metadata dictionary: (Title, Description, Subtitle, Highlights list)
missing_metadata = {
    "aec-object-style": (
        "AEC Object Style",
        "Parameters that drive architectural wall, slab, stair, and smart element definitions.",
        "Smart architectural styles for dynamic building plan and section generation.",
        [
            ("Style Parameters", "Control materials, plan representation, and 3D height settings dynamically."),
            ("DWG Export flattening", "Plan exports to plain DWG carefully, as smart elements will flatten to lines."),
            ("Property sets", "Attach custom metadata for construction takeoff and bim schedules.")
        ]
    ),
    "api-automation": (
        "API & Custom Automation",
        "Leveraging GRX, .NET, LISP, and script files to automate CAD drafting and customization.",
        "Unlock efficiency by scripting repetitive tasks and building custom add-ins.",
        [
            ("LISP scripts", "The historical standard for fast macro writing and command chaining."),
            ("GRX/ARX SDKs", "Compile high-performance C++ plugins that load natively into CAD engines."),
            ("System customization", "Distribute workspace CUI profiles and automated startup scripts across teams.")
        ]
    ),
    "bim": (
        "Building Information Modeling (BIM)",
        "Building Information Modeling: a collaborative process to model and manage physical/functional building data.",
        "A rich data-driven process that spans design, construction, and operations.",
        [
            ("Geometry + Data", "Not just 3D models—every object contains classification, cost, and lifecycle metadata."),
            ("Clash detection", "Coordinate structures and services early to eliminate field construction errors."),
            ("Interoperability", "Utilize open standards like IFC to bridge different design applications.")
        ]
    ),
    "command-alias": (
        "Command Aliases (PGP)",
        "Keyboard shortcuts to commands, bridging muscle memory when transitioning between CAD platforms.",
        "Accelerate your drafting speeds by customizing standard keyboard triggers.",
        [
            ("PGP Configuration", "Edit the standard parameter file to add custom command aliases."),
            ("Muscle Memory", "Maintain consistent shortcuts when shifting between AutoCAD and GstarCAD."),
            ("Workflow speed", "Draft two-handed: left hand on the keyboard, right hand on the pointer.")
        ]
    ),
    "data-extraction": (
        "Data Extraction",
        "Exporting attribute data, geometry property lists, and part metadata directly into schedules.",
        "Transform raw CAD drawings into quantitative schedules and spreadsheets automatically.",
        [
            ("Attribute extraction", "Collect tags, blocks, and user data fields from hundreds of sheets."),
            ("Dynamic schedules", "Link extractions to active table objects that refresh as design updates."),
            ("BOM generation", "Export directly to CSV or Excel templates to feed ERP and PDM tools.")
        ]
    ),
    "dwg-compatibility": (
        "DWG Compatibility Mode",
        "The standard for cross-platform file reading, font substitutes, proxy objects, and scale lists.",
        "Ensure seamless DWG drawing exchange across different vendor platforms.",
        [
            ("Bit-for-bit fidelity", "Verify font libraries, xref scales, and standard layer states during transition."),
            ("Proxy objects", "Handle vendor-specific custom geometries without losing detail or stability."),
            ("Purging scale lists", "Clean heavy scale metadata to prevent drawing slow-downs in external files.")
        ]
    ),
    "large-assembly": (
        "Large Assembly Viewing",
        "Performance optimization settings for handling heavy 3D CAD models and spatial coordinate scopes.",
        "Optimize viewport speed and navigate huge multi-discipline models effortlessly.",
        [
            ("Level of Detail (LOD)", "Reduce geometric fidelity on distant objects to boost frames per second."),
            ("Clipping planes", "Focus only on relevant sections to speed up rendering calculations."),
            ("GPU acceleration", "Utilize certified graphics drivers to maximize viewport panning performance.")
        ]
    ),
    "licensing": (
        "CAD Licensing Models",
        "Understanding standard CAD license tiers: Perpetual, subscription, network, and offline nodes.",
        "Make informed corporate deployment decisions across diverse vendor options.",
        [
            ("Perpetual licenses", "Own the software version forever with optional yearly maintenance."),
            ("Network sharing", "Use a central flex server to float license seats across engineering teams."),
            ("Offline nodes", "Activate nodes for use in remote field operations without internet access.")
        ]
    ),
    "markup-workflow": (
        "DWG FastView Markup",
        "Digital annotation, dimension overlays, and collaborative redlines in viewer clients.",
        "Enable frictionless drawing review loops between the field and the office.",
        [
            ("Mobile redlines", "Draw circles, clouds, and text directly on drawing sheets via portable tablet screens."),
            ("Non-destructive layers", "Markups are saved as review layers without mutating the original DWG base."),
            ("Real-time sync", "Instantly push field measurements back to draftspeople in the design studio.")
        ]
    ),
    "mechanical-bom": (
        "Mechanical Bill of Materials (BOM)",
        "Parts lists, bubble annotations, and smart quantity scheduling in mechanical drafting.",
        "Drive production precision by linking geometry to live part tables.",
        [
            ("Parts lists", "Generate structured schedules directly from annotated assembly components."),
            ("Balloon callouts", "Place associative bubbles that track standard catalog part numbers."),
            ("ERP system sync", "Export clean material lists to maintain seamless inventory coordination.")
        ]
    ),
    "objectarx-sdk": (
        "ObjectARX C++ SDK",
        "The native C++ API used for compiling advanced CAD extensions, tools, and smart objects.",
        "Extend CAD engines to build highly customized enterprise vertical applications.",
        [
            ("Native performance", "Execute complex algorithms with the speed of compiled native C++."),
            ("Custom smart objects", "Define geometric entities that behave with proprietary custom logic."),
            ("Cross-platform migration", "Port code between AutoCAD ObjectARX and GstarCAD GRX APIs with minimal edit.")
        ]
    ),
    "pdf-underlay": (
        "PDF Underlays",
        "Attaching vector and raster PDFs behind active drawings for tracing, reference, or coordination.",
        "Use external reference sheets as a drafting backdrop without converting files.",
        [
            ("Vector snapping", "Snap directly to vector lines inside the attached PDF underlay."),
            ("Scale matching", "Scale the underlay using reference points to match model coordinate space."),
            ("Performance weight", "Clip large PDFs to focus viewport resources on active drafting regions.")
        ]
    ),
    "subassembly-composer": (
        "Subassembly Composer",
        "Visual workflow builder for creating custom, parameter-driven corridor sections in civil software.",
        "Build rich, intelligent road and utility corridor cross-sections visually.",
        [
            ("Flowchart design", "Design custom geometry logic using intuitive drag-and-drop flowchart tools."),
            ("Decision logic", "Incorporate targets and conditions to handle slopes and cut/fill variables."),
            ("Reusable PKT files", "Export compiled corridor assemblies to share parameters across teams.")
        ]
    ),
    "sysvar": (
        "System Variables (SYSVAR)",
        "Global configuration properties that dictate snaps, file paths, views, and engine parameters.",
        "Fine-tune your drafting workspace environment using system-wide variables.",
        [
            ("Workspace configuration", "Modify snap behaviors, tracking settings, and default save formats."),
            ("Profile exports", "Back up your system variables to easily migrate workspace layouts."),
            ("Startup scripts", "Force specific sysvar states on drawing load to maintain office standards.")
        ]
    ),
    "tolerance": (
        "Tolerance & Manufacturing Limits",
        "Allowed dimensional variations required to ensure physical part manufacturing and assembly fit.",
        "Bridge the gap between digital CAD precision and physical manufacturing limits.",
        [
            ("Dimensional limits", "Define high and low limits to ensure inter-operating assembly fit."),
            ("GD&T symbols", "Incorporate Geometric Dimensioning and Tolerancing symbols for precise intent."),
            ("Production quality", "Match tolerance levels to mechanical machine shop capabilities.")
        ]
    )
}

template = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} · CAD Concepts · LearnCAD</title>
    <meta name="description" content="{description}" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="stylesheet" href="../../styles.css?v=v6_faq_graph_perfection" />
  </head>
  <body data-page="knowledge" class="page-kb-concepts">
    <div class="header-stack">
      <aside class="site-notice" id="site-notice" data-notice-id="global-v2" aria-label="Announcement">
        <div class="site-notice-inner container">
          <p class="site-notice-text">
            Tip: open the <a class="site-notice-link" href="../../tutorials.html">tutorial library</a> to filter by software, task, level, and source—then follow outbound links to the originals.
          </p>
          <button type="button" class="site-notice-close" aria-label="Dismiss announcement">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      </aside>
      <header class="topbar">
        <div class="container topbar-inner">
          <a class="brand" href="../../index.html">
            <span class="brand-badge">LC</span>
            <span>LearnCAD</span>
          </a>
          <nav class="nav">
            <a class="nav-link" href="../../index.html">Home</a>
            <a class="nav-link" href="../../knowledge-base.html">Knowledge Base</a>
            <a class="nav-link" href="../../tutorials.html">Tutorials</a>
            <a class="nav-link" href="../../news.html">News</a>
          </nav>
        </div>
      </header>
    </div>

    <main class="container" style="margin-top: 32px; max-width: 900px;">
      <nav class="kb-faq-breadcrumbs" aria-label="Breadcrumb">
        <a href="../../index.html">Home</a> /
        <a href="../../knowledge-base.html">Knowledge Base</a> /
        <a href="../../kb-terms.html">Terms</a> /
        <span aria-current="page">{title}</span>
      </nav>

      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 40px; border-bottom: 1px solid #e2e8f0; padding-bottom: 24px;">
          <span class="chip" style="margin-bottom: 12px; background: #fef3c7; color: #92400e; border-color: #fde68a;">Atomic Knowledge</span>
          <h1 style="font-size: 2.5rem; margin-bottom: 12px; color: #0f172a;">{title}</h1>
          <p class="hero-sub" style="font-size: 1.2rem; color: #475569;">{subtitle}</p>
        </header>

        <section class="kb-concept-section" style="margin-bottom: 48px;">
          <h2 style="font-size: 1.5rem; margin-bottom: 16px; color: #1e293b; border-left: 4px solid #d97706; padding-left: 12px;">Core Definition</h2>
          <p style="line-height: 1.7; color: #334155; font-size: 1.05rem;">{description}</p>
        </section>

        <section class="kb-concept-section" style="margin-bottom: 48px; background: #f8fafc; padding: 24px; border-radius: 16px; border: 1px solid #e2e8f0;">
          <h2 style="font-size: 1.3rem; margin-bottom: 16px; color: #1e293b;">Key Dimensions</h2>
          <ul style="display: grid; gap: 16px; padding-left: 0; list-style-type: none; color: #475569;">
            {list_items}
          </ul>
        </section>
      </article>
    </main>

    <footer class="footer site-footer">
      <div class="container">
        <p>© 2026 LearnCAD · Knowledge Base</p>
      </div>
    </footer>
    <script src="../../app.js" defer></script>
  </body>
</html>
"""

for name, (title, description, subtitle, highlights) in missing_metadata.items():
    list_items = ""
    for item_title, item_desc in highlights:
        list_items += f'            <li><strong>{item_title}:</strong> {item_desc}</li>\n'
    
    file_content = template.format(
        title=title,
        description=description,
        subtitle=subtitle,
        list_items=list_items.rstrip()
    )
    
    file_path = os.path.join(concepts_dir, f"{name}.html")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
    print(f"Generated missing concept page: {file_path}")

print("All missing concept pages generated successfully!")
