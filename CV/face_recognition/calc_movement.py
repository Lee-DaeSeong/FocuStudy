import csv
import numpy as np
import pandas as pd

frame_interval = 50
result = pd.read_csv('csv_data/frame{}.csv'.format(frame_interval), encoding='utf-8-sig')
result = result.set_index('파일 이름')
end = result.index

f = open('csv_data/frame{}_movement.csv'.format(frame_interval), 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)
writer.writerow(
    ['파일 이름', '이름', 'frame', '이해도 평가', '실제 이해도', 'movement_x', 'movement_y', 'non_detect', 'base_x', 'base_y'])

for cur_idx in end:
    temp = result.loc[cur_idx]['데이터']
    if type(temp) != str:
        continue
    temp = temp.replace('[', '').replace(', ', ' ')
    temp = temp.split('] ')
    temp.pop()
    base = [list(map(int, t.split(' '))) for t in temp]
    base_x = 0
    base_y = 0
    cnt = 0
    for x, y in base:
        if x == 0 and y == 0:
            continue
        base_x += x
        base_y += y
        cnt += 1
    if cnt != 0:
        base_x //= cnt
        base_y //= cnt
    non_detect = 0
    move_x = 0
    move_y = 0
    prev_x = int(temp[0].split(' ')[0])
    prev_y = int(temp[0].split(' ')[1])
    for i in temp[1:]:
        x, y = map(int, i.split(' '))
        if x == 0 and y == 0:
            non_detect += 1
            continue
        move_x += abs(prev_x - x)
        move_y += abs(prev_y - y)
        prev_x = x
        prev_y = y

    res = [cur_idx, result.loc[cur_idx]['이름'], result.loc[cur_idx]['frame'], result.loc[cur_idx]['이해도 평가'],
           result.loc[cur_idx]['실제 이해도'], move_x,
           move_y, non_detect, base_x, base_y]
    writer.writerow(res)
    print(res)
