import pandas as pd

pth = 'D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace\\rec-3-Mwake-20211031094033_Feature_Space.csv'
df = pd.read_csv(pth)
movement_label = df['movement_label']
segBoundary = df['segBoundary']

start = 24
end = 5000
start_index, end_index = 0, 0
if start < segBoundary[0]:
    start_index = 0
else:
    # 2. 先找到目标时间段
    for i in range(1, len(segBoundary)):
        pre, cur = segBoundary[i - 1], segBoundary[i]
        if pre < start < cur:
            start_index = i - 1
            print('start_value_range: ', pre, cur)
            print('index:', start_index)
            break
        elif start_index == cur:
            start_index = i
            print('start_value_range: ', cur)
            print('index:', start_index)
            break

if end > segBoundary[len(segBoundary) - 1]:
    end_index = len(segBoundary) - 1
else:
    for i in range(1, len(segBoundary)):
        pre, cur = segBoundary[i - 1], segBoundary[i]
        if pre < end < cur:
            end_index = i
            print('end_value_range: ', pre, cur)
            print('index:', end_index)
            break
        elif end_index == cur:
            end_index = i
            print('end_value_range: ', cur)
            print('index:', start_index)
            break


df.at[start_index, 'segBoundary'] = start
df.at[end_index, 'segBoundary'] = end
df_roi = df.copy()[start_index:end_index + 1].reset_index()

# 4. 在新的表中，记录每一个动作的持续时间
df_roi['duration'] = 0
for i in range(len(df_roi)-1):
    df_roi.at[i, 'duration'] = df_roi['segBoundary'][i+1] - df_roi['segBoundary'][i]
df_roi.at[len(df_roi)-1, 'duration'] = df_roi['duration'][len(df_roi)-2]

goubi_result = {}
for i in range(len(df_roi)):
    label = df_roi['new_label'][i]
    seg_time = df_roi['segBoundary'][i]
    duration = df_roi['duration'][i]
    if label not in goubi_result:
        goubi_result.update({label:[[seg_time, duration]]})
    else:
        goubi_result[label].append([seg_time, duration])
print(goubi_result)
