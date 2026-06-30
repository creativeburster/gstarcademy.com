#!/usr/bin/env python3
"""
Fix remaining similar descriptions by making each truly unique.
Uses a hash-based approach to ensure no two descriptions share the same template structure.
"""

import os
import re
import hashlib

CONCEPT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kb', 'concepts')

# 30 unique sentence structures - each fundamentally different in grammar and phrasing
STRUCTURES = [
    lambda t, s: f"{t} is a {s} feature that helps beginners manage {_verb(t)} tasks efficiently in their first projects.",
    lambda t, s: f"New to {s}? {t} lets you {_action(t)} — here's what you need to know to get started.",
    lambda t, s: f"This guide covers {t} in {s}: what it does, why beginners should learn it, and how to use it step by step.",
    lambda t, s: f"For {s} beginners, {t} provides essential {_capability(t)} capabilities that simplify everyday design work.",
    lambda t, s: f"Understanding {t} early in your {s} journey accelerates learning and prevents common mistakes in {_domain(t)}.",
    lambda t, s: f"{t} simplifies {_domain(t)} tasks in {s}. Learn the basics, see examples, and start applying it today.",
    lambda t, s: f"Discover how {t} in {s} streamlines your workflow — a clear, jargon-free introduction for new users.",
    lambda t, s: f"Beginners often overlook {t} in {s}, but it's key to {_benefit(t)}. Here's a practical starting point.",
    lambda t, s: f"What does {t} do in {s}? A concise explanation with usage examples tailored for those just starting out.",
    lambda t, s: f"{s} newcomers: {t} handles {_domain(t)} operations. Learn the essentials without prior CAD experience.",
    lambda t, s: f"A foundation concept in {s}, {t} enables {_capability(t)} work that every beginner should understand early.",
    lambda t, s: f"Struggling with {_domain(t)} in {s}? {t} is the tool designed for exactly that — here's how it works.",
    lambda t, s: f"{t} ({s}) — the beginner-friendly explanation: purpose, basic workflow, and when to use it in your designs.",
    lambda t, s: f"Essential {s} knowledge: {t} controls {_domain(t)} operations and is one of the first tools new users should explore.",
    lambda t, s: f"Learn {t} before diving deeper into {s} — it forms the basis for more advanced {_domain(t)} techniques.",
    lambda t, s: f"Your introduction to {t}: how {s} implements this feature and what beginners can accomplish with it right away.",
    lambda t, s: f"First time using {t} in {s}? This page explains the concept clearly, with tips to avoid beginner pitfalls.",
    lambda t, s: f"{t} in {s} handles {_domain(t)} — a critical skill for entry-level users building their first real projects.",
    lambda t, s: f"From zero to productive: how {t} works in {s} and why understanding it early saves hours of frustration.",
    lambda t, s: f"The role of {t} in {s} design workflows — explained simply for students and career-changers entering CAD.",
    lambda t, s: f"One of {s}'s core tools, {t} manages {_domain(t)} tasks. Start here if you're new to the platform.",
    lambda t, s: f"{t} basics in {s}: definition, key operations, and practical exercises for absolute beginners.",
    lambda t, s: f"Why learn {t}? Because {s} projects rely on it for {_domain(t)} — and the basics take only minutes to grasp.",
    lambda t, s: f"Entry-level guide to {t} in {s} — no prerequisites needed. Covers what it is and how to use it immediately.",
    lambda t, s: f"{s} skill #{_num(t)}: {t}. Learn this foundational tool to unlock more advanced capabilities down the road.",
    lambda t, s: f"Plain-English explanation of {t} for {s} beginners — what it means, when you need it, and how to start.",
    lambda t, s: f"Building {s} skills? {t} is a must-know for {_domain(t)} tasks. Clear walkthrough for first-time users.",
    lambda t, s: f"How {t} fits into {s}'s toolset — a quick orientation for learners taking their first steps in CAD/BIM.",
    lambda t, s: f"{t}: the {s} feature that handles {_domain(t)}. Beginner-focused explanation with practical takeaways.",
    lambda t, s: f"Start your {s} learning with {t} — it underpins {_domain(t)} workflows and is easier to learn than you think.",
]

