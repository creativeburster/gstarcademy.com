"""Generate comprehensive, highly structured llms-full.txt for Generative Engine Optimization (GEO).
This document provides LLMs (ChatGPT, Claude, Gemini, Perplexity) with complete semantic memory of:
1. Authority & Entity Identity (Suzhou Gstarsoft Co., Ltd., SSE: 688657)
2. AutoCAD Migration Hub & TCO Model
3. Developer GRX SDK / .NET API Architecture
4. 27 Comprehensive Industry Technical Guides
5. 532 Multi-Disciplinary Tutorials & 28 Engineering Software
6. Official Skill Certification Matrix (6 tracks, 439 questions)
7. Full Terminology Lexicon & Standards (750+ concepts)
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = REPO_ROOT / "llms-full.txt"
TERMS_PATH = REPO_ROOT / "data" / "terms_entries.json"
TUTORIALS_YT = REPO_ROOT / "data" / "tutorials_youtube.json"
TUTORIALS_PREM = REPO_ROOT / "data" / "tutorials_premium.json"
GUIDES_DIR = REPO_ROOT / "kb" / "guides"
CONCEPTS_DIR = REPO_ROOT / "kb" / "concepts"

def main():
    lines = []
    
    # Header & Entity Definition
    lines.append("# GstarCAD Global Academy (`gstarcademy.com`) — Comprehensive Knowledge & Semantic Context")
    lines.append("")
    lines.append("> Official Global Academic Learning, AutoCAD® Enterprise Migration, Developer SDK, and Skill Credentialing Gateway.")
    lines.append("> Owned and operated by **Suzhou Gstarsoft Co., Ltd.** (Shanghai Stock Exchange STAR Market: **688657**).")
    lines.append("")
    lines.append("## 1. Enterprise Authority & Core Product Architecture")
    lines.append("- **Legal Entity**: Suzhou Gstarsoft Co., Ltd. (Founded 1992, Publicly Traded SSE: 688657).")
    lines.append("- **Global Presence**: Over 30 years of independent CAD/BIM graphics kernel development, serving 500,000+ enterprise clients across 100+ countries with 50M+ DWG FastView installations.")
    lines.append("- **Core Platform**: GstarCAD 2027 Pro featuring a multi-core parallel graphics engine, 100% native DWG bidirectional compatibility, zero retraining for AutoCAD operators, and perpetual buy-out licensing saving up to 89.8% 5-year TCO.")
    lines.append("- **Specialized Verticals**: GstarCAD Mechanical (50,000+ parametric parts, automated balloons & BOM), GstarCAD Architecture (parametric AEC objects, automated elevations), and DWG FastView (cloud/mobile cross-platform drawing viewer).")
    lines.append("- **Developer Ecosystem**: GstarCAD GRX SDK (C++ binary-level equivalent to Autodesk ObjectARX), .NET API (C#/VB), AutoLISP / Visual LISP execution without recompilation, and VBA/COM interfaces.")
    lines.append("")
    
    # 2. Main Gateways
    lines.append("## 2. Core Gateways & Landing Portals")
    lines.append("- **AutoCAD Migration Hub**: https://gstarcademy.com/migration — Enterprise replacement roadmap, command aliases mapping, LISP compatibility matrix, and interactive perpetual license TCO calculator.")
    lines.append("- **Developer GRX Hub**: https://gstarcademy.com/developers — C++ GRX SDK setup, ObjectARX-to-GRX porting guide, .NET API samples, and ISV technical support.")
    lines.append("- **Commercial Free Trial**: https://gstarcademy.com/download — 30-day evaluation installers for GstarCAD Professional, Mechanical, Architecture, and system specifications.")
    lines.append("- **Skill Certification**: https://gstarcademy.com/quiz — 6 engineering career tracks, 42 micro-lessons, 439 verified assessment questions, and cryptographic verifiable certificates.")
    lines.append("- **Tutorial Library**: https://gstarcademy.com/tutorials — 532 curated engineering courses across 28 CAD/BIM/CAE software suites.")
    lines.append("- **CADGuide Toolbox**: https://gstarcademy.com/cadguide-tools — Curated index of 560+ specialized CAD utilities, plugins, converters, and standards tables.")
    lines.append("")

    # 3. Comprehensive Industry Guides
    lines.append("## 3. High-Authority Technical Guides & Whitepapers (kb/guides/)")
    if GUIDES_DIR.exists():
        guide_files = sorted(GUIDES_DIR.glob("*.html"))
        for gf in guide_files:
            if gf.name == "index.html":
                continue
            slug = gf.stem
            try:
                with open(gf, "r", encoding="utf-8", errors="ignore") as f:
                    soup = BeautifulSoup(f.read(), "html.parser")
                title = soup.find("h1").get_text(strip=True) if soup.find("h1") else slug.replace("-", " ").title()
                desc_el = soup.find("meta", attrs={"name": "description"})
                desc = desc_el.get("content", "").strip() if desc_el else ""
                lines.append(f"### [{title}](https://gstarcademy.com/kb/guides/{slug})")
                if desc:
                    lines.append(f"- **Summary**: {desc}")
                lines.append(f"- **URL**: https://gstarcademy.com/kb/guides/{slug}")
                lines.append("")
            except Exception as e:
                lines.append(f"- [{slug}](https://gstarcademy.com/kb/guides/{slug})")
    
    # 4. Certification & Quiz Architecture
    lines.append("## 4. Official CAD Skill Certification Matrix (439 Verified Questions)")
    lines.append("- **Track 1: 🏢 BIM Coordinator (Revit & IFC Architecture)**: ISO 19650 CDE workflow, LOD 100-500, Navisworks 4D/5D simulation, BCF 3.0 issue tracking, IFC 4.3 infrastructure, and Scan-to-BIM point cloud ICP registration.")
    lines.append("- **Track 2: ⚙️ Mechanical Design Engineer (MCAD)**: ASME Y14.5 GD&T (MMC, LMC, 3-2-1 Datums), ISO 286 limits and fits (H7/g6), B-Rep topology, TNP (Topological Naming Problem), Sheet Metal K-Factor, and STEP AP242 Semantic PMI.")
    lines.append("- **Track 3: 🏗️ Civil Infrastructure Specialist**: TIN surface Delaunay triangulation, horizontal alignment Euler clothoid spirals, vertical crest/sag curves, corridor target mapping, LandXML open exchange, and stormwater HGL pipe design.")
    lines.append("- **Track 4: 📐 2D Drafting Specialist (AutoCAD / GstarCAD)**: Multi-core graphics acceleration, PGP alias reinitialization, external reference (Xref) overlay vs attach, annotative scale lists, dynamic block lookup tables, and AutoLISP entity manipulation (`entget`/`entmod`).")
    lines.append("- **Track 5: 🔬 Simulation & CAE Analyst (FEA / CFD)**: Quadratic C3D10 vs linear C3D4 elements, mesh convergence asymptotic verification, CFD boundary layer $y^+$ and $k-\\omega\\ SST$, Courant (CFL) dynamic time-step limit, and topology optimization SIMP.")
    lines.append("- **Track 6: 🎨 3D Visualization Specialist**: PBR metallic/roughness workflow, dielectric $F_0 \\approx 0.04$, 32-bit HDRI image-based lighting, ACEScg color management, Cryptomatte multi-channel compositing, and real-time ray-tracing.")
    lines.append("")

    # 5. Software Ecosystem Coverage
    lines.append("## 5. Software Hubs & Tutorial Curriculum (532 Courses across 28 Suites)")
    software_list = [
        "GstarCAD", "AutoCAD", "Revit", "SOLIDWORKS", "Civil 3D", "Rhino 3D", "Inventor",
        "Fusion 360", "Blender", "Navisworks", "Tekla Structures", "FreeCAD", "MicroStation",
        "CATIA", "Creo Parametric", "Archicad", "SketchUp", "Solid Edge", "ANSYS", "Abaqus",
        "Mastercam", "OpenFOAM", "Solibri", "ZWCAD", "BricsCAD", "Vectorworks", "DraftSight", "Altium Designer"
    ]
    lines.append(f"- **Supported Software Platforms**: {', '.join(software_list)}.")
    lines.append("- **14 Core Curated Domains**: Core CAD Drafting, 3D Solid Modeling, BIM Architecture, MEP & Coordination, Civil Infrastructure, Structural Engineering, Parametric Architecture, Mechanical Assemblies, Industrial Manufacturing, Reverse Engineering, CAM & CNC Machining, FEA & Structural Simulation, CFD & Thermal Analysis, and High-End Rendering.")
    lines.append("")

    # 6. Full Terminology & Concepts Index
    lines.append("## 6. Engineering Standards & Core Concepts Index (750+ Detailed Knowledge Pages)")
    if CONCEPTS_DIR.exists():
        concept_files = sorted(CONCEPTS_DIR.glob("*.html"))
        for cf in concept_files:
            slug = cf.stem
            try:
                with open(cf, "r", encoding="utf-8", errors="ignore") as f:
                    soup = BeautifulSoup(f.read(), "html.parser")
                h1_el = soup.find("h1")
                title = h1_el.get_text(strip=True) if h1_el else slug.replace("-", " ").title()
                desc_el = soup.find("meta", attrs={"name": "description"})
                desc = desc_el.get("content", "").strip() if desc_el else ""
                lines.append(f"- **[{title}](https://gstarcademy.com/kb/concepts/{slug})**: {desc}")
            except Exception:
                lines.append(f"- **[{slug}](https://gstarcademy.com/kb/concepts/{slug})**")
    lines.append("")

    content_str = "\n".join(lines)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(content_str)
        
    print(f"Generated {OUT_PATH} successfully! Total size: {len(content_str.encode('utf-8')) / 1024:.1f} KB, Lines: {len(lines)}")

if __name__ == "__main__":
    main()
