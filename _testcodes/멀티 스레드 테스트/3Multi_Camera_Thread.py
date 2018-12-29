import threading
import numpy as np
import cv2
from time import sleep

# 3개의 카메라를 멀티스레드로 동시에 실행하는 테스트.

def camera1():
    cap = cv2.VideoCapture(0)	# 첫번째 카메라
    while True:
        ret, frame = cap.read()
        cv2.imshow('camera1', frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

def camera2():
    cap = cv2.VideoCapture(1)	# 두번째 카메라
    while True:
        ret, frame = cap.read()
        cv2.imshow('camera2', frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

def camera3():
    cap = cv2.VideoCapture(2)	# 세번째 카메라
    while True:
        ret, frame = cap.read()
        cv2.imshow('camera3', frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

# 객체를 할당하고 인자를 대입함.
# target = 함수이름, args = 전달받는 인자
t1 = threading.Thread(target=camera1, args=())  
t2 = threading.Thread(target=camera2, args=())
t3 = threading.Thread(target=camera3, args=())

# 반드시 객체뒤에 .start()를 붙여야 스레드가 가동됨.
t1.start()
t2.start()
t3.start()