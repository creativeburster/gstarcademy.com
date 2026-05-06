import os
import re

directory = r'f:\CAD-tutorial'
target_pattern = re.compile(r'knowledge\.js\?v=[a-zA-Z0-9_-]+')
replacement = 'knowledge.js?v=20260506_gstarcad'

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = target_pattern.sub(replacement, content)
            
            if new_content != content:
                print(f"Updating {path}")
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
