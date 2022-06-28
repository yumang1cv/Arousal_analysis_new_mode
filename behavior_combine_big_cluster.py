# -*- coding:utf-8 -*-
# @FileName  :behavior_combine_big_cluster.py
# @Time      :2022/6/20 15:33
# @Author    :XuYang
import pandas as pd
import os
from tqdm import tqdm

# class_label_dict = {1: [1, 2, 4, 11, 13, 14, 16], 2: [3, 6, 7, 10], 3: [12], 4: [8], 5: [5, 9, 15]}
# new_dict = {}
# for index, key in enumerate(class_label_dict):
#     for item in class_label_dict[key]:
#         new_dict.update({item: key})
# print(new_dict)

class_label_dict = {1: 1, 2: 1, 4: 1, 11: 1, 13: 1, 14: 1, 16: 1,
                    3: 2, 6: 2, 7: 2, 10: 2, 12: 3, 8: 4, 5: 5, 9: 5, 15: 5}


# class_label_dict = {value:key for key,value in class_label_dict.items()}


def open_data(data_path, file_type):
    file_list = []
    path_list = os.listdir(data_path)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(data_path, filename))

    return file_list


def rename_label(file_path):
    for file in file_path:
        with open(file, 'rb') as f:
            df = pd.read_excel(f)

    return


if __name__ == '__main__':
    # file_list = open_data(
    #     'D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min/new_results/BeAMapping-replace', 'Feature_Space.csv')

    file_list = open_data(
        'D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min/new_results/BeAMapping-replace', 'Movement_Labels.csv')

    # file_list = sorted(file_list, key=int)   # sort file use num
    for i in tqdm(range(0, len(file_list))):
        with open(file_list[i], 'rb') as file:
            df = pd.read_csv(file)

            first_column = df.iloc[:, 1]   # movement_label.csv 中 movement_label 的位置
            # first_column = df.iloc[:, 5]  # Feature_Space.csv 中 movement_label 的位置

            new_label = []
            for j in range(len(first_column)):
                new_label.append(class_label_dict[first_column[j]])
            df["big_cluster_label"] = new_label
            df.rename(columns={'big_cluster_label': new_label[0]}, inplace=True)    # movement_label.csv 必须使用
            df.to_csv(file_list[i], index=False)
        # df1 = df.iloc[:, [0]]  # 选取第一列数据：movement label
        # df.to_csv(file_list[0], columns="B")
