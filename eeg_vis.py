import os
import numpy as np
import mne
from scipy.signal import butter, lfilter
from tqdm import tqdm
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib as mpl
import copy
import matplotlib.colors as mcol
import matplotlib.cm as cm
import numba as nb


def open_data(datapath, file_type):
    file_list = []
    path_list = os.listdir(datapath)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(datapath, filename))

    return file_list


def eeg_fig(file_path, channel_num, Fs, T_start, T_end, Fs_start, Fs_end):
    data = mne.io.read_raw_edf(file_path)
    raw_data = data.get_data()
    # you can get the metadata included in the file and a list of all channels:
    info = data.info
    channels = data.ch_names
    x = raw_data[channel_num, :]

    f, t, Sxx = signal.spectrogram(x, fs=Fs, noverlap=10, nfft=1024, return_onesided=True)

    @nb.jit(nopython=True)
    def for_loop(F_data):

        for i in range(len(F_data[:, 1])):
            for j in range(len(F_data[1, :])):
                F_data[i, j] = 2 * np.log10(F_data[i, j]) + 30

        return F_data

    Sxx = for_loop(Sxx)

    cmap1 = copy.copy(mpl.cm.viridis)
    norm1 = mpl.colors.Normalize(vmin=0, vmax=50)
    im1 = mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1)

    plt.figure(figsize=(14, 4), dpi=300)
    plt.subplot(3, 1, 1)
    # color_camp = plt.cm.get_cmap('Spectral_r')
    color_camp = plt.cm.get_cmap('Paired_r')
    sm = plt.pcolormesh(t[T_start:T_end], f[Fs_start:Fs_end], Sxx[Fs_start:Fs_end, T_start:T_end], shading='gouraud',
                        cmap=color_camp)
    # sm = plt.pcolormesh(t[T_start:T_end], f, Sxx[:, T_start:T_end], shading='gouraud', cmap=color_camp)
    plt.xlabel('Time(s)')
    plt.ylabel('Frequency(Hz)')
    plt.title('{}'.format(channels[channel_num]))
    # plt.colorbar(im1, label='Power(PB)')
    plt.colorbar(label='Power(PB)')
    plt.show()

    return sm


def plot_all(file_path, channel_num, T_start, T_end, Fs_start, Fs_end):
    data = mne.io.read_raw_edf(file_path)
    raw_data = data.get_data()
    # you can get the metadata included in the file and a list of all channels:
    info = data.info
    channels = data.ch_names

    def data_FFT(file_data, num, FS):

        x = file_data[num, :]
        f, t, Sxx = signal.spectrogram(x, fs=FS, noverlap=100, nfft=1024, return_onesided=True)
        for i in tqdm(range(len(Sxx[:, 1]))):
            for j in range(len(Sxx[1, :])):
                Sxx[i, j] = 2 * np.log10(Sxx[i, j]) + 40

        return f, t, Sxx

    f1, t1, Sxx1 = data_FFT(raw_data, 0, 400)
    print("信号记录时长为：{}".format(len(t1)))

    # replace colorbar label
    cmap1 = copy.copy(mpl.cm.viridis)
    norm1 = mpl.colors.Normalize(vmin=0, vmax=100)
    im1 = mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1)

    plt.figure(figsize=(14, 15), dpi=300)

    plt.subplot(3, 1, 1)
    color_camp = plt.cm.get_cmap('jet')
    # colors = ["darkblue", "blue", "mediumblue", "cornflowerblue",
    #           "dodgerblue", "deepskyblue", "skyblue",
    #           "lightskyblue", "lightseagreen","indianred",
    #           "lightcoral", "green", "yellowgreen"
    #           ]
    # cmp = mpl.colors.ListedColormap(colors)
    sm = plt.pcolormesh(t1[T_start:T_end], f1[Fs_start:Fs_end], Sxx1[Fs_start:Fs_end, T_start:T_end], shading='gouraud',
                        cmap=color_camp)
    # sm = plt.pcolormesh(t[T_start:T_end], f, Sxx[:, T_start:T_end], shading='gouraud', cmap=color_camp)

    plt.xlabel('Time(s)')
    plt.ylabel('Frequency(Hz)')
    plt.title('{}'.format(channels[0]))
    # plt.colorbar(im1, label='Power(PB)')
    plt.colorbar(label='Power(PB)')

    plt.subplot(3, 1, 2)

    f2, t2, Sxx2 = data_FFT(raw_data, 1, 400)
    color_camp = plt.cm.get_cmap("jet")
    # color_camp = plt.cm.get_cmap('Accent_r')
    # colors = ["darkblue", "blue", "mediumblue", "cornflowerblue",
    #           "dodgerblue", "deepskyblue", "skyblue",
    #           "lightskyblue", "lightseagreen", "green",
    #           "yellowgreen",  "indianred", "lightcoral"
    #           ]
    # cmp = mpl.colors.ListedColormap(colors)
    sm = plt.pcolormesh(t2[T_start:T_end], f2[Fs_start:Fs_end], Sxx2[Fs_start:Fs_end, T_start:T_end], shading='gouraud',
                        cmap=color_camp)
    # sm = plt.pcolormesh(t[T_start:T_end], f, Sxx[:, T_start:T_end], shading='gouraud', cmap=color_camp)

    plt.xlabel('Time(s)')
    plt.ylabel('Frequency(Hz)')
    plt.title('{}'.format(channels[1]))
    # plt.colorbar(im1, label='Power(PB)')
    plt.colorbar(label='Power(PB)')

    plt.subplot(3, 1, 3)
    f3, t3, Sxx3 = data_FFT(raw_data, 2, 600)

    # color_camp = plt.cm.get_cmap('Paired_r')
    color_camp = plt.cm.get_cmap('jet')
    sm = plt.pcolormesh(t3[T_start:T_end], f3[:], Sxx3[:, T_start:T_end], shading='gouraud',
                        cmap=color_camp)
    # sm = plt.pcolormesh(t[T_start:T_end], f, Sxx[:, T_start:T_end], shading='gouraud', cmap=color_camp)

    plt.xlabel('Time(s)')
    plt.ylabel('Frequency(Hz)')
    plt.title('{}'.format(channels[2]))
    # plt.colorbar(im1, label='Power(PB)')
    plt.colorbar(label='Power(PB)')
    # plt.subplots_adjust(top=0.85)
    # plt.subplots_adjust(left=0.1,
    #                     bottom=0.1,
    #                     right=0.9,
    #                     top=0.9,
    #                     wspace=0.5,
    #                     hspace=0.5)
    plt.subplots_adjust(hspace=0.6)
    plt.show()
    return


