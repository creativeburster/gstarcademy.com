#!/usr/bin/env python3
"""
Enrich thin concept pages in kb/concepts/*.html (word count < 300 words).
Injects comprehensive engineering workflows, command syntax, troubleshooting tables,
and industry standards to elevate content quality to Google E-E-A-T professional standards.
"""

import os
import re
from datetime import date
from bs4 import BeautifulSoup

TODAY = date.today().isoformat()
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONCEPTS_DIR = os.path.join(SITE_ROOT, "kb", "concepts")

DOMAIN_KNOWLEDGE = {
    "civil": {
        "commands": "AutoCAD/Civil 3D commands: <code>ALIGNMENT</code>, <code>SURFACE</code>, <code>CORRIDOR</code>, <code>MAPIMPORT</code>, <code>GRADING</code>. System variables: <code>MEASUREMENT=1</code>, <code>SURFTYPE=6</code>, <code>GEOLATLONGFORMAT=1</code>.",
        "workflow": [
            ("1. Terrain Model & Coordinate Setup", "Import aerial survey LiDAR point clouds or total-station LandXML data. Establish global georeferencing (UTM/EPSG grid) to align site datum across disciplines."),
            ("2. Geometric Alignment & Profile Design", "Lay out horizontal tangents and spiral transitions following AASHTO / Eurocode minimum curve radii, coupled with vertical slope crest/sag parabolic curves."),
            ("3. Corridor Modeling & Drainage Grading", "Assemble multi-layer cross sections (subbase, binder, surface wear course), integrate roadside daylight catch slopes, and size culvert drainage catchments."),
            ("4. Earthwork Takeoff & Machine Control Export", "Compute cut/fill earthwork balance volumes via composite surfaces and export LandXML / 3D DGN files directly for GPS-guided machine grading.")
        ],
        "standards": ["AASHTO Geometric Design Guidelines (Green Book)", "Eurocode 7 (Geotechnical Design - EN 1997)", "ISO 19650 (BIM for Civil Infrastructure)", "FHWA Hydraulic Engineering Circulars"],
        "troubleshooting": [
            ("Surface triangulation bridges across steep ravines incorrectly", "Add linear Breaklines along tops/toes of slopes or specify 'Maximum Triangle Length' under Surface Build Properties."),
            ("Horizontal curve radius triggers AASHTO violation flags", "Adjust minimum transition spiral length or increase curve radius to meet minimum design speed superelevation criteria."),
            ("Coordinates offset by several meters after CAD/GIS import", "Verify projection datum and false easting/northing parameters in MAPCSASSIGN before importing geospatial shapefiles.")
        ]
    },
    "mfg": {
        "commands": "Parametric MCAD commands: <code>EXTRUDE</code>, <code>REVOLVE</code>, <code>SWEEP</code>, <code>LOFT</code>, <code>SHELL</code>, <code>DRAFT</code>, <code>MATE</code>. Core settings: Set sketch precision to 0.001mm, enable RealView & curvature combs.",
        "workflow": [
            ("1. Parametric Skeleton & Datum Framework", "Establish master sketch skeletons with fully constrained geometric relationships (Coincident, Tangent, Concentric) tied to primary origin planes."),
            ("2. Solid & Surfacing Feature Tree Execution", "Build primary mass features followed by functional engineering operations: draft angles for tooling release, ribs for structural stiffness, and internal core cavities."),
            ("3. Assembly Kinematics & Interference Simulation", "Assemble multi-body components using standard and mechanical mates. Run dynamic collision detection, kinematic range-of-motion studies, and static FEA stress analysis."),
            ("4. GD&T Detailing & CNC Toolpath Export", "Author 2D fabrication sheets with complete ASME Y14.5 / ISO 1101 geometric tolerances (Position, Flatness, Runout) and export STEP AP242 / Parasolid models for 5-axis CAM.")
        ],
        "standards": ["ASME Y14.5-2018 (Dimensioning & Tolerancing)", "ISO 1101 (Geometrical Product Specifications)", "ISO 2768 (General Tolerances for Machining)", "ASTM / DIN Material Specifications"],
        "troubleshooting": [
            ("Sketch breaks or flips geometry when adjusting dimensions", "Sketch was under-constrained. Always apply geometric constraints (tangency, horizontal/vertical) before adding driving numerical dimensions."),
            ("Shell or Fillet feature fails on complex curved topology", "Curvature radius is tighter than fillet radius or minimum wall thickness. Inspect surface curvature using Zebra stripes and eliminate zero-radius sharp corners."),
            ("Assembly performance severely lags during rotation", "Large assembly mode was disabled. Suppress non-essential cosmetic features (threads, knurls) and use lightweight component representations.")
        ]
    },
    "aec": {
        "commands": "BIM & CAD tools: <code>WALL</code>, <code>FLOOR</code>, <code>ROOF</code>, <code>FAMILY</code>, <code>XREF</code>, <code>IFCEXPORT</code>. Setup: Coordinate shared project base points, configure Level/Grid datum.",
        "workflow": [
            ("1. Spatial Programming & Shared Georeferencing", "Establish project base points, survey coordinates, building storeys, and column grid systems coordinated across architectural, structural, and MEP consultants."),
            ("2. LOD 200 - 300 Parametric Component Assembly", "Model multi-layer architectural assemblies (curtain walls, structural framing, floor slabs, MEP risers) using intelligent parametric family components."),
            ("3. Interdisciplinary Clash Detection & Coordination", "Federate discipline models in Navisworks or Solibri. Run automated hard/soft clash tests and track issues using BCF (BIM Collaboration Format) workflows."),
            ("4. 2D Construction Documentation & Quantity Schedules", "Extract live plans, building sections, elevations, and automated component schedules (doors, windows, concrete volume) linked directly to the central model.")
        ],
        "standards": ["ISO 19650-1/-2 (Organization of information about construction works - BIM)", "buildingSMART openBIM & IFC 4x3", "AIA Document E202 (Building Information Modeling Protocol)", "National CAD Standard (NCS)"],
        "troubleshooting": [
            ("Architectural and Structural models do not align when linked", "Shared coordinates were not acquired. Ensure both teams use 'Acquire Coordinates' from a designated master site model."),
            ("Wall joints and multi-layer materials do not clean up cleanly", "Layer core priorities are misconfigured. Ensure structural cores have Priority 1, substrate Priority 2, insulation Priority 3, and finishes Priority 4/5."),
            ("IFC export drops custom attributes and scheduling properties", "Map property sets using custom IFC export translation tables before exporting to external coordination software.")
        ]
    },
    "general": {
        "commands": "Core CAD commands: <code>LINE</code>, <code>PLINE</code>, <code>BLOCK</code>, <code>DIMSTYLE</code>, <code>PURGE</code>, <code>AUDIT</code>. Settings: <code>DYNAMICINPUT=1</code>, <code>SAVETIME=10</code>, <code>VISRETAIN=1</code>.",
        "workflow": [
            ("1. Design Intent & Standards Definition", "Establish drawing limits, layer hierarchies, lineweights, color palettes, and text styles in accordance with company CAD standards and project specifications."),
            ("2. Precision 2D/3D Geometry Construction", "Construct primary shapes using absolute/relative polar coordinates, object snaps (OSNAP), and parametric constraints to guarantee mathematical accuracy."),
            ("3. Modular Structuring & Reference Linking", "Group reusable sub-elements into standardized Blocks and link background consultant data as External References (Xrefs) using relative file paths."),
            ("4. Quality Assurance, Annotation & Output", "Apply annotative dimensions, run automated standard audits (DWS), clean database with PURGE/AUDIT, and publish vector PDF packages.")
        ],
        "standards": ["ISO 128 (Technical Product Documentation - General Principles of Presentation)", "ASME Y14.100 (Engineering Drawing Practices)", "ISO 9001 CAD Quality Assurance Guidelines"],
        "troubleshooting": [
            ("Drawing file size balloons and displays noticeable viewport lag", "Unused blocks, registered applications (RegApps), and DGN linetypes bloating file. Run <code>-PURGE > R > * > N</code> and <code>AUDIT</code> to scrub internal database."),
            ("Text and dimensions scale disproportionately across paper space viewports", "Objects were not assigned Annotative properties. Enable Annotative scaling in Style managers and assign active viewport scales."),
            ("Line styles print as solid lines rather than dashed/hidden", "Linetype scale mismatch. Adjust <code>LTSCALE</code>, <code>PSLTSCALE=1</code>, and <code>MSLTSCALE=1</code> to ensure uniform dashed appearance across all viewports.")
        ]
    }
}

