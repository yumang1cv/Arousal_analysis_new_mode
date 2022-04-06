import os
import pandas as pd



def open_data(datapath,file_type):

    file_list = []
    path_list = os.listdir(datapath)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(datapath, filename))

    return file_list

def read_data(csv_path):

    class_type={}

#统计movemens出现的频率

    with open(csv_path) as f:
        for line in f:
            line = line.strip('\n')
            sorted(class_type.keys())

            if line not in class_type:
                class_type[str(line)] = 0
            else:
                class_type[str(line)] +=1
    print(class_type)

#class_type dict重排序

    d = {int(k):[int(i) for i in v] for k,v in class_type.items()}
    print(d)
    aftersorted_dict = dict(sorted(d.items(), key=lambda item:item[0]))


    return aftersorted_dict
    # label = list(class_type.keys())
    # frequency = list(class_type.values())
    # return label, frequency


if __name__ == '__main__':

    # open_data('D:/3D_behavior/Spontaneous_behavior/results/BeAMapping','rec-115-G1-20210919114230_Movement_Labels.csv')
    # print(open_data('D:/3D_behavior/Spontaneous_behavior/results/BeAMapping',
    #                 'rec-115-G1-20210919114230_Movement_Labels.csv'))
    print(read_data('D:/3D_behavior/Spontaneous_behavior/results/BeAMapping\\rec-115-G1-20210919114230_Movement_Labels.csv'))

