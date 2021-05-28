from preprocessing.midi_encoder import convert_tensor_to_midi, read_np_file
from preprocessing.midi_parser import convert_midi_file
import numpy as np

file = convert_midi_file('Britney_Spears_-_Baby_One_More_Time.mid')
np.save('tmp_out', file)

np_arrays = read_np_file('tmp_out.npy')
print('Running conversion:')
convert_tensor_to_midi(np_arrays, 'tmp.mid')
