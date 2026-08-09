import http.server
import os

PORT = 8080

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Split out query parameters or hashes to map clean file paths
        path = self.path.split('?')[0].split('#')[0]
        
        if path == '/':
            self.path = '/index.html'
        elif not os.path.exists('.' + path) and os.path.exists('.' + path + '.html'):
            self.path = path + '.html'
            
        return super().do_GET()

if __name__ == '__main__':
    print(f"Starting MyLogoQR Local Dev Server on port {PORT}...")
    server = http.server.HTTPServer(('localhost', PORT), CleanURLHandler)
    server.serve_forever()
