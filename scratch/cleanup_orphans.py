import glob
import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SW_DIR = REPO / "data" / "sw"
VERCEL_JSON_PATH = REPO / "vercel.json"

def main():
    # 1. Identify active slugs
    json_files = glob.glob(str(SW_DIR / "*.json"))
    active_concept_slugs = set()
    active_sw_slugs = set()
    active_vendor_slugs = set()

    for f in json_files:
        try:
            with open(f, encoding="utf-8") as file:
                data = json.load(file)
                active_sw_slugs.add(data["slug"])
                if "vendor" in data and "slug" in data["vendor"]:
                    active_vendor_slugs.add(data["vendor"]["slug"])
                for t in data.get("terms", []):
                    active_concept_slugs.add(t["slug"])
        except Exception as e:
            print(f"Error loading {f}: {e}")

    # 2. Identify physical HTML files
    html_concepts = {os.path.basename(f).replace(".html", ""): Path(f) for f in glob.glob(str(REPO / "kb/concepts/*.html"))}
    html_software = {os.path.basename(f).replace(".html", ""): Path(f) for f in glob.glob(str(REPO / "kb/software/*.html")) if os.path.basename(f) != "index.html"}
    html_vendors = {os.path.basename(f).replace(".html", ""): Path(f) for f in glob.glob(str(REPO / "kb/vendors/*.html"))}

    # 3. Identify legacy/orphaned files
    legacy_concepts = {slug: path for slug, path in html_concepts.items() if slug not in active_concept_slugs}
    legacy_software = {slug: path for slug, path in html_software.items() if slug not in active_sw_slugs}
    legacy_vendors = {slug: path for slug, path in html_vendors.items() if slug not in active_vendor_slugs}

    print(f"Found {len(legacy_concepts)} legacy concept HTML files.")
    print(f"Found {len(legacy_software)} legacy software HTML files.")
    print(f"Found {len(legacy_vendors)} legacy vendor HTML files.")

    # 4. Generate Vercel redirects to prevent 404s
    redirects = []
    
    # Redirect legacy concepts to the glossary page
    for slug in sorted(legacy_concepts.keys()):
        redirects.append({
            "source": f"/kb/concepts/{slug}.html",
            "destination": "/knowledge-glossary.html",
            "permanent": True
        })
        
    # Redirect legacy software pages to the software landscape index page
    for slug in sorted(legacy_software.keys()):
        redirects.append({
            "source": f"/kb/software/{slug}.html",
            "destination": "/kb-software.html",
            "permanent": True
        })

    # Redirect legacy vendors to the vendor documentation hubs
    for slug in sorted(legacy_vendors.keys()):
        redirects.append({
            "source": f"/kb/vendors/{slug}.html",
            "destination": "/kb-vendors.html",
            "permanent": True
        })

    # 5. Patch vercel.json
    if VERCEL_JSON_PATH.is_file():
        try:
            config = json.loads(VERCEL_JSON_PATH.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Error parsing vercel.json: {e}")
            config = {}
    else:
        config = {}

    config["redirects"] = redirects

    VERCEL_JSON_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Patched vercel.json with {len(redirects)} redirects to prevent 404 errors.")

    # 6. Delete legacy files
    deleted_concepts = 0
    for slug, path in legacy_concepts.items():
        try:
            path.unlink()
            deleted_concepts += 1
        except Exception as e:
            print(f"Failed to delete {path}: {e}")

    deleted_software = 0
    for slug, path in legacy_software.items():
        try:
            path.unlink()
            deleted_software += 1
        except Exception as e:
            print(f"Failed to delete {path}: {e}")

    deleted_vendors = 0
    for slug, path in legacy_vendors.items():
        try:
            path.unlink()
            deleted_vendors += 1
        except Exception as e:
            print(f"Failed to delete {path}: {e}")

    print(f"Deleted files: {deleted_concepts} concepts, {deleted_software} software pages, {deleted_vendors} vendors.")
    return 0

if __name__ == "__main__":
    main()
