# encoding: utf-8
import os
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import substring
from tqdm import tqdm


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
            line = line[1:2]
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


def single_mouse_behavior(file_path):
    behavior_all = []
    for item in file_path:
        # f = pd.read_csv(item)
        class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                      9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
        """
            pandas计算步骤
        """
        # for i in range(len(f)):
        #     if int(f.iloc[i, 1:2]) not in class_type:
        #         class_type[int(f.iloc[i, 1:2])] = 0
        #     else:
        #         class_type[int(f.iloc[i, 1:2])] += 1
        # # print(class_type)
        # behavior_fre = list(class_type.values())
        # behavior_all.append(behavior_fre)
        # print(behavior_all)
        with open(item) as f:  # read single file to dict
            reader = f
            for line in reader:
                # print(line)
                line = substring.substringByChar(line, startChar=",")
                line = line[1:3]
                if line[-1] == ',':
                    line = line[0]
                else:
                    line = line
                # print(line)
                line = line.strip('\n')
                # sorted(class_type.keys())
                if line not in class_type:
                    class_type[str(line)] = 0
                else:
                    class_type[str(line)] += 1
            # print("Original dict", class_type)

            class_type_float = {float(k): float(v) for k, v in class_type.items()}  # data str to float
            class_type_int = {int(k): int(v) for k, v in class_type_float.items()}  # data str to int
            class_type_sorted = dict(sorted(class_type_int.items(), key=lambda item: item[0]))  # sort dict
            behavior_fre = list(class_type_sorted.values())

            behavior_all.append(behavior_fre)

    final_list = []
    for j in range(0, len(behavior_all), 6):
        sub_list = [sum(i) for i in zip(behavior_all[j], behavior_all[j + 1], behavior_all[j + 2],
                                        behavior_all[j + 3], behavior_all[j + 4], behavior_all[j + 5])]
        # 10、20、30、40、50、60min列表求和
        final_list.append(sub_list)
    final_array = np.array(final_list)
    final_data = pd.DataFrame(final_array)
    final_data.loc[len(final_data)] = 0

    return final_data


