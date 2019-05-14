'''
 Based on the following tutorial:
   http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_calib3d/py_depthmap/py_depthmap.html
'''

import numpy as np
import cv2

# Load the left and right images in gray scale
imgLeft = cv2.imread('./33.png', 0)
imgRight = cv2.imread('./44.png', 0)

# Initialize the stereo block matching object / 변수 numDisparities : 16으로 나누어 떨어지는 수, 변수 blockSize: 홀수
stereo = cv2.StereoBM_create(numDisparities=92, blockSize=19)   # 사진 11,22 는 parameter: 32,19

# Compute the disparity image
disparity = stereo.compute(imgLeft, imgRight)

# Normalize the image for representation
min = disparity.min()
max = disparity.max()
disparity = np.uint8(255 * (disparity - min) / (max - min))

# Display the result
cv2.imshow('disparity', np.hstack((imgLeft, imgRight, disparity)))
cv2.waitKey(0)
cv2.destroyAllWindows()