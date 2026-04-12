from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
import hashlib

API_KEY = "mysecret123"

conn = sqlite3.connect("server.db", check_same_thread=False)
cursor = conn.cursor()

conn.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    notename TEXT,
    contents TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

try:
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("test", hash_password("pass"))
    )
    conn.commit()
except:
    pass

class Handler(BaseHTTPRequestHandler):

    # -------------------------
    # AUTH CHECK
    # -------------------------
    def is_authorized(self):
        return self.headers.get("X-API-Key") == API_KEY


    def do_GET(self):
        if not self.is_authorized():
            self.send_response(403)
            self.end_headers()
            return

        if self.path == "/notes":
            cursor.execute("SELECT * FROM notes WHERE user_id = 1")
            rows = cursor.fetchall()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(rows).encode())

    def do_POST(self):

        if not self.is_authorized():
            self.send_response(403)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body)
        except:
            data = None

        if self.path == "/make-note":
            cursor.execute(
                "INSERT INTO notes (user_id, notename, contents) VALUES (1, ?, '')",
                (data,)
            )
            conn.commit()

            self.send_response(200)
            self.end_headers()

        elif self.path == "/update":
            for note in data:
                cursor.execute("""
                    UPDATE notes
                    SET contents = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (note["content"], note["id"]))

            conn.commit()

            self.send_response(200)
            self.end_headers()

        elif self.path == "/delete":
            cursor.execute("DELETE FROM notes WHERE id = ?", (data,))
            conn.commit()

            self.send_response(200)
            self.end_headers()

        elif self.path == "/login":
            username = data["username"]
            password = hash_password(data["password"])

            cursor.execute(
                "SELECT id FROM users WHERE username=? AND password=?",
                (username, password)
            )

            user = cursor.fetchone()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            if user:
                self.wfile.write(json.dumps({"status": "ok", "user_id": user[0]}).encode())
            else:
                self.wfile.write(json.dumps({"status": "error"}).encode())

server = HTTPServer(("0.0.0.0", 8000), Handler)
print("Server running on http://localhost:8000")
server.serve_forever()