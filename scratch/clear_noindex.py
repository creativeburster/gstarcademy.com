import os
import re

def clear_noindex(directory):
    # Regex to capture various styles of the noindex, nofollow tag
    robots_regex = re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\']noindex,\s*nofollow["\']\s*/?>', re.IGNORECASE)
    replacement = '<meta name="robots" content="index, follow, max-image-preview:large" />'
    
    count = 0
    for root, dirs, files in os.walk(directory):
        # Skip git or node_modules directories if present
        if '.git' in root or 'node_modules' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except UnicodeDecodeError:
                    # Fallback to latin-1 if utf-8 fails
                    with open(path, 'r', encoding='latin-1') as file:
                        content = file.read()
                
                new_content = robots_regex.sub(replacement, content)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8', newline='') as file:
                        file.write(new_content)
                    print(f"Restored indexable meta robots tag in: {os.path.relpath(path, directory)}")
                    count += 1
                    
    print(f"Total HTML files updated: {count}")

if __name__ == '__main__':
    clear_noindex('f:/CAD-tutorial')
