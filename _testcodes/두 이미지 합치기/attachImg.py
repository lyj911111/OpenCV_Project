'''
    참고 링크: https://copycoding.tistory.com/159
'''

import cv2
import numpy as np

# 사이즈 조절 W, H
size = (1280, 960)

# 좌우 이미지 불러오기
leftimg = cv2.imread('1.bmp')
rightimg = cv2.imread('2.bmp')

# 사이즈 조정
leftimg = cv2.resize(leftimg, size)
rightimg = cv2.resize(rightimg, size)

# 이미지 좌우 합치기
add_img = np.hstack((leftimg, rightimg))

cv2.imshow('leftimg', leftimg)
cv2.imshow('rightimg', rightimg)
cv2.imshow('add_img', add_img)

cv2.waitKey(0)

