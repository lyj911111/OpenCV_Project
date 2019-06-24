# 왜곡된 이미지를 쭉 펼치는 테스트

import cv2
import numpy as np

img = cv2.imread('hough.jpg')
rows, cols, ch = img.shape

a = [[65,15],[481,13],[28,439],[508,445]]
b = [[0, 0],[1000, 0],[0,500],[1000,500]]   # 왼쪽위점, 오른쪽위점, 왼쪽아래점, 오른쪽아래점

pts1 = np.float32(a)
pts2 = np.float32(b)

img = cv2.circle(img, (a[0][0], a[0][1]), 3, (0,0,255),-1)
img = cv2.circle(img, (a[1][0], a[1][1]), 3, (0,0,255),-1)
img = cv2.circle(img, (a[2][0], a[2][1]), 3, (0,0,255),-1)
img = cv2.circle(img, (a[3][0], a[3][1]), 3, (0,0,255),-1)
#cv2.circle(img, c, 5, (55, 255, 55), -1)

M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M, (1000, 500))  # 변환후 크기 (x좌표, y좌표)

cv2.imshow('imgage',img)
cv2.imshow('dst', dst)
cv2.waitKey(0)