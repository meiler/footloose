from preprocessing.midi_parser import convert_midi_file
from pathlib import Path
from tqdm import tqdm
import numpy as np

files = Path('data/midifiles/')
outfiles = Path('data/midi_as_npy/')

if not outfiles.is_dir():
    outfiles.mkdir(parents=True)

for file in tqdm(list(files.iterdir())):
    try:
        midi_array = convert_midi_file(file)
        if midi_array is not None:
            np.save(outfiles / file.stem, midi_array)
    except KeyboardInterrupt:
        raise
    except (RuntimeError, FileNotFoundError, Exception):
        continue
