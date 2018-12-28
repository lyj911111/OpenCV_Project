import numpy as np
import cv2

rect = (0,0,0,0)        # 사각형 4지점을 저장할 초기값.
startPoint = False
endPoint = False

# 사각형 4지점을 을 연속으로 저장할 리스트 -> (화면에 연속으로 사각형을 만들기 위해)
rectangle = []

# 마우스 이벤트에 따른 사각형 출력
def on_mouse(event,x,y,flags,params):

    global rect, startPoint, endPoint

    # get mouse click
    if event == cv2.EVENT_LBUTTONDOWN:

        if startPoint == True and endPoint == True:
            startPoint = False
            endPoint = False
            rect = (0, 0, 0, 0)

        if startPoint == False:
            rect = (x, y, 0, 0)
            startPoint = True

        elif endPoint == False:
            rect = (rect[0], rect[1], x, y)
            endPoint = True
            rectangle.append([rect[0], rect[1], rect[2], rect[3]])  # <= 사각형 4지점을 리스트에다 계속 추가, 연속 사각형을 만들기 위해

cap = cv2.VideoCapture(0)
waitTime = 50

#Reading the first frame
(grabbed, frame) = cap.read()

while(cap.isOpened()):

    (grabbed, frame) = cap.read()

    # 마우스 클릭 이벤트를 만들기 위한 기초작업.
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', on_mouse)

    # 사각형 그리기
    if startPoint == True and endPoint == True:
        cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 255), 2)

    # 사각형을 그리면 그 자리에 계속 사각형을 남기도록 루프를 돌림.
    for i in range(len(rectangle)):
        cv2.rectangle(frame, (rectangle[i][0], rectangle[i][1]), (rectangle[i][2], rectangle[i][3]), (255, 0, 0), 2)

    cv2.imshow('frame',frame)

    key = cv2.waitKey(waitTime)

    # 사각형 위치좌표 리스트 출력
    print(rectangle)

    # ESC 누르면 종료
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()