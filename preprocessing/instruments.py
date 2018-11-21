# 4_instruments.py
import numpy as np
import scipy


def is_drums(nptrack):
    # check if this is the last track?
    # or if track is channel 9? Do we even encode this?
    return False


def is_bass(nptrack):
    """ Checks if it only plays on pitch at a time and the average pitch is deep.
    """
    if any(nptrack.sum(axis=1) > 1):
        return False
    elif np.average(np.nonzero(nptrack)[0]) > 47:
        return False  # if the average pitch is below 47, then it may be the bass
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


def extract_instruments(array_tracks):
    # decompress sparse array
    array_tracks = {key: (np.asarray(value.todense()) if isinstance(value, scipy.sparse.csr.csr_matrix) else value)
                 for (key, value) in array_tracks.tolist().items()}

    instruments = {}
    for instrument in array_tracks:

        if is_bass(instrument):
            instruments['bass'].append(instrument)
            break
        elif is_drums(instrument):
            instruments['drums'].append(instrument)
            break
        elif is_harmony(instrument):
            instruments['harmony'].append(instrument)
            break
        elif is_lead(instrument):
            instruments['lead'].append(instrument)
            break

    if len(instruments.keys()) < 4:
        return None

    # harmony should be summed, for everything else we pick the most present channel
    drums = instruments['drum'][np.argmax(map(np.sum, instruments['drum']))]
    bass = instruments['bass'][np.argmax(map(np.sum, instruments['bass']))]
    harmony = sum(instruments['harmony'], np.zeros(instruments['harmony'][0].shape)).astype(np.int8)
    lead = instruments['lead'][np.argmax(map(np.sum, instruments['lead']))]

    return {'drums': drums,
            'bass': bass,
            'harmony': harmony,
            'lead': lead,
            }
