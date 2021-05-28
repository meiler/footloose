from preprocessing.instruments import process_to_file
from pathlib import Path
from tqdm import tqdm

files = Path('data/midi_as_npy/')
outfiles = Path('data/midi_as_4_program/')

if not outfiles.is_dir():
    outfiles.mkdir(parents=True)

for file in tqdm(list(files.iterdir())):
    process_to_file(file, outfiles / file.name)
    # try:
    #     pass
    # except KeyboardInterrupt:
    #     raise
    # except (RuntimeError, FileNotFoundError, Exception):
    #     continue
