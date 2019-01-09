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
cap1 = cv2.VideoCapture(3)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap2 = cv2.VideoCapture(2)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap3 = cv2.VideoCapture(0)
cap3.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap4 = cv2.VideoCapture(1)
cap4.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap4.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# 데이터를 저장할 위치(서버저장)
store_location = "C:/Data_Record/"

font = cv2.FONT_HERSHEY_COMPLEX  # normal size sans-serif font
fontScale = 5
thickness = 4

# <======= 사각박스 크기 입력
box_width = 0
box_height = 0

pathname = ''
# 시리얼번호 전역변수
#serialnum = 123456789

OK = 0
NG = 0
PLC_sensor = False
check_set = True
check_detect = True
check_PLC_sensor = 0

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

cam1_box_idx = 0
cam2_box_idx = 0
cam3_box_idx = 0

cam1_rect_list = []
cam2_rect_list = []
cam3_rect_list = []

cam1_except_list = []
cam2_except_list = []
cam3_except_list = []

cam1_box_list = []
cam2_box_list = []
cam3_box_list = []

Start_Rivet_flag_cam1 = 0
Start_Rivet_flag_cam2 = 0
Start_Rivet_flag_cam3 = 0

Start_except_box_cam1 = 0
Start_except_box_cam2 = 0
Start_except_box_cam3 = 0

cam1_box_width = 0
cam2_box_width = 0
cam3_box_width = 0

cam1_box_height = 0
cam2_box_height = 0
cam3_box_height = 0

Rivet_tuple_cam1 = []
Rivet_tuple_cam2 = []
Rivet_tuple_cam3 = []

exception_box_cam1 = []
exception_box_cam2 = []
exception_box_cam3 = []

rivet_center_flag1 = 0
rivet_center_flag2 = 0
rivet_center_flag3 = 0

save_revet_center1 = []
save_revet_center2 = []
save_revet_center3 = []

check_cam1_judge = 0
check_cam2_judge = 0
check_cam3_judge = 0

kernel = np.ones((3,3), np.uint8)
position = ()

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
    global count_pass_rivet_cam1, count_pass_rivet_cam2, count_pass_rivet_cam3
    global count_pass_rivet, count_fail_rivet, accum
    global result_rivet

    result_rivet = check_rivet_pass_cam1 + check_rivet_pass_cam2 + check_rivet_pass_cam3

    if result_rivet == 3:
        count_pass_rivet += 1
    else:
        count_fail_rivet += 1

    accum = count_pass_rivet + count_fail_rivet

    print("count_pass_rivet : ", count_pass_rivet, "  count_fail_rivet: ", count_fail_rivet, "  accum : ", accum)

def leave_log():
    global check_year, check_month, check_day, f
    global count_pass_rivet, count_fail_rivet, accum
    global today, Serial_No, check_result
    global RV_SN, RV_P1, RV_P2, RV_P3, RV_P4, RV_P5
    global check_make_folder, folder_name
    global store_location

    year, month, day, hour, minute, sec = check_time_value()

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

    filename = str(year) + str("%02d" % month) + str("%02d" % day)
    if (year != check_year and month != check_month and day != check_day):
        print("새로운 로그 파일 생성")
        today = get_today()
        foldername_log = store_location + today + "/rivet" + "/log"
        make_folder(foldername_log)
        f = open(store_location + today + "/rivet/log/log_%s.txt" % filename, 'w')
        data = "시리얼 넘버  //  판독 시간  //  누적 판독량  //  정상  //  불량  \n"
        f.write(data)
        '''
        f = open(store_location + today + "/rivet/log/log_%s_cam1.txt" % filename, 'w')
        data = "시리얼 넘버  //  판독 시간  //  누적 판독량  //  정상  //  불량  \n"
        f.write(data)
        f = open(store_location + today + "/rivet/log/log_%s_cam2.txt" % filename, 'w')
        data = "시리얼 넘버  //  판독 시간  //  누적 판독량  //  정상  //  불량  \n"
        f.write(data)
        f = open(store_location + today + "/rivet/log/log_%s_cam3.txt" % filename, 'w')
        data = "시리얼 넘버  //  판독 시간  //  누적 판독량  //  정상  //  불량  \n"
        f.write(data)
        '''

        check_year = datetime.datetime.now().year
        check_month = datetime.datetime.now().month
        check_day = datetime.datetime.now().day

    f = open(store_location + today + "/rivet/log/log_%s.txt" % filename, 'a')
    localtime = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + " " + str("%02d" % hour) + ":" + str("%02d" % minute) + ":" + str("%02d" % sec)
    data = str(Serial_No) + " // " + str(localtime) + " // " + str("%04d" % accum) + " // " + str("%04d" % count_pass_rivet) + " // " + str("%04d" % count_fail_rivet) + "\n"
    f.write(data)

    RV_P1.insert(20, Serial_No)
    RV_P2.insert(20, localtime)
    RV_P3.insert(20, accum)
    RV_P4.insert(20, count_pass_rivet)
    RV_P5.insert(20, count_fail_rivet)

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
    global barcode_frame

    _, frame = N

    if cam_no == 1:
        frame = RivetDetect_cam1(frame)
    elif cam_no == 2:
        frame = RivetDetect_cam2(frame)
    elif cam_no == 3:
        frame = RivetDetect_cam3(frame)
    elif cam_no ==4:
        barcode_frame = frame.copy()
        frame = Reformat_Image(barcode_frame)

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
    global Serial_No, pre_Serial_No
    global RV_SN, RV_P1, RV_P2, RV_P3, RV_P4, RV_P5

    decodedObjects = str(pyzbar.decode(im))        # 바코드와 QR코드를 찾아냄

    Serial_No = decodedObjects[16:29]

    if Serial_No != '':
        pre_Serial_No = Serial_No
        RV_SN.insert(20, Serial_No)
        RV_P1.delete(0, END)
        RV_P2.delete(0, END)
        RV_P3.delete(0, END)
        RV_P4.delete(0, END)
        RV_P5.delete(0, END)
        print("=======\n", decodedObjects)
        print("Serial_No :", Serial_No)



