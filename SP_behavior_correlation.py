# %%
# 徐阳
# 开发时间：2021/9/11 20:01
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import matplotlib
from sklearn import *
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler  # to standardize the features

matplotlib.use('Qt5Agg')

color_list = ['#845EC2', '#B39CD0', '#D65DB1', '#4FFBDF', '#FFC75F',
              '#D5CABD', '#B0A8B9', '#FF6F91', '#F9F871', '#D7E8F0',
              '#60DB73', '#E8575A', '#008B74', '#00C0A3', '#FF9671',
              '#93DEB1']
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
    df1 = pd.read_csv(file_path)
    looming_time = int(dataframe.at[num, state])
    # data = df1.iloc[looming_time - 17995:looming_time, 1:2]
    data = df1.iloc[looming_time - 5*30:looming_time+115*30, 1:2]  # looming专用 2分钟计算

    data1 = data.iloc[:, 0].tolist()

    class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
                  11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
    for line in data1:
        if line not in class_type:
            class_type[line] = 0

        else:
            class_type[line] += 1

    list_1 = list(class_type.values())

    return list_1


def sort_data(list_1):
    male_std = []
    for i in range(len(list_1)):
        male_1 = np.std(list_1[i])
        male_std.append(male_1)

    dictionary = dict(zip(male_std, list_1))
    # dictionary1 = {l: sorted(m) for l, m in dictionary.items()}
    # dictionary = sorted(dictionary.keys())

    sort_list = []

    # convert the dictionary to list using dict.keys
    dictlist = list(dictionary.keys())
    # sort the list
    dictlist.sort()
    # Print the corresponding key and value by traversing this list
    for key in dictlist:
        # print key and value
        # print(key, ":", dictionary[key])
        sort_list.append(dictionary[key])

    return sort_list


