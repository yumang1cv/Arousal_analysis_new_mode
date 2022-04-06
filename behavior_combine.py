# """
#     Behavior Class Combine
#     1、Running:[15, 16, 35, 22]         2、Right turning:[7, 31, 34]       3、Left turning:[9, 21]
#     4、Walking:[8, 18, 23, 24, 37]      5、Trotting:[3, 5, 6, 17, 19]      6、Rearing:[12, 26]
#     7、Sniffing:[1, 4, 10, 13, 14, 20, 27, 28, 29, 30]                     8、Grooming:[39, 40]
#     9、Diving:[11, 25]                  10、Rising:[2]                     11、Hunching:[36]
#     12、Falling:[32]                    13、Jumping:[33]                   14、Stepping:[38]
#
#     Right Sniffing:[1, 4, 13, 20, 28, 30]                            Right Sniffing:[14, 27, 29]
#     Immobility:{7、Sniffing:[1, 4, 6, 10, 14, 28, 29, 30],8、 Grooming:[39, 40], 9、Diving:[11, 25], 10、Rising:[2]}
# """
#
# import pandas as pd
# import os
# from tqdm import tqdm
#
# # class_label_dict = {1: [15, 16, 35, 22], 2: [7, 31, 34], 3: [9, 21], 4: [8, 18, 23, 24, 37],
# #                     5: [3, 5, 6, 17, 19], 6: [12, 26], 7: [1, 4, 10, 13, 14, 20, 27, 28, 29, 30],
# #                     8: [39, 40], 9: [11, 25], 10: [2], 11: [36], 12: [32], 13: [33], 14: [38]}
# # new_dict = {}
# # for index, key in enumerate(class_label_dict):
# #     for item in class_label_dict[key]:
# #         new_dict.update({item:key})
# # print(new_dict)
#
# class_label_dict = {15: 1, 16: 1, 35: 1, 22: 1, 7: 2, 31: 2, 34: 2, 9: 3, 21: 3, 8: 4, 18: 4, 23: 4, 24: 4, 37: 4, 3: 5,
#                     5: 5, 6: 5, 17: 5, 19: 5, 12: 6, 26: 6, 1: 7, 4: 7, 10: 7, 13: 7, 14: 7, 20: 7, 27: 7, 28: 7, 29: 7,
#                     30: 7, 39: 8, 40: 8, 11: 9, 25: 9, 2: 10, 36: 11, 32: 12, 33: 13, 38: 14}
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
# def replace_label(file_path):
#     with open(file_path, 'rb') as file:
#         dataframe = pd.read_csv(file)
#         # dataframe_1 = dataframe.iloc[:, [0]]  # 选取第一列数据：movement label
#
#         dataframe_2 = dataframe.iloc[:, [0]].replace({15: 1, 16: 1, 35: 1, 22: 1})  # 1、Running:[15, 16, 35, 22]
#         dataframe_2 = dataframe_2.replace({7: 2, 31: 2, 34: 2, 9: 3, 21: 3})  # 2、Right turning:[7, 31, 34]  3、Left
#         # turning:[9, 21]
#         dataframe_2 = dataframe_2.replace({8: 4, 18: 4, 23: 4, 24: 4, 37: 4})  # 4、Walking:[8, 18, 23, 24, 37]
#         dataframe_2 = dataframe_2.replace({3: 5, 5: 5, 6: 5, 17: 5, 19: 5})  # 5、Trotting:[3, 5, 6, 17, 19]
#         dataframe_2 = dataframe_2.replace({1: 7, 4: 7, 10: 7, 13: 7, 14: 7, 20: 7, 27: 7, 28: 7, 29: 7, 30: 7})
#         # 7、Sniffing:[1, 4, 10, 13, 14, 20, 27, 28, 29, 30]
#         dataframe_2 = dataframe_2.replace({12: 6, 26: 6, 39: 8, 40: 8})  # 6、Rearing:[12, 26]   8、Grooming:[39, 40]
#         dataframe_2 = dataframe_2.replace(
#             {11: 9, 25: 9, 2: 10, 36: 11})  # 9、Diving:[11, 25]  10、Rising:[2]  11、Hunching:[36]
#         dataframe_2 = dataframe_2.replace({32: 12, 33: 13, 38: 14})  # 12、Falling:[32]  13、Jumping:[33] 14、Stepping:[38]
#
#     return dataframe_2
#
#
# if __name__ == '__main__':
#     # file_list = open_data('D:/3D_behavior/Spontaneous_behavior/result/BeAMapping/BeAMapping_replace',
#     #                       'Feature_Space.csv')
#     file_list = open_data('D:/3D_behavior/Spontaneous_behavior/result/BeAMapping/BeAMapping_replace',
#                           'Movement_Labels.csv')
#     # file_list = sorted(file_list, key=int)   # sort file use num
#     for i in tqdm(range(0, len(file_list))):
#         with open(file_list[i], 'rb') as file:
#             df = pd.read_csv(file)
#             first_column = df.iloc[:, 0]
#             new_label = []
#             for j in range(len(first_column)):
#                 new_label.append(class_label_dict[first_column[j]])
#             df["new_label"] = new_label
#             df.rename(columns={'new_label': '2'}, inplace=True)
#             df.to_csv(file_list[i], index=False)
#         # df1 = df.iloc[:, [0]]  # 选取第一列数据：movement label
#         # df.to_csv(file_list[0], columns="B")
#     """
#         if df1.values[i] == class_label_dict
#         df1 add the key in second column
#     """
#
#     # for i in range(0, len(df1)):
#     #     if df1['31'].values[i] in class_label_dict[1]:
#     #         df1['31'].value[i] == "1"

