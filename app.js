// Register PWA Service Worker
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    // Determine the root relative path for registering sw.js
    const isSubdir = window.location.pathname.includes("/kb/concepts/") || window.location.pathname.includes("/kb/software/") || window.location.pathname.includes("/kb/vendors/");
    const swPath = isSubdir ? "../../sw.js" : "./sw.js";
    
    navigator.serviceWorker
      .register(swPath)
      .then((reg) => {
        console.log("[PWA] ServiceWorker registered with scope: ", reg.scope);
        // Active check for updates
        reg.update().catch(() => {});
        if (reg.waiting) {
          reg.waiting.postMessage({ type: "SKIP_WAITING" });
        }
        reg.addEventListener("updatefound", () => {
          const newWorker = reg.installing;
          if (newWorker) {
            newWorker.addEventListener("statechange", () => {
              if (newWorker.state === "installed" && navigator.serviceWorker.controller) {
                newWorker.postMessage({ type: "SKIP_WAITING" });
              }
            });
          }
        });
      })
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
  const PREFS_KEY = "learncad-cookie-prefs-v2";
  const GA_ID = "G-ZV3YR72933";

  /* ── helpers ─────────────────────────────────────────── */
  function getPrefs() {
    try {
      const raw = localStorage.getItem(PREFS_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch { return null; }
  }
  function savePrefs(prefs) {
    try { localStorage.setItem(PREFS_KEY, JSON.stringify(prefs)); } catch { /* ignore */ }
  }
  function applyPrefs(prefs) {
    if (!prefs) return;
    if (!prefs.analytics) {
      window["ga-disable-" + GA_ID] = true;
    }
  }
  function dismiss() {
    banner.classList.remove("is-visible");
    banner.classList.add("is-dismissed");
    setTimeout(() => {
      banner.style.display = "none";
    }, 300);
  }

  /* ── check existing prefs ────────────────────────────── */
  const existing = getPrefs();
  if (existing) {
    applyPrefs(existing);
    banner.style.display = "none";
    return;
  }

  // Show banner smoothly without triggering document layout shift
  requestAnimationFrame(() => {
    banner.style.display = "block";
    requestAnimationFrame(() => {
      banner.classList.add("is-visible");
    });
  });

  /* ── button references ───────────────────────────────── */
  const btnAccept    = banner.querySelector('[data-action="accept"]') || Array.from(banner.querySelectorAll("button")).find(b => b.textContent.trim().toLowerCase() === "accept");
  const btnDeny      = banner.querySelector('[data-action="deny"]') || Array.from(banner.querySelectorAll("button")).find(b => b.textContent.trim().toLowerCase() === "deny");
  const btnCustomize = banner.querySelector('[data-action="customize"]') || Array.from(banner.querySelectorAll("button")).find(b => b.textContent.trim().toLowerCase() === "customize");

  /* ── Accept All ──────────────────────────────────────── */
  btnAccept?.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    const prefs = { analytics: true, functional: true };
    savePrefs(prefs);
    applyPrefs(prefs);
    dismiss();
  });

  /* ── Deny All ────────────────────────────────────────── */
  btnDeny?.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    const prefs = { analytics: false, functional: false };
    savePrefs(prefs);
    applyPrefs(prefs);
    dismiss();
  });

  /* ── Customize panel (dynamic) ───────────────────────── */
  let panel = null;

  function buildPanel() {
    panel = document.createElement("div");
    panel.className = "cookie-prefs-panel";
    panel.innerHTML =
      '<div class="cookie-pref-row">' +
        '<span class="cookie-pref-label">Analytics Cookies</span>' +
        '<label class="cookie-toggle">' +
          '<input type="checkbox" checked data-pref="analytics">' +
          '<span class="cookie-toggle-slider"></span>' +
        '</label>' +
      '</div>' +
      '<div class="cookie-pref-row">' +
        '<span class="cookie-pref-label">Functional Cookies</span>' +
        '<label class="cookie-toggle">' +
          '<input type="checkbox" checked data-pref="functional">' +
          '<span class="cookie-toggle-slider"></span>' +
        '</label>' +
      '</div>' +
      '<button type="button" class="btn-cookie-primary cookie-save-prefs">Save Preferences</button>';

    /* insert after .cookie-consent-actions */
    const inner = banner.querySelector(".cookie-consent-inner");
    if (inner) inner.appendChild(panel);

    /* Save button */
    panel.querySelector(".cookie-save-prefs")?.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      const prefs = {
        analytics:  panel.querySelector('[data-pref="analytics"]').checked,
        functional: panel.querySelector('[data-pref="functional"]').checked
      };
      savePrefs(prefs);
      applyPrefs(prefs);
      dismiss();
    });
  }

  btnCustomize?.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!panel) buildPanel();
    const isOpen = panel.classList.toggle("is-open");
    btnCustomize.classList.toggle("is-active", isOpen);
  });

  /* ── Close (×) = Deny ────────────────────────────────── */
  banner.querySelector(".cookie-consent-close")?.addEventListener("click", (e) => {
    e.preventDefault();
    const prefs = { analytics: false, functional: false };
    savePrefs(prefs);
    applyPrefs(prefs);
    dismiss();
  });
})();

