import FreeSimpleGUI as sg

# Define the layout
layout = [
    [sg.Text("Click the button to exit.")],
    [sg.Button("Ok"), sg.Button("Exit")]  # Add the Exit button
]

# Create the window
window = sg.Window("My Application", layout)

# Event loop
while True:
    event, values = window.read()
    
    # Check if the user closed the window or clicked the Exit button
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    # Other event handling logic can go here
    if event == "Ok":
        sg.popup("You clicked Ok")

# Close the window
window.close()
