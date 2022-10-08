# -*- coding:utf-8 -*-
# @FileName  :State_convert_looming.py
# @Time      :2022/5/23 16:33
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

behavior_dict = {
    'flight': '#f25832',
    'Running': '#cd5c5c',
    'Trotting': '#fc7c59',
    'Walking': '#ff9e80',
    'Stepping': '#ffbfa9',
    'Left turning': '#d3afa4',
    'Right turning': '#e3c9c2',
    'Rising': '#f4a460',
    'Standing': '#ffcc00',
    'Climbing': '#ffe735',
    'Sniffing': '#ff6e00',
    'Grooming': '#48a36d',
    'Immobility': '#c896c8',
    'LORR': '#4798b3',
    'Paralysis': '#8bb9cc',
    'Twitching': '#c5dce5'
}

color_list = list(behavior_dict.values())
movement_names = list(behavior_dict.keys())


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
    start = looming_time - 0 * 30  # 起始时间
    end = looming_time + 120 * 30  # 终止时间

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

    # A = normalize_2d(A)

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

    names = movement_names

    # color_list = ['#845EC2', '#B39CD0', '#D65DB1', '#4FFBDF', '#FFC75F',
    #               '#D5CABD', '#B0A8B9', '#FF6F91', '#F9F871', '#D7E8F0',
    #               '#60DB73', '#E8575A', '#008B74', '#00C0A3', '#FF9671',
    #               '#93DEB1']

    color_list_1 = color_list

    for item in del_index:
        del names[item]
        del color_list_1[item]

    return del_data, names, color_list_1


# explicit function to normalize array
def normalize_2d(matrix):
    norm = np.linalg.norm(matrix)
    matrix = matrix / norm  # normalized matrix
    return matrix


if __name__ == '__main__':
    """
        looming arousal 2min
    """
    mouse_state = 'Wakefulness'
    a = read_csv(path=r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new',
                 name="video_info.xlsx", column="looming_time4",
                 state_name="Male_{}".format(mouse_state))  # Male_Wakefulness

    file_list_1 = []
    # for item in a['Video_name'][0:len(a['Video_name'])]:
    for item in a['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new\BeAOutputs\csv_file_output_new",
            name="{}_Movement_Labels".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new',
                 name="video_info.xlsx", column="looming_time4",
                 state_name="Female_{}".format(mouse_state))  # Female_Wakefulness

    file_list_2 = []
    # for item in b['Video_name'][0:len(a['Video_name'])]:
    for item in b['Video_name'][0:6]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new\BeAOutputs\csv_file_output_new",
            name="{}_Movement_Labels".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    """
        Wake状态 所有老鼠数据
    """
    # behavior_label = ['Right turning', 'Left turning', 'Sniffing', 'Walking', 'Trembling', 'Climbing', 'Falling',
    #                   'Immobility', 'Paralysis', 'Standing', 'Trotting', 'Grooming', 'Flight', 'Running', 'LORR',
    #                   'Stepping']
    file_list = file_list_2
    dataframe = b
    # mouse_state = 'RORR'
    looming_time = 4
    Male_data = np.zeros((16, 16))
    Female_data = np.zeros((16, 16))
    for x in range(1, looming_time+1, 1):  # 调整间隔时长：5min/10min
        # for x in range(1, 2):
        state = "looming_time{}".format(x)
        for num in range(len(file_list)):  # 访问老鼠个体
            # for num in range(2, 3):
            # sub_list2 = pre_data(file_list_2[0], b, 0, state="looming_time2")
            sub_list1 = pre_data(file_list[num], dataframe, num, state=state)
            # print(sub_list1)
            # data = Male_data + Female_data
            Male_data = Male_data + sub_list1

        for num in range(len(file_list_1)):  # 访问老鼠个体
            # for num in range(2, 3):
            # sub_list2 = pre_data(file_list_2[0], b, 0, state="looming_time2")
            sub_list2 = pre_data(file_list_1[num], a, num, state=state)
            # print(sub_list2)
            # data = Male_data + Female_data
            Female_data = Female_data + sub_list2

        all_data = Male_data + Female_data

        del_data, names, colors = del_pre_data(all_data)
        all_data = np.zeros((16, 16))
        color = ListedColormap(colors)
        fig = plt.figure(figsize=(5, 5), dpi=300)
        ax = fig.add_subplot(111)
        # chord_diagram(flux, names, gap=0.03, use_gradient=True, sort='distance', cmap=color,
        #               chord_colors=colors,
        #               rotate_names=True, fontcolor="grey", ax=ax, fontsize=10)
        chord_diagram(del_data, gap=0.03, use_gradient=True, sort='distance', cmap=color,
                      chord_colors=colors, fontcolor="grey", ax=ax, fontsize=10)

        # str_grd = "_gradient" if grads[0] else ""
        plt.xlabel('Time (s)', fontsize=15)
        plt.ylabel('Fraction', fontsize=15)
        plt.tight_layout()
        plt.show()
        plt.savefig(r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Analysis\state_convert\looming'
                    '/All_looming_{}{}_2min_v23.tiff'.format(mouse_state, int(x)), dpi=300)
        plt.close()
