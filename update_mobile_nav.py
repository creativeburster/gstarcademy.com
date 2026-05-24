#!/usr/bin/env python3
import os
import re

def update_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'class="hamburger"' not in content:
        print(f"Skipping (no hamburger): {file_path}")
        return False
    
    if '<nav class="nav">' not in content:
        print(f"Skipping (no nav): {file_path}")
        return False
    
    if 'class="nav-header"' in content:
        print(f"Skipping (already has nav-header): {file_path}")
        return False
    
    path_prefix = ''
    if '/kb/' in file_path:
        path_prefix = '../../'
    
    old_nav = '''<nav class="nav">
            <a class="nav-link" data-nav="home" href="./index.html">Home</a>
            <a class="nav-link" data-nav="knowledge" href="./knowledge-base.html">Wiki</a>
            <a class="nav-link" data-nav="tutorials" href="./tutorials.html">Tutorials</a>
            <a class="nav-link" data-nav="news" href="./news.html">News</a>
            <a class="nav-link" data-nav="about" href="./about.html">About</a>
          </nav>'''
    
    new_nav = f'''<nav class="nav">
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
    
    if old_nav in content:
        new_content = content.replace(old_nav, new_nav)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {file_path}")
        return True
    
    old_nav_alternative = '''<nav class="nav">
            <a class="nav-link" data-nav="home" href="../../index.html">Home</a>
            <a class="nav-link" data-nav="knowledge" href="../../knowledge-base.html">Wiki</a>
            <a class="nav-link" data-nav="tutorials" href="../../tutorials.html">Tutorials</a>
            <a class="nav-link" data-nav="news" href="../../news.html">News</a>
            <a class="nav-link" data-nav="about" href="../../about.html">About</a>
          </nav>'''
    
    if old_nav_alternative in content:
        new_content = content.replace(old_nav_alternative, new_nav)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {file_path}")
        return True
    
    print(f"Skipping (nav pattern not matched): {file_path}")
    return False

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
