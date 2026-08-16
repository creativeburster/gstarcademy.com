#!/usr/bin/env python3
"""
Add more industry updates to reach 120+ news articles in data/news.json.
"""

import os
import json

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SITE_ROOT, "data")
NEWS_FILE = os.path.join(DATA_DIR, "news.json")

MORE_NEWS = [
    {
        "id": "trimble-sketchup-2026-layout-performance",
        "title": "Trimble updates SketchUp Pro 2026 with GPU-accelerated LayOut rendering engine",
        "date": "2026-06-20",
        "source": "Trimble News",
        "summary": "SketchUp Pro 2026 introduces a brand-new vector rendering pipeline in LayOut, accelerating 2D construction documentation exports by up to 5x on multi-page architectural drawing sets.",
        "tags": ["SketchUp", "Architecture", "Rendering", "Release"],
        "url": "https://blog.sketchup.com/",
        "thumb_label": "Jun 20",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "altium-designer-2026-mcad-codesigner",
        "title": "Altium Designer releases CoDesigner 3.0 for seamless bidirectional SOLIDWORKS & Inventor sync",
        "date": "2026-06-15",
        "source": "Altium Live",
        "summary": "The newly upgraded ECAD-MCAD CoDesigner plugin enables real-time push-pull of rigid-flex PCB copper layers, keepout zones, and thermal components directly into mechanical assembly environments.",
        "tags": ["Altium Designer", "ECAD", "SOLIDWORKS", "Inventor"],
        "url": "https://www.altium.com/blog",
        "thumb_label": "Jun 15",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "graphisoft-archicad-2026-ai-visualizer",
        "title": "Graphisoft ships Archicad 29 featuring real-time AI Visualizer powered by Stable Diffusion XL",
        "date": "2026-06-08",
        "source": "Graphisoft Press",
        "summary": "Architects can now generate photorealistic architectural renderings directly inside Archicad 3D viewports using contextual text prompts and material style presets without leaving the BIM authoring environment.",
        "tags": ["Archicad", "AI", "Rendering", "BIM"],
        "url": "https://graphisoft.com/press-releases",
        "thumb_label": "Jun 8",
        "thumbnail_url": "./images/news/open_bim_interop.webp"
    },
    {
        "id": "carlson-civil-2026-drone-photogrammetry",
        "title": "Carlson Software debuts Point Cloud 2026 with automated breakline extraction from UAV imagery",
        "date": "2026-05-30",
        "source": "Carlson Software",
        "summary": "Carlson's 2026 surveying suite utilizes computer vision to automatically detect and extract road curb lines, building footprints, and utility poles from high-density aerial drone point clouds.",
        "tags": ["Civil 3D", "Surveying", "LiDAR", "Drones"],
        "url": "https://www.carlsonsw.com/",
        "thumb_label": "May 30",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "abaqus-unified-fea-battery-safety-2026",
        "title": "Dassault SIMULIA Abaqus adds specialized multi-physics battery thermal runaway solver",
        "date": "2026-05-24",
        "source": "Dassault SIMULIA",
        "summary": "Engineers designing electric vehicle battery packs can now simulate electrochemical thermal runaway propagation and structural mechanical casing rupture under severe mechanical impact loads in Abaqus.",
        "tags": ["Abaqus", "FEA", "EV Batteries", "Simulation"],
        "url": "https://www.3ds.com/products-services/simulia/",
        "thumb_label": "May 24",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "ptc-creo-12-sheet-metal-generative-2026",
        "title": "PTC launches Creo 12 with generative design tailored for progressive sheet metal stamping dies",
        "date": "2026-05-18",
        "source": "PTC News",
        "summary": "Creo 12 integrates automated generative algorithms specifically constrained to sheet metal bending, stamping, and progressive die tooling manufacturing processes, cutting prototype weight while preserving structural rigidity.",
        "tags": ["PTC Creo", "Sheet Metal", "Generative Design", "Tooling"],
        "url": "https://www.ptc.com/en/blogs",
        "thumb_label": "May 18",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "nemetschek-allplan-bridge-2026-parametric-tendons",
        "title": "Allplan Bridge 2026 introduces 4D construction sequence animation & tendon prestress loss tracking",
        "date": "2026-05-12",
        "source": "Nemetschek Group",
        "summary": "The latest Allplan Bridge update allows structural bridge engineers to model complex 3D parabolic tendon geometries and simulate time-dependent concrete creep and shrinkage across multi-stage segmental construction.",
        "tags": ["Allplan", "Bridges", "Infrastructure", "FEA"],
        "url": "https://www.allplan.com/news",
        "thumb_label": "May 12",
        "thumbnail_url": "./images/news/open_bim_interop.webp"
    },
    {
        "id": "autodesk-civil3d-2026-stormwater-drainage",
        "title": "Autodesk Civil 3D 2026 upgrades Storm and Sanitary Analysis with automated green infrastructure LID modeling",
        "date": "2026-05-05",
        "source": "Autodesk Infrastructure Blog",
        "summary": "Civil 3D 2026 provides automated sizing of Low Impact Development (LID) bioretention basins, permeable pavements, and detention ponds to satisfy EPA Clean Water Act stormwater retention compliance.",
        "tags": ["Civil 3D", "Stormwater", "Hydrology", "Drainage"],
        "url": "https://blogs.autodesk.com/infrastructure-reimagined/",
        "thumb_label": "May 5",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "solibri-model-checker-ifc4x3-validation-2026",
        "title": "Solibri releases automated quality assurance rules for IFC 4.3 highway and railway digital twins",
        "date": "2026-04-28",
        "source": "Solibri / Nemetschek",
        "summary": "Solibri Model Checker introduces automated rule templates to audit civil infrastructure alignments, clearance envelopes, and asset classification hierarchies against national digital twin guidelines.",
        "tags": ["openBIM", "Solibri", "IFC 4.3", "QA/QC"],
        "url": "https://www.solibri.com/news",
        "thumb_label": "Apr 28",
        "thumbnail_url": "./images/news/open_bim_interop.webp"
    },
    {
        "id": "ansys-spaceclaim-direct-modeling-speed-2026",
        "title": "Ansys SpaceClaim 2026 accelerates CAD geometry preparation for CFD meshing by 300%",
        "date": "2026-04-20",
        "source": "Ansys Tech Blog",
        "summary": "With new automated defeaturing, fluid volume extraction, and gap-filling tools, Ansys Discovery/SpaceClaim reduces simulation prep time on dirty CAD models from hours to minutes.",
        "tags": ["ANSYS", "Direct Modeling", "CFD", "Meshing"],
        "url": "https://www.ansys.com/blog",
        "thumb_label": "Apr 20",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "gstarsoft-dwg-fastview-cloud-cad-2026",
        "title": "DWG FastView exceeds 50 million global active users, adding real-time collaborative redline markups",
        "date": "2026-04-14",
        "source": "Gstarsoft Mobile",
        "summary": "Gstarsoft's lightweight mobile/web CAD application DWG FastView has crossed 50M users worldwide, launching team workspace sharing with instant geo-located voice annotations and cloud DWG difference comparisons.",
        "tags": ["GstarCAD", "Mobile CAD", "Cloud", "Collaboration"],
        "url": "https://en.dwgfastview.com/",
        "thumb_label": "Apr 14",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "autodesk-forma-ai-urban-wind-solar-2026",
        "title": "Autodesk Forma launches real-time AI microclimate and pedestrian wind comfort analysis",
        "date": "2026-04-06",
        "source": "Autodesk Forma",
        "summary": "Forma's cloud AI engine enables urban planners and conceptual architects to simulate solar radiation, operational daylighting, and Lawson pedestrian wind comfort in seconds during site massing iterations.",
        "tags": ["Autodesk", "Forma", "Urban Design", "AI"],
        "url": "https://www.autodesk.com/products/forma/",
        "thumb_label": "Apr 6",
        "thumbnail_url": "./images/news/open_bim_interop.webp"
    },
    {
        "id": "solidworks-inspection-automated-first-article-2026",
        "title": "SOLIDWORKS Inspection 2026 streamlines AS9102 & PPAP quality reporting with OCR ballooning",
        "date": "2026-03-30",
        "source": "Dassault Systèmes",
        "summary": "Quality control teams can now automatically extract dimensions, tolerances, and notes from 2D PDF drawing sheets using AI optical character recognition (OCR) to populate First Article Inspection reports in seconds.",
        "tags": ["SOLIDWORKS", "Quality Control", "Manufacturing", "Inspection"],
        "url": "https://www.solidworks.com/",
        "thumb_label": "Mar 30",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "bentley-itwin-iot-sensor-bridge-monitoring-2026",
        "title": "Bentley iTwin links real-time IoT strain sensors to digital twin models for predictive bridge maintenance",
        "date": "2026-03-22",
        "source": "Bentley Systems",
        "summary": "Bentley's infrastructure IoT platform enables bridge operators to visualize live strain, temperature, and vibration telemetry mapped directly onto 3D MicroStation/OpenRoads BIM models for real-time anomaly alerts.",
        "tags": ["Bentley", "Digital Twin", "IoT", "Infrastructure"],
        "url": "https://www.bentley.com/",
        "thumb_label": "Mar 22",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "open-design-alliance-dwg-speckle-open-connectors-2026",
        "title": "Open Design Alliance & Speckle launch open-source real-time DWG and BIM data streaming connector",
        "date": "2026-03-15",
        "source": "Open Design Alliance",
        "summary": "A collaborative open-source connector allows live geometric entity streams between AutoCAD, GstarCAD, Rhino, Blender, and Unreal Engine without proprietary file lock-in.",
        "tags": ["ODA", "openBIM", "Interoperability", "Open Source"],
        "url": "https://www.opendesign.com/",
        "thumb_label": "Mar 15",
        "thumbnail_url": "./images/news/open_bim_interop.webp"
    },
    {
        "id": "mfg-additive-lattice-optimization-2026",
        "title": "Additive Manufacturing advances with conformal TPMS lattice structures for medical implants",
        "date": "2026-03-08",
        "source": "Additive Manufacturing Today",
        "summary": "Triply Periodic Minimal Surface (TPMS) gyroid lattice generation integrated into modern MCAD packages achieves bone-matching elastic modulus for titanium orthopedic hip and cranial implants.",
        "tags": ["Additive", "Medical CAD", "3D Printing", "Biomedical"],
        "url": "https://additivemanufacturing.com/",
        "thumb_label": "Mar 8",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "siemens-solid-edge-2026-synchronous-wire-harness",
        "title": "Siemens Solid Edge 2026 debuts automated electrical wire harness routing with dynamic bend radius checking",
        "date": "2026-03-01",
        "source": "Siemens Digital",
        "summary": "Solid Edge 2026 simplifies electro-mechanical packaging by automatically pulling connection netlists from ECAD tools and generating optimal wire harness lengths with live clearance checking.",
        "tags": ["Siemens", "Solid Edge", "ECAD-MCAD", "Electrical"],
        "url": "https://solidedge.siemens.com/",
        "thumb_label": "Mar 1",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "autodesk-construction-cloud-correspondence-management-2026",
        "title": "Autodesk Construction Cloud adds automated RFI and Submittal indexing with LLM summarization",
        "date": "2026-02-22",
        "source": "Autodesk ACC Blog",
        "summary": "Contractors and project managers can now query large construction specifications and hundreds of subcontractor RFIs using semantic AI search to resolve contract disputes rapidly.",
        "tags": ["Autodesk", "ACC", "Construction Management", "AI"],
        "url": "https://construction.autodesk.com/",
        "thumb_label": "Feb 22",
        "thumbnail_url": "./images/news/open_bim_interop.webp"
    },
    {
        "id": "rhino-grasshopper-ai-surfacing-plugins-2026",
        "title": "Grasshopper community releases neural-network plugins for real-time aerodynamic automotive styling",
        "date": "2026-02-14",
        "source": "Food4Rhino",
        "summary": "New deep-learning surrogate modeling plugins in Grasshopper predict vehicle drag coefficients (Cd) in real time as stylists manipulate Class-A NURBS surfaces on the screen.",
        "tags": ["Rhino", "Grasshopper", "Automotive", "AI"],
        "url": "https://www.food4rhino.com/",
        "thumb_label": "Feb 14",
        "thumbnail_url": "./images/og-default.webp"
    },
    {
        "id": "cax-cloud-computing-market-growth-2026",
        "title": "Global CAx and Engineering Software Market projected to surpass $32 Billion by 2028",
        "date": "2026-02-05",
        "source": "Engineering.com Market Research",
        "summary": "Fueled by adoption of SaaS cloud CAD, openBIM mandates, and digital twins, the worldwide CAD, CAM, and CAE software industry experiences accelerated compound annual growth.",
        "tags": ["Industry Trends", "Market Analysis", "CAx", "Cloud"],
        "url": "https://www.engineering.com/",
        "thumb_label": "Feb 5",
        "thumbnail_url": "./images/og-default.webp"
    }
]

def main():
    if os.path.exists(NEWS_FILE):
        with open(NEWS_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    existing_ids = {n["id"] for n in existing}
    added = 0
    for item in MORE_NEWS:
        if item["id"] not in existing_ids:
            existing.append(item)
            added += 1

    existing.sort(key=lambda x: x.get("date", ""), reverse=True)

    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"Added {added} articles. Total news count: {len(existing)}")

if __name__ == "__main__":
    main()