if __name__ == '__main__':
    file_list = open_data('D:/3D_behavior/Arousal_behavior/results/eeg/edf/400HZ',
                          '.edf')

    # eeg_fig(file_list[0], 0, 400, 0, 7000, 0, 78)
    # plot_all(file_list[6], 0, 0, 3000, 0, 90)
    data = mne.io.read_raw_edf(file_list[5])

    raw_data = data.get_data()
    # you can get the metadata included in the file and a list of all channels:
    info = data.info
    channels = data.ch_names
    x = raw_data[1, :]

    # f, t, Sxx = signal.spectrogram(x, fs=400, noverlap=100, nfft=2048, return_onesided=True)
    f, t, Sxx = signal.spectrogram(x, fs=400, noverlap=10, nfft=1024, return_onesided=True)


    @nb.jit(nopython=True)
    def for_loop(F_data):

        for i in range(len(F_data[:, 1])):
            for j in range(len(F_data[1, :])):
                F_data[i, j] = 2 * np.log10(F_data[i, j]) + 30

        return F_data


    Sxx = for_loop(Sxx)
    cmap1 = copy.copy(mpl.cm.viridis)
    norm1 = mpl.colors.Normalize(vmin=40, vmax=-20)
    im1 = mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1)

    plt.figure(figsize=(16, 3), dpi=300)
    # color_camp = plt.cm.get_cmap('Spectral_r')
    color_camp = plt.cm.get_cmap("jet")
    # sm = plt.pcolormesh(t[0:60000], f[0:int(len(f)/33)], Sxx[0:int(len(f)/33), 0:60000], shading='gouraud', cmap=color_camp)
    sm = plt.pcolormesh(t[0:8000], f[0:80], Sxx[0:80, 0:8000], shading='gouraud', cmap=color_camp)
    # sm = plt.pcolormesh(t[0:7000], f[0:int(len(f))], Sxx[0:int(len(f)), 0:7000], shading='gouraud',
    #                     cmap=color_camp)
    # sm = plt.pcolormesh(t, fftshift(f), fftshift(Sxx, axes=0), cmap=color_camp)
    plt.xlabel('Time(s)')
    plt.ylabel('Frequency(Hz)')
    plt.title('{}'.format(channels[1]))
    # plt.colorbar(im1, label='Power(PB)')
    plt.colorbar(label='Power(PB)')
    plt.subplots_adjust(bottom=0.2)
    plt.show()
