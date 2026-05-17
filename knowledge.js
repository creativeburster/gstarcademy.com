if (document.body.getAttribute("data-page") === "knowledge") {
  const graphPanelDefaultTitle = () =>
    (document.documentElement.getAttribute("lang") || "")
      .toLowerCase()
      .startsWith("zh")
      ? "Selected Node Info"
      : "Knowledge Graph Panel";
  /* v2: default expanded; older collapsed prefs intentionally not carried over */
  const KB_RAIL_LS = "cad-kb-rail-collapsed-v2";
  const kbApp = document.getElementById("kb-app");
  const kbRail = document.getElementById("kb-rail");
  const kbRailToggle = document.getElementById("kb-rail-toggle");

  const applyKbRailCollapsed = (collapsed) => {
    if (!kbApp || !kbRail) return;
    kbApp.classList.toggle("kb-sidebar-collapsed", collapsed);
    try {
      localStorage.setItem(KB_RAIL_LS, collapsed ? "1" : "0");
    } catch (_) {
      /* ignore */
    }
    if (kbRailToggle) {
      kbRailToggle.setAttribute("aria-expanded", collapsed ? "false" : "true");
      kbRailToggle.title = collapsed
        ? "Show navigation"
        : "Hide navigation (wider reading)";
      const icon = kbRailToggle.querySelector(".kb-rail-toggle-icon");
      if (icon) icon.textContent = collapsed ? "▶" : "◀";
      const sr = kbRailToggle.querySelector(".kb-sr-only");
      if (sr)
        sr.textContent = collapsed
          ? "Expand navigation sidebar"
          : "Collapse navigation sidebar";
    }
  };

  let startCollapsed = false;
  try {
    startCollapsed = localStorage.getItem(KB_RAIL_LS) === "1";
  } catch (_) {
    /* ignore */
  }
  applyKbRailCollapsed(startCollapsed);

  kbRailToggle?.addEventListener("click", () => {
    const next = !kbApp.classList.contains("kb-sidebar-collapsed");
    applyKbRailCollapsed(next);
  });

  // collapsible sidebar groups - Default to Expanded
  document.querySelectorAll(".kb-nav-toggle").forEach((btn) => {
    const links = btn.nextElementSibling;
    // Force expand on init
    btn.setAttribute("aria-expanded", "true");
    links?.classList.remove("kb-collapsed");

    btn.addEventListener("click", () => {
      const expanded = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!expanded));
      links.classList.toggle("kb-collapsed", expanded);
    });
  });

  const searchInput = document.getElementById("kb-sidebar-search");
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      const q = searchInput.value.trim().toLowerCase();
      document.querySelectorAll(".kb-index-link").forEach((a) => {
        const t = a.textContent.toLowerCase();
        a.style.display = !q || t.includes(q) ? "" : "none";
      });
    });
  }

  // anchor highlight (same-page sections only; subnav uses separate HTML files)
  const anchorLinks = document.querySelectorAll("[data-kb-anchor]");
  const targets = Array.from(anchorLinks)
    .map((a) => {
      const href = a.getAttribute("href") || "";
      if (!href.startsWith("#")) return null;
      return document.querySelector(href);
    })
    .filter(Boolean);
  const setActiveAnchor = (id) => {
    anchorLinks.forEach((a) =>
      a.classList.toggle("active", a.getAttribute("href") === `#${id}`)
    );
  };
  if (targets.length) {
    const io = new IntersectionObserver(
      (entries) => {
        const v = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (v?.target?.id) setActiveAnchor(v.target.id);
      },
      { rootMargin: "-20% 0px -60% 0px", threshold: [0.1, 0.35, 0.6] }
    );
    targets.forEach((t) => io.observe(t));
  }

  // right info panel
  const infoTitle = document.getElementById("kbInfoTitle");
  const infoDesc = document.getElementById("kbInfoDesc");
  const infoRelated = document.getElementById("kbInfoRelated");
  const infoPath = document.getElementById("kbInfoPath");
  const setInfo = (title, desc, related = [], path = []) => {
    if (infoTitle) infoTitle.textContent = title || graphPanelDefaultTitle();
    if (infoDesc) infoDesc.textContent = desc || "";
    if (infoRelated) {
      infoRelated.innerHTML = "";
      (related.length ? related : ["No linked nodes"]).forEach((r) => {
        const s = document.createElement("span");
        s.className = "kb-tag kb-static";
        s.textContent = r;
        infoRelated.appendChild(s);
      });
    }
    if (infoPath && path.length) {
      infoPath.innerHTML = "";
      path.forEach((step) => {
        const li = document.createElement("li");
        li.textContent = step;
        infoPath.appendChild(li);
      });
    }
  };

  // cards click -> info panel
  const cards = document.querySelectorAll(".kb-detail-card[data-tags]");
  cards.forEach((card) => {
    card.addEventListener("click", () => {
      setInfo(
        card.dataset.title,
        `${card.dataset.desc || ""} ${card.dataset.extra || ""}`.trim(),
        (card.dataset.tags || "").split(" ").filter(Boolean).slice(0, 6)
      );
    });
  });

  // graph setup (SVG + D3 when available; sidebar filters still run without graph)
  const graphSvgRoot = document.getElementById("kbGraphSvg");
  const graphStage = document.getElementById("kbGraphStage");
  const pathBtn = document.getElementById("kbPathToggle");
  const filterButtons = document.querySelectorAll(".kb-tag[data-filter]");
  let activeFilter = "all";
  let pathMode = false;
  /** @type {() => void} */
  let refreshKbGraphPresentation = () => {};



  /**
   * Taxonomy logic (WordPress-like Categories & Tags)
   * Injected dynamically to keep sidebars in sync with knowledge base nodes
   */
  function initKbSidebarTaxonomy() {
    const rail = document.getElementById("kb-rail");
    if (!rail) return;

    const indexBox = rail.querySelector(".kb-index-box");
    if (!indexBox) return;

    // Clear old dynamic groups to prevent duplication on re-init
    rail.querySelectorAll(".kb-nav-group-dynamic").forEach(el => el.remove());

    const categories = {}; // grouping by 'type'
    const themes = {};     // grouping by individual tags

    nodes.forEach(n => {
      // Grouping by category (Type)
      const cat = n.type || "concept";
      if (!categories[cat]) categories[cat] = [];
      categories[cat].push(n.id);

      // Grouping by themes (Tags)
      (n.tags || []).forEach(t => {
        if (!themes[t]) themes[t] = [];
        themes[t].push(n.id);
      });
    });

    const createGroup = (title, itemsMap) => {
      const group = document.createElement("div");
      group.className = "kb-nav-group kb-nav-group-dynamic";
      
      const btn = document.createElement("button");
      btn.className = "kb-nav-toggle";
      btn.setAttribute("aria-expanded", "true");
      btn.textContent = title;
      
      const list = document.createElement("div");
      list.className = "kb-nav-links";
      
      Object.keys(itemsMap).sort().forEach(key => {
        const a = document.createElement("a");
        a.className = "kb-side-link";
        const count = itemsMap[key].length;
        // Clicking a category/tag links to the graph with a filter parameter
        a.href = `./kb-graph.html?filter=${encodeURIComponent(key)}`;
        a.innerHTML = `<span>${key.charAt(0).toUpperCase() + key.slice(1)}</span> <small style="opacity:0.6; font-size:0.8em;">(${count})</small>`;
        list.appendChild(a);
      });

      group.appendChild(btn);
      group.appendChild(list);

      // Simple toggle event for the newly created button
      btn.addEventListener("click", () => {
        const expanded = btn.getAttribute("aria-expanded") === "true";
        btn.setAttribute("aria-expanded", String(!expanded));
        list.classList.toggle("kb-collapsed", expanded);
      });

      return group;
    };

    // Insert tag-based "Themes" first, then type-based "Categories"
    const tagGroup = createGroup("Themes (By Tag)", themes);
    const catGroup = createGroup("Categories (By Type)", categories);

    indexBox.after(tagGroup);
    indexBox.after(catGroup);
  }

  const nodes = [
    {
      id: "CAD Basics",
      type: "concept",
      tags: ["concepts", "beginner"],
      descZh: "",
      hint: "Foundations: units, views, and drawing discipline before any app war.",
    },
    {
      id: "Terminology",
      type: "concept",
      tags: ["terms", "beginner"],
      descZh: "",
      hint: "Names for objects, commands, and industry slang you will keep meeting.",
    },
    {
      id: "2D Drafting",
      type: "concept",
      tags: ["2d", "beginner"],
      descZh: "",
      hint: "Plans, sections, dimensions—release-ready 2D storytelling.",
    },
    {
      id: "3D Modeling",
      type: "concept",
      tags: ["3d", "beginner"],
      descZh: "",
      hint: "Solids, surfaces, assemblies—the shape side of mechanical & BIM stacks.",
    },
    {
      id: "Command Line",
      type: "skill",
      tags: ["terms", "beginner", "2d"],
      descZh: "",
      hint: "Typing commands + aliases—still the fast path in many CADs.",
    },
    {
      id: "File Formats",
      type: "skill",
      tags: ["terms", "concepts"],
      descZh: "",
      hint: "Neutral carriers (DWG/DXF/STEP/IFC) for handoff between teams.",
    },
    { id: "AEC", type: "domain", tags: ["aec"], hint: "Built-environment workflows: docs, coordination, fabrication packages." },
    { id: "MFG", type: "domain", tags: ["mfg"], hint: "Mechanical/mfg context: tolerances, BOM, production intent." },
    { id: "BIM", type: "domain", tags: ["aec", "3d"], hint: "Shared model + data for multi-discipline buildings & infrastructure." },
    { id: "DWG", type: "format", tags: ["terms", "2d"], hint: "Dominant 2D CAD exchange; native to many vendors’ stacks." },
    { id: "STEP", type: "format", tags: ["terms", "3d", "mfg"], hint: "Precise 3D solids/surfaces—common between MCAD and CAM." },
    { id: "IFC", type: "format", tags: ["terms", "aec"], hint: "Open BIM schema for interoperable building models." },
    {
      id: "Software Map",
      type: "resource",
      tags: ["concepts"],
      descZh: "",
      hint: "On-site page listing product families + where to drill next.",
    },
    {
      id: "Learning branch",
      type: "resource",
      tags: ["beginner"],
      descZh: "",
      hint: "Pedagogical fork inside this visualization (not gamified Paths).",
    },
    {
      id: "Autodesk",
      type: "vendor",
      tags: ["terms", "aec", "mfg"],
      descZh: "",
      hint: "Major ISV umbrella: AutoCAD, Revit, Inventor, Civil 3D, Fusion …",
    },
    {
      id: "AutoCAD",
      type: "product",
      tags: ["2d", "aec", "terms"],
      descZh: "",
      hint: "DWG authoring platform ubiquitous in AEC + general drafting.",
    },
    {
      id: "Revit",
      type: "product",
      tags: ["aec", "3d", "terms"],
      descZh: "",
      hint: "BIM authoring for buildings—discipline-linked models.",
    },
    {
      id: "Gstarsoft",
      type: "vendor",
      tags: ["terms", "concepts"],
      descZh: "",
      hint: "Suzhou ISV publishing GstarCAD + DWG FastView for cross-platform viewers.",
    },
    {
      id: "GstarCAD",
      type: "product",
      tags: ["2d", "3d", "terms"],
      descZh: "",
      hint: "Desktop CAD suite from Gstarsoft—DWG-native OEM stack.",
    },
    {
      id: "DWG FastView",
      type: "product",
      tags: ["2d", "terms"],
      descZh: "",
      hint: "Lightweight/mobile DWG collaboration product line from Gstarsoft.",
    },
    {
      id: "DWG Compare",
      type: "skill",
      tags: ["2d", "gstarcad"],
      descZh: "",
      hint: "Review tool to diff two drawings—highlights adds, deletes, and shared geometry.",
    },
    {
      id: "Parametric Constraints",
      type: "skill",
      tags: ["3d", "gstarcad", "concepts"],
      descZh: "",
      hint: "Geometric and dimensional rules linked to variables (Parameters Manager).",
    },
    {
      id: "Drawing Merge",
      type: "skill",
      tags: ["2d", "gstarcad"],
      descZh: "",
      hint: "Consolidate multiple project files into one master DWG.",
    },
    {
      id: "Grasshopper",
      type: "skill",
      tags: ["aec", "3d", "terms"],
      descZh: "",
      hint: "Visual scripting riding on Rhino—used heavily in exploratory geometry.",
    },
    {
      id: "CAD SDK ecosystem",
      type: "resource",
      tags: ["terms", "concepts"],
      descZh: "",
      hint: "Commercial SDKs: embed viewers, translate files, render 3D—not end-user CAD seats.",
    },
    {
      id: "Apryse CAD SDK",
      type: "sdk",
      tags: ["terms", "concepts"],
      descZh: "",
      hint: "Apryse Core SDK line—CAD + PDF-aware viewing/markup inside your application.",
    },
    {
      id: "HOOPS Visualize",
      type: "sdk",
      tags: ["terms", "3d", "mfg"],
      descZh: "",
      hint: "Tech Soft 3D graphics engine commonly used for interactive 3D CAD scenes.",
    },
    {
      id: "Datakit",
      type: "vendor",
      tags: ["terms", "concepts"],
      descZh: "",
      hint: "Interoperability ISV—format converters and CAD data APIs between stacks.",
    },
    { id: "Civil 3D", type: "product", tags: ["autodesk"], hint: "Infrastructure design and documentation." },
    { id: "Inventor", type: "product", tags: ["autodesk"], hint: "Mechanical design and 3D CAD software." },
    { id: "Fusion", type: "product", tags: ["autodesk"], hint: "Integrated CAD, CAM, and CAE platform." },
    { id: "Navisworks", type: "product", tags: ["autodesk"], hint: "Project review and coordination software." },
    { id: "GstarCAD Mechanical", type: "product", tags: ["gstarcad"], hint: "Specialized mechanical design toolkit." },
    { id: "GstarCAD Architecture", type: "product", tags: ["gstarcad"], hint: "Specialized architectural design toolkit." },
    { id: "Intelligent Objects", type: "skill", tags: ["gstarcad"], hint: "Custom architectural/mechanical components." },
    { id: "Mobile BIM", type: "skill", tags: ["gstarcad"], hint: "Viewing and editing BIM data on mobile." },
    { id: "Python API", type: "skill", tags: ["gstarcad"] },
    { id: "PyRx", type: "sdk", tags: ["gstarcad"] },
    { id: "Hardware Acceleration", type: "skill", tags: ["gstarcad"] },
    { id: "Smart Blocks", type: "skill", tags: ["autocad"] },
    { id: "Cloud Worksharing", type: "skill", tags: ["revit"] },
    { id: "Scan to BIM", type: "skill", tags: ["revit"] },
    { id: "Generative Design", type: "skill", tags: ["fusion"] },
    { id: "iLogic", type: "skill", tags: ["inventor"] },
    { id: "NWD/NWF", type: "skill", tags: ["navisworks"] },
    { id: "Grading Optimization", type: "skill", tags: ["civil3d"] },
    { id: "Sheet Set Manager", type: "skill", tags: ["gstarcad"] },
    { id: "Annotative Scaling", type: "skill", tags: ["gstarcad"] },
    { id: "GRX SDK", type: "sdk", tags: ["gstarcad"] },
    { id: "CUI Custom", type: "skill", tags: ["gstarcad"] },
    { id: "Data Link", type: "skill", tags: ["gstarcad"] },
    { id: "SuperHatch", type: "skill", tags: ["gstarcad"] },
    { id: "PDF to DWG", type: "skill", tags: ["gstarcad"] },
    { id: "Dassault", type: "vendor", tags: ["mfg", "aec", "terms"], hint: "Parent of CATIA, SOLIDWORKS, and DraftSight." },
    { id: "DraftSight", type: "product", tags: ["dassault"], hint: "Professional 2D CAD by Dassault." },
    { id: "PowerTrim", type: "skill", tags: ["draftsight"] },
    { id: "G-Code Gen", type: "skill", tags: ["draftsight"] },
    { id: "Mechanical Toolbox", type: "skill", tags: ["draftsight"] },
    { id: "3DEXPERIENCE", type: "product", tags: ["dassault"], hint: "Business innovation platform." },
    { id: "Image Tracer", type: "skill", tags: ["draftsight"] },
    { id: "DraftSight API", type: "sdk", tags: ["draftsight"] },
    { id: "Smart Blocks (DS)", type: "skill", tags: ["draftsight"] },
    { id: "Mech Symbols", type: "skill", tags: ["draftsight"] },
    { id: "Batch Print", type: "skill", tags: ["draftsight"] },
    { id: "Alias Custom", type: "skill", tags: ["draftsight"] },
    { id: "LISP (DS)", type: "skill", tags: ["draftsight"] },
    { id: "Xref (DS)", type: "skill", tags: ["draftsight"] },
    { id: "Properties (DS)", type: "skill", tags: ["draftsight"] },
    { id: "SSM (DS)", type: "skill", tags: ["draftsight"] },
    { id: "3D (DS)", type: "skill", tags: ["draftsight"] },
    { id: "Markup (DS)", type: "skill", tags: ["draftsight"] },
    { id: "Licensing (DS)", type: "skill", tags: ["draftsight"] },
    { id: "Perf Tuning", type: "skill", tags: ["draftsight"] },
    { id: "Interop (DS)", type: "skill", tags: ["draftsight"] },
    { id: "PTC", type: "vendor", tags: ["mfg", "terms"], hint: "Leader in parametric 3D CAD & PLM." },
    { id: "Creo Parametric", type: "product", tags: ["ptc"], hint: "Flagship 3D modeling software." },
    { id: "Windchill", type: "product", tags: ["ptc"], hint: "Enterprise PLM system." },
    { id: "Skeleton Modeling", type: "skill", tags: ["ptc"] },
    { id: "Flexible Modeling", type: "skill", tags: ["ptc"] },
    { id: "Regeneration Logic", type: "skill", tags: ["ptc"] },
    { id: "Mathcad", type: "product", tags: ["ptc"], hint: "Engineering calculation software." },
    { id: "MBD (PTC)", type: "skill", tags: ["ptc"] },
    { id: "Generative (PTC)", type: "skill", tags: ["ptc"] },
    { id: "Additive (PTC)", type: "skill", tags: ["ptc"] },
    { id: "Cabling (PTC)", type: "skill", tags: ["ptc"] },
    { id: "Piping (PTC)", type: "skill", tags: ["ptc"] },
    { id: "Sheetmetal (PTC)", type: "skill", tags: ["ptc"] },
    { id: "Mechanism (PTC)", type: "skill", tags: ["ptc"] },
    { id: "Sim Live (PTC)", type: "skill", tags: ["ptc"] },
    { id: "ISDX (PTC)", type: "skill", tags: ["ptc"] },
    { id: "TDD (PTC)", type: "skill", tags: ["ptc"] },
    { id: "Mapkeys (PTC)", type: "skill", tags: ["ptc"] },
    { id: "Config.pro (PTC)", type: "skill", tags: ["ptc"] },
    { id: "Simp Reps (PTC)", type: "skill", tags: ["ptc"] },
    { id: "Siemens", type: "vendor", tags: ["mfg", "terms"], hint: "Global leader in PLM and automation." },
    { id: "NX", type: "product", tags: ["siemens"], hint: "High-end CAD/CAM/CAE solution." },
    { id: "Solid Edge", type: "product", tags: ["siemens"], hint: "Mid-range CAD with Synchronous Tech." },
    { id: "Teamcenter", type: "product", tags: ["siemens"], hint: "World-leading PLM system." },
    { id: "Synchronous Tech", type: "skill", tags: ["siemens"] },
    { id: "WAVE Linker", type: "skill", tags: ["siemens"] },
    { id: "Simcenter", type: "product", tags: ["siemens"], hint: "Advanced engineering simulation." },
    { id: "Convergent Modeling", type: "skill", tags: ["siemens"] },
    { id: "PMI (Siemens)", type: "skill", tags: ["siemens"] },
    { id: "Active Workspace", type: "skill", tags: ["siemens"] },
    { id: "Check-Mate", type: "skill", tags: ["siemens"] },
    { id: "NX CAM", type: "skill", tags: ["siemens"] },
    { id: "NX MCD", type: "skill", tags: ["siemens"] },
    { id: "NX PTS", type: "skill", tags: ["siemens"] },
    { id: "NX Layout", type: "skill", tags: ["siemens"] },
    { id: "NX Mold Wizard", type: "skill", tags: ["siemens"] },
    { id: "NX Progressive Die", type: "skill", tags: ["siemens"] },
    { id: "Nastran", type: "skill", tags: ["siemens"] },
    { id: "Realize Shape", type: "skill", tags: ["siemens"] },
    { id: "NX Flow", type: "skill", tags: ["siemens"] },
    { id: "Multi-CAD (Siemens)", type: "skill", tags: ["siemens"] },
    { id: "NX Expressions", type: "skill", tags: ["siemens"] },
    { id: "HD3D", type: "skill", tags: ["siemens"] },
    { id: "Bentley", type: "vendor", tags: ["aec", "terms"], hint: "Leader in infrastructure engineering software." },
    { id: "MicroStation", type: "product", tags: ["bentley"], hint: "High-performance CAD for infrastructure." },
    { id: "OpenRoads", type: "product", tags: ["bentley"], hint: "Civil engineering and road design software." },
    { id: "ProjectWise", type: "product", tags: ["bentley"], hint: "Project information management for AEC." },
    { id: "iTwin", type: "product", tags: ["bentley"], hint: "Infrastructure digital twin platform." },
    { id: "DGN Format", type: "skill", tags: ["bentley"] },
    { id: "STAAD.Pro", type: "skill", tags: ["bentley"] },
    { id: "SYNCHRO", type: "skill", tags: ["bentley"] },
    { id: "WaterGEMS", type: "skill", tags: ["bentley"] },
    { id: "RAM Structural", type: "skill", tags: ["bentley"] },
    { id: "HAMMER", type: "skill", tags: ["bentley"] },
    { id: "LumenRT", type: "skill", tags: ["bentley"] },
    { id: "AssetWise", type: "skill", tags: ["bentley"] },
    { id: "SewerGEMS", type: "skill", tags: ["bentley"] },
    { id: "gINT", type: "skill", tags: ["bentley"] },
    { id: "AutoPIPE", type: "skill", tags: ["bentley"] },
    { id: "SACS", type: "skill", tags: ["bentley"] },
    { id: "ProSteel", type: "skill", tags: ["bentley"] },
    { id: "CONNECT Ed.", type: "skill", tags: ["bentley"] },
    { id: "iModels", type: "skill", tags: ["bentley"] },
    { id: "ContextCapture", type: "skill", tags: ["bentley"] },
    { id: "SOLIDWORKS", type: "product", tags: ["dassault"], hint: "Industry standard 3D parametric mechanical CAD." },
    { id: "CATIA", type: "product", tags: ["dassault"], hint: "Enterprise high-end PLM and advanced surfacing CAD." },
    { id: "ENOVIA", type: "product", tags: ["dassault"], hint: "Enterprise data governance & lifecycle PLM." },
    { id: "SIMULIA", type: "product", tags: ["dassault"], hint: "Unified advanced engineering simulation." },
    { id: "DELMIA", type: "product", tags: ["dassault"], hint: "Digital manufacturing & factory process simulation." },
    { id: "SOLIDWORKS PDM", type: "skill", tags: ["solidworks"], hint: "Version control & vault data management." },
    { id: "CATIA GSD", type: "skill", tags: ["catia"], hint: "Generative Shape Design aerospace surfacing." },
    { id: "CAA SDK", type: "sdk", tags: ["catia"], hint: "High-performance C++ developer interface." },
    { id: "SOLIDWORKS API", type: "sdk", tags: ["solidworks"], hint: ".NET & VBA custom automation." },
    { id: "SOLIDWORKS Configurations", type: "skill", tags: ["solidworks"], hint: "Multi-dimension design variants manager." },
    { id: "Abaqus", type: "skill", tags: ["simulia"], hint: "Advanced nonlinear structural FEA solver." },
    { id: "PowerCopy", type: "skill", tags: ["catia"], hint: "Feature-level template pattern reuse." },
    { id: "Hybrid Design", type: "skill", tags: ["catia"], hint: "Solid and surface mixed chronological modeling." },
    { id: "Composites Design", type: "skill", tags: ["catia"], hint: "Carbon-fiber ply layup & draping simulation." },
    { id: "FT&A MBD", type: "skill", tags: ["catia"], hint: "Functional tolerancing & drawingless 3D annotations." },
    { id: "SpeedPak", type: "skill", tags: ["solidworks"], hint: "Large assembly high-speed graphics subset." },
    { id: "eDrawings", type: "skill", tags: ["solidworks"], hint: "Lightweight multi-CAD collaborative viewer." },
    { id: "Collaborative Sharing", type: "skill", tags: ["3dexperience"], hint: "Cloud co-authoring workspace governance." },
    { id: "Large Design Review", type: "skill", tags: ["solidworks"], hint: "Ultra-fast large assembly visualization & review." },
    { id: "Weldments (SW)", type: "skill", tags: ["solidworks"], hint: "Structural steel frames & cut lists." },
    { id: "Sheet Metal (SW)", type: "skill", tags: ["solidworks"], hint: "Folded part stretch & unfold pattern checks." },
    { id: "Part Design (CATIA)", type: "skill", tags: ["catia"], hint: "High-reliability parametric solid features." },
    { id: "Assembly Design (CATIA)", type: "skill", tags: ["catia"], hint: "Constraint resolution & clash check mockups." },
    { id: "DELMIA Simulation", type: "skill", tags: ["delmia"], hint: "Robotic cell programming offline." },
  ];
  const links = [
    ["CAD Basics", "Terminology"],
    ["CAD Basics", "2D Drafting"],
    ["CAD Basics", "3D Modeling"],
    ["2D Drafting", "Command Line"],
    ["3D Modeling", "File Formats"],
    ["File Formats", "DWG"],
    ["File Formats", "STEP"],
    ["File Formats", "IFC"],
    ["AEC", "BIM"],
    ["AEC", "IFC"],
    ["Autodesk", "AutoCAD"],
    ["Autodesk", "Revit"],
    ["Autodesk", "Civil 3D"],
    ["Autodesk", "Inventor"],
    ["Autodesk", "Fusion"],
    ["AutoCAD", "Smart Blocks"],
    ["Revit", "Cloud Worksharing"],
    ["Revit", "Scan to BIM"],
    ["Fusion", "Generative Design"],
    ["Inventor", "iLogic"],
    ["AutoCAD", "DWG"],
    ["Revit", "BIM"],
    ["Gstarsoft", "GstarCAD"],
    ["Gstarsoft", "DWG FastView"],
    ["GstarCAD", "DWG"],
    ["DWG FastView", "DWG"],
    ["GstarCAD", "Python API"],
    ["GstarCAD", "Hardware Acceleration"],
    ["Python API", "PyRx"],
    ["GstarCAD", "GstarCAD Mechanical"],
    ["GstarCAD", "GstarCAD Architecture"],
    ["GstarCAD Mechanical", "Intelligent Objects"],
    ["GstarCAD Architecture", "Intelligent Objects"],
    ["DWG FastView", "Mobile BIM"],
    ["Mobile BIM", "BIM"],
    ["Hardware Acceleration", "3D Modeling"],
    ["Siemens", "STEP"],
    ["Dassault", "DraftSight"],
    ["DraftSight", "PowerTrim"],
    ["DraftSight", "G-Code Gen"],
    ["DraftSight", "Mechanical Toolbox"],
    ["DraftSight", "DWG"],
    ["CAD Basics", "Software Map"],
    ["Software Map", "Learning branch"],
    ["Learning branch", "Autodesk"],
    ["Learning branch", "Gstarsoft"],
    ["Learning branch", "Dassault"],
    ["Dassault", "DraftSight"],
    ["DraftSight", "3DEXPERIENCE"],
    ["DraftSight", "PowerTrim"],
    ["DraftSight", "G-Code Gen"],
    ["DraftSight", "Image Tracer"],
    ["DraftSight", "DraftSight API"],
    ["DraftSight", "Smart Blocks (DS)"],
    ["DraftSight", "Mech Symbols"],
    ["DraftSight", "Batch Print"],
    ["DraftSight", "Alias Custom"],
    ["DraftSight", "LISP (DS)"],
    ["DraftSight", "Xref (DS)"],
    ["DraftSight", "Properties (DS)"],
    ["DraftSight", "SSM (DS)"],
    ["DraftSight", "3D (DS)"],
    ["DraftSight", "Markup (DS)"],
    ["DraftSight", "Licensing (DS)"],
    ["DraftSight", "Perf Tuning"],
    ["DraftSight", "Interop (DS)"],
    ["DraftSight", "DWG"],
    ["Learning branch", "PTC"],
    ["PTC", "Creo Parametric"],
    ["PTC", "Windchill"],
    ["PTC", "Mathcad"],
    ["Creo Parametric", "Skeleton Modeling"],
    ["Creo Parametric", "Flexible Modeling"],
    ["Creo Parametric", "Regeneration Logic"],
    ["Windchill", "Creo Parametric"],
    ["Mathcad", "Creo Parametric"],
    ["Creo Parametric", "MBD (PTC)"],
    ["Creo Parametric", "Generative (PTC)"],
    ["Creo Parametric", "Additive (PTC)"],
    ["Creo Parametric", "Cabling (PTC)"],
    ["Creo Parametric", "Piping (PTC)"],
    ["Creo Parametric", "Sheetmetal (PTC)"],
    ["Creo Parametric", "Mechanism (PTC)"],
    ["Creo Parametric", "Sim Live (PTC)"],
    ["Creo Parametric", "ISDX (PTC)"],
    ["Creo Parametric", "TDD (PTC)"],
    ["Creo Parametric", "Mapkeys (PTC)"],
    ["Creo Parametric", "Config.pro (PTC)"],
    ["Creo Parametric", "Simp Reps (PTC)"],
    ["PTC", "STEP"],
    ["Learning branch", "Siemens"],
    ["Siemens", "NX"],
    ["Siemens", "Solid Edge"],
    ["Siemens", "Teamcenter"],
    ["Siemens", "Simcenter"],
    ["NX", "Synchronous Tech"],
    ["NX", "WAVE Linker"],
    ["Solid Edge", "Synchronous Tech"],
    ["Teamcenter", "NX"],
    ["Simcenter", "NX"],
    ["NX", "Convergent Modeling"],
    ["NX", "PMI (Siemens)"],
    ["Teamcenter", "Active Workspace"],
    ["NX", "Check-Mate"],
    ["NX", "NX CAM"],
    ["NX", "NX MCD"],
    ["NX", "NX PTS"],
    ["NX", "NX Layout"],
    ["NX", "NX Mold Wizard"],
    ["NX", "NX Progressive Die"],
    ["Simcenter", "Nastran"],
    ["NX", "Realize Shape"],
    ["NX", "NX Flow"],
    ["Teamcenter", "Multi-CAD (Siemens)"],
    ["NX", "NX Expressions"],
    ["NX", "HD3D"],
    ["Learning branch", "Bentley"],
    ["Bentley", "MicroStation"],
    ["Bentley", "OpenRoads"],
    ["Bentley", "ProjectWise"],
    ["Bentley", "iTwin"],
    ["MicroStation", "DGN Format"],
    ["MicroStation", "CONNECT Ed."],
    ["MicroStation", "ContextCapture"],
    ["ProjectWise", "iModels"],
    ["ProjectWise", "iTwin"],
    ["Bentley", "STAAD.Pro"],
    ["Bentley", "SYNCHRO"],
    ["Bentley", "WaterGEMS"],
    ["Bentley", "RAM Structural"],
    ["WaterGEMS", "HAMMER"],
    ["MicroStation", "LumenRT"],
    ["iTwin", "AssetWise"],
    ["WaterGEMS", "SewerGEMS"],
    ["Bentley", "gINT"],
    ["Bentley", "AutoPIPE"],
    ["Bentley", "SACS"],
    ["Bentley", "ProSteel"],
    ["Learning branch", "AEC"],
    ["Learning branch", "MFG"],
    ["Siemens", "STEP"],
    ["Dassault", "SOLIDWORKS"],
    ["Dassault", "CATIA"],
    ["Dassault", "ENOVIA"],
    ["Dassault", "SIMULIA"],
    ["Dassault", "DELMIA"],
    ["SOLIDWORKS", "SOLIDWORKS PDM"],
    ["SOLIDWORKS", "SOLIDWORKS API"],
    ["SOLIDWORKS", "SOLIDWORKS Configurations"],
    ["SOLIDWORKS", "Weldments (SW)"],
    ["SOLIDWORKS", "Sheet Metal (SW)"],
    ["SOLIDWORKS", "eDrawings"],
    ["SOLIDWORKS", "Large Design Review"],
    ["SOLIDWORKS", "SpeedPak"],
    ["CATIA", "CATIA GSD"],
    ["CATIA", "CAA SDK"],
    ["CATIA", "PowerCopy"],
    ["CATIA", "Hybrid Design"],
    ["CATIA", "Composites Design"],
    ["CATIA", "FT&A MBD"],
    ["CATIA", "Part Design (CATIA)"],
    ["CATIA", "Assembly Design (CATIA)"],
    ["3DEXPERIENCE", "Collaborative Sharing"],
    ["3DEXPERIENCE", "ENOVIA"],
    ["SIMULIA", "Abaqus"],
    ["DELMIA", "DELMIA Simulation"],
  ];
  const beginnerPath = [
    "CAD Basics",
    "Terminology",
    "2D Drafting",
    "Command Line",
    "File Formats",
    "Learning branch",
  ];

  // filter buttons: cards + graph
  const applyFilter = (tag) => {
    activeFilter = tag;
    filterButtons.forEach((btn) =>
      btn.classList.toggle("active", btn.dataset.filter === tag)
    );
    cards.forEach((card) => {
      const tags = card.dataset.tags || "";
      const show = tag === "all" || tags.includes(tag);
      card.classList.toggle("kb-hidden", !show);
    });
    refreshKbGraphPresentation();
  };
  filterButtons.forEach((btn) =>
    btn.addEventListener("click", () => applyFilter(btn.dataset.filter))
  );
  applyFilter("all");

  if (pathBtn) {
    pathBtn.addEventListener("click", () => {
      pathMode = !pathMode;
      pathBtn.classList.toggle("active", pathMode);
      pathBtn.textContent = pathMode
        ? "Beginner walk highlighted (purple edges)"
        : "Highlight beginner walk (in-graph)";
      pathBtn.title =
        "Purple edges show teaching order—not the checkpoints on the Paths page.";
      refreshKbGraphPresentation();
    });
  }

  if (graphSvgRoot && typeof window.d3 !== "undefined") {
    const initKbD3Graph = () => {
    const d3 = window.d3;
    const typeLabelZh = {
      concept: "Concept",
      skill: "Skill / Workflow",
      domain: "Industry Lane",
      format: "File / Schema",
      resource: "Meta Node",
      vendor: "Vendor / ISV",
      product: "Product Name",
      sdk: "SDK / Toolkit",
    };
    const colorMap = {
      concept: "#6a82ff",
      skill: "#4ecdc4",
      domain: "#c77dff",
      format: "#35b69d",
      resource: "#f0a22f",
      vendor: "#fb7185",
      product: "#38bdf8",
      sdk: "#a78bfa",
    };
    const nodeHint = (d) => (d && d.hint) || d.descZh || "";

    const graphImmersive = document.body.classList.contains("page-kb-graph");
    const computeGraphHeight = () => {
      const narrow = window.matchMedia("(max-width:767px)").matches;
      const vh = window.innerHeight || 800;
      if (graphImmersive) {
        if (narrow) return Math.round(Math.min(Math.max(vh * 0.42, 300), vh * 0.54));
        return Math.round(Math.min(Math.max(vh * 0.62, 480), vh * 0.78));
      }
      return narrow ? 360 : 560;
    };

    const simNodes = nodes.map((n) => ({ ...n }));
    const simLinks = links.map(([source, target]) => ({ source, target }));

    let width = Math.max(graphStage?.clientWidth || 920, 320);
    let height = computeGraphHeight();

    const cxSeed = width / 2;
    const cySeed = height / 2;
    const ring = Math.min(width, height) * 0.26;
    simNodes.forEach((n, i, arr) => {
      const ang = (i / Math.max(arr.length, 1)) * Math.PI * 2 - Math.PI / 2;
      n.x = cxSeed + ring * Math.cos(ang);
      n.y = cySeed + ring * Math.sin(ang);
    });

    let hoverId = "";
    let selectedId = "";

    const svg = d3.select(graphSvgRoot);
    svg
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("preserveAspectRatio", "xMidYMid meet")
      .attr("role", "img");
    const gZoom = svg.append("g");

    gZoom
      .append("rect")
      .attr("class", "kb-graph-bg-hit")
      .attr("width", width)
      .attr("height", height)
      .attr("fill", "transparent")
      .attr("pointer-events", "all")
      .on("click", () => {
        clearGraphSelection(true, false);
      });

    const zoom = d3
      .zoom()
      .scaleExtent([0.2, 3])
      .on("zoom", (event) => {
        gZoom.attr("transform", event.transform);
      });
    svg.call(zoom);

    const simulation = d3
      .forceSimulation(simNodes)
      .force(
        "link",
        d3
          .forceLink(simLinks)
          .id((d) => d.id)
          .distance(160)
          .strength(0.5)
      )
      .force("charge", d3.forceManyBody().strength(-600))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(80))
      .velocityDecay(0.2);

    const linkSel = gZoom
      .append("g")
      .attr("stroke-linecap", "round")
      .selectAll("line")
      .data(simLinks)
      .join("line")
      .attr("class", "kb-graph-link")
      .style("stroke-opacity", 0.15)
      .style("stroke", "var(--accent)")
      .style("stroke-width", 1.5)
      .style("transition", "stroke-opacity 0.3s ease, stroke-width 0.3s ease");

    const nodeG = gZoom
      .append("g")
      .selectAll("g")
      .data(simNodes)
      .join("g")
      .attr("class", "kb-graph-node-group")
      .style("cursor", "pointer")
      .call(
        d3
          .drag()
          .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.35).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );

    nodeG
      .append("circle")
      .attr("class", "kb-graph-node-shape")
      .attr("r", (d) =>
        d.type === "vendor"
          ? 19
          : d.type === "domain"
          ? 17
          : d.type === "product"
          ? 15
          : d.type === "sdk"
          ? 15
          : d.type === "resource"
          ? 16
          : d.type === "skill"
          ? 14
          : 15
      )
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.75)
      .attr("fill", (d) => colorMap[d.type] || "#8b9dcf");

    nodeG
      .append("text")
      .attr("class", "kb-graph-node-label")
      .attr("text-anchor", "middle")
      .attr("dy", 38)
      .text((d) => d.id);

    const tooltip = document.getElementById("kbGraphTooltip");

    const pathEdgeSet = new Set(
      beginnerPath.slice(0, -1).map((id, i) => `${id}__${beginnerPath[i + 1]}`)
    );
    const pathEdgeHit = (a, b) =>
      pathEdgeSet.has(`${a}__${b}`) || pathEdgeSet.has(`${b}__${a}`);

    const neighborIds = (id) => {
      const s = new Set();
      if (!id) return s;
      links.forEach(([a, b]) => {
        if (a === id) s.add(b);
        if (b === id) s.add(a);
      });
      return s;
    };

    const GRAPH_PAGE_TITLE = (() =>
      document.documentElement.getAttribute("lang")?.toLowerCase().startsWith("zh")
        ? "Knowledge Graph · CAD Knowledge Base"
        : "CAD Knowledge Base · Knowledge graph")();
    const GRAPH_NODE_Q = "node";

    const graphPageFile = () => {
      const p = window.location.pathname || "";
      const seg = p.split("/").filter(Boolean);
      return seg.length ? seg[seg.length - 1] : "kb-graph.html";
    };

    const writeGraphNodeURL = (id, replace) => {
      const base = graphPageFile();
      const q = id ? `?${GRAPH_NODE_Q}=${encodeURIComponent(id)}` : "";
      const next = `${base}${q}`;
      (replace ? history.replaceState : history.pushState)({}, "", next);
    };

    const readGraphNodeParam = () => {
      try {
        return new URL(window.location.href).searchParams.get(GRAPH_NODE_Q);
      } catch {
        return null;
      }
    };

    const zoomToNode = (d) => {
      if (!d || d.x == null || d.y == null) return;
      const scale = 1.78;
      const tx = width / 2 - scale * d.x;
      const ty = height / 2 - scale * d.y;
      svg
        .transition()
        .duration(380)
        .call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
    };

    function fillGraphPathLinkList(steps) {
      if (!infoPath) return;
      infoPath.innerHTML = "";
      steps.forEach((step) => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = `?${GRAPH_NODE_Q}=${encodeURIComponent(step)}`;
        a.textContent = step;
        a.addEventListener("click", (e) => {
          e.preventDefault();
          const nd = simNodes.find((x) => x.id === step);
          if (nd) selectGraphNode(nd, { replaceURL: false, zoom: true });
        });
        li.appendChild(a);
        infoPath.appendChild(li);
      });
    }

    function fillGraphRelatedLinks(names) {
      if (!infoRelated) return;
      infoRelated.innerHTML = "";
      const list =
        names && names.length
          ? names
          : ["No linked nodes (pick another filter or zoom out)"];
      list.slice(0, 10).forEach((name) => {
        const isPlaceholder = /^No linked nodes/.test(name);
        if (isPlaceholder) {
          const s = document.createElement("span");
          s.className = "kb-tag kb-static";
          s.textContent = name;
          infoRelated.appendChild(s);
          return;
        }
        const a = document.createElement("a");
        a.href = `?${GRAPH_NODE_Q}=${encodeURIComponent(name)}`;
        a.className = "kb-tag";
        a.rel = "nofollow noopener noreferrer";
        a.textContent = name;
        a.addEventListener("click", (e) => {
          e.preventDefault();
          const nd = simNodes.find((x) => x.id === name);
          if (nd) selectGraphNode(nd, { replaceURL: false, zoom: true });
        });
        infoRelated.appendChild(a);
      });
    }

    function selectGraphNode(d, opts) {
      const o = opts || {};
      const doZoom = o.zoom !== false;
      const replaceURL = !!o.replaceURL;
      const silentURL = !!o.silentURL;
      const actions = document.getElementById("kbInfoActions");
      const detailsBtn = document.getElementById("kbViewDetailsBtn");
      if (actions && detailsBtn) {
        actions.style.display = "block";
        // Map node ID to concept filename (slug)
        const slug = d.id.toLowerCase().replace(/\s+/g, "-");
        detailsBtn.href = `./kb/concepts/${slug}.html`;
      }

      fillGraphRelatedLinks([...neighborIds(d.id)].slice(0, 8));
      fillGraphPathLinkList(beginnerPath);
      document.title = (() => {
        const z = (document.documentElement.getAttribute("lang") || "")
          .toLowerCase()
          .startsWith("zh");
        return `CAD Knowledge Base · Graph · ${d.id}`;
      })();
      if (!silentURL) writeGraphNodeURL(d.id, replaceURL);
      if (doZoom) zoomToNode(d);
      updateGraphPresentation();
    }

    function clearGraphSelection(pushHistory, replaceHist) {
      selectedId = "";
      hoverId = "";
      document.title = GRAPH_PAGE_TITLE;
      if (infoTitle) infoTitle.textContent = graphPanelDefaultTitle();
      if (infoDesc)
        infoDesc.textContent = (document.documentElement.getAttribute("lang") || "")
          .toLowerCase()
          .startsWith("zh")
          ? "Click a node or open a sharing link with ?node=Name."
          : "Select a node, tag, or card to inspect connected concepts.";
      const actions = document.getElementById("kbInfoActions");
      if (actions) actions.style.display = "none";
      fillGraphRelatedLinks([]);
      updateGraphPresentation();
      if (pushHistory) writeGraphNodeURL("", !!replaceHist);
    }

    function updateGraphPresentation() {
      const focusId = hoverId || selectedId;
      const nei = neighborIds(focusId);
      const rel = focusId ? new Set([focusId, ...nei]) : null;

      // Update Links
      linkSel
        .transition()
        .duration(300)
        .style("stroke-opacity", (d) => {
          const sa = typeof d.source === "object" ? d.source.id : d.source;
          const tb = typeof d.target === "object" ? d.target.id : d.target;
          if (focusId === sa || focusId === tb) return 0.8;
          return rel ? 0.05 : 0.12; // Dim others when focusing, subtle when idle
        })
        .style("stroke-width", (d) => {
          const sa = typeof d.source === "object" ? d.source.id : d.source;
          const tb = typeof d.target === "object" ? d.target.id : d.target;
          return (focusId === sa || focusId === tb) ? 3 : 1.5;
        })
        .style("stroke", (d) => {
          const sa = typeof d.source === "object" ? d.source.id : d.source;
          const tb = typeof d.target === "object" ? d.target.id : d.target;
          return (focusId === sa || focusId === tb) ? "var(--accent)" : "#94a3b8";
        });

      // Update Nodes
      nodeG.each(function (d) {
        const isFocus = d.id === focusId;
        const isRel = rel && rel.has(d.id);
        const match = activeFilter === "all" || d.tags.includes(activeFilter);
        const g = d3.select(this);

        const op = match ? (focusId ? (isRel ? 1 : 0.2) : 1) : 0.1;
        
        g.transition()
          .duration(300)
          .style("opacity", op);

        g.select("circle")
          .transition()
          .duration(300)
          .attr("r", (d) => {
            const base = d.type === "vendor" ? 22 : 18;
            return isFocus ? base * 1.3 : isRel ? base * 1.1 : base;
          })
          .attr("stroke-width", isFocus ? 4 : 2)
          .attr("stroke", isFocus ? "var(--accent)" : "#fff")
          .style("filter", isFocus ? "drop-shadow(0 0 12px var(--accent-glow))" : "none");

        g.select("text")
          .transition()
          .duration(300)
          .style("font-weight", isFocus ? "800" : "500")
          .attr("dy", isFocus ? 45 : 38)
          .style("font-size", isFocus ? "14px" : "12px");
      });
    }

    refreshKbGraphPresentation = updateGraphPresentation;

    const showTooltip = (event, d) => {
      if (!tooltip) return;
      const t1 = tooltip.querySelector("[data-tip-title]");
      const t2 = tooltip.querySelector("[data-tip-type]");
      const t3 = tooltip.querySelector("[data-tip-desc]");
      if (!t1 || !t2 || !t3) return;
      tooltip.hidden = false;
      t1.textContent = d.id;
      t2.textContent =
        typeLabelZh[d.type] || d.type;
      t3.textContent = nodeHint(d);
      const rect = graphStage?.getBoundingClientRect();
      if (!rect) return;
      tooltip.style.opacity = "1";
      const tx = event.clientX - rect.left + 12;
      const ty = event.clientY - rect.top + 12;
      tooltip.style.left = `${Math.min(tx, rect.width - 200)}px`;
      tooltip.style.top = `${Math.min(ty, rect.height - 120)}px`;
    };

    const hideTooltip = () => {
      if (tooltip) {
        tooltip.style.opacity = "0";
        tooltip.hidden = true;
      }
    };

    nodeG
      .on("mouseenter", (event, d) => {
        hoverId = d.id;
        updateGraphPresentation();
        showTooltip(event, d);
      })
      .on("mousemove", (event, d) => showTooltip(event, d))
      .on("mouseleave", () => {
        hoverId = "";
        hideTooltip();
        updateGraphPresentation();
      })
      .on("click", (event, d) => {
        event.stopPropagation();
        selectGraphNode(d, { replaceURL: false, zoom: true });
      });

    const tickPositions = () => {
      linkSel
        .attr("x1", (l) => l.source.x)
        .attr("y1", (l) => l.source.y)
        .attr("x2", (l) => l.target.x)
        .attr("y2", (l) => l.target.y);
      nodeG.attr(
        "transform",
        (d) => `translate(${d.x ?? width / 2},${d.y ?? height / 2})`
      );
    };

    simulation.on("tick", tickPositions);

    // Initial animation burst
    simulation.alpha(1).restart();

    const resize = () => {
      width = Math.max(graphStage?.clientWidth || 920, 320);
      height = computeGraphHeight();
      svg
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", `0 0 ${width} ${height}`);
      svg.select(".kb-graph-bg-hit").attr("width", width).attr("height", height);
      simulation.force(
        "center",
        d3.forceCenter(width / 2, height / 2)
      );
      simulation.alpha(0.35).restart();
    };
    window.addEventListener("resize", resize);
    if ("ResizeObserver" in window && graphStage) {
      new ResizeObserver(resize).observe(graphStage);
    }

    document.getElementById("kbGraphReset")?.addEventListener("click", () => {
      svg.transition().duration(260).call(zoom.transform, d3.zoomIdentity);
    });
    document.getElementById("kbGraphZoomIn")?.addEventListener("click", () => {
      zoom.scaleBy(svg.transition().duration(200), 1.2);
    });
    document.getElementById("kbGraphZoomOut")?.addEventListener("click", () => {
      zoom.scaleBy(svg.transition().duration(200), 1 / 1.2);
    });

    window.addEventListener("popstate", () => {
      const raw = readGraphNodeParam();
      if (!raw) {
        selectedId = "";
        document.title = GRAPH_PAGE_TITLE;
        if (infoTitle) infoTitle.textContent = graphPanelDefaultTitle();
        if (infoDesc)
          infoDesc.textContent = (document.documentElement.getAttribute("lang") || "")
            .toLowerCase()
            .startsWith("zh")
            ? "Click a node, or open a sharing link with ?node=Name."
            : "Select a node, tag, or card to inspect connected concepts.";
        fillGraphRelatedLinks([]);
        fillGraphPathLinkList(beginnerPath);
        updateGraphPresentation();
        return;
      }
      const nd = simNodes.find((n) => n.id === raw);
      if (nd) selectGraphNode(nd, { silentURL: true, zoom: true });
      else {
        if (infoDesc)
          infoDesc.textContent = `Unknown node in URL: ${raw}`;
        writeGraphNodeURL("", true);
      }
    });

    const initialNode = readGraphNodeParam();
    if (initialNode) {
      const nd = simNodes.find((n) => n.id === initialNode);
      if (nd) selectGraphNode(nd, { silentURL: true, zoom: true });
      else {
        if (infoDesc)
          infoDesc.textContent = `Unknown node in URL: ${initialNode}`;
        writeGraphNodeURL("", true);
      }
    } else {
      clearGraphSelection(false, false);
    }

    updateGraphPresentation();
    };

    // Global execution for taxonomy sidebar
    initKbSidebarTaxonomy();

    try {
      initKbD3Graph();
    } catch (err) {
      console.error("kb-graph:", err);
      const fb = graphStage?.querySelector?.("[data-kb-graph-d3-fallback]");
      if (fb) {
        fb.hidden = false;
        fb.textContent =
          "Graph initialization failed: " + (err && err.message ? err.message : String(err));
      }
    }
  } else if (graphSvgRoot) {
    const note = graphStage?.querySelector?.("[data-kb-graph-d3-fallback]");
    if (note) note.hidden = false;
  }
}
