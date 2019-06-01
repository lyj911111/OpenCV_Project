'''
    Link : http://blog.naver.com/PostView.nhn?blogId=samsjang&logNo=220664036092&parentCategoryNo=&categoryNo=66&viewDate=&isShowPopularPosts=false&from=postList
    배경을 지우고 움직임을 탐지하는 코드

'''

import numpy as np
import cv2

def backSubtraction():
    cap = cv2.VideoCapture(0)
    #mog = cv2.bgsegm.createBackgroundSubtractorMOG()
    #mog = cv2.createBackgroundSubtractorMOG2()

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

    while True:
        ret, frame = cap.read()
        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        cv2.imshow('mask', fgmask)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break


backSubtraction()
