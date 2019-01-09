# import the necessary packages
# -*- coding: utf-8 -*-
import numpy as np                          # pip install numpy
import imutils                              # pip install imutils
import cv2                                  # pip install python-opencv
from more_itertools import unique_everseen  # pip install more_itertools
from PIL import Image as Img                # pip install PIL
#import pyzbar.pyzbar as pyzbar              # pip install pyzbar
from pylibdmtx.pylibdmtx import decode
from PIL import ImageTk
from math import *
import datetime
import time
import os
from tkinter import *


#카메라 구동 설정
width, height = 640, 480
cap0 = cv2.VideoCapture(1)
cap0.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap1 = cv2.VideoCapture(2)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap2 = cv2.VideoCapture(0)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# 데이터를 저장할 위치(서버저장)
store_location = "C:/Data_Record_QR/"

#전역 변수
check_year = 0
check_month = 0
check_day = 0
check_make_log_folder = 0
check_serial_no = 0

qr_check_make_folder = 0
ss_check_make_folder = 0
qr_check_result = 2
ss_check_result = 2
qr_check_process = 0
ss_check_process = 0

count_pass_barcode = 0
count_fail_barcode = 0
accumulation = 0

count_pass_sticker = 0
count_fail_sticker = 0
volume = 0

pre_accumulation = 1000
pre_volume = 1000
qr_value_list = ['', " ", " ", " ", " ", " "]
ss_value_list = ['', " ", " ", " ", " ", " "]
#qr_value_list[0] = NONE
#ss_value_list[0] = NONE
Serial_No = ''

PLC_signal = False
check_set = True
box_set = False
count_mouse = 0

qr_x1 = 0
qr_y1 = 0
qr_x2 = 0
qr_y2 = 0

pathname = ''


#def decode(image) :
#    pass

def webCamShow_QR(N, Display):
    global Serial_N
    _, frame = N
    frame = QRDetect(frame)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cv2image = Img.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=cv2image)
    Display.imgtk = imgtk
    Display.configure(image=imgtk)

def webCamShow_SS(N, Display):
    global Serial_N
    _, frame = N
    frame = SSDetect(frame)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cv2image = Img.fromarray(cv2image)
    imgtk =ImageTk.PhotoImage(image=cv2image)
    Display.imgtk = imgtk
    Display.configure(image=imgtk)

def read_frame():
    global qr_label, sticker_label, Serial_No, check_serial_no, box_label
    global qr_check_result, ss_check_result, qr_check_process, ss_check_process
    global box_set

    print("======== read =========")
    print("Serial_No : ", Serial_No)
    print("len : ", len(SS_SN.get()), len(QR_SN.get()))
    print("process : ", ss_check_process, qr_check_process)

    if (qr_check_process == 0 and ss_check_process == 0) and len(SS_SN.get()) != 0:
        Serial_No = SS_SN.get()
    elif (qr_check_process == 0 and ss_check_process == 0) and len(QR_SN.get()) != 0:
        Serial_No = QR_SN.get()
    elif (qr_check_process == 1 or ss_check_process == 1):
        print("판독 중")

    if Serial_No == 0 or Serial_No == '':
        print("시리얼 입력 대기 중")
        Serial_No = ''

    if qr_check_process == 1 and ss_check_process == 1:
        Serial_No = ''
        ss_check_process = 0
        qr_check_process = 0
        print(Serial_No, qr_check_process, qr_check_process)

    webCamShow_QR(cap1.read(), qr_label)
    webCamShow_SS(cap0.read(), sticker_label)


    if box_set == True:
        image = qr_image()
        image_reformat = Reformat_Image(image)
        imageShow(image_reformat, box_label)
        box_set = False

    root.after(10, read_frame)


def qr_image():
    global frame_cp
    global qr_x1, qr_x2, qr_y1, qr_y2

    return frame_cp[(qr_y1):(qr_y2), (qr_x1):(qr_x2)]


def get_today():
    global Serial_No
    now = time.localtime()
    local_time = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    return local_time

def make_folder(folder_name):
    global Serial_N
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

def check_time_value():
    global Serial_N
    time = datetime.datetime.now()
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    minute = time.minute
    sec = time.second
    return year, month, day, hour, minute, sec

