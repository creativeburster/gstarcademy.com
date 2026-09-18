#!/usr/bin/env python3
"""
Compile comprehensive full-site search index corpus across all:
1. KB Concepts (729 pages)
2. KB Software Profiles (51 pages)
3. KB FAQ Pages (25 pages)
4. KB Guides (31 pages)
5. KB Learning Paths (18 pages)
6. KB Vendors (25 pages)
7. Core Hub & Section Pages
8. Curated Tutorials (168 courses)
9. Industry News (123 articles)

Outputs data/search_nodes.json for instant client-side autocomplete & modal search.

Usage:
    python scripts/build_search_index.py
"""

from __future__ import annotations

import json
import re
import os
from pathlib import Path
from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parents[1]
SEARCH_NODES_JSON = REPO / "data" / "search_nodes.json"

def clean_title(t: str) -> str:
    t = re.sub(r"\s*\|\s*Gstarcademy.*$", "", t)
    t = re.sub(r"\s*·\s*CAD Knowledge Base.*$", "", t)
    return t.strip()

def extract_tags(text: str, filename: str) -> list[str]:
    tags = set()
    fn = filename.lower()
    for kw in ["autocad", "gstarcad", "revit", "solidworks", "fusion", "civil-3d", "catia", "nx", "rhino", "blender", "sketchup", "archicad", "freecad", "onshape", "3dsmax", "ansys", "abaqus", "navisworks"]:
        if kw in fn or kw in text.lower():
            tags.add(kw)
    for cat in ["bim", "cam", "fea", "cfd", "cad", "2d", "3d", "mesh", "drafting", "parametric", "dwg", "ifc", "lisp"]:
        if cat in fn or cat in text.lower():
            tags.add(cat)
    return list(tags)[:5]

