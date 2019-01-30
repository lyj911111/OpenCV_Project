import cv2
import numpy as np

def nothing(x):
    pass

# 이미지 불러오기
img = cv2.imread('2.bmp')

# Blur 필터링 테스트 ###################
#img = cv2.blur(img, (4, 4))
#img = cv2.medianBlur(img, 9)
img = cv2.GaussianBlur(img, (13,13),0)
#img = cv2.bilateralFilter(img,9,75,75)

#########################################
# cv2.imshow('a', imga)
# cv2.imshow('b', imgb)
# cv2.imshow('c', imgc)
# cv2.imshow('d', imgd)

#img = cv2.imread('ko.jpg', cv2.IMREAD_UNCHANGED)
cv2.namedWindow("Trackbars", cv2.WINDOW_NORMAL)

# create trackbars for color change
cv2.createTrackbar("graybar", "Trackbars", 255, 255, nothing)  # 135  V
cv2.createTrackbar("bluebar", "Trackbars", 255, 255, nothing)  # 110  V
cv2.createTrackbar("greenbar", "Trackbars", 255, 255, nothing)  # 101  V
cv2.createTrackbar("redbar", "Trackbars", 255, 255, nothing)  # 101    V
cv2.createTrackbar("hsv hbar", "Trackbars", 128, 255, nothing)  # 255
cv2.createTrackbar("hsv sbar", "Trackbars", 128, 255, nothing)  # 115
cv2.createTrackbar("hsv vbar", "Trackbars", 255, 255, nothing)  # 141  V
cv2.createTrackbar("hsl hbar", "Trackbars", 128, 255, nothing)  # 255
cv2.createTrackbar("hsl sbar", "Trackbars", 255, 255, nothing)  # 170  V
cv2.createTrackbar("hsl lbar", "Trackbars", 128, 255, nothing)  # 175

# cv2.createTrackbar("graybar_", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("bluebar_", "Trackbars", 90, 255, nothing)  #  V
cv2.createTrackbar("greenbar_", "Trackbars", 90, 255, nothing)  # V
cv2.createTrackbar("redbar_", "Trackbars", 90, 255, nothing)    # V
cv2.createTrackbar("hsv hbar_", "Trackbars", 128, 255, nothing)
cv2.createTrackbar("hsv sbar_", "Trackbars", 128, 255, nothing)
cv2.createTrackbar("hsv vbar_", "Trackbars", 90, 255, nothing)  #  V
cv2.createTrackbar("hsl hbar_", "Trackbars", 128, 255, nothing)
cv2.createTrackbar("hsl sbar_", "Trackbars", 128, 255, nothing)
cv2.createTrackbar("hsl lbar_", "Trackbars", 128, 255, nothing)

cv2.createTrackbar("k1", "Trackbars", 25, 50, nothing)
cv2.createTrackbar("k2", "Trackbars", 25, 50, nothing)
cv2.createTrackbar("itera", "Trackbars", 5, 10, nothing)
cv2.createTrackbar("rank", "Trackbars", 5, 10, nothing)


