# %%
# 徐阳
# 开发时间：2021/9/11 20:01
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import matplotlib

# color_list = sns.color_palette("Spectral", 40)
color_list = ['#845EC2', '#B39CD0', '#D65DB1', '#4FFBDF', '#FFC75F',
              '#D5CABD', '#B0A8B9', '#FF6F91', '#F9F871', '#D7E8F0',
              '#60DB73', '#E8575A', '#008B74', '#00C0A3', '#FF9671',
              '#93DEB1']
"""
    Arousal Behavior Class Combine
    1、Right turning:[1]  (#845EC2)             2、Left turning:[26]  (#B39CD0)
    3、Sniffing:[2, 4, 10, 11, 12, 16, 22, 25]  (#D65DB1)
    4、Walking:[3, 6, 7, 19, 30]  (#4FFBDF)     5、Trembling:[5, 15, 32, 40]  (#FFC75F)
    6、Climbing:[8, 29]   (#D5CABD)             7、Falling:[9]         (#B0A8B9)
    8、Immobility:[13, 20, 33, 34] (#FF6F91)    9、Paralysis:[14, 35]  (#F9F871)
    10、Standing:[17]      (#D7E8F0)            11、Trotting:[18, 31]  (#60DB73)
    12、Grooming:[21]      (#E8575A)            13、Flight:[23, 38]    (#008B74)
    14、Running:[24, 36]   (#00C0A3)            15、LORR:[27, 28, 39]  (#FF9671)
    16、Stepping:[37]      (#93DEB1)
"""


def search_csv(path=".", name=""):  # 抓取csv文件
    result = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            search_csv(item_path, name)
        elif os.path.isfile(item_path):
            if name + ".csv" == item:
                # global csv_result
                # csv_result.append(name)
                result.append(item_path)
                # print(csv_result)
                # print(item_path + ";", end="")
                # result = item
    return result


def read_csv(path='.', name="", column="", element="", state_name=""):
    """
        column[0]: file_name      column[1]:第一次looming时间点
        sheet1：Fwake状态          sheet2：Frorr状态
    """
    item_path = os.path.join(path, name)
    with open(item_path, 'rb') as f:
        csv_data = pd.read_excel(f, sheet_name=state_name)

    # df1 = csv_data.set_index([column])  # 选取某一列数据
    # sel_data = df1.loc[element]  # 根据元素提取特定数据

    return csv_data


def pre_data(file_path, movement_label_num, special_time_start, special_time_end):
    # i = 0
    # special_time_start1 = a['looming_time1'][i] - 5 * 30
    # special_time_end1 = a['looming_time1'][i] + 55 * 30
    # looming_time = a['looming_time1'][i]
    # special_time_start1 = a['looming_time1'][i] - 5 * 30
    # special_time_end1 = a['looming_time1'][i] + 55 * 30

    with open(file_path, 'rb') as f:
        csv_data = pd.read_csv(f)

    label = csv_data.loc[:, 'new_label']
    segBoundary = csv_data.loc[:, 'segBoundary']

    seg_space_list = []
    seg_before_list = []

    # special_time_end = 27000
    # special_time_start = 0
    # movement_label_num = 4
    stop_num, start_num = 0, 0
    for j in range(1, len(segBoundary), 1):
        if segBoundary[j] >= special_time_end > segBoundary[j - 1]:
            stop_num = j

    for k in range(1, len(segBoundary), 1):
        if special_time_start == 0:
            start_num = 0

        elif segBoundary[k] >= special_time_start > segBoundary[k - 1]:
            start_num = k - 1

    for i in range(start_num, stop_num + 1, 1):
        # for i in range(641, 671, 1):
        cur_label = label[i + 1]
        if cur_label == movement_label_num:
            if i == start_num:
                if i == 0:
                    seg_space = segBoundary[i]
                    seg_space_list.append(seg_space)
                    seg_before = 0
                    seg_before_list.append(seg_before)
                else:
                    # print(i)
                    seg_space = segBoundary[i + 1] - special_time_start
                    seg_space_list.append(seg_space)
                    seg_before = special_time_start
                    seg_before_list.append(seg_before)
                    # print(seg_before_list, seg_space_list)

            elif i == stop_num:
                seg_space = special_time_end - segBoundary[i - 1]
                seg_space_list.append(seg_space)

                seg_before = segBoundary[i - 1]
                seg_before_list.append(seg_before)

            else:
                seg_space = segBoundary[i] - segBoundary[i - 1]
                seg_space_list.append(seg_space)

                seg_before = segBoundary[i - 1]
                seg_before_list.append(seg_before)

    # seg_space_list.remove(seg_space_list[1])
    # seg_before_list.remove(seg_before_list[1])

    # seg_before_list.insert(0, seg_before_list[0])

    x_range_list = []

    for i in range(0, len(seg_before_list), 1):
        x_left = seg_before_list[i] - special_time_start
        if x_left < 0:
            # print('========================')
            # print('index: ', i)
            # print('seg_before_list: ', seg_before_list[i])
            # print('special_time_start:', special_time_start)
            # print('=======================')
            x_left = x_broken = 0
        else:
            x_left = seg_before_list[i] - special_time_start
            x_broken = seg_space_list[i]
        # print(x_broken)
        x_range_list.append((x_left, x_broken))

    # seg_before_list.insert(0, seg_before_list[0])

    return x_range_list


