// CAD Learn Hub — PWA Service Worker (sw.js)
const CACHE_NAME = "gstarcademy-shell-v23";
const DYNAMIC_CACHE = "gstarcademy-content-v23";

// Core App Shell Assets (Pre-cached for instant loading and 100% offline baseline)
// Streamlined to essential core assets to avoid install aborts on large dynamic pages
const ASSETS_TO_PRECACHE = [
  "./",
  "./styles.min.css",
  "./app.min.js",
  "./search.min.js",
  "./favicon.svg",
  "./manifest.json",
  "./offline"
];

// Install Event: Fault-tolerant pre-cache static shell resources
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("[Service Worker v23] Pre-caching Core Shell...");
      return Promise.allSettled(
        ASSETS_TO_PRECACHE.map((url) =>
          fetch(url, { cache: "reload" })
            .then((res) => {
              if (res.ok) {
                return cache.put(url, res);
              }
            })
            .catch((err) => console.warn("[SW] Precache skipped for " + url, err))
        )
      );
    }).then(() => self.skipWaiting())
  );
});

// Activate Event: Clean up legacy caches
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME && key !== DYNAMIC_CACHE) {
            console.log("[Service Worker v23] Removing legacy cache: ", key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Listen for SKIP_WAITING message
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

// Fetch Event: Implement Cache-First for static shell, Stale-While-Revalidate for dynamic pages
self.addEventListener("fetch", (event) => {
  // Only intercept HTTP/S GET requests (ignore local file:/// and POST/PUT)
  if (event.request.method !== "GET" || !event.request.url.startsWith(self.location.origin)) {
    return;
  }

  const url = new URL(event.request.url);

  // Check if this request is a pre-cached shell asset
  const isPrecached = ASSETS_TO_PRECACHE.some(asset => {
    const cleanAsset = asset.replace(/^\.\//, "/");
    return url.pathname.endsWith(cleanAsset) || (cleanAsset === "/" && url.pathname === "/");
  });

  const isHtmlNavigation = event.request.mode === "navigate" || 
    (event.request.headers.get("accept") && event.request.headers.get("accept").includes("text/html"));

  if (isHtmlNavigation) {
    // Network-First for HTML navigation to ensure users always see freshest page updates
    event.respondWith(
      fetch(event.request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const copy = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(event.request).then((cached) => {
            return cached || caches.match("./offline") || caches.match("/offline");
          });
        })
    );
    return;
  }

  if (isPrecached) {
    // 1. Cache-First Strategy for static assets (css, js, images) to guarantee instantaneous loading
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          // Serve from cache, but update cache in background if network is active
          fetch(event.request).then((networkResponse) => {
            if (networkResponse.status === 200) {
              caches.open(CACHE_NAME).then((cache) => cache.put(event.request, networkResponse));
            }
          }).catch(() => {/* ignore background update fails */});
          return cachedResponse;
        }
        return fetch(event.request);
      })
    );
  } else {
    // 2. Stale-While-Revalidate Strategy for dynamic content pages (such as specific /kb/concepts/*.html)
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        const networkFetch = fetch(event.request).then((networkResponse) => {
          // If valid response, clone and save in dynamic cache
          if (networkResponse && networkResponse.status === 200) {
            return caches.open(DYNAMIC_CACHE).then((cache) => {
              cache.put(event.request, networkResponse.clone());
              return networkResponse;
            });
          }
          return networkResponse;
        }).catch((err) => {
          // If network fails and we are requesting an HTML page, serve offline.html
          if (event.request.headers.get("accept").includes("text/html")) {
            console.log("[Service Worker] Network down, serving offline fallback page.");
            return caches.match("./offline") || caches.match("/offline");
          }
          throw err;
        });

        return cachedResponse || networkFetch;
      })
    );
  }
});