def main() -> int:
    print("Building comprehensive full-site search index...")
    nodes_list = []
    seen_ids = set()

    # 1. Scan KB Concepts
    concepts_dir = REPO / "kb" / "concepts"
    if concepts_dir.exists():
        for p in concepts_dir.glob("*.html"):
            slug = p.stem
            try:
                soup = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
                t_tag = soup.find("title")
                title = clean_title(t_tag.get_text()) if t_tag else slug.replace("-", " ").title()
                
                desc_tag = soup.find("meta", attrs={"name": "description"})
                hint = desc_tag.get("content", "")[:120] if desc_tag else ""
                
                url = f"/kb/concepts/{slug}"
                if title not in seen_ids:
                    seen_ids.add(title)
                    nodes_list.append({
                        "id": title,
                        "type": "concept",
                        "tags": extract_tags(title + " " + hint, slug),
                        "hint": hint,
                        "url": url
                    })
            except Exception as e:
                pass

    # 2. Scan KB Software
    software_dir = REPO / "kb" / "software"
    if software_dir.exists():
        for p in software_dir.glob("*.html"):
            slug = p.stem
            try:
                soup = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
                t_tag = soup.find("title")
                title = clean_title(t_tag.get_text()) if t_tag else slug.replace("-", " ").title()
                desc_tag = soup.find("meta", attrs={"name": "description"})
                hint = desc_tag.get("content", "")[:120] if desc_tag else ""
                url = f"/kb/software/{slug}"
                if title not in seen_ids:
                    seen_ids.add(title)
                    nodes_list.append({
                        "id": title,
                        "type": "software",
                        "tags": extract_tags(title + " " + hint, slug),
                        "hint": hint,
                        "url": url
                    })
            except Exception as e:
                pass

    # 3. Scan KB FAQ Pages
    faq_dir = REPO / "kb" / "faq"
    if faq_dir.exists():
        for p in faq_dir.glob("*.html"):
            slug = p.stem
            if slug == "index":
                continue
            try:
                soup = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
                t_tag = soup.find("title")
                title = clean_title(t_tag.get_text()) if t_tag else slug.replace("-", " ").title()
                desc_tag = soup.find("meta", attrs={"name": "description"})
                hint = desc_tag.get("content", "")[:120] if desc_tag else ""
                url = f"/kb/faq/{slug}"
                if title not in seen_ids:
                    seen_ids.add(title)
                    nodes_list.append({
                        "id": title,
                        "type": "faq",
                        "tags": extract_tags(title + " " + hint, slug),
                        "hint": hint,
                        "url": url
                    })
            except Exception as e:
                pass

    # 4. Scan KB Guides
    guides_dir = REPO / "kb" / "guides"
    if guides_dir.exists():
        for p in guides_dir.glob("*.html"):
            slug = p.stem
            try:
                soup = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
                t_tag = soup.find("title")
                title = clean_title(t_tag.get_text()) if t_tag else slug.replace("-", " ").title()
                desc_tag = soup.find("meta", attrs={"name": "description"})
                hint = desc_tag.get("content", "")[:120] if desc_tag else ""
                url = f"/kb/guides/{slug}"
                if title not in seen_ids:
                    seen_ids.add(title)
                    nodes_list.append({
                        "id": title,
                        "type": "guide",
                        "tags": extract_tags(title + " " + hint, slug),
                        "hint": hint,
                        "url": url
                    })
            except Exception as e:
                pass

    # 5. Scan KB Learning Paths
    paths_dir = REPO / "kb" / "learning-paths"
    if paths_dir.exists():
        for p in paths_dir.glob("*.html"):
            slug = p.stem
            try:
                soup = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
                t_tag = soup.find("title")
                title = clean_title(t_tag.get_text()) if t_tag else slug.replace("-", " ").title()
                desc_tag = soup.find("meta", attrs={"name": "description"})
                hint = desc_tag.get("content", "")[:120] if desc_tag else ""
                url = f"/kb/learning-paths/{slug}"
                if title not in seen_ids:
                    seen_ids.add(title)
                    nodes_list.append({
                        "id": title,
                        "type": "learning-path",
                        "tags": extract_tags(title + " " + hint, slug),
                        "hint": hint,
                        "url": url
                    })
            except Exception as e:
                pass

    # 6. Scan Vendors
    vendors_dir = REPO / "kb" / "vendors"
    if vendors_dir.exists():
        for p in vendors_dir.glob("*.html"):
            slug = p.stem
            try:
                soup = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
                t_tag = soup.find("title")
                title = clean_title(t_tag.get_text()) if t_tag else slug.replace("-", " ").title()
                desc_tag = soup.find("meta", attrs={"name": "description"})
                hint = desc_tag.get("content", "")[:120] if desc_tag else ""
                url = f"/kb/vendors/{slug}"
                if title not in seen_ids:
                    seen_ids.add(title)
                    nodes_list.append({
                        "id": title,
                        "type": "vendor",
                        "tags": extract_tags(title + " " + hint, slug),
                        "hint": hint,
                        "url": url
                    })
            except Exception as e:
                pass

    # 7. Core Section Hubs
    hubs = [
        ("Knowledge Base Home", "Comprehensive index of CAD/BIM/CAE concepts and engineering terminology.", "/knowledge-base"),
        ("CAD Software Hub", "Browse 51 professional CAD, BIM, and CAM software platforms.", "/kb-software"),
        ("CAD Terminology Index", "254 atomic CAD terms arranged by alphabetical index.", "/kb-terms"),
        ("CAD Technical FAQ", "670 frequently asked questions spanning 20+ CAD tools.", "/kb-faq"),
        ("Interactive Knowledge Graph", "Visual force-directed map of CAD concepts and dependencies.", "/kb-graph"),
        ("Tutorial Navigation Library", "168 curated courses across YouTube, Coursera, and official academies.", "/tutorials"),
        ("CAD & AEC Industry News", "123 curated articles covering AI, standards, and new software releases.", "/news"),
        ("Engineering PDF Library", "Curated textbook extracts and chapter summaries.", "/knowledge-library"),
        ("CAD Skills Challenge Quiz", "Interactive CAD quiz testing multi-discipline skills.", "/quiz"),
        ("About Gstarcademy", "Project mission, editorial team, and peer-review process.", "/about"),
        ("Editorial Process & Sources", "Peer review guidelines, sourcing policies, and E-E-A-T criteria.", "/editorial-process"),
        ("CADGuide.tools Engineering Toolbox & Comparison", "560+ client-side engineering calculators (gears, hydraulics, beams, Ohm's law) and independent CAD/BIM software comparisons.", "/cadguide-tools"),
    ]
    for h_title, h_hint, h_url in hubs:
        if h_title not in seen_ids:
            seen_ids.add(h_title)
            tags = ["hub", "portal", "navigation"]
            if "cadguide" in h_url:
                tags = ["cadguide", "tools", "toolbox", "calculator", "compare", "matchmaker"]
            nodes_list.append({
                "id": h_title,
                "type": "hub",
                "tags": tags,
                "hint": h_hint,
                "url": h_url
            })

    # 8. Premium Tutorials
    prem_file = REPO / "data" / "tutorials_premium.json"
    if prem_file.exists():
        for t in json.loads(prem_file.read_text(encoding="utf-8")):
            title = t.get("title", "")
            if title and title not in seen_ids:
                seen_ids.add(title)
                nodes_list.append({
                    "id": title,
                    "type": "tutorial",
                    "tags": t.get("tags", ["tutorial"]),
                    "hint": t.get("editorial_note", "")[:120],
                    "url": f"/tutorials?search={t.get('software', '')}"
                })

    # 9. YouTube Tutorials
    yt_file = REPO / "data" / "tutorials_youtube.json"
    if yt_file.exists():
        yt_obj = json.loads(yt_file.read_text(encoding="utf-8"))
        for v in yt_obj.get("videos", []):
            title = v.get("title", "")
            if title and title not in seen_ids:
                seen_ids.add(title)
                nodes_list.append({
                    "id": title,
                    "type": "tutorial",
                    "tags": [v.get("software", "cad"), v.get("task", "tutorial"), "youtube"],
                    "hint": v.get("description", "")[:120],
                    "url": f"/tutorials?search={v.get('software', '')}"
                })

    # 10. Industry News
    news_file = REPO / "data" / "news.json"
    if news_file.exists():
        for n in json.loads(news_file.read_text(encoding="utf-8")):
            title = n.get("title", "")
            if title and title not in seen_ids:
                seen_ids.add(title)
                nodes_list.append({
                    "id": title,
                    "type": "news",
                    "tags": n.get("tags", ["news"]),
                    "hint": n.get("summary", "")[:120],
                    "url": f"/news#{n.get('id', '')}"
                })

    SEARCH_NODES_JSON.parent.mkdir(parents=True, exist_ok=True)
    SEARCH_NODES_JSON.write_text(json.dumps(nodes_list, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Successfully compiled {len(nodes_list)} full-site search entities into {SEARCH_NODES_JSON.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
