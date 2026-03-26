import FreeSimpleGUI as sg
import json
import os

DATA_FILE = "notes.json"

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

window = sg.Window(
    "Simple Notepad",
    [sidebar + [sg.VSeparator(), sg.Column(content)]],
    finalize=True
)

notes = {}  # {name: contents}


# --------------------------
# File Handling
# --------------------------
def load_notes():
    global notes
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            notes = json.load(f)
    else:
        notes = {}

    window["-NAV-"].update(values=list(notes.keys()))


def save_notes():
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=2)


load_notes()

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    if event == "-NAV-":
        if values["-NAV-"]:
            name = values["-NAV-"][0]
            window["-CONTENT-"].update(notes.get(name, ""))

    elif event == "Save":
        if values["-NAV-"]:
            name = values["-NAV-"][0]
            notes[name] = window["-CONTENT-"].get()
            save_notes()

    elif event == "New Note":
        name = sg.popup_get_text("Note name:")
        if name:
            notes[name] = ""
            window["-NAV-"].update(values=list(notes.keys()))
            save_notes()

window.close()