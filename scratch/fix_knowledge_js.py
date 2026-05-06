import os
import re

path = r'f:\CAD-tutorial\knowledge.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the missing variable name
content = content.replace('    const d3 = window.d3;\n      concept:', '    const d3 = window.d3;\n    const typeLabelZh = {\n      concept:')

# Remove descZh properties
content = re.sub(r'descZh: ".*?", ', '', content)
content = re.sub(r'descZh: "", ', '', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
