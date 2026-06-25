"""Fix kb/vendors/*.html pages:
1. Replace thin meta descriptions with proper 120-160 char descriptions
2. Fix empty Organization JSON-LD url field with vendor homepage URLs
3. Add robots meta tag (index, follow, max-image-preview:large) if missing
4. Switch styles.css to styles.min.css
"""

from __future__ import annotations
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VENDORS_DIR = REPO / "kb" / "vendors"

VENDOR_INFO = {
    "autodesk": {
        "url": "https://www.autodesk.com/",
        "desc": "Autodesk — global CAD/BIM software leader behind AutoCAD, Revit, Inventor, Civil 3D, and Fusion 360; vendor profile, product portfolio, and ecosystem context.",
    },
    "dassault-systemes": {
        "url": "https://www.3ds.com/",
        "desc": "Dassault Systèmes — maker of CATIA, SOLIDWORKS, and 3DEXPERIENCE platform; 3D design, simulation, and PLM leader for aerospace, automotive, and industrial sectors.",
    },
    "dassault": {
        "url": "https://www.3ds.com/",
        "desc": "Dassault — maker of CATIA, SOLIDWORKS, and 3DEXPERIENCE platform; 3D design, simulation, and PLM leader for aerospace, automotive, and industrial sectors.",
    },
    "siemens": {
        "url": "https://www.siemens.com/",
        "desc": "Siemens Digital Industries Software — developer of NX, Solid Edge, Teamcenter, and Simcenter; PLM, MCAD, and simulation solutions for discrete manufacturing.",
    },
    "gstarsoft": {
        "url": "https://www.gstarcad.net/",
        "desc": "Gstarsoft — pioneer of independently developed CAD platform in China; 30+ years building 2D/3D DWG CAD and verticals across AEC, mechanical, electrical, mapping, and BIM.",
    },
    "zwsoft": {
        "url": "https://www.zwsoft.com/",
        "desc": "ZWSOFT — Chinese CAD software developer behind ZWCAD and ZW3D; DWG-compatible 2D/3D CAD platform with perpetual licensing for AEC and mechanical markets.",
    },
    "bentley": {
        "url": "https://www.bentley.com/",
        "desc": "Bentley Systems — infrastructure engineering software leader; MicroStation, OpenRoads, OpenBuildings, and SYNCHRO for civil, structural, and construction workflows.",
    },
    "ptc": {
        "url": "https://www.ptc.com/",
        "desc": "PTC Inc. — developer of Creo, Windchill, and Onshape; MCAD, PLM, and IoT solutions for product design and manufacturing across discrete industries.",
    },
    "trimble": {
        "url": "https://www.trimble.com/",
        "desc": "Trimble — positioning technology and construction software leader; Tekla Structures, SketchUp, and Trimble Civil solutions for AEC and geospatial workflows.",
    },
    "graphisoft": {
        "url": "https://graphisoft.com/",
        "desc": "GRAPHISOFT — Nemetschek Group company and maker of Archicad; BIM software pioneer for architectural design, documentation, and collaboration workflows.",
    },
    "nemetschek": {
        "url": "https://www.nemetschek.com/",
        "desc": "Nemetschek Group — parent of GRAPHISOFT, Vectorworks, Bluebeam, and Allplan; building design, BIM, and construction management software portfolio.",
    },
    "hexagon": {
        "url": "https://hexagon.com/",
        "desc": "Hexagon AB — measurement and design technology conglomerate; BricsCAD, Intergraph, and Hexagon Manufacturing Intelligence for CAD, surveying, and metrology.",
    },
    "mcneel": {
        "url": "https://www.rhino3d.com/",
        "desc": "McNeel & Associates — developer of Rhinoceros 3D (Rhino); NURBS-based 3D modeling tool widely used in industrial design, architecture, and jewelry design.",
    },
    "ironcad": {
        "url": "https://www.ironcad.com/",
        "desc": "IronCAD LLC — 3D MCAD developer with drag-and-drop design methodology; IronCAD Design Collaboration Suite for mechanical engineering and manufacturing.",
    },
    "alibre": {
        "url": "https://www.alibre.com/",
        "desc": "Alibre Inc. — affordable parametric 3D MCAD developer; Alibre Design for mechanical engineering, assembly modeling, and 2D drafting with perpetual licensing.",
    },
    "allplan": {
        "url": "https://www.allplan.com/",
        "desc": "Allplan (Nemetschek) — BIM and CAD software for architecture, engineering, and construction; structural design, reinforced concrete detailing, and civil workflows.",
    },
    "altium-ltd": {
        "url": "https://www.altium.com/",
        "desc": "Altium Limited — EDA software developer; Altium Designer for PCB design, schematic capture, and electronic product development across hardware engineering.",
    },
    "ansys": {
        "url": "https://www.ansys.com/",
        "desc": "ANSYS Inc. — engineering simulation software leader; Ansys Mechanical, Fluent, and Discovery for FEA, CFD, and multiphysics analysis across industries.",
    },
    "aveva": {
        "url": "https://www.aveva.com/",
        "desc": "AVEVA Group (Schneider Electric) — industrial software for engineering, operations, and performance; plant design, process simulation, and asset management.",
    },
    "comsol-inc": {
        "url": "https://www.comsol.com/",
        "desc": "COMSOL Inc. — multiphysics simulation software developer; COMSOL Multiphysics for FEA, CFD, electromagnetics, and coupled-physics modeling in research and industry.",
    },
    "graebert": {
        "url": "https://www.graebert.com/",
        "desc": "Graebert GmbH — DWG CAD software developer; ARES Commander for 2D/3D drafting across desktop, cloud, and mobile platforms with DWG-native compatibility.",
    },
    "vectorworks": {
        "url": "https://www.vectorworks.net/",
        "desc": "Vectorworks (Nemetschek) — 2D/3D design software for architecture, landscape, entertainment, and lighting design; BIM and CAD workflows for creative professionals.",
    },
    "freecad-community": {
        "url": "https://www.freecad.org/",
        "desc": "FreeCAD Community — open-source parametric 3D CAD modeler; community-driven development for mechanical engineering, product design, and FEM analysis workflows.",
    },
    "community": {
        "url": "https://www.freecad.org/",
        "desc": "Open-source CAD community — FreeCAD and Blender Foundation projects; community-driven development for mechanical engineering, product design, and 3D modeling.",
    },
    "openfoam-foundation": {
        "url": "https://openfoam.org/",
        "desc": "OpenFOAM Foundation — maintainer of OpenFOAM open-source CFD toolbox; computational fluid dynamics simulation for research, academia, and industrial engineering.",
    },
}


