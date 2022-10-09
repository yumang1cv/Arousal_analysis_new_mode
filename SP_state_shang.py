# %%
# 徐阳
# 开发时间：2021/9/11 20:01
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
    """
        SP behavior 60min
    """
    """
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min',
                 name="video_info.xlsx", column="looming_time3", state_name="Male_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    # for item in a['Video_name'][0:len(a['Video_name'])]:
    for item in a['Video_name'][0:10]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min/new_results/BeAMapping-replace",
            name="{}_Movement_Labels".format(item))
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
            name="{}_Movement_Labels".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))
    # c = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
    #              name="video_info.xlsx", column="looming_time1", state_name="Male_Wakefulness")  # Male_Wakefulness

    # file_list_3 = []
    # for item in c['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
    #              r"/BeAMapping",
    #         name="{}_Movement_Labels".format(item))
    #     file_list_3.append(file_list1)
    # file_list_3 = list(np.ravel(file_list_3))
    #
    # d = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
    #              name="video_info.xlsx", column="looming_time1", state_name="Male_RoRR")  # Female_Wakefulness
    #
    # file_list_4 = []
    # for item in d['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
    #              r"/BeAMapping",
    #         name="{}_Movement_Labels".format(item))
    #     file_list_4.append(file_list1)
    # file_list_4 = list(np.ravel(file_list_4))

    # Male_list = pre_data(file_list_1, 20, 25)
    # Female_list = pre_data(file_list_2, 20, 25)
    all_shang = []
    for i in range(1, 13):
        Male_list = pre_looming_data(file_list_1, a, state="looming_time{}".format(i))
        Female_list = pre_looming_data(file_list_2, b, state="looming_time{}".format(i))
        # print(Male_list)
        # print(Female_list)
        MFM_list = Male_list + Female_list
        all_shang.append(MFM_list)
        # MFM_list.clear()
    all_shang_value = pd.DataFrame(all_shang)
    all_shang_value2 = (all_shang_value - all_shang_value.min()) / (all_shang_value.max() - all_shang_value.min())
    # all_shang_value1 = np.array(all_shang_value)
    all_shang_value3 = normalize_2d(all_shang_value)
    all_shang_value3 = pd.DataFrame(all_shang_value3)
    # all_shang_value3 = all_shang_value3.multiply(10)
    # sns.heatmap(all_shang_value2)
    # all_shang_value.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/SP_behavior_shang/SP_shang_old.csv')
    """

    """
        SP Arousal:       Wake:10min                 Arousal:60min
    """
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
                 name="video_info.xlsx", column="looming_time3", state_name="Male_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    # for item in a['Video_name'][0:len(a['Video_name'])]:
    for item in a['Video_name'][0:10]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2/BeAMapping",
            name="{}_Movement_Labels".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
                 name="video_info.xlsx", column="looming_time3", state_name="Female_Wakefulness")  # Female_Wakefulness

    file_list_2 = []
    # for item in b['Video_name'][0:len(a['Video_name'])]:
    for item in b['Video_name'][0:10]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2/BeAMapping",
            name="{}_Movement_Labels".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    all_shang = []
    for i in range(1, 3):
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
    # all_shang_value3 = all_shang_value3.multiply(10)
    # sns.heatmap(all_shang_value2)
    # all_shang_value.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/SP_behavior_shang/SPArousal_wake_shang_old.csv')


    """
        5分钟内16个行为的频率
    """
    # output_list = []
    # for num in range(1, 3):
    #     state = 'looming_time{}'.format(num)
    #     label_num = single_behavior_cal(file_list_1, a, state)
    #     output_list.append(label_num)
    #
    # for num in range(1, 13):
    #     state = 'looming_time{}'.format(num)
    #     label_num = single_behavior_cal(file_list_2, b, state)
    #     output_list.append(label_num)
    #
    # for num in range(1, 3):
    #     state = 'looming_time{}'.format(num)
    #     label_num = single_behavior_cal(file_list_3, c, state)
    #     output_list.append(label_num)
    #
    # for num in range(1, 13):
    #     state = 'looming_time{}'.format(num)
    #     label_num = single_behavior_cal(file_list_4, d, state)
    #     output_list.append(label_num)
    #
    # output_data = pd.DataFrame(output_list)
    # output_data = list(np.ravel(output_data))
    # output_data = pd.DataFrame(output_data)
    # output_data = output_data.to_numpy()
    # normed_matrix = normalize(output_data, axis=1, norm='l1')
    # normed_matrix = pd.DataFrame(normed_matrix)
    #
    # normed_matrix['state'] = 'Female_Wakefulness1'
    # first_column = normed_matrix.pop('state')
    # normed_matrix.insert(0, 'state', first_column)
    # state_name = ['Female_Wakefulness1', 'Female_Wakefulness2', 'Female_RORR1', 'Female_RORR2',
    #               'Female_RORR3', 'Female_RORR4', 'Female_RORR5', 'Female_RORR6', 'Female_RORR7',
    #               'Female_RORR8', 'Female_RORR9', 'Female_RORR10', 'Female_RORR11', 'Female_RORR12',
    #               'Male_Wakefulness1', 'Male_Wakefulness2', 'Male_RORR1', 'Male_RORR2', 'Male_RORR3',
    #               'Male_RORR4', 'Male_RORR5', 'Male_RORR6', 'Male_RORR7', 'Male_RORR8', 'Male_RORR9',
    #               'Male_RORR10', 'Male_RORR11', 'Male_RORR12']
    # for j in range(0, 280, 10):
    #     normed_matrix['state'][j:j + 10] = state_name[int(j / 10)]
    #
    # normed_matrix['mouse_num'] = [i for i in range(1, 11)]*28
    # second_column = normed_matrix.pop('mouse_num')
    # normed_matrix.insert(1, 'mouse_num', second_column)
    # # output_data = output_data.rename(index={0: '0~5min_wake', 1: '5~10min_wake', 2: '0~5min_RORR'})
    # normed_matrix.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space'
    #                      '/SP_Arousal_add_60/looming_behavior_fre_add/All_mouse_behavior_fre.csv')
    """
        10分钟内16个行为的频率
    """
    # output_list = []
    # for num in range(2, 3):
    #     state = 'looming_time{}'.format(num)
    #     label_num = single_behavior_cal(file_list_1, a, state)
    #     output_list.append(label_num)
    #
    # for num in range(2, 13, 2):
    #     state = 'looming_time{}'.format(num)
    #     label_num = single_behavior_cal(file_list_2, b, state)
    #     output_list.append(label_num)
    #
    # for num in range(2, 3):
    #     state = 'looming_time{}'.format(num)
    #     label_num = single_behavior_cal(file_list_3, c, state)
    #     output_list.append(label_num)
    #
    # for num in range(2, 13, 2):
    #     state = 'looming_time{}'.format(num)
    #     label_num = single_behavior_cal(file_list_4, d, state)
    #     output_list.append(label_num)
    #
    # output_data = pd.DataFrame(output_list)
    # output_data = list(np.ravel(output_data))
    # output_data = pd.DataFrame(output_data)
    # output_data = output_data.to_numpy()
    # normed_matrix = normalize(output_data, axis=1, norm='l1')
    # normed_matrix = pd.DataFrame(normed_matrix)
    #
    # normed_matrix['state'] = 'Female_Wakefulness1'
    # first_column = normed_matrix.pop('state')
    # normed_matrix.insert(0, 'state', first_column)
    # state_name = ['Female_Wakefulness', 'Female_RORR1', 'Female_RORR2', 'Female_RORR3', 'Female_RORR4',
    #               'Female_RORR5', 'Female_RORR6', 'Male_Wakefulness', 'Male_RORR1', 'Male_RORR2',
    #               'Male_RORR3', 'Male_RORR4', 'Male_RORR5', 'Male_RORR6']
    #
    # for j in range(0, 140, 10):
    #     normed_matrix['state'][j:j + 10] = state_name[int(j / 10)]
    #
    # normed_matrix['mouse_num'] = [i for i in range(1, 11)] * 14
    # second_column = normed_matrix.pop('mouse_num')
    # normed_matrix.insert(1, 'mouse_num', second_column)
    # # output_data = output_data.rename(index={0: '0~5min_wake', 1: '5~10min_wake', 2: '0~5min_RORR'})
    # normed_matrix.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space'
    #                      '/SP_Arousal_add_60/looming_behavior_fre_add/All_mouse_behavior_fre_10min.csv')

    """
        behavior frequency test code
    """
    # file_path = file_list_1
    # dataframe = a
    # # state = 'looming_time1'
    # behavior_label_num = []
    # output_list = []
    # # j = 2
    # for num in range(1, 3):
    #     state = 'looming_time{}'.format(num)
    #     # behavior_label_num.clear()
    #     for j in range(len(file_path)):
    #         looming_time = int(dataframe.at[j, state])
    #         df1 = pd.read_csv(file_path[j])
    #
    #         data = df1.iloc[looming_time - 300 * 30:looming_time + 0 * 30, 1:2]
    #
    #         class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
    #                       9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
    #         for line in data.iloc[:, 0]:
    #             if line not in class_type:
    #                 class_type[line] = 0
    #             else:
    #                 class_type[line] += 1
    #
    #         class_type = dict(sorted(class_type.items(), key=lambda item: item[0]))  # sort dict
    #
    #         # behavior_label_num = list(class_type.values())
    #         class_type_value = list(class_type.values())
    #         behavior_label_num.append(class_type_value)
    #
    #     output_list.append(behavior_label_num)
    #     behavior_label_num = []

    """
        5分钟内所有行为产生的个数
    """
    # output_list = []
    # for num in range(2, 3):
    #     state = 'looming_time{}'.format(num)
    #     label_num = behavior_num(file_list_1, a, state)
    #     output_list.append(label_num)
    #
    # for num in range(2, 13, 2):
    #     state = 'looming_time{}'.format(num)
    #     label_num = behavior_num(file_list_2, b, state)
    #     output_list.append(label_num)
    #
    # output_data = pd.DataFrame(output_list)
    # output_data = output_data.rename(index={0: '0~10min_wake', 1: '0~10min_RORR', 2: '10~20min_RORR'})
    # output_data.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space'
    #                    '/SP_Arousal_add_60/looming_behavior_fre_add/Male_behavior_number_10min.csv')

    """
        熵值代码测试
    """
    # fre = 1
    # start = 20 * 60 * 30
    # end = 25 * 60 * 30
    # fre_list = []
    # # j = 3
    # for j in range(len(file_list_2)):
    #     df1 = pd.read_csv(file_list_2[j])
    #
    #     data = df1.iloc[start:end, 1:2]
    #     for i in range(1, len(data)):
    #         if data.iloc[i, 0] != data.iloc[i - 1, 0]:
    #             fre = fre + 1
    #     fre_list.append(fre)
    #     # print('第{}个文件的熵值为:'.format(j), fre)
    #     fre = 1

    # explicit function to normalize array
    # def normalize(arr, t_min, t_max):
    #     norm_arr = []
    #     diff = t_max - t_min
    #     diff_arr = max(arr) - min(arr)
    #     for i in arr:
    #         temp = (((i - min(arr)) * diff) / diff_arr) + t_min
    #         norm_arr.append(temp)
    #     return norm_arr
    #
    #
    # range_to_normalize = (-1, 1)
    # normalized_array_1d = normalize(output_data.all(),
    #                                 range_to_normalize[0],
    #                                 range_to_normalize[1])
