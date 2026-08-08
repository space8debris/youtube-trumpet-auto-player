import subprocess
import time
import re
import pyautogui
from collections import defaultdict
from python_mpv_jsonipc import MPV
from pathlib import Path  
from pathlib import Path
from mido import MidiFile
import sys


home = Path.home()
instruments_dir = home / "Documents" / "YT_trumpet" / "insterments"
folder = home / "Documents" / "YT_trumpet" / "songs"
root = home / "Documents" / "YT_trumpet"



if len(sys.argv) > 1:
    target_path = Path(sys.argv[1])
else:
    text_songs = []
    for item in folder.iterdir():
        if item.is_file() and item.suffix == '.txt' and 'mpv_log' not in item.name:
            text_songs.append(item.name)

    print('\n'.join(f"{idx}. {song}" for idx, song in enumerate(text_songs, 1)))

    song_selection_num = int(input("Select track number to play: "))
    chosen_text_file = text_songs[song_selection_num - 1]

    target_path = folder.joinpath(chosen_text_file)

string = target_path.read_text()

min_voices_per = {"T": 0, "D": 0, "P": 0, "G": 0}
song_data = string


if "Max Voices:" in string:
    lines = [line.strip() for line in string.splitlines() if line.strip()]
    header_line = lines[0]
    song_data = "\n".join(lines[1:])
    
    header = header_line.replace("Max Voices:", "").replace(",", " ").strip()
    
    for token in header.split():
        if len(token) >= 2:
            inst_letter = token[0].upper()
            max_voice_num = token[1:]
            
            if inst_letter in min_voices_per and max_voice_num.isdigit():
                  min_voices_per[inst_letter] = int(max_voice_num)


instruments = {
    "T": {
        "url": str(instruments_dir / "trumpet_fast.mp4"),
        "volume": 60,
        "midi_note": 60,          
        "seek_start": 15.2,            
        "voices": [f"T{i}" for i in range(1, min_voices_per["T"] + 1)],
        "voice_index": 0               
    },
    "D": {
        "url": str(instruments_dir / "drum_fast.mp4"),
        "volume": 60,
        "midi_note": 60,          
        "seek_start": 15.0,            
        "voices": [f"D{i}" for i in range(1, min_voices_per["D"] + 1)],    
        "voice_index": 0
    },
    "P": {
        "url": str(instruments_dir / "piano_fast.mp4"),
        "volume": 60,
        "midi_note": 60,          
        "seek_start": 15.0,            
        "voices": [f"P{i}" for i in range(1, min_voices_per["P"] + 1)],  
        "voice_index": 0
    },
     "G": {
            "url": str(instruments_dir / "Guitar_fast.mp4"),
            "volume": 70,
            "midi_note": 60,          
            "seek_start": 15.0,            
            "voices": [f"G{i}" for i in range(1, min_voices_per["G"] + 1)],  
            "voice_index": 0
        },
}

all_pipes = []
for letter in instruments:
    all_pipes.extend(instruments[letter]["voices"])

wfl = {pipe_name: i for i, pipe_name in enumerate(all_pipes)}

screen_w, screen_h = pyautogui.size()

windows = len(all_pipes)
needed = max(1, min(10, windows)) 

grid_w = screen_w// 6
grid_h = screen_h// 6

positions = []
for i in range(len(all_pipes)):
    col = i % 6
    row = i // 6
    positions.append((col * grid_w, row * grid_h))

MPV_PATH = home / "Documents" / "YT_trumpet" / "MPV" / "mpv.exe"

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

order = re.compile(r"(?P<time>\d+\.?\d*)(?P<letter>[A-Za-z])(?P<voice>\d{1,2})(?P<note>\d{2})(?P<velocity>\d{3})")

def spliter(token):
    m = order.match(token)
    if not m:
        raise ValueError(f"Bad entry: {token}")
    return float(m.group("time")), m.group("letter"), m.group("voice"), m.group("note"), m.group("velocity")

split = song_data.split()
play = [spliter(t) for t in split]
play.sort(key=lambda e: e[0])
print(play)

thing = defaultdict(list)
for ev in play:
 rounded_event_time = round(ev[0], 2)
 thing[rounded_event_time].append(ev)


for conntrol in conntrols:
    try:
        conntrol.command("set_property", "pause", False)
    except Exception:
        pass


ct = 0.0
end_time = max(thing.keys()) if thing else 0

start_time = time.perf_counter()

active_voices = {}

while ct <= end_time:
    ct = round(time.perf_counter() - start_time, 2)

    if ct in thing:
        for info in thing[ct]:
            event_time, letter, voice, note, velocity = info
            print(f"Time {event_time}: play {letter}{voice} note {note}")

            if letter in instruments:
                inst_data = instruments[letter]
                
                picked_pipe = f"{letter}{int(voice)}"
                
                conntrol_list_i_am_running_out_of_names = wfl[picked_pipe]
                conntrol = conntrols[conntrol_list_i_am_running_out_of_names]
                
                midi_note = int(note)
                
                semitone_offset = midi_note - inst_data["midi_note"]
                
                
                pitch_multiplier = 2 ** (semitone_offset / 12)
                #honesly no clue how this eqation works but it dose i found i on wikipida 
                try:

                    velocity_scale = int(velocity) / 127
                    scaled_volume = inst_data["volume"] * velocity_scale
                    
                    conntrol.command("set_property", "volume", inst_data["volume"])
                    conntrol.command("set_property", "pitch", pitch_multiplier)
                    conntrol.command("seek", inst_data["seek_start"], "absolute+keyframes")

                except:
                    pass


    time.sleep(0.001)
    #let me just
    #make it a nice 222 lines