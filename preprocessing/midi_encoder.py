#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""midi_parser.py

This converts into numpy tensors into midi file.
The input tensor should contain: time (midi ticks) x pitch (127) x instruments

"""
import numpy as np
import mido
#from .instruments import is_bass, is_harmony, is_lead
from preprocessing.midi_parser import convert_midi_file
from mido import Message, MidiFile, MidiTrack


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


def convert_tensor_to_midi(array_tracks, filename):
    mid = MidiFile()

    for channel in array_tracks:
        mid_track = get_track_from_array(array_tracks[channel])
        mid.tracks.append(mid_track)

    mid.save(filename)
