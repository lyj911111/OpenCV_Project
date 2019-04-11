import cv2 as cv
import numpy as np


bins = np.arange(256).reshape(256, 1)


def draw_histogram(img):


    h = np.zeros((img.shape[0], 513), dtype=np.uint8)

    # 히스토그램을 출력함.
    # [이미지], [ 채널: [0]그래이스케일/ 컬러 경우, BGR채널[0][1][2] ], 전체이미지 : None , x축범위, 막대의 갯수
    hist_item = cv.calcHist([img],[0],None,[256],[0,256])


    print("히스토",hist_item)
    cv.normalize(hist_item,hist_item,0,255,cv.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    for x,y in enumerate(hist):
        cv.line(h,(x,0+10),(x,y+10),(255,255,255))

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


clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
equ = clahe.apply(gray)


line =  draw_histogram(equ)
result2 = np.hstack((equ, line))
cv.imshow('result2', result2)


cv.waitKey(0)
cv.destroyAllWindows()