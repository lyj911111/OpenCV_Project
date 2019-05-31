'''
    마우스 드레그 위치지정 사물 위치 탐지코드.

    사용방법:
        1. 코드 실행
        2. 키 i 를 누르고 마우스 드레그로 영역 지정
        3. 지정한 영역의 HSV(채도)를 기준으로 위치 탐지
'''

import numpy as np
import cv2

col, width, row, height = -1, -1, -1, -1
frame = None
frame2 = None
inputmode = False
rectangle = False
trackWindow = None
roi_hist = None


# 키보드 'i' 키를 누를때, 화면을 멈추고 마우스 클릭 모드 활성화
def onMouse(event, x, y, flags, param):
    global col, width, row, height, frame, frame2, inputmode
    global rectangle, roi_hist, trackWindow

    if inputmode:
        # 왼쪽 마우스 클릭시 retangle 플레그 활성화,
        if event == cv2.EVENT_LBUTTONDOWN:
            rectangle = True                # 마우스가 움직일때 이벤트를 발생시키기 위해
            col, row = x, y                 # 왼쪽마우스 클릭시 좌표를 기억.
            print(x, y)
        # 마우스를 움직일 때 발생 이벤트
        elif event == cv2.EVENT_MOUSEMOVE:
            if rectangle:
                # 멈춘 화면에
                frame = frame2.copy()
                cv2.rectangle(frame, (col, row), (x, y), (0, 255, 0), 2)
                cv2.imshow('frame', frame)
        elif event == cv2.EVENT_LBUTTONUP:
            inputmode = False
            rectangle = False
            cv2.rectangle(frame, (col, row), (x, y), (0, 255, 0), 2)
            height, width = abs(row - y), abs(col - x)
            trackWindow = (col, row, width, height)
            roi = frame[row:row + height, col:col + width]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            roi_hist = cv2.calcHist([roi], [0], None, [180], [0, 180])
            cv2.normalize(roi_hist, roi_hist, 0, 255 , cv2.NORM_MINMAX)
    return

def camShift():
    global frame2, frame, inputmode, trackWindow, roi_hist

    try:
        cap = cv2.VideoCapture(0)
    except Exception as e:
        print(e)
        return

    ret, frame = cap.read()

    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', onMouse, param=(frame, frame2))

    termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    while True:
        # 영상을 취득
        ret, frame = cap.read()

        if not ret:
            break

        # 추적물체를 표시.
        if trackWindow is not None:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
            ret, trackWindow = cv2.meanShift(dst, trackWindow, termination)

            x, y, w, h = trackWindow
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('frame', frame)

        k = cv2.waitKey(60) & 0xFF
        if k == 27: break

        # i 키를 누를때 input Mode 활성화하고 화면을 멈춤.
        if k == ord('i'):
            print('Select Area for Camshift and Enter a Key')
            inputmode = True
            frame2 = frame.copy()

            while inputmode:
                cv2.imshow('frame', frame)
                cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()

camShift()