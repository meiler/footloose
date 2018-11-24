#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""midi_parser.py

This converts into numpy tensors into midi file.
The input tensor should contain: time (midi ticks) x pitch (127) x instruments

"""
import numpy as np
import mido
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


def set_program(track, channel, program):
    if program is not None:
        track.append(Message('program_change', channel=int(channel), program=int(program), time=0))
    else:
        track.append(Message('program_change', channel=int(channel), time=0))


def get_track_from_array(array_track, tick_size, channel, program):
    mid_track = mido.MidiTrack()
    set_program(mid_track, channel, program)

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


def get_midi_file_header(meta):
    mid_track = mido.MidiTrack()
    mid_track.append(mido.MetaMessage('midi_port', port=0, time=0))
    mid_track.append(mido.MetaMessage('track_name', name='ladebandet', time=0))
    mid_track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4,
                                      clocks_per_click=24, notated_32nd_notes_per_beat=meta['notated_32'],
                                      time=0))
    mid_track.append(mido.MetaMessage('set_tempo', tempo=meta['tempo'], time=0))
    return mid_track


def convert_tensor_to_midi(array_tracks, filename):
    mid = MidiFile()
    tracks = array_tracks['tracks']
    meta = array_tracks['meta']
    tick_size = meta['tick_size']

    mid.tracks.append(get_midi_file_header(meta))

    for channel, track in tracks.items():
        if channel is not None:
            mid_track = get_track_from_array(track, tick_size, channel, meta['program'][channel])
            mid.tracks.append(mid_track)

    mid.save(filename)


def read_np_file(filename):
    np_arrays = np.load(filename)

    np_arrays = np_arrays.tolist()
    np_arrays['tracks'] = {key: np.asarray(value.todense()) for (key, value) in np_arrays['tracks'].items()}

    return np_arrays
