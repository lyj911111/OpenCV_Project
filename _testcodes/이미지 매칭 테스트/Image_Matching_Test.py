import cv2
import numpy as np
from matplotlib import pyplot as plt

List = []

# 원본 불러오기.
img_rgb = cv2.imread('2.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)  # gray로 변환.
result = img_rgb.copy()                               # 결과출력을 위한 원본 복사


# 이미지 매칭할 template 불러옴. (2개의 template으로 이미지 매칭)
template1 = cv2.imread('template1.jpg',0)
template2 = cv2.imread('template2.jpg',0)


# 매칭할 template의 가로, 세로 사이즈를 return
w1, h1 = template1.shape[::-1]
w2, h2 = template2.shape[::-1]


# 1번째 template 매칭.
res1 = cv2.matchTemplate(img_gray,template1,cv2.TM_CCOEFF_NORMED)
# 이미지 매칭률을 결정함.
threshold = 0.75
loc = np.where(res1 >= threshold)

cnt = 0
for pt in zip(*loc[::-1]):
    cnt = cnt + 1
    if cnt > 6:    # 매칭률에 따라 사격형을 표시할 때, 6회 이하인 경우는 제외, 그 이상일때만 허용.
        cv2.rectangle(result, pt, (pt[0] + w1, pt[1] + h1), (0,0,255), 1)
        #List.append([pt, (pt[0] + w1, pt[1] + h1)])


# 2번째 template 매칭.
res2 = cv2.matchTemplate(img_gray,template2,cv2.TM_CCOEFF_NORMED)
# 이미지 매칭률을 결정함.
threshold = 0.76
loc = np.where(res2 >= threshold)

cnt = 0
for pt in zip(*loc[::-1]):
    cnt = cnt + 1
    if cnt > 5:
        cv2.rectangle(result, pt, (pt[0] + w2, pt[1] + h2), (0,255,0), 1)

#print(List)

cv2.imshow('res.png',result)
cv2.waitKey(0)