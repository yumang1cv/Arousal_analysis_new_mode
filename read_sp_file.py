# encoding: utf-8
import os
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import substring
from tqdm import tqdm


# csv_result = []


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

    # print(class_fre_result_sorted)

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

    print("结果为：", sev_file_dict)
    print('\n')

    return sev_file_dict


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


if __name__ == '__main__':
    a = read_csv(path=r'D:\\3D_behavior\\Spontaneous_behavior\\result',
                 name="video_info.xlsx", column="ExperimentTime", element="day")
    # csv_F = []
    # for item in a['Unique_serial_number']:
    #     csv_result1 = search_csv(
    #         path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\",
    #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    #     csv_F.append(csv_result1[0])
    #
    # female_result = read_several_file(csv_F)
    # female_result_nor = several_file_sum(female_result)

    # b = read_csv(path=r'D:\\3D_behavior\\Spontaneous_behavior\\result',
    #              name="video_info.xlsx", column="gender", element="male")
    # csv_b = []
    # for item in b['Unique_serial_number']:
    #     csv_result2 = search_csv(
    #         path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\",
    #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    #     csv_b.append(csv_result2[0])
    #
    # male_result = read_several_file(csv_b)
    # male_result_nor = several_file_sum(male_result)

    # bar_plot(male_result_nor, female_result_nor)

    # 多条件筛选
    x = choose_data(a, column='gender', element='female')
    df_day = pd.DataFrame(x, columns=["Unique_serial_number"])
    # data = df_day.values.tolist()
    csv_FD = []
    for item in tqdm(df_day['Unique_serial_number']):
        csv_result3 = search_csv(
            path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\",
            name="rec-{}-G1-2021114230_Movement_Labels".format(item))
        csv_FD.append(csv_result3[0])

    femaleDay_result = read_several_file(csv_FD)
    femaleDay_result_nor = several_file_sum(femaleDay_result)

    y = choose_data(a, column='gender', element='male')
    df_night = pd.DataFrame(y, columns=["Unique_serial_number"])
    # data = df_night.values.tolist()
    csv_FN = []
    for item in tqdm(df_night['Unique_serial_number']):
        csv_result4 = search_csv(
            path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\",
            name="rec-{}-G1-2021114230_Movement_Labels".format(item))
        csv_FN.append(csv_result4[0])

    femaleNight_result = read_several_file(csv_FN)
    femaleNight_result_nor = several_file_sum(femaleNight_result)

    # bar_plot(femaleDay_result_nor, femaleNight_result_nor)
"""   
    # 多条件筛选
    x = choose_data(a, column='ExperimentTime', element='day')
    df_day = pd.DataFrame(x, columns=["Unique_serial_number"])
    data = df_day.values.tolist()

    for item in df_day['Unique_serial_number']:
        search_csv(path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\",
                   name="rec-{}-G1-2021114230_Movement_Labels".format(item))

    read_single_file('D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_rename')
"""
