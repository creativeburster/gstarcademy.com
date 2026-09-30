import json
import re

def main():
    json_path = "f:/gstarcademy/data/tutorials_gstarcad.json"
    html_path = "f:/gstarcademy/tutorials.html"

    with open(json_path, "r", encoding="utf-8") as f:
        tutorials = json.load(f)

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    articles = []
    
    # Header panel for official section
    official_header = """            <!-- Official GstarCAD Curriculum Hub Header -->
            <div class="panel" style="background: linear-gradient(135deg, rgba(37,99,235,0.08) 0%, rgba(99,102,241,0.06) 100%); border-color: rgba(37,99,235,0.3); box-shadow: 0 4px 20px rgba(37,99,235,0.06); margin-bottom: 24px;">
              <div class="section-head" style="margin-bottom: 0">
                <h2 class="panel-title" style="margin: 0; color: var(--accent,#2563eb); display: flex; align-items: center; gap: 8px;">
                  <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#2563eb;"></span>
                  ★ Official GstarCAD &amp; DWG FastView Academy Curriculum
                </h2>
                <div class="chips" style="margin-top: 0">
                  <span class="chip pill-ok" style="background:#2563eb; color:#fff; font-weight:700;">31 Official Courses</span>
                  <span class="chip" style="background:rgba(99,102,241,0.15); color:#6366f1; font-weight:600;">Full Ecosystem</span>
                  <span class="chip" style="font-weight:600;">Free Access 🎁</span>
                </div>
              </div>
              <p class="meta" style="margin-top: 10px; font-size: 14px; line-height: 1.6; color: var(--text, #333);">
                Official knowledge curriculum authored by <strong>Suzhou Gstarsoft Co., Ltd. (SSE: 688657)</strong> technical architects. Master GstarCAD 2027 multi-core drafting, DWG FastView mobile precision measuring, real-world video annotations, CAD table to Excel extraction, missing font fix, 14+ 3D format viewing, mechanical BOM generation, and GRX/Web SDK development.
              </p>
            </div>
"""
    articles.append(official_header)

    for i, tut in enumerate(tutorials):
        tut_id = tut.get("id", "")
        software = tut.get("software", "gstarcad")
        product = tut.get("product", "GstarCAD 2027 Pro")
        task = tut.get("task", "2d-drafting")
        level = tut.get("level", "beginner")
        title = tut.get("title", "")
        meta_info = tut.get("meta_info", "")
        editorial_note = tut.get("editorial_note", "")
        tags = tut.get("tags", [])
        url = tut.get("url", "")
        thumb = tut.get("thumbnail_url", "./images/tutorials/gstarcad_academy.webp")
        rating = tut.get("rating", 4.95)
        duration_min = tut.get("duration_minutes", 30)
        duration_sec = duration_min * 60
        pub_day = f"{max(1, 31 - i):02d}"
        published = f"2026-03-{pub_day}"

        # Software tokens for filter
        software_tokens = [software, "gstarcad"]
        if "fastview" in software or "fv" in tut_id:
            software_tokens = ["fastview", "gstarcad"]
        elif "mechanical" in software or "mech" in tut_id:
            software_tokens = ["mechanical", "gstarcad"]
        elif "architecture" in software or "arch" in tut_id:
            software_tokens = ["architecture", "gstarcad"]
        elif "migration" in software or "migration" in task or tut_id == "gcad-core-106":
            software_tokens = ["migration", "gstarcad"]
        elif "developers" in software or "dev" in tut_id:
            software_tokens = ["developers", "gstarcad"]

        # Task tokens
        task_tokens = [task]
        if "2d-drafting" in task:
            task_tokens.extend(["drafting", "fundamentals"])
        if "mobile-cloud" in task or "fv" in tut_id:
            task_tokens.extend(["mobile-cloud", "mobile", "cloud", "field"])
        if "mechanical" in task or "mech" in tut_id:
            task_tokens.extend(["mechanical-design", "mechanical", "assemblies"])
        if "architectural" in task or "arch" in tut_id:
            task_tokens.extend(["architectural-design", "architectural", "bim"])
        if "migration" in task or tut_id == "gcad-core-106":
            task_tokens.extend(["migration", "autocad"])
        if "productivity" in task or "Table" in title or "Font" in title or "Hatch" in title:
            task_tokens.extend(["productivity", "tools"])
        if "3d-modeling" in task or "3D" in title:
            task_tokens.extend(["3d-modeling", "3d", "modeling"])
        if "customization-api" in task or "SDK" in title or "LISP" in title:
            task_tokens.extend(["customization-api", "api", "lisp", "grx", "sdk"])
        if "rendering" in task or "Render" in title:
            task_tokens.extend(["rendering", "viz"])

        software_str = " ".join(dict.fromkeys(software_tokens))
        task_str = " ".join(dict.fromkeys(task_tokens))

        # Actions and button destinations
        if "fastview" in software or "fv" in tut_id:
            if "measure" in title.lower() or "radius" in title.lower() or "slope" in title.lower():
                primary_href = "/tutorial-fastview#measure"
                primary_label = "Open Measuring Guide →"
            elif "video" in title.lower() or "markup" in title.lower() or "annotation" in title.lower():
                primary_href = "/tutorial-fastview#markups"
                primary_label = "Open Markup Guide →"
            elif "cloud" in title.lower() or "qr" in title.lower() or "web" in title.lower():
                primary_href = "/tutorial-fastview#cloud"
                primary_label = "Open Cloud Guide →"
            else:
                primary_href = "/tutorial-fastview"
                primary_label = "Read FastView Guide →"
            primary_target = ""
            sec_href = "https://en.dwgfastview.com/"
            sec_label = "Get DWG FastView ↗"
            sec_target = ' target="_blank" rel="noopener"'
            badge_color = "#6366f1"
        elif "mechanical" in software or "mech" in tut_id:
            primary_href = "https://www.gstarcad.net/mechanical/"
            primary_label = "Mechanical Guide ↗"
            primary_target = ' target="_blank" rel="noopener"'
            sec_href = "/download"
            sec_label = "Download Mechanical Trial"
            sec_target = ""
            badge_color = "#10b981"
        elif "architecture" in software or "arch" in tut_id:
            primary_href = "https://www.gstarcad.net/architecture/"
            primary_label = "Architecture Guide ↗"
            primary_target = ' target="_blank" rel="noopener"'
            sec_href = "/download"
            sec_label = "Download Architecture Trial"
            sec_target = ""
            badge_color = "#f59e0b"
        elif "developers" in software or "dev" in tut_id:
            if "sdk" in tut_id or "Web SDK" in title or "Mobile SDK" in title:
                primary_href = url if url else "/developers"
                primary_label = "Open SDK Guide ↗"
                primary_target = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
            else:
                primary_href = "/developers"
                primary_label = "Developer Hub →"
                primary_target = ""
            sec_href = "/download"
            sec_label = "Download SDK & Pro"
            sec_target = ""
            badge_color = "#8b5cf6"
        elif tut_id == "gcad-core-106" or "migration" in software:
            primary_href = "/migration"
            primary_label = "AutoCAD Migration Hub →"
            primary_target = ""
            sec_href = "/download"
            sec_label = "Test DWG Compatibility"
            sec_target = ""
            badge_color = "#ec4899"
        elif "render" in tut_id or "ai" in tut_id or "GstarRender" in title:
            primary_href = "https://enweb.gstarcad.net/ai/render/?clientType=Gs_PC&fromEvent=nav"
            primary_label = "Launch GstarRender AI ↗"
            primary_target = ' target="_blank" rel="noopener"'
            sec_href = "/download"
            sec_label = "Download GstarCAD Pro"
            sec_target = ""
            badge_color = "#0ea5e9"
        elif "365" in title:
            primary_href = "https://enweb.gstarcad.net/gstarcad365/"
            primary_label = "Explore GstarCAD 365 ↗"
            primary_target = ' target="_blank" rel="noopener"'
            sec_href = "/download"
            sec_label = "Start Free Trial"
            sec_target = ""
            badge_color = "#2563eb"
        else:
            primary_href = "https://www.gstarcad.net/video/"
            primary_label = "Watch Official Video ↗"
            primary_target = ' target="_blank" rel="noopener"'
            sec_href = "/download"
            sec_label = "Download 30-Day Trial"
            sec_target = ""
            badge_color = "#2563eb"

        tags_html = "".join([f'<span class="tag">{t}</span>' for t in tags])

        card_html = f"""            <article class="tutorial-item tutorial-item--official" data-software="{software_str}" data-task="{task_str}" data-level="{level}" data-price="free" data-duration="{duration_sec}" data-rating="{rating}" data-published="{published}">
              <div class="thumb thumb--cover" style="background-image: url('{thumb}')" role="img" aria-label="{title}"></div>
              <div class="item-body">
                <h3>{title} <span class="badge" style="background:{badge_color}; color:#fff; font-weight:700;">★ Official Course</span></h3>
                <p class="meta"><strong>Product:</strong> {product} · <strong>Author:</strong> Suzhou Gstarsoft Official · <strong>Duration:</strong> {duration_min}m · <strong>Rating:</strong> ★ {rating}</p>
                <p class="meta" style="color:var(--text, #333);">{editorial_note}</p>
                <div class="item-tags">
                  <span class="tag" style="background:rgba(37,99,235,0.12); color:#1d4ed8; font-weight:700;">Official Academy</span>
                  {tags_html}
                </div>
                <div class="actions">
                  <a class="btn btn-primary" href="{primary_href}"{primary_target}>{primary_label}</a>
                  <a class="btn" href="{sec_href}"{sec_target}>{sec_label}</a>
                </div>
              </div>
            </article>"""
        articles.append(card_html)

    inserted_block = "\n".join(articles) + "\n\n            <!-- Standard Community & Video Index -->\n            "

    marker = '<!-- youtube-build:begin -->'
    if marker not in html_content:
        print(f"Error: {marker} not found in HTML!")
        return

    # Find from marker to the first non-official tutorial-item or community item
    pattern = re.compile(r'<!-- youtube-build:begin -->\s*.*?<!-- Standard Community & Video Index -->\s*', re.DOTALL)
    m = pattern.search(html_content)
    if not m:
        # Fallback to older pattern
        pattern = re.compile(r'<!-- youtube-build:begin -->\s*<div class="panel">.*?</div>\s*(?=<article class="tutorial-item)', re.DOTALL)
        m = pattern.search(html_content)
        if not m:
            print("Could not match the replacement boundary!")
            return

    new_html = html_content[:m.start()] + marker + "\n" + inserted_block + html_content[m.end():]

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"Successfully injected {len(tutorials)} official GstarCAD tutorials into tutorials.html!")

if __name__ == "__main__":
    main()
