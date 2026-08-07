import PySimpleGUI as sg
from pathlib import Path
import subprocess
import sys
from mido import MidiFile

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



midi_files = [
    file.name
    for file in midi_dir.iterdir()
    if file.suffix.lower() in (".mid", ".midi")
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

                    mid = MidiFile(midi_path)

                    song_names = {}
                    for i, track in enumerate(mid.tracks):
                        song_names[i] = f"Track {i} (Unnamed)"
                        for track_msg in track:
                            if track_msg.type in ['track_name', 'instrument_name']:
                                song_names[i] = track_msg.name
                                break

                    channel_track_info = {}
                    for i, track in enumerate(mid.tracks):
                        for track_msg in track:
                            if track_msg.type == 'note_on' and track_msg.velocity > 0 and hasattr(track_msg, 'channel'):
                                channel_track_info[track_msg.channel] = song_names[i]

                    sorted_channels = sorted(list(channel_track_info.keys()))

                    track_layout = [
                        [sg.Text("Assign instruments")],
                    ]

                    for ch in sorted_channels:
                        track_layout.append([
                            sg.Text(f"Channel {ch} ({channel_track_info[ch]})"),
                            sg.Combo(instruments, key=f"-CH-{ch}-", readonly=True)
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

                            for ch in sorted_channels:
                                assignments.append(track_values[f"-CH-{ch}-"])

                            break

                    midi_name = sg.popup_get_text('Song name?')
                    print(midi_path)
                    print(assignments)
                    print(midi_name)
                    name_to_letter = {"Trumpet": "T", "Drums": "D", "Piano": "P", "Guitar": "G"}

                    answer_lines = []
                    for choice in assignments:
                        letter = name_to_letter.get(choice, "")  
                        answer_lines.append(letter)

                    answer_lines.append(midi_name)  

                    input_text = "\n".join(answer_lines) + "\n"

                    result = subprocess.run(
                        [sys.executable, "midi maker.py", str(midi_path)],
                        input=input_text,
                        text=True,
                        cwd=home / "Documents" / "YT_trumpet",
                        capture_output=True
                    )

                    print("STDOUT:", result.stdout)
                    print("STDERR:", result.stderr)

                   
                    break
        
        track_window.close()
        midi_window.close()

    if event == "Play song":
        song_files = [
        file.name
        for file in song_dir.iterdir()
        if file.suffix.lower() == ".txt"
         ]
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
                    subprocess.Popen(
                    [sys.executable, "many yt trumpets .py", str(song_path)],
                    cwd=home / "Documents" / "YT_trumpet"
                    )
                    break

        song_window.close()

window.close()
