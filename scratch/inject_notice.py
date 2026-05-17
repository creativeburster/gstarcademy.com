import os
import re

# Standard site-notice HTML to inject
notice_html = """
      <aside
        class="site-notice"
        id="site-notice"
        data-notice-id="global-v1"
        aria-label="Announcement"
      >
        <div class="site-notice-inner container">
          <p class="site-notice-text">
            Tip: open the
            <a class="site-notice-link" href="./tutorials.html">tutorial library</a>
            to filter by software, task, level, and source—then follow outbound links to the originals.
          </p>
          <button type="button" class="site-notice-close" aria-label="Dismiss announcement">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      </aside>"""

files = ["index.html", "tutorials.html", "news.html", "about.html", "knowledge-base.html"]

for f in files:
    path = os.path.join(os.getcwd(), f)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove any existing site-notice to avoid duplicates
        content = re.sub(r'<aside[^>]*class="site-notice[^"]*"[^>]*>.*?</aside>', '', content, flags=re.DOTALL)
        
        # Inject notice right after <div class="header-stack ..."> or before <header class="topbar">
        # Let's wrap topbar in header-stack if it's not already
        if '<div class="header-stack">' not in content and '<div class="header-stack ' not in content:
            # For news and tutorials, we might need to wrap it
            content = content.replace('<header class="topbar">', '<div class="header-stack"><header class="topbar">')
            content = content.replace('</header>\n\n\n    <main', '</header></div>\n\n\n    <main')

        # Find header-stack opening and inject after it
        content = re.sub(r'(<div class="header-stack[^>]*>)', r'\1' + notice_html, content)
        
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Injected notice into {f}")
