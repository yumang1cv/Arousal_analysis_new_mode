#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 15:06:05 2021

@author: yejohnny
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

import matplotlib.style
import matplotlib as mpl

mpl.style.use('ggplot')

file = 'D:/3D_behavior/Spontaneous_behavior/result/3Dskeleton_result_all/rec-1-G1-20210916114230_Cali_Data3d.csv'
file2 = 'D:/3D_behavior/Spontaneous_behavior/result/BeAMapping/rec-1-G1-20210916114230_Movement_Labels.csv'
df1 = pd.read_csv(file, skiprows=range(1, 2))
neck_coor = df1.filter(like='neck')
back_coor = df1.filter(like='back')
back_coor.columns = ['x', 'y', 'z']

center = ((back_coor['x'].max() + back_coor['x'].min()) / 2, (back_coor['y'].max() + back_coor['y'].min()) / 2)
normalized_center_x = back_coor['x'] - center[0]
normalized_center_y = back_coor['y'] - center[1]

x_range = back_coor['x'].max() - back_coor['x'].min()
y_range = back_coor['y'].max() - back_coor['y'].min()

normalized_x = (normalized_center_x / x_range) * 500
normalized_y = (normalized_center_y / y_range) * 500

df2 = pd.DataFrame({'x': normalized_x, 'y': normalized_y})
df2['location'] = 'outside'
# inside_index = df2[np.logical_and(df2['x']>-125,df2['x']<125)&np.logical_and(df2['y']>-125,df2['y']<125)].index.to_list()
# df2.loc[inside_index,'location']='inside'

for i in range(df2.shape[0]):
    x = df2['x'][i]
    y = df2['y'][i]
    if (x * x + y * y) < 125 * 125:
        df2['location'][i] = 'inside'

df3 = pd.read_csv(file2, names=['movement'])

df3 = pd.concat([df2, df3], axis=1)

timeSeries_Proportion = []
begin_pos = 0
end_pos = 0
num = 0
for i in range(int(df3.shape[0] / 60), df3.shape[0] + 1, int(df3.shape[0] / 60)):
    num += 1
    end_pos = i
    temp_df = df3.iloc[begin_pos:end_pos, :]
    location = temp_df['location'].value_counts()

    begin_pos = end_pos
    frequence_count = temp_df['movement'].value_counts()
    df = pd.DataFrame(frequence_count.index, columns=['movement'])
    df['movement'].astype('str')
    df['frequence'] = frequence_count.values
    df['percentage'] = round(df['frequence'] / df['frequence'].sum(), 4)
    df['seg'] = num
    if len(location) < 2:
        if location.index[0] == 'outside':
            df['outside'] = location[0] / 300
        else:
            df['inside'] = location[1] / 300
    else:
        df['outside'] = location[0] / 300
        df['inside'] = location[1] / 300
    # print(df)
    timeSeries_Proportion.append(df)

all_df = pd.concat(timeSeries_Proportion)

df_forPlot_list = {'seg': [], 'movement': [], 'percentage': []}
for i in all_df['seg'].unique():
    for j in all_df['movement'].unique():
        percentage = all_df[(all_df['seg'] == i) & (all_df['movement'] == j)]['percentage']
        if percentage.empty:
            percentage = 0
        else:
            percentage = percentage.values[0]
        df_forPlot_list['seg'].append(i)
        df_forPlot_list['movement'].append(j)
        df_forPlot_list['percentage'].append(percentage)

df_forPlot = pd.DataFrame(df_forPlot_list)

colors = ['#4169E1', '#6495ED', '#1E90FF', '#87CEEB', '#E1FFFF',
          '#D4F2E7', '#AFEEEE', '#40E0D0', '#20B2AA', '#008B8B',
          '#3CB371', '#32CD32', '#00FF00', '#7FFF00', '#FFFF00',
          '#F0E68C', '#BDB76B', '#FFD700', '#DAA520', '#FFA500',
          '#FF8C00', '#D2691E', '#FF7F50', '#FA8072', '#FF6347',
          '#FF4500', '#A52A2A', '#800000', '#800080', '#9400D3',
          '#9932CC', '#BA55D3', '#9370DB', '#DDA0DD', '#EE82EE',
          '#FF00FF', '#FF00FF', '#4B0082', '#000080', '#2F4F4F',
          '#000000', '#696969', '#808080', '#A9A9A9', '#C0C0C0']
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8), constrained_layout=True)
b = np.zeros(60)
p = np.zeros(60)
num = 0
for i in df_forPlot['movement'].unique():
    temp_df = df_forPlot[df_forPlot['movement'] == i]
    p += temp_df['percentage'].values
    ax.bar(temp_df['seg'].values, p, bottom=b, label=i, width=1, color=colors[num])
    b += temp_df['percentage'].values
    num += 1

ax.set_xticks(np.arange(0, 61, 10))
ax.set_yticks(np.round(np.arange(0, 1.1, 0.2), 1))
ax.set_xticklabels(np.arange(0, 61, 10), family='arial', color='black', weight='normal', size=15)
ax.set_yticklabels(np.round(np.arange(0, 1.1, 0.2), 1), family='arial', color='black', weight='normal', size=15)
ax.set_xlabel('time', family='arial', color='black', weight='normal', size=20, labelpad=20)
ax.set_ylabel('percentage', family='arial', color='black', weight='normal', size=20, labelpad=20)
ax.set_ylim(0, 1)
ax.set_xlim(0.5, 60.5)

sns.lineplot(x='seg', y='inside', data=all_df, legend=False, linewidth=10)
sns.lineplot(x='seg', y='outside', data=all_df, legend=False, linewidth=10)
plt.show()

