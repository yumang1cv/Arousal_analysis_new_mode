# %%
# 徐阳
# 开发时间：2021/9/11 20:01
import numpy as np
import pandas as pd
import os
from sklearn.decomposition import PCA

color_list = ['#845EC2', '#B39CD0', '#D65DB1', '#4FFBDF', '#FFC75F',
              '#D5CABD', '#B0A8B9', '#FF6F91', '#F9F871', '#D7E8F0',
              '#60DB73', '#E8575A', '#008B74', '#00C0A3', '#FF9671',
              '#93DEB1']
"""
    Arousal Behavior Class Combine
    1、Right turning:[1]  (#845EC2)             2、Left turning:[26]  (#B39CD0)
    3、Sniffing:[2, 4, 10, 11, 12, 16, 22, 25]  (#D65DB1)
    4、Walking:[3, 6, 7, 19, 30]  (#4FFBDF)     5、Trembling:[5, 15, 32, 40]  (#FFC75F)
    6、Climbing:[8, 29]   (#D5CABD)             7、Falling:[9]         (#B0A8B9)
    8、Immobility:[13, 20, 33, 34] (#FF6F91)    9、Paralysis:[14, 35]  (#F9F871)
    10、Standing:[17]      (#D7E8F0)            11、Trotting:[18, 31]  (#60DB73)
    12、Grooming:[21]      (#E8575A)            13、Flight:[23, 38]    (#008B74)
    14、Running:[24, 36]   (#00C0A3)            15、LORR:[27, 28, 39]  (#FF9671)
    16、Stepping:[37]      (#93DEB1)
"""


def search_csv(path=".", name=""):  # 抓取csv文件
    result = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            search_csv(item_path, name)
        elif os.path.isfile(item_path):
            if name + ".csv" == item:
                # global csv_result
                # csv_result.append(name)
                result.append(item_path)
                # print(csv_result)
                # print(item_path + ";", end="")
                # result = item
    return result


def read_csv(path='.', name="", column="", element="", state_name=""):
    """
        column[0]: file_name      column[1]:第一次looming时间点
        sheet1：Fwake状态          sheet2：Frorr状态
    """
    item_path = os.path.join(path, name)
    with open(item_path, 'rb') as f:
        csv_data = pd.read_excel(f, sheet_name=state_name)

    # df1 = csv_data.set_index([column])  # 选取某一列数据
    # sel_data = df1.loc[element]  # 根据元素提取特定数据

    return csv_data


def pre_data(file_path, dataframe, num, state=""):
    df1 = pd.read_csv(file_path)
    looming_time = int(dataframe.at[num, state])
    data = df1.iloc[looming_time - 5 * 30:looming_time + 115 * 30, 1:2]

    data1 = data.iloc[:, 0].tolist()

    class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
                  11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
    for line in data1:
        if line not in class_type:
            class_type[line] = 0

        else:
            class_type[line] += 1

    list_1 = list(class_type.values())

    return list_1


def sort_data(list_1):
    male_std = []
    for i in range(len(list_1)):
        male_1 = np.std(list_1[i])
        male_std.append(male_1)

    dictionary = dict(zip(male_std, list_1))
    # dictionary1 = {l: sorted(m) for l, m in dictionary.items()}
    # dictionary = sorted(dictionary.keys())

    sort_list = []

    # convert the dictionary to list using dict.keys
    dictlist = list(dictionary.keys())
    # sort the list
    dictlist.sort()
    # Print the corresponding key and value by traversing this list
    for key in dictlist:
        # print key and value
        # print(key, ":", dictionary[key])
        sort_list.append(dictionary[key])

    return sort_list


if __name__ == '__main__':
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all',
                 name="video_info.xlsx", column="looming_time1", state_name="Male_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    for item in a['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace",
            name="{}_Movement_Labels".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all',
                 name="video_info.xlsx", column="looming_time1", state_name="Female_Wakefulness")  # Female_Wakefulness

    file_list_2 = []
    for item in b['Video_name'][0:6]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace",
            name="{}_Movement_Labels".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    Male_list = []
    for i in range(len(file_list_1)):
        sub_list1 = pre_data(file_list_1[i], a, i, state="looming_time1")
        # print(sub_list1)
        Male_list.append(sub_list1)
    Male_list = sort_data(Male_list)

    Female_list = []
    for i in range(len(file_list_2)):
        sub_list2 = pre_data(file_list_2[i], b, i, state="looming_time1")
        # print(sub_list2)
        Female_list.append(sub_list2)
    Female_list = sorted(Female_list)

    # Female_list2 = []
    # for i in range(len(file_list_2)):
    #     sub_list3 = pre_data(file_list_2[i], b, i, state="looming_time2")
    #     # print(sub_list2)
    #     Female_list2.append(sub_list3)
    # Female_list2 = sort_data(Female_list2)
    #
    # Female_list3 = []
    # for i in range(len(file_list_2)):
    #     sub_list4 = pre_data(file_list_2[i], b, i, state="looming_time3")
    #     # print(sub_list2)
    #     Female_list3.append(sub_list4)
    # # Female_list3 = sort_data(Female_list3)
    #
    # Female_list4 = []
    # for i in range(len(file_list_2)):
    #     sub_list4 = pre_data(file_list_2[i], b, i, state="looming_time4")
    #     # print(sub_list2)
    #     Female_list4.append(sub_list4)
    # # Female_list3 = sort_data(Female_list3)

    result_list = Male_list
    Behavior_cal = []
    for j in range(len(result_list)):
        t = 0
        for i in range(len(result_list[j])):
            if result_list[j][i] != 0:
                t = t + 1
        # print(t)
        Behavior_cal.append(t)
    print(Behavior_cal)

    all = Male_list + Female_list
    concat_list = [j for i in all for j in i]

    label_fre = []
    label = [i for i in range(1, 17)]
    for i in range(len(Male_list[0])):
        label_fre1 = [label[i], Male_list[0][i]]
        label_fre.append(label_fre1)
    print(label_fre)


    # X = np.array(Female_list3)
    # pca = PCA(n_components=1)  # 降到2维
    # pca.fit(X)  # 训练
    # newX = pca.fit_transform(X)  # 降维后的数据
    # newX = newX.tolist()
    # # PCA(copy=True, n_components=2, whiten=False)
    # print(pca.explained_variance_ratio_)  # 输出贡献率
    # print(newX)  # 输出降维后的数据

    # explicit function to normalize array
    def normalize(arr, t_min, t_max):
        norm_arr = []
        diff = t_max - t_min
        diff_arr = max(arr) - min(arr)
        for i in arr:
            temp = (((i - min(arr)) * diff) / diff_arr) + t_min
            norm_arr.append(temp)
        return norm_arr


    range_to_normalize = (0, 1)
    normalized_array_1d = normalize(concat_list,
                                    range_to_normalize[0],
                                    range_to_normalize[1])

    X = np.array_split(normalized_array_1d, len(file_list_1)+len(file_list_2))   # reshape:文件个数
    all_data = pd.DataFrame(X)
    all_data = np.transpose(all_data)
    all_data.to_csv("D:\\3D_behavior\\Arousal_behavior\\Arousal_result_all\\Analysis_result\\State_space"
                    "\\looming_behavior_fre\\Wakefulness.csv")
