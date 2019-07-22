# -*- coding: utf-8 -*-
import numpy as np  # pip install numpy==1.15.4
import cv2  # pip install opencv-python==3.4.4.19
from PIL import Image as Img  # pip install image==1.5.27
import pyzbar.pyzbar as pyzbar  # pip install pyzbar==0.1.7
from more_itertools import unique_everseen  # pip install more_itertools==4.3.0
import serial  # pip install pyserial==3.4
from PIL import ImageTk
from math import *
import datetime
import time
import os
from tkinter import filedialog
from tkinter import *
import socket
import copy
import sys
import math
import pickle
import glob
import imutils
import threading

# 데이터를 저장할 위치(서버저장)
store_local_location = "D:/Air3239/"
store_server_location = "//192.168.105.4/Multimedia/Air3239/"
Serial_No = ''
pre_Serial_No = '1'
protocol = 0
port_num = ''
PLC_ready = ''
judgeFlag = 0
tactFlag = 0
sum_tact_time = 0
sum_tact_time_list = []

check_barcode_area = 0
check_year = 0
check_month = 0
check_day = 0
check_make_folder = 0
check_result = 0
pre_day = 0

# 카메라 연결
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4024)  # Width 4024
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3036)  # Height 3036
print("카메라 현재 해상도 %d x %d" %(cap.get(3), cap.get(4)))

# PLC와 RS232통신 연결
try:
    ser = serial.Serial(
        port='COM3',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5  # PLC would sent to
    )
    print("Suceessfully connected with PLC")
except:
    print("[ERROR] : please check PLC RS232")

# 조명 모듈과 RS232통신 연결
try:
    ser1 = serial.Serial(
        port='COM7',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
    )
    print("Suceessfully connected with Light module")
except:
    print("[ERROR] : please check Light module RS232")

global_cnt = 0
def timerCounter(judge, Serial_No):
    global global_cnt, storeTacttime
    global_cnt += 1
    print("Timer counter:", global_cnt)
    print("inside timer SN:", Serial_No)

    # 날짜, 시간 취득
    local_time = get_today()
    yy,mm,dd,h,m,s = check_time_value()

    threading.Timer(1000, timerCounter).start()  # 1000 타이머 카운트 스레드 작동
    if global_cnt > 1 and Serial_No != '':
        sendSignal(judge)
        light_off()
        result_display(0, data=Serial_No)    # GUI에 시리얼번호 출력
        result_display(2, data="{} // {}:{}:{}".format(local_time, h, m, s))
        result_display(3, data=storeTacttime)
        global_cnt = 0
        # 결과 저장 알림 라벨
        text_label = Label(root, text="image file saved\n log file saved", width=int(screen_width * (14 / tk_width)), height=int(screen_height * (2 / tk_height)), font="Helvetica 20 bold", fg="RoyalBlue")
        text_label.place(x=screen_width * (1640 / tk_width), y=screen_height * (660 / tk_height))
        # OK, NG 알림 라벨 출력
        if judge == 1:
            result_label = Label(root, text="OK", font="Helvetica 140 bold", fg="RoyalBlue")
            result_label.place(x=screen_width * (1550 / tk_width), y=screen_height * (760 / tk_height))
        elif judge == 2:
            result_label = Label(root, text="NG", font="Helvetica 140 bold", fg="red")
            result_label.place(x=screen_width * (1550 / tk_width), y=screen_height * (760 / tk_height))
    elif global_cnt > 5:
        sendSignal(2)
        light_off()
        result_display(1)
        result_display(2, data="{} // {}:{}:{}".format(local_time, h, m, s))
        result_display(3, data=storeTacttime)
        global_cnt = 0
        # 결과 저장 알림 라벨
        text_label = Label(root, text="image file saved\n log file saved", width=int(screen_width * (14 / tk_width)), height=int(screen_height * (2 / tk_height)), font="Helvetica 20 bold", fg="RoyalBlue")
        text_label.place(x=screen_width * (1640 / tk_width), y=screen_height * (660 / tk_height))
        # Tact Time over 알림 라벨 출력
        result_label = Label(root, text="Over\nTact Time", font="Helvetica 65 bold", fg="red")
        result_label.place(x=screen_width * (1450 / tk_width), y=screen_height * (760 / tk_height))

        print("Serial Number Timout Error")


# 작동시간을 리턴
def logging_time(original_fn):
    global tact_time
    def wrapper_fn(*args, **kwargs):
        global tact_time
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        tact_time = end_time - start_time
        # print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time - start_time))
        return result

    return wrapper_fn


class calulateCoordinate:

    def __init__(self):
        pass

    # (x1, y1) (x2, y2)값을 입력하면 점과 점사이 거리를 반환
    def distance(self, x1, y1, x2, y2):

        distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)   # 두 점 사이의 거리값
        return distance

    # (x1, y1) (x2, y2)값을 입력하면 중간지점의 점(x, y) 을 반환
    def midpoint(self, x1, y1, x2, y2):

        x = int((x1 + x2) / 2)
        y = int((y1 + y2) / 2)
        return x, y

    # 직각삼각형의 밑변과 높이를 입력하면 각도를 반환.
    def angle(self, baseline, height):
        theta = math.atan((abs(height)/abs(baseline)))
        degree = round(theta*(180/math.pi), 4)           # 4째자리에서 반올림, theta x 라디안
        return degree


'''
    이미지 채도 향상.

    :param
        컬러이미지 , 0~255
    :return
        채도향상된이미지
'''
def increase_brightness(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return img


'''
    mask 바이너리 이미지의 폐쇄된 빈 공간을 채워줌.

    :param
        Binary 이미지
    :return
        Binary 이미지 (Closed 된 빈공간을 매꿈)
'''
def fullfill_inside(im_in):
    im_in = cv2.bitwise_not(im_in)

    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255.
    th, im_th = cv2.threshold(im_in, 220, 255, cv2.THRESH_BINARY_INV);
    # cv2.imshow('im_th', im_th)

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


'''
    체스 보정값으로 렌즈 왜곡을 보정하여 리턴.

    :param
        (raw) 원본이미지
    :return
        체스보정값으로 보정한 왜곡보정된 이미지
'''
def calibration(img):
    global objpoints, imgpoints

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]

    # undistort
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]

    return dst


