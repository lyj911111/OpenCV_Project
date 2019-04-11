'''
    히스토그램 평활화.
    이미지에 밝기가 골구로 퍼지도록 하는 효과.
    어둡거나 밝거나 한쪽으로 히스토그램이 치우쳐져있을때 유용.

    이미지 대조 Contrast 를 확실하게 만듦.
    어떤 조명에서도 일정한 조명량을 지닌 이미지를 만듦.

    참고: https://webnautes.tistory.com/1274

'''

import cv2 as cv
import numpy as np


bins = np.arange(256).reshape(256,1)


def draw_histogram(img):

    h = np.zeros((img.shape[0], 513), dtype=np.uint8)

    hist_item = cv.calcHist([img],[0],None,[256],[0,256])
    cv.normalize(hist_item,hist_item,0,255,cv.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    for x,y in enumerate(hist):
        cv.line(h,(x,0+10),(x,y+10),(255,255,255))

    print(hist_item)

    cv.line(h, (0, 0 + 10), (0, 5), (255, 255, 255) )
    cv.line(h, (255, 0 + 10), (255, 5), (255, 255, 255))
    y = np.flipud(h)

    #draw curve
    hist, bin = np.histogram(img.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()
    cv.normalize(cdf_normalized, cdf_normalized, 0, 255, cv.NORM_MINMAX)
    hist = np.int32(np.around(cdf_normalized))
    pts = np.int32(np.column_stack((bins, hist)))
    pts += [257, 10]

    cv.line(h, (0+257, 0 + 10), (0+257, 5), (255, 255, 255) )
    cv.line(h, (255+257, 0 + 10), (255+257, 5), (255, 255, 255))
    cv.polylines(h, [pts], False, (255,255,255))

    return y


img = cv.imread('./img/15000.bmp', cv.IMREAD_COLOR)
img = cv.resize(img,(1260,960))
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


line =  draw_histogram(gray)
result1 = np.hstack((gray, line))
cv.imshow('result1', result1)


#equ = cv.equalizeHist(gray)
hist, bin = np.histogram(img.flatten(), 256, [0, 256])
cdf = hist.cumsum()
cdf_mask = np.ma.masked_equal(cdf,0)
cdf_mask = (cdf_mask - cdf_mask.min())*255/(cdf_mask.max()-cdf_mask.min())
cdf = np.ma.filled(cdf_mask,0).astype('uint8')
equ = cdf[gray]


line =  draw_histogram(equ)
result2 = np.hstack((equ, line))
cv.imshow('result2', result2)


cv.waitKey(0)
cv.destroyAllWindows()