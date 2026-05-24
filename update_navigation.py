#!/usr/bin/env python3
import os
import glob

def replace_text_in_file(file_path, search_text, replace_text):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if search_text in content:
            content = content.replace(search_text, replace_text)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    # Get all HTML files
    html_files = []
    for root, dirs, files in os.walk('/workspace'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    search_text = 'Knowledge Base'
    replace_text = 'Wiki'
    
    updated_count = 0
    for file_path in html_files:
        if replace_text_in_file(file_path, search_text, replace_text):
            updated_count += 1
    
    print(f"\nTotal files updated: {updated_count}")

if __name__ == "__main__":
    main()
