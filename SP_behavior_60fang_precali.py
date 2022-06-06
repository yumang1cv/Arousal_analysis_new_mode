# -*- coding:utf-8 -*-
# @FileName  :SP_behavior_60fang_precali.py
# @Time      :2022/4/11 16:08
# @Author    :XuYang
# encoding: utf-8
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
import substring

# color_list = sns.color_palette("Spectral", 40)
from typing import List

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
        SP_behavior_analysis
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
    #         name="{}_Movement_Labels".format(item))
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
    #         name="{}_Movement_Labels".format(item))
    #     file_list_2.append(file_list1)
    # file_list_2 = list(np.ravel(file_list_2))
    #
    # behavior_all = []
    # for item in file_list_1:
    #     f = pd.read_csv(item)
    #     """
    #         pandas计算步骤
    #     """
    #     for time in range(0, len(f), 9000):
    #         class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
    #                       9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
    #
    #         for i in range(time, time+9000-1):  # i: start time --> end time
    #             if int(f.iloc[i, 1:2]) not in class_type:
    #                 class_type[int(f.iloc[i, 1:2])] = 0
    #             else:
    #                 class_type[int(f.iloc[i, 1:2])] += 1
    #         # print(class_type)
    #         behavior_fre = list(class_type.values())
    #         behavior_all.append(behavior_fre)
    #         # print(behavior_all)
    #         print('第{}分钟已计算完'.format(time/9000*5))
    # final_list = []
    # for x in range(0, 6):
    #     ten_minute_list = []
    #     for j in range(x, len(behavior_all), 6):
    #         ten_minute_list.append(behavior_all[j])
    #     # ten_minute_array = np.array(ten_minute_list)
    #     # ten_minute_data = pd.DataFrame(ten_minute_array)
    #     final_list.append(ten_minute_list)
    #
    # final_list_array = np.array(final_list).reshape(60*2, 16)
    # final_data = pd.DataFrame(final_list_array)
    # # final_data.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/active_line/Male_active_5min.csv')

    """
        SP_Arousal_analysis
    """
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
                 name="video_info.xlsx", column="looming_time3", state_name="Male_RoRR")  # Male_Wakefulness

    file_list_1 = []
    # for item in a['Video_name'][0:len(a['Video_name'])]:
    for item in a['Video_name'][0:10]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
                 r"/BeAMapping_correct", name="{}_Movement_Labels".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
                 name="video_info.xlsx", column="looming_time3", state_name="Female_RoRR")  # Female_Wakefulness

    file_list_2 = []
    # for item in b['Video_name'][0:len(a['Video_name'])]:
    for item in b['Video_name'][0:10]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
                 r"/BeAMapping_correct", name="{}_Movement_Labels".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    behavior_all = []
    for item in file_list_1:
        f = pd.read_csv(item)
        """
            pandas计算步骤
        """
        for time in range(0, len(f), 9000 * 2):
            class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                          9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}

            for i in range(time, time + 9000 * 2 - 1):  # i: start time --> end time
                if int(f.iloc[i, 1:2]) not in class_type:
                    class_type[int(f.iloc[i, 1:2])] = 0
                else:
                    class_type[int(f.iloc[i, 1:2])] += 1
            # print(class_type)
            behavior_fre = list(class_type.values())
            behavior_all.append(behavior_fre)
            # print(behavior_all)
            print('第{}分钟已计算完'.format(time / 1800))
    final_list = []
    for x in range(0, 6):
        ten_minute_list = []
        for j in range(x, len(behavior_all), 6):
            ten_minute_list.append(behavior_all[j])
        # ten_minute_array = np.array(ten_minute_list)
        # ten_minute_data = pd.DataFrame(ten_minute_array)
        final_list.append(ten_minute_list)

    final_list_array = np.array(final_list).reshape(60, 16)
    final_data = pd.DataFrame(final_list_array)
    row_index = [['0~10min'] * 10, ['11~20min'] * 10, ['21~30min'] * 10,
                 ['31~40min'] * 10, ['41~50min'] * 10, ['51~60min'] * 10]
    row_index = list(np.ravel(row_index))
    final_data.index = [row_index]
    """
        求取behavior_numbers的数量
    """
    behavior_num = list((final_data == 0).astype(int).sum(axis=1))
    behavior_num = (16 - np.array(behavior_num)).tolist()
    final_data['behavior_numbers'] = behavior_num
    final_data.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/SP_behavior'
                      '/SP_Arousal_Male_v2.csv')

    """
        SP behavior wake 行为个数
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
    #         name="{}_Movement_Labels".format(item))
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
    #         name="{}_Movement_Labels".format(item))
    #     file_list_2.append(file_list1)
    # file_list_2 = list(np.ravel(file_list_2))
    #
    # behavior_all = []
    # for item in file_list_1:
    #     f = pd.read_csv(item)
    #     """
    #         pandas计算步骤
    #     """
    #     for time in range(0, len(f), 9000 * 2):
    #         class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
    #                       9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
    #
    #         for i in range(time, time + 9000 * 2 - 1):  # i: start time --> end time
    #             if int(f.iloc[i, 1:2]) not in class_type:
    #                 class_type[int(f.iloc[i, 1:2])] = 0
    #             else:
    #                 class_type[int(f.iloc[i, 1:2])] += 1
    #         # print(class_type)
    #         behavior_fre = list(class_type.values())
    #         behavior_all.append(behavior_fre)
    #         # print(behavior_all)
    #         print('第{}分钟已计算完'.format(time / 1800))
    # final_list = []
    # for x in range(0, 6):
    #     ten_minute_list = []
    #     for j in range(x, len(behavior_all), 6):
    #         ten_minute_list.append(behavior_all[j])
    #     # ten_minute_array = np.array(ten_minute_list)
    #     # ten_minute_data = pd.DataFrame(ten_minute_array)
    #     final_list.append(ten_minute_list)
    #
    # final_list_array = np.array(final_list).reshape(60, 16)
    # final_data = pd.DataFrame(final_list_array)
    # row_index = [['0~10min'] * 10, ['11~20min'] * 10, ['21~30min'] * 10,
    #              ['31~40min'] * 10, ['41~50min'] * 10, ['51~60min'] * 10]
    # row_index = list(np.ravel(row_index))
    # final_data.index = [row_index]
    # """
    #     求取behavior_numbers的数量
    # """
    # behavior_num = list((final_data == 0).astype(int).sum(axis=1))
    # behavior_num = (16 - np.array(behavior_num)).tolist()
    # final_data['behavior_numbers'] = behavior_num
    # final_data.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/SP_behavior'
    #                   '/SP_behavior_Male.csv')

    """
        归一化代码
    """
    # all_value = pd.read_excel('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre'
    #                           '/SP_behavior/SP_Wake_rorr.xlsx')
    # del all_value['Unnamed: 0']
    # all_value2 = (all_value - all_value.min()) / (all_value.max() - all_value.min())  # 归一化代码
    # all_value2.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/SP_behavior'
    #                   '/SP_Wake_rorr_norm.csv')
