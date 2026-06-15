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
})();(function initTutorialFilters() {
  if (document.body.getAttribute("data-page") !== "tutorials") return;

  const chips = document.querySelectorAll(".chips .chip");
  const searchInput = document.querySelector(".search-row input");
  const searchBtn = document.querySelector(".search-row button");
  const tutorialItems = document.querySelectorAll(".tutorial-item");
  const listContainer = document.querySelector(".list");

  const state = {
    software: "all",
    task: "all",
    level: "all",
    price: "all",
    search: ""
  };

  // 创建动态空状态占位
  let noResultsEl = document.getElementById("tutorials-no-results");
  if (!noResultsEl && listContainer) {
    noResultsEl = document.createElement("div");
    noResultsEl.id = "tutorials-no-results";
    noResultsEl.style.display = "none";
    noResultsEl.style.flexDirection = "column";
    noResultsEl.style.alignItems = "center";
    noResultsEl.style.justifyContent = "center";
    noResultsEl.style.padding = "60px 40px";
    noResultsEl.style.textAlign = "center";
    noResultsEl.style.background = "var(--surface-soft)";
    noResultsEl.style.border = "1px dashed var(--line-strong)";
    noResultsEl.style.borderRadius = "20px";
    noResultsEl.style.margin = "20px 0";
    noResultsEl.style.gap = "12px";
    
    noResultsEl.innerHTML = `
      <span style="font-size: 40px;">🔍</span>
      <h3 style="font-size: 1.25rem; font-weight: 700; color: var(--text-main); margin: 0;">No Tutorials Found</h3>
      <p style="font-size: 14px; color: var(--text-muted); max-width: 380px; margin: 0 auto;">We couldn't find any lessons matching your filters. Try selecting a different software, clearing your search, or resetting pricing filters.</p>
      <button type="button" class="btn btn-secondary" id="btn-reset-filters" style="margin-top: 8px; font-size: 13px; font-weight: 700;">Reset Filters</button>
    `;
    listContainer.appendChild(noResultsEl);

    noResultsEl.querySelector("#btn-reset-filters").addEventListener("click", () => {
      document.querySelectorAll(".chips").forEach(group => {
        group.querySelectorAll(".chip").forEach(c => c.classList.remove("active"));
        const allChip = group.querySelector('.chip[data-filter-value="all"]');
        if (allChip) allChip.classList.add("active");
      });
      if (searchInput) searchInput.value = "";
      state.software = "all";
      state.task = "all";
      state.level = "all";
      state.price = "all";
      state.search = "";
      applyFilters();
    });
  }

  // 1. Function to apply the current filter state
  function applyFilters() {
    let visibleCount = 0;

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
        visibleCount++;
        // 先设为 display 展现，重置不带转换的初始值
        if (item.style.display === "none") {
          item.style.display = "";
          item.style.opacity = "0";
          item.style.transform = "translateY(12px)";
        }
        
        // 微小延迟触发 CSS 过渡
        setTimeout(() => {
          item.style.opacity = "1";
          item.style.transform = "translateY(0)";
        }, 20);
      } else {
        item.style.display = "none";
        item.style.opacity = "0";
      }
    });

    // 控制空状态显隐
    if (noResultsEl) {
      noResultsEl.style.display = visibleCount === 0 ? "flex" : "none";
    }
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
          // 清空同组 active 并高亮此项
          const groupEl = chip.closest(".chips");
          if (groupEl) {
            groupEl.querySelectorAll(".chip").forEach(c => c.classList.remove("active"));
          }
          chip.classList.add("active");
          state[key] = val;
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
          const groupEl = chip.closest(".chips");
          if (groupEl) {
            groupEl.querySelectorAll(".chip").forEach(c => c.classList.remove("active"));
          }
          chip.classList.add("active");
          state.software = mappedSoftware;
        }
      } else {
        // Just put it in the search input and filter
        if (searchInput) {
          searchInput.value = query;
          state.search = query;
        }
      }
    }
    
    // 执行初次筛选
    applyFilters();
  }

  // 5. Sorting logic
  const sortSelect = document.getElementById("tutorial-sort-select");

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
  window.ROADMAP_DATA = {
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
          pitfall: "Do not treat BIM as just a 3D visual model; a 3D model without metadata is not a BIM model.",
          wiki: "./kb/concepts/bim",
          tutorials: "./tutorials?q=bim"
        },
        {
          id: "revit",
          title: "Revit",
          difficulty: "Intermediate",
          level: 2,
          desc: "Autodesk's flagship BIM coordinator tool organizing structural, architectural and MEP models.",
          why: "Revit is the primary authoring platform used by design offices for model coordination.",
          pitfall: "Avoid loading high-polygon nested families directly, which degrades pan/zoom and synchronization speed.",
          wiki: "./kb/software/revit",
          tutorials: "./tutorials?q=revit"
        },
        {
          id: "shared-coords",
          title: "Shared Coordinates",
          difficulty: "Intermediate",
          level: 2,
          desc: "Multi-disciplinary coordinate system ensuring all project elements align perfectly in global coordinate space.",
          why: "Prevents drawing shift errors during multi-discipline assembly merges and clash checks.",
          pitfall: "Never manually drag linked models to align them. Always acquire coordinates to maintain georeferenced accuracy.",
          wiki: "./kb/concepts/shared-coordinates-revit",
          tutorials: "./tutorials?q=coordinates"
        },
        {
          id: "clash",
          title: "Clash Detection",
          difficulty: "Pro",
          level: 3,
          desc: "Diagnostic clash detection verifying physical geometry intersections between MEP and structural frameworks.",
          why: "Crucial project deliverable. Saves millions in site reconstruction costs by finding overlaps pre-build.",
          pitfall: "Do not run clash tests on the entire model without filter rules. This creates thousands of useless duplicate clash reports.",
          wiki: "./kb/concepts/navisworks-clash-detection",
          tutorials: "./tutorials?q=clash"
        },
        {
          id: "ifc",
          title: "IFC Export",
          difficulty: "Pro",
          level: 3,
          desc: "Industry Foundation Classes (IFC) data export mapping drawing entities to open-standard definitions.",
          why: "Critical for openBIM coordination, letting Revit, Bentley, and ArchiCAD models federate cleanly.",
          pitfall: "Always specify the required IFC Schema version in the BEP, as incorrect export settings strip custom parameters.",
          wiki: "./kb/concepts/ifc-export-revit",
          tutorials: "./tutorials?q=ifc"
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
          pitfall: "Avoid over-constraining sketch geometries; doing so locks relations and triggers parametric solver conflicts.",
          wiki: "./kb/concepts/parametric-constraints",
          tutorials: "./tutorials?q=constraints"
        },
        {
          id: "solidworks",
          title: "SOLIDWORKS",
          difficulty: "Intermediate",
          level: 2,
          desc: "Industry standard solid modeler utilizing parametric feature trees and assembly constraints.",
          why: "The most widely deployed mid-range MCAD software for industrial product design.",
          pitfall: "Never rename CAD part files directly in Windows Explorer; doing so breaks mates and assembly links.",
          wiki: "./kb/software/solidworks",
          tutorials: "./tutorials?q=solidworks"
        },
        {
          id: "brep",
          title: "B-Rep Modeling",
          difficulty: "Intermediate",
          level: 2,
          desc: "Boundary Representation kernels maintaining model topology via mathematical faces, edges, and vertices.",
          why: "Understanding B-Rep prevents solver failures and zero-thickness geometry regeneration errors.",
          pitfall: "Avoid creating zero-thickness geometries or self-intersecting boundary loops, which crash feature regeneration.",
          wiki: "./kb/concepts/intelligent-objects",
          tutorials: "./tutorials?q=modeling"
        },
        {
          id: "assembly",
          title: "MCAD Assembly",
          difficulty: "Pro",
          level: 3,
          desc: "Assembling discrete parts together using kinematic mate conditions (coincident, concentric, parallel).",
          why: "Enables designers to verify fits, tolerances, clearances, and run mechanical animations.",
          pitfall: "Never create circular mate references in assemblies. They trigger rebuild loops and slow performance.",
          wiki: "./kb/concepts/skeleton-creo",
          tutorials: "./tutorials?q=assembly"
        },
        {
          id: "mbd",
          title: "Model-Based Definition",
          difficulty: "Pro",
          level: 3,
          desc: "Injecting manufacturing dimensions and product specifications (GD&T) directly into 3D solid profiles.",
          why: "Eliminates the need for tedious 2D drawing sheets by using rich digital metadata.",
          pitfall: "Do not skip datum references in GD&T tolerances. Coordinate tolerance ranges must be tied to physical datum frames.",
          wiki: "./kb/concepts/model-based-definition-solidworks",
          tutorials: "./tutorials?q=mbd"
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
          pitfall: "Do not build surfaces using too many dense points without filtering. Unfiltered raw files cause massive file lag.",
          wiki: "./kb/concepts/surfaces-civil-3d",
          tutorials: "./tutorials?q=surfaces"
        },
        {
          id: "civil3d",
          title: "Civil 3D",
          difficulty: "Intermediate",
          level: 2,
          desc: "Autodesk's land development platform built on top of the AutoCAD drafting engine.",
          why: "The primary tool for civil drawings, grading, and road network designs.",
          pitfall: "Avoid working in un-projected drawing spaces. Always establish a coordinate projection zone before drawing.",
          wiki: "./kb/software/civil-3d",
          tutorials: "./tutorials?q=civil"
        },
        {
          id: "alignments",
          title: "Alignments & Profiles",
          difficulty: "Intermediate",
          level: 2,
          desc: "Horizontal road centerlines (alignments) paired with vertical elevation grids (profiles).",
          why: "Defines the 3D pathway coordinates for highways, pipelines, and rail tracks.",
          pitfall: "Do not edit horizontal alignments manually by moving vertex points without checking curve design speed rules.",
          wiki: "./kb/concepts/profiles-civil-3d",
          tutorials: "./tutorials?q=profile"
        },
        {
          id: "corridors",
          title: "Corridor Modeling",
          difficulty: "Pro",
          level: 3,
          desc: "Sweeping road cross-sections (assemblies) along a 3D alignment and profile path.",
          why: "Creates rich 3D road models with dynamic shoulders, daylight grading, and cut limits.",
          pitfall: "Never build corridor surfaces without boundary settings. Unbounded surfaces will cross corridor limit lines.",
          wiki: "./kb/concepts/subassembly-civil-3d",
          tutorials: "./tutorials?q=corridor"
        },
        {
          id: "landxml",
          title: "LandXML Exchange",
          difficulty: "Pro",
          level: 3,
          desc: "Open standard file format transferring surfaces, alignments, and parcels to survey equipment.",
          why: "Essential for site deployment. Connects designer offices directly to GPS grading hardware.",
          pitfall: "Ensure coordinate unit projection settings are correct before exporting LandXML; wrong units shift site coordinates.",
          wiki: "./kb/concepts/pressure-networks-civil-3d",
          tutorials: "./tutorials?q=xml"
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
          pitfall: "Avoid drawing elements directly on Layer 0. Layer 0 should only be used to create blocks.",
          wiki: "./kb/concepts/layer",
          tutorials: "./tutorials?q=layer"
        },
        {
          id: "xref",
          title: "Xrefs & Blocks",
          difficulty: "Intermediate",
          level: 2,
          desc: "Linking external DWG files (Xrefs) and grouping recurring items as block references.",
          why: "Crucial for team drafting. Keeps parent files lightweight by referencing background plates.",
          pitfall: "Avoid using absolute paths for Xrefs. Absolute paths break reference links when files move between servers.",
          wiki: "./kb/concepts/xref",
          tutorials: "./tutorials?q=xref"
        },
        {
          id: "alias",
          title: "Command Aliases",
          difficulty: "Intermediate",
          level: 2,
          desc: "Keyboard shortcuts mapping fast inputs (L for LINE, CO for COPY) into the CAD console.",
          why: "Draftsman speed enhancer. Minimizes reliance on mouse clicks, boosting efficiency.",
          pitfall: "Do not map too many custom command aliases. It makes collaborating on other work PCs extremely difficult.",
          wiki: "./kb/concepts/command-alias",
          tutorials: "./tutorials?q=alias"
        },
        {
          id: "plot",
          title: "Plot & Layout Setup",
          difficulty: "Pro",
          level: 3,
          desc: "Configuring paperspace layouts, viewports, annotation scaling, and CTB plot styles.",
          why: "Guarantees drawings print accurately to scale without overlapping lines.",
          pitfall: "Never override object line thicknesses manually in layout space; always control them via CTB styles.",
          wiki: "./kb/concepts/plot-style",
          tutorials: "./tutorials?q=plot"
        },
        {
          id: "merge",
          title: "Drawing Merge & Compare",
          difficulty: "Pro",
          level: 3,
          desc: "Auditing revision changes and merging changes from external coordinates cleanly.",
          why: "Crucial for coordination. Ensures concurrent edits merge without database corruption.",
          pitfall: "Avoid merging drawings with different base units or scale factors, which corrupts coordinate database scales.",
          wiki: "./kb/concepts/drawing-merge",
          tutorials: "./tutorials?q=compare"
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
  const ROADMAP_DATA = window.ROADMAP_DATA;

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

  const inspectBackdrop = document.getElementById("inspect-backdrop");
  const btnInspectClose = document.getElementById("btn-inspect-close");
  const inspectPitfall = document.getElementById("inspect-pitfall");

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
      const nodeSlug = node.wiki ? node.wiki.split("/").pop().replace("", "") : "";
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
    closeInspectorPanel();

    // Set quiz button link dynamically
    const quizBtn = document.getElementById("btn-inspect-quiz");
    if (quizBtn) {
      quizBtn.href = `./quiz?track=${activeTrack}`;
    }

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

    if (inspectPitfall) {
      if (node.pitfall) {
        inspectPitfall.innerHTML = `<strong>Common Pitfall:</strong> ${node.pitfall}`;
        inspectPitfall.style.display = "block";
      } else {
        inspectPitfall.style.display = "none";
      }
    }

    btnWiki.href = node.wiki;
    btnWiki.style.display = "inline-flex";

    btnTuts.href = node.tutorials;
    btnTuts.style.display = "inline-flex";

    const quizBtn = document.getElementById("btn-inspect-quiz");
    if (quizBtn) {
      const idx = ROADMAP_DATA[activeTrack].nodes.findIndex(n => n.id === node.id);
      let lessonId = 1;
      if (idx === 0) lessonId = 1;
      else if (idx === 1 || idx === 2) lessonId = 2;
      else if (idx === 3 || idx === 4) lessonId = 3;
      quizBtn.href = `./quiz?track=${activeTrack}&lesson=${lessonId}`;
    }

    // Open Drawer
    const panel = document.getElementById("skill-inspector-panel");
    if (panel) panel.classList.add("open");
    if (inspectBackdrop) inspectBackdrop.classList.add("open");
  }

  function closeInspectorPanel() {
    const panel = document.getElementById("skill-inspector-panel");
    if (panel) panel.classList.remove("open");
    if (inspectBackdrop) inspectBackdrop.classList.remove("open");
    document.querySelectorAll(".skill-node").forEach(n => n.classList.remove("selected"));
  }

  // Hook close buttons
  if (btnInspectClose) {
    btnInspectClose.addEventListener("click", closeInspectorPanel);
  }
  if (inspectBackdrop) {
    inspectBackdrop.addEventListener("click", closeInspectorPanel);
  }

  function toggleMastery(nodeId, cardEl) {
    const masteredList = masteredProgress[activeTrack];
    const index = masteredList.indexOf(nodeId);
    const nodeObj = ROADMAP_DATA[activeTrack].nodes.find(n => n.id === nodeId);
    const nodeSlug = nodeObj && nodeObj.wiki ? nodeObj.wiki.split("/").pop().replace("", "") : "";
    
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
    if (inspectPitfall) inspectPitfall.style.display = "none";
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
      
      const quizBtn = document.getElementById("btn-inspect-quiz");
      if (quizBtn) {
        quizBtn.href = `./quiz?track=${activeTrack}`;
      }
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
          const slug = node.wiki.split("/").pop().replace("", "");
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
        if (container.getAttribute("data-answered") === "true") return;
        container.setAttribute("data-answered", "true");

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
              feedbackTitle.textContent = "✓ Correct! +10 XP";
              feedbackTitle.style.color = "#10b981";
            } else {
              feedbackTitle.textContent = "✕ Incorrect. Try studying the concept again!";
              feedbackTitle.style.color = "#ef4444";
            }
          }
        }

        if (isCorrect) {
          // 1. Save concept mastery to localStorage if new
          if (!masteredConcepts.includes(termSlug)) {
            masteredConcepts.push(termSlug);
            try {
              localStorage.setItem("gstarcademy_concept_mastery", JSON.stringify(masteredConcepts));
            } catch (e) {}
          }

          // 2. Add 10 XP
          let currentTotalXp = 0;
          try {
            currentTotalXp = parseInt(localStorage.getItem("gstarcademy_total_xp"), 10) || 0;
          } catch (e) {}
          currentTotalXp += 10;
          try {
            localStorage.setItem("gstarcademy_total_xp", String(currentTotalXp));
          } catch (e) {}

          // 3. Sync and light up Roadmap Nodes
          if (window.ROADMAP_DATA) {
            let matchedNodeId = null;
            let matchedTrackKey = null;
            for (const trackKey in window.ROADMAP_DATA) {
              const node = window.ROADMAP_DATA[trackKey].nodes.find(n => n.wiki && n.wiki.includes(termSlug));
              if (node) {
                matchedNodeId = node.id;
                matchedTrackKey = trackKey;
                break;
              }
            }
            if (matchedNodeId && matchedTrackKey) {
              let masteredProgress = { bim: [], mcad: [], civil: [], draft: [] };
              try {
                masteredProgress = JSON.parse(localStorage.getItem("gstarcademy_roadmap_progress")) || {
                  bim: [], mcad: [], civil: [], draft: []
                };
              } catch (e) {}
              // Ensure safety
              ["bim", "mcad", "civil", "draft"].forEach(t => {
                if (!masteredProgress[t]) masteredProgress[t] = [];
              });
              if (!masteredProgress[matchedTrackKey].includes(matchedNodeId)) {
                masteredProgress[matchedTrackKey].push(matchedNodeId);
                try {
                  localStorage.setItem("gstarcademy_roadmap_progress", JSON.stringify(masteredProgress));
                } catch (e) {}
              }
            }
          }

          // 4. Remove from mistake book if present
          let mistakes = [];
          try {
            mistakes = JSON.parse(localStorage.getItem("gstarcademy_mistakes")) || [];
          } catch (e) {}
          if (mistakes.includes(termSlug)) {
            mistakes = mistakes.filter(s => s !== termSlug);
            try {
              localStorage.setItem("gstarcademy_mistakes", JSON.stringify(mistakes));
            } catch (e) {}
          }

          // 5. Highlight parent card and trigger float XP animation
          container.style.borderColor = "#10b981";
          container.style.boxShadow = "0 8px 24px -4px rgba(16, 185, 129, 0.12)";

          const floatXp = document.createElement("div");
          floatXp.className = "float-xp-indicator";
          floatXp.textContent = "+10 XP 🎉";
          floatXp.style.cssText = `
            position: absolute;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: #fff;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 800;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
            pointer-events: none;
            z-index: 10;
            animation: floatUpFade 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
          `;
          container.style.position = "relative";
          container.appendChild(floatXp);
          setTimeout(() => floatXp.remove(), 1200);

        } else {
          // Save as mistake in local mistakes book
          let mistakes = [];
          try {
            mistakes = JSON.parse(localStorage.getItem("gstarcademy_mistakes")) || [];
          } catch (e) {}
          if (!mistakes.includes(termSlug)) {
            mistakes.push(termSlug);
            try {
              localStorage.setItem("gstarcademy_mistakes", JSON.stringify(mistakes));
            } catch (e) {}
          }
          
          container.style.borderColor = "#ef4444";
          container.style.boxShadow = "0 8px 24px -4px rgba(239, 68, 68, 0.12)";
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



