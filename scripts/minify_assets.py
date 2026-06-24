import re
import os

def minify_css(css_content):
    # 移除注释
    css = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # 移除换行和多余空格
    css = re.sub(r'\s+', ' ', css)
    # 移除大括号、冒号、分号、逗号周围的空格
    css = re.sub(r'\s*([\{\}:;\,])\s*', r'\1', css)
    # 移除最后一个分号
    css = re.sub(r';\}', '}', css)
    return css.strip()

def minify_js(js_content):
    # 用一个状态机安全地移除注释而不会误伤字符串内的 // 或 /*
    result = []
    i = 0
    length = len(js_content)
    
    in_string = False
    string_char = None
    in_single_comment = False
    in_multi_comment = False
    
    while i < length:
        char = js_content[i]
        next_char = js_content[i+1] if i + 1 < length else ''
        
        # 处理单行注释结束
        if in_single_comment:
            if char == '\n' or char == '\r':
                in_single_comment = False
                result.append(char)
            i += 1
            continue
            
        # 处理多行注释结束
        if in_multi_comment:
            if char == '*' and next_char == '/':
                in_multi_comment = False
                i += 2
            else:
                i += 1
            continue
            
        # 处理字符串内部
        if in_string:
            if char == '\\':
                result.append(char)
                if i + 1 < length:
                    result.append(js_content[i+1])
                    i += 2
                else:
                    i += 1
                continue
            if char == string_char:
                in_string = False
            result.append(char)
            i += 1
            continue
            
        # 检测字符串开始
        if char in ("'", '"', '`'):
            in_string = True
            string_char = char
            result.append(char)
            i += 1
            continue
            
        # 检测注释开始
        if char == '/' and next_char == '/':
            in_single_comment = True
            i += 2
            continue
        elif char == '/' and next_char == '*':
            in_multi_comment = True
            i += 2
            continue
            
        result.append(char)
        i += 1
        
    js = "".join(result)
    
    # 压缩多余的空白字符，同时保留换行以避免缺少分号自动插入(ASI)的问题
    lines = js.splitlines()
    minified_lines = []
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        # 将多个连续空格替换成单个空格
        line_clean = re.sub(r'[ \t]+', ' ', line_clean)
        # 移除符号两边的空格
        line_clean = re.sub(r'\s*([\{\}\(\)=\+\-\*\/%&\|\!\?<>;:\,])\s*', r'\1', line_clean)
        minified_lines.append(line_clean)
        
    # 合并为一行
    return "\n".join(minified_lines)

def process_file(src_path, dest_path, file_type):
    print(f"Compressing {src_path} -> {dest_path}...")
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if file_type == 'css':
        minified = minify_css(content)
    elif file_type == 'js':
        minified = minify_js(content)
    else:
        minified = content
        
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(minified)
        
    orig_size = os.path.getsize(src_path)
    mini_size = os.path.getsize(dest_path)
    reduction = (orig_size - mini_size) / orig_size * 100
    print(f"Size: {orig_size} B -> {mini_size} B ({reduction:.1f}% reduction)")

if __name__ == '__main__':
    base_dir = 'f:/CAD-tutorial'
    
    # 1. 压缩 styles.css
    process_file(f"{base_dir}/styles.css", f"{base_dir}/styles.min.css", 'css')
    
    # 2. 压缩 app.js
    process_file(f"{base_dir}/app.js", f"{base_dir}/app.min.js", 'js')
    
    # 3. 压缩 search.js
    process_file(f"{base_dir}/search.js", f"{base_dir}/search.min.js", 'js')
    
    # 4. 压缩 knowledge.js
    process_file(f"{base_dir}/knowledge.js", f"{base_dir}/knowledge.min.js", 'js')
    
    # 5. 压缩 quiz.js
    process_file(f"{base_dir}/quiz.js", f"{base_dir}/quiz.min.js", 'js')
