import PySimpleGUI as sg
from pathlib import Path

instruments = [
    "Trumpet",
    "Piano",
    "Guitar",
    "Drums"
]

home = Path.home()
midi_dir = home / "Documents" / "YT_trumpet" / "midis"
song_dir = home / "Documents" / "YT_trumpet" / "songs"
logo_path = home / "Documents" / "YT_trumpet" / "Big_Logo.png"
icon_path = home / "Documents" / "YT_trumpet" / "Big_Logo_alt.ico"

track_number = 5

midi_files = [
    file.name
    for file in midi_dir.iterdir()
    if file.suffix.lower() in (".mid", ".midi")
]
song_files = [
    file.name
    for file in song_dir.iterdir()
    if file.suffix.lower() == ".txt"
]

layout = [
    [sg.Text("What would you like to do?")],
    [sg.Button('Convert MIDI')],
    [sg.Button('Play song')],
    [sg.VPush()],
    [sg.Push(), sg.Image(filename=logo_path)]
]

window = sg.Window('Youtube trumpet autoplayer', layout, size=(500, 300), icon=icon_path)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if event == "Convert MIDI":
        midi_layout = [
            [sg.Text("Select MIDI")],
            [sg.Combo(midi_files, key="-MIDI-", readonly=True)],
            [sg.Button('Convert')],
            [sg.VPush()],
            [sg.Push(), sg.Image(filename=logo_path)]
        ]

        midi_window = sg.Window('MIDI converter', midi_layout, size=(350, 250), icon=icon_path)

        while True:
            midi_event, midi_values = midi_window.read()
            if midi_event == sg.WINDOW_CLOSED or midi_event == 'Quit':
                    break
            if midi_event == "Convert":
                selected_file = midi_values["-MIDI-"]

                if not selected_file:
                    sg.popup("Please select a MIDI file first.")

                else:
                    midi_path = midi_dir / selected_file

                    track_layout = [
                        [sg.Text("Assign instruments")],
                    ]

                    for i in range(track_number):
                        track_layout.append([
                            sg.Text(f"Track {i + 1}"),
                            sg.Combo(instruments, key=f"-TRACK-{i}-", readonly=True)
                        ])

                    track_layout.append([
                        sg.Button("Continue")
                    ])

                    track_layout.append ([
                        [sg.VPush()],
                        [sg.Push(), sg.Image(filename=logo_path)]
                    ])

                    track_window = sg.Window("Insturment assignment", track_layout, size=(300,250), icon=icon_path)

                    while True:
                        track_event, track_values = track_window.read()
                        if track_event == sg.WINDOW_CLOSED or midi_event == 'Quit':
                            break

                        if track_event == "Continue":
                            assignments = []

                            for i in range(track_number):
                                assignments.append(track_values[f"-TRACK-{i}-"])

                            break

                    midi_name = sg.popup_get_text('Song name?')
                    print(midi_path)
                    print(assignments)
                    print(midi_name)
                    #convert code go here
                    break
        
        track_window.close()
        midi_window.close()

    if event == "Play song":
        song_layout = [
            [sg.Text("Select song")],
            [sg.Combo(song_files, key="-SONG-", readonly=True)],
            [sg.Button('Play')],
            [sg.VPush()],
            [sg.Push(), sg.Image(filename=logo_path)]
        ]

        song_window = sg.Window('Song player', song_layout, size=(350, 250), icon=icon_path)

        while True:
            song_event, song_values = song_window.read()
            if song_event == sg.WINDOW_CLOSED or song_event == 'Quit':
                break
            if song_event == "Play":
                selected_file = song_values["-SONG-"]

                if not selected_file:
                    sg.popup("Please select a song first.")

                else:
                    song_path = song_dir / selected_file

                    print(song_path)
                    #play code go here i think
                    break

        song_window.close()

window.close()