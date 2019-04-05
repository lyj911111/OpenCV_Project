# 왜곡된 이미지를 쭉 펼치는 테스트

import cv2
import numpy as np

# img = cv2.imread('hough.jpg')


# 이미지 불러오기
img = cv2.imread('./img/new_default.bmp')

rows, cols, ch = img.shape
print("이미지의 크기:", rows, "x", cols)

# Resize 시킬 이미지크기 [x y]
set_imgsize = [1280, 960]
a = [[500, 120], [4135, 100], [505, 3165], [4155, 3150]]    # 이미지 펼칠 지점
b = [[0, 0], [set_imgsize[0], 0], [0, set_imgsize[1]], [set_imgsize[0], set_imgsize[1]]]              # 펼친 이미지 넓이값 1200 x 900 의 크기로

pts1 = np.float32(a)
pts2 = np.float32(b)

img = cv2.circle(img, (a[0][0], a[0][1]), 3, (0, 0, 255), -1)
img = cv2.circle(img, (a[1][0], a[1][1]), 3, (0, 0, 255), -1)
img = cv2.circle(img, (a[2][0], a[2][1]), 3, (0, 0, 255), -1)
img = cv2.circle(img, (a[3][0], a[3][1]), 3, (0, 0, 255), -1)

M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M, (set_imgsize[0], set_imgsize[1]))

cv2.imshow('imgage',img)    # 원본
cv2.imshow('dst', dst)      # 이미지 편집 후
cv2.waitKey(0)