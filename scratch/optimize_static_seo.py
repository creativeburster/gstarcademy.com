import pathlib
import os
import re

def process_file(file_path: pathlib.Path, root_dir: pathlib.Path):
    rel_path = file_path.relative_to(root_dir)
    rel_path_str = str(rel_path).replace("\\", "/")
    
    # Skip generated directories to avoid double-processing (we only process core handwritten pages)
    # Allow kb/software/index.html but skip the software profile pages
    if "kb/concepts/" in rel_path_str or "kb/vendors/" in rel_path_str or ("kb/software/" in rel_path_str and not rel_path_str.endswith("index.html")):
        # Skip them
        return
        
    print(f"Optimizing static page: {rel_path_str}")
    content = file_path.read_text(encoding="utf-8")
    
    # Calculate depth relative path prefix (relpath)
    depth = len(rel_path.parent.parts)
    if depth == 0:
        relpath = "./"
    else:
        relpath = "../" * depth

    # --- 1. Replace Footer Dead Links ---
    # We replace both ./kb/concepts/ and ../../kb/concepts/ styles
    footer_replacements = {
        "intelligent-objects.html": "kb-terms.html",
        "bim.html": "kb/concepts/bim-workbench.html",
        "parametric-constraints.html": "kb/concepts/constraints-fusion.html",
        "command-alias.html": "kb/concepts/dynamic-input.html",
        "drawing-merge.html": "kb/concepts/dwg-file-format.html",
        "dwg-compare.html": "kb/concepts/file-comparison-zw.html",
        "layer.html": "kb/concepts/layers-gstarcad.html",
        "xref.html": "kb/concepts/dynamic-blocks-autocad.html"
    }
    
    # Perform string replacements for both root and subfolder links
    for old_file, new_file in footer_replacements.items():
        # Case A: ./kb/concepts/old_file -> ./new_file
        content = content.replace(f'href="./kb/concepts/{old_file}"', f'href="{relpath}{new_file}"')
        content = content.replace(f'href="kb/concepts/{old_file}"', f'href="{relpath}{new_file}"')
        # Case B: ../../kb/concepts/old_file -> ../../new_file (e.g. from subdirectories)
        content = content.replace(f'href="../../kb/concepts/{old_file}"', f'href="{relpath}{new_file}"')

    # --- 2. Heading Upgrades H3 -> H1 (Only for specific knowledge pages) ---
    is_knowledge_hub = rel_path_str in [
        "knowledge-cax.html", "knowledge-curriculum.html", "knowledge-domains.html",
        "knowledge-library.html", "knowledge-roadmap.html"
    ]
    if is_knowledge_hub:
        # Replace <div class="kb-section-head">\n                <h3>...</h3> with <h1>
        pattern = re.compile(r'(<div class="kb-section-head">\s*)<h3>(.*?)</h3>', re.DOTALL)
        content, count = pattern.subn(r'\1<h1>\2</h1>', content)
        print(f"  Upgraded {count} main headings to <h1>")

    # --- 3. Inject EEAT Byline Trust Signatures ---
    eeat_pages = [
        "about.html", "kb-graph.html", "knowledge-base.html", "knowledge-cax.html",
        "knowledge-curriculum.html", "knowledge-domains.html", "knowledge-library.html",
        "knowledge-roadmap.html", "quiz.html", "tutorials.html", "kb/software/index.html"
    ]
    if rel_path_str in eeat_pages:
        # Check if already contains byline
        if "ink-byline" not in content and "Author:" not in content:
            byline_html = f"""
            <div class="ink-byline" style="margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--ink-line); font-size: 13px; display: flex; flex-wrap: wrap; gap: 16px; color: var(--ink-text-muted);">
              <span><strong>Author:</strong> Gstarcademy Editorial Board</span>
              <span><strong>Reviewer:</strong> Gstarcademy Technical Review Committee</span>
              <span><strong>Last reviewed:</strong> <time datetime="2026-06-14">June 2026</time></span>
              <span><a href="{relpath}about.html#editorial-process" style="color: var(--ink-text-muted); text-decoration: underline;">Editorial Process</a></span>
            </div>
            """
            # Insert before </main> or </div> <!-- End kb-main --> or before </footer>
            if "</main>" in content:
                content = content.replace("</main>", f"{byline_html}\n    </main>", 1)
                print("  Injected EEAT Trust Byline before </main>")
            elif "</div> <!-- End kb-main -->" in content:
                content = content.replace("</div> <!-- End kb-main -->", f"{byline_html}\n            </div> <!-- End kb-main -->", 1)
                print("  Injected EEAT Trust Byline before kb-main closer")
            elif "</footer>" in content:
                content = content.replace("</footer>", f"{byline_html}\n    </footer>", 1)
                print("  Injected EEAT Trust Byline before </footer>")

    # --- 4. Robots Noindex Configuration for Redirects / Service pages ---
    if rel_path_str == "kb-vendors.html":
        # Replace robots meta tag
        content = content.replace(
            '<meta name="robots" content="index, follow, max-image-preview:large" />',
            '<meta name="robots" content="noindex, follow" />'
        )
        print("  Marked kb-vendors.html as noindex, follow")
        
    if rel_path_str == "offline.html":
        # Ensure robots noindex is set
        if 'name="robots"' not in content:
            content = content.replace(
                '<head>',
                '<head>\n    <meta name="robots" content="noindex, nofollow" />'
            )
            print("  Injected noindex, nofollow into offline.html head")
        # Ensure canonical tag is set
        if 'rel="canonical"' not in content:
            content = content.replace(
                '<head>',
                f'<head>\n    <link rel="canonical" href="https://learncad.io/offline.html" />'
            )
            print("  Injected canonical link into offline.html head")
            
    # --- 5. Term page Starter Cards link replacement with Letter Anchors ---
    if rel_path_str == "kb-terms.html":
        # Match cards with non-existent concept pages
        # e.g., <a href="./kb/concepts/layer.html" class="kb-card-link"> ... data-title="Layer"
        card_pattern = re.compile(
            r'(<a\s+href="\./kb/concepts/[^"]+\.html"\s+class="kb-card-link">\s*<article[^>]+data-title="([^"]+)")',
            re.DOTALL
        )
        
        def replace_card(m):
            full_match = m.group(1)
            title = m.group(2)
            first_char = title[0].upper()
            # Replace href="./kb/concepts/xxx.html" with href="#letter-{first_char}"
            new_match = re.sub(r'href="\./kb/concepts/[^"]+\.html"', f'href="#letter-{first_char}"', full_match)
            return new_match
            
        new_content, count = card_pattern.subn(replace_card, content)
        if count > 0:
            content = new_content
            print(f"  Re-routed {count} Starter Card dead links to smooth alphabetical anchors (e.g. #letter-L)")

        # Replace the remaining 5 static non-existent concept links in kb-terms.html lists
        content = content.replace('href="./kb/concepts/dynamic-blocks.html"', 'href="./kb/concepts/dynamic-blocks-gstarcad.html"')
        content = content.replace('href="./kb/concepts/annotative-scaling.html"', 'href="./kb/concepts/annotative-objects.html"')
        content = content.replace('href="./kb/concepts/block.html"', 'href="./kb/concepts/attributes-blocks.html"')
        content = content.replace('href="./kb/concepts/point-cloud-decimation.html"', 'href="./kb/concepts/gstarcad-point-cloud-term-1.html"')
        content = content.replace('href="./kb/concepts/licensing.html"', 'href="./kb/concepts/flexnet-floating.html"')
        print("  Replaced remaining 5 static dead links in kb-terms.html")

    file_path.write_text(content, encoding="utf-8")

def main():
    root = pathlib.Path("f:/CAD-tutorial")
    html_files = list(root.glob("*.html")) + list((root / "kb" / "software").glob("*.html"))
    
    for f in html_files:
        process_file(f, root)
    print("Optimization completed!")

if __name__ == "__main__":
    main()