while(1):

    frame2 = img.copy()

    # col,row,_ = frame.shape # frame 화면크기 출력, (y ,x) = (480x640)
    # print(col,row)
    frame2 = img.copy()  # 영상원본

    # 카메라 일때만 사용.
    #img = cv2.GaussianBlur(img, (3, 3), 0)  # 원본에 가우시안 필터적용

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(img)  # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

    frame_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)  # H,L,S 분리
    kernel = np.ones((3, 3), np.uint8)

    gray_c = cv2.getTrackbarPos("graybar", "Trackbars")
    blue_c = cv2.getTrackbarPos("bluebar", "Trackbars")
    green_c = cv2.getTrackbarPos("greenbar", "Trackbars")
    red_c = cv2.getTrackbarPos("redbar", "Trackbars")
    hsv_h_c = cv2.getTrackbarPos("hsv hbar", "Trackbars")
    hsv_s_c = cv2.getTrackbarPos("hsv sbar", "Trackbars")
    hsv_v_c = cv2.getTrackbarPos("hsv vbar", "Trackbars")
    hsl_h_c = cv2.getTrackbarPos("hsl hbar", "Trackbars")
    hsl_s_c = cv2.getTrackbarPos("hsl sbar", "Trackbars")
    hsl_l_c = cv2.getTrackbarPos("hsl lbar", "Trackbars")

    gray_c_ = cv2.getTrackbarPos("graybar_", "Trackbars")
    blue_c_ = cv2.getTrackbarPos("bluebar_", "Trackbars")
    green_c_ = cv2.getTrackbarPos("greenbar_", "Trackbars")
    red_c_ = cv2.getTrackbarPos("redbar_", "Trackbars")
    hsv_h_c_ = cv2.getTrackbarPos("hsv hbar_", "Trackbars")
    hsv_s_c_ = cv2.getTrackbarPos("hsv sbar_", "Trackbars")
    hsv_v_c_ = cv2.getTrackbarPos("hsv vbar_", "Trackbars")
    hsl_h_c_ = cv2.getTrackbarPos("hsl hbar_", "Trackbars")
    hsl_s_c_ = cv2.getTrackbarPos("hsl sbar_", "Trackbars")
    hsl_l_c_ = cv2.getTrackbarPos("hsl lbar_", "Trackbars")

    k1 = cv2.getTrackbarPos("k1", "Trackbars")
    k2 = cv2.getTrackbarPos("k2", "Trackbars")
    itera = cv2.getTrackbarPos("itera", "Trackbars")
    rank = cv2.getTrackbarPos("rank", "Trackbars")

    _, gray1 = cv2.threshold(gray_frame, gray_c, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, blue_c, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, green_c, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, red_c, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, hsv_h_c, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, hsv_s_c, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, hsv_v_c, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, hsl_h_c, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, hsl_s_c, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, hsl_l_c, 255, cv2.THRESH_BINARY_INV)

    _, gray_ = cv2.threshold(gray_frame, gray_c_, 255, cv2.THRESH_BINARY)
    _, blue_ = cv2.threshold(blue, blue_c_, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, green_c_, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, red_c_, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, hsv_h_c_, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, hsv_s_c_, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, hsv_v_c_, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, hsl_h_c_, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, hsl_s_c_, 255, cv2.THRESH_BINARY)
    _, S_ = cv2.threshold(S, hsl_l_c_, 255, cv2.THRESH_BINARY)

    final_mask = gray1
    final_mask = cv2.bitwise_and(final_mask, blue1)
    final_mask = cv2.bitwise_and(final_mask, green1)
    final_mask = cv2.bitwise_and(final_mask, red1)
    final_mask = cv2.bitwise_and(final_mask, h1)
    final_mask = cv2.bitwise_and(final_mask, s1)
    final_mask = cv2.bitwise_and(final_mask, v1)
    final_mask = cv2.bitwise_and(final_mask, H1)
    final_mask = cv2.bitwise_and(final_mask, L1)
    final_mask = cv2.bitwise_and(final_mask, S1)

    final_mask = cv2.bitwise_and(final_mask, gray_)
    final_mask = cv2.bitwise_and(final_mask, blue_)
    final_mask = cv2.bitwise_and(final_mask, green_)
    final_mask = cv2.bitwise_and(final_mask, red_)
    # final_mask = cv2.bitwise_and(final_mask, h_)
    # final_mask = cv2.bitwise_and(final_mask, s_)
    final_mask = cv2.bitwise_and(final_mask, v_)
    # final_mask = cv2.bitwise_and(final_mask, H_)
    # final_mask = cv2.bitwise_and(final_mask, L_)
    # final_mask = cv2.bitwise_and(final_mask, S_)


    final_mask = cv2.dilate(final_mask, kernel, iterations=4)
    final_mask = cv2.erode(final_mask, kernel, iterations=4)

    #final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)
    #final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)
    # final_mask = cv2.blur(final_mask, (4, 4))

    #final_mask = cv2.erode(final_mask, kernel, iterations=4)


    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    #################### 리벳 중심좌표값 자동 저장용 ##########################

    Rivet_center = []

    # _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    # if len(contours) != 0:
    #     for contour in contours:
    #         if (cv2.contourArea(contour) > 30) and (cv2.contourArea(contour) < 500):  # **필요한 면적을 찾아 중심점 좌표를 저장
    #             ball_area = cv2.contourArea(contour)
    #             mom = contour
    #             M = cv2.moments(mom)
    #             cx_origin = int(M['m10'] / M['m00'])
    #             cy_origin = int(M['m01'] / M['m00'])
    #
    #             cv2.circle(img, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시
    #             Rivet_center.append([cx_origin, cy_origin])


    final_mask = cv2.resize(final_mask, (1945, 1500))
    cv2.imshow('damm', final_mask)
    #
    img =cv2.resize(img, (1940, 1500))
    cv2.imshow('ori',img)


    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
