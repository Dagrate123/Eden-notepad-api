# stage1_local_notes.py

import FreeSimpleGUI as sg
import sqlite3

conn = sqlite3.connect("server.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT
)
""")

conn.commit()

def load_notes():
    cursor.execute("SELECT id, title FROM notes")
    return {title: note_id for note_id, title in cursor.fetchall()}

notes = load_notes()

layout = [
    [sg.Listbox(list(notes.keys()), key="-NAV-", size=(20,20), enable_events=True)],
    [sg.Multiline(key="-CONTENT-", size=(60,20))],
    [sg.Button("Save"), sg.Button("New")]
]

window = sg.Window("Notes", layout)

current_id = None

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "-NAV-":
        name = values["-NAV-"][0]
        current_id = notes[name]
        cursor.execute("SELECT content FROM notes WHERE id=?", (current_id,))
        window["-CONTENT-"].update(cursor.fetchone()[0])

    if event == "Save" and current_id:
        cursor.execute("UPDATE notes SET content=? WHERE id=?",
                       (values["-CONTENT-"], current_id))
        conn.commit()

    if event == "New":
        name = sg.popup_get_text("Name:")
        if name:
            cursor.execute("INSERT INTO notes (title, content) VALUES (?,?)", (name, ""))
            conn.commit()
            notes = load_notes()
            window["-NAV-"].update(list(notes.keys()))

window.close()