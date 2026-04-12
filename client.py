import FreeSimpleGUI as sg
import requests

ip = "192.168.20.74"
port = 8000
headers = {"X-API-Key": "mysecret123"}

def load_notes():
    r = requests.get(f"http://{ip}:{port}/notes", headers=headers)

    if r.status_code != 200:
        return {}, {}

    data = r.json()

    notes = {}
    contents = {}

    for row in data:
        note_id = row[0]
        title = row[2] if len(row) > 2 else f"Note {note_id}"
        content = row[3] if len(row) > 3 else ""

        notes[title] = note_id
        contents[note_id] = content

    return notes, contents

def refresh():
    global notes_dict, contents_dict

    notes_dict, contents_dict = load_notes()

    window["-NAV-"].update(values=list(notes_dict.keys()))

sidebar = [
    [sg.Text("Notes", font=("Any", 12, "bold"))],
    [sg.Listbox(
        values=[],
        size=(20, 35),
        key="-NAV-",
        enable_events=True
    )],
    [sg.Button("Save")],
    [sg.Button("New Note")],
    [sg.Button("Delete")],
    [sg.Button("Exit")]
]

content = [
    [sg.Multiline(
        key="-CONTENT-",
        size=(80, 35),
        border_width=0
    )]
]

layout = [
    [sg.Column(sidebar), sg.VSeparator(), sg.Column(content)]
]

window = sg.Window("Notes App", layout, resizable=True, finalize=True)

notes_dict, contents_dict = load_notes()
window["-NAV-"].update(list(notes_dict.keys()))

current_note_id = None

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    if event == "-NAV-":
        selected = values["-NAV-"]
        if selected:
            name = selected[0]
            current_note_id = notes_dict[name]
            window["-CONTENT-"].update(contents_dict.get(current_note_id, ""))

    if event == "Save" and current_note_id:
        payload = [
            {
                "id": current_note_id,
                "content": values["-CONTENT-"]
            }
        ]
        requests.post(
            f"http://{ip}:{port}/update",
            headers=headers,
            json=payload
        )

    if event == "New Note":
        name = sg.popup_get_text("Note name:")

        if name:
            requests.post(
                f"http://{ip}:{port}/make-note",
                headers=headers,
                json=name
            )
            refresh()

    if event == "Delete" and current_note_id:
        requests.post(
            f"http://{ip}:{port}/delete",
            headers=headers,
            json=current_note_id
        )

        current_note_id = None
        window["-CONTENT-"].update("")
        refresh()

window.close()