import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# -*- coding: utf-8 -*-
"""
GitHub Gist (DA 96) Publisher for CAD Learn Hub using gh CLI
"""
import os
import sys
import subprocess
import tempfile
from tracker import add_backlink

def publish_github_gist(description, filename, content, target_url="https://gstarcademy.com"):
    print("=" * 60)
    print(f"🚀 Publishing public GitHub Gist (DA 96): {description}")
    print("=" * 60)
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=f"_{filename}", delete=False, encoding="utf-8") as tmp:
        tmp.write(content)
        tmp_path = tmp.name
        
    try:
        cmd = ["gh", "gist", "create", tmp_path, "-d", description, "--public"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        
        if res.returncode == 0:
            gist_url = res.stdout.strip()
            print(f"🎉 Gist created successfully! Live URL: {gist_url}")
            
            # Record backlink
            add_backlink(
                platform="GitHub Gist (Top Authority DA 96)",
                domain_authority="DA 96",
                category="Open-Source Technical Reference",
                post_title=description,
                target_url=target_url,
                backlink_url=gist_url,
                anchor_text="CAD Learn Hub: Interactive Knowledge & Certification Hub",
                link_type="Dofollow / Public Gist",
                status="Live",
                notes="Published as public reference gist via authenticated GitHub CLI"
            )
            return gist_url
        else:
            print(f"❌ Failed to create Gist: {res.stderr}")
            return None
    except Exception as e:
        print(f"❌ Error invoking gh: {e}")
        return None
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

if __name__ == "__main__":
    desc = "CAD & BIM Essential Standards Cheat Sheet (2026 Edition)"
    fname = "cad-standards-reference.md"
    content = """# CAD & BIM Essential Engineering Standards Cheat Sheet (2026)

A quick-reference guide covering core ISO, ASME, and AIA drafting standards for professional engineers and architectural technicians.

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
    publish_github_gist(desc, fname, content, target_url="https://gstarcademy.com/kb-terms.html")
