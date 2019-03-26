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

# 데이터를 저장할 위치(서버저장)
store_local_location = "C:/AceVision/"
#store_location = "//192.168.105.4/Multimedia/Air3239/"
Serial_No = ''
pre_Serial_No = 0
PLC_rx = 'ready'
PLC_tx_OK = '1'
PLC_tx_NG = '2'
protocol = 0
port_num = ''

check_protocol = False
barcode_set = False
Big_ROI_setting = False
Small_ROI_setting = False
except_big_setting = False
except_small_setting = False
detect_once_big = False
detect_once_small = False
rivet_detect = False
check_set = True
PLC_sensor = False
check_result_label = False
check_local_path = False
check_server_path = False

count_mouse = 0
save_rivet_center_flag_big = 0
save_rivet_center_flag_small = 0
Start_except_box_big = 0
Start_except_box_small = 0
tact_time_flag = 0
start_time = 0
tact_time = 0
cnt = 0
rotate = 0

check_year = 0
check_month = 0
check_day = 0
check_make_folder = 0
check_result = 0
pre_day = 0

accum = 0
count_pass_rivet = 0
count_fail_rivet = 0

circle_center_list = []
rivet_empty_list = []
circle_center_area_list = []

Big_ROI_list = []
Small_ROI_list = []
except_box_big = []
except_box_small = []
ex_w_big = 0
ex_w_small = 0
ex_h_big = 0
ex_h_small = 0
whole_circle_list_big = []
whole_circle_list_small = []
except_center_list_big = []
except_center_list_small = []
circle_area_list_big = []
circle_area_list_small = []
except_box_list_big = []
except_box_list_small = []
rect_list_big = []
rect_list_small = []
except_list_big = []
except_list_small = []
save_delete_item_list_big = []
save_delete_item_list_small = []
temp_whole_circle_big = []
temp_whole_circle_small = []
except_box_wh_big = []
except_box_wh_small = []

'''
# 2대의 카메라 해상도 설정 및 출력.
cap0 = cv2.VideoCapture(0)
cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # Width 4608
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 960) # Height 3288
print("첫번째 카메라 현재 해상도 %d x %d" %(cap0.get(3), cap0.get(4)))
'''

cap1 = cv2.VideoCapture(1)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 4608)  # Width 4608
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 3288)  # Height 3288


# ("두번째 카메라 현재 해상도 %d x %d" %(cap1.get(3), cap1.get(4)))


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


def leave_log():
    global check_year, check_month, check_day, f
    global today, pre_day, localtime
    global check_make_folder, folder_name
    global foldername_pass, foldername_fail, foldername_log

    year, month, day, hour, minute, sec = check_time_value()

    fn = datetime.datetime.now()
    folder_name = str(fn.year) + "-" + str("%02d" % fn.month) + "-" + str("%02d" % fn.day)

    if pre_day != day:
        check_make_folder = 0

    if check_make_folder == 0:
        today = get_today()
        foldername_today = store_local_location + today
        make_folder(foldername_today)
        foldername_barcode = store_local_location + today + "/rivet"
        make_folder(foldername_barcode)
        foldername_pass = store_local_location + today + "/rivet" + "/pass"
        make_folder(foldername_pass)
        foldername_fail = store_local_location + today + "/rivet" + "/fail"
        make_folder(foldername_fail)
        check_make_folder = 1

    filename = str(year) + str("%02d" % month) + str("%02d" % day)
    if day != check_day:
        # print("새로운 로그 파일 생성")
        today = get_today()
        foldername_log = store_local_location + today + "/rivet" + "/log"
        make_folder(foldername_log)
        f = open(store_local_location + today + "/rivet/log/log_%s.txt" % filename, 'w', encoding='utf - 8')
        data = "시리얼 넘버  //  판독 시간  //  누적 판독량  //  정상  //  불량  \n"
        f.write(data)

        check_year = datetime.datetime.now().year
        check_month = datetime.datetime.now().month
        check_day = datetime.datetime.now().day
        pre_day = check_day

    f = open(store_local_location + today + "/rivet/log/log_%s.txt" % filename, 'a')
    localtime = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + " " + str("%02d" % hour) + ":" + str(
        "%02d" % minute) + ":" + str("%02d" % sec)
    data = str(Serial_No) + " // " + str(localtime) + " // " + str("%04d" % accum) + " // " + str(
        "%04d" % count_pass_rivet) + " // " + str("%04d" % count_fail_rivet) + "\n"
    f.write(data)

    '''
    RV_SN.insert(20, Serial_No)
    RV_TIME.insert(20, localtime)
    RV_ACC.insert(20, accum)
    RV_PASS.insert(20, count_pass_rivet)
    RV_NG.insert(20, count_fail_rivet)
    RV_TACT.insert(20, tact_time)
    '''

    f.close()


def Reformat_Image(image, ratio_w, ratio_h):
    height, width = image.shape[:2]
    width = int(width * ratio_w)
    height = int(height * ratio_h)
    # res = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    res = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

    return res


def TCP_IP():
    global PORT, sock
    global PLC_sensor

    PORT = int(PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    receive_data = sock.recv(1024)  # 서버로 부터 오는 데이터
    receive_data = receive_data.decode('utf-8')
    # print("서버에서 받은 메세지 : ", receive_data)  # 서버에서 받은 데이터를 출력.

    receive_data = receive_data.lower()

    # print("최종 receive_data : ", receive_data)
    if receive_data == PLC_rx:
        PLC_sensor = True


def RS_232():
    global PLC_sensor
    # global ser, check_detect, port_num
    # global PLC_rx, PLC_tx_OK, PLC_tx_NG

    res = ser.readline()
    PLC_ready = res.decode()[:len(res) - 2]  # 공백이 있을시 추가.
    PLC_ready = PLC_ready.lower()

    # print("PLC_ready : ", PLC_ready)
    if PLC_ready == 'ready':
        # print("아두이노로 부터 받은 프로토콜:", PLC_ready)            # 받은 프로토콜
        PLC_sensor = True
    else:
        pass


def imageShow(N, Display):
    frame = N
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2image = Img.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=cv2image)
    Display.imgtk = imgtk
    Display.configure(image=imgtk)


def webCamShow(N, Display, cam_no):
    _, frame = N

    if cam_no == 1:
        frame = RivetDetect_Big(frame)
        frame = Reformat_Image(frame, 0.5, 0.5)

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cv2image = Img.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=cv2image)
    Display.imgtk = imgtk
    Display.configure(image=imgtk)


def decode(im):
    global Serial_No, pre_Serial_No
    # global RV_SN, RV_TIME, RV_ACC, RV_PASS, RV_NG, RV_TACT

    im = Reformat_Image(im, 2, 2)
    decodedObjects = str(pyzbar.decode(im))  # 바코드와 QR코드를 찾아냄
    Serial_No = decodedObjects[16:29]

    #Serial_No += str(accum)

    if Serial_No != '':
        # RV_SN.insert(20, Serial_No)

        RV_SN.delete(0, END)
        RV_TIME.delete(0, END)
        RV_ACC.delete(0, END)
        RV_PASS.delete(0, END)
        RV_NG.delete(0, END)
        RV_TACT.delete(0, END)

        # print("=======\n", decodedObjects)
        # print("Serial_No :", Serial_No)


def Rotate(src, num):
    if num == 0:
        dst = src
    elif num == 1:
        dst = cv2.transpose(src)
        dst = cv2.flip(dst, 1)
    elif num == 2:
        dst = cv2.transpose(src)
        dst = cv2.flip(src, -1)
    elif num == 3:
        dst = cv2.transpose(src)
        dst = cv2.flip(dst, 0)
    elif num == -1:
        dst = cv2.transpose(src)
        dst = cv2.flip(src, -1)
        dst = Rotate(dst, 1)
    elif num == -2:
        dst = cv2.transpose(src)
        dst = cv2.flip(src, 1)
        dst = Rotate(dst, 2)
        dst = cv2.flip(src, -1)
    elif num == -3:
        dst = cv2.transpose(src)
        dst = cv2.flip(src, -1)
        dst = Rotate(dst, 3)

    return dst


def roate_left():
    global rotate

    rotate -= 1
    if rotate == -4:
        rotate = 0


def roate_right():
    global rotate

    rotate += 1
    if rotate == 4:
        rotate = 0


