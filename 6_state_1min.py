# encoding: utf-8
import os
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import substring
from tqdm import tqdm
import seaborn as sns

"""
    Exploratory behavior:{1、Running, 2、Right turning, 3、Left turning, 4、Walking, 5、Trotting,
    7、Sniffing, 14、Stepping}
    Prison break behavior:{6、Rearing, 11、Hunching, 13、Jumping}
    Inactive behavior:{8、Grooming, 9、Diving, 10、Rising, 12、Falling}  
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


def open_data(datapath, file_type):
    file_list = []
    path_list = os.listdir(datapath)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(datapath, filename))

    return file_list


def read_csv(path='.', name="", column="", element=""):
    """
    Unique_serial_number:1,2,...,438          date:20210916
    mouse:#13                                 gender:female/male
    ExperimentTime:day/night                  origin_seg:1,2,3
    re_seg_Index:1,2,...,73                   split_number:1,2,...,6
    coordinate_file:calibrationimages_XY20210916_1
    """
    item_path = os.path.join(path, name)
    with open(item_path, 'rb') as f:
        df = pd.read_excel(f)

    df1 = df.set_index([column])  # 选取某一列数据
    sel_data = df1.loc[element]  # 根据元素提取特定数据

    return sel_data


def choose_data(dataframe, column="", element=""):
    df = dataframe.loc[dataframe[column].isin([element])]  # 限定条件挑选数据(二次限定使用)

    return df


def read_single_file(sub_file_path):
    """
    read single file to dict
    """
    class_type = {}
    with open(sub_file_path) as f:  # read single file to dict
        reader = f
        for line in reader:
            line = substring.substringByChar(line, startChar=",")
            line = line[1:]
            line = line.strip('\n')
            # sorted(class_type.keys())
            if line not in class_type:
                class_type[str(line)] = 0

            else:
                class_type[str(line)] += 1
        # print("Original dict", class_type)

        class_type_int = {int(k): int(v) for k, v in class_type.items()}  # data str to int
        class_type_sorted = dict(sorted(class_type_int.items(), key=lambda item: item[0]))  # sort dict
        # print("After sorted dict:", class_type_sorted)

    return class_type_sorted


def read_several_file(file_path):  # several file variance analysis
    """
    Statistics several file data to one dict
    """
    class_fre = []
    for file in file_path:
        class_frequency = read_single_file(file)
        class_fre.append(class_frequency)
        # print("总共有   ", len(class_frequency), "  个类别")

    class_fre_result = defaultdict(list)
    for element in class_fre:
        for key, value in element.items():
            class_fre_result[key].append(value)

    class_fre_result_sorted = dict(sorted(class_fre_result.items(), key=lambda item: item[0]))  # sort dict

    print(class_fre_result_sorted)

    return class_fre_result_sorted


def several_file_sum(sev_file_dict):  # several file mean analysis
    """
    Sum dict all value and normalization
    """
    for key in sev_file_dict:  # sum
        sev_file_dict[key] = sum(sev_file_dict[key])

    factor = 1.0 / sum(sev_file_dict.values())  # normalization
    for k in sev_file_dict:
        sev_file_dict[k] = sev_file_dict[k] * factor

    # print(sev_file_dict)
    print('\n')

    return sev_file_dict


def state1to6(dou_choose_data, spilt_number):
    state = choose_data(dou_choose_data, column='split_number', element=spilt_number)
    df_MD = pd.DataFrame(state, columns=["Unique_serial_number"])
    csv_MD = []
    for item in tqdm(df_MD['Unique_serial_number']):
        csv_result2 = search_csv(
            path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\",
            name="rec-{}-G1-2021114230_Movement_Labels".format(item))
        csv_MD.append(csv_result2[0])

    csv_MD = read_several_file(csv_MD)
    state_result_nor = several_file_sum(csv_MD)

    return state_result_nor


def bar_plot(dict_a, dict_b):
    labels = ['Running', 'Right turning', 'Left turning', 'Walking',
              'Trotting', 'Rearing', 'Sniffing', 'Grooming', 'Diving',
              'Rising', 'Hunching', 'Falling', 'Jumping', 'Stepping']
    key = np.arange(1, 15)
    a_value_list = dict_a.values()
    b_value_list = dict_b.values()
    # width = [2 for _ in range(40)]

    plt.figure(figsize=(15, 13), dpi=300)
    plt.bar(key + 0.15, a_value_list, width=0.3, color='lightpink', align='center')
    plt.bar(key - 0.15, b_value_list, width=0.3, color='#AFEEEE', align='center')
    plt.legend(('Female', 'Male'), fontsize=15)
    plt.xticks(key, labels, fontsize=15, rotation=70)
    plt.yticks(fontsize=15)
    plt.title("Male and female in AM difference", fontsize=15)
    plt.subplots_adjust(bottom=0.3)
    plt.show()

    return


def histogram_intersection(a, b):
    v = np.minimum(a, b).sum().round(decimals=1)
    return v


if __name__ == '__main__':
    a = read_csv(path=r'D:\\3D_behavior\\Spontaneous_behavior\\result',
                 name="video_info.xlsx", column="gender", element="male")

    # 多条件筛选
    x = choose_data(a, column='ExperimentTime', element='night')
    df_day = pd.DataFrame(x, columns=["Unique_serial_number"])
    # data = df_day.values.tolist()
    csv_FD = []
    for item in tqdm(df_day['Unique_serial_number']):
        csv_result1 = search_csv(
            path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\",
            name="rec-{}-G1-2021114230_Movement_Labels".format(item))
        csv_FD.append(csv_result1[0])

    class_type = {}
    # key_list = [i for i in range(1, 15)]
    # value = 0
    # for i in key_list:
    #     class_type[i] = value

    df = pd.read_csv(csv_FD[0])
    # print(df.iloc[0:1800, 1:])
    df1 = df.iloc[0:1800, 1:]
    for item in df1:
        if item not in class_type:
            class_type[str(item)] = 0

        else:
            class_type[str(item)] += 1
        print("Original dict", class_type)
    # femaleDay_result = read_several_file(csv_FD[0])
    # femaleDay_result_nor = several_file_sum(femaleDay_result)
    # # state_1 = state1to6(x, 1)
    # # state_2 = state1to6(x, 2)
    # state_result = []
    # for i in range(1, 7, 1):
    #     print("第{}0分钟的状态为".format(i))
    #     state = state1to6(x, i)
    #     state_result.append(state)
    #
    # state_1 = pd.DataFrame(state_result)
    # # bar_plot(state_result[0], state_result[1])
    # name_list = ['Running', 'Right turning', 'Left turning', 'Walking',
    #              'Trotting', 'Rearing', 'Sniffing', 'Grooming', 'Diving',
    #              'Rising', 'Hunching', 'Falling', 'Jumping', 'Stepping']
    # # state_1.index.names = ['Running', 'Right turning', 'Left turning', 'Walking',
    # #                        'Trotting', 'Rearing', 'Sniffing', 'Grooming', 'Diving',
    # #                        'Rising', 'Hunching', 'Falling', 'Jumping', 'Stepping']
    # for i in range(len(name_list)):
    #     state_1 = state_1.rename(columns={state_1.columns[i]: name_list[i]})
    #
    # state_1.insert(5, 'Sniffing', state_1.pop('Sniffing'))
    # state_1.insert(6, 'Stepping', state_1.pop('Stepping'))
    # state_1.insert(8, 'Hunching', state_1.pop('Hunching'))
    # state_1.insert(9, 'Jumping', state_1.pop('Jumping'))
    # state_1.insert(10, 'Grooming', state_1.pop('Grooming'))
    #
    # # state_1.plot(kind='bar', stacked=True, figsize=(15, 8))
    #
    # name_list2 = ['Exploratory behavior', 'Exploratory behavior', 'Exploratory behavior',
    #               'Exploratory behavior', 'Exploratory behavior', 'Exploratory behavior',
    #               'Exploratory behavior', 'Prison break behavior', 'Prison break behavior',
    #               'Prison break behavior', 'Inactivate behavior', 'Inactivate behavior',
    #               'Inactivate behavior', 'Inactivate behavior']
    # state_2 = state_1
    # for i in range(len(name_list2)):
    #     state_2 = state_2.rename(columns={state_1.columns[i]: name_list2[i]})
    #
    # color_red = sns.light_palette('red', 10)[1:8]
    # color_blue = sns.light_palette('blue', 10)[2:5]
    # color_green = sns.light_palette('green', 10)[3:7]
    # color_list2 = color_red + color_blue + color_green
    #
    # x_tickets = ['00:00~10:00', '10:01~20:00', '20:01~30:00', '30:01~40:00', '40:01~50:00', '50:01~60:00']
    # plt.rcParams["figure.dpi"] = 300
    # # plt.rcParams["figure.autolayout"] = True
    # state_1.plot(kind='bar', figsize=[15, 8], stacked=True, color=color_list2, width=0.5)
    # plt.xticks(range(0, len(x_tickets)), x_tickets, rotation=0, fontsize=10)
    # plt.yticks(fontsize=10)
    # plt.legend(loc=2, bbox_to_anchor=(1.0, 1.0), borderaxespad=0., fontsize=10)
    # plt.xlabel('Time state/(min)', fontsize=15)
    # plt.ylabel('Ratio of behavior/(%)', fontsize=15)
    # plt.title("Behavior frequency in males at PM", fontsize=15)
    # plt.subplots_adjust(bottom=0.2, right=0.8, top=0.9)
    # # plt.tight_layout()
    # plt.show()
    #
    # state_corr = state_1.T.corr(method=histogram_intersection)
    # ax = sns.heatmap(state_corr, center=0)
