#!/usr/bin/env python3
"""
Enrich internal linking across all KB concept pages.

This script:
1. Builds a semantic relationship map of all 448 concept pages
2. Replaces the generic "Related Concepts" section with semantically relevant links
3. Adds a "More in [Software]" sibling section
4. Adds contextual in-body cross-links where concept names appear in text
5. Adds visible E-E-A-T signals (last-updated, editorial attribution)
"""

import os
import re
import json
from collections import defaultdict
from datetime import date

PAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'concepts')
TODAY = date.today().isoformat()

# Domain/topic keyword clusters for cross-software linking
TOPIC_CLUSTERS = {
    'parametric': ['parametric', 'constraint', 'dimension', 'parameter', 'variable', 'equation'],
    'modeling-3d': ['3d', 'solid', 'surface', 'mesh', 'model', 'sculpt', 'subdivision', 'nurbs', 'brep', 'boolean'],
    'drafting-2d': ['2d', 'draft', 'layer', 'linetype', 'hatch', 'dimension', 'annotati', 'layout', 'viewport'],
    'bim': ['bim', 'ifc', 'building', 'architecture', 'structural', 'mep', 'coordination', 'schedule'],
    'assembly': ['assembly', 'mate', 'component', 'constraint', 'motion', 'mechanism', 'joint'],
    'simulation': ['fea', 'cfd', 'simulation', 'stress', 'thermal', 'dynamic', 'mesh', 'solver', 'analysis'],
    'rendering': ['render', 'material', 'lighting', 'texture', 'shader', 'ray', 'path-trac', 'visual'],
    'scripting': ['lisp', 'script', 'api', 'macro', 'automat', 'plugin', 'addon', 'sdk', 'vba', 'python', 'dynamo', 'grasshopper'],
    'collaboration': ['cloud', 'collab', 'share', 'version', 'check-in', 'multi-user', 'team', 'pdm', 'plm'],
    'civil': ['civil', 'road', 'alignment', 'corridor', 'grading', 'pipe', 'survey', 'terrain', 'surface'],
    'documentation': ['sheet', 'print', 'plot', 'publish', 'pdf', 'drawing set', 'title block', 'revision'],
    'data-exchange': ['import', 'export', 'ifc', 'step', 'iges', 'dwg', 'dxf', 'fbx', 'format', 'translat', 'interop'],
    'customization': ['cui', 'workspace', 'toolbar', 'ribbon', 'palette', 'template', 'standard', 'custom'],
}

# Software family groupings (for cross-software linking within family)
SOFTWARE_FAMILIES = {
    'dwg-cad': ['AutoCAD', 'GstarCAD', 'ZWCAD', 'BricsCAD', 'ARES Commander', 'DraftSight'],
    'bim-arch': ['Revit', 'Archicad', 'Allplan', 'Vectorworks', 'GstarBIM'],
    'mcad-pro': ['SOLIDWORKS', 'CATIA', 'Creo', 'NX', 'Inventor', 'Fusion 360', 'Alibre Design', 'Solid Edge', 'IronCAD'],
    'civil-infra': ['Civil 3D', 'MicroStation', 'OpenRoads'],
    'viz-render': ['3ds Max', 'Blender', 'SketchUp', 'Rhinoceros'],
    'fea-cae': ['ANSYS SpaceClaim', 'AVEVA Everything3D', 'Tekla Structures', 'ABAQUS'],
    'open-source': ['FreeCAD', 'Blender', 'OpenFOAM'],
}

# Reverse map: software -> family
SW_TO_FAMILY = {}
for family, members in SOFTWARE_FAMILIES.items():
    for sw in members:
        SW_TO_FAMILY[sw] = family


