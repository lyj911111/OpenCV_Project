import cv2 as cv
import numpy as np

#bins = np.arange(256).reshape(256,1)

'''
원본 이미지에 마스크를 씌우고 그 부분에서의 밝기에 대한 histogram을 찾는 함수. (밝기에 대한 분포도)

    param 1 : 히스토그램을 구할 원본이미지
    param 2~4: (x1,y1) 부터 (x2, y2) 의 이미지 마스크를 씌워서 구분함
'''
def mask_histogram(img, x1,y1,x2,y2):
    h = np.zeros((img.shape[0], 256), dtype=np.uint8)   # 히스토그램을 만들 공간 생성.

    # mask생성
    mask = np.zeros(img.shape[:2], np.uint8)
    mask[y1:y2, x1:x2] = 255                 # [세로 x 가로]의 픽셀을 255으로 마스크 씌움

    # 이미지에 mask가 적용된 결과
    masked_img = cv.bitwise_and(img, img, mask=mask)

    # Histogram: [이미지], [ 채널: [0]그래이스케일/ 컬러 경우, BGR채널[0][1][2] ], 전체이미지 : None , x축범위, 막대의 갯수
    hist_item = cv.calcHist([img], [0], mask, [256], [0, 256])

    cv.normalize(hist_item, hist_item, 0, 255, cv.NORM_MINMAX)
    hist = np.int32(np.around(hist_item))
    for x, y in enumerate(hist):
        cv.line(h, (x, 0 + 10), (x, y + 10), (255, 255, 255))

    cv.line(h, (0, 0 + 10), (0, 5), (255, 255, 255))
    cv.line(h, (255, 0 + 10), (255, 5), (255, 255, 255))
    y = np.flipud(h)

    result = np.hstack((masked_img, y))  # 이미지와 히스토그램을 붙이기

    # histogram의 y값, 마스크씌운 이미지를 리턴.
    return hist_item, result


def draw_histogram(img):
    h = np.zeros((img.shape[0], 256), dtype=np.uint8)

    # Histogram: [이미지], [ 채널: [0]그래이스케일/ 컬러 경우, BGR채널[0][1][2] ], 전체이미지 : None , x축범위, 막대의 갯수
    hist_item = cv.calcHist([img], [0], None, [256], [0, 256])


    cv.normalize(hist_item,hist_item,0,255,cv.NORM_MINMAX)
    hist = np.int32(np.around(hist_item))
    for x, y in enumerate(hist):
        cv.line(h, (x, 0+10), (x, y+10), (255, 255, 255))

    cv.line(h, (0, 0 + 10), (0, 5), (255, 255, 255) )
    cv.line(h, (255, 0 + 10), (255, 5), (255, 255, 255))
    y = np.flipud(h)

    result = np.hstack((img, y))  # 이미지와 히스토그램을 붙이기

    # histogram의 y값, 마스크씌운 이미지를 리턴.
    return hist_item, result



img = cv.imread('./img/15000.bmp', cv.IMREAD_COLOR)
img = cv.resize(img,(1260,960))
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 원본 이미지에 대한 히스토그램
# result1 = draw_histogram(gray)
# cv.imshow('result1', result1)

# 위에서부터 아래로 차례대로 스캔하면서 감.
for i in range(0, 550, 10):
    for j in range(0, 560, 10):
        # 마스크 씌운 이미지의 히스토그램
        y, result2 = mask_histogram(gray, 103+j,40+i,665+j,490+i)
        cv.imshow('result2', result2)
        print(y)
        cv.waitKey(100)
        #cv.destroyAllWindows()


