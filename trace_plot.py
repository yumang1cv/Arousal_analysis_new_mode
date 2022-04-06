import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math
from sklearn import preprocessing


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


def trace_data(dataframe, file_list, be_looming_time, after_looming_time, num, rotation, row_name=''):
    global start_time
    global end_time
    global start_label
    global end_label
    start_time = []
    end_time = []
    for i in dataframe[row_name][0:8]:
        if i == 'nan':
            start_label = 0
            end_label = 0
            start_time.append(start_label)
            end_time.append(end_label)
        else:
            start_label = int(i) - 30 * be_looming_time
            end_label = int(i) + 30 * after_looming_time
            start_time.append(start_label)
            end_time.append(end_label)

    with open(file_list[num], 'rb') as f:
        df = pd.read_csv(f)
        df1 = df.iloc[2:, 36:38]  # select back vector
        df1 = df1.astype(float)

    # x_mean = np.mean(df1.iloc[:, 0])
    # y_mean = np.mean(df1.iloc[:, 1])
    y_x = []
    y_y = []
    for i in range(len(df1)):
        # print(df1.iat[0, i], df1.iat[1, i])
        x = [df1.iat[i, 0], df1.iat[i, 1]]
        # y = rotate_around_point_highperf(x, 1*math.pi/6, origin=(x_mean, y_mean))
        y = rotate_around_point_highperf(x, 1 * math.pi / rotation, origin=(0, 0))
        # y = rotate(x, [x_mean, y_mean], 40)
        y_x.append(y[0])
        y_y.append(y[1])

    y_x = np.array(y_x).reshape(-1, 1)
    y_y = np.array(y_y).reshape(-1, 1)
    norm_style = preprocessing.MinMaxScaler()
    y_x_norm = norm_style.fit_transform(y_x) * 30
    y_y_norm = norm_style.fit_transform(y_y) * 30

    df1['rotation_x'] = y_x_norm
    df1['rotation_y'] = y_y_norm

    return df1


def rotate_around_point_highperf(point, radians, origin=(0, 0)):
    """Rotate a point around a given point.

    I call this the "high performance" version since we're caching some
    values that are needed >1 time. It's less readable than the previous
    function but it's faster.
    """
    x_1, y_1 = point
    offset_x, offset_y = origin
    adjusted_x = (x_1 - offset_x)
    adjusted_y = (y_1 - offset_y)
    cos_rad = math.cos(radians)
    sin_rad = math.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y

    return qx, qy


def line_plot(ax1, line_width, color=''):
    line_with = line_width
    x1 = [0, 0]
    y1 = [0, 30]
    ax1.plot(x1, y1, 'black', linewidth=line_with, color='white', alpha=0)
    x2 = [0, 30]
    y2 = [0, 0]
    ax1.plot(x2, y2, 'black', linewidth=line_with, color='white', alpha=0)
    x3 = [30, 30]
    y3 = [0, 20]
    ax1.plot(x3, y3, 'black', linewidth=line_with, color='white', alpha=0)
    x4 = [0, 10]
    y4 = [30, 30]
    ax1.plot(x4, y4, 'black', linewidth=line_with, color='white', alpha=0)
    x5 = [10, 30]
    y5 = [20, 20]
    ax1.plot(x5, y5, 'black', linewidth=line_with, color='white', alpha=0)
    x6 = [10, 10]
    y6 = [20, 30]
    ax1.plot(x6, y6, 'black', linewidth=line_with, color='white', alpha=0)

    ax1.add_patch(Rectangle((0, 0), 30, 20, facecolor=color, fill=True, alpha=0.4))
    ax1.add_patch(Rectangle((0, 20), 10, 10, facecolor=color, fill=True, alpha=0.4))

    return


