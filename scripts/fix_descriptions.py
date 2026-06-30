#!/usr/bin/env python3
"""
Fix duplicate/similar meta descriptions across concept pages.
Two groups to fix:
1. term-N pages: "In [Software], [Term] represents a core architectural mechanism."
2. niche pages: "Professional guide to [topic] in CAD/BIM engineering — workflows, tools, and best practices."

Strategy: Generate unique descriptions based on each page's H1 title and software context.
"""

import os
import re

CONCEPT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'concepts')

# Unique description templates - varied openings to avoid similarity
TERM_TEMPLATES = [
    "Learn how {term} works in {sw} — key functions, practical applications, and workflow tips for beginners.",
    "What is {term} in {sw}? Understand its purpose, how to use it, and why it matters in your design workflow.",
    "{term} in {sw} explained: core functionality, when to use it, and how it connects to other tools.",
    "A beginner's guide to {term} in {sw} — what it does, step-by-step usage, and common scenarios.",
    "Understand {term} ({sw}): definition, practical use cases, and tips to get started quickly.",
    "Getting started with {term} in {sw} — clear explanation of what it does and how to apply it in projects.",
    "{sw}'s {term} feature: what beginners need to know about its role in the design workflow.",
    "Quick reference for {term} in {sw}: purpose, basic usage, and real-world applications explained.",
    "Master {term} in {sw}: foundational knowledge, key operations, and best practices for new users.",
    "Everything beginners need to know about {term} in {sw}: definition, context, and practical guidance.",
    "{term} ({sw}) — how this feature fits into your design process and why understanding it saves time.",
    "Introduction to {term} in {sw}: what it controls, how to access it, and practical examples.",
    "Demystifying {term} in {sw} — a plain-language explanation of this essential design tool.",
    "{sw} {term} basics: understand its role, learn the workflow, and avoid common beginner mistakes.",
    "Why {term} matters in {sw}: quick overview of functionality, typical use cases, and learning path.",
]

NICHE_TEMPLATES = [
    "Introduction to {topic} — essential concepts, recommended tools, and step-by-step workflows for beginners.",
    "Getting started with {topic}: fundamental principles, software options, and practical first steps.",
    "Beginner's guide to {topic} — understand the basics, choose the right tools, and build foundational skills.",
    "{topic} fundamentals: what beginners need to know about tools, standards, and workflows.",
    "Learn {topic} from scratch — core concepts, industry tools, and practical exercises for new practitioners.",
    "Your first steps in {topic}: essential knowledge, recommended software, and learning roadmap.",
    "{topic} explained for beginners — key principles, tool selection guide, and hands-on starting points.",
    "Starting with {topic}: understand the fundamentals, explore available tools, and plan your learning path.",
    "Newcomer's guide to {topic} — from basic concepts to practical application in real projects.",
    "Foundation knowledge for {topic}: concepts, tools, and workflows every beginner should master.",
]


