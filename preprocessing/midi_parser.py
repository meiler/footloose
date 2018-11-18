"""midi_parser.py

This converts midi files into numpy tensors.
The output tensor should contain: time (midi ticks) x pitch (127) x instruments

"""
import numpy as np
import mido
from .instruments import is_bass, is_harmony, is_lead


def detect_instruments(track):
    """This should be based on what Simon described,
    some basic logic for pitches"""
    if is_bass(track):
        return 'bass'

    if is_harmony(track):
        return 'harmony'

    if is_lead(track):
        return 'trumpet'
    return 'other'


def get_notes(track):
    return set([mes.note for mes in track if mes.type == 'note_on'])


def get_messages(track):
    for mes in track:
        if mes.type == 'note_on':
            yield mes


def get_messages_with_note(track, note):
    return [mes for mes in get_messages(track) if mes.note == note]


def get_channel(track):
    for mes in get_messages(track):
        if 'channel' in mes.dict():
            return mes.channel
    return None


def convert_to_array(track, tick_size, total_ticks):
    """Create an array for one instrument; time x pitch"""
    output_array = np.zeros((total_ticks, 128))

    notes = get_notes(track)

    for note in notes:
        time_now = 0
        messages = get_messages_with_note(track, note)
        for mes in messages:
            time_now += mes.time // tick_size
            output_array[time_now:, note] = 1 if mes.velocity > 0 else 0

    return output_array


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

    return int(np.ceil(file.length / (tempo / 1000000)))


def split_to_instruments(array_tracks):
    # split and apply `and` within instrument groups
    instruments = {}
    for i, track in array_tracks.items():
        if i == 10:
            instrument = 'drum'
        else:
            instrument = detect_instruments(track)

        if instrument == 'other':
            continue

        # gather instruments together
        if instrument not in instruments:
            instruments[instrument] = []
        instruments[instrument].append(track)

    if len(instruments.keys()) < 4:
        return None

    # harmony should be summed, for everything else we pick the most present channel
    drums = instruments['drum'][np.argmax(map(np.sum, instruments['drum']))]
    bass = instruments['bass'][np.argmax(map(np.sum, instruments['bass']))]
    harmony = sum(instruments['harmony'], np.zeros(instruments['harmony'][0].shape)).astype(np.int8)
    trumpets = instruments['trumpet'][np.argmax(map(np.sum, instruments['trumpet']))]

    return np.array([drums,
                     bass,
                     harmony,
                     trumpets
                     ])


def convert_midi_file(filename, split_to_instruments=False):
    """Convert a midi file into the trainable numpy tensor

    :param filename: Name of file to read
    :return: A numpy tensor with: time x pitch x instruments
    """
    file = mido.MidiFile(filename)
    tick_size = get_tick_size(file)
    total_ticks = get_total_ticks(file, tick_size)

    array_tracks = {
        get_channel(track): convert_to_array(track, tick_size, total_ticks)
        for track in file.tracks
    }

    if split_to_instruments:
        return split_to_instruments(array_tracks)
    return array_tracks
