import numpy as np
import cv2
import csv
import time


def get_movement_distance(cap, frame_interval):
    cur_frame = 1.0
    last_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT) - 30
    if last_frame < 0:
        writer.writerow(cur)
    frame_cnt = 1
    stack = ''

    while cur_frame <= last_frame:
        cap.set(cv2.CAP_PROP_POS_FRAMES, cur_frame)
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # 좌우 대칭
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.05, 5)

        if len(faces):
            for (x, y, w, h) in faces:
                p = str(x) + ', ' + str(y)
                stack += '[' + p + '] '

        if len(faces) == 0:
            stack += '[' + '0, 0] '
        k = cv2.waitKey(30) & 0xff
        if k == 27 or k == ord('q'):  # Esc 키를 누르면 종료
            break
        cur_frame += frame_interval
        frame_cnt += 1
    writer.writerow(cur + [frame_cnt, stack])


face_cascade = cv2.CascadeClassifier('haarcascade_frontface.xml')
f = open('../csv_data/result.csv', encoding='utf-8-sig')
using_list = csv.reader(f)
next(using_list)
base = '../data/'
frame_interval = 100
f1 = open('../csv_data/frame{}.csv'.format(frame_interval), 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f1)
writer.writerow(['파일 이름', '이름', '문제 번호', '이해도 평가', '실제 이해도', 'frame', '데이터'])

prev = time.time()
for cur in using_list:
    file_name = cur[0]
    print(file_name)
    cap = cv2.VideoCapture(base + file_name)
    get_movement_distance(cap, frame_interval)

print(time.time() - prev)
f.close()
