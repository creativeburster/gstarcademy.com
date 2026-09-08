import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# -*- coding: utf-8 -*-
"""
CAD Learn Hub (gstarcademy.com) Multi-Platform Overseas Backlinks Batch Executor
Publishes high-quality, high-DA technical English articles & cheat sheets across:
- Dev.to (DA 90+)
- GitHub Gist (DA 96)
- Telegraph (DA 92+)
- Rentry.co (DA 78)
"""
import os
import sys
import time
import json
import urllib.request
import urllib.parse
import http.cookiejar

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CUR_DIR)

from tracker import add_backlink, generate_report
from devto_runner import publish_devto_article
from gist_runner import publish_github_gist
from telegraph_runner import publish_telegraph_page

def publish_rentry(title, text_markdown, target_url="https://gstarcademy.com"):
    print("=" * 60)
    print(f"🚀 Publishing to Rentry.co (DA 78): {title}")
    print("=" * 60)
    
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    try:
        # 1. Get csrf token
        req0 = urllib.request.Request("https://rentry.co", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        })
        resp0 = opener.open(req0, timeout=10)
        html = resp0.read().decode("utf-8")
        
        csrf = None
        for cookie in cj:
            if cookie.name == "csrftoken":
                csrf = cookie.value
                break
                
        if not csrf and 'csrfmiddlewaretoken' in html:
            parts = html.split('csrfmiddlewaretoken')
            for part in parts[1:]:
                if 'value="' in part:
                    csrf = part.split('value="')[1].split('"')[0]
                    break
                
        if not csrf:
            print("❌ Failed to extract CSRF token from Rentry")
            return None
            
        # 2. Post content
        payload = urllib.parse.urlencode({
            "csrfmiddlewaretoken": csrf,
            "text": text_markdown,
            "edit_code": "cadlearn2026"
        }).encode("utf-8")
        
        req1 = urllib.request.Request("https://rentry.co/api/new", data=payload, headers={
            "Referer": "https://rentry.co",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        })
        
        resp1 = opener.open(req1, timeout=10)
        res_data = json.loads(resp1.read().decode("utf-8"))
        
        if res_data.get("status") == "200":
            url = res_data.get("url")
            print(f"🎉 Successfully published to Rentry! Live URL: {url}")
            
            add_backlink(
                platform="Rentry.co (Markdown Paste DA 78)",
                domain_authority="DA 78",
                category="Engineering Reference & Cheat Sheet",
                post_title=title,
                target_url=target_url,
                backlink_url=url,
                anchor_text="CAD Learn Hub: Interactive Terminology & Standards",
                link_type="Dofollow / Public Note",
                status="Live",
                notes="Lightweight high-DA markdown paste for engineering cheat sheets"
            )
            return url
        else:
            print(f"❌ Rentry publish error: {res_data}")
            return None
    except Exception as e:
        print(f"❌ Exception publishing to Rentry: {e}")
        return None

