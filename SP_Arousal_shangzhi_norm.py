import numpy as np
import seaborn as sns
import pandas as pd


# explicit function to normalize array
def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr)) * diff) / diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr


"""
    SP Arousal 熵值
"""
Male_list_W1 = [236, 250, 230, 205, 266, 328, 252, 274, 212, 210]
Female_list_W1 = [359, 247, 265, 222, 246, 245, 430, 229, 472, 225]

Male_list_W2 = [231, 254, 236, 257, 242, 275, 238, 229, 227, 194]
Female_list_W2 = [321, 257, 250, 210, 246, 218, 343, 217, 384, 226]

Male_list_RORR1 = [9, 1, 1, 1, 3, 26, 33, 7, 13, 14]
Female_list_RORR1 = [10, 6, 1, 2, 139, 7, 1, 8, 1, 3]

Male_list_RORR2 = [5, 27, 8, 20, 24, 28, 8, 37, 52, 61]
Female_list_RORR2 = [26, 29, 25, 107, 4, 32, 24, 20, 2, 58]

Male_list_RORR3 = [42, 31, 54, 41, 36, 60, 83, 71, 80, 62]
Female_list_RORR3 = [53, 38, 16, 33, 86, 32, 44, 68, 25, 30]

Male_list_RORR4 = [42, 74, 64, 57, 66, 104, 81, 64, 113, 54]
Female_list_RORR4 = [69, 29, 69, 38, 59, 55, 34, 93, 79, 65]

Male_list_RORR5 = [51, 84, 62, 143, 50, 85, 144, 131, 165, 137]
Female_list_RORR5 = [148, 102, 46, 127, 131, 72, 29, 119, 57, 121]

Male_list_RORR6 = [59, 135, 117, 165, 138, 103, 164, 136, 154, 132]
Female_list_RORR6 = [163, 111, 94, 107, 151, 128, 152, 178, 129, 167]

Male_list_RORR7 = [137, 201, 119, 183, 169, 95, 116, 150, 185, 124]
Female_list_RORR7 = [174, 117, 76, 161, 232, 156, 145, 203, 153, 156]

Male_list_RORR8 = [91, 200, 140, 190, 186, 79, 156, 182, 189, 126]
Female_list_RORR8 = [194, 167, 162, 142, 191, 155, 98, 157, 125, 185]

Male_list_RORR9 = [130, 196, 149, 164, 194, 132, 196, 182, 48, 111]
Female_list_RORR9 = [125, 173, 152, 172, 236, 190, 174, 229, 146, 147]

Male_list_RORR10 = [120, 159, 188, 124, 162, 158, 176, 198, 154, 55]
Female_list_RORR10 = [176, 141, 88, 167, 199, 161, 137, 127, 203, 166]

Male_list_RORR11 = [99, 122, 150, 128, 132, 87, 124, 161, 42, 54]
Female_list_RORR11 = [166, 198, 147, 129, 195, 178, 99, 197, 157, 142]

Male_list_RORR12 = [98, 197, 152, 101, 48, 65, 123, 217, 120, 22]
Female_list_RORR12 = [109, 163, 187, 151, 223, 126, 175, 188, 194, 153]
"""
    looming 熵值
"""
# Male_list_W1 = [74, 12, 76, 64, 83]
# Female_list_W1 = [115, 56, 100, 73, 117, 76]
#
# Male_list_RORR1 = [7, 1, 21, 7, 1]
# Female_list_RORR1 = [24, 5, 2, 5, 4, 1]
#
# Male_list_RORR2 = [46, 9, 10, 1, 9]
# Female_list_RORR2 = [44, 33, 37, 26, 7, 17]
#
# Male_list_RORR3 = [46, 19, 19, 1, 46]
# Female_list_RORR3 = [44, 11, 58, 39, 33, 5]
#
# Male_list_RORR4 = [35, 21, 60, 45, 22]
# Female_list_RORR4 = [68, 21, 39, 21, 27, 42]
#
# newX = Male_list_W1 + Female_list_W1 + Male_list_RORR1 + Female_list_RORR1 + \
#        Male_list_RORR2 + Female_list_RORR2 + Male_list_RORR3 + Female_list_RORR3 \
#        + Male_list_RORR4 + Female_list_RORR4

newX = Male_list_W1 + Female_list_W1 + Male_list_W2 + Female_list_W2 + Male_list_RORR1 + Female_list_RORR1 + \
       Male_list_RORR2 + Female_list_RORR2 + Male_list_RORR3 + Female_list_RORR3 \
       + Male_list_RORR4 + Female_list_RORR4 + Male_list_RORR5 + Female_list_RORR5 \
       + Male_list_RORR6 + Female_list_RORR6 + Male_list_RORR7 + Female_list_RORR7 \
       + Male_list_RORR8 + Female_list_RORR8 + Male_list_RORR9 + Female_list_RORR9 \
       + Male_list_RORR10 + Female_list_RORR10 + Male_list_RORR11 + Female_list_RORR11 \
       + Male_list_RORR12 + Female_list_RORR12

range_to_normalize = (0, 1)
normalized_array_1d = normalize(newX,
                                range_to_normalize[0],
                                range_to_normalize[1])

# X = np.array_split(normalized_array_1d, 2*len(Male_list_W1))
X = np.array_split(normalized_array_1d, 14)
y = np.array_split(newX, 14)
y = pd.DataFrame(y)
# x = pd.DataFrame(np.transpose(X))
x = pd.DataFrame(X)
# x.to_csv("D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_space/looming_behavior_fre"
#          "/shang_v2.csv")
# sns.heatmap(X, center=0, cmap="vlag", yticklabels=False, xticklabels=False, vmin=0, vmax=1)