def read_frame():
    ## 바코드 인식 카메라 추가 시 바코드 리드 함수 추가 위치 ##
    # global Serial_No, pre_Serial_No
    # global RV_SN, RV_P1, RV_P2, RV_P3, RV_P4, RV_P5
    # global check_cam1_judge, check_cam2_judge, check_cam3_judge
    global PLC_sensor, folder_name
    # global check_PLC_sensor, image_reformat, result_rivet
    # global store_location
    # global position
    # global HOST, PORT, PLC_rx, PLC_tx_OK, PLC_tx_NG
    # global ser, sock, protocol, port_num, set
    global check_result_label, result_label, image_label, SN_label
    global check_result, barcode_area, tact_time_flag, start_time, tact_time

    # global barcode_set, result_frame, pass_frame, ng_frame, frame_cp, rivet_empty_list, small_frame

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    tk_width, tk_height = 1920, 1080

    #webCamShow(cap1.read(), cam1_label, 1)

    if check_set == False and tact_time_flag == 0:
        start_time = time.time()
        tact_time_flag = 1

    if check_set == False:
        if barcode_set == True:
            barcode_area = frame_cp[(bar_y1 - 5):(bar_y2 + 5), (bar_x1 - 5):(bar_x2 + 5)]
            image_reformat = Reformat_Image(barcode_area, 1, 1)
            image_reformat = Rotate(image_reformat, rotate)
            # print(image_reformat.shape)
            height, width, _ = image_reformat.shape
            # label = 1100, 800
            # if (int(bar_x2) - int(bar_x1)) < (int(bar_y2) - int(bar_y1)):
            #    image_reformat = Rotate(image_reformat, 270)
            # imageShow(image_reformat, SN_label)

        #decode(barcode_area)
        leave_log()

        if Serial_No != '':
            if protocol == 1:
                RS_232()
            elif protocol == 2:
                TCP_IP()

            if check_result == 1:
                check_result = 0
                tact_time = str(round(time.time() - start_time, 2)) + ' [sec]'
                leave_log()
                PLC_sensor = False
                tact_time_flag = 0

                '''
                if barcode_set == True:
                    SN_label = Label(root)
                    SN_label.place(x=screen_width * (1152 / tk_width) - (width / 2),
                                   y=screen_height * (861 / tk_height) - (height / 2))
                    imageShow(image_reformat, SN_label)
                '''
                if check_result_label == True and Serial_No != '':
                    result_label.destroy()
                    image_label.destroy()
                    SN_label.destroy()
                    check_result_label = False

                if barcode_set == True:
                    SN_label = Label(root)
                    SN_label.place(x=screen_width * (1252 / tk_width) - (width / 2),
                                   y=screen_height * (861 / tk_height) - (height / 2))
                    imageShow(image_reformat, SN_label)

                if PassOrNG == 1:
                    if check_local_path == True:
                        cv2.imwrite(store_local_location + "%s/rivet/pass/%s.png" % (folder_name, Serial_No), pass_frame)
                    if check_server_path == True:
                        cv2.imwrite(store_server_location + "%s/rivet/pass/%s.png" % (folder_name, Serial_No), pass_frame)
                    result_label = Label(root, text="OK", font="Helvetica 140 bold", fg="RoyalBlue")
                    result_label.place(x=screen_width * (1500 / tk_width), y=screen_height * (760 / tk_height))

                    image_label = Label(root)
                    image_label.place(x=screen_width * (960 / tk_width), y=screen_height * (10 / tk_height))
                    result_image = Reformat_Image(pass_frame, 0.5, 0.5)
                    imageShow(result_image, image_label)

                    if protocol == 1:
                        ser.write(bytes(PLC_tx_OK, encoding='ascii'))
                    elif protocol == 2:
                        sock.send(PLC_tx_OK.encode())

                else:
                    rivet_empty_list.clear()
                    if check_local_path == True:
                        cv2.imwrite(store_local_location + "%s/rivet/fail/%s.png" % (folder_name, Serial_No), ng_frame)
                    if check_server_path == True:
                        cv2.imwrite(store_server_location + "%s/rivet/fail/%s.png" % (folder_name, Serial_No), ng_frame)
                    result_label = Label(root, text="NG", font="Helvetica 140 bold", fg="red")
                    result_label.place(x=screen_width * (1500 / tk_width), y=screen_height * (760 / tk_height))

                    image_label = Label(root)
                    image_label.place(x=screen_width * (960 / tk_width), y=screen_height * (10 / tk_height))
                    result_image = Reformat_Image(ng_frame, 0.5, 0.5)
                    imageShow(result_image, image_label)

                    if protocol == 1:
                        ser.write(bytes(PLC_tx_NG, encoding='ascii'))
                    elif protocol == 2:
                        sock.send(PLC_tx_NG.encode())

                check_result_label = True
                RV_SN.insert(20, Serial_No)
                RV_TIME.insert(20, localtime)
                RV_ACC.insert(20, accum)
                RV_PASS.insert(20, count_pass_rivet)
                RV_NG.insert(20, count_fail_rivet)
                RV_TACT.insert(20, tact_time)

    root.after(20, read_frame)


def judgefunc():
    global rivet_empty_list, check_result, ng_frame, pass_frame

    sum = 0

    for i in range(len(circle_center_list)):
        pixel_avg = 0
        count = 0

        for j in range(-2, 3):
            temp_pixel = int(frame_cp[circle_center_list[i][1] + j, circle_center_list[i][0], 0])
            pixel_avg += temp_pixel

            temp_pixel = int(frame_cp[circle_center_list[i][1], circle_center_list[i][0] + j, 0])
            pixel_avg += temp_pixel
            count += 2

        pixel_avg = pixel_avg / count

        if pixel_avg >= 100:
            sum += 1
        else:
            rivet_empty_list.append([circle_center_list[i][0], circle_center_list[i][1]])

    if len(rivet_empty_list) > 0:
        print("rivet_empty_list:", rivet_empty_list)
        print(Serial_No)

    check_result = 1

    if sum == len(circle_center_list):
        pass_frame = frame_cp.copy()
        for i in range(len(circle_center_list)):
            cv2.circle(pass_frame, (circle_center_list[i][0], circle_center_list[i][1]), circle_center_area_list[i],
                       (0, 255, 0), 2)
        return 1
    else:
        ng_frame = frame_cp.copy()
        if len(rivet_empty_list) != 0:
            for i in range(len(rivet_empty_list)):
                cv2.circle(ng_frame, (rivet_empty_list[i][0], rivet_empty_list[i][1]), 10, (0, 0, 255), 2)
        return -1


