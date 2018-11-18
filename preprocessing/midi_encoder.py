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


convert_midi_file('/Users/william/Projects/footloose/Britney_Spears_-_Baby_One_More_Time.mid')


file = mido.MidiFile('/Users/william/Projects/footloose/Britney_Spears_-_Baby_One_More_Time.mid')




from mido import Message
msg = Message('note_on', note=60)
msg







from mido import Message, MidiFile, MidiTrack

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)


track.append(Message('program_change', program=12, time=0))
track.append(Message('note_on', note=64, velocity=64, time=32))
track.append(Message('note_off', note=64, velocity=127, time=32))

mid.save('new_song.mid')


tic_size = get_tick_size('/Users/william/Projects/footloose/Britney_Spears_-_Baby_One_More_Time.mid')

tick_size = 15
program_num = 12

array_tracks = convert_midi_file('/Users/william/Projects/footloose/Britney_Spears_-_Baby_One_More_Time.mid')

def add_track_from_array(instrument, tick_size, track_input):
    track.append(Message('program_change', program=instrument, time=0))
    for note_num in range(0,128):
        last_time = 0
        hold_note = False
        for timestep in range(len(track_input)):
            if track_input[timestep][note_num] == 1:
                if hold_note == False:
                    #start node
                    time = timestep*tick_size-last_time
                    last_time = timestep*tick_size
                    hold_note = True
                    track.append(Message('note_on', note=note_num, velocity=100, time=time))
            else:
                if hold_note == True:
                    #end node
                    time = timestep*tick_size-last_time
                    last_time = timestep*tick_size
                    hold_note = False
                    #adds a message with 0 velocity equivalent to note_off
                    track.append(Message('note_on', note=note_num, velocity=0, time=time))




def convert_tensor_to_midi(array_tracks,filename):
    instrument = 1 #all instruments are piano
    tick_size = 15 # sets the tempo
    
    mid = MidiFile()
    
    for i in range(0,len(array_tracks)-1):
        track = MidiTrack()
        mid.tracks.append(track)
        
        track_input = array_tracks[i]
        add_track_from_array(instrument, tick_size, track_input)
    mid.save(filename)


#get_tick_size('/Users/william/Projects/footloose/Britney_Spears_-_Baby_One_More_Time.mid')




array_tracks = convert_midi_file('/Users/william/Projects/footloose/Britney_Spears_-_Baby_One_More_Time.mid')
filename = '/Users/william/Projects/footloose/Britney_Spears_-_recontructed3.mid'

convert_tensor_to_midi(array_tracks,filename)




for timestep in range(conv[0][0]):
    print(timestep)





from mido import Message, MidiFile, MidiTrack

mid = MidiFile()

track = MidiTrack()
mid.tracks.append(track)


track.append(Message('program_change', program=1, time=0))
track.append(Message('note_on', note=64, velocity=100, time=0))
track.append(Message('note_on', note=64, velocity=0, time=15))

track = MidiTrack()
mid.tracks.append(track)

track.append(Message('note_on', note=1, velocity=100, time=0))
track.append(Message('note_on', note=1, velocity=0, time=15))

track = MidiTrack()
mid.tracks.append(track)

track.append(Message('note_on', note=2, velocity=100, time=0))
track.append(Message('note_on', note=2, velocity=0, time=11))
track.append(Message('note_on', note=2, velocity=100, time=1))
track.append(Message('note_on', note=2, velocity=0, time=1))
track.append(Message('note_on', note=2, velocity=100, time=1))
track.append(Message('note_on', note=2, velocity=0, time=1))

mid.save('new_song3.mid')
















