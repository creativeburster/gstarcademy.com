const navLinks = document.querySelectorAll("[data-nav]");
const current = document.body.getAttribute("data-page");

navLinks.forEach((link) => {
  if (link.getAttribute("data-nav") === current) link.classList.add("active");
});

document.getElementById("footer-year")?.append(String(new Date().getFullYear()));

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
    banner.style.display = "none"; // 强制立即隐藏
    banner.classList.add("is-dismissed");
    try {
      localStorage.setItem(key, "1");
    } catch { /* ignore */ }
  };

  banner.querySelector(".cookie-consent-accept")?.addEventListener("click", handleAccept);
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
