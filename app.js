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

  // Run initial parsing on load
  parseUrlParams();
})();

