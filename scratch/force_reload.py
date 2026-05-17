import os
import re

# New version string to bust cache
new_v = "v=preview_v2_1800"

files = ["index.html", "tutorials.html", "news.html", "about.html", "knowledge-base.html"]

for f in files:
    path = os.path.join(os.getcwd(), f)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Update ?v= query string
        updated_content = re.sub(r'\?v=[^"\']+', f'?{new_v}', content)
        
        with open(path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print(f"Updated {f}")
