#!/usr/bin/env python3
"""
Frontend Web Server for Midnight Compliance Intelligence
Serves the X402 payment frontend on port 8000
Run payment_api.py on port 5008 separately
"""

import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Prettier logging
        print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print("""
╔════════════════════════════════════════════════════════════════╗
║  🌙 Midnight Compliance Intelligence - Frontend Server        ║
╠════════════════════════════════════════════════════════════════╣
║  🔗 Diagnostic:   http://localhost:8000/phantom-test.html     ║
║  🚀 Main App:     http://localhost:8000/midnight-x402-fixed.html
║                                                                ║
║  ⚠️  IMPORTANT: Payment API must be running separately!       ║
║      Run in another terminal: python payment_api.py           ║
║                                                                ║
║  🛑 Press Ctrl+C to stop                                      ║
╚════════════════════════════════════════════════════════════════╝
""")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped")