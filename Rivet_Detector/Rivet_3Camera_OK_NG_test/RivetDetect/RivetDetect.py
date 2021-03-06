# Author  : Won Jae Lee
# Version : 3.7.1

import cv2
import numpy as np
import serial
import datetime
import time

def nothing(x):
    pass

# 사용할 카메라를 인자로 받음 ( 선택카메라(0,1,2) )
def execute(cam):

    # 사용할 카메라 설정.
    cap = cv2.VideoCapture(cam)
    cv2.namedWindow("Trackbars" + str(cam), cv2.WINDOW_NORMAL)

    # 플레그, 초기값
    Start_Rivet_flag = 0
    Rivet_tuple = []                                  # 튜플값을 저장할 리스트
    camm = cam                                        # 예외처리 박스 int형 변수 전달.
    cam = str(cam)                                    # 실행창 번호 할당을 위해

    # FIND_BLACK
    cv2.createTrackbar("graybar", "Trackbars", 255, 255, nothing)  # 135
    cv2.createTrackbar("bluebar", "Trackbars", 225, 255, nothing)  # 110
    cv2.createTrackbar("greenbar", "Trackbars", 240, 255, nothing)  # 101
    cv2.createTrackbar("redbar", "Trackbars", 255, 255, nothing)  # 101
    cv2.createTrackbar("hsv hbar", "Trackbars", 255, 255, nothing)  # 255
    cv2.createTrackbar("hsv sbar", "Trackbars", 255, 255, nothing)  # 115
    cv2.createTrackbar("hsv vbar", "Trackbars", 245, 255, nothing)  # 141
    cv2.createTrackbar("hsl hbar", "Trackbars", 215, 255, nothing)  # 255
    cv2.createTrackbar("hsl sbar", "Trackbars", 225, 255, nothing)  # 170
    cv2.createTrackbar("hsl lbar", "Trackbars", 200, 255, nothing)  # 175

    # cv2.createTrackbar("graybar_", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("bluebar_", "Trackbars", 0, 255, nothing)  # 33
    cv2.createTrackbar("greenbar_", "Trackbars", 0, 255, nothing)  # 35
    cv2.createTrackbar("redbar_", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("hsv hbar_", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("hsv sbar_", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("hsv vbar_", "Trackbars", 50, 255, nothing)
    cv2.createTrackbar("hsl hbar_", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("hsl sbar_", "Trackbars", 100, 255, nothing)
    cv2.createTrackbar("hsl lbar_", "Trackbars", 50, 255, nothing)

    cv2.createTrackbar("k1", "Trackbars", 21, 50, nothing)
    cv2.createTrackbar("k2", "Trackbars", 33, 50, nothing)
    cv2.createTrackbar("itera", "Trackbars", 6, 10, nothing)
    cv2.createTrackbar("rank", "Trackbars", 4, 10, nothing)

    while True:

        _, frame = cap.read()

        # col,row,_ = frame.shape # frame 화면크기 출력, (y ,x) = (480x640)
        # print(col,row)
        frame2 = frame.copy()  # 영상원본

        frame = cv2.GaussianBlur(frame, (3, 3), 0)              # 원본에 가우시안 필터적용
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blue, green, red = cv2.split(frame)                     # 원본에서 BGR 분리
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)      # HSV(색상, 채도, 명도) 분리
        h, s, v = cv2.split(frame_hsv)                          # 분리후 저장.

        frame_hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)      # BGR -> HLS로
        H, L, S = cv2.split(frame_hls)                          # H,L,S 분리
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
        final_mask = cv2.dilate(final_mask, kernel, iterations=1)
        # final_mask = cv2.dilate(final_mask, kernel, iterations=1)
        # final_mask = cv2.dilate(final_mask, kernel, iterations=1)
        # final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)

        # final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)
        final_mask = cv2.blur(final_mask, (2, 2))

        result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

        ############# 테스트 ##########################################
        dilate = cv2.dilate(final_mask, kernel, iterations=1)
        di_di = cv2.dilate(dilate, kernel, iterations=1)
        erosion = cv2.erode(final_mask, kernel, iterations=1)
        ero_ero = cv2.erode(erosion, kernel, iterations=1)
        # opening = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)
        # closing = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)

        ############# 테스트 ##############################################

        #################### 리벳 중심좌표값 자동 저장용 ##########################
        Rivet_center = []

        _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
        if len(contours) != 0:
            for contour in contours:
                if (cv2.contourArea(contour) > 30) and (cv2.contourArea(contour) < 500):  # **필요한 면적을 찾아 중심점 표시
                    ball_area = cv2.contourArea(contour)
                    mom = contour
                    M = cv2.moments(mom)
                    cx_origin = int(M['m10'] / M['m00'])
                    cy_origin = int(M['m01'] / M['m00'])

                    cv2.circle(frame, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시
                    Rivet_center.append([cx_origin, cy_origin])  # 중심좌표 list에 추가

        ##### 자동 좌표값 저장하기 #####
        print(Rivet_center)  # 자동 저장된 중심점값 출력
        Rivet_num = len(Rivet_center)  # 자동 저장된 리벳의 갯수값 저장.

        for i in range(Rivet_num):
            Rivet_tuple.append(tuple(Rivet_center[i]))  # 자동 저장된 리벳 좌표값을 튜플로 변환후 리스트에 저장. -> (Circle 마크에 쓰기 위해)

        reverse = cv2.bitwise_not(final_mask)
        reverse_copy = reverse.copy()

        # # ** 리벳을 검출할 위치에 원으로 좌표 표시.
        # for i in range(Rivet_num):
        #     reverse_copy = cv2.circle(reverse_copy, Rivet_tuple[i], 10, (0, 0, 0), -1)      # 가운데 점 픽셀값 확인용 (x,y)값으로 받음.
        #     frame = cv2.circle(frame, Rivet_tuple[i], 10, (0, 255, 255), -1)                # 원본에도 색상이 있는 점 표시.


        cv2.imshow('Frame' + cam, frame)                      # 원본
        cv2.imshow('result' + cam, final_mask)                # 필터링후
        #cv2.imshow('reverse' + cam, reverse)                  # 반전 (픽셀값을 찍어보기 위해 흑백)
        cv2.imshow('location_check' + cam, reverse_copy)      # 리벳위치 픽셀체크 위치 확인용

        # 종료키
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

if __name__ == "__main__":

    #카메라 번호 선택 0~2
    execute(1)

