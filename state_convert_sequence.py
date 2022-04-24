# -*- coding:utf-8 -*-
# @FileName  :state_convert_sequence.py
# @Time      :2022/4/24 10:19
# @Author    :XuYang
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_chord_diagram import chord_diagram
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib

matplotlib.use('Qt5Agg')
sys.path.append(os.path.abspath(".."))

# color_list = ['#845EC2', '#B39CD0', '#D65DB1', '#4FFBDF', '#FFC75F',
#               '#D5CABD', '#B0A8B9', '#FF6F91', '#F9F871', '#D7E8F0',
#               '#60DB73', '#E8575A', '#008B74', '#00C0A3', '#FF9671',
#               '#93DEB1']
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


def pre_data(file_path, dataframe, num, state=""):
    # j = 0
    A = np.zeros((16, 16))

    fre_list = []
    looming_time = int(dataframe.at[num, state])
    start = looming_time - 600 * 30  # 起始时间
    end = looming_time + 0 * 30  # 终止时间

    df2 = pd.read_csv(file_path)

    data = df2.iloc[start:end, 1:2]
    for i in range(1, len(data)):
        if data.iloc[i, 0] != data.iloc[i - 1, 0]:
            a = data.iloc[i, 0] - 1
            b = data.iloc[i - 1, 0] - 1
            A[a, b] = A[a, b] + 1
    # print(A)

    class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                  9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}

    for line in data.iloc[:, 0]:
        if line not in class_type:
            class_type[line] = 0

        else:
            class_type[line] += 1

    class_type = dict(sorted(class_type.items(), key=lambda item: item[0]))  # sort dict
    # print(class_type)
    behavior_fre = list(class_type.values())

    # if behavior_fre.count(0) == 15:
    #     behavior_fre[8] = 50
    #     behavior_fre[14] = 9000 - behavior_fre[8]
    # # print(behavior_fre)

    A = normalize_2d(A)

    behavior_fre_norm = behavior_fre / np.linalg.norm(behavior_fre)
    for j in range(len(behavior_fre_norm)):
        # A[j, j] = behavior_fre_norm[j]
        A[j, j] = 0

    return A


def del_pre_data(data_list):
    del_index = []
    del_data = data_list
    t = 0
    for i in range(len(del_data)):
        if np.any(del_data[:, [i]]) == 0 and np.any(del_data[[i], :]) == 0:
            # print(i, t, i - t)
            del_index.append(i - t)
            t = t + 1

    for item in del_index:
        del_data = np.delete(del_data, item, 1)
        del_data = np.delete(del_data, item, 0)

    names = ['Right turning', 'Left turning', 'Sniffing', 'Walking', 'Trembling', 'Climbing', 'Falling',
             'Immobility', 'Paralysis', 'Standing', 'Trotting', 'Grooming', 'Flight', 'Running', 'LORR', 'Stepping']

    color_list = ['#845EC2', '#B39CD0', '#D65DB1', '#4FFBDF', '#FFC75F',
                  '#D5CABD', '#B0A8B9', '#FF6F91', '#F9F871', '#D7E8F0',
                  '#60DB73', '#E8575A', '#008B74', '#00C0A3', '#FF9671',
                  '#93DEB1']
    for item in del_index:
        del names[item]
        del color_list[item]

    return del_data, names, color_list


# explicit function to normalize array
def normalize_2d(matrix):
    norm = np.linalg.norm(matrix)
    matrix = matrix / norm  # normalized matrix
    return matrix


def getNumofCommonSubstr(str1, str2):
    lstr1 = len(str1)
    lstr2 = len(str2)
    record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]
    # 开辟列表空间 为什么要多一位呢?主要是不多一位的话,会存在边界问题
    # 多了一位以后就不存在超界问题
    maxNum = 0  # 最长匹配长度
    p = 0  # 匹配的起始位

    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
                # 相同则累加
                record[i + 1][j + 1] = record[i][j] + 1
                if record[i + 1][j + 1] > maxNum:
                    # 获取最大匹配长度
                    maxNum = record[i + 1][j + 1]
                    # 记录最大匹配长度的终止位置
                    p = i + 1
                    start1 = i
                    start2 = j
    return str1[p - maxNum:p], maxNum, start1, start2


if __name__ == '__main__':
    """
        SP Arousal wake 60min
    """
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min',
                 name="video_info.xlsx", column="looming_time3", state_name="Male_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    # for item in a['Video_name'][0:len(a['Video_name'])]:
    for item in a['Video_name'][0:10]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min/new_results/BeAMapping-replace",
            name="{}_Feature_Space".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min',
                 name="video_info.xlsx", column="looming_time3", state_name="Female_Wakefulness")  # Female_Wakefulness

    file_list_2 = []
    # for item in b['Video_name'][0:len(a['Video_name'])]:
    for item in b['Video_name'][0:10]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min/new_results/BeAMapping-replace",
            name="{}_Feature_Space".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    movement_label_all = []
    for i in range(len(file_list_2)):
        data_1 = pd.read_csv(file_list_2[i])
        movement_label = data_1['new_label'].to_list()
        movement_label = [str(x) for x in movement_label]
        movement_label = ' '.join(movement_label)
        movement_label_all.append(movement_label)

    for j in range(len(movement_label_all) - 1):
        res = getNumofCommonSubstr(movement_label_all[j], movement_label_all[j + 1])
        print(res)
