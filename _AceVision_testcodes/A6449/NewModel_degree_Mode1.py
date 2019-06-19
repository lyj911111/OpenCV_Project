'''
    새로운 모델, Dipole 각도 검출.
    Mode1 : Fullfill 함수와 Dilate, Erosion 을 이용해 사각형 Threshold만 검출.
    제품이 확실하게 같은위치로 들어와 동일한 조명을 받을때. (안정적일 때 Mode 1)

    "a" key            : 화면 정지, 각도 판독.
    "ESC" key          : 종료
'''

import cv2
import numpy as np
import glob
import re
import math


'''
    각도 검출을 위한 삼각함수 알고리즘
'''
class calulateCoordinate:

    def __init__(self):
        pass

    # (x1, y1) (x2, y2)값을 입력하면 점과 점사이 거리를 반환
    def distance(self, x1, y1, x2, y2):

        distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)   # 두 점 사이의 거리값
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


def nothing(x):
    pass


'''
    원본이미지의 채도를 향상시켜줌.
    :param  (원본이미지, 0~255)
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
    Binary 이미지로 들어온 Threshold의 내부 구멍을 매꿔줌.

'''
def fullfill_inside(im_in):

    im_in = cv2.bitwise_not(im_in)

    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255.
    th, im_th = cv2.threshold(im_in, 220, 255, cv2.THRESH_BINARY_INV);
    cv2.imshow('im_th', im_th)

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
    Chess 보정값을 적용하여 보정된 이미지를 리턴.
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
    원본 이미지를 필터링하여 최종 binary 이미지를 리턴.
'''
def img_filtering(img):

    img = increase_brightness(img, 255)         # 채도를 최대로 조정.
    img = cv2.GaussianBlur(img, (5, 5), 0)      # Blur 필터링

    frame2 = img.copy()  # 영상원본

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(img)  # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

    frame_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)  # H,L,S 분리
    kernel = np.ones((3, 3), np.uint8)

    _, gray1 = cv2.threshold(gray_frame, 255, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 255, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 255, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 255, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 39, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 120, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 255, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 255, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 255, 255, cv2.THRESH_BINARY_INV)

    _, blue_ = cv2.threshold(blue, 40, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 29, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 20, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 125, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 119, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 37, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, 138, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, 113, 255, cv2.THRESH_BINARY)
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

    final_mask = fullfill_inside(final_mask)                    # Threshold 내부를 채움
    final_mask = cv2.erode(final_mask, kernel, iterations=11)   # 사각형만 남기도록 깍음
    final_mask = cv2.dilate(final_mask, kernel, iterations=12)  # 정리된 사각형을 다시 확대

    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    #cv2.imshow('c', img)
    #cv2.imshow('b',ROImask)

    return final_mask

'''
    이미지의 각도를 판정하여 OK NG 인지 판독.
