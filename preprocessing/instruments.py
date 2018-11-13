# 4_instruments.py


def is_drums(track):


def is_bass(track):
    if any(track.sum(axis=1) > 1):
        return False
    else:
        return True


def is_harmony(track):
    pass


def is_lead(track):
    pass
