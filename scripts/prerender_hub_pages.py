#!/usr/bin/env python3
"""
Prerender Hub/Index pages (kb-faq.html, kb-terms.html, knowledge-library.html)
Injects rich static HTML directly into initial DOM so web crawlers and users
see full content immediately without waiting for client-side JavaScript execution.
"""

import os
import json
from bs4 import BeautifulSoup

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SITE_ROOT, "data")

def prerender_terms():
    terms_file = os.path.join(DATA_DIR, "terms_entries.json")
    index_file = os.path.join(DATA_DIR, "terms_index.json")
    html_file = os.path.join(SITE_ROOT, "kb-terms.html")

    if not os.path.exists(terms_file) or not os.path.exists(html_file):
        print("Missing terms data or kb-terms.html")
        return

    with open(terms_file, "r", encoding="utf-8") as f:
        terms_data = json.load(f)
    with open(index_file, "r", encoding="utf-8") as f:
        index_data = json.load(f)
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # 1. Prerender Highlighted Terms Grid
    grid = soup.find(id="kb-terms-cards-grid")
    if grid:
        grid.clear()
        for item in terms_data[:12]:
            card = soup.new_tag("div", attrs={"class": "kb-term-card", "style": "padding: 20px; background: var(--ink-surface); border: 1px solid var(--ink-line); border-radius: 12px;"})
            
            # Tag badge
            raw_tags = item.get("tags", "")
            if isinstance(raw_tags, list):
                raw_tags = " ".join(raw_tags)
            tag_tokens = [t.strip().upper() for t in str(raw_tags).split() if t.strip() and t.strip().lower() != "terms"]
            tag_label = " / ".join(tag_tokens[:2]) if tag_tokens else "CAD CONCEPT"
            tag_span = soup.new_tag("span", attrs={"class": "chip pill-warn", "style": "font-size: 11px; margin-bottom: 8px; display: inline-block;"})
            tag_span.string = tag_label
            card.append(tag_span)
            
            # Title
            title_text = item.get("title", "")
            t_h3 = soup.new_tag("h3", attrs={"style": "margin: 6px 0 8px; font-size: 1.05rem; font-weight: 700; color: var(--ink-text);"})
            t_h3.string = title_text
            card.append(t_h3)
            
            # Desc
            p_desc = soup.new_tag("p", attrs={"style": "font-size: 13.5px; line-height: 1.6; color: var(--ink-text-soft); margin: 0 0 12px;"})
            p_desc.string = item.get("desc", "")
            card.append(p_desc)
            
            # Link to concept
            concept_slug = item.get("slug") or re_slug(title_text)
            starter_slug_map = {
                "constraint": "constraints-autocad",
                "dwg-compatibility-mode": "dwg-file-format",
                "command-alias-pgp": "cui-autocad",
                "point-cloud-scan": "point-cloud-autocad",
            }
            if concept_slug in starter_slug_map:
                concept_slug = starter_slug_map[concept_slug]
            a_link = soup.new_tag("a", href=f"/kb/concepts/{concept_slug}", attrs={"style": "font-size: 13px; font-weight: 600; color: var(--accent); text-decoration: none;"})
            a_link.string = "Explore Concept & Graph Node →"
            card.append(a_link)
            
            grid.append(card)

    # 2. Prerender Alphabetical Index Container
    idx_container = soup.find(id="kb-terms-index-container")
    if idx_container:
        idx_container.clear()
        
        # Letter nav bar
        letter_nav = soup.new_tag("div", attrs={"style": "display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 24px; padding: 12px 16px; background: var(--ink-surface-2); border-radius: 10px;"})
        for letter in sorted(index_data.keys()):
            l_a = soup.new_tag("a", href=f"#{letter}", attrs={"style": "display: inline-block; width: 28px; height: 28px; line-height: 28px; text-align: center; font-weight: 700; font-size: 13px; color: var(--ink-text); text-decoration: none; border-radius: 6px; background: var(--ink-surface); border: 1px solid var(--ink-line);"})
            l_a.string = letter
            letter_nav.append(l_a)
        idx_container.append(letter_nav)

        # Alphabetical Groups
        for letter, terms_list in sorted(index_data.items()):
            group_div = soup.new_tag("div", id=letter, attrs={"style": "margin-bottom: 32px; padding: 20px; background: var(--ink-surface); border: 1px solid var(--ink-line); border-radius: 12px;"})
            
            g_h3 = soup.new_tag("h3", attrs={"style": "margin: 0 0 14px; font-size: 1.25rem; font-weight: 800; color: var(--accent); border-bottom: 2px solid var(--ink-line); padding-bottom: 6px;"})
            g_h3.string = f"Letter {letter}"
            group_div.append(g_h3)
            
            ul = soup.new_tag("ul", attrs={"style": "list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 10px;"})
            for term in terms_list:
                li = soup.new_tag("li")
                raw_href = term.get("href", "")
                if raw_href.startswith("./"):
                    href = "/" + raw_href[2:]
                elif not raw_href.startswith("/"):
                    href = "/" + raw_href
                else:
                    href = raw_href
                title = term.get("title", "").replace("&amp;", "&")
                meta = term.get("meta", "")
                
                t_link = soup.new_tag("a", href=href, attrs={"style": "color: var(--ink-text); text-decoration: none; font-size: 14px; font-weight: 500;"})
                strong = soup.new_tag("strong")
                strong.string = title
                t_link.append(strong)
                li.append(t_link)
                
                if meta:
                    meta_span = soup.new_tag("span", attrs={"class": "meta", "style": "font-size: 12px; color: var(--ink-text-soft); margin-left: 6px;"})
                    meta_span.string = meta
                    li.append(meta_span)
                
                ul.append(li)
            group_div.append(ul)
            idx_container.append(group_div)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("Prerendered kb-terms.html successfully!")