def RivetDetect_Big(frame):
    global detect_once_big, whole_circle_list_big, except_center_list_big, circle_area_list_big
    global Start_except_box_big, rect_list_big, except_list_big
    global detect_once_small, whole_circle_list_small, except_center_list_small, circle_area_list_small
    global Start_except_box_small, rect_list_small, except_list_small
    global frame_cp, result_frame, result
    global accum, count_pass_rivet, count_fail_rivet, PassOrNG, pass_frame
    # while True:

    # 프레임 읽기
    # 화면 크기 조절 (본인에게 맞는 해상도 조절)
    result = cv2.resize(frame, (1280, 960), interpolation=cv2.INTER_LINEAR)
    frame_cp = result.copy()
    img_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)  # gray로 변환.

    if Start_except_box_big == 1:
        rect_list_big.append(except_idx_big)
        except_list_big.append([ex_w_big, ex_h_big])
        Start_except_box_big = 0

    if Start_except_box_small == 1:
        rect_list_small.append(except_idx_small)
        except_list_small.append([ex_w_small, ex_h_small])
        Start_except_box_small = 0

    # 관심영역(ROI, Range of Interest) 지정.
    for i in range(len(Big_ROI_list)):
        result = cv2.rectangle(result, Big_ROI_list[i][0], Big_ROI_list[i][1], (150, 50, 150), 5)
        # cv2.putText(result, 'ROI%d' %(i + 1), (ROI_list[i][0][0], ROI_list[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # 관심영역(ROI, Range of Interest) 지정.
    for i in range(len(Small_ROI_list)):
        result = cv2.rectangle(result, Small_ROI_list[i][0], Small_ROI_list[i][1], (150, 50, 150), 5)
        # cv2.putText(result, 'ROI%d' %(i + 1), (ROI_list[i][0][0], ROI_list[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # 예외처리(Exception Box) 지정.
    for i in range(len(rect_list_big)):
        result = cv2.rectangle(result, (except_box_list_big[i][0] - int((except_list_big[i][0]) / 2),
                                        except_box_list_big[i][1] - int((except_list_big[i][1]) / 2)), \
                               (except_box_list_big[i][0] + int((except_list_big[i][0]) / 2),
                                except_box_list_big[i][1] + int((except_list_big[i][1]) / 2)), (0, 255, 255), 1)

        result = cv2.circle(result, (except_box_list_big[i][0], except_box_list_big[i][1]), 2, (50, 205, 50), -1)

        result = cv2.line(result, (except_box_list_big[i][0] - int((except_list_big[i][0]) / 2),
                                   except_box_list_big[i][1] - int((except_list_big[i][1]) / 2)), \
                          (except_box_list_big[i][0] + int((except_list_big[i][0]) / 2),
                           except_box_list_big[i][1] + int((except_list_big[i][1]) / 2)), (0, 255, 255), 1)

        result = cv2.line(result, (except_box_list_big[i][0] + int((except_list_big[i][0]) / 2),
                                   except_box_list_big[i][1] - int((except_list_big[i][1]) / 2)), \
                          (except_box_list_big[i][0] - int((except_list_big[i][0]) / 2),
                           except_box_list_big[i][1] + int((except_list_big[i][1]) / 2)), (0, 255, 255), 1)

    # 예외처리(Exception Box) 지정.
    for i in range(len(rect_list_small)):
        result = cv2.rectangle(result, (except_box_list_small[i][0] - int((except_list_small[i][0]) / 2),
                                        except_box_list_small[i][1] - int((except_list_small[i][1]) / 2)), \
                               (except_box_list_small[i][0] + int((except_list_small[i][0]) / 2),
                                except_box_list_small[i][1] + int((except_list_small[i][1]) / 2)), (0, 255, 255), 1)

        result = cv2.circle(result, (except_box_list_small[i][0], except_box_list_small[i][1]), 2, (50, 205, 50), -1)

        result = cv2.line(result, (except_box_list_small[i][0] - int((except_list_small[i][0]) / 2),
                                   except_box_list_small[i][1] - int((except_list_small[i][1]) / 2)), \
                          (except_box_list_small[i][0] + int((except_list_small[i][0]) / 2),
                           except_box_list_small[i][1] + int((except_list_small[i][1]) / 2)), (0, 255, 255), 1)

        result = cv2.line(result, (except_box_list_small[i][0] + int((except_list_small[i][0]) / 2),
                                   except_box_list_small[i][1] - int((except_list_small[i][1]) / 2)), \
                          (except_box_list_small[i][0] - int((except_list_small[i][0]) / 2),
                           except_box_list_small[i][1] + int((except_list_small[i][1]) / 2)), (0, 255, 255), 1)

    if rivet_detect == True:

        # param1 = 250, param2 = 20
        # 원본과 비율 / 찾은 원들간의 최소 중심거리 / param1, param2를 조절해 원을 찾음 250 20 5 30
        big_circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1.208, 10, param1=34, param2=24, minRadius=10,
                                       maxRadius=13)

        # 관심영역내 원만을 탐지함.
        if big_circles is not None:
            big_circles = np.uint16(np.around(big_circles))

            if detect_once_big == False:
                detect_once_big = True
                pass_frame = frame_cp.copy()

                for i in big_circles[0, :]:
                    for j in range(len(Big_ROI_list)):
                        if (i[0] > Big_ROI_list[j][0][0] and i[0] < Big_ROI_list[j][1][0]) and (
                                i[1] > Big_ROI_list[j][0][1] and i[1] < Big_ROI_list[j][1][1]):  # ROI 관심영역 내에서 찾아냄.
                            whole_circle_list_big.append([i[0], i[1]])  # ROI 내 모든 중심점.
                            circle_area_list_big.append(i[2])

                for k in range(len(except_box_big)):
                    if (whole_circle_list_big[k][0] > except_box_big[k][0] and whole_circle_list_big[k][0] < (
                            except_box_big[k][0] + ex_w_big)) and (
                            whole_circle_list_big[k][1] > except_box_big[k][1] and whole_circle_list_big[k][1] < (
                            except_box_big[k][1] + ex_h_big)):
                        except_center_list_big.append(
                            [whole_circle_list_big[k][0], whole_circle_list_big[k][1]])  # 예외처리 중심점을 리스트에 추가
                        whole_circle_list_big.remove(except_center_list_big[0])  # 예외처리 리스트에 있는 중심점들을 전체 중심점리스트에서 제거
                        except_center_list_big.pop()  # 제외 처리를 하고나서 값을 빼서 다음 값을 프로세스 진행하도록 함.

            if check_set == True:
                for idx in range(len(whole_circle_list_big)):
                    cv2.circle(result, (whole_circle_list_big[idx][0], whole_circle_list_big[idx][1]),
                               circle_area_list_big[idx], (0, 255, 0), 2)  # 원 외곽 컨투어 표시.
                    cv2.circle(result, (whole_circle_list_big[idx][0], whole_circle_list_big[idx][1]), 3, (255, 0, 40),
                               -1)  # 원의 중심점을 표시


            elif check_set == False:
                circle_area_list_big.clear()
                except_center_list_big.clear()
                whole_circle_list_big.clear()
                for i in big_circles[0, :]:
                    for j in range(len(Big_ROI_list)):
                        if (i[0] > Big_ROI_list[j][0][0] and i[0] < Big_ROI_list[j][1][0]) and (
                                i[1] > Big_ROI_list[j][0][1] and i[1] < Big_ROI_list[j][1][1]):  # ROI 관심영역 내에서 찾아냄.
                            whole_circle_list_big.append([i[0], i[1]])  # ROI 내 모든 중심점.
                            circle_area_list_big.append(i[2])

                try:
                    for i in range(len(save_delete_item_list_big)):
                        for j in range(len(whole_circle_list_big)):
                            if ((0 <= abs(
                                    int(whole_circle_list_big[j][0]) - int(save_delete_item_list_big[i][0]))) and (abs(
                                    int(whole_circle_list_big[j][0]) - int(save_delete_item_list_big[i][0])) <= 5)) and \
                                    ((0 <= abs(
                                        int(whole_circle_list_big[j][1]) - int(save_delete_item_list_big[i][1]))) and (
                                             abs(int(whole_circle_list_big[j][1]) - int(
                                                 save_delete_item_list_big[i][1])) <= 5)):
                                whole_circle_list_big[j][0] = save_delete_item_list_big[i][0]
                                whole_circle_list_big[j][1] = save_delete_item_list_big[i][1]

                        whole_circle_list_big.remove([save_delete_item_list_big[i][0], save_delete_item_list_big[i][1]])
                except ValueError:
                    pass

                for i in range(len(whole_circle_list_big)):
                    for j in range(len(circle_center_list)):
                        if ((0 <= abs(int(whole_circle_list_big[i][0]) - int(circle_center_list[j][0]))) and (
                                abs(int(whole_circle_list_big[i][0]) - int(circle_center_list[j][0])) <= 5)) and \
                                ((0 <= abs(int(whole_circle_list_big[i][1]) - int(circle_center_list[j][1]))) and (
                                        abs(int(whole_circle_list_big[i][1]) - int(circle_center_list[j][1])) <= 5)):
                            whole_circle_list_big[i][0] = circle_center_list[j][0]
                            whole_circle_list_big[i][1] = circle_center_list[j][1]
                try:
                    for k in range(len(except_box_big)):
                        if ((whole_circle_list_big[k][0] > except_box_big[k][0]) and (
                                whole_circle_list_big[k][0] < (except_box_big[k][0] + ex_w_big))) and (
                                (whole_circle_list_big[k][1] > except_box_big[k][1]) and (
                                whole_circle_list_big[k][1] < (except_box_big[k][1] + ex_h_big))):
                            except_center_list_big.append(
                                [whole_circle_list_big[k][0], whole_circle_list_big[k][1]])  # 예외처리 중심점을 리스트에 추가
                            whole_circle_list_big.remove(except_center_list_big[0])  # 예외처리 리스트에 있는 중심점들을 전체 중심점리스트에서 제거
                            # print("예외처리 중심점:", except_center_list)
                            except_center_list_big.pop()  # 제외 처리를 하고나서 값을 빼서 다음 값을 프로세스 진행하도록 함.
                except IndexError:
                    pass

                for idx in range(len(whole_circle_list_big)):
                    cv2.circle(result, (whole_circle_list_big[idx][0], whole_circle_list_big[idx][1]),
                               circle_area_list_big[idx], (0, 0, 255), 2)  # 원 외곽 컨투어 표시.
                    cv2.circle(result, (whole_circle_list_big[idx][0], whole_circle_list_big[idx][1]), 3, (255, 0, 40),
                               -1)  # 원의 중심점을 표시

    if rivet_detect == True:

        # param1 = 250, param2 = 20
        # 원본과 비율 / 찾은 원들간의 최소 중심거리 / param1, param2를 조절해 원을 찾음 250 20 5 30
        small_circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 0.5, 10, param1=70, param2=10, minRadius=8,
                                         maxRadius=10)

        # 관심영역내 원만을 탐지함.
        if small_circles is not None:
            small_circles = np.uint16(np.around(small_circles))

            if detect_once_small == False:
                detect_once_small = True
                pass_frame = frame_cp.copy()

                for i in small_circles[0, :]:
                    for j in range(len(Small_ROI_list)):
                        if (i[0] > Small_ROI_list[j][0][0] and i[0] < Small_ROI_list[j][1][0]) and (
                                i[1] > Small_ROI_list[j][0][1] and i[1] < Small_ROI_list[j][1][1]):  # ROI 관심영역 내에서 찾아냄.
                            whole_circle_list_small.append([i[0], i[1]])  # ROI 내 모든 중심점.
                            circle_area_list_small.append(i[2])

                for k in range(len(except_box_small)):
                    if (whole_circle_list_small[k][0] > except_box_small[k][0] and whole_circle_list_small[k][0] < (
                            except_box_small[k][0] + ex_w_small)) and (
                            whole_circle_list_small[k][1] > except_box_small[k][1] and whole_circle_list_small[k][1] < (
                            except_box_small[k][1] + ex_h_small)):
                        except_center_list_small.append(
                            [whole_circle_list_small[k][0], whole_circle_list_small[k][1]])  # 예외처리 중심점을 리스트에 추가
                        whole_circle_list_small.remove(except_center_list_small[0])  # 예외처리 리스트에 있는 중심점들을 전체 중심점리스트에서 제거
                        except_center_list_small.pop()  # 제외 처리를 하고나서 값을 빼서 다음 값을 프로세스 진행하도록 함.

            if check_set == True:
                for idx in range(len(whole_circle_list_small)):
                    cv2.circle(result, (whole_circle_list_small[idx][0], whole_circle_list_small[idx][1]),
                               circle_area_list_small[idx], (0, 255, 0), 2)  # 원 외곽 컨투어 표시.
                    cv2.circle(result, (whole_circle_list_small[idx][0], whole_circle_list_small[idx][1]), 3,
                               (255, 0, 40), -1)  # 원의 중심점을 표시


            elif check_set == False:
                circle_area_list_small.clear()
                except_center_list_small.clear()
                whole_circle_list_small.clear()
                for i in small_circles[0, :]:
                    for j in range(len(Small_ROI_list)):
                        if (i[0] > Small_ROI_list[j][0][0] and i[0] < Small_ROI_list[j][1][0]) and (
                                i[1] > Small_ROI_list[j][0][1] and i[1] < Small_ROI_list[j][1][1]):  # ROI 관심영역 내에서 찾아냄.
                            whole_circle_list_small.append([i[0], i[1]])  # ROI 내 모든 중심점.
                            circle_area_list_small.append(i[2])

                try:
                    for i in range(len(save_delete_item_list_small)):
                        for j in range(len(whole_circle_list_small)):
                            if ((0 <= abs(
                                    int(whole_circle_list_small[j][0]) - int(save_delete_item_list_small[i][0]))) and (
                                        abs(int(whole_circle_list_small[j][0]) - int(
                                                save_delete_item_list_small[i][0])) <= 5)) and \
                                    ((0 <= abs(int(whole_circle_list_small[j][1]) - int(
                                        save_delete_item_list_small[i][1]))) and (abs(
                                        int(whole_circle_list_small[j][1]) - int(
                                            save_delete_item_list_small[i][1])) <= 5)):
                                whole_circle_list_small[j][0] = save_delete_item_list_small[i][0]
                                whole_circle_list_small[j][1] = save_delete_item_list_small[i][1]
                        whole_circle_list_small.remove(
                            [save_delete_item_list_small[i][0], save_delete_item_list_small[i][1]])
                except ValueError:
                    pass

                for i in range(len(whole_circle_list_small)):
                    for j in range(len(circle_center_list)):
                        if ((0 <= abs(int(whole_circle_list_small[i][0]) - int(circle_center_list[j][0]))) and (
                                abs(int(whole_circle_list_small[i][0]) - int(circle_center_list[j][0])) <= 5)) and \
                                ((0 <= abs(int(whole_circle_list_small[i][1]) - int(circle_center_list[j][1]))) and (
                                        abs(int(whole_circle_list_small[i][1]) - int(circle_center_list[j][1])) <= 5)):
                            whole_circle_list_small[i][0] = circle_center_list[j][0]
                            whole_circle_list_small[i][1] = circle_center_list[j][1]
                try:
                    for k in range(len(except_box_small)):
                        if ((whole_circle_list_small[k][0] > except_box_small[k][0]) and (
                                whole_circle_list_small[k][0] < (except_box_small[k][0] + ex_w_small))) and (
                                (whole_circle_list_small[k][1] > except_box_small[k][1]) and (
                                whole_circle_list_small[k][1] < (except_box_small[k][1] + ex_h_small))):
                            except_center_list_small.append(
                                [whole_circle_list_small[k][0], whole_circle_list_small[k][1]])  # 예외처리 중심점을 리스트에 추가
                            whole_circle_list_small.remove(
                                except_center_list_small[0])  # 예외처리 리스트에 있는 중심점들을 전체 중심점리스트에서 제거
                            # print("예외처리 중심점:", except_center_list)
                            except_center_list_small.pop()  # 제외 처리를 하고나서 값을 빼서 다음 값을 프로세스 진행하도록 함.
                except IndexError:
                    pass

                for idx in range(len(whole_circle_list_small)):
                    cv2.circle(result, (whole_circle_list_small[idx][0], whole_circle_list_small[idx][1]),
                               circle_area_list_small[idx], (0, 0, 255), 2)  # 원 외곽 컨투어 표시.
                    cv2.circle(result, (whole_circle_list_small[idx][0], whole_circle_list_small[idx][1]), 3,
                               (255, 0, 40), -1)  # 원의 중심점을 표시
                # 원의 갯수

                if PLC_sensor == True and  Serial_No != '':
                    PassOrNG = judgefunc()

                    if (PassOrNG == 1):
                        count_pass_rivet += 1
                        result_frame = result.copy()
                    elif (PassOrNG == -1):
                        count_fail_rivet += 1
                    else:
                        pass

                    accum = count_pass_rivet + count_fail_rivet

    if check_set == False:
        return frame_cp
    else:
        return result


