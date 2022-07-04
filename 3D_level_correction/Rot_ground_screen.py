# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 20:34:12 2021

@author: Administrator
"""


import cv2
import math
import numpy as np
import scipy.signal as signal

def speed_pop_index(data_3d, percent_num=35, total_index_num = 5000):
    # data_3d_pop = data_3d
    posX = np.array(data_3d.iloc[:,36])
    posX_minan_index = np.where(~np.isnan(posX))[0].astype(int)
    posY = np.array(data_3d.iloc[:,37])
    posY_minan_index = np.where(~np.isnan(posY))[0].astype(int)
    pos_intersect1d = np.intersect1d(posX_minan_index, posY_minan_index)
    
    # del_index_list = list()
    # for i in range(len(posX)):
    #     if np.isnan(posX[i]) or np.isnan(posY[i]):
    #         del_index_list.append(i)
    # if len(del_index_list) != 0:
    #     posX = np.delete(posX, del_index_list)
    #     posY = np.delete(posY, del_index_list)
    #     data_3d_pop = data_3d_pop.drop(del_index_list)
    
    data_3d_pop = data_3d.iloc[pos_intersect1d, :]
    data_3d_pop.reset_index(drop=True, inplace=True)
    pos = np.array([posX[pos_intersect1d], posY[pos_intersect1d]])
    pos_diff = np.diff(pos).T
    distance_XY = np.sqrt(pos_diff[:,0]**2 + pos_diff[:,1]**2)
    distance_quantile = np.percentile(distance_XY, percent_num)
    
    # choice_index_list1 = list()
    # for dis_num in range(len(distance_XY)):
    #     if distance_XY[dis_num] > distance_quantile:
    #         choice_index_list1.append(dis_num)
    
    choice_index_list = np.arange(0, len(distance_XY), 1)
    choice_index_list = choice_index_list[distance_XY > distance_quantile]
    
    if len(choice_index_list) > total_index_num:
        choice_index_list = np.sort(np.random.choice(choice_index_list, total_index_num, replace=False))
        
    result_data = data_3d_pop.loc[choice_index_list,:]
    return result_data


def Rot_2_ground(data3d, choice_order, filter_window):
    #data3d  3D数据
    if choice_order == True:
        choice_data = speed_pop_index(data3d)
    elif choice_order == False:
        choice_data = data3d
    
    #filter_window   滤波
    if (filter_window % 2) == 0:
        filter_window = int(filter_window + 1)
    else:
        filter_window = int(filter_window)
    
    np_data3d = np.array(choice_data)
    size_each = np_data3d.shape
    filter_data = np.zeros(size_each)
    for k in range(size_each[1]):
        filter_data[:,k] = signal.medfilt(np_data3d[:,k], kernel_size=filter_window)
    
    
    immobility_XYZ = np.vstack([filter_data[:,30:33], filter_data[:,33:36]])
    X = np.vstack([np.ones(immobility_XYZ.shape[0]),immobility_XYZ[:,0],immobility_XYZ[:,1]]).T
    b, _, _, _  = np.linalg.lstsq(X, immobility_XYZ[:,2], 95)
    XFIT, YFIT = np.meshgrid(immobility_XYZ[:,0], immobility_XYZ[:,1])
    ZFIT = b[0] + b[1] * XFIT + b[2] * YFIT
    normal_vector_plane = [b[1], b[2], 1]
    normal_vector_plane = normal_vector_plane / np.linalg.norm(normal_vector_plane)
    normal_vector_z = [0, 0, 1]
    cross_vector = np.cross(normal_vector_plane, normal_vector_z)
    cross_vector = cross_vector / np.linalg.norm(cross_vector)
    angle = math.acos(np.dot(normal_vector_plane,normal_vector_z)/(np.linalg.norm(normal_vector_plane)*np.linalg.norm(normal_vector_z)))
    cross_vector = -angle * cross_vector
    R, _ = cv2.Rodrigues(cross_vector)
    
    # rot_immobility_XYZ1 = np.zeros(immobility_XYZ.shape)
    # for m in range(immobility_XYZ.shape[0]):
    #     rot_immobility_XYZ1[m] = (R * np.mat(immobility_XYZ[m]).T).T
    
    immobility_XYZ_size = immobility_XYZ.shape
    R_size = R.shape
    rot_immobility_XYZ = np.matmul(R.reshape(1, R_size[0], R_size[1]).repeat(immobility_XYZ_size[0], axis=0),
                                   immobility_XYZ.reshape(immobility_XYZ_size[0], immobility_XYZ_size[1], 1))
    rot_immobility_XYZ = np.squeeze(rot_immobility_XYZ)
    
    rot_X = np.vstack([np.ones(rot_immobility_XYZ.shape[0]),rot_immobility_XYZ[:,0],rot_immobility_XYZ[:,1]]).T
    rot_b, _, _, _  = np.linalg.lstsq(rot_X, rot_immobility_XYZ[:,2], 95)
    rot_XFIT, rot_YFIT = np.meshgrid(rot_immobility_XYZ[:,0], rot_immobility_XYZ[:,1])
    rot_ZFIT = rot_b[0] + rot_b[1] * rot_XFIT + rot_b[2] * rot_YFIT
    
    rotate_data = np.zeros(data3d.shape)
    for rot_m in np.arange(0, data3d.shape[1], 3):
        rotate_data[:,rot_m:rot_m+3] = (R * np.mat(data3d.iloc[:,rot_m:rot_m+3]).T).T
    
    # rotate_data1 = 
    
    
    rot_size = rotate_data.shape
    rotate_data[:, np.arange(2, rot_size[1], 3)] = rotate_data[:, np.arange(2, rot_size[1], 3)] - rot_ZFIT.min()
    return rotate_data






