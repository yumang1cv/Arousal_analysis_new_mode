# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 13:46:44 2021

@author: kangh
"""

import os
import ezc3d
import numpy as np
import pandas as pd


def to_c3d(FPS, csv_path, headernum):  
    c3d = ezc3d.c3d()
    data = pd.read_csv(csv_path, header=list(range(0,headernum)))
    # data = data_raw.iloc[1:, :]

    n_frame = data.shape[0]
    n_feature = int((data.shape[1])/3)
    body_parts = data#.iloc[:, 0:-1]
    body_parts = body_parts.to_numpy()
    body_parts = body_parts.astype(np.float)
    coord = np.zeros((4, n_feature, n_frame))
    
    for j in range(n_feature):
        coord[0, j, :] = body_parts[:, j*3]
        coord[1, j, :] = body_parts[:, j*3+1]
        coord[2, j, :] = body_parts[:, j*3+2] 
        coord[3, j, :] = n_feature*np.ones(n_frame)

    # Fill it 
    c3d['parameters']['POINT']['RATE']['value'] = [int(FPS)]
    c3d['parameters']['POINT']['RATE']['SCALE'] = [int(FPS)]
    c3d['parameters']['POINT']['LABELS']['value'] = tuple(data.columns.get_level_values(0).unique().to_list())
    c3d['data']['points'] = coord

    # Add a custom parameter to the POINT group
    c3d.add_parameter("POINT", "newParam", [1, 2, 3])
    
    # Add a custom parameter a new group
    c3d.add_parameter("NewGroup", "newParam", ["MyParam1", "MyParam2"])
    
    # Write the data
    # print('正在生成：', os.path.splitext(csv_path)[0] + ".c3d")
    c3d.write(os.path.splitext(csv_path)[0] + ".c3d")




