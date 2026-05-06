/**
 * Knowledge base IA patch. Run: node scripts/patch_kb_ia.cjs
 */
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");

const NAV = {
  base: [true, false, false, false, false, false, false],
  cax: [false, true, false, false, false, false, false],
  terms: [false, false, true, false, false, false, false],
  graph: [false, false, false, true, false, false, false],
  software: [false, false, false, false, true, false, false],
  vendor: [false, false, false, false, false, true, false],
  domains: [false, false, false, false, false, false, true],
  none: [false, false, false, false, false, false, false],
};

function subnavHtml(active) {
  const hrefs = [
    ["./knowledge-base.html", "Overview"],
    ["./knowledge-cax.html", "CAx"],
    ["./kb-terms.html", "Terms"],
    ["./kb-graph.html", "Graph"],
    ["./kb-software.html", "Software"],
    ["./kb-vendors.html", "Vendor hubs"],
    ["./knowledge-domains.html", "Domains"],
  ];
  let s =
    '        <nav class="kb-subnav" aria-label="Knowledge base sections">\n';
  hrefs.forEach(([href, label], i) => {
    const cls =
      active[i] ? ' class="kb-subnav-link active"' : ' class="kb-subnav-link"';
    s += `          <a${cls} href="${href}">${label}</a>\n`;
  });
  s += "        </nav>\n";
  return s;
}

const sidebarInnerNew = `
            <div class="kb-index-box">
              <strong class="kb-index-title">Core Index</strong>
              <p class="meta kb-sidebar-taxonomy-note">
                Topics can overlap—like tag-like lenses and category-like buckets on the same idea.
              </p>
              <a class="kb-index-link" href="./knowledge-base.html">Overview</a>
              <a class="kb-index-link" href="./knowledge-cax.html">CAD / CAE / CAM</a>
              <a class="kb-index-link" href="./paths.html">Learning tracks</a>
              <a class="kb-index-link" href="./kb-terms.html#kb-term-jump">Terms <span>40+</span></a>
              <a class="kb-index-link" href="./knowledge-domains.html">Domain tracks</a>
              <a class="kb-index-link" href="./kb-graph.html">Knowledge graph</a>
              <a class="kb-index-link" href="./kb-software.html">Software map</a>
              <a class="kb-index-link" href="./kb-vendors.html">Vendor docs</a>
            </div>

            <div class="kb-nav-group">
              <button class="kb-nav-toggle" aria-expanded="true">Maps &amp; lanes</button>
              <div class="kb-nav-links">
                <a class="kb-side-link" href="./knowledge-cax.html">CAD · CAE · CAM</a>
                <a class="kb-side-link" href="./paths.html">Learning paths · tracks</a>
                <a class="kb-side-link" href="./kb-graph.html">Knowledge graph</a>
              </div>
            </div>
            <div class="kb-nav-group">
              <button class="kb-nav-toggle" aria-expanded="true">Topics</button>
              <div class="kb-nav-links">
                <a class="kb-side-link" href="./kb-terms.html#kb-term-jump">Terms</a>
                <a class="kb-side-link" href="./kb-software.html">Software map</a>
                <a class="kb-side-link" href="./kb-vendors.html">Vendor docs (official)</a>
                <a class="kb-side-link" href="./knowledge-domains.html">Domains &amp; industries</a>
              </div>
            </div>
            <div class="kb-nav-group">
              <button class="kb-nav-toggle" aria-expanded="false">Meta</button>
              <div class="kb-nav-links kb-collapsed">
                <a class="kb-side-link" href="./knowledge-base.html#kb-about">About this hub</a>
              </div>
            </div>
`;

