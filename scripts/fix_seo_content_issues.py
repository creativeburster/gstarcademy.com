#!/usr/bin/env python3
"""
Fix SEO content issues in Gstarcademy KB concept pages:
1. Replace template quiz wrong options (441 pages) with topic-relevant distractors
2. Remove template quiz feedback filler text (180 pages)
3. Replace template definition phrasing (350 pages) with varied alternatives
4. Replace template "why it matters" phrasing (16 pages) with varied alternatives
5. Add noindex to thin content industry pages (~278 pages with page-shell)
"""

import os
import re
import random
import hashlib
from pathlib import Path
from html import unescape

KB_CONCEPTS_DIR = Path(r"f:\gstarcademy\kb\concepts")
random.seed(42)

# ─── Template strings to find ───
SQL_OPTION = "Failing to manually re-index the SQL server database."
CLOUD_OPTION = "Over-allocating virtual memory caches in the cloud settings."
LINETYPE_OPTION = "Restricting linetype scales strictly to 1:1 paper coordinates."

FEEDBACK_TEMPLATE = (
    "\n\nWithout it, downstream fabrication or cross-discipline model federation "
    "will face geometric conversion anomalies, topological reference losses, and "
    "data transfer discrepancies."
)

DEFINITION_TEMPLATE = "represents a core architectural mechanism"
WHY_IT_MATTERS_TEMPLATE = "separates routine work from high-quality output that meets professional standards"

# ─── Varied replacement phrasings ───
DEFINITION_PHRASINGS = [
    "is a fundamental design mechanism",
    "serves as a key modeling principle",
    "functions as an essential workflow component",
    "acts as a core structural element",
    "operates as a primary design driver",
    "constitutes a critical modeling concept",
    "forms an integral part of the design workflow",
    "provides a foundational technical capability",
    "represents a key engineering principle",
    "serves as a central modeling mechanism",
    "is an essential design tool",
    "functions as a core engineering concept",
    "acts as a fundamental modeling element",
    "provides a key technical foundation",
    "operates as a central design principle",
]

WHY_IT_MATTERS_PHRASINGS = [
    "distinguishes basic drafting from production-ready deliverables",
    "marks the difference between amateur and professional-grade work",
    "is critical for achieving industry-standard documentation quality",
    "directly impacts the precision and reliability of final deliverables",
    "determines whether output meets professional review standards",
    "is what separates competent work from expert-level output",
    "elevates work from basic completion to professional excellence",
]

# ─── Generic but plausible CAD-related distractor pool ───
# Used as fallback if we can't extract enough pitfalls from other pages
GENERIC_DISTRACTORS = [
    "Relying on automatic saves instead of implementing a version control strategy.",
    "Ignoring layer management conventions, causing disorganized drawing files.",
    "Failing to define proper datum references before applying geometric tolerances.",
    "Using default template settings without customizing for project requirements.",
    "Neglecting to purge unused blocks and layers, inflating file size.",
    "Mixing annotation scales incorrectly, leading to inconsistent text display.",
    "Over-constraining sketches without checking degrees of freedom status.",
    "Not validating file exports against target software import requirements.",
    "Ignoring model history dependency order when reordering features.",
    "Failing to assign correct material properties before running analysis.",
    "Using inconsistent naming conventions for views and sheets.",
    "Not setting up proper drawing units at project initialization.",
    "Neglecting to create backup configurations before major design changes.",
    "Forgetting to lock reference geometry before modifying dependent features.",
    "Overlooking coordinate system alignment when importing external data.",
    "Not using parametric relationships where manual dimensions would suffice.",
    "Failing to document design intent in feature names and comments.",
    "Ignoring software-specific file compatibility limitations during export.",
    "Not testing assemblies for interference before final documentation.",
    "Relying on visual alignment instead of precise constraint placement.",
]


def strip_html(text):
    """Remove HTML tags and unescape entities."""
    text = re.sub(r'<[^>]+>', '', text)
    return unescape(text).strip()


