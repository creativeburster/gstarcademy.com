#!/usr/bin/env python3
"""
Final batch of pages to push past 1000 total.
Generates additional comparison pairs and niche topic pages.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import date
from scripts.generate_comparison_pages import SW_MAP, generate_comparison_page

TODAY = date.today().isoformat()
COMPARE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'compare')
CONCEPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'concepts')

# More comparison pairs to generate
FINAL_PAIRS = [
    ("gstarcad", "zwcad"), ("gstarcad", "ares-commander"), ("gstarcad", "freecad"),
    ("zwcad", "ares-commander"), ("zwcad", "draftsight"), ("zwcad", "freecad"),
    ("bricscad", "draftsight"), ("bricscad", "zwcad"), ("bricscad", "freecad"),
    ("autocad", "archicad"), ("autocad", "catia"), ("autocad", "inventor"),
    ("autocad", "siemens-nx"), ("autocad", "3dsmax"),
    ("revit", "civil-3d"), ("revit", "inventor"), ("revit", "fusion-360"),
    ("solidworks", "3dsmax"), ("solidworks", "blender"), ("solidworks", "sketchup"),
    ("catia", "fusion-360"), ("catia", "onshape"),
    ("siemens-nx", "catia"), ("siemens-nx", "inventor"), ("siemens-nx", "fusion-360"),
    ("inventor", "creo-parametric"), ("inventor", "catia"),
    ("onshape", "freecad"), ("onshape", "bricscad"), ("onshape", "inventor"),
    ("fusion-360", "catia"), ("fusion-360", "creo-parametric"),
    ("fusion-360", "solid-edge"), ("fusion-360", "sketchup"),
    ("blender", "rhinoceros"), ("blender", "fusion-360"),
    ("rhinoceros", "fusion-360"), ("rhinoceros", "catia"),
    ("sketchup", "rhinoceros"), ("sketchup", "archicad"),
    ("sketchup", "vectorworks"), ("sketchup", "freecad"),
    ("3dsmax", "blender"), ("3dsmax", "rhinoceros"), ("3dsmax", "sketchup"),
    ("civil-3d", "revit"), ("civil-3d", "archicad"),
    ("microstation", "revit"), ("microstation", "archicad"),
    ("freecad", "solidworks"), ("freecad", "inventor"),
    ("freecad", "sketchup"), ("freecad", "rhinoceros"),
    ("allplan", "revit"), ("allplan", "bricscad"),
    ("vectorworks", "sketchup"), ("vectorworks", "rhinoceros"),
    ("solid-edge", "inventor"), ("solid-edge", "creo-parametric"),
    ("solid-edge", "onshape"), ("solid-edge", "catia"),
    ("draftsight", "freecad"), ("draftsight", "gstarcad"),
    ("ares-commander", "autocad"), ("ares-commander", "gstarcad"),
    ("ansys-mechanical", "solidworks"), ("abaqus", "solidworks"),
    ("creo-parametric", "onshape"), ("creo-parametric", "freecad"),
]

existing = set(f.replace('.html','') for f in os.listdir(COMPARE_DIR))
generated_comp = 0

for a, b in FINAL_PAIRS:
    if a not in SW_MAP or b not in SW_MAP:
        continue
    slug1 = f"{a}-vs-{b}"
    slug2 = f"{b}-vs-{a}"
    if slug1 in existing or slug2 in existing:
        continue
    page_slug, html = generate_comparison_page(a, b)
    with open(os.path.join(COMPARE_DIR, f"{page_slug}.html"), 'w', encoding='utf-8') as f:
        f.write(html)
    existing.add(page_slug)
    generated_comp += 1

print(f"Generated {generated_comp} additional comparison pages")

# Additional niche concept pages
NICHE_CONCEPTS = [
    {"slug": "lidar-scanning-cad", "name": "LiDAR Scanning for CAD", "sw_slug": "civil-3d"},
    {"slug": "photogrammetry-cad", "name": "Photogrammetry to 3D Model", "sw_slug": "blender"},
    {"slug": "augmented-reality-construction", "name": "AR in Construction", "sw_slug": "revit"},
    {"slug": "robotic-fabrication", "name": "Robotic Fabrication & CAD", "sw_slug": "rhinoceros"},
    {"slug": "computational-design", "name": "Computational Design", "sw_slug": "rhinoceros"},
    {"slug": "mass-timber-design", "name": "Mass Timber Design in BIM", "sw_slug": "revit"},
    {"slug": "steel-connection-design", "name": "Steel Connection Design", "sw_slug": "revit"},
    {"slug": "precast-concrete-bim", "name": "Precast Concrete in BIM", "sw_slug": "revit"},
    {"slug": "electrical-cad-design", "name": "Electrical CAD (ECAD) Design", "sw_slug": "autocad"},
    {"slug": "pcb-mechanical-integration", "name": "PCB-Mechanical Integration", "sw_slug": "fusion-360"},
    {"slug": "cable-harness-design", "name": "Cable Harness Design", "sw_slug": "solidworks"},
    {"slug": "piping-design-3d", "name": "3D Piping Design", "sw_slug": "autocad"},
    {"slug": "hvac-ductwork-design", "name": "HVAC Ductwork Design", "sw_slug": "revit"},
    {"slug": "structural-steel-detailing", "name": "Structural Steel Detailing", "sw_slug": "revit"},
    {"slug": "rebar-detailing-bim", "name": "Rebar Detailing in BIM", "sw_slug": "revit"},
    {"slug": "earthwork-calculation", "name": "Earthwork Volume Calculation", "sw_slug": "civil-3d"},
    {"slug": "drainage-design", "name": "Drainage System Design", "sw_slug": "civil-3d"},
    {"slug": "traffic-engineering-cad", "name": "Traffic Engineering in CAD", "sw_slug": "civil-3d"},
    {"slug": "rail-design-cad", "name": "Railway Design in CAD", "sw_slug": "civil-3d"},
    {"slug": "port-marine-design", "name": "Port & Marine Design", "sw_slug": "microstation"},
    {"slug": "power-plant-design", "name": "Power Plant 3D Design", "sw_slug": "autocad"},
    {"slug": "process-plant-piping", "name": "Process Plant Piping Design", "sw_slug": "autocad"},
    {"slug": "offshore-platform-design", "name": "Offshore Platform Design", "sw_slug": "siemens-nx"},
    {"slug": "ship-hull-design", "name": "Ship Hull Design (Naval Architecture)", "sw_slug": "rhinoceros"},
    {"slug": "aircraft-structural-design", "name": "Aircraft Structural Design", "sw_slug": "catia"},
    {"slug": "turbomachinery-cad", "name": "Turbomachinery Design", "sw_slug": "siemens-nx"},
    {"slug": "gear-design-cad", "name": "Gear Design & Analysis", "sw_slug": "solidworks"},
    {"slug": "spring-design-cad", "name": "Spring Design in CAD", "sw_slug": "solidworks"},
    {"slug": "cam-mechanism-design", "name": "Cam Mechanism Design", "sw_slug": "solidworks"},
    {"slug": "linkage-mechanism-design", "name": "Linkage Mechanism Design", "sw_slug": "solidworks"},
    {"slug": "packaging-design-cad", "name": "Packaging Design in 3D", "sw_slug": "solidworks"},
    {"slug": "medical-device-cad", "name": "Medical Device Design in CAD", "sw_slug": "solidworks"},
    {"slug": "prosthetics-orthotic-cad", "name": "Prosthetics & Orthotics CAD", "sw_slug": "fusion-360"},
    {"slug": "dental-cad-cam", "name": "Dental CAD/CAM", "sw_slug": "fusion-360"},
    {"slug": "eyewear-design-cad", "name": "Eyewear/Optical Design", "sw_slug": "rhinoceros"},
    {"slug": "shoe-last-design", "name": "Shoe Last & Footwear Design", "sw_slug": "rhinoceros"},
    {"slug": "watch-design-cad", "name": "Watch & Micro-Mechanism Design", "sw_slug": "solidworks"},
    {"slug": "musical-instrument-cad", "name": "Musical Instrument Design", "sw_slug": "fusion-360"},
    {"slug": "bicycle-frame-design", "name": "Bicycle Frame Design", "sw_slug": "solidworks"},
    {"slug": "automotive-body-panel", "name": "Automotive Body Panel Design", "sw_slug": "catia"},
    {"slug": "ev-battery-pack-design", "name": "EV Battery Pack Design", "sw_slug": "solidworks"},
    {"slug": "solar-panel-mounting", "name": "Solar Panel Mounting Design", "sw_slug": "solidworks"},
    {"slug": "wind-turbine-blade", "name": "Wind Turbine Blade Design", "sw_slug": "catia"},
    {"slug": "heat-exchanger-design", "name": "Heat Exchanger Design", "sw_slug": "solidworks"},
    {"slug": "pressure-vessel-design", "name": "Pressure Vessel Design", "sw_slug": "solidworks"},
    {"slug": "conveyor-system-design", "name": "Conveyor System Design", "sw_slug": "solidworks"},
    {"slug": "elevator-design-cad", "name": "Elevator & Lift Design", "sw_slug": "revit"},
    {"slug": "escalator-design-bim", "name": "Escalator Design in BIM", "sw_slug": "revit"},
    {"slug": "facade-engineering", "name": "Facade Engineering in BIM", "sw_slug": "revit"},
    {"slug": "tensile-structure-design", "name": "Tensile & Membrane Structure Design", "sw_slug": "rhinoceros"},
    {"slug": "parametric-facade-design", "name": "Parametric Facade Design", "sw_slug": "rhinoceros"},
    {"slug": "landscape-grading-design", "name": "Landscape Grading Design", "sw_slug": "civil-3d"},
    {"slug": "retaining-wall-design", "name": "Retaining Wall Design", "sw_slug": "civil-3d"},
    {"slug": "roundabout-design", "name": "Roundabout Design", "sw_slug": "civil-3d"},
    {"slug": "parking-lot-design", "name": "Parking Lot Design", "sw_slug": "civil-3d"},
    {"slug": "airport-design-cad", "name": "Airport Design in CAD", "sw_slug": "civil-3d"},
    {"slug": "dam-design-cad", "name": "Dam Design in CAD/BIM", "sw_slug": "civil-3d"},
    {"slug": "water-treatment-design", "name": "Water Treatment Plant Design", "sw_slug": "autocad"},
    {"slug": "data-center-design", "name": "Data Center Design in BIM", "sw_slug": "revit"},
    {"slug": "hospital-design-bim", "name": "Hospital Design in BIM", "sw_slug": "revit"},
    {"slug": "stadium-design-bim", "name": "Stadium & Arena Design", "sw_slug": "revit"},
    {"slug": "high-rise-design-bim", "name": "High-Rise Building Design", "sw_slug": "revit"},
    {"slug": "heritage-conservation-bim", "name": "Heritage Conservation (HBIM)", "sw_slug": "revit"},
    {"slug": "modular-construction-bim", "name": "Modular Construction Design", "sw_slug": "revit"},
    {"slug": "net-zero-building-design", "name": "Net-Zero Building Design", "sw_slug": "revit"},
    {"slug": "smart-building-bim", "name": "Smart Building Systems in BIM", "sw_slug": "revit"},
    {"slug": "underground-space-design", "name": "Underground Space Design", "sw_slug": "revit"},
]

generated_niche = 0
for c in NICHE_CONCEPTS:
    filepath = os.path.join(CONCEPTS_DIR, f"{c['slug']}.html")
    if os.path.exists(filepath):
        continue
    
    canonical = f"https://gstarcademy.com/kb/concepts/{c['slug']}"
    html = f'''<!doctype html>
<html lang="en">
  <head>
    <link rel="preconnect" href="https://www.googletagmanager.com" />
    <link rel="dns-prefetch" href="https://www.googletagmanager.com" />
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}};window.gtag=gtag;window.addEventListener('load',function(){{const i=()=>{{const s=document.createElement('script');s.src='https://www.googletagmanager.com/gtag/js?id=G-ZV3YR72933';s.async=true;document.head.appendChild(s);gtag('js',new Date());gtag('config','G-ZV3YR72933');}};'requestIdleCallback' in window?requestIdleCallback(i):setTimeout(i,1);}});</script>
    <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{c['name']} | Gstarcademy</title>
    <meta name="description" content="Professional guide to {c['name'].lower()} — tools, workflows, software recommendations, and best practices for engineers and designers." />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <link rel="canonical" href="{canonical}" />
    <meta property="og:type" content="article" /><meta property="og:title" content="{c['name']}" /><meta property="og:url" content="{canonical}" /><meta property="og:site_name" content="Gstarcademy" />
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
    <link rel="preload" href="../../styles.min.css" as="style" />
    <link rel="preconnect" href="https://fonts.googleapis.com" /><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap" />
    <link rel="stylesheet" href="../../styles.min.css" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{c['name']}","url":"{canonical}","datePublished":"{TODAY}","dateModified":"{TODAY}","author":{{"@type":"Organization","name":"Gstarcademy Editorial Team"}},"publisher":{{"@type":"Organization","name":"Gstarcademy"}}}}</script>
  </head>
  <body>
    <div class="page-shell"><header class="topbar"><div class="container topbar-inner"><a class="brand" href="../../"><span class="brand-badge">GC</span><span>Gstarcademy</span></a><nav class="nav"><a class="nav-link" href="../../">Home</a><a class="nav-link active" href="../../knowledge-base">Wiki</a><a class="nav-link" href="../../tutorials">Tutorials</a><a class="nav-link" href="../../news">News</a><a class="nav-link" href="../../about">About</a></nav></div></header></div>
    <main class="container" style="margin-top: 32px; max-width: 920px;">
      <nav class="kb-faq-breadcrumbs" aria-label="Breadcrumb"><a href="../../">Home</a> / <a href="../../knowledge-base">Knowledge Base</a> / <a href="../../kb-terms">Terms</a> / <span aria-current="page">{c['name']}</span></nav>
      <article class="kb-concept-detail">
        <header class="kb-concept-header" style="margin-bottom: 28px;">
          <span class="chip pill-warn">Industry Application</span>
          <h1 style="margin-top: 12px;">{c['name']}</h1>
          <p class="hero-sub">Professional guide to {c['name'].lower()} — tools, workflows, software recommendations, and best practices for engineers and designers.</p>
        </header>
        <div class="ink-byline" role="contentinfo"><span><strong>By</strong> Gstarcademy Editorial Team</span><span><strong>Updated</strong> <time datetime="{TODAY}">{TODAY}</time></span></div>
        <section class="kb-concept-section">
          <h2>Overview</h2>
          <p>{c['name']} is a specialized domain within CAD/BIM engineering that requires both deep technical knowledge and specific software capabilities. This guide covers the fundamental workflows, key software tools, and industry best practices that professionals in this field need to master.</p>
          <p>The intersection of {c['name'].lower()} with modern parametric modeling, simulation, and digital fabrication technologies creates unique opportunities for engineers to optimize designs, reduce material waste, and accelerate project delivery timelines.</p>
          <p>Whether you are entering this specialization or expanding your existing practice, understanding the software ecosystem, industry standards, and collaboration workflows specific to {c['name'].lower()} will significantly improve your project outcomes and professional value.</p>
        </section>
        <section class="kb-concept-section">
          <h2>Key Considerations</h2>
          <ul>
            <li>Select software that supports the specific geometric and analytical requirements of this application domain</li>
            <li>Ensure compliance with relevant industry codes, standards, and certification requirements</li>
            <li>Develop templates, libraries, and standardized workflows early to maximize team productivity</li>
            <li>Integrate simulation and analysis tools to validate designs before physical fabrication or construction</li>
            <li>Maintain awareness of evolving regulatory requirements and technological advances in the field</li>
          </ul>
        </section>
        <section class="kb-concept-section">
          <h2>Recommended Software</h2>
          <p>Explore our <a href="../software/{c['sw_slug']}">detailed software profiles</a> and <a href="../compare/">comparison guides</a> to find the best tools for your {c['name'].lower()} projects.</p>
        </section>
        <aside style="margin-top: 32px; padding: 20px 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 14px;"><p style="font-size: 12px; font-weight: 600; margin: 0;">Gstarcademy Editorial Team &middot; <time datetime="{TODAY}">{TODAY}</time></p></aside>
      </article>
    </main>
    <footer class="footer site-footer"><div class="container site-footer-bottom"><p>&copy; Gstarcademy.</p></div></footer>
    <script src="../../app.min.js" defer></script>
  </body>
</html>'''
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    generated_niche += 1

print(f"Generated {generated_niche} niche concept pages")
print(f"Total new: {generated_comp + generated_niche}")
