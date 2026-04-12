import FreeSimpleGUI as sg
import requests

def load_notes():
    r = requests.get("http://192.168.20.74:8000/notes")
    data = r.json()
    return {row[1]: row[0] for row in data}

notes = load_notes()

layout = [
    [sg.Listbox(list(notes.keys()), key="-NAV-", size=(20,20))]
]

window = sg.Window("Notes", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()