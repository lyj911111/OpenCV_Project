import cv2
import time
import serial
import datetime
from PIL import Image
import numpy as np


cap = cv2.VideoCapture(1)

while True:
    _, frame = cap.read()

    copy_frame = frame.copy()                               # 다듬기 위해 원본 복사
    copy_frame = cv2.GaussianBlur(copy_frame, (3, 3), 0)    # 복사본에 가우시안 필터
    gray = cv2.cvtColor(copy_frame, cv2.COLOR_BGR2GRAY)     # 필터위에 그레이로 씌워줌

    #_, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 60, param1=60, param2=50, minRadius=0, maxRadius=0) # 그레이 이미지에서 원형 검출

    # 원형 탐지
    if circles is not None:
        circles = np.uint16(np.around(circles))

        print(circles) # 탐지된 원의 리스트 출력

        # 탐지된 원의 외곽선을 그려줌
        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (255, 255, 0), 2)

    else:
        print('원을 찾을 수 없음')

    cv2.imshow('gray', gray)
    cv2.imshow('fr', frame)         # 그레이에서 추출한 원을 표시


    # 종료키
    if cv2.waitKey(1) & 0xff == ord('q'):
        break