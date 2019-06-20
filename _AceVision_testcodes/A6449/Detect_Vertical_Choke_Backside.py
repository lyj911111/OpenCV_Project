'''
    Choke의 각도 검출.
    Mode2 : 2개의 중앙 hole을 이용해서 위아래 마스크

    "a" key            : 화면 정지, 각도 판독.
    "ESC" key          : 종료
'''

import cv2
import numpy as np
import glob
import re
import math
import imutils

'''
    각도계산 클래스.
'''
class calulateCoordinate:

    def __init__(self):
        pass

    # (x1, y1) (x2, y2)값을 입력하면 점과 점사이 거리를 반환
    def distance(self, x1, y1, x2, y2):

        distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)   # 두 점 사이의 거리값
        return distance

    # (x1, y1) (x2, y2) 두점의 수직거리값
    def vertical_distance(self, x1, y1, x2, y2):

        distance = x2 - x1
        return distance

    # (x1, y1) (x2, y2) 두점의 수평거리값
    def horizontal_distance(self, x1, y1, x2, y2):

        distance = y2 - y1
        return distance

    # (x1, y1) (x2, y2)값을 입력하면 중간지점의 점(x, y) 을 반환
    def midpoint(self, x1, y1, x2, y2):

        x = int((x1 + x2) / 2)
        y = int((y1 + y2) / 2)
        return x, y

    # 직각삼각형의 밑변과 높이를 입력하면 각도를 반환.
    def angle(self, baseline, height):
        theta = math.atan((abs(height)/abs(baseline)))
        degree = round(theta*(180/math.pi), 4)           # 4째자리에서 반올림, theta x 라디안
        return degree


'''
    이미지 채도 향상.
    
    :param
        컬러이미지 , 0~255
    :return
        채도향상된이미지
'''
def increase_brightness(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return img


'''
    mask 바이너리 이미지의 폐쇄된 빈 공간을 채워줌.
    
    :param
        Binary 이미지
    :return
        Binary 이미지 (Closed 된 빈공간을 매꿈)
'''
def fullfill_inside(im_in):

    im_in = cv2.bitwise_not(im_in)

    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255.
    th, im_th = cv2.threshold(im_in, 220, 255, cv2.THRESH_BINARY_INV);
    # cv2.imshow('im_th', im_th)

    # Copy the thresholded image.
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
    im_out = im_th | im_floodfill_inv

    return im_out


'''
    체스 보정값으로 렌즈 왜곡을 보정하여 리턴.
    
    :param
        (raw) 원본이미지
    :return
        체스보정값으로 보정한 왜곡보정된 이미지
'''
def calibration(img):
    global objpoints, imgpoints

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]

    # undistort
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]

    return dst


'''
    Dipole 부분을 탐지하여 마스킹씌워 리턴
    
    :param
        원본이미지
    :return
         Dipole부분 마스크 Threshold 씌어진 Binary 이미지
'''
def square_img_filtering(img):
    img = increase_brightness(img, 255)
    img = cv2.GaussianBlur(img, (11, 11), 0)  # Blur 필터링

    # cv2.imshow('asdf', img)

    frame2 = img.copy()  # 영상원본

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(img)  # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

    frame_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)  # H,L,S 분리
    kernel = np.ones((3, 3), np.uint8)

    _, gray1 = cv2.threshold(gray_frame, 255, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 240, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 255, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 255, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 36, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 106, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 255, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 49, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)

    _, blue_ = cv2.threshold(blue, 138, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 149, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 51, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 134, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 134, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 222, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, 122, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, 123, 255, cv2.THRESH_BINARY)
    _, S_ = cv2.threshold(S, 123, 255, cv2.THRESH_BINARY)

    final_mask = gray1
    final_mask = cv2.bitwise_and(final_mask, blue1)
    final_mask = cv2.bitwise_and(final_mask, green1)
    final_mask = cv2.bitwise_and(final_mask, red1)
    final_mask = cv2.bitwise_and(final_mask, h1)
    final_mask = cv2.bitwise_and(final_mask, s1)
    final_mask = cv2.bitwise_and(final_mask, v1)
    final_mask = cv2.bitwise_and(final_mask, H1)
    final_mask = cv2.bitwise_and(final_mask, L1)
    final_mask = cv2.bitwise_and(final_mask, S1)

    final_mask = cv2.bitwise_and(final_mask, blue_)
    final_mask = cv2.bitwise_and(final_mask, green_)
    final_mask = cv2.bitwise_and(final_mask, red_)
    final_mask = cv2.bitwise_and(final_mask, v_)

    final_mask = cv2.erode(final_mask, kernel, iterations=10)
    final_mask = cv2.dilate(final_mask, kernel, iterations=15)
    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    # cv2.imshow('bbbbbbbbbb',final_mask)

    return final_mask


