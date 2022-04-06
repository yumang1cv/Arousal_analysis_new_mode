import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import matplotlib

'''
    color:
    Wakefulness: '#f2b67c'
    RORR: '#808080'
    post-RORR1: '#8aaad2'
    post-RORR2: '#d6afaf'
    post-RORR3: '#d3d3d3'
    color_list_shadow = ['#a8a8a8', '#9ba7ca', '#c29799']
    color_list_line = ['#000000', '#0c5172', '#851717']
'''


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

        v_smooth = list(savgol_filter(v_list, 29, 2))

    return v_smooth


def sns_data(dataframe, file_list, be_looming_time, after_looming_time, typename="", row_name=''):
    global start_time
    global end_time
    global start_label
    global end_label
    start_time = []
    end_time = []
    for i in dataframe[row_name][0:8]:
        start_label = int(i) - 30 * be_looming_time
        end_label = int(i) + 30 * after_looming_time
        start_time.append(start_label)
        end_time.append(end_label)

    # dataframe['start_time'] = start_time
    # dataframe['end_time'] = end_time

    v_list = []
    for i in range(len(file_list)):
        # velocity(csv_result, i)
        v_list.append(velocity(file_list, i))
    # print(v_list)

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


def single_sns_data(dataframe, file_list, num, be_looming_time, after_looming_time, row_name="", typename=""):
    start_time_label = int(dataframe[row_name][num]) - 30 * be_looming_time
    end_time_label = int(dataframe[row_name][num]) + 30 * after_looming_time

    with open(file_list, 'rb') as f:
        df = pd.read_csv(f)
        df1 = df.iloc[2:, 36:39]  # select back vector
        df1 = df1.astype(float)
        v = df1.diff()
        v_x = v.iloc[start_time_label:end_time_label + 1, 0].tolist()
        v_y = v.iloc[start_time_label:end_time_label + 1, 1].tolist()
        v_z = v.iloc[start_time_label:end_time_label + 1, 2].tolist()
        v_list = []
        for j in range(0, len(v_x)):
            absolute_v = np.sqrt(np.square(v_x[j]) + np.square(v_y[j]) + +np.square(v_z[j]))  # Cali absolute velocity
            # absolute_v = smooth(absolute_v, 30)
            v_list.append(absolute_v)

        v_smooth = list(savgol_filter(v_list, 29, 2))

    # back_v_all = {"time": [], "value": [], "type": []}
    back_v_all = {"time": [], "value": []}

    time_list = [i for i in range(0, end_time_label - start_time_label + 1)]

    # back_v_all["type"] = [typename] * (end_time_label - start_time_label + 1)
    back_v_all["time"] = time_list
    back_v_all["value"] = v_smooth
    df = pd.DataFrame(back_v_all)

    return df


