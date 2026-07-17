import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB_TERMS_PATH = ROOT / "kb-terms.html"

def extract_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
    if m:
        t = m.group(1).strip()
        # Clean title suffix
        for sep in [" · Gstarcademy", " — Gstarcademy", " - Gstarcademy", " | Gstarcademy"]:
            if sep in t:
                t = t.split(sep, 1)[0]
                break
        return t
    return ""

def scan_links():
    links = []
    scan_dirs = [
        ("kb/concepts", "./kb/concepts/"),
        ("kb/software", "./kb/software/"),
        ("kb/vendors", "./kb/vendors/"),
        ("kb/guides", "./kb/guides/"),
        ("kb/learning-paths", "./kb/learning-paths/")
    ]
    
    for folder_rel, href_prefix in scan_dirs:
        folder = ROOT / folder_rel
        if not folder.exists():
            continue
            
        for f in sorted(folder.glob("*.html")):
            if f.name == "index.html":
                continue
                
            try:
                html = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                html = f.read_text(encoding="utf-8-sig")
                
            title = extract_title(html) or f.stem.replace("-", " ").title()
            href = f"{href_prefix}{f.name}"
            links.append(f'      <a href="{href}">{title}</a>')
            
    return links

def main():
    if not KB_TERMS_PATH.exists():
        print(f"Error: {KB_TERMS_PATH} not found.")
        return
        
    print("Scanning all static HTML files to build fallback links...")
    links = scan_links()
    print(f"Found {len(links)} links to inject.")
    
    # Build fallback markup
    fallback_content = (
        "  <!-- START_STATIC_FALLBACK_LINKS -->\n"
        "  <noscript>\n"
        "    <div class=\"static-fallback-links\" style=\"display:none;\" aria-hidden=\"true\">\n"
        "      " + "\n      ".join(links) + "\n"
        "    </div>\n"
        "  </noscript>\n"
        "  <!-- END_STATIC_FALLBACK_LINKS -->"
    )
    
    html = KB_TERMS_PATH.read_text(encoding="utf-8")
    
    # Match existing block if present
    pattern = re.compile(
        r"<!-- START_STATIC_FALLBACK_LINKS -->.*?<!-- END_STATIC_FALLBACK_LINKS -->",
        re.DOTALL
    )
    
    if pattern.search(html):
        html = pattern.sub(fallback_content, html)
        print("Updated existing fallback links block in kb-terms.html.")
    else:
        # Insert before </body>
        if "</body>" in html:
            html = html.replace("</body>", f"{fallback_content}\n</body>", 1)
            print("Injected fallback links block before </body> in kb-terms.html.")
        else:
            html += f"\n{fallback_content}"
            print("Appended fallback links block to the end of kb-terms.html.")
            
    KB_TERMS_PATH.write_text(html, encoding="utf-8")
    print("Done!")

if __name__ == "__main__":
    main()
