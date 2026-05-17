with open("knowledge.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# 1. Define nodes to append
NEW_NODES = """    { id: "SOLIDWORKS", type: "product", tags: ["dassault"], hint: "Industry standard 3D parametric mechanical CAD." },
    { id: "CATIA", type: "product", tags: ["dassault"], hint: "Enterprise high-end PLM and advanced surfacing CAD." },
    { id: "ENOVIA", type: "product", tags: ["dassault"], hint: "Enterprise data governance & lifecycle PLM." },
    { id: "SIMULIA", type: "product", tags: ["dassault"], hint: "Unified advanced engineering simulation." },
    { id: "DELMIA", type: "product", tags: ["dassault"], hint: "Digital manufacturing & factory process simulation." },
    { id: "SOLIDWORKS PDM", type: "skill", tags: ["solidworks"], hint: "Version control & vault data management." },
    { id: "CATIA GSD", type: "skill", tags: ["catia"], hint: "Generative Shape Design aerospace surfacing." },
    { id: "CAA SDK", type: "sdk", tags: ["catia"], hint: "High-performance C++ developer interface." },
    { id: "SOLIDWORKS API", type: "sdk", tags: ["solidworks"], hint: ".NET & VBA custom automation." },
    { id: "SOLIDWORKS Configurations", type: "skill", tags: ["solidworks"], hint: "Multi-dimension design variants manager." },
    { id: "Abaqus", type: "skill", tags: ["simulia"], hint: "Advanced nonlinear structural FEA solver." },
    { id: "PowerCopy", type: "skill", tags: ["catia"], hint: "Feature-level template pattern reuse." },
    { id: "Hybrid Design", type: "skill", tags: ["catia"], hint: "Solid and surface mixed chronological modeling." },
    { id: "Composites Design", type: "skill", tags: ["catia"], hint: "Carbon-fiber ply layup & draping simulation." },
    { id: "FT&A MBD", type: "skill", tags: ["catia"], hint: "Functional tolerancing & drawingless 3D annotations." },
    { id: "SpeedPak", type: "skill", tags: ["solidworks"], hint: "Large assembly high-speed graphics subset." },
    { id: "eDrawings", type: "skill", tags: ["solidworks"], hint: "Lightweight multi-CAD collaborative viewer." },
    { id: "Collaborative Sharing", type: "skill", tags: ["3dexperience"], hint: "Cloud co-authoring workspace governance." },
    { id: "Large Design Review", type: "skill", tags: ["solidworks"], hint: "Ultra-fast large assembly visualization & review." },
    { id: "Weldments (SW)", type: "skill", tags: ["solidworks"], hint: "Structural steel frames & cut lists." },
    { id: "Sheet Metal (SW)", type: "skill", tags: ["solidworks"], hint: "Folded part stretch & unfold pattern checks." },
    { id: "Part Design (CATIA)", type: "skill", tags: ["catia"], hint: "High-reliability parametric solid features." },
    { id: "Assembly Design (CATIA)", type: "skill", tags: ["catia"], hint: "Constraint resolution & clash check mockups." },
    { id: "DELMIA Simulation", type: "skill", tags: ["delmia"], hint: "Robotic cell programming offline." },"""

# Locate final node
node_needle = '{ id: "ContextCapture", type: "skill", tags: ["bentley"] },'
if 'id: "SOLIDWORKS"' not in js_content:
    js_content = js_content.replace(node_needle, node_needle + "\n" + NEW_NODES)
    print("Injected Dassault nodes successfully.")
else:
    print("Nodes already existed.")

# 2. Define links to append
NEW_LINKS = """    ["Dassault", "SOLIDWORKS"],
    ["Dassault", "CATIA"],
    ["Dassault", "ENOVIA"],
    ["Dassault", "SIMULIA"],
    ["Dassault", "DELMIA"],
    ["SOLIDWORKS", "SOLIDWORKS PDM"],
    ["SOLIDWORKS", "SOLIDWORKS API"],
    ["SOLIDWORKS", "SOLIDWORKS Configurations"],
    ["SOLIDWORKS", "Weldments (SW)"],
    ["SOLIDWORKS", "Sheet Metal (SW)"],
    ["SOLIDWORKS", "eDrawings"],
    ["SOLIDWORKS", "Large Design Review"],
    ["SOLIDWORKS", "SpeedPak"],
    ["CATIA", "CATIA GSD"],
    ["CATIA", "CAA SDK"],
    ["CATIA", "PowerCopy"],
    ["CATIA", "Hybrid Design"],
    ["CATIA", "Composites Design"],
    ["CATIA", "FT&A MBD"],
    ["CATIA", "Part Design (CATIA)"],
    ["CATIA", "Assembly Design (CATIA)"],
    ["3DEXPERIENCE", "Collaborative Sharing"],
    ["3DEXPERIENCE", "ENOVIA"],
    ["SIMULIA", "Abaqus"],
    ["DELMIA", "DELMIA Simulation"],"""

link_needle = '["Siemens", "STEP"],'
# Let's check which is the last link in knowledge.js.
# Around line 640:
#     ["Siemens", "STEP"],
#   ];
# Since there are multiple ["Siemens", "STEP"], let's use a unique sequence or the block near 639-640.
# Let's inspect the target block in knowledge.js to replace:
#     ["Bentley", "ProSteel"],
#     ["Learning branch", "AEC"],
#     ["Learning branch", "MFG"],
#     ["Siemens", "STEP"],
#   ];

target_block = """    ["Bentley", "ProSteel"],
    ["Learning branch", "AEC"],
    ["Learning branch", "MFG"],
    ["Siemens", "STEP"],"""

replacement_block = target_block + "\n" + NEW_LINKS

if '["Dassault", "SOLIDWORKS"]' not in js_content:
    js_content = js_content.replace(target_block, replacement_block)
    print("Injected Dassault links successfully.")
else:
    print("Links already existed.")

with open("knowledge.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("Knowledge graph enrichment complete!")
