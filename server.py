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

def do_POST(self):
    if self.path == "/make-note":
        length = int(self.headers["Content-Length"])
        data = json.loads(self.rfile.read(length))

        cursor.execute("INSERT INTO notes (title, content) VALUES (?,?)", (data, ""))
        conn.commit()

        self.send_response(200)
        self.end_headers()