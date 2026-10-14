import http.server
import os

PORT = 8080

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        clean = path.split('?')[0].split('#')[0]
        
        if clean == '/':
            clean = '/index.html'
        elif clean in ['/blog', '/blog/']:
            clean = '/blog.html'
        elif clean.startswith('/blog/'):
            sub = clean[len('/blog/'):].strip('/')
            if not any(sub.endswith(ext) for ext in ['.svg', '.png', '.jpg', '.jpeg', '.css', '.js']):
                if os.path.exists(os.path.join('blog', f'{sub}.html')):
                    clean = f'/blog/{sub}.html'
        elif not os.path.exists('.' + clean) and os.path.exists('.' + clean.rstrip('/') + '.html'):
            clean = clean.rstrip('/') + '.html'
            
        return super().translate_path(clean)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    print(f"Starting MyLogoQR Local Dev Server on port {PORT}...")
    server = http.server.ThreadingHTTPServer(('localhost', PORT), CleanURLHandler)
    server.serve_forever()
