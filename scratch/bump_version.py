import os

def main():
    root_dir = r"f:\CAD-tutorial"
    target = "styles.css?v=v3_theme_separation"
    replacement = "styles.css?v=v4_sidebar_dark_fix"
    
    count = 0
    for root, dirs, files in os.walk(root_dir):
        # Exclude git directory
        if ".git" in dirs:
            dirs.remove(".git")
            
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    if target in content:
                        new_content = content.replace(target, replacement)
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        count += 1
                        print(f"Updated: {os.path.relpath(file_path, root_dir)}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
    print(f"\nTotal files updated: {count}")

if __name__ == "__main__":
    main()
