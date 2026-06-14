import json
import pathlib

def main():
    path = pathlib.Path("f:/CAD-tutorial/vercel.json")
    if not path.exists():
        print("Error: vercel.json not found!")
        return 1
    
    # 读取原始文本并替换 `/knowledge-glossary.html` 为 `/kb-terms.html`
    text = path.read_text(encoding="utf-8")
    
    # 计数替换次数
    count = text.count("/knowledge-glossary.html")
    print(f"Found {count} occurrences of '/knowledge-glossary.html'")
    
    new_text = text.replace("/knowledge-glossary.html", "/kb-terms.html")
    
    # 解析 JSON
    try:
        data = json.loads(new_text)
    except Exception as e:
        print(f"JSON parsing error after replace: {e}")
        return 1
        
    # 添加 cleanUrls = True
    data["cleanUrls"] = True
    
    # 写回文件，使用漂亮的缩进
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Successfully updated vercel.json with cleanUrls and replaced redirect targets.")
    return 0

if __name__ == "__main__":
    exit(main())
