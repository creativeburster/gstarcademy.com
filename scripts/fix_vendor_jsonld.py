"""Fix Organization JSON-LD url field in kb/vendors/*.html files.
The previous fix_vendor_pages.py script missed the JSON-LD url fix.
"""
from __future__ import annotations
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VENDORS_DIR = REPO / "kb" / "vendors"

VENDOR_URLS = {
    "autodesk": "https://www.autodesk.com/",
    "dassault-systemes": "https://www.3ds.com/",
    "dassault": "https://www.3ds.com/",
    "siemens": "https://www.siemens.com/",
    "gstarsoft": "https://www.gstarcad.net/",
    "zwsoft": "https://www.zwsoft.com/",
    "bentley": "https://www.bentley.com/",
    "ptc": "https://www.ptc.com/",
    "trimble": "https://www.trimble.com/",
    "graphisoft": "https://graphisoft.com/",
    "nemetschek": "https://www.nemetschek.com/",
    "hexagon": "https://hexagon.com/",
    "mcneel": "https://www.rhino3d.com/",
    "ironcad": "https://www.ironcad.com/",
    "alibre": "https://www.alibre.com/",
    "allplan": "https://www.allplan.com/",
    "altium-ltd": "https://www.altium.com/",
    "ansys": "https://www.ansys.com/",
    "aveva": "https://www.aveva.com/",
    "comsol-inc": "https://www.comsol.com/",
    "graebert": "https://www.graebert.com/",
    "vectorworks": "https://www.vectorworks.net/",
    "freecad-community": "https://www.freecad.org/",
    "community": "https://www.freecad.org/",
    "openfoam-foundation": "https://openfoam.org/",
}

VENDOR_DESCS = {
    "autodesk": "Autodesk — global CAD/BIM software leader behind AutoCAD, Revit, Inventor, Civil 3D, and Fusion 360; vendor profile, product portfolio, and ecosystem context.",
    "dassault-systemes": "Dassault Systèmes — maker of CATIA, SOLIDWORKS, and 3DEXPERIENCE platform; 3D design, simulation, and PLM leader for aerospace, automotive, and industrial sectors.",
    "dassault": "Dassault — maker of CATIA, SOLIDWORKS, and 3DEXPERIENCE platform; 3D design, simulation, and PLM leader for aerospace, automotive, and industrial sectors.",
    "siemens": "Siemens Digital Industries Software — developer of NX, Solid Edge, Teamcenter, and Simcenter; PLM, MCAD, and simulation solutions for discrete manufacturing.",
    "gstarsoft": "Gstarsoft — pioneer of independently developed CAD platform in China; 30+ years building 2D/3D DWG CAD and verticals across AEC, mechanical, electrical, mapping, and BIM.",
    "zwsoft": "ZWSOFT — Chinese CAD software developer behind ZWCAD and ZW3D; DWG-compatible 2D/3D CAD platform with perpetual licensing for AEC and mechanical markets.",
    "bentley": "Bentley Systems — infrastructure engineering software leader; MicroStation, OpenRoads, OpenBuildings, and SYNCHRO for civil, structural, and construction workflows.",
    "ptc": "PTC Inc. — developer of Creo, Windchill, and Onshape; MCAD, PLM, and IoT solutions for product design and manufacturing across discrete industries.",
    "trimble": "Trimble — positioning technology and construction software leader; Tekla Structures, SketchUp, and Trimble Civil solutions for AEC and geospatial workflows.",
    "graphisoft": "GRAPHISOFT — Nemetschek Group company and maker of Archicad; BIM software pioneer for architectural design, documentation, and collaboration workflows.",
    "nemetschek": "Nemetschek Group — parent of GRAPHISOFT, Vectorworks, Bluebeam, and Allplan; building design, BIM, and construction management software portfolio.",
    "hexagon": "Hexagon AB — measurement and design technology conglomerate; BricsCAD, Intergraph, and Hexagon Manufacturing Intelligence for CAD, surveying, and metrology.",
    "mcneel": "McNeel & Associates — developer of Rhinoceros 3D (Rhino); NURBS-based 3D modeling tool widely used in industrial design, architecture, and jewelry design.",
    "ironcad": "IronCAD LLC — 3D MCAD developer with drag-and-drop design methodology; IronCAD Design Collaboration Suite for mechanical engineering and manufacturing.",
    "alibre": "Alibre Inc. — affordable parametric 3D MCAD developer; Alibre Design for mechanical engineering, assembly modeling, and 2D drafting with perpetual licensing.",
    "allplan": "Allplan (Nemetschek) — BIM and CAD software for architecture, engineering, and construction; structural design, reinforced concrete detailing, and civil workflows.",
    "altium-ltd": "Altium Limited — EDA software developer; Altium Designer for PCB design, schematic capture, and electronic product development across hardware engineering.",
    "ansys": "ANSYS Inc. — engineering simulation software leader; Ansys Mechanical, Fluent, and Discovery for FEA, CFD, and multiphysics analysis across industries.",
    "aveva": "AVEVA Group (Schneider Electric) — industrial software for engineering, operations, and performance; plant design, process simulation, and asset management.",
    "comsol-inc": "COMSOL Inc. — multiphysics simulation software developer; COMSOL Multiphysics for FEA, CFD, electromagnetics, and coupled-physics modeling in research and industry.",
    "graebert": "Graebert GmbH — DWG CAD software developer; ARES Commander for 2D/3D drafting across desktop, cloud, and mobile platforms with DWG-native compatibility.",
    "vectorworks": "Vectorworks (Nemetschek) — 2D/3D design software for architecture, landscape, entertainment, and lighting design; BIM and CAD workflows for creative professionals.",
    "freecad-community": "FreeCAD Community — open-source parametric 3D CAD modeler; community-driven development for mechanical engineering, product design, and FEM analysis workflows.",
    "community": "Open-source CAD community — FreeCAD and Blender Foundation projects; community-driven development for mechanical engineering, product design, and 3D modeling.",
    "openfoam-foundation": "OpenFOAM Foundation — maintainer of OpenFOAM open-source CFD toolbox; computational fluid dynamics simulation for research, academia, and industrial engineering.",
}


