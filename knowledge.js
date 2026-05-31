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
    // overlay & body scroll handling for mobile
    const overlayEl = document.querySelector('.kb-sidebar-overlay');
    if (overlayEl) overlayEl.style.display = collapsed ? 'none' : 'block';
    document.body.style.overflow = collapsed ? '' : 'hidden';
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

  // Create overlay for mobile sidebar
  const overlay = document.createElement('div');
  overlay.className = 'kb-sidebar-overlay';
  overlay.addEventListener('click', () => applyKbRailCollapsed(true));
  document.body.appendChild(overlay);

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
  { id: "AutoCAD Layer States", group: 2, type: "concept", radius: 8, tags: ["autocad", "2d"] },
  { id: "AutoCAD Dynamic Blocks", group: 2, type: "concept", radius: 8, tags: ["autocad", "2d"] },
  { id: "AutoCAD Sheet Sets", group: 2, type: "concept", radius: 8, tags: ["autocad", "2d"] },
  { id: "AutoCAD XREF Management", group: 2, type: "concept", radius: 8, tags: ["autocad", "2d", "collaboration"] },
  { id: "AutoCAD AutoLISP", group: 2, type: "concept", radius: 8, tags: ["autocad", "automation"] },
  { id: "AutoCAD Trace", group: 2, type: "concept", radius: 8, tags: ["autocad", "collaboration"] },
  { id: "AutoCAD Annotative Scale", group: 2, type: "concept", radius: 8, tags: ["autocad", "2d"] },
  { id: "AutoCAD Paper Space", group: 2, type: "concept", radius: 8, tags: ["autocad", "2d"] },
  { id: "AutoCAD Web App", group: 2, type: "product", radius: 8, tags: ["autocad", "cloud"] },
  { id: "Revit Families", group: 2, type: "concept", radius: 8, tags: ["revit", "bim"] },
  { id: "Revit Worksharing", group: 2, type: "concept", radius: 8, tags: ["revit", "collaboration"] },
  { id: "Revit Schedules", group: 2, type: "concept", radius: 8, tags: ["revit", "bim"] },
  { id: "Revit View Templates", group: 2, type: "concept", radius: 8, tags: ["revit", "standards"] },
  { id: "Revit Dynamo", group: 2, type: "product", radius: 8, tags: ["revit", "automation"] },
  { id: "Revit Phasing", group: 2, type: "concept", radius: 8, tags: ["revit", "bim"] },
  { id: "Revit Design Options", group: 2, type: "concept", radius: 8, tags: ["revit", "bim"] },
  { id: "Revit MEP Systems", group: 2, type: "concept", radius: 8, tags: ["revit", "mep"] },
  { id: "Inventor iLogic", group: 2, type: "concept", radius: 8, tags: ["inventor", "automation"] },
  { id: "Inventor AnyCAD", group: 2, type: "concept", radius: 8, tags: ["inventor", "collaboration"] },
  { id: "Inventor Frame Generator", group: 2, type: "concept", radius: 8, tags: ["inventor", "mfg"] },
  { id: "Inventor Sheet Metal", group: 2, type: "concept", radius: 8, tags: ["inventor", "mfg"] },
  { id: "Inventor Content Center", group: 2, type: "concept", radius: 8, tags: ["inventor", "standards"] },
  { id: "Inventor Model States", group: 2, type: "concept", radius: 8, tags: ["inventor", "mfg"] },
  { id: "Inventor Nastran", group: 2, type: "product", radius: 8, tags: ["inventor", "simulation"] },
  { id: "Inventor CAM", group: 2, type: "product", radius: 8, tags: ["inventor", "cam"] },
  { id: "Inventor Vault Integration", group: 2, type: "concept", radius: 8, tags: ["inventor", "pdm"] },
  { id: "Fusion Timeline", group: 2, type: "concept", radius: 8, tags: ["fusion", "3d"] },
  { id: "Fusion Joints", group: 2, type: "concept", radius: 8, tags: ["fusion", "3d"] },
  { id: "Fusion Generative Design", group: 2, type: "concept", radius: 8, tags: ["fusion", "ai"] },
  { id: "Fusion T-Splines", group: 2, type: "concept", radius: 8, tags: ["fusion", "3d"] },
  { id: "Fusion CAM Setup", group: 2, type: "concept", radius: 8, tags: ["fusion", "cam"] },
  { id: "Fusion Mesh Repair", group: 2, type: "concept", radius: 8, tags: ["fusion", "3d"] },
  { id: "Fusion Cloud Render", group: 2, type: "concept", radius: 8, tags: ["fusion", "cloud"] },
  { id: "Fusion Direct Modeling", group: 2, type: "concept", radius: 8, tags: ["fusion", "3d"] },
  { id: "Fusion Extensions", group: 2, type: "concept", radius: 8, tags: ["fusion", "cloud"] },
  { id: "Civil 3D Corridors", group: 2, type: "concept", radius: 8, tags: ["civil3d", "infrastructure"] },
  { id: "Civil 3D Alignments", group: 2, type: "concept", radius: 8, tags: ["civil3d", "infrastructure"] },
  { id: "Civil 3D Surfaces", group: 2, type: "concept", radius: 8, tags: ["civil3d", "infrastructure"] },
  { id: "Civil 3D Feature Lines", group: 2, type: "concept", radius: 8, tags: ["civil3d", "infrastructure"] },
  { id: "Civil 3D Pipe Networks", group: 2, type: "concept", radius: 8, tags: ["civil3d", "infrastructure"] },
  { id: "Civil 3D Data Shortcuts", group: 2, type: "concept", radius: 8, tags: ["civil3d", "collaboration"] },
  { id: "Civil 3D Grading Optimization", group: 2, type: "concept", radius: 8, tags: ["civil3d", "infrastructure"] },
  { id: "Civil 3D Assemblies", group: 2, type: "concept", radius: 8, tags: ["civil3d", "infrastructure"] },
  { id: "Civil 3D Parcels", group: 2, type: "concept", radius: 8, tags: ["civil3d", "infrastructure"] },
  { id: "Navisworks Clash Detective", group: 2, type: "concept", radius: 8, tags: ["navisworks", "bim"] },
  { id: "Navisworks TimeLiner", group: 2, type: "concept", radius: 8, tags: ["navisworks", "bim"] },
  { id: "Navisworks Quantification", group: 2, type: "concept", radius: 8, tags: ["navisworks", "bim"] },
  { id: "Navisworks NWD Format", group: 2, type: "concept", radius: 8, tags: ["navisworks", "bim"] },
  { id: "Navisworks Viewpoints", group: 2, type: "concept", radius: 8, tags: ["navisworks", "bim"] },
  { id: "Navisworks SwitchBack", group: 2, type: "concept", radius: 8, tags: ["navisworks", "collaboration"] },
  { id: "Navisworks Search Sets", group: 2, type: "concept", radius: 8, tags: ["navisworks", "bim"] },
  { id: "Navisworks Point Cloud Rendering", group: 2, type: "concept", radius: 8, tags: ["navisworks", "bim"] },
  { id: "Navisworks Animator", group: 2, type: "concept", radius: 8, tags: ["navisworks", "bim"] },
  { id: "SOLIDWORKS SpeedPak", group: 2, type: "concept", radius: 8, tags: ["solidworks", "mfg"] },
  { id: "SOLIDWORKS SmartMates", group: 2, type: "concept", radius: 8, tags: ["solidworks", "mfg"] },
  { id: "CATIA PowerCopy", group: 2, type: "concept", radius: 8, tags: ["catia", "mfg"] },
  { id: "Creo Direct", group: 2, type: "product", radius: 8, tags: ["creo", "mfg"] },
  { id: "Creo Simulate", group: 2, type: "product", radius: 8, tags: ["creo", "simulation"] },
  { id: "Creo Unite Technology", group: 2, type: "concept", radius: 8, tags: ["creo", "collaboration"] },
  { id: "Creo Skeleton Modeling", group: 2, type: "concept", radius: 8, tags: ["creo", "mfg"] },
  { id: "Creo Flexible Modeling", group: 2, type: "concept", radius: 8, tags: ["creo", "mfg"] },
  { id: "Creo Windchill Integration", group: 2, type: "concept", radius: 8, tags: ["creo", "pdm"] },
  { id: "Creo Family Tables", group: 2, type: "concept", radius: 8, tags: ["creo", "mfg"] },
  { id: "Creo Mechanism Design", group: 2, type: "concept", radius: 8, tags: ["creo", "simulation"] },
  { id: "Creo Topology Optimization", group: 2, type: "concept", radius: 8, tags: ["creo", "simulation"] },
  { id: "GstarCAD Mech BOM", group: 2, type: "concept", radius: 8, tags: ["gstarcad-mech", "mfg"] },
  { id: "GstarCAD Mech Intelligent Dimensions", group: 2, type: "concept", radius: 8, tags: ["gstarcad-mech", "mfg"] },
  { id: "GstarCAD Mech Hole Chart", group: 2, type: "concept", radius: 8, tags: ["gstarcad-mech", "mfg"] },
  { id: "GstarCAD Mech Hidden Lines", group: 2, type: "concept", radius: 8, tags: ["gstarcad-mech", "2d"] },
  { id: "GstarCAD Mech Standard Parts", group: 2, type: "concept", radius: 8, tags: ["gstarcad-mech", "mfg"] },
  { id: "GstarCAD Mech Drawing Borders", group: 2, type: "concept", radius: 8, tags: ["gstarcad-mech", "standards"] },
  { id: "GstarCAD Mech Welding Symbols", group: 2, type: "concept", radius: 8, tags: ["gstarcad-mech", "mfg"] },
  { id: "GstarCAD Mech Detail Views", group: 2, type: "concept", radius: 8, tags: ["gstarcad-mech", "2d"] },
  { id: "GstarCAD Mech Surface Texture", group: 2, type: "concept", radius: 8, tags: ["gstarcad-mech", "mfg"] },
  { id: "GstarCAD Mech Power Erase", group: 2, type: "concept", radius: 8, tags: ["gstarcad-mech", "2d"] },
  { id: "FastView Cloud Sync", group: 2, type: "concept", radius: 8, tags: ["fastview", "cloud"] },
  { id: "FastView Mobile Markup", group: 2, type: "concept", radius: 8, tags: ["fastview", "mobile"] },
  { id: "FastView Inquiry Tools", group: 2, type: "concept", radius: 8, tags: ["fastview", "mobile"] },
  { id: "FastView Font Manager", group: 2, type: "concept", radius: 8, tags: ["fastview", "mobile"] },
  { id: "FastView Offline Mode", group: 2, type: "concept", radius: 8, tags: ["fastview", "mobile"] },
  { id: "FastView Version Compare", group: 2, type: "concept", radius: 8, tags: ["fastview", "mobile"] },
  { id: "FastView PDF Export", group: 2, type: "concept", radius: 8, tags: ["fastview", "mobile"] },
  { id: "FastView Text Extraction", group: 2, type: "concept", radius: 8, tags: ["fastview", "mobile"] },
  { id: "FastView Layer Control", group: 2, type: "concept", radius: 8, tags: ["fastview", "mobile"] },
  { id: "FastView Layout Switch", group: 2, type: "concept", radius: 8, tags: ["fastview", "mobile"] },
  { id: "Dassault 3DEXPERIENCE", group: 1, type: "vendor", radius: 12, tags: ["dassault", "cloud"] },
  { id: "Dassault ENOVIA", group: 1, type: "vendor", radius: 12, tags: ["dassault", "pdm"] },
  { id: "Dassault DELMIA", group: 1, type: "vendor", radius: 12, tags: ["dassault", "mfg"] },
  { id: "Autodesk AEC Collection", group: 1, type: "vendor", radius: 12, tags: ["autodesk", "bim"] },
  { id: "Autodesk PDM Collection", group: 1, type: "vendor", radius: 12, tags: ["autodesk", "mfg"] },
  { id: "Autodesk Construction Cloud", group: 1, type: "vendor", radius: 12, tags: ["autodesk", "bim"] },
  { id: "Autodesk Platform Services", group: 1, type: "vendor", radius: 12, tags: ["autodesk", "cloud"] },
  { id: "Autodesk Flex", group: 1, type: "vendor", radius: 12, tags: ["autodesk", "licensing"] },
  { id: "Autodesk Access", group: 1, type: "vendor", radius: 12, tags: ["autodesk", "licensing"] },

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
    { id: "Alibre", type: "vendor", group: 1, radius: 12, tags: ["alibre"], hint: "Vendor of Alibre Design." },
    { id: "Allplan (Nemetschek)", type: "vendor", group: 1, radius: 12, tags: ["allplan"], hint: "Nemetschek group company; vendor of Allplan." },
    { id: "Graebert", type: "vendor", group: 1, radius: 12, tags: ["graebert"], hint: "Vendor of ARES Commander and DWG-based CAD technologies." },
    { id: "AVEVA", type: "vendor", group: 1, radius: 12, tags: ["aveva"], hint: "Industrial software vendor for process plant and marine design." },
    { id: "FreeCAD Community (FOSS)", type: "vendor", group: 1, radius: 12, tags: ["freecad", "community", "foss"], hint: "Open-source community behind FreeCAD." },
    { id: "IronCAD LLC", type: "vendor", group: 1, radius: 12, tags: ["ironcad"], hint: "Vendor of IronCAD dual-engine MCAD." },
    { id: "ZWSOFT", type: "vendor", group: 1, radius: 12, tags: ["zwsoft", "zwcad"], hint: "Vendor of ZWCAD high-performance DWG-native CAD." },
    { id: "ANSYS", type: "vendor", group: 1, radius: 12, tags: ["ansys", "spaceclaim"], hint: "Engineering simulation vendor; parent of SpaceClaim." },
    { id: "Trimble", type: "vendor", group: 1, radius: 12, tags: ["trimble", "tekla-structures", "sketchup"], hint: "Technology vendor for construction and geospatial; parent of SketchUp and Tekla." },
    { id: "McNeel & Associates", type: "vendor", group: 1, radius: 12, tags: ["mcneel", "rhinoceros"], hint: "Vendor of Rhinoceros NURBS modeler." },
    { id: "Vectorworks (Nemetschek)", type: "vendor", group: 1, radius: 12, tags: ["vectorworks"], hint: "Nemetschek group company; vendor of Vectorworks." },
    { id: "Hexagon", type: "vendor", group: 1, radius: 12, tags: ["hexagon", "bricscad"], hint: "Global leader in digital reality solutions; parent of Bricsys and BricsCAD." },
  /* AUTO-GEN sw-nodes START */
  { id: "Alibre Design", type: "product", group: 1, radius: 14, tags: ["alibre", "alibre-design"], hint: "A high-precision, budget-friendly parametric 3D solid modeler for mechanical parts and assemblies." },
  { id: "Alibre Design Concept 1", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 1 in Alibre Design." },
  { id: "Alibre Design Concept 2", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 2 in Alibre Design." },
  { id: "Alibre Design Concept 3", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 3 in Alibre Design." },
  { id: "Alibre Design Concept 4", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 4 in Alibre Design." },
  { id: "Alibre Design Concept 5", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 5 in Alibre Design." },
  { id: "Alibre Design Concept 6", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 6 in Alibre Design." },
  { id: "Alibre Design Concept 7", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 7 in Alibre Design." },
  { id: "Alibre Design Concept 8", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 8 in Alibre Design." },
  { id: "Alibre Design Concept 9", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 9 in Alibre Design." },
  { id: "Alibre Design Concept 10", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 10 in Alibre Design." },
  { id: "Alibre Design Concept 11", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 11 in Alibre Design." },
  { id: "Alibre Design Concept 12", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 12 in Alibre Design." },
  { id: "Alibre Design Concept 13", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 13 in Alibre Design." },
  { id: "Alibre Design Concept 14", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 14 in Alibre Design." },
  { id: "Alibre Design Concept 15", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Concept 15 in Alibre Design." },
  { id: "Allplan", type: "product", group: 1, radius: 14, tags: ["allplan", "allplan"], hint: "Nemetschek's high-performance BIM platform focused on structural engineering and precast concrete." },
  { id: "Allplan Concept 1", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 1 in Allplan." },
  { id: "Allplan Concept 2", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 2 in Allplan." },
  { id: "Allplan Concept 3", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 3 in Allplan." },
  { id: "Allplan Concept 4", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 4 in Allplan." },
  { id: "Allplan Concept 5", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 5 in Allplan." },
  { id: "Allplan Concept 6", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 6 in Allplan." },
  { id: "Allplan Concept 7", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 7 in Allplan." },
  { id: "Allplan Concept 8", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 8 in Allplan." },
  { id: "Allplan Concept 9", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 9 in Allplan." },
  { id: "Allplan Concept 10", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 10 in Allplan." },
  { id: "Allplan Concept 11", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 11 in Allplan." },
  { id: "Allplan Concept 12", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 12 in Allplan." },
  { id: "Allplan Concept 13", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 13 in Allplan." },
  { id: "Allplan Concept 14", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 14 in Allplan." },
  { id: "Allplan Concept 15", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Concept 15 in Allplan." },
  { id: "ARES Commander", type: "product", group: 1, radius: 14, tags: ["graebert", "ares-commander"], hint: "Graebert's core DWG-native CAD engine, the foundation powering DraftSight, CorelCAD, and extensive cloud workflows." },
  { id: "ARES Commander Concept 1", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 1 in ARES Commander." },
  { id: "ARES Commander Concept 2", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 2 in ARES Commander." },
  { id: "ARES Commander Concept 3", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 3 in ARES Commander." },
  { id: "ARES Commander Concept 4", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 4 in ARES Commander." },
  { id: "ARES Commander Concept 5", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 5 in ARES Commander." },
  { id: "ARES Commander Concept 6", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 6 in ARES Commander." },
  { id: "ARES Commander Concept 7", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 7 in ARES Commander." },
  { id: "ARES Commander Concept 8", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 8 in ARES Commander." },
  { id: "ARES Commander Concept 9", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 9 in ARES Commander." },
  { id: "ARES Commander Concept 10", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 10 in ARES Commander." },
  { id: "ARES Commander Concept 11", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 11 in ARES Commander." },
  { id: "ARES Commander Concept 12", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 12 in ARES Commander." },
  { id: "ARES Commander Concept 13", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 13 in ARES Commander." },
  { id: "ARES Commander Concept 14", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 14 in ARES Commander." },
  { id: "ARES Commander Concept 15", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Concept 15 in ARES Commander." },
  { id: "AutoCAD XREF Tree", type: "skill", group: 2, radius: 9, tags: ["autocad", "collaboration"], hint: "Multi-discipline external-reference workflow." },
  { id: "AutoCAD Dynamic Block", type: "concept", group: 2, radius: 9, tags: ["autocad", "blocks"], hint: "Parametric reusable blocks with grips and lookups." },
  { id: "AutoCAD Sheet Set", type: "skill", group: 2, radius: 9, tags: ["autocad", "documentation"], hint: "Coordinated multi-sheet document management." },
  { id: "AutoCAD Plot Styles", type: "concept", group: 2, radius: 9, tags: ["autocad", "plotting"], hint: "CTB / STB plot-style configuration." },
  { id: "AutoCAD Data Extraction", type: "skill", group: 2, radius: 9, tags: ["autocad", "schedules"], hint: "Extract block attributes to tables/CSV." },
  { id: "AutoCAD Constraints", type: "concept", group: 2, radius: 9, tags: ["autocad", "parametric"], hint: "Geometric and dimensional constraints." },
  { id: "AVEVA Everything3D", type: "product", group: 1, radius: 14, tags: ["aveva", "aveva-e3d"], hint: "AVEVA's high-end process plant and marine 3D design platform, optimized for huge coordinated piping projects." },
  { id: "AVEVA Everything3D Concept 1", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 1 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 2", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 2 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 3", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 3 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 4", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 4 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 5", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 5 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 6", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 6 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 7", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 7 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 8", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 8 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 9", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 9 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 10", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 10 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 11", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 11 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 12", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 12 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 13", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 13 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 14", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 14 in AVEVA Everything3D." },
  { id: "AVEVA Everything3D Concept 15", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Concept 15 in AVEVA Everything3D." },
  { id: "BricsCAD", type: "product", group: 1, radius: 14, tags: ["hexagon", "dwg", "bim", "mcad"], hint: "Hexagon's unified DWG-native 2D/3D CAD platform." },
  { id: "Direct Modeling", type: "concept", group: 2, radius: 10, tags: ["bricscad", "modeling"], hint: "History-free solid geometric manipulation." },
  { id: "BIMIFY", type: "concept", group: 2, radius: 9, tags: ["bricscad", "bim", "ai"], hint: "AI-driven automatic classification of architectural elements." },
  { id: "BricsCAD Communicator", type: "product", group: 1, radius: 9, tags: ["bricscad", "interop"], hint: "High-fidelity translation plugin for industrial B-Rep formats." },
  { id: "CATIA Workbenches", type: "concept", group: 2, radius: 10, tags: ["catia"], hint: "Modular workbench-based UI." },
  { id: "CATIA Sketcher", type: "concept", group: 2, radius: 8, tags: ["catia"], hint: "2D sketch environment." },
  { id: "GSD", type: "skill", group: 2, radius: 11, tags: ["catia", "surfacing"], hint: "Generative Shape Design surfacing." },
  { id: "Multi-Section Surface", type: "concept", group: 2, radius: 8, tags: ["catia", "surfacing"], hint: "Class-A lofted surface." },
  { id: "CATIA Product Structure", type: "concept", group: 2, radius: 9, tags: ["catia", "assembly"], hint: "Hierarchical assembly tree." },
  { id: "Contextual Design", type: "skill", group: 2, radius: 9, tags: ["catia", "assembly"], hint: "Top-down assembly with cross-part refs." },
  { id: "Publications", type: "concept", group: 2, radius: 9, tags: ["catia", "assembly"], hint: "Named exposed references for stability." },
  { id: "DMU Navigator", type: "product", group: 1, radius: 9, tags: ["catia", "review"], hint: "Lightweight assembly visualization." },
  { id: "CATIA Drafting", type: "skill", group: 2, radius: 8, tags: ["catia", "documentation"], hint: "2D drawings from 3D model." },
  { id: "Knowledgeware", type: "sdk", group: 2, radius: 9, tags: ["catia", "automation"], hint: "Parameters, rules, optimiser." },
  { id: "CAA RADE", type: "sdk", group: 2, radius: 8, tags: ["catia", "customization"], hint: "C++ deep customisation framework." },
  { id: "Civil 3D Alignment", type: "concept", group: 2, radius: 10, tags: ["civil3d", "geometry"], hint: "Horizontal centreline with stationing." },
  { id: "Civil 3D Profile", type: "concept", group: 2, radius: 9, tags: ["civil3d", "geometry"], hint: "Vertical alignment along an alignment." },
  { id: "Civil 3D Corridor", type: "concept", group: 2, radius: 11, tags: ["civil3d", "roads"], hint: "3D parametric road model." },
  { id: "Civil 3D Assembly", type: "concept", group: 2, radius: 9, tags: ["civil3d", "roads"], hint: "Cross-section template for corridors." },
  { id: "Civil 3D Subassembly", type: "concept", group: 2, radius: 8, tags: ["civil3d", "roads"], hint: "Parametric cross-section component." },
  { id: "Civil 3D Surface", type: "concept", group: 2, radius: 10, tags: ["civil3d", "terrain"], hint: "TIN or grid terrain model." },
  { id: "Civil 3D Grading", type: "skill", group: 2, radius: 9, tags: ["civil3d", "site"], hint: "Site grading with feature lines + criteria." },
  { id: "Civil 3D Pipe Network", type: "concept", group: 2, radius: 9, tags: ["civil3d", "stormwater"], hint: "Gravity sewer/storm network." },
  { id: "Civil 3D Pressure Network", type: "concept", group: 2, radius: 8, tags: ["civil3d", "water"], hint: "Pressurised water mains." },
  { id: "Civil 3D LandXML", type: "format", group: 2, radius: 8, tags: ["civil3d", "interop"], hint: "Vendor-neutral civil data exchange." },
  { id: "Creo Features", type: "concept", group: 2, radius: 9, tags: ["creo", "parametric"], hint: "Ordered feature history of a Creo part." },
  { id: "Creo Skeleton", type: "skill", group: 2, radius: 10, tags: ["creo", "top-down"], hint: "Master reference part for top-down design." },
  { id: "Creo Top-Down Design", type: "skill", group: 2, radius: 10, tags: ["creo", "assembly"], hint: "Assembly-level design driving parts." },
  { id: "Creo Layouts", type: "concept", group: 2, radius: 7, tags: ["creo", "specs"], hint: "2D spec-capture file driving downstream models." },
  { id: "Creo Sheet Metal", type: "skill", group: 2, radius: 8, tags: ["creo", "fabrication"], hint: "Wall/bend/unbend modelling." },
  { id: "Creo Style", type: "skill", group: 2, radius: 9, tags: ["creo", "surfacing"], hint: "Class-A and freeform surfacing." },
  { id: "Creo MBD", type: "skill", group: 2, radius: 8, tags: ["creo", "drawings"], hint: "Model-Based Definition on 3D model." },
  { id: "Pro/TOOLKIT", type: "sdk", group: 2, radius: 8, tags: ["creo", "api"], hint: "C API for Creo customisation." },
  { id: "DraftSight Concept 1", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 1 in DraftSight." },
  { id: "DraftSight Concept 2", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 2 in DraftSight." },
  { id: "DraftSight Concept 3", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 3 in DraftSight." },
  { id: "DraftSight Concept 4", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 4 in DraftSight." },
  { id: "DraftSight Concept 5", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 5 in DraftSight." },
  { id: "DraftSight Concept 6", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 6 in DraftSight." },
  { id: "DraftSight Concept 7", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 7 in DraftSight." },
  { id: "DraftSight Concept 8", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 8 in DraftSight." },
  { id: "DraftSight Concept 9", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 9 in DraftSight." },
  { id: "DraftSight Concept 10", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 10 in DraftSight." },
  { id: "DraftSight Concept 11", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 11 in DraftSight." },
  { id: "DraftSight Concept 12", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 12 in DraftSight." },
  { id: "DraftSight Concept 13", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 13 in DraftSight." },
  { id: "DraftSight Concept 14", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 14 in DraftSight." },
  { id: "DraftSight Concept 15", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Concept 15 in DraftSight." },
  { id: "FreeCAD", type: "product", group: 1, radius: 14, tags: ["community", "foss", "mcad", "open-source"], hint: "The premier open-source parametric 3D modeler." },
  { id: "Topological Naming", type: "concept", group: 2, radius: 10, tags: ["freecad", "modeling"], hint: "Geometric reference limitation on face renaming." },
  { id: "FreeCAD Python", type: "sdk", group: 2, radius: 9, tags: ["freecad", "api"], hint: "Python scripting and macro automation console." },
  { id: "CalculiX FEM", type: "product", group: 1, radius: 9, tags: ["freecad", "simulation"], hint: "Open-source solver for FEM workbench." },
  { id: "Fusion 360", type: "product", group: 1, radius: 14, tags: ["autodesk", "cloud", "mcad", "cam"], hint: "Cloud-native unified CAD/CAM/CAE." },
  { id: "Fusion Components", type: "concept", group: 2, radius: 9, tags: ["fusion", "assembly"], hint: "Assembly containers with joints." },
  { id: "Fusion Sheet Metal", type: "skill", group: 2, radius: 8, tags: ["fusion", "fabrication"], hint: "Rule-driven flange-based modelling." },
  { id: "Fusion T-Spline", type: "concept", group: 2, radius: 8, tags: ["fusion", "surfacing"], hint: "Form workspace freeform modelling." },
  { id: "Fusion Tool Library", type: "concept", group: 2, radius: 8, tags: ["fusion", "cam"], hint: "Cataloged CNC tooling with feeds/speeds." },
  { id: "Fusion Post Processor", type: "concept", group: 2, radius: 8, tags: ["fusion", "cam"], hint: "Toolpath-to-G-code translator script." },
  { id: "Fusion Drawings", type: "skill", group: 2, radius: 8, tags: ["fusion", "documentation"], hint: "2D drawing environment." },
  { id: "Fusion Data Panel", type: "concept", group: 2, radius: 8, tags: ["fusion", "cloud"], hint: "Cloud project/folder/file UI." },
  { id: "GstarCAD Layers", type: "concept", group: 2, radius: 8, tags: ["gstarcad", "drafting"], hint: "Drawing partition system." },
  { id: "GstarCAD Object Snaps", type: "concept", group: 2, radius: 7, tags: ["gstarcad", "drafting"], hint: "Precision input snap system." },
  { id: "GstarCAD Model/Paper Space", type: "concept", group: 2, radius: 9, tags: ["gstarcad", "drafting"], hint: "Geometry and sheet composition." },
  { id: "GstarCAD Annotative", type: "concept", group: 2, radius: 8, tags: ["gstarcad", "drafting"], hint: "Scale-aware annotation system." },
  { id: "GstarCAD Dynamic Blocks", type: "concept", group: 2, radius: 9, tags: ["gstarcad", "blocks"], hint: "Parametric block definitions." },
  { id: "GstarCAD Attributes", type: "concept", group: 2, radius: 8, tags: ["gstarcad", "data"], hint: "Block-attached variable data." },
  { id: "GstarCAD Xrefs", type: "concept", group: 2, radius: 9, tags: ["gstarcad", "collaboration"], hint: "External DWG references." },
  { id: "GstarCAD Solid Editing", type: "skill", group: 2, radius: 9, tags: ["gstarcad", "3d"], hint: "3D solid Boolean and edit operations." },
  { id: "GstarCAD UCS", type: "concept", group: 2, radius: 8, tags: ["gstarcad", "3d"], hint: "User Coordinate System for 3D work." },
  { id: "GstarCAD MEP", type: "product", group: 1, radius: 11, tags: ["gstarcad", "mep", "vertical"], hint: "Mechanical/electrical/plumbing systems vertical." },
  { id: "GstarCAD Electrical", type: "product", group: 1, radius: 10, tags: ["gstarcad", "electrical", "vertical"], hint: "Electrical schematics + panel layouts." },
  { id: "GstarCAD Mapping", type: "product", group: 1, radius: 10, tags: ["gstarcad", "survey", "vertical"], hint: "Survey and mapping vertical." },
  { id: "GstarBIM", type: "product", group: 1, radius: 12, tags: ["gstarsoft", "bim", "flagship"], hint: "Gstarsoft's native BIM platform." },
  { id: "GstarCAD AutoLISP", type: "sdk", group: 2, radius: 9, tags: ["gstarcad", "api"], hint: "Full AutoLISP / Visual LISP support." },
  { id: "GstarCAD VBA", type: "sdk", group: 2, radius: 8, tags: ["gstarcad", "api"], hint: "Visual Basic for Applications inside GstarCAD." },
  { id: "GRX", type: "sdk", group: 2, radius: 9, tags: ["gstarcad", "api"], hint: "C++ runtime extension API (ObjectARX equivalent)." },
  { id: "GstarCAD AI Tools", type: "skill", group: 2, radius: 10, tags: ["gstarcad", "ai"], hint: "AI-assisted drawing review and commands." },
  { id: "Inventor Project (.ipj)", type: "concept", group: 2, radius: 8, tags: ["inventor"], hint: "Workspace/library configuration file." },
  { id: "Inventor Features", type: "concept", group: 2, radius: 9, tags: ["inventor", "parametric"], hint: "Ordered feature history of a part." },
  { id: "Inventor Joints", type: "concept", group: 2, radius: 9, tags: ["inventor", "assembly"], hint: "Single-step assembly DOF relationships." },
  { id: "Frame Generator", type: "skill", group: 2, radius: 9, tags: ["inventor", "structural"], hint: "Structural frame design tool." },
  { id: "iParts / iAssemblies", type: "concept", group: 2, radius: 8, tags: ["inventor", "variants"], hint: "Factory-table-driven family variants." },
  { id: "Content Center", type: "product", group: 1, radius: 9, tags: ["inventor", "library"], hint: "Standard parts database." },
  { id: "Vault", type: "product", group: 1, radius: 10, tags: ["autodesk", "pdm"], hint: "Autodesk's PDM for Inventor/AutoCAD/Revit." },
  { id: "Inventor Presentations", type: "skill", group: 2, radius: 7, tags: ["inventor", "documentation"], hint: "Animated exploded-view files." },
  { id: "IronCAD", type: "product", group: 1, radius: 14, tags: ["ironcad", "ironcad"], hint: "A unique dual-engine (Parasolid + ACIS) MCAD that excels at drag-and-drop catalog modeling and absolute design freedom." },
  { id: "IronCAD Concept 1", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 1 in IronCAD." },
  { id: "IronCAD Concept 2", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 2 in IronCAD." },
  { id: "IronCAD Concept 3", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 3 in IronCAD." },
  { id: "IronCAD Concept 4", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 4 in IronCAD." },
  { id: "IronCAD Concept 5", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 5 in IronCAD." },
  { id: "IronCAD Concept 6", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 6 in IronCAD." },
  { id: "IronCAD Concept 7", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 7 in IronCAD." },
  { id: "IronCAD Concept 8", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 8 in IronCAD." },
  { id: "IronCAD Concept 9", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 9 in IronCAD." },
  { id: "IronCAD Concept 10", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 10 in IronCAD." },
  { id: "IronCAD Concept 11", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 11 in IronCAD." },
  { id: "IronCAD Concept 12", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 12 in IronCAD." },
  { id: "IronCAD Concept 13", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 13 in IronCAD." },
  { id: "IronCAD Concept 14", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 14 in IronCAD." },
  { id: "IronCAD Concept 15", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Concept 15 in IronCAD." },
  { id: "MicroStation Concept 1", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 1 in MicroStation." },
  { id: "MicroStation Concept 2", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 2 in MicroStation." },
  { id: "MicroStation Concept 3", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 3 in MicroStation." },
  { id: "MicroStation Concept 4", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 4 in MicroStation." },
  { id: "MicroStation Concept 5", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 5 in MicroStation." },
  { id: "MicroStation Concept 6", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 6 in MicroStation." },
  { id: "MicroStation Concept 7", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 7 in MicroStation." },
  { id: "MicroStation Concept 8", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 8 in MicroStation." },
  { id: "MicroStation Concept 9", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 9 in MicroStation." },
  { id: "MicroStation Concept 10", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 10 in MicroStation." },
  { id: "MicroStation Concept 11", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 11 in MicroStation." },
  { id: "MicroStation Concept 12", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 12 in MicroStation." },
  { id: "MicroStation Concept 13", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 13 in MicroStation." },
  { id: "MicroStation Concept 14", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 14 in MicroStation." },
  { id: "MicroStation Concept 15", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Concept 15 in MicroStation." },
  { id: "Revit Worksets", type: "concept", group: 2, radius: 9, tags: ["revit", "collaboration"], hint: "Worksharing ownership partitions." },
  { id: "Revit Linked Models", type: "skill", group: 2, radius: 9, tags: ["revit", "coordination"], hint: "Multi-discipline RVT linking." },
  { id: "Revit Shared Coordinates", type: "concept", group: 2, radius: 8, tags: ["revit", "coordination"], hint: "Tie internal origin to real-world site." },
  { id: "Revit View Template", type: "concept", group: 2, radius: 8, tags: ["revit", "documentation"], hint: "Saved view-graphic configurations." },
  { id: "Dynamo", type: "sdk", group: 2, radius: 9, tags: ["revit", "automation"], hint: "Visual programming bundled with Revit." },
  { id: "Revit IFC Export", type: "format", group: 2, radius: 8, tags: ["revit", "ifc", "interop"], hint: "Open-standard model exchange." },
  { id: "Revit Shared Parameters", type: "concept", group: 2, radius: 8, tags: ["revit", "data"], hint: "External GUID-keyed parameter store." },
  { id: "Rhinoceros", type: "product", group: 1, radius: 14, tags: ["mcneel", "rhinoceros"], hint: "The ultimate 3D NURBS-based geometric modeler, famed for complex freeform curves and Grasshopper algorithmic automation." },
  { id: "Rhinoceros Concept 1", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 1 in Rhinoceros." },
  { id: "Rhinoceros Concept 2", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 2 in Rhinoceros." },
  { id: "Rhinoceros Concept 3", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 3 in Rhinoceros." },
  { id: "Rhinoceros Concept 4", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 4 in Rhinoceros." },
  { id: "Rhinoceros Concept 5", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 5 in Rhinoceros." },
  { id: "Rhinoceros Concept 6", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 6 in Rhinoceros." },
  { id: "Rhinoceros Concept 7", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 7 in Rhinoceros." },
  { id: "Rhinoceros Concept 8", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 8 in Rhinoceros." },
  { id: "Rhinoceros Concept 9", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 9 in Rhinoceros." },
  { id: "Rhinoceros Concept 10", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 10 in Rhinoceros." },
  { id: "Rhinoceros Concept 11", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 11 in Rhinoceros." },
  { id: "Rhinoceros Concept 12", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 12 in Rhinoceros." },
  { id: "Rhinoceros Concept 13", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 13 in Rhinoceros." },
  { id: "Rhinoceros Concept 14", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 14 in Rhinoceros." },
  { id: "Rhinoceros Concept 15", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Concept 15 in Rhinoceros." },
  { id: "Siemens NX", type: "product", group: 1, radius: 14, tags: ["siemens", "mcad", "cam", "high-end"], hint: "Siemens' high-end CAD/CAM/CAE platform." },
  { id: "Synchronous Technology", type: "concept", group: 2, radius: 11, tags: ["nx", "hybrid"], hint: "Direct + parametric hybrid editing." },
  { id: "NX Features", type: "concept", group: 2, radius: 9, tags: ["nx", "parametric"], hint: "Ordered parametric feature history." },
  { id: "Master Model", type: "concept", group: 2, radius: 9, tags: ["nx", "documents"], hint: "Source 3D part referenced by drawings/assemblies/CAM." },
  { id: "WAVE", type: "skill", group: 2, radius: 10, tags: ["nx", "top-down"], hint: "Inter-part linking for top-down design." },
  { id: "NX Assembly Constraints", type: "concept", group: 2, radius: 8, tags: ["nx", "assembly"], hint: "Geometric positioning of components." },
  { id: "NX PMI", type: "skill", group: 2, radius: 8, tags: ["nx", "drawings"], hint: "Product Manufacturing Information on 3D." },
  { id: "NX Sheet Metal", type: "skill", group: 2, radius: 8, tags: ["nx", "fabrication"], hint: "Tab/flange-based sheet metal." },
  { id: "NX Surfacing", type: "skill", group: 2, radius: 9, tags: ["nx", "surfacing"], hint: "Free-form and class-A surfacing." },
  { id: "NX Open", type: "sdk", group: 2, radius: 9, tags: ["nx", "api"], hint: "Multi-language API (Python/.NET/C++)." },
  { id: "SketchUp", type: "product", group: 1, radius: 14, tags: ["trimble", "sketchup"], hint: "Trimble's extremely intuitive 3D conceptual design and presentation modeler, highly popular in architecture." },
  { id: "SketchUp Concept 1", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 1 in SketchUp." },
  { id: "SketchUp Concept 2", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 2 in SketchUp." },
  { id: "SketchUp Concept 3", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 3 in SketchUp." },
  { id: "SketchUp Concept 4", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 4 in SketchUp." },
  { id: "SketchUp Concept 5", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 5 in SketchUp." },
  { id: "SketchUp Concept 6", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 6 in SketchUp." },
  { id: "SketchUp Concept 7", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 7 in SketchUp." },
  { id: "SketchUp Concept 8", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 8 in SketchUp." },
  { id: "SketchUp Concept 9", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 9 in SketchUp." },
  { id: "SketchUp Concept 10", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 10 in SketchUp." },
  { id: "SketchUp Concept 11", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 11 in SketchUp." },
  { id: "SketchUp Concept 12", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 12 in SketchUp." },
  { id: "SketchUp Concept 13", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 13 in SketchUp." },
  { id: "SketchUp Concept 14", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 14 in SketchUp." },
  { id: "SketchUp Concept 15", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Concept 15 in SketchUp." },
  { id: "SOLIDWORKS Mates", type: "concept", group: 2, radius: 10, tags: ["solidworks", "assembly"], hint: "Geometric constraints between assembly components." },
  { id: "SOLIDWORKS Design Tables", type: "concept", group: 2, radius: 8, tags: ["solidworks", "automation"], hint: "Excel-driven configuration tables." },
  { id: "SOLIDWORKS Sheet Metal", type: "skill", group: 2, radius: 9, tags: ["solidworks", "fabrication"], hint: "Flange-driven fabricated sheet metal." },
  { id: "SOLIDWORKS Weldments", type: "skill", group: 2, radius: 9, tags: ["solidworks", "fabrication"], hint: "Multi-body structural welded frames." },
  { id: "SOLIDWORKS Feature Tree", type: "concept", group: 2, radius: 10, tags: ["solidworks", "parametric"], hint: "Ordered feature history of a part." },
  { id: "SOLIDWORKS MBD", type: "skill", group: 2, radius: 8, tags: ["solidworks", "drawings", "gdt"], hint: "Model-based definition replacing 2D drawings." },
  { id: "SOLIDWORKS Simulation", type: "product", group: 1, radius: 9, tags: ["solidworks", "fea"], hint: "Integrated FEA for SOLIDWORKS models." },
  { id: "SOLIDWORKS Toolbox", type: "concept", group: 2, radius: 8, tags: ["solidworks", "library"], hint: "Standard fasteners and hardware library." },
  { id: "ANSYS SpaceClaim", type: "product", group: 1, radius: 14, tags: ["ansys", "spaceclaim"], hint: "A high-speed direct 3D modeler built to prepare, clean, and simplify geometry for finite element analysis." },
  { id: "ANSYS SpaceClaim Concept 1", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 1 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 2", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 2 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 3", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 3 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 4", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 4 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 5", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 5 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 6", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 6 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 7", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 7 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 8", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 8 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 9", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 9 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 10", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 10 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 11", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 11 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 12", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 12 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 13", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 13 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 14", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 14 in ANSYS SpaceClaim." },
  { id: "ANSYS SpaceClaim Concept 15", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Concept 15 in ANSYS SpaceClaim." },
  { id: "Tekla Structures", type: "product", group: 1, radius: 14, tags: ["trimble", "tekla-structures"], hint: "Trimble's premier structural BIM authoring tool, delivering detailed LOD 500 models for steel and concrete." },
  { id: "Tekla Structures Concept 1", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 1 in Tekla Structures." },
  { id: "Tekla Structures Concept 2", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 2 in Tekla Structures." },
  { id: "Tekla Structures Concept 3", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 3 in Tekla Structures." },
  { id: "Tekla Structures Concept 4", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 4 in Tekla Structures." },
  { id: "Tekla Structures Concept 5", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 5 in Tekla Structures." },
  { id: "Tekla Structures Concept 6", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 6 in Tekla Structures." },
  { id: "Tekla Structures Concept 7", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 7 in Tekla Structures." },
  { id: "Tekla Structures Concept 8", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 8 in Tekla Structures." },
  { id: "Tekla Structures Concept 9", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 9 in Tekla Structures." },
  { id: "Tekla Structures Concept 10", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 10 in Tekla Structures." },
  { id: "Tekla Structures Concept 11", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 11 in Tekla Structures." },
  { id: "Tekla Structures Concept 12", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 12 in Tekla Structures." },
  { id: "Tekla Structures Concept 13", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 13 in Tekla Structures." },
  { id: "Tekla Structures Concept 14", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 14 in Tekla Structures." },
  { id: "Tekla Structures Concept 15", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Concept 15 in Tekla Structures." },
  { id: "Vectorworks", type: "product", group: 1, radius: 14, tags: ["vectorworks", "vectorworks"], hint: "A versatile BIM and CAD platform tailored for architects, landscape architects, and entertainment designers." },
  { id: "Vectorworks Concept 1", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 1 in Vectorworks." },
  { id: "Vectorworks Concept 2", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 2 in Vectorworks." },
  { id: "Vectorworks Concept 3", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 3 in Vectorworks." },
  { id: "Vectorworks Concept 4", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 4 in Vectorworks." },
  { id: "Vectorworks Concept 5", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 5 in Vectorworks." },
  { id: "Vectorworks Concept 6", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 6 in Vectorworks." },
  { id: "Vectorworks Concept 7", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 7 in Vectorworks." },
  { id: "Vectorworks Concept 8", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 8 in Vectorworks." },
  { id: "Vectorworks Concept 9", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 9 in Vectorworks." },
  { id: "Vectorworks Concept 10", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 10 in Vectorworks." },
  { id: "Vectorworks Concept 11", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 11 in Vectorworks." },
  { id: "Vectorworks Concept 12", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 12 in Vectorworks." },
  { id: "Vectorworks Concept 13", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 13 in Vectorworks." },
  { id: "Vectorworks Concept 14", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 14 in Vectorworks." },
  { id: "Vectorworks Concept 15", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Concept 15 in Vectorworks." },
  { id: "ZWCAD", type: "product", group: 1, radius: 14, tags: ["zwsoft", "dwg", "drafting", "high-speed"], hint: "ZWSOFT's high-performance DWG-native 2D/3D CAD platform." },
  { id: "ZRX SDK", type: "sdk", group: 2, radius: 9, tags: ["zwcad", "api"], hint: "ObjectARX-compatible C++ developer kit." },
  { id: "Smart Voice", type: "skill", group: 2, radius: 8, tags: ["zwcad", "ui"], hint: "Embeds audio annotations directly inside DWG." },
  { id: "Multi-Core Rendering", type: "concept", group: 2, radius: 9, tags: ["zwcad", "performance"], hint: "Multi-threaded CPU canvas acceleration." },
    /* AUTO-GEN sw-nodes END */

  ];
  const links = [
  ["AutoCAD Layer States", "AutoCAD"],
  ["AutoCAD Dynamic Blocks", "AutoCAD"],
  ["AutoCAD Sheet Sets", "AutoCAD"],
  ["AutoCAD XREF Management", "AutoCAD"],
  ["AutoCAD AutoLISP", "AutoCAD"],
  ["AutoCAD Trace", "AutoCAD"],
  ["AutoCAD Annotative Scale", "AutoCAD"],
  ["AutoCAD Paper Space", "AutoCAD"],
  ["AutoCAD Web App", "AutoCAD"],
  ["Revit Families", "Revit"],
  ["Revit Worksharing", "Revit"],
  ["Revit Schedules", "Revit"],
  ["Revit View Templates", "Revit"],
  ["Revit Dynamo", "Revit"],
  ["Revit Phasing", "Revit"],
  ["Revit Design Options", "Revit"],
  ["Revit MEP Systems", "Revit"],
  ["Inventor iLogic", "Inventor"],
  ["Inventor AnyCAD", "Inventor"],
  ["Inventor Frame Generator", "Inventor"],
  ["Inventor Sheet Metal", "Inventor"],
  ["Inventor Content Center", "Inventor"],
  ["Inventor Model States", "Inventor"],
  ["Inventor Nastran", "Inventor"],
  ["Inventor CAM", "Inventor"],
  ["Inventor Vault Integration", "Inventor"],
  ["Fusion Timeline", "Fusion"],
  ["Fusion Joints", "Fusion"],
  ["Fusion Generative Design", "Fusion"],
  ["Fusion T-Splines", "Fusion"],
  ["Fusion CAM Setup", "Fusion"],
  ["Fusion Mesh Repair", "Fusion"],
  ["Fusion Cloud Render", "Fusion"],
  ["Fusion Direct Modeling", "Fusion"],
  ["Fusion Extensions", "Fusion"],
  ["Civil 3D Corridors", "Civil 3D"],
  ["Civil 3D Alignments", "Civil 3D"],
  ["Civil 3D Surfaces", "Civil 3D"],
  ["Civil 3D Feature Lines", "Civil 3D"],
  ["Civil 3D Pipe Networks", "Civil 3D"],
  ["Civil 3D Data Shortcuts", "Civil 3D"],
  ["Civil 3D Grading Optimization", "Civil 3D"],
  ["Civil 3D Assemblies", "Civil 3D"],
  ["Civil 3D Parcels", "Civil 3D"],
  ["Navisworks Clash Detective", "Navisworks"],
  ["Navisworks TimeLiner", "Navisworks"],
  ["Navisworks Quantification", "Navisworks"],
  ["Navisworks NWD Format", "Navisworks"],
  ["Navisworks Viewpoints", "Navisworks"],
  ["Navisworks SwitchBack", "Navisworks"],
  ["Navisworks Search Sets", "Navisworks"],
  ["Navisworks Point Cloud Rendering", "Navisworks"],
  ["Navisworks Animator", "Navisworks"],
  ["SOLIDWORKS SpeedPak", "SOLIDWORKS"],
  ["SOLIDWORKS SmartMates", "SOLIDWORKS"],
  ["CATIA GSD", "CATIA"],
  ["CATIA PowerCopy", "CATIA"],
  ["Creo Parametric", "Creo Parametric"],
  ["Creo Direct", "Creo Parametric"],
  ["Creo Simulate", "Creo Parametric"],
  ["Creo Unite Technology", "Creo Parametric"],
  ["Creo Skeleton Modeling", "Creo Parametric"],
  ["Creo Flexible Modeling", "Creo Parametric"],
  ["Creo Windchill Integration", "Creo Parametric"],
  ["Creo Family Tables", "Creo Parametric"],
  ["Creo Mechanism Design", "Creo Parametric"],
  ["Creo Topology Optimization", "Creo Parametric"],
  ["GstarCAD Mech BOM", "GstarCAD"],
  ["GstarCAD Mech Intelligent Dimensions", "GstarCAD"],
  ["GstarCAD Mech Hole Chart", "GstarCAD"],
  ["GstarCAD Mech Hidden Lines", "GstarCAD"],
  ["GstarCAD Mech Standard Parts", "GstarCAD"],
  ["GstarCAD Mech Drawing Borders", "GstarCAD"],
  ["GstarCAD Mech Welding Symbols", "GstarCAD"],
  ["GstarCAD Mech Detail Views", "GstarCAD"],
  ["GstarCAD Mech Surface Texture", "GstarCAD"],
  ["GstarCAD Mech Power Erase", "GstarCAD"],
  ["FastView Cloud Sync", "DWG FastView"],
  ["FastView Mobile Markup", "DWG FastView"],
  ["FastView Inquiry Tools", "DWG FastView"],
  ["FastView Font Manager", "DWG FastView"],
  ["FastView Offline Mode", "DWG FastView"],
  ["FastView Version Compare", "DWG FastView"],
  ["FastView PDF Export", "DWG FastView"],
  ["FastView Text Extraction", "DWG FastView"],
  ["FastView Layer Control", "DWG FastView"],
  ["FastView Layout Switch", "DWG FastView"],
  ["Dassault 3DEXPERIENCE", "Dassault"],
  ["Dassault ENOVIA", "Dassault"],
  ["Dassault DELMIA", "Dassault"],
  ["Autodesk AEC Collection", "Autodesk"],
  ["Autodesk PDM Collection", "Autodesk"],
  ["Autodesk Construction Cloud", "Autodesk"],
  ["Autodesk Platform Services", "Autodesk"],
  ["Autodesk Flex", "Autodesk"],
  ["Autodesk Access", "Autodesk"],

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
    ["Software Map", "Autodesk"],
    ["Software Map", "Gstarsoft"],
    ["Software Map", "Dassault"],
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
    ["Software Map", "PTC"],
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
    ["Software Map", "Siemens"],
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
    ["Software Map", "Bentley"],
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
    ["Software Map", "AEC"],
    ["Software Map", "MFG"],
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
    ["Autodesk", "Navisworks"],
    ["Civil 3D", "Grading Optimization"],
    ["Navisworks", "NWD/NWF"],  /* AUTO-GEN sw-links START */
  ["Alibre Design", "Alibre"],
  ["Alibre Design Concept 1", "Alibre Design"],
  ["Alibre Design Concept 2", "Alibre Design"],
  ["Alibre Design Concept 3", "Alibre Design"],
  ["Alibre Design Concept 4", "Alibre Design"],
  ["Alibre Design Concept 5", "Alibre Design"],
  ["Alibre Design Concept 6", "Alibre Design"],
  ["Alibre Design Concept 7", "Alibre Design"],
  ["Alibre Design Concept 8", "Alibre Design"],
  ["Alibre Design Concept 9", "Alibre Design"],
  ["Alibre Design Concept 10", "Alibre Design"],
  ["Alibre Design Concept 11", "Alibre Design"],
  ["Alibre Design Concept 12", "Alibre Design"],
  ["Alibre Design Concept 13", "Alibre Design"],
  ["Alibre Design Concept 14", "Alibre Design"],
  ["Alibre Design Concept 15", "Alibre Design"],
  ["Allplan", "Allplan (Nemetschek)"],
  ["Allplan Concept 1", "Allplan"],
  ["Allplan Concept 2", "Allplan"],
  ["Allplan Concept 3", "Allplan"],
  ["Allplan Concept 4", "Allplan"],
  ["Allplan Concept 5", "Allplan"],
  ["Allplan Concept 6", "Allplan"],
  ["Allplan Concept 7", "Allplan"],
  ["Allplan Concept 8", "Allplan"],
  ["Allplan Concept 9", "Allplan"],
  ["Allplan Concept 10", "Allplan"],
  ["Allplan Concept 11", "Allplan"],
  ["Allplan Concept 12", "Allplan"],
  ["Allplan Concept 13", "Allplan"],
  ["Allplan Concept 14", "Allplan"],
  ["Allplan Concept 15", "Allplan"],
  ["ARES Commander", "Graebert"],
  ["ARES Commander Concept 1", "ARES Commander"],
  ["ARES Commander Concept 2", "ARES Commander"],
  ["ARES Commander Concept 3", "ARES Commander"],
  ["ARES Commander Concept 4", "ARES Commander"],
  ["ARES Commander Concept 5", "ARES Commander"],
  ["ARES Commander Concept 6", "ARES Commander"],
  ["ARES Commander Concept 7", "ARES Commander"],
  ["ARES Commander Concept 8", "ARES Commander"],
  ["ARES Commander Concept 9", "ARES Commander"],
  ["ARES Commander Concept 10", "ARES Commander"],
  ["ARES Commander Concept 11", "ARES Commander"],
  ["ARES Commander Concept 12", "ARES Commander"],
  ["ARES Commander Concept 13", "ARES Commander"],
  ["ARES Commander Concept 14", "ARES Commander"],
  ["ARES Commander Concept 15", "ARES Commander"],
  ["AutoCAD Paper Space", "AutoCAD"],
  ["AutoCAD XREF Tree", "AutoCAD"],
  ["AutoCAD Dynamic Block", "AutoCAD"],
  ["AutoCAD Sheet Set", "AutoCAD"],
  ["AutoCAD Annotative Scale", "AutoCAD"],
  ["AutoCAD AutoLISP", "AutoCAD"],
  ["AutoCAD Plot Styles", "AutoCAD"],
  ["AutoCAD Data Extraction", "AutoCAD"],
  ["AutoCAD Constraints", "AutoCAD"],
  ["AutoCAD", "Autodesk"],
  ["AutoCAD Sheet Set", "AutoCAD Paper Space"],
  ["AutoCAD Annotative Scale", "AutoCAD Paper Space"],
  ["AutoCAD Data Extraction", "AutoCAD Dynamic Block"],
  ["AVEVA Everything3D", "AVEVA"],
  ["AVEVA Everything3D Concept 1", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 2", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 3", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 4", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 5", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 6", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 7", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 8", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 9", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 10", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 11", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 12", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 13", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 14", "AVEVA Everything3D"],
  ["AVEVA Everything3D Concept 15", "AVEVA Everything3D"],
  ["BricsCAD", "Hexagon"],
  ["Direct Modeling", "BricsCAD"],
  ["BIMIFY", "BricsCAD"],
  ["BricsCAD Communicator", "BricsCAD"],
  ["CATIA", "Dassault"],
  ["CATIA Workbenches", "CATIA"],
  ["CATIA Sketcher", "CATIA Workbenches"],
  ["GSD", "CATIA Workbenches"],
  ["Multi-Section Surface", "GSD"],
  ["CATIA Product Structure", "CATIA"],
  ["Contextual Design", "CATIA Product Structure"],
  ["Publications", "Contextual Design"],
  ["DMU Navigator", "CATIA Product Structure"],
  ["CATIA Drafting", "CATIA"],
  ["Knowledgeware", "CATIA"],
  ["CAA RADE", "CATIA"],
  ["Civil 3D", "Autodesk"],
  ["Civil 3D Alignment", "Civil 3D"],
  ["Civil 3D Profile", "Civil 3D Alignment"],
  ["Civil 3D Corridor", "Civil 3D Alignment"],
  ["Civil 3D Corridor", "Civil 3D Profile"],
  ["Civil 3D Corridor", "Civil 3D Assembly"],
  ["Civil 3D Assembly", "Civil 3D Subassembly"],
  ["Civil 3D Surface", "Civil 3D"],
  ["Civil 3D Grading", "Civil 3D Surface"],
  ["Civil 3D Pipe Network", "Civil 3D"],
  ["Civil 3D Pressure Network", "Civil 3D"],
  ["Civil 3D Data Shortcuts", "Civil 3D"],
  ["Civil 3D LandXML", "Civil 3D"],
  ["Creo Parametric", "PTC"],
  ["Creo Features", "Creo Parametric"],
  ["Creo Skeleton", "Creo Parametric"],
  ["Creo Top-Down Design", "Creo Skeleton"],
  ["Creo Layouts", "Creo Top-Down Design"],
  ["Creo Family Tables", "Creo Parametric"],
  ["Creo Sheet Metal", "Creo Parametric"],
  ["Creo Style", "Creo Parametric"],
  ["Creo Flexible Modeling", "Creo Parametric"],
  ["Creo MBD", "Creo Parametric"],
  ["Windchill", "Creo Parametric"],
  ["Pro/TOOLKIT", "Creo Parametric"],
  ["DraftSight", "Dassault"],
  ["DraftSight Concept 1", "DraftSight"],
  ["DraftSight Concept 2", "DraftSight"],
  ["DraftSight Concept 3", "DraftSight"],
  ["DraftSight Concept 4", "DraftSight"],
  ["DraftSight Concept 5", "DraftSight"],
  ["DraftSight Concept 6", "DraftSight"],
  ["DraftSight Concept 7", "DraftSight"],
  ["DraftSight Concept 8", "DraftSight"],
  ["DraftSight Concept 9", "DraftSight"],
  ["DraftSight Concept 10", "DraftSight"],
  ["DraftSight Concept 11", "DraftSight"],
  ["DraftSight Concept 12", "DraftSight"],
  ["DraftSight Concept 13", "DraftSight"],
  ["DraftSight Concept 14", "DraftSight"],
  ["DraftSight Concept 15", "DraftSight"],
  ["FreeCAD", "FreeCAD Community (FOSS)"],
  ["Topological Naming", "FreeCAD"],
  ["FreeCAD Python", "FreeCAD"],
  ["CalculiX FEM", "FreeCAD"],
  ["Fusion 360", "Autodesk"],
  ["Fusion Timeline", "Fusion 360"],
  ["Fusion Components", "Fusion 360"],
  ["Fusion Joints", "Fusion Components"],
  ["Fusion Sheet Metal", "Fusion 360"],
  ["Fusion T-Spline", "Fusion 360"],
  ["Fusion Generative Design", "Fusion 360"],
  ["Fusion CAM Setup", "Fusion 360"],
  ["Fusion Tool Library", "Fusion CAM Setup"],
  ["Fusion Post Processor", "Fusion CAM Setup"],
  ["Fusion Drawings", "Fusion 360"],
  ["Fusion Data Panel", "Fusion 360"],
  ["GstarCAD", "Gstarsoft"],
  ["GstarCAD Layers", "GstarCAD"],
  ["GstarCAD Object Snaps", "GstarCAD"],
  ["GstarCAD Model/Paper Space", "GstarCAD"],
  ["GstarCAD Annotative", "GstarCAD Model/Paper Space"],
  ["GstarCAD Dynamic Blocks", "GstarCAD"],
  ["GstarCAD Attributes", "GstarCAD Dynamic Blocks"],
  ["GstarCAD Xrefs", "GstarCAD"],
  ["GstarCAD Solid Editing", "GstarCAD"],
  ["GstarCAD UCS", "GstarCAD Solid Editing"],
  ["GstarCAD Architecture", "GstarCAD"],
  ["GstarCAD Mechanical", "GstarCAD"],
  ["GstarCAD MEP", "GstarCAD"],
  ["GstarCAD Electrical", "GstarCAD"],
  ["GstarCAD Mapping", "GstarCAD"],
  ["GstarBIM", "Gstarsoft"],
  ["GstarBIM", "GstarCAD Architecture"],
  ["GstarCAD AutoLISP", "GstarCAD"],
  ["GstarCAD VBA", "GstarCAD"],
  ["GRX", "GstarCAD"],
  ["GstarCAD AI Tools", "GstarCAD"],
  ["Inventor", "Autodesk"],
  ["Inventor Project (.ipj)", "Inventor"],
  ["Inventor Features", "Inventor"],
  ["Inventor Joints", "Inventor"],
  ["Frame Generator", "Inventor"],
  ["Inventor Sheet Metal", "Inventor"],
  ["iLogic", "Inventor"],
  ["iParts / iAssemblies", "Inventor"],
  ["Content Center", "Inventor"],
  ["Vault", "Inventor"],
  ["Inventor Presentations", "Inventor"],
  ["Inventor Model States", "Inventor"],
  ["IronCAD", "IronCAD LLC"],
  ["IronCAD Concept 1", "IronCAD"],
  ["IronCAD Concept 2", "IronCAD"],
  ["IronCAD Concept 3", "IronCAD"],
  ["IronCAD Concept 4", "IronCAD"],
  ["IronCAD Concept 5", "IronCAD"],
  ["IronCAD Concept 6", "IronCAD"],
  ["IronCAD Concept 7", "IronCAD"],
  ["IronCAD Concept 8", "IronCAD"],
  ["IronCAD Concept 9", "IronCAD"],
  ["IronCAD Concept 10", "IronCAD"],
  ["IronCAD Concept 11", "IronCAD"],
  ["IronCAD Concept 12", "IronCAD"],
  ["IronCAD Concept 13", "IronCAD"],
  ["IronCAD Concept 14", "IronCAD"],
  ["IronCAD Concept 15", "IronCAD"],
  ["MicroStation", "Bentley"],
  ["MicroStation Concept 1", "MicroStation"],
  ["MicroStation Concept 2", "MicroStation"],
  ["MicroStation Concept 3", "MicroStation"],
  ["MicroStation Concept 4", "MicroStation"],
  ["MicroStation Concept 5", "MicroStation"],
  ["MicroStation Concept 6", "MicroStation"],
  ["MicroStation Concept 7", "MicroStation"],
  ["MicroStation Concept 8", "MicroStation"],
  ["MicroStation Concept 9", "MicroStation"],
  ["MicroStation Concept 10", "MicroStation"],
  ["MicroStation Concept 11", "MicroStation"],
  ["MicroStation Concept 12", "MicroStation"],
  ["MicroStation Concept 13", "MicroStation"],
  ["MicroStation Concept 14", "MicroStation"],
  ["MicroStation Concept 15", "MicroStation"],
  ["Revit", "Autodesk"],
  ["Revit Families", "Revit"],
  ["Revit Worksets", "Revit"],
  ["Revit Linked Models", "Revit"],
  ["Revit Shared Coordinates", "Revit Linked Models"],
  ["Revit Phasing", "Revit"],
  ["Revit View Template", "Revit"],
  ["Revit Schedules", "Revit"],
  ["Revit Schedules", "Revit Families"],
  ["Dynamo", "Revit"],
  ["Revit IFC Export", "Revit"],
  ["Navisworks", "Revit"],
  ["Navisworks", "Autodesk"],
  ["Revit IFC Export", "Navisworks"],
  ["Revit Shared Parameters", "Revit Families"],
  ["Rhinoceros", "McNeel & Associates"],
  ["Rhinoceros Concept 1", "Rhinoceros"],
  ["Rhinoceros Concept 2", "Rhinoceros"],
  ["Rhinoceros Concept 3", "Rhinoceros"],
  ["Rhinoceros Concept 4", "Rhinoceros"],
  ["Rhinoceros Concept 5", "Rhinoceros"],
  ["Rhinoceros Concept 6", "Rhinoceros"],
  ["Rhinoceros Concept 7", "Rhinoceros"],
  ["Rhinoceros Concept 8", "Rhinoceros"],
  ["Rhinoceros Concept 9", "Rhinoceros"],
  ["Rhinoceros Concept 10", "Rhinoceros"],
  ["Rhinoceros Concept 11", "Rhinoceros"],
  ["Rhinoceros Concept 12", "Rhinoceros"],
  ["Rhinoceros Concept 13", "Rhinoceros"],
  ["Rhinoceros Concept 14", "Rhinoceros"],
  ["Rhinoceros Concept 15", "Rhinoceros"],
  ["Siemens NX", "Siemens"],
  ["Synchronous Technology", "Siemens NX"],
  ["NX Features", "Siemens NX"],
  ["Master Model", "Siemens NX"],
  ["WAVE", "Siemens NX"],
  ["NX Assembly Constraints", "Siemens NX"],
  ["NX PMI", "Master Model"],
  ["NX Sheet Metal", "Siemens NX"],
  ["NX Surfacing", "Siemens NX"],
  ["NX CAM", "Siemens NX"],
  ["Teamcenter", "Siemens NX"],
  ["NX Open", "Siemens NX"],
  ["SketchUp", "Trimble"],
  ["SketchUp Concept 1", "SketchUp"],
  ["SketchUp Concept 2", "SketchUp"],
  ["SketchUp Concept 3", "SketchUp"],
  ["SketchUp Concept 4", "SketchUp"],
  ["SketchUp Concept 5", "SketchUp"],
  ["SketchUp Concept 6", "SketchUp"],
  ["SketchUp Concept 7", "SketchUp"],
  ["SketchUp Concept 8", "SketchUp"],
  ["SketchUp Concept 9", "SketchUp"],
  ["SketchUp Concept 10", "SketchUp"],
  ["SketchUp Concept 11", "SketchUp"],
  ["SketchUp Concept 12", "SketchUp"],
  ["SketchUp Concept 13", "SketchUp"],
  ["SketchUp Concept 14", "SketchUp"],
  ["SketchUp Concept 15", "SketchUp"],
  ["SOLIDWORKS", "Dassault"],
  ["SOLIDWORKS Mates", "SOLIDWORKS"],
  ["SOLIDWORKS Configurations", "SOLIDWORKS"],
  ["SOLIDWORKS Design Tables", "SOLIDWORKS Configurations"],
  ["SOLIDWORKS Sheet Metal", "SOLIDWORKS"],
  ["SOLIDWORKS Weldments", "SOLIDWORKS"],
  ["SOLIDWORKS Feature Tree", "SOLIDWORKS"],
  ["SOLIDWORKS PDM", "SOLIDWORKS"],
  ["SOLIDWORKS MBD", "SOLIDWORKS"],
  ["SOLIDWORKS Simulation", "SOLIDWORKS"],
  ["SOLIDWORKS Toolbox", "SOLIDWORKS"],
  ["eDrawings", "SOLIDWORKS"],
  ["ANSYS SpaceClaim", "ANSYS"],
  ["ANSYS SpaceClaim Concept 1", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 2", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 3", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 4", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 5", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 6", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 7", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 8", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 9", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 10", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 11", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 12", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 13", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 14", "ANSYS SpaceClaim"],
  ["ANSYS SpaceClaim Concept 15", "ANSYS SpaceClaim"],
  ["Tekla Structures", "Trimble"],
  ["Tekla Structures Concept 1", "Tekla Structures"],
  ["Tekla Structures Concept 2", "Tekla Structures"],
  ["Tekla Structures Concept 3", "Tekla Structures"],
  ["Tekla Structures Concept 4", "Tekla Structures"],
  ["Tekla Structures Concept 5", "Tekla Structures"],
  ["Tekla Structures Concept 6", "Tekla Structures"],
  ["Tekla Structures Concept 7", "Tekla Structures"],
  ["Tekla Structures Concept 8", "Tekla Structures"],
  ["Tekla Structures Concept 9", "Tekla Structures"],
  ["Tekla Structures Concept 10", "Tekla Structures"],
  ["Tekla Structures Concept 11", "Tekla Structures"],
  ["Tekla Structures Concept 12", "Tekla Structures"],
  ["Tekla Structures Concept 13", "Tekla Structures"],
  ["Tekla Structures Concept 14", "Tekla Structures"],
  ["Tekla Structures Concept 15", "Tekla Structures"],
  ["Vectorworks", "Vectorworks (Nemetschek)"],
  ["Vectorworks Concept 1", "Vectorworks"],
  ["Vectorworks Concept 2", "Vectorworks"],
  ["Vectorworks Concept 3", "Vectorworks"],
  ["Vectorworks Concept 4", "Vectorworks"],
  ["Vectorworks Concept 5", "Vectorworks"],
  ["Vectorworks Concept 6", "Vectorworks"],
  ["Vectorworks Concept 7", "Vectorworks"],
  ["Vectorworks Concept 8", "Vectorworks"],
  ["Vectorworks Concept 9", "Vectorworks"],
  ["Vectorworks Concept 10", "Vectorworks"],
  ["Vectorworks Concept 11", "Vectorworks"],
  ["Vectorworks Concept 12", "Vectorworks"],
  ["Vectorworks Concept 13", "Vectorworks"],
  ["Vectorworks Concept 14", "Vectorworks"],
  ["Vectorworks Concept 15", "Vectorworks"],
  ["ZWCAD", "ZWSOFT"],
  ["ZRX SDK", "ZWCAD"],
  ["Smart Voice", "ZWCAD"],
  ["Multi-Core Rendering", "ZWCAD"],
    /* AUTO-GEN sw-links END */

  ];
  const beginnerPath = [
    "CAD Basics",
    "Terminology",
    "2D Drafting",
    "Command Line",
    "File Formats",
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
    // Deep Ink Engineering — graph palette aligned with site tokens.
    // Vendor + flagship product nodes use champagne to signal authority.
    const colorMap = {
      concept: "#7C8AFF",   // sapphire-violet (primary)
      skill:   "#A6B0FF",   // softer sapphire for skills/workflows
      domain:  "#8A6BC7",   // muted violet for industry lanes
      format:  "#5DC2A7",   // sage — file/schema neutral
      resource:"#D9B074",   // champagne — meta / curated nodes
      vendor:  "#E8C68A",   // champagne brighter — vendors
      product: "#5BB6E5",   // cool steel blue — products
      sdk:     "#B198F2",   // lilac — SDKs / extensions
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

    // Compute link degrees dynamically (frequently appearing / connected nodes are larger)
    const degreeMap = {};
    simNodes.forEach((n) => { degreeMap[n.id] = 0; });
    links.forEach(([source, target]) => {
      if (degreeMap[source] !== undefined) degreeMap[source]++;
      if (degreeMap[target] !== undefined) degreeMap[target]++;
    });

    let width = Math.max(graphStage?.clientWidth || 920, 320);
    let height = computeGraphHeight();

    const cxSeed = width / 2;
    const cySeed = height / 2;
    const ring = Math.min(width, height) * 0.26;
    simNodes.forEach((n, i, arr) => {
      const ang = (i / Math.max(arr.length, 1)) * Math.PI * 2 - Math.PI / 2;
      n.x = cxSeed + ring * Math.cos(ang);
      n.y = cySeed + ring * Math.sin(ang);
      
      const deg = degreeMap[n.id] || 0;
      // Core base size is 12. Connective nodes get larger up to +12px (max 24px)
      const sizeBoost = Math.min(deg * 1.5, 12);
      const baseSize = 12 + sizeBoost;
      n.baseRadius = n.type === "vendor" ? baseSize + 3 : baseSize;
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
          .distance(110)
          .strength(0.6)
      )
      .force("charge", d3.forceManyBody().strength(-240))
      .force("x", d3.forceX(width / 2).strength(0.16))
      .force("y", d3.forceY(height / 2).strength(0.16))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius((d) => d.baseRadius + 22))
      .velocityDecay(0.18); // Stable initial decay

    // Kinetic entrance animation settling smoothly
    simulation.alpha(1.2).restart();
    setTimeout(() => {
      simulation.velocityDecay(0.38);
    }, 2000);

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

    // Visible shape circle
    nodeG
      .append("circle")
      .attr("class", "kb-graph-node-shape")
      .attr("r", (d) => d.radius || d.baseRadius || 8)
      .attr("stroke", "#ffffff")
      .attr("stroke-width", 2)
      .attr("fill", (d) => colorMap[d.type] || "#8b9dcf")
      .style("filter", "none");

    // Text label
    nodeG
      .append("text")
      .attr("class", "kb-graph-node-label")
      .attr("text-anchor", "middle")
      .attr("dy", (d) => d.baseRadius + 16)
      .text((d) => d.id);

    // Fixed-size invisible interaction sensor overlay on top
    nodeG
      .append("circle")
      .attr("class", "kb-graph-node-sensor")
      .attr("r", (d) => Math.max(d.baseRadius + 15, 35))
      .attr("fill", "transparent");

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

    const nodeUrlMap = {
      "CAD Basics": "./knowledge-base.html",
      "Terminology": "./kb-terms.html",
      "2D Drafting": "./knowledge-roadmap.html",
      "3D Modeling": "./knowledge-roadmap.html",
      "Command Line": "./kb/concepts/command-alias.html",
      "File Formats": "./kb-terms.html",
      "AEC": "./knowledge-domains.html#aec-detail",
      "MFG": "./knowledge-domains.html#mfg-detail",
      "BIM": "./kb/concepts/bim.html",
      "DWG": "./kb/concepts/dwg-compatibility.html",
      "STEP": "./knowledge-cax.html",
      "IFC": "./kb/concepts/ifc-interoperability.html",
      "Software Map": "./kb-software.html",
      "Autodesk": "./kb/vendors/autodesk.html",
      "AutoCAD": "./kb/software/autocad.html",
      "Revit": "./kb/software/revit.html",
      "Gstarsoft": "./kb/vendors/gstarsoft.html",
      "GstarCAD": "./kb/software/gstarcad.html",
      "DWG FastView": "./kb/software/dwg-fastview.html",
      "DWG Compare": "./kb/concepts/dwg-compare.html",
      "Parametric Constraints": "./kb/concepts/parametric-constraints.html",
      "Drawing Merge": "./kb/concepts/drawing-merge.html",
      "Grasshopper": "./kb-software.html",
      "CAD SDK ecosystem": "./kb-software.html#cad-sdk",
      "Apryse CAD SDK": "./kb-software.html#cad-sdk",
      "HOOPS Visualize": "./kb-software.html#cad-sdk",
      "Datakit": "./kb-software.html#cad-sdk",
      "Civil 3D": "./kb/software/civil-3d.html",
      "Inventor": "./kb/software/inventor.html",
      "Fusion": "./kb/software/fusion-360.html",
      "Navisworks": "./kb/concepts/navisworks-formats.html",
      "GstarCAD Mechanical": "./kb/software/gstarcad-mechanical.html",
      "GstarCAD Architecture": "./kb/software/gstarcad-architecture.html",
      "Intelligent Objects": "./kb/concepts/intelligent-objects.html",
      "Mobile BIM": "./kb/concepts/bim-mobile-viewing.html",
      "Python API": "./kb/concepts/python-api.html",
      "PyRx": "./kb/concepts/grx-sdk.html",
      "Hardware Acceleration": "./kb/concepts/hardware-acceleration.html",
      "Smart Blocks": "./kb/concepts/smart-blocks.html",
      "Cloud Worksharing": "./kb/concepts/cloud-worksharing.html",
      "Scan to BIM": "./kb/concepts/scan-to-bim.html",
      "Generative Design": "./kb/concepts/generative-design.html",
      "iLogic": "./kb/concepts/ilogic-automation.html",
      "NWD/NWF": "./kb/concepts/navisworks-formats.html",
      "Grading Optimization": "./kb/concepts/grading-optimization.html",
      "Sheet Set Manager": "./kb/concepts/sheet-set-manager.html",
      "Annotative Scaling": "./kb/concepts/annotative-scaling.html",
      "GRX SDK": "./kb/concepts/grx-sdk.html",
      "CUI Custom": "./kb/concepts/cui-customization.html",
      "Data Link": "./kb/concepts/data-link.html",
      "SuperHatch": "./kb/concepts/superhatch.html",
      "PDF to DWG": "./kb/concepts/pdf-to-dwg.html",
      "Dassault": "./kb-software.html",
      "DraftSight": "./kb-software.html",
      "PowerTrim": "./kb/concepts/powertrim-efficiency.html",
      "G-Code Gen": "./kb/concepts/g-code-generator.html",
      "Mechanical Toolbox": "./kb/concepts/mechanical-toolbox.html",
      "3DEXPERIENCE": "./kb/concepts/3dexperience-platform.html",
      "Image Tracer": "./kb/concepts/image-tracer.html",
      "DraftSight API": "./kb/concepts/draftsight-api.html",
      "Smart Blocks (DS)": "./kb/concepts/smart-block-ds.html",
      "Mech Symbols": "./kb/concepts/ds-mechanical-symbols.html",
      "Batch Print": "./kb/concepts/ds-batch-print.html",
      "Alias Custom": "./kb/concepts/ds-alias-customization.html",
      "LISP (DS)": "./kb/concepts/ds-lisp-automation.html",
      "Xref (DS)": "./kb/concepts/ds-xref-manager.html",
      "Properties (DS)": "./kb/concepts/ds-entity-properties.html",
      "SSM (DS)": "./kb/concepts/ds-sheet-set-manager.html",
      "3D (DS)": "./kb/concepts/ds-3d-modeling.html",
      "Markup (DS)": "./kb/concepts/ds-markup-tools.html",
      "Licensing (DS)": "./kb/concepts/ds-license-types.html",
      "Perf Tuning": "./kb/concepts/ds-performance-tuning.html",
      "Interop (DS)": "./kb/concepts/ds-file-interoperability.html",
      "PTC": "./kb-software.html",
      "Creo Parametric": "./kb-software.html",
      "Windchill": "./kb/concepts/windchill-pdm.html",
      "Skeleton Modeling": "./kb/concepts/skeleton-modeling.html",
      "Flexible Modeling": "./kb/concepts/creo-flexible-modeling.html",
      "Regeneration Logic": "./kb/concepts/creo-regeneration-logic.html",
      "Mathcad": "./kb-software.html",
      "MBD (PTC)": "./kb/concepts/creo-mbd.html",
      "Generative (PTC)": "./kb/concepts/creo-generative-design.html",
      "Additive (PTC)": "./kb/concepts/creo-additive-mfg.html",
      "Cabling (PTC)": "./kb/concepts/creo-cabling-harness.html",
      "Piping (PTC)": "./kb/concepts/creo-piping-design.html",
      "Sheetmetal (PTC)": "./kb/concepts/creo-sheetmetal-design.html",
      "Mechanism (PTC)": "./kb/concepts/creo-mechanism-sim.html",
      "Sim Live (PTC)": "./kb/concepts/creo-simulation-live.html",
      "ISDX (PTC)": "./kb/concepts/creo-isdx-surfacing.html",
      "TDD (PTC)": "./kb/concepts/creo-top-down-design.html",
      "Mapkeys (PTC)": "./kb/concepts/creo-mapkeys.html",
      "Config.pro (PTC)": "./kb/concepts/creo-config-pro.html",
      "Simp Reps (PTC)": "./kb/concepts/creo-simplified-reps.html",
      "Siemens": "./kb-software.html",
      "NX": "./kb-software.html",
      "Solid Edge": "./kb-software.html",
      "Teamcenter": "./kb/concepts/teamcenter-plm.html",
      "Synchronous Tech": "./kb/concepts/siemens-synchronous-technology.html",
      "WAVE Linker": "./kb/concepts/nx-wave-geometry-linker.html",
      "Simcenter": "./kb/concepts/simcenter-nastran.html",
      "Convergent Modeling": "./kb/concepts/siemens-convergent-modeling.html",
      "PMI (Siemens)": "./kb/concepts/siemens-pmi-mbd.html",
      "Active Workspace": "./kb/concepts/teamcenter-active-workspace.html",
      "Check-Mate": "./kb/concepts/nx-check-mate.html",
      "NX CAM": "./kb/concepts/nx-cam-manufacturing.html",
      "NX MCD": "./kb/concepts/nx-mcd-simulation.html",
      "NX PTS": "./kb/concepts/nx-product-template-studio.html",
      "NX Layout": "./kb/concepts/nx-layout-design.html",
      "NX Mold Wizard": "./kb/concepts/nx-mold-wizard.html",
      "NX Progressive Die": "./kb/concepts/nx-progressive-die-wizard.html",
      "Nastran": "./kb/concepts/simcenter-nastran.html",
      "Realize Shape": "./kb/concepts/nx-realize-shape.html",
      "NX Flow": "./kb/concepts/nx-flow-simulation.html",
      "Multi-CAD (Siemens)": "./kb/concepts/siemens-multi-cad-mgmt.html",
      "NX Expressions": "./kb/concepts/nx-expressions.html",
      "HD3D": "./kb/concepts/nx-hd3d-reporting.html",
      "Bentley": "./kb-software.html",
      "MicroStation": "./kb/concepts/bentley-microstation.html",
      "OpenRoads": "./kb/concepts/openroads-designer.html",
      "ProjectWise": "./kb/concepts/projectwise-collaboration.html",
      "iTwin": "./kb/concepts/bentley-itwin-platform.html",
      "DGN Format": "./kb/concepts/bentley-microstation.html",
      "STAAD.Pro": "./kb/concepts/bentley-staad-pro.html",
      "SYNCHRO": "./kb/concepts/synchro-4d-construction.html",
      "WaterGEMS": "./kb/concepts/bentley-watergems.html",
      "RAM Structural": "./kb/concepts/ram-structural-system.html",
      "HAMMER": "./kb/concepts/bentley-hammer-transient.html",
      "LumenRT": "./kb/concepts/bentley-lumenrt.html",
      "AssetWise": "./kb/concepts/bentley-assetwise.html",
      "SewerGEMS": "./kb/concepts/bentley-sewergems.html",
      "gINT": "./kb/concepts/bentley-gint-geotech.html",
      "AutoPIPE": "./kb/concepts/bentley-autopipe.html",
      "SACS": "./kb/concepts/bentley-sacs-offshore.html",
      "ProSteel": "./kb/concepts/bentley-prosteel.html",
      "CONNECT Ed.": "./kb/concepts/microstation-connect-edition.html",
      "iModels": "./kb/concepts/bentley-imodels.html",
      "ContextCapture": "./kb/concepts/bentley-contextcapture.html",
      "SOLIDWORKS": "./kb-software.html",
      "CATIA": "./kb/concepts/catia-part-design.html",
      "ENOVIA": "./kb/concepts/enovia-plm.html",
      "SIMULIA": "./kb/concepts/simulia-abaqus.html",
      "DELMIA": "./kb/concepts/delmia-digital-mfg.html",
      "SOLIDWORKS PDM": "./kb/concepts/solidworks-pdm.html",
      "CATIA GSD": "./kb/concepts/catia-gsd.html",
      "CAA SDK": "./kb/concepts/catia-caa-sdk.html",
      "SOLIDWORKS API": "./kb/concepts/solidworks-api.html",
      "SOLIDWORKS Configurations": "./kb/concepts/solidworks-configurations.html",
      "Abaqus": "./kb/concepts/simulia-abaqus.html",
      "PowerCopy": "./kb/concepts/catia-part-design.html",
      "Hybrid Design": "./kb/concepts/catia-v5-v6-hybrid.html",
      "Composites Design": "./kb/concepts/catia-composites-design.html",
      "FT&A MBD": "./kb/concepts/siemens-pmi-mbd.html",
      "SpeedPak": "./kb/concepts/large-assembly.html",
      "eDrawings": "./kb/concepts/solidworks-edrawings.html",
      "Collaborative Sharing": "./kb/concepts/3dexperience-collaborative-sharing.html",
      "Large Design Review": "./kb/concepts/large-assembly.html",
      "Weldments (SW)": "./kb/concepts/solidworks-weldments.html",
      "Sheet Metal (SW)": "./kb/concepts/solidworks-sheetmetal.html",
      "Part Design (CATIA)": "./kb/concepts/catia-part-design.html",
      "Assembly Design (CATIA)": "./kb/concepts/catia-assembly-design.html",
      "DELMIA Simulation": "./kb/concepts/delmia-digital-mfg.html"
    };

    function selectGraphNode(d, opts) {
      const o = opts || {};
      const doZoom = o.zoom !== false;
      const replaceURL = !!o.replaceURL;
      const silentURL = !!o.silentURL;
      const actions = document.getElementById("kbInfoActions");
      const detailsBtn = document.getElementById("kbViewDetailsBtn");
      if (actions && detailsBtn) {
        actions.style.display = "block";
        const customUrl = nodeUrlMap[d.id];
        if (customUrl) {
          detailsBtn.href = customUrl;
        } else {
          const slug = d.id.toLowerCase().replace(/\s+/g, "-");
          detailsBtn.href = `./kb/concepts/${slug}.html`;
        }
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
          if (focusId) {
            // Highlight connected lines, completely fade out others
            return (focusId === sa || focusId === tb) ? 0.95 : 0.03;
          }
          return 0.15; // steady idle state opacity
        })
        .style("stroke-width", (d) => {
          const sa = typeof d.source === "object" ? d.source.id : d.source;
          const tb = typeof d.target === "object" ? d.target.id : d.target;
          if (focusId) {
            return (focusId === sa || focusId === tb) ? 3.5 : 1.0;
          }
          return 1.5;
        })
        .style("stroke", (d) => {
          const sa = typeof d.source === "object" ? d.source.id : d.source;
          const tb = typeof d.target === "object" ? d.target.id : d.target;
          if (focusId) {
            if (focusId === sa || focusId === tb) {
              const otherId = focusId === sa ? tb : sa;
              const otherNode = simNodes.find((x) => x.id === otherId);
              return otherNode ? colorMap[otherNode.type] : "var(--accent)";
            }
          }
          return "#475569";
        });

      // Update Nodes
      nodeG.each(function (d) {
        const isFocus = d.id === focusId;
        const isRel = rel && rel.has(d.id);
        const match = activeFilter === "all" || d.tags.includes(activeFilter);
        const g = d3.select(this);

        const op = match ? (focusId ? (isRel ? 1 : 0.2) : 1) : 0.1;
        
        g.style("opacity", op);
        g.classed("kb-focus", isFocus); // Toggle focus class for high contrast CSS animations

        g.select(".kb-graph-node-shape")
          .attr("r", isFocus ? d.baseRadius * 1.25 : d.baseRadius)
          .attr("stroke-width", isFocus ? 3.5 : 2)
          .attr("stroke", "#ffffff")
          .attr("fill", colorMap[d.type] || "#8b9dcf")
          .style("filter", null); // Remove hardcoded override to allow CSS filters to work!

        g.select(".kb-graph-node-label")
          .attr("dy", isFocus ? d.baseRadius * 1.25 + 18 : d.baseRadius + 16)
          .style("font-weight", isFocus ? "800" : "700")
          .style("font-size", isFocus ? "13px" : "11px");
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
        const customUrl = nodeUrlMap[d.id];
        const dest = customUrl || `./kb/concepts/${d.id.toLowerCase().replace(/\s+/g, "-")}.html`;
        
        // Protocol check: file:// protocol blocks HEAD fetches, so navigate directly
        if (window.location.protocol === "file:") {
          window.location.href = dest;
          return;
        }

        // Live check to prevent 404 and fallback elegantly
        fetch(dest, { method: "HEAD" })
          .then((res) => {
            if (res.ok) {
              window.location.href = dest;
            } else {
              window.location.href = `./kb-terms.html?search=${encodeURIComponent(d.id)}`;
            }
          })
          .catch(() => {
            window.location.href = dest;
          });
      })
      .on("dblclick", (event, d) => {
        event.stopPropagation();
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