def leave_log(check_function):
    global check_year, check_month, check_day, f
    global count_pass_barcode, count_fail_barcode, accumulation
    global count_pass_sticker, count_fail_sticker, volume
    global today, Serial_No, check_make_log_folder

    year, month, day, hour, minute, sec = check_time_value()

    filename = str(year) + str("%02d" % month) + str("%02d" % day)
    if (year != check_year and month != check_month and day != check_day) or check_make_log_folder != 2:
        print("새로운 로그 파일 생성")
        check_make_log_folder +=1
        if check_function ==0:
            today = get_today()
            foldername_log = store_location + today + "/barcode" + "/log"
            make_folder(foldername_log)
            f = open(store_location + today + "/barcode/log/log_%s.txt" % filename, 'w')
            data = "시리얼 넘버  //  판독 시간  //  누적 판독량  //  정상  //  불량  \n"
        else:
            today = get_today()
            foldername_log = store_location + today + "/sticker" + "/log"
            make_folder(foldername_log)
            f = open(store_location + today + "/sticker/log/log_%s.txt" % filename, 'w')
            data = "시리얼 넘버  //  판독 시간  //  누적 판독량  //  정상  //  불량  \n"

        f.write(data)

        check_year = datetime.datetime.now().year
        check_month = datetime.datetime.now().month
        check_day = datetime.datetime.now().day

    if check_function == 0:
        f = open(store_location + today + "/barcode/log/log_%s.txt" % filename, 'a')
        localtime = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + " " + str("%02d" % hour) + ":" + str(
            "%02d" % minute) + ":" + str("%02d" % sec)
        data = str(Serial_No) + " // " + str(localtime) + " // " + str("%04d" % accumulation) + " // " + str(
            "%04d" % count_pass_barcode) + \
               " // " + str("%04d" % count_fail_barcode) + "\n"
    else :
        f = open(store_location + today + "/sticker/log/log_%s.txt" % filename, 'a')
        time = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + " " + str("%02d" % hour) + ":" + str(
            "%02d" % minute) + ":" + str("%02d" % sec)
        data = str(Serial_No) + " // " + str(time) + " // " + str("%04d" % volume) + " // " + str(
            "%04d" % count_pass_sticker) + " // " + str("%04d" % count_fail_sticker) + "\n"

    f.write(data)
    f.close()

def imageShow(N, Display):
    frame = N
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2image = Img.fromarray(cv2image)
    imgtk =ImageTk.PhotoImage(image=cv2image)
    Display.imgtk = imgtk
    Display.configure(image=imgtk)




def Reformat_Image(image):
    height, width = image.shape[:2]
    print(width, height)
    width = int(width*1.2)
    height = int(height*1.2)
    if height == 0:
        height = width
    res = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    return res

