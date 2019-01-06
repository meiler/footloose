#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:30:41 2018

@author: william
"""
from keras.layers import Input, Conv2D, BatchNormalization, UpSampling2D, MaxPool2D
from keras.models import Model
import os
from  preprocessing.midi_encoder import read_np_file
import numpy as np

def _down_block(input_tensor, n_filt, filt_size=(4, 18), pool_size=(4, 4)):
    x = Conv2D(n_filt, filt_size, activation='relu', padding='same')(input_tensor)
    x = BatchNormalization()(x)
    x = Conv2D(n_filt, filt_size, activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = MaxPool2D(pool_size=(4, 4))(x)

    return x


def _up_block(input_tensor, n_filt, filt_size=(4, 18), pool_size=(4, 4)):
    x = UpSampling2D(pool_size)(input_tensor)
    x = Conv2D(n_filt, filt_size, activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = Conv2D(n_filt, filt_size, activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    
    return x


input_tensor = Input(shape=(None, 128, 1))

n_filt = 2
pool_size = (4, 4)

encoded = _down_block(input_tensor, n_filt, filt_size=(4, 18), pool_size=(4, 4))
decoded = _up_block(encoded, n_filt, filt_size=(4, 18), pool_size=(4, 4))

decoded = Conv2D(1, (4, 4), activation='sigmoid', padding='same')(decoded)

model = Model(inputs=input_tensor, outputs=decoded)

model.compile(optimizer='adadelta', loss='binary_crossentropy')




# =============================================================================
# Training the model
# =============================================================================


x_train = []

# loads the files
for filename in os.listdir('/Users/william/Projects/footloose/midi_as_np/'):
    song_tracks = read_np_file('/Users/william/Projects/footloose/midi_as_np/'+filename)
    if 9 in song_tracks:
        x_train.append(song_tracks[9])
            
        

x_train_reshaped = []
       
# reshapes the files
for track in x_train:
    shape = track.shape
    if shape[0] < 3000:
        continue
    x_train_reshaped.append(track[:3000, :].reshape(3000,shape[1],1))

x_train_reshaped = np.array(x_train_reshaped)



half = int(len(x_train_reshaped)-4)

train_set = x_train_reshaped[:half]
test_set = x_train_reshaped[half:]

model.fit(train_set, train_set,
                epochs=10,
                batch_size=4,
                shuffle=True,
                steps=2,
                verbose=1,
                validation_data=(test_set, test_set))


# =============================================================================
# What I write to run the code
# 
# =============================================================================
#
#
#britney_track = read_np_file('/Users/william/Projects/footloose/midi_as_np/Britney_Spears_-_Baby_One_More_Time.npy')
#
#
#output_filename = '/Users/william/Projects/footloose/Britney_Spears_-_recontructed6.mid'
#
#convert_tensor_to_midi(britney_track, output_filename)
#
#
#
#
#britney_track2 = britney_track
#
#
#result = model.predict(britney_track[3].reshape(1, 6450, 128,1))
#result = (result>0.5).astype(np.int8)
#
#britney_track2[3] = result.reshape(6448,128)
#
#output_filename = '/Users/william/Projects/footloose/Britney_Spears_-_recontructed6.mid'
#convert_tensor_to_midi(britney_track2, output_filename)