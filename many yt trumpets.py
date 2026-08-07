import subprocess
import time
import re
import pyautogui
from collections import defaultdict
from python_mpv_jsonipc import MPV
from pathlib import Path  
import math

home = Path.home()

instruments_dir = home / "Documents" / "code_things" / "insterments"

instruments = {
    "T": {
        "url": str(instruments_dir / "trumpet_fast.mp4"),
        "midi_note": 60,          
        "seek_start": 15.2,            
        "voices": ["T1", "T2", "T3", "T4", "T5", "T6"],  
        "voice_index": 0               
    },
    "D": {
        "url": str(instruments_dir / "drum_fast.mp4"),
        "midi_note": 60,          
        "seek_start": 15.0,            
        "voices": ["D1", "D2", "D3","D4","D5","D6"],    
        "voice_index": 0
    },
    "P": {
        "url": str(instruments_dir / "piano_fast.mp4"),
        "midi_note": 60,          
        "seek_start": 15.0,            
        "voices": ["P1", "P2", "P3", "P4", "P5", "P6"],  
        "voice_index": 0
    },
}

all_pipes = []
for letter in instruments:
    all_pipes.extend(instruments[letter]["voices"])

wfl = {pipe_name: i for i, pipe_name in enumerate(all_pipes)}

screen_w, screen_h = pyautogui.size()

grid_w = screen_w// 6
grid_h = screen_h// 3

positions = []
for i in range(len(all_pipes)):
    col = i % 6
    row = i // 6
    positions.append((col * grid_w, row * grid_h))

MPV_PATH = r"C:\MVP\mpv.exe"

pipes = []
for i, pipe in enumerate(all_pipes):
    letter = pipe[0]
    video_url = instruments[letter]["url"]

    subprocess.Popen([
        MPV_PATH,
        f"--geometry={grid_w}x{grid_h}+{positions[i][0]}+{positions[i][1]}",
        f"--input-ipc-server=\\\\.\\pipe\\{pipe}",
        "--keep-open=yes",
        "--cache=yes",
        "--demuxer-max-bytes=500M",
        "--audio-pitch-correction=no",
        "--pause",
        "--volume=40",
        video_url,
    ])
    pipes.append(pipe)
    #tbh i have no clue how this part works but it dose and i found it on stack over folw so it wtvr ig :)

time.sleep(2)

def retry_pipe_thing(pipe_name, tries=30, delay=0.5):
    last_err = None
    for i in range(tries):
        try:
            return MPV(start_mpv=False, ipc_socket=pipe_name)
        except Exception as e:
         last_err = e
         time.sleep(delay)
            
    raise RuntimeError(f":( {pipe_name}: {last_err}")
#same with this part lolz

conntrols = [retry_pipe_thing(p) for p in pipes]

#this is were setup code endss i dont like to put comments


order = re.compile(r"(?P<time>\d+\.?\d*)(?P<letter>[A-Za-z])(?P<voice>\d)(?P<note>\d+)")

def spliter(token):
    m = order.match(token)
    if not m:
        raise ValueError(f"Bad entry: {token}")
    return float(m.group("time")), m.group("letter"), m.group("voice"), m.group("note")


folder = home / "Documents" / "code_things" / "songs"

text_songs = []
for item in folder.iterdir():
    
    if item.is_file() and item.suffix == '.txt' and 'mpv_log' not in item.name:
        text_songs.append(item.name)

print('\n'.join(f"{idx}. {song}" for idx, song in enumerate(text_songs, 1)))

song_selection_num = int(input("Select track number to play: "))
chosen_text_file = text_songs[song_selection_num - 1]

target_timeline_path = folder.joinpath(chosen_text_file)
string = target_timeline_path.read_text()


split = string.split()
play = [spliter(t) for t in split]
play.sort(key=lambda e: e[0])
print(play)

thing = defaultdict(list)
for ev in play:
 rounded_event_time = round(ev[0], 2)
 thing[rounded_event_time].append(ev)

input("space to start")

for conntrol in conntrols:
    try:
        conntrol.command("set_property", "pause", False)
    except Exception:
        pass


ct = 0.0
end_time = max(thing.keys()) if thing else 0

start_time = time.perf_counter()

while ct <= end_time:
    ct = round(time.perf_counter() - start_time, 2)

    if ct in thing:
        for info in thing[ct]:
            event_time, letter, voice, note = info
            print(f"Time {event_time}: play {letter} note {note}")

            if letter in instruments:
                inst_data = instruments[letter]
                
                picked_pipe = f"{letter}{voice}"
                
                conntrol_list_i_am_running_out_of_names = wfl[picked_pipe]
                conntrol = conntrols[conntrol_list_i_am_running_out_of_names]
                
                midi_note = int(note)
                
                semitone_offset = midi_note - inst_data["midi_note"]
                
                
                pitch_multiplier = 2 ** (semitone_offset / 12)
                #honesly no clue how this eqation works but it dose i found i on wikipida 
                try:
                    
                    conntrol.command("set_property", "pitch", pitch_multiplier)
                    
            
                    conntrol.command("seek", inst_data["seek_start"], "absolute+keyframes")
                    
                except Exception as e:
                 print(f"It failed i think the stack overflow page said to add this{picked_pipe} at t={event_time}: {e}")

    
    time.sleep(0.001)
