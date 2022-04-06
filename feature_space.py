# %%
# 徐阳
# 开发时间：2021/9/11 20:01
# importing the module
import csv
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import pyplot

# sns.color_palette("flare")
# sns.color_palette("pastel")
# palette = sns.color_palette("pastel", 3)
color_list = sns.color_palette("hls", 40)


# print(len(color_list))
def data_input(csv_path, movement_label_num):
    # open the file in read mode
    filename = open(csv_path, 'r')
    # filename = open('D:/硕士课题/results/BeAMapping/rec-4-G1-20210825114230_Feature_Space.csv', 'r')

    # creating dictreader object
    file = csv.DictReader(filename)

    # creating empty lists
    movement_label = []
    segBoundary = []

    # iterating over each row and append
    # values to empty list
    for col in file:
        movement_label.append(col['movement_label'])
        segBoundary.append(col['segBoundary'])

    movement_label = [int(i) for i in movement_label]
    # printing lists
    # print('movement_label:', movement_label)
    print('movement_label:', len(movement_label))

    segBoundary = [int(i) for i in segBoundary]
    # print('segBoundary:', segBoundary)
    print('segBoundary:', len(segBoundary))

    '''mydict = {y[0]: y[1] for y in [x.split(",") for x in open(
    'D:/硕士课题/results/BeAMapping/rec-4-G1-20210825114230_Feature_Space.csv').read().split('\n') if x]} print(mydict) '''
    seg_space_list = []
    seg_before_list = []
    for i in range(0, len(segBoundary), 1):
        if movement_label[i] == movement_label_num:
            seg_space = segBoundary[i] - segBoundary[i - 1]
            seg_space_list.append(seg_space)

            seg_before = segBoundary[i - 1]
            seg_before_list.append(seg_before)

            # print('上一个为:', movement_label[i-1], segBoundary[i-1], segBoundary[i] - segBoundary[i-1])
            # print(movement_label[i], segBoundary[i])

            # print(seg_space, seg_before)

    # print(seg_space_list)
    # print(seg_before_list)

    x_list = seg_before_list
    delay_list = seg_space_list
    x_range_list = []
    for i in range(1, len(seg_before_list), 1):
        x_left = seg_before_list[i]
        x_broken = seg_space_list[i]
        x_range_list.append((x_left, x_broken))

    print(f'movement_label_num is {movement_label_num}:', x_range_list)
    return x_range_list


if __name__ == '__main__':
    y_1 = (0, 1)
    y_2 = (1, 1)
    y_3 = (2, 1)
    y_4 = (3, 1)
    y_5 = (4, 1)
    y_6 = (5, 1)
    x_1 = data_input(
        'D:\\硕士课题\\results\\0825_Movement_labels\\0824_feature_space\\rec-7-G1-20210825114230_Feature_Space.csv', 27)
    x_2 = data_input(
        'D:\\硕士课题\\results\\0825_Movement_labels\\0824_feature_space\\rec-8-G1-20210825114230_Feature_Space.csv', 27)
    x_3 = data_input(
        'D:\\硕士课题\\results\\0825_Movement_labels\\0824_feature_space\\rec-9-G1-20210825114230_Feature_Space.csv', 27)
    x_4 = data_input(
        'D:\\硕士课题\\results\\0825_Movement_labels\\0824_feature_space\\rec-10-G1-20210825114230_Feature_Space.csv', 27)
    x_5 = data_input(
        'D:\\硕士课题\\results\\0825_Movement_labels\\0824_feature_space\\rec-11-G1-20210825114230_Feature_Space.csv', 27)
    # x_6 = data_input('D:\\硕士课题\\results\\0825_Movement_labels\\0824_feature_space\\rec-6-G1-20210825114230_Feature_Space.csv', 27)
    # x_8 = data_input('D:\\硕士课题\\results\\0825_Movement_labels\\0824_feature_space\\rec-8-G1-20210825114230_Feature_Space.csv', 27)
    pyplot.figure(figsize=(10, 3), dpi=400)
    plt.broken_barh(x_1, y_1, facecolors=color_list[35])

    plt.broken_barh(x_2, y_2, facecolors=color_list[1])

    plt.broken_barh(x_3, y_3, facecolors=color_list[10])
    plt.broken_barh(x_4, y_4, facecolors=color_list[0])
    plt.broken_barh(x_5, y_5, facecolors=color_list[9])
    # plt.broken_barh(x_6, y_6, facecolors=color_list[19])
    # plt.broken_barh(x_8, y_4, facecolors=color_list[29])

    # plt.broken_barh(x_4, y_5, facecolors=color_list[15])
    #
    # plt.broken_barh(x_5, y_5, facecolors=color_list[30])
    plt.yticks([0.5, 1.5, 2.5, 3.5, 4.5], ['T1', 'T2', 'T3', 'T4', 'T5'])
    plt.xticks([3000, 6000, 9000, 12000, 15000, 18000], ['100', '200', '300', '400', '500', '600'])
    # Adding title to the plot
    plt.title('Female-2-Day-grooming')

    # adding x axis label to the plot
    plt.xlabel('Time')

    # label for y axis  for the plot
    plt.ylabel('State')

    plt.show()

# %%
