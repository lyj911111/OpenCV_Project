import cv2
import time
import serial
import datetime
from PIL import Image
import numpy as np

# 시리얼 통신.
# NANOserial = serial.Serial(
#     port='COM3',\
#     baudrate=115200,\
#     parity=serial.PARITY_NONE,\
#     stopbits=serial.STOPBITS_ONE,\
#     bytesize=serial.EIGHTBITS,\
#     timeout=0)

# NG출력 폰트, 문자크기, 두께 설정.
font = cv2.FONT_HERSHEY_COMPLEX  # normal size sans-serif font
fontScale = 5
thickness = 4

# 사용할 카메라 설정.
cap = cv2.VideoCapture(1)
cv2.namedWindow("Trackbars", cv2.WINDOW_NORMAL)

# 플레그, 초기값
Start_Rivet_flag = 0
cnt = 0
judge = 0
Rivet_tuple = []                                  # 튜플값을 저장할 리스트
check_year = 0
check_month = 0
check_day = 0
accum = 0       # 누적 판독
OK = 0
NG = 0
serialnum = 0

def nothing(x):
    pass

def leave_log(OK, NG):
    global check_year, check_month, check_day, f
    global accum
    time = datetime.datetime.now()
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    minute = time.minute
    sec = time.second

    filename = str(year) + str(month) + str(day)
    if year != check_year and month != check_month and day != check_day:
        print("새로운 로그파일 생성")
        f = open("C:/Data_Record/log_%s.txt" %filename, 'w')
        check_year = time.year
        check_month = time.month
        check_day = time.day
        data = "     시리얼번호      //       현재 시간        //   누적 판독수   //   정상   //   불량\n"
        f.write(data)

    f = open("C:/Data_Record/log_%s.txt" % filename, 'a')
    time = str(year) + "_" + str(month) + "_" + str(day) + "_" + str(hour) + "_" + str(minute) + "_" + str(sec)
    data = str(serialnum) + "       //        "+ str(time) + "  //        " + str(accum) + "          //     " + str(OK) + "    //    " + str(NG) + '\n'
    f.write(data)
    f.close()


# FIND_BLACK
cv2.createTrackbar("graybar", "Trackbars", 145, 255, nothing) #135
cv2.createTrackbar("bluebar", "Trackbars", 170,  255, nothing) #110
cv2.createTrackbar("greenbar", "Trackbars", 101, 255, nothing) #101
cv2.createTrackbar("redbar", "Trackbars", 141,  255, nothing) #101
cv2.createTrackbar("hsv hbar", "Trackbars", 205, 255, nothing)#255
cv2.createTrackbar("hsv sbar", "Trackbars", 95, 255, nothing)#115
cv2.createTrackbar("hsv vbar", "Trackbars", 136, 255, nothing)#141
cv2.createTrackbar("hsl hbar", "Trackbars", 245, 255, nothing)#255
cv2.createTrackbar("hsl sbar", "Trackbars", 150, 255, nothing)#170
cv2.createTrackbar("hsl lbar", "Trackbars", 200, 255, nothing)#175

