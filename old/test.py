import FreeSimpleGUI as sg

sg.theme("DarkGrey11")

# LEFT SIDEBAR
sidebar = [
    [sg.Text("Notes", font=("Any", 12, "bold"))],
    [sg.Listbox(
        values=[
            "band notes",
            "daily mix",
            "haster som faem",
            "rsdfs",
            "the same album",
            "søknad",
            "Welcome"
        ],
        size=(20, 20),
        key="-NAV-",
        enable_events=True
    )]
]

# RIGHT CONTENT
content = [
    [sg.Text("albums", font=("Any", 20, "bold"), text_color="#e5c07b")],
    [sg.Text("formula", font=("Any", 12, "bold"))],
    [sg.Multiline(
        """1. epic intro
2. energetic
3. keep the momentum
4. slow down a little
5. ballad
6. knock the pace up
7. orchestral
8. single
9. rock
10. fastest song
11. sentimental song
12. epic conclusion

album 1
""",
        size=(50, 20),
        border_width=0,
        background_color=sg.theme_background_color(),
        key="-CONTENT-"
    )]
]

# LAYOUT
layout = [
    [
        sg.Column(sidebar, pad=(0, 0)),
        sg.VSeparator(),
        sg.Column(content, pad=(10, 0), expand_x=True, expand_y=True)
    ]
]

window = sg.Window("Notes App", layout, resizable=True)

# EVENT LOOP
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "-NAV-":
        selected = values["-NAV-"][0]
        window["-CONTENT-"].update(f"You selected:\n\n{selected}")

window.close()