if __name__ == '__main__':
    """
        SP Arousal 60min
    """
    # """
    #     Wakefulness状态
    # """
    # a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
    #              name="video_info.xlsx", column="looming_time1", state_name="Male_Wakefulness")  # Male_Wakefulness
    # file_list_1 = []
    # for item in a['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
    #              r"/BeAMapping",
    #         name="{}_Movement_Labels".format(item))
    #     file_list_1.append(file_list1)
    # file_list_1 = list(np.ravel(file_list_1))
    #
    # b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
    #              name="video_info.xlsx", column="looming_time1", state_name="Female_Wakefulness")  # Female_Wakefulness
    # file_list_2 = []
    # for item in b['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
    #              r"/BeAMapping",
    #         name="{}_Movement_Labels".format(item))
    #     file_list_2.append(file_list1)
    # file_list_2 = list(np.ravel(file_list_2))
    #
    # Male_list = []
    # for i in range(len(file_list_1)):
    #     sub_list1 = pre_data(file_list_1[i], a, i, state="looming_time2")
    #     # print(sub_list1)
    #     Male_list.append(sub_list1)
    # # Male_list = sort_data(Male_list)
    #
    # Female_list = []
    # for i in range(len(file_list_2)):
    #     sub_list2 = pre_data(file_list_2[i], b, i, state="looming_time2")
    #     # print(sub_list2)
    #     Female_list.append(sub_list2)
    # # Female_list = sorted(Female_list)
    # # Female_list = sort_data(Female_list)
    #
    # Wake = Male_list + Female_list
    # Wake = pd.DataFrame(Wake)
    #
    # """
    #     主成分分析
    # """
    # # pca = PCA(n_components=3)
    # # Wake_pca = pca.fit(Wake.T)
    # # print(pca.explained_variance_ratio_)
    # # Wake1 = Wake_pca.components_.T
    # # Wake1 = pd.DataFrame(Wake1)
    # # Wake1.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/correlation/wake.csv')
    #
    # """
    #     RORR状态
    # """
    # c = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
    #              name="video_info.xlsx", column="looming_time1", state_name="Male_RoRR")  # Male_Wakefulness
    # file_list_3 = []
    # for item in c['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list3 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
    #              r"/BeAMapping",
    #         name="{}_Movement_Labels".format(item))
    #     file_list_3.append(file_list3)
    # file_list_3 = list(np.ravel(file_list_3))
    #
    # d = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
    #              name="video_info.xlsx", column="looming_time1", state_name="Female_RoRR")  # Male_Wakefulness
    # file_list_4 = []
    # for item in d['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list4 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
    #              r"/BeAMapping",
    #         name="{}_Movement_Labels".format(item))
    #     file_list_4.append(file_list4)
    # file_list_4 = list(np.ravel(file_list_4))
    #
    # for j in range(2, 14, 2):
    #     state = 'looming_time{}'.format(j)
    #
    #     Male_RORR = []
    #     for i in range(len(file_list_3)):
    #         sub_list3 = pre_data(file_list_3[i], c, i, state=state)
    #         # print(sub_list2)
    #         Male_RORR.append(sub_list3)
    #     # Male_RORR = sort_data(Male_RORR)
    #
    #     Female_RORR = []
    #     for i in range(len(file_list_4)):
    #         sub_list4 = pre_data(file_list_4[i], d, i, state=state)
    #         # print(sub_list2)
    #         Female_RORR.append(sub_list4)
    #     # Female_RORR = sort_data(Female_RORR)
    #
    #     RORR = Male_RORR + Female_RORR
    #     RORR = sort_data(RORR)
    #
    #     """
    #         主成分分析
    #     """
    #     # RORR = pd.DataFrame(RORR)
    #     # pca = PCA(n_components=3)
    #     # RORR_pca = pca.fit(RORR.T)
    #     # print(pca.explained_variance_ratio_)
    #     # RORR1 = RORR_pca.components_.T
    #     # RORR1 = pd.DataFrame(RORR1)
    #     # RORR1.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/correlation/RORR_{}min.csv'.format(j * 5))
    #
    #     # all_list = Male_list + Female_list + Female_list2 + Female_list3
    #     all_list = Wake + RORR
    #
    #     X = np.corrcoef(all_list)
    #     # ax = sns.heatmap(X, center=0, cmap="YlGnBu")
    #
    #     # sort_list = sort_data(all_list)
    #     # x_ticks = ['', '', '', 'Wakefulness', '', '', '', '', '', '', 'RoRR', '', '', '', ]
    #     # y_ticks = ['Wakefulness', 'RoRR']
    #     """
    #         计算相关性，绘制热图
    #     """
    #     X = np.corrcoef(all_list)
    #     fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    #     # ax = sns.heatmap(X, center=0, cmap="Spectral", yticklabels=False, xticklabels=False, vmin=-1, vmax=1)
    #     ax = sns.heatmap(X, center=0, cmap="vlag", yticklabels=False, xticklabels=False, vmin=-1, vmax=1)
    #     # ax.set_xticklabels(['Wakefulness', 'RoRR'])
    #
    #     cbar = ax.collections[0].colorbar
    #     # here set the labelsize by 20
    #     cbar.ax.tick_params(labelsize=25)
    #     plt.tight_layout()
    #     plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/correlation'
    #                 '/SP_behavior_Wake_{}min_v2.tiff'.format(j * 5), dpi=300)
    #     plt.show()
    #     plt.close()


    """
        SP behavior 60min corr SP Arousal 60min
    """

    # """
    #         Wakefulness状态
    # """
    # a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min',
    #              name="video_info.xlsx", column="looming_time1", state_name="Male_Wakefulness")  # Male_Wakefulness
    # file_list_1 = []
    # for item in a['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min/new_results/BeAMapping-replace",
    #         name="{}_Movement_Labels".format(item))
    #     file_list_1.append(file_list1)
    # file_list_1 = list(np.ravel(file_list_1))
    #
    # b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min',
    #              name="video_info.xlsx", column="looming_time1", state_name="Female_Wakefulness")  # Female_Wakefulness
    # file_list_2 = []
    # for item in b['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min/new_results/BeAMapping-replace",
    #         name="{}_Movement_Labels".format(item))
    #     file_list_2.append(file_list1)
    # file_list_2 = list(np.ravel(file_list_2))
    #
    # Male_list = []
    # for i in range(len(file_list_1)):
    #     sub_list1 = pre_data(file_list_1[i], a, i, state="looming_time12")
    #     # print(sub_list1)
    #     Male_list.append(sub_list1)
    # # Male_list = sort_data(Male_list)
    #
    # Female_list = []
    # for i in range(len(file_list_2)):
    #     sub_list2 = pre_data(file_list_2[i], b, i, state="looming_time12")
    #     # print(sub_list2)
    #     Female_list.append(sub_list2)
    # # Female_list = sorted(Female_list)
    # # Female_list = sort_data(Female_list)
    #
    # Wake = Male_list + Female_list
    # # Wake = pd.DataFrame(Wake)
    #
    # """
    #     RORR状态
    # """
    # c = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
    #              name="video_info.xlsx", column="looming_time1", state_name="Male_RoRR")  # Male_Wakefulness
    # file_list_3 = []
    # for item in c['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list3 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
    #              r"/BeAMapping",
    #         name="{}_Movement_Labels".format(item))
    #     file_list_3.append(file_list3)
    # file_list_3 = list(np.ravel(file_list_3))
    #
    # d = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
    #              name="video_info.xlsx", column="looming_time1", state_name="Female_RoRR")  # Male_Wakefulness
    # file_list_4 = []
    # for item in d['Video_name'][0:10]:
    #     item = item.replace("-camera-0", "")
    #     file_list4 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
    #              r"/BeAMapping",
    #         name="{}_Movement_Labels".format(item))
    #     file_list_4.append(file_list4)
    # file_list_4 = list(np.ravel(file_list_4))
    #
    # for j in range(12, 14, 2):
    #     # Wake = []
    #     RORR = []
    #     state = 'looming_time{}'.format(j)
    #
    #     # Male_list = []
    #     # for i in range(len(file_list_1)):
    #     #     sub_list1 = pre_data(file_list_1[i], a, i, state=state)
    #     #     # print(sub_list1)
    #     #     Male_list.append(sub_list1)
    #     # # Male_list = sort_data(Male_list)
    #     # Female_list = []
    #     # for i in range(len(file_list_2)):
    #     #     sub_list2 = pre_data(file_list_2[i], b, i, state=state)
    #     #     # print(sub_list2)
    #     #     Female_list.append(sub_list2)
    #     # # Female_list = sorted(Female_list)
    #     # # Female_list = sort_data(Female_list)
    #     # Wake = Male_list + Female_list
    #     # # Wake = pd.DataFrame(Wake)
    #     # Wake = sort_data(Wake)
    #
    #     Male_RORR = []
    #     for i in range(len(file_list_3)):
    #         sub_list3 = pre_data(file_list_3[i], c, i, state=state)
    #         # print(sub_list2)
    #         Male_RORR.append(sub_list3)
    #     # Male_RORR = sort_data(Male_RORR)
    #
    #     Female_RORR = []
    #     for i in range(len(file_list_4)):
    #         sub_list4 = pre_data(file_list_4[i], d, i, state=state)
    #         # print(sub_list2)
    #         Female_RORR.append(sub_list4)
    #     # Female_RORR = sort_data(Female_RORR)
    #
    #     RORR = Male_RORR + Female_RORR
    #     RORR = sort_data(RORR)
    #
    #     # all_list = Male_list + Female_list + Female_list2 + Female_list3
    #     all_list = Wake + RORR
    #
    #     X = np.corrcoef(all_list)
    #     # ax = sns.heatmap(X, center=0, cmap="YlGnBu")
    #
    #     # sort_list = sort_data(all_list)
    #     # x_ticks = ['', '', '', 'Wakefulness', '', '', '', '', '', '', 'RoRR', '', '', '', ]
    #     # y_ticks = ['Wakefulness', 'RoRR']
    #     """
    #         计算相关性，绘制热图
    #     """
    #     X = np.corrcoef(all_list)
    #     fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    #     # ax = sns.heatmap(X, center=0, cmap="Spectral", yticklabels=False, xticklabels=False, vmin=-1, vmax=1)
    #     ax = sns.heatmap(X, center=0, cmap="vlag", yticklabels=False, xticklabels=False, vmin=-1, vmax=1)
    #     # ax.set_xticklabels(['Wakefulness', 'RoRR'])
    #
    #     cbar = ax.collections[0].colorbar
    #     # here set the labelsize by 20
    #     cbar.ax.tick_params(labelsize=25)
    #     plt.tight_layout()
    #     plt.show()
    #     # plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/correlation/Wake_RORR'
    #     #             '/SP_Wake_RORR_{}min_v3.tiff'.format(j * 5), dpi=300, transparent=True)
    #     # plt.close()


    """
        looming wake corr Rorr
    """

    """
                Wakefulness状态
    """
    a = read_csv(path=r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new',
                 name="video_info.xlsx", column="looming_time1", state_name="Male_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    for item in a['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new\BeAOutputs\csv_file_output_new",
            name="{}_Movement_Labels".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new',
                 name="video_info.xlsx",
                 column="looming_time1", state_name="Female_Wakefulness")  # Female_Wakefulness

    file_list_2 = []
    for item in b['Video_name'][0:6]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new\BeAOutputs\csv_file_output_new",
            name="{}_Movement_Labels".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    Male_list = []
    for i in range(len(file_list_1)):
        sub_list1 = pre_data(file_list_1[i], a, i, state="looming_time1")
        # print(sub_list1)
        Male_list.append(sub_list1)
    Male_list = sort_data(Male_list)

    Female_list = []
    for i in range(len(file_list_2)):
        sub_list2 = pre_data(file_list_2[i], b, i, state="looming_time1")
        # print(sub_list2)
        Female_list.append(sub_list2)
    Female_list = sorted(Female_list)
    # Female_list = sort_data(Female_list)

    Wake = Male_list + Female_list
    # Wake = pd.DataFrame(Wake)

    """
        RORR状态
    """
    c = read_csv(path=r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new',
                 name="video_info.xlsx", column="looming_time1", state_name="Male_RoRR")  # Male_Wakefulness

    file_list_3 = []
    for item in c['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list3 = search_csv(
            path=r"D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new\BeAOutputs\csv_file_output_new",
            name="{}_Movement_Labels".format(item))
        file_list_3.append(file_list3)
    file_list_3 = list(np.ravel(file_list_3))

    d = read_csv(path=r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new',
                 name="video_info.xlsx",
                 column="looming_time1", state_name="Female_RoRR")  # Female_Wakefulness

    file_list_4 = []
    for item in d['Video_name'][0:6]:
        item = item.replace("-camera-0", "")
        file_list4 = search_csv(
            path=r"D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new\BeAOutputs\csv_file_output_new",
            name="{}_Movement_Labels".format(item))
        file_list_4.append(file_list4)
    file_list_4 = list(np.ravel(file_list_4))

    for j in range(1, 5, 1):
        # Wake = []
        RORR = []
        state = 'looming_time{}'.format(j)

        # Male_list = []
        # for i in range(len(file_list_1)):
        #     sub_list1 = pre_data(file_list_1[i], a, i, state=state)
        #     # print(sub_list1)
        #     Male_list.append(sub_list1)
        # # Male_list = sort_data(Male_list)
        # Female_list = []
        # for i in range(len(file_list_2)):
        #     sub_list2 = pre_data(file_list_2[i], b, i, state=state)
        #     # print(sub_list2)
        #     Female_list.append(sub_list2)
        # # Female_list = sorted(Female_list)
        # # Female_list = sort_data(Female_list)
        # Wake = Male_list + Female_list
        # # Wake = pd.DataFrame(Wake)
        # Wake = sort_data(Wake)

        Male_RORR = []
        for i in range(len(file_list_3)):
            sub_list3 = pre_data(file_list_3[i], c, i, state=state)
            # print(sub_list2)
            Male_RORR.append(sub_list3)
        # Male_RORR = sort_data(Male_RORR)

        Female_RORR = []
        for i in range(len(file_list_4)):
            sub_list4 = pre_data(file_list_4[i], d, i, state=state)
            # print(sub_list2)
            Female_RORR.append(sub_list4)
        # Female_RORR = sort_data(Female_RORR)

        RORR = Male_RORR + Female_RORR
        # RORR = sort_data(RORR)

        # all_list = Male_list + Female_list + Female_list2 + Female_list3
        all_list = Wake + RORR

        X = np.corrcoef(all_list)
        # ax = sns.heatmap(X, center=0, cmap="YlGnBu")

        # sort_list = sort_data(all_list)
        # x_ticks = ['', '', '', 'Wakefulness', '', '', '', '', '', '', 'RoRR', '', '', '', ]
        # y_ticks = ['Wakefulness', 'RoRR']
        """
            计算相关性，绘制热图
        """
        X = np.corrcoef(all_list)
        fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
        # ax = sns.heatmap(X, center=0, cmap="Spectral", yticklabels=False, xticklabels=False, vmin=-1, vmax=1)
        ax = sns.heatmap(X, center=0, cmap="vlag", yticklabels=False, xticklabels=False, vmin=-1, vmax=1)
        # ax.set_xticklabels(['Wakefulness', 'RoRR'])

        cbar = ax.collections[0].colorbar
        # here set the labelsize by 20
        cbar.ax.tick_params(labelsize=25)
        plt.tight_layout()
        plt.show()
        plt.savefig(r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Analysis\corr_matrix\looming'
                    '/Wake_RORR_looming_time{}_v23.tiff'.format(j), dpi=300, transparent=True)
        plt.close()
