"""
    Arousal Behavior Class Combine-looming 2022.08.06
    1、Flight:[23, 38]                 2、Running:[6, 24, 36]
    3、Trotting:[7, 31]                4、Walking:[10, 18, 19, 30]
    5、Stepping:[37]                   6、Crawling:[3]
    7、Left turning:[26]               8、Right turning:[16]
    9、Standing:[17, 29]               10、Climbing:[8, 9]
    11、Sniffing:[2, 4, 11, 12, 13, 22, 25, 40]
    12、Grooming:[21]                  13、Immobility:[1, 20, 32, 33, 34]
    14、LORR:[28, 39]                  15、Paralysis:[14]
    16、Trembling:[5, 15, 35]

"""

import pandas as pd
import os
from tqdm import tqdm

# class_label_dict = {1: [23, 38], 2: [6, 24, 36], 3: [7, 31], 4: [10, 18, 19, 30], 5: [37], 6: [3], 7: [26], 8: [16],
#                     9: [17, 29], 10: [8, 9], 11: [2, 4, 11, 12, 13, 22, 25, 40], 12: [21], 13: [1, 20, 32, 33, 34],
#                     14: [28, 39], 15: [14], 16: [5, 15, 35]}
# new_dict = {}
# for index, key in enumerate(class_label_dict):
#     for item in class_label_dict[key]:
#         new_dict.update({item: key})
# print(new_dict)

class_label_dict = {23: 1, 38: 1, 6: 2, 24: 2, 36: 2, 7: 3, 31: 3, 10: 4, 18: 4, 19: 4, 30: 4, 37: 5, 3: 6, 26: 7,
                    16: 8, 17: 9, 29: 9, 8: 10, 9: 10, 2: 11, 4: 11, 11: 11, 12: 11, 13: 11, 22: 11, 25: 11, 40: 11,
                    21: 12, 1: 13, 20: 13, 32: 13, 33: 13, 34: 13, 28: 14, 39: 14, 14: 15, 5: 16, 15: 16, 35: 16}


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
    # file_list = open_data('D:/3D_behavior/Arousal_behavior/Arousal_analysis_new/Arousal_looming_new/results/BeAOutputs/csv_file_output',
    #                       'Feature_Space.csv')
    file_list = open_data(
        'D:/3D_behavior/Arousal_behavior/Arousal_analysis_new/Arousal_looming_new/results/BeAOutputs/csv_file_output',
        'Movement_Labels.csv')
    # file_list = sorted(file_list, key=int)   # sort file use num
    for i in tqdm(range(0, len(file_list))):
        with open(file_list[i], 'rb') as file:
            df = pd.read_csv(file)
            first_column = df.iloc[:, 0]
            new_label = []
            for j in range(len(first_column)):
                new_label.append(class_label_dict[first_column[j]])
            df["new_label"] = new_label
            df.rename(columns={'new_label': new_label[0]}, inplace=True)  # Movement_Labels需要注释
            df.to_csv(file_list[i], index=False)
        # df1 = df.iloc[:, [0]]  # 选取第一列数据：movement label
        # df.to_csv(file_list[0], columns="B")
    # """
    #     if df1.values[i] == class_label_dict
    #     df1 add the key in second column
    # """
    #
    # for i in range(0, len(df1)):
    #     if df1['31'].values[i] in class_label_dict[1]:
    #         df1['31'].value[i] == "1"

# """
#     Arousal Behavior Class Combine-SP_behavior:60min
#     1、Right turning:[3]               2、Left turning:[20]
#     3、Sniffing:[7, 8, 9, 10, 14, 19, 24, 25, 33]
#     4、Walking:[5, 6, 15, 16, 29, 36]  5、Trembling:[]
#     6、Climbing:[1, 11, 12]            7、Falling:[17, 21]
#     8、Immobility:[13]                 9、Paralysis:[23]
#     10、Standing:[2, 18, 22]           11、Trotting:[30, 37]
#     12、Grooming:[26, 27, 28, 38]      13、Flight:[34, 35]
#     14、Running:[31, 32]               15、LORR:[39, 40]
#     16、Stepping:[4]
# """
#
# import pandas as pd
# import os
# from tqdm import tqdm
#
# # class_label_dict = {1: [3], 2: [20], 3: [7, 8, 9, 10, 14, 19, 24, 25, 33], 4: [5, 6, 15, 16, 29, 36],
# #                     5: [], 6: [1, 11, 12], 7: [17, 21], 8: [13], 9: [23], 10: [2, 18, 22], 11: [30, 37],
# #                     12: [26, 27, 28, 38], 13: [34, 35], 14: [31, 32], 15: [39, 40], 16: [4]}
# # new_dict = {}
# # for index, key in enumerate(class_label_dict):
# #     for item in class_label_dict[key]:
# #         new_dict.update({item: key})
# # print(new_dict)
#
# class_label_dict = {3: 1, 20: 2, 7: 3, 8: 3, 9: 3, 10: 3, 14: 3, 19: 3, 24: 3, 25: 3, 33: 3,
#                     5: 4, 6: 4, 15: 4, 16: 4, 29: 4, 36: 4, 1: 6, 11: 6, 12: 6, 17: 7, 21: 7,
#                     13: 8, 23: 9, 2: 10, 18: 10, 22: 10, 30: 11, 37: 11, 26: 12, 27: 12, 28: 12,
#                     38: 12, 34: 13, 35: 13, 31: 14, 32: 14, 39: 15, 40: 15, 4: 16}
#
#
# # class_label_dict = {value:key for key,value in class_label_dict.items()}
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
#     file_list = open_data(
#             'D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min/new_results/BeAMapping-replace',
#             'Feature_Space.csv')
#     # file_list = open_data(
#     #     'D:/3D_behavior/Arousal_behavior/Arousal_result_all/SP_behavior_60min/new_results/BeAMapping-replace',
#     #     'Movement_Labels.csv')
#     # file_list = sorted(file_list, key=int)   # sort file use num
#     for i in tqdm(range(0, len(file_list))):
#         with open(file_list[i], 'rb') as file:
#             df = pd.read_csv(file)
#             first_column = df.iloc[:, 0]
#             new_label = []
#             for j in range(len(first_column)):
#                 new_label.append(class_label_dict[first_column[j]])
#             df["new_label"] = new_label
#             # df.rename(columns={'new_label': new_label[0]}, inplace=True)
#             df.to_csv(file_list[i], index=False)
#         # df1 = df.iloc[:, [0]]  # 选取第一列数据：movement label
#         # df.to_csv(file_list[0], columns="B")
