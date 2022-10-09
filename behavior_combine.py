# """
#     Arousal Behavior Class Combine-looming 2022.09.23
#     1、Flight:[13, 14]                 2、Running:[3, 31]
#     3、Trotting:[4, 29]                4、Walking:[17, 18, 28, 30]
#     5、Stepping:[22, 27]               6、Left turning:[7]
#     7、Right turning:[26]               8、Rising:[8]
#     9、Standing:[21]                    10、Climbing:[20]
#     11、Sniffing:[1, 2, 24, 25, 35]     12、Grooming:[36]
#     13、Immobility:[11, 12, 19, 23, 32, 40]
#     14、LORR:[5, 6, 15, 16, 38, 39]
#     15、Paralysis:[9, 37]               16、Twitching:[10, 33, 34]
#
#
# """

# import pandas as pd
# import os
# from tqdm import tqdm
#
# # class_label_dict = {1: [13, 14], 2: [3, 31], 3: [4, 29], 4: [17, 18, 28, 30], 5: [22, 27], 6: [7], 7: [26], 8: [8],
# #                     9: [21], 10: [20], 11: [1, 2, 24, 25, 35], 12: [36], 13: [11, 12, 19, 23, 32, 40],
# #                     14: [5, 6, 15, 16, 38, 39], 15: [9, 37], 16: [10, 33, 34]}
# # new_dict = {}
# # for index, key in enumerate(class_label_dict):
# #     for item in class_label_dict[key]:
# #         new_dict.update({item: key})
# # print(new_dict)
#
# class_label_dict = {13: 1, 14: 1, 3: 2, 31: 2, 4: 3, 29: 3, 17: 4, 18: 4, 28: 4, 30: 4, 22: 5, 27: 5, 7: 6, 26: 7,
#                     8: 8, 21: 9, 20: 10, 1: 11, 2: 11, 24: 11, 25: 11, 35: 11, 36: 12, 11: 13, 12: 13, 19: 13,
#                     23: 13, 32: 13, 40: 13, 5: 14, 6: 14, 15: 14, 16: 14, 38: 14, 39: 14, 9: 15,
#                     37: 15, 10: 16, 33: 16, 34: 16}
#
# # class_label_dict = {value: key for key, value in class_label_dict.items()}
#
#
# def open_data(data_path, file_type):
#     file_list = []
#     path_list = os.listdir(data_path)
#     for filename in path_list:
#         if file_type in filename:
#             file_list.append(os.path.join(data_path, filename))
#
#     return file_list
#
#
# def rename_label(file_path):
#     for file in file_path:
#         with open(file, 'rb') as f:
#             df = pd.read_excel(f)
#
#     return
#
#
# if __name__ == '__main__':
#
#     # file_list = open_data(r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new\BeAOutputs\csv_file_output_new/',
#     #                       'Feature_Space.csv')
#     file_list = open_data(
#         r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new\BeAOutputs\csv_file_output_new/',
#         'Movement_Labels.csv')
#     # file_list = sorted(file_list, key=int)   # sort file use num
#     for i in tqdm(range(0, len(file_list))):
#         with open(file_list[i], 'rb') as file:
#             df = pd.read_csv(file)
#             # df = df.drop(df.columns[[1]], axis=1)
#             first_column = df.iloc[:, 0]
#             new_label = []
#             for j in range(len(first_column)):
#                 new_label.append(class_label_dict[first_column[j]])
#             df["new_label"] = new_label
#             df.rename(columns={'new_label': new_label[0]}, inplace=True)  # Movement_Labels需要注释
#             df.to_csv(file_list[i], index=False)


"""
    Arousal Behavior Class Combine-SP behavior 2022.09.23
    2、Running:[23, 24, 38]            3、Trotting:[6, 7, 36]
    4、Walking:[19, 30, 31]            5、Stepping:[10, 18]
    6、Left turning:[26]               7、Right turning:[16]
    8、Rising:[17]                     9、Standing:[29]
    10、Climbing:[8, 9]
    11、Sniffing:[2, 3, 4, 11, 21, 22, 25, 33, 37]
    12、Grooming:[20, 34, 40]          13、Immobility:[1, 12, 13]
    14、LORR:[27, 28, 39]              15、Paralysis:[5]
    16、Twitching:[14, 15, 32, 35]
"""

import pandas as pd
import os
from tqdm import tqdm

# class_label_dict = {2: [23, 24, 38], 3: [6, 7, 36], 4: [19, 30, 31], 5: [10, 18], 6: [26], 7: [16], 8: [17],
#                     9: [29], 10: [8, 9], 11: [2, 3, 4, 11, 21, 22, 25, 33, 37], 12: [20, 34, 40], 13: [1, 12, 13],
#                     14: [27, 28, 39], 15: [5], 16: [14, 15, 32, 35]}
# new_dict = {}
# for index, key in enumerate(class_label_dict):
#     for item in class_label_dict[key]:
#         new_dict.update({item: key})
# print(new_dict)

class_label_dict = {23: 2, 24: 2, 38: 2, 6: 3, 7: 3, 36: 3, 19: 4, 30: 4, 31: 4, 10: 5, 18: 5, 26: 6, 16: 7,
                    17: 8, 29: 9, 8: 10, 9: 10, 2: 11, 3: 11, 4: 11, 11: 11, 21: 11, 22: 11, 25: 11, 33: 11,
                    37: 11, 20: 12, 34: 12, 40: 12, 1: 13, 12: 13, 13: 13, 27: 14, 28: 14, 39: 14, 5: 15,
                    14: 16, 15: 16, 32: 16, 35: 16}


# class_label_dict = {value: key for key, value in class_label_dict.items()}


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

    file_list = open_data(r'E:\Arousal_result_new\SP_behavior_new\add\results\BeAOutputs\csv_file_output/',
                          'Feature_Space.csv')
    # file_list = open_data(
    #     r'E:\Arousal_result_new\SP_behavior_new\add\results\BeAOutputs\csv_file_output/',
    #     'Movement_Labels.csv')
    # file_list = sorted(file_list, key=int)   # sort file use num
    for i in tqdm(range(0, len(file_list))):
        with open(file_list[i], 'rb') as file:
            df = pd.read_csv(file)
            first_column = df.iloc[:, 0]
            new_label = []
            for j in range(len(first_column)):
                new_label.append(class_label_dict[first_column[j]])
            df["new_label"] = new_label
            # df.rename(columns={'new_label': new_label[0]}, inplace=True)  # Feature_Space需要注释
            df.to_csv(file_list[i], index=False)
