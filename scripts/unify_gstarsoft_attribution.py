import glob
import re

patterns = ["*.html", "kb/**/*.html"]
updated_count = 0

for pattern in patterns:
    for fn in glob.glob(pattern, recursive=True):
        with open(fn, "r", encoding="utf-8") as f:
            orig = f.read()
        html = orig

        # 1. Update meta publisher
        if 'name="publisher"' in html:
            html = re.sub(
                r'<meta\s+name=["\']publisher["\']\s+content=["\'][^"\']*["\']\s*/?>',
                '<meta name="publisher" content="Suzhou Gstarsoft Co., Ltd. (SSE: 688657)" />',
                html
            )

        # 2. Update author if Gstarcademy or Gstarsoft
        html = re.sub(
            r'<meta\s+name=["\']author["\']\s+content=["\'](?:Gstarcademy|Gstarsoft(?:\s+Co\.,\s+Ltd\.)?)["\']\s*/?>',
            '<meta name="author" content="Suzhou Gstarsoft Co., Ltd. (SSE: 688657)" />',
            html
        )

        # 3. Update footer copyright
        html = re.sub(
            r'©\s*(?:<span[^>]*>(?:2026)?</span>|2026)?\s*(?:Gstarcademy|Gstarsoft\s+Co\.,\s+Ltd\.)\.?\s*All rights reserved\.',
            '© <span id="year">2026</span> Suzhou Gstarsoft Co., Ltd. (SSE: 688657). All rights reserved.',
            html
        )
        html = html.replace(
            '<p>© <span id="footer-year"></span> Gstarcademy. All rights reserved.</p>',
            '<p>© <span id="footer-year">2026</span> Suzhou Gstarsoft Co., Ltd. (SSE: 688657). All rights reserved.</p>'
        )

        # 4. JSON-LD publisher name
        html = re.sub(
            r'"publisher":\s*\{\s*"@type":\s*"Organization",\s*"name":\s*"(?:Gstarcademy|Gstarsoft\s+Co\.,\s+Ltd\.)"',
            '"publisher": {"@type": "Organization", "name": "Suzhou Gstarsoft Co., Ltd. (SSE: 688657)"',
            html
        )

        if html != orig:
            with open(fn, "w", encoding="utf-8") as f:
                f.write(html)
            updated_count += 1

# Also update generator scripts so future regenerations keep official attribution
scripts_to_update = [
    "scripts/build_software_content.py",
    "scripts/render_kb_software_pages.py",
    "scripts/split_knowledge_pages.py"
]
for sfn in scripts_to_update:
    try:
        with open(sfn, "r", encoding="utf-8") as f:
            s_content = f.read()
        s_content = s_content.replace(
            '<p>© <span id="footer-year"></span> Gstarcademy. All rights reserved.</p>',
            '<p>© <span id="footer-year">2026</span> Suzhou Gstarsoft Co., Ltd. (SSE: 688657). All rights reserved.</p>'
        )
        s_content = s_content.replace(
            'Gstarsoft Co., Ltd.',
            'Suzhou Gstarsoft Co., Ltd. (SSE: 688657)'
        )
        with open(sfn, "w", encoding="utf-8") as f:
            f.write(s_content)
        print(f"Updated script: {sfn}")
    except Exception as e:
        print(f"Error updating {sfn}: {e}")

print(f"Total HTML files updated for official attribution: {updated_count}")
