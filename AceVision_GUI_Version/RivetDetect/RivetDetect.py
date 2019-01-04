# Author  : Won Jae Lee
# Version : 3.7.1

import numpy as np                          # pip install numpy
import cv2                                  # pip install python-opencv
from PIL import Image as Img                # pip install PIL
import pyzbar.pyzbar as pyzbar              # pip install pyzbar
from more_itertools import unique_everseen  # pip install more_itertools
from PIL import ImageTk
from math import *
import datetime
import time
import os
from tkinter import *


width, height = 640, 480
cap1 = cv2.VideoCapture(0)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap2 = cv2.VideoCapture(1)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap3 = cv2.VideoCapture(2)
cap3.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


# 데이터를 저장할 위치(서버저장)
store_location = "C:\Data_Record/"

font = cv2.FONT_HERSHEY_COMPLEX  # normal size sans-serif font
fontScale = 5
thickness = 4

# 시리얼번호 전역변수
#serialnum = 123456789

OK = 0
NG = 0

check_year = 0
check_month = 0
check_day = 0
check_make_folder = 0
check_result = 0

Serial_No = ''
pre_Serial_No = 0

accum_cam1 = 0
count_fail_rivet_cam1 = 0
count_pass_rivet_cam1 = 0

accum_cam2 = 0
count_fail_rivet_cam2 = 0
count_pass_rivet_cam2 = 0

accum_cam3 = 0
count_fail_rivet_cam3 = 0
count_pass_rivet_cam3 = 0

accum = 0
count_fail_rivet = 0
count_pass_rivet = 0

Rivet_num1 = 0
Rivet_num2 = 0
Rivet_num3 = 0

# <======= 사각박스 크기 입력
box_width = 10
box_height = 10

Start_Rivet_flag_cam1 = 0
Start_Rivet_flag_cam2 = 0
Start_Rivet_flag_cam3 = 0

Rivet_tuple_cam1 = []
Rivet_tuple_cam2 = []
Rivet_tuple_cam3 = []

exception_box_cam1 = []
exception_box_cam2 = []
exception_box_cam3 = []

'''
exception_box_cam1 = [[100, 100], [200, 200]]  # <======= 1번 카메라 이곳에 예외처리할 사각박스 좌표를 입력.
exception_box_cam2 = [[300, 300], [400, 400]]  # <======= 2번 카메라 이곳에 예외처리할 사각박스 좌표를 입력.
exception_box_cam3 = [[200, 100], [300, 200]]  # <======= 3번 카메라 이곳에 예외처리할 사각박스 좌표를 입력.
'''

def get_today():
    now = time.localtime()
    local_time = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    return local_time

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

def check_rivet_result():
    global check_rivet_pass_cam1, check_rivet_fail_cam1
    global check_rivet_pass_cam2, check_rivet_fail_cam2
    global check_rivet_pass_cam3, check_rivet_fail_cam3
    global count_pass_rivet, count_fail_rivet, accum
    global judge1, judge2, judge3

    check_rivet_result = check_rivet_pass_cam1 + check_rivet_pass_cam2 + check_rivet_pass_cam3

    print("judge1", judge1, "judge2", judge2, "judge3", judge3)

    if judge1 != '' and judge1 != '' and judge1 != '':
        if check_rivet_result == 3:
            count_pass_rivet += 1
        else:
            count_fail_rivet += 1

    accum = count_pass_rivet + count_fail_rivet

    print("count_pass_rivet : ", count_pass_rivet, "  count_fail_rivet: ", count_fail_rivet, "  accum : ", accum)

def leave_log(cam_no):
    global check_year, check_month, check_day, f
    global count_pass_rivet, count_fail_rivet, accum
    global count_pass_rivet_cam1, count_fail_rivet_cam1, accum_cam1
    global count_pass_rivet_cam2, count_fail_rivet_cam2, accum_cam2
    global count_pass_rivet_cam3, count_fail_rivet_cam3, accum_cam3
    global today, Serial_No, check_result

    year, month, day, hour, minute, sec = check_time_value()

    filename = str(year) + str("%02d" % month) + str("%02d" % day)
    if (year != check_year and month != check_month and day != check_day):
        print("새로운 로그 파일 생성")
        today = get_today()
        foldername_log = store_location + today + "/rivet" + "/log"
        make_folder(foldername_log)
        f = open(store_location + today + "/rivet/log/log_%s.txt" % filename, 'w')
        data = "시리얼 넘버  //  판독 시간  //  누적 판독량  //  정상  //  불량  \n"
        f.write(data)
        f = open(store_location + today + "/rivet/log/log_%s_cam1.txt" % filename, 'w')
        data = "시리얼 넘버  //  판독 시간  //  누적 판독량  //  정상  //  불량  \n"
        f.write(data)
        f = open(store_location + today + "/rivet/log/log_%s_cam2.txt" % filename, 'w')
        data = "시리얼 넘버  //  판독 시간  //  누적 판독량  //  정상  //  불량  \n"
        f.write(data)
        f = open(store_location + today + "/rivet/log/log_%s_cam3.txt" % filename, 'w')
        data = "시리얼 넘버  //  판독 시간  //  누적 판독량  //  정상  //  불량  \n"
        f.write(data)

        check_year = datetime.datetime.now().year
        check_month = datetime.datetime.now().month
        check_day = datetime.datetime.now().day

    if cam_no == 1:
        f = open(store_location + today + "/rivet/log/log_%s_cam1.txt" % filename, 'a')
        localtime = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + " " + str("%02d" % hour) + ":" + str("%02d" % minute) + ":" + str("%02d" % sec)
        data = str(Serial_No) + " // " + str(localtime) + " // " + str("%04d" % accum_cam1) + " // " + str("%04d" % count_pass_rivet_cam1) + " // " + str("%04d" % count_fail_rivet_cam1) + "\n"
    elif cam_no == 2:
        f = open(store_location + today + "/rivet/log/log_%s_cam2.txt" % filename, 'a')
        localtime = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + " " + str("%02d" % hour) + ":" + str("%02d" % minute) + ":" + str("%02d" % sec)
        data = str(Serial_No) + " // " + str(localtime) + " // " + str("%04d" % accum_cam2) + " // " + str("%04d" % count_pass_rivet_cam2) + " // " + str("%04d" % count_fail_rivet_cam2) + "\n"
    elif cam_no == 3:
        f = open(store_location + today + "/rivet/log/log_%s_cam3.txt" % filename, 'a')
        localtime = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + " " + str("%02d" % hour) + ":" + str("%02d" % minute) + ":" + str("%02d" % sec)
        data = str(Serial_No) + " // " + str(localtime) + " // " + str("%04d" % accum_cam3) + " // " + str("%04d" % count_pass_rivet_cam3) + " // " + str("%04d" % count_fail_rivet_cam3) + "\n"

    elif cam_no == 4:
        f = open(store_location + today + "/rivet/log/log_%s.txt" % filename, 'a')
        localtime = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + " " + str("%02d" % hour) + ":" + str("%02d" % minute) + ":" + str("%02d" % sec)
        data = str(Serial_No) + " // " + str(localtime) + " // " + str("%04d" % accum) + " // " + str("%04d" % count_pass_rivet) + " // " + str("%04d" % count_fail_rivet) + "\n"

    f.write(data)
    f.close()

