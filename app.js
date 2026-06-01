// Register PWA Service Worker
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    // Determine the root relative path for registering sw.js
    const isSubdir = window.location.pathname.includes("/kb/concepts/") || window.location.pathname.includes("/kb/software/") || window.location.pathname.includes("/kb/vendors/");
    const swPath = isSubdir ? "../../sw.js" : "./sw.js";
    
    navigator.serviceWorker
      .register(swPath)
      .then((reg) => console.log("[PWA] ServiceWorker registered with scope: ", reg.scope))
      .catch((err) => console.error("[PWA] ServiceWorker registration failed: ", err));
  });
}

const navLinks = document.querySelectorAll("[data-nav]");
const current = document.body.getAttribute("data-page");

navLinks.forEach((link) => {
  if (link.getAttribute("data-nav") === current) link.classList.add("active");
});

document.getElementById("footer-year")?.append(String(new Date().getFullYear()));

// ---- Mobile hamburger menu ----
// Use event delegation on document so the handler keeps working even if
// the hamburger / nav / overlay nodes are duplicated or re-rendered, and
// even if this script runs before any of those nodes are present.
function getTopbarNav() {
  // Always re-query — the first `.nav` in DOM is the primary topbar nav.
  return document.querySelector(".nav");
}
function getTopbarHamburger() {
  return document.querySelector(".hamburger");
}
function getNavOverlay() {
  return document.querySelector(".nav-overlay");
}
function toggleMenu(forceState) {
  const nav = getTopbarNav();
  const hb = getTopbarHamburger();
  const ov = getNavOverlay();
  if (!nav) return;
  const willOpen = typeof forceState === "boolean"
    ? forceState
    : !nav.classList.contains("active");
  nav.classList.toggle("active", willOpen);
  if (hb) hb.classList.toggle("active", willOpen);
  if (ov) ov.classList.toggle("active", willOpen);
  // Prevent background scroll when the drawer is open.
  document.body.style.overflow = willOpen ? "hidden" : "";
}

// Delegated tap/click handler — survives DOM swaps, late hydration, etc.
function _navDelegatedHandler(ev) {
  const target = ev.target;
  if (!target || !target.closest) return;
  if (target.closest(".hamburger")) {
    ev.preventDefault();
    toggleMenu();
    return;
  }
  if (target.closest(".nav-close")) {
    ev.preventDefault();
    toggleMenu(false);
    return;
  }
  if (target.closest(".nav-overlay")) {
    toggleMenu(false);
    return;
  }
  // If a nav link is clicked AND the drawer is open, close it after.
  const link = target.closest(".nav .nav-link, .nav [data-nav]");
  const navEl = getTopbarNav();
  if (link && navEl && navEl.classList.contains("active")) {
    toggleMenu(false);
  }
}
document.addEventListener("click", _navDelegatedHandler);
document.addEventListener("touchend", function (ev) {
  // Only handle the hamburger via touch to keep delays low; click handles the rest.
  const t = ev.target;
  if (t && t.closest && t.closest(".hamburger")) {
    ev.preventDefault();
    toggleMenu();
  }
}, { passive: false });

// Close on Escape for keyboard users.
document.addEventListener("keydown", (ev) => {
  if (ev.key === "Escape") {
    const nav = getTopbarNav();
    if (nav && nav.classList.contains("active")) toggleMenu(false);
  }
});

(function initSiteNotice() {
  const notice = document.getElementById("site-notice");
  if (!notice) return;
  const id = notice.dataset.noticeId || "default";
  const key = `learncad-site-notice-${id}`;
  try {
    if (localStorage.getItem(key) === "1") {
      notice.classList.add("is-dismissed");
      return;
    }
  } catch {
    /* ignore */
  }
  const closeBtn = notice.querySelector(".site-notice-close");
  closeBtn?.addEventListener("click", () => {
    notice.classList.add("is-dismissed");
    try {
      localStorage.setItem(key, "1");
    } catch {
      /* ignore */
    }
  });
})();

(function initCookieConsent() {
  const banner = document.querySelector("[data-cookie-banner]");
  if (!banner) return;
  const key = "learncad-cookie-consent-v1";
  try {
    if (localStorage.getItem(key) === "1") {
      banner.classList.add("is-dismissed");
      return;
    }
  } catch {
    /* ignore */
  }
  const handleAccept = (e) => {
    if (e) e.preventDefault();
    banner.classList.add("is-dismissed");
    try {
      localStorage.setItem(key, "1");
    } catch { /* ignore */ }
  };

  banner.querySelectorAll(".cookie-consent-actions button")?.forEach(btn => {
    btn.addEventListener("click", handleAccept);
  });
  banner.querySelector(".cookie-consent-close")?.addEventListener("click", handleAccept);
})();

