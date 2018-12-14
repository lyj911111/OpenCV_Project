import cv2
import numpy as np
import sys
import time
import pyzbar.pyzbar as pyzbar
from matplotlib import pyplot as plt



x = 3  # 바코드 확대 배율

img_ori = cv2.imread('barcode.jpg', cv2.IMREAD_UNCHANGED)  #바코드 원본 저장.
img_gray = cv2.imread('barcode.jpg', cv2.IMREAD_GRAYSCALE) #바코드 Gray로 저장.

img_mark = cv2.circle(img_ori, (111, 262), 3, (0, 0, 255), -1)  # 모서리의 위치를 찾음 점으로 표시.
img_mark = cv2.circle(img_ori, (111, 378), 3, (0, 0, 255), -1)
img_mark = cv2.circle(img_ori, (365, 374), 3, (0, 0, 255), -1)
img_mark = cv2.circle(img_ori, (367, 269), 3, (0, 0, 255), -1)

pts1 = np.float32([[111, 262], [367, 269], [111, 378], [365, 374]])  # 사진에서 바코드 4지점을 따옴
pts2 = np.float32([[0, 0], [255*x, 0], [0, 110*x], [255*x, 110*x]])  # 바코드의 크기를 x2로 키움.
M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img_gray, M, (255*x, 110*x))              # x2 로 키운 바코드를 Gray로 저장.

_, thresh = cv2.threshold(dst, 106, 255, cv2.THRESH_BINARY_INV)

#외곽선 필터링 사용안함
#laplacian = cv2.Laplacian(thresh, cv2.CV_64F)
#sobelx = cv2.Sobel(thresh, cv2.CV_64F, 1, 0, ksize=3)

#cv2.imshow('dot_mark', img_mark)
#cv2.imshow('gray', img_gray)
#cv2.imshow('pyR', temp)

cv2.imshow('dst', dst)
cv2.imshow('thresh', thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()
