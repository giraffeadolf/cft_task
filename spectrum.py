import os
import librosa as lr
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment


def mp3_to_img(file):
    dst = 'uploads/{}.wav'.format(file[:-4])
    if file[-4:] == '.mp3':
        src = 'uploads/' + file
        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")
        os.remove(src)

    y, sr = lr.load(dst)
    time = np.arange(0, len(y)) / sr

    fig, ax = plt.subplots()
    ax.plot(time, y)
    ax.set(xlabel='Time (s)', ylabel='Sound Amplitude')
    filepath = 'static/images/{}.png'.format(file[:-4])
    plt.savefig(filepath)
