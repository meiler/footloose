# 4_instruments.py
import numpy as np


def is_bass(track):
    """ Checks if it only plays on pitch at a time and the average pitch is deep.
    """
    if any(track.sum(axis=1) > 1):
        return False
    elif np.average(np.nonzero(track)[0]) > 47:
        return False  # if the average pitch is below 47, then it may be the bass
    else:
        return True


def is_harmony(track):
    """ Checks if it mostly plays several pitch at a time.
    """
    instrument_present = [nodes for nodes in track.sum(axis=1) if nodes > 0]
    harmonies = [nodes for nodes in instrument_present if nodes > 1]

    harmony_percentage = len(harmonies) / len(instrument_present)

    if harmony_percentage < 0.9:  # often (90 percent) two nodes at the same time
        return False
    else:
        return True


def is_lead(track):
    # the lead is mostly 1 pitch at a time
    # and it is above 47 on average
    """ Checks if it mostly plays one pitch at a time and the average pitch is high.
    """
    instrument_present = [nodes for nodes in track.sum(axis=1) if nodes > 0]
    harmonies = [nodes for nodes in instrument_present if nodes > 1]

    harmony_percentage = len(harmonies) / len(instrument_present)

    if harmony_percentage > 0.1:  # often (90 percent) two nodes at the same time
        return False
    elif np.average(np.nonzero(track)[0]) < 47:
        return False
    else:
        return True


def extract_instruments(midi_track):
    # split and apply `and` within instrument groups
    instruments = {}
    for i, track in array_tracks.items():
        if i == 9:  # mido starts at channel 0
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

    return {'drums': drums,
            'bass': bass,
            'harmony': harmony,
            'trumpets': trumpets,
            }
