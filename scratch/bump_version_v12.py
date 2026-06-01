import sys
from pathlib import Path

ROOT = Path("f:/CAD-tutorial")
OLD_VER = "v11_cad_graph_stability"
NEW_VER = "v12_roadmap_sorting_credibility"

def main():
    changed = []
    # 1. Update build_software_content.py
    generator_file = ROOT / "scripts" / "build_software_content.py"
    if generator_file.is_file():
        txt = generator_file.read_text(encoding="utf-8")
        if f'CSS_VER = "{OLD_VER}"' in txt:
            txt = txt.replace(f'CSS_VER = "{OLD_VER}"', f'CSS_VER = "{NEW_VER}"')
            generator_file.write_text(txt, encoding="utf-8")
            print(f"Updated CSS_VER in build_software_content.py.")
            
    # 2. Search for all HTML files and replace query params
    for path in ROOT.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if f"?v={OLD_VER}" in text:
            text = text.replace(f"?v={OLD_VER}", f"?v={NEW_VER}")
            path.write_text(text, encoding="utf-8")
            changed.append(path)
                
    print(f"Bumped cache version in {len(changed)} HTML files to {NEW_VER}.")
    for p in changed:
        print(" -", p.relative_to(ROOT))

if __name__ == "__main__":
    main()