def extract_pitfalls(html):
    """Extract pitfall items from the Common pitfalls section."""
    match = re.search(r'<h2>Common pitfalls</h2>\s*<ul>(.*?)</ul>', html, re.DOTALL)
    if not match:
        return []
    ul_content = match.group(1)
    li_items = re.findall(r'<li>(.*?)</li>', ul_content, re.DOTALL)
    return [strip_html(item) for item in li_items if strip_html(item)]


def extract_concept_name(html):
    """Extract the concept name from the page."""
    match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if match:
        return strip_html(match.group(1))
    match = re.search(r'<title>(.*?)\s*\|', html)
    if match:
        return match.group(1).strip()
    return "Unknown"


def extract_software_family(filepath):
    """Extract software family from filename pattern."""
    name = filepath.stem
    # Patterns: alibre-design-term-1, allplan-term-10, constraints-fusion, etc.
    if '-term-' in name:
        return name.rsplit('-term-', 1)[0]
    # Try to extract software from common suffixes
    for suffix in ['-autocad', '-revit', '-fusion', '-solidworks', '-catia',
                   '-nx', '-inventor', '-civil-3d', '-gstarcad', '-zwcad',
                   '-bricscad', '-sketchup', '-rhinoceros', '-blender',
                   '-archicad', '-allplan', '-microstation', '-freecad',
                   '-altium', '-3dsmax', '-draftsight', '-ironcad',
                   '-spaceclaim', '-tekla', '-vectorworks', '-creo',
                   '-abaqus', '-aveva', '-ares']:
        if name.endswith(suffix):
            return suffix[1:]  # remove leading dash
    return "general"


def get_phrasing(concept_name, phrasings_list):
    """Get a deterministic phrasing based on concept name hash."""
    h = int(hashlib.md5(concept_name.encode()).hexdigest(), 16)
    return phrasings_list[h % len(phrasings_list)]


def is_thin_page(html):
    """Check if a page is a thin content page (simple structure, no header-stack)."""
    return 'class="page-shell"' in html and 'class="header-stack"' not in html


def fix_quiz_options(html, concept_name, all_pitfalls, own_pitfalls):
    """Replace the 3 template wrong quiz options with topic-relevant distractors."""
    # Check if this page has quiz options
    if SQL_OPTION not in html:
        return html, False

    # Build a pool of distractors: pitfalls from other pages, excluding own
    own_set = set(own_pitfalls)
    other_pitfalls = [p for p in all_pitfalls if p not in own_set]

    # Pick 3 distractors, preferring shorter ones for quiz options
    random.shuffle(other_pitfalls)

    # Try to get pitfalls from different concept pages
    distractors = []
    seen = set()
    for p in other_pitfalls:
        # Avoid duplicates and overly long options
        if p not in seen and len(p) < 120:
            distractors.append(p)
            seen.add(p)
            if len(distractors) >= 3:
                break

    # Fallback to generic distractors if not enough
    while len(distractors) < 3:
        d = random.choice(GENERIC_DISTRACTORS)
        if d not in distractors and d not in own_set:
            distractors.append(d)

    # Replace the three template options
    html = html.replace(SQL_OPTION, distractors[0])
    html = html.replace(CLOUD_OPTION, distractors[1])
    html = html.replace(LINETYPE_OPTION, distractors[2])

    return html, True


def fix_quiz_feedback(html):
    """Remove the template feedback filler text."""
    if FEEDBACK_TEMPLATE.strip() not in html:
        # Try without leading newlines (might be formatted differently)
        clean_template = FEEDBACK_TEMPLATE.strip()
        if clean_template in html:
            html = html.replace(clean_template, "")
            return html, True
        return html, False

    # Remove the template text, handling both \n\n prefix and standalone
    html = html.replace(FEEDBACK_TEMPLATE, "")
    # Also clean up any remaining version without the leading newlines
    remaining = (
        "Without it, downstream fabrication or cross-discipline model federation "
        "will face geometric conversion anomalies, topological reference losses, and "
        "data transfer discrepancies."
    )
    if remaining in html:
        html = html.replace(remaining, "")

    return html, True


def fix_definition_template(html, concept_name):
    """Replace 'represents a core architectural mechanism' with varied phrasing."""
    if DEFINITION_TEMPLATE not in html:
        return html, False

    phrasing = get_phrasing(concept_name, DEFINITION_PHRASINGS)
    html = html.replace(DEFINITION_TEMPLATE, phrasing)
    return html, True


