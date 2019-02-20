import cv2
import time
import serial
import datetime
from PIL import Image
import numpy as np


def houghCircle():
    img1 = cv2.imread('2.png')    # 원형이 있는 이미지를 올림.
    img2 = img1.copy()

    img2 = cv2.GaussianBlur(img2, (9, 9), 0) # 0~9까지 가우시안 필터로 흐리게 만들어 조절함.

    imgray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) # 그레이 이미지로 바꿔서 실행해야함.


    # param1 = 250, param2 = 20
                                 # 원본과 비율 / 찾은 원들간의 최소 중심거리 / param1, param2를 조절해 원을 찾음
    circles = cv2.HoughCircles(imgray, cv2.HOUGH_GRADIENT, 1, 10, param1=250, param2=20, minRadius=5, maxRadius=8)

    if circles is not None:
        circles = np.uint16(np.around(circles))

        print(circles)

        cnt = 0
        for i in circles[0, :]:
            cv2.circle(img1, (i[0], i[1]), i[2], (0, 0, 255), 2)    # 원 외곽 컨투어 표시.
            cnt = cnt + 1

        for i in circles[0, :]:
            cv2.circle(img1, (i[0], i[1]), 3, (255, 0, 40), -1)     # 원의 중심점을 표시

        #cv2.imshow('ori',img2)
        cv2.imshow('HoughCircle', img1)
        print(cnt)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('원을 찾을 수 없음')


houghCircle()