# 4_instruments.py

# manipulates and returns numpy files.

import numpy as np
from scipy import sparse
from preprocessing.midi_encoder import read_np_file


""" Dictionary:
Lead = 0
Harmony = 1
Bass = 2
Drums = 9
"""
leadprogram = 57 # trumpet
harmonyprogram = 1 # piano
bassprogram = 34 # bass guitar (picked)
# drums are assigned by channel 9.

def get_drumtracks(array_tracks):
    drumtracks = []
    tracks = array_tracks['tracks']
    meta = array_tracks['meta']
    for track in tracks.keys():
        if meta['program'][track] in range(112, 122): # maybe too small range?
            drumtracks.append(track)
        if track == 9 and meta['program'][track] is None:
            drumtracks.append(track)

    return drumtracks


def is_lead(nptrack):
    # the lead is mostly 1 pitch at a time
    # and it is above 47 on average
    """ Checks if it mostly plays one pitch at a time and the average pitch is high.
    """
    instrument_present = [nodes for nodes in nptrack.sum(axis=1) if nodes > 0]
    harmonies = [nodes for nodes in instrument_present if nodes > 1]

    harmony_percentage = len(harmonies) / len(instrument_present)

    if harmony_percentage > 0.1:  # often (90 percent) two nodes at the same time
        return False
    elif np.average(np.nonzero(nptrack)[0]) < 47:
        return False
    else:
        return True


def is_harmony(nptrack):
    """ Checks if it mostly plays several pitch at a time.
    """
    instrument_present = [nodes for nodes in nptrack.sum(axis=1) if nodes > 0]
    harmonies = [nodes for nodes in instrument_present if nodes > 1]

    harmony_percentage = len(harmonies) / len(instrument_present)

    if harmony_percentage < 0.9:  # often (90 percent) two nodes at the same time
        return False
    else:
        return True


def is_bass(nptrack):
    """ Checks if it only plays on pitch at a time and the average pitch is deep.
    """
    if any(nptrack.sum(axis=1) > 1):
        return False
    elif np.average(np.nonzero(nptrack)[0]) > 47:
        return False  # if the average pitch is below 47, then it may be the bass
    else:
        return True


def encode_lead(array_tracks):  # finds the most likely lead track
    out_array = {'tracks': {}, 'meta': array_tracks['meta']}
    tracks = []
    for channel, track in array_tracks['tracks'].items():
        if is_lead(track):
            tracks.append(channel)

    out_array['tracks'][0] = np.argmax([array_tracks['tracks'][track] for track in tracks])
    out_array['meta']['program'][0] = leadprogram
    return out_array


def encode_harmony(array_tracks):  # combines harmony tracks
    out_array = {'tracks': {}, 'meta': array_tracks['meta']}
    tracks = []
    for channel, track in array_tracks['tracks'].items():
        if is_harmony(track):
            tracks.append(channel)

    out_array['tracks'][1] = sum([array_tracks['tracks'][track] for track in tracks])
    out_array['meta']['program'][1] = harmonyprogram
    return out_array


def encode_bass(array_tracks):  # finds the most likely bass track
    out_array = {'tracks': {}, 'meta': array_tracks['meta']}
    tracks = []
    for channel, track in array_tracks['tracks'].items():
        if is_bass(track):
            tracks.append(channel)

    out_array['tracks'][2] = np.argmax([array_tracks['tracks'][track] for track in tracks])
    out_array['meta']['program'][2] = bassprogram
    return out_array


def encode_drums(array_tracks):  # hopefully finds out if there are multiple drum tracks or not.
    out_array = {'tracks': {}, 'meta': array_tracks['meta']}
    drumtracks = get_drumtracks(array_tracks)
    if len(drumtracks) > 1:
        drumtrack = sum([array_tracks['tracks'][track] for track in drumtracks])

    out_array['tracks'][9] = drumtrack
    out_array['meta']['program'][9] = None

    return out_array


def process_array(array_tracks):
    out_array = {'tracks': {}, 'meta': array_tracks['meta']}
    out_array.append(encode_lead(array_tracks) + encode_harmony(array_tracks) + encode_bass(array_tracks)\
                + encode_drums(array_tracks))
    return out_array


def process_to_file(filename):
    array_tracks = read_np_file(filename)
    out_array = {'tracks': {}, 'meta': array_tracks['meta']}
    out_array.append(encode_lead(array_tracks) + encode_harmony(array_tracks) + encode_bass(array_tracks)\
                + encode_drums(array_tracks))

    np.save(filename, sparse.csr_matrix(out_array))