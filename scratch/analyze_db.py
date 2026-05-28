import re

def analyze_detailed_terms(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'<article\s+[^>]*class="[^"]*kb-detail-card[^"]*"\s+[^>]*data-tags="([^"]*)"[^>]*>'
    matches = re.findall(pattern, content, re.IGNORECASE)
    
    detailed_counts = {}
    
    for tags_str in matches:
        tags = tags_str.lower().split()
        for tag in tags:
            # We don't care about generic tags like 'terms', 'beginner', 'intermediate', 'advanced', '2d', '3d', 'aec', 'mfg', 'collaboration', 'standards', 'developer'
            if tag not in ['terms', 'beginner', 'intermediate', 'advanced', '2d', '3d', 'aec', 'mfg', 'collaboration', 'standards', 'developer', 'general']:
                detailed_counts[tag] = detailed_counts.get(tag, 0) + 1
                
    # Group detailed tags under parent vendors
    groups = {
        'Autodesk': {},
        'Gstarsoft': {},
        'Dassault Systèmes': {},
        'PTC': {},
        'Siemens': {},
        'Bentley': {},
        'DraftSight': {}
    }
    
    for tag, val in detailed_counts.items():
        if tag in ['autodesk', 'autocad', 'revit', 'inventor', 'civil3d', 'fusion']:
            groups['Autodesk'][tag] = val
        elif tag in ['gstarcad', 'gstarsoft', 'fastview', 'fastview-3d', 'dwg-fastview', 'dwg-fastview-plus', 'gstarbim', 'houseplan']:
            groups['Gstarsoft'][tag] = val
        elif tag in ['dassault', 'solidworks', 'catia', 'dassault-systemes']:
            groups['Dassault Systèmes'][tag] = val
        elif tag in ['ptc', 'creo', 'creo-parametric', 'onshape']:
            groups['PTC'][tag] = val
        elif tag in ['siemens', 'siemens-nx', 'nx']:
            groups['Siemens'][tag] = val
        elif tag in ['bentley']:
            groups['Bentley'][tag] = val
        elif tag in ['draftsight']:
            groups['DraftSight'][tag] = val
        else:
            # print(f"Other tag: {tag} ({val})")
            pass
            
    print("DETAILED GROUPS:")
    for group, subtags in groups.items():
        print(f"{group}: {subtags}")

if __name__ == '__main__':
    analyze_detailed_terms('kb-terms.html')
