import cv2
import numpy as np
from matplotlib import pyplot as plt

# before_point (이전좌표)
bfr_pt = 0

# 검출할 영역(관심영역)을 지정 (start point to end point).
s_pt = (500, 30)
e_pt = (900, 900)

# 확률이 떨어지는 이하 매칭률을 제외
min = 0


# 원본 불러오기.
img_rgb = cv2.imread('2.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)  # gray로 변환.
result = img_rgb.copy()                               # 결과출력을 위한 원본 복사

result = cv2.rectangle(result, s_pt, e_pt, (255, 0, 0), 2)

# 이미지 매칭할 template 불러옴. (2개의 template으로 이미지 매칭)
template1 = cv2.imread('template1.jpg',0)
template2 = cv2.imread('template2.jpg',0)


# 매칭할 template의 가로, 세로 사이즈를 return
w1, h1 = template1.shape[::-1]
w2, h2 = template2.shape[::-1]


# 1번째 template 매칭.
res1 = cv2.matchTemplate(img_gray,template1,cv2.TM_CCOEFF_NORMED)
# 이미지 매칭률을 결정함.
threshold = 0.7
loc = np.where(res1 >= threshold)

cnt = 0
cnt_list = []
for pt in zip(*loc[::-1]):

    if cnt == 0:
        cnt_list = []

    if (pt[0] > s_pt[0] and pt[1] > s_pt[1]) and ((pt[0] + w1 < e_pt[0]) and (pt[1] + h1 < e_pt[1])):       # 관심영역(ROI)으로 판독 제한.

        cnt = cnt + 1           # 매칭률에 따라 얼마나 매칭시켰는지 갯수를 셈.
        str_cnt = str(cnt)

        # 매칭률에 따라 사각형을 표시할 때, min 회 이하인 경우는 제외, 그 이상일때만 허용. (아무거나 다 잡히는 것을 제외하기 위함)
        if cnt > min:

            cv2.rectangle(result, pt, (pt[0] + w1, pt[1] + h1), (0, 0, 255), 1)     # 판독위치 마킹.
            cnt_list.append(cnt)
            max_cnt = str(max(cnt_list))        # 판독 갯수 중 최대값 저장.

            print(cnt_list)
            print(max_cnt)

            # 초기에 before_point가 없으므로 있을경우에 if문 진입.
            if bfr_pt:

                # y좌표가 급격히 변하는 부분일때.
                if (abs(bfr_pt[1] - pt[1]) > 10) or (abs(bfr_pt[0] - pt[0]) > 10) :
                    str_cnt = str(cnt)
                    cv2.putText(result, 'match:' + max_cnt, bfr_pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
                    print("ok!!!")
                    cnt = 0
                    k = 0

        bfr_pt = pt
cv2.putText(result, 'match:' + max_cnt, bfr_pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)




# 2번째 template 매칭.
res2 = cv2.matchTemplate(img_gray,template2,cv2.TM_CCOEFF_NORMED)
# 이미지 매칭률을 결정함.
threshold = 0.80
loc = np.where(res2 >= threshold)

cnt = 0
for pt in zip(*loc[::-1]):

    if pt < e_pt and (pt[0] + w1, pt[1] + h1) > s_pt:  # 관심영역으로 판독 제한.

        cnt = cnt + 1
        if cnt > 5:
            cv2.rectangle(result, pt, (pt[0] + w2, pt[1] + h2), (0,255,0), 1)


cv2.imshow('res.png',result)
cv2.waitKey(0)