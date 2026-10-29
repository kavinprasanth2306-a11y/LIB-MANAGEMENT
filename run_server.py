import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Clean terminal logging
        try:
            sys.stdout.write(f"[LuminaLib Web Server] {self.address_string()} - {format % args}\n")
            sys.stdout.flush()
        except Exception:
            pass

    def copyfile(self, source, outputfile):
        """Handle client disconnects gracefully without crashing the server."""
        try:
            super().copyfile(source, outputfile)
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            pass

def main():
    os.chdir(DIRECTORY)
    # Enable address reuse
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 65)
        print("  LuminaLib — DSA Glassmorphism Library Management System")
        print("=" * 65)
        print(f"  [+] Local URL:   {url}")
        print(f"  [+] Directory:   {DIRECTORY}")
        print(f"  [+] Status:      Server is live! Press Ctrl+C to stop.")
        print("=" * 65)
        
        # Open in default browser automatically
        try:
            webbrowser.open(url)
            print("  [>] Launched site automatically in your browser!")
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server gracefully...")
            httpd.server_close()

if __name__ == "__main__":
    main()

