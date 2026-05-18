import re

def analyze_faq():
    with open("kb-faq.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find all data-kb-faq-topic attributes
    topics = re.findall(r'data-kb-faq-topic=["\'](.*?)["\']', content)
    print("=== FAQ Counts ===")
    from collections import Counter
    c = Counter(topics)
    for topic, count in c.most_common():
        print(f"{topic}: {count}")

def analyze_terms():
    with open("kb-terms.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Let's count how many terms links exist in the file
    links = re.findall(r'href=["\']\./kb/concepts/(.*?)["\']', content)
    print("\n=== Terms/Concepts Links in kb-terms.html ===")
    print(f"Total concept links in kb-terms.html: {len(links)}")
    
    # Categorize them roughly by prefix/vendor
    categories = {
        "dassault": 0,
        "solidworks": 0,
        "catia": 0,
        "draftsight": 0,
        "autodesk": 0,
        "autocad": 0,
        "revit": 0,
        "fusion": 0,
        "inventor": 0,
        "civil3d": 0,
        "gstarcad": 0,
        "gstarsoft": 0,
        "siemens": 0,
        "ptc": 0,
        "bentley": 0,
        "neutral/basic": 0
    }
    
    for l in links:
        matched = False
        for key in categories.keys():
            if key in l.lower().replace("-", ""):
                categories[key] += 1
                matched = True
                break
        if not matched:
            categories["neutral/basic"] += 1
            
    for cat, count in categories.items():
        if count > 0:
            print(f"  {cat}: {count}")

def analyze_graph():
    with open("knowledge.js", "r", encoding="utf-8") as f:
        content = f.read()
    
    # We want to parse the const nodes array in knowledge.js
    # Let's find the nodes array
    nodes_match = re.search(r'const nodes\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not nodes_match:
        print("\nCould not find nodes array in knowledge.js")
        return
        
    nodes_text = nodes_match.group(1)
    # Parse individual node objects
    # Example: { id: "AutoCAD", type: "product", tags: ["2d", "aec", "terms"], descZh: "", hint: "..." }
    node_entries = re.findall(r'\{\s*id:\s*["\'](.*?)["\'](.*?)\}', nodes_text)
    
    print("\n=== Graph Nodes in knowledge.js ===")
    print(f"Total graph nodes: {len(node_entries)}")
    
    # Let's count nodes by tag/vendor
    vendor_counts = {
        "autodesk": 0,
        "dassault": 0,
        "gstarcad": 0,
        "gstarsoft": 0,
        "siemens": 0,
        "ptc": 0,
        "bentley": 0,
        "other": 0
    }
    
    for node_id, rest in node_entries:
        rest_lower = rest.lower() + " " + node_id.lower()
        matched = False
        for vendor in ["autodesk", "dassault", "siemens", "ptc", "bentley"]:
            if vendor in rest_lower or vendor in node_id.lower():
                vendor_counts[vendor] += 1
                matched = True
                break
        if not matched:
            if "gstarcad" in rest_lower or "gstarsoft" in rest_lower:
                vendor_counts["gstarcad"] += 1
            else:
                vendor_counts["other"] += 1
                
    for vendor, count in vendor_counts.items():
        print(f"  {vendor}: {count}")

def print_autodesk_faqs():
    with open("kb-faq.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Let's find all article blocks with data-kb-faq-topic for autocad, revit, civil3d, inventor, fusion
    import re
    articles = re.findall(r'<article class="kb-faq-entry" data-kb-faq-topic="(autocad|revit|civil3d|inventor|fusion)">(.*?)</article>', content, re.DOTALL)
    
    print("\n=== Autodesk FAQs ===")
    for topic, body in articles:
        q_match = re.search(r'<h3>(.*?)</h3>', body)
        q = q_match.group(1) if q_match else "No Q"
        print(f"[{topic.upper()}] {q}")

if __name__ == "__main__":
    analyze_faq()
    print_autodesk_faqs()
