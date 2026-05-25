import os
import re

# Base directory of the workspace
base_dir = r"f:\CAD-tutorial"

def get_relative_prefix(file_path):
    # Calculate the depth of the file relative to base_dir
    rel_path = os.path.relpath(file_path, base_dir)
    parts = rel_path.split(os.sep)
    depth = len(parts) - 1
    if depth == 0:
        return "./"
    else:
        return "../" * depth

def generate_footer_html(prefix):
    return f"""<footer class="footer site-footer">
      <div class="container site-footer-inner">
        <div class="site-footer-brand">
          <p class="site-footer-tagline">Gstarcademy</p>
          <p class="site-footer-desc">CAD knowledge base and tutorial navigation. We link to high-quality, curated external CAD sources for AEC, MFG, and Civil Engineering professionals.</p>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Software Hubs</h4>
          <ul class="site-footer-links">
            <li><a href="{prefix}kb/software/autocad.html">AutoCAD Guide</a></li>
            <li><a href="{prefix}kb/software/revit.html">Revit Guide</a></li>
            <li><a href="{prefix}kb/software/fusion-360.html">Fusion 360</a></li>
            <li><a href="{prefix}kb/software/civil-3d.html">Civil 3D Guide</a></li>
            <li><a href="{prefix}kb/software/solidworks.html">SOLIDWORKS</a></li>
            <li><a href="{prefix}kb/software/catia.html">CATIA Guide</a></li>
            <li><a href="{prefix}kb/software/gstarcad.html">GstarCAD</a></li>
            <li><a href="{prefix}kb/software/inventor.html">Autodesk Inventor</a></li>
          </ul>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Technical Core</h4>
          <ul class="site-footer-links">
            <li><a href="{prefix}kb/concepts/intelligent-objects.html">2D Drafting</a></li>
            <li><a href="{prefix}kb/concepts/bim.html">BIM Coordination</a></li>
            <li><a href="{prefix}kb/concepts/parametric-constraints.html">Parametrics</a></li>
            <li><a href="{prefix}kb/concepts/command-alias.html">Command Line</a></li>
            <li><a href="{prefix}kb/concepts/drawing-merge.html">Drawing Merge</a></li>
            <li><a href="{prefix}kb/concepts/dwg-compare.html">DWG Compare</a></li>
            <li><a href="{prefix}kb/concepts/layer.html">Layer Strategy</a></li>
            <li><a href="{prefix}kb/concepts/xref.html">Xrefs &amp; Blocks</a></li>
          </ul>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Structured Learn</h4>
          <ul class="site-footer-links">
            <li><a href="{prefix}tutorials.html">Tutorial Library</a></li>
            <li><a href="{prefix}knowledge-base.html">Knowledge Center</a></li>
            <li><a href="{prefix}kb-graph.html">Interactive Graph</a></li>
            <li><a href="{prefix}knowledge-domains.html">Domain Map</a></li>
            <li><a href="{prefix}kb-software.html">Software Index</a></li>
            <li><a href="{prefix}kb-terms.html">CAD Glossary</a></li>
            <li><a href="{prefix}kb-faq.html">Technical FAQ</a></li>
          </ul>
        </div>
        <div class="site-footer-col">
          <h4 class="site-footer-heading">Company &amp; Legal</h4>
          <ul class="site-footer-links">
            <li><a href="{prefix}about.html">About Project</a></li>
            <li><a href="{prefix}contact.html">Contact Us</a></li>
            <li><a href="{prefix}privacy.html">Privacy Policy</a></li>
            <li><a href="{prefix}terms.html">Terms of Use</a></li>
            <li><a href="{prefix}legal.html">Copyright &amp; Disclaimer</a></li>
          </ul>
        </div>
      </div>
      <div class="container site-footer-bottom">
        <p>© <span id="footer-year"></span> Gstarcademy. All rights reserved.</p>
      </div>
    </footer>"""

def enrich_file_footer(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    prefix = get_relative_prefix(file_path)
    new_footer = generate_footer_html(prefix)
    
    # Locate <footer ...> ... </footer> using regex
    pattern = re.compile(r'<footer class="footer site-footer">.*?</footer>', re.DOTALL)
    
    if pattern.search(content):
        updated_content = pattern.sub(new_footer, content)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Updated footer in: {file_path} (Depth: {prefix})")
    else:
        print(f"No footer found in: {file_path}")

def main():
    for root, dirs, files in os.walk(base_dir):
        # Exclude common directories to speed up walking
        if ".git" in dirs:
            dirs.remove(".git")
        if ".gemini" in dirs:
            dirs.remove(".gemini")
            
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                enrich_file_footer(full_path)

if __name__ == "__main__":
    main()
