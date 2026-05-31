import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

FILES_TO_PATCH = [
    # Root level
    ("about.html", "."),
    ("contact.html", "."),
    ("kb-faq.html", "."),
    ("kb-graph.html", "."),
    ("kb-software.html", "."),
    ("kb-terms.html", "."),
    ("knowledge-base.html", "."),
    ("knowledge-cax.html", "."),
    ("knowledge-roadmap.html", "."),
    ("knowledge-library.html", "."),
    ("knowledge-curriculum.html", "."),
    ("knowledge-glossary.html", "."),
    ("knowledge-domains.html", "."),
    ("legal.html", "."),
    ("privacy.html", "."),
    ("terms.html", "."),
    ("tutorial-detail.html", "."),
    ("topic.html", "."),
    ("editorial-process.html", "."),
    # Sub directories
    ("kb/software/index.html", "../.."),
    ("kb/pilot/autocad/index.html", "../../.."),
    ("kb/pilot/autocad/qa.html", "../../.."),
]

def patch_file(relative_path: str, root_rel: str):
    file_path = REPO / relative_path
    if not file_path.is_file():
        print(f"Skipping {relative_path} (does not exist)")
        return
        
    content = file_path.read_text(encoding="utf-8")
    
    modified = False
    manifest_tag = f'<link rel="manifest" href="{root_rel}/manifest.json" />'
    search_tag = f'<script src="{root_rel}/search.js" defer></script>'
    
    # Check if manifest tag is already there
    has_manifest = "manifest.json" in content
    has_search = "search.js" in content
    
    inject_lines = []
    if not has_manifest:
        inject_lines.append(f"    {manifest_tag}")
    if not has_search:
        inject_lines.append(f"    {search_tag}")
        
    if inject_lines:
        # Inject right before </head>
        needle = "</head>"
        if needle in content:
            replacement = "\n".join(inject_lines) + "\n  " + needle
            content = content.replace(needle, replacement, 1)
            modified = True
            
    if modified:
        file_path.write_text(content, encoding="utf-8")
        print(f"Patched {relative_path} with PWA & Search tags")
    else:
        print(f"No changes needed for {relative_path}")

def main():
    print("Starting PWA headers injection...")
    for rel_path, root_rel in FILES_TO_PATCH:
        patch_file(rel_path, root_rel)
    print("Done!")

if __name__ == "__main__":
    main()
