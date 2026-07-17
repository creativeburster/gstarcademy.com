#!/usr/bin/env python3
"""
Fix template 'Market Position' and 'Learning Resources' text in 12 vendor pages.
Replaces generic fill-in-the-blank paragraphs with vendor-specific content.
"""

import re
from pathlib import Path

VENDORS_DIR = Path(r"f:\gstarcademy\kb\vendors")

# Vendor-specific replacement text for Market Position & Learning Resources sections.
# Key = filename stem, Value = (market_position_html, learning_resources_html)
VENDOR_FIXES = {
    "alibre": (
        '''<p>Alibre occupies the budget-conscious segment of the parametric MCAD market, competing primarily on price and perpetual licensing against subscription-based tools like SolidWorks and Inventor. The company targets independent engineers, small workshops, and hobbyists who need professional-grade solid modeling without annual maintenance fees.</p>
<p>While Alibre Design lacks the simulation, CAM, and PLM integration of enterprise platforms, its focused feature set covers the core mechanical design workflow — parametric sketching, solid modeling, sheet metal, assemblies, and 2D drawings — at a fraction of the cost. Users often adopt Alibre as a primary 3D tool alongside free 2D editors or cloud-based viewers for collaboration.</p>''',
        '''<p>Alibre provides learning resources through the <a href="https://www.alibre.com/learning-center/" rel="noopener noreferrer nofollow" target="_blank">Alibre Learning Center</a>, including video tutorials, written guides, and sample projects. The community forum is active for troubleshooting. Third-party courses are limited but growing on YouTube.</p>'''
    ),
    "allplan": (
        '''<p>Allplan competes in the BIM authoring space alongside Autodesk Revit and Graphisoft ArchiCAD, but differentiates through deep structural engineering and reinforcement detailing capabilities. Its strongest market presence is in German-speaking countries and European infrastructure projects where Eurocode compliance and precast-concrete workflows are critical.</p>
<p>As part of the Nemetschek Group, Allplan benefits from integration with Solibri (BIM quality checking) and Bluebeam (PDF collaboration) while supporting open BIM standards (IFC, BCF). Firms handling complex structural documentation — particularly precast and rebar — often choose Allplan over Revit for its superior detailing tools, supplementing with Revit or ArchiCAD for architectural coordination when needed.</p>''',
        '''<p>Allplan offers training through <a href="https://www.allplan.com/en/support/training" rel="noopener noreferrer nofollow" target="_blank">Allplan Academy</a> with role-based e-learning courses, classroom training, and certification programs. The Allplan Knowledgebase and community forum provide additional self-service resources.</p>'''
    ),
    "altium-ltd": (
        '''<p>Altium holds a strong position in the mid-to-professional PCB design market, competing with Cadence Allegro and Mentor Graphics (Siemens EDA) at a more accessible price point. The Altium 365 cloud platform extends the desktop tool with version control, design review, and supply-chain integration — a strategy that differentiates Altium from pure desktop EDA tools.</p>
<p>Altium Designer is widely used in electronics manufacturing companies that need professional schematic capture and PCB layout without the overhead of enterprise EDA suites. The unified environment (schematic + PCB + library management in one application) appeals to teams transitioning from entry-level tools like KiCad or Eagle. Users typically pair Altium Designer with MCAD tools (SolidWorks, Inventor) for mechanical-electronic co-design via STEP exports.</p>''',
        '''<p>Altium provides extensive learning resources through <a href="https://www.altium.com/education" rel="noopener noreferrer nofollow" target="_blank">Altium Education</a>, including free courses for students, the Altium Academy YouTube channel, and live webinars. The AltiumLive community forum is active for design questions and component library sharing.</p>'''
    ),
    "community": (
        '''<p>Open-source CAD tools occupy a unique market position: zero-cost alternatives to commercial software that lower barriers to entry for education, research, and small-scale professional work. FreeCAD and Blender have grown significantly in capability, with FreeCAD approaching mid-range MCAD functionality and Blender dominating open-source 3D modeling and rendering.</p>
<p>These projects thrive on community contributions — plugin development, documentation, and bug fixes — rather than corporate R&D budgets. Professionals often use open-source tools alongside commercial software: FreeCAD for quick modifications or scripting, Blender for visualization and rendering, and OpenFOAM for research-grade CFD where source-code access is essential. The lack of licensing costs makes them ideal for education, startups, and markets where commercial CAD pricing is prohibitive.</p>''',
        '''<p>FreeCAD documentation is maintained at <a href="https://wiki.freecad.org/" rel="noopener noreferrer nofollow" target="_blank">the FreeCAD Wiki</a> with tutorials, scripting references, and workbench guides. Blender Foundation provides training at <a href="https://www.blender.org/support/tutorials/" rel="noopener noreferrer nofollow" target="_blank">blender.org/support/tutorials</a>. Both projects have active community forums and extensive YouTube tutorial ecosystems.</p>'''
    ),
    "comsol-inc": (
        '''<p>COMSOL competes in the multiphysics simulation market alongside ANSYS and Dassault Systèmes SIMULIA, differentiating through its focus on coupled-physics modeling and the Application Builder. While ANSYS dominates enterprise simulation and SIMULIA leads in non-linear structural analysis, COMSOL's strength lies in solving problems where multiple physics interact — thermal-structural, electromagnetic-thermal, fluid-structure — within a single unified environment.</p>
<p>The Application Builder is a key differentiator: simulation engineers can create custom apps with simplified GUIs that allow non-specialist colleagues to run pre-configured simulations without learning the full COMSOL interface. This capability extends simulation access within organizations. COMSOL is widely adopted in academia for research and teaching, and in R&D departments where custom physics modeling and source-code-level access to solver settings are essential. Users typically pair COMSOL with a CAD tool (SolidWorks, Inventor, Creo) via LiveLink connections for geometry import and parametric updates.</p>''',
        '''<p>COMSOL provides training through <a href="https://www.comsol.com/events" rel="noopener noreferrer nofollow" target="_blank">COMSOL Events</a>, including hands-on workshops, webinars, and the COMSOL Conference. The Application Library (built into the software) contains hundreds of tutorial models with step-by-step instructions. The COMSOL Blog and Discussion Forum are valuable for troubleshooting and modeling techniques.</p>'''
    ),
    "freecad-community": (
        '''<p>FreeCAD competes as the leading open-source parametric 3D CAD modeler, filling the gap between commercial mid-range MCAD (SolidWorks, Inventor) and entry-level tools (Tinkercad, Fusion 360 free tier). Its modular workbench architecture allows community-driven extension into specialized domains — FEM, BIM, CAM, robotics — without requiring a single monolithic codebase.</p>
<p>The project's growth has been accelerated by the maker movement, open-source hardware projects, and increasing adoption in professional workflows where budget constraints or customization requirements favor open-source solutions. FreeCAD is commonly used in education (university engineering courses), independent product design, and as a secondary tool by professionals who need scripting or format conversion capabilities. The ongoing topological naming problem and assembly workbench limitations remain the primary barriers to broader professional adoption, though active development is addressing these issues.</p>''',
        '''<p>FreeCAD learning resources include the <a href="https://wiki.freecad.org/" rel="noopener noreferrer nofollow" target="_blank">FreeCAD Wiki</a> (official documentation and tutorials), the FreeCAD Forum (community support), and a growing collection of YouTube tutorials. The FreeCAD Adventure blog and Joko Engineeringhelp YouTube channel are popular community-created learning resources.</p>'''
    ),
    "graebert": (
        '''<p>Graebert occupies a niche in the DWG-compatible CAD market as a cross-platform alternative to AutoCAD. While Autodesk dominates DWG editing on Windows, Graebert differentiates through native macOS and Linux support, browser-based editing (ARES Kudo), and mobile CAD (ARES Touch) — addressing workflows where AutoCAD is unavailable or impractical.</p>
<p>Graebert's OEM licensing strategy extends its reach beyond branded products: the Trinity CAD engine powers DraftSight (Dassault Systèmes), CorelCAD, and other vendor-branded CAD applications. This makes Graebert a significant technology provider in the 2D CAD market despite lower brand recognition. Users typically choose ARES Commander for macOS/Linux DWG editing or cloud-connected workflows, often alongside AutoCAD on Windows for compatibility with industry-standard workflows.</p>''',
        '''<p>Graebert provides learning resources through the <a href="https://www.graebert.com/support" rel="noopener noreferrer nofollow" target="_blank">Graebert Support Center</a>, including video tutorials, a knowledge base, and webinars. The ARES Forum offers community support for cross-platform DWG editing questions.</p>'''
    ),
    "ironcad": (
        '''<p>IronCAD targets the mid-range mechanical design market with a unique dual-kernel (ACIS + Parasolid) architecture that no other CAD tool offers. This positioning appeals to companies that receive geometry from multiple CAD sources and need to edit imported models without feature-history dependencies. IronCAD's drag-and-drop catalog approach also differentiates it from traditional parametric-only workflows.</p>
<p>While IronCAD has a smaller installed base than SolidWorks or Inventor, it retains loyal users in manufacturing environments where design flexibility and multi-CAD data handling are critical. The dual-kernel approach means IronCAD can natively process both ACIS-based and Parasolid-based geometry without translation — a practical advantage in supply-chain collaboration. Users often deploy IronCAD alongside a mainstream parametric tool, using IronCAD for concept design and imported geometry editing, then transferring finalized models to SolidWorks or Inventor for detailed documentation.</p>''',
        '''<p>IronCAD provides training through <a href="https://www.ironcad.com/support/training" rel="noopener noreferrer nofollow" target="_blank">IronCAD University</a>, including self-paced tutorials, instructor-led classes, and certification programs. The IronCAD YouTube channel offers product walkthroughs and tips.</p>'''
    ),
    "mcneel": (
        '''<p>Robert McNeel & Associates occupies a unique position in the 3D modeling market: Rhino is neither a full parametric MCAD tool (like SolidWorks) nor a BIM authoring tool (like Revit), but rather a NURBS surface modeler prized for free-form geometry creation. This positioning makes Rhino the tool of choice for industrial design, marine design, jewelry, automotive surfacing, and architectural form-finding where complex curves are the primary deliverable.</p>
<p>Grasshopper — Rhino's visual programming environment — has become a platform in its own right, spawning ecosystems of plugins (Ladybug for environmental analysis, Karamba for structural analysis, Kangaroo for physics simulation) that extend Rhino into computational design territory. Rhino.Inside technology allows Rhino and Grasshopper to run inside Revit, AutoCAD, and Unreal Engine, making Rhino a complementary tool rather than a competitor in many workflows. Users typically pair Rhino with a parametric solid modeler or BIM tool for production documentation, using Rhino for conceptual design and complex surface work.</p>''',
        '''<p>McNeel provides learning resources through <a href="https://www.rhino3d.com/learn" rel="noopener noreferrer nofollow" target="_blank">Rhino Learn</a> (official video tutorials), the Rhino Wiki, and the McNeel Forum. Grasshopper tutorials are available at <a href="https://www.grasshopper3d.com/" rel="noopener noreferrer nofollow" target="_blank">grasshopper3d.com</a>. Modelab, Parametric House, and YouTube channels like Gediminas Kirdeikis offer extensive Grasshopper training.</p>'''
    ),
    "openfoam-foundation": (
        '''<p>OpenFOAM competes as the leading open-source CFD toolbox, offering a free alternative to commercial solvers like ANSYS Fluent and Siemens STAR-CCM+. Its market position is strongest in academia and research, where source-code access enables custom solver development and physics model implementation — capabilities that commercial CFD tools restrict or charge premium rates for.</p>
<p>The OpenFOAM Foundation maintains the official codebase, while ESI Group maintains a fork (OpenFOAM+ / v2006+) with additional features and commercial support. This dual-maintenance model gives users a choice between the foundation version (stability-focused) and the ESI version (feature-focused). Industrial users typically adopt OpenFOAM for specific applications where licensing costs of commercial CFD are prohibitive or where custom physics implementation is required. OpenFOAM is commonly paired with ParaView for post-processing and with meshing tools (snappyHexMesh, cfMesh, ANSYS Meshing) for pre-processing.</p>''',
        '''<p>OpenFOAM documentation is maintained at <a href="https://openfoam.org/documentation/" rel="noopener noreferrer nofollow" target="_blank">openfoam.org/documentation</a>, including the User Guide, Programmer's Guide, and tutorial cases. The OpenFOAM Forum (CFD Online) and OpenFOAM Foundation YouTube channel provide community support and video tutorials. Wolf Dynamics and CFD Direct offer paid training courses.</p>'''
    ),
    "vectorworks": (
        '''<p>Vectorworks competes in the BIM and design software market with a focus on architecture, landscape architecture, and entertainment design — segments where design aesthetics and visual presentation matter as much as technical documentation. As a Nemetschek Group brand, Vectorworks complements Allplan (structural/engineering focus) and ArchiCAD (architecture focus) by serving design-forward professionals.</p>
<p>Vectorworks differentiates through native macOS support (most CAD tools are Windows-first), strong entertainment-industry features (Spotlight for lighting and event design), and an intuitive design environment that blends 2D drafting, 3D modeling, and BIM in a single application. The software's rendering capabilities (via Renderworks) and GIS integration appeal to firms that need presentation-quality output alongside construction documentation. Users in architecture often pair Vectorworks with Rhino for complex surface modeling, or with Revit for firms requiring Revit-format deliverables on collaborative projects.</p>''',
        '''<p>Vectorworks provides training through <a href="https://www.vectorworks.net/en-US/support/training" rel="noopener noreferrer nofollow" target="_blank">Vectorworks Academy</a>, including on-demand courses, live webinars, and the Vectorworks YouTube channel. The Vectorworks Community Board offers peer-to-peer support, and the annual Vectorworks Design Summit features advanced training sessions.</p>'''
    ),
}


