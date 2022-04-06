import os
import pandas as pd
import numpy as np


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

    coordinate_x = []
    coordinate_y = []
    coordinate_z = []


    df = pd.read_csv(file_name)

    for i in range(0, 47, 3):
        # print(df.iloc[2:, i])
        # coordinate_x.append(df.iloc[:, i])
        coordinate_y.append(df.iloc[1:, i+1])
        # coordinate_z.append(df.iloc[:, i+2])
        # like = np.transpose(likelihood)

    # print(likelihood,len(likelihood))

    return coordinate_y



if __name__ == '__main__':
    file_list = open_data('D:/3D_behavior/looming_behavior/results-YJL/results/3Dskeleton/Calibrated_3DSkeleton', 'Data3d.csv')
    y = get_data(file_list[0])
    list_all_y = []
    for item in y:
        item = list(float(n) for n in item)
        # list_all_y.append(item)
        print(np.max(item), np.min(item))

    # list_y = y[0]
    # list_y = list(float(n) for n in list_y)
    # print(np.max(list_y),np.min(list_y))




    # for item in y:
    #     # print(item)
    #     print(item.max())
