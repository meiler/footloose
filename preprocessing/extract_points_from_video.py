from keras.models import load_model
from preprocessing.process_video import process
import skvideo.io
import sys
import matplotlib.pyplot as plt
from tqdm import tqdm

model = load_model('paf_testing_model.h5')
movie_path = "../footloose2/footloose/data/video/Jade Chynoweth performs 'Baby One More Time' Choreography by Yanis Marshall _ Filmed by @TimMilgram.mkv"  # sys.argv[1]

movie = skvideo.io.vreader(movie_path)

frame_points = []
for i in tqdm(range(50)):
    print(i)
    img = next(movie)
    frame_points.append(process(img, model))

    # do stuff
    fig = plt.figure()
    plt.imshow(img)
    for points in frame_points[-1]:
        plt.plot(points[:, 0], points[:, 1], 'x')
    plt.axis('off')
    fig.savefig('output_frames/frame_%i.png' % i)
    fig.close()
