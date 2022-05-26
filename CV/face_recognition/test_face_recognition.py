import numpy as np
import cv2
import time

face_cascade = cv2.CascadeClassifier('haarcascade_frontface.xml')
cap = cv2.VideoCapture(0)  # 노트북 웹캠을 카메라로 사용
cap.set(3, 640)  # 너비
cap.set(4, 480)  # 높이

prev_x, prev_y = 0, 0
move = 0
prev = 0
move_frame_cnt = 0
prev_time = time.time()

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # 좌우 대칭
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 5)

    if len(faces):
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            p = str(x) + ', ' + str(y)
            cv2.putText(frame, p, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
            cur_x, cur_y = x, y
            move += abs(prev_x - cur_x) + abs(prev_y - cur_y)
            move_frame_cnt += 1
            prev_x, prev_y = cur_x, cur_y

    if move_frame_cnt == 25:    # 인식된 25 frame 동안의 이동 거리 계산
        print(prev, move)   # prev: 이전 25 frame 동안 움직인 거리, move: 최근 25 frame 동안 움직인 거리
        move_frame_cnt = 0
        prev = move
        move = 0
        res = 0

    cv2.imshow('test', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27 or k == ord('q'):  # Esc 키를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()
