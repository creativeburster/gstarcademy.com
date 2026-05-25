import os
import http.server
import socketserver

PORT_START = 3001
MAX_PORT_TRIES = 100

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Default translation
        translated = super().translate_path(path)
        
        # If it's a directory, let SimpleHTTPRequestHandler handle index.html
        if os.path.isdir(translated):
            return translated
            
        # Get path without query parameters or hash
        pure_path = path.split('?')[0].split('#')[0]
        
        # If the file exists directly, use it
        if os.path.exists(translated) and os.path.isfile(translated):
            return translated
            
        # If it doesn't have an extension, try appending .html
        _, ext = os.path.splitext(pure_path)
        if not ext:
            html_path = translated + '.html'
            if os.path.exists(html_path) and os.path.isfile(html_path):
                return html_path
                
        return translated

def run_server():
    handler = CleanURLHandler
    
    # Try finding an open port starting from 3001
    port = PORT_START
    server = None
    
    while port < PORT_START + MAX_PORT_TRIES:
        try:
            server = socketserver.TCPServer(("", port), handler)
            print("\n" + "="*50)
            print(f" Gstarcademy Clean URLs Dev Server is active!")
            print(f" Local URL: http://localhost:{port}")
            print(" Press Ctrl+C to stop the server.")
            print("="*50 + "\n")
            server.serve_forever()
            break
        except OSError as e:
            # Port in use, try next
            print(f"Port {port} is currently busy. Trying next port...")
            port += 1
            
    if not server:
        print("Error: Could not find any available ports to start the server.")

if __name__ == "__main__":
    run_server()
