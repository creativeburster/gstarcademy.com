#!/usr/bin/env python3
import os
import re

def update_kb_concept_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'class="nav-header"' in content:
        print(f"Skipping (already has nav-header): {file_path}")
        return False
    
    path_prefix = '../../'
    
    old_nav_pattern = r'<nav class="nav">(.*?)</nav>'
    match = re.search(old_nav_pattern, content, re.DOTALL)
    
    if not match:
        print(f"Skipping (no nav found): {file_path}")
        return False
    
    nav_content = match.group(1)
    
    hamburger_pattern = r'\s*<button class="hamburger".*?</button>\s*'
    nav_content = re.sub(hamburger_pattern, '\n', nav_content, flags=re.DOTALL)
    
    new_nav = f'''<nav class="nav">
          <div class="nav-header">
            <button class="nav-close" aria-label="Close navigation menu">
              <span class="nav-close-icon">×</span>
            </button>
          </div>
          <a class="nav-link" href="{path_prefix}index.html">Home</a>
          <a class="nav-link" href="{path_prefix}knowledge-base.html">Wiki</a>
          <a class="nav-link" href="{path_prefix}tutorials.html">Tutorials</a>
          <a class="nav-link" href="{path_prefix}news.html">News</a>
        </nav>'''
    
    new_content = content[:match.start()] + new_nav + content[match.end():]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated: {file_path}")
    return True

def main():
    kb_files = []
    kb_dir = '/workspace/kb/concepts'
    
    if os.path.exists(kb_dir):
        for file in os.listdir(kb_dir):
            if file.endswith('.html'):
                kb_files.append(os.path.join(kb_dir, file))
    
    updated_count = 0
    for file_path in kb_files:
        if update_kb_concept_file(file_path):
            updated_count += 1
    
    print(f"\nTotal kb/concept files updated: {updated_count}")

if __name__ == '__main__':
    main()
