import cv2
from more_itertools import unique_everseen
import numpy as np


'''
##폴더 경로 설정
from tkinter import filedialog
from tkinter import *

root = Tk()
root.dirName = filedialog.askdirectory();
data_path = root.dirName
print(data_path)


### 폴더 열기
import os
path="D:\workspace\AceVision\Samsung\AAA"
path=os.path.realpath(path)
os.startfile(path)

'''


'''
from more_itertools import unique_everseen  # pip install more_itertools==4.3.0
import copy


list1 = [[10, 20], [30, 40], [50, 60], [423, 34], [234, 876], [5, 5]]
list2 = [[10, 20], [30, 40], [50, 60], [423, 34], [587, 333]]
list3 = []


list3 = copy.deepcopy(list1)

for i in list2:
    for j in list1:
        if i == j:
            list3.remove(i)


print(list3)


list4 = [1,2,3,4,5]

del list4[0]
print(list4)

'''

'''
import cv2
import numpy as np

img = cv2.imread('C:/AceVision/abcde.png', cv2.IMREAD_COLOR)

print(img[745, 652])
'''

'''

list1 = [[10,20], [30, 40], [50, 60]]
list2 = [[70, 80], [90, 100]]
list3 = list1+list2
print(list3)

'''

'''
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

img = cv2.imread('C:/AceVision/2019-03-21/rivet\pass/61000163006321.png')


img = Rotate(img, 0)
img_1 = Rotate(img, -1)
img_2 = Rotate(img, -2)
img_3 = Rotate(img, -3)

#cv2.imshow("img", img)
#cv2.imshow("img_1", img_1)
cv2.imshow("img_2", img_2)
cv2.imshow("img_3", img_3)

cv2.waitKey(0)
cv2.destroyAllWindows()
'''





import numpy as np
import cv2

'''
cap1 = cv2.VideoCapture(1)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 4608)  # Width 4608
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 3288)  # Height 3288

while True:
    ret, img = cap1.read()
    img = cv2.resize(img, (1280, 960), interpolation=cv2.INTER_LINEAR)

    img1 = img.copy()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)




    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
cv2.destroyAllWindows()
'''


import numpy as np                          # pip install numpy==1.15.4
import cv2                                  # pip install opencv-python==3.4.4.19
from PIL import Image as Img                # pip install image==1.5.27
import pyzbar.pyzbar as pyzbar              # pip install pyzbar==0.1.7
from more_itertools import unique_everseen  # pip install more_itertools==4.3.0
import serial                               # pip install pyserial==3.4
from PIL import ImageTk
from math import *
import datetime
import time
import os
from tkinter import filedialog
from tkinter import *
import socket
import copy
from pylibdmtx.pylibdmtx import decode


def decode(im):
    global Serial_No, pre_Serial_No
    # global RV_SN, RV_TIME, RV_ACC, RV_PASS, RV_NG, RV_TACT

    im = Reformat_Image(im, 2, 2)
    decodedObjects = str(pyzbar.decode(im))  # 바코드와 QR코드를 찾아냄
    print("decodedObjects", decodedObjects)
    Serial_No = decodedObjects[16:29]
    print(Serial_No, len(Serial_No))
    return len(Serial_No)


def Reformat_Image(image, ratio_w, ratio_h):
    height, width = image.shape[:2]
    width = int(width*ratio_w)
    height = int(height*ratio_h)
    #res = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    res = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

    return res

a = 3

img = cv2.imread('C:/AceVision/barcode13.png')

while True:
    img = Reformat_Image(img, a, a)
    lens = decode(img)
    a += 0.1
    if lens != 0:
        print(Serial_No)
        break