'''
    원본 이미지 필터링
'''
def img_filtering(img):

    img = increase_brightness(img, 255)         # 채도를 최대로 조정.
    img = cv2.GaussianBlur(img, (7, 7), 0)      # Blur 필터링

    frame2 = img.copy()  # 영상원본

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(img)  # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

    frame_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)  # H,L,S 분리
    kernel = np.ones((3, 3), np.uint8)

    # _, gray1 = cv2.threshold(gray_frame, 255, 255, cv2.THRESH_BINARY_INV)
    # _, blue1 = cv2.threshold(blue, 255, 255, cv2.THRESH_BINARY_INV)
    # _, green1 = cv2.threshold(green, 255, 255, cv2.THRESH_BINARY_INV)
    # _, red1 = cv2.threshold(red, 255, 255, cv2.THRESH_BINARY_INV)
    # _, h1 = cv2.threshold(h, 39, 255, cv2.THRESH_BINARY_INV)
    # _, s1 = cv2.threshold(s, 120, 255, cv2.THRESH_BINARY_INV)
    # _, v1 = cv2.threshold(v, 255, 255, cv2.THRESH_BINARY_INV)
    # _, H1 = cv2.threshold(H, 255, 255, cv2.THRESH_BINARY_INV)
    # _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    # _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)
    #
    # _, blue_ = cv2.threshold(blue, 40, 255, cv2.THRESH_BINARY)
    # _, green_ = cv2.threshold(green, 29, 255, cv2.THRESH_BINARY)
    # _, red_ = cv2.threshold(red, 20, 255, cv2.THRESH_BINARY)
    # _, h_ = cv2.threshold(h, 125, 255, cv2.THRESH_BINARY)
    # _, s_ = cv2.threshold(s, 119, 255, cv2.THRESH_BINARY)
    # _, v_ = cv2.threshold(v, 37, 255, cv2.THRESH_BINARY)
    # _, H_ = cv2.threshold(H, 138, 255, cv2.THRESH_BINARY)
    # _, L_ = cv2.threshold(L, 113, 255, cv2.THRESH_BINARY)
    # _, S_ = cv2.threshold(S, 123, 255, cv2.THRESH_BINARY)

    _, gray1 = cv2.threshold(gray_frame, 250, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 230, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 255, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 255, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 36, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 106, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 255, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 138, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)

    _, blue_ = cv2.threshold(blue, 58, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 156, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 164, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 130, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 190, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 192, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, 141, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, 117, 255, cv2.THRESH_BINARY)
    _, S_ = cv2.threshold(S, 141, 255, cv2.THRESH_BINARY)

    final_mask = gray1
    final_mask = cv2.bitwise_and(final_mask, blue1)
    final_mask = cv2.bitwise_and(final_mask, green1)
    final_mask = cv2.bitwise_and(final_mask, red1)
    final_mask = cv2.bitwise_and(final_mask, h1)
    final_mask = cv2.bitwise_and(final_mask, s1)
    final_mask = cv2.bitwise_and(final_mask, v1)
    final_mask = cv2.bitwise_and(final_mask, H1)
    final_mask = cv2.bitwise_and(final_mask, L1)
    final_mask = cv2.bitwise_and(final_mask, S1)

    final_mask = cv2.bitwise_and(final_mask, blue_)
    final_mask = cv2.bitwise_and(final_mask, green_)
    final_mask = cv2.bitwise_and(final_mask, red_)
    final_mask = cv2.bitwise_and(final_mask, v_)

    # final_mask = cv2.erode(final_mask, kernel, iterations=3)   # 사각형만 남기도록 깍음
    final_mask = cv2.dilate(final_mask, kernel, iterations=3)  # 정리된 사각형을 다시 확대

    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    # cv2.imshow('c', result)

    return final_mask


