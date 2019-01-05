#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 16:57:24 2019

@author: william
"""


# =============================================================================
# Makes statistical analysis of instrument roles vs. original instrument chosen
# =============================================================================

import instruments as ins
import numpy as np
import matplotlib.pyplot as plt

# example with 1 file

npy_song = ins.read_np_file('/Users/william/Projects/footloose/original/Guns_n_Roses_-_Sweet_Child_O_Mine.npy')

channel_instrument = npy_song['meta']['program']

songtracks = npy_song['tracks']

print(songtracks[None])
print(npy_song)

#def check_instruments(npy_song):
#    for track in song(npy_song):
#        if track is_lead():
#            channel_instrument_dic.append("lead")
#        if track is_bass():
#            dkkada
#        if track is_harmony():
#            dkaod
#        if track is_drums():
#            ofkad

channel_role = {}

for key in songtracks:
#    print(key)
#    print(songtracks[key])
    track = songtracks[key]
    if not (key == None):
        
        if key == 9: #check if drums
            channel_role[key]='drums'
            print(str(key)+'drum')
        elif ins.is_lead(track):
            print(str(key)+'lead')
            channel_role[key]='lead'
        elif ins.is_bass(track):
            print(str(key)+'bass')
            channel_role[key]='bass'
        elif ins.is_harmony(track):
            print(str(key)+'harmony')
            channel_role[key]='harmony'

print(channel_role)

print(channel_instrument)

# plot all


# subtract 1 from table below
#1-8	Piano
#9-16	Chromatic Percussion
#17-24	Organ
#25-32	Guitar
#33-40	Bass
#41-48	Strings
#49-56	Ensemble
#57-64	Brass
#65-72	Reed
#73-80	Pipe
#81-88	Synth Lead
#89-96	Synth Pad
#97-104	Synth Effects
#105-112	Ethnic
#113-120	Percussive
#121-128	Sound Effects




drumtracks = 0
leadtracks = 0
basstracks = 0
harmonytracks = 0

# makes all 4 plots for 1 song (the drums is redundant)
instrument_tags = ('Piano',
    'Chromatic Percussion',
    'Organ',
    'Guitar',
    'Bass',
    'Strings',
    'Ensemble',
    'Brass',
    'Reed',
    'Pipe',
    'Synth Lead',
    'Synth Pad',
    'Synth Effects',
    'Ethnic',
    'Percussive',
    'Sound Effects'
        )
values_harmony = [0 for instrument in instrument_tags]
values_bass = [0 for instrument in instrument_tags]
values_drums = [0 for instrument in instrument_tags]
values_lead = [0 for instrument in instrument_tags]

x = np.arange(len(instrument_tags))

for channel in channel_role:
    print("New instrument")
    print(channel_role[channel])
    instrumentnumber = channel_instrument[channel]
    if not instrumentnumber == 0:
        instrument_cat = int((instrumentnumber)/8)
    else:
        instrument_cat = 0
    
    print(instrumentnumber)
    print(instrument_cat)
    print(instrument_tags[instrument_cat])
    print("bassaxis "+str(any(songtracks[channel].sum(axis=1)>1 )))
    print("bassaverage "+str(np.average(np.nonzero(songtracks[channel])[1])))
    print(ins.is_bass(songtracks[channel]))
    
    if channel_role[channel] == 'bass':
        values_bass[instrument_cat] += 1
        basstracks += 1
        
    elif channel_role[channel] == 'harmony':
        values_harmony[instrument_cat] += 1
        harmonytracks += 1
        
    elif channel_role[channel] == 'drums':
        values_drums[instrument_cat] += 1
        drumtracks += 1

    elif channel_role[channel] == 'lead':
        values_lead[instrument_cat] += 1
        leadtracks += 1


def plot(instrument,values):
    fig, ax = plt.subplots()
    plt.title(instrument)
    plt.bar(x, values)
    
    plt.xticks(x, instrument_tags, rotation='vertical')
    plt.show()


plot('Harmony',values_harmony)
plot('Lead',values_lead)
plot('Drums',values_drums)
plot('Bass',values_bass) #redundant


def is_bass2(nptrack):
    """ Checks if it only plays on pitch at a time and the average pitch is deep.
    """
    if any(nptrack.sum(axis=1) > 1):
        print("anynptrack.sum fail")
        return False
    elif np.average(np.nonzero(nptrack)[1]) > 47:
        print("npaverage fail")
        print("npaverage was " + str(np.average(np.nonzero(nptrack)[0])))
        return False  # if the average pitch is below 47, then it may be the bass
    else:
        return True

###plot number of tracks vs. roles
print("Number of Tracks:" + str(len(channel_instrument)))
print("Number of Lead:" + str(leadtracks))
print("Number of Bass:" + str(basstracks))
print("Number of Harmony:" + str(harmonytracks))
print("Number of Drums:" + str(drumtracks))

# plot best


