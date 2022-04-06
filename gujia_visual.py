# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 21:39:51 2021

@author: 12517
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import seaborn as sns

'''data_input'''
df = pd.read_csv(r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/3Dskeleton/Calibrated_3DSkeleton/'
                 r'rec-4-M-20211201110704_Cali_Data3d.csv')  # read file
df1 = np.transpose(df[0:len(df)])

a = []
b = []
c = []
# Frame_num = 20092
# for i in range(0, 47, 3):
#     x = np.float64(df1.iloc[[i], [Frame_num]].values[0][0])
#     y = np.float64(df1.iloc[[i + 1], [Frame_num]].values[0][0])
#     z = np.float64(df1.iloc[[i + 2], [Frame_num]].values[0][0])
#
#     a.append(x)
#     b.append(y)
#     c.append(z)


def get_data(dataframe, fps_num):
    # a = []
    # b = []
    # c = []
    for i in range(0, 47, 3):
        x = np.float64(dataframe.iloc[[i], [fps_num]].values[0][0])
        y = np.float64(dataframe.iloc[[i + 1], [fps_num]].values[0][0])
        z = np.float64(dataframe.iloc[[i + 2], [fps_num]].values[0][0])

        a.append(x)
        b.append(y)
        c.append(z)

    return a, b, c


def point_connnet(list_a, list_b, list_c, x, y):
    # ax.scatter([list_a[x], list_a[y]], [list_b[x], list_b[y]], [list_c[x], list_c[y]])
    ax.plot([list_a[x], list_a[y]], [list_b[x], list_b[y]], [list_c[x], list_c[y]], color='black')

    return


def plane_vis(list_a, list_b, list_c, x, y, z):
    vertices = [list(
        zip([list_a[x], list_a[y], list_a[z]], [list_b[x], list_b[y], list_b[z]], [list_c[x], list_c[y], list_c[z]]))]
    # poly = Poly3DCollection(vertices, alpha=0.8, edgecolors='blue', facecolors='gray')
    poly = Poly3DCollection(vertices, alpha=0.8, facecolors='#ececea')
    ax.add_collection3d(poly)

    return


def point_color(list_a, list_b, list_c, point_size):
    # ax.scatter(list_a[z], list_b[x], list_c[y], c=color, s=point_size)

    ax.scatter(list_a[0:3], list_b[0:3], list_c[0:3], c='goldenrod', s=point_size)  # Nose、Left_ear、Right_ear
    ax.scatter(list_a[4:12], list_b[4:12], list_c[4:12], c='lightseagreen', s=point_size)  # Limb、Claw
    ax.scatter(list_a[3:4], list_b[3:4], list_c[3:4], c='crimson', s=point_size)  # Back
    ax.scatter(list_a[12:16], list_b[12:16], list_c[12:16], c='crimson', s=point_size)  # Tail

    return


"""
    nose:0    left_ear:1   Right_ear:2    neck:3    left_front_limb:4     right_front_limb:5     left_hind_limb:6     right_hind_limb:7
    left_front_claw:8      right_front_claw:9       left_hind_claw:10     right_hind_claw:11     back:12              
    root_tail:13           mid_tail:14              tip_tail:15
"""

if __name__ == "__main__":
    get_data(df1, 12645)     # 帧数

    fig = plt.figure(figsize=(10, 10), dpi=300)
    # plt.style.use("dark_background")
    ax = fig.add_subplot(111, projection='3d')

    plane_vis(a, b, c, 0, 1, 2)
    plane_vis(a, b, c, 0, 1, 3)
    plane_vis(a, b, c, 0, 2, 3)
    plane_vis(a, b, c, 1, 2, 3)
    plane_vis(a, b, c, 3, 4, 8)
    plane_vis(a, b, c, 5, 8, 3)
    plane_vis(a, b, c, 5, 9, 3)
    plane_vis(a, b, c, 3, 4, 9)
    plane_vis(a, b, c, 4, 5, 12)
    plane_vis(a, b, c, 4, 12, 6)
    plane_vis(a, b, c, 7, 5, 12)
    plane_vis(a, b, c, 7, 6, 12)
    plane_vis(a, b, c, 4, 6, 10)
    plane_vis(a, b, c, 7, 5, 11)
    plane_vis(a, b, c, 7, 6, 13)
    # plane_vis(a, b, c, 7, 8, 10)

    point_connnet(a, b, c, 0, 1)  # nose2Lear
    point_connnet(a, b, c, 0, 2)  # nose2Rear
    point_connnet(a, b, c, 1, 2)  # Lear2Rear
    point_connnet(a, b, c, 1, 3)  # Lear2Neck
    point_connnet(a, b, c, 2, 3)  # Rear2Neck
    point_connnet(a, b, c, 3, 4)  # Neck2LFLimb
    point_connnet(a, b, c, 3, 5)  # Neck2RFLimb
    point_connnet(a, b, c, 4, 8)  # LFLimb2LFClaw
    point_connnet(a, b, c, 5, 9)  # RFLimb2RFClaw
    point_connnet(a, b, c, 4, 6)  # LFLimb2LHLimb
    point_connnet(a, b, c, 5, 7)  # RFLimb2RHLimb
    point_connnet(a, b, c, 6, 10)  # LHLimb2LHClaw
    point_connnet(a, b, c, 7, 11)  # RHLimb2RHClaw
    point_connnet(a, b, c, 6, 13)  # LHLimb2Rtail
    point_connnet(a, b, c, 7, 13)  # RHLimb2Rtail
    point_connnet(a, b, c, 14, 13)  # Rtail2Mtail
    point_connnet(a, b, c, 4, 12)  # LFLimb2Back
    point_connnet(a, b, c, 5, 12)  # RFLimb2Back
    point_connnet(a, b, c, 6, 12)  # LHLimb2Back
    point_connnet(a, b, c, 7, 12)  # RHLimb2Back
    point_connnet(a, b, c, 14, 15)  # Mtail2Ttail
    # ax.set_xlim(0, 200)
    # ax.set_ylim(-200, 200)
    # ax.set_zlim(0, 600)
    point_color(a, b, c, 10)
    # ax.scatter(a[0:2], b[0:2], c[0:2], c='#965454', s=5)
    plt.axis('off')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    plt.show()
