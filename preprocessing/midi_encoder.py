#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""midi_parser.py

This converts into numpy tensors into midi file.
The input tensor should contain: time (midi ticks) x pitch (127) x instruments

"""
import numpy as np
import mido
from preprocessing.instruments import is_bass, is_harmony, is_lead, is_drums
from mido import Message, MidiFile, MetaMessage, MidiTrack
from scipy import sparse


def get_off_notes(old_state, new_state):
    return [pos for (pos, state) in enumerate(new_state) if state == 0 and old_state[pos] == 1]


def get_on_notes(old_state, new_state):
    return [pos for (pos, state) in enumerate(new_state) if state == 1 and old_state[pos] == 0]


def turn_off(track, note, time):
    track.append(Message('note_on', note=note, velocity=0, time=time))


def turn_on(track, note, time):
    track.append(Message('note_on', note=note, velocity=100, time=time))


def get_track_from_array(array_track, tick_size=15, instrument=1):
    mid_track = mido.MidiTrack()
    state = np.zeros(128, dtype=np.int8)
    last_event = 0

    for time in range(len(array_track)):
        new_state = array_track[time, :]

        on_notes = get_on_notes(state, new_state)
        off_notes = get_off_notes(state, new_state)

        for note in on_notes:
            delta_time = (time - last_event) * tick_size
            turn_on(mid_track, note, delta_time)
            last_event = time

        for note in off_notes:
            delta_time = (time - last_event) * tick_size
            turn_off(mid_track, note, delta_time)
            last_event = time

        state = new_state

    return mid_track


def convert_tensor_to_midi(array_tracks, suffix, instrument=1):
    mid = MidiFile(type=1)
    track = MidiTrack()
    mid.tracks.append(track)

    # get these right at some point. maybe read from a filename where it should be encoded? split by " - "
    artist = array_tracks[meta][artist]
    title = "one more time"
    tempo = 546000

    # append meta track 0
    mid.tracks[0].append(MetaMessage('midi_port', port=0, time=0))
    mid.tracks[0].append(MetaMessage('track_name', name=artist, time=0))
    mid.tracks[0].append(MetaMessage('track_name', name=title, time=0))
    mid.tracks[0].append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24,
                                     notated_32nd_notes_per_beat=8, time=0))
    mid.tracks[0].append(MetaMessage('set_tempo', tempo=int(tempo), time=0))

    track = 1
    for channel in array_tracks:
        mid_track = get_track_from_array(array_tracks[channel])
        mid.tracks[track].append(MetaMessage('midi_port', port=0, time=0)) # track header

        if instrument == 1:
            if is_lead(mid_track):
                # 57 is trumpet!
                mid.tracks[track].append(Message('program_change', channel=channel, program=57, time=0))
            elif is_bass(mid_track):
                # 34 is bass
                mid.tracks[track].append(Message('program_change', channel=channel, program=34, time=0))
            elif is_harmony(mid_track):
                # 1 is piano
                mid.tracks[track].append(Message('program_change', channel=channel, program=1, time=0))
            elif is_drums(mid_track):
                # channel 9 is always drums. (midi counts channels from 1 but mido counts from 0)
                mid.tracks[track].append(Message('control_change', channel=9, control=10, value=64, time=0))
                # how britney.mid sets drums. I think it's unnecessary. iirc ctrl=10 is pan adjustment, val=64 centers.

        mid.tracks[track].append(mid_track)
        track = track + 1

    mid.save(artist + " " + title + suffix)


def read_np_file(filename):
    np_arrays = np.load(filename)
    np_arrays = {key: (np.asarray(value.todense()) if isinstance(value, sparse.csr.csr_matrix) else value)
                 for (key, value) in np_arrays.tolist().items()}

    return np_arrays
