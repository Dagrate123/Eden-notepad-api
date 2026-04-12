# stage2_server_basic.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json

conn = sqlite3.connect("server.db", check_same_thread=False)
cursor = conn.cursor()

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/notes":
            cursor.execute("SELECT * FROM notes")
            rows = cursor.fetchall()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(rows).encode())

server = HTTPServer(("0.0.0.0", 8000), Handler)
server.serve_forever()