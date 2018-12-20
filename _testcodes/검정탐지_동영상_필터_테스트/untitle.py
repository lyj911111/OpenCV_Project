import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(1)
cv2.namedWindow("Trackbars", cv2.WINDOW_NORMAL)

cv2.createTrackbar("hsv hbar", "Trackbars", 136, 255, nothing)
cv2.createTrackbar("hsv sbar", "Trackbars", 145, 255, nothing)
cv2.createTrackbar("hsv vbar", "Trackbars", 78, 255, nothing)
cv2.createTrackbar("hsl hbar", "Trackbars", 127, 255, nothing)
cv2.createTrackbar("hsl sbar", "Trackbars", 107, 255, nothing) # 75
cv2.createTrackbar("hsl lbar", "Trackbars", 255, 255, nothing)

while(1):

    ret, frame = cap.read()
    frame2 = frame.copy()  # 영상원본

    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(frame)                     # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)      # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)                          # 분리후 저장.

    frame_hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)      # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)                          # H,L,S 분리

    # define range of blue color in HSV
    lower_hue = np.array([0, 0, 0])
    upper_hue = np.array([50, 50, 50])

    hsv_h_c = cv2.getTrackbarPos("hsv hbar", "Trackbars")
    hsv_s_c = cv2.getTrackbarPos("hsv sbar", "Trackbars")
    hsv_v_c = cv2.getTrackbarPos("hsv vbar", "Trackbars")
    hsl_h_c = cv2.getTrackbarPos("hsl hbar", "Trackbars")
    hsl_s_c = cv2.getTrackbarPos("hsl sbar", "Trackbars")
    hsl_l_c = cv2.getTrackbarPos("hsl lbar", "Trackbars")

    hsv_h_c_ = cv2.getTrackbarPos("hsv hbar_", "Trackbars")
    hsv_s_c_ = cv2.getTrackbarPos("hsv sbar_", "Trackbars")
    hsv_v_c_ = cv2.getTrackbarPos("hsv vbar_", "Trackbars")
    hsl_h_c_ = cv2.getTrackbarPos("hsl hbar_", "Trackbars")
    hsl_s_c_ = cv2.getTrackbarPos("hsl sbar_", "Trackbars")
    hsl_l_c_ = cv2.getTrackbarPos("hsl lbar_", "Trackbars")

    _, h1 = cv2.threshold(h, hsv_h_c, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, hsv_s_c, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, hsv_v_c, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, hsl_h_c, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, hsl_s_c, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, hsl_l_c, 255, cv2.THRESH_BINARY_INV)

    final_mask = cv2.inRange(frame_hsv, lower_hue, upper_hue)

    final_mask = cv2.bitwise_and(final_mask, h1)
    final_mask = cv2.bitwise_and(final_mask, s1)
    final_mask = cv2.bitwise_and(final_mask, v1)
    final_mask = cv2.bitwise_and(final_mask, H1)
    final_mask = cv2.bitwise_and(final_mask, L1)
    final_mask = cv2.bitwise_and(final_mask, S1)

    kernel = np.ones((3,3), np.uint8)
    erosion = cv2.erode(final_mask, kernel, iterations=1)
    dilation = cv2.dilate(final_mask, kernel, iterations=1)

    ero_dil = cv2.erode(final_mask, kernel, iterations=1)
    ero_dil = cv2.dilate(ero_dil, kernel, iterations=1)
    ero_dil_dil = cv2.dilate(ero_dil, kernel, iterations=1)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= final_mask)

    cv2.imshow('ori', frame2)
    cv2.imshow('mask', final_mask)
    cv2.imshow('ero', erosion)
    cv2.imshow('dil', dilation)
    cv2.imshow('ero_dil', ero_dil)
    cv2.imshow('ero_dil_dil', ero_dil_dil)



    if cv2.waitKey(1) & 0xff == ord('q'):
        break
