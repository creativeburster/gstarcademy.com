import os

GTAG_HTML = """    <!-- Google tag (gtag.js) - Performance Optimized Loading -->
    <link rel="preconnect" href="https://www.googletagmanager.com" />
    <link rel="dns-prefetch" href="https://www.googletagmanager.com" />
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      window.gtag = gtag;
      window.addEventListener('load', function() {
        const initGtag = () => {
          const script = document.createElement('script');
          script.src = 'https://www.googletagmanager.com/gtag/js?id=G-ZV3YR72933';
          script.async = true;
          document.head.appendChild(script);
          gtag('js', new Date());
          gtag('config', 'G-ZV3YR72933');
        };
        if ('requestIdleCallback' in window) {
          requestIdleCallback(initGtag);
        } else {
          setTimeout(initGtag, 1);
        }
      });
    </script>"""

def inject_gtag(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        if '.git' in root or 'node_modules' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except UnicodeDecodeError:
                    with open(path, 'r', encoding='latin-1') as file:
                        content = file.read()
                
                # Check if tag is already there
                if 'G-ZV3YR72933' in content:
                    continue
                
                if '<head>' in content:
                    # Insert right after <head>
                    new_content = content.replace('<head>', f'<head>\n{GTAG_HTML}')
                    with open(path, 'w', encoding='utf-8', newline='') as file:
                        file.write(new_content)
                    print(f"Injected Google Tag into: {os.path.relpath(path, directory)}")
                    count += 1
                    
    print(f"Total HTML files updated statically: {count}")

if __name__ == '__main__':
    inject_gtag('f:/CAD-tutorial')
