import os
import re

def optimize_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    # 1. 优化 GTag 脚本
    gtag_old_pattern = r'<!-- Google tag \(gtag\.js\).*?<\/script>'
    gtag_new = '''<!-- Google tag (gtag.js) - Performance Optimized Loading -->
    <link rel="preconnect" href="https://www.googletagmanager.com" />
    <link rel="dns-prefetch" href="https://www.googletagmanager.com" />
    <script data-cfasync="false" async src="https://www.googletagmanager.com/gtag/js?id=G-ZV3YR72933"></script>
    <script data-cfasync="false">
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      window.gtag = gtag;
      (function() {
        var gaId = 'G-ZV3YR72933';
        if (window['ga-disable-' + gaId] === true) return;
        try {
          var ua = navigator.userAgent || '';
          if (navigator.webdriver === true) {
            window['ga-disable-' + gaId] = true;
            return;
          }
          if (/HeadlessChrome|PhantomJS|Playwright|Puppeteer|SlimerJS|CasperJS/i.test(ua)) {
            window['ga-disable-' + gaId] = true;
            return;
          }
          var sw = window.screen ? window.screen.width : 0;
          var sh = window.screen ? window.screen.height : 0;
          var res = sw + 'x' + sh;
          var botRes = {
            '1280x1200': 1,
            '1366x1366': 1,
            '1280x1280': 1,
            '1600x1600': 1,
            '1280x1600': 1,
            '1600x1200': 1,
            '800x600': 1
          };
          if (botRes[res] === 1 || (sw > 0 && sw === sh)) {
            window['ga-disable-' + gaId] = true;
            return;
          }
          var canvas = document.createElement('canvas');
          var gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
          if (gl) {
            var debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            if (debugInfo) {
              var renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) || '';
              if (/SwiftShader|llvmpipe|Software Rasterizer/i.test(renderer)) {
                window['ga-disable-' + gaId] = true;
                return;
              }
            }
          }
        } catch (e) {}
        gtag('consent', 'default', {
          'analytics_storage': 'denied', 'ad_storage': 'denied', 'ad_user_data': 'denied', 'ad_personalization': 'denied',
          'region': ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','GB','CH'],
          'wait_for_update': 500
        });
        gtag('consent', 'default', {
          'analytics_storage': 'granted', 'ad_storage': 'denied', 'ad_user_data': 'denied', 'ad_personalization': 'denied'
        });
        try {
          var cp = JSON.parse(localStorage.getItem('learncad-cookie-prefs-v2') || 'null');
          if (cp) gtag('consent', 'update', { 'analytics_storage': cp.analytics ? 'granted' : 'denied' });
        } catch (e) {}
        gtag('js', new Date());
        gtag('config', gaId);
      })();
    </script>'''
    
    if "googletagmanager.com/gtag/js" in content:
        content = re.sub(gtag_old_pattern, gtag_new, content, flags=re.DOTALL)

    # 2. 优化 Google Fonts 异步非阻塞
    fonts_pattern = r'<link\s+rel="stylesheet"\s+href="(https:\/\/fonts\.googleapis\.com\/css2\?[^"]+)"\s*\/?>'
    
    def fonts_repl(match):
        url = match.group(1)
        return (
            f'<link rel="preload" as="style" href="{url}" />\n'
            f'    <link rel="stylesheet" href="{url}" media="print" onload="this.media=\'all\'" />\n'
            f'    <noscript>\n'
            f'      <link rel="stylesheet" href="{url}" />\n'
            f'    </noscript>'
        )
        
    # Only replace if not already preload + media="print"
    if "media=\"print\" onload=\"this.media='all'\"" not in content:
        content = re.sub(fonts_pattern, fonts_repl, content)

    # 3. 优化 Cookie Consent 容器初始隐藏以消除 CLS
    cookie_pattern = r'(<div\s+id="cookie-consent"[^>]*data-cookie-banner)([^>]*)>'
    def cookie_repl(m):
        attrs = m.group(1) + m.group(2)
        if 'style=' not in attrs:
            return attrs + ' style="display:none;">'
        elif 'display:none' not in attrs:
            return re.sub(r'style="([^"]*)"', r'style="\1;display:none;"', attrs) + '>'
        return m.group(0)

    content = re.sub(cookie_pattern, cookie_repl, content)

    # 4. 优化页脚标题层级 (h4 -> h3 for .site-footer-heading)
    content = re.sub(r'<h4 class="site-footer-heading">([^<]+)</h4>', r'<h3 class="site-footer-heading">\1</h3>', content)

    if content != orig:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def scan_and_optimize(base_dir):
    updated = 0
    total = 0
    for root, dirs, files in os.walk(base_dir):
        # 排除 git 等隐藏目录
        if '.git' in root or '.system_generated' in root or 'scratch' in root or 'node_modules' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                total += 1
                path = os.path.join(root, f)
                if optimize_html_file(path):
                    updated += 1
                    print(f"Optimized: {os.path.relpath(path, base_dir)}")
    print(f"Optimization complete. {updated}/{total} HTML files updated.")

if __name__ == '__main__':
    base_path = 'F:/gstarcademy'
    scan_and_optimize(base_path)
