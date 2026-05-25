#!/usr/bin/env python3
import os

def add_hamburger_to_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check if already has hamburger menu
        if 'hamburger' in content:
            print(f"Skipping (already updated): {file_path}")
            return False
        
        # Find and replace the navigation section
        old_nav_start = '<header class="topbar">'
        old_nav_end = '</header>'
        
        if old_nav_start not in content:
            print(f"Warning: No topbar found in {file_path}")
            return False
        
        # Find the position of the closing nav tag
        nav_tag_end = content.find('</nav>')
        if nav_tag_end == -1:
            print(f"Warning: No nav tag found in {file_path}")
            return False
        
        # Insert hamburger menu after the brand link
        brand_end = content.find('</a>', nav_tag_end - 200)
        if brand_end == -1:
            print(f"Warning: No brand link found in {file_path}")
            return False
        
        # Define the hamburger menu HTML
        hamburger_html = '''
          <button class="hamburger" aria-label="Toggle navigation menu" aria-expanded="false">
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
          </button>
'''
        
        # Insert hamburger button after the brand link
        content = content[:brand_end + 4] + hamburger_html + content[brand_end + 4:]
        
        # Add nav overlay before the closing header tag
        header_end = content.find('</header>')
        if header_end != -1:
            overlay_html = '''
        <div class="nav-overlay" aria-hidden="true"></div>'''
            content = content[:header_end] + overlay_html + content[header_end:]
        
        # Write the modified content back
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"Updated: {file_path}")
        return True
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
    
    updated_count = 0
    for file_path in html_files:
        if add_hamburger_to_html(file_path):
            updated_count += 1
    
    print(f"\nTotal files updated with hamburger menu: {updated_count}")

if __name__ == "__main__":
    main()
