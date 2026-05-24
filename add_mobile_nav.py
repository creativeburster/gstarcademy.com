#!/usr/bin/env python3
import os
import re

def update_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'class="hamburger"' in content:
        print(f"Skipping (already has hamburger): {file_path}")
        return False
    
    if '<header class="topbar">' not in content:
        print(f"Skipping (no topbar): {file_path}")
        return False
    
    if '</header>' not in content:
        print(f"Skipping (no closing header): {file_path}")
        return False
    
    old_pattern = r'(<header class="topbar">.*?<div class="[^"]*">)(.*?)(</header>)'
    match = re.search(old_pattern, content, re.DOTALL)
    
    if not match:
        print(f"Skipping (pattern not found): {file_path}")
        return False
    
    prefix = match.group(1)
    inner_content = match.group(2)
    suffix = match.group(3)
    
    brand_match = re.search(r'(<a class="brand"[^>]*>.*?</a>)', inner_content, re.DOTALL)
    if not brand_match:
        print(f"Skipping (no brand found): {file_path}")
        return False
    
    brand_html = brand_match.group(1)
    
    path_prefix = ''
    if '/kb/' in file_path:
        path_prefix = '../../'
    
    hamburger_html = f'''
          <button class="hamburger" aria-label="Toggle navigation menu" aria-expanded="false">
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
          </button>'''
    
    nav_html = f'''
          <nav class="nav">
            <div class="nav-header">
              <button class="nav-close" aria-label="Close navigation menu">
                <span class="nav-close-icon">×</span>
              </button>
            </div>
            <a class="nav-link" data-nav="home" href="{path_prefix}index.html">Home</a>
            <a class="nav-link" data-nav="knowledge" href="{path_prefix}knowledge-base.html">Wiki</a>
            <a class="nav-link" data-nav="tutorials" href="{path_prefix}tutorials.html">Tutorials</a>
            <a class="nav-link" data-nav="news" href="{path_prefix}news.html">News</a>
            <a class="nav-link" data-nav="about" href="{path_prefix}about.html">About</a>
          </nav>'''
    
    new_inner = inner_content + hamburger_html + nav_html
    
    new_content = content[:match.start()] + prefix + new_inner + suffix + content[match.end():]
    
    overlay_html = '''
      
        <div class="nav-overlay" aria-hidden="true"></div>'''
    
    header_end = new_content.find('</header>')
    if header_end != -1 and '<div class="nav-overlay"' not in new_content:
        new_content = new_content[:header_end] + overlay_html + new_content[header_end:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated: {file_path}")
    return True

def main():
    html_files = []
    for root, dirs, files in os.walk('/workspace'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    updated_count = 0
    for file_path in html_files:
        if update_html_file(file_path):
            updated_count += 1
    
    print(f"\nTotal files updated: {updated_count}")

if __name__ == '__main__':
    main()