def fix_vendor_file(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    original = html
    slug = path.stem
    info = VENDOR_INFO.get(slug)

    if not info:
        print(f"  WARNING: no vendor info for {slug}, skipping")
        return False

    new_desc = info["desc"]
    vendor_url = info["url"]

    # 1. Fix meta description
    html = re.sub(
        r'(<meta\s+name="description"\s+content=")([^"]*)("\s*/?>)',
        lambda m: m.group(1) + new_desc + m.group(3),
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    # Also fix og:description and twitter:description if they match the thin desc
    og_desc_match = re.search(
        r'<meta\s+property="og:description"\s+content="([^"]*)"',
        html, re.IGNORECASE,
    )
    if og_desc_match and len(og_desc_match.group(1)) < 50:
        html = re.sub(
            r'(<meta\s+property="og:description"\s+content=")([^"]*)("\s*/?>)',
            lambda m: m.group(1) + new_desc + m.group(3),
            html, count=1, flags=re.IGNORECASE,
        )
    tw_desc_match = re.search(
        r'<meta\s+name="twitter:description"\s+content="([^"]*)"',
        html, re.IGNORECASE,
    )
    if tw_desc_match and len(tw_desc_match.group(1)) < 50:
        html = re.sub(
            r'(<meta\s+name="twitter:description"\s+content=")([^"]*)("\s*/?>)',
            lambda m: m.group(1) + new_desc + m.group(3),
            html, count=1, flags=re.IGNORECASE,
        )

    # 2. Fix Organization JSON-LD url and description
    org_pattern = re.compile(
        r'(<script\s+type="application/ld\+json">\{"@context":"https://schema\.org","@type":"Organization","name":"[^"]*",)"url":"([^"]*)","description":"([^"]*)"(</script>)',
    )
    html = org_pattern.sub(
        lambda m: m.group(1) + f'"url":"{vendor_url}","description":"{new_desc}"' + m.group(4),
        html,
    )

    # 3. Add robots meta tag if missing (insert after canonical link)
    if 'name="robots"' not in html.lower():
        html = re.sub(
            r'(<link\s+rel="canonical"[^>]*>)',
            lambda m: m.group(1) + '\n    <meta name="robots" content="index, follow, max-image-preview:large" />',
            html,
            count=1,
            flags=re.IGNORECASE,
        )

    # 4. Switch styles.css to styles.min.css
    html = html.replace(
        '../../styles.css?v=v16_css_purge',
        '../../styles.min.css',
    )

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> int:
    fixed = 0
    for path in sorted(VENDORS_DIR.glob("*.html")):
        if fix_vendor_file(path):
            fixed += 1
            print(f"  fixed: {path.name}")
        else:
            print(f"  unchanged: {path.name}")
    print(f"Vendor page fix: {fixed} fixed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
