import os
import re

directory = r'f:\CAD-tutorial'
css_pattern = re.compile(r'styles\.css\?v=[a-zA-Z0-9_-]+')
js_pattern = re.compile(r'knowledge\.js\?v=[a-zA-Z0-9_-]+')

css_replacement = 'styles.css?v=v6_faq_graph_perfection'
js_replacement = 'knowledge.js?v=v6_faq_graph_perfection'

updated_count = 0

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = css_pattern.sub(css_replacement, content)
                new_content = js_pattern.sub(js_replacement, new_content)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {path}")
                    updated_count += 1
            except Exception as e:
                print(f"Error processing {path}: {e}")

print(f"Total HTML files updated: {updated_count}")
