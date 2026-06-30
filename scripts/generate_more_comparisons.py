#!/usr/bin/env python3
"""
Generate additional comparison pages for secondary software pairs.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generate_comparison_pages import SW_MAP, generate_comparison_page, OUTPUT_DIR

# Additional comparison pairs
MORE_PAIRS = [
    # More DWG CAD comparisons
    ("autocad", "zwcad"), ("zwcad", "draftsight"), ("gstarcad", "draftsight"),
    # More BIM comparisons
    ("revit", "vectorworks"), ("allplan", "vectorworks"), ("archicad", "vectorworks"),
    # More MCAD
    ("catia", "solid-edge"), ("creo-parametric", "inventor"),
    ("creo-parametric", "solid-edge"), ("siemens-nx", "onshape"),
    ("fusion-360", "solid-edge"), ("inventor", "onshape"),
    # Viz comparisons
    ("rhinoceros", "3dsmax"), ("rhinoceros", "blender"),
    ("sketchup", "blender"), ("3dsmax", "rhinoceros"),
    # Cross-category high-value
    ("solidworks", "autocad"), ("revit", "solidworks"),
    ("fusion-360", "blender"), ("freecad", "blender"),
    ("sketchup", "revit"), ("autocad", "rhinoceros"),
    ("autocad", "civil-3d"), ("gstarcad", "bricscad"),
    ("solidworks", "inventor"), ("catia", "solidworks"),
    ("onshape", "fusion-360"), ("bricscad", "autocad"),
    ("archicad", "revit"), ("siemens-nx", "solidworks"),
    ("solid-edge", "solidworks"),
    # Simulation
    ("ansys-mechanical", "abaqus"),
    # Additional value
    ("autocad", "blender"), ("fusion-360", "rhinoceros"),
    ("inventor", "fusion-360"), ("solidworks", "rhinoceros"),
    ("gstarcad", "freecad"), ("autocad", "onshape"),
    ("revit", "blender"), ("civil-3d", "autocad"),
    ("draftsight", "autocad"),
]

# Filter to unique pairs that don't already exist as files
existing = set(f.replace('.html','') for f in os.listdir(OUTPUT_DIR))
generated = 0

for slug_a, slug_b in MORE_PAIRS:
    if slug_a not in SW_MAP or slug_b not in SW_MAP:
        continue
    
    page_slug_1 = f"{slug_a}-vs-{slug_b}"
    page_slug_2 = f"{slug_b}-vs-{slug_a}"
    
    if page_slug_1 in existing or page_slug_2 in existing:
        continue
    
    page_slug, html = generate_comparison_page(slug_a, slug_b)
    filepath = os.path.join(OUTPUT_DIR, f"{page_slug}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    existing.add(page_slug)
    generated += 1

print(f"Generated {generated} additional comparison pages")