if __name__ == '__main__':
    """
        单组分分析
    """
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
                 name="video_info.xlsx", column="looming_time3", state_name="Male_RoRR")  # Male_Wakefulness

    file_list_1 = []
    for item in a['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2/BeAMapping_correct",
            name="{}_Movement_Labels".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
                 name="video_info.xlsx", column="looming_time3", state_name="Female_Wakefulness")  # Female_Wakefulness

    file_list_2 = []
    for item in b['Video_name'][0:6]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2/BeAMapping_correct",
            name="{}_Movement_Labels".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    # 多条件筛选
    # x = choose_data(a, column='gender', element=gender)
    # df_day = pd.DataFrame(a, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    # csv_FD = []
    # for item in tqdm(df_day['Unique_serial_number']):
    #     csv_result3 = search_csv(
    #         path=r"D:/3D_behavior/Spontaneous_behavior/result/BeAMapping-Final/BeAMapping_replace/",
    #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    #     csv_FD.append(csv_result3[0])

    behavior_all = []
    # for item in file_list_1:
    data = file_list_2
    pre_df = b
    for x in range(1, 2):
        for j in range(len(data)):
            item = data[j]
            f = pd.read_csv(item)
            class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                          9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
            start_time = int(pre_df['looming_time{}'.format(x)][j] - 0)
            end_time = int(start_time + 2*60*30)
            """
                pandas计算步骤
            """
            # for i in range(len(f)):
            for i in range(start_time, end_time + 1):
                # i = int(i)
                if int(f.iloc[i, 1:2]) not in class_type:
                    class_type[int(f.iloc[i, 1:2])] = 0
                else:
                    class_type[int(f.iloc[i, 1:2])] += 1
            # print(class_type)
            behavior_fre = list(class_type.values())
            behavior_all.append(behavior_fre)
        behavior_all.append([0] * 16)
        # print(behavior_all)
    final_data = pd.DataFrame(behavior_all)

    # final_data.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/Radar_chart/'
    #                   'Female_looming_wake_v2.csv')

    # with open(item) as f:  # read single file to dict
    #     reader = f
    #     for line in reader:
    #         # print(line)
    #         line = substring.substringByChar(line, startChar=",")
    #         line = line[1:3]
    #         if line[-1] == ',':
    #             line = line[0]
    #         else:
    #             line = line
    #         # print(line)
    #         line = line.strip('\n')
    #         # sorted(class_type.keys())
    #         if line not in class_type:
    #             class_type[str(line)] = 0
    #         else:
    #             class_type[str(line)] += 1
    #     # print("Original dict", class_type)
    #
    #     class_type_float = {float(k): float(v) for k, v in class_type.items()}  # data str to float
    #     class_type_int = {int(k): int(v) for k, v in class_type_float.items()}  # data str to int
    #     class_type_sorted = dict(sorted(class_type_int.items(), key=lambda item: item[0]))  # sort dict
    #     behavior_fre = list(class_type_sorted.values())
    #
    #     behavior_all.append(behavior_fre)
    #
    # final_list = []
    # for j in range(0, len(behavior_all), 6):
    #     sub_list = [sum(i) for i in zip(behavior_all[j], behavior_all[j + 1], behavior_all[j + 2],
    #                                     behavior_all[j + 3], behavior_all[j + 4], behavior_all[j + 5])]
    #     # 10、20、30、40、50、60min列表求和
    #     final_list.append(sub_list)
    # final_array = np.array(final_list)
    # final_data = pd.DataFrame(final_array)
    # final_data.to_csv('D:/3D_behavior/Spontaneous_behavior/result/analysis_result/behavior_fre/'
    #                   'Round3.csv')

    """
        多组分分析
    """
    # ExperimentTime = 'night'
    # gender = 'female'
    # Round = 1
    # a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result',
    #              name="video_info.xlsx", column="ExperimentTime", element=ExperimentTime)
    # # csv_F = []
    # # for item in a['Unique_serial_number']:
    # #     csv_result1 = search_csv(
    # #         path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\",
    # #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    # #     csv_F.append(csv_result1[0])
    # #
    # # female_result = read_several_file(csv_F)
    # # female_result_nor = several_file_sum(female_result)
    #
    # # b = read_csv(path=r'D:\\3D_behavior\\Spontaneous_behavior\\result',
    # #              name="video_info.xlsx", column="gender", element="male")
    # # csv_b = []
    # # for item in b['Unique_serial_number']:
    # #     csv_result2 = search_csv(
    # #         path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\",
    # #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    # #     csv_b.append(csv_result2[0])
    # #
    # # male_result = read_several_file(csv_b)
    # # male_result_nor = several_file_sum(male_result)
    #
    # # bar_plot(male_result_nor, female_result_nor)
    #
    # # 多条件筛选
    # x = choose_data(a, column='gender', element=gender)
    # y = choose_data(x, column='origin_seg', element=Round)
    # df_day = pd.DataFrame(y, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    # csv_FD = []
    # for item in tqdm(df_day['Unique_serial_number']):
    #     csv_result3 = search_csv(
    #         path=r"D:/3D_behavior/Spontaneous_behavior/result/BeAMapping-Final/BeAMapping_replace/",
    #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    #     csv_FD.append(csv_result3[0])
    # # behavior_all = []
    # # for item in csv_FD:
    # #     # f = pd.read_csv(item)
    # #     class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
    # #                   9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
    # #     """
    # #         pandas计算步骤
    # #     """
    # #     # for i in range(len(f)):
    # #     #     if int(f.iloc[i, 1:2]) not in class_type:
    # #     #         class_type[int(f.iloc[i, 1:2])] = 0
    # #     #     else:
    # #     #         class_type[int(f.iloc[i, 1:2])] += 1
    # #     # # print(class_type)
    # #     # behavior_fre = list(class_type.values())
    # #     # behavior_all.append(behavior_fre)
    # #     # print(behavior_all)
    # #     with open(item) as f:  # read single file to dict
    # #         reader = f
    # #         for line in reader:
    # #             # print(line)
    # #             line = substring.substringByChar(line, startChar=",")
    # #             line = line[1:3]
    # #             if line[-1] == ',':
    # #                 line = line[0]
    # #             else:
    # #                 line = line
    # #             # print(line)
    # #             line = line.strip('\n')
    # #             # sorted(class_type.keys())
    # #             if line not in class_type:
    # #                 class_type[str(line)] = 0
    # #             else:
    # #                 class_type[str(line)] += 1
    # #         # print("Original dict", class_type)
    # #
    # #         class_type_float = {float(k): float(v) for k, v in class_type.items()}  # data str to float
    # #         class_type_int = {int(k): int(v) for k, v in class_type_float.items()}  # data str to int
    # #         class_type_sorted = dict(sorted(class_type_int.items(), key=lambda item: item[0]))  # sort dict
    # #         behavior_fre = list(class_type_sorted.values())
    # #
    # #         behavior_all.append(behavior_fre)
    # #
    # # final_list = []
    # # for j in range(0, len(behavior_all), 6):
    # #     sub_list = [sum(i) for i in zip(behavior_all[j], behavior_all[j + 1], behavior_all[j + 2],
    # #                                     behavior_all[j + 3], behavior_all[j + 4], behavior_all[j + 5])]
    # #     # 10、20、30、40、50、60min列表求和
    # #     final_list.append(sub_list)
    # # final_array = np.array(final_list)
    # # final_data = pd.DataFrame(final_array)
    # # final_data.to_csv('D:/3D_behavior/Spontaneous_behavior/result/analysis_result/behavior_fre/'
    # #                   'Round3.csv')
    # data_1 = single_mouse_behavior(csv_FD)
    #
    # a1 = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result',
    #               name="video_info.xlsx", column="ExperimentTime", element='day')
    # # csv_F = []
    # # for item in a['Unique_serial_number']:
    # #     csv_result1 = search_csv(
    # #         path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\",
    # #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    # #     csv_F.append(csv_result1[0])
    # #
    # # female_result = read_several_file(csv_F)
    # # female_result_nor = several_file_sum(female_result)
    #
    # # b = read_csv(path=r'D:\\3D_behavior\\Spontaneous_behavior\\result',
    # #              name="video_info.xlsx", column="gender", element="male")
    # # csv_b = []
    # # for item in b['Unique_serial_number']:
    # #     csv_result2 = search_csv(
    # #         path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\",
    # #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    # #     csv_b.append(csv_result2[0])
    # #
    # # male_result = read_several_file(csv_b)
    # # male_result_nor = several_file_sum(male_result)
    #
    # # bar_plot(male_result_nor, female_result_nor)
    #
    # # 多条件筛选
    # x1 = choose_data(a1, column='gender', element=gender)
    # y1 = choose_data(x1, column='origin_seg', element=2)
    # df_day = pd.DataFrame(y1, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    # csv_FD1 = []
    # for item in tqdm(df_day['Unique_serial_number']):
    #     csv_result31 = search_csv(
    #         path=r"D:/3D_behavior/Spontaneous_behavior/result/BeAMapping-Final/BeAMapping_replace/",
    #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    #     csv_FD1.append(csv_result31[0])
    #
    # data_2 = single_mouse_behavior(csv_FD1)
    #
    # y2 = choose_data(x, column='origin_seg', element=3)
    # df_day = pd.DataFrame(y2, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    # csv_FD2 = []
    # for item in tqdm(df_day['Unique_serial_number']):
    #     csv_result32 = search_csv(
    #         path=r"D:/3D_behavior/Spontaneous_behavior/result/BeAMapping-Final/BeAMapping_replace/",
    #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    #     csv_FD2.append(csv_result32[0])
    #
    # data_3 = single_mouse_behavior(csv_FD2)
    # data_all = pd.concat([data_1, data_2, data_3], ignore_index=True)
    # data_all.to_csv('D:/3D_behavior/Spontaneous_behavior/result/analysis_result/behavior_fre/'
    #                 'F_NDN_group2.csv')

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
