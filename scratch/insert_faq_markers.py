import re

def main():
    path = "kb-faq.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Insert sw-faq-tabs markers if not present
    tab_marker_start = "<!-- AUTO-GEN sw-faq-tabs START -->"
    if tab_marker_start not in content:
        needle = '<button type="button" class="kb-faq-tab" role="tab" aria-selected="false" data-kb-faq-filter="catia">CATIA</button>'
        replacement = needle + "\n                <!-- AUTO-GEN sw-faq-tabs START -->\n                <!-- AUTO-GEN sw-faq-tabs END -->"
        content = content.replace(needle, replacement)
        print("Injected sw-faq-tabs markers.")
    else:
        print("sw-faq-tabs markers already present.")
        
    # 2. Insert sw-faqs markers if not present
    faq_marker_start = "<!-- AUTO-GEN sw-faqs START -->"
    if faq_marker_start not in content:
        needle = '<div class="kb-faq-pagination"></div>'
        replacement = "<!-- AUTO-GEN sw-faqs START -->\n                <!-- AUTO-GEN sw-faqs END -->\n\n                " + needle
        # Replace the first occurrence of pagination div in the main list
        content = content.replace(needle, replacement, 1)
        print("Injected sw-faqs markers.")
    else:
        print("sw-faqs markers already present.")
        
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
        
if __name__ == "__main__":
    main()