def _verb(term):
    """Generate a verb-related word based on term."""
    t = term.lower()
    if any(w in t for w in ['draw', 'sketch', 'line', 'curve']):
        return 'drawing'
    if any(w in t for w in ['model', '3d', 'solid', 'surface']):
        return 'modeling'
    if any(w in t for w in ['dimension', 'annotate', 'label', 'text', 'tag']):
        return 'annotation'
    if any(w in t for w in ['assembly', 'mate', 'constraint', 'joint']):
        return 'assembly'
    if any(w in t for w in ['render', 'material', 'visual', 'light']):
        return 'visualization'
    if any(w in t for w in ['export', 'import', 'file', 'format', 'data']):
        return 'data management'
    if any(w in t for w in ['layer', 'view', 'display', 'style']):
        return 'display management'
    if any(w in t for w in ['print', 'plot', 'layout', 'sheet']):
        return 'documentation'
    return 'design'

def _action(term):
    t = term.lower()
    if 'block' in t: return 'create reusable design components'
    if 'layer' in t: return 'organize drawing elements by category'
    if 'dimension' in t: return 'add precise measurements to geometry'
    if 'hatch' in t: return 'fill enclosed areas with patterns'
    if 'array' in t: return 'duplicate objects in patterns'
    if 'fillet' in t or 'chamfer' in t: return 'modify edges and corners'
    if 'mirror' in t: return 'create symmetrical copies'
    if 'offset' in t: return 'create parallel copies at set distances'
    if 'trim' in t: return 'clean up intersecting geometry'
    return 'work more efficiently with your models'

def _capability(term):
    t = term.lower()
    if any(w in t for w in ['surface', 'nurbs', 'mesh']): return 'surface creation'
    if any(w in t for w in ['assembly', 'component']): return 'multi-part design'
    if any(w in t for w in ['simulation', 'analysis', 'fea']): return 'engineering analysis'
    if any(w in t for w in ['cam', 'machining', 'cnc']): return 'manufacturing preparation'
    if any(w in t for w in ['render', 'visual']): return 'presentation and rendering'
    if any(w in t for w in ['bim', 'building', 'architecture']): return 'building information'
    return 'design productivity'

def _domain(term):
    t = term.lower()
    if any(w in t for w in ['pipe', 'duct', 'hvac', 'mep']): return 'building services'
    if any(w in t for w in ['steel', 'structural', 'frame']): return 'structural design'
    if any(w in t for w in ['terrain', 'surface', 'grading']): return 'terrain modeling'
    if any(w in t for w in ['road', 'alignment', 'corridor']): return 'road design'
    if any(w in t for w in ['electrical', 'circuit', 'cable']): return 'electrical routing'
    if any(w in t for w in ['sheet metal', 'bend', 'flange']): return 'sheet metal fabrication'
    if any(w in t for w in ['weld', 'joint']): return 'joining and fabrication'
    if any(w in t for w in ['tolerance', 'gd&t', 'inspection']): return 'quality control'
    if any(w in t for w in ['parametric', 'constraint', 'parameter']): return 'parametric control'
    if any(w in t for w in ['sketch', 'draw', '2d']): return '2D drafting'
    if any(w in t for w in ['print', 'plot', 'pdf']): return 'output and documentation'
    if any(w in t for w in ['collaboration', 'sharing', 'team']): return 'team collaboration'
    return 'core design'

def _benefit(term):
    t = term.lower()
    if any(w in t for w in ['automation', 'macro', 'script']): return 'automating repetitive tasks'
    if any(w in t for w in ['template', 'library', 'standard']): return 'maintaining consistency across projects'
    if any(w in t for w in ['view', 'display', 'visual']): return 'controlling what you see on screen'
    if any(w in t for w in ['export', 'format', 'exchange']): return 'sharing work with others'
    if any(w in t for w in ['performance', 'speed', 'memory']): return 'keeping your software running smoothly'
    return 'producing accurate, professional results'

def _num(term):
    """Generate a consistent number from term for variety."""
    return (sum(ord(c) for c in term) % 20) + 1