(function initContactFormDemo() {
  const form = document.getElementById("contact-form");
  const status = document.getElementById("contact-form-status");
  if (!form || !status) return;
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    status.hidden = false;
    status.textContent =
      "Demo only: nothing was transmitted. For real inquiries, use the mailbox links on this page.";
  });
})();

(function initTutorialFilters() {
  if (document.body.getAttribute("data-page") !== "tutorials") return;

  const chips = document.querySelectorAll(".chips .chip");
  const searchInput = document.querySelector(".search-row input");
  const searchBtn = document.querySelector(".search-row button");
  const tutorialItems = document.querySelectorAll(".tutorial-item");

  const state = {
    software: "all",
    task: "all",
    level: "all",
    price: "all",
    search: ""
  };

  // 1. Function to apply the current filter state
  function applyFilters() {
    tutorialItems.forEach((item) => {
      // Software filter (handles space-separated values)
      const itemSoftwareAttr = item.getAttribute("data-software") || "";
      const itemSoftwares = itemSoftwareAttr.split(/\s+/).filter(Boolean);
      const matchesSoftware =
        state.software === "all" || itemSoftwares.includes(state.software);

      // Task filter
      const matchesTask =
        state.task === "all" || item.getAttribute("data-task") === state.task;

      // Level filter
      const matchesLevel =
        state.level === "all" || item.getAttribute("data-level") === state.level;

      // Price filter
      const matchesPrice =
        state.price === "all" || item.getAttribute("data-price") === state.price;

      // Search text filter (title, description, tags)
      let matchesSearch = true;
      if (state.search.trim()) {
        const query = state.search.toLowerCase();
        const title = item.querySelector("h3")?.textContent.toLowerCase() || "";
        const desc = item.querySelector("p")?.textContent.toLowerCase() || "";
        const tags = Array.from(item.querySelectorAll(".tag"))
          .map((t) => t.textContent.toLowerCase())
          .join(" ");

        matchesSearch =
          title.includes(query) || desc.includes(query) || tags.includes(query);
      }

      if (matchesSoftware && matchesTask && matchesLevel && matchesPrice && matchesSearch) {
        item.style.display = "";
        setTimeout(() => {
          item.style.opacity = "1";
          item.style.transform = "translateY(0)";
        }, 10);
      } else {
        item.style.display = "none";
        item.style.opacity = "0";
      }
    });
  }

  // 2. Chip click handlers
  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const groupEl = chip.closest(".chips");
      if (!groupEl) return;

      const groupName = groupEl.getAttribute("data-filter-group");
      const filterValue = chip.getAttribute("data-filter-value");

      if (!groupName || !filterValue) return;

      // Toggle active classes in this group
      groupEl.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");

      // Update state and apply
      state[groupName] = filterValue;
      applyFilters();
    });
  });

  // 3. Search input handler
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      state.search = e.target.value;
      applyFilters();
    });

    // Also handle search button click
    searchBtn?.addEventListener("click", () => {
      state.search = searchInput.value;
      applyFilters();
    });

    // Support enter key on search input
    searchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        state.search = searchInput.value;
        applyFilters();
      }
    });
  }

  // 4. URL query parameter parsing
  function parseUrlParams() {
    const params = new URLSearchParams(window.location.search);
    
    // Check direct filter params (e.g. ?software=autocad)
    ["software", "task", "level", "price"].forEach((key) => {
      const val = params.get(key);
      if (val) {
        const chip = document.querySelector(`.chips[data-filter-group="${key}"] .chip[data-filter-value="${val}"]`);
        if (chip) {
          chip.click();
        }
      }
    });

    // Check generic search query parameter ?q=
    const query = params.get("q");
    if (query) {
      const lowerQuery = query.toLowerCase();

      // Check if query directly maps to one of our software values
      let mappedSoftware = null;
      if (lowerQuery.includes("autocad")) mappedSoftware = "autocad";
      else if (lowerQuery.includes("autodesk")) mappedSoftware = "autocad"; // fallback to AutoCAD
      else if (lowerQuery.includes("revit")) mappedSoftware = "revit";
      else if (lowerQuery.includes("fusion")) mappedSoftware = "fusion";
      else if (lowerQuery.includes("solidworks")) mappedSoftware = "solidworks";
      else if (lowerQuery.includes("catia")) mappedSoftware = "catia";
      else if (lowerQuery.includes("dassault")) mappedSoftware = "solidworks";
      else if (lowerQuery.includes("inventor")) mappedSoftware = "inventor";
      else if (lowerQuery.includes("civil")) mappedSoftware = "civil3d";
      else if (lowerQuery.includes("creo")) mappedSoftware = "creo";
      else if (lowerQuery.includes("ptc")) mappedSoftware = "creo";
      else if (lowerQuery.includes("siemens")) mappedSoftware = "nx";
      else if (lowerQuery.includes("nx")) mappedSoftware = "nx";
      else if (lowerQuery.includes("gstarcad")) mappedSoftware = "gstarcad";
      else if (lowerQuery.includes("gstarsoft")) mappedSoftware = "gstarcad";
      else if (lowerQuery.includes("rhino")) mappedSoftware = "rhino";

      if (mappedSoftware) {
        const chip = document.querySelector(`.chips[data-filter-group="software"] .chip[data-filter-value="${mappedSoftware}"]`);
        if (chip) {
          chip.click();
        }
      } else {
        // Just put it in the search input and filter
        if (searchInput) {
          searchInput.value = query;
          state.search = query;
          applyFilters();
        }
      }
    }
  }

  // 5. Sorting logic
  const sortSelect = document.getElementById("tutorial-sort-select");
  const listContainer = document.querySelector(".list");

  function sortTutorials() {
    if (!sortSelect || !listContainer) return;
    const sortBy = sortSelect.value;
    const items = Array.from(listContainer.querySelectorAll(".tutorial-item"));
    
    items.sort((a, b) => {
      if (sortBy === "duration-asc") {
        const durA = parseInt(a.getAttribute("data-duration") || "0", 10);
        const durB = parseInt(b.getAttribute("data-duration") || "0", 10);
        return durA - durB;
      } else if (sortBy === "duration-desc") {
        const durA = parseInt(a.getAttribute("data-duration") || "0", 10);
        const durB = parseInt(b.getAttribute("data-duration") || "0", 10);
        return durB - durA;
      } else if (sortBy === "difficulty-asc") {
        const levels = { "beginner": 1, "beginner–intermediate": 1.5, "intermediate": 2, "pro": 3, "—": 2 };
        const lvlA = levels[a.getAttribute("data-level")] || 2;
        const lvlB = levels[b.getAttribute("data-level")] || 2;
        return lvlA - lvlB;
      } else if (sortBy === "difficulty-desc") {
        const levels = { "beginner": 1, "beginner–intermediate": 1.5, "intermediate": 2, "pro": 3, "—": 2 };
        const lvlA = levels[a.getAttribute("data-level")] || 2;
        const lvlB = levels[b.getAttribute("data-level")] || 2;
        return lvlB - lvlA;
      } else if (sortBy === "newest") {
        const dateA = a.getAttribute("data-published") || "";
        const dateB = b.getAttribute("data-published") || "";
        return dateB.localeCompare(dateA);
      } else { // featured / highest rated
        const ratA = parseFloat(a.getAttribute("data-rating") || "0");
        const ratB = parseFloat(b.getAttribute("data-rating") || "0");
        return ratB - ratA;
      }
    });

    items.forEach(item => {
      listContainer.appendChild(item);
    });
  }

  if (sortSelect) {
    sortSelect.addEventListener("change", sortTutorials);
  }

  // Run initial parsing on load
  parseUrlParams();
  sortTutorials();
})();

