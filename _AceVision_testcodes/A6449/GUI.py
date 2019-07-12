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

# 데이터를 저장할 위치(서버저장)
store_local_location = "D:/Air3239/"
store_server_location = "//192.168.105.4/Multimedia/Air3239/"
Serial_No = ''
pre_Serial_No = '1'
PLC_rx = 'ready'
PLC_tx_OK = '1'
PLC_tx_NG = '2'
protocol = 0
port_num = ''
PLC_ready = ''

check_barcode_area = 0
check_year = 0
check_month = 0
check_day = 0
check_make_folder = 0
check_result = 0
pre_day = 0

cap = cv2.VideoCapture(0)
# cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 4024)  # Width 4024
# cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 3036)  # Height 3036
print("카메라 현재 해상도 %d x %d" %(cap.get(3), cap.get(4)))


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

def read_frame():
    global cam1_label

    webCamShow(cap.read(), cam1_label, 0)
    root.after(20, read_frame)                # ms단위로 프레임을 읽음.

def main():
    global root, cam1_label

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

    # 1st 라인 라벨
    Label(root, text="Information", height=int(screen_height * (25 / tk_height)), width=int(screen_width * (11 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 13 bold").place(x=-14, y=(screen_height / 3) + screen_height * (140 / tk_height) + (0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 2nd 라인 라벨 정보 Label 생성
    name = ["Serial\nNumber", "Time", "No. of\nAccumulation", "No. of\nOK", "No. of\nNG", "Tact Time", ]    # 라벨 타이틀
    for i in range(len(name)):
        Label(root, text=name[i], height=int(screen_height * (5 / tk_height)), width=int(screen_width * (17 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 9 bold").place(x=screen_width * (95 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (i * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 3rd 라인 Text입력 상자 (2nd의 name 라벨의 갯수에 따라 달라짐)
    for i in range(len(name)):
        RV_SN = Entry(root, width=int(screen_width * (19 / tk_width)), relief="groove", font="Helvetica 50 bold")
        RV_SN.place(x=screen_width * (218 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (i * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 4th 오른쪽 전체박스 생성
    Label(root, height=int(screen_height * (25 / tk_height)), width=int(screen_width * (90 / tk_width)), relief="groove", bg="#ebebeb", font="Helvetica 13 bold").place(x=screen_width * (970 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 5th Open folder 라벨 생성
    Label(root, text="Open folder", height=int(screen_height * (5 / tk_height)), width=int(screen_width * (13 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 13 bold").place(x=screen_width * (970 / tk_width), y=(screen_height / 3) + screen_height * (140 / tk_height) + (0 * screen_height * (80 / tk_height)), relx=0.01, rely=0.01)

    # 6th 하위 목록 라벨 생성 pass, fail, log
    MF_name_list = ["PASS", "FAIL", "LOG"]
    for i in range(len(MF_name_list)):
        Label(root, text=MF_name_list[i], height=int(screen_height * (4 / tk_height)), width=int(screen_width * (10 / tk_width)), fg="red", relief="groove", bg="#ebebeb", font="Helvetica 12 bold").place(x=screen_width * (1160 / tk_width) + (i * 230), y=(screen_height / 3) + screen_height * (150 / tk_height), relx=0.01, rely=0.01)

    # 7th 3개의 버튼 생성
    Button(root, text="Open\nPass Folder", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", width=int(screen_width * (10 / tk_width)), height=int(screen_height * (4 / tk_height)), bd=3, padx=2, pady=2,command=open_folder_pass).place(x=screen_width * (1290 / tk_width) + (0 * 230), y=(screen_height / 3) + screen_height * (161 / tk_height) + (0 * screen_height * (80 / tk_height)))
    Button(root, text="Open\nFail Folder", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", width=int(screen_width * (10 / tk_width)), height=int(screen_height * (4 / tk_height)), bd=3, padx=2, pady=2,command=open_folder_ng).place(x=screen_width * (1290 / tk_width) + (1 * 230), y=(screen_height / 3) + screen_height * (161 / tk_height) + (0 * screen_height * (80 / tk_height)))
    Button(root, text="Open\nLog Folder", font="Helvetica 10 bold", relief="raised", overrelief="solid", bg="#ebebeb", width=int(screen_width * (10 / tk_width)), height=int(screen_height * (4 / tk_height)), bd=3, padx=2, pady=2,command=open_folder_log).place(x=screen_width * (1290 / tk_width) + (2 * 230), y=(screen_height / 3) + screen_height * (161 / tk_height) + (0 * screen_height * (80 / tk_height)))



    read_frame()        # 연속Frame loop
    root.mainloop()     # Gui를 가동시키는 loop

if __name__ == "__main__":
    main()