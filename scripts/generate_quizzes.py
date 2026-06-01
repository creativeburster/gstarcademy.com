#!/usr/bin/env python3
"""
Generate and inject professional technical self-test quizzes
into all terms across data/sw/*.json.

Usage:
    python scripts/generate_quizzes.py
"""

import json
import glob
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SW_DIR = REPO / "data" / "sw"

# Hand-crafted expert quizzes for prominent concepts
CUSTOM_QUIZZES = {
    "bim": [
        {
            "question": "What is the primary architectural difference between CAD and BIM coordination?",
            "options": [
                "BIM operates on object-based relational databases with smart parameters, while CAD is primarily line-and-layer representation.",
                "BIM is restricted to cloud storage, while CAD can only run offline.",
                "BIM allows unlimited layers, while CAD has a hard limit of 255 layers.",
                "BIM models do not support 2D drawing generation, forcing 3D-only deliverables."
            ],
            "answer_idx": 0,
            "explanation": "BIM is data-centric; it models intelligent objects (walls, doors) in a relational database, whereas 2D CAD relies on geometric lines, arcs, and layering strategies to convey design intent."
        }
    ],
    "xref-autocad": [
        {
            "question": "Why are XREFs preferred over copying and pasting shared geometry in host CAD drawings?",
            "options": [
                "XREFs automatically merge block attributes and assign random colors to avoid drawing overlapping.",
                "XREFs keep host files lightweight and ensure that modifications in the referenced file propagate automatically on reload.",
                "XREFs explode dynamic blocks upon insertion to optimize GPU rendering performance.",
                "XREFs convert drawing coordinates to GIS latitude and longitude coordinates automatically."
            ],
            "answer_idx": 1,
            "explanation": "XREFs maintain external links to DWGs rather than copying their entities locally. This keeps host drawing databases compact and ensures all concurrent modifications reload automatically."
        }
    ],
    "paper-space-autocad": [
        {
            "question": "What is the best-practice setup for plotting annotations and sheet titles in AutoCAD layouts?",
            "options": [
                "Draw the sheet title block in model space at 1:1, scale it up by 100x, and place annotations inside model space.",
                "Draft the sheet border and title block at 1:1 in paper space, using locked viewports to scale and display model-space geometry.",
                "Avoid layouts entirely and plot directly from model space using manual annotation scale overrides.",
                "Configure a different CTB file for every drawing viewport and scale coordinates by hand."
            ],
            "answer_idx": 1,
            "explanation": "Best practice is to draw layout sheets and title blocks at 1:1 in Paper Space, placing viewports to scale and view the underlying 1:1 Model Space geometry, then locking the viewport scale."
        }
    ],
    "dynamic-blocks-autocad": [
        {
            "question": "Which of the following is true regarding Dynamic Blocks in AutoCAD?",
            "options": [
                "Dynamic Blocks contain parametric grips, lookup tables, and visibility actions, but do not carry native BIM database schedules.",
                "Dynamic Blocks automatically inherit 3D BIM structural constraints and sync coordination scales.",
                "Dynamic Blocks remain fully parametric even after executing the EXPLODE command.",
                "Dynamic Blocks cannot be customized or edited once saved in the active DWG database."
            ],
            "answer_idx": 0,
            "explanation": "Dynamic Blocks offer excellent graphical intelligence (grips, stretches, lookup states) but are not full BIM database objects; also, exploding them completely destroys their parametric behavior."
        }
    ],
    "annotative-objects": [
        {
            "question": "What is the primary function of Annotative scaling in AutoCAD?",
            "options": [
                "It automatically changes the lineweight of objects based on printing paper size.",
                "It scales annotations (text, dimensions, hatches) to display at identical plotted sizes across viewports of different scales.",
                "It converts text fonts to vectors to make PDFs searchable.",
                "It locks the coordinate systems of XREFs to align with model space."
            ],
            "answer_idx": 1,
            "explanation": "Annotative scaling lets text, dimensions, and blocks resize themselves relative to the viewport scale. This ensures a 2.5mm text note plots at exactly 2.5mm whether viewed at 1:100 or 1:20."
        }
    ],
    "autolisp": [
        {
            "question": "What happens when you load and execute an AutoLISP script in a multi-document CAD environment?",
            "options": [
                "The LISP script acts globally across all active workgroups and projects.",
                "AutoLISP is document-specific; its variables and functions load into the active drawing's namespace and must be reloaded for other drawings.",
                "The script compiled binary code directly into the CPU core caches.",
                "The script requires a continuous cloud connection to execute ObjectARX interfaces."
            ],
            "answer_idx": 1,
            "explanation": "AutoLISP operates within the context of a single document's memory namespace. To run automation across multiple drawings, scripts are typically auto-loaded via 'acaddoc.lsp' or batch utilities like ScriptPro."
        }
    ],
    "plot-style": [
        {
            "question": "What is the key difference between color-dependent (.ctb) and named (.stb) plot styles?",
            "options": [
                "CTB files map plotting settings directly to entity index colors, while STB files assign style definitions independent of color.",
                "CTB works for raster layouts, whereas STB works exclusively for vector plotting.",
                "CTB styles can only plot in black and white, while STB allows full true color.",
                "CTB is used for 3D modeling projections, and STB is limited to 2D drafting sheets."
            ],
            "answer_idx": 0,
            "explanation": "CTB (Color-Dependent) maps the 255 AutoCAD color index codes directly to lineweights and plotted colors. STB (Style-Dependent) decouples plotting representation from entity color, allowing more flexible styling."
        }
    ],
    "constraints-autocad": [
        {
            "question": "How do CAD parametric constraints differ from standard drawing geometry?",
            "options": [
                "Constraints enforce geometric or dimensional rules that govern object behavior, maintaining design relationships under edits.",
                "Constraints convert 2D lines into high-performance 3D STL meshes automatically.",
                "Constraints bypass AutoCAD's coordinates and save files in raw cloud formats.",
                "Constraints lock the entire DWG database, preventing any further user edits."
            ],
            "answer_idx": 0,
            "explanation": "Parametric constraints apply mathematical rules (parallelism, concentricity, exact distance formulas) to elements so that altering one part updates related elements automatically."
        }
    ]
}

