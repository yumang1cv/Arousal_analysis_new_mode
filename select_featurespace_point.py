# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 09:31:58 2021

@author: 12517
"""

# selet point
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
import matplotlib.colors as mcolors

df_nearest = pd.read_csv('E:/Analysis_video/Arousal_data/results/df_nearest1.csv')
c = mcolors.CSS4_COLORS

# df_random = df_random[(df_random['z'] > 0)]
df_nearest = df_nearest[(df_nearest['z'] < 0)]
# df_nearest = df_nearest[(df_nearest['z'] > 0)]
# # df_random = df_random[(df_random['z'] > 0.1) & (df_random['z'] < 6)]
# # df_nearest = df_nearest[(df_nearest['z'] > 0.1) & (df_nearest['z'] < 6)]

fig, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(8, 6), dpi=300)

ax2 = fig.add_subplot(111, projection='3d')
for i in df_nearest['movement_label'].unique():
    # if i not in [34]:
    #     label = i
    #     temp_df = df_nearest[df_nearest['movement_label'] == i]
    #     x, y, z = temp_df['x'], temp_df['y'], temp_df['z']
    #     ax2.scatter(x, y, z, color=list(c.values())[i + 5], s=5)
    #     ax2.text(x.tolist()[0], y.tolist()[0], z.tolist()[0], s=label, fontsize=10)

    label = i
    temp_df = df_nearest[df_nearest['movement_label'] == i]
    x, y, z = temp_df['x'], temp_df['y'], temp_df['z']
    ax2.scatter(x, y, z, color=list(c.values())[i + 5], s=5)
    ax2.text(x.tolist()[0], y.tolist()[0], z.tolist()[0], s=label, fontsize=10)

# for i in df_nearest['movement_label'].unique():
#     label = i
#     temp_df = df_nearest[df_nearest['movement_label'] == i]
#     x, y, z = temp_df['x'], temp_df['y'], temp_df['z']
#     ax2.scatter(x, y, z, color=list(c.values())[i + 5], s=5)
#     ax2.text(x.tolist()[0], y.tolist()[0], z.tolist()[0], s=label, fontsize=10)

# ax2.remove()
# plt.xticks([]), plt.yticks([])
ax2.set_title('nearest 50 points from each 40 cluster')
ax2.set_xlabel("umap1")
ax2.set_ylabel("umap2")
ax2.set_zlabel("zs_velocity")
ax2.grid(False)
ax2.view_init(90, 0)
plt.show()
