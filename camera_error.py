import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def open_data(datapath, file_type):

    file_list = []
    path_list = os.listdir(datapath)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(datapath, filename))

    return file_list

def get_data(file_name):

    """
        nose:0    left_ear:1   Right_ear:2    neck:3    left_front_limb:4     right_front_limb:5
        left_hind_limb:6       right_hind_limb:7          left_front_claw:8     right_front_claw:9
        left_hind_claw:10       right_hind_claw:11        back:12      root_tail:13
        mid_tail:14              tip_tail:15
    """

    likelihood = []
    df = pd.read_csv(file_name)
    for i in range(3, 49, 3):
        # print(df.iloc[2:, i])
        likelihood.append(df.iloc[:, i])
        like = np.transpose(likelihood)

    # print(likelihood,len(likelihood))

    return like

def camera1_max_likelihood(data_list):

    likelihood_max = []
    for i in range(2, 18002, 1):
        likelihood_max.append(np.max(data_list[i, :]))

    likelihood_max = [float(i) for i in likelihood_max]

    return likelihood_max

def camera2_max_likelihood(data_list1, data_list2):

    likelihood_max = []
    likelihood_max1 = []
    likelihood_max2 = []
    for i in range(2, 18002, 1):
        likelihood_max1.append(np.max(data_list1[i, :]))
        likelihood_max2.append(np.max(data_list2[i, :]))

    likelihood_max1 = [float(i) for i in likelihood_max1]
    likelihood_max2 = [float(i) for i in likelihood_max2]

    likelihood_max3 = likelihood_max1 + likelihood_max2
    likelihood_max4 = np.array(likelihood_max3).reshape(18000, 2)

    for i in range(0, len(likelihood_max4), 1):
        likelihood_max.append(np.max(likelihood_max4[i, :]))

    return likelihood_max

def camera3_max_likelihood(data_list1, data_list2, data_list3):

    likelihood_max = []
    likelihood_max1 = []
    likelihood_max2 = []
    likelihood_max3 = []
    for i in range(2, 18002, 1):
        likelihood_max1.append(np.max(data_list1[i, :]))
        likelihood_max2.append(np.max(data_list2[i, :]))
        likelihood_max3.append(np.max(data_list3[i, :]))

    likelihood_max1 = [float(i) for i in likelihood_max1]
    likelihood_max2 = [float(i) for i in likelihood_max2]
    likelihood_max3 = [float(i) for i in likelihood_max3]

    likelihood_max_a = likelihood_max1 + likelihood_max2 + likelihood_max3
    likelihood_max_b = np.array(likelihood_max_a).reshape(18000, 3)

    for i in range(0, len(likelihood_max_b), 1):
        likelihood_max.append(np.max(likelihood_max_b[i, :]))

    return likelihood_max

def camera4_max_likelihood(data_list1, data_list2, data_list3, data_list4):

    likelihood_max = []
    likelihood_max1 = []
    likelihood_max2 = []
    likelihood_max3 = []
    likelihood_max4 = []
    for i in range(2, 18002, 1):
        likelihood_max1.append(np.max(data_list1[i, :]))
        likelihood_max2.append(np.max(data_list2[i, :]))
        likelihood_max3.append(np.max(data_list3[i, :]))
        likelihood_max4.append(np.max(data_list4[i, :]))

    likelihood_max1 = [float(i) for i in likelihood_max1]
    likelihood_max2 = [float(i) for i in likelihood_max2]
    likelihood_max3 = [float(i) for i in likelihood_max3]
    likelihood_max4 = [float(i) for i in likelihood_max4]

    likelihood_max_a = likelihood_max1 + likelihood_max2 + likelihood_max3 +likelihood_max4
    likelihood_max_b = np.array(likelihood_max_a).reshape(18000, 4)

    for i in range(0, len(likelihood_max_b), 1):
        likelihood_max.append(np.max(likelihood_max_b[i, :]))

    return likelihood_max

if __name__ == '__main__':

    # open_data('D:/3D_behavior/Spontaneous_behavior/results/BeAMapping','rec-115-G1-20210919114230_Movement_Labels.csv')
    file_list = open_data('D:/3D_behavior/looming_behavior/YJL-camera-test/data',
                    'DLC_resnet50_black_miceOct24shuffle1_1030000.csv')

    camera1_data = get_data(file_list[5])
    camera1_likelihood_max = camera1_max_likelihood(camera1_data)
    # plt.boxplot(likelihood_max)

    camera2_data1 = get_data(file_list[18])
    camera2_data2 = get_data(file_list[19])
    camera2_likelihood_max = camera2_max_likelihood(camera2_data1, camera2_data2)

    camera3_data1 = get_data(file_list[24])
    camera3_data2 = get_data(file_list[25])
    camera3_data3 = get_data(file_list[19])
    camera3_likelihood_max = camera3_max_likelihood(camera3_data1, camera3_data2, camera3_data3)

    camera4_data1 = get_data(file_list[1])
    camera4_data2 = get_data(file_list[2])
    camera4_data3 = get_data(file_list[3])
    camera4_data4 = get_data(file_list[4])
    camera4_likelihood_max = camera4_max_likelihood(camera4_data1, camera4_data2, camera4_data3, camera4_data4)


    data = pd.DataFrame({
        "1_camera": camera1_likelihood_max,
        "2_camera": camera2_likelihood_max,
        "3_camera": camera3_likelihood_max,
        "4_camera": camera4_likelihood_max
    })
    fig = plt.figure(figsize=(15, 10), dpi=300)
    ax1 = fig.add_subplot(121)
    ax1.set_title('Different Camera of likelihood', fontsize=11)
    ax1 = data.boxplot(fontsize=11, grid=False)
    # plt.show()

    df = np.transpose(data)
    camera_1 = df.iloc[0]
    camera_2 = df.iloc[1]
    camera_3 = df.iloc[2]
    camera_4 = df.iloc[3]


    # # Create a plot
    # ax.violinplot([camera_1, camera_2, camera_3, camera_4], points=40, widths=0.5)
    # ax.set_xticklabels(["1_camera", "2_camera", "3_camera", "4_camera"])
    # # data.violinplot()

    # fig = plt.figure(figsize=(15, 10), dpi=300)
    ax2 = fig.add_subplot(122)
    ax2.set_title('Different Camera of likelihood', fontsize=11)
    fig = ax2.violinplot([camera_1, camera_2, camera_3, camera_4], points=40, widths=0.5)
    plt.show(ax1, ax2)