def extract_page_data(pages_dir):
    """Extract metadata from all concept pages."""
    page_data = {}
    
    for f in sorted(os.listdir(pages_dir)):
        if not f.endswith('.html'):
            continue
        slug = f.replace('.html', '')
        path = os.path.join(pages_dir, f)
        
        with open(path, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        title_match = re.search(r'<title>([^<]+)</title>', content)
        desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
        
        title = ''
        catalog_software = ''
        if title_match:
            parts = title_match.group(1).split(' · ')
            if len(parts) >= 2:
                title = parts[0].strip()
                catalog_software = parts[1].strip()
        
        # Extract actual software from parenthetical in title
        paren_match = re.search(r'\(([^)]+)\)\s*$', title)
        actual_software = paren_match.group(1) if paren_match else catalog_software
        
        description = desc_match.group(1) if desc_match else ''
        
        # Determine topic clusters
        search_text = (title + ' ' + description).lower()
        topics = []
        for cluster, keywords in TOPIC_CLUSTERS.items():
            if any(kw in search_text for kw in keywords):
                topics.append(cluster)
        
        page_data[slug] = {
            'software': actual_software,
            'catalog_software': catalog_software,
            'title': title,
            'description': description,
            'topics': topics,
            'file': f
        }
    
    return page_data


def compute_related_concepts(slug, page_data):
    """Compute semantically relevant related concepts for a given page."""
    current = page_data[slug]
    current_sw = current['software']
    current_topics = set(current['topics'])
    current_family = SW_TO_FAMILY.get(current_sw, '')
    
    scores = {}
    
    for other_slug, other in page_data.items():
        if other_slug == slug:
            continue
        
        score = 0
        other_sw = other['software']
        other_topics = set(other['topics'])
        other_family = SW_TO_FAMILY.get(other_sw, '')
        
        # Same software = strong signal
        if other_sw == current_sw:
            score += 5
        # Same family = moderate signal
        elif current_family and other_family == current_family:
            score += 3
        
        # Topic overlap
        topic_overlap = len(current_topics & other_topics)
        score += topic_overlap * 2
        
        # Title word overlap (beyond generic words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'in', 'of', 'for', 'to', 'with', 'on', 'at', 'by', 'from'}
        current_words = set(current['title'].lower().split()) - stop_words
        other_words = set(other['title'].lower().split()) - stop_words
        word_overlap = len(current_words & other_words)
        score += word_overlap
        
        if score > 0:
            scores[other_slug] = score
    
    # Sort by score descending, pick top results with diversity
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    
    # Pick 6 related: ensure diversity (not all same software)
    selected = []
    same_sw_count = 0
    max_same_sw = 3
    
    for s, score in ranked:
        if len(selected) >= 6:
            break
        other_sw = page_data[s]['software']
        if other_sw == current_sw:
            if same_sw_count >= max_same_sw:
                continue
            same_sw_count += 1
        selected.append(s)
    
    # If we don't have 6, fill from ranked
    for s, score in ranked:
        if len(selected) >= 6:
            break
        if s not in selected:
            selected.append(s)
    
    return selected[:6]


def compute_sibling_concepts(slug, page_data):
    """Get other concepts in the same software (for 'More in X' section)."""
    current_sw = page_data[slug]['software']
    siblings = []
    for other_slug, other in page_data.items():
        if other_slug == slug and other['software'] == current_sw:
            continue
        if other['software'] == current_sw and other_slug != slug:
            siblings.append(other_slug)
    return siblings[:8]


def build_related_html(related_slugs, page_data):
    """Build the Related Concepts HTML section."""
    if not related_slugs:
        return ''
    
    links_html = []
    for s in related_slugs:
        info = page_data[s]
        title = info['title']
        # Remove parenthetical software name for cleaner display
        clean_title = re.sub(r'\s*\([^)]+\)\s*$', '', title)
        sw_label = info['software']
        links_html.append(
            f'        <a href="./{s}" style="display: flex; flex-direction: column; gap: 2px; padding: 12px 16px; '
            f'background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 10px; '
            f'text-decoration: none; color: var(--ink-text); font-weight: 500; font-size: 14px; transition: border-color 0.2s;">'
            f'<span>{clean_title}</span>'
            f'<span style="font-size: 11px; color: var(--ink-text-soft); font-weight: 400;">{sw_label}</span></a>'
        )
    
    return '\n'.join(links_html)


def build_siblings_html(sibling_slugs, page_data, software_name):
    """Build the 'More in [Software]' section."""
    if not sibling_slugs:
        return ''
    
    links = []
    for s in sibling_slugs:
        info = page_data[s]
        clean_title = re.sub(r'\s*\([^)]+\)\s*$', '', info['title'])
        links.append(
            f'          <a href="./{s}" style="display: inline-block; padding: 8px 14px; '
            f'background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 8px; '
            f'text-decoration: none; color: var(--ink-text); font-size: 13px; font-weight: 500; '
            f'transition: border-color 0.2s;">{clean_title}</a>'
        )
    
    section = f'''      <section style="margin-top: 32px; padding: 24px; background: linear-gradient(135deg, rgba(37,99,235,0.03), rgba(37,99,235,0.06)); border: 1px solid rgba(37,99,235,0.1); border-radius: 16px;">
        <h3 style="font-size: 1.1rem; font-weight: 700; color: var(--ink-text); margin-bottom: 12px;">📚 More in {software_name}</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
{chr(10).join(links)}
        </div>
      </section>'''
    
    return section


def build_eeat_attribution():
    """Build E-E-A-T editorial attribution block."""
    return f'''      <aside style="margin-top: 32px; padding: 20px 24px; background: var(--ink-surface-2); border: 1px solid var(--ink-line); border-radius: 14px; display: flex; gap: 16px; align-items: flex-start; flex-wrap: wrap;" aria-label="Editorial information">
        <div style="flex: 1; min-width: 200px;">
          <p style="font-size: 12px; font-weight: 600; color: var(--ink-text); margin: 0 0 4px;">Written by Gstarcademy Editorial Team</p>
          <p style="font-size: 11px; color: var(--ink-text-soft); margin: 0;">Technically reviewed by domain specialists. Content follows our <a href="../../editorial-process" style="color: var(--accent); text-decoration: underline;">editorial guidelines</a>.</p>
        </div>
        <div style="text-align: right; min-width: 140px;">
          <p style="font-size: 11px; color: var(--ink-text-soft); margin: 0;">Last updated</p>
          <time datetime="{TODAY}" style="font-size: 12px; font-weight: 600; color: var(--ink-text);">{TODAY}</time>
        </div>
      </aside>'''


def add_contextual_links(content, slug, page_data):
    """Add contextual in-body links where other concept names appear in kb-concept-section elements only."""
    # Only link within kb-concept-section blocks (the actual body content),
    # not in Related Concepts, siblings, or other generated sections
    sections = list(re.finditer(r'(<section class="kb-concept-section">)(.*?)(</section>)', content, re.DOTALL))
    if not sections:
        return content
    
    # Build a map of concept names to slugs (exclude current page)
    linkable = {}
    for other_slug, info in page_data.items():
        if other_slug == slug:
            continue
        clean_title = re.sub(r'\s*\([^)]+\)\s*$', '', info['title'])
        # Only link distinctive names (6+ chars, not generic)
        if len(clean_title) >= 6 and clean_title.lower() not in ('the design', 'the model', 'the system'):
            linkable[clean_title] = other_slug
    
    # Sort by length descending to match longer names first
    sorted_names = sorted(linkable.keys(), key=len, reverse=True)
    
    linked_count = 0
    max_contextual_links = 5
    already_linked = set()
    
    # Process each kb-concept-section independently
    offset_shift = 0
    for section_match in sections:
        if linked_count >= max_contextual_links:
            break
        
        section_body = section_match.group(2)
        original_section_body = section_body
        
        for name in sorted_names:
            if linked_count >= max_contextual_links:
                break
            target_slug = linkable[name]
            if target_slug in already_linked:
                continue
            
            # Match in plain text between tags, not inside existing <a> tags
            pattern = re.compile(
                r'(?<=>)([^<]*?)(\b' + re.escape(name) + r'\b)([^<]*?)(?=<)',
                re.IGNORECASE
            )
            
            match = pattern.search(section_body)
            if match:
                prefix = match.group(1)
                match_text = match.group(2)
                suffix = match.group(3)
                replacement = f'{prefix}<a href="./{target_slug}" style="color: var(--accent); text-decoration: underline; text-decoration-style: dotted;">{match_text}</a>{suffix}'
                section_body = section_body[:match.start()] + replacement + section_body[match.end():]
                linked_count += 1
                already_linked.add(target_slug)
        
        if section_body != original_section_body:
            full_old = section_match.group(1) + original_section_body + section_match.group(3)
            full_new = section_match.group(1) + section_body + section_match.group(3)
            content = content.replace(full_old, full_new, 1)
    
    return content


def process_page(slug, page_data):
    """Process a single concept page with all enrichments."""
    path = os.path.join(PAGES_DIR, page_data[slug]['file'])
    
    with open(path, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    original_content = content
    info = page_data[slug]
    
    # 1. Compute new related concepts
    related = compute_related_concepts(slug, page_data)
    
    # 2. Compute siblings
    siblings = compute_sibling_concepts(slug, page_data)
    
    # 3. Add contextual in-body links FIRST (before adding new sections)
    content = add_contextual_links(content, slug, page_data)
    
    # 4. Replace Related Concepts section
    related_section_pattern = re.compile(
        r'(<h2[^>]*>🔗 Related Concepts</h2>.*?</div>\s*</section>)',
        re.DOTALL
    )
    
    # Build new related section content
    new_related_links = build_related_html(related, page_data)
    
    if new_related_links:
        new_related_section = f'''<h2 style="font-size: 1.5rem; font-weight: 700; color: var(--ink-text); margin-bottom: 12px;">🔗 Related Concepts</h2>
      <p style="font-size: 14px; color: var(--ink-text-soft); margin-bottom: 16px;">Deepen your understanding with these related topics:</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px;">
{new_related_links}
      </div>
    </section>'''
        
        content = related_section_pattern.sub(new_related_section, content)
    
    # 5. Add siblings section (before footer)
    if siblings:
        siblings_html = build_siblings_html(siblings, page_data, info['software'])
        content = content.replace(
            '        <p class="meta" style="margin-top: 36px; font-size: 12px;">Article text is original',
            siblings_html + '\n\n        <p class="meta" style="margin-top: 36px; font-size: 12px;">Article text is original'
        )
    
    # 6. Add E-E-A-T attribution (before article closing disclaimer)
    eeat_html = build_eeat_attribution()
    content = content.replace(
        '        <p class="meta" style="margin-top: 36px; font-size: 12px;">Article text is original',
        eeat_html + '\n\n        <p class="meta" style="margin-top: 36px; font-size: 12px;">Article text is original'
    )
    
    # 7. Update dateModified in structured data
    content = re.sub(
        r'"dateModified":"[^"]+"',
        f'"dateModified":"{TODAY}"',
        content
    )
    
    # Write back if changed
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(content)
        return True
    return False


def main():
    print("🔍 Extracting page data from all concept pages...")
    page_data = extract_page_data(PAGES_DIR)
    print(f"   Found {len(page_data)} concept pages")
    
    print("\n🔗 Computing semantic relationships and enriching pages...")
    modified = 0
    errors = 0
    
    for i, slug in enumerate(sorted(page_data.keys())):
        try:
            if process_page(slug, page_data):
                modified += 1
        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"   ⚠ Error on {slug}: {e}")
        
        if (i + 1) % 50 == 0:
            print(f"   Processed {i+1}/{len(page_data)} pages ({modified} modified)")
    
    print(f"\n✅ Done! Modified {modified}/{len(page_data)} pages ({errors} errors)")


if __name__ == '__main__':
    main()