def read_frame():
    ## 바코드 인식 카메라 추가 시 바코드 리드 함수 추가 위치 ##
    global exception_box_cam1, exception_box_cam2, exception_box_cam3
    global Serial_No, pre_Serial_No
    global RV_SN,  RV_P1, RV_P2, RV_P3, RV_P4, RV_P5
    global check_cam1_judge, check_cam2_judge, check_cam3_judge
    global PLC_sensor, check_PLC_sensor, image_reformat, folder_name, result_rivet
    global store_location
    global position

    webCamShow(cap1.read(), cam1_label, 1)
    webCamShow(cap2.read(), cam2_label, 2)
    webCamShow(cap3.read(), cam3_label, 3)
    #print("store_location", store_location, type(store_location))

    #print("Serial_No:", Serial_No, "pre_Serial_No:", pre_Serial_No)

    if check_set == False:
        if Serial_No != pre_Serial_No:
            webCamShow(cap4.read(), cam4_label, 4)
            #_, barcode_frame = cap4.read()
            #cv2.imshow("barcode", barcode_frame)
            decode(barcode_frame)
            pass

        if check_cam1_judge == 1 and check_cam2_judge == 1 and check_cam3_judge == 1:
            check_rivet_result()
            leave_log()
            check_cam1_judge = 0
            check_cam2_judge = 0
            check_cam3_judge = 0
            PLC_sensor = False
            print("로그 완료")
            image = image_save()
            image_reformat = Reformat_Image(image)
            check_PLC_sensor = 1

        if check_PLC_sensor == 1:
            imageShow(image_reformat, image_label)
            if result_rivet == 3:
                cv2.imwrite(store_location + "%s/rivet/pass/%s.jpg" % (folder_name, Serial_No), image)
                Label(root, text="OK", font="Helvetica 140 bold", fg="RoyalBlue").place(x=1550, y=780)
            else:
                cv2.imwrite(store_location + "%s/rivet/fail/%s.jpg" % (folder_name, Serial_No), image)
                Label(root, text="NG", font="Helvetica 140 bold", fg="red").place(x=1600, y=780)

            Serial_No = ''
            check_PLC_sensor = 0
            RV_SN.delete(0,END)

        '''
        print("============   Exception Box   ==================")
        print("exception_box_cam1", exception_box_cam1)
        print("exception_box_cam2", exception_box_cam2)
        print("exception_box_cam3", exception_box_cam3)

        print("============   Rivet Center   ==================")
        print("Rivet_center1", Rivet_center1)
        print("Rivet_center2", Rivet_center2)
        print("Rivet_center3", Rivet_center3)
        '''

    root.after(10, read_frame)


