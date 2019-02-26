import cv2
import numpy as np
import time
from matplotlib import pyplot as plt

# 카메라 불러오기, 해상도 지정.
cap0 = cv2.VideoCapture(0)
cap0.set(3, 4608)
cap0.set(4, 3288)
print("현재 해상도 %d x %d" %(cap0.get(3), cap0.get(4)))

cap1 = cv2.VideoCapture(1)
cap1.set(3, 4608)
cap1.set(4, 3288)
print("현재 해상도 %d x %d" %(cap0.get(3), cap0.get(4)))

# 검출할 영역(관심영역)을 지정 (start point to end point of Rectangle Box).
s_pt = (500, 30)
e_pt = (900, 900)

# before_point (이전좌표)
bfr_pt = 0

# 메인실행 함수.
def execute():
    global bfr_pt

    # 프레임 불러오기.
    #img_rgb = cv2.imread('2.png')
    while True:

        ret, frame = cap1.read()
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # gray로 변환.
        result = frame.copy()                               # 결과출력을 위한 원본 복사

        # 관심영역(ROI, Range of Interest) 지정.
        result = cv2.rectangle(result, s_pt, e_pt, (255, 0, 0), 2)
        cv2.putText(result, 'ROI', s_pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # 이미지 매칭할 template 불러옴. (2개의 template으로 이미지 매칭)
        template1 = cv2.imread('template1.jpg',0)
        template2 = cv2.imread('template2.jpg',0)


        # 매칭할 template의 가로, 세로 사이즈를 return
        w1, h1 = template1.shape[::-1]
        w2, h2 = template2.shape[::-1]


        # 1번째 template 매칭.
        res1 = cv2.matchTemplate(img_gray, template1, cv2.TM_CCOEFF_NORMED)
        # 이미지 매칭률을 결정함.
        threshold = 0.7
        loc = np.where(res1 >= threshold)

        print("loc?", loc)

        try:
            cnt = 0
            cnt_list = []
            for pt in zip(*loc[::-1]):

                if cnt == 0:
                    cnt_list = []

                if (pt[0] > s_pt[0] and pt[1] > s_pt[1]) and ((pt[0] + w1 < e_pt[0]) and (pt[1] + h1 < e_pt[1])):       # 관심영역(ROI)으로 판독 제한.

                    cnt = cnt + 1           # 매칭률에 따라 얼마나 매칭시켰는지 갯수를 셈.

                    cv2.rectangle(result, pt, (pt[0] + w1, pt[1] + h1), (255, 255, 0), 1)     # 판독위치 마킹.
                    cnt_list.append(cnt)
                    max_cnt = str(max(cnt_list))        # 판독 갯수 중 최대값 저장.

                    # 초기에 before_point가 없으므로 있을경우에 if문 진입.
                    if bfr_pt:

                        # y좌표가 급격히 변하는 부분일때.
                        if (abs(bfr_pt[1] - pt[1]) > 10) or (abs(bfr_pt[0] - pt[0]) > 10) :
                            cv2.putText(result, 'match:' + max_cnt, bfr_pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1, cv2.LINE_AA)
                            cnt = 0
                    bfr_pt = pt
            cv2.putText(result, 'match:' + max_cnt, bfr_pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1, cv2.LINE_AA)
        except:
            pass

        #
        # # 2번째 template 매칭.
        # res2 = cv2.matchTemplate(img_gray,template2,cv2.TM_CCOEFF_NORMED)
        # # 이미지 매칭률을 결정함.
        # threshold = 0.75
        # loc = np.where(res2 >= threshold)
        #
        # cnt = 0
        # cnt_list = []
        # for pt in zip(*loc[::-1]):
        #
        #     if cnt == 0:
        #         cnt_list = []
        #
        #     if (pt[0] > s_pt[0] and pt[1] > s_pt[1]) and (
        #             (pt[0] + w2 < e_pt[0]) and (pt[1] + h2 < e_pt[1])):  # 관심영역(ROI)으로 판독 제한.
        #
        #         cnt = cnt + 1  # 매칭률에 따라 얼마나 매칭시켰는지 갯수를 셈.
        #
        #         cv2.rectangle(result, pt, (pt[0] + w2, pt[1] + h2), (0, 255, 0), 1)  # 판독위치 마킹.
        #         cnt_list.append(cnt)
        #         max_cnt = str(max(cnt_list))  # 판독 갯수 중 최대값 저장.
        #
        #         # 초기에 before_point가 없으므로 있을경우에 if문 진입.
        #         if bfr_pt:
        #
        #             # y좌표가 급격히 변하는 부분일때.
        #             if (abs(bfr_pt[1] - pt[1]) > 10) or (abs(bfr_pt[0] - pt[0]) > 10):
        #                 cv2.putText(result, 'match:' + max_cnt, bfr_pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
        #                 cnt = 0
        #         bfr_pt = pt
        # cv2.putText(result, 'match:' + max_cnt, bfr_pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)

        # 화면 크기 조절
        result = cv2.resize(result, (640 * 2, 480 * 2), interpolation=cv2.INTER_LINEAR)

        #cv2.namedWindow('window title', cv2.WINDOW_NORMAL)
        #cv2.imshow('window title', img_gray)
        cv2.imshow('res.png', result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":

    #카메라 번호 선택 0~2
    execute()