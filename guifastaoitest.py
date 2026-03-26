import requests
import FreeSimpleGUI as sg

server = "https://192.168.20.74:8000"

sidebar = [
    [sg.Listbox(values=[], size=(20, 50), key="-NAV-", enable_events=True)],
    [sg.Button("New Note"), sg.Button("Save"), sg.Button("Exit")]
]

content = [
    [sg.Multiline(
        size=(80, 20),
        key="-CONTENT-",
        border_width=0,
        background_color=sg.theme_background_color()
    )]
]

window = sg.Window("Simple Notepad", [sidebar + [sg.VSeparator(), sg.Column(content)]], finalize=True)
notes = {}  

def load_notes():
    global notes
    r = requests.get(f"{server}/notes", verify=False)  # verify=False if using self-signed HTTPS
    r.raise_for_status()
    notes_list = r.json()
    notes = {n["notename"]: n["id"] for n in notes_list}
    window["-NAV-"].update(values=list(notes.keys()))

load_notes()

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break

    if event == "-NAV-":
        name = values["-NAV-"][0]
        r = requests.get(f"{server}/notes", verify=False)
        note = next(n for n in r.json() if n["id"] == notes[name])
        window["-CONTENT-"].update(note["contents"])

    elif event == "Save":
        name = values["-NAV-"][0]
        note_id = notes[name]
        requests.put(f"{server}/notes/{note_id}",
                     json={"notename": name, "contents": window["-CONTENT-"].get()},
                     verify=False)

    elif event == "New Note":
        name = sg.popup_get_text("Note name:")
        if name:
            r = requests.post(f"{server}/notes",
                              json={"notename": name, "contents": ""},
                              verify=False)
            notes[name] = r.json()["id"]
            window["-NAV-"].update(values=list(notes.keys()))

window.close()