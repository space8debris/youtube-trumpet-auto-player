from pathlib import Path
from mido import MidiFile
import sys   

print("ARGV:", sys.argv)

home = Path.home()

midi_dir = home / "Documents" / "YT_trumpet" / "midis"
song_dir = home / "Documents" / "YT_trumpet" / "songs"

folder_path = (midi_dir)

file_list = []
midi_list = []
absolute_time = 0.0

if len(sys.argv) > 1:
    midi_file = Path(sys.argv[1])
    print(f"Received file from prent: {midi_file}")
else:
    for item in folder_path.iterdir():
        if item.is_file():
            file_list.append(item.name)

    print('\n'.join(f"{i}. {file}" for i, file in enumerate(file_list, 1)))

    midi_num = int(input("what file:"))
    midi = file_list[midi_num-1]
    print(midi)
    midi_file = folder_path.joinpath(midi)
    print(midi_file)

mid = MidiFile(midi_file)

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

for channel in sorted_channels:
    track_text = channel_track_info[channel]
    print(f"Channel {channel:2d} -> {track_text}")

instrument_map = {}
print("\n(T, D, P, G) hit Enter to skip:")
for channel in sorted_channels:
    user_choice = input(f"Channel {channel} ({channel_track_info[channel]}) -> (T/D/P): ").strip().upper()
    
    if user_choice in ['T', 'D', 'P', 'G']:
       instrument_map[channel] = user_choice
#stack overflow was usefull
print(f"\ninstruments: {instrument_map}\nProcessing timeline...")


for msg in mid: 

    absolute_time += msg.time
    
    if msg.type == 'note_off':
     continue
    
    if msg.type == 'note_on' and msg.velocity == 0:
      continue
    
    if msg.type == 'end_of_track':
       continue
        
    msg_dict = msg.dict()

    msg_dict['time'] = round(absolute_time, 2)

    if 'channel' in msg_dict:
        if msg_dict['channel'] in instrument_map:
            msg_dict['channel'] = instrument_map[msg_dict['channel']]
        else:
          continue

    if 'note' in msg_dict:
        active_voices = set()
        for past_item in reversed(midi_list):
            if past_item.get('channel') == msg_dict['channel']:
                time_gap = msg_dict['time'] - past_item['time']

                if time_gap > 0.3:
                 break
                
                if 'voice' in past_item:
                 active_voices.add(past_item['voice'])

        chosen_voice = 1
        while chosen_voice in active_voices:
            chosen_voice += 1

        if chosen_voice > 18:
            chosen_voice = 1

        msg_dict['voice'] = chosen_voice

    midi_list.append(msg_dict)


for item in midi_list:
    if 'note' in item and 'channel' in item and 'voice' in item:
        print(f"{item['time']}{item['channel']}{item['voice']}{item['note']}{item['velocity']:03d}", end=" ")
print()


most_voices = {}
for item in midi_list:
    if 'channel' in item and 'voice' in item:
        channel = item['channel']
        voice = item['voice']

        if channel not in most_voices or voice > most_voices[channel]:
         most_voices[channel] = voice

header_list = [f"{ch}{v}" for ch, v in sorted(most_voices.items())]
header_string = "Max Voices: " + ", ".join(header_list) + "\n\n"

final_string = " ".join(
    f"{item['time']}{item['channel']}{item['voice']}{item['note']}{item['velocity']:03d}" 
    for item in midi_list 
    if 'note' in item and 'channel' in item and 'voice' in item
)

final_song = header_string + final_string


export_folder = Path(song_dir)

songname = input("name ")+ ".txt"

output_file = export_folder.joinpath(songname)


file_path = export_folder.joinpath(songname)


output_file.write_text(final_song)

print(f"\n\n->saved to: {output_file.name}")
#hii