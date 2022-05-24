import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA
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

"""
    Locomotion : 4-Walking   11-Trotting  16-Stepping  14-Running  13-Flight  2-Left turning  1-Right turning
    Exploration : 10-Standing  6-Climbing  7-Falling  3-Sniffing
    Maintenance : 12-Grooming
    Non-locomtion : 8-Immobility
    Posture : 15-LORR  9-Paralysis  5-Trembling
"""

behavior_labels = ['Right turning', 'Left turning', 'Sniffing', 'Walking', 'Trembling',
                   'Climbing', 'Falling', 'Immobility', 'Paralysis', 'Standing',
                   'Trotting', 'Grooming', 'Flight', 'Running', 'LORR', 'Stepping']

group_1 = ['Walking', 'Trotting', 'Stepping', 'Running', 'Flight', 'Left turning', 'Right turning']
# group_1 = ['Walking', 'Trotting', 'Flight', 'Running', 'Stepping']
group_1_index = []
for item in group_1:
    # print(behavior_labels.index(item))
    group_1_index.append(behavior_labels.index(item))

group_1_index = sorted(group_1_index)
group_2_index = list(set([i for i in range(16)]) - set(group_1_index))
group_2 = []
for item in group_2_index:
    group_2.append(behavior_labels[item])
# group_2 = list(set(behavior_labels) - set(group_1))
# group_2 = group_1.pop(group_1_index)


data = 'FM_looming'
df1 = pd.read_excel('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/Radar_chart'
                    '/looming/{}.xlsx'.format(data), sheet_name='Wake')

df2 = pd.read_excel('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/Radar_chart'
                    '/looming/{}.xlsx'.format(data), sheet_name='looming_1')

df3 = pd.read_excel('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/Radar_chart'
                    '/looming/{}.xlsx'.format(data), sheet_name='looming_2')

df4 = pd.read_excel('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/Radar_chart'
                    '/looming/{}.xlsx'.format(data), sheet_name='looming_3')

df5 = pd.read_excel('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/Radar_chart'
                    '/looming/{}.xlsx'.format(data), sheet_name='looming_4')


# df6 = pd.read_excel('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/Radar_chart'
#                     '/looming/{}.xlsx'.format(data), sheet_name='looming_5')
#
# df7 = pd.read_excel('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/Radar_chart'
#                     '/looming/{}.xlsx'.format(data), sheet_name='looming_6')


def data_list(data):
    behavior_fre1 = []
    behavior_label_all1 = []
    for i in range(len(data.T)):
        x = data.iloc[:, i].tolist()
        behavior_fre1.append(x)
        behavior_label = [i] * len(data)
        behavior_label_all1.append(behavior_label)

    behavior_fre1 = list(np.ravel(behavior_fre1))
    behavior_label_all1 = list(np.ravel(behavior_label_all1))
    return behavior_fre1, behavior_label_all1


def data_reduceD(data):
    values = data.T.iloc[:, :]  # 读取前4列数据
    pca1 = PCA(n_components=2)  # 选取2个主成分
    pc1 = pca1.fit_transform(values)
    x = pca1.components_[0]
    y = pca1.components_[1]
    # print(pca1.components_[0])
    # print("explained variance ratio: %s" % pca1.explained_variance_ratio_)
    return x, y


def del_data(data_name, del_list):
    data_name = data_name.drop(data_name.columns[del_list], axis=1)  # df.columns is zero-based pd.Index
    return data_name


def pre_data(data, label_list):
    # Each attribute we'll plot in the radar chart.
    labels = label_list
    # Let's look at the 1970 Chevy Impala and plot it.
    values = data.iloc[len(data) - 1, 0:17].tolist()
    # Number of variables we're plotting.
    num_vars = len(labels)
    # Split the circle into even parts and save the angles
    # so we know where to put each axis.
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    # The plot is a circle, so we need to "complete the loop"
    # and append the start value to the end.
    values += values[:1]
    angles += angles[:1]

    return values, angles


