import requests 
import FreeSimpleGUI as sg
import sqlite3

server = sqlite3.connect("server.db") #connecter serveren til db-fil
cursor = server.cursor() #pointer til serveren
server.execute("PRAGMA foreign_keys = ON") #æøå allowed

server.execute(""" 
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(25) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
""") #lager tabellen users - work in progress

server.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    notename VARCHAR(25),
    contents TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
""") #lage trabellen dr notatene blir lagret 

cursor.execute("SELECT COUNT(*) FROM notes") #skal inserte users safely, men det er null brukere
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("test", "pass"))

    cursor.execute("INSERT INTO notes (user_id, notename, contents) VALUES (?, ?, ?)", (1, "note1", "hei, content"))
    cursor.execute("INSERT INTO notes (user_id, notename, contents) VALUES (?, ?, ?)", (1, "note2", "hei2, content2"))
    cursor.execute("INSERT INTO notes (user_id, notename, contents) VALUES (?, ?, ?)", (1, "note3", "hei3, content3"))

    server.commit()

def load_notes(): #loader riktig notat fra listen
    cursor.execute("SELECT id, notename FROM notes WHERE user_id = ?", (1,))
    rows = cursor.fetchall()
    return {name: note_id for note_id, name in rows}
 
def refresh_listbox(): #refresh sidebaren
    global notat_dictionary
    notat_dictionary = load_notes()
    window["-NAV-"].update(values=list(notat_dictionary.keys()))

sidebar = [ #sidebar på siden av skjermen 
    [sg.Text("Notes", font=("Any", 12, "bold"))],
    [sg.Listbox(
        values=[],
        size=(20, 40),
        key="-NAV-",
        enable_events=True,
        expand_y=True,
        right_click_menu=['', ['Rename', 'Delete', 'Add To-Do']] #når du right clcker kommer denne menuen opp
    )],
    [sg.Button('Save')],
    [sg.Button('New Note')],
    [sg.Button('Exit')]
]

content = [
    [sg.Multiline(
        size=(256, 65),
        border_width=0,
        background_color=sg.theme_background_color(),
        key="-CONTENT-"
    )]
]

layout = [ #layouten gjør den om til en sidebar med Litt padding
    [
        sg.Column(sidebar, pad=(0, 0)), 
        sg.VSeparator(), 
        sg.Column(content, pad=(10, 0), expand_x=True, expand_y=True)
    ]
]

window = sg.Window('Notes App', layout, resizable=True, finalize=True) #storskjerm
window.maximize()

cursor = server.cursor()
cursor.execute("SELECT id, notename FROM notes WHERE user_id = ?", (1, )),
notater = cursor.fetchall()
notat_dictionary = {name: note_id for note_id, name in notater}

window["-NAV-"].update(values=list(notat_dictionary.keys()))

while True: #notatene
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "-NAV-":
        selected = values["-NAV-"]
        if selected:
            note_name = selected[0]
            note_id = notat_dictionary[note_name]

            cursor.execute("SELECT contents FROM notes WHERE id = ?", (note_id, ))
            content = cursor.fetchone()[0]

            window["-CONTENT-"].update(value=content)

    if event == "Save": #lagrer notatene i databasen
        selected = values["-NAV-"]
        if selected:
            note_name = selected[0]
            note_id = notat_dictionary[note_name]
            new_content = values["-CONTENT-"]
            print("Saving:", note_name, new_content)

            cursor.execute(
                """
                UPDATE notes
                SET contents = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ? 
                """, (new_content, note_id)
            )

            server.commit()

    if event == "New Note": #legger til ny notat i tabellen 
        new_name = sg.popup_get_text("Enter note name:")
        if new_name:
            cursor.execute(
                "INSERT INTO notes (user_id, notename, contents) VALUES (?, ?, ?)",
                (1, new_name, "")
            )
            server.commit()
            refresh_listbox()

    if event == "Rename": #popup vindu som lar deg rename notatene
        selected = values["-NAV-"]
        if selected:
            old_name = selected[0]
            new_name = sg.popup_get_text("Rename note:", default_text=old_name)
 
            if new_name:
                note_id = notat_dictionary[old_name]
                cursor.execute(
                    "UPDATE notes SET notename = ? WHERE id = ?",
                    (new_name, note_id)
                )
                server.commit()
                refresh_listbox()
 
    if event == "Delete": #sletter notatene 
        selected = values["-NAV-"]
        if selected:
            note_name = selected[0]
            note_id = notat_dictionary[note_name]
 
            confirm = sg.popup_yes_no(f"Delete '{note_name}'?")
            if confirm == "Yes":
                cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
                server.commit()
                window["-CONTENT-"].update("")
                refresh_listbox()
 
    if event == "Add To-Do":
        selected = values["-NAV-"]
        if selected:

            layout = [
                [sg.Text('Select your tasks:')],
                [sg.Checkbox('Task 1', default=True, key='-OPT1-')],
                [sg.Checkbox('Task 2', key='-OPT2-')],
                [sg.Button('Submit'), sg.Button('Exit')]
            ]

            todo_window = sg.Window('Add To-Do', layout)

            while True:
                ev, vals = todo_window.read()

                if ev == sg.WIN_CLOSED or ev == 'Exit':
                    break

                if ev == 'Submit':
                    tasks = []

                    if vals['-OPT1-']:
                        tasks.append("- [x] Task 1")
                    else:
                        tasks.append("- [ ] Task 1")

                    if vals['-OPT2-']:
                        tasks.append("- [x] Task 2")
                    else:
                        tasks.append("- [ ] Task 2")

                    current = values["-CONTENT-"]
                    updated = current + "\n" + "\n".join(tasks)
                    window["-CONTENT-"].update(updated)

                    break

            todo_window.close()


window.close()