def affiche(com_port):
    global choices, port_num

    port_num = com_port

    # print(port_num)


def mouse_position(event):
    global count_mouse
    # print("===== 마우스 포지션 출력 =====")
    # print("click - ", event.x *2 , event.y * 2)

    try:
        if Big_ROI_setting == False:
            if count_mouse == 0:
                BIg_LU_X.insert(20, event.x)
                Big_LU_Y.insert(20, event.y)
                count_mouse += 1
            elif count_mouse == 1:
                Big_RD_X.insert(20, event.x)
                Big_RD_Y.insert(20, event.y)
                count_mouse = 0
        elif Big_ROI_setting == True and Small_ROI_setting == False:
            if count_mouse == 0:
                Small_LU_X.insert(20, event.x)
                Small_LU_Y.insert(20, event.y)
                count_mouse += 1
            elif count_mouse == 1:
                Small_RD_X.insert(20, event.x)
                Small_RD_Y.insert(20, event.y)
                count_mouse = 0
        elif Small_ROI_setting == True and except_big_setting == False:
            Big_Except_X.insert(20, event.x)
            Big_Except_Y.insert(20, event.y)
        elif except_big_setting == True and except_small_setting == False:
            Small_Except_X.insert(20, event.x)
            Small_Except_Y.insert(20, event.y)
            # Except_W.insert(20, 5)
            # Except_H.insert(20, 5)

        if except_big_setting == True and except_small_setting == True:
            if count_mouse == 0:
                B_LU_X.insert(20, event.x)
                B_LU_Y.insert(20, event.y)
                count_mouse += 1
            elif count_mouse == 1:
                B_RD_X.insert(20, event.x)
                B_RD_Y.insert(20, event.y)
                count_mouse = 0
    except ValueError:
        pass


def open_folder_pass():
    ### 폴더 경로 변경
    if check_make_folder == 1:
        path = foldername_pass
        path = os.path.realpath(path)
        os.startfile(path)


def open_folder_ng():
    ### 폴더 경로 변경
    if check_make_folder == 1:
        path = foldername_fail
        path = os.path.realpath(path)
        os.startfile(path)


def open_folder_log():
    ### 폴더 경로 변경
    if check_make_folder == 1:
        path = foldername_log
        path = os.path.realpath(path)
        os.startfile(path)