def fix_vendor_page(filepath, market_html, learning_html):
    """Replace template Market Position and Learning Resources text in a vendor page."""
    html = filepath.read_text(encoding="utf-8")
    original = html

    # Pattern 1: Replace the first template paragraph (Market Position intro)
    # Matches: "[Vendor] develops [product], serving the ... rather than attempting to cover the full breadth of the CAD/BIM market."
    pattern1 = r'<p>[^<]*develops[^<]*, serving the[^<]*market segment\.[^<]*The product\'s primary focus is[^<]*, competing in the broader[^<]*category\.[^<]*The company maintains a specialized position by focusing on[^<]*workflows rather than attempting to cover the full breadth of the CAD/BIM market\.</p>'
    html = re.sub(pattern1, lambda m: market_html.split('</p>')[0] + '</p>', html, count=1)

    # Pattern 2: Replace the second template paragraph
    # Matches: "In a market increasingly dominated by large platform vendors ... often using it alongside other tools for tasks outside its core specialty."
    pattern2 = r'<p>In a market increasingly dominated by large platform vendors \(Autodesk, Dassault Systèmes, Siemens\), specialized tools like[^<]*retain value by offering deeper functionality in their specific domain than general-purpose platforms can provide\. Users typically choose[^<]*for its particular strengths in[^<]*, often using it alongside other tools for tasks outside its core specialty\.</p>'
    # Extract second paragraph from market_html
    second_p = market_html.split('</p>')[1].strip() if '</p>' in market_html else ''
    if second_p:
        second_p = '<p>' + second_p.lstrip('<p>') if not second_p.startswith('<p>') else second_p
        html = re.sub(pattern2, second_p, html, count=1)

    # Pattern 3: Replace Learning Resources template
    # Matches: "[Vendor] provides learning resources through official documentation, community forums, and partner networks. Users new to [product] should start with the vendor's official getting-started guides and supplement with community-produced tutorials and courses available on platforms like YouTube, Udemy, and LinkedIn Learning."
    pattern3 = r'<p>[^<]* provides learning resources through official documentation, community forums, and partner networks\. Users new to[^<]*should start with the vendor\'s official getting-started guides and supplement with community-produced tutorials and courses available on platforms like YouTube, Udemy, and LinkedIn Learning\.</p>'
    html = re.sub(pattern3, learning_html, html, count=1)

    if html != original:
        filepath.write_text(html, encoding="utf-8")
        return True
    return False


def main():
    print("Fixing vendor page template text...")
    fixed = 0
    skipped = 0

    for stem, (market_html, learning_html) in VENDOR_FIXES.items():
        filepath = VENDORS_DIR / f"{stem}.html"
        if not filepath.exists():
            print(f"  SKIP: {stem}.html not found")
            skipped += 1
            continue

        success = fix_vendor_page(filepath, market_html, learning_html)
        if success:
            print(f"  FIXED: {stem}.html")
            fixed += 1
        else:
            print(f"  NO CHANGE: {stem}.html (template not found)")
            skipped += 1

    print(f"\nDone: {fixed} fixed, {skipped} skipped")


if __name__ == "__main__":
    main()