def fix_org_jsonld(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    original = html
    slug = path.stem
    vendor_url = VENDOR_URLS.get(slug)
    vendor_desc = VENDOR_DESCS.get(slug)

    if not vendor_url:
        return False

    # Fix Organization JSON-LD: replace "url":"","description":"..." with proper values
    # Match the entire Organization script block
    def replace_org(m: re.Match) -> str:
        prefix = m.group(1)
        name = m.group(2)
        suffix = m.group(3)
        # Escape for JSON
        desc_escaped = vendor_desc.replace('"', '\\"')
        return f'{prefix}"name":"{name}","url":"{vendor_url}","description":"{desc_escaped}"{suffix}'

    html = re.sub(
        r'(<script\s+type="application/ld\+json">\{"@context":"https://schema\.org","@type":"Organization",)"name":"([^"]*)","url":"[^"]*","description":"[^"]*"(\}</script>)',
        replace_org,
        html,
    )

    # Also fix Article JSON-LD description if it's thin (just the vendor name)
    def replace_article_desc(m: re.Match) -> str:
        prefix = m.group(1)
        name = m.group(2)
        rest = m.group(3)
        desc_escaped = vendor_desc.replace('"', '\\"')
        return f'{prefix}"headline":"{name}","description":"{desc_escaped}","url":"{rest}'

    html = re.sub(
        r'(<script\s+type="application/ld\+json">\{"@context":"https://schema\.org","@type":"Article","headline":"[^"]*","description":")([^"]*)(","url":")',
        lambda m: m.group(1) + vendor_desc.replace('"', '\\"') + m.group(3),
        html,
    )

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> int:
    fixed = 0
    for path in sorted(VENDORS_DIR.glob("*.html")):
        if fix_org_jsonld(path):
            fixed += 1
            print(f"  fixed: {path.name}")
        else:
            print(f"  unchanged: {path.name}")
    print(f"Org JSON-LD fix: {fixed} fixed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