#cv2.createTrackbar("graybar_", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("bluebar_", "Trackbars", 13,  255, nothing)#33
cv2.createTrackbar("greenbar_", "Trackbars", 35, 255, nothing)#35
cv2.createTrackbar("redbar_", "Trackbars", 0,  255, nothing)
cv2.createTrackbar("hsv hbar_", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("hsv sbar_", "Trackbars", 20, 255, nothing)
cv2.createTrackbar("hsv vbar_", "Trackbars", 40, 255, nothing)
cv2.createTrackbar("hsl hbar_", "Trackbars", 40, 255, nothing)
cv2.createTrackbar("hsl sbar_", "Trackbars", 90, 255, nothing)
cv2.createTrackbar("hsl lbar_", "Trackbars", 65, 255, nothing)

cv2.createTrackbar("k1", "Trackbars", 5, 50, nothing)
cv2.createTrackbar("k2", "Trackbars", 30, 50, nothing)
cv2.createTrackbar("itera", "Trackbars", 1, 10, nothing)
cv2.createTrackbar("rank", "Trackbars", 0, 10, nothing)

while True:

    _, frame = cap.read()

    # col,row,_ = frame.shape # frame 화면크기 출력, (y ,x) = (480x640)
    # print(col,row)
    frame2 = frame.copy() # 영상원본

    frame = cv2.GaussianBlur(frame, (3, 3), 0)              # 원본에 가우시안 필터적용
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(frame)                     # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)      # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)                          # 분리후 저장.

    frame_hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)      # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)                          # H,L,S 분리

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
    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    #################### 리벳 중심좌표값 자동 저장용 ##########################

    if Start_Rivet_flag == 0:   # 시작할때 한번만 작동 플레그.
        Rivet_center = []

        _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
        if len(contours) != 0:
            for contour in contours:
                if (cv2.contourArea(contour) > 800) and (cv2.contourArea(contour) < 4500):  # **필요한 면적을 찾아 중심점 표시
                    ball_area = cv2.contourArea(contour)
                    mom = contour
                    M = cv2.moments(mom)
                    cx_origin = int(M['m10'] / M['m00'])
                    cy_origin = int(M['m01'] / M['m00'])
                    cv2.circle(frame, (cx_origin, cy_origin), 10, (0, 255, 0), -1)          # 중심 좌표 표시
                    Rivet_center.append([cx_origin, cy_origin])                             # 중심좌표 list에 추가


        ##### 자동 좌표값 저장하기 #####
        print(Rivet_center)  # 자동 저장된 중심점값 출력
        Rivet_num = len(Rivet_center)  # 자동 저장된 리벳의 갯수값 저장.

        for i in range(Rivet_num):
            Rivet_tuple.append(tuple(Rivet_center[i]))  # 자동 저장된 리벳 좌표값을 튜플로 변환후 리스트에 저장. -> (Circle 마크에 쓰기 위해)


        cv2.imshow('capture_img.jpg', frame)    # 이미지 확인용.
        cv2.imwrite('capture_img.jpg', frame)   # 처음 이미지 캡쳐후 저장.
        ##############################

        Start_Rivet_flag = 1

    #############################################################################

    reverse = cv2.bitwise_not(final_mask)
    reverse_copy = reverse.copy()

    # ** 리벳을 검출할 위치에 원으로 좌표 표시.
    for i in range(Rivet_num):
        reverse_copy = cv2.circle(reverse_copy, Rivet_tuple[i], 10, (0, 0, 0), -1)      # 가운데 점 픽셀값 확인용 (x,y)값으로 받음.
        frame = cv2.circle(frame, Rivet_tuple[i], 10, (0, 255, 255), -1)                # 원본에도 색상이 있는 점 표시.

    # ** 한 픽셀당 Binary 값을 표시.
    # [y , x]의 픽셀값 입력받음.
    pixel_val_list = []

    # 리벳이 탐지유무에 따른 화면 출력.
    if Rivet_num != 0:
        for i in range(Rivet_num):
            pixel_val = reverse[Rivet_center[i][1], Rivet_center[i][0]]  # 픽셀값 저장 (0, 255)
            if pixel_val == 255:                                         # 검출된곳은 1, 검출되지 않을곳은 0으로 변환.
                pixel_val = 0
            else:
                pixel_val = 1

            pixel_val_list.append(pixel_val)  # 변환된 값을 리스트에 추가
            pixel_sum = sum(pixel_val_list)  # 모든 픽셀의 합

        #print(pixel_val_list, pixel_sum)    # 픽셀값과 합계 출력

        if pixel_sum == Rivet_num:
            # 리벳의 갯수와 픽셀의 값이 일치하면 합격
            judge = "OK"
        else:
            # 그 외 불합격
            cv2.putText(frame, '**NG**', (50, 300), font, fontScale, (0, 0, 255), 2, cv2.LINE_AA)
            judge = "NG"
    else:
        cv2.putText(frame, "No data", (50, 300), font, 2, (255, 0, 0), 2, cv2.LINE_AA)


    cv2.imshow('Frame', frame)                      # 원본
    cv2.imshow('result', final_mask)                # 필터링후
    cv2.imshow('reverse', reverse)                  # 반전 (픽셀값을 찍어보기 위해 흑백)
    cv2.imshow('location_check', reverse_copy)      # 리벳위치 픽셀체크 위치 확인용

    # 현재 날짜, 시간 데이터
    # s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    now = time.localtime()
    s = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

    # stopper로 부터 아스키코드 'a' 가 들어오면 화면 캡쳐 - 데이터 저장. 로그기록.
    if cv2.waitKey(1) & 0xff == ord('a'):

        accum = accum + 1       # 누적 판독수 축적.
        cnt = cnt + 1

        if judge != 0:
            if judge == "OK":
                cv2.imwrite("C:/Data_Record/PASS/serialnum_" + s + "_" + str(cnt) + "_" + judge + ".jpg", frame)
            else:
                cv2.imwrite("C:/Data_Record/NG/serialnum_" + s + "_" + str(cnt) + "_" + judge + ".jpg", frame)
        else:
            print("No data")

        if judge == "OK":       # 판독 PASS 축적.
            OK = OK + 1
        elif judge == "NG":     # 판독 NG 축적.
            NG = NG + 1
        else:
            pass

        leave_log(OK, NG)       # 판독값을 로그로 남김.

    # 종료키
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
