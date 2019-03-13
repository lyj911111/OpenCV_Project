import cv2
import time
import serial
import datetime
from PIL import Image
import numpy as np

# 2대의 카메라 해상도 설정 및 출력.
cap0 = cv2.VideoCapture(0)
cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # Width 4608
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 960) # Height 3288
print("첫번째 카메라 현재 해상도 %d x %d" %(cap0.get(3), cap0.get(4)))

cap1 = cv2.VideoCapture(1)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 4608) # Width 4608
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 3288) # Height 3288
print("두번째 카메라 현재 해상도 %d x %d" %(cap1.get(3), cap1.get(4)))


def houghCircle():

    while True:

        # 프레임 읽기
        ret, frame = cap1.read()
        # 화면 크기 조절 (본인에게 맞는 해상도 조절)
        result = cv2.resize(frame, (1280, 960), interpolation=cv2.INTER_LINEAR)
        img_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)  # gray로 변환.



        # param1 = 250, param2 = 20
                                     # 원본과 비율 / 찾은 원들간의 최소 중심거리 / param1, param2를 조절해 원을 찾음 250 20 5 30
        circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 10, param1=60, param2=19, minRadius=10, maxRadius=13)

        if circles is not None:
            circles = np.uint16(np.around(circles))

            #print(circles)

            cnt = 0
            for i in circles[0, :]:
                cv2.circle(result, (i[0], i[1]), i[2], (0, 0, 255), 2)    # 원 외곽 컨투어 표시.
                cnt = cnt + 1

            for i in circles[0, :]:
                cv2.circle(result, (i[0], i[1]), 3, (255, 0, 40), -1)     # 원의 중심점을 표시

            #cv2.imshow('ori',img2)
            cv2.imshow('HoughCircle', result)
            print(cnt)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print('원을 찾을 수 없음')

    cap1.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # 메인함수
    houghCircle()