def RivetDetect_cam1(frame):
    global Start_Rivet_flag_cam1, judge1
    global accum_cam1, count_fail_rivet_cam1, count_pass_rivet_cam1
    global check_make_folder, Rivet_num1, Rivet_tuple_cam1
    global Serial_No, check_result, Rivet_center1
    global frame_cam1, check_rivet_pass_cam1, check_rivet_fail_cam1
    global exception_box_cam1
    global box_width, box_height, cam1_box_idx, cam1_rect_list, Start_except_box_cam1
    global cam1_except_list, cam1_box_width, cam1_box_height, cam1_box_list
    global PLC_sensor, check_cam1_judge, folder_name, check_detect

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

    _, gray1 = cv2.threshold(gray_frame, 255, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 255, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 255, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 255, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 255, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 255, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 255, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 255, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)

    _, gray_ = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY)
    _, blue_ = cv2.threshold(blue, 0, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 5, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 5, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 0, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 0, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 10, 255, cv2.THRESH_BINARY)
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
    final_mask = cv2.bitwise_and(final_mask, v_)
    # final_mask = cv2.bitwise_and(final_mask, H_)
    # final_mask = cv2.bitwise_and(final_mask, L_)
    # final_mask = cv2.bitwise_and(final_mask, S_)

    final_mask = cv2.dilate(final_mask, kernel, iterations=1)

    final_mask = cv2.erode(final_mask, kernel, iterations=1)
    final_mask = cv2.erode(final_mask, kernel, iterations=1)
    final_mask = cv2.erode(final_mask, kernel, iterations=1)

    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)


    #################### 리벳 중심좌표값 자동 저장용 ##########################

    num = 1
    judge1 = ''
    check_rivet_pass_cam1 = 0
    check_rivet_fail_cam1 = 0
    pixel_sum = 0

    #print("*" * 10)
    #print(Start_except_box_cam1)

    if Start_except_box_cam1 == 1:
        cam1_rect_list.append(cam1_box_idx)
        cam1_except_list.append([cam1_box_width, cam1_box_height])
        Start_except_box_cam1 = 0
        print("rect_list", cam1_rect_list)
        print(exception_box_cam1)
        print(cam1_box_list)

    if check_detect == False:
        for i in range(len(cam1_rect_list)):
            frame = cv2.rectangle(frame, (cam1_box_list[i][0] - int((cam1_except_list[i][0]) / 2),
                                          cam1_box_list[i][1] - int((cam1_except_list[i][1]) / 2)), \
                                  (cam1_box_list[i][0] + int((cam1_except_list[i][0]) / 2),
                                   cam1_box_list[i][1] + int((cam1_except_list[i][1]) / 2)), (255, 255, 0), 1)


        if Start_Rivet_flag_cam1 == 0:  # 시작할때 한번만 작동 플레그.
            #Rivet_tuple = Rivet_tuple_cam1
            Rivet_center1 = []
            cx_origin = 0
            cy_origin = 0

            _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
            if len(contours) != 0:
                for contour in contours:
                    if (cv2.contourArea(contour) > 30) and (cv2.contourArea(contour) < 500):  # **필요한 면적을 찾아 중심점 좌표를 저장
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
        #print(str(num) + " 저장된 리벳의 좌표:", Rivet_center1)  # 자동 저장된 중심점값 출력
        Rivet_num1 = len(Rivet_center1)  # 자동 저장된 리벳의 갯수값 저장.

        Rivet_tuple_cam1 = []
        for i in range(Rivet_num1):
            Rivet_tuple_cam1.append(tuple(Rivet_center1[i]))  # 자동 저장된 리벳 좌표값을 튜플로 변환후 리스트에 저장. -> (Circle 마크에 쓰기 위해)

        #cv2.imshow('init_location' + str(num) +'.jpg', frame)  # 이미지 확인용.
        #cv2.imwrite('init_location' + str(num) + '.jpg', frame)  # 처음 이미지 캡쳐후 저장.
        ##############################

        Start_Rivet_flag_cam1 = 1

        #############################################################################

        reverse = cv2.bitwise_not(final_mask)
        reverse_copy = reverse.copy()

            # ** 리벳을 검출할 위치에 원으로 좌표 표시.
        for i in range(Rivet_num1):
            reverse_copy = cv2.circle(reverse_copy, Rivet_tuple_cam1[i], 10, (0, 0, 0), -1)  # 가운데 점 픽셀값 확인용 (x,y)값으로 받음.
            #frame = cv2.circle(frame, Rivet_tuple_cam1[i], 3, (0, 255, 255), -1)  # 원본에도 색상이 있는 점 표시.

        # ** 한 픽셀당 Binary 값을 표시.
        # [y , x]의 픽셀값 입력받음.
        pixel_val_list = []

        #print("Rivet_num1 : ",Rivet_num1)
        # 리벳이 탐지유무에 따른 화면 출력.
        if Rivet_num1 != 0:
            for i in range(Rivet_num1):
                pixel_val1 = reverse[Rivet_center1[i][1], Rivet_center1[i][0]]  # 픽셀값 저장 (0, 255)
                if pixel_val1 == 0:  # 검출된곳은 1, 검출되지 않을곳은 0으로 변환.
                    pixel_val1 = 0
                    frame = cv2.circle(frame, Rivet_tuple_cam1[i], 3, (0, 0, 255), -1)
                    if Rivet_center1[i][0]>= 550:
                        cv2.putText(frame, '%d, %d' % (Rivet_center1[i][0], Rivet_center1[i][1]),(Rivet_center1[i][0]-55, Rivet_center1[i][1]-5), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                    else:
                        cv2.putText(frame, '%d, %d'%(Rivet_center1[i][0], Rivet_center1[i][1]), (Rivet_center1[i][0], Rivet_center1[i][1]-5), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                else:
                    frame = cv2.circle(frame, Rivet_tuple_cam1[i], 3, (0, 255, 0), -1)
                    pixel_val1 = 1

                pixel_val_list.append(pixel_val1)  # 변환된 값을 리스트에 추가
                pixel_sum = sum(pixel_val_list)  # 모든 픽셀의 합

            # print(pixel_val_list, pixel_sum)    # 픽셀값과 합계 출력
        #else:
            #cv2.putText(frame, "No data", (50, 300), font, 2, (255, 0, 0), 2, cv2.LINE_AA)


        # stopper로 부터 아스키코드 'a' 가 들어오면 화면 캡쳐 - 데이터 저장. 로그기록.
        if PLC_sensor == True:
            check_cam1_judge = 1
            frame_cam1 = frame
            #accum = accum + 1  # 누적 판독수 축적.
            print("===== cam1 판독중 =====")
            if pixel_sum == Rivet_num1:
                if Rivet_num1 == 0:
                    cv2.putText(frame_cam1, "No Data", (500, 50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
                else:
                    #cv2.imwrite(store_location + "%s/rivet/pass/%s.jpg" % (folder_name, Serial_No), frame)
                    count_pass_rivet_cam1 += 1
                    check_rivet_pass_cam1 = 1
                    cv2.putText(frame_cam1, "PASS", (550, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                #cv2.imwrite(store_location + "%s/rivet/fail/%s.jpg" % (folder_name, Serial_No), frame)
                count_fail_rivet_cam1 += 1
                check_rivet_fail_cam1 = 1
                cv2.putText(frame_cam1, "NG", (550, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

        #print("accum_cam1, count_pass_rivet_cam1, count_fail_rivet_cam1", accum_cam1, count_pass_rivet_cam1, count_fail_rivet_cam1)

    return frame

def RivetDetect_cam2(frame):
    global Start_Rivet_flag_cam2, judge2
    global accum_cam2, count_fail_rivet_cam2, count_pass_rivet_cam2
    global check_make_folder, Rivet_num2, Rivet_tuple_cam2
    global Serial_No, check_result, Rivet_center2
    global frame_cam2, check_rivet_pass_cam2, check_rivet_fail_cam2
    global exception_box_cam2
    global box_width, box_height, cam2_box_idx, cam2_rect_list, Start_except_box_cam2
    global cam2_except_list, cam2_box_width, cam2_box_height, cam2_box_list
    global PLC_sensor, check_cam2_judge, check_detect

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

    _, gray1 = cv2.threshold(gray_frame, 255, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 255, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 255, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 255, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 255, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 255, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 255, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 255, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)

    _, gray_ = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY)
    _, blue_ = cv2.threshold(blue, 0, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 5, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 5, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 0, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 0, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 10, 255, cv2.THRESH_BINARY)
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
    final_mask = cv2.bitwise_and(final_mask, v_)
    # final_mask = cv2.bitwise_and(final_mask, H_)
    # final_mask = cv2.bitwise_and(final_mask, L_)
    # final_mask = cv2.bitwise_and(final_mask, S_)

    final_mask = cv2.dilate(final_mask, kernel, iterations=1)

    final_mask = cv2.erode(final_mask, kernel, iterations=1)
    final_mask = cv2.erode(final_mask, kernel, iterations=1)
    final_mask = cv2.erode(final_mask, kernel, iterations=1)

    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    #################### 리벳 중심좌표값 자동 저장용 ##########################


    num = 2
    judge2 = ''
    check_rivet_pass_cam2 = 0
    check_rivet_fail_cam2 = 0
    pixel_sum = 0

    #print("*"*10)
    #print(Start_except_box_cam2)

    if Start_except_box_cam2 == 1:
        cam2_rect_list.append(cam2_box_idx)
        cam2_except_list.append([cam2_box_width, cam2_box_height])
        Start_except_box_cam2 = 0
        print("rect_list", cam2_rect_list)
        print(exception_box_cam2)
        print(cam2_box_list)

    if check_detect == False:
        for i in range(len(cam2_rect_list)):
            frame = cv2.rectangle(frame, ( cam2_box_list[i][0] - int( (cam2_except_list[i][0])/2 ), cam2_box_list[i][1] - int( (cam2_except_list[i][1]) /2) ), \
                                  (cam2_box_list[i][0] + int( (cam2_except_list[i][0]) /2), cam2_box_list[i][1] + int( (cam2_except_list[i][1]) /2)), (255, 255, 0), 1)


        if Start_Rivet_flag_cam2 == 0:  # 시작할때 한번만 작동 플레그.
            #Rivet_tuple = Rivet_tuple_cam2
            Rivet_center2 = []
            cx_origin = 0
            cy_origin = 0

            _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
            if len(contours) != 0:
                for contour in contours:
                    if (cv2.contourArea(contour) > 30) and (cv2.contourArea(contour) < 500):  # **필요한 면적을 찾아 중심점 좌표를 저장
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
        #print(str(num) + " 저장된 리벳의 좌표:", Rivet_center2)  # 자동 저장된 중심점값 출력
        Rivet_num2 = len(Rivet_center2)  # 자동 저장된 리벳의 갯수값 저장.

        Rivet_tuple_cam2 = []
        for i in range(Rivet_num2):
            Rivet_tuple_cam2.append(tuple(Rivet_center2[i]))  # 자동 저장된 리벳 좌표값을 튜플로 변환후 리스트에 저장. -> (Circle 마크에 쓰기 위해)

        #cv2.imshow('init_location' + str(num) +'.jpg', frame)  # 이미지 확인용.
        #cv2.imwrite('init_location' + str(num) + '.jpg', frame)  # 처음 이미지 캡쳐후 저장.
        ##############################

        Start_Rivet_flag_cam2 = 1

        #############################################################################

        reverse = cv2.bitwise_not(final_mask)
        reverse_copy = reverse.copy()

            # ** 리벳을 검출할 위치에 원으로 좌표 표시.
        for i in range(Rivet_num2):
            reverse_copy = cv2.circle(reverse_copy, Rivet_tuple_cam2[i], 10, (0, 0, 0), -1)  # 가운데 점 픽셀값 확인용 (x,y)값으로 받음.
            #frame = cv2.circle(frame, Rivet_tuple_cam2[i], 3, (0, 255, 255), -1)  # 원본에도 색상이 있는 점 표시.

        # ** 한 픽셀당 Binary 값을 표시.
        # [y , x]의 픽셀값 입력받음.
        pixel_val_list = []

        #print("Rivet_num2 : ",Rivet_num2)
        # 리벳이 탐지유무에 따른 화면 출력.
        if Rivet_num2 != 0:
            for i in range(Rivet_num2):
                pixel_val2 = reverse[Rivet_center2[i][1], Rivet_center2[i][0]]  # 픽셀값 저장 (0, 255)
                if pixel_val2 == 0:  # 검출된곳은 1, 검출되지 않을곳은 0으로 변환.
                    pixel_val2 = 0
                    frame = cv2.circle(frame, Rivet_tuple_cam2[i], 3, (0, 0, 255), -1)
                    if Rivet_center2[i][0]>= 550:
                        cv2.putText(frame, '%d, %d' % (Rivet_center2[i][0], Rivet_center2[i][1]),(Rivet_center2[i][0]-55, Rivet_center2[i][1]-5), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                    else:
                        cv2.putText(frame, '%d, %d'%(Rivet_center2[i][0], Rivet_center2[i][1]), (Rivet_center2[i][0], Rivet_center2[i][1]-5), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                else:
                    frame = cv2.circle(frame, Rivet_tuple_cam2[i], 3, (0, 255, 0), -1)
                    pixel_val2 = 1

                pixel_val_list.append(pixel_val2)  # 변환된 값을 리스트에 추가
                pixel_sum = sum(pixel_val_list)  # 모든 픽셀의 합

            # print(pixel_val_list, pixel_sum)    # 픽셀값과 합계 출력
        #else:
        #    cv2.putText(frame, "No data", (50, 300), font, 2, (255, 0, 0), 2, cv2.LINE_AA)


        # stopper로 부터 아스키코드 'a' 가 들어오면 화면 캡쳐 - 데이터 저장. 로그기록.
        if PLC_sensor == True:
            check_cam2_judge = 1

            #accum = accum + 1  # 누적 판독수 축적.

            frame_cam2 = frame
            print("===== cam2 판독중 =====")
            if pixel_sum == Rivet_num2:
                if Rivet_num2 == 0:
                    cv2.putText(frame_cam2, "No Data", (500, 50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
                else:
                #cv2.imwrite(store_location + "%s/rivet/pass/%s.jpg" % (folder_name, Serial_No), frame)
                    count_pass_rivet_cam2 += 1
                    check_rivet_pass_cam2 = 1
                    cv2.putText(frame_cam2, "PASS", (550, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                #cv2.imwrite(store_location + "%s/rivet/fail/%s.jpg" % (folder_name, Serial_No), frame)
                count_fail_rivet_cam2 += 1
                check_rivet_fail_cam2 = 1
                cv2.putText(frame_cam2, "NG", (550, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

            accum_cam2 = count_pass_rivet_cam2 + count_fail_rivet_cam2
            #leave_log(num)  # 판독값을 로그로 남김.

        #print("accum_cam2, count_pass_rivet_cam2, count_fail_rivet_cam2", accum_cam2, count_pass_rivet_cam2, count_fail_rivet_cam2)
    return frame

def RivetDetect_cam3(frame):
    global Start_Rivet_flag_cam3, judge3
    global accum_cam3, count_fail_rivet_cam3, count_pass_rivet_cam3
    global check_make_folder, Rivet_num3, Rivet_tuple_cam3
    global Serial_No, check_result, Rivet_center3
    global frame_cam3, check_rivet_pass_cam3, check_rivet_fail_cam3
    global exception_box_cam3
    global box_width, box_height, cam3_box_idx, cam3_rect_list, Start_except_box_cam3
    global cam3_except_list, cam3_box_width, cam3_box_height, cam3_box_list
    global PLC_sensor, check_cam3_judge, check_detect

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

    _, gray1 = cv2.threshold(gray_frame, 255, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 255, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 255, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 255, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 255, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 255, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 255, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 255, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)

    _, gray_ = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY)
    _, blue_ = cv2.threshold(blue, 0, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 5, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 5, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 0, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 0, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 10, 255, cv2.THRESH_BINARY)
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
    final_mask = cv2.bitwise_and(final_mask, v_)
    # final_mask = cv2.bitwise_and(final_mask, H_)
    # final_mask = cv2.bitwise_and(final_mask, L_)
    # final_mask = cv2.bitwise_and(final_mask, S_)

    final_mask = cv2.dilate(final_mask, kernel, iterations=1)

    final_mask = cv2.erode(final_mask, kernel, iterations=1)
    final_mask = cv2.erode(final_mask, kernel, iterations=1)
    final_mask = cv2.erode(final_mask, kernel, iterations=1)

    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    #################### 리벳 중심좌표값 자동 저장용 ##########################

    num = 3
    judge3 = ''
    check_rivet_pass_cam3 = 0
    check_rivet_fail_cam3 = 0
    pixel_sum = 0

    #print("*"*10)
    #print(Start_except_box_cam3)

    if Start_except_box_cam3 == 1:
        cam3_rect_list.append(cam3_box_idx)
        cam3_except_list.append([cam3_box_width, cam3_box_height])
        Start_except_box_cam3 = 0
        print("rect_list", cam3_rect_list)
        print(exception_box_cam3)
        print(cam3_box_list)

    if check_detect == False:
        for i in range(len(cam3_rect_list)):
            frame = cv2.rectangle(frame, ( cam3_box_list[i][0] - int( (cam3_except_list[i][0])/2 ), cam3_box_list[i][1] - int( (cam3_except_list[i][1]) /2) ), \
                                  (cam3_box_list[i][0] + int( (cam3_except_list[i][0]) /2), cam3_box_list[i][1] + int( (cam3_except_list[i][1]) /2)), (255, 255, 0), 1)


        if Start_Rivet_flag_cam3 == 0:  # 시작할때 한번만 작동 플레그.
            #Rivet_tuple = Rivet_tuple_cam3

            Rivet_center3 = []
            cx_origin = 0
            cy_origin = 0

            _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
            if len(contours) != 0:
                for contour in contours:
                    if (cv2.contourArea(contour) > 30) and (cv2.contourArea(contour) < 500):  # **필요한 면적을 찾아 중심점 좌표를 저장
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
        #print(str(num) + " 저장된 리벳의 좌표:", Rivet_center3)  # 자동 저장된 중심점값 출력
        Rivet_num3 = len(Rivet_center3)  # 자동 저장된 리벳의 갯수값 저장.

        Rivet_tuple_cam3 = []
        for i in range(Rivet_num3):
            Rivet_tuple_cam3.append(tuple(Rivet_center3[i]))  # 자동 저장된 리벳 좌표값을 튜플로 변환후 리스트에 저장. -> (Circle 마크에 쓰기 위해)

        #cv2.imshow('init_location' + str(num) +'.jpg', frame)  # 이미지 확인용.
        #cv2.imwrite('init_location' + str(num) + '.jpg', frame)  # 처음 이미지 캡쳐후 저장.
        ##############################

        Start_Rivet_flag_cam3 = 1

        #############################################################################

        reverse = cv2.bitwise_not(final_mask)
        reverse_copy = reverse.copy()

            # ** 리벳을 검출할 위치에 원으로 좌표 표시.
        for i in range(Rivet_num3):
            reverse_copy = cv2.circle(reverse_copy, Rivet_tuple_cam3[i], 10, (0, 0, 0), -1)  # 가운데 점 픽셀값 확인용 (x,y)값으로 받음.
            #frame = cv2.circle(frame, Rivet_tuple_cam3[i], 3, (0, 255, 255), -1)  # 원본에도 색상이 있는 점 표시.

        # ** 한 픽셀당 Binary 값을 표시.
        # [y , x]의 픽셀값 입력받음.
        pixel_val_list = []

        #print("Rivet_num3 : ",Rivet_num1)
        # 리벳이 탐지유무에 따른 화면 출력.
        if Rivet_num3 != 0:
            for i in range(Rivet_num3):
                pixel_val3 = reverse[Rivet_center3[i][1], Rivet_center3[i][0]]  # 픽셀값 저장 (0, 255)
                if pixel_val3 == 0:  # 검출된곳은 1, 검출되지 않을곳은 0으로 변환.
                    pixel_val3 = 0
                    frame = cv2.circle(frame, Rivet_tuple_cam3[i], 3, (0, 0, 255), -1)  # 원본에도 색상이 있는 점 표시.
                    if Rivet_center3[i][0]>= 550:
                        cv2.putText(frame, '%d, %d' % (Rivet_center3[i][0], Rivet_center3[i][1]),(Rivet_center3[i][0]-55, Rivet_center3[i][1]-5), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                    else:
                        cv2.putText(frame, '%d, %d'%(Rivet_center3[i][0], Rivet_center3[i][1]), (Rivet_center3[i][0], Rivet_center3[i][1]-5), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                else:
                    frame = cv2.circle(frame, Rivet_tuple_cam3[i], 3, (0, 255, 0), -1)  # 원본에도 색상이 있는 점 표시.
                    pixel_val3 = 1

                pixel_val_list.append(pixel_val3)  # 변환된 값을 리스트에 추가
                pixel_sum = sum(pixel_val_list)  # 모든 픽셀의 합



        # PLC로 부터 신호를 받으면 판독 시작
        if PLC_sensor == True:
            check_cam3_judge = 1

            frame_cam3 = frame
            print("===== cam3 판독중 =====")
            if pixel_sum == Rivet_num3:
                if Rivet_num3 == 0:
                    cv2.putText(frame_cam3, "No Data", (500, 50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
                else:
                    count_pass_rivet_cam3 += 1
                    check_rivet_pass_cam3 = 1
                    cv2.putText(frame_cam3, "PASS", (550, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                count_fail_rivet_cam3 += 1
                check_rivet_fail_cam3 = 1
                cv2.putText(frame_cam3, "NG", (550, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

    return frame

def add_exception_area_cam1():
    global exception_box_cam1
    global EB1_X, EB1_Y, EB1_W, EB1_H, EB2_X, EB2_Y, EB2_W, EB2_H, EB3_X, EB3_Y, EB3_W, EB3_H
    global Rivet_center1, Rivet_num1
    global Start_Rivet_flag_cam1
    global cam1_box_width, cam1_box_height
    global cam1_box_idx, Start_except_box_cam1
    global rivet_center_flag1, save_revet_center1
    global cam1_box_list

    try:
        x = eval(EB1_X.get())
        y = eval(EB1_Y.get())
        cam1_box_width = eval(EB1_W.get())
        cam1_box_height = eval(EB1_H.get())
        exception_box_cam1.append([x, y])
        EB1_X.delete(0, END)
        EB1_Y.delete(0, END)
        EB2_X.delete(0, END)
        EB2_Y.delete(0, END)
        EB3_X.delete(0, END)
        EB3_Y.delete(0, END)
        EB1_W.delete(0, END)
        EB1_H.delete(0, END)

        Start_except_box_cam1 = 1

        if(rivet_center_flag1 == 0):
            rivet_center_flag1 = 1
            save_revet_center1 = Rivet_center1

        list_delete_item = []
        for i in range(len(exception_box_cam1)):
            for j in range(len(Rivet_center1)):
                if ((exception_box_cam1[i][0] - cam1_box_width) <= Rivet_center1[j][0]) and (
                        Rivet_center1[j][0] <= (exception_box_cam1[i][0] + cam1_box_width)) and (
                        (exception_box_cam1[i][1] - cam1_box_height) <= Rivet_center1[j][1]) and (
                        Rivet_center1[j][1] <= (exception_box_cam1[i][1] + cam1_box_height)):
                    list_delete_item.append([Rivet_center1[j][0], Rivet_center1[j][1]])

        list_delete_item = list(unique_everseen(list_delete_item))
        cam1_box_idx = save_revet_center1.index([list_delete_item[0][0], list_delete_item[0][1]])

        print("delte item", list_delete_item)
        cam1_box_list.append(list_delete_item[0])
        for i in range(len(list_delete_item)):
            Rivet_center1.remove([list_delete_item[i][0], list_delete_item[i][1]])

        print(Rivet_center3)

    except IndexError:
        Start_except_box_cam1 = 0


def add_exception_area_cam2():
    global exception_box_cam2
    global EB1_X, EB1_Y, EB1_W, EB1_H, EB2_X, EB2_Y, EB2_W, EB2_H, EB3_X, EB3_Y, EB3_W, EB3_H
    global Rivet_center2, Rivet_num2
    global Start_Rivet_flag_cam2
    global cam2_box_width, cam2_box_height
    global cam2_box_idx, Start_except_box_cam2
    global rivet_center_flag2, save_revet_center2
    global cam2_box_list

    try:
        x = eval(EB2_X.get())
        y = eval(EB2_Y.get())
        cam2_box_width = eval(EB2_W.get())
        cam2_box_height = eval(EB2_H.get())
        exception_box_cam2.append([x, y])
        EB1_X.delete(0, END)
        EB1_Y.delete(0, END)
        EB2_X.delete(0, END)
        EB2_Y.delete(0, END)
        EB3_X.delete(0, END)
        EB3_Y.delete(0, END)
        EB2_W.delete(0, END)
        EB2_H.delete(0, END)

        Start_except_box_cam2 = 1

        if (rivet_center_flag2 == 0):
            rivet_center_flag2 = 1
            save_revet_center2 = Rivet_center2

        list_delete_item = []
        for i in range(len(exception_box_cam2)):
            for j in range(len(Rivet_center2)):
                if ((exception_box_cam2[i][0] - cam2_box_width) <= Rivet_center2[j][0]) and (
                        Rivet_center2[j][0] <= (exception_box_cam2[i][0] + cam2_box_width)) and (
                        (exception_box_cam2[i][1] - cam2_box_height) <= Rivet_center2[j][1]) and (
                        Rivet_center2[j][1] <= (exception_box_cam2[i][1] + cam2_box_height)):
                    list_delete_item.append([Rivet_center2[j][0], Rivet_center2[j][1]])

        list_delete_item = list(unique_everseen(list_delete_item))
        cam2_box_idx = save_revet_center2.index([list_delete_item[0][0], list_delete_item[0][1]])

        print("delte item", list_delete_item)
        cam2_box_list.append(list_delete_item[0])
        for i in range(len(list_delete_item)):
            Rivet_center2.remove([list_delete_item[i][0], list_delete_item[i][1]])

        print(Rivet_center2)

    except IndexError:
        Start_except_box_cam2 = 0

def add_exception_area_cam3():
    global exception_box_cam3
    global EB1_X, EB1_Y, EB1_W, EB1_H, EB2_X, EB2_Y, EB2_W, EB2_H, EB3_X, EB3_Y, EB3_W, EB3_H
    global Rivet_center3, Rivet_num3
    global Start_Rivet_flag_cam3
    global cam3_box_width, cam3_box_height
    global cam3_box_idx, Start_except_box_cam3
    global rivet_center_flag3, save_revet_center3
    global cam3_box_list

    try:
        x = eval(EB3_X.get())
        y = eval(EB3_Y.get())
        cam3_box_width = eval(EB3_W.get())
        cam3_box_height = eval(EB3_H.get())
        exception_box_cam3.append([x, y])
        EB1_X.delete(0, END)
        EB1_Y.delete(0, END)
        EB2_X.delete(0, END)
        EB2_Y.delete(0, END)
        EB3_X.delete(0, END)
        EB3_Y.delete(0, END)
        EB3_W.delete(0, END)
        EB3_H.delete(0, END)

        Start_except_box_cam3 = 1

        if(rivet_center_flag3 == 0):
            rivet_center_flag3 = 1
            save_revet_center3 = Rivet_center3

        list_delete_item = []
        for i in range(len(exception_box_cam3)):
            for j in range(len(Rivet_center3)):
                if ((exception_box_cam3[i][0] - cam3_box_width) <= Rivet_center3[j][0]) and (
                        Rivet_center3[j][0] <= (exception_box_cam3[i][0] + cam3_box_width)) and (
                        (exception_box_cam3[i][1] - cam3_box_height) <= Rivet_center3[j][1]) and (
                        Rivet_center3[j][1] <= (exception_box_cam3[i][1] + cam3_box_height)):
                    list_delete_item.append([Rivet_center3[j][0], Rivet_center3[j][1]])
                    #cam3_box_idx = i

        list_delete_item = list(unique_everseen(list_delete_item))
        cam3_box_idx = save_revet_center3.index([list_delete_item[0][0], list_delete_item[0][1]])

        print("delte item", list_delete_item)
        cam3_box_list.append(list_delete_item[0])
        for i in range(len(list_delete_item)):
            Rivet_center3.remove([list_delete_item[i][0], list_delete_item[i][1]])

        print(Rivet_center3)

    except IndexError:
        Start_except_box_cam3 = 0


def start_detect():
    global check_detect

    check_detect = False


def PLC_sensor():
    global PLC_sensor, check_set

    if check_set == False:
        PLC_sensor = True

def check_setting():
    global check_set, store_location, pathname, set

    check_set = False
    store_location_input = datapath.get()
    set.destroy()

    if store_location_input != '':
        parsing = store_location_input.split('/')
        print(parsing)
        for i in range(len(parsing)):
            if parsing[i] != '':
                pathname += parsing[i] + '/'
                print(pathname)
            elif parsing[i] == '/':
                break
            if i != 0:
                make_folder(pathname)

        store_location = pathname

    PLC_signal_window()


def PLC_signal_window():
    ### 가상 PLC 신호창

    PLC = Toplevel(root)
    PLC.geometry("400x300")
    PLC.title("Setting Window")
    PLC.configure(bg="#ebebeb")

    Label(PLC, text="PLC 신호 전송", font="돋움체", bg="#ebebeb", bd=2, width=25, height=2, relief="groove",
          anchor=CENTER).place(x=0, y=0)
    Button(PLC, text="PLC 신호 전송", font="돋움체", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=20, height=10, bd=3, padx=2, pady=2, command=PLC_sensor).place(x=10, y=50)


def setting_window():
    global datapath, set
    global EB1_X, EB1_Y, EB1_W, EB1_H, EB2_X, EB2_Y, EB2_W, EB2_H, EB3_X, EB3_Y, EB3_W, EB3_H
    ### 설정창

    set = Toplevel(root)
    set.geometry("1000x600")
    set.title("Setting Window")
    set.configure(bg="#ebebeb")
    qr_width, qr_height = 1920, 1080

    Label(set, text="예외지역 설정", font="돋움체", bg="#ebebeb", bd=2, width=25, height=2, relief="groove", anchor=CENTER).place(x=0, y=0)
    Label(set, text="데이터 저장 경로 설정", font="돋움체", bg="#ebebeb", bd=2, width=25, height=2, relief="groove", anchor=CENTER).place(x=0, y=440)

    datapath = Entry(set, width=35, relief="groove", font="Helvetica 35 bold")
    datapath.place(x=0, y=490 , relx=0.001, rely=0)

    Button(set, text="설정 완료", font="Helvetica 13 bold", relief="groove", overrelief="solid", bg="#ebebeb", \
           bd=3, padx=2, pady=2, command=check_setting).pack(side=BOTTOM, fill=X)

    Button(set, text="리벳 감지 \n시작버튼", font="돋움체", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=15, height=3, bd=3, padx=2, pady=2, command=start_detect).place(x=660, y=390)

    CAM_name_list = ["CAM1", "CAM2", "CAM3"]
    for i in range(3):
        Label(set, text=CAM_name_list[i], height=2, width=15, fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 13 bold").place(x=60 + (i * 260), y=65, relx=0.01,rely=0.01)

    excpet_item_list = ["X", "Y", "W", "H"]
    for i in range(4):
        Label(set, text=excpet_item_list[i], height=4, width=5, fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 8 bold").place(x=5, y=(qr_height / 8) + (i*61) , relx=0.01, rely=0.01)
    for i in range(4):
        Label(set, text=excpet_item_list[i], height=4, width=5, fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 8 bold").place(x=265, y=(qr_height / 8) + (i*61) , relx=0.01, rely=0.01)
    for i in range(4):
        Label(set, text=excpet_item_list[i], height=4, width=5, fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 8 bold").place(x=525, y=(qr_height / 8) + (i*61) , relx=0.01, rely=0.01)

    ###예외 지역 설정 엔트리
    ##CAM1
    EB1_X = Entry(set, width=5, relief="groove", font="Helvetica 35 bold")
    EB1_X.place(x=45, y=(qr_height / 8) + 0 , relx=0.01, rely=0.01)

    EB1_Y = Entry(set, width=5, relief="groove", font="Helvetica 35 bold")
    EB1_Y.place(x=45, y=(qr_height / 8) + 61 , relx=0.01, rely=0.01)

    EB1_W = Entry(set, width=5, relief="groove", font="Helvetica 35 bold")
    EB1_W.place(x=45, y=(qr_height / 8) + 122 , relx=0.01, rely=0.01)

    EB1_H = Entry(set, width=5, relief="groove", font="Helvetica 35 bold")
    EB1_H.place(x=45, y=(qr_height / 8) + 183 , relx=0.01, rely=0.01)


    ##CAM2
    EB2_X = Entry(set, width=5, relief="groove", font="Helvetica 35 bold")
    EB2_X.place(x=305, y=(qr_height / 8) + 0 , relx=0.01, rely=0.01)

    EB2_Y = Entry(set, width=5, relief="groove", font="Helvetica 35 bold")
    EB2_Y.place(x=305, y=(qr_height / 8) + 61 , relx=0.01, rely=0.01)

    EB2_W = Entry(set, width=5, relief="groove", font="Helvetica 35 bold")
    EB2_W.place(x=305, y=(qr_height / 8) + 122 , relx=0.01, rely=0.01)

    EB2_H = Entry(set, width=5, relief="groove", font="Helvetica 35 bold")
    EB2_H.place(x=305, y=(qr_height / 8) + 183 , relx=0.01, rely=0.01)

    ##CAM3
    EB3_X = Entry(set, width=5, relief="groove", font="Helvetica 35 bold")
    EB3_X.place(x=565, y=(qr_height / 8) + 0 , relx=0.01, rely=0.01)

    EB3_Y = Entry(set, width=5, relief="groove", font="Helvetica 35 bold")
    EB3_Y.place(x=565, y=(qr_height / 8) + 61 , relx=0.01, rely=0.01)

    EB3_W = Entry(set, width=5, relief="groove", font="Helvetica 35 bold")
    EB3_W.place(x=565, y=(qr_height / 8) + 122 , relx=0.01, rely=0.01)

    EB3_H = Entry(set, width=5, relief="groove", font="Helvetica 35 bold")
    EB3_H.place(x=565, y=(qr_height / 8) + 183 , relx=0.01, rely=0.01)

    text_list = ["CAM1 \nAdd", "CAM2 \nAdd", "CAM3 \nAdd"]
    command_list = [add_exception_area_cam1, add_exception_area_cam2, add_exception_area_cam3]
    for i in range(3):
        Button(set, text=text_list[i], font="돋움체", relief="raised", overrelief="solid", bg="#ebebeb", \
               width=5, height=9, bd=3, padx=2, pady=2, command=command_list[i]).place(x=190 + (i * 262), y=140)


def mouse_position(event):
    global EB1_X, EB1_Y, EB1_W, EB1_H, EB2_X, EB2_Y, EB2_W, EB2_H, EB3_X, EB3_Y, EB3_W, EB3_H

    print("===== 마우스 포지션 출력 =====")
    print("click - ", event.x, event.y)

    EB1_X.insert(20, event.x)
    EB1_Y.insert(20, event.y)

    EB2_X.insert(20, event.x)
    EB2_Y.insert(20, event.y)

    EB3_X.insert(20, event.x)
    EB3_Y.insert(20, event.y)


def execute():
    global cam1_label, cam2_label, cam3_label, cam4_label, image_label, root
    global RV_SN, RV_P1, RV_P2, RV_P3, RV_P4, RV_P5, set, datapath


    root = Tk()

    root.bind('<Escape>', lambda e: root.quit())
    root.bind("<Double-Button-1>", mouse_position)
    #root.bind("<Motion>", mouse_position)
    cam1_label = Label(root)
    cam1_label.place(y=10, anchor=NW)

    cam2_label = Label(root)
    cam2_label.place(x=640, y=10)

    cam3_label = Label(root)
    cam3_label.place(x=1280, y=10)

    cam4_label = Label(root)
    cam4_label.place(x = 1155, y = 780)

    image_label = Label(root)
    image_label.place(x=1138, y=(1080 / 3) + 205)

    #width, height = 640, 480

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

    Label(root, text="전체 이미지\nFull Image\n(reduced)", height=10, width=13, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=970, y=(qr_height / 3) + 195 + (0 * 80), relx=0.01, rely=0.01)
    Label(root, text="바코드 카메라\nBarcode CAM", height=12, width=13, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=970, y=(qr_height / 3) + 390 + (0 * 80), relx=0.01, rely=0.01)
    Label(root, text="결과\nResult", height=12, width=13, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=1420, y=(qr_height / 3) + 390 + (0 * 80), relx=0.01, rely=0.01)

    CAM_name_list = ["CAM1", "CAM2", "CAM3"]
    for i in range(3):
        Label(root, text=CAM_name_list[i], height=2, width=15, fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 13 bold").place(x=1160 + (i*260), y=(qr_height / 3) + 140 + (0 * 80), relx=0.01, rely=0.01)


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

    setting_window()

    read_frame()
    root.mainloop()


if __name__=="__main__":
    execute()
    cap1.release()
    cap2.release()
    cap3.release()
    cv2.destroyAllWindows()