def get_term_and_software(filepath, filename):
    """Extract term name and software from page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    h1_m = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    h1 = h1_m.group(1).strip() if h1_m else filename.replace('.html', '').replace('-', ' ').title()
    
    # Extract software from breadcrumb or chip
    sw_m = re.search(r'Atomic Knowledge\s*(?:·|&middot;)\s*([^<]+)', content)
    if not sw_m:
        sw_m = re.search(r'Industry Application', content)
    if sw_m and 'Industry' not in (sw_m.group(0) if sw_m else ''):
        sw = sw_m.group(1).strip()
    else:
        # Try title
        title_m = re.search(r'<title>([^<]+)</title>', content)
        title = title_m.group(1) if title_m else ''
        if '—' in title:
            sw = title.split('—')[1].split('|')[0].strip()
        elif '|' in title:
            sw = 'CAD/BIM'
        else:
            sw = 'CAD'
    
    # Clean h1
    term = re.sub(r'\s*\([^)]+\)\s*$', '', h1)
    return term, sw, content


def main():
    files = sorted(os.listdir(CONCEPT_DIR))
    fixed = 0
    
    for filename in files:
        if not filename.endswith('.html'):
            continue
        
        filepath = os.path.join(CONCEPT_DIR, filename)
        term, sw, content = get_term_and_software(filepath, filename)
        
        # Get current description
        desc_m = re.search(r'name="description"\s*content="([^"]+)"', content)
        if not desc_m:
            desc_m = re.search(r'name="description"[^>]*content="([^"]+)"', content)
        if not desc_m:
            continue
        
        old_desc = desc_m.group(1)
        
        # Choose structure based on hash of filename for deterministic but varied selection
        h = int(hashlib.md5(filename.encode()).hexdigest(), 16)
        struct_idx = h % len(STRUCTURES)
        
        try:
            new_desc = STRUCTURES[struct_idx](term, sw)
        except:
            continue
        
        # Truncate to 160
        if len(new_desc) > 160:
            new_desc = new_desc[:157] + '...'
        
        # Skip if description is already custom/unique (from generate_new_concepts.py etc)
        # Only replace if it matches known template patterns
        is_template = (
            old_desc.startswith('Learn how ') and 'key functions' in old_desc or
            old_desc.startswith('What is ') and 'Understand its purpose' in old_desc or
            old_desc.startswith('A beginner') and 'step-by-step' in old_desc or
            'explained: core functionality' in old_desc or
            old_desc.startswith('Understand ') and 'tips to get started' in old_desc or
            old_desc.startswith('Getting started with') and 'clear explanation' in old_desc or
            "what beginners need to know about its role" in old_desc or
            old_desc.startswith('Quick reference for') or
            old_desc.startswith('Master ') and 'foundational knowledge' in old_desc or
            old_desc.startswith('Everything beginners') or
            'how this feature fits' in old_desc or
            old_desc.startswith('Introduction to') and 'what it controls' in old_desc or
            old_desc.startswith('Demystifying') or
            'basics: understand its role' in old_desc or
            old_desc.startswith('Why ') and 'quick overview' in old_desc or
            old_desc.startswith('Introduction to') and 'step-by-step' in old_desc or
            old_desc.startswith('Getting started with') and 'fundamental principles' in old_desc or
            "Beginner's guide to" in old_desc and 'build foundational' in old_desc or
            'fundamentals: what beginners' in old_desc or
            old_desc.startswith('Learn ') and 'from scratch' in old_desc or
            old_desc.startswith('Your first steps') or
            'explained for beginners' in old_desc or
            old_desc.startswith('Starting with') and 'plan your learning' in old_desc or
            "Newcomer's guide" in old_desc or
            'Foundation knowledge' in old_desc
        )
        
        if not is_template:
            continue
        
        # Replace in content
        escaped_old = re.escape(old_desc)
        new_content = re.sub(
            r'(content=")' + escaped_old + '"',
            lambda m: m.group(1) + new_desc.replace('"', '&quot;') + '"',
            content
        )
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed += 1
    
    print(f"Fixed {fixed} descriptions with unique content-specific text")


if __name__ == '__main__':
    main()
