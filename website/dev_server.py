import http.server
import socketserver
import os
import urllib.parse
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        clean_path = urllib.parse.unquote(parsed.path).strip('/')
        
        if clean_path == '':
            return super().do_GET()

        local_target = os.path.join(DIRECTORY, clean_path.replace('/', os.sep))

        if os.path.isdir(local_target):
            idx_file = os.path.join(local_target, 'index.html')
            if os.path.exists(idx_file):
                if not parsed.path.endswith('/'):
                    self.send_response(301)
                    new_loc = parsed.path + '/'
                    if parsed.query:
                        new_loc += '?' + parsed.query
                    self.send_header('Location', new_loc)
                    self.end_headers()
                    return
                return super().do_GET()

        if not os.path.exists(local_target):
            if os.path.exists(local_target + '.html'):
                self.path = '/' + clean_path + '.html'
                if parsed.query:
                    self.path += '?' + parsed.query

        return super().do_GET()

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    # Bind to 0.0.0.0 so localhost, 127.0.0.1 and LAN IP all work
    with socketserver.TCPServer(('0.0.0.0', PORT), CleanURLHandler) as httpd:
        print(f'Server running at http://localhost:{PORT}/ (Press Ctrl+C to stop)')
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
