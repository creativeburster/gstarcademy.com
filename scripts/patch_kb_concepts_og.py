import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONCEPTS_DIR = ROOT / "kb" / "concepts"

def escape_html_attr(s: str) -> str:
    return s.replace('"', '&quot;')

def patch_file(file_path: Path) -> bool:
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = file_path.read_text(encoding="utf-8-sig")
        except Exception as e:
            print(f"Failed to read {file_path.name}: {e}")
            return False
            
    modified = False
    
    # 1. Check if we already patched it
    if 'property="og:image:width"' in content and 'name="twitter:image"' in content:
        return False
        
    # 2. Extract title and description
    title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "Gstarcademy"
    for sep in [" · Gstarcademy", " — Gstarcademy", " - Gstarcademy", " | Gstarcademy"]:
        if sep in title:
            title = title.split(sep, 1)[0]
            break
            
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content, re.IGNORECASE)
    desc = desc_match.group(1).strip() if desc_match else "CAD atomic concepts by Gstarcademy."
    
    # Escape quotes
    esc_title = escape_html_attr(title)
    esc_desc = escape_html_attr(desc)
    
    # 3. Inject og:image:width, og:image:height, twitter:image
    og_image_pattern = r'(<meta\s+property="og:image"\s+content="https://gstarcademy.com/images/og-default.webp"\s*/>)'
    if re.search(og_image_pattern, content):
        replace_with = (
            '\\1\n    <meta property="og:image:width" content="1200" />\n'
            '    <meta property="og:image:height" content="630" />\n'
            '    <meta name="twitter:image" content="https://gstarcademy.com/images/og-default.webp" />'
        )
        content, count = re.subn(og_image_pattern, replace_with, content, flags=re.IGNORECASE)
        if count > 0:
            modified = True
            
    # 4. Inject twitter:title and twitter:description after twitter:card
    twitter_card_pattern = r'(<meta\s+name="twitter:card"\s+content="summary_large_image"\s*/>)'
    if re.search(twitter_card_pattern, content):
        replace_with = (
            f'\\1\n    <meta name="twitter:title" content="{esc_title}" />\n'
            f'    <meta name="twitter:description" content="{esc_desc}" />'
        )
        content, count = re.subn(twitter_card_pattern, replace_with, content, flags=re.IGNORECASE)
        if count > 0:
            modified = True
            
    if modified:
        file_path.write_text(content, encoding="utf-8")
        return True
        
    return False

def main():
    dirs_to_scan = [
        ROOT / "kb" / "concepts",
        ROOT / "kb" / "software",
        ROOT / "kb" / "vendors",
        ROOT / "kb" / "guides",
        ROOT / "kb" / "learning-paths",
        ROOT / "kb" / "pilot"
    ]
    
    total_found = 0
    total_patched = 0
    
    for folder in dirs_to_scan:
        if not folder.exists():
            continue
            
        print(f"Scanning {folder.relative_to(ROOT)} for pages...")
        files = list(folder.glob("*.html"))
        print(f"Found {len(files)} files to check in {folder.name}.")
        
        folder_patched = 0
        for f in files:
            if patch_file(f):
                folder_patched += 1
                
        total_found += len(files)
        total_patched += folder_patched
        print(f"Patched {folder_patched} files in {folder.name}.")
        
    print(f"Completed! Patched {total_patched} files out of {total_found} total files.")

if __name__ == "__main__":
    main()
