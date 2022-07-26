# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 20:34:12 2021

@author: Administrator
"""

import sys
# sys.path.append('Y:/sunchunhui/code/3D_level_correction')
sys.path.append('D:/3D_behavior/Arousal_behavior/Arousal_result_all/code/3D_level_correction')



import os
import glob
import tqdm
import pandas as pd
from natsort import natsorted

import Rot_ground_screen as rgs
from Toc3d import to_c3d


header_num = 3
# work_path = 'Y:/sunchunhui/Cloudplatform/history_data_results/sichuan_kangchengxinchuang/2022-0317/results'
work_path = 'D:/3D_behavior/Arousal_behavior/Arousal_result_all'
data_path = natsorted(glob.glob(os.path.join(work_path, '3Dskeleton/Calibrated_3DSkeleton', '*_Cali_Data3d.csv')))

save_path = os.path.join(work_path, '3Dskeleton/Calibrated_3DSkeleton_level')
if not os.path.exists(save_path):
    os.makedirs(save_path)


for path in tqdm.tqdm(data_path, desc='3D Level'):
    csv_data = pd.read_csv(path, index_col=None, header=list(range(0,header_num)))
    
    rotate_data = rgs.Rot_2_ground(csv_data, choice_order=True, filter_window=89)
    
    df_rotate_data = pd.DataFrame(rotate_data)
    df_rotate_data.columns = csv_data.columns
    
    save_csv_path = os.path.join(save_path, os.path.basename(path))
    # print(save_csv_path)
    df_rotate_data.to_csv(save_csv_path, index=0)
    
    if header_num == 3:
        FPS = csv_data.columns.get_level_values(2).to_list()[0].split(':')[1]
    else:
        FPS = 30
        # print("默认 FPS=30")
    to_c3d(FPS, save_csv_path, header_num)







