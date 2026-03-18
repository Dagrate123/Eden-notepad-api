import requests 
import FreeSimpleGUI as sg

tab_layout1 = [[sg.Button('Exit'), sg.Checkbox('My first Checkbox!')],
               [sg.Button('Another Button.')]]
tab_layout2 = [
    [sg.Button('My third Button!'), sg.Checkbox('My second Checkbox!')],
        [sg.Text("Enter your message:")],
        [sg.Multiline(size=(150, 150), key='-MESSAGE-')],
]

tab_layout3 = [[sg.Button('Exit')]]

layout = [
    [sg.TabGroup([[sg.Tab("Tab 1", tab_layout1), sg.Tab("Tab 2", tab_layout2), sg.Tab("Exit", tab_layout3)]])],
    [sg.Button('Exit')]]


layout1 = [
    [sg.Multiline(key='-ML-', write_only=True, size=(60,10))]
]

window = sg.Window('Fullscreen', layout, finalize=True, element_justification='center')
window.maximize()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()