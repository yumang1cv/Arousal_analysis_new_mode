
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import collections



def open_data(datapath,file_type):

    file_list = []
    path_list = os.listdir(datapath)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(datapath, filename))

    return file_list

def read_data(file_name):

    df1 = pd.read_csv(file_name, usecols = ['movement_label','umap1', 'umap2', 'zs_velocity'])
    # print(df1,type(df1))

    return df1

# def collect_data(data_list):
#
#
#     movement_label_list = data_list.values[0:len(data_list), 0]
#     create_label_list = [x*x for x in range(1, 4, 1)]
#
#
#     for value in movement_label_list:
#         if value in create_label_list:
#             print(movement_label_list.index)
#
#     return

def groupby_data(result):

    merge_data = []
    for i in range(0, len(result), 1):
        merge_data.append(result[i])

    merged_df = pd.concat(merge_data, ignore_index=False)

    return merged_df

def mergedf_center(merged_data):

    umap1_mean = merged_data['umap1'].mean()
    umap2_mean = merged_data['umap2'].mean()
    v_mean = merged_data['zs_velocity'].mean()
    center = [umap1_mean, umap2_mean, v_mean]

    return center

def data3D(merged_data):

    umap1 = merged_data['umap1']
    umap2 = merged_data['umap2']
    v = merged_data['zs_velocity']

    return umap1,umap2,v

def cluster_dis(center,x,y,z):

    distance = [np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2 + (z - center[2])** 2)]

    return distance

def same_cluster_dis(file_list, label_num):

    result = []
    for i in range(0, len(file_list), 1):
        data_list = read_data(file_list[i])
        # group_data = data_list.groupby("movement_label")
        # print(group_data)
        # for key, df in group_data:
        #     print(key)
        #     print(df)

        res = dict(tuple(data_list.groupby('movement_label')))

        # result_ = 'result_' + str(i+1)
        # result = result.append([res[i]])
        result.append(res[label_num])


    merged_df2 = groupby_data(result)
    center = mergedf_center(merged_df2)
    [umap1, umap2, v] = data3D(merged_df2)
    distance = cluster_dis(center, umap1, umap2, v)
    distance =distance[0].mean()

    return distance


def diff_cluster_dis(file_list, label_num1, label_num2):
    result1 = []
    result2 = []
    for i in range(0, len(file_list), 1):
        data_list = read_data(file_list[i])
        # group_data = data_list.groupby("movement_label")
        # print(group_data)
        # for key, df in group_data:
        #     print(key)
        #     print(df)

        res = dict(tuple(data_list.groupby('movement_label')))

        # result_ = 'result_' + str(i+1)
        # result = result.append([res[i]])
        result1.append(res[label_num1])
        result2.append(res[label_num2])

    merged_df1 = groupby_data(result1)                #label_1 cluster
    merged_df2 = groupby_data(result2)                #label_2 cluster

    center = mergedf_center(merged_df1)               #label_1 center
    [umap1, umap2, v] = data3D(merged_df2)            #label_1 data
    distance = cluster_dis(center, umap1, umap2, v)
    distance = distance[0].mean()

    return distance

if __name__ == '__main__':

    file_list = open_data('D:/3D_behavior/looming_behavior/results-YJL/BeAMapping', 'Feature_Space.csv')
    # print(file_list)
    result = []
    print(file_list)
    for i in range(0, len(file_list), 1):
        data_list = read_data(file_list[i])
        # group_data = data_list.groupby("movement_label")
        # print(group_data)
        # for key, df in group_data:
        #     print(key)
        #     print(df)

        res = dict(tuple(data_list.groupby('movement_label')))

        # result_ = 'result_' + str(i+1)
        # result = result.append([res[i]])
        result.append(res)


    # result -> list[dic1, dic2, .., dic12]
    # each dic{1:dataframe, 2:dataframe, ..., 40:dataframe}
    # merge to a big dict{1:dataframe, ..., 40:dataframe}
    big_dict = {}
    for item in result:
        for behave in item:  # behave key value is int
            # 如果当前的行为不在大的big_dict, 那么我们就把这个行为放进去
            # {行为：dataframe} 行为：1-40key
            # item{1:dataframe, 2:dataframe}
            if behave not in big_dict:big_dict.update({behave:item[behave]})
            else:
                big_dict[behave] = pd.concat([big_dict[behave], item[behave]])
    print(len(big_dict))
    big_dict_order = collections.OrderedDict(sorted(big_dict.items()))

    # merged_df2 = groupby_data(result)
    # center = mergedf_center(merged_df2)
    # [umap1,umap2,v] = data3D(merged_df2)
    # distance = cluster_dis(center,umap1,umap2,v)
    # print(distance[0].mean())

    # # plt.plot(distance[0],x=2)
    # # plt.show()
    # try:
    #
    #     for j in range(1,40,1):
    #         label = same_cluster_dis(file_list, j)
    #         print(label)
    #
    # except:
    #     print(f'label{j} error'.format(j))
    #     j = j+1
    #     label = same_cluster_dis(file_list, j)
    #     print(label)

    # diff_distance= diff_cluster_dis(file_list, 11, 11)



