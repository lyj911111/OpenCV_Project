import cv2
import numpy as np

# 검출할 영역(관심영역)의 가로,세로 크기 지정. <175 x 125 = 21,875 사각형 면적 크기>
ROI_w = 175
ROI_h = 125

# ROI 좌표 지정.
ROI_list = [
    [(1300, 5)], # 까지 첫번째 줄

    [(5, 150)],
    [(250, 150)],
    [(500, 150)],
    [(750, 150)],
    [(990, 150)],
    [(1235, 150)], # 까지 두번째줄

    [(340, 340)],
    [(620, 340)],
    [(890, 340)],
    [(1160, 340)], # 까지 세번째 줄

    [(470, 560)],
    [(1070, 560)], # 까지 네번째 줄
]

def nothing(x):
    pass

# 면적을 퍼센트로 구해줌
def areaToPercentage(area):
    global ROI_h, ROI_w
    percentage = 100 * area / (ROI_w * ROI_h)
    return percentage  # [%]단위

# Contour 내부의 구멍을 모두 채워줌.
def fullfill_inside(im_in):

    im_in = cv2.bitwise_not(im_in)

    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255.
    th, im_th = cv2.threshold(im_in, 220, 255, cv2.THRESH_BINARY_INV);
    cv2.imshow('im_th', im_th)

    # Copy the thresholded image.
    im_floodfill = im_th.copy()
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255);

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv

    return im_out

# 트렉바 생성
cv2.namedWindow('trackbarwindow')
cv2.createTrackbar('Lower_R', 'trackbarwindow', 0, 255, nothing)
cv2.createTrackbar('Lower_G', 'trackbarwindow', 80, 255, nothing)
cv2.createTrackbar('Lower_B', 'trackbarwindow', 0, 255, nothing)
cv2.createTrackbar('Upper_R', 'trackbarwindow', 255, 255, nothing)
cv2.createTrackbar('Upper_G', 'trackbarwindow', 255, 255, nothing)
cv2.createTrackbar('Upper_B', 'trackbarwindow', 255, 255, nothing)
cv2.createTrackbar('Gaussian_Blur', 'trackbarwindow', 0, 255, nothing)

while(1):
    img = cv2.imread('Test.PNG')

    # ROI의 사각형 마스크를 씌우기 위해
    h, w = img.shape[:2]
    rec_mask = np.zeros((h, w), np.uint8)
    for i in range(len(ROI_list)):
        frame = cv2.rectangle(rec_mask, ROI_list[i][0], (ROI_list[i][0][0] + ROI_w, ROI_list[i][0][1] + ROI_h), (255, 255, 255), -1)
    #cv2.imshow('recmask', rec_mask)

    l_r = cv2.getTrackbarPos('Lower_R', 'trackbarwindow')
    l_g = cv2.getTrackbarPos('Lower_G', 'trackbarwindow')
    l_b = cv2.getTrackbarPos('Lower_B', 'trackbarwindow')
    u_r = cv2.getTrackbarPos('Upper_R', 'trackbarwindow')
    u_g = cv2.getTrackbarPos('Upper_G', 'trackbarwindow')
    u_b = cv2.getTrackbarPos('Upper_B', 'trackbarwindow')
    Gauss_blur = cv2.getTrackbarPos('Gaussian_Blur', 'trackbarwindow')

    # 가우시안 필터, 짝수일때 +1, 홀수일때 그데로
    if Gauss_blur % 2 == 1:     # 홀수
        pass
    else:                       # 짝수
        Gauss_blur = Gauss_blur + 1
    # 가우시안 필터
    img = cv2.GaussianBlur(img, (Gauss_blur, Gauss_blur), 0)

    frame = img
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ROI 설정구역 Display
    for i in range(len(ROI_list)):
        frame = cv2.rectangle(frame, ROI_list[i][0], (ROI_list[i][0][0] + ROI_w, ROI_list[i][0][1] + ROI_h), (150, 50, 150), 5)
        cv2.putText(frame, 'ROI%d' % (i + 1), (ROI_list[i][0][0], ROI_list[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (150, 50, 150), 2, cv2.LINE_AA)

    # define range of blue color in HSV (B,G,R)
    # lower_blue = np.array([110,50,50])
    lower = np.array([l_b, l_g, l_r])
    upper = np.array([u_r, u_g, u_b])

    # Threshold the HSV image to get all range
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask= mask)
    # 사각마스크로 관심영역 범위만 추출함.
    res_rec = cv2.bitwise_and(mask, mask, mask= rec_mask)

    # # 사각 마스크 위에 원본 씌우기
    # frame_rec_res = cv2.bitwise_and(frame, frame, mask=res_rec)
    # cv2.imshow('rec_mask+result', frame_rec_res)

    # Closed shape에 채우기.
    im_floodfill = res_rec.copy()                         # 스레솔드 마스크 복사.
    im_floodfill = fullfill_inside(im_floodfill)          # 내부 Hole이 채워진 이미지 리턴.

    # 컨투어 찾기, 중심점 찾기
    # cnt = 0
    _, contours, _ = cv2.findContours(im_floodfill, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    if len(contours) != 0:
        for contour in contours:
            if (cv2.contourArea(contour) > 0) and (cv2.contourArea(contour) < 21875):  # **필요한 면적을 찾아 중심점 표시
                ball_area = cv2.contourArea(contour)
                print(ball_area)
                mom = contour
                cv2.drawContours(frame, [mom], 0, (0, 255, 0), 2)
                M = cv2.moments(mom)
                cx_origin = int(M['m10'] / M['m00'])
                cy_origin = int(M['m01'] / M['m00'])
                #cv2.circle(frame, (cx_origin, cy_origin), 10, (0, 0, 255), -1) # Center of puck

                # cv2.putText(frame, 'area : %d' % (ball_area), (ROI_list[cnt][0][0], ROI_list[cnt][0][1]+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255),
                #                2, cv2.LINE_AA)
                ball_area = areaToPercentage(ball_area)

                if ball_area > 50:
                    cv2.putText(frame, '%d%%' % (ball_area), (cx_origin - 30, cy_origin), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3, cv2.LINE_AA)
                else:
                    cv2.putText(frame, 'NG', (cx_origin - 30, cy_origin), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
                # cnt = cnt + 1
                # print(cx_origin, cy_origin) # 중심점값읽기

    print("****" * 30)
    # cv2.putText(frame, 'Number of Gasket : %d' % (cnt), (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    #cv2.imshow('blur', blur)
    cv2.imshow('inside fullfill', im_floodfill)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