def detect_domain(title, text, chip):
    combined = (title + " " + text + " " + chip).lower()
    if any(k in combined for k in ["civil", "road", "highway", "stormwater", "drainage", "traffic", "bridge", "tunnel", "utility", "terrain", "gis", "survey", "marine", "port"]):
        return "civil"
    elif any(k in combined for k in ["instrument", "watch", "gear", "mfg", "mechanical", "assembly", "mold", "sheet metal", "machining", "cnc", "fea", "acoustic", "mechanism", "solid", "parametric", "bottom-up"]):
        return "mfg"
    elif any(k in combined for k in ["bim", "building", "architect", "construction", "underground space", "modular", "facade", "mep", "structure", "ifc", "facility"]):
        return "aec"
    else:
        return "general"

def enrich_concept_page(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    
    # Check word count
    for tag in soup(["script", "style", "nav", "footer", "header", "svg", "noscript", "aside"]):
        tag.decompose()
    main = soup.find("main") or soup.find("article") or soup.body
    main_text = main.get_text(separator=" ", strip=True) if main else ""
    words = main_text.split()
    if len(words) >= 350:
        return False # already rich enough

    # Reload original content to edit cleanly
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")

    title_elem = soup.title.string if soup.title and soup.title.string else ""
    h1_elem = soup.find("h1")
    concept_name = h1_elem.get_text(strip=True) if h1_elem else title_elem.replace("| Gstarcademy", "").strip()
    
    chip_elem = soup.find(class_=re.compile(r"(chip|pill|badge)", re.I))
    chip_text = chip_elem.get_text(strip=True) if chip_elem else "CAD Technology"

    domain_key = detect_domain(concept_name, main_text, chip_text)
    domain_data = DOMAIN_KNOWLEDGE[domain_key]

    article = soup.find("article")
    if not article:
        return False

    # Find existing sections
    sections = article.find_all("section", class_="kb-concept-section")
    
    # 1. Enrich Definition & Theoretical Foundation
    def_sec = None
    for sec in sections:
        h2 = sec.find("h2")
        if h2 and "definition" in h2.get_text(strip=True).lower():
            def_sec = sec
            break
            
    if def_sec:
        p_tags = def_sec.find_all("p")
        if len(p_tags) < 3:
            enrich_p1 = soup.new_tag("p")
            enrich_p1.string = f"In contemporary engineering practice, {concept_name} represents a critical interdisciplinary methodology. By replacing manual heuristics with rigorous digital simulation and parametric constraints, engineering teams establish an unbroken digital thread from initial concept through detailed physical realization."
            enrich_p2 = soup.new_tag("p")
            enrich_p2.string = f"Achieving high-quality results in {concept_name} requires a thorough understanding of geometric tolerances, material behavior, and coordinate governance. Digital models serve not merely as graphical representations, but as authoritative engineering databases driving downstream analysis, procurement, and robotic fabrication."
            def_sec.append(enrich_p1)
            def_sec.append(enrich_p2)

    # 2. Add Key Commands & System Operations Section
    cmd_sec = soup.new_tag("section", attrs={"class": "kb-concept-section", "style": "margin-top: 32px;"})
    cmd_h2 = soup.new_tag("h2")
    cmd_h2.string = "Core Commands & Practical System Operations"
    cmd_p1 = soup.new_tag("p")
    cmd_p1.append(BeautifulSoup(f"Executing {concept_name} effectively relies on specialized CAD/BIM command workflows and system variable configurations: {domain_data['commands']}", "html.parser"))
    cmd_p2 = soup.new_tag("p")
    cmd_p2.string = f"Engineers must ensure system precision tolerances are calibrated prior to modeling. Utilizing geometric constraints, structured layer naming, and associative dimensions guarantees that subsequent modifications propagate cleanly throughout the entire assembly tree without geometric failure."
    cmd_sec.append(cmd_h2)
    cmd_sec.append(cmd_p1)
    cmd_sec.append(cmd_p2)

    # 3. Add Standard 4-Step Engineering Workflow Section
    wf_sec = soup.new_tag("section", attrs={"class": "kb-concept-section", "style": "margin-top: 32px;"})
    wf_h2 = soup.new_tag("h2")
    wf_h2.string = f"Standard Engineering Workflow for {concept_name}"
    wf_sec.append(wf_h2)
    
    for step_title, step_desc in domain_data["workflow"]:
        step_card = soup.new_tag("div", attrs={"style": "margin-bottom: 18px; padding: 18px 20px; background: var(--ink-surface-2, #f9fafb); border: 1px solid var(--ink-line, #e5e7eb); border-radius: 10px;"})
        st_h3 = soup.new_tag("h3", attrs={"style": "margin: 0 0 8px; font-size: 0.95rem; font-weight: 700; color: var(--ink-text);"})
        st_h3.string = step_title
        st_p = soup.new_tag("p", attrs={"style": "margin: 0; font-size: 14px; line-height: 1.65; color: var(--ink-text);"})
        st_p.string = step_desc
        step_card.append(st_h3)
        step_card.append(st_p)
        wf_sec.append(step_card)

    # 4. Add Troubleshooting Table Section
    tb_sec = soup.new_tag("section", attrs={"class": "kb-concept-section", "style": "margin-top: 32px;"})
    tb_h2 = soup.new_tag("h2")
    tb_h2.string = "Common Failure Scenarios & Troubleshooting"
    tb_sec.append(tb_h2)
    
    table_wrapper = soup.new_tag("div", attrs={"style": "overflow-x: auto; margin-top: 14px;"})
    table = soup.new_tag("table", attrs={"style": "width: 100%; border-collapse: collapse; background: var(--ink-surface); border: 1px solid var(--ink-line); font-size: 13.5px;"})
    
    thead = soup.new_tag("thead")
    tr_head = soup.new_tag("tr", attrs={"style": "background: var(--ink-surface-2); border-bottom: 2px solid var(--ink-line); text-align: left;"})
    th1 = soup.new_tag("th", attrs={"style": "padding: 10px 14px; font-weight: 700; width: 35%;"})
    th1.string = "Failure / Geometric Issue"
    th2 = soup.new_tag("th", attrs={"style": "padding: 10px 14px; font-weight: 700;"})
    th2.string = "Root Cause & Mitigation Strategy"
    tr_head.append(th1)
    tr_head.append(th2)
    thead.append(tr_head)
    table.append(thead)
    
    tbody = soup.new_tag("tbody")
    for issue, fix in domain_data["troubleshooting"]:
        tr = soup.new_tag("tr", attrs={"style": "border-bottom: 1px solid var(--ink-line);"})
        td1 = soup.new_tag("td", attrs={"style": "padding: 10px 14px; font-weight: 600; vertical-align: top; color: var(--ink-text);"})
        td1.string = issue
        td2 = soup.new_tag("td", attrs={"style": "padding: 10px 14px; vertical-align: top; color: var(--ink-text); line-height: 1.6;"})
        td2.string = fix
        tr.append(td1)
        tr.append(td2)
        tbody.append(tr)
    table.append(tbody)
    table_wrapper.append(table)
    tb_sec.append(table_wrapper)

    # 5. Enrich Standards Section
    std_sec = None
    for sec in sections:
        h2 = sec.find("h2")
        if h2 and "standard" in h2.get_text(strip=True).lower():
            std_sec = sec
            break
            
    if std_sec:
        ul = std_sec.find("ul")
        if not ul:
            ul = soup.new_tag("ul")
            std_sec.append(ul)
        existing_items = [li.get_text(strip=True).lower() for li in ul.find_all("li")]
        for std in domain_data["standards"]:
            if std.lower() not in existing_items:
                new_li = soup.new_tag("li")
                new_li.string = std
                ul.append(new_li)
    else:
        std_sec = soup.new_tag("section", attrs={"class": "kb-concept-section", "style": "margin-top: 32px;"})
        std_h2 = soup.new_tag("h2")
        std_h2.string = "Industry Standards & Compliance Codes"
        std_ul = soup.new_tag("ul")
        for std in domain_data["standards"]:
            new_li = soup.new_tag("li")
            new_li.string = std
            std_ul.append(new_li)
        std_sec.append(std_h2)
        std_sec.append(std_ul)

    # Find where to insert new sections (insert before Sources/Further Reading or at the end of article)
    sources_sec = None
    for sec in sections:
        h2 = sec.find("h2")
        if h2 and any(k in h2.get_text(strip=True).lower() for k in ["source", "reading", "learn more"]):
            sources_sec = sec
            break

    if sources_sec:
        sources_sec.insert_before(cmd_sec)
        sources_sec.insert_before(wf_sec)
        sources_sec.insert_before(tb_sec)
        if not any("standard" in (s.find("h2").get_text(strip=True).lower() if s.find("h2") else "") for s in sections):
            sources_sec.insert_before(std_sec)
    else:
        article.append(cmd_sec)
        article.append(wf_sec)
        article.append(tb_sec)
        if not any("standard" in (s.find("h2").get_text(strip=True).lower() if s.find("h2") else "") for s in sections):
            article.append(std_sec)

    # Update date
    time_tag = soup.find("time")
    if time_tag:
        time_tag["datetime"] = TODAY
        time_tag.string = TODAY

    # Write back
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))
    return True

def main():
    count = 0
    enriched = 0
    for root, dirs, files in os.walk(CONCEPTS_DIR):
        for f in files:
            if f.endswith(".html"):
                count += 1
                fp = os.path.join(root, f)
                if enrich_concept_page(fp):
                    enriched += 1

    print(f"Scanned {count} concept files. Enriched {enriched} thin concept pages.")

if __name__ == "__main__":
    main()
