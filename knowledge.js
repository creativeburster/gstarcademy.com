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
  { id: "CATIA GSD", group: 2, type: "concept", radius: 8, tags: ["catia", "mfg"] },
  { id: "CATIA PowerCopy", group: 2, type: "concept", radius: 8, tags: ["catia", "mfg"] },
  { id: "Creo Parametric", group: 2, type: "product", radius: 8, tags: ["creo", "mfg"] },
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
  ["Fusion Timeline", "Fusion 360"],
  ["Fusion Joints", "Fusion 360"],
  ["Fusion Generative Design", "Fusion 360"],
  ["Fusion T-Splines", "Fusion 360"],
  ["Fusion CAM Setup", "Fusion 360"],
  ["Fusion Mesh Repair", "Fusion 360"],
  ["Fusion Cloud Render", "Fusion 360"],
  ["Fusion Direct Modeling", "Fusion 360"],
  ["Fusion Extensions", "Fusion 360"],
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
  ["Creo Parametric", "Creo"],
  ["Creo Direct", "Creo"],
  ["Creo Simulate", "Creo"],
  ["Creo Unite Technology", "Creo"],
  ["Creo Skeleton Modeling", "Creo"],
  ["Creo Flexible Modeling", "Creo"],
  ["Creo Windchill Integration", "Creo"],
  ["Creo Family Tables", "Creo"],
  ["Creo Mechanism Design", "Creo"],
  ["Creo Topology Optimization", "Creo"],
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
  ["Dassault 3DEXPERIENCE", "Dassault Systemes"],
  ["Dassault ENOVIA", "Dassault Systemes"],
  ["Dassault DELMIA", "Dassault Systemes"],
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
    ["Navisworks", "NWD/NWF"],
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
      .attr("r", (d) => d.baseRadius)
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
