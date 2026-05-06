import os
import re

def set_noindex_nofollow(directory):
    pattern = re.compile(r'<meta name="robots" content="[^"]+" />', re.IGNORECASE)
    replacement = '<meta name="robots" content="noindex, nofollow" />'

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = pattern.sub(replacement, content)
                
                # If no meta robots found, add it after the title or description
                if new_content == content and '<meta name="robots"' not in content.lower():
                    # Find <head> and insert after it
                    new_content = content.replace('<head>', '<head>\n    <meta name="robots" content="noindex, nofollow" />')

                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {file_path}")

if __name__ == "__main__":
    set_noindex_nofollow('f:/CAD-tutorial')
