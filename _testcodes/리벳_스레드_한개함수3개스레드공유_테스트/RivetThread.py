from RivetDetect import RivetDetect
import threading
import numpy as np
import cv2
import time

# 시리얼 번호를 여기서 쓰면, 모든 쓰레드로 시리얼 번호가 날라감.
serialnum = 99994444

# 3개의 카메라를 멀티스레드로 동시에 실행
def camera1():
    RivetDetect.execute(0, serialnum)
def camera2():
    RivetDetect.execute(1, serialnum)
def camera3():
    RivetDetect.execute(2, serialnum)

# 스레드를 실행하기 위해 객체(t1, t2, t3)를 할당하고 인자를 대입함(인자 없음)
# target = 함수이름, args = 전달받는 인자
t1 = threading.Thread(target=camera3, args=(), daemon=True)
t2 = threading.Thread(target=camera2, args=(), daemon=True)
t3 = threading.Thread(target=camera1, args=(), daemon=False)    # 0번 카메라가 메인 쓰레드, 종료시 모두 같이 종료됨.

def execute():
    # 반드시 객체.start()를 붙여야 스레드가 동시에 작동 시작.
    t1.start()
    t2.start()
    t3.start()

if __name__ == "__main__":

    execute()
