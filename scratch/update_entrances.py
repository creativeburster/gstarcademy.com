import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def update_file(file_path):
    rel_path = os.path.relpath(file_path, ROOT_DIR)
    depth = 0 if rel_path == '.' else len(rel_path.split(os.sep)) - 1
    prefix = '../../' if depth == 2 else '../' if depth == 1 else './'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original_len = len(content)
    
    # 1. 确定当前页面的 active-nav 类型
    file_name = os.path.basename(file_path)
    active_nav = 'none'
    if file_name == 'index.html':
        active_nav = 'home'
    elif file_name == 'knowledge-domains.html':
        active_nav = 'domains'
    elif file_name == 'knowledge-roadmap.html':
        active_nav = 'roadmap'
    elif file_name == 'quiz.html':
        active_nav = 'quiz'
    elif file_name in ['knowledge-base.html', 'kb-software.html', 'kb-terms.html', 'kb-faq.html', 'kb-graph.html', 'kb-vendors.html', 'knowledge-cax.html', 'knowledge-curriculum.html', 'knowledge-library.html', 'knowledge-glossary.html'] or 'kb/' in rel_path.replace('\\', '/'):
        active_nav = 'knowledge'
    elif file_name in ['tutorials.html', 'tutorial-detail.html']:
        active_nav = 'tutorials'
    elif file_name == 'news.html':
        active_nav = 'news'
    elif file_name in ['about.html', 'contact.html', 'editorial-process.html']:
        active_nav = 'about'

    # 2. 生成新版 Topbar Navigation Link (精简顶栏，Wiki在domains/roadmap激活)
    is_knowledge_active = active_nav in ['knowledge', 'domains', 'roadmap']
    nav_html = f'''<nav class="nav">
            <div class="nav-header">
              <button class="nav-close" aria-label="Close navigation menu">
                <span class="nav-close-icon">×</span>
              </button>
            </div>
            <a class="nav-link{" active" if active_nav == "home" else ""}" data-nav="home" href="{prefix}index.html">Home</a>
            <a class="nav-link{" active" if is_knowledge_active else ""}" data-nav="knowledge" href="{prefix}knowledge-base.html">Wiki</a>
            <a class="nav-link{" active" if active_nav == "quiz" else ""}" data-nav="quiz" href="{prefix}quiz.html">Quiz</a>
            <a class="nav-link{" active" if active_nav == "tutorials" else ""}" data-nav="tutorials" href="{prefix}tutorials.html">Tutorials</a>
            <a class="nav-link{" active" if active_nav == "news" else ""}" data-nav="news" href="{prefix}news.html">News</a>
            <a class="nav-link{" active" if active_nav == "about" else ""}" data-nav="about" href="{prefix}about.html">About</a>
            <!-- Streak Fire Badge -->
            <div class="streak-fire-hud" id="global-streak-badge" style="display:none;" title="Your daily streak Days">
              🔥 <span id="global-streak-count">0</span> Days
            </div>
          </nav>'''
    content = re.sub(r'<nav class="nav">.*?</nav>', nav_html, content, flags=re.DOTALL)

    # 3. 替换 Footer 的 Structured Learn 板块
    footer_html = f'''<div class="site-footer-col">
          <h4 class="site-footer-heading">Structured Learn</h4>
          <ul class="site-footer-links">
            <li><a href="{prefix}knowledge-domains.html">Domain Map</a></li>
            <li><a href="{prefix}knowledge-roadmap.html">Interactive Map</a></li>
            <li><a href="{prefix}quiz.html">Quiz Challenge</a></li>
            <li><a href="{prefix}tutorials.html">Tutorial Library</a></li>
            <li><a href="{prefix}knowledge-base.html">Knowledge Center</a></li>
            <li><a href="{prefix}kb-graph.html">Interactive Graph</a></li>
            <li><a href="{prefix}kb-software.html">Software Index</a></li>
            <li><a href="{prefix}kb-terms.html">CAD Glossary</a></li>
            <li><a href="{prefix}kb-faq.html">Technical FAQ</a></li>
          </ul>
        </div>'''
        
    content = re.sub(r'<div class="site-footer-col">\s*<h4 class="site-footer-heading">Structured Learn</h4>.*?</ul>\s*</div>', footer_html, content, flags=re.DOTALL)

    # 4. 替换 Sidebar (若存在) - 仅限知识库相关页面
    if 'class="kb-sidebar' in content or 'id="kb-rail"' in content:
        # 先清除之前已经可能添加过的 "Learning Tools" 盒子，防止重复插入
        content = re.sub(r'\s*<div class="kb-index-box"[^>]*?>\s*<strong class="kb-index-title">Learning Tools</strong>.*?</div>', '', content, flags=re.DOTALL)
        
        sidebar_inject = f'''<input
          type="search"
          id="kb-sidebar-search"
          class="kb-portal-search"
          placeholder="Search titles &amp; terms…"
          autocomplete="off"
        />
            <div class="kb-index-box" style="margin-top: 16px;">
              <strong class="kb-index-title">Learning Tools</strong>
              <a class="kb-index-link" href="{prefix}knowledge-roadmap.html">Interactive Roadmap</a>
              <a class="kb-index-link" href="{prefix}quiz.html">Quiz Challenge</a>
            </div>'''
        
        # 在搜索框后注入 Learning Tools 盒子
        content = re.sub(r'<input[^>]*?class="kb-portal-search"[^>]*?>', sidebar_inject, content, count=1, flags=re.DOTALL)

    # 5. 替换二级子导航栏 kb-subnav (若存在)
    if 'class="kb-subnav"' in content:
        # 确定二级栏的活跃子项
        kb_active = 'overview'
        if file_name in ['kb-software.html', 'kb-vendors.html'] or 'kb/software/' in rel_path.replace('\\', '/'):
            kb_active = 'software'
        elif file_name in ['kb-terms.html', 'knowledge-glossary.html']:
            kb_active = 'terms'
        elif file_name == 'kb-faq.html':
            kb_active = 'faq'
        elif file_name == 'kb-graph.html':
            kb_active = 'graph'
        elif file_name == 'quiz.html':
            kb_active = 'quiz'
        elif file_name == 'knowledge-domains.html':
            kb_active = 'domains'
        elif file_name == 'knowledge-roadmap.html':
            kb_active = 'roadmap'

        subnav_html = f'''<nav class="kb-subnav" aria-label="Knowledge base sections">
          <a class="kb-subnav-link{" active" if kb_active == "overview" else ""}" href="{prefix}knowledge-base.html">Overview</a>
          <a class="kb-subnav-link{" active" if kb_active == "software" else ""}" href="{prefix}kb-software.html">Software</a>
          <a class="kb-subnav-link{" active" if kb_active == "terms" else ""}" href="{prefix}kb-terms.html">Terms</a>
          <a class="kb-subnav-link{" active" if kb_active == "faq" else ""}" href="{prefix}kb-faq.html">FAQ</a>
          <a class="kb-subnav-link{" active" if kb_active == "graph" else ""}" href="{prefix}kb-graph.html">Graph</a>
          <div class="kb-subnav-dropdown">
            <a class="kb-subnav-link{" active" if kb_active in ["quiz", "domains", "roadmap"] else ""}" href="{prefix}quiz.html">Quiz ▾</a>
            <div class="kb-subnav-dropdown-content">
              <a href="{prefix}knowledge-domains.html">Domains</a>
              <a href="{prefix}knowledge-roadmap.html">Roadmap</a>
            </div>
          </div>
        </nav>'''
        
        content = re.sub(r'<nav class="kb-subnav".*?</nav>', subnav_html, content, flags=re.DOTALL)

    if len(content) != original_len:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {rel_path}")

def main():
    print("Scanning for HTML files in workspace...")
    for root, dirs, files in os.walk(ROOT_DIR):
        if '.git' in root or '.system_generated' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                update_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
