"""midi_parser.py

This converts midi files into numpy tensors.
The output tensor should contain: time (midi ticks) x pitch (127) x instruments

"""
import numpy as np
from scipy import sparse
import mido


def get_note_messages(track):
    for mes in track:
        if mes.type == 'note_on' or mes.type == 'note_off':
            yield mes


def get_messages_with_note(track, note):
    return [mes for mes in get_note_messages(track) if mes.note == note]


def get_channel(track):
    for mes in get_note_messages(track):
        if 'channel' in mes.dict():
            return mes.channel
    return None


def convert_to_array(track, tick_size, total_ticks):
    output = np.zeros((total_ticks, 128), dtype=np.int8)
    state = np.zeros(128, dtype=np.int8)
    cur_time = 0

    for message in get_note_messages(track):
        if message.time > 0:
            output[cur_time:(cur_time + message.time // tick_size), :] = state
            cur_time += message.time // tick_size

        state[message.note] = message.velocity > 0

    return output


def get_notated_32(file):
    time_signature = [mes for mes in file.tracks[0] if mes.type == 'time_signature']
    if time_signature:
        notated_32 = time_signature[0].notated_32nd_notes_per_beat
    else:
        print('Missing time signature, assuming 4')
        notated_32 = 4
    return notated_32


def get_tempo(file, tick_size):
    tempo = [mes for mes in file.tracks[0] if mes.type == 'set_tempo']
    if tempo:
        tempo = tempo[0].tempo
    else:
        print('Missing tempo, assuming 120 bmp')
        tempo = 500000

    return tempo


def get_program(track):
    for message in track:
        if hasattr(message, 'program'):
            return int(message.program)


def convert_midi_file(filename, split_to_instruments=False):
    """Convert a midi file into the trainable numpy tensor

    :param filename: Name of file to read
    :return: A numpy tensor with: time x pitch x instruments
    """
    file = mido.MidiFile(filename)

    notated_32 = get_notated_32(file)
    tick_size = file.ticks_per_beat // notated_32
    tempo = get_tempo(file, tick_size)
    total_ticks = int(np.ceil(file.length / (tempo / 10000000)))

    array_tracks = {
        'tracks': {
            get_channel(track): sparse.csr_matrix(convert_to_array(track, tick_size, total_ticks))
            for track in file.tracks
        }
    }

    program_changes = {
        get_channel(track): get_program(track) for track in file.tracks
    }

    array_tracks['meta'] = {
        'notated_32': notated_32,
        'tick_size': tick_size,
        'tempo': tempo,
        'total_ticks': total_ticks,
        'program': program_changes,
    }

    return array_tracks
