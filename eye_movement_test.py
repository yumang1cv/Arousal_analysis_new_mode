import time

import numpy as np
import pandas as pd
import seaborn as sns
from scipy.signal import savgol_filter
import os
import matplotlib.pyplot as plt
import datetime


# explicit function to normalize array
# @jit
def normalize(data):
    data_norm = (data - np.min(data)) / (np.max(data) - np.min(data))
    return data_norm


def m_data(file_path):
    # df = pd.read_csv(r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/eye_movement/data/mf4.txt',
    #                  delimiter="\t")
    df1 = pd.read_csv(file_path, delimiter="\t")
    df1['time'] = df1.iloc[:, 0:1]
    df1['looming_label'] = df1.iloc[:, 1:2]
    df1.drop(df1.iloc[:, 0:2], inplace=True, axis=1)
    df1['time1'] = df1['time']

    time_list1 = []
    time_list2 = []

    for item in df1['time1']:
        item = format(item, 'f')
        # print(type(item))
        item = item[:2] + ':' + item[2:4] + ':' + item[4:]
        time_list1.append(item)

    # format the string in the given format :
    # day/month/year hours/minutes/seconds-micro
    # seconds
    format_data = "%H:%M:%S.%f"

    for item1 in time_list1:
        item1 = datetime.datetime.strptime(item1, format_data)
        time_list2.append(item1)
        # print(item1, type(item1))

    df1['time1'] = time_list2

    delay_time = []
    for i in range(1, len(time_list2)):
        t = str(time_list2[i] - time_list2[i - 1])

        t = t[-4:-3]
        # print(t[-4:-2], type(t))
        delay_time.append(t)

    # for item in delay_time:
    #     item = int(item)
    # # delay_time = list(map(int, delay_time))

    delay_time.insert(0, '0')
    df1['delay_time_ms'] = delay_time
    df1['delay_time_ms'] = df1['delay_time_ms'].astype(int)
    fps_num = []
    item1 = 0
    for item in df1['delay_time_ms']:
        item = item * 0.03
        item1 = item + item1
        fps_num.append(item1)

    df1['fps_num'] = fps_num

    # for item, index in df['looming_label']:
    #     if item == 4:
    #         print(item.index)
    # for i in range(len(df['looming_label'])):
    #     if df['looming_label'].iloc[i] == 4:
    #         print(i, df['fps_num'].iloc[i]/30/60)
    fps_num_new = []
    for item in fps_num:
        item = item * 125512 / df1['fps_num'].iloc[-1]
        # print(item)
        fps_num_new.append(item)
    df1['fps_num_new'] = fps_num_new

    return df1


