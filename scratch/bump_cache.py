import os
import glob
import re

html_files = glob.glob('*.html') + glob.glob('kb/concepts/*.html') + glob.glob('kb/software/*.html')
old_version = 'v=v6_faq_graph_perfection'
new_version = 'v=v7_graph_fix'

count = 0
for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_version in content:
            content = content.replace(old_version, new_version)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"Bumped cache version in {count} HTML files.")
