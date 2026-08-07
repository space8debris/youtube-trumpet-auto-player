from pathlib import Path
from mido import MidiFile

folder_path = Path('C:/Users/dakoda/Documents/code_things/midis')

file_list = []
midi_list = []
absolute_time = 0.0

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
print("\n(T, D, P) hit Enter to skip:")
for channel in sorted_channels:
    user_choice = input(f"Channel {channel} ({channel_track_info[channel]}) -> (T/D/P): ").strip().upper()
    
    if user_choice in ['T', 'D', 'P']:
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

    msg_dict.pop('velocity', None)

    msg_dict['time'] = round(absolute_time, 2)

    if 'channel' in msg_dict:
        if msg_dict['channel'] in instrument_map:
            msg_dict['channel'] = instrument_map[msg_dict['channel']]
        else:
          continue

    if 'note' in msg_dict:
        msg_dict['note'] = msg_dict['note']
        msg_dict['voice'] = 1
        for past_item in reversed(midi_list):
            if 'channel' in past_item and 'channel' in msg_dict and past_item['channel'] == msg_dict['channel']:
                time_gap = msg_dict['time'] - past_item['time']
                
                if time_gap <= 0.3:
                    if past_item.get('voice') == 1:
                        msg_dict['voice'] = 2
                    elif past_item.get('voice') == 2:
                        msg_dict['voice'] = 3
                    elif past_item.get('voice') == 3:
                        msg_dict['voice'] = 4
                    elif past_item.get('voice') == 4:
                        msg_dict['voice'] = 5
                    elif past_item.get('voice') == 5:
                        msg_dict['voice'] = 6
                    elif past_item.get('voice') == 6:
                        msg_dict['voice'] = 1
                break

    midi_list.append(msg_dict)


for item in midi_list:
    if 'note' in item and 'channel' in item and 'voice' in item:
        print(f"{item['time']}{item['channel']}{item['voice']}{item['note']}", end=" ")
print()


final_string_data = " ".join(
    f"{item['time']}{item['channel']}{item['voice']}{item['note']}" 
    for item in midi_list 
    if 'note' in item and 'channel' in item and 'voice' in item
)
export_folder = Path(r"C:\Users\dakoda\Documents\code_things\songs")

songname = input("name ")+ ".txt"

output_file = export_folder.joinpath(songname)


file_path = export_folder.joinpath(songname)


output_file.write_text(final_string_data)

print(f"\n\n->saved to: {output_file.name}")
#hii