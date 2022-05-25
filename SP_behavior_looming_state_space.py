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

matplotlib.use('Qt5Agg')
# color_list = sns.color_palette("Spectral", 40)
color_list = ['#A86A74', '#CB4042', '#FF6E00', '#EF8C92', '#89BDDE',
              '#FFB67F', '#FFC408', '#937DAD', '#478FB1', '#FFE2CC',
              '#EFB4C5', '#1d953f', '#B34C5A', '#D35889', '#A8DBD9',
              '#EACAC9']

"""
    New color: Arousal Behavior Class Combine
    1、Right turning:[1]  (#A86A74)             2、Left turning:[26]  (#CB4042)
    3、Sniffing:[2, 4, 10, 11, 12, 16, 22, 25]  (#FF6E00)
    4、Walking:[3, 6, 7, 19, 30]  (#EF8C92)     5、Trembling:[5, 15, 32, 40]  (#89BDDE)
    6、Climbing:[8, 29]   (#FFB67F)             7、Falling:[9]         (#FFC408)
    8、Immobility:[13, 20, 33, 34] (#937DAD)    9、Paralysis:[14, 35]  (#478FB1)
    10、Standing:[17]      (#FFE2CC)            11、Trotting:[18, 31]  (#EFB4C5)
    12、Grooming:[21]      (#1d953f)            13、Flight:[23, 38]    (#B34C5A)
    14、Running:[24, 36]   (#D35889)            15、LORR:[27, 28, 39]  (#A8DBD9)
    16、Stepping:[37]      (#EACAC9)
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
    with open(file_path, 'rb') as f:
        csv_data = pd.read_csv(f)

    label = csv_data.loc[:, 'new_label']
    segBoundary = csv_data.loc[:, 'segBoundary']

    seg_space_list = []
    seg_before_list = []

    # special_time_end = 27000
    # special_time_start = 0
    # movement_label_num = 15
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
        if label[i] == movement_label_num:
            if i == start_num:
                if i == 0:
                    seg_space = segBoundary[i]
                    seg_space_list.append(seg_space)
                    seg_before = 0
                    seg_before_list.append(seg_before)
                else:
                    # print(i)
                    seg_space = segBoundary[i] - special_time_start
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
        x_broken = seg_space_list[i]

        if x_left < 0:
            x_broken = seg_space_list[i] + x_left
            x_left = 0
        elif x_broken < 0:
            x_broken = 0
        else:
            x_left = seg_before_list[i] - special_time_start
            x_broken = seg_space_list[i]

        x_range_list.append((x_left, x_broken))

    # seg_before_list.insert(0, seg_before_list[0])

    return x_range_list


def data_combine(file_path, special_time_start, special_time_end):
    # special_time1 = special_time_start * 60 * 30
    # special_time2 = special_time_end * 60 * 30
    special_time1 = special_time_start
    special_time2 = special_time_end
    data = []
    for i in range(1, 17):
        behavior = pre_data(file_path, i, special_time1, special_time2)
        data.append(behavior)
    return data


if __name__ == '__main__':
    # a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all',
    #              name="video_info.xlsx", column="looming_time3", state_name="Male_RoRR")  # Male_Wakefulness
    #
    # file_list_1 = []
    # # for item in a['Video_name'][0:len(a['Video_name'])]:
    # for item in a['Video_name'][0:5]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace",
    #         name="{}_Feature_Space".format(item))
    #     file_list_1.append(file_list1)
    # file_list_1 = list(np.ravel(file_list_1))
    #
    # b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all',
    #              name="video_info.xlsx", column="looming_time3", state_name="Female_RoRR")  # Female_Wakefulness
    #
    # file_list_2 = []
    # # for item in b['Video_name'][0:len(a['Video_name'])]:
    # for item in b['Video_name'][0:6]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace",
    #         name="{}_Feature_Space".format(item))
    #     file_list_2.append(file_list1)
    # file_list_2 = list(np.ravel(file_list_2))
    #
    # time = 2
    #
    # Male_data = []
    # for i in range(0, len(file_list_1)):
    #     # single_data = data_combine(file_list_1[i], 2, 4)
    #     single_data = data_combine(file_list_1[i], a['looming_time{}'.format(time)][i], a['looming_time{}'.format(time)][i]+2* 1800)
    #     Male_data.append(single_data)
    #
    # Female_data = []
    # for i in range(0, len(file_list_2)):
    #     # single_data = data_combine(file_list_2[i], 0, 2)
    #     single_data = data_combine(file_list_2[i], b['looming_time{}'.format(time)][i], b['looming_time{}'.format(time)][i] + 2 * 1800)
    #     Female_data.append(single_data)
    #
    # # plt.figure(figsize=(10, 3), dpi=300)
    # fig = plt.figure(figsize=(5, 3), dpi=300)
    # ax = fig.add_subplot(111)
    # for j in range(len(Male_data)):
    #     for i in range(len(Male_data[0])):
    #         plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
    #         plt.broken_barh(Female_data[j][i], (j + 5, 0.8), facecolors=color_list[i])
    #
    # for i in range(len(Female_data[5])):
    #     plt.broken_barh(Female_data[5][i], (10, 0.8), facecolors=color_list[i])
    #
    # plt.axhline(y=4.9, linewidth=1.5, color='black', linestyle='--')
    # plt.yticks([3, 8], ['Males', 'Females'], fontsize=12, rotation=90)
    # # plt.xticks([0, 18000], ['0', '10'], fontsize=12)
    # plt.xticks([0, 3600], ['0', '2'])
    # # plt.xticks([0, 18000, 36000, 54000, 72000, 90000, 108000], ['0', '10', '20', '30', '40', '50', '60'])
    # plt.tight_layout()
    # # plt.axis('off')
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # for axis in ['top', 'bottom', 'left', 'right']:
    #     ax.spines[axis].set_linewidth(1.5)
    # plt.show()
    #
    # # plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/looming/'
    # #             'Wake_looming{}_V8.tiff'.format(time), dpi=300)
    # plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/looming/'
    #             'RORR_looming{}_V8.tiff'.format(time), dpi=300)
    # plt.close()

    """
        test code
    """

    # file_path = file_list_1[1]
    # special_time_start = a['looming_time{}'.format(1)][0]
    # special_time_end = a['looming_time{}'.format(1)][0] + 2 * 1800
    #
    # all_data = []
    # for movement_label_num in range(0, 16):
    #     # movement_label_num = 10
    #
    #     with open(file_path, 'rb') as f:
    #         csv_data = pd.read_csv(f)
    #
    #     label = csv_data.loc[:, 'new_label']
    #     segBoundary = csv_data.loc[:, 'segBoundary']
    #
    #     seg_space_list = []
    #     seg_before_list = []
    #
    #     # special_time_end = 27000
    #     # special_time_start = 0
    #     # movement_label_num = 15
    #     for j in range(1, len(segBoundary), 1):
    #         if segBoundary[j] >= special_time_end > segBoundary[j - 1]:
    #             stop_num = j
    #
    #     for k in range(1, len(segBoundary), 1):
    #         if special_time_start == 0:
    #             start_num = 0
    #
    #         elif segBoundary[k] >= special_time_start > segBoundary[k - 1]:
    #             start_num = k - 1
    #
    #     for i in range(start_num +1, stop_num + 1, 1):
    #         # for i in range(641, 671, 1):
    #         if label[i] == movement_label_num:
    #             if i == start_num:
    #                 if i == 0:
    #                     seg_space = segBoundary[i]
    #                     seg_space_list.append(seg_space)
    #                     seg_before = 0
    #                     seg_before_list.append(seg_before)
    #                 else:
    #                     # print(i)
    #                     seg_space = segBoundary[i] - special_time_start
    #                     seg_space_list.append(seg_space)
    #                     seg_before = special_time_start
    #                     seg_before_list.append(seg_before)
    #                     # print(seg_before_list, seg_space_list)
    #
    #             elif i == stop_num:
    #                 seg_space = special_time_end - segBoundary[i - 1]
    #                 seg_space_list.append(seg_space)
    #
    #                 seg_before = segBoundary[i - 1]
    #                 seg_before_list.append(seg_before)
    #
    #             else:
    #                 seg_space = segBoundary[i] - segBoundary[i - 1]
    #                 seg_space_list.append(seg_space)
    #
    #                 seg_before = segBoundary[i - 1]
    #                 seg_before_list.append(seg_before)
    #
    #     # seg_space_list.remove(seg_space_list[1])
    #     # seg_before_list.remove(seg_before_list[1])
    #
    #     # seg_before_list.insert(0, seg_before_list[0])
    #     # for i in range(len(seg_before_list)):
    #     #     if seg_before_list[i] < special_time_start:
    #     #         seg_space_list[i] =
    #     #         seg_before_list[i] = special_time_start
    #
    #     x_range_list = []
    #
    #     for i in range(0, len(seg_before_list), 1):
    #         x_left = seg_before_list[i] - special_time_start
    #         x_broken = seg_space_list[i]
    #
    #         if x_left < 0:
    #             x_broken = seg_space_list[i] + x_left
    #             x_left = 0
    #         else:
    #             x_left = seg_before_list[i] - special_time_start
    #             x_broken = seg_space_list[i]
    #
    #         x_range_list.append((x_left, x_broken))
    #
    #     all_data.append(x_range_list)

    """
        单只老鼠使用   
    """
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all',
                     name="video_info.xlsx", column="looming_time3", state_name="Male_RoRR")  # Male_Wakefulness  #  Male_RoRR

    file_list_1 = []
    # for item in a['Video_name'][0:len(a['Video_name'])]:
    for item in a['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace",
            name="{}_Feature_Space".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all',
                 name="video_info.xlsx", column="looming_time3", state_name="Female_RoRR")  # Female_Wakefulness  # Female_RoRR

    file_list_2 = []
    # for item in b['Video_name'][0:len(a['Video_name'])]:
    for item in b['Video_name'][0:6]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace",
            name="{}_Feature_Space".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))
    """
        单只老鼠所有结果
    """
    # Male_data = []
    # single_data = data_combine(file_list_1[4], 0, 25)
    # Male_data.append(single_data)
    #
    # fig = plt.figure(figsize=(12.5, 1), dpi=300)
    # ax = fig.add_subplot(111)
    # for j in range(len(Male_data)):
    #     for i in range(len(Male_data[0])):
    #         plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
    #         # plt.broken_barh(Female_data[j][i], (j + 5, 0.8), facecolors=color_list[i])
    #
    # plt.tight_layout()
    # plt.axis('off')
    #
    # plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/looming/M_15_v2/'
    #             'RORR_all.tiff', transparent=True, dpi=300)
    # plt.close()

    """
        单只老鼠looming后时刻的数据
    """
    mouse_state = "RORR"
    # time = 1
    for time in range(1, 5):
        mouse_num = 4
        Male_data = []
        single_data = data_combine(file_list_1[mouse_num], a['looming_time{}'.format(time)][mouse_num] - 5*30,
                                   a['looming_time{}'.format(time)][mouse_num]+115*30)
        Male_data.append(single_data)

        fig = plt.figure(figsize=(5, 1), dpi=300)
        ax = fig.add_subplot(111)
        for j in range(len(Male_data)):
            for i in range(len(Male_data[0])):
                plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
                # plt.broken_barh(Female_data[j][i], (j + 5, 0.8), facecolors=color_list[i])

        plt.tight_layout()
        plt.axis('off')

        plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/looming/M_15_v2/'
                    '{}_looming_time_{}.tiff'.format(mouse_state, time), transparent=True, dpi=300)
        plt.close()