def fix_why_it_matters_template(html, concept_name):
    """Replace template 'why it matters' phrasing with varied alternative."""
    if WHY_IT_MATTERS_TEMPLATE not in html:
        return html, False

    phrasing = get_phrasing(concept_name, WHY_IT_MATTERS_PHRASINGS)
    html = html.replace(WHY_IT_MATTERS_TEMPLATE, phrasing)
    return html, True


def fix_thin_page_noindex(html):
    """Change robots meta from index to noindex on thin content pages."""
    # Match: <meta name="robots" content="index, follow
    # Replace with: <meta name="robots" content="noindex, follow
    if 'name="robots" content="index, follow' in html:
        html = html.replace(
            'name="robots" content="index, follow',
            'name="robots" content="noindex, follow'
        )
        return html, True
    return html, False


def main():
    print("=" * 60)
    print("SEO Content Issue Fixer")
    print("=" * 60)

    # Phase 1: Collect all pitfalls from all concept pages
    print("\n[Phase 1] Collecting pitfalls from all concept pages...")
    html_files = list(KB_CONCEPTS_DIR.glob("*.html"))
    print(f"  Found {len(html_files)} concept HTML files")

    file_data = {}  # filepath -> (html, concept_name, pitfalls, software_family)
    all_pitfalls = []

    for fpath in html_files:
        try:
            html = fpath.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  WARNING: Could not read {fpath.name}: {e}")
            continue

        concept_name = extract_concept_name(html)
        pitfalls = extract_pitfalls(html)
        family = extract_software_family(fpath)

        file_data[fpath] = {
            "html": html,
            "concept_name": concept_name,
            "pitfalls": pitfalls,
            "family": family,
        }
        all_pitfalls.extend(pitfalls)

    # Deduplicate pitfalls
    all_pitfalls = list(set(all_pitfalls))
    print(f"  Collected {len(all_pitfalls)} unique pitfalls across all pages")

    # Phase 2: Fix all issues
    print("\n[Phase 2] Fixing issues...")
    stats = {
        "quiz_options": 0,
        "quiz_feedback": 0,
        "definition_template": 0,
        "why_it_matters": 0,
        "thin_noindex": 0,
        "total_files_modified": 0,
    }

    for fpath, data in file_data.items():
        html = data["html"]
        concept_name = data["concept_name"]
        pitfalls = data["pitfalls"]
        modified = False

        # Fix 1: Quiz wrong options
        html, changed = fix_quiz_options(html, concept_name, all_pitfalls, pitfalls)
        if changed:
            stats["quiz_options"] += 1
            modified = True

        # Fix 2: Quiz feedback template text
        html, changed = fix_quiz_feedback(html)
        if changed:
            stats["quiz_feedback"] += 1
            modified = True

        # Fix 3: Definition template phrasing
        html, changed = fix_definition_template(html, concept_name)
        if changed:
            stats["definition_template"] += 1
            modified = True

        # Fix 4: "Why it matters" template phrasing
        html, changed = fix_why_it_matters_template(html, concept_name)
        if changed:
            stats["why_it_matters"] += 1
            modified = True

        # Fix 5: Thin content pages - add noindex
        if is_thin_page(html):
            html, changed = fix_thin_page_noindex(html)
            if changed:
                stats["thin_noindex"] += 1
                modified = True

        if modified:
            fpath.write_text(html, encoding="utf-8")
            stats["total_files_modified"] += 1

    # Report
    print("\n" + "=" * 60)
    print("FIX SUMMARY")
    print("=" * 60)
    print(f"  Quiz options replaced:        {stats['quiz_options']}")
    print(f"  Quiz feedback text removed:    {stats['quiz_feedback']}")
    print(f"  Definition templates fixed:    {stats['definition_template']}")
    print(f"  'Why it matters' templates:    {stats['why_it_matters']}")
    print(f"  Thin pages set to noindex:     {stats['thin_noindex']}")
    print(f"  Total files modified:          {stats['total_files_modified']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