if __name__ == '__main__':
    path = r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/eye_movement/data'
    list_of_files = []

    for root, dirs, files in os.walk(path):
        for file in files:
            list_of_files.append(os.path.join(root, file))

    # pth = 'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/eye_movement' \
    #       '/F1DLC_resnet50_ET_projectApr21shuffle1_1000000.csv '
    df = pd.read_csv(list_of_files[2])
    print(list_of_files[2])

    center = df.iloc[2:, 1:4]
    dict_name = {'DLC_resnet50_ET_projectApr21shuffle1_1000000': 'x',
                 'DLC_resnet50_ET_projectApr21shuffle1_1000000.1': 'y',
                 'DLC_resnet50_ET_projectApr21shuffle1_1000000.2': 'likelihood'}
    center = center.rename(columns=dict_name)

    # center = center.to_string()
    center["x"] = pd.to_numeric(center["x"], downcast="float")
    center["y"] = pd.to_numeric(center["y"], downcast="float")
    center["likelihood"] = pd.to_numeric(center["likelihood"], downcast="float")
    # print(center['x'].mean())
    # print(center['y'].mean())
    # print(center['likelihood'].mean())
    # sns.scatterplot(x="x", y="y", data=center)
    center['x_mean'] = center['x'].mean()
    center['y_mean'] = center['y'].mean()
    # sns.scatterplot(x='x_mean', y='y_mean', data=center)
    # sns.displot(center, x="x", y="y")

    # print(center["x"].iloc[0], center["y"].iloc[0])
    distance_list = []
    for i in range(1, len(center["x"]) - 1):
        distance = np.sqrt(np.sum(np.square(center["x"].iloc[i + 1] - center["x"].iloc[i]) + np.square(
            center["y"].iloc[i + 1] - center["y"].iloc[i])))
        distance_list.append(distance)

    distance_list.insert(0, 0)
    distance_list.insert(len(center["x"]), 0)

    normalized_array_1d = savgol_filter(distance_list, 301, 2)

    normalized_array_1d = normalize(normalized_array_1d)

    center['distance'] = distance_list
    center['distance_norm'] = normalized_array_1d
    center['index'] = [i for i in range(0, len(center["x"]))]
    fig = plt.figure(figsize=(9, 4), dpi=300)
    ax = fig.add_subplot(111)

    sns.lineplot(data=center, x="index", y="distance_norm", color='#7a0855')
    time_tag = [9762.019342318552, 15271.69212198918, 22970.099394424993, 33909.00006151369]
    for item in time_tag:
        plt.axvspan(int(item), int(item + 149.82), color='gray', alpha=0.5, lw=0)

    plt.xlabel('Time (s)', fontsize=15)
    plt.ylabel('Fraction', fontsize=15)
    plt.tight_layout()

    # sns.scatterplot(x="x", y="y", data=center, s=5, color=".15")
    # sns.histplot(x="x", y="y", data=center, bins=100, pthresh=.1, cmap="mako")
    # sns.kdeplot(x="x", y="y", data=center, thresh=.1, color="w", linewidths=1)
    #
    # g = sns.JointGrid(x="x", y="y", data=center, space=0)

    # df = pd.read_csv(r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/eye_movement/data/mf4.txt',
    #                  delimiter="\t")
    # df['time'] = df.iloc[:, 0:1]
    # df['looming_label'] = df.iloc[:, 1:2]
    # df.drop(df.iloc[:, 0:2], inplace=True, axis=1)
    # df['time1'] = df['time']
    #
    # time_list1 = []
    # time_list2 = []
    #
    # for item in df['time1']:
    #     item = format(item, 'f')
    #     # print(type(item))
    #     item = item[:2] + ':' + item[2:4] + ':' + item[4:]
    #     time_list1.append(item)
    #
    # # format the string in the given format :
    # # day/month/year hours/minutes/seconds-micro
    # # seconds
    # format_data = "%H:%M:%S.%f"
    #
    # for item1 in time_list1:
    #     item1 = datetime.datetime.strptime(item1, format_data)
    #     time_list2.append(item1)
    #     # print(item1, type(item1))
    #
    # df['time1'] = time_list2
    #
    # delay_time = []
    # for i in range(1, len(time_list2)):
    #     t = str(time_list2[i] - time_list2[i - 1])
    #
    #     t = t[-4:-3]
    #     # print(t[-4:-2], type(t))
    #     delay_time.append(t)
    #
    # # for item in delay_time:
    # #     item = int(item)
    # # # delay_time = list(map(int, delay_time))
    #
    # delay_time.insert(0, '0')
    # df['delay_time_ms'] = delay_time
    # df['delay_time_ms'] = df['delay_time_ms'].astype(int)
    # fps_num = []
    # item1 = 0
    # for item in df['delay_time_ms']:
    #     item = item * 0.03
    #     item1 = item + item1
    #     fps_num.append(item1)
    #
    # df['fps_num'] = fps_num
    #
    # # for item, index in df['looming_label']:
    # #     if item == 4:
    # #         print(item.index)
    # # for i in range(len(df['looming_label'])):
    # #     if df['looming_label'].iloc[i] == 4:
    # #         print(i, df['fps_num'].iloc[i]/30/60)
    # fps_num_new = []
    # for item in fps_num:
    #     item = item * 159018 / 188274.5400
    #     # print(item)
    #     fps_num_new.append(item)
    # df['fps_num_new'] = fps_num_new
    df = m_data('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/eye_movement/data/mf1.txt')
    looming_time = []
    for i in range(len(df['looming_label'])):
        if df['looming_label'].iloc[i] == 4:
            # print(i, df['fps_num_new'].iloc[i]/30/60)
            print(i, df['fps_num_new'].iloc[i])
            # print(i, df['time1'].iloc[i])
            looming_time.append(df['fps_num_new'].iloc[i])

    for i in range(len(looming_time) - 1):
        if looming_time[i + 1] - looming_time[i] > 100:
            print(looming_time[i])
