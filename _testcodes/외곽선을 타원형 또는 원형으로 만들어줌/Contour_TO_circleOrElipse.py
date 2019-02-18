# 윤곽선 찾기 -> 윤곽선을 원 or 타원으로 만듬

import cv2
import numpy as np

# Canny를 위한 외곽선 탐지를 위한 필터.
lower = 84
upper = 200

# 테스트할 이미지를 불러오기, img1 으로 불러오기 , img2 으로 복사 , img는 Gray로 변환.
img1 = cv2.imread('det.jpg', 1)
img2 = img1.copy()
img = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

# Blur처리함.
img = cv2.GaussianBlur(img,(5, 5),0)

# 외곽선 탐지를 위해 cv2.Canny 함수를 사용. (불러온이미지, min 값, max 값)
edges = cv2.Canny(img, lower, upper)

# 찾은 영역범위에 외곽선을 그려줌.
_, contours , _= cv2.findContours(edges, cv2.RETR_TREE, 1)
rep = cv2.drawContours(img1, contours, -1, (0,255,0), 3)

# 외곽선을 원형 형태로 바꾸어줌. (원 또는 타원)
for i in range(0, len(contours)):
    ellipse = cv2.fitEllipse(contours[i])
    (center, axes, orientation) = ellipse
    majoraxis_length = max(axes)
    minoraxis_length = min(axes)
    eccentricity=(np.sqrt(1-(minoraxis_length / majoraxis_length)**2))
    cv2.ellipse(img2,ellipse,(0,0,255),2)

# 엣지 검출한것.
cv2.imshow('Edges', edges )
# 외곽선 표시한 것.
cv2.imshow('contours',rep)
# 타원으로 만든 것.
cv2.imshow('Detected ellipse', img2)

cv2.waitKey(0)