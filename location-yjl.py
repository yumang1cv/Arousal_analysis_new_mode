#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 12:26:06 2021

@author: yejohnny
"""

import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec

# fir_dir = '/Users/yejohnny/Desktop/code/3D/Calibrated_3DSkeleton/rec-9-G1-20210825114230_Cali_Data3d.csv'
# file_name_list =

file = 'D:/3D_behavior/Spontaneous_behavior/result/3Dskeleton_result_all/rec-1-G1-20210916114230_Cali_Data3d.csv'
file2 = 'D:/3D_behavior/Spontaneous_behavior/result/BeAMapping/rec-1-G1-20210916114230_Movement_Labels.csv'
df1 = pd.read_csv(file, skiprows=range(1, 2))
neck_coor = df1.filter(like='neck')
back_coor = df1.filter(like='back')
back_coor.columns = ['x', 'y', 'z']

center = (
    (back_coor['x'].max() + back_coor['x'].min()) / 2, (back_coor['y'].max() + back_coor['y'].min()) / 2)  # 获取圆心位置
normalized_center_x = back_coor['x'] - center[0]  # 将圆心位置设置为原点
normalized_center_y = back_coor['y'] - center[1]  # 将圆心位置设置为原点

x_range = back_coor['x'].max() - back_coor['x'].min()
y_range = back_coor['y'].max() - back_coor['y'].min()

normalized_x = (normalized_center_x / x_range) * 500
normalized_y = (normalized_center_y / y_range) * 500  # 上面四行是将数据换到到真实比例，单位mm

df2 = pd.DataFrame({'x': normalized_x, 'y': normalized_y})
df2['location'] = 'outside'

for i in range(df2.shape[0]):
    x = df2['x'][i]
    y = df2['y'][i]
    if (x * x + y * y) < 125 * 125:
        df2['location'][i] = 'inside'  # 计算属于圆内的点

df3 = pd.read_csv(file2, names=['movement'])  # 获取行为标签

df2 = pd.concat([df2, df3], axis=1)

inside_time = df2['location'].value_counts(ascending=True)[0]
outside_time = df2['location'].value_counts(ascending=True)[1]  # 统计在圆内和园外的时间

df_inside = df2[df2['location'] == 'inside']
behavior_inside = df_inside['movement'].value_counts()
df_behavior_inside = pd.DataFrame(behavior_inside.index, columns=['movement'])
df_behavior_inside['relative_time'] = behavior_inside.values / inside_time  # 行为在圆内圆外相对时间
df_behavior_inside['location'] = 'inside'

df_outside = df2[df2['location'] == 'outside']
behavior_outside = df_outside['movement'].value_counts()
df_behavior_outside = pd.DataFrame(behavior_outside.index, columns=['movement'])
df_behavior_outside['location'] = 'outside'
df_behavior_outside['relative_time'] = behavior_outside.values / outside_time

df4 = pd.concat([df_behavior_outside, df_behavior_inside], axis=0)

fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2, figsize=(18, 8), constrained_layout=True)
ax1.scatter(0, 0, color='red')
sns.scatterplot(x=normalized_x, y=normalized_y, hue='location', data=df2, s=5, ax=ax1)
draw_circle = plt.Circle((0, 0), 125, color='y', alpha=0.3)
ax1.set_aspect(1)
ax1.add_artist(draw_circle)
ax1.set_xticks(np.arange(-250, 251, 100))
ax1.set_xticklabels(range(-25, 26, 10), family='arial', color='black', weight='normal', size=15)
ax1.set_yticks(np.arange(-250, 251, 100))
ax1.set_yticklabels(range(-25, 26, 10), family='arial', color='black', weight='normal', size=15)
ax1.set_xlabel('')
ax1.set_ylabel('')

sns.barplot(x='movement', y='relative_time', data=df4, ci=0)
ax2.set_xlabel('behavior type', family='arial', color='black', weight='normal', size=20, labelpad=6)
ax2.set_ylabel('relative_time(s)', family='arial', color='black', weight='normal', size=20, labelpad=10)
plt.show()

'''
fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2, figsize=(18, 8),constrained_layout=True)
ax1.scatter(0,0,color='red')
sns.scatterplot(x=normalized_x,y=normalized_y,hue='location',data=df2,s=5,ax=ax1)
draw_circle = plt.Circle((0, 0), 125, color='y',alpha=0.3)
ax1.set_aspect(1)
ax1.add_artist(draw_circle)
ax1.set_xticks(np.arange(-250,251,100))
ax1.set_xticklabels(range(-25,26,10),family='arial',color='black', weight='normal', size = 15)
ax1.set_yticks(np.arange(-250,251,100))
ax1.set_yticklabels(range(-25,26,10),family='arial',color='black', weight='normal', size = 15)
ax1.set_xlabel('')
ax1.set_ylabel('')

sns.countplot(data=df2, x='movement',ax=ax2,hue='location')
ax2.set_xlabel('behavior type',family='arial', color='black', weight='normal', size = 20,labelpad = 6)
ax2.set_ylabel('time(s)',family='arial', color='black', weight='normal', size = 20,labelpad = 10)
ax2.set_yticks(np.arange(0,2700,300))
ax2.set_yticklabels(range(0,90,10),family='arial',color='black', weight='normal', size = 15)
'''
