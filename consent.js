/*
 * Cookie consent banner + Google Consent Mode v2 bridge.
 *
 * Kept separate from app.js on purpose: app.min.js also carries the contact
 * form logic and must not be rebuilt for consent changes.
 *
 * The regional default (denied in EEA/UK/CH, granted elsewhere) and the
 * restore of a saved choice are set inline in each page's <head> before
 * gtag('config'). This file only renders the banner and records choices.
 */
(function () {
  "use strict";
  var PREFS_KEY = "learncad-cookie-prefs-v2";
  var SESSION_KEY = "learncad-cookie-banner-dismissed";
  var GA_ID = "G-ZV3YR72933";

  function getPrefs() {
    try { return JSON.parse(localStorage.getItem(PREFS_KEY) || "null"); } catch (e) { return null; }
  }
  function savePrefs(p) {
    try { localStorage.setItem(PREFS_KEY, JSON.stringify(p)); } catch (e) { /* ignore */ }
  }
  function applyPrefs(p) {
    if (!p) return;
    if (typeof window.gtag === "function") {
      window.gtag("consent", "update", { analytics_storage: p.analytics ? "granted" : "denied" });
    }
    window["ga-disable-" + GA_ID] = !p.analytics;
  }

  var existing = getPrefs();
  if (existing) { applyPrefs(existing); return; }
  try { if (sessionStorage.getItem(SESSION_KEY) === "1") return; } catch (e) { /* ignore */ }

  function init() {
    // data-consent-banner (not data-cookie-banner) so the legacy handler in app.min.js stays inert.
    var b = document.createElement("div");
    b.className = "cookie-consent";
    b.setAttribute("data-consent-banner", "");
    b.setAttribute("role", "dialog");
    b.setAttribute("aria-label", "Cookie consent");
    b.innerHTML =
      '<button type="button" class="cookie-consent-close" aria-label="Close">&times;</button>' +
      '<p class="cookie-consent-text">We use Google Analytics cookies to understand how this site is used. ' +
      'See our <a href="/privacy">Privacy Policy</a>.</p>' +
      '<div class="cookie-consent-actions">' +
      '<button type="button" class="btn-cookie-primary" data-consent="accept">Accept</button>' +
      '<button type="button" class="btn-cookie-outline" data-consent="reject">Reject</button>' +
      "</div>";
    document.body.appendChild(b);

    function close() {
      b.classList.remove("is-visible");
      b.classList.add("is-dismissed");
    }
    b.addEventListener("click", function (e) {
      var t = e.target;
      if (!t || !t.closest) return;
      if (t.closest('[data-consent="accept"]')) {
        var a = { analytics: true, functional: true };
        savePrefs(a); applyPrefs(a); close();
      } else if (t.closest('[data-consent="reject"]')) {
        var r = { analytics: false, functional: false };
        savePrefs(r); applyPrefs(r); close();
      } else if (t.closest(".cookie-consent-close")) {
        // Closing is not a choice: hide for this session, keep the regional default.
        try { sessionStorage.setItem(SESSION_KEY, "1"); } catch (err) { /* ignore */ }
        close();
      }
    });
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { b.classList.add("is-visible"); });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
