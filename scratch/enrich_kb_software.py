import json
import glob
import re
import os

def load_sw_data():
    software_list = []
    files = glob.glob("data/sw/*.json")
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            software_list.append(json.load(file))
    return software_list

def main():
    software_list = load_sw_data()
    
    # 1. Prepare manual stubs to merge
    manual_stubs = [
        {
            "slug": "fastview-3d",
            "name": "3D FastView",
            "vendor": {"name": "Gstarsoft"},
            "tagline": "High-performance 3D CAD visualization and markup tool supporting massive assemblies and 3D formats.",
            "tag": "3D Visualization",
            "icon": "🌐"
        },
        {
            "slug": "archicad",
            "name": "Archicad",
            "vendor": {"name": "GRAPHISOFT"},
            "tagline": "Pioneering BIM authoring platform tailored for architectural design, building models, and documentation.",
            "tag": "BIM / AEC",
            "icon": "🏢"
        },
        {
            "slug": "dwg-fastview",
            "name": "DWG FastView",
            "vendor": {"name": "Gstarsoft"},
            "tagline": "Viewing, editing, and sharing DWG drawings across mobile devices, tablets, and web browsers.",
            "tag": "Mobile / Web CAD",
            "icon": "📱"
        },
        {
            "slug": "dwg-fastview-plus",
            "name": "DWG FastView Plus",
            "vendor": {"name": "Gstarsoft"},
            "tagline": "Fast, lightweight desktop DWG viewer with advanced measurement, comparison, and print capabilities.",
            "tag": "Lightweight CAD Viewer",
            "icon": "🖥️"
        },
        {
            "slug": "gstarbim",
            "name": "GstarBIM",
            "vendor": {"name": "Gstarsoft"},
            "tagline": "Autodesk Revit compatible BIM design and documentation add-on specifically optimized for GstarCAD.",
            "tag": "BIM / AEC",
            "icon": "🏢"
        },
        {
            "slug": "gstarcad-365",
            "name": "GstarCAD 365",
            "vendor": {"name": "Gstarsoft"},
            "tagline": "Collaborative drawing and cloud file sharing platform specifically integrated for GstarCAD ecosystems.",
            "tag": "Cloud CAD / SaaS",
            "icon": "☁️"
        },
        {
            "slug": "gstarcad-architecture",
            "name": "GstarCAD Architecture",
            "vendor": {"name": "Gstarsoft"},
            "tagline": "Tailored architectural CAD package driven by custom 3D parametric components and schedules.",
            "tag": "Architectural CAD",
            "icon": "🏛️"
        },
        {
            "slug": "gstarcad-mechanical",
            "name": "GstarCAD Mechanical",
            "vendor": {"name": "Gstarsoft"},
            "tagline": "Standardized mechanical design vertical offering dynamic BOM lists, bubbles, and parts libraries.",
            "tag": "Mechanical CAD",
            "icon": "🔧"
        },
        {
            "slug": "gstarcad-point-cloud",
            "name": "GstarCAD Point Cloud",
            "vendor": {"name": "Gstarsoft"},
            "tagline": "High-density laser scan data rendering and vectorization add-on natively running inside GstarCAD.",
            "tag": "3D Scanning / CAD",
            "icon": "☁️"
        },
        {
            "slug": "houseplan",
            "name": "Houseplan",
            "vendor": {"name": "Gstarsoft"},
            "tagline": "Lightweight, ultra-fast 3D home floor planning, scene building, and conceptual rendering tool.",
            "tag": "3D Design / Home",
            "icon": "🏡"
        },
        {
            "slug": "onshape",
            "name": "Onshape",
            "vendor": {"name": "PTC"},
            "tagline": "The premier cloud-native parametric 3D CAD platform with built-in version control and team sharing.",
            "tag": "Cloud MCAD / PLM",
            "icon": "☁️"
        }
    ]

    # Map icons to slugs for compiled software
    slug_icons = {
        "autocad": "📐",
        "revit": "🏙️",
        "fusion-360": "⚙️",
        "inventor": "🛠️",
        "civil-3d": "🛣️",
        "solidworks": "🗳️",
        "catia": "✈️",
        "creo-parametric": "🔩",
        "siemens-nx": "🌀",
        "bricscad": "⚡",
        "freecad": "🔓",
        "zwcad": "💫",
        "draftsight": "✏️",
        "sketchup": "🏡",
        "tekla-structures": "🏗️",
        "microstation": "🛤️",
        "vectorworks": "🎨",
        "allplan": "🏢",
        "ares-commander": "💻",
        "alibre-design": "🔧",
        "ironcad": "🧱",
        "rhinoceros": "🦦",
        "aveva-e3d": "🏭",
        "spaceclaim": "🛸",
        "gstarcad": "🎨"
    }

    # Map tags to slugs for compiled software
    slug_tags = {
        "autocad": "2D/3D Drafting",
        "revit": "BIM / AEC",
        "fusion-360": "Cloud MCAD / CAM",
        "inventor": "Parametric 3D MCAD",
        "civil-3d": "Civil Infrastructure",
        "solidworks": "Parametric 3D MCAD",
        "catia": "High-End PLM / MCAD",
        "creo-parametric": "High-End Parametric MCAD",
        "siemens-nx": "High-End MCAD / CAM",
        "bricscad": "DWG-Native CAD / BIM",
        "freecad": "Open-Source 3D MCAD",
        "zwcad": "DWG-Native CAD",
        "draftsight": "Professional 2D CAD",
        "sketchup": "3D Modeling / Design",
        "tekla-structures": "BIM / Structural",
        "microstation": "Civil Infrastructure",
        "vectorworks": "BIM / AEC / Landscape",
        "allplan": "BIM / Structural",
        "ares-commander": "DWG-Native CAD",
        "alibre-design": "Parametric 3D MCAD",
        "ironcad": "Innovative 3D MCAD",
        "rhinoceros": "NURBS Modeling",
        "aveva-e3d": "Industrial Plant BIM",
        "spaceclaim": "Direct 3D Modeling",
        "gstarcad": "DWG-Native CAD"
    }

    # Compile the final card list
    cards = []
    # Add manual stubs
    for stub in manual_stubs:
        cards.append(stub)
        
    # Add compiled software
    for sw in software_list:
        slug = sw["slug"]
        # Skip if already manual stub (should not happen, but safeguard)
        if any(c["slug"] == slug for c in cards):
            continue
            
        icon = slug_icons.get(slug, "🛠️")
        tag = slug_tags.get(slug, "CAD Engineering")
        
        cards.append({
            "slug": slug,
            "name": sw["name"],
            "vendor": sw["vendor"],
            "tagline": sw["tagline"],
            "tag": tag,
            "icon": icon
        })
        
    # Sort cards alphabetically by name
    cards.sort(key=lambda x: x["name"].lower())
    
    # 2. Render cards HTML
    cards_html = []
    for c in cards:
        html = f"""                  <div class="kb-software-card">
                    <div>
                      <div class="kb-software-card-header">
                        <div class="kb-software-card-icon" aria-hidden="true">{c['icon']}</div>
                        <div>
                          <h3 class="kb-software-card-title">{c['name']}</h3>
                          <span class="kb-software-card-vendor">{c['vendor']['name']}</span>
                        </div>
                      </div>
                      <p class="kb-software-card-body">{c['tagline']}</p>
                    </div>
                    <div>
                      <span class="kb-software-card-tag">{c['tag']}</span>
                      <div class="kb-software-card-footer">
                        <a href="./kb/software/{c['slug']}.html" class="kb-software-card-link">View Profile &rarr;</a>
                      </div>
                    </div>
                  </div>"""
        cards_html.append(html)
        
    grid_block = "\n".join(cards_html)
    
    # 3. Read and patch kb-software.html
    path = "kb-software.html"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        
    # Replace the card grid
    grid_start_needle = '<div class="kb-software-card-grid">'
    grid_end_needle = '</div>\n\n              </section>' # Wait, let's locate the ending uniquely
    
    # Let's search for the grid using regex
    pattern = re.compile(r'<div class="kb-software-card-grid">.*?</div>\s*</section>', re.DOTALL)
    match = pattern.search(text)
    if match:
        full_replacement = f'<div class="kb-software-card-grid">\n                  <!-- AUTO-GEN sw-grid START -->\n{grid_block}\n                  <!-- AUTO-GEN sw-grid END -->\n                </div>\n              </section>'
        text = pattern.sub(full_replacement, text)
        print("Patched card grid successfully!")
    else:
        # Fallback to simple replace if markers already present
        auto_pattern = re.compile(r'<!-- AUTO-GEN sw-grid START -->.*?<!-- AUTO-GEN sw-grid END -->', re.DOTALL)
        if auto_pattern.search(text):
            text = auto_pattern.sub(f'<!-- AUTO-GEN sw-grid START -->\n{grid_block}\n                  <!-- AUTO-GEN sw-grid END -->', text)
            print("Patched existing card grid markers successfully!")
        else:
            print("ERROR: Could not locate card grid container structure.")
            
    # 4. Patch Section 3: Interactive Matchmaker Script
    # Let's target the renderResults() method inside the script in kb-software.html.
    # We will replace the rendering options for 'aec/modeling', 'aec/drafting' standard, and 'mcad/modeling' standard.
    
    # Let's locate the 'aec' -> 'modeling' block
    aec_modeling_old = """                      } else if (state.goal === 'modeling') {
                        title = "3D AEC Modeler & Visualizer";
                        desc = "You require 3D spatial models. For quick home visualization, Gstarsoft Houseplan is extremely intuitive. For complete standard structural coordination, Revit is the market benchmark.";
                        recs = [
                          { name: "Revit", icon: "🏙️", reason: "Mainstream building database for architects to model fully coordinated 3D buildings.", link: "./kb/software/revit.html", search: "autodesk" },
                          { name: "Houseplan", icon: "🏡", reason: "Extremely fast, easy 3D floor plan layout, scene modeling, and light rendering.", link: "./kb/software/houseplan.html", search: "gstarsoft" }
                        ];"""
                        
    aec_modeling_new = """                      } else if (state.goal === 'modeling') {
                        title = "3D AEC Modeler & Visualizer";
                        desc = "For high-fidelity 3D conceptual modeling, Rhinoceros is unmatched. For structural BIM detailing, Tekla Structures is the global gold standard, while Revit serves as the master building database coordinator.";
                        recs = [
                          { name: "Revit", icon: "🏙️", reason: "Mainstream building database for architects to model fully coordinated 3D buildings.", link: "./kb/software/revit.html", search: "autodesk" },
                          { name: "Rhinoceros", icon: "🦦", reason: "Advanced NURBS modeler with generative Grasshopper programming interface.", link: "./kb/software/rhinoceros.html", search: "rhinoceros" },
                          { name: "Tekla Structures", icon: "🏗️", reason: "Industry-standard structural steel and concrete detailing BIM platform.", link: "./kb/software/tekla-structures.html", search: "trimble" }
                        ];"""
                        
    # Let's locate the 'aec' -> 'drafting' -> non-premium block
    aec_drafting_std_old = """                          title = "Smart & Economical 2D Designer";
                          desc = "If you want high-performance DWG drawing and construction drafts without premium seat licenses, GstarCAD Architecture offers an incredibly efficient CAD engine.";
                          recs = [
                            { name: "GstarCAD Architecture", icon: "🏛️", reason: "Supercharged architectural drafting vertical on dwg with custom parametric layouts.", link: "./kb/software/gstarcad-architecture.html", search: "gstarsoft" },
                            { name: "GstarCAD", icon: "🎨", reason: "Ultra-fast, lightweight 2D core program requiring fraction of hardware memory.", link: "./kb/software/gstarcad.html", search: "gstarsoft" }
                          ];"""
                          
    aec_drafting_std_new = """                          title = "Smart & Economical 2D Designer";
                          desc = "If you want high-performance DWG drawing and construction drafts without premium seat licenses, GstarCAD Architecture and ZWCAD offer extremely optimized CAD engines.";
                          recs = [
                            { name: "GstarCAD Architecture", icon: "🏛️", reason: "Supercharged architectural drafting vertical on dwg with custom parametric layouts.", link: "./kb/software/gstarcad-architecture.html", search: "gstarsoft" },
                            { name: "ZWCAD", icon: "💫", reason: "DWG-native, rapid multi-core rendering, C++ ZRX API compatible alternative.", link: "./kb/software/zwcad.html", search: "zwsoft" }
                          ];"""
                          
    # Let's locate the 'mcad' -> 'modeling' -> non-premium block
    mcad_modeling_std_old = """                          title = "Modern & Cost-Effective 3D Modeler";
                          desc = "For affordable or open-source mechanical modeling, Fusion 360 integrates complete CAD/CAM in the cloud. FreeCAD is fully open-source and free.";
                          recs = [
                            { name: "Fusion 360", icon: "⚙️", reason: "Cloud-connected, budget-friendly suite connecting CAD, generative design, and CAM.", link: "./kb/software/fusion-360.html", search: "autodesk" },
                            { name: "FreeCAD", icon: "🔓", reason: "100% free open-source parametric CAD modeler for students and hobbyists.", link: "./kb/software/freecad.html", search: "freecad" }
                          ];"""
                          
    mcad_modeling_std_new = """                          title = "Modern & Cost-Effective 3D Modeler";
                          desc = "For affordable or open-source mechanical modeling, Fusion 360 integrates complete CAD/CAM in the cloud. FreeCAD is fully free and open-source, while Alibre Design offers premium desktop parametrics.";
                          recs = [
                            { name: "Fusion 360", icon: "⚙️", reason: "Cloud-connected, budget-friendly suite connecting CAD, generative design, and CAM.", link: "./kb/software/fusion-360.html", search: "autodesk" },
                            { name: "FreeCAD", icon: "🔓", reason: "100% free open-source parametric CAD modeler for students and hobbyists.", link: "./kb/software/freecad.html", search: "freecad" },
                            { name: "Alibre Design", icon: "🔧", reason: "A buy-once-own-forever desktop parametric 3D CAD engine for mechanical designers.", link: "./kb/software/alibre-design.html", search: "alibre" }
                          ];"""

    if aec_modeling_old in text:
        text = text.replace(aec_modeling_old, aec_modeling_new)
        print("Updated AEC 3D Matchmaker recommendations.")
    else:
        print("Could not match AEC 3D Matchmaker block.")
        
    if aec_drafting_std_old in text:
        text = text.replace(aec_drafting_std_old, aec_drafting_std_new)
        print("Updated AEC 2D Standard Matchmaker recommendations.")
    else:
        print("Could not match AEC 2D Standard Matchmaker block.")
        
    if mcad_modeling_std_old in text:
        text = text.replace(mcad_modeling_std_old, mcad_modeling_std_new)
        print("Updated MCAD 3D Standard Matchmaker recommendations.")
    else:
        print("Could not match MCAD 3D Standard Matchmaker block.")

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
        
    print("kb-software.html enrichment complete!")

if __name__ == "__main__":
    main()
