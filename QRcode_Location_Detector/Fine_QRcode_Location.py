# import the necessary packages
# -*- coding: utf-8 -*-
import numpy as np                          #pip install numpy
import imutils                              #pip install imutils
import cv2                                  #pip install python-opencv
from  more_itertools import unique_everseen #pip install more_itertools
import math
from math import *
import datetime
import time
import os


blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0 ,255)

color = green
check_image_center = True
count_pass = 0
count_fail = 0
accumulation = 0

qr_x1 = 141
qr_y1 = 236
qr_x2 = 254
qr_y2 = 348

check_year = 0
check_month = 0
check_day = 0

def nothing(x):
    pass

def leave_log():
    global check_year, check_month, check_day, f
    time = datetime.datetime.now()
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    minute = time.minute
    sec = time.second

    '''
    print("현재 시간 : ", time)
    print(time.year, time.month, time.day, time.hour)
    print("누적 판독 바코드 : %d" % accumulation)
    print("정상 바코드 : %d" % count_pass)
    print("불량 바코드 : %d" % count_fail)
    '''

    filename = str(year)+str(month)+str(day)
    if year != check_year and month != check_month and day != check_day:
        print("새로운 로그 파일 생성")
        f = open("log\\%s.txt"%filename, 'w')
        check_year = time.year
        check_month = time.month
        check_day = time.day
        data = "현재 시간  //  누적 판독 바코드  //  정상 바코드  //  불량 바코드\n"
        f.write(data)

    time = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(sec)
    data = str(time) + " // " + str(accumulation) + " // " + str(count_pass) + " // " + str(count_fail) + "\n"
    print(data)
    f.write(data)

def get_today():
    now = time.localtime()
    s = "%04d-%02d-%02d"%(now.tm_year,now.tm_mon,now.tm_mday)
    return s

def make_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    
cv2.namedWindow("Trackbars", cv2.WINDOW_NORMAL)

# FIND_BLACK_PUCK
cv2.createTrackbar("graybar", "Trackbars", 105, 255, nothing)
cv2.createTrackbar("bluebar", "Trackbars", 164,  255, nothing)
cv2.createTrackbar("greenbar", "Trackbars", 138, 255, nothing)
cv2.createTrackbar("redbar", "Trackbars", 87,  255, nothing)
cv2.createTrackbar("hsv hbar", "Trackbars", 225, 255, nothing)
cv2.createTrackbar("hsv sbar", "Trackbars", 187, 255, nothing)
cv2.createTrackbar("hsv vbar", "Trackbars", 156, 255, nothing)
cv2.createTrackbar("hsl hbar", "Trackbars", 209, 255, nothing)
cv2.createTrackbar("hsl sbar", "Trackbars", 255, 255, nothing) 
cv2.createTrackbar("hsl lbar", "Trackbars", 188, 255, nothing)