(function initContactForm() {
  const form = document.getElementById("site-contact-form") || document.getElementById("contact-form");
  const status = document.getElementById("site-contact-form-status") || document.getElementById("contact-form-status");
  if (!form || !status || form.dataset.bound === "1") return;
  form.dataset.bound = "1";

  const submitBtn = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const nameInput = document.getElementById("contact-name");
    const emailInput = document.getElementById("contact-email");
    const topicInput = document.getElementById("contact-topic");
    const messageInput = document.getElementById("contact-message");

    const name = nameInput ? nameInput.value.trim() : "";
    const email = emailInput ? emailInput.value.trim() : "";
    const topic = topicInput ? topicInput.value : "general";
    const message = messageInput ? messageInput.value.trim() : "";

    if (!name || !email || !message) {
      status.hidden = false;
      status.style.color = "#dc2626";
      status.textContent = "Please fill in all required fields (Name, Email, and Message).";
      return;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = "Sending...";
    }
    status.hidden = false;
    status.style.color = "var(--ink-text-soft)";
    status.textContent = "Sending your message...";

    try {
      const response = await fetch("https://formsubmit.co/ajax/will@blog.dwgfastview.com", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({
          name: name,
          email: email,
          topic: topic,
          message: message,
          _subject: `[GstarCAD Academy Contact] New message from ${name} (${topic})`,
          _template: "table",
          _captcha: "false"
        })
      });

      const data = await response.json();
      if (response.ok && (data.success === "true" || data.success === true || data.message)) {
        status.hidden = false;
        status.style.color = "#16a34a";
        status.textContent = "✓ Thank you! Your message has been sent successfully. We will get back to you shortly.";
        form.reset();
      } else {
        throw new Error(data.message || "Failed to send message");
      }
    } catch (err) {
      console.error("[Contact Form Error]", err);
      status.hidden = false;
      status.style.color = "#dc2626";
      status.textContent = "Failed to send message online. Please email us directly at will@blog.dwgfastview.com.";
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = "Send Message";
      }
    }
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

      // Task filter (supports space-separated aliases)
      const taskList = (item.getAttribute("data-task") || "").split(/\s+/).filter(Boolean);
      const matchesTask =
        state.task === "all" || taskList.includes(state.task);

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

    // Check generic search query parameter ?q= or ?search=
    const query = params.get("q") || params.get("search");
    if (query) {
      const lowerQuery = query.toLowerCase();

      // Check if query directly maps to one of our official GstarCAD faculties
      let mappedSoftware = null;
      if (lowerQuery.includes("fastview") || lowerQuery.includes("dwgfastview") || lowerQuery.includes("mobile")) mappedSoftware = "fastview";
      else if (lowerQuery.includes("mechanical") || lowerQuery.includes("gcad-mech") || lowerQuery.includes("bom") || lowerQuery.includes("solidworks") || lowerQuery.includes("inventor") || lowerQuery.includes("catia") || lowerQuery.includes("creo")) mappedSoftware = "mechanical";
      else if (lowerQuery.includes("architecture") || lowerQuery.includes("gcad-arch") || lowerQuery.includes("revit") || lowerQuery.includes("bim") || lowerQuery.includes("archicad")) mappedSoftware = "architecture";
      else if (lowerQuery.includes("developer") || lowerQuery.includes("grx") || lowerQuery.includes("lisp") || lowerQuery.includes("sdk") || lowerQuery.includes("api")) mappedSoftware = "developers";
      else if (lowerQuery.includes("migration") || lowerQuery.includes("migrate") || lowerQuery.includes("autocad") || lowerQuery.includes("autodesk") || lowerQuery.includes("switch")) mappedSoftware = "migration";
      else if (lowerQuery.includes("gstarrender") || lowerQuery.includes("render")) mappedSoftware = "gstarrender";
      else if (lowerQuery.includes("gstarcad") || lowerQuery.includes("gstarsoft") || lowerQuery.includes("drafting")) mappedSoftware = "gstarcad";

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

// --- Phase 1 Wave 4: Zero-Login Study Passport, Auto-Scroll Replay & Bookmark Engine ---
(function initStudyPassportAndReplay() {
  const HISTORY_KEY = "gstarcademy_learning_history";
  const BOOKMARKS_KEY = "gstarcademy_bookmarks";
  const COMPLETED_KEY = "gstarcademy_completed_pages";
  const REPLAY_KEY = "gstarcademy_last_quiz_replay";

  function safeGetJson(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key)) || fallback; } catch (_) { return fallback; }
  }
  function safeSetJson(key, val) {
    try { localStorage.setItem(key, JSON.stringify(val)); } catch (_) {}
  }

  // 1. Check URL Hash/Query for Magic Resume Link (#resume=... or ?resume=...)
  function checkMagicResumeUrl() {
    let token = "";
    if (window.location.hash && window.location.hash.indexOf("#resume=") === 0) {
      token = window.location.hash.substring(8);
    } else {
      const params = new URLSearchParams(window.location.search);
      if (params.get("resume")) token = params.get("resume");
    }
    if (!token) return;
    try {
      const jsonStr = decodeURIComponent(escape(atob(token)));
      const parsed = JSON.parse(jsonStr);
      if (parsed && parsed.data) {
        const d = parsed.data;
        if (d.totalXp !== undefined) localStorage.setItem("gstarcademy_total_xp", String(d.totalXp));
        if (d.streak !== undefined) localStorage.setItem("gstarcademy_streak_v1", String(d.streak));
        if (d.lastDate !== undefined) localStorage.setItem("gstarcademy_last_quiz_completed_date", d.lastDate);
        if (d.roadmapProgress !== undefined) localStorage.setItem("gstarcademy_roadmap_progress", d.roadmapProgress);
        if (d.conceptMastery !== undefined) localStorage.setItem("gstarcademy_concept_mastery", d.conceptMastery);
        if (d.lessonsProgress !== undefined) localStorage.setItem("gstarcademy_lessons_progress", d.lessonsProgress);
        if (d.mistakes !== undefined) localStorage.setItem("gstarcademy_mistakes", d.mistakes);
        if (d.learningHistory !== undefined) localStorage.setItem(HISTORY_KEY, d.learningHistory);
        if (d.bookmarks !== undefined) localStorage.setItem(BOOKMARKS_KEY, d.bookmarks);
        if (d.completedPages !== undefined) localStorage.setItem(COMPLETED_KEY, d.completedPages);
        if (window.history && window.history.replaceState) {
          window.history.replaceState(null, "", window.location.pathname + window.location.search.replace(/[?&]resume=[^&]+/, ""));
        }
        setTimeout(() => {
          alert("🎉 Study Passport Restored! Your XP, course progress, bookmarks, and quiz mastery have been synchronized to this browser.");
          window.location.reload();
        }, 120);
      }
    } catch (e) {
      console.warn("Magic resume parse failed:", e);
    }
  }
  checkMagicResumeUrl();

  function buildFullPassportToken() {
    const payload = {
      version: 1,
      timestamp: Date.now(),
      data: {
        totalXp: parseInt(localStorage.getItem("gstarcademy_total_xp") || "0", 10),
        streak: parseInt(localStorage.getItem("gstarcademy_streak_v1") || "0", 10),
        lastDate: localStorage.getItem("gstarcademy_last_quiz_completed_date") || "",
        roadmapProgress: localStorage.getItem("gstarcademy_roadmap_progress") || "{}",
        conceptMastery: localStorage.getItem("gstarcademy_concept_mastery") || "[]",
        lessonsProgress: localStorage.getItem("gstarcademy_lessons_progress") || "{}",
        mistakes: localStorage.getItem("gstarcademy_mistakes") || "[]",
        learningHistory: localStorage.getItem(HISTORY_KEY) || "[]",
        bookmarks: localStorage.getItem(BOOKMARKS_KEY) || "[]",
        completedPages: localStorage.getItem(COMPLETED_KEY) || "[]"
      }
    };
    return btoa(unescape(encodeURIComponent(JSON.stringify(payload))));
  }

  // 2. Article Auto-Scroll Tracking, Resume Banner & Bookmark/Complete Toolbar
  const path = window.location.pathname.replace(/\.html$/, "");
  const isArticlePage = /^\/kb\/(guides|faq|concepts|software|vendors)\//.test(path);
  const articleEl = document.querySelector("main article");

  if (isArticlePage && articleEl) {
    const pageTitle = (document.querySelector("h1") ? document.querySelector("h1").textContent : document.title).trim();
    let history = safeGetJson(HISTORY_KEY, []);
    const prevEntry = history.find(h => h.path === path);

    // Inject Resume Banner if user previously scrolled >= 12% and < 95%
    if (prevEntry && prevEntry.pct >= 12 && prevEntry.pct < 95 && prevEntry.scrollY > 220) {
      const banner = document.createElement("div");
      banner.style.cssText = "margin-bottom:18px;padding:12px 18px;background:rgba(37,99,235,0.08);border:1px solid #2563eb;border-radius:10px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:13.5px;";
      const secLabel = prevEntry.section ? ` (“${prevEntry.section}”)` : "";
      banner.innerHTML = `<span>👋 <strong>Welcome back!</strong> You previously read <strong>${prevEntry.pct}%</strong> of this guide${secLabel}.</span>
        <div style="display:flex;gap:8px;">
          <button type="button" id="gs-resume-scroll-btn" style="background:#2563eb;color:#fff;border:none;padding:6px 12px;border-radius:6px;cursor:pointer;font-weight:600;font-size:12.5px;">▶ Resume Where I Left Off</button>
          <button type="button" id="gs-dismiss-resume-btn" style="background:transparent;color:var(--ink-text-soft);border:1px solid var(--ink-line);padding:6px 10px;border-radius:6px;cursor:pointer;font-size:12px;">Dismiss</button>
        </div>`;
      articleEl.insertBefore(banner, articleEl.firstChild);
      document.getElementById("gs-resume-scroll-btn").addEventListener("click", () => {
        window.scrollTo({ top: prevEntry.scrollY, behavior: "smooth" });
        banner.remove();
      });
      document.getElementById("gs-dismiss-resume-btn").addEventListener("click", () => banner.remove());
    }

    // Inject Action Bar (Bookmark, Mark Complete, Copy Magic Resume Link)
    const actionBar = document.createElement("div");
    actionBar.style.cssText = "display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:14px 0 22px;padding:10px 14px;background:var(--ink-surface-2,#f8fafc);border:1px solid var(--ink-line,#e2e8f0);border-radius:10px;font-size:13px;";
    const bookmarks = safeGetJson(BOOKMARKS_KEY, []);
    const completed = safeGetJson(COMPLETED_KEY, []);
    const isBookmarked = bookmarks.some(b => b.path === path);
    const isDone = completed.includes(path);

    actionBar.innerHTML = `
      <button type="button" id="gs-btn-bookmark" style="padding:6px 12px;border-radius:6px;border:1px solid var(--ink-line,#cbd5e1);background:var(--ink-surface,#fff);color:var(--ink-text);cursor:pointer;font-weight:600;">
        ${isBookmarked ? "⭐ Bookmarked" : "☆ Bookmark Guide"}
      </button>
      <button type="button" id="gs-btn-complete" style="padding:6px 12px;border-radius:6px;border:1px solid ${isDone ? "#16a34a" : "var(--ink-line,#cbd5e1)"};background:${isDone ? "rgba(22,163,74,0.12)" : "var(--ink-surface,#fff)"};color:${isDone ? "#15803d" : "var(--ink-text)"};cursor:pointer;font-weight:600;">
        ${isDone ? "✅ Completed" : "☐ Mark as Completed"}
      </button>
      <button type="button" id="gs-btn-magic-link" style="padding:6px 12px;border-radius:6px;border:1px solid var(--ink-line,#cbd5e1);background:var(--ink-surface,#fff);color:#2563eb;cursor:pointer;font-weight:600;margin-left:auto;">
        🔗 Copy Cross-Device Resume Link
      </button>
    `;
    const headerEl = articleEl.querySelector("header");
    if (headerEl && headerEl.nextSibling) {
      articleEl.insertBefore(actionBar, headerEl.nextSibling);
    } else {
      articleEl.insertBefore(actionBar, articleEl.firstChild);
    }

    document.getElementById("gs-btn-bookmark").addEventListener("click", function() {
      let bks = safeGetJson(BOOKMARKS_KEY, []);
      const idx = bks.findIndex(b => b.path === path);
      if (idx >= 0) {
        bks.splice(idx, 1);
        this.textContent = "☆ Bookmark Guide";
      } else {
        bks.unshift({ path, title: pageTitle, ts: Date.now() });
        this.textContent = "⭐ Bookmarked";
      }
      safeSetJson(BOOKMARKS_KEY, bks.slice(0, 50));
    });

    document.getElementById("gs-btn-complete").addEventListener("click", function() {
      let cmp = safeGetJson(COMPLETED_KEY, []);
      const idx = cmp.indexOf(path);
      if (idx >= 0) {
        cmp.splice(idx, 1);
        this.textContent = "☐ Mark as Completed";
        this.style.borderColor = "var(--ink-line,#cbd5e1)";
        this.style.background = "var(--ink-surface,#fff)";
        this.style.color = "var(--ink-text)";
      } else {
        cmp.push(path);
        this.textContent = "✅ Completed";
        this.style.borderColor = "#16a34a";
        this.style.background = "rgba(22,163,74,0.12)";
        this.style.color = "#15803d";
      }
      safeSetJson(COMPLETED_KEY, cmp);
    });

    document.getElementById("gs-btn-magic-link").addEventListener("click", function() {
      const url = window.location.origin + path + "#resume=" + buildFullPassportToken();
      if (navigator.clipboard) navigator.clipboard.writeText(url);
      this.textContent = "✓ Magic Resume Link Copied!";
      setTimeout(() => { this.textContent = "🔗 Copy Cross-Device Resume Link"; }, 3000);
    });

    // Throttled scroll progress recorder
    let scrollTimer = null;
    function recordScroll() {
      const docH = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
      const pct = Math.min(100, Math.max(5, Math.round((window.scrollY / docH) * 100)));
      let currentSec = "";
      const headings = articleEl.querySelectorAll("h2, h3");
      headings.forEach(h => {
        if (h.getBoundingClientRect().top <= 180) currentSec = h.textContent.trim().slice(0, 65);
      });
      let hist = safeGetJson(HISTORY_KEY, []).filter(h => h.path !== path);
      hist.unshift({ path, title: pageTitle, pct, scrollY: Math.round(window.scrollY), section: currentSec, ts: Date.now() });
      safeSetJson(HISTORY_KEY, hist.slice(0, 20));
    }
    recordScroll();
    window.addEventListener("scroll", () => {
      if (scrollTimer) return;
      scrollTimer = setTimeout(() => { scrollTimer = null; recordScroll(); }, 600);
    }, { passive: true });
  }

  // 3. Decorate Course Cards on tutorials.html / kb/guides/ with completion & progress badges
  const completedPaths = safeGetJson(COMPLETED_KEY, []);
  const histMap = {};
  safeGetJson(HISTORY_KEY, []).forEach(h => { histMap[h.path] = h; });
  document.querySelectorAll('a[href^="/kb/guides/"], a[href^="/kb/faq/"]').forEach(a => {
    const href = a.getAttribute("href").replace(/\.html$/, "");
    if (completedPaths.includes(href)) {
      const badge = document.createElement("span");
      badge.style.cssText = "display:inline-block;margin-left:6px;padding:2px 6px;font-size:10.5px;font-weight:700;background:#dcfce7;color:#15803d;border-radius:4px;";
      badge.textContent = "✅ Completed";
      a.prepend(badge);
    } else if (histMap[href] && histMap[href].pct >= 15) {
      const badge = document.createElement("span");
      badge.style.cssText = "display:inline-block;margin-left:6px;padding:2px 6px;font-size:10.5px;font-weight:700;background:#dbeafe;color:#1d4ed8;border-radius:4px;";
      badge.textContent = `⏳ ${histMap[href].pct}% Read`;
      a.prepend(badge);
    }
  });

  // 4. Global Topbar "📚 Progress" Drawer & Quiz Session Replay Modal
  const navEl = document.querySelector(".topbar .nav");
  if (navEl) {
    const progBtn = document.createElement("button");
    progBtn.type = "button";
    progBtn.className = "nav-link";
    progBtn.style.cssText = "background:none;border:1px solid var(--ink-line,#cbd5e1);border-radius:6px;padding:4px 10px;cursor:pointer;font-size:13px;font-weight:600;margin-left:4px;";
    const xp = parseInt(localStorage.getItem("gstarcademy_total_xp") || "0", 10);
    progBtn.innerHTML = `📚 Progress ${xp > 0 ? `<span style="color:#2563eb;">(${xp} XP)</span>` : ""}`;
    navEl.insertBefore(progBtn, navEl.lastElementChild);

    progBtn.addEventListener("click", openProgressDrawer);
  }

  function openProgressDrawer() {
    let existing = document.getElementById("gs-progress-modal");
    if (existing) existing.remove();

    const hist = safeGetJson(HISTORY_KEY, []);
    const bks = safeGetJson(BOOKMARKS_KEY, []);
    const cmp = safeGetJson(COMPLETED_KEY, []);
    const replay = safeGetJson(REPLAY_KEY, null);
    const xp = parseInt(localStorage.getItem("gstarcademy_total_xp") || "0", 10);
    const streak = parseInt(localStorage.getItem("gstarcademy_streak_v1") || "0", 10);

    const histHtml = hist.length ? hist.slice(0, 6).map(h => `
      <a href="${h.path}" style="display:flex;justify-content:space-between;align-items:center;padding:10px 12px;border:1px solid #e2e8f0;border-radius:8px;text-decoration:none;color:#0f172a;margin-bottom:8px;">
        <div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:75%;">
          <strong style="font-size:13px;">${h.title}</strong>
          ${h.section ? `<div style="font-size:11.5px;color:#64748b;">Last section: ${h.section}</div>` : ""}
        </div>
        <span style="font-size:12px;font-weight:700;color:#2563eb;white-space:nowrap;">▶ ${h.pct}%</span>
      </a>`).join("") : `<p style="font-size:13px;color:#64748b;">No recent guides yet. Open any course or guide to auto-save your reading position.</p>`;

    const bkHtml = bks.length ? bks.slice(0, 6).map(b => `
      <a href="${b.path}" style="display:block;padding:8px 12px;border:1px solid #e2e8f0;border-radius:8px;text-decoration:none;color:#0f172a;margin-bottom:6px;font-size:13px;font-weight:600;">⭐ ${b.title}</a>`).join("") : `<p style="font-size:13px;color:#64748b;">Click "☆ Bookmark Guide" on any article to pin it here.</p>`;

    const replayHtml = replay && Array.isArray(replay.questions) ? `
      <div style="margin-top:16px;padding:12px;background:#f8fafc;border:1px solid #cbd5e1;border-radius:10px;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <strong style="font-size:13.5px;">🎬 Last Quiz Session Replay (${replay.track.toUpperCase()}${replay.lessonId ? " L"+replay.lessonId : ""})</strong>
          <button type="button" id="gs-toggle-replay-btn" style="background:#2563eb;color:#fff;border:none;padding:4px 10px;border-radius:6px;font-size:12px;cursor:pointer;">View Q&A Replay</button>
        </div>
        <div id="gs-replay-details" style="display:none;margin-top:10px;max-height:220px;overflow-y:auto;font-size:12.5px;">
          ${replay.questions.map((q, i) => `
            <div style="padding:8px;border-bottom:1px solid #e2e8f0;">
              <div><strong>Q${i+1}:</strong> ${q.question}</div>
              <div style="color:#15803d;margin-top:3px;">✓ <strong>Answer:</strong> ${q.options[q.correctIdx]}</div>
              <div style="color:#475569;margin-top:2px;"><em>${q.why}</em></div>
            </div>`).join("")}
        </div>
      </div>` : "";

    const modal = document.createElement("div");
    modal.id = "gs-progress-modal";
    modal.style.cssText = "position:fixed;inset:0;background:rgba(15,23,42,0.55);z-index:9999;display:flex;justify-content:flex-end;";
    modal.innerHTML = `
      <div style="width:100%;max-width:460px;background:#fff;color:#0f172a;height:100%;overflow-y:auto;padding:24px;box-shadow:-8px 0 30px rgba(0,0,0,0.2);">
        <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e2e8f0;padding-bottom:14px;">
          <h3 style="margin:0;font-size:18px;">📚 Zero-Login Study Passport</h3>
          <button type="button" id="gs-close-modal" style="background:none;border:none;font-size:22px;cursor:pointer;color:#64748b;">×</button>
        </div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:16px 0;text-align:center;">
          <div style="padding:10px;background:#f1f5f9;border-radius:8px;"><div style="font-size:11px;color:#64748b;">TOTAL XP</div><strong style="font-size:16px;color:#2563eb;">${xp} XP</strong></div>
          <div style="padding:10px;background:#f1f5f9;border-radius:8px;"><div style="font-size:11px;color:#64748b;">STREAK</div><strong style="font-size:16px;color:#ea580c;">🔥 ${streak}d</strong></div>
          <div style="padding:10px;background:#f1f5f9;border-radius:8px;"><div style="font-size:11px;color:#64748b;">COMPLETED</div><strong style="font-size:16px;color:#16a34a;">✅ ${cmp.length}</strong></div>
        </div>
        <h4 style="margin:16px 0 8px;font-size:14px;">⏳ Continue Where You Left Off</h4>
        ${histHtml}
        ${replayHtml}
        <h4 style="margin:18px 0 8px;font-size:14px;">⭐ Saved Engineering Bookmarks (${bks.length})</h4>
        ${bkHtml}
        <div style="margin-top:20px;padding:14px;background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;">
          <h4 style="margin:0 0 6px;font-size:13.5px;color:#1e40af;">⚡ Cloudless Cross-Device Sync (No Login Required)</h4>
          <p style="margin:0 0 10px;font-size:12px;color:#3b82f6;line-height:1.5;">Save your Magic Resume Link as a browser bookmark or download your JSON Study Passport to continue on any PC or mobile device.</p>
          <div style="display:flex;gap:8px;flex-wrap:wrap;">
            <button type="button" id="gs-modal-copy-link" style="background:#2563eb;color:#fff;border:none;padding:7px 12px;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer;">🔗 Copy Magic Resume URL</button>
            <button type="button" id="gs-modal-dl-json" style="background:#fff;color:#0f172a;border:1px solid #cbd5e1;padding:7px 12px;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer;">💾 Download .JSON Passport</button>
          </div>
        </div>
      </div>`;
    document.body.appendChild(modal);

    document.getElementById("gs-close-modal").addEventListener("click", () => modal.remove());
    modal.addEventListener("click", e => { if (e.target === modal) modal.remove(); });
    const repBtn = document.getElementById("gs-toggle-replay-btn");
    if (repBtn) {
      repBtn.addEventListener("click", () => {
        const det = document.getElementById("gs-replay-details");
        det.style.display = det.style.display === "none" ? "block" : "none";
      });
    }
    document.getElementById("gs-modal-copy-link").addEventListener("click", function() {
      const url = window.location.origin + "/quiz#resume=" + buildFullPassportToken();
      if (navigator.clipboard) navigator.clipboard.writeText(url);
      this.textContent = "✓ Copied Magic URL!";
    });
    document.getElementById("gs-modal-dl-json").addEventListener("click", () => {
      const blob = new Blob([atob(buildFullPassportToken())], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "GstarCAD-Study-Passport.json";
      a.click();
    });
  }
})();
