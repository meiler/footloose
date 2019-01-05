# 4_instruments.py

# manipulates and returns numpy files.

import numpy as np
from scipy import sparse


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

    if len(instrument_present) == 0:
        return False

    else:
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

    if instrument_present and (len(harmonies) / len(instrument_present)) > .9:
        return True
    return False


def is_bass(nptrack):
    """ Checks if it only plays on pitch at a time and the average pitch is deep.
    """
#    if any(nptrack.sum(axis=1) > 1):
#        print("anynptrack.sum fail")
#        return False
    if np.average(np.nonzero(nptrack)[1]) > 47:
        print("npaverage fail")
        print("npaverage was " + str(np.average(np.nonzero(nptrack)[0])))
        return False  # if the average pitch is below 47, then it may be the bass
    else:
        return True


def encode_lead(out_array, array_tracks):  # finds the most likely lead track
    tracks = []
    for channel, track in array_tracks['tracks'].items():
        if is_lead(track):
            tracks.append(channel)

    best_track = np.argmax([array_tracks['tracks'][track].sum() for track in tracks])
    out_array['tracks'][0] = array_tracks['tracks'][best_track]
    out_array['meta']['program'][0] = leadprogram


def encode_harmony(out_array, array_tracks):  # combines harmony tracks
    tracks = []
    for channel, track in array_tracks['tracks'].items():
        if is_harmony(track):
            tracks.append(channel)

    if tracks:
        out_array['tracks'][1] = sum([array_tracks['tracks'][track] for track in tracks])
        out_array['meta']['program'][1] = harmonyprogram


def encode_bass(out_array, array_tracks):  # finds the most likely bass track
    tracks = []
    for channel, track in array_tracks['tracks'].items():
        if is_bass(track):
            tracks.append(channel)

    if tracks:
        best_track = np.argmax([array_tracks['tracks'][track].sum() for track in tracks])
        out_array['tracks'][0] = array_tracks['tracks'][best_track]
        out_array['meta']['program'][2] = bassprogram


def encode_drums(out_array, array_tracks):  # hopefully finds out if there are multiple drum tracks or not.
    drumtracks = get_drumtracks(array_tracks)
    if drumtracks:
        drumtracks = sum([array_tracks['tracks'][track] for track in drumtracks])

        out_array['tracks'][9] = drumtracks
        out_array['meta']['program'][9] = None


def process_array(array_tracks):
    out_array = {'tracks': {}, 'meta': array_tracks['meta']}

    encode_lead(out_array, array_tracks)
    encode_harmony(out_array, array_tracks)
    encode_bass(out_array, array_tracks)
    encode_drums(out_array, array_tracks)

    return out_array


def process_to_file(filename):
    array_tracks = read_np_file(filename)
    out_array = process_array(array_tracks)

    np.save(filename, sparse.csr_matrix(out_array))


def read_np_file(filename):
    np_arrays = np.load(filename)
    np_arrays = {key: (np.asarray(value.todense()) if isinstance(value, sparse.csr.csr_matrix) else value)
                 for (key, value) in np_arrays.tolist().items()}

    return np_arrays