// --- Phase 9: Interactive Roadmap & Career Skill Tree Logic ---
(function initRoadmapSkillTree() {
  const container = document.querySelector(".roadmap-container");
  if (!container) return; // Only run on knowledge-roadmap.html

  // Career Tracks Data
  const ROADMAP_DATA = {
    bim: {
      title: "BIM Coordinator (BIM 协调员)",
      salary: "Est. Salary: $65,000 - $95,000 / yr",
      software: "Revit, Navisworks, Solibri, IFC",
      nodes: [
        {
          id: "bim",
          title: "BIM Coordination",
          difficulty: "Beginner",
          level: 1,
          desc: "Building Information Modeling (BIM) operates on active, object-based relational databases coordinate design data.",
          why: "Essential core concept. BIM replaces basic 2D lines with smart parametric entities representing walls, doors, and piping.",
          wiki: "./kb/concepts/bim.html",
          tutorials: "./tutorials.html?q=bim"
        },
        {
          id: "revit",
          title: "Revit",
          difficulty: "Intermediate",
          level: 2,
          desc: "Autodesk's flagship BIM coordinator tool organizing structural, architectural and MEP models.",
          why: "Revit is the primary authoring platform used by design offices for model coordination.",
          wiki: "./kb/software/revit.html",
          tutorials: "./tutorials.html?q=revit"
        },
        {
          id: "shared-coords",
          title: "Shared Coordinates",
          difficulty: "Intermediate",
          level: 2,
          desc: "Multi-disciplinary coordinate system ensuring all project elements align perfectly in global coordinate space.",
          why: "Prevents drawing shift errors during multi-discipline assembly merges and clash checks.",
          wiki: "./kb/concepts/shared-coordinates-revit.html",
          tutorials: "./tutorials.html?q=coordinates"
        },
        {
          id: "clash",
          title: "Clash Detection",
          difficulty: "Pro",
          level: 3,
          desc: "Diagnostic clash detection verifying physical geometry intersections between MEP and structural frameworks.",
          why: "Crucial project deliverable. Saves millions in site reconstruction costs by finding overlaps pre-build.",
          wiki: "./kb/concepts/navisworks-clash-detection.html",
          tutorials: "./tutorials.html?q=clash"
        },
        {
          id: "ifc",
          title: "IFC Export",
          difficulty: "Pro",
          level: 3,
          desc: "Industry Foundation Classes (IFC) data export mapping drawing entities to open-standard definitions.",
          why: "Critical for openBIM coordination, letting Revit, Bentley, and ArchiCAD models federate cleanly.",
          wiki: "./kb/concepts/ifc-export-revit.html",
          tutorials: "./tutorials.html?q=ifc"
        }
      ],
      links: [
        { from: "bim", to: "revit" },
        { from: "bim", to: "shared-coords" },
        { from: "revit", to: "clash" },
        { from: "shared-coords", to: "clash" },
        { from: "clash", to: "ifc" }
      ]
    },
    mcad: {
      title: "Mechanical Design Engineer (机械设计工程师)",
      salary: "Est. Salary: $70,000 - $105,000 / yr",
      software: "SOLIDWORKS, Autodesk Inventor, CATIA",
      nodes: [
        {
          id: "parametrics",
          title: "Parametric Constraints",
          difficulty: "Beginner",
          level: 1,
          desc: "Mathematical dimension and relationship rules governing sketch behavior (tangency, concentricity).",
          why: "Foundation of mechanical solid modeling. Lets designers change dimensions and automatically update parts.",
          wiki: "./kb/concepts/parametric-constraints.html",
          tutorials: "./tutorials.html?q=constraints"
        },
        {
          id: "solidworks",
          title: "SOLIDWORKS",
          difficulty: "Intermediate",
          level: 2,
          desc: "Industry standard solid modeler utilizing parametric feature trees and assembly constraints.",
          why: "The most widely deployed mid-range MCAD software for industrial product design.",
          wiki: "./kb/software/solidworks.html",
          tutorials: "./tutorials.html?q=solidworks"
        },
        {
          id: "brep",
          title: "B-Rep Modeling",
          difficulty: "Intermediate",
          level: 2,
          desc: "Boundary Representation kernels maintaining model topology via mathematical faces, edges, and vertices.",
          why: "Understanding B-Rep prevents solver failures and zero-thickness geometry regeneration errors.",
          wiki: "./kb/concepts/intelligent-objects.html",
          tutorials: "./tutorials.html?q=modeling"
        },
        {
          id: "assembly",
          title: "MCAD Assembly",
          difficulty: "Pro",
          level: 3,
          desc: "Assembling discrete parts together using kinematic mate conditions (coincident, concentric, parallel).",
          why: "Enables designers to verify fits, tolerances, clearances, and run mechanical animations.",
          wiki: "./kb/concepts/skeleton-creo.html",
          tutorials: "./tutorials.html?q=assembly"
        },
        {
          id: "mbd",
          title: "Model-Based Definition",
          difficulty: "Pro",
          level: 3,
          desc: "Injecting manufacturing dimensions and product specifications (GD&T) directly into 3D solid profiles.",
          why: "Eliminates the need for tedious 2D drawing sheets by using rich digital metadata.",
          wiki: "./kb/concepts/model-based-definition-solidworks.html",
          tutorials: "./tutorials.html?q=mbd"
        }
      ],
      links: [
        { from: "parametrics", to: "solidworks" },
        { from: "parametrics", to: "brep" },
        { from: "solidworks", to: "assembly" },
        { from: "brep", to: "assembly" },
        { from: "assembly", to: "mbd" }
      ]
    },
    civil: {
      title: "Civil Infrastructure Engineer (市政/土木工程师)",
      salary: "Est. Salary: $68,000 - $100,000 / yr",
      software: "Civil 3D, Infraworks, LandXML",
      nodes: [
        {
          id: "surfaces",
          title: "Surfaces & Grading",
          difficulty: "Beginner",
          level: 1,
          desc: "Creating digital terrain models (DTM) using triangles (TIN) representing topography.",
          why: "Foundation of all civil sites. Surfaces calculate precise cut-and-fill volumes.",
          wiki: "./kb/concepts/surfaces-civil-3d.html",
          tutorials: "./tutorials.html?q=surfaces"
        },
        {
          id: "civil3d",
          title: "Civil 3D",
          difficulty: "Intermediate",
          level: 2,
          desc: "Autodesk's land development platform built on top of the AutoCAD drafting engine.",
          why: "The primary tool for civil drawings, grading, and road network designs.",
          wiki: "./kb/software/civil-3d.html",
          tutorials: "./tutorials.html?q=civil"
        },
        {
          id: "alignments",
          title: "Alignments & Profiles",
          difficulty: "Intermediate",
          level: 2,
          desc: "Horizontal road centerlines (alignments) paired with vertical elevation grids (profiles).",
          why: "Defines the 3D pathway coordinates for highways, pipelines, and rail tracks.",
          wiki: "./kb/concepts/profiles-civil-3d.html",
          tutorials: "./tutorials.html?q=profile"
        },
        {
          id: "corridors",
          title: "Corridor Modeling",
          difficulty: "Pro",
          level: 3,
          desc: "Sweeping road cross-sections (assemblies) along a 3D alignment and profile path.",
          why: "Creates rich 3D road models with dynamic shoulders, daylight grading, and cut limits.",
          wiki: "./kb/concepts/subassembly-civil-3d.html",
          tutorials: "./tutorials.html?q=corridor"
        },
        {
          id: "landxml",
          title: "LandXML Exchange",
          difficulty: "Pro",
          level: 3,
          desc: "Open standard file format transferring surfaces, alignments, and parcels to survey equipment.",
          why: "Essential for site deployment. Connects designer offices directly to GPS grading hardware.",
          wiki: "./kb/concepts/pressure-networks-civil-3d.html",
          tutorials: "./tutorials.html?q=xml"
        }
      ],
      links: [
        { from: "surfaces", to: "civil3d" },
        { from: "surfaces", to: "alignments" },
        { from: "civil3d", to: "corridors" },
        { from: "alignments", to: "corridors" },
        { from: "corridors", to: "landxml" }
      ]
    },
    draft: {
      title: "2D Drafting & Standard Specialist (CAD 制图专家)",
      salary: "Est. Salary: $50,000 - $75,000 / yr",
      software: "AutoCAD, GstarCAD, ZWCAD",
      nodes: [
        {
          id: "layer",
          title: "Layer Strategy",
          difficulty: "Beginner",
          level: 1,
          desc: "Organizing DWG assets by layers with strict color, linetype, and viewport visibility properties.",
          why: "Basic hygiene of all drawing files. Structured layering keeps drawings readable.",
          wiki: "./kb/concepts/layer.html",
          tutorials: "./tutorials.html?q=layer"
        },
        {
          id: "xref",
          title: "Xrefs & Blocks",
          difficulty: "Intermediate",
          level: 2,
          desc: "Linking external DWG files (Xrefs) and grouping recurring items as block references.",
          why: "Crucial for team drafting. Keeps parent files lightweight by referencing background plates.",
          wiki: "./kb/concepts/xref.html",
          tutorials: "./tutorials.html?q=xref"
        },
        {
          id: "alias",
          title: "Command Aliases",
          difficulty: "Intermediate",
          level: 2,
          desc: "Keyboard shortcuts mapping fast inputs (L for LINE, CO for COPY) into the CAD console.",
          why: "Draftsman speed enhancer. Minimizes reliance on mouse clicks, boosting efficiency.",
          wiki: "./kb/concepts/command-alias.html",
          tutorials: "./tutorials.html?q=alias"
        },
        {
          id: "plot",
          title: "Plot & Layout Setup",
          difficulty: "Pro",
          level: 3,
          desc: "Configuring paperspace layouts, viewports, annotation scaling, and CTB plot styles.",
          why: "Guarantees drawings print accurately to scale without overlapping lines.",
          wiki: "./kb/concepts/plot-style.html",
          tutorials: "./tutorials.html?q=plot"
        },
        {
          id: "merge",
          title: "Drawing Merge & Compare",
          difficulty: "Pro",
          level: 3,
          desc: "Auditing revision changes and merging changes from external coordinates cleanly.",
          why: "Crucial for coordination. Ensures concurrent edits merge without database corruption.",
          wiki: "./kb/concepts/drawing-merge.html",
          tutorials: "./tutorials.html?q=compare"
        }
      ],
      links: [
        { from: "layer", to: "xref" },
        { from: "layer", to: "alias" },
        { from: "xref", to: "plot" },
        { from: "alias", to: "plot" },
        { from: "plot", to: "merge" }
      ]
    }
  };

  // State Management
  let activeTrack = "bim";
  let masteredProgress = JSON.parse(localStorage.getItem("gstarcademy_roadmap_progress")) || {
    bim: [],
    mcad: [],
    civil: [],
    draft: []
  };

  // Ensure default structures are safe
  ["bim", "mcad", "civil", "draft"].forEach(t => {
    if (!masteredProgress[t]) masteredProgress[t] = [];
  });

  // UI Element Selectors
  const trackTabs = document.querySelectorAll(".roadmap-track-tab");
  const trackTitle = document.getElementById("track-title");
  const trackSalary = document.getElementById("track-salary");
  const trackSoftware = document.getElementById("track-software");
  const progressPercent = document.getElementById("progress-percent");
  const progressFill = document.getElementById("progress-fill");
  
  const levels = {
    1: document.getElementById("level-1"),
    2: document.getElementById("level-2"),
    3: document.getElementById("level-3")
  };

  const inspectTitle = document.getElementById("inspect-title");
  const inspectDifficulty = document.getElementById("inspect-difficulty");
  const inspectDesc = document.getElementById("inspect-desc");
  const inspectWhy = document.getElementById("inspect-why");
  const btnWiki = document.getElementById("btn-inspect-wiki");
  const btnTuts = document.getElementById("btn-inspect-tutorials");
  const btnReset = document.getElementById("btn-reset-track");

  // Render nodes for active track
  function renderTree() {
    // Clear stages
    levels[1].innerHTML = "";
    levels[2].innerHTML = "";
    levels[3].innerHTML = "";
    
    const track = ROADMAP_DATA[activeTrack];
    
    // Set Header details
    trackTitle.textContent = track.title;
    trackSalary.innerHTML = `💼 <strong>Est. Salary:</strong> ${track.salary}`;
    trackSoftware.innerHTML = `🛠️ <strong>Stack:</strong> ${track.software}`;
    
    // Render Nodes
    track.nodes.forEach(node => {
      const nodeSlug = node.wiki ? node.wiki.split("/").pop().replace(".html", "") : "";
      let isMastered = masteredProgress[activeTrack].includes(node.id);
      
      // Sync from quiz mastery
      let masteredConcepts = [];
      try {
        masteredConcepts = JSON.parse(localStorage.getItem("gstarcademy_concept_mastery")) || [];
      } catch (e) {}
      
      if (nodeSlug && masteredConcepts.includes(nodeSlug)) {
        isMastered = true;
        if (!masteredProgress[activeTrack].includes(node.id)) {
          masteredProgress[activeTrack].push(node.id);
          localStorage.setItem("gstarcademy_roadmap_progress", JSON.stringify(masteredProgress));
        }
      }
      
      const card = document.createElement("div");
      card.className = "skill-node" + (isMastered ? " mastered" : "");
      card.setAttribute("data-node-id", node.id);
      
      card.innerHTML = `
        <div class="skill-node-checkbox"></div>
        <div class="skill-node-info">
          <span class="skill-node-title">${node.title}</span>
          <span class="skill-node-difficulty">${isMastered ? "✓ Mastered" : node.difficulty}</span>
        </div>
      `;
      
      // Node Click handler - show details in inspector
      card.addEventListener("click", (e) => {
        // If click is on checkbox, toggle mastery
        if (e.target.closest(".skill-node-checkbox")) {
          e.stopPropagation();
          toggleMastery(node.id, card);
          return;
        }
        
        selectNode(node, card);
      });
      
      levels[node.level].appendChild(card);
    });

    updateProgressHUD();
    
    // Clear inspector
    resetInspectorPanel();

    // Draw lines after layout renders
    setTimeout(drawConnectorLines, 100);
  }

  function selectNode(node, cardEl) {
    document.querySelectorAll(".skill-node").forEach(n => n.classList.remove("selected"));
    cardEl.classList.add("selected");

    inspectTitle.textContent = node.title;
    inspectDifficulty.textContent = node.difficulty;
    inspectDifficulty.style.display = "inline-block";
    
    // Set difficulty badge colors
    if (node.difficulty === "Beginner") {
      inspectDifficulty.style.background = "rgba(16, 185, 129, 0.1)";
      inspectDifficulty.style.color = "#10b981";
    } else if (node.difficulty === "Intermediate") {
      inspectDifficulty.style.background = "rgba(59, 130, 246, 0.1)";
      inspectDifficulty.style.color = "#3b82f6";
    } else {
      inspectDifficulty.style.background = "rgba(99, 102, 241, 0.1)";
      inspectDifficulty.style.color = "#6366f1";
    }

    inspectDesc.textContent = node.desc;
    inspectWhy.innerHTML = `<strong>Why it matters:</strong> ${node.why}`;
    inspectWhy.style.display = "block";

    btnWiki.href = node.wiki;
    btnWiki.style.display = "inline-flex";

    btnTuts.href = node.tutorials;
    btnTuts.style.display = "inline-flex";
  }

  function toggleMastery(nodeId, cardEl) {
    const masteredList = masteredProgress[activeTrack];
    const index = masteredList.indexOf(nodeId);
    const nodeObj = ROADMAP_DATA[activeTrack].nodes.find(n => n.id === nodeId);
    const nodeSlug = nodeObj && nodeObj.wiki ? nodeObj.wiki.split("/").pop().replace(".html", "") : "";
    
    let masteredConcepts = [];
    try {
      masteredConcepts = JSON.parse(localStorage.getItem("gstarcademy_concept_mastery")) || [];
    } catch (e) {}
    
    if (index >= 0) {
      // Remove mastery
      masteredList.splice(index, 1);
      cardEl.classList.remove("mastered");
      cardEl.querySelector(".skill-node-difficulty").textContent = nodeObj.difficulty;
      
      // Sync out to quiz mastery
      if (nodeSlug) {
        const qIndex = masteredConcepts.indexOf(nodeSlug);
        if (qIndex >= 0) {
          masteredConcepts.splice(qIndex, 1);
          localStorage.setItem("gstarcademy_concept_mastery", JSON.stringify(masteredConcepts));
        }
      }
    } else {
      // Add mastery
      masteredList.push(nodeId);
      cardEl.classList.add("mastered");
      cardEl.querySelector(".skill-node-difficulty").textContent = "✓ Mastered";
      
      // Sync out to quiz mastery
      if (nodeSlug && !masteredConcepts.includes(nodeSlug)) {
        masteredConcepts.push(nodeSlug);
        localStorage.setItem("gstarcademy_concept_mastery", JSON.stringify(masteredConcepts));
      }
      
      // Simple particle shockwave or visual shake on checking
      cardEl.style.transform = "scale(0.96)";
      setTimeout(() => { cardEl.style.transform = ""; }, 100);
    }
    
    // Update local storage
    localStorage.setItem("gstarcademy_roadmap_progress", JSON.stringify(masteredProgress));
    
    updateProgressHUD();
    drawConnectorLines();
  }

  function updateProgressHUD() {
    const track = ROADMAP_DATA[activeTrack];
    const total = track.nodes.length;
    const completed = masteredProgress[activeTrack].length;
    const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
    
    progressPercent.textContent = `${pct}%`;
    progressFill.style.width = `${pct}%`;
  }

  function resetInspectorPanel() {
    inspectTitle.textContent = "Click a skill node to inspect";
    inspectDifficulty.style.display = "none";
    inspectDesc.textContent = "Select any competency node above to view core technical definitions, industry importance, and quick links to master it.";
    inspectWhy.style.display = "none";
    btnWiki.style.display = "none";
    btnTuts.style.display = "none";
  }

  // Draw linking curves in SVG
  function drawConnectorLines() {
    const svg = document.getElementById("roadmap-connectors");
    if (!svg) return;
    svg.innerHTML = ""; // Clear
    
    const containerRect = svg.getBoundingClientRect();
    const track = ROADMAP_DATA[activeTrack];
    
    track.links.forEach(link => {
      const fromNode = document.querySelector(`[data-node-id="${link.from}"]`);
      const toNode = document.querySelector(`[data-node-id="${link.to}"]`);
      if (!fromNode || !toNode) return;
      
      const fromRect = fromNode.getBoundingClientRect();
      const toRect = toNode.getBoundingClientRect();
      
      // SVG local coordinates
      const x1 = (fromRect.left + fromRect.right) / 2 - containerRect.left;
      const y1 = fromRect.bottom - containerRect.top;
      
      const x2 = (toRect.left + toRect.right) / 2 - containerRect.left;
      const y2 = toRect.top - containerRect.top;
      
      const isFromMastered = masteredProgress[activeTrack].includes(link.from);
      const isToMastered = masteredProgress[activeTrack].includes(link.to);
      const isActive = isFromMastered && isToMastered;
      
      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      const midY = (y1 + y2) / 2;
      const d = `M ${x1} ${y1} C ${x1} ${midY}, ${x2} ${midY}, ${x2} ${y2}`;
      
      path.setAttribute("d", d);
      path.setAttribute("class", "roadmap-connector-path" + (isActive ? " active" : ""));
      svg.appendChild(path);
    });
  }

  // Hook tab switch listeners
  trackTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      trackTabs.forEach(t => {
        t.classList.remove("active");
        t.setAttribute("aria-selected", "false");
      });
      tab.classList.add("active");
      tab.setAttribute("aria-selected", "true");
      activeTrack = tab.getAttribute("data-track");
      renderTree();
    });
  });

  // Hook reset progress
  btnReset.addEventListener("click", () => {
    if (confirm(`Reset all progress for the ${ROADMAP_DATA[activeTrack].title} pathway?`)) {
      // Clear roadmap nodes completed state
      masteredProgress[activeTrack] = [];
      localStorage.setItem("gstarcademy_roadmap_progress", JSON.stringify(masteredProgress));
      
      // Clear associated concept masteries for this track
      let masteredConcepts = [];
      try {
        masteredConcepts = JSON.parse(localStorage.getItem("gstarcademy_concept_mastery")) || [];
      } catch (e) {}
      
      const trackNodes = ROADMAP_DATA[activeTrack].nodes;
      trackNodes.forEach(node => {
        if (node.wiki) {
          const slug = node.wiki.split("/").pop().replace(".html", "");
          const idx = masteredConcepts.indexOf(slug);
          if (idx >= 0) {
            masteredConcepts.splice(idx, 1);
          }
        }
      });
      
      try {
        localStorage.setItem("gstarcademy_concept_mastery", JSON.stringify(masteredConcepts));
      } catch (e) {}
      
      renderTree();
    }
  });

  // Initial render
  renderTree();
  window.addEventListener("resize", drawConnectorLines);
})();