def prerender_faq():
    faq_file = os.path.join(DATA_DIR, "faq_entries.json")
    html_file = os.path.join(SITE_ROOT, "kb-faq.html")

    if not os.path.exists(faq_file) or not os.path.exists(html_file):
        print("Missing faq data or kb-faq.html")
        return

    with open(faq_file, "r", encoding="utf-8") as f:
        faq_data = json.load(f)
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    faq_list = soup.find(id="kb-faq-list")
    if faq_list:
        faq_list.clear()
        
        # Group by software
        sw_groups = {}
        for item in faq_data:
            sw = item.get("s", "general")
            if sw not in sw_groups:
                sw_groups[sw] = []
            sw_groups[sw].append(item)

        # Prerender top Q&As per software
        for sw, items in sorted(sw_groups.items()):
            sw_name = sw.replace("-", " ").title()
            sec_div = soup.new_tag("div", attrs={"class": "kb-faq-category-group", "style": "margin-bottom: 36px;"})
            
            cat_h2 = soup.new_tag("h2", attrs={"style": "margin: 0 0 16px; font-size: 1.3rem; font-weight: 700; color: var(--ink-text); border-bottom: 2px solid var(--accent); padding-bottom: 6px;"})
            cat_h2.string = f"{sw_name} Frequently Asked Questions"
            sec_div.append(cat_h2)
            
            for qa in items[:6]:
                q_card = soup.new_tag("details", attrs={"style": "margin-bottom: 14px; padding: 16px 20px; background: var(--ink-surface); border: 1px solid var(--ink-line); border-radius: 10px;"})
                
                summary = soup.new_tag("summary", attrs={"style": "font-size: 15px; font-weight: 700; color: var(--ink-text); cursor: pointer;"})
                summary.string = qa.get("q", "")
                q_card.append(summary)
                
                ans_div = soup.new_tag("div", attrs={"style": "margin-top: 12px; font-size: 14px; line-height: 1.7; color: var(--ink-text); border-top: 1px solid var(--ink-line); padding-top: 10px;"})
                ans_div.string = qa.get("a", "")
                q_card.append(ans_div)
                
                sec_div.append(q_card)
                
            faq_list.append(sec_div)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("Prerendered kb-faq.html successfully!")


def prerender_library():
    pdf_file = os.path.join(DATA_DIR, "pdf_extract_index.json")
    html_file = os.path.join(SITE_ROOT, "knowledge-library.html")

    if not os.path.exists(pdf_file) or not os.path.exists(html_file):
        print("Missing pdf data or knowledge-library.html")
        return

    with open(pdf_file, "r", encoding="utf-8") as f:
        pdf_data = json.load(f)
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    main_article = soup.find("article") or soup.find("main")
    if main_article:
        # Check if library grid exists or create
        lib_container = soup.find(id="pdf-library-cards") or soup.find(class_=re_compile(r"library-grid|cards-grid"))
        if not lib_container:
            lib_container = soup.new_tag("div", id="pdf-library-cards", attrs={"style": "display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 24px; margin-top: 32px;"})
            main_article.append(lib_container)
        else:
            lib_container.clear()

        for doc in pdf_data:
            card = soup.new_tag("div", attrs={"style": "padding: 24px; background: var(--ink-surface); border: 1px solid var(--ink-line); border-radius: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);"})
            
            title = doc.get("title_meta", doc.get("file", "Engineering Reference"))
            pages = doc.get("pages", "~200")
            size_mb = round(doc.get("file_size_bytes", 0) / (1024*1024), 1)
            
            c_h3 = soup.new_tag("h3", attrs={"style": "margin: 0 0 8px; font-size: 1.2rem; font-weight: 700; color: var(--ink-text);"})
            c_h3.string = f"📖 {title}"
            card.append(c_h3)
            
            meta_p = soup.new_tag("p", attrs={"style": "font-size: 12.5px; color: var(--ink-text-soft); margin: 0 0 14px;"})
            meta_p.string = f"File: {doc.get('file')} · {pages} Pages · {size_mb} MB"
            card.append(meta_p)
            
            hints = doc.get("chapter_hints", [])
            if hints:
                h_p = soup.new_tag("p", attrs={"style": "font-size: 13px; font-weight: 700; margin: 0 0 6px; color: var(--ink-text);"})
                h_p.string = "Key Topics & Chapters Covered:"
                card.append(h_p)
                
                ul = soup.new_tag("ul", attrs={"style": "padding-left: 18px; margin: 0 0 16px; font-size: 13px; color: var(--ink-text); line-height: 1.6;"})
                for hint in hints[:4]:
                    li = soup.new_tag("li")
                    li.string = hint
                    ul.append(li)
                card.append(ul)

            summary_text = doc.get("text_sample", "")[:280] + "..." if doc.get("text_sample") else "Comprehensive reference guide covering CAD operations, 3D modeling workspaces, command syntax, and production drawing standards."
            sum_p = soup.new_tag("p", attrs={"style": "font-size: 13.5px; line-height: 1.65; color: var(--ink-text-soft); margin: 0;"})
            sum_p.string = summary_text
            card.append(sum_p)
            
            lib_container.append(card)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("Prerendered knowledge-library.html successfully!")


def re_slug(text):
    import re
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    return s

def re_compile(pattern):
    import re
    return re.compile(pattern, re.I)

def main():
    prerender_terms()
    prerender_faq()
    prerender_library()

if __name__ == "__main__":
    main()
