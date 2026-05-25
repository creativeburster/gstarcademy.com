const navLinks = document.querySelectorAll("[data-nav]");
const current = document.body.getAttribute("data-page");

navLinks.forEach((link) => {
  if (link.getAttribute("data-nav") === current) link.classList.add("active");
});

document.getElementById("footer-year")?.append(String(new Date().getFullYear()));

// Mobile hamburger menu functionality
const hamburger = document.querySelector(".hamburger");
const nav = document.querySelector(".nav");
const navOverlay = document.querySelector(".nav-overlay");

function toggleMenu() {
  if (hamburger && nav) {
    hamburger.classList.toggle("active");
    nav.classList.toggle("active");
    if (navOverlay) {
      navOverlay.classList.toggle("active");
    }
    // Prevent scrolling when menu is open
    document.body.style.overflow = nav.classList.contains("active") ? "hidden" : "";
  }
}

if (hamburger) {
  hamburger.addEventListener("click", toggleMenu);
}

const navClose = document.querySelector(".nav-close");
if (navClose) {
  navClose.addEventListener("click", toggleMenu);
}

if (navOverlay) {
  navOverlay.addEventListener("click", toggleMenu);
}

// Close menu when a link is clicked
navLinks.forEach(link => {
  link.addEventListener("click", () => {
    if (nav && nav.classList.contains("active")) {
      toggleMenu();
    }
  });
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
