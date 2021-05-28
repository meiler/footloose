import pytest
from preprocessing.midi_parser import (get_notes,
                                       get_messages,
                                       get_messages_with_note,
                                       get_channel,
                                       convert_to_array,
                                       get_tick_size,
                                       get_total_ticks,
                                       convert_midi_file)
from mido import Message, MidiFile, MidiTrack
import numpy as np

# Fixtures


def note_track():
    # create note track
    track = MidiTrack()

    track.append(Message('program_change', program=12, time=0))
    track.append(Message('note_on', note=64, velocity=69, time=32))
    track.append(Message('note_on', note=64, velocity=0, time=32))
    track.append(Message('note_on', note=68, velocity=69, time=0))
    track.append(Message('note_on', note=68, velocity=0, time=32))

    track.append(Message('note_on', note=64, velocity=69, time=32))
    track.append(Message('note_on', note=68, velocity=69, time=0))
    track.append(Message('note_on', note=64, velocity=0, time=32))
    track.append(Message('note_on', note=68, velocity=0, time=0))

    return track


def midi_file():
    file = MidiFile()
    file.tracks.append(note_track())
    return file


class TestMidiParser(object):
    note_track = note_track()
    midi_file = midi_file()

    def test_get_notes(self):
        # Only note is 64
        assert len(get_notes(self.note_track)) == 1

    def test_get_messages(self):
        messages = get_messages(self.note_track)

        # Check it's a generator
        assert hasattr(messages, '__next__')

        # Check both notes returned
        assert len(list(messages)) == 2

    def test_get_messages_with_note(self):
        # Check doesn't return for missing notes
        no_notes = get_messages_with_note(self.note_track, 11)
        assert len(no_notes) == 0

        # Check returns two messages when there
        with_notes = get_messages_with_note(self.note_track, 64)
        assert len(with_notes) == 2

    def test_get_channel(self):
        assert get_channel(self.note_track) == 0

    def test_convert_to_array(self):
        array = convert_to_array(self.note_track, 16, 4)

        output_array = np.zeros((4, 128))
        output_array[:, 64] = [0, 0, 1, 1]

        np.testing.assert_array_equal(array, output_array)
