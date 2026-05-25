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
