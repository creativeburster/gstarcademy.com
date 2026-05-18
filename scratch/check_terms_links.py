import os
import re

root_dir = r'f:\CAD-tutorial'
terms_path = os.path.join(root_dir, 'kb-terms.html')

with open(terms_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all hrefs matching ./kb/concepts/something.html or ./kb/software/something.html
links = re.findall(r'href="(\./kb/[^"]+\.html)"', content)

missing_links = []
valid_count = 0

for link in links:
    # Resolve file path
    rel_path = link.replace('/', os.sep)
    if rel_path.startswith('.' + os.sep):
        rel_path = rel_path[2:]
    
    full_path = os.path.join(root_dir, rel_path)
    if not os.path.isfile(full_path):
        missing_links.append((link, full_path))
    else:
        valid_count += 1

print(f"Total links checked: {len(links)}")
print(f"Valid links: {valid_count}")
print(f"Missing (404) links: {len(missing_links)}")
for link, path in sorted(list(set(missing_links))):
    print(f"  - {link} (resolves to: {path})")
