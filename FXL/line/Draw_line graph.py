# -*- coding: utf-8 -*-
"""
Created on Tue May 25 22:00:11 2021

@author: 43865
"""

import matplotlib.pyplot as plt
import numpy as np
import xlrd
import matplotlib.patches as mpathes

wb = xlrd.open_workbook(r'D:/3D_behavior/Spontaneous_behavior/code/FXL/line/draw_line.xls')
x = np.arange(0.5, 13.5, 1)
plt.figure(figsize=(9, 3), dpi=1000)


# 设置颜色
def change(R, G, B):
    r = round(R / 255, 6);
    g = round(G / 255, 6);
    b = round(B / 255, 6)
    c = [r, g, b]
    return c


# 准备第二组数据 雄鼠
y = wb.sheet_by_index(0).col_values(4)[1:14]
plt.plot(x, y, linewidth=0.8, color=change(200, 222, 249),
         label='Male')  # Cre组：female(255,224,224) (255,200,200)   male(185,225,238)
y_lower = wb.sheet_by_index(0).col_values(5)[1:14]
y_upper = wb.sheet_by_index(0).col_values(6)[1:14]
plt.fill_between(x, y_lower, y_upper, linewidth=0.3, color=change(200, 222, 249), alpha=0.45)  # 阴影颜色

# 准备第一组数据 雌鼠
y0 = wb.sheet_by_index(0).col_values(0)[1:14]
plt.plot(x, y0, linewidth=0.8, color=change(255, 224, 224),
         label='Female')  # GFP组：female(223,223,223) (200 *3)     male(253, 221,178)
y_lower0 = wb.sheet_by_index(0).col_values(1)[1:14]
y_upper0 = wb.sheet_by_index(0).col_values(2)[1:14]
plt.fill_between(x, y_lower0, y_upper0, linewidth=0.3, color=change(255, 224, 224), alpha=0.45)  # 阴影颜色

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
font1 = {'family': 'Arial', 'weight': 'bold', 'size': 24}

# 设置y轴
ax.yaxis.set_ticks_position('left')
# ax.spines['left'].set_position(('axes',-0.03)) 
ax.spines['left'].set_position(('data', 0))
ax.spines['left'].set_linewidth(1.5)
ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
# ax.set_yticklabels('')
ax.set_yticklabels([0, 0.1, 0.2, 0.3, 0.4, 0.5], fontfamily='Arial', fontsize=10, fontweight='bold')
ax.set_ylim([0, 0.5])
# ax.set_ylabel('Fractions',font1)

# #设置x轴
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', -0.0025))
ax.spines['bottom'].set_linewidth(1.5)
ax.set_xticks(np.arange(0.5, 40.5, 1))
ax.set_xticklabels('')
ax.set_xlim([0, 13])
# ax.set_xlabel('Time (s)',fontdict=font1)  #labelpad= 115
# plt.annotate('6', (5.43,0.78),fontfamily='Arial',fontsize=11)
# plt.annotate('*', (5.45,0.72),fontfamily='Arial',fontsize=11)

# plt.annotate('2', (1.405,0.28),fontfamily='Arial')
# plt.annotate('*', (1.43,0.22),fontfamily='Arial')


# m=[-5,-5]
# n=[-2.99,2.99]
# plt.plot(m,n,'black')

# 添加looming示意阴影
# rect = mpathes.Rectangle([-0,-2],5,4,color=change(0,0,0),alpha=0.1)
# ax.add_patch(rect)


# plt.title('Male',font1)
plt.legend(loc='upper right')  # 图注
plt.tick_params(width=1.5)
# plt.savefig(r'draw_line_0625.png')
plt.show()
