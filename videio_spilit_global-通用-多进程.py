#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 19:29:11 2021

@author: yejohnny
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2
import os
import time
from multiprocessing import Pool
from multiprocessing import Process
import pandas as pd
from tqdm import tqdm


##############################################################################

def video_split(file, start_frame, end_frame, outpath):
    cap = cv2.VideoCapture(file)
    fps = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    start_frame = start_frame  # 开始帧,从1开始计数
    end_frame = end_frame  # 结束帧

    # 获取视频分辨率
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # 输出文件编码，Linux下可选X264
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')

    # 视频帧率
    fps = cap.get(cv2.CAP_PROP_FPS)

    success, image = cap.read()
    count = 0
    success = True

    # 从视频开头获取每一帧，直到到达开始帧
    while success:
        success, image = cap.read()
        count += 1
        if (count == start_frame):
            success = False

    # 开始帧的时间(单位ms)，相当于ffmpeg的ss参数
    ss = int(cap.get(cv2.CAP_PROP_POS_MSEC))
    # 输出
    out = cv2.VideoWriter(outpath, fourcc, fps, size)

    # 读取开始帧到结束帧的每一帧并写入新视频
    while (count < end_frame):
        success, image = cap.read()
        out.write(image)
        count += 1

    # 结束帧的时间，相对于ffmpeg的to参数
    to = int(cap.get(cv2.CAP_PROP_POS_MSEC))

    cap.release()
    out.release()




info_df = pd.read_csv(
    'H:/Z01_3D_behavior/SP_square_box/result/df_nearest1.csv')
raw_video_dir = 'H:/Z01_3D_behavior/SP_square_box/split_video'  # 输入视频存放的文件夹
output_dir = 'H:/Z01_3D_behavior/SP_square_box/video_resplit'

### 获取输入文件夹下待切割视频路径
raw_video_path = {}
file_name_list = info_df['file'].unique()

for file_name in file_name_list:
    raw_video_path.setdefault(file_name, [])
    for v_file_name in os.listdir(raw_video_dir):
        if v_file_name.endswith('.avi'):
            if v_file_name.startswith(file_name):
                raw_video_path[file_name].append(raw_video_dir +'/'+ v_file_name)




    

if __name__ == '__main__':
    t1 = time.time()
    pool = Pool(5)
    for i in info_df.index:
        label = info_df.loc[i, 'movement_label']
        boundary = info_df.loc[i, 'boundary']
        file_name = info_df.loc[i, 'file']
        start_frame = int(boundary.split(',')[0].strip('('))
        end_frame = int(boundary.split(',')[1].strip(')')) + 1
        video_list = raw_video_path[file_name]
        video_list.sort()
        input_file = video_list[2]
        sub_output_dir = output_dir + '/{0}/{1}'.format(label, input_file[-12:-4])
        folder = os.path.exists(sub_output_dir)
        if not folder:
            os.makedirs(sub_output_dir)
            #print('--- establish {} ---\n'.format(sub_output_dir))
        output_file = sub_output_dir + '/{0}_{1}_{2}.avi'.format(file_name, start_frame, end_frame)
        pool.apply_async(video_split, args=(input_file, start_frame, end_frame, output_file))
    pool.close()
    pool.join()
    t2 = time.time()
    print('\n finish! Total time:{:.2f} min \n'.format((t2 - t1) / 60))






'''
### 开始循环处理视频
print('processing data ......\n')
p = Pool(6)
for i in info_df.index:
    label = info_df.loc[i, 'movement_label']
    boundary = info_df.loc[i, 'boundary']
    file_name = info_df.loc[i, 'file']
    start_frame = int(boundary.split(',')[0].strip('('))
    end_frame = int(boundary.split(',')[1].strip(')')) + 1
    video_list = raw_video_path[file_name]

    for video_path in video_list[2:4]:
        input_file = video_path
        sub_output_dir = output_dir + '/{0}/{1}'.format(label, video_path[-12:-4])
        folder = os.path.exists(sub_output_dir)
        if not folder:
            os.makedirs(sub_output_dir)
            #print('--- establish {} ---\n'.format(sub_output_dir))
        output_file = sub_output_dir + '/{0}_{1}_{2}.avi'.format(file_name, start_frame, end_frame)
        #video_split(input_file, start_frame, end_frame, output_file)
        p.apply_async(video_split, args=(input_file, start_frame, end_frame, output_file))
        print(video_path,output_file)
    p.close()
    p.join()

t2 = time.time()
print('\n finish! Total time:{:.2f} min \n'.format((t2 - t1) / 60))
'''