def select_RS_232():
    global protocol, check_protocol
    # global set, RSC_B, PLC_IP_label, PLC_IP, PLC_PORT
    global list_box, SP_label, RS_B, TI_B, PLC_PORT_label

    RS_B.destroy()
    TI_B.destroy()

    if protocol == 2:
        PLC_IP_label.destroy()
        PLC_PORT_label.destroy()
        PLC_IP.destroy()
        PLC_PORT.destroy()

    protocol = 1
    check_protocol = True

    screen_width = set.winfo_screenwidth()
    screen_height = set.winfo_screenheight()
    tk_width, tk_height = 1920, 1080

    RS_B = Button(set, text="RS-232", font="Helvetica 10", relief="raised", overrelief="solid", bg="#dfffbf", \
                  width=int(screen_width * (14 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3, padx=2,
                  pady=2, command=select_RS_232)
    RS_B.place(x=screen_width * (135 / tk_width), y=screen_height * (710 / tk_height))

    TI_B = Button(set, text="TCP/IP", font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb", \
                  width=int(screen_width * (14 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3, padx=2,
                  pady=2, command=select_TCP_IP)
    TI_B.place(x=screen_width * (135 / tk_width), y=screen_height * (760 / tk_height))

    SP_label = Label(set, text="Serial Port", height=int(screen_height * (2 / tk_height)),
                     width=int(screen_width * (12 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
                     font="Helvetica 13 bold")
    SP_label.place(x=screen_width * (265 / tk_width), y=screen_height * (705 / tk_height), relx=0.01, rely=0.01)

    choices = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', \
               'COM9', 'COM10', 'COM11', 'COM12', 'COM13', 'COM14', 'COM15', 'COM16']

    variable = StringVar(root)
    variable.set('     COM_Port     ')
    list_box = OptionMenu(set, variable, *choices, command=affiche)
    list_box.place(x=screen_width * (265 / tk_width), y=screen_height * (765 / tk_height), relx=0.01, rely=0.01)

    # print("통신방식 : RS-232 ")


def select_TCP_IP():
    global protocol, check_protocol
    # global set, list_box, SP_label, RSC_B
    global RS_B, TI_B, PLC_IP_label, PLC_IP, PLC_PORT_label, PLC_PORT

    TI_B.destroy()

    if protocol == 1:
        list_box.destroy()
        SP_label.destroy()

    protocol = 2
    check_protocol = True

    screen_width = set.winfo_screenwidth()
    screen_height = set.winfo_screenheight()
    tk_width, tk_height = 1920, 1080

    PLC_IP_label = Label(set, text="PLC IP Address", height=int(screen_height * (2 / tk_height)),
                         width=int(screen_width * (15 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
                         font="Helvetica 13 bold")
    PLC_IP_label.place(x=screen_width * (265 / tk_width), y=screen_height * (705 / tk_height), relx=0.01, rely=0.01)

    PLC_PORT_label = Label(set, text="PLC PORT Number", height=int(screen_height * (2 / tk_height)),
                           width=int(screen_width * (16 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
                           font="Helvetica 13 bold")
    PLC_PORT_label.place(x=screen_width * (610 / tk_width), y=screen_height * (705 / tk_height), relx=0.01, rely=0.01)

    PLC_IP = Entry(set, width=int(screen_width * (15 / tk_width)), relief="groove", font="Helvetica 30 bold")
    PLC_IP.place(x=screen_width * (265 / tk_width), y=screen_height * (750 / tk_height) + 0, relx=0.01, rely=0.01)

    PLC_PORT = Entry(set, width=int(screen_width * (8 / tk_width)), relief="groove", font="Helvetica 30 bold")
    PLC_PORT.place(x=screen_width * (610 / tk_width), y=screen_height * (750 / tk_height) + 0, relx=0.01, rely=0.01)

    RS_B = Button(set, text="RS-232", font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb", \
                  width=int(screen_width * (14 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3, padx=2,
                  pady=2, command=select_RS_232)
    RS_B.place(x=screen_width * (135 / tk_width), y=screen_height * (710 / tk_height))

    TI_B = Button(set, text="TCP/IP", font="Helvetica 10", relief="raised", overrelief="solid", bg="#dfffbf", \
                  width=int(screen_width * (14 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3, padx=2,
                  pady=2, command=select_TCP_IP)
    TI_B.place(x=screen_width * (135 / tk_width), y=screen_height * (760 / tk_height))

    # print("통신방식 : TCP/IP")


def check_setting():
    global check_set, store_local_location, pathname
    global ser, HOST, PORT
    global circle_center_list, circle_center_area_list
    # global port_num, protocol, check_protocol, set, whole_circle_list_big, circle_area_list_big, whole_circle_list_small, circle_area_list_small

    # print("pro, port : ", protocol, port_num)

    #### circle_center_list 에 big + small 적용
    circle_center_list = copy.deepcopy(whole_circle_list_big) + copy.deepcopy(whole_circle_list_small)
    circle_center_area_list = copy.deepcopy(circle_area_list_big) + copy.deepcopy(circle_area_list_small)
    # print(len(circle_center_list), len(circle_center_area_list))
    # print(circle_center_list)
    whole_circle_list_big.clear()
    whole_circle_list_small.clear()
    circle_area_list_big.clear()
    circle_area_list_small.clear()

    if protocol == 1 and port_num != '':
        ser = serial.Serial(
            port=port_num,
            baudrate=115200,
            parity=serial.PARITY_NONE, \
            stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, \
            timeout=0
        )
        check_communication = True
    elif protocol == 2:
        HOST = PLC_IP.get()
        PORT = PLC_PORT.get()
        check_communication = True

    if check_protocol == True and check_communication == True:
        check_set = False
        store_location_input = datapath_local.get()

        # print(HOST, PORT)
        set.destroy()

        pathname = ''
        print(store_location_input)
        if store_location_input != '':
            parsing = store_location_input.split('/')
            print("parsing", parsing)
            #if parsing[0] != '' and parsing[1] != '':
            for i in range(len(parsing)):
                if parsing[i] != '':
                    pathname += parsing[i] + '/'
                    # print(pathname)
                elif parsing[i] == '':
                    pathname += '\\'
                elif parsing[i] == '/':
                    break

            if i != 0 and parsing[i] != '':
                print(pathname)
                #make_folder(pathname)

            store_local_location = pathname
            print("location : ", store_local_location)


def start_rivet_detect():
    global rivet_detect

    rivet_detect = True


def restart_rivet_detect():
    global detect_once_big, detect_once_small, whole_circle_list_big, whole_circle_list_small

    whole_circle_list_big = []
    whole_circle_list_small = []
    detect_once_big = False
    detect_once_small = False
    # print("리벳 위치 재감지")


def add_Big_ROI():
    global Big_ROI_list, count_mouse

    try:
        ROI_X1 = int(BIg_LU_X.get()) * 2
        ROI_Y1 = int(Big_LU_Y.get()) * 2
        ROI_X2 = int(Big_RD_X.get()) * 2
        ROI_Y2 = int(Big_RD_Y.get()) * 2

        Big_ROI_list.append([(ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2)])

        count_mouse = 0

        BIg_LU_X.delete(0, END)
        Big_LU_Y.delete(0, END)
        Big_RD_X.delete(0, END)
        Big_RD_Y.delete(0, END)
    except ValueError:
        pass


def add_small_ROI():
    global Small_ROI_list, count_mouse

    try:
        ROI_X1 = int(Small_LU_X.get()) * 2
        ROI_Y1 = int(Small_LU_Y.get()) * 2
        ROI_X2 = int(Small_RD_X.get()) * 2
        ROI_Y2 = int(Small_RD_Y.get()) * 2

        Small_ROI_list.append([(ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2)])

        count_mouse = 0

        Small_LU_X.delete(0, END)
        Small_LU_Y.delete(0, END)
        Small_RD_X.delete(0, END)
        Small_RD_Y.delete(0, END)
    except ValueError:
        pass


def set_comp_Big_ROI():
    global Big_ROI_setting

    Big_ROI_setting = True

    BIg_LU_X.delete(0, END)
    Big_LU_Y.delete(0, END)
    Big_RD_X.delete(0, END)
    Big_RD_Y.delete(0, END)


def set_comp_Small_ROI():
    global Small_ROI_setting

    Small_ROI_setting = True

    Small_LU_X.delete(0, END)
    Small_LU_Y.delete(0, END)
    Small_RD_X.delete(0, END)
    Small_RD_Y.delete(0, END)


def set_comp_big_except():
    global except_big_setting

    except_big_setting = True

    Big_Except_X.delete(0, END)
    Big_Except_Y.delete(0, END)
    # Except_W.delete(0, END)
    # Except_H.delete(0, END)


def set_comp_small_except():
    global except_small_setting

    except_small_setting = True

    Small_Except_X.delete(0, END)
    Small_Except_Y.delete(0, END)
    # Except_W.delete(0, END)
    # Except_H.delete(0, END)


def set_Bar_area():
    global barcode_set
    global bar_x1, bar_y1, bar_x2, bar_y2

    try:
        barcode_set = True

        bar_x1 = int(B_LU_X.get()) * 2
        bar_y1 = int(B_LU_Y.get()) * 2
        bar_x2 = int(B_RD_X.get()) * 2
        bar_y2 = int(B_RD_Y.get()) * 2

        B_LU_X.delete(0, END)
        B_RD_X.delete(0, END)
        B_LU_Y.delete(0, END)
        B_RD_Y.delete(0, END)
    except ValueError:
        pass


def reset_Bar_area():
    global barcode_set

    barcode_set = False


def add_except_big_area():
    global except_box_big, ex_w_big, ex_h_big
    global whole_circle_list_big, except_box_wh_big
    global save_rivet_center_flag_big, except_box_list_big, temp_whole_circle_big
    global except_idx_big, Start_except_box_big, save_delete_item_list_big, circle_area_list_big

    try:
        if Big_ROI_setting == True:
            EA_X_big = int(Big_Except_X.get()) * 2
            EA_Y_big = int(Big_Except_Y.get()) * 2
            ex_w_big = 10
            ex_h_big = 10
            # ex_w = int(Except_W.get()) * 2
            # ex_h = int(Except_H.get()) * 2

            Big_Except_X.delete(0, END)
            Big_Except_Y.delete(0, END)
            # Except_W.delete(0, END)
            # Except_H.delete(0, END)

            except_box_big.append([EA_X_big, EA_Y_big])
            except_box_wh_big.append([ex_w_big, ex_h_big])

            Start_except_box_big = 1

            if save_rivet_center_flag_big == 0:
                save_rivet_center_flag_big = 1
                temp_whole_circle_big = whole_circle_list_big

            idx = 0
            delete_item_list_big = []
            for i in range(len(except_box_big)):
                for j in range(len(whole_circle_list_big)):
                    if ((except_box_big[i][0] - ex_w_big) <= whole_circle_list_big[j][0]) and (
                            whole_circle_list_big[j][0] <= (except_box_big[i][0] + ex_w_big)) \
                            and ((except_box_big[i][1] - ex_h_big) <= whole_circle_list_big[j][1]) and (
                            whole_circle_list_big[j][1] <= (except_box_big[i][1] + ex_h_big)):
                        delete_item_list_big.append([whole_circle_list_big[j][0], whole_circle_list_big[j][1]])

            delete_item_list_big = list(unique_everseen(delete_item_list_big))

            # print("1. whole_circle_list", whole_circle_list)

            for i in range(len(delete_item_list_big)):
                if (0 <= abs(delete_item_list_big[i][0] - EA_X_big) and abs(
                        delete_item_list_big[i][0] - EA_X_big) <= 3) and (
                        0 <= abs(delete_item_list_big[i][1] - EA_Y_big) and abs(
                        delete_item_list_big[i][1] - EA_Y_big) <= 3):
                    idx = i

            except_idx_big = temp_whole_circle_big.index([delete_item_list_big[idx][0], delete_item_list_big[idx][1]])
            except_box_list_big.append(temp_whole_circle_big[except_idx_big])
            del circle_area_list_big[except_idx_big]

            for i in range(len(delete_item_list_big)):
                whole_circle_list_big.remove([delete_item_list_big[i][0], delete_item_list_big[i][1]])
                save_delete_item_list_big.append([delete_item_list_big[i][0], delete_item_list_big[i][1]])

            # print("2. whole_circle_list", whole_circle_list)
            # print("3. delete_item_list", delete_item_list)

    except IndexError:
        Start_except_box_big = 0

    except ValueError:
        pass


def add_except_small_area():
    global except_box_small, ex_w_small, ex_h_small
    global whole_circle_list_small, except_box_wh_small
    global save_rivet_center_flag_small, except_box_list_small, temp_whole_circle_small
    global except_idx_small, Start_except_box_small, save_delete_item_list_small, circle_area_list_small

    try:
        if Big_ROI_setting == True:
            EA_X_small = int(Small_Except_X.get()) * 2
            EA_Y_small = int(Small_Except_Y.get()) * 2
            ex_w_small = 10
            ex_h_small = 10
            # ex_w = int(Except_W.get()) * 2
            # ex_h = int(Except_H.get()) * 2

            Small_Except_X.delete(0, END)
            Small_Except_Y.delete(0, END)
            # Except_W.delete(0, END)
            # Except_H.delete(0, END)

            except_box_small.append([EA_X_small, EA_Y_small])
            except_box_wh_small.append([ex_w_small, ex_h_small])

            Start_except_box_small = 1

            if save_rivet_center_flag_small == 0:
                save_rivet_center_flag_small = 1
                temp_whole_circle_small = whole_circle_list_small

            idx = 0
            delete_item_list_small = []
            for i in range(len(except_box_small)):
                for j in range(len(whole_circle_list_small)):
                    if ((except_box_small[i][0] - ex_w_small) <= whole_circle_list_small[j][0]) and (
                            whole_circle_list_small[j][0] <= (except_box_small[i][0] + ex_w_small)) \
                            and ((except_box_small[i][1] - ex_h_small) <= whole_circle_list_small[j][1]) and (
                            whole_circle_list_small[j][1] <= (except_box_small[i][1] + ex_h_small)):
                        delete_item_list_small.append([whole_circle_list_small[j][0], whole_circle_list_small[j][1]])

            delete_item_list_small = list(unique_everseen(delete_item_list_small))

            # print("1. whole_circle_list", whole_circle_list)

            for i in range(len(delete_item_list_small)):
                if (0 <= abs(delete_item_list_small[i][0] - EA_X_small) and abs(
                        delete_item_list_small[i][0] - EA_X_small) <= 3) and (
                        0 <= abs(delete_item_list_small[i][1] - EA_Y_small) and abs(
                        delete_item_list_small[i][1] - EA_Y_small) <= 3):
                    idx = i

            except_idx_small = temp_whole_circle_small.index(
                [delete_item_list_small[idx][0], delete_item_list_small[idx][1]])
            except_box_list_small.append(temp_whole_circle_small[except_idx_small])
            del circle_area_list_small[except_idx_small]

            for i in range(len(delete_item_list_small)):
                whole_circle_list_small.remove([delete_item_list_small[i][0], delete_item_list_small[i][1]])
                save_delete_item_list_small.append([delete_item_list_small[i][0], delete_item_list_small[i][1]])

            # print("2. whole_circle_list", whole_circle_list)
            # print("3. delete_item_list", delete_item_list)

    except IndexError:
        Start_except_box_small = 0

    except ValueError:
        pass


def browse_folder_local():
    global store_local_location, check_local_path

    check_local_path = True
    datapath_local.delete(0, END)
    browse = Tk()
    browse.dirName = filedialog.askdirectory()
    store_local_location = browse.dirName
    datapath_local.insert(20, store_local_location)
    browse.destroy()
    # print(store_location)

def browse_folder_server():
    global store_server_location, check_server_path

    check_server_path = True
    datapath_server.delete(0, END)
    browse = Tk()
    browse.dirName = filedialog.askdirectory()
    store_server_location = browse.dirName
    datapath_server.insert(20, store_server_location)
    browse.destroy()
    # print(store_location)


def setting_window():
    global datapath_local, datapath_server, set
    # global choices
    global RS_B, TI_B
    global BIg_LU_X, Big_RD_X, Big_LU_Y, Big_RD_Y
    global Small_LU_X, Small_RD_X, Small_LU_Y, Small_RD_Y
    global Big_Except_X, Big_Except_Y, Small_Except_X, Small_Except_Y
    global B_LU_X, B_RD_X, B_LU_Y, B_RD_Y

    ### 설정창

    set = Toplevel(root)
    screen_width = set.winfo_screenwidth()
    screen_height = set.winfo_screenheight()
    tk_width, tk_height = 1920, 1080

    set.iconbitmap("aceantenna.ico")
    set.geometry("{}x{}+{}+{}".format(int(screen_width * (830 / tk_width)), int(screen_height * (1000 / tk_height)), \
                                      int((screen_width / 2) - int(screen_width * (830 / tk_width) / 2)),
                                      int((screen_height / 2) - int(screen_height * (950 / tk_height) / 2)) - 65))
    # set.geometry("800x600")
    set.title("Setting Window")
    set.configure(bg="#ebebeb")

    Label(set, text="Initial Setting", font="Helvetica 15 bold", bg="#ebebeb", bd=2, width=int(screen_width * (20 / tk_width)), \
          height=int(screen_height * (2 / tk_height)), relief="groove", anchor=CENTER).place(x=0, y=0)

    ### ROI
    Label(set, font="Helvetica 15 bold", bg="#ebebeb", bd=2, width=int(screen_width * (33 / tk_width)), \
          height=int(screen_height * (12 / tk_height)), relief="groove", anchor=CENTER).place(
        x=screen_width * (0 / tk_width), y=screen_height * (70 / tk_height), relx=0.01, rely=0.01)

    Label(set, font="Helvetica 15 bold", bg="#ebebeb", bd=2, width=int(screen_width * (33 / tk_width)), \
          height=int(screen_height * (12 / tk_height)), relief="groove", anchor=CENTER).place(
        x=screen_width * (410 / tk_width), y=screen_height * (70 / tk_height), relx=0.01, rely=0.01)

    ###예외 지역
    Label(set, font="Helvetica 15 bold", bg="#ebebeb", bd=2, width=int(screen_width * (33 / tk_width)), \
          height=int(screen_height * (12 / tk_height)), relief="groove", anchor=CENTER).place(
        x=screen_width * (0 / tk_width), y=screen_height * (400 / tk_height), relx=0.01, rely=0.01)
    ### 바코드 위치
    Label(set, font="Helvetica 15 bold", bg="#ebebeb", bd=2, width=int(screen_width * (33 / tk_width)), \
          height=int(screen_height * (12 / tk_height)), relief="groove", anchor=CENTER).place(
        x=screen_width * (410 / tk_width), y=screen_height * (400 / tk_height), relx=0.01, rely=0.01)

    Label(set, text="Set ROI(Large_Rivet)", height=int(screen_height * (2 / tk_height)),
          width=int(screen_width * (20 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=screen_width * (95 / tk_width), y=screen_height * (55 / tk_height),
                                          relx=0.01, rely=0.01)

    Label(set, text="Set ROI(Small_Rivet)", height=int(screen_height * (2 / tk_height)),
          width=int(screen_width * (20 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=screen_width * (505 / tk_width), y=screen_height * (55 / tk_height),
                                          relx=0.01, rely=0.01)

    Label(set, text="Set Exception Area", height=int(screen_height * (2 / tk_height)), width=int(screen_width * (20 / tk_width)),
          fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=screen_width * (95 / tk_width), y=screen_height * (380 / tk_height),
                                          relx=0.01, rely=0.01)

    Label(set, text="Set Barcode position", height=int(screen_height * (2 / tk_height)), width=int(screen_width * (20 / tk_width)),
          fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=screen_width * (505 / tk_width), y=screen_height * (385 / tk_height),
                                          relx=0.01, rely=0.01)

    Label(set, text="Set Data Save Path", font="Helvetica 12 bold", fg="red", bg="#ebebeb", bd=2,
          width=int(screen_width * (25 / tk_width)), \
          height=int(screen_height * (2 / tk_height)), relief="groove", anchor=CENTER).place(x=0, y=screen_height * (
                817 / tk_height))

    Label(set, text="Local", font="Helvetica 12 bold", fg="red", bg="#ebebeb", bd=2,
          width=int(screen_width * (10 / tk_width)), \
          height=int(screen_height * (2 / tk_height)), relief="groove", anchor=CENTER).place(x=0, y=screen_height * (
            870 / tk_height))

    datapath_local = Entry(set, width=int(screen_width * (55 / tk_width)), relief="groove", font="Helvetica 25 bold")
    datapath_local.place(x=103, y=screen_height * (870 / tk_height), relx=0.001, rely=0)

    Label(set, text="Server", font="Helvetica 12 bold", fg="red", bg="#ebebeb", bd=2,
          width=int(screen_width * (10 / tk_width)), \
          height=int(screen_height * (2 / tk_height)), relief="groove", anchor=CENTER).place(x=0, y=screen_height * (
            913 / tk_height))

    datapath_server = Entry(set, width=int(screen_width * (55 / tk_width)), relief="groove", font="Helvetica 25 bold")
    datapath_server.place(x=103, y=screen_height * (913 / tk_height), relx=0.001, rely=0)


    Button(set, text="Set Complete", font="Helvetica 13 bold", relief="groove", overrelief="solid", bg="#ebebeb", \
           bd=3, padx=2, pady=2, command=check_setting).pack(side=BOTTOM, fill=X)

    Button(set, text="Detect Rivet ", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=int(screen_width * (20 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3, padx=2, pady=2,
           command=start_rivet_detect).place(x=screen_width * (460 / tk_width), y=screen_height * (815 / tk_height))

    Button(set, text="Redetect Rivet", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=int(screen_width * (20 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3, padx=2, pady=2,
           command=restart_rivet_detect).place(x=screen_width * (640 / tk_width), y=screen_height * (815 / tk_height))

    Button(set, text="Browse\n(Local)", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=int(screen_width * (10 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3, padx=2, pady=2,
           command=browse_folder_local).place(x=screen_width * (260 / tk_width), y=screen_height * (815 / tk_height))

    Button(set, text="Browse\n(Server)", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=int(screen_width * (10 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3, padx=2, pady=2,
           command=browse_folder_server).place(x=screen_width * (360 / tk_width), y=screen_height * (815 / tk_height))

    ### 통신 방식
    ### Label
    Label(set, text="Set\nCommunication", height=int(screen_height * (4 / tk_height)), width=int(screen_width * (12 / tk_width)),
          fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=screen_width * (0 / tk_width), y=screen_height * (713 / tk_height),
                                          relx=0.01, rely=0.01)

    ### Button
    RS_B = Button(set, text="RS-232", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", \
                  width=int(screen_width * (14 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3, padx=2,
                  pady=2, command=select_RS_232)
    RS_B.place(x=screen_width * (135 / tk_width), y=screen_height * (710 / tk_height))

    TI_B = Button(set, text="TCP/IP", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", \
                  width=int(screen_width * (14 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3, padx=2,
                  pady=2, command=select_TCP_IP)
    TI_B.place(x=screen_width * (135 / tk_width), y=screen_height * (760 / tk_height))

    ##### ROI #####
    ### ROI Label
    box_list = ["Left Up", "Right Down"]
    position_list = ["X", "Y"]
    for i in range(2):
        Label(set, text=box_list[i], height=int(screen_height * (2 / tk_height)),
              width=int(screen_width * (15 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 13 bold").place(x=screen_width * (10 / tk_width) + (i * screen_width * (220 / tk_width)),
                                              y=screen_height * (105 / tk_height), relx=0.01, rely=0.01)

        Label(set, text=box_list[i], height=int(screen_height * (2 / tk_height)),
              width=int(screen_width * (15 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 13 bold").place(x=screen_width * (420 / tk_width) + (i * screen_width * (220 / tk_width)),
                                              y=screen_height * (105 / tk_height), relx=0.01, rely=0.01)

        Label(set, text=box_list[i], height=int(screen_height * (2 / tk_height)),
              width=int(screen_width * (15 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 13 bold").place(x=screen_width * (420 / tk_width) + (i * screen_width * (220 / tk_width)),
                                              y=screen_height * (435 / tk_height), relx=0.01, rely=0.01)

        ## ROI(BIG)
        Label(set, text=position_list[i], height=int(screen_height * (4 / tk_height)),
              width=int(screen_width * (5 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 8 bold").place(x=screen_width * (5 / tk_width), y=(screen_height / 7) + (
                    i * screen_height * (61 / tk_height)) + screen_height * (10 / tk_height), relx=0.01, rely=0.01)

        Label(set, text=position_list[i], height=int(screen_height * (4 / tk_height)),
              width=int(screen_width * (5 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 8 bold").place(x=screen_width * (215 / tk_width), y=(screen_height / 7) + (
                    i * screen_height * (61 / tk_height)) + screen_height * (10 / tk_height), relx=0.01, rely=0.01)

        ### ROI(Small)
        Label(set, text=position_list[i], height=int(screen_height * (4 / tk_height)),
              width=int(screen_width * (5 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 8 bold").place(x=screen_width * (415 / tk_width), y=(screen_height / 7) + (
                    i * screen_height * (61 / tk_height)) + screen_height * (10 / tk_height), relx=0.01, rely=0.01)

        Label(set, text=position_list[i], height=int(screen_height * (4 / tk_height)),
              width=int(screen_width * (5 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 8 bold").place(x=screen_width * (625 / tk_width), y=(screen_height / 7) + (
                    i * screen_height * (61 / tk_height)) + screen_height * (10 / tk_height), relx=0.01, rely=0.01)

        ### barcode
        Label(set, text=position_list[i], height=int(screen_height * (4 / tk_height)),
              width=int(screen_width * (5 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 8 bold").place(x=screen_width * (415 / tk_width), y=(screen_height / 7) + (
                    i * screen_height * (61 / tk_height)) + screen_height * (340 / tk_height), relx=0.01, rely=0.01)

        Label(set, text=position_list[i], height=int(screen_height * (4 / tk_height)),
              width=int(screen_width * (5 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 8 bold").place(x=screen_width * (625 / tk_width), y=(screen_height / 7) + (
                    i * screen_height * (61 / tk_height)) + screen_height * (340 / tk_height), relx=0.01, rely=0.01)

    ### ROI(BIG) X, Y Entry
    BIg_LU_X = Entry(set, width=int(screen_width * (5 / tk_width)), relief="groove", font="Helvetica 35 bold")
    BIg_LU_X.place(x=screen_width * (45 / tk_width), y=(screen_height / 10) + (screen_height * (57 / tk_height)),
                   relx=0.01, rely=0.01)

    Big_RD_X = Entry(set, width=int(screen_width * (5 / tk_width)), relief="groove", font="Helvetica 35 bold")
    Big_RD_X.place(x=screen_width * (255 / tk_width), y=(screen_height / 10) + (screen_height * (57 / tk_height)),
                   relx=0.01, rely=0.01)

    Big_LU_Y = Entry(set, width=int(screen_width * (5 / tk_width)), relief="groove", font="Helvetica 35 bold")
    Big_LU_Y.place(x=screen_width * (45 / tk_width), y=(screen_height / 10) + (screen_height * (118 / tk_height)),
                   relx=0.01, rely=0.01)

    Big_RD_Y = Entry(set, width=int(screen_width * (5 / tk_width)), relief="groove", font="Helvetica 35 bold")
    Big_RD_Y.place(x=screen_width * (255 / tk_width), y=(screen_height / 10) + (screen_height * (118 / tk_height)),
                   relx=0.01, rely=0.01)

    ### ROI(small) X, Y Entry
    Small_LU_X = Entry(set, width=int(screen_width * (5 / tk_width)), relief="groove", font="Helvetica 35 bold")
    Small_LU_X.place(x=screen_width * (455 / tk_width), y=(screen_height / 10) + (screen_height * (57 / tk_height)),
                     relx=0.01, rely=0.01)

    Small_RD_X = Entry(set, width=int(screen_width * (5 / tk_width)), relief="groove", font="Helvetica 35 bold")
    Small_RD_X.place(x=screen_width * (665 / tk_width), y=(screen_height / 10) + (screen_height * (57 / tk_height)),
                     relx=0.01, rely=0.01)

    Small_LU_Y = Entry(set, width=int(screen_width * (5 / tk_width)), relief="groove", font="Helvetica 35 bold")
    Small_LU_Y.place(x=screen_width * (455 / tk_width), y=(screen_height / 10) + (screen_height * (118 / tk_height)),
                     relx=0.01, rely=0.01)

    Small_RD_Y = Entry(set, width=int(screen_width * (5 / tk_width)), relief="groove", font="Helvetica 35 bold")
    Small_RD_Y.place(x=screen_width * (665 / tk_width), y=(screen_height / 10) + (screen_height * (118 / tk_height)),
                     relx=0.01, rely=0.01)

    ### ROI(Big) Button
    Big_ROI_B = Button(set, text="ROI Add", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", \
                       width=int(screen_width * (15 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3,
                       padx=2, pady=2, command=add_Big_ROI)
    Big_ROI_B.place(x=screen_width * (30 / tk_width), y=screen_height * (310 / tk_height))

    Big_ROI_SC_B = Button(set, text="ROI Set Complete", font="Helvetica 10 bold", relief="raised", overrelief="solid",
                          bg="#ebebeb", \
                          width=int(screen_width * (15 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3,
                          padx=2, pady=2, command=set_comp_Big_ROI)
    Big_ROI_SC_B.place(x=screen_width * (245 / tk_width), y=screen_height * (310 / tk_height))

    ### ROI(Small) Button
    Small_ROI_B = Button(set, text="ROI Add", font="Helvetica 10 bold", relief="raised", overrelief="solid",
                         bg="#ebebeb", \
                         width=int(screen_width * (15 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3,
                         padx=2, pady=2, command=add_small_ROI)
    Small_ROI_B.place(x=screen_width * (440 / tk_width), y=screen_height * (310 / tk_height))

    Small_ROI_SC_B = Button(set, text="ROI Set Complete", font="Helvetica 10 bold", relief="raised", overrelief="solid",
                            bg="#ebebeb", \
                            width=int(screen_width * (15 / tk_width)), height=int(screen_height * (2 / tk_height)),
                            bd=3, padx=2, pady=2, command=set_comp_Small_ROI)
    Small_ROI_SC_B.place(x=screen_width * (655 / tk_width), y=screen_height * (310 / tk_height))

    ### Barcode X, Y Entry

    B_LU_X = Entry(set, width=int(screen_width * (5 / tk_width)), relief="groove", font="Helvetica 35 bold")
    B_LU_X.place(x=screen_width * (455 / tk_width), y=(screen_height / 10) + (screen_height * (387 / tk_height)),
                 relx=0.01, rely=0.01)

    B_RD_X = Entry(set, width=int(screen_width * (5 / tk_width)), relief="groove", font="Helvetica 35 bold")
    B_RD_X.place(x=screen_width * (665 / tk_width), y=(screen_height / 10) + (screen_height * (387 / tk_height)),
                 relx=0.01, rely=0.01)

    B_LU_Y = Entry(set, width=int(screen_width * (5 / tk_width)), relief="groove", font="Helvetica 35 bold")
    B_LU_Y.place(x=screen_width * (455 / tk_width), y=(screen_height / 10) + (screen_height * (448 / tk_height)),
                 relx=0.01, rely=0.01)

    B_RD_Y = Entry(set, width=int(screen_width * (5 / tk_width)), relief="groove", font="Helvetica 35 bold")
    B_RD_Y.place(x=screen_width * (665 / tk_width), y=(screen_height / 10) + (screen_height * (448 / tk_height)),
                 relx=0.01, rely=0.01)

    ### Barcode Button

    B_ROI_B = Button(set, text="Set Barcode Area", font="Helvetica 10 bold", relief="raised", overrelief="solid",
                     bg="#ebebeb", \
                     width=int(screen_width * (15 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3,
                     padx=2, pady=2, command=set_Bar_area)
    B_ROI_B.place(x=screen_width * (440 / tk_width), y=screen_height * (640 / tk_height))

    B_SC_B = Button(set, text="Reset Barcode Area", font="Helvetica 10 bold", relief="raised", overrelief="solid",
                    bg="#ebebeb", \
                    width=int(screen_width * (15 / tk_width)), height=int(screen_height * (2 / tk_height)), bd=3,
                    padx=2, pady=2, command=reset_Bar_area)
    B_SC_B.place(x=screen_width * (655 / tk_width), y=screen_height * (640 / tk_height))

    Label(set, text="Big", height=int(screen_height * (6 / tk_height)), width=int(screen_width * (5 / tk_width)),
          fg="red", relief="groove", bg="#ebebeb", font="Helvetica 11 bold") \
        .place(x=screen_width * (5 / tk_width), y=screen_height * (442 / tk_height), relx=0.01, rely=0.01)
    Label(set, text="Small", height=int(screen_height * (6 / tk_height)), width=int(screen_width * (5 / tk_width)),
          fg="red", relief="groove", bg="#ebebeb", font="Helvetica 11 bold") \
        .place(x=screen_width * (5 / tk_width), y=screen_height * (564 / tk_height), relx=0.01, rely=0.01)

    excpet_item_list = ["X", "Y", "X", "Y"]
    for i in range(len(excpet_item_list)):
        Label(set, text=excpet_item_list[i], height=int(screen_height * (4 / tk_height)),
              width=int(screen_width * (5 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 8 bold").place(x=screen_width * (60 / tk_width), y=screen_height * (437 / tk_height) + (
                    i * screen_height * (61 / tk_height)), relx=0.01, rely=0.01)
    ### Except Entry
    Big_Except_X = Entry(set, width=int(screen_width * (6 / tk_width)), relief="groove", font="Helvetica 35 bold")
    Big_Except_X.place(x=screen_width * (100 / tk_width),
                       y=screen_height * (437 / tk_height) + (screen_height * (0 / tk_height)), relx=0.01, rely=0.01)

    Big_Except_Y = Entry(set, width=int(screen_width * (6 / tk_width)), relief="groove", font="Helvetica 35 bold")
    Big_Except_Y.place(x=screen_width * (100 / tk_width),
                       y=screen_height * (437 / tk_height) + (screen_height * (61 / tk_height)), relx=0.01, rely=0.01)

    Small_Except_X = Entry(set, width=int(screen_width * (6 / tk_width)), relief="groove", font="Helvetica 35 bold")
    Small_Except_X.place(x=screen_width * (100 / tk_width),
                         y=screen_height * (437 / tk_height) + (screen_height * (122 / tk_height)), relx=0.01,
                         rely=0.01)

    Small_Except_Y = Entry(set, width=int(screen_width * (6 / tk_width)), relief="groove", font="Helvetica 35 bold")
    Small_Except_Y.place(x=screen_width * (100 / tk_width),
                         y=screen_height * (437 / tk_height) + (screen_height * (183 / tk_height)), relx=0.01,
                         rely=0.01)

    ### Except Button
    Big_Except_B = Button(set, text="Add", font="Helvetica 10 bold", relief="raised", overrelief="solid",
                          bg="#ebebeb", \
                          width=int(screen_width * (6 / tk_width)), height=int(screen_height * (5 / tk_height)), bd=3,
                          padx=2, pady=2, command=add_except_big_area)
    Big_Except_B.place(x=screen_width * (270 / tk_width), y=screen_height * (460 / tk_height))

    Small_Except_B = Button(set, text="Add", font="Helvetica 10 bold", relief="raised", overrelief="solid",
                            bg="#ebebeb", \
                            width=int(screen_width * (6 / tk_width)), height=int(screen_height * (5 / tk_height)), bd=3,
                            padx=2, pady=2, command=add_except_small_area)
    Small_Except_B.place(x=screen_width * (270 / tk_width), y=screen_height * (580 / tk_height))

    Big_Except_SC_B = Button(set, text="Setting\nComplete", font="Helvetica 10 bold", relief="raised", overrelief="solid",
                             bg="#ebebeb", \
                             width=int(screen_width * (7 / tk_width)), height=int(screen_height * (5 / tk_height)),
                             bd=3, padx=2, pady=2, command=set_comp_big_except)
    Big_Except_SC_B.place(x=screen_width * (335 / tk_width), y=screen_height * (460 / tk_height))

    Small_Except_SC_B = Button(set, text="Setting\nComplete", font="Helvetica 10 bold", relief="raised", overrelief="solid",
                               bg="#ebebeb", \
                               width=int(screen_width * (7 / tk_width)), height=int(screen_height * (5 / tk_height)),
                               bd=3, padx=2, pady=2, command=set_comp_small_except)
    Small_Except_SC_B.place(x=screen_width * (335 / tk_width), y=screen_height * (580 / tk_height))


def main():
    global root, cam1_label
    global RV_SN, RV_TIME, RV_ACC, RV_PASS, RV_NG, RV_TACT
    # global SN_label
    # global image_label, set, datapath_local

    root = Tk()
    root.iconbitmap("aceantenna.ico")

    root.bind('<Escape>', lambda e: root.quit())
    root.bind("<Double-Button-1>", mouse_position)
    # root.bind("<Motion>", mouse_position)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    tk_width, tk_height = 1920, 1080

    cam1_label = Label(root)
    cam1_label.place(x=screen_width * (10 / tk_width), y=screen_height * (10 / tk_height))

    logo_label = Label(root)
    logo_label.place(x=screen_width * (10 / tk_width), y=screen_height * (10 / tk_height))


    root.title("Air3239 Check Rivet")
    root.geometry("{}x{}+{}+{}".format(screen_width, screen_height, -10, 0))

    name = ["Serial\nNumber", "Time", "No. of\nAccumulation",
            "No. of\nOK", "No. of\nNG", "Tact Time", ]

    ##정보 Label 생성
    for i in range(len(name)):
        Label(root, text=name[i], height=int(screen_height * (5 / tk_height)),
              width=int(screen_width * (17 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 9 bold") \
            .place(x=screen_width * (95 / tk_width),
                   y=(screen_height / 3) + screen_height * (140 / tk_height) + (i * screen_height * (80 / tk_height)),
                   relx=0.01, rely=0.01)

    Label(root, text="Rivet \nDetect Info", height=int(screen_height * (25 / tk_height)),
          width=int(screen_width * (11 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=-14, y=(screen_height / 3) + screen_height * (140 / tk_height) + (
                0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    Label(root, height=int(screen_height * (25 / tk_height)), width=int(screen_width * (90 / tk_width)), fg="red",
          relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=screen_width * (970 / tk_width),
                                          y=(screen_height / 3) + screen_height * (140 / tk_height) + (
                                                      0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    Label(root, text="Open folder", height=int(screen_height * (5 / tk_height)),
          width=int(screen_width * (13 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=screen_width * (970 / tk_width),
                                          y=(screen_height / 3) + screen_height * (140 / tk_height) + (
                                                      0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    Label(root, text="Barcode Image", height=int(screen_height * (5 / tk_height)),
          width=int(screen_width * (13 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=screen_width * (970 / tk_width),
                                          y=(screen_height / 3) + screen_height * (270 / tk_height) + (
                                                      0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    Label(root, text="Result", height=int(screen_height * (5 / tk_height)),
          width=int(screen_width * (13 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
          font="Helvetica 13 bold").place(x=screen_width * (1550 / tk_width),
                                          y=(screen_height / 3) + screen_height * (270 / tk_height) + (
                                                      0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    MF_name_list = ["PASS", "FAIL", "LOG"]
    for i in range(len(MF_name_list)):
        Label(root, text=MF_name_list[i], height=int(screen_height * (4 / tk_height)),
              width=int(screen_width * (10 / tk_width)), fg="red", relief="groove", bg="#ebebeb",
              font="Helvetica 12 bold") \
            .place(x=screen_width * (1160 / tk_width) + (i * 230),
                   y=(screen_height / 3) + screen_height * (150 / tk_height), relx=0.01, rely=0.01)

    Button(root, text="Open\nPass Folder", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=int(screen_width * (10 / tk_width)), height=int(screen_height * (4 / tk_height)), bd=3, padx=2, pady=2,
           command=open_folder_pass) \
        .place(x=screen_width * (1290 / tk_width) + (0 * 230),
               y=(screen_height / 3) + screen_height * (161 / tk_height) + (0 * screen_height * (80 / tk_height)))

    Button(root, text="Open\nFail Folder", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=int(screen_width * (10 / tk_width)), height=int(screen_height * (4 / tk_height)), bd=3, padx=2, pady=2,
           command=open_folder_ng) \
        .place(x=screen_width * (1290 / tk_width) + (1 * 230),
               y=(screen_height / 3) + screen_height * (161 / tk_height) + (0 * screen_height * (80 / tk_height)))

    Button(root, text="Open\nLog Folder", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=int(screen_width * (10 / tk_width)), height=int(screen_height * (4 / tk_height)), bd=3, padx=2, pady=2,
           command=open_folder_log) \
        .place(x=screen_width * (1290 / tk_width) + (2 * 230),
               y=(screen_height / 3) + screen_height * (161 / tk_height) + (0 * screen_height * (80 / tk_height)))

    Button(root, text="Rotate\n-90 degree", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=int(screen_width * (10 / tk_width)), height=int(screen_height * (4 / tk_height)), bd=3, padx=2, pady=2,
           command=roate_left) \
        .place(x=screen_width * (1150 / tk_width), y=(screen_height / 3) + screen_height * (290 / tk_height))

    Button(root, text="Rotate\n90 degree", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=int(screen_width * (10 / tk_width)), height=int(screen_height * (4 / tk_height)), bd=3, padx=2, pady=2,
           command=roate_right) \
        .place(x=screen_width * (1250 / tk_width), y=(screen_height / 3) + screen_height * (290 / tk_height))

    RV_SN = Entry(root, width=int(screen_width * (19 / tk_width)), relief="groove", font="Helvetica 50 bold")
    RV_SN.place(x=screen_width * (218 / tk_width),
                y=(screen_height / 3) + screen_height * (140 / tk_height) + (0 * screen_height * (80 / tk_height)),
                relx=0.01, rely=0.01)

    RV_TIME = Entry(root, width=int(screen_width * (19 / tk_width)), relief="groove", font="Helvetica 50 bold")
    RV_TIME.place(x=screen_width * (218 / tk_width),
                  y=(screen_height / 3) + screen_height * (140 / tk_height) + (1 * screen_height * (80 / tk_height)),
                  relx=0.01, rely=0.01)

    RV_ACC = Entry(root, width=int(screen_width * (19 / tk_width)), relief="groove", font="Helvetica 50 bold")
    RV_ACC.place(x=screen_width * (218 / tk_width),
                 y=(screen_height / 3) + screen_height * (140 / tk_height) + (2 * screen_height * (80 / tk_height)),
                 relx=0.01, rely=0.01)

    RV_PASS = Entry(root, width=int(screen_width * (19 / tk_width)), relief="groove", font="Helvetica 50 bold")
    RV_PASS.place(x=screen_width * (218 / tk_width),
                  y=(screen_height / 3) + screen_height * (140 / tk_height) + (3 * screen_height * (80 / tk_height)),
                  relx=0.01, rely=0.01)

    RV_NG = Entry(root, width=int(screen_width * (19 / tk_width)), relief="groove", font="Helvetica 50 bold")
    RV_NG.place(x=screen_width * (218 / tk_width),
                y=(screen_height / 3) + screen_height * (140 / tk_height) + (4 * screen_height * (80 / tk_height)),
                relx=0.01, rely=0.01)

    RV_TACT = Entry(root, width=int(screen_width * (19 / tk_width)), relief="groove", font="Helvetica 50 bold")
    RV_TACT.place(x=screen_width * (218 / tk_width),
                  y=(screen_height / 3) + screen_height * (140 / tk_height) + (5 * screen_height * (80 / tk_height)),
                  relx=0.01, rely=0.01)

    setting_window()
    read_frame()

    root.mainloop()


if __name__ == "__main__":
    main()

