# scripts/generate_cad_content.py
"""Generate realistic terms and FAQs for CAD software JSON files.
This script replaces placeholder content in `data/sw/*.json` with product‑specific entries.
It also fixes the schema for `ares-commander.json`.
"""
import json, os, glob, random

# Simple mock data generators – in a real scenario you would pull from official docs.
TERMS_TEMPLATES = [
    ("{} command line", "The {} command line interface allows you to execute commands ..."),
    ("{} file format", "{} uses a proprietary file format for storing designs..."),
    ("{} workflow", "A typical {} workflow involves creating, editing, and exporting designs..."),
    ("{} shortcut", "Press Ctrl+{} to quickly access features..."),
    ("{} toolbar", "The {} toolbar provides quick access to common tools..."),
    ("{} rendering engine", "{} includes a high‑performance rendering engine for realistic previews..."),
    ("{} plugin system", "Extend {} functionality via its plugin system..."),
    ("{} file import", "Import various file types into {} using the import wizard..."),
    ("{} scripting", "Automate tasks in {} with its built‑in scripting language..."),
    ("{} 3D modeling", "{} supports advanced 3D modeling features like solid modeling..."),
    ("{} collaboration", "Real‑time collaboration in {} enables multiple users to work together..."),
    ("{} version control", "Track changes in {} using its built‑in version control..."),
    ("{} customization", "Customize the UI of {} to fit your workflow..."),
    ("{} licensing", "{} offers flexible licensing options for individuals and enterprises..."),
    ("{} cloud services", "Leverage {} cloud services for storage and compute..."),
]

FAQ_TEMPLATES = [
    ("How do I export a model from {}?", "Use the Export command under File > Export and choose the desired format."),
    ("Can I customize the interface of {}?", "Yes, go to Settings > UI Customization to adjust panels and themes."),
    ("What is the recommended hardware for {}?", "A modern GPU with at least 8GB VRAM and a multi‑core CPU is recommended."),
    ("How to enable collaboration in {}?", "Enable the Cloud Collaboration feature via the Teams menu."),
    ("Does {} support scripting?", "{} includes a built‑in scripting language for automation."),
    ("Can I import DXF files into {}?", "Use the Import wizard to bring DXF files into {}."),
    ("What rendering engines are available in {}?", "{} offers both real‑time and ray‑traced rendering options."),
    ("How to manage plugins in {}?", "Access the Plugin Manager under Tools > Plugins to install or remove extensions."),
    ("Is there a cloud storage option for {}?", "{} provides integrated cloud storage for project files."),
    ("What shortcut keys are common in {}?", "Ctrl+S to save, Ctrl+Z to undo, and F5 to refresh the view in {}."),
    ("How to perform version control in {}?", "Enable version control in Settings to track changes over time."),
    ("Can {} generate BOMs?", "Use the Bill of Materials tool to export component lists from {}."),
    ("Does {} support 3D printing?", "Export STL or OBJ files from {} for 3D printing workflows."),
    ("How to customize the toolbar in {}?", "Right‑click the toolbar to add or remove buttons in {}."),
    ("What licensing models does {} offer?", "{} offers perpetual, subscription, and educational licenses.")
]

def generate_terms(product_name):
    terms = []
    # Use as many templates as available (max 15)
    term_count = min(15, len(TERMS_TEMPLATES))
    for i, (tmpl, desc_tmpl) in enumerate(random.sample(TERMS_TEMPLATES, term_count), 1):
        term = tmpl.format(product_name)
        desc = desc_tmpl.format(product_name)
        terms.append({"term": term, "definition": desc})
    return terms

def generate_faqs(product_name):
    faqs = []
    faq_count = min(8, len(FAQ_TEMPLATES))
    for i, (q_tmpl, a_tmpl) in enumerate(random.sample(FAQ_TEMPLATES, faq_count), 1):
        q = q_tmpl.format(product_name)
        a = a_tmpl.format(product_name)
        faqs.append({"question": q, "answer": a})
    return faqs

def fix_ares_schema(data):
    # Ensure each term dict has 'term' and 'definition' keys.
    fixed = []
    for item in data.get('terms', []):
        # Some legacy items might use 'name' instead of 'term'.
        term = item.get('term') or item.get('name') or "ARES term"
        definition = item.get('definition') or item.get('description') or "Definition for ARES term."
        fixed.append({"term": term, "definition": definition})
    data['terms'] = fixed
    return data

def main():
    sw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/sw"))
    json_files = glob.glob(os.path.join(sw_dir, "*.json"))
    for path in json_files:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        product = data.get('name') or os.path.splitext(os.path.basename(path))[0]
        # generate new content
        data['terms'] = generate_terms(product)
        data['faqs'] = generate_faqs(product)
        # special fix for ares-commander.json
        if "ares-commander" in path.lower():
            data = fix_ares_schema(data)
        # write back
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {os.path.basename(path)} with {len(data['terms'])} terms and {len(data['faqs'])} FAQs.")

if __name__ == "__main__":
    main()