'''
    원본 이미지 필터링
'''
def choke_img_filtering(img):

    img = increase_brightness(img, 255)         # 채도를 최대로 조정.
    img = cv2.GaussianBlur(img, (7, 7), 0)      # Blur 필터링

    frame2 = img.copy()  # 영상원본

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(img)  # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

    frame_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)  # H,L,S 분리
    kernel = np.ones((3, 3), np.uint8)

    _, gray1 = cv2.threshold(gray_frame, 250, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 230, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 255, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 255, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 36, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 106, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 255, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 138, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)

    _, blue_ = cv2.threshold(blue, 58, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 156, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 164, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 130, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 190, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 192, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, 141, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, 117, 255, cv2.THRESH_BINARY)
    _, S_ = cv2.threshold(S, 141, 255, cv2.THRESH_BINARY)

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

    final_mask = cv2.bitwise_and(final_mask, blue_)
    final_mask = cv2.bitwise_and(final_mask, green_)
    final_mask = cv2.bitwise_and(final_mask, red_)
    final_mask = cv2.bitwise_and(final_mask, v_)

    final_mask = cv2.dilate(final_mask, kernel, iterations=3)  # 정리된 사각형을 다시 확대

    return final_mask


'''
    Canny Edge로 탐색하여 가장 큰 edge의 사각형 외곽선을 탐지
    꼭지점 4개의 좌표와 이미지를 리턴.

    param 
        1280 x 960 resized 된 이미지 input.
    return
        왼쪽상단 좌표, 오른쪽하단 좌표
'''


def find_outline(img):
    global ttt_count, diff
    global pre_x1, pre_y1, find_cnt

    img1 = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # close gaps in between object edges
    edged = cv2.Canny(gray, 30, 20)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    # # 탐지된 Edge 확인용. (디버깅)
    # cv2.imshow("edged", cv2.resize(edged, (1280, 960)))
    # cv2.waitKey(0)

    # find contours in the edge map
    try:
        img, contours, hierachy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    except:
        contours, hierachy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_area_list = []
    for i in range(len(contours)):
        mom = contours[i]
        M = cv2.moments(mom)
        area = cv2.contourArea(mom)
        contours_area_list.append(area)

    MAX = 0
    idx = 0
    for i in range(len(contours_area_list)):
        MAX = (MAX > contours_area_list[i]) and MAX or contours_area_list[i]

    idx = contours_area_list.index(MAX)
    cnt = contours[idx]

    box = cv2.minAreaRect(cnt)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")

    cv2.drawContours(img1, [box.astype("int")], -1, (0, 255, 0), 1)

    # 원본 해상도 / Resized 해상도
    ratio_x = 4024 / 1280
    ratio_y = 3036 / 960

    cnt = 1
    coordListx = []
    coordListy = []
    for (xA, yA) in list(box):
        globals()['x{}'.format(cnt)], globals()['y{}'.format(cnt)] = math.ceil(int(xA) * ratio_x), math.ceil(
            int(yA) * ratio_y)
        # globals()['x{}'.format(cnt)], globals()['y{}'.format(cnt)] = math.ceil(int(xA)), math.ceil(int(yA))
        # draw circles corresponding to the current points and
        cv2.circle(img1, (int(xA), int(yA)), 3, (0, 0, 255), -1)
        cv2.putText(img1, "({},{})".format(xA, yA), (int(xA - 80), int(yA + 10)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 255, 0), 1)
        coordListx.append(int(xA))
        coordListy.append(int(yA))
        cnt += 1

    list_point = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    # print("1. list_point", list_point)
    list_point.sort()
    # print("2. list_point", list_point)
    diff = 10 * ratio_x

    for i in range(4):
        cv2.circle(img1, (list_point[i][0], list_point[i][1]), 3, (0, 0, 255), -1)

    return min(coordListx), min(coordListy), max(coordListx), max(coordListy)


'''
    원본이미지, x1, y1 좌표, x2, y2 좌표
    그 부분만 사각형으로 마스크를 씌워 
    Masked된 Binary 이미지를 리턴.
'''
def edge_mask(img, x1, y1, x2, y2):

    # 좌표값 만큼 마스크
    masked = np.zeros(img.shape[:2], np.uint8)
    masked = cv2.rectangle(masked, (x1, y1), (x2, y2), (255, 255, 255), -1)
    return masked


