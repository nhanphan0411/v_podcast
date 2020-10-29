import numpy as np
import librosa
import librosa.display

import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram
import IPython.display as ipd

import os
import glob
import pathlib

from datetime import datetime
from tqdm import tqdm

import argparse

cmaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples',
         'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd',
         'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn',
         'YlGn', 'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
         'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
         'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr',
         'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr',
         'seismic', 'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
         'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot',
         'afmhot', 'gist_heat', 'copper', 'twilight', 'twilight_shifted', 'hsv',
         'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2',
         'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'flag', 'prism', 'ocean',
         'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
         'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral',
         'gist_ncar']


def visualize_one(path, style, save=False, folder=None, fig_width=15, fig_height=10, dpi=600):
    """ TO PLOT A SPECTROGRAM 
    path: string - direct path to audio file
    style: string - Matplotlib colormap, if 'random', it will be picked randomly
    save: boolean - save output
    folder: string - direct path to output folder
    dpi: int - dot per inch, recommend 300 at minimum 
    """
    x, sr = librosa.load(path)
    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))

    plt.figure(figsize=(fig_width, fig_height))
    if style == 'random':
        i = np.random.randint(98)
        style = cmaps[i]
        print(f'Palette | {style}')
    librosa.display.specshow(Xdb, sr=sr, cmap=style)
    plt.axis('off')

    if save:
        now = datetime.now()
        save_folder = os.path.join(folder, now.date().isoformat())
        try:
            os.mkdir(save_folder)
        except:
            pass

        audio_name = path.split('/')[-1].split('.')[0]
        fname = os.path.join(
            save_folder, f'{now.strftime("%H_%M")}-{audio_name}')
        plt.savefig(fname=fname, dpi=dpi, transparent=True,
                    bbox_inches='tight', pad_inches=0)
        print(f'Image is successfully saved at {fname}.png')

    plt.show()


def visualize_many(path, style, save=False, folder=None, dpi=600):
    """ TO VISUALIZE MANY SPECTROGRAM"""
    p_list = list(pathlib.Path(path).glob('*'))
    for i in tqdm(range(len(p_list))):
        print(str(p_list[i]))
        visualize_one(str(p_list[i]), style=style,
                      save=save, folder=folder, dpi=dpi)


def run_one():
    path = str(input('Enter audio path: \n'))
    style = str(input('Which style should we use? Random for magic. \n'))
    save = str(input('You want to save this spectrogram - True or False? \n'))
    if save:
        folder = str(input('If save, what is the destination folder? \n'))
    fig_width = int(
        input('How big the spectrogram should be in inches - width? \n'))
    fig_height = int(
        input('How big the spectrogram should be in inches - height? \n'))
    dpi = int(input('Dot per inch, minimum of 600. \n'))

    visualize_one(path, style, save, folder, fig_width, fig_height, dpi)


def run_many():
    path = str(input('Enter audio path: \n'))
    style = str(input('Which style should we use? Random for magic. \n'))
    save = str(input('You want to save this spectrogram - True or False? \n'))
    if save:
        folder = str(input('If save, what is the destination folder? \n'))
    fig_width = int(
        input('How big the spectrogram should be in inches - width? \n'))
    fig_height = int(
        input('How big the spectrogram should be in inches - height? \n'))
    dpi = int(input('Dot per inch, minimum of 600. \n'))

    p_list = list(pathlib.Path(path).glob('*'))
    for i in tqdm(range(len(p_list))):
        print(str(p_list[i]))
        visualize_one(str(p_list[i]), style, save,
                      folder, fig_width, fig_height, dpi)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='one', help='one, many')
    args = parser.parse_args()
    if args.mode == 'one':
        run_one()
    elif args.mode == 'many':
        run_many()
    else:
        raise Exception('Unknown --mode')