"""
    Arousal Behavior Class Combine
    1、Right turning:[1]               2、Left turning:[26]
    3、Sniffing:[2, 4, 10, 11, 12, 16, 22, 25]
    4、Walking:[3, 6, 7, 19, 30]       5、Trembling:[5, 15, 32, 40]
    6、Climbing:[8, 29]                7、Falling:[9]
    8、Immobility:[13, 20, 33, 34]     9、Paralysis:[14, 35]
    10、Standing:[17]                  11、Trotting:[18, 31]
    12、Grooming:[21]                  13、Flight:[23, 38]
    14、Running:[24, 36]               15、LORR:[27, 28, 39]
    16、Stepping:[37]
"""

import pandas as pd
import os
from tqdm import tqdm

# class_label_dict = {1: [1], 2: [26], 3: [2, 4, 10, 11, 12, 16, 22, 25], 4: [3, 6, 7, 19, 30],
#                     5: [5, 15, 32, 40], 6: [8, 29], 7: [9], 8: [13, 20, 33, 34], 9: [14, 35], 10: [17],
#                     11: [18, 31], 12: [21], 13: [23, 38], 14: [24, 36], 15: [27, 28, 39], 16:[37]}
# new_dict = {}
# for index, key in enumerate(class_label_dict):
#     for item in class_label_dict[key]:
#         new_dict.update({item:key})
# print(new_dict)

class_label_dict = {1: 1, 26: 2, 2: 3, 4: 3, 10: 3, 11: 3, 12: 3, 16: 3, 22: 3,
                    25: 3, 3: 4, 6: 4, 7: 4, 19: 4, 30: 4, 5: 5, 15: 5, 32: 5, 40: 5,
                    8: 6, 29: 6, 9: 7, 13: 8, 20: 8, 33: 8, 34: 8, 14: 9, 35: 9, 17: 10,
                    18: 11, 31: 11, 21: 12, 23: 13, 38: 13, 24: 14, 36: 14, 27: 15, 28: 15, 39: 15, 37: 16}

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


def replace_label(file_path):
    with open(file_path, 'rb') as file:
        dataframe = pd.read_csv(file)
        # dataframe_1 = dataframe.iloc[:, [0]]  # 选取第一列数据：movement label

        dataframe_2 = dataframe.iloc[:, [0]].replace({15: 1, 16: 1, 35: 1, 22: 1})  # 1、Running:[15, 16, 35, 22]
        dataframe_2 = dataframe_2.replace({7: 2, 31: 2, 34: 2, 9: 3, 21: 3})  # 2、Right turning:[7, 31, 34]  3、Left
        # turning:[9, 21]
        dataframe_2 = dataframe_2.replace({8: 4, 18: 4, 23: 4, 24: 4, 37: 4})  # 4、Walking:[8, 18, 23, 24, 37]
        dataframe_2 = dataframe_2.replace({3: 5, 5: 5, 6: 5, 17: 5, 19: 5})  # 5、Trotting:[3, 5, 6, 17, 19]
        dataframe_2 = dataframe_2.replace({1: 7, 4: 7, 10: 7, 13: 7, 14: 7, 20: 7, 27: 7, 28: 7, 29: 7, 30: 7})
        # 7、Sniffing:[1, 4, 10, 13, 14, 20, 27, 28, 29, 30]
        dataframe_2 = dataframe_2.replace({12: 6, 26: 6, 39: 8, 40: 8})  # 6、Rearing:[12, 26]   8、Grooming:[39, 40]
        dataframe_2 = dataframe_2.replace(
            {11: 9, 25: 9, 2: 10, 36: 11})  # 9、Diving:[11, 25]  10、Rising:[2]  11、Hunching:[36]
        dataframe_2 = dataframe_2.replace({32: 12, 33: 13, 38: 14})  # 12、Falling:[32]  13、Jumping:[33] 14、Stepping:[38]

    return dataframe_2


if __name__ == '__main__':
    # file_list = open_data('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2/BeAMapping',
    #                       'Feature_Space.csv')
    file_list = open_data('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2/BeAMapping',
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
            df.rename(columns={'new_label': new_label[0]}, inplace=True)
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