def extract_page_info(filepath):
    """Extract title, H1, current description, and software from a page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_m = re.search(r'<title>([^<]+)</title>', content)
    h1_m = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    desc_m = re.search(r'name="description"\s*content="([^"]+)"', content)
    if not desc_m:
        desc_m = re.search(r'name="description"[^>]*content="([^"]+)"', content)
    
    return {
        'title': title_m.group(1) if title_m else '',
        'h1': h1_m.group(1) if h1_m else '',
        'desc': desc_m.group(1) if desc_m else '',
        'content': content
    }


def get_software_name(filename):
    """Extract software name from filename pattern like 'autocad-term-5.html'."""
    SW_NAMES = {
        'alibre-design': 'Alibre Design', 'allplan': 'Allplan', 'ares-commander': 'ARES Commander',
        'aveva-e3d': 'AVEVA E3D', 'bricscad': 'BricsCAD', 'draftsight': 'DraftSight',
        'ironcad': 'IronCAD', 'microstation': 'MicroStation', 'rhinoceros': 'Rhino',
        'sketchup': 'SketchUp', 'spaceclaim': 'SpaceClaim', 'tekla-structures': 'Tekla Structures',
        'vectorworks': 'Vectorworks', 'archicad': 'ArchiCAD',
        'dwg-fastview-plus': 'DWG FastView Plus', 'dwg-fastview': 'DWG FastView',
        'fastview-3d': 'FastView 3D', 'gstarbim': 'GstarBIM',
        'gstarcad-365': 'GstarCAD 365', 'gstarcad-architecture': 'GstarCAD Architecture',
        'gstarcad-mechanical': 'GstarCAD Mechanical', 'gstarcad-point-cloud': 'GstarCAD Point Cloud',
        'gstarcad': 'GstarCAD', 'houseplan': 'HousePlan',
    }
    base = filename.replace('.html', '')
    if '-term-' in base:
        sw_slug = base.rsplit('-term-', 1)[0]
    else:
        sw_slug = base
    return SW_NAMES.get(sw_slug, sw_slug.replace('-', ' ').title())


def get_term_name(filepath):
    """Get the concept term name from the H1 or title."""
    info = extract_page_info(filepath)
    h1 = info['h1']
    # Remove software name suffix pattern like "(Alibre Design)"
    h1_clean = re.sub(r'\s*\([^)]+\)\s*$', '', h1)
    # Remove "— Software | Gstarcademy" from title
    if not h1_clean and info['title']:
        h1_clean = info['title'].split('—')[0].split('|')[0].strip()
    return h1_clean or 'this feature'


def fix_term_pages():
    """Fix term-N pages with template descriptions."""
    fixed = 0
    used_descs = set()
    
    files = sorted([f for f in os.listdir(CONCEPT_DIR) if 'term-' in f and f.endswith('.html')])
    
    for i, filename in enumerate(files):
        filepath = os.path.join(CONCEPT_DIR, filename)
        info = extract_page_info(filepath)
        desc = info['desc']
        
        # Only fix if it has the template pattern
        if 'represents a core' not in desc and 'represents an essential' not in desc:
            continue
        
        sw_name = get_software_name(filename)
        term_name = get_term_name(filepath)
        
        # Pick template based on index to ensure variety
        template = TERM_TEMPLATES[i % len(TERM_TEMPLATES)]
        new_desc = template.format(term=term_name, sw=sw_name)
        
        # Ensure unique
        while new_desc in used_descs:
            template = TERM_TEMPLATES[(i + 3) % len(TERM_TEMPLATES)]
            new_desc = template.format(term=term_name, sw=sw_name)
            break
        
        # Truncate to 160 chars if needed
        if len(new_desc) > 160:
            new_desc = new_desc[:157] + '...'
        
        used_descs.add(new_desc)
        
        # Replace in file
        old_desc_escaped = re.escape(desc)
        new_content = re.sub(
            r'(name="description"\s*content=")' + old_desc_escaped + r'"',
            lambda m: m.group(1) + new_desc + '"',
            info['content']
        )
        
        # Also update OG description if present
        new_content = re.sub(
            r'(property="og:description"\s*content=")' + old_desc_escaped + r'"',
            lambda m: m.group(1) + new_desc + '"',
            new_content
        )
        
        if new_content != info['content']:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed += 1
    
    return fixed


def fix_niche_pages():
    """Fix niche/workflow pages with 'Professional guide to...' template."""
    fixed = 0
    used_descs = set()
    
    files = sorted([f for f in os.listdir(CONCEPT_DIR) if f.endswith('.html') and 'term-' not in f])
    
    for i, filename in enumerate(files):
        filepath = os.path.join(CONCEPT_DIR, filename)
        info = extract_page_info(filepath)
        desc = info['desc']
        
        if not desc.startswith('Professional guide to'):
            continue
        
        # Extract topic name from H1 or filename
        topic = info['h1'] or filename.replace('.html', '').replace('-', ' ').title()
        
        template = NICHE_TEMPLATES[i % len(NICHE_TEMPLATES)]
        new_desc = template.format(topic=topic)
        
        if len(new_desc) > 160:
            new_desc = new_desc[:157] + '...'
        
        used_descs.add(new_desc)
        
        # Replace
        old_desc_pattern = re.escape(desc)
        new_content = re.sub(
            r'(name="description"\s*content=")' + old_desc_pattern + r'"',
            lambda m: m.group(1) + new_desc + '"',
            info['content']
        )
        new_content = re.sub(
            r'(property="og:description"\s*content=")' + old_desc_pattern + r'"',
            lambda m: m.group(1) + new_desc + '"',
            new_content
        )
        
        if new_content != info['content']:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed += 1
    
    return fixed


def main():
    print("Fixing template descriptions...")
    term_fixed = fix_term_pages()
    print(f"  Fixed {term_fixed} term-N pages")
    
    niche_fixed = fix_niche_pages()
    print(f"  Fixed {niche_fixed} niche/workflow pages")
    
    print(f"\nTotal fixed: {term_fixed + niche_fixed}")


if __name__ == '__main__':
    main()