const sidebarInnerVendor = `
        <div class="kb-index-box">
          <strong class="kb-index-title">Core Index</strong>
          <p class="meta kb-sidebar-taxonomy-note">
            Topics can overlap—like tag-like lenses and category-like buckets on the same idea.
          </p>
          <a class="kb-index-link" href="./knowledge-base.html">Overview</a>
          <a class="kb-index-link" href="./knowledge-cax.html">CAD / CAE / CAM</a>
          <a class="kb-index-link" href="./paths.html">Learning tracks</a>
          <a class="kb-index-link" href="./kb-terms.html#kb-term-jump">Terms <span>40+</span></a>
          <a class="kb-index-link" href="./knowledge-domains.html">Domain tracks</a>
          <a class="kb-index-link" href="./kb-graph.html">Knowledge graph</a>
          <a class="kb-index-link" href="./kb-software.html">Software map</a>
          <a class="kb-index-link" href="./kb-vendors.html">Vendor docs</a>
        </div>

        <div class="kb-nav-group">
          <button class="kb-nav-toggle" aria-expanded="true">Maps &amp; lanes</button>
          <div class="kb-nav-links">
            <a class="kb-side-link" href="./knowledge-cax.html">CAD · CAE · CAM</a>
            <a class="kb-side-link" href="./paths.html">Learning paths · tracks</a>
            <a class="kb-side-link" href="./kb-graph.html">Knowledge graph</a>
          </div>
        </div>
        <div class="kb-nav-group">
          <button class="kb-nav-toggle" aria-expanded="true">Topics</button>
          <div class="kb-nav-links">
            <a class="kb-side-link" href="./kb-terms.html#kb-term-jump">Terms</a>
            <a class="kb-side-link" href="./kb-software.html">Software map</a>
            <a class="kb-side-link" href="./kb-vendors.html">Vendor docs (official)</a>
            <a class="kb-side-link" href="./knowledge-domains.html">Domains &amp; industries</a>
          </div>
        </div>
        <div class="kb-nav-group">
          <button class="kb-nav-toggle" aria-expanded="false">Meta</button>
          <div class="kb-nav-links kb-collapsed">
            <a class="kb-side-link" href="./knowledge-base.html#kb-about">About this hub</a>
          </div>
        </div>
`;

function replaceSidebar(html, variant) {
  const inner = variant === "vendor" ? sidebarInnerVendor : sidebarInnerNew;
  const start = html.indexOf('<div class="kb-index-box">');
  if (start < 0) throw new Error("kb-index-box not found");
  const end = html.indexOf("</aside>", start);
  if (end < 0) throw new Error("</aside> not found");
  return html.slice(0, start) + inner.trim() + "\n      " + html.slice(end);
}

function replaceNav(html, key) {
  const active = NAV[key];
  return html.replace(
    /<nav class="kb-subnav" aria-label="Knowledge base sections">[\s\S]*?<\/nav>\r?\n/,
    subnavHtml(active)
  );
}

const pages = {
  "knowledge-base.html": { side: "standard", nav: "base" },
  "knowledge-cax.html": { side: "standard", nav: "cax" },
  "kb-terms.html": { side: "standard", nav: "terms" },
  "kb-graph.html": { side: "standard", nav: "graph" },
  "kb-software.html": { side: "standard", nav: "software" },
  "kb-vendors.html": { side: "vendor", nav: "vendor" },
  "knowledge-domains.html": { side: "standard", nav: "domains" },
  "knowledge-glossary.html": { side: "standard", nav: "terms" },
  "knowledge-curriculum.html": { side: "standard", nav: "none" },
  "knowledge-library.html": { side: "standard", nav: "none" },
  "knowledge-roadmap.html": { side: "standard", nav: "none" },
};

for (const [name, cfg] of Object.entries(pages)) {
  const fp = path.join(ROOT, name);
  let html = fs.readFileSync(fp, "utf8");
  if (name === "kb-vendors.html") {
    html = html.replace(
      'for="kb-sidebar-search-vendor"',
      'for="kb-sidebar-search"'
    );
    html = html.replace(
      'id="kb-sidebar-search-vendor"',
      'id="kb-sidebar-search"'
    );
  }
  html = replaceSidebar(html, cfg.side);
  html = replaceNav(html, cfg.nav);
  fs.writeFileSync(fp, html);
  console.log("patched", name);
}
