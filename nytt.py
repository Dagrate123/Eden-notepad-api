import requests 
import FreeSimpleGUI as sg

sidebar = [
    [sg.Text("Notes", font=("Any", 12, "bold"))],
    [sg.Listbox(
        values=[],
        size=(20, 50),
        key="-NAV-",
        enable_events=True
    )],
    [sg.Button('Exit')],
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

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
window.close()