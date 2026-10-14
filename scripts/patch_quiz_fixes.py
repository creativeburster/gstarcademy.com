import re

with open("quiz.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. successPrimaryBtn selector fix
code = code.replace(
    "const successPrimaryBtn = successView.querySelector('.btn-primary');",
    "const successPrimaryBtn = document.getElementById('quiz-continue-btn') || successView.querySelector('a.btn-primary');"
)

# 2. viz-l3-aov-passes multiple choice fix
old_viz = '''          {
            "nodeId": "rendering",
            "slug": "viz-l3-aov-passes",
            "difficulty": "intermediate",
            "question": "Which layers are typically rendered as separate AOVs (passes) for post-production compositing? (Select all correct)",
            "options": [
              "Diffuse color and lighting",
              "Reflections and specular highlights",
              "Z-depth for fog and depth-of-field effects",
              "Polygon count statistics of the scene"
            ],
            "correctIdx": 0,'''

new_viz = '''          {
            "type": "multiple",
            "nodeId": "rendering",
            "slug": "viz-l3-aov-passes",
            "difficulty": "intermediate",
            "question": "Which layers are typically rendered as separate AOVs (passes) for post-production compositing? (Select all correct)",
            "options": [
              "Diffuse color and lighting",
              "Reflections and specular highlights",
              "Z-depth for fog and depth-of-field effects",
              "Polygon count statistics of the scene"
            ],
            "correctIndices": [
              0,
              1,
              2
            ],'''
code = code.replace(old_viz, new_viz)

# 3. lod-bim fix
old_lodbim = '''            "options": [
              "LOD 300 contains approximate sizing for aesthetic design, while LOD 400 includes precise fabrication, assembly, and installation details.",'''
new_lodbim = '''            "options": [
              "LOD 300 defines specific assemblies with accurate quantity, size, shape, location, and orientation suitable for construction documentation, whereas LOD 400 includes shop fabrication, assembly, and installation details.",'''
code = code.replace(old_lodbim, new_lodbim)

# 4. placement-bim-lod why fix
old_place_why = '"why": "LOD 300 defines approximate elements with general size and orientation. LOD 400 includes exact fabrication detailing suitable for site installers."'
new_place_why = '"why": "LOD 300 defines accurate element geometry (size, shape, location, and orientation) suitable for construction documentation, while LOD 400 adds precise shop fabrication and installation detailing."'
code = code.replace(old_place_why, new_place_why)

# 5. surface roughness fix
old_rz = '"Ra calculates the arithmetic mean roughness across the profile, while Rz measures the average height of the 5 highest peaks and 5 deepest valleys."'
new_rz = '"Ra calculates the arithmetic mean height of profile deviations, whereas Rz measures the mean peak-to-valley profile height across sampling lengths, making it far more sensitive to isolated scratch defects."'
code = code.replace(old_rz, new_rz)

old_rz_why = '"why": "Ra averages out extreme scratches and spikes; Rz highlights deep surface gouges that could cause seal leakage or fatigue notch cracking."'
new_rz_why = '"why": "Under modern ISO 4287 and ISO 21920-2, Rz measures the mean of the maximum peak-to-valley heights across sampling lengths (replacing legacy 10-point height RzJIS). Unlike Ra, which averages out isolated defects, Rz directly catches deep scratches or burrs on sealing and bearing surfaces."'
code = code.replace(old_rz_why, new_rz_why)

# 6. EEXTRACT fix
code = code.replace(
    '"The Data Extraction (EEXTRACT) wizard over block attributes and object properties"',
    '"The Data Extraction (DATAEXTRACTION / EATTEXT) wizard over block attributes and object properties"'
)

# 7. duplicate slug fix
old_dup_slug = '''          {
            "type": "single",
            "nodeId": "gdt",
            "slug": "gdt-geometric-tolerancing",
            "difficulty": "intermediate",
            "question": "Which geometric characteristic symbol in ASME Y14.5 / ISO 1101 controls the form of a cylindrical feature surface without requiring a reference datum?",'''

new_dup_slug = '''          {
            "type": "single",
            "nodeId": "gdt",
            "slug": "mcad-l7-cylindricity-form-control",
            "difficulty": "intermediate",
            "question": "Which geometric characteristic symbol in ASME Y14.5 / ISO 1101 controls the form of a cylindrical feature surface without requiring a reference datum?",'''
code = code.replace(old_dup_slug, new_dup_slug)

# 8. LaTeX to Unicode transformations for clean rendering
replacements = [
    (r"\$\\varnothing\s*([0-9\.]+)\s*\\pm\s*([0-9\.]+)\$", r"⌀\1 ± \2"),
    (r"\$\\varnothing\s*([0-9\.]+)\$", r"⌀\1"),
    (r"\\varnothing", "⌀"),
    (r"\\pm", "±"),
    (r"\\ge", "≥"),
    (r"\\le", "≤"),
    (r"\\times", "×"),
    (r"\\mu\s*m", "µm"),
    (r"\\mu", "µ"),
    (r"\\Delta\s*t", "Δt"),
    (r"\\Delta\s*x", "Δx"),
    (r"\\Delta", "Δ"),
    (r"\$\{y\}\^\{\+\}\s*<\s*1\$", "y⁺ < 1"),
    (r"\$\{y\}\^\{\+\}\s*\\le\s*5\$", "y⁺ ≤ 5"),
    (r"\$\{y\}\^\{\+\}\$", "y⁺"),
    (r"\$\{y\}\^\{\+\}", "y⁺"),
    (r"\$y\^\+\$", "y⁺"),
    (r"\$y\^\+", "y⁺"),
    (r"\\\(E\(\\rho\)\s*=\s*\\rho\^p\s*E_0\\\)", "E(ρ) = ρᵖ E₀"),
    (r"\\\(C\s*=\s*u\s*\\Delta\s*t\s*/\s*\\Delta\s*x\s*\\le\s*C_\{max\}\\\)", "C = u Δt / Δx ≤ C_max"),
    (r"\\\(C\s*=\s*u\s*\\Delta\s*t\s*/\s*\\Delta\s*x\\\)", "C = u Δt / Δx"),
    (r"\\\(u\s*\\Delta\s*t\s*/\s*\\Delta\s*x\\\)", "u Δt / Δx"),
    (r"\\\(v\s*\\Delta\s*t\s*/\s*\\Delta\s*y\\\)", "v Δt / Δy"),
    (r"\\\(w\s*\\Delta\s*t\s*/\s*\\Delta\s*z\\\)", "w Δt / Δz"),
    (r"\\\(.*?\\le.*?\\\)", lambda m: m.group(0).replace(r"\(", "").replace(r"\)", "").replace(r"\le", "≤")),
    (r"\$k\$-\$\\omega\$", "k-ω"),
    (r"\$k\$-\$\\epsilon\$", "k-ε"),
]

for pat, repl in replacements:
    if callable(repl):
        code = re.sub(pat, repl, code)
    else:
        code = re.sub(pat, repl, code)

# Clean any remaining inline dollar math wrappers like $0.20$ or $0.18$
code = re.sub(r"\$([0-9\.]+)\$", r"\1", code)

with open("quiz.js", "w", encoding="utf-8") as f:
    f.write(code)

print("quiz.js logic, concepts, and LaTeX formatting successfully patched!")