'''
    함수) 마스크를 이용해 초크부위만 남길 수 있도록 함. (1차가공)

        param
            masked_img : Threshold 영상 (이진화 영상)
            img        : 원본영상, display용

        return
            center_pt :  좌표 List
'''
def find_area(masked_img, img):

    imgcp = img.copy()

    centerPoint = []
    try:
        _, contours, _ = cv2.findContours(masked_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    except:
        contours, _ = cv2.findContours(masked_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기

    # 마스크할 창 생성.
    chokemask = np.zeros(img.shape[:2], np.uint8)

    if len(contours) != 0:
        for contour in contours:
            if (cv2.contourArea(contour) > 1000) and (cv2.contourArea(contour) < 1000000):  # **필요한 면적을 찾아 중심점 좌표를 저장 (영역 제한)

                # 사각박스 영역 지정
                x, y, w, h = cv2.boundingRect(contour)
                #cv2.rectangle(img,(x, y), (x+w, y+h), (0, 0, 255), 2)

                cv2.rectangle(chokemask, (x, y), (x+w, y+h), (255, 255, 255), -1)

                # area = cv2.contourArea(contour)       # 면적값 출력
                # print(area)
                mom = contour
                M = cv2.moments(mom)
                cx_origin = int(M['m10'] / M['m00'])
                cy_origin = int(M['m01'] / M['m00'])
                #cv2.drawContours(img, contour, -1, (0, 255, 0), 1)
                #cv2.circle(img, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시
                centerPoint.append([cx_origin, cy_origin])

        onlyChoke = cv2.bitwise_and(imgcp, imgcp, mask=chokemask)  # 합성하여 뽑아냄.

        finalchokemask = onlychokeFiltering(onlyChoke)
        detect_LineDegree(img , finalchokemask)

        return centerPoint


'''
    Choke만 남아있는 마스킹된 이미지를 필터링하여 순수 choke부만 남기고 필터링 (2차 가공)
'''
def onlychokeFiltering(onlychoke):

    onlychoke = cv2.GaussianBlur(onlychoke, (7, 7), 0)
    frame2 = onlychoke.copy()
    grayChoke = cv2.cvtColor(onlychoke, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(onlychoke)  # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(onlychoke, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

    frame_hls = cv2.cvtColor(onlychoke, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)  # H,L,S 분리
    kernel = np.ones((3, 3), np.uint8)

    _, gray1 = cv2.threshold(grayChoke, 255, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 255, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 255, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 255, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 120, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 255, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 255, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 86, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)

    _, blue_ = cv2.threshold(blue, 0, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 91, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 15, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 94, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 78, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, 124, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, 117, 255, cv2.THRESH_BINARY)
    _, S_ = cv2.threshold(S, 128, 255, cv2.THRESH_BINARY)

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

    final_mask = cv2.bitwise_and(final_mask, blue_)
    final_mask = cv2.bitwise_and(final_mask, green_)
    final_mask = cv2.bitwise_and(final_mask, red_)
    final_mask = cv2.bitwise_and(final_mask, v_)

    final_mask = cv2.dilate(final_mask, kernel, iterations=3)
    final_mask = fullfill_inside(final_mask)                    # 초크부위만 딱 추출
    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    #cv2.imshow('TTest', result)

    # 초크부위 마스크를 씌울 검정색 빈상자 생성.
    chokerecMask = np.zeros(onlychoke.shape[:2], np.uint8)

    try:
        _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    except:
        contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    if len(contours) != 0:
        for contour in contours:
            if (cv2.contourArea(contour) > 2000) and (cv2.contourArea(contour) < 10000000):  # **필요한 면적을 찾아 중심점 좌표를 저장

                # 근사 사각형으로 치환
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame2, [box], 0, (255, 255, 0), 2)
                cv2.drawContours(chokerecMask, [box], 0, (255, 255, 255), -1)

                ball_area = cv2.contourArea(contour)
                mom = contour
                M = cv2.moments(mom)
                cx_origin = int(M['m10'] / M['m00'])
                cy_origin = int(M['m01'] / M['m00'])
                cv2.drawContours(frame2, contour, -1, (0, 255, 0), 1)
                cv2.circle(frame2, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시

    return chokerecMask


'''
    최종 평균 라인을 검출하여 디스플레이 함.
'''
def display_final(finalimg, x1,y1, x2,y2, final_function):
    global cp_final
    cv2.line(finalimg, (x1, y1), (x2, y2), (0, 255, 255), 2)
    cv2.putText(finalimg, final_function, (x1+500, y1-30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 0), 2)
    # cv2.imshow("FFianl", finalimg)
    cp_final = finalimg.copy()
    return finalimg


# 원본, choke마스크이미지(이진화)
def detect_LineDegree(img, final_mask):
    flag = 0
    save_function_list = []
    final_end_ptList = []

    cp_img = img.copy()
    showimg = img.copy()
    try:
        _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    except:
        contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    if len(contours) != 0:
        aList = []
        bList = []
        cnt = 1
        count = 0
        for contour in contours:
            if (cv2.contourArea(contour) > 500) and (cv2.contourArea(contour) < 10000000):  # **필요한 면적을 찾아 중심점 좌표를 저장

                ball_area = cv2.contourArea(contour)
                mom = contour
                M = cv2.moments(mom)
                cx_origin = int(M['m10'] / M['m00'])
                cy_origin = int(M['m01'] / M['m00'])
                #cv2.drawContours(frame2, contour, -1, (0, 255, 0), 1)
                cv2.circle(img, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시

                # then apply fitline() function
                [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
                # Now find two extreme points on the line to draw line
                lefty = int((-x * vy / vx) + y)
                righty = int(((cp_img.shape[1] - x) * vy / vx) + y)
                cv2.line(img, (0, lefty),(cp_img.shape[1] - 1, righty), 255, 2)     # 기본 직선의 좌표

                # 1차 함수표현 y = ax * b
                a = (righty - lefty) / (cp_img.shape[1] - 1)
                b = lefty
                cv2.putText(img, "y = ({})x + {}".format(a, b), (cx_origin-200, cy_origin-30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)    # 좌표의 1차 함수방정식

                try:
                    if abs(bf_cy - cy_origin) > 100 :     # y좌표가 급격히 바뀔때 하나의 함수로
                        # print(aList, bList)
                        flag = 1
                        aList.clear()
                        bList.clear()
                        cnt = 1
                except:
                    pass
                bf_cy = cy_origin
                aList.append(a)
                bList.append(b)
                asum = sum(aList)
                bsum = sum(bList)

                cv2.putText(img, "y = ({})x + {}".format((asum/cnt), (bsum/cnt)), (cx_origin-200, cy_origin-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)   # 평균을 구한 일차함수

                save_function_list.append("y = ({})x + {}".format((asum / cnt), (bsum / cnt)))
                final_end_ptList.append([(0, int(bsum / (cnt))), ( int(cp_img.shape[1] - 1), int(((asum / (cnt)) * cp_img.shape[1] - 1) + (bsum / (cnt))))])

                # 평균을 낸 값.  (오른쪽, 왼쪽)
                cv2.line(img, (0, int(bsum / (cnt))), ( int(cp_img.shape[1] - 1), int(((asum / (cnt)) * cp_img.shape[1] - 1) + (bsum / (cnt)))) , (0, 255, 255), 1)

                if flag == 1:
                    display_final(showimg, final_end_ptList[count-1][0][0], final_end_ptList[count-1][0][1], final_end_ptList[count-1][1][0], final_end_ptList[count-1][1][1], save_function_list[count-1])
                    flag = 0

                cnt = cnt + 1
                count = count + 1

        display_final(showimg, final_end_ptList[count - 1][0][0], final_end_ptList[count - 1][0][1], final_end_ptList[count - 1][1][0], final_end_ptList[count - 1][1][1], save_function_list[count - 1])


def MaskFromCircle_bin(img):

    img = increase_brightness(img, 100)
    img = cv2.GaussianBlur(img, (3, 3), 0)

    dipoleMask = np.zeros(img.shape[:2], np.uint8)
    dipoleMask = np.bitwise_not(dipoleMask)

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((3, 3), np.uint8)
    th2 = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)  # 11 2
    th2 = cv2.erode(th2, kernel, iterations=1)
    circles = cv2.HoughCircles(th2, cv2.HOUGH_GRADIENT, 1, 13, param1=110, param2=9, minRadius=9, maxRadius=11)

    # 외곽선 탐지하여 꼭지점 2개좌표 리턴.
    leftup, leftdn, rightup, rightdn = find_outline(img)
    # 이미지의 중심선 찾음.
    midline = int((rightup - leftdn) / 2) + leftup
    # 중심선으로부터 Offset한 거리.
    gap = 60
    img = cv2.line(img, (midline, leftup), (midline, rightdn), (0, 0, 255), 2, cv2.LINE_4)
    img = cv2.line(img, (midline - gap, leftup), (midline - gap, rightdn), (0, 255, 0), 2)
    img = cv2.line(img, (midline + gap, leftup), (midline + gap, rightdn), (0, 255, 0), 2)

    # 범위내 원 검출
    circlelist = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            if circle[0] > midline - gap and circle[0] < midline + gap:
                # print((circle[0], circle[1]))
                circlelist.append((circle[0], circle[1], circle[2]))
    for i in range(len(circlelist)):
        cv2.circle(img, (circlelist[i][0], circlelist[i][1]), circlelist[i][2], (255, 0, 255), 2)

    # 마스크 씌우기
    dipoleMask = cv2.rectangle(dipoleMask, (0, circlelist[0][1]-128),(img.shape[1], circlelist[0][1]-25), (0, 0, 0), -1)
    dipoleMask = cv2.rectangle(dipoleMask, (0, circlelist[0][1]+20),(img.shape[1], circlelist[0][1]+125), (0, 0, 0), -1)
    dipoleMask = cv2.rectangle(dipoleMask, (0, circlelist[1][1]-128),(img.shape[1], circlelist[1][1]-22), (0, 0, 0), -1)
    dipoleMask = cv2.rectangle(dipoleMask, (0, circlelist[1][1]+20),(img.shape[1], circlelist[1][1]+125), (0, 0, 0), -1)
    return dipoleMask


def img_filtering(img):

    img = increase_brightness(img, 255)         # 채도를 최대로 조정.
    img = cv2.GaussianBlur(img, (5, 5), 0)      # Blur 필터링

    frame2 = img.copy()  # 영상원본

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(img)  # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

    frame_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)  # H,L,S 분리
    kernel = np.ones((3, 3), np.uint8)

    _, gray1 = cv2.threshold(gray_frame, 255, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 255, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 255, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 255, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 39, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 120, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 255, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 255, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)

    _, blue_ = cv2.threshold(blue, 40, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 29, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 20, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 125, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 119, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 37, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, 138, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, 113, 255, cv2.THRESH_BINARY)
    _, S_ = cv2.threshold(S, 123, 255, cv2.THRESH_BINARY)

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

    final_mask = cv2.bitwise_and(final_mask, blue_)
    final_mask = cv2.bitwise_and(final_mask, green_)
    final_mask = cv2.bitwise_and(final_mask, red_)
    final_mask = cv2.bitwise_and(final_mask, v_)

    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    #cv2.imshow('c', img)
    # cv2.imshow('final_mask',final_mask)

    return final_mask

resolution = (1280, 960)
def judgeImage(img):
    global resolution
    NGcnt = 0
    OKcnt = 0

    img = calibration(img)  # 보정된 이미지 리턴 (속도가 느려짐)
    cal_img = img.copy()
    img = cv2.resize(img, resolution)

    final_mask = img_filtering(img)     # 이미지를 가공하여 사각형만 남긴 Threshold를 내보냄.
    #cv2.imshow('b',final_mask)

    pt_list = []
    right_mid_list = []
    left_mid_list = []
    minx_contour = []
    miny_contour = []
    square_center = []
    try:
        _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    except:
        contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    if len(contours) != 0:
        for contour in contours:
            if (cv2.contourArea(contour) > 8000) and (cv2.contourArea(contour) < 9800):  # **필요한 면적을 찾아 중심점 좌표를 저장
                ball_area = cv2.contourArea(contour)
                # print("area: ", ball_area)
                mom = contour
                M = cv2.moments(mom)
                cx_origin = int(M['m10'] / M['m00'])
                cy_origin = int(M['m01'] / M['m00'])

                # 외곽선 근사화 시키기 (사각형의 형상을 얻기 위해), epsilon값에 따라 근사 민감도 결정.
                epsilon = 0.12 * cv2.arcLength(mom, True)
                approx = cv2.approxPolyDP(mom, epsilon, True)

                # 근사화 시킨 놈
                cv2.drawContours(img, [approx], -1, (255, 255, 255), 3)  # 근사화 시킨 컨투어 그리기
                # cv2.drawContours(img, [mom], 0, (0, 255, 0), 5) # 실제 컨투어를 그림.
                cv2.circle(img, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시

                # 근사화 시킨 형상중 사각형만 고름.
                if len(approx) != 0:
                    if len(approx) == 4:
                        # midp = cal.midpoint(approx[0][0][0], approx[0][0][1], approx[3][0][0], approx[3][0][1])
                        for i in range(len(approx)):
                            minx_contour.append(approx[i][0][0])  # x좌표에 대한 꼭지점 좌표. 리스트에 추가
                            miny_contour.append(approx[i][0][1])  # y좌표에 대한 꼭지점 좌표. 리스트에 추가
                            cv2.circle(img, (approx[i][0][0], approx[i][0][1]), 5, (255, 255, 255),
                                       -1)  # 근사화 사각에서의 꼭지점 표시
                            # 중심점의 x좌표를 기준으로 왼쪽과 오른쪽으로 나누어 왼쪽, 오른쪽 리스트에 추가(꼭지점의 중점을 계산하기 위한 선행작업)
                            pt_list.append(tuple((minx_contour[i], miny_contour[i])))
                            if pt_list[i][0] < cx_origin:
                                left_mid_list.append(pt_list[i])
                            else:
                                right_mid_list.append(pt_list[i])

                        #print(pt_list)
                        cal = calulateCoordinate()  # 계산 클래스 객체 할당.

                        # 왼쪽 오른쪽의 중심점을 반환
                        left_midpt = cal.midpoint(left_mid_list[0][0], left_mid_list[0][1], left_mid_list[1][0],
                                                  left_mid_list[1][1])
                        right_midpt = cal.midpoint(right_mid_list[0][0], right_mid_list[0][1], right_mid_list[1][0],
                                                   right_mid_list[1][1])
                        #print("왼쪽, 오른쪽 미드 중심점값", left_midpt, right_midpt)

                        # 왼쪽 오른쪽 중심점을 찍고 선으로 이어줌.
                        cv2.circle(img, left_midpt, 5, (0, 255, 0), -1)  # 근사화 시킨 사각형의 꼭지점 출력
                        cv2.circle(img, right_midpt, 5, (0, 255, 0), -1)  # 근사화 시킨 사각형의 꼭지점 출력
                        cv2.line(img, left_midpt, right_midpt, (0, 255, 0), 3)  # 사각형의 중심점을 선분으로 이음.

                        # 중심선분의 길이값 구함. 직각삼각형을 만들어 밑변, 높이를 이용해 tan 삼각함수로 각도 계산
                        midDistance = cal.distance(left_midpt[0], left_midpt[1], right_midpt[0], right_midpt[1])
                        baseline = cal.distance(left_midpt[0], left_midpt[1], right_midpt[0], left_midpt[1])
                        height = cal.distance(right_midpt[0], right_midpt[1], right_midpt[0], left_midpt[1])
                        angle = cal.angle(baseline, height)

                        # # 모든 각도 출력
                        # cv2.putText(img, 'angle: %.2f' % (round(angle, 2)), (cx_origin - 35, cy_origin - 25),
                        #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)

                        # 각도가 2.2도 이상 틀어지면 불합격, 그 이하 합격
                        if angle > 2.2:
                            cv2.putText(img, 'angle: %.2f NG' % (round(angle, 2)), (cx_origin - 35, cy_origin - 25),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
                            NGcnt = NGcnt + 1
                        else:
                            cv2.putText(img, 'angle: %.2f' % (round(angle, 2)), (cx_origin - 35, cy_origin - 25),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
                            OKcnt = OKcnt + 1
                else:
                    print("사각형이 아닙니다.")

                square_center.append([cx_origin, cy_origin])
                # 리스트를 비워줌 반복
                minx_contour = []
                miny_contour = []
                left_mid_list = []
                right_mid_list = []
                pt_list = []

    print('OKcnt, NGcnt:', OKcnt, NGcnt)
    if OKcnt == 24:
        judge = 1
    else:
        judge = 2

    return img, cal_img, judge


def choke_judgeImage(img):
    global resolution

    # img = calibration(img)  # 보정된 이미지 리턴 (속도가 느려짐)    //    이미 보정된 이미지 이용
    img = cv2.resize(img, resolution)

    # 좌표값과 마킹된 이미지 리턴.
    x1, y1, x4, y4 = find_outline(img)
    masked_edge = edge_mask(img, x1, y1, x4, y4)

    # 제품영역 외 모든 부분 마스크
    masked_edge_img = cv2.bitwise_and(img, img, mask=masked_edge)
    # cv2.imshow('masked_edge', masked_edge_img)

    # 제품외 영역 제외 + Dipole 부분 마스크 = Choke 마스크만 남김.
    line_alive = choke_img_filtering(img)
    rec_alive = MaskFromCircle_bin(masked_edge_img)

    rec_alive_masked = cv2.bitwise_and(line_alive, line_alive, mask=rec_alive)

    kernel = np.ones((3, 3), np.uint8)
    msk_result = cv2.bitwise_and(masked_edge, masked_edge, mask=rec_alive_masked)
    msk_result = cv2.dilate(msk_result, kernel, iterations=6)  # 정리된 사각형을 다시 확대
    msk_result = cv2.erode(msk_result, kernel, iterations=6)  # 사각형만 남기도록 깍음

    find_area(msk_result, img)

    return img


def leave_log(check):
    global check_year, check_month, check_day, f
    global today, pre_day, localtime
    global check_make_folder, folder_name
    global foldername_pass, foldername_fail, foldername_log
    global open_foldername_pass, open_foldername_fail, open_foldername_log
    global count_make_folder, count_make_log

    # 서버로 저장할지, 로컬로 저장할지 check 플레그 확인
    if check == 1:
        store_location = store_local_location + '/'
    elif check == 2:
        store_location = store_server_location + '/'

    year, month, day, hour, minute, sec = check_time_value()
    fn = datetime.datetime.now()

    # 폴더명, 파일명 생성
    folder_name = str(fn.year) + "-" + str("%02d" % fn.month) + "-" + str("%02d" % fn.day)
    filename = str(year) + str("%02d" % month) + str("%02d" % day)

    # 날짜변경 처리
    if pre_day != day:
        check_make_folder = 0
        count_make_folder = 2
        count_make_log = 2

    if day != check_day or count_make_log != 0:
        print("새로운 로그 파일 생성")
        today = get_today()
        foldername_log = store_location + today + "/rivet" + "/log"
        make_folder(foldername_log)
        f = open(store_location + today + "/rivet/log/log_%s.txt" % filename, 'w', encoding='utf - 8')
        data = "시리얼 넘버  //  판독 시간  //  누적 판독량  //  정상  //  불량  \n"
        f.write(data)

        check_year = datetime.datetime.now().year
        check_month = datetime.datetime.now().month
        check_day = datetime.datetime.now().day
        pre_day = check_day

        count_make_log -= 1




    # 파일을
    f = open(store_location + today + "/rivet/log/log_%s.txt" % filename, 'a')
    localtime = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + " " + str("%02d" % hour) + ":" + str("%02d" % minute) + ":" + str("%02d" % sec)
    data = str(Serial_No) + " // " + str(localtime) + " // " + str("%04d" % accum) + " // " + str("%04d" % count_pass_rivet) + " // " + str("%04d" % count_fail_rivet) + "\n"
    f.write(data)





# 오늘 날짜 취득
def get_today():
    now = time.localtime()
    local_time = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    return local_time

# 폴더 생성
def make_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

def check_time_value():
    time = datetime.datetime.now()
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    minute = time.minute
    sec = time.second

    return year, month, day, hour, minute, sec

def open_folder_pass():
    ### 폴더 경로 변경
    if check_make_folder == 1:
        path = open_foldername_pass
        path = os.path.realpath(path)
        os.startfile(path)


def open_folder_ng():
    ### 폴더 경로 변경
    if check_make_folder == 1:
        path = open_foldername_fail
        path = os.path.realpath(path)
        os.startfile(path)


def open_folder_log():
    ### 폴더 경로 변경
    if check_make_folder == 1:
        path = open_foldername_log
        path = os.path.realpath(path)
        os.startfile(path)

# 조명 모두 켜기
def light_on():
    DATA = chr(0x02) + chr(0x43) + chr(0x48) + chr(0x41) + chr(0x53) + chr(0x32) + chr(0x30) + chr(0x30) + chr(
        0x32) + chr(0x30) + chr(0x30) + chr(0x32) + chr(0x30) + chr(0x30) + chr(0x32) + chr(0x30) + chr(0x30) + chr(
        0x03)
    if ser1.readable():
        DATA = DATA.encode()
        ser1.write(DATA)  # 시리얼 데이터 전송

# 조명 모두 끄기
def light_off():
    DATA = chr(0x02) + chr(0x43) + chr(0x48) + chr(0x41) + chr(0x53) + chr(0x30) + chr(0x30) + chr(0x30) + chr(
        0x30) + chr(0x30) + chr(0x30) + chr(0x30) + chr(0x30) + chr(0x30) + chr(0x30) + chr(0x30) + chr(0x30) + chr(
        0x03)

    if ser1.readable():
        DATA = DATA.encode()
        ser1.write(DATA)  # 시리얼 데이터 전송


'''
    함수) Resized된 ROI 구간을 원본영상에서 확대
        화면 비율 원본 - 4024 : 3036
        축소 비율      - 1260 : 960
        (계산 x축 => 1260:4024 = 1:x)
        (계산 y축 => 960:3036 = 1:y)
        화면 배율 x = 3.1936, y = 3.1625

        param
            ori_img : 원본 영상
            x1, y1  : Resized 된 영상속에서 ROI 지정. (시작지점)
            x2, y2  : Resized 된 영상속에서 ROI 지정. (끝지점)
'''
def displayRate(ori_img, x1, y1, x2, y2):
    x1 = int(x1 * 3.1936)
    x2 = int(x2 * 3.1936)
    y1 = int(y1 * 3.1625)
    y2 = int(y2 * 3.1625)

    # ROI 영역 원본영상에서 확대
    roi = ori_img[y1:y2, x1:x2]

    # 바코드가 선명해지도록 Contrast(대조) 적용
    # roi = img_Contrast(roi)

    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    return roi



def decode(im):

    im = Reformat_Image(im, 1.5, 1.5)
    #im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 45, 5)   # 51 5, 49 5, 47 5,
    # cv2.imshow("barcode_area", im)
    decodedObjects = pyzbar.decode(im)  # 바코드와 QR코드를 찾아냄

    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data, '\n')
    try:
        Serial_No = decodedObjects[0][0].decode()
        return Serial_No
    except:
        Serial_No = ''
        return Serial_No



def checkSerialNumber(img):
    global resolution
    barcode_area = [(730, 350), (800, 600)]
    raw_img = img.copy()

    img = cv2.resize(img, resolution)
    img = cv2.rectangle(img, barcode_area[0], barcode_area[1], (0, 255, 0), 2)
    roi = displayRate(raw_img, barcode_area[0][0], barcode_area[0][1], barcode_area[1][0], barcode_area[1][1])

    # FOR DEBUGGING OF BARCODE !!
    # cv2.imshow('serialcheck', img)
    return roi


readyflag = 0
count = 0
def checkStatusSignal(img):
    global readyflag, count, tact_time, tactFlag, sum_tact_time_list, sum_tact_time
    global cp_final

    count = count + 1
    if count > 5:
        readyflag = 0
        count = 0
    print("waiting read signal...")

    if tactFlag == 1:
        try:
            sum_tact_time_list.append(tact_time)
            # print("list", sum_tact_time_list)
            sum_tact_time = sum(sum_tact_time_list)
            print("sumTact", sum_tact_time)
        except:
            pass

    # PLC신호 읽음
    try:
        if ser.readable():
            res = ser.readline()
            PLC_ready = res.decode()
            PLC_ready = PLC_ready.lower()  # 소문자로 변환

            if readyflag == 0:

                readyflag = 1
                if PLC_ready[0:5] == 'ready':
                    light_on()  # Turn on the light

                    tactFlag = 1

                    # check serial Number
                    roi =checkSerialNumber(img)
                    Serial_No = decode(roi)
                    print("Serial:", Serial_No)

                    print("이곳에 판독 함수를 작성")
                    dipoleResult, cal_img, judge = judgeImage(img)     # result를 GUI로 이용. 리턴: 다이폴이미지, 왜곡보정이미지, 판독값
                    # choke_judgeImage(cal_img)
                    # cv2.imshow('chokefinal', cp_final)
                    temp = cv2.imread('temp.png')

                    print("OK 인지 NG 인지 전송")
                    # sendSignal(judge)                   # send judgement to PLC
                    # light_off()
                    timerCounter(judge, Serial_No)
                    return [dipoleResult, temp]
    except:
        print("Test모드 실행중 - 조명시리얼, PLC시리얼을 연결해세요.")

'''
    합격일때 : sendSignal(1)
    불합일때 : sendSignal(2)
    의 형태로 함수 사용.
'''
def sendSignal(signal=0):
    global tactFlag, sum_tact_time_list, sum_tact_time, storeTacttime

    signal = str(signal)
    signal = signal.encode()
    tactFlag = 0
    storeTacttime = round(sum_tact_time, 4)
    sum_tact_time = 0
    sum_tact_time_list.clear()
    ser.write(signal)  # 전송

# 결과를 GUI 라벨옆 Text Box에 출력
def result_display(select, data='input data'):

    if select == 0:
        RV_SN.delete(0, END)
        RV_SN.insert(20, str(data))
    elif select == 1:
        RV_SN.delete(0, END)
        RV_SN.insert(20, "Serial Number Error")
    elif select == 2:
        RV_TIME.delete(0, END)
        RV_TIME.insert(20, data)
    elif select == 3:
        RV_TACT.delete(0, END)
        RV_TACT.insert(20, str(data) + " [sec]")

def Reformat_Image(image, ratio_w, ratio_h):
    height, width = image.shape[:2]
    width = int(width * ratio_w)
    height = int(height * ratio_h)
    # res = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    res = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
    return res


def chessDistortionInit():
    global objpoints, imgpoints, resolution

    # 체스판으로 이미지 보정.
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((9 * 13, 3), np.float32)
    objp[:, :2] = np.mgrid[0:13, 0:9].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob('D:/chess/*.bmp')  # 체스 이미지들

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (13, 9), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)
    print("Complete Calibration of Chess board")

# 결과 저장 이미지 출력
def imageShow(N, Display):
    frame = N
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2image = Img.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=cv2image)
    Display.imgtk = imgtk
    Display.configure(image=imgtk)

# 실시간웹캠 출력
def webCamShow(N, Display, cam_no):
    _, frame = N
    framecp = frame.copy()

    # GUI에 표현되는 프레임 크기 비율 (x, y 값 비율)
    frame = Reformat_Image(frame, 0.16, 0.16)

    # tk 상으로 변환하기 위해
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cv2image = Img.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=cv2image)
    Display.imgtk = imgtk
    Display.configure(image=imgtk)
    return framecp

# 무한 루프
@logging_time  # tact time 측정 deco 함수
def read_frame():
    global cam1_label, dipoleResult, dipole_label, choke_label
    global resolution

    rawframe = webCamShow(cap.read(), cam1_label, 0)
    Resultlist = checkStatusSignal(rawframe)         # (PLC 가 Ready를 보내는지 polling으로 체크), Return Dipole result

    # print(type(Resultlist))

    if Resultlist == None:
        pass
    else:
        # Choke Label Mark
        choke_label = Label(root)
        choke_label.place(x=screen_width * (640 / tk_width), y=screen_height * (10 / tk_height))

        chokeResult = Reformat_Image(Resultlist[1], 0.51, 0.51)
        imageShow(chokeResult, choke_label)

        # Dipole Label Mark
        dipole_label = Label(root)
        dipole_label.place(x=screen_width * (1280 / tk_width), y=screen_height * (10 / tk_height))

        dipoleResult = Reformat_Image(Resultlist[0], 0.51, 0.51)
        imageShow(dipoleResult, dipole_label)

    root.after(10, read_frame)                # ms단위로 프레임을 읽음.


def main():
    global root, cam1_label
    global RV_SN, RV_TIME, RV_ACC, RV_PASS, RV_NG, RV_TACT, DA_PASS, DA_NG, DA_ACC
    global screen_width, screen_height, tk_width, tk_height
    global dipole_label, choke_label

    # initial turn off the light
    try:
        light_off()
    except:
        print("조명이 연결되어 있지 않습니다")

    # Tk 객체 소환
    root = Tk()
    root.bind('<Escape>', lambda e: root.quit())    # ESC를 누르면 GUI 종료

    screen_width = root.winfo_screenwidth()  # 모니터 폭을 읽음
    screen_height = root.winfo_screenheight()  # 모니터 너비를 읽음
    tk_width, tk_height = 1920, 1080

    # Real-time Frame 라벨 위치 설정 (동영상)
    cam1_label = Label(root)
    cam1_label.place(x=screen_width * (10 / tk_width), y=screen_height * (10 / tk_height))

    # 메인 윈도우 이름설정, Geometry 설정
    root.title("Air6449")
    root.geometry("{}x{}+{}+{}".format(screen_width, screen_height, -10, 0))

    # choke Label
    choke_label = Label(root)

    # Dipole 라벨
    dipole_label = Label(root)

    # 1st 라인 라벨
    Label(root, text="Information", height=int(screen_height * (25 / tk_height)), width=int(screen_width * (11 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 13 bold").place(x=-14, y=(screen_height / 3) + screen_height * (140 / tk_height) + (0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 2nd 라인 라벨 정보 Label 생성
    name = ["Serial\nNumber", "Current Time", "Tact Time", "No. of\nAccumulation", "No. of\nOK", "No. of\nNG",  ]  # 라벨 타이틀
    for i in range(len(name)):
        Label(root, text=name[i], height=int(screen_height * (5 / tk_height)), width=int(screen_width * (17 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 9 bold").place(x=screen_width * (95 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (i * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 3rd 라인 긴 Text입력 상자 3개
    RV_SN = Entry(root, width=int(screen_width * (19 / tk_width)), relief="groove", font="Helvetica 50 bold")
    RV_SN.place(x=screen_width * (218 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    RV_TIME = Entry(root, width=int(screen_width * (19 / tk_width)), relief="groove", font="Helvetica 50 bold")
    RV_TIME.place(x=screen_width * (218 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (1 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    RV_TACT = Entry(root, width=int(screen_width * (19 / tk_width)), relief="groove", font="Helvetica 50 bold")
    RV_TACT.place(x=screen_width * (218 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (2 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 4th 라인 짧은 Text입력 상자 6개
    RV_ACC = Entry(root, width=int(screen_width * (7 / tk_width)), relief="groove", font="Helvetica 50 bold")
    RV_ACC.place(x=screen_width * (322 / tk_width), y=(screen_height / 3) + screen_height * (138 / tk_height) + (3 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    RV_PASS = Entry(root, width=int(screen_width * (7 / tk_width)), relief="groove", font="Helvetica 50 bold")
    RV_PASS.place(x=screen_width * (322 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (4 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    RV_NG = Entry(root, width=int(screen_width * (7 / tk_width)), relief="groove", font="Helvetica 50 bold")
    RV_NG.place(x=screen_width * (322 / tk_width),y=(screen_height / 3) + screen_height * (140 / tk_height) + (5 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    DA_ACC = Entry(root, width=int(screen_width * (7 / tk_width)), relief="groove", font="Helvetica 50 bold")
    DA_ACC.place(x=screen_width * (662 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (3 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    DA_PASS = Entry(root, width=int(screen_width * (7 / tk_width)), relief="groove", font="Helvetica 50 bold")
    DA_PASS.place(x=screen_width * (662 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (4 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    DA_NG = Entry(root, width=int(screen_width * (7 / tk_width)), relief="groove", font="Helvetica 50 bold")
    DA_NG.place(x=screen_width * (662 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (5 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 5th 6개의 하위목록 라벨 생성.
    for i in range(3):
        Label(root, text="Choke", height=int(screen_height * (5 / tk_height)), width=int(screen_width * (14 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 9 bold").place(x=screen_width * (219 / tk_width), y=(screen_height / 3) + screen_height * (139 / tk_height) + ((i + 3) * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)
        Label(root, text="Dipole", height=int(screen_height * (5 / tk_height)), width=int(screen_width * (14 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 9 bold").place(x=screen_width * (559 / tk_width), y=(screen_height / 3) + screen_height * (139 / tk_height) + ((i + 3) * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 6th 오른쪽 전체박스 생성
    Label(root, height=int(screen_height * (25 / tk_height)), width=int(screen_width * (90 / tk_width)), relief="groove", bg="#ebebeb", font="Helvetica 13 bold").place(x=screen_width * (970 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 7th Open folder 라벨 생성
    Label(root, text="Open folder", height=int(screen_height * (5 / tk_height)),
          width=int(screen_width * (13 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 13 bold").place(x=screen_width * (970 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 8th 하위 목록 라벨 생성 pass, fail, log
    MF_name_list = ["PASS", "FAIL", "LOG"]
    for i in range(len(MF_name_list)):
        Label(root, text=MF_name_list[i], height=int(screen_height * (4 / tk_height)), width=int(screen_width * (10 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 12 bold").place(x=screen_width * (1160 / tk_width) + (i * 230), y=(screen_height / 3) + screen_height * (150 / tk_height), relx=0.01, rely=0.01)

    # 9th 3개의 버튼 생성
    Button(root, text="Open\nPass Folder", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", width=int(screen_width * (10 / tk_width)), height=int(screen_height * (4 / tk_height)), bd=3, padx=2, pady=2, command=open_folder_pass).place(x=screen_width * (1290 / tk_width) + (0 * 230), y=(screen_height / 3) + screen_height * (161 / tk_height) + (0 * screen_height * (80 / tk_height)))
    Button(root, text="Open\nFail Folder", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", width=int(screen_width * (10 / tk_width)), height=int(screen_height * (4 / tk_height)), bd=3, padx=2, pady=2, command=open_folder_ng).place(x=screen_width * (1290 / tk_width) + (1 * 230), y=(screen_height / 3) + screen_height * (161 / tk_height) + (0 * screen_height * (80 / tk_height)))
    Button(root, text="Open\nLog Folder", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", width=int(screen_width * (10 / tk_width)), height=int(screen_height * (4 / tk_height)), bd=3, padx=2, pady=2, command=open_folder_log).place(x=screen_width * (1290 / tk_width) + (2 * 230), y=(screen_height / 3) + screen_height * (161 / tk_height) + (0 * screen_height * (80 / tk_height)))

    # 10th Choke Counter 라벨
    Label(root, text="Choke Count\n(NG Count)", height=int(screen_height * (5 / tk_height)), width=int(screen_width * (13 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 13 bold").place(x=screen_width * (970 / tk_width), y=(screen_height / 3) + screen_height * (270 / tk_height) + (0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 11th Result 라벨
    Label(root, text="Result", height=int(screen_height * (5 / tk_height)), width=int(screen_width * (13 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 13 bold").place(x=screen_width * (1480 / tk_width),y=(screen_height / 3) + screen_height * (270 / tk_height) + (0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 10th Dipole Counter 라벨
    Label(root, text="Dipole Count\n(NG Count)", height=int(screen_height * (5 / tk_height)), width=int(screen_width * (13 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 13 bold").place(x=screen_width * (970 / tk_width), y=(screen_height / 3) + screen_height * (395 / tk_height) + (0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    chessDistortionInit()   # 왜곡 보정 초기화

    read_frame()        # 연속Frame loop
    root.mainloop()     # Gui를 가동시키는 loop

if __name__ == "__main__":
    main()