def clean_value(v):
    if isinstance(v, list):
        return [clean_value(x) for x in v]
    if isinstance(v, dict):
        return {k: clean_value(val) for k, val in v.items()}
    if isinstance(v, str):
        # strip markdown and carriage returns
        return v.replace("\r\n", "\n").replace("\r", "\n").strip()
    return v

def generate_fallback_quiz(term: dict) -> list[dict]:
    title = term.get("title", "this concept")
    short_def = term.get("short_def") or "a key engineering concept."
    why_matters = term.get("why_matters") or "It optimizes productivity and coordinates design deliverables."
    pitfalls = term.get("common_pitfalls") or []
    
    # Capitalize title first char for grammar
    cap_title = title[0].upper() + title[1:] if title else "This concept"
    
    if pitfalls and len(pitfalls) >= 1:
        primary_pitfall = pitfalls[0].strip(".")
        question = f"When working with {title}, which of the following represents a common technical pitfall?"
        options = [
            f"{primary_pitfall}.",
            f"Failing to manually re-index the SQL server database.",
            f"Over-allocating virtual memory caches in the cloud settings.",
            f"Restricting linetype scales strictly to 1:1 paper coordinates."
        ]
        answer_idx = 0
        explanation = f"Correct. A common pitfall is '{primary_pitfall}.' As the editorial review notes: '{why_matters}'"
    else:
        question = f"What is the primary technical objective of {title}?"
        options = [
            f"{short_def.strip('.')}.",
            f"Enforcing automatic cloud-only model synchronization cycles.",
            f"Replacing the standard DWG entity database with SVG text.",
            f"Converting all 2D layouts to multi-axis CAM scripts."
        ]
        answer_idx = 0
        explanation = f"Correct. {cap_title} is primarily used to {short_def.lower().strip('.')}. {why_matters}"

    return [
        {
            "question": question,
            "options": options,
            "answer_idx": answer_idx,
            "explanation": explanation
        }
    ]

def main():
    files = sorted(SW_DIR.glob("*.json"))
    modified_count = 0
    total_quizzes = 0
    
    for file_path in files:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        changed = False
        
        for term in data.get("terms", []):
            slug = term.get("slug")
            
            # Clean existing keys first to keep structure clean
            for k in ["definition", "why_matters", "short_def"]:
                if k in term:
                    term[k] = clean_value(term[k])
            if "common_pitfalls" in term:
                term["common_pitfalls"] = [clean_value(x) for x in term["common_pitfalls"]]
            
            # Check if quiz exists. If not, inject.
            if "quiz" not in term or not term["quiz"]:
                if slug in CUSTOM_QUIZZES:
                    term["quiz"] = CUSTOM_QUIZZES[slug]
                else:
                    term["quiz"] = generate_fallback_quiz(term)
                changed = True
                total_quizzes += 1
                
        if changed:
            file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            modified_count += 1
            
    print(f"Injected {total_quizzes} quizzes across {modified_count} software JSON files.")

if __name__ == "__main__":
    main()