def image_save():
    global frame_cam1, frame_cam2, frame_cam3
    global Serial_No, today

    today = get_today()
    image_add = np.hstack((frame_cam1, frame_cam2))
    image_add = np.hstack((image_add, frame_cam3))

    ##전체 이미지 저장 경로 설정
    cv2.imwrite("%s.jpg"%(Serial_No), image_add)

    print("이미지 저장 완료")
    return image_add


def webCamShow(N, Display, cam_no):
    _, frame = N

    if cam_no == 1:
        frame = RivetDetect_cam1(frame)
    elif cam_no == 2:
        frame = RivetDetect_cam2(frame)
    elif cam_no == 3:
        frame = RivetDetect_cam3(frame)

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cv2image = Img.fromarray(cv2image)
    imgtk =ImageTk.PhotoImage(image=cv2image)
    Display.imgtk = imgtk
    Display.configure(image=imgtk)

def imageShow(N, Display):
    frame = N
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2image = Img.fromarray(cv2image)
    imgtk =ImageTk.PhotoImage(image=cv2image)
    Display.imgtk = imgtk
    Display.configure(image=imgtk)


def Reformat_Image(image):
    height, width = image.shape[:2]
    width = int(width*0.4)
    height = int(height*0.4)
    res = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    return res

def decode(im) :
    global Serial_No, pre_Serial_No, RV_SN

    decodedObjects = str(pyzbar.decode(im))        # 바코드와 QR코드를 찾아냄

    Serial_No = decodedObjects[16:29]

    if Serial_No != '':
        pre_Serial_No = Serial_No
        RV_SN.insert(20, Serial_No)
        print("=======\n", decodedObjects)
        print("Serial_No :", Serial_No)



def read_frame():
    ## 바코드 인식 카메라 추가 시 바코드 리드 함수 추가 위치 ##
    global exception_box_cam1, exception_box_cam2, exception_box_cam3
    global Serial_No, pre_Serial_No
    global RV_SN, frame_cam3

    webCamShow(cap1.read(), cam1_label, 1)
    webCamShow(cap2.read(), cam2_label, 2)
    webCamShow(cap3.read(), cam3_label, 3)

    #print("Serial_No:", Serial_No, "pre_Serial_No:", pre_Serial_No)
    if Serial_No != pre_Serial_No:
        decode(frame_cam3)

    image = image_save()
    image = Reformat_Image(image)
    imageShow(image, image_label)

    if cv2.waitKey(1) & 0xff == ord('s'):
        check_rivet_result()
        leave_log(1)
        leave_log(2)
        leave_log(3)
        leave_log(4)
        print("로그 완료")

    print("============   Exception Box   ==================")
    print("exception_box_cam1", exception_box_cam1)
    print("exception_box_cam2", exception_box_cam2)
    print("exception_box_cam3", exception_box_cam3)

    print("============   Rivet Center   ==================")
    print("Rivet_center1", Rivet_center1)
    print("Rivet_center2", Rivet_center2)
    print("Rivet_center3", Rivet_center3)

    root.after(10, read_frame)


