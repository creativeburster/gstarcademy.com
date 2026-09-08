import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# -*- coding: utf-8 -*-
"""
Dev.to (DA 90+) Publisher for CAD Learn Hub
"""
import os
import sys
import json
import urllib.request
from tracker import add_backlink

DEVTO_API_KEY = "hd31xweRq1x3qVmGwWfk1qXk"

def publish_devto_article(title, body_markdown, tags, series=None, canonical_url="https://gstarcademy.com"):
    print("=" * 60)
    print(f"🚀 Publishing article to Dev.to (DA 90+): {title}")
    print("=" * 60)
    
    article_data = {
        "article": {
            "title": title,
            "published": True,
            "body_markdown": body_markdown,
            "tags": tags,
            "canonical_url": canonical_url
        }
    }
    if series:
        article_data["article"]["series"] = series
        
    payload = json.dumps(article_data).encode("utf-8")
    req = urllib.request.Request("https://dev.to/api/articles", data=payload, headers={
        "api-key": DEVTO_API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CADLearnBot/1.0"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            live_url = data.get("url")
            print(f"🎉 Successfully published to Dev.to! Live URL: {live_url}")
            
            # Record backlink
            add_backlink(
                platform="Dev.to (Global Dev Community DA 90+)",
                domain_authority="DA 90+",
                category="Engineering & Architecture Blog",
                post_title=title,
                target_url=canonical_url,
                backlink_url=live_url,
                anchor_text="CAD Learn Hub: Interactive Learning Matrix & Benchmark",
                link_type="Dofollow / Editorial",
                status="Live",
                notes="Published via Dev.to Official API under certified author profile"
            )
            return live_url
    except Exception as e:
        print(f"❌ Failed to publish to Dev.to: {e}")
        if hasattr(e, "read"):
            print("Error response:", e.read().decode("utf-8", errors="ignore"))
        return None

if __name__ == "__main__":
    test_title = "Modern CAD Proficiency Benchmark: The 2026 Skill Roadmap for Draftspersons & Engineers"
    test_tags = ["cad", "engineering", "architecture", "webdev"]
    test_body = """# Modern CAD Proficiency Benchmark: The 2026 Skill Roadmap

Computer-Aided Design (CAD) workflows are undergoing massive transformations. From classical 2D orthographic projection and drafting standards to multi-discipline Building Information Modeling (BIM) and parametric mechanical assemblies, modern engineers require structured literacy.

---

## 🧭 The Six Core Disciplines of Modern CAD

1. **Architectural BIM**: Parametric family creation, LOD 300-400 modeling, and IFC open-standard coordination.
2. **Mechanical CAD (MCAD)**: Constraint-based sketches, feature-based solids, tolerance analysis, and GD&T per ASME Y14.5.
3. **Civil & Infrastructure**: Digital elevation modeling (DEM), corridor alignments, and volume cut/fill calculations.
4. **General 2D Drafting**: Precision geometry, layers, block management, and print sheet layout standards.
5. **Engineering Simulation (CAE/FEA)**: Finite element meshing, boundary conditions, and structural stress validation.
6. **Visualization & Rendering**: PBR material workflows, lighting, and real-time photorealistic presentation.

---

## 🚀 Free Diagnostic Benchmark & Career Roadmap

Whether transitioning from legacy AutoCAD workflows to modern parametric platforms like SolidWorks, Revit, or FreeCAD, evaluating proficiency across core concepts is essential.

You can take the complete interactive diagnostic evaluation with instant track progression at [CAD Learn Hub Interactive Career Quiz](https://gstarcademy.com/quiz.html).

Explore the full interactive graph topology of design concepts and software tools:
- **Interactive Career Skill Tree**: [https://gstarcademy.com/knowledge-roadmap.html](https://gstarcademy.com/knowledge-roadmap.html)
- **CAD & BIM Knowledge Topology**: [https://gstarcademy.com/kb-graph.html](https://gstarcademy.com/kb-graph.html)
- **Engineering Terminology Lexicon**: [https://gstarcademy.com/kb-terms.html](https://gstarcademy.com/kb-terms.html)
- **CAD Software Benchmark & Selection**: [https://gstarcademy.com/kb-software.html](https://gstarcademy.com/kb-software.html)

Continuous learning in technical drafting requires structured mastery. Keep honing your precision.
"""
    publish_devto_article(test_title, test_body, test_tags, canonical_url="https://gstarcademy.com/quiz.html")
