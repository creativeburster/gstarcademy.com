import os
import re

notice_html = """
    <div class="header-stack">
      <aside
        class="site-notice"
        id="site-notice"
        data-notice-id="global-v2"
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
      </aside>
      <header class="topbar">"""

files = ["index.html", "tutorials.html", "news.html", "about.html", "knowledge-base.html"]

for f in files:
    path = os.path.join(os.getcwd(), f)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove any existing site-notice AND header-stack wrappers
        content = re.sub(r'<div class="header-stack[^>]*>.*?<header class="topbar">', '<header class="topbar">', content, flags=re.DOTALL)
        content = re.sub(r'<aside[^>]*class="site-notice[^"]*"[^>]*>.*?</aside>', '', content, flags=re.DOTALL)
        
        # Inject the new clean structure
        content = content.replace('<header class="topbar">', notice_html)
        
        # Ensure we close the header-stack div after topbar
        # Usually topbar ends with </div>\n    </header>
        if '</div>\n    </header>' in content:
            content = content.replace('</div>\n    </header>', '</div>\n    </header>\n    </div>')
        elif '</div>\n      </header>' in content:
            content = content.replace('</div>\n      </header>', '</div>\n      </header>\n    </div>')

        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Refreshed global notice in {f}")
