"""Enrich the 3 guides with words around 160-199 to ensure all guides are 350+ words."""
from pathlib import Path
from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parents[1]
GUIDES_DIR = REPO_ROOT / "kb" / "guides"

GUIDES_DATA = {
    "mfg-sheetmetal-and-bom-migration": {
        "sec3": """
<section class="kb-concept-section">
  <h2>3. Legacy AutoCAD Mechanical (ACM) Drawing Migration</h2>
  <p>GstarCAD Mechanical natively opens and parses drawings authored in AutoCAD Mechanical without requiring proxy object conversions or data flattening:</p>
  <ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
    <li><strong>Native Part References:</strong> Existing ACM part references, user-defined attributes, and standard fastener definitions retain their dynamic editing capabilities.</li>
    <li><strong>Title Block & Border Synchronization:</strong> Standard drawing borders dynamically read project metadata, synchronizing scale changes across drawing title sheets.</li>
    <li><strong>Hole Charts & Fits:</strong> Automated hole tables categorize drilling, reaming, and counterboring coordinates with real-time associative updates when hole clusters move.</li>
  </ul>
</section>
<section class="kb-concept-section">
  <h2>4. BOM Integrity & Multi-Level Assembly Best Practices</h2>
  <p>To ensure flawless ERP integration: verify that assembly drawings enforce hierarchical part parentage rather than loose disconnected blocks; utilize the <code>GMCONFIG</code> command to align custom title block tags with company ERP field definitions; and export structured XML or CSV manifests directly into production management software.</p>
</section>
""",
    },
    "aec-dwg-worksharing-and-xrefs-migration": {
        "sec3": """
<section class="kb-concept-section">
  <h2>3. Sheet Set Manager (DST) Enterprise Publishing</h2>
  <p>Collaborative multi-discipline architectural delivery relies on unified Sheet Set Manager (.dst) databases:</p>
  <ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
    <li><strong>Centralized Project Fields:</strong> Updating the project title, revision date, or issue code in the Sheet Set Manager automatically synchronizes across 100+ drawing layout title blocks.</li>
    <li><strong>Automated Sheet Indexing:</strong> Dynamic callout blocks and automated sheet lists compile drawing deliverable tables without manual data entry.</li>
    <li><strong>Batch PDF Publishing:</strong> Background publishing outputs multi-page, searchable vector PDF sets with layer structures preserved for contractor review.</li>
  </ul>
</section>
<section class="kb-concept-section">
  <h2>4. Network Storage Latency & Reference Governance</h2>
  <p>When hosting DWG files on shared enterprise NAS or cloud drives: enforce 'Overlay' instead of 'Attach' to eliminate recursive reference loops; standardize relative path mappings (<code>.\\Xrefs\\</code>) rather than absolute drive letters; and schedule weekly automated scripts to audit and purge unregistered application dictionaries (RegApps) from all referenced base drawings.</p>
</section>
""",
    },
    "civil-plant-piping-dwg-migration": {
        "sec3": """
<section class="kb-concept-section">
  <h2>3. Multi-Core Graphics Acceleration & 100MB+ DWG Performance</h2>
  <p>Municipal utility networks and civil piping drawings frequently exceed 100MB, containing millions of vector coordinates that overwhelm legacy single-threaded CAD engines:</p>
  <ul style="line-height:1.8; color:var(--ink-text-soft); padding-left:20px;">
    <li><strong>Parallel Graphics Pipeline:</strong> GstarCAD leverages multi-core CPU architecture to distribute entity regeneration, viewport culling, and spatial index searches across available threads.</li>
    <li><strong>Hardware OpenGL Optimization:</strong> Accelerated GPU pipelines buffer dense polyline meshes directly in dedicated VRAM, maintaining 60 FPS pan and zoom speeds.</li>
    <li><strong>Memory Management:</strong> 64-bit address allocation prevents 'Out of Memory' crashes during massive coordinate transforms or batch plot runs.</li>
  </ul>
</section>
<section class="kb-concept-section">
  <h2>4. Coordinate System Integrity & Geo-Referencing Hygiene</h2>
  <p>Large infrastructure plant drawings must anchor to true geographic coordinate reference systems (State Plane or UTM): align the User Coordinate System (UCS) with survey baselines; verify that large background aerial ECW/GeoTIFF images use spatial clipping boundaries; and freeze dense topographic contour layers during real-time piping routing to maximize viewport responsiveness.</p>
</section>
""",
    }
}

def run():
    for name, data in GUIDES_DATA.items():
        file_path = GUIDES_DIR / f"{name}.html"
        if not file_path.exists():
            print(f"File not found: {file_path}")
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        soup = BeautifulSoup(content, "html.parser")
        article = soup.find("article", class_="kb-concept-detail")
        sections = article.find_all("section", class_="kb-concept-section")
        # resource section is the last one
        resource_sec = sections[-1]
        extra_soup = BeautifulSoup(data["sec3"], "html.parser")
        resource_sec.insert_before(extra_soup)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Enriched guide: {name}.html")

if __name__ == "__main__":
    run()