'''
    Canny Edge로 탐색하여 가장 큰 edge의 사각형 외곽선을 탐지
    꼭지점 4개의 좌표와 이미지를 리턴.
    
    param 
        1280 x 960 resized 된 이미지 input.
    return
        왼쪽상단 좌표, 오른쪽하단 좌표
'''
def find_outline(img):
    global ttt_count, diff
    global pre_x1, pre_y1, find_cnt

    img1 = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # # 들어온 이미지 확인용.
    # cv2.imshow('img', cv2.resize(img, (1280, 960)))
    # cv2.waitKey(0)

    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv2.Canny(gray, 30, 5)
    edged = cv2.dilate(edged, None, iterations=1)
    #edged = cv2.erode(edged, None, iterations=1)

    # 탐지된 Edge 확인용. (디버깅)
    # cv2.imshow("edged", cv2.resize(edged, (1280, 960)))
    # cv2.waitKey(0)

    # find contours in the edge map
    try:
        img, contours, hierachy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    except:
        contours, hierachy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_area_list = []
    for i in range(len(contours)):
        mom = contours[i]
        M = cv2.moments(mom)
        area = cv2.contourArea(mom)
        contours_area_list.append(area)

    MAX = 0
    idx = 0
    for i in range(len(contours_area_list)):
        MAX = (MAX > contours_area_list[i]) and MAX or contours_area_list[i]

    idx = contours_area_list.index(MAX)
    cnt = contours[idx]

    # print(cnt)
    box = cv2.minAreaRect(cnt)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")

    cv2.drawContours(img1, [box.astype("int")], -1, (0, 255, 0), 1)

    # 원본 해상도 / Resized 해상도
    ratio_x = 4024 / 1280
    ratio_y = 3036 / 960

    cnt = 1
    coordListx = []
    coordListy = []
    for (xA, yA) in list(box):
        globals()['x{}'.format(cnt)], globals()['y{}'.format(cnt)] = math.ceil(int(xA) * ratio_x), math.ceil(int(yA) * ratio_y)
        # globals()['x{}'.format(cnt)], globals()['y{}'.format(cnt)] = math.ceil(int(xA)), math.ceil(int(yA))
        # draw circles corresponding to the current points and
        cv2.circle(img1, (int(xA), int(yA)), 3, (0, 0, 255), -1)
        cv2.putText(img1, "({},{})".format(xA, yA), (int(xA - 80), int(yA + 10)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)
        coordListx.append(int(xA))
        coordListy.append(int(yA))
        cnt += 1

    # # 2개의 resized 된 좌표 리턴
    # print(coordListx)
    # print(coordListy)
    # print(type(coordListx[0]))
    # print(max(coordListx))

    list_point = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    #print("1. list_point", list_point)
    list_point.sort()
    #print("2. list_point", list_point)
    diff = 10 * ratio_x

    for i in range(4):
        cv2.circle(img1, (list_point[i][0], list_point[i][1]), 3, (0, 0, 255), -1)

    # 선택된 좌표 보여줌
    cv2.imshow('coord', img1)
    print(list_point[0], list_point[3])

    return min(coordListx), min(coordListy), max(coordListx), max(coordListy)

    # # 원본크기의 배율 좌표
    # return list_point[0][0], list_point[0][1], list_point[2][0], list_point[2][1], \
    #        list_point[1][0], list_point[1][1], list_point[3][0], list_point[3][1], img1

'''
    원본이미지, x1, y1 좌표, x2, y2 좌표
    그 부분만 사각형으로 마스크를 씌워 
    Masked된 Binary 이미지를 리턴.
'''
def edge_mask(img, x1, y1, x2, y2):

    # 좌표값 만큼 마스크
    masked = np.zeros(img.shape[:2], np.uint8)
    print((x1, y1), (x2, y2))
    masked = cv2.rectangle(masked, (x1, y1), (x2, y2), (255, 255, 255), -1)
    return masked


'''
    함수) 마스크를 이용해 초크부위만 남길 수 있도록 함. (1차가공)

        param
            masked_img : Threshold 영상 (이진화 영상)
            img        : 원본영상, display용

        return
            center_pt :  좌표 List
'''
def find_area(masked_img, img):

    imgcp = img.copy()

    centerPoint = []
    try:
        _, contours, _ = cv2.findContours(masked_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    except:
        contours, _ = cv2.findContours(masked_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기

    # 마스크할 창 생성.
    chokemask = np.zeros(img.shape[:2], np.uint8)

    if len(contours) != 0:
        for contour in contours:
            if (cv2.contourArea(contour) > 1000) and (cv2.contourArea(contour) < 1000000):  # **필요한 면적을 찾아 중심점 좌표를 저장 (영역 제한)

                # 사각박스 영역 지정
                x, y, w, h = cv2.boundingRect(contour)
                #cv2.rectangle(img,(x, y), (x+w, y+h), (0, 0, 255), 2)

                cv2.rectangle(chokemask, (x, y), (x+w, y+h), (255, 255, 255), -1)

                # rect = cv2.minAreaRect(contour)
                # box = cv2.boxPoints(rect)
                # box = np.int0(box)
                #cv2.drawContours(img, [box], 0, (255, 255, 0), 2)

                # area = cv2.contourArea(contour)       # 면적값 출력
                # print(area)
                mom = contour
                M = cv2.moments(mom)
                cx_origin = int(M['m10'] / M['m00'])
                cy_origin = int(M['m01'] / M['m00'])
                #cv2.drawContours(img, contour, -1, (0, 255, 0), 1)
                #cv2.circle(img, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시
                centerPoint.append([cx_origin, cy_origin])

        onlyChoke = cv2.bitwise_and(imgcp, imgcp, mask=chokemask)  # 합성하여 뽑아냄.

        finalchokemask = onlychokeFiltering(onlyChoke)
        detect_LineDegree(img , finalchokemask)

        # cv2.imwrite('b.png', chokemask)
        # cv2.imshow('chokmask', chokemask)
        cv2.imshow('rrreal result', img)
        # cv2.imshow('onlyChoke', onlyChoke)
        return centerPoint

'''
    Choke만 남아있는 마스킹된 이미지를 필터링하여 순수 choke부만 남기고 필터링 (2차 가공)
'''
def onlychokeFiltering(onlychoke):

    onlychoke = cv2.GaussianBlur(onlychoke, (7, 7), 0)
    frame2 = onlychoke.copy()
    grayChoke = cv2.cvtColor(onlychoke, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(onlychoke)  # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(onlychoke, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

    frame_hls = cv2.cvtColor(onlychoke, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)  # H,L,S 분리
    kernel = np.ones((3, 3), np.uint8)

    _, gray1 = cv2.threshold(grayChoke, 255, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 255, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 255, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 255, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 120, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 255, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 255, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 86, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)

    _, blue_ = cv2.threshold(blue, 0, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 91, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 15, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 94, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 78, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, 124, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, 117, 255, cv2.THRESH_BINARY)
    _, S_ = cv2.threshold(S, 128, 255, cv2.THRESH_BINARY)

    final_mask = gray1
    final_mask = cv2.bitwise_and(final_mask, blue1)
    final_mask = cv2.bitwise_and(final_mask, green1)
    final_mask = cv2.bitwise_and(final_mask, red1)
    final_mask = cv2.bitwise_and(final_mask, h1)
    final_mask = cv2.bitwise_and(final_mask, s1)
    final_mask = cv2.bitwise_and(final_mask, v1)
    final_mask = cv2.bitwise_and(final_mask, H1)
    final_mask = cv2.bitwise_and(final_mask, L1)
    final_mask = cv2.bitwise_and(final_mask, S1)

    final_mask = cv2.bitwise_and(final_mask, blue_)
    final_mask = cv2.bitwise_and(final_mask, green_)
    final_mask = cv2.bitwise_and(final_mask, red_)
    final_mask = cv2.bitwise_and(final_mask, v_)

    final_mask = cv2.dilate(final_mask, kernel, iterations=3)
    final_mask = fullfill_inside(final_mask)                    # 초크부위만 딱 추출
    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    #cv2.imshow('TTest', result)

    # 초크부위 마스크를 씌울 검정색 빈상자 생성.
    chokerecMask = np.zeros(onlychoke.shape[:2], np.uint8)

    try:
        _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    except:
        contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    if len(contours) != 0:
        for contour in contours:
            if (cv2.contourArea(contour) > 2000) and (cv2.contourArea(contour) < 10000000):  # **필요한 면적을 찾아 중심점 좌표를 저장

                # 근사 사각형으로 치환
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame2, [box], 0, (255, 255, 0), 2)
                cv2.drawContours(chokerecMask, [box], 0, (255, 255, 255), -1)

                ball_area = cv2.contourArea(contour)
                mom = contour
                M = cv2.moments(mom)
                cx_origin = int(M['m10'] / M['m00'])
                cy_origin = int(M['m01'] / M['m00'])
                cv2.drawContours(frame2, contour, -1, (0, 255, 0), 1)
                cv2.circle(frame2, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시

    cv2.imshow('Masked Testoutput', chokerecMask)
    cv2.imshow('TestOutput', frame2)
    return chokerecMask



'''
    최종 평균 라인을 검출하여 디스플레이 함.
    
'''
def display_final(img, x1,y1, x2,y2, final_function):
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
    cv2.putText(img, final_function, (x1+500, y1-30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 0), 2)
    cv2.imshow("FFianl", img)
    return img


# 원본, choke마스크이미지(이진화)
def detect_LineDegree(img, final_mask):

    cp_img = img.copy()
    showimg = img.copy()
    try:
        _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    except:
        contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    if len(contours) != 0:
        for contour in contours:
            if (cv2.contourArea(contour) > 500) and (cv2.contourArea(contour) < 10000000):  # **필요한 면적을 찾아 중심점 좌표를 저장

                ball_area = cv2.contourArea(contour)
                mom = contour
                M = cv2.moments(mom)
                cx_origin = int(M['m10'] / M['m00'])
                cy_origin = int(M['m01'] / M['m00'])
                #cv2.drawContours(frame2, contour, -1, (0, 255, 0), 1)
                cv2.circle(img, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시

                # then apply fitline() function
                [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
                # Now find two extreme points on the line to draw line
                lefty = int((-x * vy / vx) + y)
                righty = int(((cp_img.shape[1] - x) * vy / vx) + y)
                cv2.line(img, (0, lefty),(cp_img.shape[1] - 1, righty), 255, 2)     # 기본 직선의 좌표
                cv2.circle(img, (0, lefty), 10, (0, 0, 255), -1)
                cv2.circle(img, (cp_img.shape[1] - 1, righty), 3, (0, 0, 255), -1)

                cal = calulateCoordinate()
                d = cal.distance(0, lefty, cp_img.shape[1] - 1, righty)
                print("두점사이거리",d)
                e = cal.horizontal_distance(0, lefty, cp_img.shape[1] - 1, righty)

                print("수평한 거리", e)
                f = cal.vertical_distance(0, lefty, cp_img.shape[1] - 1, righty)
                print("수직한 거리", f)
                z = round(cal.angle(f,e),2)
                print( "각도는", z )
                if e < 0:
                    z = 90 + (90-z)

                # 1차 함수표현 y = ax * b
                a = (righty - lefty) / (cp_img.shape[1] - 1)
                b = lefty
                cv2.putText(img, "{}".format(z), (cx_origin+20, cy_origin), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)    # 좌표의 1차 함수방정식

                print("y = ({})x + {}".format(a, b))
                print("두개의 점:", (0, lefty), (cp_img.shape[1] - 1, righty))

                # try:
                #     if abs(bf_cy - cy_origin) > 100 :     # y좌표가 급격히 바뀔때 하나의 함수로
                #         # print(aList, bList)
                #         print("=============다음으로=================")
                #         flag = 1
                #         aList.clear()
                #         bList.clear()
                #         cnt = 1
                # except:
                #     pass
                # bf_cy = cy_origin
                # # aList.append(a)
                # # bList.append(b)
                # # asum = sum(aList)
                # # bsum = sum(bList)
                #
                # # cv2.putText(img, "y = ({})x + {}".format((asum/cnt), (bsum/cnt)), (cx_origin-200, cy_origin-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)   # 평균을 구한 일차함수
                #
                # # print("리스트값", aList, bList)
                # # print("총합값", asum, bsum)
                # # print("평균 1차함수값: y = ({})x + {}".format((asum / cnt), (bsum / cnt)))    # 기울기 평균 / y절편 평균
                # #
                # # print("평균의 양끝 좌표 값", (0, (bsum / cnt)), ( cp_img.shape[1] - 1 , (asum / cnt) * (cp_img.shape[1] - 1) + (bsum / cnt)))
                # # print("{} / {} = {}".format(bsum, cnt, int(bsum / (cnt))))
                # # print("y절편값:", int(bsum / (cnt)))
                #
                # # save_function_list.append("y = ({})x + {}".format((asum / cnt), (bsum / cnt)))
                # # print(save_function_list)
                # # final_end_ptList.append([(0, int(bsum / (cnt))), ( int(cp_img.shape[1] - 1), int(((asum / (cnt)) * cp_img.shape[1] - 1) + (bsum / (cnt))))])
                # # print(final_end_ptList)
                # # print("---")
                #
                # # 평균을 낸 값.  (오른쪽, 왼쪽)
                # # cv2.line(img, (0, int(bsum / (cnt))), ( int(cp_img.shape[1] - 1), int(((asum / (cnt)) * cp_img.shape[1] - 1) + (bsum / (cnt)))) , (0, 255, 255), 1)



                # cv2.imshow('321321321', showimg)
                # cv2.imshow('123123123', img)
                cv2.waitKey(1)

def MaskFromCircle_bin(img):
    img_cp = img.copy()

    img = increase_brightness(img, 100)
    img = cv2.GaussianBlur(img, (3, 3), 0)

    dipoleMask = np.zeros(img.shape[:2], np.uint8)
    dipoleMask = np.bitwise_not(dipoleMask)

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((3, 3), np.uint8)
    th2 = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)  # 11 2
    th2 = cv2.erode(th2, kernel, iterations=1)
    circles = cv2.HoughCircles(th2, cv2.HOUGH_GRADIENT, 1, 13, param1=110, param2=9, minRadius=9, maxRadius=11)

    cv2.imshow('b', th2)

    # 외곽선 탐지하여 꼭지점 2개좌표 리턴.
    leftup, leftdn, rightup, rightdn = find_outline(img)
    # 이미지의 중심선 찾음.
    midline = int((rightup - leftdn) / 2) + leftup
    # 중심선으로부터 Offset한 거리.
    gap = 60
    img = cv2.line(img, (midline, leftup), (midline, rightdn), (0, 0, 255), 2, cv2.LINE_4)
    img = cv2.line(img, (midline - gap, leftup), (midline - gap, rightdn), (0, 255, 0), 2)
    img = cv2.line(img, (midline + gap, leftup), (midline + gap, rightdn), (0, 255, 0), 2)

    # 범위내 원 검출
    circlelist = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            if circle[0] > midline - gap and circle[0] < midline + gap:
                print((circle[0], circle[1]))
                circlelist.append((circle[0], circle[1], circle[2]))
    for i in range(len(circlelist)):
        cv2.circle(img, (circlelist[i][0], circlelist[i][1]), circlelist[i][2], (255, 0, 255), 2)

    print(img.shape[0], img.shape[1])
    print(circlelist)

    # 마스크 씌우기
    # dipoleMask = cv2.rectangle(dipoleMask, (0, circlelist[0][1]-128),(img.shape[1], circlelist[0][1]-25), (0, 0, 0), -1)
    # dipoleMask = cv2.rectangle(dipoleMask, (0, circlelist[0][1]+20),(img.shape[1], circlelist[0][1]+125), (0, 0, 0), -1)
    # dipoleMask = cv2.rectangle(dipoleMask, (0, circlelist[1][1]-128),(img.shape[1], circlelist[1][1]-22), (0, 0, 0), -1)
    # dipoleMask = cv2.rectangle(dipoleMask, (0, circlelist[1][1]+20),(img.shape[1], circlelist[1][1]+125), (0, 0, 0), -1)
    return dipoleMask


def judgeImage(img):
    global resolution

    img = calibration(img)  # 보정된 이미지 리턴 (속도가 느려짐)
    img = cv2.resize(img, resolution)

    # 좌표값과 마킹된 이미지 리턴.
    x1, y1, x4, y4 = find_outline(img)
    masked_edge = edge_mask(img, x1, y1, x4, y4)

    # 제품영역 외 모든 부분 마스크
    masked_edge_img = cv2.bitwise_and(img, img, mask=masked_edge)
    cv2.imshow('masked_edge', masked_edge_img)

    # 제품외 영역 제외 + Dipole 부분 마스크 = Choke 마스크만 남김.
    line_alive = img_filtering(img)
    # rec_alive = square_img_filtering(masked_edge_img)
    # rec_alive = cv2.bitwise_not(rec_alive)
    rec_alive = MaskFromCircle_bin(masked_edge_img)
    #rec_alive = np.zeros(img.shape[:2], np.uint8)*255

    rec_alive_masked = cv2.bitwise_and(line_alive, line_alive, mask=rec_alive)

    kernel = np.ones((3, 3), np.uint8)
    msk_result = cv2.bitwise_and(masked_edge, masked_edge, mask=rec_alive_masked)
    msk_result = cv2.dilate(msk_result, kernel, iterations=6)  # 정리된 사각형을 다시 확대
    msk_result = cv2.erode(msk_result, kernel, iterations=6)  # 사각형만 남기도록 깍음

    cv2.imshow('msk_result', msk_result)

    result = find_area(msk_result, img)


    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # # gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # #edges = cv2.Canny(gray, 100, 200)


    cv2.imshow('line', line_alive)
    # cv2.imshow('rec', rec_alive)
    # cv2.waitKey(0)

    return img


def main():
    global objpoints, imgpoints, resolution

    # 체스판으로 이미지 보정.
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((9 * 13, 3), np.float32)
    objp[:, :2] = np.mgrid[0:13, 0:9].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob('C:/Users/DELL/Desktop/newmodel/chess/*.bmp')  # 체스 이미지들

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (13, 9), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)

    # 해상도 지정.
    resolution = (1280, 960)

    while True:
        img = cv2.imread("./img/backcorrect.bmp")  # 연속 이미지 취득 (비디오 프레임 가정) - 양품

        frame = img.copy()
        frame = cv2.resize(frame, resolution)

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1)
        if k == 27:  # ESC 종료
            break
        elif k == -1:
            continue
        # 세팅 모드
            # print(k)
        elif k == ord('a') or k == ord('A'):  # a 키를 눌렀을 때 키보드 이벤트 캡쳐, 판독.
            result = judgeImage(img)

            print("현재 판독 이미지를 출력합니다.")
        else:
            cv2.destroyWindow('result') # 다른키를 누르면 판독 창 닫기.


if __name__ == "__main__":
    main()