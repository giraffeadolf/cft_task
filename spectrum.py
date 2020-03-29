import os
import librosa as lr
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment


def mp3_to_img(file):

    if file[-4:] == '.mp3':
        src = file
        dst = '{}.wav'.format(file[:-4])
        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")
        os.remove(file)
        file = dst

    y, sr = lr.load(file)
    time = np.arange(0, len(y)) / sr

    fig, ax = plt.subplots()
    ax.plot(time, y)
    ax.set(xlabel='Time (s)', ylabel='Sound Amplitude')
    filepath = 'static/images/spectrum.png'
    plt.savefig(filepath)
