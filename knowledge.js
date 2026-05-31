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
    { id: "Altium", type: "vendor", group: 1, radius: 12, tags: ["altium"], hint: "Leader in printed circuit board (PCB) design tools." },
    { id: "Community (FOSS)", type: "vendor", group: 1, radius: 12, tags: ["community", "foss"], hint: "Open source community collaborative developers." },
    { id: "COMSOL", type: "vendor", group: 1, radius: 12, tags: ["comsol"], hint: "Leader in multiphysics finite element simulation." },
    { id: "OpenFOAM Foundation", type: "vendor", group: 1, radius: 12, tags: ["openfoam"], hint: "Developer of open source computational fluid dynamics." },
    { id: "Nemetschek", type: "vendor", group: 1, radius: 12, tags: ["nemetschek"], hint: "Parent of Archicad, Allplan, Vectorworks, and Solibri." },
  /* AUTO-GEN sw-nodes START */
  { id: "3ds Max", type: "product", group: 1, radius: 14, tags: ["3dsmax", "3dsmax"], hint: "Autodesk's premium 3D modeling, animation, and rendering software, widely used for architectural visualization.", slug: "3dsmax" },
  { id: "Subdivision Polygonal Modeling (3ds Max)", type: "concept", group: 2, radius: 8, tags: ["3dsmax"], hint: "High-fidelity polygon mesh creation for complex forms.", slug: "3dsmax-polygonal-modeling" },
  { id: "Arnold Path-Tracing Renderer (3ds Max)", type: "concept", group: 2, radius: 8, tags: ["3dsmax"], hint: "Physically-based path-tracing engine for realistic outputs.", slug: "3dsmax-arnold-renderer" },
  { id: "Abaqus FEA", type: "product", group: 1, radius: 14, tags: ["abaqus", "abaqus"], hint: "SIMULIA's flagship suite for high-end finite element analysis, renowned for its advanced non-linear solver and explicit dynamics.", slug: "abaqus" },
  { id: "Abaqus Explicit Dynamics (Abaqus)", type: "concept", group: 2, radius: 8, tags: ["abaqus"], hint: "Time-integration solver for highly transient non-linear events.", slug: "abaqus-explicit-dynamics" },
  { id: "User Material Subroutine UMAT (Abaqus)", type: "concept", group: 2, radius: 8, tags: ["abaqus"], hint: "Custom FORTRAN/C++ material constitutive law hook.", slug: "abaqus-umat" },
  { id: "Alibre Design", type: "product", group: 1, radius: 14, tags: ["alibredesign", "alibre-design"], hint: "A high-precision, budget-friendly parametric 3D solid modeler for mechanical parts and assemblies.", slug: "alibre-design" },
  { id: "Parametric Dimension Driver (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Driving sketch and feature parameters using logical mathematical variables.", slug: "alibre-design-term-1" },
  { id: "Geometric Constraints (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Rules governing the relative positioning and behavior of sketch elements.", slug: "alibre-design-term-2" },
  { id: "Feature History Tree (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "The chronological stack of active modeling operations in parametric design.", slug: "alibre-design-term-3" },
  { id: "Assembly Mates (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "3D constraints linking coordinate systems and surfaces of components.", slug: "alibre-design-term-4" },
  { id: "B-Rep Solid Engine (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Boundary Representation mathematical representation of solid geometry.", slug: "alibre-design-term-5" },
  { id: "Sheet Metal Flanges (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Bent sheet panels created relative to baseline flat sheets.", slug: "alibre-design-term-6" },
  { id: "2D Drafting Sheets (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Production-ready orthogonal and auxiliary drawing representations.", slug: "alibre-design-term-7" },
  { id: "Alibre Script (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Python-based scripting API for automation and custom tools.", slug: "alibre-design-term-8" },
  { id: "Equations Editor (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "A central spreadsheet-like control panel for managing variables.", slug: "alibre-design-term-9" },
  { id: "Configurations Manager (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "System for maintaining multiple physical variants in a single file.", slug: "alibre-design-term-10" },
  { id: "Catalog Features (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Library of reusable feature blocks and templates.", slug: "alibre-design-term-11" },
  { id: "3D PDF Publishing (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Standardized interactive PDF documents hosting 3D geometry.", slug: "alibre-design-term-12" },
  { id: "Thread Creator (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Parametric modeling of cosmetic or real helical threads.", slug: "alibre-design-term-13" },
  { id: "STEP/IGES Translation (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Standardized neutral formats for cross-platform CAD exchange.", slug: "alibre-design-term-14" },
  { id: "Design Booleans (Alibre Design)", type: "concept", group: 2, radius: 8, tags: ["alibre-design"], hint: "Solid-state geometric operations combining or intersecting volumes.", slug: "alibre-design-term-15" },
  { id: "Allplan", type: "product", group: 1, radius: 14, tags: ["allplan", "allplan"], hint: "Nemetschek's high-performance BIM platform focused on structural engineering and precast concrete.", slug: "allplan" },
  { id: "SmartParts (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Parametric, script-driven object definitions for structural BIM.", slug: "allplan-term-1" },
  { id: "3D Reinforcement Modeling (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Dynamic, physical modeling of reinforcing bars in concrete.", slug: "allplan-term-2" },
  { id: "Allplan Bridge (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Parametric modeler for complex civil bridge structures.", slug: "allplan-term-3" },
  { id: "BIM Model Topology (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Story-based spatial organization of architectural projects.", slug: "allplan-term-4" },
  { id: "Reinforcement Reports (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Automated schedules driven directly by 3D rebar models.", slug: "allplan-term-5" },
  { id: "PythonParts (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Next-generation parametric BIM elements driven by Python.", slug: "allplan-term-6" },
  { id: "IFC Exchange (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Standardized data exchange for open BIM collaboration.", slug: "allplan-term-7" },
  { id: "Quantity Takeoff (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Automated calculation of concrete, formwork, and finish areas.", slug: "allplan-term-8" },
  { id: "Terrain Modeling (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Site contour and surface generation from coordinate data.", slug: "allplan-term-9" },
  { id: "Multi-Layer Walls (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Complex wall definitions hosting structural, thermal, and finish layers.", slug: "allplan-term-10" },
  { id: "Element Plan Generator (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Automated drafting generator for precast concrete components.", slug: "allplan-term-11" },
  { id: "Clash Detection (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Spatial conflict checker for overlapping structural elements.", slug: "allplan-term-12" },
  { id: "Reference Planes (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Custom baseline sheets controlling geometry heights.", slug: "allplan-term-13" },
  { id: "CineRender Engine (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "High-end photo-realistic rendering engine integrated inside Allplan.", slug: "allplan-term-14" },
  { id: "Nemetschek Allplan Connect (Allplan)", type: "concept", group: 2, radius: 8, tags: ["allplan"], hint: "Cloud-based collaboration and asset portal.", slug: "allplan-term-15" },
  { id: "Altium Designer", type: "product", group: 1, radius: 14, tags: ["altium-designer", "altium-designer"], hint: "The premier unified electronic CAD (ECAD) environment for printed circuit board (PCB) design and engineering.", slug: "altium-designer" },
  { id: "Unified Schematic Capture (Altium)", type: "concept", group: 2, radius: 8, tags: ["altium-designer"], hint: "Logical component drawing and netlist configuration workspace.", slug: "altium-schematic-capture" },
  { id: "Interactive 3D PCB Engine (Altium)", type: "concept", group: 2, radius: 8, tags: ["altium-designer"], hint: "Integrated real-time STEP visualization of component clearance.", slug: "altium-3d-pcb" },
  { id: "ANSYS Fluent", type: "product", group: 1, radius: 14, tags: ["ansys-fluent", "ansys-fluent"], hint: "Industry-leading fluid dynamics simulation software known for its advanced physics modeling capabilities and accuracy.", slug: "ansys-fluent" },
  { id: "Unstructured CFD Meshing (Fluent)", type: "concept", group: 2, radius: 8, tags: ["ansys-fluent"], hint: "High-fidelity mesh generation for complex fluid volumes.", slug: "fluent-cfd-mesh" },
  { id: "SST k-omega Turbulence Model (Fluent)", type: "concept", group: 2, radius: 8, tags: ["ansys-fluent"], hint: "Standard industry two-equation shear stress transport model.", slug: "fluent-turbulence-model" },
  { id: "ANSYS Mechanical", type: "product", group: 1, radius: 14, tags: ["ansys-mechanical", "ansys-mechanical"], hint: "The premier structural mechanics simulation software utilizing finite element analysis (FEA) for linear, non-linear, and dynamic studies.", slug: "ansys-mechanical" },
  { id: "Hexahedral Structural Meshing (Mechanical)", type: "concept", group: 2, radius: 8, tags: ["ansys-mechanical"], hint: "Structured brick element meshing for high-accuracy stress fields.", slug: "mechanical-fea-mesh" },
  { id: "Frictional Nonlinear Contacts (Mechanical)", type: "concept", group: 2, radius: 8, tags: ["ansys-mechanical"], hint: "Iterative contact boundary conditions with friction.", slug: "mechanical-nonlinear-contact" },
  { id: "ARES Commander", type: "product", group: 1, radius: 14, tags: ["arescommander", "ares-commander"], hint: "Graebert's core DWG-native CAD engine, the foundation powering DraftSight, CorelCAD, and extensive cloud workflows.", slug: "ares-commander" },
  { id: "Trinity Concept (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Unified DWG editing across Desktop, Cloud, and Mobile.", slug: "ares-commander-term-1" },
  { id: "DWG Native Engine (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "High-performance drafting engine utilizing the DWG standard.", slug: "ares-commander-term-2" },
  { id: "ARES Kudo (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Cloud-based DWG editing and sharing platform.", slug: "ares-commander-term-3" },
  { id: "ARES Touch (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Mobile CAD application for tablets and smartphones.", slug: "ares-commander-term-4" },
  { id: "Custom Blocks (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Parametric drawing blocks offering dynamic geometry variations.", slug: "ares-commander-term-5" },
  { id: "AutoLISP Migration (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Familiar scripting interpreter for CAD task automation.", slug: "ares-commander-term-6" },
  { id: "C++ & .NET APIs (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Professional programming interfaces for enterprise CAD plugins.", slug: "ares-commander-term-7" },
  { id: "Sheet Set Manager (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Enterprise organization system for multi-drawing sheets.", slug: "ares-commander-term-8" },
  { id: "DGN Import & Underlay (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Bentley CAD file compatibility and exchange tools.", slug: "ares-commander-term-9" },
  { id: "GIS & Coordinate Integration (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Geospatial map integration inside DWG environments.", slug: "ares-commander-term-10" },
  { id: "PDF Import & Vectorization (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Vector path extraction from PDF drawings.", slug: "ares-commander-term-11" },
  { id: "Version History Cloud Sync (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Cloud-driven file tracking and recovery.", slug: "ares-commander-term-12" },
  { id: "Smart Voice Notes (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Audio voice annotations embedded inside drawings.", slug: "ares-commander-term-13" },
  { id: "Batch Plotting Utility (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "Automated publishing of drawing layouts.", slug: "ares-commander-term-14" },
  { id: "3D Solid Modeling (ARES Commander)", type: "concept", group: 2, radius: 8, tags: ["ares-commander"], hint: "ACIS-based 3D design and editing tools.", slug: "ares-commander-term-15" },
  { id: "AutoCAD XREF Tree", type: "skill", group: 2, radius: 9, tags: ["autocad", "collaboration"], hint: "Multi-discipline external-reference workflow.", slug: "" },
  { id: "AutoCAD Dynamic Block", type: "concept", group: 2, radius: 9, tags: ["autocad", "blocks"], hint: "Parametric reusable blocks with grips and lookups.", slug: "" },
  { id: "AutoCAD Sheet Set", type: "skill", group: 2, radius: 9, tags: ["autocad", "documentation"], hint: "Coordinated multi-sheet document management.", slug: "" },
  { id: "AutoCAD Plot Styles", type: "concept", group: 2, radius: 9, tags: ["autocad", "plotting"], hint: "CTB / STB plot-style configuration.", slug: "" },
  { id: "AutoCAD Data Extraction", type: "skill", group: 2, radius: 9, tags: ["autocad", "schedules"], hint: "Extract block attributes to tables/CSV.", slug: "" },
  { id: "AutoCAD Constraints", type: "concept", group: 2, radius: 9, tags: ["autocad", "parametric"], hint: "Geometric and dimensional constraints.", slug: "" },
  { id: "AVEVA Everything3D", type: "product", group: 1, radius: 14, tags: ["avevae3d", "aveva-e3d"], hint: "AVEVA's high-end process plant and marine 3D design platform, optimized for huge coordinated piping projects.", slug: "aveva-e3d" },
  { id: "Spec-Driven Piping Design (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Automated piping layout governed by standardized engineering specifications.", slug: "aveva-e3d-term-1" },
  { id: "Laser Data & Point Clouds (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Direct integration of 3D laser scans into plant layouts.", slug: "aveva-e3d-term-2" },
  { id: "Bubble View (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Interactive panoramic bubble views linked to 3D designs.", slug: "aveva-e3d-term-3" },
  { id: "Clash Detection & Clearance (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Automated plant-wide interference check engine.", slug: "aveva-e3d-term-4" },
  { id: "Draft Workbench (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Automated 2D orthographic drawing extraction from 3D models.", slug: "aveva-e3d-term-5" },
  { id: "AVEVA PML Scripting (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Proprietary programming language for E3D customization.", slug: "aveva-e3d-term-6" },
  { id: "Catalog & Spec Editor (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Database engine defining piping and structural components.", slug: "aveva-e3d-term-7" },
  { id: "Structural Steelwork (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Parametric modeling of steel frames and joints.", slug: "aveva-e3d-term-8" },
  { id: "Marine Design Module (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Specialized hull and marine outfitting modeling tools.", slug: "aveva-e3d-term-9" },
  { id: "Cable Design & Routing (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Automated electrical cable tray and conduit routing.", slug: "aveva-e3d-term-10" },
  { id: "HVAC Ducting Systems (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Intelligent modeling of ventilation and duct systems.", slug: "aveva-e3d-term-11" },
  { id: "Structural Joints & Plates (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Automated steel connection detailing.", slug: "aveva-e3d-term-12" },
  { id: "Multi-User Database Coordination (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Real-time database sharing for distributed design teams.", slug: "aveva-e3d-term-13" },
  { id: "Intelligent Isometric Generation (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Automated 3D piping isometric extraction.", slug: "aveva-e3d-term-14" },
  { id: "Equipment Modeling (AVEVA Everything3D)", type: "concept", group: 2, radius: 8, tags: ["aveva-e3d"], hint: "Parametric construction of plant primitives.", slug: "aveva-e3d-term-15" },
  { id: "Blender", type: "product", group: 1, radius: 14, tags: ["blender", "blender"], hint: "The premier free and open-source 3D creation suite, increasingly used in CAD visualization and Open BIM via BlenderBIM.", slug: "blender" },
  { id: "BlenderBIM Add-on (Blender)", type: "concept", group: 2, radius: 8, tags: ["blender"], hint: "Open-source plugin converting Blender into an IFC-native BIM authoring tool.", slug: "blender-blenderbim" },
  { id: "Cycles Render Engine (Blender)", type: "concept", group: 2, radius: 8, tags: ["blender"], hint: "Physically-based path-tracing render engine for photo-realistic CAD viz.", slug: "blender-cycles" },
  { id: "CATIA Workbenches", type: "concept", group: 2, radius: 10, tags: ["catia"], hint: "Modular workbench-based UI.", slug: "" },
  { id: "CATIA Sketcher", type: "concept", group: 2, radius: 8, tags: ["catia"], hint: "2D sketch environment.", slug: "" },
  { id: "GSD", type: "skill", group: 2, radius: 11, tags: ["catia", "surfacing"], hint: "Generative Shape Design surfacing.", slug: "" },
  { id: "Multi-Section Surface", type: "concept", group: 2, radius: 8, tags: ["catia", "surfacing"], hint: "Class-A lofted surface.", slug: "" },
  { id: "CATIA Product Structure", type: "concept", group: 2, radius: 9, tags: ["catia", "assembly"], hint: "Hierarchical assembly tree.", slug: "" },
  { id: "Contextual Design", type: "skill", group: 2, radius: 9, tags: ["catia", "assembly"], hint: "Top-down assembly with cross-part refs.", slug: "" },
  { id: "Publications", type: "concept", group: 2, radius: 9, tags: ["catia", "assembly"], hint: "Named exposed references for stability.", slug: "" },
  { id: "DMU Navigator", type: "product", group: 1, radius: 9, tags: ["catia", "review"], hint: "Lightweight assembly visualization.", slug: "" },
  { id: "CATIA Drafting", type: "skill", group: 2, radius: 8, tags: ["catia", "documentation"], hint: "2D drawings from 3D model.", slug: "" },
  { id: "Knowledgeware", type: "sdk", group: 2, radius: 9, tags: ["catia", "automation"], hint: "Parameters, rules, optimiser.", slug: "" },
  { id: "CAA RADE", type: "sdk", group: 2, radius: 8, tags: ["catia", "customization"], hint: "C++ deep customisation framework.", slug: "" },
  { id: "Civil 3D Alignment", type: "concept", group: 2, radius: 10, tags: ["civil3d", "geometry"], hint: "Horizontal centreline with stationing.", slug: "" },
  { id: "Civil 3D Profile", type: "concept", group: 2, radius: 9, tags: ["civil3d", "geometry"], hint: "Vertical alignment along an alignment.", slug: "" },
  { id: "Civil 3D Corridor", type: "concept", group: 2, radius: 11, tags: ["civil3d", "roads"], hint: "3D parametric road model.", slug: "" },
  { id: "Civil 3D Assembly", type: "concept", group: 2, radius: 9, tags: ["civil3d", "roads"], hint: "Cross-section template for corridors.", slug: "" },
  { id: "Civil 3D Subassembly", type: "concept", group: 2, radius: 8, tags: ["civil3d", "roads"], hint: "Parametric cross-section component.", slug: "" },
  { id: "Civil 3D Surface", type: "concept", group: 2, radius: 10, tags: ["civil3d", "terrain"], hint: "TIN or grid terrain model.", slug: "" },
  { id: "Civil 3D Grading", type: "skill", group: 2, radius: 9, tags: ["civil3d", "site"], hint: "Site grading with feature lines + criteria.", slug: "" },
  { id: "Civil 3D Pipe Network", type: "concept", group: 2, radius: 9, tags: ["civil3d", "stormwater"], hint: "Gravity sewer/storm network.", slug: "" },
  { id: "Civil 3D Pressure Network", type: "concept", group: 2, radius: 8, tags: ["civil3d", "water"], hint: "Pressurised water mains.", slug: "" },
  { id: "Civil 3D LandXML", type: "format", group: 2, radius: 8, tags: ["civil3d", "interop"], hint: "Vendor-neutral civil data exchange.", slug: "" },
  { id: "COMSOL Multiphysics", type: "product", group: 1, radius: 14, tags: ["comsol", "comsol"], hint: "A powerful cross-disciplinary FEA platform specializing in coupled multiphysics simulations and custom application building.", slug: "comsol" },
  { id: "Fully Coupled Multiphysics Solvers (COMSOL)", type: "concept", group: 2, radius: 8, tags: ["comsol"], hint: "Simultaneous solver matrices for interactive physical fields.", slug: "comsol-multiphysics-coupling" },
  { id: "COMSOL Application Builder (COMSOL)", type: "concept", group: 2, radius: 8, tags: ["comsol"], hint: "GUI builder that converts models into simple standalone apps.", slug: "comsol-app-builder" },
  { id: "Creo Features", type: "concept", group: 2, radius: 9, tags: ["creo", "parametric"], hint: "Ordered feature history of a Creo part.", slug: "" },
  { id: "Creo Skeleton", type: "skill", group: 2, radius: 10, tags: ["creo", "top-down"], hint: "Master reference part for top-down design.", slug: "" },
  { id: "Creo Top-Down Design", type: "skill", group: 2, radius: 10, tags: ["creo", "assembly"], hint: "Assembly-level design driving parts.", slug: "" },
  { id: "Creo Layouts", type: "concept", group: 2, radius: 7, tags: ["creo", "specs"], hint: "2D spec-capture file driving downstream models.", slug: "" },
  { id: "Creo Sheet Metal", type: "skill", group: 2, radius: 8, tags: ["creo", "fabrication"], hint: "Wall/bend/unbend modelling.", slug: "" },
  { id: "Creo Style", type: "skill", group: 2, radius: 9, tags: ["creo", "surfacing"], hint: "Class-A and freeform surfacing.", slug: "" },
  { id: "Creo MBD", type: "skill", group: 2, radius: 8, tags: ["creo", "drawings"], hint: "Model-Based Definition on 3D model.", slug: "" },
  { id: "Pro/TOOLKIT", type: "sdk", group: 2, radius: 8, tags: ["creo", "api"], hint: "C API for Creo customisation.", slug: "" },
  { id: "DWG/DXF Native Engine (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "High-performance 2D/3D drafting platform using the DWG format.", slug: "draftsight-term-1" },
  { id: "Custom Blocks (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Parametric 2D block elements offering dynamic variations.", slug: "draftsight-term-2" },
  { id: "LISP & API Integrations (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Comprehensive scripting engine for automation.", slug: "draftsight-term-3" },
  { id: "Sheet Set Manager (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Central organization console for multi-sheet project packages.", slug: "draftsight-term-4" },
  { id: "Image Tracer Vectorization (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Automated raster-to-vector conversion utility.", slug: "draftsight-term-5" },
  { id: "G-Code Generator (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Direct export of CNC programming toolpaths.", slug: "draftsight-term-6" },
  { id: "DGN Underlay & Import (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Bentley drawing standard integration.", slug: "draftsight-term-7" },
  { id: "Tool Palettes Customization (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Centralized catalog drag-and-drop drafting panels.", slug: "draftsight-term-8" },
  { id: "DWG Compare Utility (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Visual overlay comparing two drawing revisions.", slug: "draftsight-term-9" },
  { id: "Batch Print Utility (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Automated publishing of drawing layouts.", slug: "draftsight-term-10" },
  { id: "Power Trim Tool (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Intelligent drag-to-trim geometric boundary modifier.", slug: "draftsight-term-11" },
  { id: "PDF Form Fill (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Direct data mapping into PDF sheet documents.", slug: "draftsight-term-12" },
  { id: "Mechanical Toolbox (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Standardized hardware library and drafting symbols.", slug: "draftsight-term-13" },
  { id: "3D Mesh Modeling (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Lightweight 3D surface mesh generation tools.", slug: "draftsight-term-14" },
  { id: "Active Command Suggestions (DraftSight)", type: "concept", group: 2, radius: 8, tags: ["draftsight"], hint: "Context-aware input and auto-completion panel.", slug: "draftsight-term-15" },
  { id: "FreeCAD", type: "product", group: 1, radius: 14, tags: ["community", "foss", "mcad", "open-source"], hint: "The premier open-source parametric 3D modeler.", slug: "freecad" },
  { id: "Topological Naming", type: "concept", group: 2, radius: 10, tags: ["freecad", "modeling"], hint: "Geometric reference limitation on face renaming.", slug: "" },
  { id: "FreeCAD Python", type: "sdk", group: 2, radius: 9, tags: ["freecad", "api"], hint: "Python scripting and macro automation console.", slug: "" },
  { id: "CalculiX FEM", type: "product", group: 1, radius: 9, tags: ["freecad", "simulation"], hint: "Open-source solver for FEM workbench.", slug: "" },
  { id: "Fusion 360", type: "product", group: 1, radius: 14, tags: ["autodesk", "cloud", "mcad", "cam"], hint: "Cloud-native unified CAD/CAM/CAE.", slug: "fusion-360" },
  { id: "Fusion Components", type: "concept", group: 2, radius: 9, tags: ["fusion", "assembly"], hint: "Assembly containers with joints.", slug: "" },
  { id: "Fusion Sheet Metal", type: "skill", group: 2, radius: 8, tags: ["fusion", "fabrication"], hint: "Rule-driven flange-based modelling.", slug: "" },
  { id: "Fusion T-Spline", type: "concept", group: 2, radius: 8, tags: ["fusion", "surfacing"], hint: "Form workspace freeform modelling.", slug: "" },
  { id: "Fusion Tool Library", type: "concept", group: 2, radius: 8, tags: ["fusion", "cam"], hint: "Cataloged CNC tooling with feeds/speeds.", slug: "" },
  { id: "Fusion Post Processor", type: "concept", group: 2, radius: 8, tags: ["fusion", "cam"], hint: "Toolpath-to-G-code translator script.", slug: "" },
  { id: "Fusion Drawings", type: "skill", group: 2, radius: 8, tags: ["fusion", "documentation"], hint: "2D drawing environment.", slug: "" },
  { id: "Fusion Data Panel", type: "concept", group: 2, radius: 8, tags: ["fusion", "cloud"], hint: "Cloud project/folder/file UI.", slug: "" },
  { id: "GstarCAD Layers", type: "concept", group: 2, radius: 8, tags: ["gstarcad", "drafting"], hint: "Drawing partition system.", slug: "" },
  { id: "GstarCAD Object Snaps", type: "concept", group: 2, radius: 7, tags: ["gstarcad", "drafting"], hint: "Precision input snap system.", slug: "" },
  { id: "GstarCAD Model/Paper Space", type: "concept", group: 2, radius: 9, tags: ["gstarcad", "drafting"], hint: "Geometry and sheet composition.", slug: "" },
  { id: "GstarCAD Annotative", type: "concept", group: 2, radius: 8, tags: ["gstarcad", "drafting"], hint: "Scale-aware annotation system.", slug: "" },
  { id: "GstarCAD Dynamic Blocks", type: "concept", group: 2, radius: 9, tags: ["gstarcad", "blocks"], hint: "Parametric block definitions.", slug: "" },
  { id: "GstarCAD Attributes", type: "concept", group: 2, radius: 8, tags: ["gstarcad", "data"], hint: "Block-attached variable data.", slug: "" },
  { id: "GstarCAD Xrefs", type: "concept", group: 2, radius: 9, tags: ["gstarcad", "collaboration"], hint: "External DWG references.", slug: "" },
  { id: "GstarCAD Solid Editing", type: "skill", group: 2, radius: 9, tags: ["gstarcad", "3d"], hint: "3D solid Boolean and edit operations.", slug: "" },
  { id: "GstarCAD UCS", type: "concept", group: 2, radius: 8, tags: ["gstarcad", "3d"], hint: "User Coordinate System for 3D work.", slug: "" },
  { id: "GstarCAD MEP", type: "product", group: 1, radius: 11, tags: ["gstarcad", "mep", "vertical"], hint: "Mechanical/electrical/plumbing systems vertical.", slug: "gstarcad-mep" },
  { id: "GstarCAD Electrical", type: "product", group: 1, radius: 10, tags: ["gstarcad", "electrical", "vertical"], hint: "Electrical schematics + panel layouts.", slug: "gstarcad-electrical" },
  { id: "GstarCAD Mapping", type: "product", group: 1, radius: 10, tags: ["gstarcad", "survey", "vertical"], hint: "Survey and mapping vertical.", slug: "gstarcad-mapping" },
  { id: "GstarBIM", type: "product", group: 1, radius: 12, tags: ["gstarsoft", "bim", "flagship"], hint: "Gstarsoft's native BIM platform.", slug: "" },
  { id: "GstarCAD AutoLISP", type: "sdk", group: 2, radius: 9, tags: ["gstarcad", "api"], hint: "Full AutoLISP / Visual LISP support.", slug: "" },
  { id: "GstarCAD VBA", type: "sdk", group: 2, radius: 8, tags: ["gstarcad", "api"], hint: "Visual Basic for Applications inside GstarCAD.", slug: "" },
  { id: "GRX", type: "sdk", group: 2, radius: 9, tags: ["gstarcad", "api"], hint: "C++ runtime extension API (ObjectARX equivalent).", slug: "" },
  { id: "GstarCAD AI Tools", type: "skill", group: 2, radius: 10, tags: ["gstarcad", "ai"], hint: "AI-assisted drawing review and commands.", slug: "" },
  { id: "Inventor Project (.ipj)", type: "concept", group: 2, radius: 8, tags: ["inventor"], hint: "Workspace/library configuration file.", slug: "" },
  { id: "Inventor Features", type: "concept", group: 2, radius: 9, tags: ["inventor", "parametric"], hint: "Ordered feature history of a part.", slug: "" },
  { id: "Inventor Joints", type: "concept", group: 2, radius: 9, tags: ["inventor", "assembly"], hint: "Single-step assembly DOF relationships.", slug: "" },
  { id: "Frame Generator", type: "skill", group: 2, radius: 9, tags: ["inventor", "structural"], hint: "Structural frame design tool.", slug: "" },
  { id: "iParts / iAssemblies", type: "concept", group: 2, radius: 8, tags: ["inventor", "variants"], hint: "Factory-table-driven family variants.", slug: "" },
  { id: "Content Center", type: "product", group: 1, radius: 9, tags: ["inventor", "library"], hint: "Standard parts database.", slug: "" },
  { id: "Vault", type: "product", group: 1, radius: 10, tags: ["autodesk", "pdm"], hint: "Autodesk's PDM for Inventor/AutoCAD/Revit.", slug: "" },
  { id: "Inventor Presentations", type: "skill", group: 2, radius: 7, tags: ["inventor", "documentation"], hint: "Animated exploded-view files.", slug: "" },
  { id: "IronCAD", type: "product", group: 1, radius: 14, tags: ["ironcad", "ironcad"], hint: "A unique dual-engine (Parasolid + ACIS) MCAD that excels at drag-and-drop catalog modeling and absolute design freedom.", slug: "ironcad" },
  { id: "Dual-Kernel Engine (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Unified MCAD modeling utilizing both ACIS and Parasolid kernels.", slug: "ironcad-term-1" },
  { id: "Unified Assembly Environment (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Single-file workspace design hosting parts and assemblies without separate file structures.", slug: "ironcad-term-2" },
  { id: "Catalog Drag-and-Drop (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Fast modeling by dropping predefined shapes from sidebars onto active models.", slug: "ironcad-term-3" },
  { id: "TriBall Geometric Manipulator (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Unified 3D transform tool for positioning, rotating, and patterning geometry.", slug: "ironcad-term-4" },
  { id: "SmartAssembly Positioning (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Rule-based assembly connection points that automatically snap parts together.", slug: "ironcad-term-5" },
  { id: "Creative vs. Structured Design (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Dual-method design allowing history-free modeling alongside traditional parametric trees.", slug: "ironcad-term-6" },
  { id: "2D Detail Drafting Sheet (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Associative 2D drawings generated directly from unified 3D files.", slug: "ironcad-term-7" },
  { id: "IronCAD C++ API (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Deep software extension framework for enterprise CAD plugins.", slug: "ironcad-term-8" },
  { id: "KeyShot Rendering (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Real-time photo-realistic rendering integration.", slug: "ironcad-term-9" },
  { id: "Direct Face Modeling (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "History-free 3D solid face editing.", slug: "ironcad-term-10" },
  { id: "Standard Parts Catalog (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Library of international standard machinery hardware.", slug: "ironcad-term-11" },
  { id: "IronCAD Mechanical Tools (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Specialized utilities for mechanical machinery design.", slug: "ironcad-term-12" },
  { id: "B-Rep Booleans (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Solid-state geometric operations combining or intersecting volumes.", slug: "ironcad-term-13" },
  { id: "STEP/IGES Interoperability (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Neutral 3D format translator for CAD data exchange.", slug: "ironcad-term-14" },
  { id: "SmartAssembly Configurator (IronCAD)", type: "concept", group: 2, radius: 8, tags: ["ironcad"], hint: "Rule-based product customization engine.", slug: "ironcad-term-15" },
  { id: "DGN Design File Format (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "High-precision native file format for civil and infrastructure engineering.", slug: "microstation-term-1" },
  { id: "Cells & Shared Cells (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Reusable drawing symbols and parametric components.", slug: "microstation-term-2" },
  { id: "Levels & Level Manager (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Comprehensive drawing organization and standard systems.", slug: "microstation-term-3" },
  { id: "Reference Files (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Live, cross-discipline reference overlays for coordinate-perfect design.", slug: "microstation-term-4" },
  { id: "Item Types (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Dynamic metadata schemas attached to drawing elements.", slug: "microstation-term-5" },
  { id: "Parametric Modeling & Constraints (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Dimension-driven infrastructure design.", slug: "microstation-term-6" },
  { id: "AccuDraw & AccuSnap (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Dynamic coordinate input and precise snap helper.", slug: "microstation-term-7" },
  { id: "ProjectWise Collaboration (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Enterprise document management system integration.", slug: "microstation-term-8" },
  { id: "Mesh Modeling Tools (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Lightweight 3D surface modeling for complex terrains.", slug: "microstation-term-9" },
  { id: "Print Organizer (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Enterprise batch plotting and PDF publishing pipeline.", slug: "microstation-term-10" },
  { id: "Bentley View Compatibility (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Seamless file sharing and review tool.", slug: "microstation-term-11" },
  { id: "Geographic Coordinate Systems (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Geospatial projection mapping and map alignment.", slug: "microstation-term-12" },
  { id: "MDL C++ API (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Native-level C++ SDK for deep application customization.", slug: "microstation-term-13" },
  { id: "Point Cloud Visualisation (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "High-performance loading and styling of laser scan data.", slug: "microstation-term-14" },
  { id: "VBA Automation (MicroStation)", type: "concept", group: 2, radius: 8, tags: ["microstation"], hint: "Accessible programming engine for CAD task automation.", slug: "microstation-term-15" },
  { id: "Clash Detective Matrix (Navisworks)", type: "concept", group: 2, radius: 8, tags: ["navisworks"], hint: "Automated geometric overlap detection across federated multi-discipline models.", slug: "navisworks-clash-detective" },
  { id: "TimeLiner 4D Simulator (Navisworks)", type: "concept", group: 2, radius: 8, tags: ["navisworks"], hint: "Linking 3D models to construction schedules for visual sequencing.", slug: "navisworks-timeliner" },
  { id: "Onshape", type: "product", group: 1, radius: 14, tags: ["onshape", "onshape"], hint: "The premier cloud-native parametric 3D CAD platform with built-in version control and team sharing.", slug: "onshape" },
  { id: "Unified Part Studios (Onshape)", type: "concept", group: 2, radius: 8, tags: ["onshape"], hint: "Multi-part parametric design space driven by shared sketch features.", slug: "onshape-part-studio" },
  { id: "Cloud Document Versioning (Onshape)", type: "concept", group: 2, radius: 8, tags: ["onshape"], hint: "Git-style branching and merging for 3D CAD models.", slug: "onshape-version-control" },
  { id: "OpenFOAM", type: "product", group: 1, radius: 14, tags: ["openfoam", "openfoam"], hint: "The premier free and open-source Computational Fluid Dynamics (CFD) toolbox used in science and engineering globally.", slug: "openfoam" },
  { id: "blockMesh Mesh Generator (OpenFOAM)", type: "concept", group: 2, radius: 8, tags: ["openfoam"], hint: "Text-based dictionary tool for structured hexahedral meshing.", slug: "openfoam-blockmesh" },
  { id: "controlDict Configuration Dictionary (OpenFOAM)", type: "concept", group: 2, radius: 8, tags: ["openfoam"], hint: "Core runtime directory parameter control file.", slug: "openfoam-controldict" },
  { id: "OpenRoads Designer", type: "product", group: 1, radius: 14, tags: ["openroads", "openroads"], hint: "Bentley's premium BIM civil infrastructure design environment for road, rail, corridor, drainage, and utility networks.", slug: "openroads" },
  { id: "Parametric Corridor Modeler (OpenRoads)", type: "concept", group: 2, radius: 8, tags: ["openroads"], hint: "3D dynamic roadway extrusion based on alignments and templates.", slug: "openroads-corridor" },
  { id: "Dynamic Terrain Models (OpenRoads)", type: "concept", group: 2, radius: 8, tags: ["openroads"], hint: "High-performance surface modeler for survey data.", slug: "openroads-terrain" },
  { id: "Revit Worksets", type: "concept", group: 2, radius: 9, tags: ["revit", "collaboration"], hint: "Worksharing ownership partitions.", slug: "" },
  { id: "Revit Linked Models", type: "skill", group: 2, radius: 9, tags: ["revit", "coordination"], hint: "Multi-discipline RVT linking.", slug: "" },
  { id: "Revit Shared Coordinates", type: "concept", group: 2, radius: 8, tags: ["revit", "coordination"], hint: "Tie internal origin to real-world site.", slug: "" },
  { id: "Revit View Template", type: "concept", group: 2, radius: 8, tags: ["revit", "documentation"], hint: "Saved view-graphic configurations.", slug: "" },
  { id: "Dynamo", type: "sdk", group: 2, radius: 9, tags: ["revit", "automation"], hint: "Visual programming bundled with Revit.", slug: "" },
  { id: "Revit IFC Export", type: "format", group: 2, radius: 8, tags: ["revit", "ifc", "interop"], hint: "Open-standard model exchange.", slug: "" },
  { id: "Revit Shared Parameters", type: "concept", group: 2, radius: 8, tags: ["revit", "data"], hint: "External GUID-keyed parameter store.", slug: "" },
  { id: "Rhinoceros", type: "product", group: 1, radius: 14, tags: ["rhinoceros", "rhinoceros"], hint: "The ultimate 3D NURBS-based geometric modeler, famed for complex freeform curves and Grasshopper algorithmic automation.", slug: "rhinoceros" },
  { id: "NURBS Geometry (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Mathematical representation of highly precise smooth curves and freeform surfaces.", slug: "rhinoceros-term-1" },
  { id: "Grasshopper (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Integrated algorithmic and visual programming modeling environment.", slug: "rhinoceros-term-2" },
  { id: "SubD Modeling (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Subdivision surface modeling for organic and freeform structures.", slug: "rhinoceros-term-3" },
  { id: "Mesh vs. NURBS (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Understanding different geometric representations and data types.", slug: "rhinoceros-term-4" },
  { id: "Gumball Manipulator (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Interactive graphical gizmo for fast translation, scaling, and rotation.", slug: "rhinoceros-term-5" },
  { id: "Command Line & Aliases (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Keyboard-driven efficiency system for instant command execution.", slug: "rhinoceros-term-6" },
  { id: "Layer States (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Saved layer visibility and property configurations.", slug: "rhinoceros-term-7" },
  { id: "Make2D (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Automated generation of flat 2D drawings from 3D models.", slug: "rhinoceros-term-8" },
  { id: "Named Views & Viewports (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Saved camera alignments and viewport configuration schemes.", slug: "rhinoceros-term-9" },
  { id: "QuadMesh Retopology (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Automated reconstruction of messy geometry into clean quad meshes.", slug: "rhinoceros-term-10" },
  { id: "RhinoCommon API (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Comprehensive .NET SDK for custom tool and plugin development.", slug: "rhinoceros-term-11" },
  { id: "Worksession (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Multi-file coordination workspace for large-scale design teams.", slug: "rhinoceros-term-12" },
  { id: "Point Clouds & Reverse Engineering (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Laser scan integration and direct curve fitting.", slug: "rhinoceros-term-13" },
  { id: "Rendering & Display Modes (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Real-time viewport shading styles and visual settings.", slug: "rhinoceros-term-14" },
  { id: "File Interoperability (Rhinoceros)", type: "concept", group: 2, radius: 8, tags: ["rhinoceros"], hint: "Broad support for neutral and native CAD exchange formats.", slug: "rhinoceros-term-15" },
  { id: "Siemens NX", type: "product", group: 1, radius: 14, tags: ["siemens", "mcad", "cam", "high-end"], hint: "Siemens' high-end CAD/CAM/CAE platform.", slug: "siemens-nx" },
  { id: "Synchronous Technology", type: "concept", group: 2, radius: 11, tags: ["nx", "hybrid"], hint: "Direct + parametric hybrid editing.", slug: "" },
  { id: "NX Features", type: "concept", group: 2, radius: 9, tags: ["nx", "parametric"], hint: "Ordered parametric feature history.", slug: "" },
  { id: "Master Model", type: "concept", group: 2, radius: 9, tags: ["nx", "documents"], hint: "Source 3D part referenced by drawings/assemblies/CAM.", slug: "" },
  { id: "WAVE", type: "skill", group: 2, radius: 10, tags: ["nx", "top-down"], hint: "Inter-part linking for top-down design.", slug: "" },
  { id: "NX Assembly Constraints", type: "concept", group: 2, radius: 8, tags: ["nx", "assembly"], hint: "Geometric positioning of components.", slug: "" },
  { id: "NX PMI", type: "skill", group: 2, radius: 8, tags: ["nx", "drawings"], hint: "Product Manufacturing Information on 3D.", slug: "" },
  { id: "NX Sheet Metal", type: "skill", group: 2, radius: 8, tags: ["nx", "fabrication"], hint: "Tab/flange-based sheet metal.", slug: "" },
  { id: "NX Surfacing", type: "skill", group: 2, radius: 9, tags: ["nx", "surfacing"], hint: "Free-form and class-A surfacing.", slug: "" },
  { id: "NX Open", type: "sdk", group: 2, radius: 9, tags: ["nx", "api"], hint: "Multi-language API (Python/.NET/C++).", slug: "" },
  { id: "SketchUp", type: "product", group: 1, radius: 14, tags: ["sketchup", "sketchup"], hint: "Trimble's extremely intuitive 3D conceptual design and presentation modeler, highly popular in architecture.", slug: "sketchup" },
  { id: "Push/Pull Tool (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Interactive mouse-driven extrusion and pocketing of planar faces.", slug: "sketchup-term-1" },
  { id: "Components vs. Groups (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Managing distinct geometric assemblies and parametric links.", slug: "sketchup-term-2" },
  { id: "3D Warehouse (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Cloud-integrated portal hosting millions of pre-built CAD assets.", slug: "sketchup-term-3" },
  { id: "LayOut (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Associative 2D presentation and construction documentation toolset.", slug: "sketchup-term-4" },
  { id: "Ruby API & Extensions (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Programming engine driving custom scripts and plugins.", slug: "sketchup-term-5" },
  { id: "Tags & Outliner (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Hierarchical spatial organization and visibility control system.", slug: "sketchup-term-6" },
  { id: "Section Planes & Fills (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Dynamic architectural clipping and cut overlays.", slug: "sketchup-term-7" },
  { id: "Styles & Visual Presentation (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Viewport rendering styles and artistic hand-drawn sketches.", slug: "sketchup-term-8" },
  { id: "Dynamic Components (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Parametric component families hosting customized formula attributes.", slug: "sketchup-term-9" },
  { id: "Shadows & Geo-location (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Precise solar study projections and map mapping.", slug: "sketchup-term-10" },
  { id: "Tape Measure Tool (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Interactive coordinate measurement and global model scaling.", slug: "sketchup-term-11" },
  { id: "Sandbox Tools (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Terrain modeling and earthwork generation tools.", slug: "sketchup-term-12" },
  { id: "Intersect with Model (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Boolean-like edge generation at intersecting faces.", slug: "sketchup-term-13" },
  { id: "Solid Tools (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "ACIS-like boolean operations for clean solids.", slug: "sketchup-term-14" },
  { id: "Extension Manager (SketchUp)", type: "concept", group: 2, radius: 8, tags: ["sketchup"], hint: "Central dashboard for managing and updating CAD add-ons.", slug: "sketchup-term-15" },
  { id: "Solibri Office", type: "product", group: 1, radius: 14, tags: ["solibri", "solibri"], hint: "The industry-standard quality assurance software for BIM, offering advanced model checking and code compliance auditing.", slug: "solibri" },
  { id: "Solibri Rule Manager (Solibri)", type: "concept", group: 2, radius: 8, tags: ["solibri"], hint: "Boolean-based logical constraint checker for building databases.", slug: "solibri-rule-manager" },
  { id: "BCF Issue Management (Solibri)", type: "concept", group: 2, radius: 8, tags: ["solibri"], hint: "Standard open-format coordination sync protocol.", slug: "solibri-bcf-coordination" },
  { id: "Synchronous Technology (Solid Edge)", type: "concept", group: 2, radius: 8, tags: ["solid-edge"], hint: "Hybrid modeling combining history-tree parametric and history-free direct editing.", slug: "solidedge-synchronous-tech" },
  { id: "Synchronous Steering Wheel (Solid Edge)", type: "concept", group: 2, radius: 8, tags: ["solid-edge"], hint: "3D geometric manipulator for rapid direct editing.", slug: "solidedge-steering-wheel" },
  { id: "SOLIDWORKS Mates", type: "concept", group: 2, radius: 10, tags: ["solidworks", "assembly"], hint: "Geometric constraints between assembly components.", slug: "" },
  { id: "SOLIDWORKS Design Tables", type: "concept", group: 2, radius: 8, tags: ["solidworks", "automation"], hint: "Excel-driven configuration tables.", slug: "" },
  { id: "SOLIDWORKS Sheet Metal", type: "skill", group: 2, radius: 9, tags: ["solidworks", "fabrication"], hint: "Flange-driven fabricated sheet metal.", slug: "" },
  { id: "SOLIDWORKS Weldments", type: "skill", group: 2, radius: 9, tags: ["solidworks", "fabrication"], hint: "Multi-body structural welded frames.", slug: "" },
  { id: "SOLIDWORKS Feature Tree", type: "concept", group: 2, radius: 10, tags: ["solidworks", "parametric"], hint: "Ordered feature history of a part.", slug: "" },
  { id: "SOLIDWORKS MBD", type: "skill", group: 2, radius: 8, tags: ["solidworks", "drawings", "gdt"], hint: "Model-based definition replacing 2D drawings.", slug: "" },
  { id: "SOLIDWORKS Simulation", type: "product", group: 1, radius: 9, tags: ["solidworks", "fea"], hint: "Integrated FEA for SOLIDWORKS models.", slug: "simulation-solidworks" },
  { id: "SOLIDWORKS Toolbox", type: "concept", group: 2, radius: 8, tags: ["solidworks", "library"], hint: "Standard fasteners and hardware library.", slug: "toolbox-solidworks" },
  { id: "ANSYS SpaceClaim", type: "product", group: 1, radius: 14, tags: ["spaceclaim", "spaceclaim"], hint: "A high-speed direct 3D modeler built to prepare, clean, and simplify geometry for finite element analysis.", slug: "spaceclaim" },
  { id: "Direct Modeling (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "History-free geometry editing through direct face manipulation.", slug: "spaceclaim-term-1" },
  { id: "Pull Tool (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Unified mouse handle for extrusion, revolving, sweeping, and drafting.", slug: "spaceclaim-term-2" },
  { id: "Move Tool (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Multi-functional geometric handle for precise 3D translation and rotation.", slug: "spaceclaim-term-3" },
  { id: "Fill Tool (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Intelligent geometric healing and feature removal tool.", slug: "spaceclaim-term-4" },
  { id: "Sheet Metal Unfolding (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Watertight flat pattern extraction from 3D sheet metal parts.", slug: "spaceclaim-term-5" },
  { id: "Prep for Simulation (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Automated tools to extract beams, shells, and fluid volumes.", slug: "spaceclaim-term-6" },
  { id: "Reverse Engineering (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Direct fitting of curves and surfaces onto imported STL files.", slug: "spaceclaim-term-7" },
  { id: "Facet Tools (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Direct editing and repair of STL and mesh files.", slug: "spaceclaim-term-8" },
  { id: "Assembly Structure (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Flexible component management in a unified workspace.", slug: "spaceclaim-term-9" },
  { id: "IronPython Scripting (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Integrated Python automation for CAD workflows.", slug: "spaceclaim-term-10" },
  { id: "Shared Topology (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Automated mesh node alignment for finite element solvers.", slug: "spaceclaim-term-11" },
  { id: "Dimensional Control (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Direct, history-free dimensions that act as parameters.", slug: "spaceclaim-term-12" },
  { id: "Clean Up & Repair (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Automated tool for finding and fixing geometry errors.", slug: "spaceclaim-term-13" },
  { id: "STEP/IGES Import (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "Watertight neutral 3D CAD data translation.", slug: "spaceclaim-term-14" },
  { id: "Measurement & Mass (ANSYS SpaceClaim)", type: "concept", group: 2, radius: 8, tags: ["spaceclaim"], hint: "High-precision physical properties and geometric analysis.", slug: "spaceclaim-term-15" },
  { id: "STAAD Analytical Frame Model (STAAD.Pro)", type: "concept", group: 2, radius: 8, tags: ["staad-pro"], hint: "Node-and-beam center-line finite element structural representation.", slug: "staad-analytical-model" },
  { id: "Automated Steel Code Checker (STAAD.Pro)", type: "concept", group: 2, radius: 8, tags: ["staad-pro"], hint: "Built-in optimization engine for structural steel profiles.", slug: "staad-code-checking" },
  { id: "Siemens Teamcenter", type: "product", group: 1, radius: 14, tags: ["teamcenter", "teamcenter"], hint: "The world's most widely adopted product lifecycle management (PLM) system, connecting teams and CAD data across the enterprise.", slug: "teamcenter" },
  { id: "Active Workspace Interface (Teamcenter)", type: "concept", group: 2, radius: 8, tags: ["teamcenter"], hint: "Modern web UI for enterprise-wide CAD and metadata search.", slug: "teamcenter-active-workspace" },
  { id: "JT Open Data Format (Teamcenter)", type: "concept", group: 2, radius: 8, tags: ["teamcenter"], hint: "ISO standard lightweight 3D CAD visualization format.", slug: "teamcenter-jt-format" },
  { id: "Tekla Structures", type: "product", group: 1, radius: 14, tags: ["teklastructures", "tekla-structures"], hint: "Trimble's premier structural BIM authoring tool, delivering detailed LOD 500 models for steel and concrete.", slug: "tekla-structures" },
  { id: "Steel Detailing (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "High-precision 3D structural steel modeling and connection design.", slug: "tekla-structures-term-1" },
  { id: "Cast-in-Place Concrete (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Advanced 3D modeling of cast-in-place concrete structures.", slug: "tekla-structures-term-2" },
  { id: "Rebar Detailing (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Interactive, physical 3D modeling of reinforcing steel.", slug: "tekla-structures-term-3" },
  { id: "Tekla Model Sharing (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Cloud-based collaboration for distributed structural teams.", slug: "tekla-structures-term-4" },
  { id: "Custom Components (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Parametric, reusable structural detail templates.", slug: "tekla-structures-term-5" },
  { id: "Drawing List (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Central organization dashboard for structural sheet packages.", slug: "tekla-structures-term-6" },
  { id: "Assembly Drawings (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Watertight shop drawings for structural steel fabricators.", slug: "tekla-structures-term-7" },
  { id: "Clash Check (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Automated plant-wide structural interference checking.", slug: "tekla-structures-term-8" },
  { id: "Organizer (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Dynamic quantity takeoff and material tracking engine.", slug: "tekla-structures-term-9" },
  { id: "Open API (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Comprehensive C# and .NET SDK for custom tool development.", slug: "tekla-structures-term-10" },
  { id: "IFC Import/Export (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Open BIM coordination and exchange tools.", slug: "tekla-structures-term-11" },
  { id: "Weld Marks & Specs (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Standardized 3D welding definition and notation tools.", slug: "tekla-structures-term-12" },
  { id: "Phase Manager (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Construction sequencing and project phasing system.", slug: "tekla-structures-term-13" },
  { id: "User-Defined Attributes (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Custom metadata fields attached to structural elements.", slug: "tekla-structures-term-14" },
  { id: "NC/DSTV Export (Tekla Structures)", type: "concept", group: 2, radius: 8, tags: ["tekla-structures"], hint: "Direct CNC file generation for steel cutting machines.", slug: "tekla-structures-term-15" },
  { id: "Vectorworks", type: "product", group: 1, radius: 14, tags: ["vectorworks", "vectorworks"], hint: "A versatile BIM and CAD platform tailored for architects, landscape architects, and entertainment designers.", slug: "vectorworks" },
  { id: "Marionette (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Visual scripting and algorithmic modeling interface.", slug: "vectorworks-term-1" },
  { id: "Design vs. Sheet Layers (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Modular environment separation for geometry creation and drafting.", slug: "vectorworks-term-2" },
  { id: "Resource Manager (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Centralized catalog browser for managing CAD and BIM assets.", slug: "vectorworks-term-3" },
  { id: "Hybrid Symbols (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "2D/3D dual-state CAD blocks and dynamic components.", slug: "vectorworks-term-4" },
  { id: "Landmark Site Model (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Advanced GIS and digital terrain modeling toolset.", slug: "vectorworks-term-5" },
  { id: "Spotlight Lighting (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Specialized lighting and entertainment event design suite.", slug: "vectorworks-term-6" },
  { id: "Classes vs. Layers (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Dual-attribute organization separating object types and spatial locations.", slug: "vectorworks-term-7" },
  { id: "Data Tag Tool (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Dynamic, model-linked annotation and schedule system.", slug: "vectorworks-term-8" },
  { id: "Wall Join Tool (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Automated clean-up of wall component intersections.", slug: "vectorworks-term-9" },
  { id: "Plant Database (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Comprehensive botanical database linked to GIS modeling tools.", slug: "vectorworks-term-10" },
  { id: "ConnectCAD (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Signal flow and cable routing design vertical.", slug: "vectorworks-term-11" },
  { id: "Braceworks (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Structural rigging and load analysis engine.", slug: "vectorworks-term-12" },
  { id: "Sheet Border & Title Block (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Associative title block and drawing boundary manager.", slug: "vectorworks-term-13" },
  { id: "IFC & BIM Collaboration (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Open BIM coordinate and data exchange tools.", slug: "vectorworks-term-14" },
  { id: "Marionette Nodes (Vectorworks)", type: "concept", group: 2, radius: 8, tags: ["vectorworks"], hint: "Modular programming blocks for visual scripting.", slug: "vectorworks-term-15" },
  { id: "ZWCAD", type: "product", group: 1, radius: 14, tags: ["zwsoft", "dwg", "drafting", "high-speed"], hint: "ZWSOFT's high-performance DWG-native 2D/3D CAD platform.", slug: "zwcad" },
  { id: "ZRX SDK", type: "sdk", group: 2, radius: 9, tags: ["zwcad", "api"], hint: "ObjectARX-compatible C++ developer kit.", slug: "" },
  { id: "Smart Voice", type: "skill", group: 2, radius: 8, tags: ["zwcad", "ui"], hint: "Embeds audio annotations directly inside DWG.", slug: "" },
  { id: "Multi-Core Rendering", type: "concept", group: 2, radius: 9, tags: ["zwcad", "performance"], hint: "Multi-threaded CPU canvas acceleration.", slug: "" },
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
  ["3ds Max", "Autodesk"],
  ["Subdivision Polygonal Modeling (3ds Max)", "3ds Max"],
  ["Arnold Path-Tracing Renderer (3ds Max)", "3ds Max"],
  ["Abaqus FEA", "Dassault"],
  ["Abaqus Explicit Dynamics (Abaqus)", "Abaqus FEA"],
  ["User Material Subroutine UMAT (Abaqus)", "Abaqus FEA"],
  ["Alibre Design", "Alibre"],
  ["Parametric Dimension Driver (Alibre Design)", "Alibre Design"],
  ["Geometric Constraints (Alibre Design)", "Alibre Design"],
  ["Feature History Tree (Alibre Design)", "Alibre Design"],
  ["Assembly Mates (Alibre Design)", "Alibre Design"],
  ["B-Rep Solid Engine (Alibre Design)", "Alibre Design"],
  ["Sheet Metal Flanges (Alibre Design)", "Alibre Design"],
  ["2D Drafting Sheets (Alibre Design)", "Alibre Design"],
  ["Alibre Script (Alibre Design)", "Alibre Design"],
  ["Equations Editor (Alibre Design)", "Alibre Design"],
  ["Configurations Manager (Alibre Design)", "Alibre Design"],
  ["Catalog Features (Alibre Design)", "Alibre Design"],
  ["3D PDF Publishing (Alibre Design)", "Alibre Design"],
  ["Thread Creator (Alibre Design)", "Alibre Design"],
  ["STEP/IGES Translation (Alibre Design)", "Alibre Design"],
  ["Design Booleans (Alibre Design)", "Alibre Design"],
  ["Allplan", "Allplan (Nemetschek)"],
  ["SmartParts (Allplan)", "Allplan"],
  ["3D Reinforcement Modeling (Allplan)", "Allplan"],
  ["Allplan Bridge (Allplan)", "Allplan"],
  ["BIM Model Topology (Allplan)", "Allplan"],
  ["Reinforcement Reports (Allplan)", "Allplan"],
  ["PythonParts (Allplan)", "Allplan"],
  ["IFC Exchange (Allplan)", "Allplan"],
  ["Quantity Takeoff (Allplan)", "Allplan"],
  ["Terrain Modeling (Allplan)", "Allplan"],
  ["Multi-Layer Walls (Allplan)", "Allplan"],
  ["Element Plan Generator (Allplan)", "Allplan"],
  ["Clash Detection (Allplan)", "Allplan"],
  ["Reference Planes (Allplan)", "Allplan"],
  ["CineRender Engine (Allplan)", "Allplan"],
  ["Nemetschek Allplan Connect (Allplan)", "Allplan"],
  ["Altium Designer", "Altium"],
  ["Unified Schematic Capture (Altium)", "Altium Designer"],
  ["Interactive 3D PCB Engine (Altium)", "Altium Designer"],
  ["ANSYS Fluent", "ANSYS"],
  ["Unstructured CFD Meshing (Fluent)", "ANSYS Fluent"],
  ["SST k-omega Turbulence Model (Fluent)", "ANSYS Fluent"],
  ["ANSYS Mechanical", "ANSYS"],
  ["Hexahedral Structural Meshing (Mechanical)", "ANSYS Mechanical"],
  ["Frictional Nonlinear Contacts (Mechanical)", "ANSYS Mechanical"],
  ["ARES Commander", "Graebert"],
  ["Trinity Concept (ARES Commander)", "ARES Commander"],
  ["DWG Native Engine (ARES Commander)", "ARES Commander"],
  ["ARES Kudo (ARES Commander)", "ARES Commander"],
  ["ARES Touch (ARES Commander)", "ARES Commander"],
  ["Custom Blocks (ARES Commander)", "ARES Commander"],
  ["AutoLISP Migration (ARES Commander)", "ARES Commander"],
  ["C++ & .NET APIs (ARES Commander)", "ARES Commander"],
  ["Sheet Set Manager (ARES Commander)", "ARES Commander"],
  ["DGN Import & Underlay (ARES Commander)", "ARES Commander"],
  ["GIS & Coordinate Integration (ARES Commander)", "ARES Commander"],
  ["PDF Import & Vectorization (ARES Commander)", "ARES Commander"],
  ["Version History Cloud Sync (ARES Commander)", "ARES Commander"],
  ["Smart Voice Notes (ARES Commander)", "ARES Commander"],
  ["Batch Plotting Utility (ARES Commander)", "ARES Commander"],
  ["3D Solid Modeling (ARES Commander)", "ARES Commander"],
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
  ["Spec-Driven Piping Design (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Laser Data & Point Clouds (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Bubble View (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Clash Detection & Clearance (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Draft Workbench (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["AVEVA PML Scripting (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Catalog & Spec Editor (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Structural Steelwork (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Marine Design Module (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Cable Design & Routing (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["HVAC Ducting Systems (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Structural Joints & Plates (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Multi-User Database Coordination (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Intelligent Isometric Generation (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Equipment Modeling (AVEVA Everything3D)", "AVEVA Everything3D"],
  ["Blender", "Community (FOSS)"],
  ["BlenderBIM Add-on (Blender)", "Blender"],
  ["Cycles Render Engine (Blender)", "Blender"],
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
  ["COMSOL Multiphysics", "COMSOL"],
  ["Fully Coupled Multiphysics Solvers (COMSOL)", "COMSOL Multiphysics"],
  ["COMSOL Application Builder (COMSOL)", "COMSOL Multiphysics"],
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
  ["DWG/DXF Native Engine (DraftSight)", "DraftSight"],
  ["Custom Blocks (DraftSight)", "DraftSight"],
  ["LISP & API Integrations (DraftSight)", "DraftSight"],
  ["Sheet Set Manager (DraftSight)", "DraftSight"],
  ["Image Tracer Vectorization (DraftSight)", "DraftSight"],
  ["G-Code Generator (DraftSight)", "DraftSight"],
  ["DGN Underlay & Import (DraftSight)", "DraftSight"],
  ["Tool Palettes Customization (DraftSight)", "DraftSight"],
  ["DWG Compare Utility (DraftSight)", "DraftSight"],
  ["Batch Print Utility (DraftSight)", "DraftSight"],
  ["Power Trim Tool (DraftSight)", "DraftSight"],
  ["PDF Form Fill (DraftSight)", "DraftSight"],
  ["Mechanical Toolbox (DraftSight)", "DraftSight"],
  ["3D Mesh Modeling (DraftSight)", "DraftSight"],
  ["Active Command Suggestions (DraftSight)", "DraftSight"],
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
  ["Dual-Kernel Engine (IronCAD)", "IronCAD"],
  ["Unified Assembly Environment (IronCAD)", "IronCAD"],
  ["Catalog Drag-and-Drop (IronCAD)", "IronCAD"],
  ["TriBall Geometric Manipulator (IronCAD)", "IronCAD"],
  ["SmartAssembly Positioning (IronCAD)", "IronCAD"],
  ["Creative vs. Structured Design (IronCAD)", "IronCAD"],
  ["2D Detail Drafting Sheet (IronCAD)", "IronCAD"],
  ["IronCAD C++ API (IronCAD)", "IronCAD"],
  ["KeyShot Rendering (IronCAD)", "IronCAD"],
  ["Direct Face Modeling (IronCAD)", "IronCAD"],
  ["Standard Parts Catalog (IronCAD)", "IronCAD"],
  ["IronCAD Mechanical Tools (IronCAD)", "IronCAD"],
  ["B-Rep Booleans (IronCAD)", "IronCAD"],
  ["STEP/IGES Interoperability (IronCAD)", "IronCAD"],
  ["SmartAssembly Configurator (IronCAD)", "IronCAD"],
  ["MicroStation", "Bentley"],
  ["DGN Design File Format (MicroStation)", "MicroStation"],
  ["Cells & Shared Cells (MicroStation)", "MicroStation"],
  ["Levels & Level Manager (MicroStation)", "MicroStation"],
  ["Reference Files (MicroStation)", "MicroStation"],
  ["Item Types (MicroStation)", "MicroStation"],
  ["Parametric Modeling & Constraints (MicroStation)", "MicroStation"],
  ["AccuDraw & AccuSnap (MicroStation)", "MicroStation"],
  ["ProjectWise Collaboration (MicroStation)", "MicroStation"],
  ["Mesh Modeling Tools (MicroStation)", "MicroStation"],
  ["Print Organizer (MicroStation)", "MicroStation"],
  ["Bentley View Compatibility (MicroStation)", "MicroStation"],
  ["Geographic Coordinate Systems (MicroStation)", "MicroStation"],
  ["MDL C++ API (MicroStation)", "MicroStation"],
  ["Point Cloud Visualisation (MicroStation)", "MicroStation"],
  ["VBA Automation (MicroStation)", "MicroStation"],
  ["Navisworks", "Autodesk"],
  ["Clash Detective Matrix (Navisworks)", "Navisworks"],
  ["TimeLiner 4D Simulator (Navisworks)", "Navisworks"],
  ["Onshape", "PTC"],
  ["Unified Part Studios (Onshape)", "Onshape"],
  ["Cloud Document Versioning (Onshape)", "Onshape"],
  ["OpenFOAM", "OpenFOAM Foundation"],
  ["blockMesh Mesh Generator (OpenFOAM)", "OpenFOAM"],
  ["controlDict Configuration Dictionary (OpenFOAM)", "OpenFOAM"],
  ["OpenRoads Designer", "Bentley"],
  ["Parametric Corridor Modeler (OpenRoads)", "OpenRoads Designer"],
  ["Dynamic Terrain Models (OpenRoads)", "OpenRoads Designer"],
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
  ["NURBS Geometry (Rhinoceros)", "Rhinoceros"],
  ["Grasshopper (Rhinoceros)", "Rhinoceros"],
  ["SubD Modeling (Rhinoceros)", "Rhinoceros"],
  ["Mesh vs. NURBS (Rhinoceros)", "Rhinoceros"],
  ["Gumball Manipulator (Rhinoceros)", "Rhinoceros"],
  ["Command Line & Aliases (Rhinoceros)", "Rhinoceros"],
  ["Layer States (Rhinoceros)", "Rhinoceros"],
  ["Make2D (Rhinoceros)", "Rhinoceros"],
  ["Named Views & Viewports (Rhinoceros)", "Rhinoceros"],
  ["QuadMesh Retopology (Rhinoceros)", "Rhinoceros"],
  ["RhinoCommon API (Rhinoceros)", "Rhinoceros"],
  ["Worksession (Rhinoceros)", "Rhinoceros"],
  ["Point Clouds & Reverse Engineering (Rhinoceros)", "Rhinoceros"],
  ["Rendering & Display Modes (Rhinoceros)", "Rhinoceros"],
  ["File Interoperability (Rhinoceros)", "Rhinoceros"],
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
  ["Push/Pull Tool (SketchUp)", "SketchUp"],
  ["Components vs. Groups (SketchUp)", "SketchUp"],
  ["3D Warehouse (SketchUp)", "SketchUp"],
  ["LayOut (SketchUp)", "SketchUp"],
  ["Ruby API & Extensions (SketchUp)", "SketchUp"],
  ["Tags & Outliner (SketchUp)", "SketchUp"],
  ["Section Planes & Fills (SketchUp)", "SketchUp"],
  ["Styles & Visual Presentation (SketchUp)", "SketchUp"],
  ["Dynamic Components (SketchUp)", "SketchUp"],
  ["Shadows & Geo-location (SketchUp)", "SketchUp"],
  ["Tape Measure Tool (SketchUp)", "SketchUp"],
  ["Sandbox Tools (SketchUp)", "SketchUp"],
  ["Intersect with Model (SketchUp)", "SketchUp"],
  ["Solid Tools (SketchUp)", "SketchUp"],
  ["Extension Manager (SketchUp)", "SketchUp"],
  ["Solibri Office", "Nemetschek"],
  ["Solibri Rule Manager (Solibri)", "Solibri Office"],
  ["BCF Issue Management (Solibri)", "Solibri Office"],
  ["Solid Edge", "Siemens"],
  ["Synchronous Technology (Solid Edge)", "Solid Edge"],
  ["Synchronous Steering Wheel (Solid Edge)", "Solid Edge"],
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
  ["Direct Modeling (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["Pull Tool (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["Move Tool (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["Fill Tool (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["Sheet Metal Unfolding (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["Prep for Simulation (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["Reverse Engineering (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["Facet Tools (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["Assembly Structure (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["IronPython Scripting (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["Shared Topology (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["Dimensional Control (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["Clean Up & Repair (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["STEP/IGES Import (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["Measurement & Mass (ANSYS SpaceClaim)", "ANSYS SpaceClaim"],
  ["STAAD.Pro", "Bentley"],
  ["STAAD Analytical Frame Model (STAAD.Pro)", "STAAD.Pro"],
  ["Automated Steel Code Checker (STAAD.Pro)", "STAAD.Pro"],
  ["Siemens Teamcenter", "Siemens"],
  ["Active Workspace Interface (Teamcenter)", "Siemens Teamcenter"],
  ["JT Open Data Format (Teamcenter)", "Siemens Teamcenter"],
  ["Tekla Structures", "Trimble"],
  ["Steel Detailing (Tekla Structures)", "Tekla Structures"],
  ["Cast-in-Place Concrete (Tekla Structures)", "Tekla Structures"],
  ["Rebar Detailing (Tekla Structures)", "Tekla Structures"],
  ["Tekla Model Sharing (Tekla Structures)", "Tekla Structures"],
  ["Custom Components (Tekla Structures)", "Tekla Structures"],
  ["Drawing List (Tekla Structures)", "Tekla Structures"],
  ["Assembly Drawings (Tekla Structures)", "Tekla Structures"],
  ["Clash Check (Tekla Structures)", "Tekla Structures"],
  ["Organizer (Tekla Structures)", "Tekla Structures"],
  ["Open API (Tekla Structures)", "Tekla Structures"],
  ["IFC Import/Export (Tekla Structures)", "Tekla Structures"],
  ["Weld Marks & Specs (Tekla Structures)", "Tekla Structures"],
  ["Phase Manager (Tekla Structures)", "Tekla Structures"],
  ["User-Defined Attributes (Tekla Structures)", "Tekla Structures"],
  ["NC/DSTV Export (Tekla Structures)", "Tekla Structures"],
  ["Vectorworks", "Vectorworks (Nemetschek)"],
  ["Marionette (Vectorworks)", "Vectorworks"],
  ["Design vs. Sheet Layers (Vectorworks)", "Vectorworks"],
  ["Resource Manager (Vectorworks)", "Vectorworks"],
  ["Hybrid Symbols (Vectorworks)", "Vectorworks"],
  ["Landmark Site Model (Vectorworks)", "Vectorworks"],
  ["Spotlight Lighting (Vectorworks)", "Vectorworks"],
  ["Classes vs. Layers (Vectorworks)", "Vectorworks"],
  ["Data Tag Tool (Vectorworks)", "Vectorworks"],
  ["Wall Join Tool (Vectorworks)", "Vectorworks"],
  ["Plant Database (Vectorworks)", "Vectorworks"],
  ["ConnectCAD (Vectorworks)", "Vectorworks"],
  ["Braceworks (Vectorworks)", "Vectorworks"],
  ["Sheet Border & Title Block (Vectorworks)", "Vectorworks"],
  ["IFC & BIM Collaboration (Vectorworks)", "Vectorworks"],
  ["Marionette Nodes (Vectorworks)", "Vectorworks"],
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
        if (narrow) return Math.round(vh * 0.65);
        return Math.round(vh * 0.88);
      }
      return narrow ? 450 : 750;
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
    const ring = Math.min(width, height) * 0.28;
    simNodes.forEach((n, i, arr) => {
      const ang = (i / Math.max(arr.length, 1)) * Math.PI * 2 - Math.PI / 2;
      n.x = cxSeed + ring * Math.cos(ang);
      n.y = cySeed + ring * Math.sin(ang);
      
      const deg = degreeMap[n.id] || 0;
      let baseSize = 14; // Default base size for standard nodes
      if (n.type === "product") baseSize = 18;
      else if (n.type === "vendor") baseSize = 20;
      else if (n.type === "domain") baseSize = 22;
      
      // Connecting hubs get a significant dynamic boost up to +30px max (so key nodes can reach 52px radius / 104px diameter!)
      const sizeBoost = Math.min(deg * 2.8, 30);
      n.baseRadius = baseSize + sizeBoost;
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
          .distance((d) => 125 + Math.max(d.source.baseRadius || 0, d.target.baseRadius || 0) * 0.8)
          .strength(0.55)
      )
      .force("charge", d3.forceManyBody().strength((d) => -350 - (d.baseRadius * 16)))
      .force("x", d3.forceX(width / 2).strength(0.14))
      .force("y", d3.forceY(height / 2).strength(0.14))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius((d) => d.baseRadius + 20))
      .velocityDecay(0.20); // Stable initial decay

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
          const slug = d.slug || d.id.toLowerCase().replace(/\s+/g, "-");
          if (d.type === "product") {
            detailsBtn.href = `./kb/software/${slug}.html`;
          } else if (d.type === "vendor") {
            detailsBtn.href = `./kb/vendors/${slug}.html`;
          } else {
            detailsBtn.href = `./kb/concepts/${slug}.html`;
          }
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
        let dest = customUrl;
        if (!dest) {
          const slug = d.slug || d.id.toLowerCase().replace(/\s+/g, "-");
          if (d.type === "product") {
            dest = `./kb/software/${slug}.html`;
          } else if (d.type === "vendor") {
            dest = `./kb/vendors/${slug}.html`;
          } else {
            dest = `./kb/concepts/${slug}.html`;
          }
        }
        
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

  // -------------------------------------------------------------
  // Phase 5: Interactive Sub-Graph for Concept Detail Pages
  // -------------------------------------------------------------
  const subGraphStage = document.getElementById("kb-sub-graph-stage");
  if (subGraphStage && typeof window.d3 !== "undefined") {
      const d3 = window.d3;
      const currentNodeId = subGraphStage.getAttribute("data-current-node");
      
      const colorMap = {
        concept: "#7C8AFF",
        skill:   "#A6B0FF",
        domain:  "#8A6BC7",
        format:  "#5DC2A7",
        resource:"#D9B074",
        vendor:  "#E8C68A",
        product: "#5BB6E5",
        sdk:     "#B198F2",
      };

      const rootNode = nodes.find(n => n.id === currentNodeId);
      if (rootNode) {
          // Identify connected nodes in links list
          const connectedNodeIds = new Set();
          connectedNodeIds.add(currentNodeId);
          
          links.forEach(([source, target]) => {
              if (source === currentNodeId) connectedNodeIds.add(target);
              if (target === currentNodeId) connectedNodeIds.add(source);
          });

          // Expand: find parent software (product type) and sibling nodes under that product
          const parentProductNode = nodes.find(n => n.type === "product" && connectedNodeIds.has(n.id));
          if (parentProductNode) {
              links.forEach(([source, target]) => {
                  if (source === parentProductNode.id) connectedNodeIds.add(target);
                  if (target === parentProductNode.id) connectedNodeIds.add(source);
              });
          }

          // Limit siblings to prevent overcrowding in the small 320px widget
          const subNodes = nodes.filter(n => connectedNodeIds.has(n.id));
          let finalNodes = subNodes.filter(n => n.id === currentNodeId || n.type === "product");
          let otherNodes = subNodes.filter(n => n.id !== currentNodeId && n.type !== "product");
          finalNodes = finalNodes.concat(otherNodes.slice(0, 10)); // Max 12 nodes total

          const finalNodeIds = new Set(finalNodes.map(n => n.id));
          const finalLinks = links
              .filter(([source, target]) => finalNodeIds.has(source) && finalNodeIds.has(target))
              .map(([source, target]) => ({ source: source, target: target }));

          // Render micro sub-graph
          const width = subGraphStage.clientWidth || 600;
          const height = 320;

          // Append SVG
          const svg = d3.select(subGraphStage)
              .append("svg")
              .attr("width", "100%")
              .attr("height", "100%")
              .attr("viewBox", `0 0 ${width} ${height}`)
              .attr("preserveAspectRatio", "xMidYMid meet");

          const simNodes = finalNodes.map(n => ({ ...n }));
          
          // Seed positions
          simNodes.forEach((n, i) => {
              const angle = (i / simNodes.length) * Math.PI * 2;
              n.x = width / 2 + Math.cos(angle) * 70;
              n.y = height / 2 + Math.sin(angle) * 70;
          });

          const simulation = d3.forceSimulation(simNodes)
              .force("link", d3.forceLink(finalLinks).id(d => d.id).distance(105).strength(0.85))
              .force("charge", d3.forceManyBody().strength(-280))
              .force("center", d3.forceCenter(width / 2, height / 2))
              .force("collision", d3.forceCollide().radius(d => {
                  if (d.id === currentNodeId) return 30;
                  if (d.type === "product" || d.type === "vendor") return 24;
                  return 18;
              }))
              .velocityDecay(0.35);

          const linkSel = svg.append("g")
              .selectAll("line")
              .data(finalLinks)
              .join("line")
              .attr("stroke", "var(--accent)")
              .attr("stroke-opacity", 0.25)
              .attr("stroke-width", 1.5);

          const nodeG = svg.append("g")
              .selectAll("g")
              .data(simNodes)
              .join("g")
              .style("cursor", "pointer")
              .call(d3.drag()
                  .on("start", (event, d) => {
                      if (!event.active) simulation.alphaTarget(0.3).restart();
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

          // Render circles
          nodeG.append("circle")
              .attr("r", d => {
                  if (d.id === currentNodeId) return 22;
                  if (d.type === "product" || d.type === "vendor") return 16;
                  return 11;
              })
              .attr("fill", d => colorMap[d.type] || "#8b9dcf")
              .attr("stroke", d => d.id === currentNodeId ? "var(--accent)" : "#ffffff")
              .attr("stroke-width", d => d.id === currentNodeId ? 3.5 : 1.5);

          // Text labels
          nodeG.append("text")
              .attr("text-anchor", "middle")
              .attr("dy", d => {
                  if (d.id === currentNodeId) return 34;
                  if (d.type === "product" || d.type === "vendor") return 26;
                  return 20;
              })
              .style("font-size", "11px")
              .style("font-family", "Inter, sans-serif")
              .style("font-weight", d => d.id === currentNodeId ? "700" : "500")
              .style("fill", "var(--ink-text, #ffffff)")
              .text(d => d.id.includes(" (") ? d.id.split(" (")[0] : d.id); // strip software suffix

          // Tooltip on hover
          nodeG.append("title")
              .text(d => `${d.id}\nType: ${d.type}\nHint: ${d.hint || ""}`);

          // Navigation on click (single click is standard for smooth user flow)
          nodeG.on("click", (event, d) => {
              event.stopPropagation();
              if (d.id === currentNodeId) return; // ignore click on active
              
              // Map node ID to its slug and URL
              let dest = "";
              const slug = d.slug || d.id.toLowerCase().replace(/\s+/g, "-");
              
              const pathname = window.location.pathname;
              const isSoftware = pathname.includes("/kb/software/");
              const isVendors = pathname.includes("/kb/vendors/");
              const isConcepts = pathname.includes("/kb/concepts/");
              
              if (d.type === "product") {
                  if (isSoftware) {
                      dest = `./${slug}.html`;
                  } else {
                      dest = `../software/${slug}.html`;
                  }
              } else if (d.type === "vendor") {
                  if (isVendors) {
                      dest = `./${slug}.html`;
                  } else {
                      dest = `../vendors/${slug}.html`;
                  }
              } else {
                  // Default to concept
                  if (isConcepts) {
                      dest = `./${slug}.html`;
                  } else {
                      dest = `../concepts/${slug}.html`;
                  }
              }

              // Simple client-side head check to ensure page exists
              if (dest) {
                  if (window.location.protocol === "file:") {
                      window.location.href = dest;
                      return;
                  }
                  fetch(dest, { method: "HEAD" })
                      .then(res => {
                          if (res.ok) window.location.href = dest;
                          else window.location.href = `../../kb-terms.html?search=${encodeURIComponent(d.id)}`;
                      })
                      .catch(() => {
                          window.location.href = dest;
                      });
              }
          });

          simulation.on("tick", () => {
              linkSel
                  .attr("x1", l => l.source.x)
                  .attr("y1", l => l.source.y)
                  .attr("x2", l => l.target.x)
                  .attr("y2", l => l.target.y);
              nodeG.attr("transform", d => `translate(${d.x},${d.y})`);
          });
      }
  }
}
