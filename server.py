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
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(rows).encode())

    def do_POST(self):

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body)
        except:
            data = None

        if self.path == "/make-note":
            cursor.execute(
                "INSERT INTO notes (title, content) VALUES (?, ?)",
                (data, "")
            )
            conn.commit()

            self.send_response(200)
            self.end_headers()

        elif self.path == "/update":
            for n in data:
                cursor.execute("""
                    UPDATE notes
                    SET content = ?
                    WHERE id = ?
                """, (n["content"], n["id"]))

            conn.commit()

            self.send_response(200)
            self.end_headers()

        elif self.path == "/delete":
            cursor.execute(
                "DELETE FROM notes WHERE id = ?",
                (data,)
            )
            conn.commit()

            self.send_response(200)
            self.end_headers()


server = HTTPServer(("0.0.0.0", 8000), Handler)
print("Server running on port 8000")
server.serve_forever()