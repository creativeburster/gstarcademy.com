import os
import re

root_dir = r'f:\CAD-tutorial'
terms_path = os.path.join(root_dir, 'kb-terms.html')

with open(terms_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match links starting with ./kb/concepts/ that do not have .html extension
# Specifically match things that only contain word chars and dashes after the slash
pattern = r'href="\./kb/concepts/([a-zA-Z0-9\-]+)"'

matches = re.findall(pattern, content)
print(f"Found {len(matches)} links lacking extensions:")
for m in matches:
    print(f"  - {m}")

# Replace all matching occurrences
fixed_content, count = re.subn(pattern, r'href="./kb/concepts/\1.html"', content)
print(f"Replaced {count} occurrences.")

if count > 0:
    with open(terms_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    print("kb-terms.html successfully updated!")
else:
    print("No changes made.")