'''
def judgeImage(img):
    global resolution

    img = calibration(img)  # 보정된 이미지 리턴 (속도가 느려짐)
    img = cv2.resize(img, resolution)

    final_mask = img_filtering(img)     # 이미지를 가공하여 사각형만 남긴 Threshold를 내보냄.
    #cv2.imshow('b',final_mask)

    pt_list = []
    right_mid_list = []
    left_mid_list = []
    minx_contour = []
    miny_contour = []
    square_center = []
    try:
        _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    except:
        contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    if len(contours) != 0:
        for contour in contours:
            if (cv2.contourArea(contour) > 8000) and (cv2.contourArea(contour) < 9800):  # **필요한 면적을 찾아 중심점 좌표를 저장
                ball_area = cv2.contourArea(contour)
                mom = contour
                M = cv2.moments(mom)
                cx_origin = int(M['m10'] / M['m00'])
                cy_origin = int(M['m01'] / M['m00'])

                # 외곽선 근사화 시키기 (사각형의 형상을 얻기 위해), epsilon값에 따라 근사 민감도 결정.
                epsilon = 0.12 * cv2.arcLength(mom, True)
                approx = cv2.approxPolyDP(mom, epsilon, True)

                # 근사화 시킨 놈
                cv2.drawContours(img, [approx], -1, (255, 255, 255), 3)  # 근사화 시킨 컨투어 그리기
                # cv2.drawContours(img, [mom], 0, (0, 255, 0), 5) # 실제 컨투어를 그림.
                cv2.circle(img, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시

                # 근사화 시킨 형상중 사각형만 고름.
                if len(approx) != 0:
                    if len(approx) == 4:
                        # midp = cal.midpoint(approx[0][0][0], approx[0][0][1], approx[3][0][0], approx[3][0][1])
                        for i in range(len(approx)):
                            minx_contour.append(approx[i][0][0])  # x좌표에 대한 꼭지점 좌표. 리스트에 추가
                            miny_contour.append(approx[i][0][1])  # y좌표에 대한 꼭지점 좌표. 리스트에 추가
                            cv2.circle(img, (approx[i][0][0], approx[i][0][1]), 5, (255, 255, 255),
                                       -1)  # 근사화 사각에서의 꼭지점 표시
                            # 중심점의 x좌표를 기준으로 왼쪽과 오른쪽으로 나누어 왼쪽, 오른쪽 리스트에 추가(꼭지점의 중점을 계산하기 위한 선행작업)
                            pt_list.append(tuple((minx_contour[i], miny_contour[i])))
                            if pt_list[i][0] < cx_origin:
                                left_mid_list.append(pt_list[i])
                            else:
                                right_mid_list.append(pt_list[i])

                        #print(pt_list)
                        cal = calulateCoordinate()  # 계산 클래스 객체 할당.

                        # 왼쪽 오른쪽의 중심점을 반환
                        left_midpt = cal.midpoint(left_mid_list[0][0], left_mid_list[0][1], left_mid_list[1][0],
                                                  left_mid_list[1][1])
                        right_midpt = cal.midpoint(right_mid_list[0][0], right_mid_list[0][1], right_mid_list[1][0],
                                                   right_mid_list[1][1])
                        #print("왼쪽, 오른쪽 미드 중심점값", left_midpt, right_midpt)

                        # 왼쪽 오른쪽 중심점을 찍고 선으로 이어줌.
                        cv2.circle(img, left_midpt, 5, (0, 255, 0), -1)  # 근사화 시킨 사각형의 꼭지점 출력
                        cv2.circle(img, right_midpt, 5, (0, 255, 0), -1)  # 근사화 시킨 사각형의 꼭지점 출력
                        cv2.line(img, left_midpt, right_midpt, (0, 255, 0), 3)  # 사각형의 중심점을 선분으로 이음.

                        # 중심선분의 길이값 구함. 직각삼각형을 만들어 밑변, 높이를 이용해 tan 삼각함수로 각도 계산
                        midDistance = cal.distance(left_midpt[0], left_midpt[1], right_midpt[0], right_midpt[1])
                        baseline = cal.distance(left_midpt[0], left_midpt[1], right_midpt[0], left_midpt[1])
                        height = cal.distance(right_midpt[0], right_midpt[1], right_midpt[0], left_midpt[1])
                        angle = cal.angle(baseline, height)

                        # # 모든 각도 출력
                        # cv2.putText(img, 'angle: %.2f' % (round(angle, 2)), (cx_origin - 35, cy_origin - 25),
                        #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)

                        # 각도가 2.2도 이상 틀어지면 불합격, 그 이하 합격
                        if angle > 2.2:
                            cv2.putText(img, 'angle: %.2f NG' % (round(angle, 2)), (cx_origin - 35, cy_origin - 25),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
                        else:
                            cv2.putText(img, 'angle: %.2f' % (round(angle, 2)), (cx_origin - 35, cy_origin - 25),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
                else:
                    print("사각형이 아닙니다.")

                square_center.append([cx_origin, cy_origin])
                # 리스트를 비워줌 반복
                minx_contour = []
                miny_contour = []
                left_mid_list = []
                right_mid_list = []
                pt_list = []

    #cv2.waitKey(0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # cv2.imshow('a', img)
    # cv2.waitKey(0)



    # cv2.imshow('mask', mask)
    # cv2.imshow('result', result)
    # cv2.imshow('c', res)
    # cv2.imshow('img', img)

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
    resolution = (1260, 960)

    while True:
        img = cv2.imread("./img/G1.bmp")  # 연속 이미지 취득 (비디오 프레임 가정) - 정상제품
        # img = cv2.imread("./img/backside_no.bmp")  # 연속 이미지 취득 (비디오 프레임 가정) - 불량품

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
        elif k == 97:  # a 키를 눌렀을 때 키보드 이벤트 캡쳐, 판독.
            result = judgeImage(img)
            cv2.imshow('result', result)
            print("현재 판독 이미지를 출력합니다.")
        else:
            cv2.destroyWindow('result') # 다른키를 누르면 판독 창 닫기.

if __name__ == "__main__":
    main()