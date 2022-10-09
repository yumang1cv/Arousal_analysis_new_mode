# -*- coding:utf-8 -*-
# @FileName  :Arousal_looming_shang.py
# @Time      :2022/10/9 15:17

import numpy as np
import pandas as pd
import os
import seaborn as sns
from sklearn.preprocessing import normalize
from sklearn import preprocessing
import matplotlib
import seaborn as sns

matplotlib.use('Qt5Agg')

color_list = ['#845EC2', '#B39CD0', '#D65DB1', '#4FFBDF', '#FFC75F',
              '#D5CABD', '#B0A8B9', '#FF6F91', '#F9F871', '#D7E8F0',
              '#60DB73', '#E8575A', '#008B74', '#00C0A3', '#FF9671',
              '#93DEB1']
"""
    Arousal Behavior Class Combine-SP behavior 2022.09.23
    2、Running:[23, 24, 38]            3、Trotting:[6, 7, 36]
    4、Walking:[19, 30, 31]            5、Stepping:[10, 18]
    6、Left turning:[26]               7、Right turning:[16]
    8、Rising:[17]                     9、Standing:[29]
    10、Climbing:[8, 9]
    11、Sniffing:[2, 3, 4, 11, 21, 22, 25, 33, 37]
    12、Grooming:[20, 34, 40]          13、Immobility:[1, 12, 13]
    14、LORR:[27, 28, 39]              15、Paralysis:[5]
    16、Twitching:[14, 15, 32, 35]
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


def pre_data(file_path, start_time, end_time):
    fre = 1
    start = start_time * 60 * 30
    end = end_time * 60 * 30
    fre_list = []
    # j = 3
    for j in range(len(file_path)):
        df1 = pd.read_csv(file_path[j])

        data = df1.iloc[start:end, 1:2]
        for i in range(1, len(data)):
            if data.iloc[i, 0] != data.iloc[i - 1, 0]:
                fre = fre + 1
        fre_list.append(fre)
        # print('第{}个文件的熵值为:'.format(j), fre)
        fre = 1

    return fre_list


def pre_looming_data(file_path, dataframe, state=""):  # 计算熵值
    fre = 1
    fre_list = []
    # j = 3
    for j in range(len(file_path)):
        looming_time = int(dataframe.at[j, state])
        df1 = pd.read_csv(file_path[j])

        data = df1.iloc[looming_time - 300 * 30:looming_time + 0 * 30, 1:2]
        for i in range(1, len(data)):
            if data.iloc[i, 0] != data.iloc[i - 1, 0]:
                fre = fre + 1
        fre_list.append(fre)
        # print('第{}个文件的熵值为:'.format(j), fre)
        fre = 1

    return fre_list


def behavior_num(file_path, dataframe, state=""):  # 计算行为种类个数
    behavior_label_num = []
    for j in range(len(file_path)):
        looming_time = int(dataframe.at[j, state])
        df1 = pd.read_csv(file_path[j])

        data = df1.iloc[looming_time - 600 * 30:looming_time + 0 * 30, 1:2]

        class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                      9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
        for line in data.iloc[:, 0]:
            if line not in class_type:
                class_type[line] = 0
            else:
                class_type[line] += 1

        class_type = dict(sorted(class_type.items(), key=lambda item: item[0]))  # sort dict

        t = 0
        for item in class_type:
            if class_type[item] != 0:
                t = t + 1
                # fre_list.append(class_type.keys())
        # x = t
        behavior_label_num.append(t)

    return behavior_label_num


def single_behavior_cal(file_path, dataframe, state=""):  # 计算16个行为的数量
    behavior_label_num = []
    for j in range(len(file_path)):
        looming_time = int(dataframe.at[j, state])
        df1 = pd.read_csv(file_path[j])

        data = df1.iloc[looming_time - 600 * 30:looming_time + 0 * 30, 1:2]

        class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                      9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
        for line in data.iloc[:, 0]:
            if line not in class_type:
                class_type[line] = 0
            else:
                class_type[line] += 1

        class_type = dict(sorted(class_type.items(), key=lambda item: item[0]))  # sort dict
        class_type_value = list(class_type.values())
        behavior_label_num.append(class_type_value)

    return behavior_label_num


def dataframe_norm(input_data):
    x = input_data.values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    norm_data = pd.DataFrame(x_scaled)

    return norm_data


def normalize_2d(matrix):
    norm = np.linalg.norm(matrix)
    matrix = matrix / norm  # normalized matrix
    return matrix


if __name__ == '__main__':

    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_analysis_new/Arousal_result_final/looming_new',
                 name="video_info.xlsx", column="looming_time3", state_name="Male_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    # for item in a['Video_name'][0:len(a['Video_name'])]:
    for item in a['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_analysis_new/Arousal_result_final/looming_new/BeAOutputs/csv_file_output_new",
            name="{}_Movement_Labels".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_analysis_new/Arousal_result_final/looming_new',
                 name="video_info.xlsx", column="looming_time3", state_name="Female_Wakefulness")  # Female_Wakefulness

    file_list_2 = []
    # for item in b['Video_name'][0:len(a['Video_name'])]:
    for item in b['Video_name'][0:6]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_analysis_new/Arousal_result_final/looming_new/BeAOutputs/csv_file_output_new",
            name="{}_Movement_Labels".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    all_shang = []
    for i in range(1, 2):
        Male_list = pre_looming_data(file_list_1, a, state="looming_time{}".format(i))
        Female_list = pre_looming_data(file_list_2, b, state="looming_time{}".format(i))
        # print(Male_list)
        # print(Female_list)
        MFM_list = Male_list + Female_list
        print(MFM_list)
        all_shang.append(MFM_list)
        # MFM_list.clear()
    all_shang_value = pd.DataFrame(all_shang)
    all_shang_value2 = (all_shang_value - all_shang_value.min()) / (all_shang_value.max() - all_shang_value.min())
    # all_shang_value1 = np.array(all_shang_value)
    all_shang_value3 = normalize_2d(all_shang_value)
    all_shang_value3 = pd.DataFrame(all_shang_value3)
    all_shang_value3.set_axis(['Male', 'Male', 'Male', 'Male', 'Male', 'Female', 'Female', 'Female',
                               'Female', 'Female', 'Female'], axis='columns', inplace=True)
    # all_shang_value3.set_axis(['looming time_1', 'looming time_2', 'looming time_3', 'looming time_4'], axis='rows', inplace=True)
    all_shang_value3.set_axis(['looming time_1'], axis='rows', inplace=True)
    # all_shang_value3 = all_shang_value3.multiply(10)
    # sns.heatmap(all_shang_value2)
    all_shang_value.to_csv(r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Analysis\shang/Arousal_looming_wake_shang.csv')