if __name__ == '__main__':
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
                 name="video_info.xlsx", column="looming_time1", state_name="Female_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    for item in a['Video_name'][0:10]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
                 r"/3Dskeleton/Calibrated_3DSkeleton",
            name="{}_Cali_Data3d".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))
    #
    # sns_data_1 = sns_data(a, file_list_1, 7, 53, typename="Male_Wakefulness", row_name='looming_time1')
    # # csv_result.clear()
    #
    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
                 name="video_info.xlsx", column="looming_time1", state_name="Female_RoRR")
    file_list_2 = []
    for item in b['Video_name'][0:10]:
        item = item.replace("-camera-0", "")
        file_list2 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
                 r"/3Dskeleton/Calibrated_3DSkeleton",
            name="{}_Cali_Data3d".format(item))
        file_list_2.append(file_list2)
    file_list_2 = list(np.ravel(file_list_2))
    #
    # sns_data_2 = sns_data(b, file_list_2, 7, 53, typename="Female_RoRR_1", row_name='looming_time1')
    # sns_data_3 = sns_data(b, file_list_2, 5, 55, typename="Female_RoRR_2", row_name='looming_time2')
    # sns_data_4 = sns_data(b, file_list_2, 3, 57, typename="Female_RoRR_3", row_name='looming_time3')
    # # sns_data = sns_data_1.append(sns_data_4)
    # # sns_data = pd.concat([sns_data_1, sns_data_2, sns_data_3, sns_data_4])
    # sns_data = pd.concat([sns_data_2, sns_data_1, sns_data_4])

    '''
        单只典型鼠
    '''
    num = 1
    # file_path = file_list_1[0]
    # sns_data_0 = single_sns_data(a, file_list_1[num], num, 4, 56,
    #                              typename="Wakefulness", row_name='looming_time1')
    # sns_data_1 = single_sns_data(b, file_list_2[num], num, 9, 51,
    #                              typename="Female_RoRR_3", row_name='looming_time1')
    # sns_data_2 = single_sns_data(b, file_list_2[num], num, 7, 53,
    #                              typename="Female_RoRR_1", row_name='looming_time2')
    # sns_data_3 = single_sns_data(b, file_list_2[num], num, 7, 53,
    #                              typename="Female_RoRR_2", row_name='looming_time3')
    # sns_data_4 = single_sns_data(b, file_list_2[num], num, 7, 53,
    #                              typename="Female_RoRR_4", row_name='looming_time4')

    # sns_data_0 = single_sns_data(a, file_list_1[num], num, 299, 0,
    #                              row_name='looming_time1')
    # sns_data_1 = single_sns_data(b, file_list_2[num], num, 299, 0,
    #                              row_name='looming_time1')
    # sns_data_2 = single_sns_data(b, file_list_2[num], num, 299, 0,
    #                              row_name='looming_time2')
    # sns_data_3 = single_sns_data(b, file_list_2[num], num, 299, 0,
    #                              row_name='looming_time3')
    # sns_data_4 = single_sns_data(b, file_list_2[num], num, 299, 0,
    #                              row_name='looming_time4')
    # sns_data_5 = single_sns_data(b, file_list_2[num], num, 299, 0,
    #                              row_name='looming_time5')
    for x in range(11, 12, 1):
        # x = 1
        row_name = 'looming_time{}'.format(x)
        sns_data_1 = single_sns_data(b, file_list_2[num], num, 299, 0,
                                     row_name=row_name)

        # sns_data = pd.concat([sns_data_0, sns_data_1, sns_data_2, sns_data_3, sns_data_4])
        # sns_data = pd.concat([sns_data_1, sns_data_2, sns_data_3])
        color_list_shadow = ['#a8a8a8', '#9ba7ca', '#c29799']
        # color_list_line = ['#000000', '#0c5172', '#851717']
        color_list_line = ['#851717']
        fig = plt.figure(figsize=(5, 2), dpi=300)

        ax = sns.barplot(x="time", y="value", data=sns_data_1, color='#d6afaf')





        # # sns.lineplot(data=sns_data_0, x="time", y="value", hue='type', palette=color_list_line)
        # ax = sns.lineplot(data=sns_data_4, x="time", y="value", color='#f2b67c', linewidth=4)
        # # sns.lineplot(data=sns_data, x="time", y="value", hue='type')
        # plt.axvspan(150, 300, color='gray', alpha=0.3, lw=0)
        # plt.rcParams.update({'font.family': 'Arial'})
        # x = [i for i in range(0, 1801, 300)]
        # labels = ['0', '10', '20', '30', '40', '50', '60']
        plt.ylim(0, 15, 5)
        # plt.xticks(x, labels, fontsize=24)
        # plt.yticks([0, 5, 10, 15, 20], fontsize=24)
        # plt.legend(fontsize=6)
        # plt.xlabel('Time (s)', fontsize=26)
        # plt.ylabel('Speed (cm/s)', fontsize=26)
        # # plt.title("Male-15 velocity after looming stimulate", fontsize=8)
        # # plt.title("Male-15 velocity after looming stimulate during RORR", fontsize=8)
        # # plt.title("Wakefulness", fontsize=8)
        # # figure.subplots_adjust(bottom=0.2, right=0.8, top=0.9)
        # ax.spines['top'].set_visible(False)
        # ax.spines['right'].set_visible(False)
        # ax.spines['bottom'].set_linewidth(3.5)
        # ax.spines['left'].set_linewidth(3.5)
        plt.axis('off')
        plt.tight_layout()

        plt.show()
        plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/velocity/SP_Arousal_add'
                    '/F_2_{}.tiff'.format(row_name), dpi=300)
        plt.close()
