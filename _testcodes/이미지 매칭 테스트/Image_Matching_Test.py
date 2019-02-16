import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread('2.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('template.jpg',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

# 이미지 매칭률을 결정함.
threshold = 0.75

loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    list = []
    list.append((pt, (pt[0] + w, pt[1] + h)))

print(list)


cv2.imshow('res.png',img_rgb)
cv2.waitKey(0)