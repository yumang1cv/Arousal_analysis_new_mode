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

color_list = ['#e62600', '#f25832', '#fc7c59', '#ff9e80', '#ffbfa9',
              '#ffdfd3', '#d3afa4', '#e3c9c2', '#ffcc00', '#ffe735',
              '#ff6e00', '#48a36d', '#c574a9', '#4798b3', '#8bb9cc',
              '#c5dce5']

"""
    Arousal Behavior Class Combine-looming 2022.08.06
    1、Flight:[23, 38]   (#e62600)                 2、Running:[6, 24, 36]       (#f25832)
    3、Trotting:[7, 31]  (#fc7c59)                 4、Walking:[10, 18, 19, 30]  (#ff9e80)
    5、Stepping:[37]     (#ffbfa9)                 6、Crawling:[3]              (#ffdfd3)
    7、Left turning:[26] (#d3afa4)                 8、Right turning:[16]        (#e3c9c2)
    9、Standing:[17, 29] (#ffcc00)                 10、Climbing:[8, 9]          (#ffe735)
    11、Sniffing:[2, 4, 11, 12, 13, 22, 25, 40]     (#ff6e00)
    12、Grooming:[21]    (#48a36d)                 13、Immobility:[1, 20, 32, 33, 34]  (#c574a9)
    14、LORR:[28, 39]    (#4798b3)                 15、Paralysis:[14]           (#8bb9cc)
    16、Trembling:[5, 15, 35]   (#c5dce5)
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

    """
        Arousal looming
    """
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_analysis_new/Arousal_looming_new',
                 name="video_info.xlsx", column="looming_time4", state_name="Male_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    # for item in a['Video_name'][0:len(a['Video_name'])]:
    for item in a['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_analysis_new/Arousal_looming_new/results/BeAOutputs/csv_file_output",
            name="{}_Feature_Space".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_analysis_new/Arousal_looming_new',
                 name="video_info.xlsx", column="looming_time4", state_name="Female_Wakefulness")  # Female_Wakefulness

    file_list_2 = []
    # for item in b['Video_name'][0:len(a['Video_name'])]:
    for item in b['Video_name'][0:6]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_analysis_new/Arousal_looming_new/results/BeAOutputs/csv_file_output",
            name="{}_Feature_Space".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    # time = 4
    for time in range(1, 2):

        Male_data = []
        Male_time = []
        for i in range(0, len(file_list_1)):
            # single_data = data_combine(file_list_1[i], 10, 15)
            # print(a['looming_time{}'.format(time)][i] + 0 * 30, a['looming_time{}'.format(time)][i] + 120 * 30)

            single_data = data_combine(file_list_1[i], a['looming_time{}'.format(time)][i],
                                       a['looming_time{}'.format(time)][i] + 120 * 30)
            # single_data = data_combine(file_list_1[i], 0, 108000)

            Male_data.append(single_data)

        Female_data = []
        for i in range(0, len(file_list_2)):
            # single_data = data_combine(file_list_2[i], 10, 15)
            # single_data = data_combine(file_list_2[i], 0, 108000)
            single_data = data_combine(file_list_2[i], b['looming_time{}'.format(time)][i],
                                       b['looming_time{}'.format(time)][i] + 120 * 30)
            # single_data = data_combine(file_list_2[i], 6618, 6618 + 2 * 1800)
            Female_data.append(single_data)

        # plt.figure(figsize=(10, 3), dpi=300)
        fig = plt.figure(figsize=(4, 3), dpi=300)
        ax = fig.add_subplot(111)
        for j in range(len(Male_data)):
            for i in range(len(Female_data[0])):
                plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
                plt.broken_barh(Female_data[j][i], (j + 5, 0.8), facecolors=color_list[i])

        for i in range(len(Female_data[5])):
            plt.broken_barh(Female_data[5][i], (10, 0.8), facecolors=color_list[i])

        plt.axhline(y=4.9, linewidth=1.5, color='black', linestyle='--')
        plt.yticks([2.5, 7.5], ['Males', 'Females'], fontsize=12, rotation=90)
        # plt.xticks([0, 18000], ['0', '10'], fontsize=12)
        plt.xticks([0, 3600], ['0', '2'])
        # plt.xticks([0, 18000, 36000, 54000, 72000, 90000, 108000], ['0', '10', '20', '30', '40', '50', '60'])
        plt.tight_layout()
        # plt.axis('off')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(1.5)
        plt.show()
        plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_analysis_new/Analysis/state_space/looming_Wakefulness_stage_{'
                    '}_v22.tiff'.format(time), dpi=300)

        plt.close()

    """
        SP_Arousal behavior wake: 10min  RORR:60min
    """
    # a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
    #              name="video_info.xlsx", column="looming_time3", state_name="Male_RoRR")  # Male_Wakefulness
    #
    # file_list_1 = []
    # # for item in a['Video_name'][0:len(a['Video_name'])]:
    # for item in a['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2/BeAMapping_correct",
    #         name="{}_Feature_Space".format(item))
    #     file_list_1.append(file_list1)
    # file_list_1 = list(np.ravel(file_list_1))
    #
    # b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
    #              name="video_info.xlsx", column="looming_time3", state_name="Female_RoRR")  # Female_Wakefulness
    #
    # file_list_2 = []
    # # for item in b['Video_name'][0:len(a['Video_name'])]:
    # for item in b['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2/BeAMapping_correct",
    #         name="{}_Feature_Space".format(item))
    #     file_list_2.append(file_list1)
    # file_list_2 = list(np.ravel(file_list_2))
    #
    # # time = 4
    # # for time in range(1, 2):
    #
    # Male_data = []
    # Male_time = []
    # for i in range(0, len(file_list_1)):
    #     single_data = data_combine(file_list_1[i], 0, 60)
    #     # single_data = data_combine(file_list_1[i], a['looming_time{}'.format(time)][i],
    #     #                            a['looming_time{}'.format(time)][i] + 2 * 1800)
    #     # single_data = data_combine(file_list_1[i], 0, 107900)
    #     Male_data.append(single_data)
    #
    # Female_data = []
    # for i in range(0, len(file_list_2)):
    #     single_data = data_combine(file_list_2[i], 0, 60)
    #     # single_data = data_combine(file_list_2[i], 0, 107900)
    #     # single_data = data_combine(file_list_2[i], 6618, 6618 + 2 * 1800)
    #     Female_data.append(single_data)
    #
    # # plt.figure(figsize=(10, 3), dpi=300)
    # fig = plt.figure(figsize=(24, 6), dpi=300)
    # ax = fig.add_subplot(111)
    # for j in range(len(Male_data)):
    #     for i in range(len(Male_data[0])):
    #         plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
    #         plt.broken_barh(Female_data[j][i], (j + 10, 0.8), facecolors=color_list[i])
    #
    # # for i in range(len(Female_data[5])):
    # #     plt.broken_barh(Female_data[5][i], (10, 0.8), facecolors=color_list[i])
    #
    # plt.axhline(y=9.9, linewidth=2.5, color='black', linestyle='--')
    # plt.yticks([5, 15], ['Males', 'Females'], fontsize=12, rotation=90)
    # # plt.xticks([0, 18000], ['0', '10'], fontsize=12)
    # # plt.xticks([0, 3600], ['0', '2'])
    # plt.xticks([0, 18000, 36000, 54000, 72000, 90000, 108000], ['0', '10', '20', '30', '40', '50', '60'])
    # plt.tight_layout()
    # # plt.axis('off')
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # for axis in ['top', 'bottom', 'left', 'right']:
    #     ax.spines[axis].set_linewidth(1.5)
    # plt.show()
    # # plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/SP_Arousal_add_60'
    # #             '/RoRR_all_V2.tiff', dpi=300)
    # # plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/State_space_normal'
    # #             '/Wakefulness_{}_v5.tiff'.format(time), dpi=300)
    # plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/SP_Arousal_add_60'
    #             '/RORR_all_v11.tiff', dpi=300)
    # plt.close()

    """
        SP behavior wake: 60min  
    """
    # a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min',
    #              name="video_info.xlsx", column="looming_time3", state_name="Male_Wakefulness")  # Male_Wakefulness
    #
    # file_list_1 = []
    # # for item in a['Video_name'][0:len(a['Video_name'])]:
    # for item in a['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min/new_results/BeAMapping-replace",
    #         name="{}_Feature_Space".format(item))
    #     file_list_1.append(file_list1)
    # file_list_1 = list(np.ravel(file_list_1))
    #
    # b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min',
    #              name="video_info.xlsx", column="looming_time3", state_name="Female_Wakefulness")  # Female_Wakefulness
    #
    # file_list_2 = []
    # # for item in b['Video_name'][0:len(a['Video_name'])]:
    # for item in b['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min/new_results/BeAMapping-replace",
    #         name="{}_Feature_Space".format(item))
    #     file_list_2.append(file_list1)
    # file_list_2 = list(np.ravel(file_list_2))
    #
    # # time = 4
    # Male_data = []
    # Male_time = []
    # for i in range(0, len(file_list_1)):
    #     # single_data = data_combine(file_list_1[i], 10, 15)
    #     single_data = data_combine(file_list_1[i], 0, 108000)
    #     Male_data.append(single_data)
    #
    # Female_data = []
    # for i in range(0, len(file_list_2)):
    #     # single_data = data_combine(file_list_2[i], 10, 15)
    #     single_data = data_combine(file_list_2[i], 0, 108000)
    #     # single_data = data_combine(file_list_2[i], 6618, 6618 + 2 * 1800)
    #     Female_data.append(single_data)
    #
    # # plt.figure(figsize=(10, 3), dpi=300)
    # fig = plt.figure(figsize=(24, 6), dpi=300)
    # ax = fig.add_subplot(111)
    # for j in range(len(Male_data)):
    #     for i in range(len(Male_data[0])):
    #         plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
    #         plt.broken_barh(Female_data[j][i], (j + 10, 0.8), facecolors=color_list[i])
    #
    # # for i in range(len(Female_data[5])):
    # #     plt.broken_barh(Female_data[5][i], (10, 0.8), facecolors=color_list[i])
    #
    # plt.axhline(y=9.9, linewidth=2.5, color='black', linestyle='--')
    # plt.yticks([5, 15], ['Males', 'Females'], fontsize=12, rotation=90)
    # # plt.xticks([0, 18000], ['0', '10'], fontsize=12)
    # # plt.xticks([0, 3600], ['0', '2'])
    # plt.xticks([0, 18000, 36000, 54000, 72000, 90000, 108000], ['0', '10', '20', '30', '40', '50', '60'])
    # plt.tight_layout()
    # # plt.axis('off')
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # for axis in ['top', 'bottom', 'left', 'right']:
    #     ax.spines[axis].set_linewidth(1.5)
    # plt.show()
    # # plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/SP_Arousal_add_60'
    # #             '/RoRR_all_V2.tiff', dpi=300)
    # plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/SP_behavior_60min/'
    #             'SP_behavior_60min_test_V8.tiff', dpi=300)
    # plt.close()

    """
        单只老鼠使用
    """
    # # single_data = data_combine(file_list_1[0], 0, 25)
    # # Male_data.append(single_data)
    # # x = 5
    # for x in range(0, 60, 5):
    #     Female_data = []
    #     # for i in range(0, 10):
    #     #     single_data = data_combine(file_list_2[i], 0, 5)
    #     #     Female_data.append(single_data)
    #     single_data = data_combine(file_list_1[1], x, x+5)
    #     Female_data.append(single_data)
    #     # Female_data = single_data
    #     #
    #     # # plt.figure(figsize=(5, 1), dpi=300)
    #     # fig, ax = plt.subplot()
    #     fig = plt.figure(figsize=(4, 1), dpi=300)
    #     ax = fig.add_subplot(111)
    #     for j in range(len(Female_data)):
    #         for i in range(len(Female_data[0])):
    #             # plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
    #             plt.broken_barh(Female_data[j][i], (j + 10, 0.8), facecolors=color_list[i])
    #
    #     # for i in range(len(Female_data[6])):
    #     #     plt.broken_barh(Female_data[6][i], (12, 0.8), facecolors=color_list[i])
    #
    #     # plt.axhline(y=9.9, linewidth=1.5, color='black', linestyle='--')
    #     # plt.yticks([5, 15], ['Males', 'Females'], fontsize=12, rotation=90)
    #     plt.xticks([0, 18000], ['0', '10'], fontsize=12)
    #     # plt.xticks([9000, 18000], ['0', '5'])
    #     # plt.xticks([0, 18000, 36000, 54000, 72000, 90000, 108000], ['0', '10', '20', '30', '40', '50', '60'])
    #     plt.tight_layout()
    #     plt.axis('off')
    #     ax.spines['right'].set_visible(False)
    #     ax.spines['top'].set_visible(False)
    #     for axis in ['top', 'bottom', 'left', 'right']:
    #         ax.spines[axis].set_linewidth(1.5)
    #     plt.show()
    #     # plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/SP_Arousal_2'
    #     #             '/F2_RoRR_{}.tiff'.format((x+5)/5), dpi=300)
    #     # plt.close()
    #     # Female_data = []
