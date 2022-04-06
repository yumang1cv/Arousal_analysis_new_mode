import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

csv_result = []


def search_csv(path=".", name=""):  # 抓取csv文件

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            search_csv(item_path, name)
        elif os.path.isfile(item_path):
            if name + ".csv" == item:
                global csv_result
                # csv_result.append(name)
                csv_result.append(item_path)
                # print(item_path + ";", end="")

    return csv_result


def read_csv(path='.', name="", column="", element="", state_name=""):
    """
        column[0]: file_name     column[1]:第一次looming时间点
        sheet1：Fwake状态          sheet2：Frorr状态
    """
    item_path = os.path.join(path, name)
    with open(item_path, 'rb') as f:
        csv_data = pd.read_excel(f, sheet_name=state_name)

    # df1 = csv_data.set_index([column])  # 选取某一列数据
    # sel_data = df1.loc[element]  # 根据元素提取特定数据

    return csv_data


def velocity(file_path, num):  # Cali velocity
    """
        nose:0    left_ear:1   Right_ear:2    neck:3    left_front_limb:4     right_front_limb:5
        left_hind_limb:6       right_hind_limb:7          left_front_claw:8     right_front_claw:9
        left_hind_claw:10      right_hind_claw:11        back:12      root_tail:13
        mid_tail:14            tip_tail:15
    """

    with open(file_path[num], 'rb') as f:
        df = pd.read_csv(f)
        df1 = df.iloc[2:, 36:39]  # select back vector
        df1 = df1.astype(float)
        v = df1.diff()
        v_x = v.iloc[start_time[num]:end_time[num] + 1, 0].tolist()
        v_y = v.iloc[start_time[num]:end_time[num] + 1, 1].tolist()
        v_z = v.iloc[start_time[num]:end_time[num] + 1, 2].tolist()
        v_list = []
        for j in range(0, len(v_x)):
            absolute_v = np.sqrt(np.square(v_x[j]) + np.square(v_y[j]) + +np.square(v_z[j]))  # Cali absolute velocity
            # absolute_v = smooth(absolute_v, 30)
            v_list.append(absolute_v)

        v_smooth = list(savgol_filter(v_list, 29, 3))

    return v_smooth


def sns_data(dataframe, file_list, be_looming_time, after_looming_time, typename=""):
    global start_time
    global end_time
    global start_label
    global end_label
    start_time = []
    end_time = []
    for i in dataframe['time']:
        start_label = i - 30 * be_looming_time
        end_label = i + 30 * after_looming_time
        start_time.append(start_label)
        end_time.append(end_label)

    dataframe['start_time'] = start_time
    dataframe['end_time'] = end_time

    v_list = []
    for i in range(len(file_list)):
        # velocity(csv_result, i)
        v_list.append(velocity(file_list, i))
    print(v_list)

    back_v_all = {"time": [], "value": [], "type": []}

    time_list = [i for i in range(0, end_label - start_label + 1)]

    time_list_all = []
    for i in range(len(v_list)):
        time_list_all.append(time_list)
        back_v_all["type"].append([typename] * (end_label - start_label + 1))
    time_list_all = sum(time_list_all, [])
    back_v_all["time"] = time_list_all
    back_v_all["value"] = v_list

    back_v_all["value"] = sum(back_v_all["value"], [])
    back_v_all["type"] = sum(back_v_all["type"], [])

    df = pd.DataFrame(back_v_all)

    return df


if __name__ == '__main__':
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/results-20211217/3Dskeleton',
                 name="looming_tag_time.xlsx", column="time", state_name="Frorr")
    for item in a['name']:
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/results-20211217/3Dskeleton/Calibrated_3DSkeleton",
            name="{}_Cali_Data3d".format(item))

    sns_data_1 = sns_data(a, file_list1, 3, 30, typename="Frorr")
    csv_result.clear()

    # b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/results-20211217/3Dskeleton',
    #              name="looming_tag_time.xlsx", column="time", state_name="Mrorr")
    # for item in b['name']:
    #     file_list2 = search_csv(path=r"D:/3D_behavior/Arousal_behavior/results-20211217/3Dskeleton/Calibrated_3DSkeleton",
    #                             name="{}_Cali_Data3d".format(item))
    #
    # sns_data_2 = sns_data(b, file_list2, 3, 30, typename="Mrorr")
    # sns_data = sns_data_1.append(sns_data_2)
    # sns.lineplot(data=sns_data, x="time", y="value", hue="type")



    # with open(file_list1[0], 'rb') as f:
    #     df = pd.read_csv(f)
    #     df1 = df.iloc[2:, 36:39]  # select back vector
    #     df1 = df1.astype(float)
    #     v = df1.diff()
    #     v_x = v.iloc[start_time[0]:end_time[0] + 1, 0].tolist()
    #     v_y = v.iloc[start_time[0]:end_time[0] + 1, 1].tolist()
    #     v_z = v.iloc[start_time[0]:end_time[0] + 1, 2].tolist()
    #     v_list = []
    #     for j in range(0, len(v_x)):
    #         absolute_v = np.sqrt(np.square(v_x[j]) + np.square(v_y[j]) + +np.square(v_z[j]))  # Cali absolute velocity
    #         # absolute_v = smooth(absolute_v, 30)
    #         v_list.append(absolute_v)
    #
    #     v_smooth = list(savgol_filter(v_list, 29, 3))