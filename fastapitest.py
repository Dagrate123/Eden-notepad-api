from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import sqlite3 

app = FastAPI(title="notepad server")

DB = "server.db"

class Note(BaseModel):
    id: int | None = None
    user_id: int
    notename: str
    contents: str

class NoteCreate(BaseModel):
    user_id: int
    notename: str
    contents: str

def init_db():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    con.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    notename VARCHAR(25),
    contents TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
""")
    con.commit()
    con.close()

init_db()

@app.get("/notes/{user_id}", response_model=List[Note])
def get_notes(user_id: int):
    con = sqlite3.connect(DB)
    cursor = con.cursor()
    cursor.execute("SELECT id, notename FROM notes WHERE user_id = ?", (1, )),
    notater = cursor.fetchall()
    con.close()
    return [Note(id=i[0]), user_id(id=i[1], notename=i[2], contents = i[3]) for i in notater]

@app.post("/notes")
def create_note(note: Note):
    con = sqlite3.connect(DB)
    cursor = con.cursor()
    cursor.execute("INSERT INTO notes (notename, contents) VALUES (?, ?)", (note.notename, note.contents))
    note.id = cursor.lastrowid
    con.commit()
    con.close()
    return note

@app.put("/notes/{note_id}")
def update_note(note_id: int, note: Note):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET notename=?, contents=? WHERE id=?", (note.notename, note.contents, note_id))
    conn.commit()
    conn.close()
    return note
