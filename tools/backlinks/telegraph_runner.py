import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# -*- coding: utf-8 -*-
"""
Telegraph (DA 92+) Publisher for CAD Learn Hub
"""
import os
import sys
import json
import urllib.request
from tracker import add_backlink

TELEGRAPH_TOKEN = None

def get_or_create_token():
    global TELEGRAPH_TOKEN
    if TELEGRAPH_TOKEN:
        return TELEGRAPH_TOKEN
        
    token_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "telegraph_token.txt")
    if os.path.exists(token_file):
        with open(token_file, "r", encoding="utf-8") as f:
            t = f.read().strip()
            if t:
                TELEGRAPH_TOKEN = t
                return t
                
    # Create new account
    payload = json.dumps({
        "short_name": "cadlearn",
        "author_name": "CAD Learn Hub Editorial",
        "author_url": "https://gstarcademy.com"
    }).encode("utf-8")
    req = urllib.request.Request("https://api.telegra.ph/createAccount", data=payload, headers={
        "Content-Type": "application/json"
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        if data.get("ok"):
            t = data["result"]["access_token"]
            with open(token_file, "w", encoding="utf-8") as f:
                f.write(t)
            TELEGRAPH_TOKEN = t
            return t
    return None

def publish_telegraph_page(title, content_nodes, target_url="https://gstarcademy.com"):
    print("=" * 60)
    print(f"🚀 Publishing to Telegraph (DA 92+): {title}")
    print("=" * 60)
    
    token = get_or_create_token()
    if not token:
        print("❌ Could not get Telegraph token!")
        return None
        
    payload = json.dumps({
        "access_token": token,
        "title": title,
        "author_name": "CAD Learn Hub",
        "author_url": "https://gstarcademy.com",
        "content": content_nodes,
        "return_content": False
    }).encode("utf-8")
    
    req = urllib.request.Request("https://api.telegra.ph/createPage", data=payload, headers={
        "Content-Type": "application/json"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                url = data["result"]["url"]
                print(f"🎉 Successfully published to Telegraph! Live URL: {url}")
                
                # Record backlink
                add_backlink(
                    platform="Telegraph (High Authority DA 92+)",
                    domain_authority="DA 92+",
                    category="Technical Engineering Guide",
                    post_title=title,
                    target_url=target_url,
                    backlink_url=url,
                    anchor_text="CAD Learn Hub: Comparison Matrix & Learning Center",
                    link_type="Dofollow / Editorial",
                    status="Live",
                    notes="Instant indexing, permanent high-DA publishing platform"
                )
                return url
            else:
                print(f"❌ Telegraph error: {data.get('error')}")
                return None
    except Exception as e:
        print(f"❌ Error calling Telegraph API: {e}")
        return None

if __name__ == "__main__":
    t = "CAD Software Comparison 2026: AutoCAD vs SolidWorks vs Revit vs FreeCAD"
    nodes = [
        {"tag": "h3", "children": ["The Modern CAD Landscape in 2026"]},
        {"tag": "p", "children": ["Selecting the right Computer-Aided Design (CAD) environment is one of the most critical decisions for engineering departments and aspiring drafters. Below is a structured comparison across the four primary industry pillars."]},
        {"tag": "h4", "children": ["1. General Drafting & Documentation: AutoCAD / GstarCAD"]},
        {"tag": "p", "children": ["AutoCAD remains the global standard for 2D technical drawings, schematics, and construction documentation (.dwg format). Cost-effective direct alternatives like GstarCAD provide full DWG compatibility with zero learning curve and perpetual licensing options."]},
        {"tag": "h4", "children": ["2. Mechanical Product Design: SolidWorks / Inventor / Fusion 360"]},
        {"tag": "p", "children": ["Feature-based parametric modeling dominates consumer product, aerospace, and machinery engineering. SolidWorks leads in traditional desktop assembly modeling, while cloud-native tools offer agile revision control."]},
        {"tag": "h4", "children": ["3. Architecture & Construction: Revit / ArchiCAD"]},
        {"tag": "p", "children": ["Building Information Modeling (BIM) replaces dumb lines with data-rich parametric components. Revit enables collaborative multi-discipline coordination across structural, MEP, and architectural scopes."]},
        {"tag": "h4", "children": ["4. Open-Source Freedom: FreeCAD"]},
        {"tag": "p", "children": ["For developers, makers, and cost-conscious startups, FreeCAD provides a fully extensible Python-scripted parametric kernel without subscription vendor lock-in."]},
        {"tag": "hr"},
        {"tag": "h3", "children": ["Explore In-Depth Software Benchmarks & Tutorials"]},
        {"tag": "p", "children": [
            "Access detailed feature comparisons, format support, and pricing models at the ",
            {"tag": "a", "attrs": {"href": "https://gstarcademy.com/kb-software.html"}, "children": ["CAD Software Comparison Matrix on CAD Learn Hub"]},
            "."
        ]},
        {"tag": "p", "children": [
            "Test your CAD competency across 6 disciplines: ",
            {"tag": "a", "attrs": {"href": "https://gstarcademy.com/quiz.html"}, "children": ["Free Interactive CAD Proficiency Assessment"]},
            "."
        ]}
    ]
    publish_telegraph_page(t, nodes, target_url="https://gstarcademy.com/kb-software.html")
