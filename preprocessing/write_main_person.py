from keras.models import load_model
from preprocessing.process_video import process
import skvideo.io
import numpy as np
from tqdm import tqdm

model = load_model('paf_testing_model.h5')
movie_path = "../footloose2/footloose/data/video/Jade Chynoweth performs 'Baby One More Time' Choreography by Yanis Marshall _ Filmed by @TimMilgram.mkv"  # sys.argv[1]

movie = skvideo.io.vreader(movie_path)

# skip ahead
for i in range(200):
    next(movie)

# save all frames
frame_points = []
for i in tqdm(range(5)):
    next(movie)
    next(movie)
    img = next(movie)
    frame_points.append(process(img, model))

part_str = ['nose', 'neck', 'Rsho', 'Relb', 'Rwri', 'Lsho', 'Lelb', 'Lwri',
            'Rhip', 'Rkne', 'Rank', 'Lhip', 'Lkne', 'Lank', 'Leye', 'Reye',
            'Lear', 'Rear', 'pt19']

# find connection in the specified sequence, center 29 is in the position 15
limbSeq = [[2, 3], [2, 6], [3, 4], [4, 5], [6, 7], [7, 8], [2, 9], [9, 10],
           [10, 11], [2, 12], [12, 13], [13, 14], [2, 1], [1, 15], [15, 17],
           [1, 16], [16, 18], [3, 17], [6, 18]]


def track_person(positions, last_position):
    diffs = []
    for points in positions:
        diffs.append((last_position - points).sum())
    return np.argmin(diffs)


def get_largest_person(positions):
    sizes = []
    for points in positions:
        # remove missing body parts
        points = points[points.sum(axis=1) > 0]

        if len(points) > 0:
            # calc size of bounding box
            minx, miny = np.min(points, axis=0)
            maxx, maxy = np.max(points, axis=0)
            size = (maxx - minx) * (maxy - miny)
            sizes.append(size)
        else:
            sizes.append(0.0)
    return np.argmax(sizes)


def plot_image_with_person(image, position):
    pass


def draw_person(position):
    pass


# for points in frames
    # find largest person - or closest to old location?
    # moved too long since last frame?
    # yes; find next
    # no; continue

# alternative;
# for persons in frame:
#   find most probable new position
#   Make MIDI-like person placement

# normalize person positions to left hip
