import os
import json
import re

def main():
    print("=================== CAD Learn Hub Stats ===================")
    
    # 1. Vendors (商家/厂商)
    vendor_files = []
    if os.path.exists("kb/vendors"):
        vendor_files = [f for f in os.listdir("kb/vendors") if f.endswith(".html")]
    print(f"1. 厂商页面 (kb/vendors/ *.html): 共 {len(vendor_files)} 个页面文件")
    for f in sorted(vendor_files):
        size = os.path.getsize(os.path.join("kb/vendors", f))
        # print(f"   - {f} ({size} bytes)")

    # 2. Software (软件)
    software_files = []
    if os.path.exists("kb/software"):
        software_files = [f for f in os.listdir("kb/software") if f.endswith(".html") and f != "index.html"]
    print(f"2. 软件页面 (kb/software/ *.html): 共 {len(software_files)} 个页面文件 (排除 index.html)")

    # Let's load data/kb_software.json
    sw_json_items = []
    if os.path.exists("data/kb_software.json"):
        with open("data/kb_software.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            sw_json_items = data.get("items", [])
    print(f"   - data/kb_software.json 中定义的软件项: 共 {len(sw_json_items)} 个")

    # Let's load files in data/sw/
    sw_data_files = []
    if os.path.exists("data/sw"):
        sw_data_files = [f for f in os.listdir("data/sw") if f.endswith(".json")]
    print(f"   - data/sw/ 目录下的软件JSON详情数据: 共 {len(sw_data_files)} 个文件")

    # 3. Completeness analysis (档案是否齐全)
    # Check if every software in data/kb_software.json or data/sw has a corresponding HTML in kb/software
    print("\n3. 软件档案齐全度分析:")
    json_slugs = {item["slug"] for item in sw_json_items}
    sw_dir_slugs = {f.replace(".json", "") for f in sw_data_files}
    html_slugs = {f.replace(".html", "") for f in software_files}
    
    all_known_slugs = json_slugs.union(sw_dir_slugs)
    
    missing_html = all_known_slugs - html_slugs
    extra_html = html_slugs - all_known_slugs
    
    print(f"   - 总共涉及的软件标识 (slug) 数量: {len(all_known_slugs)}")
    print(f"   - 已生成 HTML 档案的软件数量: {len(html_slugs)}")
    if missing_html:
        print(f"   - [警告] 缺少 HTML 档案的软件: {sorted(list(missing_html))}")
    else:
        print(f"   - [恭喜] 所有已知软件均有对应的 HTML 档案！")
        
    # Check vendor completeness
    # Read all vendor slugs defined in kb_software.json or data/sw files
    vendor_slugs_in_sw = set()
    for item in sw_json_items:
        if "vendor_slug" in item:
            vendor_slugs_in_sw.add(item["vendor_slug"])
            
    for f in sw_data_files:
        try:
            with open(os.path.join("data/sw", f), "r", encoding="utf-8") as file:
                sw_detail = json.load(file)
                if "vendor_slug" in sw_detail:
                    vendor_slugs_in_sw.add(sw_detail["vendor_slug"])
                elif "vendor" in sw_detail and "slug" in sw_detail["vendor"]:
                    vendor_slugs_in_sw.add(sw_detail["vendor"]["slug"])
        except Exception:
            pass
            
    html_vendor_slugs = {f.replace(".html", "") for f in vendor_files}
    print(f"   - 软件数据中引用的厂商标识 (vendor_slug) 数量: {len(vendor_slugs_in_sw)}")
    print(f"   - 已生成 HTML 档案的厂商数量: {len(html_vendor_slugs)}")
    
    missing_vendors = vendor_slugs_in_sw - html_vendor_slugs
    # Note: 'community' might be community FOSS
    if missing_vendors:
        print(f"   - 缺少 HTML 档案的厂商: {sorted(list(missing_vendors))}")
    else:
        print(f"   - 所有引用的厂商均有对应的 HTML 档案！")

    # 4. Terms (术语)
    concept_files = []
    if os.path.exists("kb/concepts"):
        concept_files = [f for f in os.listdir("kb/concepts") if f.endswith(".html")]
    print(f"\n4. 术语/概念统计 (kb/concepts/ *.html): 共 {len(concept_files)} 个概念页面")
    
    # Read kb-terms.html and check how many distinct terms/concept links it lists
    terms_links = []
    if os.path.exists("kb-terms.html"):
        with open("kb-terms.html", "r", encoding="utf-8") as f:
            content = f.read()
            terms_links = re.findall(r'href=["\']\./kb/concepts/(.*?)["\']', content)
    print(f"   - kb-terms.html 中包含的独立术语链接数: {len(set(terms_links))}")
    print(f"   - kb-terms.html 中包含的总术语链接数: {len(terms_links)}")

    # 5. FAQs (常见问题)
    faq_entries = []
    if os.path.exists("kb-faq.html"):
        with open("kb-faq.html", "r", encoding="utf-8") as f:
            content = f.read()
            faq_entries = re.findall(r'<article[^>]*class="[^"]*kb-faq-entry[^"]*"[^>]*data-kb-faq-topic=["\'](.*?)["\']', content)
            
    print(f"\n5. 常见问题统计 (kb-faq.html): 共 {len(faq_entries)} 个 FAQ 条目")
    # Group by topic
    from collections import Counter
    c = Counter(faq_entries)
    print("   - 各主题 FAQ 分布:")
    for topic, count in c.most_common():
        print(f"     * {topic}: {count} 个")

    # 6. Knowledge Graph Nodes & Links (知识图谱节点及链接)
    graph_nodes = []
    graph_links = []
    if os.path.exists("knowledge.js"):
        with open("knowledge.js", "r", encoding="utf-8") as f:
            content = f.read()
            
        nodes_match = re.search(r'const nodes\s*=\s*\[(.*?)\];', content, re.DOTALL)
        if nodes_match:
            nodes_text = nodes_match.group(1)
            graph_nodes = re.findall(r'\{\s*id:\s*["\'](.*?)["\']', nodes_text)
            
        links_match = re.search(r'const links\s*=\s*\[(.*?)\]\s*;', content, re.DOTALL)
        if not links_match:
            # Fallback if there are spaces or newlines around the semicolon or it's just const links = [ ... ]
            links_match = re.search(r'const links\s*=\s*\[(.*?)\]\s*', content, re.DOTALL)
            
        if links_match:
            links_text = links_match.group(1)
            # Parse arrays like ["source", "target"] or ['source', 'target']
            graph_links = re.findall(r'\[\s*["\'](.*?)["\']\s*,\s*["\'](.*?)["\']\s*\]', links_text)
            
    print(f"\n6. 知识图谱统计 (knowledge.js):")
    print(f"   - 节点 (Nodes) 数量: {len(graph_nodes)} 个")
    print(f"   - 连线 (Links) 数量: {len(graph_links)} 条")

if __name__ == "__main__":
    main()
