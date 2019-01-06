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
    if any(nptrack.sum(axis=1) > 1):
        return False
    elif np.average(np.nonzero(nptrack)[1]) > 47:
        return False  # if the average pitch is below 47, then it may be the bass
    else:
        return True


def encode_test(out_array, array_tracks):
    tracks = []
    tracksum = []
    for channel, track in array_tracks['tracks'].items():
        if is_harmony(track):
            tracks.append(channel)
            tracksum.append(array_tracks['tracks'][channel].sum())

    # sort tracks by values. track[0]=highest value.
    print("tracks: " +str(tracks))
    print("tracksum: " +str(tracksum))
    sorted_tracks = [tracksum for _,tracksum in sorted(zip(tracksum,tracks), reverse=True)]
    print("sorted tracks: " +str(sorted_tracks))

    def returnarray(integer):
        return array_tracks['tracks'][sorted_tracks[integer]]

    # sort tracks by simultaneous notes.
    instrument_present = [nodes for nodes in returnarray(0).sum(axis=1) if nodes > 0]

    # harmonies = [nodes for nodes in instrument_present if nodes > 1]

    # Her er jeg i gang med et wacky projekt der måske forbedrer kombination af tracks.
    # Idéen er at kombinere den bedste med den værste og tjekke for overlap.
    # Hvis der ikke er for meget overlap, gør vi det igen med den næste.
    # Lige nu virker det ikke.
    
    for i in reversed(range(5)):
        harmonies = [nodes for nodes in instrument_present if nodes > i]
        if len(harmonies):
            combined_2tracks = 0
            print("Best candidate for harmony has a peak of " + str(i) + " simultaneous notes.")
            for track in reversed(sorted_tracks[:1]):
                if len(np.intersect1d(returnarray(track),returnarray(0))) < 10:
                    combined_tracks = returnarray(track) + returnarray(0)
                    print("Amount of intersections between best candidate and worst is " + str(len(np.intersect1d(returnarray(track),returnarray(0)))))
                    print("Terminating loop. Peak amount of simultaneous notes is now: " + nodes for nodes in combined_tracks.sum(axis=1))
                    return combined_tracks
                elif len(np.intersect1d(returnarray(track),returnarray(1))) < 10:
                    combined_tracks = returnarray(track) + returnarray(1)
                    print("Amount of intersections between best candidate and second worst is " + str(len(np.intersect1d(returnarray(track),returnarray(1)))))
                    print("Combining best with worst and second worst.")
                    combined_2tracks = combined_tracks + returnarray(0)
                    print("Peak amount of simultaneous notes is now: " + nodes for nodes in combined_2tracks.sum(axis=1))
                    return combined_2tracks
                elif len(np.intersect1d(returnarray(track),returnarray(1))) < 10:
                    combined_2tracks = returnarray(track) + returnarray(1) + returnarray(0)
                    combined_3tracks = combined_2tracks + returnarray(2)
                    print("Amount of intersections between best candidate and second worst is " + str(len(np.intersect1d(combined_2tracks+returnarray(2)))))
                    print("Peak amount of simultaneous notes is now: " + nodes for nodes in combined_3tracks.sum(axis=1))
                    return combined_3tracks


def encode_lead(out_array, array_tracks):  # finds the most likely lead track
    tracks = []
    for channel, track in array_tracks['tracks'].items():
        if is_lead(track):
            tracks.append(channel)

    if tracks:
        best_track = tracks[np.argmax([array_tracks['tracks'][track].sum() for track in tracks])]
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


#def encode_harmony(out_array, array_tracks):  # combines harmony tracks
#    tracks = []
#    for channel, track in array_tracks['tracks'].items():
#        if is_harmony(track):
#            tracks.append(channel)
#
#    if tracks:
#        out_array['tracks'][1] = sum([array_tracks['tracks'][track] for track in tracks])
#        out_array['meta']['program'][1] = harmonyprogram


def encode_bass(out_array, array_tracks):  # finds the most likely bass track
    tracks = []
    for channel, track in array_tracks['tracks'].items():
        if is_bass(track):
            tracks.append(channel)

    if tracks:
        best_track = tracks[np.argmax([array_tracks['tracks'][track].sum() for track in tracks])]
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


def process_to_file(in_file, out_file):
    array_tracks = read_np_file(in_file)
    out_array = process_array(array_tracks)

    out_array['tracks'] = {key: sparse.csr_matrix(value) for (key, value) in out_array['tracks'].items()}
    np.save(out_file, out_array)


def read_np_file(filename):
    np_arrays = np.load(filename).tolist()
    np_arrays['tracks'] = {key: (np.asarray(value.todense()) if isinstance(value, sparse.csr.csr_matrix) else value)
                 for (key, value) in np_arrays['tracks'].items()}

    return np_arrays