def QRDetect(frame):
    global pre_accumulation, qr_check_make_folder
    global count_pass_barcode, count_fail_barcode, accumulation
    global Serial_No, QR_SN
    global qr_cx, qr_cy, qr_check_result
    global qr_check_process, ss_check_process
    global qr_x1, qr_y1, qr_x2, qr_y2
    global frame_cp, PLC_signal
    global point_x1, point_x2, point_y1, point_y2

    '''
    qr_x1 = 141
    qr_y1 = 236
    qr_x2 = 254
    qr_y2 = 348
    '''

    frame = cv2.flip(frame, 0)
    frame = cv2.flip(frame, 1)

    frame2 = frame.copy()
    frame3 = frame.copy()

    frame4 = frame.copy()
    frame_cp = frame.copy()
    cv2.rectangle(frame3, (qr_x1, qr_y1), (qr_x2, qr_y2), (255, 0, 0), 3)
    cx_ref = int(abs(qr_x1 + qr_x2) / 2)
    cy_ref = int(abs(qr_y1 + qr_y2) / 2)
    qr_area = abs(qr_x2 - qr_x1) * abs(qr_y2 - qr_y1)
    cv2.circle(frame3, (cx_ref, cy_ref), 3, (255, 0, 0), -1)

    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blue, green, red = cv2.split(frame)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(frame_hsv)
    frame_hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    H, L, S = cv2.split(frame_hls)

    _, gray1 = cv2.threshold(gray_frame, 105, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 164, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 138, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 87, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 255, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 187, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 156, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 209, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 188, 255, cv2.THRESH_BINARY_INV)

    _, gray_ = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY)
    _, blue_ = cv2.threshold(blue, 0, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 0, 255, cv2.THRESH_BINARY)
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
    #     final_mask = cv2.bitwise_and(final_mask, L1)
    #     final_mask = cv2.bitwise_and(final_mask, S1)
    #
    #     final_mask = cv2.bitwise_and(final_mask, gray_)
    #     final_mask = cv2.bitwise_and(final_mask, blue_)
    #     final_mask = cv2.bitwise_and(final_mask, green_)
    #     final_mask = cv2.bitwise_and(final_mask, red_)
    #     # final_mask = cv2.bitwise_and(final_mask, h_)
    #     # final_mask = cv2.bitwise_and(final_mask, s_)
    #     final_mask = cv2.bitwise_and(final_mask, v_)
    #     # final_mask = cv2.bitwise_and(final_mask, H_)
    # final_mask = cv2.bitwise_and(final_mask, L_)
    # final_mask = cv2.bitwise_and(final_mask, S_)
    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    blurred = cv2.blur(final_mask, (4, 4))
    (_, thresh) = cv2.threshold(blurred, 134, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (33, 26))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    closed = cv2.erode(closed, None, iterations=10)
    closed = cv2.dilate(closed, None, iterations=10)

    cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if (len(cnts) != 0):
        c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        M = cv2.moments(c)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
        box = np.int0(box)

        # cv2.drawContours(frame2, [box], -1, (0, 255, 0), 2)
        cv2.drawContours(frame3, [box], -1, (0, 255, 0), 2)

        box_x = []
        box_y = []
        for i in range(len(box)):
            box_x.append(box[i][0])
            box_y.append(box[i][1])

        box_x = list(unique_everseen(box_x))
        box_y = list(unique_everseen(box_y))

        if (len(box_x) == 4) and (len(box_y) == 4):
            dx = int(abs(box_x[0] - box_x[2]))
            dy = int(abs(box_y[0] - box_y[2]))
            qr_cx = int(abs(box_x[0] + box_x[2]) / 2)
            qr_cy = int(abs(box_y[0] + box_y[2]) / 2)
            Area = dx * dy
            print("Area", Area)
            box_x.sort()
            box_y.sort()
            point_x1 = box_x[0]
            point_x2 = box_x[3]
            point_y1 = box_y[0]
            point_y2 = box_y[3]
        elif (len(box_x) == 2) and (len(box_y) == 2):
            dx = int(abs(box_x[0] - box_x[1]))
            dy = int(abs(box_y[0] - box_y[1]))
            qr_cx = int(abs(box_x[0] + box_x[1]) / 2)
            qr_cy = int(abs(box_y[0] + box_y[1]) / 2)
            Area = dx * dy
            print("Area", Area)
            box_x.sort()
            box_y.sort()
            point_x1 = box_x[0]
            point_x2 = box_x[1]
            point_y1 = box_y[0]
            point_y2 = box_y[1]

        cv2.circle(frame3, (qr_cx, qr_cy), 3, (0, 255, 0), -1)

        cv2.putText(frame2, "%d" % qr_cx, (400, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 1)

        box_x0 = box_x[0] < box_x[1] and box_x[0] or box_x[1]
        #box_y1 = box_y[0] > box_y[1] and box_y[0] or box_y[1]
        box_y0 = box_y[0] < box_y[1] and box_y[0] or box_y[1]

        dx = qr_cx - box_x0
        dy = qr_cy - box_y0

        degree = int(atan2(dx, dy) * 180 / pi)

        fn = datetime.datetime.now()
        folder_name = str(fn.year) + "-" + str("%02d" % fn.month) + "-" + str("%02d" % fn.day)

        cv2.putText(frame3, "%d" % degree, (400, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 1)
        if abs(qr_cx - cx_ref) <= 3 and qr_check_process == 0 and qr_check_result == 2 and PLC_signal == True:

            roi = frame4[(point_y1  - 30):(point_y2 + 30), (point_x1 - 30):(point_x2 + 30)]
            qr_image = Reformat_Image(roi)

            cv2.imshow("qr_image", qr_image)
            data = str(decode(qr_image))
            sn = data[24:37]
            Serial_No = sn
            QR_SN.insert(20, Serial_No)

            print("=====  판독 중  =====")
            qr_check_process = 1
            if qr_check_make_folder == 0:
                today = get_today()
                foldername_today = store_location + today
                make_folder(foldername_today)
                foldername_barcode = store_location + today + "/barcode"
                make_folder(foldername_barcode)
                foldername_pass = store_location + today + "/barcode" + "/pass"
                make_folder(foldername_pass)
                foldername_fail = store_location + today + "/barcode" + "/fail"
                make_folder(foldername_fail)
                qr_check_make_folder = 1

            # print(abs(cx- cx_ref), abs(box_y[0]-qr_y2), abs(box_y[1] - qr_y1))
            # if abs(cx- cx_ref) <= 5 and abs(box_y0-qr_y1) <= 7 and abs(box_y1 - qr_y2) <= 7 :
            #print("box_x0, qr_x1, box_y0, qr_y1, box_y1, qr_y2", box_x0, qr_x1, box_y0, qr_y1, box_y1, qr_y2)
            #print(abs(int(box_x0) - int(qr_x1)))
            ##print(abs(box_y0 - qr_y1))
            #print(abs(box_y1 - qr_y2))

            cv2.imwrite("image.jpg", frame3)

            if (40 < degree and degree < 50) and abs(int(box_x0) - int(qr_x1)) <= 7 \
                    and abs(box_y0 - qr_y1) <= 7:
                cv2.putText(frame3, "PASS", (qr_cx - 100, qr_cy - 50), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
                cv2.imwrite(store_location + "%s/barcode/pass/%s.jpg" % (folder_name, Serial_No), frame3)
                # cv2.imwrite(store_location + "/%s/pass/qr%d" % (folder_name, count_pass), frame3)
                # cv2.imwrite(".\\%s\\pass\\qr%d.jpg" % count_pass, frame3)
                count_pass_barcode += 1
                print("정상 위치")
                qr_check_result = 1
            else:
                cv2.putText(frame3, "NG", (qr_cx - 100, qr_cy - 50), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
                cv2.imwrite(store_location + "%s/barcode/fail/%s.jpg" % (folder_name, Serial_No), frame3)
                # cv2.imwrite(store_location + "/%s/fail/qr%d" % (folder_name, count_fail), frame3)
                count_fail_barcode += 1
                print("불량")
                qr_check_result = 0
            accumulation = count_pass_barcode + count_fail_barcode
            leave_log(0)
        else:
            #print("판독 위치가 아닙니다.")
            qr_check_result = 2

    year, month, day, hour, minute, sec = check_time_value()

    if accumulation != pre_accumulation:
        time = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + " " + str("%02d" % hour) + ":" + str(
            "%02d" % minute) + ":" + str("%02d" % sec)
        qr_value_list[0] = Serial_No
        qr_value_list[1] = Serial_No
        qr_value_list[2] = time
        qr_value_list[3] = accumulation
        qr_value_list[4] = count_pass_barcode
        qr_value_list[5] = count_fail_barcode
        # value_list = [time, accumulation, count_pass_barcode, count_fail_barcode]
        # print("======="*10)
        SS_SN.delete(0, END)
        QR_SN.delete(0, END)
        QR_P1.delete(0, END)
        QR_P2.delete(0, END)
        QR_P3.delete(0, END)
        QR_P4.delete(0, END)
        QR_P5.delete(0, END)
        # SN.delete(0,END)

        # P0.insert(20, qr_value_list[0])
        QR_P1.insert(20, qr_value_list[1])
        QR_P2.insert(20, qr_value_list[2])
        QR_P3.insert(20, qr_value_list[3])
        QR_P4.insert(20, qr_value_list[4])
        QR_P5.insert(20, qr_value_list[5])
        pre_accumulation = accumulation

        if qr_check_result == 1:
            qr_label_ok_ng = Label(root, text="OK", font="Helvetica 140 bold", fg="RoyalBlue")
            qr_label_ok_ng.place(x=660, y=200)
        elif qr_check_result == 0:
            qr_label_ok_ng = Label(root, text="NG", font="Helvetica 140 bold", fg="red")
            qr_label_ok_ng.place(x=660, y=200)

    return frame3



def SSDetect(frame):
    global pre_volume, ss_check_make_folder
    global count_pass_sticker, count_fail_sticker, volume
    global Serial_No
    global ss_cx, ss_cy, ss_check_result
    global qr_check_process, ss_check_process
    global cnts, PLC_signal

    def filter(frame):
        global cnts
        # blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
        frame = cv2.GaussianBlur(frame_cp, (3, 3), 0)
        # frame = cv2.blur(frame,(3,3))
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # ret, thresh = cv2.threshold(gray_frame, 45, 255, cv2.THRESH_BINARY_INV)

        blue, green, red = cv2.split(frame)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(frame_hsv)
        frame_hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
        H, L, S = cv2.split(frame_hls)

        _, gray1 = cv2.threshold(gray_frame, 160, 255, cv2.THRESH_BINARY_INV)
        _, blue1 = cv2.threshold(blue, 184, 255, cv2.THRESH_BINARY_INV)
        _, green1 = cv2.threshold(green, 163, 255, cv2.THRESH_BINARY_INV)
        _, red1 = cv2.threshold(red, 117, 255, cv2.THRESH_BINARY_INV)
        _, h1 = cv2.threshold(h, 155, 255, cv2.THRESH_BINARY_INV)
        _, s1 = cv2.threshold(s, 250, 255, cv2.THRESH_BINARY_INV)
        _, v1 = cv2.threshold(v, 146, 255, cv2.THRESH_BINARY_INV)
        _, H1 = cv2.threshold(H, 164, 255, cv2.THRESH_BINARY_INV)
        _, L1 = cv2.threshold(L, 145, 255, cv2.THRESH_BINARY_INV)
        _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)

        _, gray_ = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY)
        _, blue_ = cv2.threshold(blue, 0, 255, cv2.THRESH_BINARY)
        _, green_ = cv2.threshold(green, 0, 255, cv2.THRESH_BINARY)
        _, red_ = cv2.threshold(red, 0, 255, cv2.THRESH_BINARY)
        _, h_ = cv2.threshold(h, 0, 255, cv2.THRESH_BINARY)
        _, s_ = cv2.threshold(s, 0, 255, cv2.THRESH_BINARY)
        _, v_ = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY)
        _, H_ = cv2.threshold(H, 40, 255, cv2.THRESH_BINARY)
        _, L_ = cv2.threshold(L, 0, 255, cv2.THRESH_BINARY)
        _, S_ = cv2.threshold(S, 115, 255, cv2.THRESH_BINARY)

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
        result = cv2.bitwise_and(frame, frame, mask=final_mask)
        # cv2.imshow('result', final_mask)

        blurred = cv2.blur(final_mask, (4, 4))
        (_, thresh) = cv2.threshold(blurred, 109, 255, cv2.THRESH_BINARY)
        # cv2.imshow('thresh', thresh)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        closed = cv2.erode(closed, None, iterations=2)
        closed = cv2.dilate(closed, None, iterations=2)
        # cv2.imshow('closed', closed)

        cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

    frame = cv2.flip(frame, 1)
    frame = cv2.flip(frame, 0)

    # img_rgb = cv2.imread('image\\match.png')
    frame_cp = frame.copy()
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ################# 템플릿 경로 설정 ########################
    template = cv2.imread('C:/Data_Record_QR/template.jpg', 0)
    ##########################################################

    w, h = template.shape[::-1]

    col, row, _ = frame.shape
    cx_ref = int(row / 2)
    cy_ref = int(col / 2)
    cv2.circle(frame, (cx_ref, cy_ref), 3, (255, 0, 0), -1)

    filter(frame_cp)

    if (len(cnts) != 0):
        c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        M = cv2.moments(c)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
        box = np.int0(box)

        # cv2.drawContours(img_rgb, [box], -1, (0,255,0), 2)

        box_x = []
        box_y = []
        for i in range(len(box)):
            box_x.append(box[i][0])
            box_y.append(box[i][1])

        box_x = list(unique_everseen(box_x))
        box_y = list(unique_everseen(box_y))

        print("box : ", len(box_y))
        if (len(box_x) == 4) and (len(box_y) == 4):
            dx = int(abs(box_x[0] - box_x[2]))
            dy = int(abs(box_y[0] - box_y[2]))
            ss_cx = int(abs(box_x[0] + box_x[2]) / 2)
            ss_cy = int(abs(box_y[0] + box_y[2]) / 2)
            Area = dx * dy
        elif (len(box_x) == 2) and (len(box_y) == 2):
            dx = int(abs(box_x[0] - box_x[1]))
            dy = int(abs(box_y[0] - box_y[1]))
            ss_cx = int(abs(box_x[0] + box_x[1]) / 2)
            ss_cy = int(abs(box_y[0] + box_y[1]) / 2)
            Area = dx * dy
        else:
            Area = 0

        print("Area : ", Area)
        cv2.circle(frame, (ss_cx, ss_cy), 3, (0, 255, 0), -1)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        threshold = 60
        threshold = threshold / 100
        # print(threshold)
        # threshold = 0.32 => 확인 후 값 고정
        loc = np.where(res >= threshold)

        f = set()
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)

            sensitivity = 650
            # sensitivity = 580 => 확인 후 값 고정
            f.add((round(pt[0] / sensitivity), round(pt[1] / sensitivity)))
        found_count = len(f)
        print("count : ", found_count)

        #Serial_No = SS_SN.get()
        #print(Serial_No)

        #print("SS 시리얼 넘버: ", Serial_No)

        fn = datetime.datetime.now()
        folder_name = str(fn.year) + "-" + str("%02d" % fn.month) + "-" + str("%02d" % fn.day)

        if str(Serial_No) != '' and (qr_check_process == 1 and ss_check_process == 0) and ss_check_result == 2 and PLC_signal == True:
        #if abs(ss_cx - cx_ref) <= 1 and (35000 <= Area and Area <= 75000) and str(Serial_No) != '' and (qr_check_process == 1 and ss_check_process == 0) and ss_check_result == 2:
            # if abs(cx - cx_ref) <= 1 and (10000 <= Area and Area <= 18000):
            print("=====  판독 중  =====")
            PLC_signal = False
            ss_check_process = 1
            if ss_check_make_folder == 0:
                today = get_today()
                foldername_today = store_location + today
                make_folder(foldername_today)
                foldername_barcode = store_location + today + "/sticker"
                make_folder(foldername_barcode)
                foldername_pass = store_location + today + "/sticker" + "/pass"
                make_folder(foldername_pass)
                foldername_fail = store_location + today + "/sticker" + "/fail"
                make_folder(foldername_fail)
                ss_check_make_folder = 1

            if (found_count == 2):
                cv2.putText(frame, "OK", (ss_cx, ss_cy), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 10)
                # cv2.putText(frame3, "PASS", (cx - 100, cy - 50), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
                cv2.imwrite(store_location + "%s/sticker/pass/%s.jpg" % (folder_name, Serial_No), frame)
                # cv2.imwrite(store_location + "/%s/pass/qr%d" % (folder_name, count_pass), frame3)
                # cv2.imwrite(".\\%s\\pass\\qr%d.jpg" % count_pass, frame3)
                count_pass_sticker += 1
                print("정상 위치")
                ss_check_result = 1
            else:
                cv2.putText(frame, "NG", (ss_cx, ss_cy), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
                # cv2.putText(frame3, "NG", (cx - 100, cy - 50), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
                cv2.imwrite(store_location + "%s/sticker/fail/%s.jpg" % (folder_name, Serial_No), frame)
                # cv2.imwrite(store_location + "/%s/fail/qr%d" % (folder_name, count_fail), frame3)
                count_fail_sticker += 1
                print("불량")
                ss_check_result = 0
            volume = count_pass_sticker + count_fail_sticker
            leave_log(1)
        else:
            #print("판독 위치가 아닙니다..")
            ss_check_result = 2

    year, month, day, hour, minute, sec = check_time_value()
    if volume != pre_volume:
        time = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + " " + str("%02d" % hour) + ":" + str("%02d" % minute) + ":" + str("%02d" % sec)
        ss_value_list[0] = Serial_No
        ss_value_list[1] = Serial_No
        ss_value_list[2] = time
        ss_value_list[3] = volume
        ss_value_list[4] = count_pass_sticker
        ss_value_list[5] = count_fail_sticker
        #value_list = [time, accumulation, count_pass_barcode, count_fail_barcode]
        #print("======="*10)
        SS_SN.delete(0, END)
        QR_SN.delete(0, END)
        SS_P1.delete(0, END)
        SS_P2.delete(0, END)
        SS_P3.delete(0, END)
        SS_P4.delete(0, END)
        SS_P5.delete(0, END)
        #SN.delete(0,END)

        #P0.insert(20, ss_value_list[0])
        SS_P1.insert(20, ss_value_list[1])
        SS_P2.insert(20, ss_value_list[2])
        SS_P3.insert(20, ss_value_list[3])
        SS_P4.insert(20, ss_value_list[4])
        SS_P5.insert(20, ss_value_list[5])
        pre_volume = volume

        if ss_check_result == 1:
            ss_label_ok_ng = Label(root, text="OK", font="Helvetica 140 bold", fg="RoyalBlue1")
            ss_label_ok_ng.place(x=1620, y=200)
        elif ss_check_result == 0:
            ss_label_ok_ng = Label(root, text="NG", font="Helvetica 140 bold", fg="red")
            ss_label_ok_ng.place(x=1620, y=200)

    return frame


def start_detect():
    global check_detect

    check_detect = False


def check_setting():
    global check_set, store_location, pathname, setting

    check_set = False
    store_location_input = datapath.get()
    setting.destroy()

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




def PLC_sensor():
    global PLC_signal, check_set

    if check_set == False:
        PLC_signal = True



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


def box_setting():
    global qr_x1, qr_y1, qr_x2, qr_y2
    global LU_X, LU_Y, RD_X, RD_Y
    global box_set

    #if box_set == False:
    qr_x1 = eval(LU_X.get())
    qr_y1 = eval(LU_Y.get())
    qr_x2 = eval(RD_X.get())
    qr_y2 = eval(RD_Y.get())

    LU_X.delete(0, END)
    LU_Y.delete(0, END)
    RD_X.delete(0, END)
    RD_Y.delete(0, END)

    box_set = True


def box_resetting():
    global box_set, count_mouse
    global qr_x1, qr_y1, qr_x2, qr_y2
    global LU_X, LU_Y, RD_X, RD_Y

    box_set = False
    count_mouse = 0


def setting_window():
    global datapath, setting, box_label
    global LU_X, LU_Y, RD_X, RD_Y
    global box_set
    ### 설정창

    setting = Toplevel(root)
    setting.geometry("800x600")
    setting.title("Setting Window")
    setting.configure(bg="#ebebeb")
    qr_width, qr_height = 1920, 1080

    Label(setting, text="QR 사각박스 설정", font="돋움체", bg="#ebebeb", bd=2, width=25, height=2, relief="groove",\
          anchor=CENTER).place(x=110, y=0)

    box_list = ["LU", "RD"]
    position_list = ["X", "Y"]
    for i in range(2):
        Label(setting, text=box_list[i], height=2, width=15, fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 13 bold").place(x=10 + (i * 220), y=65, relx=0.01, rely=0.01)
        Label(setting, text=position_list[i], height=4, width=5, fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 8 bold").place(x=5, y=(qr_height / 8) + (i * 61), relx=0.01, rely=0.01)
        Label(setting, text=position_list[i], height=4, width=5, fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 8 bold").place(x=215, y=(qr_height / 8) + (i * 61), relx=0.01, rely=0.01)

    Button(setting, text="사각박스 설정하기", font="돋움체", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=47, height=2, bd=3, padx=2, pady=2, command=box_setting).place(x=10 , y=270)

    ###사각박스 엔트리
    ##LU
    LU_X = Entry(setting, width=5, relief="groove", font="Helvetica 35 bold")
    LU_X.place(x=45, y=(qr_height / 8) + 0 , relx=0.01, rely=0.01)

    LU_Y = Entry(setting, width=5, relief="groove", font="Helvetica 35 bold")
    LU_Y.place(x=45, y=(qr_height / 8) + 61 , relx=0.01, rely=0.01)

    ##RU
    RD_X = Entry(setting, width=5, relief="groove", font="Helvetica 35 bold")
    RD_X.place(x=255, y=(qr_height / 8) + 0, relx=0.01, rely=0.01)

    RD_Y = Entry(setting, width=5, relief="groove", font="Helvetica 35 bold")
    RD_Y.place(x=255, y=(qr_height / 8) + 61, relx=0.01, rely=0.01)

    #사각박스 확인
    box_label = Label(setting)
    box_label.place(x=530, y=100)


    Label(setting, text="설정한 사각박스 확인", font="돋움체", bg="#ebebeb", bd=2, width=25, height=2, relief="groove", \
          anchor=CENTER).place(x=500, y=0)
    Button(setting, text="사각박스 재설정하기", font="돋움체", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=47, height=2, bd=3, padx=2, pady=2, command=box_resetting).place(x=410, y=270)

    # 데이터 저장 경로 설정
    Label(setting, text="데이터 저장 경로 설정", font="돋움체", bg="#ebebeb", bd=2, width=25, height=2, relief="groove", \
          anchor=CENTER).place(x=0, y=440)
    datapath = Entry(setting, width=35, relief="groove", font="Helvetica 35 bold")
    datapath.place(x=0, y=490, relx=0.001, rely=0)

    #설정 완료 버튼
    Button(setting, text="설정 완료", font="Helvetica 13 bold", relief="groove", overrelief="solid", bg="#ebebeb", \
           bd=3, padx=2, pady=2, command=check_setting).pack(side=BOTTOM, fill=X)


def mouse_position(event):
    global LU_X, LU_Y, RD_X, RD_Y, count_mouse
    global box_set

    print("===== 마우스 포지션 출력 =====")
    print("click - ", event.x, event.y)

    if box_set == False:
        if count_mouse == 0:
            LU_X.insert(20, event.x)
            LU_Y.insert(20, event.y)
            count_mouse += 1
        elif count_mouse == 1:
            RD_X.insert(20, event.x)
            RD_Y.insert(20, event.y)
            count_mouse += 1

def execute():
    global qr_label, sticker_label, root
    global QR_SN, QR_P1, QR_P2, QR_P3, QR_P4, QR_P5
    global SS_SN, SS_P1, SS_P2, SS_P3, SS_P4, SS_P5
    global Serial_N

    root = Tk()

    root.bind('<Escape>', lambda e: root.quit())
    root.bind("<Double-Button-1>", mouse_position)
    qr_label = Label(root)
    qr_label.place(y=10, anchor=NW)

    sticker_label = Label(root)
    sticker_label.place(x=960, y=10)

    qr_width, qr_height = 1920, 1080
    root.title("Check_QR")
    root.geometry("{}x{}+{}+{}".format(qr_width, qr_height, -10, 0))

    name = ["시리얼 넘버 입력\nInput SerialNumber", "시리얼 넘버\nSerialNumber", "판독시간\nTime", "판독 수량\nNo. of Accumulation",
            "합격 수량\nNo. of OK", "불합격수량\nNo. of NG"]

    ##Label 생성
    for i in range(6):
        Label(root, text=name[i], height=5, width=17, fg="red", relief="groove", bg="#ebebeb") \
            .place(x=95, y=(qr_height / 3) + 140 + (i * 80), relx=0.01, rely=0.01)
        Label(root, text=name[i], height=5, width=17, fg="red", relief="groove", bg="#ebebeb") \
            .place(x=1055, y=(qr_height / 3) + 140 + (i * 80), relx=0.01, rely=0.01)

    Label(root, text="QR \nDetect Info", height=25, width=11, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=-14, y=(qr_height / 3) + 140 + (0 * 80), relx=0.01, rely=0.01)

    Label(root, text="Suction \nSticker \nDetect Info", height=25, width=11, fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=946, y=(qr_height / 3) + 140 + (0 * 80), relx=0.01, rely=0.01)

    Label(root, text="결과\nResult", height=5, width=17, fg="red", relief="groove", bd = 0,
          font="Helvetica 20 bold").place(x=635, y=0, relx=0.01, rely=0.01)
    Label(root, text="결과\nResult", height=5, width=18, fg="red", relief="groove", bd = 0,
          font="Helvetica 20 bold").place(x=1590, y=0, relx=0.01, rely=0.01)

    ##QR Entry
    QR_SN = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    QR_SN.place(x=218, y=(qr_height / 3) + 140 + (0 * 80), relx=0.01, rely=0.01)

    QR_P1 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    QR_P1.place(x=218, y=(qr_height / 3) + 140 + (1 * 80), relx=0.01, rely=0.01)

    QR_P2 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    QR_P2.place(x=218, y=(qr_height / 3) + 140 + (2 * 80), relx=0.01, rely=0.01)

    QR_P3 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    QR_P3.place(x=218, y=(qr_height / 3) + 140 + (3 * 80), relx=0.01, rely=0.01)

    QR_P4 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    QR_P4.place(x=218, y=(qr_height / 3) + 140 + (4 * 80), relx=0.01, rely=0.01)

    QR_P5 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    QR_P5.place(x=218, y=(qr_height / 3) + 140 + (5 * 80), relx=0.01, rely=0.01)

    ##Suction Sticker Entry
    SS_SN = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    SS_SN.place(x=1178, y=(qr_height / 3) + 140 + (0 * 80), relx=0.01, rely=0.01)

    SS_P1 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    SS_P1.place(x=1178, y=(qr_height / 3) + 140 + (1 * 80), relx=0.01, rely=0.01)

    SS_P2 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    SS_P2.place(x=1178, y=(qr_height / 3) + 140 + (2 * 80), relx=0.01, rely=0.01)

    SS_P3 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    SS_P3.place(x=1178, y=(qr_height / 3) + 140 + (3 * 80), relx=0.01, rely=0.01)

    SS_P4 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    SS_P4.place(x=1178, y=(qr_height / 3) + 140 + (4 * 80), relx=0.01, rely=0.01)

    SS_P5 = Entry(root, width=19, relief="groove", font="Helvetica 50 bold")
    SS_P5.place(x=1178, y=(qr_height / 3) + 140 + (5 * 80), relx=0.01, rely=0.01)

    setting_window()
    read_frame()
    root.mainloop()

if __name__=="__main__":
    execute()
