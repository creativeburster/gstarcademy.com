import os
import re

def update_html_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # 替换样式表
    content = re.sub(r'href=(["\'])(.*?/)?styles\.css(\?v=[a-zA-Z0-9_-]+)?\1', r'href=\1\2styles.min.css\1', content)
    
    # 替换 JS
    content = re.sub(r'src=(["\'])(.*?/)?app\.js(\?v=[a-zA-Z0-9_-]+)?\1', r'src=\1\2app.min.js\1', content)
    content = re.sub(r'src=(["\'])(.*?/)?search\.js(\?v=[a-zA-Z0-9_-]+)?\1', r'src=\1\2search.min.js\1', content)
    content = re.sub(r'src=(["\'])(.*?/)?knowledge\.js(\?v=[a-zA-Z0-9_-]+)?\1', r'src=\1\2knowledge.min.js\1', content)
    content = re.sub(r'src=(["\'])(.*?/)?quiz\.js(\?v=[a-zA-Z0-9_-]+)?\1', r'src=\1\2quiz.min.js\1', content)
    
    # 另外在 preload 里的 styles.css 也要替换
    content = re.sub(r'href=(["\'])(.*?/)?styles\.css(\?v=[a-zA-Z0-9_-]+)?\1', r'href=\1\2styles.min.css\1', content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    root_dir = 'f:/CAD-tutorial'
    updated_count = 0
    
    # 扫描根目录 HTML
    for file_name in os.listdir(root_dir):
        if file_name.endswith('.html'):
            file_path = os.path.join(root_dir, file_name)
            if update_html_content(file_path):
                updated_count += 1
                print(f"Updated: {file_name}")
                
    # 扫描 kb/concepts 目录 HTML
    concepts_dir = os.path.join(root_dir, 'kb/concepts')
    if os.path.exists(concepts_dir):
        for file_name in os.listdir(concepts_dir):
            if file_name.endswith('.html'):
                file_path = os.path.join(concepts_dir, file_name)
                if update_html_content(file_path):
                    updated_count += 1
                    
    print(f"Total HTML files updated: {updated_count}")

if __name__ == '__main__':
    main()
