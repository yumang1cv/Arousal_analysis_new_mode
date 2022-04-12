# -*- coding:utf-8 -*-
# @FileName  :SP_behavior_60fang_activeline.py
# @Time      :2022/4/11 20:22
# @Author    :XuYang
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

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

male_day = pd.read_csv(
    r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/active_line/Male_RORR_active.csv')

female_day = pd.read_csv(r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/active_line'
                         r'/Female_RORR_active.csv')

del male_day['Unnamed: 0']
del female_day['Unnamed: 0']


def dataframe_norm(input_data):
    x = input_data.values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    norm_data = pd.DataFrame(x_scaled)

    return norm_data


male_data = dataframe_norm(male_day)
female_data = dataframe_norm(female_day)

"""
    PCA code
"""
# male_day_data = male_day.values
# male_day_data_1 = male_day_data.tolist()
# # X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
#
# pca = PCA(n_components=2)
# newX = pca.fit_transform(male_day_data_1)  # 等价于pca.fit(X) pca.transform(X)
# newX = [-l for l in newX]
# # invX = pca.inverse_transform(male_day_data_1)
# print(pca.explained_variance_ratio_)
# newX_1 = pd.DataFrame(newX, columns=['PCA1', 'PCA2'])
# newX_1['time'] = [i for i in range(1, 61)]
# sns.lineplot(data=newX_1, x="time", y="PCA1")
# sns.scatterplot(data=newX_1, x="PCA1", y="PCA2")


"""
    t-SNE code
"""
# X_embedded = TSNE(n_components=1, learning_rate='auto', init='random').fit_transform(male_day_data_1)

# pca_tsne = TSNE(n_components=1)
# newMat = pca_tsne.fit_transform(male_day_data)
# newMat = pd.DataFrame(newMat, columns=['PCA1'])
# newMat['time'] = [i for i in range(1, 61)]
# sns.lineplot(data=newMat, x="time", y="PCA1")

# x = newX[:, 0]
# y = [i for i in range(1, 61)]
# y = np.array(y)
# with warnings.catch_warnings():
#     warnings.simplefilter('ignore', np.RankWarning)
#     p30 = np.poly1d(np.polyfit(x, y, 30))
#
# xp = np.linspace(1, 61, 1)
# _ = plt.plot(x, y, '.', xp, p30(xp), '--')

"""
    加权求和
"""
data = female_data
active_value = []
for i in range(len(data)):
    active_data = data.iloc[i, 2] + data.iloc[i, 3] + data.iloc[i, 9] + \
                                   data.iloc[i, 10] - data.iloc[i, 11]
    # data['active_value'].iloc[i] = 11 * data.iloc[i, 2] + 27 * data.iloc[i, 3] + 2 * data.iloc[i, 9] + \
    #                                5 * data.iloc[i, 10] - 45 * data.iloc[i, 11]
    active_value.append(active_data)

data['active_value'] = active_value

data.to_csv('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/active_line/Female_RORR_active_value_bili1.csv')

# sns.scatterplot(data=male_day, x="time", y="mean")


# def pre_data(data_name, statename):
#     data_list = data_name
#     name = '{}'.format(statename)
#     cali_data = []
#     for i in range(len(data_list)):
#         a = data_list.iloc[i, 0] + data_list.iloc[i, 1] + data_list.iloc[i, 2] + data_list.iloc[i, 3] + \
#             data_list.iloc[i, 5] + data_list.iloc[i, 9] - data_list.iloc[i, 8] - data_list.iloc[i, 13]
#         cali_data.append(a)
#
#     data_list['mean'] = cali_data
#     data_list['time'] = [i for i in range(delay, 60 + delay, delay)]  # 间隔时长
#     data_list["species"] = ['{}'.format(name)] * int(60 / delay)  # 间隔时长
#     # data_list['time'] = [i for i in range(10, 70, 10)]
#     # data_list["species"] = ['{}'.format(name)] * 6
#     return data_list
#
#
# male_day_data = pre_data(male_day, 'male_day')
# male_night_data = pre_data(male_night, 'male_night')
# female_day_data = pre_data(female_day, 'female_day')
# female_night_data = pre_data(female_night, 'female_night')
# data = pd.concat([male_day_data, male_night_data, female_day_data, female_night_data], ignore_index=True)
# # data = male_day_data
# # sns.lmplot(data=data, x="time", y="mean", hue="species")
#
# violon_color = ['#FFC75F', '#00C9A7', '#D65DB1', '#0081CF']
# fig = plt.figure(figsize=(8, 5), dpi=300)
# ax = fig.add_subplot(111)
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
# # chord_diagram(flux, names, gap=0.03, use_gradient=True, sort='distance', cmap=color,
# #               chord_colors=colors,
# #               rotate_names=True, fontcolor="grey", ax=ax, fontsize=10)
# # sns.lineplot(data=data, x="time", y="mean", hue="species", color=violon_color)
# # sns.set(style="ticks", font='cmr10')
# sns.lineplot(data=data, x="time", y="mean", hue="species", palette=violon_color)
# plt.xticks(fontsize=12)
# # ax.yaxis.set_ticks([-0.05, 0, 0.05, 0.1, 0.15])
# plt.yticks(fontsize=12)
# # str_grd = "_gradient" if grads[0] else ""
#
# plt.xlabel('Time (min)', fontsize=15)
# plt.ylabel('Fraction', fontsize=15)
# plt.tight_layout()
# plt.show()
# plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline/fang_data'
#             '/figure/active_line_{}min.tiff'.format(delay), dpi=300)
# plt.close()
#
"""
    fit data plot
"""
# # fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
# # ax = fig.add_subplot(111)
# ax = sns.lmplot(data=data, x="time", y="mean", hue="species", palette=violon_color,
#                 height=7, aspect=1.4, legend=False)
# # ax = sns.lmplot(data=data, x="time", y="mean", hue="species", palette=violon_color)
# ax.set_axis_labels("Time (min)", "Fraction", fontsize=20)
# # ax.fig.set_figwidth(8)
# # ax.fig.set_figheight(5)
# # sns.set(rc={'figure.figsize': (8, 8)})
# """
#     下面2行一块使用
# """
# ax.set(xticks=np.arange(0, 60, 5), yticks=np.arange(-0.3, 0.5, 0.1))
# ax.set_xticklabels(np.arange(0, 60, 5), rotation=0, size=15)
# # ax.set(xticks=np.arange(delay, 60+delay, delay*5))
# # ax.set_xticklabels(np.arange(delay, 60+delay, delay*5), rotation=0, size=15)
#
# # ax.set_yticklabels(np.arange(-1, 1.6, 0.5), rotation=0, size=15)
# # ax.set_xticklabels(np.arange(0, 61, 10), size=15)
# ax.set_yticklabels(size=15)
# plt.legend(bbox_to_anchor=(1, 0), loc=3, borderaxespad=0, fontsize=18, frameon=False)
# ax.tight_layout()
# # plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline/fang_data'
# #             '/figure/active_fitline_{}min.tiff'.format(delay), dpi=300)
