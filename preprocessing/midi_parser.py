"""midi_parser.py

This converts midi files into numpy tensors.
The output tensor should contain: time (midi ticks) x pitch (127) x instruments

"""
import numpy as np
from scipy import sparse
import mido


def get_notes(track):
    return set([mes.note for mes in track if mes.type == 'note_on'])


def get_messages(track):
    for mes in track:
        if mes.type == 'note_on' or mes.type == 'note_off':
            yield mes


def get_messages_with_note(track, note):
    return [mes for mes in get_messages(track) if mes.note == note]


def get_channel(track):
    for mes in get_messages(track):
        if 'channel' in mes.dict():
            return mes.channel
    return None


def convert_to_array(track, tick_size, total_ticks):
    output = np.zeros((total_ticks, 128), dtype=np.int8)
    state = np.zeros(128, dtype=np.int8)
    cur_time = 0

    for message in get_messages(track):
        if message.time > 0:
            output[cur_time:(cur_time + message.time // tick_size), :] = state
            cur_time += message.time // tick_size

        state[message.note] = message.velocity > 0

    return output


def get_tick_size(file):
    time_signature = [mes for mes in file.tracks[0] if mes.type == 'time_signature']
    if time_signature:
        notated_32 = time_signature[0].notated_32nd_notes_per_beat
    else:
        print('Missing time signature, assuming 4')
        notated_32 = 4

    return file.ticks_per_beat // notated_32


def get_total_ticks(file, tick_size):
    tempo = [mes for mes in file.tracks[0] if mes.type == 'set_tempo']
    if tempo:
        tempo = tempo[0].tempo
    else:
        print('Missing tempo, assuming 120 bmp')
        tempo = 500000

    return int(np.ceil(file.length / (tempo / 10000000)))


def convert_midi_file(filename, split_to_instruments=False):
    """Convert a midi file into the trainable numpy tensor

    :param filename: Name of file to read
    :return: A numpy tensor with: time x pitch x instruments
    """
    file = mido.MidiFile(filename)
    tick_size = get_tick_size(file)
    total_ticks = get_total_ticks(file, tick_size)

    array_tracks = {
        get_channel(track): sparse.csr_matrix(convert_to_array(track, tick_size, total_ticks))
        for track in file.tracks
    }

    return array_tracks
