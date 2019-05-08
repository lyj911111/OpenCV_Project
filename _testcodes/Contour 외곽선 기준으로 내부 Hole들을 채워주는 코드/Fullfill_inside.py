'''
    Threshold 내부에 빈공간(Hole)을 가득 체워주는 코드
    외부의 Contour를 기준으로 내부는 모두 체워버림.
    참고 링크: https://www.learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/
'''

import cv2
import numpy as np

# 이미지 읽기
#im_in = cv2.imread('inside.PNG', cv2.IMREAD_GRAYSCALE);
im_in = cv2.imread('inside.PNG')

# 내부 체움 함수.
def fullfill_inside(im_in):

    im_in = cv2.cvtColor(im_in, cv2.COLOR_BGR2GRAY)     # 바이너리 이미지 일 경우 필요 없음.
    im_in = cv2.bitwise_not(im_in)                      # 비트 반전

    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255.

    th, im_th = cv2.threshold(im_in, 220, 255, cv2.THRESH_BINARY_INV);
    cv2.imshow('im_th', im_th)

    # Threshold 이미지 복사.
    im_floodfill = im_th.copy()
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255);

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv                           # ***

    # Display images.
    # 이미지 프로세싱 과정 디스플레이
    cv2.imshow("Thresholded Image", im_th)
    cv2.imshow("Floodfilled Image", im_floodfill)
    cv2.imshow("Inverted Floodfilled Image", im_floodfill_inv)

    cv2.imshow("Foreground", im_out)

    # 내부 채움이 완성된 이미지 리턴.
    return im_out


res = fullfill_inside(im_in)
cv2.imshow('Final Result !!!!', res)
cv2.waitKey(0)