def data_combine(file_path, data_1):
    special_time_start1 = data_1 - 5 * 30
    special_time_end1 = data_1 + 120 * 30
    # special_time1 = special_time_start1
    # special_time2 = special_time_end1
    data = []
    for i in range(1, 17):
        behavior = pre_data(file_path, i, special_time_start1, special_time_end1)
        data.append(behavior)
        # print(behavior)
    return data


if __name__ == '__main__':
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all',
                 name="video_info.xlsx", column="looming_time1", state_name="Male_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    for item in a['Video_name'][0:len(a['Video_name'])]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace",
            name="{}_Feature_Space".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all',
                 name="video_info.xlsx", column="looming_time1", state_name="Female_Wakefulness")  # Female_Wakefulness

    file_list_2 = []
    for item in b['Video_name'][0:len(a['Video_name'])]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace",
            name="{}_Feature_Space".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    Male_data = []
    for i in range(0, 5):
        single_data = data_combine(file_list_1[i], a['looming_time1'][i])
        Male_data.append(single_data)
    # single_data = data_combine(file_list_1[0], 0, 25)
    # Male_data.append(single_data)
    # Male_data[1][7].append((0, 150))

    Female_data = []
    for i in range(0, 7):
        single_data = data_combine(file_list_2[i], b['looming_time1'][i])
        Female_data.append(single_data)

    # plt.figure(figsize=(5, 1), dpi=300)
    # fig, ax = plt.subplot()
    fig = plt.figure(figsize=(4, 3), dpi=300)
    ax = fig.add_subplot(111)
    for j in range(len(Male_data)):
        for i in range(len(Male_data[0])):
            plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
            plt.broken_barh(Female_data[j][i], (j + 5, 0.8), facecolors=color_list[i])

    for i in range(len(Female_data[6])):
        plt.broken_barh(Female_data[6][i], (10, 0.8), facecolors=color_list[i])

    plt.axhline(y=4.9, linewidth=1.5, color='black', linestyle='--')
    plt.yticks([2.4, 7.9], ['Males', 'Females'], fontsize=12)
    # plt.xticks([0, 150, 3600], ['-5', '0', '115'], fontsize=12)
    plt.xticks([150, 3750], ['0', '2'], fontsize=12)
    # plt.xticks([9000, 18000], ['0', '5'])
    # plt.xticks([0, 9000, 18000, 27000, 36000, 45000], ['0', '5', '10', '15', '20', '25'])
    plt.tight_layout()
    # plt.axis('off')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(1.5)
    plt.show()
