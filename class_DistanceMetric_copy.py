import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import collections
import heapq


def open_data(datapath, file_type):
    file_list = []
    path_list = os.listdir(datapath)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(datapath, filename))

    return file_list


def read_data(file_name):
    df1 = pd.read_csv(file_name, usecols=['movement_label', 'umap1', 'umap2', 'zs_velocity'])
    # print(df1,type(df1))

    return df1


def groupby_data(result):
    merge_data = []
    for i in range(0, len(result), 1):
        merge_data.append(result[i])

    merged_df = pd.concat(merge_data, ignore_index=False)

    return merged_df


def mergedf_center(merged_data):
    umap1 = merged_data['umap1']
    umap2 = merged_data['umap2']
    v = merged_data['zs_velocity']
    umap1_mean = umap1.mean()
    umap2_mean = umap2.mean()
    v_mean = v.mean()
    center = [umap1_mean, umap2_mean, v_mean]

    return center


def data3D(merged_data):
    umap1 = merged_data['umap1']
    umap2 = merged_data['umap2']
    v = merged_data['zs_velocity']

    return umap1, umap2, v


def cluster_dis(center, x, y, z):
    distance = [np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2 + (z - center[2]) ** 2)]

    return distance


def same_cluster_dis(file_list, label_num):
    result = []
    # print(file_list)
    for i in range(0, len(file_list), 1):
        data_list = read_data(file_list[i])
        res = dict(tuple(data_list.groupby('movement_label')))
        result.append(res)
    '''
        result -> list[dic1, dic2, .., dic12]
        each dic{1:dataframe, 2:dataframe, ..., 40:dataframe}
        merge to a big dict{1:dataframe, ..., 40:dataframe}
    '''
    big_dict = {}
    for item in result:
        for behave in item:  # behave key value is int
            # 如果当前的行为不在大的big_dict, 那么我们就把这个行为放进去
            # {行为：dataframe} 行为：1-40key
            # item{1:dataframe, 2:dataframe}
            if behave not in big_dict:
                big_dict.update({behave: item[behave]})
            else:
                big_dict[behave] = pd.concat([big_dict[behave], item[behave]])
    # print(len(big_dict))
    big_dict_order = collections.OrderedDict(sorted(big_dict.items()))

    label = big_dict_order[label_num]

    center = mergedf_center(label)
    [umap1, umap2, v] = data3D(label)
    distance = cluster_dis(center, umap1, umap2, v)
    distance = distance[0]
    distance = heapq.nsmallest(14, distance)

    return distance


def diff_cluster_dis(file_list, label_num1, label_num2):
    result = []
    # print(file_list)
    for i in range(0, len(file_list), 1):
        data_list = read_data(file_list[i])
        res = dict(tuple(data_list.groupby('movement_label')))
        result.append(res)
    '''
        result -> list[dic1, dic2, .., dic12]
        each dic{1:dataframe, 2:dataframe, ..., 40:dataframe}
        merge to a big dict{1:dataframe, ..., 40:dataframe}
    '''
    big_dict = {}
    for item in result:
        for behave in item:  # behave key value is int
            # 如果当前的行为不在大的big_dict, 那么我们就把这个行为放进去
            # {行为：dataframe} 行为：1-40key
            # item{1:dataframe, 2:dataframe}
            if behave not in big_dict:
                big_dict.update({behave: item[behave]})
            else:
                big_dict[behave] = pd.concat([big_dict[behave], item[behave]])
    # print(len(big_dict))
    big_dict_order = collections.OrderedDict(sorted(big_dict.items()))

    label_1 = big_dict_order[label_num1]
    label_2 = big_dict_order[label_num2]

    center = mergedf_center(label_1)
    [umap1, umap2, v] = data3D(label_2)
    distance = cluster_dis(center, umap1, umap2, v)
    distance = distance[0]
    # distance = heapq.nlargest(40, distance)
    distance = distance.mean()

    return distance


def cut(obj, sec):  # list cut
    return [obj[i:i + sec] for i in range(0, len(obj), sec)]


if __name__ == '__main__':

    file_list = open_data('D:/3D_behavior/looming_behavior/results-YJL/BeAMapping', 'Feature_Space.csv')

    same_distance = []
    for i in range(1,41,1):
        distance_1 = same_cluster_dis(file_list, i)
        same_distance.append(distance_1)

    same_distance_all = []
    for i in range(0, len(same_distance)):
        same_distance_all.append(same_distance[i])

    same_distance_norm = (same_distance_all - np.min(same_distance_all)) / (
                np.max(same_distance_all) - np.min(same_distance_all))
    same_distance_norm = 1 - same_distance_norm

    df = pd.DataFrame(same_distance_norm)

    # saving the dataframe
    df.to_csv(r'D:\3D_behavior\looming_behavior\results-YJL\gujia-vis\same.csv')

    # diff_distance = []
    # for j in range(1, 41):
    #     for i in range(1, 41):
    #         diff_dis = diff_cluster_dis(file_list, j, i)
    #         diff_distance.append(diff_dis)
    #
    # diff_distance_norm = (diff_distance - np.min(diff_distance)) / (np.max(diff_distance) - np.min(diff_distance))
    # diff_distance_cut = cut(diff_distance_norm, 40)
    # #
    # # plt.violinplot(diff_distance_cut[0])
    # df = pd.DataFrame(diff_distance_cut)
    #
    # # saving the dataframe
    # df.to_csv(r'D:\3D_behavior\looming_behavior\results-YJL\gujia-vis\diff.csv')
