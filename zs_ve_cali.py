import numpy as np
import pandas as pd
import os
import seaborn as sns
from scipy.signal import savgol_filter

# looming_time_tag = [150, 160, 170]
# time_window = {}
# for i in range(len(looming_time_tag)):
#     start_label = looming_time_tag[i] - 30 * 3
#     end_label = looming_time_tag[i] + 30 * 30
#     time_window[start_label] = end_label
# start_label = time_window.keys()
# end_label = time_window.values()
start_label = 1
end_label = 1+30*33


def open_data(data_path, file_type):
    file_list = []
    path_list = os.listdir(data_path)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(data_path, filename))

    return file_list


def velocity(file_path):  # Cali velocity
    """
        nose:0    left_ear:1   Right_ear:2    neck:3    left_front_limb:4     right_front_limb:5
        left_hind_limb:6       right_hind_limb:7          left_front_claw:8     right_front_claw:9
        left_hind_claw:10      right_hind_claw:11        back:12      root_tail:13
        mid_tail:14            tip_tail:15
    """
    with open(file_path, 'rb') as f:
        df = pd.read_csv(f)
        df1 = df.iloc[2:, 36:39]  # select back vector

    df1 = df1.astype(float)
    v = df1.diff()
    v_x = v.iloc[start_label:end_label + 1, 0].tolist()
    v_y = v.iloc[start_label:end_label + 1, 1].tolist()
    v_z = v.iloc[start_label:end_label + 1, 2].tolist()
    v_list = []
    for i in range(0, len(v_x)):
        absolute_v = np.sqrt(np.square(v_x[i]) + np.square(v_y[i]) + +np.square(v_z[i]))  # Cali absolute velocity
        v_list.append(absolute_v)

    v_smooth = list(savgol_filter(v_list, 29, 2))

    return v_smooth


# def time_window(looming_tag, looming_before_time, looming_end_time):
#     time_window = {}
#     for i in range(len(looming_tag)):
#         start_label = looming_tag[i] - 30 * looming_before_time
#         end_label = looming_tag[i] + 30 * looming_end_time
#         time_window[start_label] = end_label
#
#         return time_window


if __name__ == '__main__':
    file_list = open_data('D:/3D_behavior/Arousal_behavior/results-20211217/3Dskeleton/Calibrated_3DSkeleton',
                          'Cali_Data3d.csv')
    back_v_all = {"time": [], "value": [], "type": []}

    time_list = [i for i in range(start_label, end_label + 1)]

    time_list_all = []
    for i in range(5):
        time_list_all.append(time_list)
    time_list_all = sum(time_list_all, [])
    back_v_all["time"] = time_list_all

    for i in range(0, 5):
        back_v = velocity(file_list[i])
        back_v_all["value"].append(back_v)
        back_v_all["type"].append(["A"] * (end_label - start_label + 1))
    back_v_all["value"] = sum(back_v_all["value"], [])
    back_v_all["type"] = sum(back_v_all["type"], [])

    df = pd.DataFrame(back_v_all)
    #
    sns.lineplot(data=df, x="time", y="value", hue="type")