// --- Self-Test Quiz Interaction Logic ---
(function initConceptQuiz() {
  const quizContainers = document.querySelectorAll("[data-quiz-container]");
  if (!quizContainers.length) return;

  // Load mastered concepts from localStorage
  let masteredConcepts = [];
  try {
    masteredConcepts = JSON.parse(localStorage.getItem("gstarcademy_concept_mastery")) || [];
  } catch (e) {
    masteredConcepts = [];
  }

  quizContainers.forEach(container => {
    const termSlug = container.getAttribute("data-term-slug");
    const correctIdx = parseInt(container.getAttribute("data-correct-idx"), 10);
    const optionBtns = container.querySelectorAll(".kb-quiz-option-btn");
    const explanationBox = container.querySelector("[data-explanation-box]");
    const feedbackTitle = container.querySelector("[data-feedback-title]");

    // If already mastered previously, show it as correct immediately
    if (masteredConcepts.includes(termSlug)) {
      optionBtns.forEach((btn, idx) => {
        btn.classList.add("disabled");
        if (idx === correctIdx) {
          btn.classList.add("correct");
        }
      });
      if (explanationBox) {
        explanationBox.style.display = "block";
        if (feedbackTitle) {
          feedbackTitle.textContent = "✓ Mastered (Previously Completed)";
          feedbackTitle.style.color = "#10b981";
        }
      }
    }

    // Add click listeners to option buttons
    optionBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        const selectedIdx = parseInt(btn.getAttribute("data-option-idx"), 10);
        const isCorrect = selectedIdx === correctIdx;

        // Visual feedback on selected option
        optionBtns.forEach((b, idx) => {
          b.classList.add("disabled");
          if (idx === correctIdx) {
            b.classList.add("correct");
          } else if (idx === selectedIdx && !isCorrect) {
            b.classList.add("incorrect");
          }
        });

        // Show explanation
        if (explanationBox) {
          explanationBox.style.display = "block";
          if (feedbackTitle) {
            if (isCorrect) {
              feedbackTitle.textContent = "✓ Correct!";
              feedbackTitle.style.color = "#10b981";
            } else {
              feedbackTitle.textContent = "✕ Incorrect. Try studying the concept again!";
              feedbackTitle.style.color = "#ef4444";
            }
          }
        }

        // If correct, save to localStorage
        if (isCorrect && !masteredConcepts.includes(termSlug)) {
          masteredConcepts.push(termSlug);
          try {
            localStorage.setItem("gstarcademy_concept_mastery", JSON.stringify(masteredConcepts));
          } catch (e) {}

          // Highlight the parent card
          container.style.borderColor = "#10b981";
          container.style.boxShadow = "0 8px 24px -4px rgba(16, 185, 129, 0.12)";
        }
      });
    });
  });
})();

// --- Article Helpfulness Feedback Widget ---
(function initArticleFeedback() {
  const container = document.querySelector("[data-feedback-container]");
  if (!container) return;

  const termSlug = container.getAttribute("data-term-slug");
  const promptEl = container.querySelector("[data-feedback-prompt]");
  const thankyouEl = container.querySelector("[data-feedback-thankyou]");
  const buttons = container.querySelectorAll(".feedback-btn");

  let votedArticles = [];
  try {
    votedArticles = JSON.parse(localStorage.getItem("gstarcademy_feedback_votes")) || [];
  } catch (e) {}

  if (votedArticles.includes(termSlug)) {
    promptEl.style.display = "none";
    thankyouEl.style.display = "block";
    thankyouEl.textContent = "✓ You have already voted on this article. Thank you!";
  }

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      // Save vote state locally
      votedArticles.push(termSlug);
      try {
        localStorage.setItem("gstarcademy_feedback_votes", JSON.stringify(votedArticles));
      } catch (e) {}

      // Visual feedback
      promptEl.style.display = "none";
      thankyouEl.style.display = "block";
    });
  });
})();