def run_all_batches():
    print("############################################################")
    print("### STARTING CAD LEARN HUB OVERSEAS BACKLINK CAMPAIGN    ###")
    print("############################################################\n")
    
    results = []
    
    # ------------------------------------------------------------
    # 1. Dev.to (DA 90+)
    # ------------------------------------------------------------
    devto_title = "The 2026 CAD Engineer Skill Roadmap: From 2D Drafting to Generative BIM"
    devto_tags = ["cad", "engineering", "architecture", "career"]
    devto_body = """# The 2026 CAD Engineer Skill Roadmap: From 2D Drafting to Generative BIM

As modern engineering and architecture projects become increasingly collaborative, Computer-Aided Design (CAD) professionals must expand beyond conventional line-drawing. Today's industry demands structured multi-discipline literacy across mechanical modeling, civil infrastructure, and building information modeling (BIM).

---

## 🏗️ The 6 Industry Career Tracks

1. **Architectural BIM Specialist**: Parametric family design, LOD 300/400 detailing, clash detection, and ISO 19650 BIM workflows.
2. **Mechanical CAD (MCAD) Designer**: Constraint-based sketch architecture, complex solid/surface features, tolerance stack-up analysis, and ASME Y14.5 GD&T standards.
3. **Civil & Infrastructure Engineer**: Digital terrain modeling, corridor alignments, stormwater grading, and survey surface processing.
4. **Professional 2D Draftsperson**: Micro-precision geometric constructions, dynamic blocks, layer management, and ANSI/ISO drawing standards.
5. **Simulation & CAE Analyst**: Meshing discipline, boundary conditions, linear static stress analysis, and structural optimization.
6. **Architectural Visualization Artist**: Photorealistic PBR shader graphs, HDRI environment lighting, and cinematic walkthrough renders.

---

## 📊 Benchmark Your Proficiency

Are you industry-ready for 2026? You can self-evaluate your competencies across all 6 career tracks with immediate scoring and progress tracking at the [CAD Learn Hub Interactive Proficiency Assessment](https://gstarcademy.com/quiz.html).

Explore our full interactive open learning hub:
- **Interactive Career Skill Matrix**: [https://gstarcademy.com/knowledge-roadmap.html](https://gstarcademy.com/knowledge-roadmap.html)
- **CAD & BIM Knowledge Graph**: [https://gstarcademy.com/kb-graph.html](https://gstarcademy.com/kb-graph.html)
- **Comprehensive CAD Terminology Lexicon**: [https://gstarcademy.com/kb-terms.html](https://gstarcademy.com/kb-terms.html)
- **Software Benchmark & Selection Guide**: [https://gstarcademy.com/kb-software.html](https://gstarcademy.com/kb-software.html)
- **Curated Video Tutorials Index**: [https://gstarcademy.com/tutorials.html](https://gstarcademy.com/tutorials.html)

Continuous technical growth requires structured foundations. Master the essentials today.
"""
    res_devto = publish_devto_article(devto_title, devto_body, devto_tags, canonical_url="https://gstarcademy.com/knowledge-roadmap.html")
    results.append(("Dev.to", res_devto))
    time.sleep(3)
    
    # ------------------------------------------------------------
    # 2. GitHub Gist #1 (DA 96) - Standards Cheat Sheet
    # ------------------------------------------------------------
    gist1_desc = "BIM & CAD Engineering Standards Quick Reference Cheat Sheet (2026)"
    gist1_fname = "bim-cad-standards-reference.md"
    gist1_content = """# BIM & CAD Engineering Standards Quick Reference (2026)

A curated reference sheet summarizing core ISO, ASME, and AIA standards for engineers, architects, and CAD managers.

## 1. Line Weights & Hierarchy (ISO 128 / ASME Y14.2)
- **Extra Thick (0.70 mm)**: Sheet borders, title block division lines, cutting planes.
- **Thick (0.50 mm)**: Visible object outlines, prominent architectural contours.
- **Medium (0.35 mm)**: Hidden lines, text notes, standard grid lines.
- **Thin (0.25 mm)**: Dimension lines, extension lines, leaders, hatching/section fills.

## 2. Geometric Dimensioning & Tolerancing (GD&T) Quick Keys
| Symbol | Characteristic | Tolerance Type | Datum Reference Required? |
| :--- | :--- | :--- | :--- |
| **⏤** | Straightness | Form | No |
| **⏥** | Flatness | Form | No |
| **○** | Circularity | Form | No |
| **⌭** | Cylindricity | Form | No |
| **⟂** | Perpendicularity | Orientation | Yes |
| **∥** | Parallelism | Orientation | Yes |
| **∠** | Angularity | Orientation | Yes |
| **⌖** | True Position | Location | Yes |
| **◎** | Concentricity | Location | Yes |

## 3. BIM Level of Development (LOD) Definitions (BIMForum 2026)
- **LOD 100**: Conceptual massing with approximate volume and location.
- **LOD 200**: Generic system, assembly, or element with approximate size and shape.
- **LOD 300**: Specific assembly with accurate size, shape, location, and orientation.
- **LOD 350**: Includes connection details and coordination with adjoining building components.
- **LOD 400**: Fabrication-ready detail with full manufacturing tolerances.
- **LOD 500**: Field-verified as-built model for facilities maintenance.

---

### 🌐 Comprehensive Online Learning & Certification
For full interactive term breakdowns, career tracks, and self-assessment quizzes, explore:
- **CAD Learn Hub Official**: [https://gstarcademy.com](https://gstarcademy.com)
- **Engineering Terminology Dictionary**: [https://gstarcademy.com/kb-terms.html](https://gstarcademy.com/kb-terms.html)
- **CAD Career Roadmap & Skill Matrix**: [https://gstarcademy.com/knowledge-roadmap.html](https://gstarcademy.com/knowledge-roadmap.html)
- **Interactive CAD Proficiency Test**: [https://gstarcademy.com/quiz.html](https://gstarcademy.com/quiz.html)
"""
    res_gist1 = publish_github_gist(gist1_desc, gist1_fname, gist1_content, target_url="https://gstarcademy.com/kb-terms.html")
    results.append(("GitHub Gist 1", res_gist1))
    time.sleep(3)
    
    # ------------------------------------------------------------
    # 3. GitHub Gist #2 (DA 96) - Top Shortcut Keys
    # ------------------------------------------------------------
    gist2_desc = "AutoCAD & GstarCAD Top 50 Productivity Shortcuts & Commands (2026 Edition)"
    gist2_fname = "cad-shortcuts-cheatsheet.md"
    gist2_content = """# AutoCAD & GstarCAD Top 50 Productivity Shortcuts (2026)

Boost your drafting speed with this essential command reference for DWG-based CAD software.

## Top Drawing Commands
- `L` -> LINE: Creates straight line segments
- `PL` -> PLINE: 2D polyline with continuous segments
- `C` -> CIRCLE: Creates a circle (center, radius, or 2P/3P)
- `REC` -> RECTANGLE: Creates a rectangular polyline
- `A` -> ARC: Creates an arc using 3 points
- `H` -> HATCH: Fills an enclosed boundary with a hatch pattern
- `REG` -> REGION: Converts an enclosed 2D loop into a planar 2D surface

## High-Frequency Modification Commands
- `M` -> MOVE: Moves objects at a specified distance and direction
- `CO` / `CP` -> COPY: Duplicates objects
- `RO` -> ROTATE: Rotates objects around a base point
- `TR` -> TRIM: Trims objects to meet the edges of other objects
- `EX` -> EXTEND: Extends objects to meet the edges of other objects
- `F` -> FILLET: Rounds and fillets the edges of objects
- `CHA` -> CHAMFER: Bevels the edges of objects
- `O` -> OFFSET: Creates concentric circles, parallel lines, and parallel curves
- `MI` -> MIRROR: Creates a mirrored copy of selected objects
- `SC` -> SCALE: Enlarges or reduces selected objects proportionally
- `X` -> EXPLODE: Breaks a compound object into its component objects
- `J` -> JOIN: Combines linear and curved objects to create a single object

## Precision Snaps (OSNAP)
- `F3` -> Toggle Object Snap (OSNAP) ON/OFF
- `F8` -> Toggle Ortho Mode ON/OFF
- `F9` -> Toggle Snap Mode ON/OFF
- `F10` -> Toggle Polar Tracking ON/OFF
- `F11` -> Toggle Object Snap Tracking ON/OFF

---

### 🚀 Self-Study & Certification Portal
- **CAD Learn Hub Hub**: [https://gstarcademy.com](https://gstarcademy.com)
- **Curated Video Tutorials Index**: [https://gstarcademy.com/tutorials.html](https://gstarcademy.com/tutorials.html)
- **Interactive Career Roadmap**: [https://gstarcademy.com/knowledge-roadmap.html](https://gstarcademy.com/knowledge-roadmap.html)
- **Interactive Skills Quiz**: [https://gstarcademy.com/quiz.html](https://gstarcademy.com/quiz.html)
"""
    res_gist2 = publish_github_gist(gist2_desc, gist2_fname, gist2_content, target_url="https://gstarcademy.com/tutorials.html")
    results.append(("GitHub Gist 2", res_gist2))
    time.sleep(3)

    # ------------------------------------------------------------
    # 4. Telegraph #1 (DA 92+) - Software Comparison
    # ------------------------------------------------------------
    t1_title = "The 2026 CAD Software Benchmark: AutoCAD vs SolidWorks vs Revit vs FreeCAD"
    t1_nodes = [
        {"tag": "h3", "children": ["The Modern CAD Landscape in 2026"]},
        {"tag": "p", "children": ["Selecting the right Computer-Aided Design (CAD) environment is one of the most critical decisions for engineering departments, architectural studios, and aspiring drafters. Below is a structured comparison across the four primary industry pillars."]},
        {"tag": "h4", "children": ["1. General Drafting & Documentation: AutoCAD / GstarCAD"]},
        {"tag": "p", "children": ["AutoCAD remains the global standard for 2D technical drawings, schematics, and construction documentation (.dwg format). Cost-effective direct alternatives like GstarCAD provide full DWG compatibility with zero learning curve and perpetual licensing options."]},
        {"tag": "h4", "children": ["2. Mechanical Product Design: SolidWorks / Inventor / Fusion 360"]},
        {"tag": "p", "children": ["Feature-based parametric modeling dominates consumer product, aerospace, and machinery engineering. SolidWorks leads in traditional desktop assembly modeling, while cloud-native tools offer agile revision control."]},
        {"tag": "h4", "children": ["3. Architecture & Construction: Revit / ArchiCAD"]},
        {"tag": "p", "children": ["Building Information Modeling (BIM) replaces dumb lines with data-rich parametric components. Revit enables collaborative multi-discipline coordination across structural, MEP, and architectural scopes."]},
        {"tag": "h4", "children": ["4. Open-Source Freedom: FreeCAD"]},
        {"tag": "p", "children": ["For developers, makers, and cost-conscious startups, FreeCAD provides a fully extensible Python-scripted parametric kernel without subscription vendor lock-in."]},
        {"tag": "hr"},
        {"tag": "h3", "children": ["Explore In-Depth Software Benchmarks & Tutorials"]},
        {"tag": "p", "children": [
            "Access detailed feature comparisons, format support, and pricing models at the ",
            {"tag": "a", "attrs": {"href": "https://gstarcademy.com/kb-software.html"}, "children": ["CAD Software Comparison Matrix on CAD Learn Hub"]},
            "."
        ]},
        {"tag": "p", "children": [
            "Test your CAD competency across 6 disciplines: ",
            {"tag": "a", "attrs": {"href": "https://gstarcademy.com/quiz.html"}, "children": ["Free Interactive CAD Proficiency Assessment"]},
            "."
        ]}
    ]
    res_t1 = publish_telegraph_page(t1_title, t1_nodes, target_url="https://gstarcademy.com/kb-software.html")
    results.append(("Telegraph 1", res_t1))
    time.sleep(3)

    # ------------------------------------------------------------
    # 5. Telegraph #2 (DA 92+) - Career Roadmap
    # ------------------------------------------------------------
    t2_title = "Modern CAD Career Path Guide: Essential Competencies for Drafters & Modelers"
    t2_nodes = [
        {"tag": "h3", "children": ["Mastering Modern CAD Disciplines"]},
        {"tag": "p", "children": ["CAD is no longer just about using a digital pencil. Modern engineering workflows demand specialized fluency across parametric sketch constraints, geometric dimensioning, multi-discipline coordination, and cloud collaboration."]},
        {"tag": "h4", "children": ["Foundational 2D Drafting Competencies"]},
        {"tag": "p", "children": ["Mastering precision coordinates, layer naming standards (AIA / ISO 13567), dynamic block attributes, paper space viewport scaling, and plot style tables (CTB/STB)."]},
        {"tag": "h4", "children": ["3D Parametric & BIM Advancement"]},
        {"tag": "p", "children": ["Progressing to constraint-driven 3D modeling: sketch planes, extrude/revolve/sweep operations, assembly mates, interference detection, and BIM Level of Development (LOD 100 to 500)."]},
        {"tag": "hr"},
        {"tag": "h3", "children": ["Interactive Career Skill Matrix"]},
        {"tag": "p", "children": [
            "Review your career milestone checklist with our interactive node tree at the ",
            {"tag": "a", "attrs": {"href": "https://gstarcademy.com/knowledge-roadmap.html"}, "children": ["Interactive CAD Career Roadmap"]},
            "."
        ]},
        {"tag": "p", "children": [
            "Verify your concept mastery across 289+ curated assessment questions: ",
            {"tag": "a", "attrs": {"href": "https://gstarcademy.com/quiz.html"}, "children": ["Launch Free CAD Career Quiz"]},
            "."
        ]}
    ]
    res_t2 = publish_telegraph_page(t2_title, t2_nodes, target_url="https://gstarcademy.com/knowledge-roadmap.html")
    results.append(("Telegraph 2", res_t2))
    time.sleep(3)

    # ------------------------------------------------------------
    # 6. Rentry.co (DA 78) - GD&T Guide
    # ------------------------------------------------------------
    rentry_title = "Geometric Dimensioning and Tolerancing (GD&T) Engineering Quick Guide"
    rentry_body = """# Geometric Dimensioning & Tolerancing (GD&T) Quick Guide (ASME Y14.5)

Geometric Dimensioning and Tolerancing is the universal language used on mechanical engineering drawings to explicitly convey permissible variations in geometry.

## The 14 Standard GD&T Symbols

### 1. Form Controls (No Datum Reference Allowed)
- **Straightness (⏤)**: Line element must lie between two parallel lines.
- **Flatness (⏥)**: Surface elements must lie between two parallel planes.
- **Circularity (○)**: Radial cross-section elements must lie within two concentric circles.
- **Cylindricity (⌭)**: Cylindrical surface must lie within two coaxial cylinders.

### 2. Orientation Controls (Datum Reference Required)
- **Perpendicularity (⟂)**: Feature oriented at exactly 90 degrees relative to a datum.
- **Parallelism (∥)**: Feature oriented equidistant to a datum plane or axis.
- **Angularity (∠)**: Feature oriented at a specified angle relative to a datum.

### 3. Location Controls (Datum Reference Required)
- **True Position (⌖)**: Controls the theoretical center of a feature (holes, pins, slots).
- **Concentricity (◎)**: Coaxiality of opposing surface median points.
- **Symmetry (⌯)**: Medians of opposing elements symmetrical about a central plane.

### 4. Runout Controls
- **Circular Runout (↗)**: Individual circular cross-section variation during 360-degree rotation.
- **Total Runout (⌕)**: Composite variation across the entire cylindrical surface.

---

### 🌐 Official Learning Resource & Interactive Quiz
- **CAD Learn Hub**: [https://gstarcademy.com](https://gstarcademy.com)
- **CAD Terminology Encyclopedia**: [https://gstarcademy.com/kb-terms.html](https://gstarcademy.com/kb-terms.html)
- **CAD & BIM Interactive Skill Quiz**: [https://gstarcademy.com/quiz.html](https://gstarcademy.com/quiz.html)
- **Mechanical CAD Career Roadmap**: [https://gstarcademy.com/knowledge-roadmap.html](https://gstarcademy.com/knowledge-roadmap.html)
"""
    res_rentry = publish_rentry(rentry_title, rentry_body, target_url="https://gstarcademy.com/kb-terms.html")
    results.append(("Rentry.co", res_rentry))

    print("\n============================================================")
    print("### BATCH CAMPAIGN SUMMARY")
    print("============================================================")
    for platform, url in results:
        status = "✅ SUCCESS" if url else "❌ FAILED"
        print(f"- {platform}: {status} -> {url}")
        
    generate_report()
    print("\n🎉 All tasks complete. Check seo/BACKLINKS_REPORT.md for full ledger.")

if __name__ == "__main__":
    run_all_batches()
