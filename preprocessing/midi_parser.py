"""midi_parser.py

This converts midi files into numpy tensors.
The output tensor should contain: time (midi ticks) x pitch (127) x instruments

"""
import numpy as np
import mido


def detect_instruments():
    """This should be based on what Simon described,
    some basic logic for pitches"""
    pass


def get_track_messages(mid_file):
    """split a midi file into list of note_on/note_off for each channel"""
    pass


def get_notes(track):
    return set([mes.note for mes in track if mes.type == 'note_on'])


def get_messages_with_note(track, note):
    return [mes for mes in track if mes.type == 'note_on' and mes.note == 60]


def convert_to_array(track, tick_size, total_ticks):
    """Create an array for one instrument; time x pitch"""
    output_array = np.zeros((total_ticks, 127))

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


def convert_midi_file(filename, detect_instrument=None):
    """Convert a midi file into the trainable numpy tensor

    :param filename: Name of file to read
    :param detect_instrument: function to evaluate the instrument of a channel
    :return: A numpy tensor with: time x pitch x instruments
    """
    file = mido.MidiFile(filename)
    tick_size = get_tick_size(file)
    total_ticks = get_total_ticks(file, tick_size)
    tracks = get_track_messages(file)

    # split and apply `and` within instrument groups
    instruments = {}
    if not detect_instrument:
        detect_instrument = dict(zip(range(len(tracks)), tracks))

    for track in tracks:
        instrument = detect_instrument(track)
        if instrument not in instruments:
            instruments[instrument] = []
        instrument[instrument].append(track)

    midi_arrays = [convert_to_array(track, tick_size, total_ticks) for track in tracks]
