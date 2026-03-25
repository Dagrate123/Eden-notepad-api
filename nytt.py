import requests 
import FreeSimpleGUI as sg
import sqlite3

server = sqlite3.connect('server.db')
cursor = server.cursor()

sidebar = [
    [sg.Text("Notes", font=("Any", 12, "bold"))],
    [sg.Listbox(
        values=[],
        size=(20, 50),
        key="-NAV-",
        enable_events=True
    )],
    [sg.Button('Save')], [sg.Button('Exit')],
]

content = [
    [sg.Multiline(
        size=(256, 65),
        border_width=0,
        background_color=sg.theme_background_color(),
        key="-CONTENT-"
    )]
]

layout = [
    [
        sg.Column(sidebar, pad=(0, 0)), 
        sg.VSeparator(), 
        sg.Column(content, pad=(10, 0), expand_x=True, expand_y=True)
    ]
]

window = sg.Window('Fullscreen', layout, finalize=True)
window.maximize()

cursor = server.cursor()
server.execute("SELECT id, notename FROM notes WHERE user_id = ?", (1, )),
notater = cursor.fetchall()
notat_dictionary = {name: note_id for note_id, name in notater}

window["-NAV-"].update(values=list(notat_dictionary.keys()))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "-NAV-":
        selected = values["-NAV-"]
        if selected:
            note_name = selected[0]
            note_id = notat_dictionary[note_name]

            cursor.execute("SELECT contents FROM notater WHERE id = ?", (note_id, ))
            content = cursor.fetchone()[0]

            window["-CONTENT-"].update(value=content)

    if event == Save:
        selected = values["-NAV-"]
        if selected:
            note_name = selected[0]
            note_id = notat_dictionary[note_name]
            new_content = values["-CONTENT-"]

            cursor.execute(
                """
                UPDATE notater
                SET contents = ?, updated_at = CURRENT_TIMESTAMP,
                WHERE id = ? 
                """, (new_content, note_id)
            )

            server.commit()

window.close()