if __name__ == '__main__':
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
                 name="video_info.xlsx", column="looming_time1", state_name="Female_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    for item in a['Video_name'][0:8]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
                 r"/3Dskeleton/Calibrated_3DSkeleton",
            name="{}_Cali_Data3d".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    for x in range(2, 4, 2):
        # x = 1
        row_name = 'looming_time{}'.format(x)
        for num in range(1, 2, 1):
            # num = 1
            """
            race_data(dataframe, file_list, be_looming_time, after_looming_time, num, rotation, row_name='')
            """
            data = trace_data(a, file_list_1, 600, 0, num, 4.5, row_name=row_name)

            fig = plt.figure(figsize=(3, 3), dpi=300)
            ax = fig.add_subplot(111)
            # figure = plt.figure(figsize=(3, 3), dpi=300)

            # ax = sns.scatterplot(data=data, x="rotation_x", y="rotation_y", alpha=1)
            # sns.scatterplot(data=df1.iloc[start_time[num]:end_time[num]], x="rotation_x", y="rotation_y")
            ax.plot(data['rotation_x'].iloc[start_time[num]:end_time[num]],
                    data['rotation_y'].iloc[start_time[num]:end_time[num]], color='black', linewidth=1)
            '''
                color:
                Wakefulness: '#f2b67c'
                RORR: '#808080'
                post-RORR1: '#8aaad2'
                # post-RORR2: '#d3d3d3'
                11~15min: '#cbc2a0'
                16~20min: '#9c7abb'
                post-RORR3: '#d6afaf'
                color_list_shadow = ['#a8a8a8', '#9ba7ca', '#c29799']
                color_list_line = ['#000000', '#0c5172', '#851717']
            '''

            # plt a circle
            # x = data['rotation_x'].iloc[start_time[num] + 180:start_time[num] + 181]
            # y = data['rotation_y'].iloc[start_time[num] + 180:start_time[num] + 181]
            # plt.scatter(x, y, s=200, facecolors='none', edgecolors='red')
            color = '#d6afaf'
            line_plot(ax, 1, color=color)
            plt.axis('off')
            plt.show()
            plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/Guiji/SP_Arousal_add'
                        '/{}_{}.tiff'.format(file_list_1[num][-39:-16], row_name), dpi=300)
            plt.close()
            # print(num, row_name)

    """
        批量代码
    """
    # for x in range(1, 2, 1):
    #     # x = 1
    #     row_name = 'looming_time{}'.format(x)
    #     for num in range(8):
    #         # num = 1
    #         """
    #         race_data(dataframe, file_list, be_looming_time, after_looming_time, num, rotation, row_name='')
    #         """
    #         data = trace_data(a, file_list_1, 300, 0, num, 4.4, row_name=row_name)
    #
    #         fig = plt.figure(figsize=(3, 3), dpi=300)
    #         ax = fig.add_subplot(111)
    #         # figure = plt.figure(figsize=(3, 3), dpi=300)
    #
    #         # ax = sns.scatterplot(data=data, x="rotation_x", y="rotation_y", alpha=1)
    #         # sns.scatterplot(data=df1.iloc[start_time[num]:end_time[num]], x="rotation_x", y="rotation_y")
    #         ax.plot(data['rotation_x'].iloc[start_time[num]:end_time[num]],
    #                 data['rotation_y'].iloc[start_time[num]:end_time[num]], color='black', linewidth=1)
    #         '''
    #             color:
    #             Wakefulness: '#f2b67c'
    #             RORR: '#808080'
    #             post-RORR1: '#8aaad2'
    #             # post-RORR2: '#d3d3d3'
    #             11~15min: '#cbc2a0'
    #             16~20min: '#9c7abb'
    #             post-RORR3: '#d6afaf'
    #             color_list_shadow = ['#a8a8a8', '#9ba7ca', '#c29799']
    #             color_list_line = ['#000000', '#0c5172', '#851717']
    #         '''
    #
    #         # plt a circle
    #         # x = data['rotation_x'].iloc[start_time[num] + 180:start_time[num] + 181]
    #         # y = data['rotation_y'].iloc[start_time[num] + 180:start_time[num] + 181]
    #         # plt.scatter(x, y, s=200, facecolors='none', edgecolors='red')
    #         color = '#d6afaf'
    #         line_plot(ax, 1, color=color)
    #         plt.axis('off')
    #         plt.show()
    #         plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/Guiji/SP_Arousal_add'
    #                     '/{}_{}.tiff'.format(file_list_1[num][-39:-16], row_name), dpi=300)
    #         plt.close()
    #         # print(num, row_name)
