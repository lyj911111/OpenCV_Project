import cv2
import numpy as np

def nothing(x):
    pass

# 트렉바 생성
cv2.namedWindow('trackbarwindow')
cv2.createTrackbar('Lower_R', 'trackbarwindow', 30, 255, nothing)
cv2.createTrackbar('Lower_G', 'trackbarwindow', 25, 255, nothing)
cv2.createTrackbar('Lower_B', 'trackbarwindow', 76, 255, nothing)
cv2.createTrackbar('Upper_R', 'trackbarwindow', 100, 255, nothing)
cv2.createTrackbar('Upper_G', 'trackbarwindow', 255, 255, nothing)
cv2.createTrackbar('Upper_B', 'trackbarwindow', 255, 255, nothing)

img = cv2.imread('model.PNG')
while(1):
    #ret, frame = cap.read()

    l_r = cv2.getTrackbarPos('Lower_R', 'trackbarwindow')
    l_g = cv2.getTrackbarPos('Lower_G', 'trackbarwindow')
    l_b = cv2.getTrackbarPos('Lower_B', 'trackbarwindow')
    u_r = cv2.getTrackbarPos('Upper_R', 'trackbarwindow')
    u_g = cv2.getTrackbarPos('Upper_G', 'trackbarwindow')
    u_b = cv2.getTrackbarPos('Upper_B', 'trackbarwindow')

    frame = img
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV (B,G,R)
    # lower_blue = np.array([110,50,50])
    lower_blue = np.array([l_b, l_g, l_r])
    upper_blue = np.array([u_r, u_g, u_b])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Closed shape에 채우기.
    im_floodfill = mask.copy()                         # 스레솔드 마스크 복사.
    h, w = mask.shape[:2]
    mask2 = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask2, (0, 0), 255)     # closed 된 부분의 구멍을 채움.

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask= mask)

    # 컨투어 찾기, 중심점 찾기
    cnt = 0
    _, contours, _ = cv2.findContours(im_floodfill, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    if len(contours) != 0:
        for contour in contours:
            if (cv2.contourArea(contour) > 100) and (cv2.contourArea(contour) < 100000):  # **필요한 면적을 찾아 중심점 표시
                ball_area = cv2.contourArea(contour)
                mom = contour
                cv2.drawContours(res, [mom], 0, (0, 0, 255), 2)
                M = cv2.moments(mom)
                cx_origin = int(M['m10'] / M['m00'])
                cy_origin = int(M['m01'] / M['m00'])
                cv2.circle(frame, (cx_origin, cy_origin), 10, (0, 0, 255), -1) # Center of puck
                #print(cx_origin, cy_origin) # 중심점값읽기
                cnt =  cnt + 1
    print("가스켓 갯수:", cnt)
    cv2.putText(frame, 'Number of Gasket : %d' % (cnt), (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('im_floodfill', im_floodfill)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