if __name__ == '__main__':
    """
        分组code
    """
    delete_list = group_2_index
    labels = group_1
    # labels = behavior_labels

    df1 = del_data(df1, delete_list)
    df2 = del_data(df2, delete_list)
    df3 = del_data(df3, delete_list)
    df4 = del_data(df4, delete_list)
    df5 = del_data(df5, delete_list)
    # # df6 = del_data(df6, delete_list)
    # # df7 = del_data(df7, delete_list)
    # labels = behavior_labels
    df5.iloc[:, 3:4] = 0
    """
        雷达图
    """
    # data = df1
    # # Each attribute we'll plot in the radar chart.
    num_vars = len(labels)
    # # Let's look at the 1970 Chevy Impala and plot it.
    # values = data.iloc[len(data) - 1, 0:17].tolist()
    # values2 = df2.iloc[len(data) - 1, 0:17].tolist()
    # values3 = df3.iloc[len(data) - 1, 0:17].tolist()
    # values4 = df4.iloc[len(data) - 1, 0:17].tolist()
    # values5 = df5.iloc[len(data) - 1, 0:17].tolist()
    # # Number of variables we're plotting.

    # # Split the circle into even parts and save the angles
    # # so we know where to put each axis.
    # angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    # # The plot is a circle, so we need to "complete the loop"
    # # and append the start value to the end.
    # values += values[:1]
    # angles += angles[:1]
    #
    # values2 += values2[:1]
    # values3 += values3[:1]
    # values4 += values4[:1]
    # values4 += values5[:1]
    values1, angles1 = pre_data(df1, labels)
    values2, angles2 = pre_data(df2, labels)
    values3, angles3 = pre_data(df3, labels)
    values4, angles4 = pre_data(df4, labels)
    values5, angles5 = pre_data(df5, labels)
    # values6, angles6 = pre_data(df6, labels)
    # values7, angles7 = pre_data(df7, labels)
    line_width = 2
    # ax = plt.subplot(polar=True)
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(polar=True), dpi=300)
    plt.style.use('ggplot')
    # Draw the outline of our data.
    ax.plot(angles1, values1, color='#d8b0b0', linewidth=line_width, label='Wakefulness')
    # Fill it in.
    # ax.fill(angles1, values1, color='#D65DB1', alpha=0.1)

    # ax.plot(angles2, values2, color='#59ccf3', linewidth=1, label="0-10")
    # # # Fill it in.
    # # ax.fill(angles, values1, color='#0081CF', alpha=0.1)
    # #
    # ax.plot(angles3, values3, color='#247aae', linewidth=1, label='11-20')
    # # # Fill it in.
    # # ax.fill(angles, values2, color='#FFC75F', alpha=0.1)
    # ax.plot(angles4, values4, color='#d5aa84', linewidth=1, label='21-30')
    # ax.plot(angles5, values5, color='#f5a17b', linewidth=1, label='31-40')
    # ax.plot(angles6, values6, color='#7b374c', linewidth=1, label='41-50')
    # ax.plot(angles7, values7, color='#5d3f8a', linewidth=1, label='51-60')

    ax.plot(angles2, values2, color='#bebebe', linewidth=line_width, label="Stage 1")
    # # Fill it in.
    # ax.fill(angles, values1, color='#0081CF', alpha=0.1)
    #
    ax.plot(angles3, values3, color='#8babd3', linewidth=line_width, label='Stage 2')
    # # Fill it in.
    # ax.fill(angles, values2, color='#FFC75F', alpha=0.1)
    ax.plot(angles4, values4, color='#808080', linewidth=line_width, label='Stage 3')
    ax.plot(angles5, values5, color='#f5a17b', linewidth=line_width, label='Stage 4')

    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # for labels, angles in zip(labels, range(0, np.pi, 24)):
    #     if angles <= 180:
    #         labels.set_rotation(np.pi / 2 - angles)
    #     else:
    #         labels.set_rotation(2*np.pi / 3 - angles)

    # Draw axis lines for each angle and label.
    ax.set_thetagrids(np.degrees(angles1[0:len(angles1) - 1]), labels, fontsize=15, weight="bold")

    # Go through labels and adjust alignment based on where
    # it is in the circle.
    for label, angle in zip(ax.get_xticklabels(), angles1):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    # Ensure radar goes from 0 to 100.
    # ax.set_ylim(0, 1400)
    ax.set_ylim(0, 400)
    plt.yticks(fontsize=12)
    # ax.set(ytickets=None)
    # You can also set gridlines manually like this:
    # ax.set_rgrids([20, 40, 60, 80, 100])

    # Set position of y-labels (0-100) to be in the middle
    # of the first two axes.
    ax.set_rlabel_position(180 / num_vars)
    # plt.legend(["first round", "second round", 'third_round'], loc='upper right')
    # Add some custom styling.
    # Change the color of the tick labels.
    ax.tick_params(colors='#222222')

    ax.tick_params(axis='y', labelsize=10, color='#AAAAAA')

    # Change the color of the circular gridlines.
    ax.grid(color='#AAAAAA', alpha=0.3)
    # Change the color of the outermost gridline (the spine).
    ax.spines['polar'].set_color('#222222')

    # Add a legend as well.
    # ax.legend(loc='upper right', bbox_to_anchor=(1.55, 1.15), fontsize=12, fancybox=True, framealpha=0.001)
    # ax.legend(loc='upper right', bbox_to_anchor=(1.55, 0.1), fontsize=15, fancybox=True, framealpha=0.001)
    plt.tight_layout()
    plt.savefig(
        "D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/Radar_chart"
        "/FM_looming_Locomotion_v12.tiff", dpi=300, transparent=True)
    # plt.savefig(
    #     "D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/behavior_fre/Radar_chart/{}_group1_V4"
    #     ".tiff".format(data), dpi=300, transparent=True)
    plt.show()
    plt.close()

    # import matplotlib
    # R = 190
    # G = 190
    # B = 190
    # print(matplotlib.colors.to_hex([R / 255, G / 255, B / 255]))