#cv2.createTrackbar("graybar_", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("bluebar_", "Trackbars", 0,  255, nothing)
cv2.createTrackbar("greenbar_", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("redbar_", "Trackbars", 0,  255, nothing)
cv2.createTrackbar("hsv hbar_", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("hsv sbar_", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("hsv vbar_", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("hsl hbar_", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("hsl sbar_", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("hsl lbar_", "Trackbars", 0, 255, nothing)

cv2.createTrackbar("k1", "Trackbars", 33, 50, nothing)
cv2.createTrackbar("k2", "Trackbars", 26, 50, nothing)
cv2.createTrackbar("itera", "Trackbars", 10, 10, nothing)
cv2.createTrackbar("th", "Trackbars", 134, 255, nothing)
cv2.createTrackbar("rank", "Trackbars", 0, 10, nothing)

cap = cv2.VideoCapture(1)
while True:
    
    '''
    _, frame = cap.read()
    # col,row,_ = frame.shape 
    # print(col,row)
    frame2 = frame.copy() 
    '''
    #frame = cv2.imread("image\\qr123.png")
    
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.flip(frame, 0)
    frame2 = frame.copy()
    frame3 = frame.copy()
    
    '''
    if check_image_center:
        col, row, _ = frame.shape
        const_refx = int(row/2)
        const_refy = int(col/2)
        #print(const_refx, const_refy)
    check_image_center = False
    '''

    #바코드 입력 위치
    cv2.rectangle(frame3, (qr_x1, qr_y1), (qr_x2, qr_y2), (255, 0 , 0), 3)
##    dx_ref = abs(qr_x1-qr_x2)
##    dy_ref = abs(qr_y1-qr_y2)
    cx_ref = int(abs(qr_x1+qr_x2)/2)
    cy_ref = int(abs(qr_y1+qr_y2)/2)
    cv2.circle(frame3, (cx_ref, cy_ref), 3, (255,0,0), -1)

    # blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    # frame = cv2.blur(frame,(3,3))
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(gray_frame, 45, 255, cv2.THRESH_BINARY_INV)

    blue, green, red = cv2.split(frame)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(frame_hsv)
    frame_hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    H, L, S = cv2.split(frame_hls)

    gray_c  = cv2.getTrackbarPos("graybar", "Trackbars")
    blue_c  = cv2.getTrackbarPos("bluebar",  "Trackbars")
    green_c = cv2.getTrackbarPos("greenbar", "Trackbars")
    red_c   = cv2.getTrackbarPos("redbar",   "Trackbars")
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
    th = cv2.getTrackbarPos("th", "Trackbars")
    rank = cv2.getTrackbarPos("rank", "Trackbars")
 
    _, gray1 = cv2.threshold(gray_frame,gray_c,255,cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, blue_c, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, green_c, 255, cv2.THRESH_BINARY_INV)
    _, red1   = cv2.threshold(red, red_c, 255, cv2.THRESH_BINARY_INV)
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
    #final_mask = cv2.bitwise_and(final_mask, h_)
    #final_mask = cv2.bitwise_and(final_mask, s_)
    final_mask = cv2.bitwise_and(final_mask, v_)
    #final_mask = cv2.bitwise_and(final_mask, H_)
    #final_mask = cv2.bitwise_and(final_mask, L_)
    #final_mask = cv2.bitwise_and(final_mask, S_)
    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)
    #cv2.imshow('result', final_mask)

    # blur and threshold the image
    blurred = cv2.blur(final_mask, (4, 4))
    #cv2.imshow("blurred", blurred)
    (_, thresh) = cv2.threshold(blurred, th, 255, cv2.THRESH_BINARY)
    #cv2.imshow("thresh", thresh)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k1, k2))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    closed = cv2.erode(closed, None, iterations = itera)
    closed = cv2.dilate(closed, None, iterations = itera)

    #cv2.imshow("closed", closed)

    cnts= cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if(len(cnts) != 0) :
        c = sorted(cnts, key = cv2.contourArea, reverse = True)[rank]
        M = cv2.moments(c)
        rect = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
        box = np.int0(box)

        cv2.drawContours(frame2, [box], -1, color, 2)
        cv2.drawContours(frame3, [box], -1, color, 2)

        box_x = []
        box_y = []
        for i in range(len(box)):
            box_x.append(box[i][0])
            box_y.append(box[i][1])

        box_x = list(unique_everseen(box_x))
        box_y = list(unique_everseen(box_y))
        
        if(len(box_x) == 4):
            dx = int(abs(box_x[0] - box_x[2]))
            dy = int(abs(box_y[0] - box_y[2]))
            cx = int(abs(box_x[0] + box_x[2])/2)
            cy = int(abs(box_y[0] + box_y[2])/2)
            Area = dx * dy
        elif (len(box_x) == 2):
            dx = int(abs(box_x[0] - box_x[1]))
            dy = int(abs(box_y[0] - box_y[1]))
            cx = int(abs(box_x[0] + box_x[1])/2)
            cy = int(abs(box_y[0] + box_y[1])/2)
            Area = dx * dy

        cv2.circle(frame3, (cx, cy), 3, (0,255,0), -1)    
        print(cx, cy)
        print(Area)
        print(box)
        
        cv2.putText(frame2, "%d" % cx, (400, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 1)
        cv2.putText(frame2, "%d" % cy, (400, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 1)
        #cv2.putText(frame2, "%d" % Area, (400, 300), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 1)

        
        box_x0 = box_x[0]<box_x[1] and box_x[0] or box_x[1]
        box_y1 = box_y[0]>box_y[1] and box_y[0] or box_y[1]
        box_y0 = box_y[0]<box_y[1] and box_y[0] or box_y[1]

        dx = cx - box_x0
        dy = cy - box_y0
        
        PI = 3.141592
        degree = int(atan2(dx, dy)*180/PI)
        print(degree)
        cv2.putText(frame3, "%d"%degree, (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
        
        #print(box_x[0], box_x[1])
        #print(box_y[0], box_y[1])
        #print(box_y0, box_y1)

        #print(cx, cx_ref)
        
        '''
        print(abs(int(box_x[0]) - int(qr_x1)), abs(int(box_x[1]) - int(qr_x2)), abs(int(box_x[1]) - int(qr_x1)))
        print(int(box_x[0]), int(qr_x1))
        print(int(box_x[1]), int(qr_x2))
        print(box_x0)
        
        qr_x1 = 141
        qr_y1 = 236
        qr_x2 = 254
        qr_y2 = 348
        '''
        
        fn = datetime.datetime.now()
        folder_name = str(fn.year) + "-" + str(fn.month) + "-" + str(fn.day)
        #print(box_x0, qr_x1)
        if abs(cx- cx_ref) <= 1 and (10000 <= Area and Area <= 18000) :
        #if abs(int(box_x0) - int(qr_x1)) <= 2 and 10000<=Area and Area <= 18000:
            print("=====  판독 중  =====")
            today = get_today()
            foldername_today = ".\\" + today
            make_folder(foldername_today)
            foldername_pass = ".\\" + today + "\\pass"
            make_folder(foldername_pass)
            foldername_fail = ".\\" + today + "\\fail"
            make_folder(foldername_fail)

            #print(abs(cx- cx_ref), abs(box_y[0]-qr_y2), abs(box_y[1] - qr_y1))
            #if abs(cx- cx_ref) <= 5 and abs(box_y0-qr_y1) <= 7 and abs(box_y1 - qr_y2) <= 7 :
            if (40 < degree and degree < 50) and abs(int(box_x0) - int(qr_x1)) <= 7 \
               and abs(box_y0 - qr_y1) <= 7 and abs(box_y1 - qr_y2) <= 7 :
                cv2.putText(frame3, "PASS", (cx-100, cy-50), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
                cv2.imwrite(".\\%s\\pass\\qr%d.jpg" % (folder_name, count_pass), frame3)
                #cv2.imwrite(".\\%s\\pass\\qr%d.jpg" % count_pass, frame3)
                count_pass += 1
                print("정상 위치")
            else:
                cv2.putText(frame3, "NG", (cx-100, cy-50), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
                cv2.imwrite(".\\%s\\fail\\qr%d.jpg" % (folder_name, count_fail), frame3)
                #cv2.imwrite(".\\save_image\\fail\\qr%d.jpg" % count_fail, frame3)
                count_fail += 1
                print("불량")
            accumulation = count_pass + count_fail;    
            leave_log()
        else:
            print("판독 위치가 아닙니다.")

        
    #print(box)

    #cv2.imshow('Frame', frame)
    cv2.imshow('Frame2', frame2)
    cv2.imshow('Frame3', frame3)

    if cv2.waitKey(10) & 0xff == ord('q'):
        f.close()
        break

cap.release()
cv2.destroyAllWindows()