def RivetDetect_cam1(frame):
    global Start_Rivet_flag_cam1, judge1
    global accum_cam1, count_fail_rivet_cam1, count_pass_rivet_cam1
    global check_make_folder, Rivet_num1, Rivet_tuple_cam1
    global Serial_No, check_result, Rivet_center1
    global frame_cam1, check_rivet_pass_cam1, check_rivet_fail_cam1
    global exception_box_cam1, final_mask1

    # col,row,_ = frame.shape # frame 화면크기 출력, (y ,x) = (480x640)
    # print(col,row)
    frame2 = frame.copy()  # 영상원본
    frame_cam1 = frame.copy()

    frame = cv2.GaussianBlur(frame, (3, 3), 0)  # 원본에 가우시안 필터적용
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(frame)  # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

    frame_hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)  # H,L,S 분리

    _, gray1 = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 93, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 99, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 25, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 165, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 230, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 120, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 165, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 110, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 170, 255, cv2.THRESH_BINARY_INV)

    _, gray_ = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY)
    _, blue_ = cv2.threshold(blue, 0, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 10, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 0, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 5, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 10, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, 40, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, 95, 255, cv2.THRESH_BINARY)
    _, S_ = cv2.threshold(S, 65, 255, cv2.THRESH_BINARY)

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
    final_mask1 = cv2.bitwise_and(final_mask, v_)
    # final_mask = cv2.bitwise_and(final_mask, H_)
    # final_mask = cv2.bitwise_and(final_mask, L_)
    # final_mask = cv2.bitwise_and(final_mask, S_)
    result = cv2.bitwise_and(frame2, frame2, mask=final_mask1)

    #################### 리벳 중심좌표값 자동 저장용 ##########################

    num = 1
    judge1 = ''
    check_rivet_pass_cam1 = 0
    check_rivet_fail_cam1 = 0

    # 예외 처리할 부분 사각박스 씌우기
    for i in range(len(exception_box_cam1)):
        frame = cv2.rectangle(frame, tuple(exception_box_cam1[i]),(exception_box_cam1[i][0] + box_width, exception_box_cam1[i][1] + box_height), (0, 255, 0), 1)

    if Start_Rivet_flag_cam1 == 0:  # 시작할때 한번만 작동 플레그.
        #Rivet_tuple = Rivet_tuple_cam1
        Rivet_center1 = []
        cx_origin = 0
        cy_origin = 0

        _, contours, _ = cv2.findContours(final_mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
        if len(contours) != 0:
            for contour in contours:
                if (cv2.contourArea(contour) > 800) and (cv2.contourArea(contour) < 4500):  # **필요한 면적을 찾아 중심점 좌표를 저장
                    ball_area = cv2.contourArea(contour)
                    mom = contour
                    M = cv2.moments(mom)
                    cx_origin = int(M['m10'] / M['m00'])
                    cy_origin = int(M['m01'] / M['m00'])

                    Rivet_center1.append([cx_origin, cy_origin])  # 중심좌표 list에 추가

                    # 좌표값 사각박스 내 예외 처리

                    for i in range(len(exception_box_cam1)):
                        if (exception_box_cam1[i][0] < cx_origin  and cx_origin < (exception_box_cam1[i][0] + box_width)) \
                                and (exception_box_cam1[i][1] < cy_origin and cy_origin < (exception_box_cam1[i][1] + box_height)):  # 중심좌표가 예외 처리 사각박스 안에 있나 비교
                            Rivet_center1.pop()  # 예외처리 박스 안에 있으면, append된 마지막 리스트를 다시 빼버림.

                    cv2.circle(frame, (cx_origin, cy_origin), 10, (0, 255, 0), -1)  # 처음에 찍힌 원래 중심 좌표 표시, 예외처리 하기 전 중심좌표들 표시

    ##### 자동 좌표값 저장하기 #####
    print(str(num) + " 저장된 리벳의 좌표:", Rivet_center1)  # 자동 저장된 중심점값 출력
    Rivet_num1 = len(Rivet_center1)  # 자동 저장된 리벳의 갯수값 저장.

    Rivet_tuple_cam1 = []
    for i in range(Rivet_num1):
        Rivet_tuple_cam1.append(tuple(Rivet_center1[i]))  # 자동 저장된 리벳 좌표값을 튜플로 변환후 리스트에 저장. -> (Circle 마크에 쓰기 위해)

    #cv2.imshow('init_location' + str(num) +'.jpg', frame)  # 이미지 확인용.
    cv2.imwrite('init_location' + str(num) + '.jpg', frame)  # 처음 이미지 캡쳐후 저장.
    ##############################

    Start_Rivet_flag_cam1 = 1

    #############################################################################

    reverse = cv2.bitwise_not(final_mask1)
    reverse_copy = reverse.copy()

        # ** 리벳을 검출할 위치에 원으로 좌표 표시.
    for i in range(Rivet_num1):
        reverse_copy = cv2.circle(reverse_copy, Rivet_tuple_cam1[i], 10, (0, 0, 0), -1)  # 가운데 점 픽셀값 확인용 (x,y)값으로 받음.
        frame = cv2.circle(frame, Rivet_tuple_cam1[i], 10, (0, 255, 255), -1)  # 원본에도 색상이 있는 점 표시.

    # ** 한 픽셀당 Binary 값을 표시.
    # [y , x]의 픽셀값 입력받음.
    pixel_val_list = []

    #print("Rivet_num1 : ",Rivet_num1)
    # 리벳이 탐지유무에 따른 화면 출력.
    if Rivet_num1 != 0:
        for i in range(Rivet_num1):
            pixel_val1 = reverse[Rivet_center1[i][1], Rivet_center1[i][0]]  # 픽셀값 저장 (0, 255)
            if pixel_val1 == 255:  # 검출된곳은 1, 검출되지 않을곳은 0으로 변환.
                pixel_val1 = 0
            else:
                pixel_val1 = 1

            pixel_val_list.append(pixel_val1)  # 변환된 값을 리스트에 추가
            pixel_sum = sum(pixel_val_list)  # 모든 픽셀의 합

        # print(pixel_val_list, pixel_sum)    # 픽셀값과 합계 출력

        if pixel_sum == Rivet_num1:
            # 리벳의 갯수와 픽셀의 값이 일치하면 합격
            judge1 = "OK"
        else:
            # 그 외 불합격
            cv2.putText(frame, '**NG**', (50, 300), font, fontScale, (0, 0, 255), 2, cv2.LINE_AA)
            judge1 = "NG"
    else:
        cv2.putText(frame, "No data", (50, 300), font, 2, (255, 0, 0), 2, cv2.LINE_AA)


    # stopper로 부터 아스키코드 'a' 가 들어오면 화면 캡쳐 - 데이터 저장. 로그기록.
    if cv2.waitKey(1) & 0xff == ord('a'):

        #accum = accum + 1  # 누적 판독수 축적.

        fn = datetime.datetime.now()
        folder_name = str(fn.year) + "-" + str("%02d" % fn.month) + "-" + str("%02d" % fn.day)

        if check_make_folder == 0:
            today = get_today()
            foldername_today = store_location + today
            make_folder(foldername_today)
            foldername_barcode = store_location + today + "/rivet"
            make_folder(foldername_barcode)
            foldername_pass = store_location + today + "/rivet" + "/pass"
            make_folder(foldername_pass)
            foldername_fail = store_location + today + "/rivet" + "/fail"
            make_folder(foldername_fail)
            check_make_folder = 1

        if judge1 != '':
            if judge1 == "OK":
                cv2.imwrite(store_location + "%s/rivet/pass/%s.jpg" % (folder_name, Serial_No), frame)
                count_pass_rivet_cam1 += 1
                check_rivet_pass_cam1 = 1
                '''         
                cv2.imwrite(store_location + "/PASS/" + str(serialnum) + "_" + "cam" + cam + "_" + s + "_" + str(
                    cnt) + "_" + judge + ".jpg", frame)
                '''
            else:
                cv2.imwrite(store_location + "%s/rivet/fail/%s.jpg" % (folder_name, Serial_No), frame)
                count_fail_rivet_cam1 += 1
                check_rivet_fail_cam1 = 1
                '''
                cv2.imwrite(store_location + "/NG/" + str(serialnum) + "_" + "cam" + cam + "_" + s + "_" + str(
                    cnt) + "_" + judge + ".jpg", frame)
                '''
            accum_cam1 = count_pass_rivet_cam1 + count_fail_rivet_cam1
            #leave_log(num)  # 판독값을 로그로 남김.
        else:
            print("No data")

    print("judge1", judge1)
    return frame

def RivetDetect_cam2(frame):
    global Start_Rivet_flag_cam2, judge2
    global accum_cam2, count_fail_rivet_cam2, count_pass_rivet_cam2
    global check_make_folder, Rivet_num2, Rivet_tuple_cam2
    global Serial_No, check_result, Rivet_center2
    global frame_cam2, check_rivet_pass_cam2, check_rivet_fail_cam2
    global exception_box_cam2, final_mask2

    # col,row,_ = frame.shape # frame 화면크기 출력, (y ,x) = (480x640)
    # print(col,row)
    frame2 = frame.copy()  # 영상원본
    frame_cam2 = frame.copy()

    frame = cv2.GaussianBlur(frame, (3, 3), 0)  # 원본에 가우시안 필터적용
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(frame)  # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

    frame_hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)  # H,L,S 분리

    _, gray1 = cv2.threshold(gray_frame, 229, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 218, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 218, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 222, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 255, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 255, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 239, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 255, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 213, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)

    _, gray_ = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY)
    _, blue_ = cv2.threshold(blue, 0, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 10, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 0, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 0, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 0, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, 0, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, 0, 255, cv2.THRESH_BINARY)
    _, S_ = cv2.threshold(S, 0, 255, cv2.THRESH_BINARY)

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
    final_mask2 = cv2.bitwise_and(final_mask, v_)
    # final_mask = cv2.bitwise_and(final_mask, H_)
    # final_mask = cv2.bitwise_and(final_mask, L_)
    # final_mask = cv2.bitwise_and(final_mask, S_)
    result = cv2.bitwise_and(frame2, frame2, mask=final_mask2)

    #################### 리벳 중심좌표값 자동 저장용 ##########################


    num = 2
    judge2 = ''
    check_rivet_pass_cam2 = 0
    check_rivet_fail_cam2 = 0

    # 예외 처리할 부분 사각박스 씌우기
    for i in range(len(exception_box_cam2)):
        frame = cv2.rectangle(frame, tuple(exception_box_cam2[i]),
                              (exception_box_cam2[i][0] + box_width, exception_box_cam2[i][1] + box_height), (0, 255, 0), 1)

    if Start_Rivet_flag_cam2 == 0:  # 시작할때 한번만 작동 플레그.
        #Rivet_tuple = Rivet_tuple_cam2
        Rivet_center2 = []
        cx_origin = 0
        cy_origin = 0

        _, contours, _ = cv2.findContours(final_mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
        if len(contours) != 0:
            for contour in contours:
                if (cv2.contourArea(contour) > 800) and (cv2.contourArea(contour) < 4500):  # **필요한 면적을 찾아 중심점 좌표를 저장
                    ball_area = cv2.contourArea(contour)
                    mom = contour
                    M = cv2.moments(mom)
                    cx_origin = int(M['m10'] / M['m00'])
                    cy_origin = int(M['m01'] / M['m00'])

                    Rivet_center2.append([cx_origin, cy_origin])  # 중심좌표 list에 추가

                    # 좌표값 사각박스 내 예외 처리

                    for i in range(len(exception_box_cam2)):
                        if (cx_origin > exception_box_cam2[i][0] and cx_origin < (exception_box_cam2[i][0] + box_width)) and (
                                cy_origin > exception_box_cam2[i][1] and cy_origin < (
                                exception_box_cam2[i][1] + box_height)):  # 중심좌표가 예외 처리 사각박스 안에 있나 비교
                            Rivet_center2.pop()  # 예외처리 박스 안에 있으면, append된 마지막 리스트를 다시 빼버림.

                    cv2.circle(frame, (cx_origin, cy_origin), 10, (0, 255, 0), -1)  # 처음에 찍힌 원래 중심 좌표 표시, 예외처리 하기 전 중심좌표들 표시

    ##### 자동 좌표값 저장하기 #####
    print(str(num) + " 저장된 리벳의 좌표:", Rivet_center2)  # 자동 저장된 중심점값 출력
    Rivet_num2 = len(Rivet_center2)  # 자동 저장된 리벳의 갯수값 저장.

    Rivet_tuple_cam2 = []
    for i in range(Rivet_num2):
        Rivet_tuple_cam2.append(tuple(Rivet_center2[i]))  # 자동 저장된 리벳 좌표값을 튜플로 변환후 리스트에 저장. -> (Circle 마크에 쓰기 위해)

    #cv2.imshow('init_location' + str(num) +'.jpg', frame)  # 이미지 확인용.
    cv2.imwrite('init_location' + str(num) + '.jpg', frame)  # 처음 이미지 캡쳐후 저장.
    ##############################

    Start_Rivet_flag_cam2 = 1

    #############################################################################

    reverse = cv2.bitwise_not(final_mask2)
    reverse_copy = reverse.copy()

        # ** 리벳을 검출할 위치에 원으로 좌표 표시.
    for i in range(Rivet_num2):
        reverse_copy = cv2.circle(reverse_copy, Rivet_tuple_cam2[i], 10, (0, 0, 0), -1)  # 가운데 점 픽셀값 확인용 (x,y)값으로 받음.
        frame = cv2.circle(frame, Rivet_tuple_cam2[i], 10, (0, 255, 255), -1)  # 원본에도 색상이 있는 점 표시.

    # ** 한 픽셀당 Binary 값을 표시.
    # [y , x]의 픽셀값 입력받음.
    pixel_val_list = []

    #print("Rivet_num2 : ",Rivet_num2)
    # 리벳이 탐지유무에 따른 화면 출력.
    if Rivet_num2 != 0:
        for i in range(Rivet_num2):
            pixel_val2 = reverse[Rivet_center2[i][1], Rivet_center2[i][0]]  # 픽셀값 저장 (0, 255)
            if pixel_val2 == 255:  # 검출된곳은 1, 검출되지 않을곳은 0으로 변환.
                pixel_val2 = 0
            else:
                pixel_val2 = 1

            pixel_val_list.append(pixel_val2)  # 변환된 값을 리스트에 추가
            pixel_sum = sum(pixel_val_list)  # 모든 픽셀의 합

        # print(pixel_val_list, pixel_sum)    # 픽셀값과 합계 출력

        if pixel_sum == Rivet_num2:
            # 리벳의 갯수와 픽셀의 값이 일치하면 합격
            judge2 = "OK"
        else:
            # 그 외 불합격
            cv2.putText(frame, '**NG**', (50, 300), font, fontScale, (0, 0, 255), 2, cv2.LINE_AA)
            judge2 = "NG"
    else:
        cv2.putText(frame, "No data", (50, 300), font, 2, (255, 0, 0), 2, cv2.LINE_AA)


    # stopper로 부터 아스키코드 'a' 가 들어오면 화면 캡쳐 - 데이터 저장. 로그기록.
    if cv2.waitKey(1) & 0xff == ord('b'):

        #accum = accum + 1  # 누적 판독수 축적.

        fn = datetime.datetime.now()
        folder_name = str(fn.year) + "-" + str("%02d" % fn.month) + "-" + str("%02d" % fn.day)

        if check_make_folder == 0:
            today = get_today()
            foldername_today = store_location + today
            make_folder(foldername_today)
            foldername_barcode = store_location + today + "/rivet"
            make_folder(foldername_barcode)
            foldername_pass = store_location + today + "/rivet" + "/pass"
            make_folder(foldername_pass)
            foldername_fail = store_location + today + "/rivet" + "/fail"
            make_folder(foldername_fail)
            check_make_folder = 1


        if judge2 != '':
            if judge2 == "OK":
                cv2.imwrite(store_location + "%s/rivet/pass/%s.jpg" % (folder_name, Serial_No), frame)
                count_pass_rivet_cam2 += 1
                check_rivet_pass_cam2 = 1
                '''         
                cv2.imwrite(store_location + "/PASS/" + str(serialnum) + "_" + "cam" + cam + "_" + s + "_" + str(
                    cnt) + "_" + judge + ".jpg", frame)
                '''
            else:
                cv2.imwrite(store_location + "%s/rivet/fail/%s.jpg" % (folder_name, Serial_No), frame)
                count_fail_rivet_cam2 += 1
                check_rivet_fail_cam2 = 1
                '''
                cv2.imwrite(store_location + "/NG/" + str(serialnum) + "_" + "cam" + cam + "_" + s + "_" + str(
                    cnt) + "_" + judge + ".jpg", frame)
                '''
            accum_cam2 = count_pass_rivet_cam2 + count_fail_rivet_cam2
            #leave_log(num)  # 판독값을 로그로 남김.
        else:
            print("No data")

    print("judge2", judge2)
    return frame

def RivetDetect_cam3(frame):
    global Start_Rivet_flag_cam3, judge3
    global accum_cam3, count_fail_rivet_cam3, count_pass_rivet_cam3
    global check_make_folder, Rivet_num3, Rivet_tuple_cam3
    global Serial_No, check_result, Rivet_center3
    global frame_cam3, check_rivet_pass_cam3, check_rivet_fail_cam3
    global exception_box_cam3, final_mask3

    # col,row,_ = frame.shape # frame 화면크기 출력, (y ,x) = (480x640)
    # print(col,row)
    frame2 = frame.copy()  # 영상원본
    frame_cam3 = frame.copy()

    frame = cv2.GaussianBlur(frame, (3, 3), 0)  # 원본에 가우시안 필터적용
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(frame)  # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

    frame_hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)  # H,L,S 분리

    _, gray1 = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 93, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 99, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 25, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 165, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 230, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 120, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 165, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 110, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 170, 255, cv2.THRESH_BINARY_INV)

    _, gray_ = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY)
    _, blue_ = cv2.threshold(blue, 0, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 10, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 0, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 5, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 10, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, 40, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, 95, 255, cv2.THRESH_BINARY)
    _, S_ = cv2.threshold(S, 65, 255, cv2.THRESH_BINARY)

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
    final_mask3 = cv2.bitwise_and(final_mask, v_)
    # final_mask = cv2.bitwise_and(final_mask, H_)
    # final_mask = cv2.bitwise_and(final_mask, L_)
    # final_mask = cv2.bitwise_and(final_mask, S_)
    result = cv2.bitwise_and(frame2, frame2, mask=final_mask3)

    #################### 리벳 중심좌표값 자동 저장용 ##########################


    num = 3
    judge3 = ''
    check_rivet_pass_cam3 = 0
    check_rivet_fail_cam3 = 0

    # 예외 처리할 부분 사각박스 씌우기
    for i in range(len(exception_box_cam3)):
        frame = cv2.rectangle(frame, tuple(exception_box_cam3[i]),
                              (exception_box_cam3[i][0] + box_width, exception_box_cam3[i][1] + box_height), (0, 255, 0), 1)

    if Start_Rivet_flag_cam3 == 0:  # 시작할때 한번만 작동 플레그.
        #Rivet_tuple = Rivet_tuple_cam3

        Rivet_center3 = []
        cx_origin = 0
        cy_origin = 0

        _, contours, _ = cv2.findContours(final_mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
        if len(contours) != 0:
            for contour in contours:
                if (cv2.contourArea(contour) > 800) and (cv2.contourArea(contour) < 4500):  # **필요한 면적을 찾아 중심점 좌표를 저장
                    ball_area = cv2.contourArea(contour)
                    mom = contour
                    M = cv2.moments(mom)
                    cx_origin = int(M['m10'] / M['m00'])
                    cy_origin = int(M['m01'] / M['m00'])

                    Rivet_center3.append([cx_origin, cy_origin])  # 중심좌표 list에 추가

                    # 좌표값 사각박스 내 예외 처리

                    for i in range(len(exception_box_cam3)):
                        if (cx_origin > exception_box_cam3[i][0] and cx_origin < (exception_box_cam3[i][0] + box_width)) and (
                                cy_origin > exception_box_cam3[i][1] and cy_origin < (
                                exception_box_cam3[i][1] + box_height)):  # 중심좌표가 예외 처리 사각박스 안에 있나 비교
                            Rivet_center3.pop()  # 예외처리 박스 안에 있으면, append된 마지막 리스트를 다시 빼버림.

                    cv2.circle(frame, (cx_origin, cy_origin), 10, (0, 255, 0), -1)  # 처음에 찍힌 원래 중심 좌표 표시, 예외처리 하기 전 중심좌표들 표시

    ##### 자동 좌표값 저장하기 #####
    print(str(num) + " 저장된 리벳의 좌표:", Rivet_center3)  # 자동 저장된 중심점값 출력
    Rivet_num3 = len(Rivet_center3)  # 자동 저장된 리벳의 갯수값 저장.

    Rivet_tuple_cam3 = []
    for i in range(Rivet_num3):
        Rivet_tuple_cam3.append(tuple(Rivet_center3[i]))  # 자동 저장된 리벳 좌표값을 튜플로 변환후 리스트에 저장. -> (Circle 마크에 쓰기 위해)

    #cv2.imshow('init_location' + str(num) +'.jpg', frame)  # 이미지 확인용.
    cv2.imwrite('init_location' + str(num) + '.jpg', frame)  # 처음 이미지 캡쳐후 저장.
    ##############################

    Start_Rivet_flag_cam3 = 1

    #############################################################################

    reverse = cv2.bitwise_not(final_mask3)
    reverse_copy = reverse.copy()

        # ** 리벳을 검출할 위치에 원으로 좌표 표시.
    for i in range(Rivet_num3):
        reverse_copy = cv2.circle(reverse_copy, Rivet_tuple_cam3[i], 10, (0, 0, 0), -1)  # 가운데 점 픽셀값 확인용 (x,y)값으로 받음.
        frame = cv2.circle(frame, Rivet_tuple_cam3[i], 10, (0, 255, 255), -1)  # 원본에도 색상이 있는 점 표시.

    # ** 한 픽셀당 Binary 값을 표시.
    # [y , x]의 픽셀값 입력받음.
    pixel_val_list = []

    #print("Rivet_num3 : ",Rivet_num1)
    # 리벳이 탐지유무에 따른 화면 출력.
    if Rivet_num3 != 0:
        for i in range(Rivet_num3):
            pixel_val3 = reverse[Rivet_center3[i][1], Rivet_center3[i][0]]  # 픽셀값 저장 (0, 255)
            if pixel_val3 == 255:  # 검출된곳은 1, 검출되지 않을곳은 0으로 변환.
                pixel_val3 = 0
            else:
                pixel_val3 = 1

            pixel_val_list.append(pixel_val3)  # 변환된 값을 리스트에 추가
            pixel_sum = sum(pixel_val_list)  # 모든 픽셀의 합

        # print(pixel_val_list, pixel_sum)    # 픽셀값과 합계 출력

        if pixel_sum == Rivet_num3:
            # 리벳의 갯수와 픽셀의 값이 일치하면 합격
            judge3 = "OK"
        else:
            # 그 외 불합격
            cv2.putText(frame, '**NG**', (50, 300), font, fontScale, (0, 0, 255), 2, cv2.LINE_AA)
            judge3 = "NG"
    else:
        cv2.putText(frame, "No data", (50, 300), font, 2, (255, 0, 0), 2, cv2.LINE_AA)


    # stopper로 부터 아스키코드 'a' 가 들어오면 화면 캡쳐 - 데이터 저장. 로그기록.
    if cv2.waitKey(1) & 0xff == ord('c'):

        #accum = accum + 1  # 누적 판독수 축적.

        fn = datetime.datetime.now()
        folder_name = str(fn.year) + "-" + str("%02d" % fn.month) + "-" + str("%02d" % fn.day)

        if check_make_folder == 0:
            today = get_today()
            foldername_today = store_location + today
            make_folder(foldername_today)
            foldername_barcode = store_location + today + "/rivet"
            make_folder(foldername_barcode)
            foldername_pass = store_location + today + "/rivet" + "/pass"
            make_folder(foldername_pass)
            foldername_fail = store_location + today + "/rivet" + "/fail"
            make_folder(foldername_fail)
            check_make_folder = 1

        if judge3 != '':
            if judge3 == "OK":
                cv2.imwrite(store_location + "%s/rivet/pass/%s.jpg" % (folder_name, Serial_No), frame)
                count_pass_rivet_cam3 += 1
                check_rivet_pass_cam3 = 1
                '''         
                cv2.imwrite(store_location + "/PASS/" + str(serialnum) + "_" + "cam" + cam + "_" + s + "_" + str(
                    cnt) + "_" + judge + ".jpg", frame)
                '''
            else:
                cv2.imwrite(store_location + "%s/rivet/fail/%s.jpg" % (folder_name, Serial_No), frame)
                count_fail_rivet_cam3 += 1
                check_rivet_fail_cam3 = 1
                '''
                cv2.imwrite(store_location + "/NG/" + str(serialnum) + "_" + "cam" + cam + "_" + s + "_" + str(
                    cnt) + "_" + judge + ".jpg", frame)
                '''
            accum_cam3 = count_pass_rivet_cam3 + count_fail_rivet_cam3
            #leave_log(num)  # 판독값을 로그로 남김.
        else:
            print("No data")

    #print("judge3", judge3)
    return frame

def add_exception_area_cam1():
    global exception_box_cam1
    global EB1_X, EB1_Y
    global Rivet_center1, Rivet_num1
    global Start_Rivet_flag_cam1
    global box_width, box_height
    x = eval(EB1_X.get())
    y = eval(EB1_Y.get())
    exception_box_cam1.append([x,y])
    EB1_X.delete(0, END)
    EB1_Y.delete(0, END)
    #Start_Rivet_flag_cam1 = 0
    #Rivet_center1.remove([x,y])

    list_delete_item = []
    for i in range(len(exception_box_cam1)):
        for j in range(len(Rivet_center1)):
            if ((exception_box_cam1[i][0] - box_width) < Rivet_center1[j][0]) and (
                    Rivet_center1[j][0] < (exception_box_cam1[i][0] + box_width)) and (
                    (exception_box_cam1[i][1] - box_height) < Rivet_center1[j][1]) and (
                    Rivet_center1[j][1] < (exception_box_cam1[i][1] + box_height)):
                list_delete_item.append([Rivet_center1[j][0], Rivet_center1[j][1]])

    list_delete_item = list(unique_everseen(list_delete_item))
    for i in range(len(list_delete_item)):
        Rivet_center1.remove([list_delete_item[i][0], list_delete_item[i][1]])

    print(Rivet_center1)
    #Rivet_num1 -= 1

def add_exception_area_cam2():
    global exception_box_cam2
    global EB2_X, EB2_Y
    global Rivet_center2, Rivet_num2
    global Start_Rivet_flag_cam2
    global box_width, box_height
    x = eval(EB2_X.get())
    y = eval(EB2_Y.get())
    exception_box_cam2.append([x, y])
    EB2_X.delete(0, END)
    EB2_Y.delete(0, END)
    #Start_Rivet_flag_cam2 = 0
    #Rivet_center2.remove([x, y])

    #lenth = len(Rivet_center2) > len(exception_box_cam2) and len(Rivet_center2) or len(exception_box_cam2)
    #print("==========")
    #print("lenth:", lenth)

    list_delete_item = []
    for i in range(len(exception_box_cam2)):
        for j in range(len(Rivet_center2)):
            if ((exception_box_cam2[i][0] - box_width) < Rivet_center2[j][0]) and (
                    Rivet_center2[j][0] < (exception_box_cam2[i][0] + box_width)) and (
                    (exception_box_cam2[i][1] - box_height) < Rivet_center2[j][1]) and (
                    Rivet_center2[j][1] < (exception_box_cam2[i][1] + box_height)):
                list_delete_item.append([Rivet_center2[j][0], Rivet_center2[j][1]])

    list_delete_item = list(unique_everseen(list_delete_item))
    for i in range(len(list_delete_item)):
        Rivet_center2.remove([list_delete_item[i][0], list_delete_item[i][1]])
    print(Rivet_center2)
    #Rivet_num2 -= 1

def add_exception_area_cam3():
    global exception_box_cam3
    global EB3_X, EB3_Y
    global Rivet_center3, Rivet_num3
    global Start_Rivet_flag_cam3
    global box_width, box_height
    x = eval(EB3_X.get())
    y = eval(EB3_Y.get())
    exception_box_cam3.append([x, y])
    EB3_X.delete(0, END)
    EB3_Y.delete(0, END)
    #Start_Rivet_flag_cam3 = 0
    #Rivet_center3.remove([x, y])
    list_delete_item = []
    for i in range(len(exception_box_cam3)):
        for j in range(len(Rivet_center3)):
            if ((exception_box_cam3[i][0] - box_width) < Rivet_center3[j][0]) and (
                    Rivet_center3[j][0] < (exception_box_cam3[i][0] + box_width)) and (
                    (exception_box_cam3[i][1] - box_height) < Rivet_center3[j][1]) and (
                    Rivet_center3[j][1] < (exception_box_cam3[i][1] + box_height)):
                list_delete_item.append([Rivet_center3[j][0], Rivet_center3[j][1]])

    list_delete_item = list(unique_everseen(list_delete_item))
    for i in range(len(list_delete_item)):
        Rivet_center3.remove([list_delete_item[i][0], list_delete_item[i][1]])

    print(Rivet_center3)

    #Rivet_num3 -= 1

def execute():
    global cam1_label, cam2_label, cam3_label, image_label, root
    global RV_SN, RV_P1, RV_P2, RV_P3, RV_P4, RV_P5
    global EB1_X, EB1_Y, EB2_X, EB2_Y, EB3_X, EB3_Y

    root = Tk()

    root.bind('<Escape>', lambda e: root.quit())
    cam1_label = Label(root)
    cam1_label.place(y=10, anchor=NW)

    cam2_label = Label(root)
    cam2_label.place(x=640, y=10)

    cam3_label = Label(root)
    cam3_label.place(x=1280, y=10)

    image_label = Label(root)
    image_label.place(x=1138, y=(1080 / 3) + 205)

    width, height = 640, 480

    qr_width, qr_height = 1920, 1080
    root.title("Check_Rivet")
    root.geometry("{}x{}+{}+{}".format(qr_width, qr_height, -10, 0))

    name = ["시리얼 넘버 입력\nInput SerialNumber", "시리얼 넘버\nSerialNumber", "판독시간\nTime", "판독 수량\nNo. of Accumulation",
            "합격 수량\nNo. of OK", "불합격수량\nNo. of NG"]

    ##Label 생성
    for i in range(6):
        Label(root, text=name[i], height=5, width=17, fg="red", relief="groove", bg="#ebebeb") \
            .place(x=95, y=(qr_height / 3) + 140 + (i * 80), relx=0.01, rely=0.01)
        #Label(root, text=name[i], height=5, width=17, fg="red", relief="groove", bg="#ebebeb") \
        #    .place(x=1055, y=(qr_height / 3) + 140 + (i * 80), relx=0.01, rely=0.01)

    Label(root, text="Rivet \nDetect Info", height=25, width=11, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=-14, y=(qr_height / 3) + 140 + (0 * 80), relx=0.01, rely=0.01)

    Label(root, text="Full Image\n(reduced)", height=10, width=13, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=970, y=(qr_height / 3) + 195 + (0 * 80), relx=0.01, rely=0.01)
    Label(root, text="Add \nexception area", height=12, width=13, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=970, y=(qr_height / 3) + 390 + (0 * 80), relx=0.01, rely=0.01)

    Label(root, text="CAM1", height=2, width=15, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=1160, y=(qr_height / 3) + 145 + (0 * 80), relx=0.01, rely=0.01)
    Label(root, text="CAM2", height=2, width=15, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=1420, y=(qr_height / 3) + 145 + (0 * 80), relx=0.01, rely=0.01)
    Label(root, text="CAM3", height=2, width=15, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=1680, y=(qr_height / 3) + 145 + (0 * 80), relx=0.01, rely=0.01)

    Label(root, text="X", height=4, width=5, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=1120, y=(qr_height / 3) + 403 + (0 * 80), relx=0.01, rely=0.01)
    Label(root, text="Y", height=4, width=5, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=1120, y=(qr_height / 3) + 483 + (0 * 80), relx=0.01, rely=0.01)

    Label(root, text="X", height=4, width=5, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=1380, y=(qr_height / 3) + 403 + (0 * 80), relx=0.01, rely=0.01)
    Label(root, text="Y", height=4, width=5, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=1380, y=(qr_height / 3) + 483 + (0 * 80), relx=0.01, rely=0.01)

    Label(root, text="X", height=4, width=5, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=1640, y=(qr_height / 3) + 403 + (0 * 80), relx=0.01, rely=0.01)
    Label(root, text="Y", height=4, width=5, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=1640, y=(qr_height / 3) + 483 + (0 * 80), relx=0.01, rely=0.01)

    #Label(root, text="Suction \nSticker \nDetect Info", height=25, width=11, fg="red", relief="groove", bg="#ebebeb",
    #      font="Helvetica 13 bold").place(x=946, y=(qr_height / 3) + 140 + (0 * 80), relx=0.01, rely=0.01)

    RV_SN = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    RV_SN.place(x=218, y=(qr_height / 3) + 140 + (0 * 80), relx=0.01, rely=0.01)

    RV_P1 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    RV_P1.place(x=218, y=(qr_height / 3) + 140 + (1 * 80), relx=0.01, rely=0.01)

    RV_P2 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    RV_P2.place(x=218, y=(qr_height / 3) + 140 + (2 * 80), relx=0.01, rely=0.01)

    RV_P3 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    RV_P3.place(x=218, y=(qr_height / 3) + 140 + (3 * 80), relx=0.01, rely=0.01)

    RV_P4 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    RV_P4.place(x=218, y=(qr_height / 3) + 140 + (4 * 80), relx=0.01, rely=0.01)

    RV_P5 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    RV_P5.place(x=218, y=(qr_height / 3) + 140 + (5 * 80), relx=0.01, rely=0.01)

    ###예외 지역 설정 엔트리
    EB1_X = Entry(root, width=5, relief="groove", font="Helvetica 50 bold")
    EB1_X.place(x=1180, y=(qr_height / 3) + 403 + (0 * 80), relx=0.01, rely=0.01)

    EB1_Y = Entry(root, width=5, relief="groove", font="Helvetica 50 bold")
    EB1_Y.place(x=1180, y=(qr_height / 3) + 483 + (0 * 80), relx=0.01, rely=0.01)

    EB2_X = Entry(root, width=5, relief="groove", font="Helvetica 50 bold")
    EB2_X.place(x=1440, y=(qr_height / 3) + 403 + (0 * 80), relx=0.01, rely=0.01)

    EB2_Y = Entry(root, width=5, relief="groove", font="Helvetica 50 bold")
    EB2_Y.place(x=1440, y=(qr_height / 3) + 483 + (0 * 80), relx=0.01, rely=0.01)

    EB3_X = Entry(root, width=5, relief="groove", font="Helvetica 50 bold")
    EB3_X.place(x=1700, y=(qr_height / 3) + 403 + (0 * 80), relx=0.01, rely=0.01)

    EB3_Y = Entry(root, width=5, relief="groove", font="Helvetica 50 bold")
    EB3_Y.place(x=1700, y=(qr_height / 3) + 483 + (0 * 80), relx=0.01, rely=0.01)


    text_list = ["CAM1 Add", "CAM2 Add", "CAM3 Add"]
    command_list = [add_exception_area_cam1, add_exception_area_cam2, add_exception_area_cam3]
    for i in range(3):
        Button(root, text=text_list[i], font="돋움체", relief="raised", overrelief="solid", bg="#ebebeb", \
               width=30, height=2, bd=3, padx=2, pady=2, command=command_list[i]).place(x=1137 + (i*262), y=943)

    read_frame()
    root.mainloop()


if __name__=="__main__":
    execute()
    cap1.release()
    cap2.release()
    cap3.release()
    cv2.destroyAllWindows()

