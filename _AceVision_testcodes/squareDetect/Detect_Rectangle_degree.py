import cv2
import numpy as np
import math

def nothing(x):
    pass

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

flag = 0
cnt = 0

# 관심영역 ROI 지정.
ROI_list = [
    [(500, 560), (4100, 2700)]  # 첫번째 관심영역 (start_pt, end_pt) 30 200 1200 500
]

    # 이미지 불러오기
img = cv2.imread('product45.bmp')
#img = cv2.resize(img, (1280, 960))

# Blur 필터링 테스트 ###################
#img = cv2.blur(img, (4, 4))
#img = cv2.medianBlur(img, 9)
img = cv2.GaussianBlur(img, (19, 19),3)

#img = cv2.bilateralFilter(img,9,75,75)

#########################################
# cv2.imshow('a', imga)
# cv2.imshow('b', imgb)
# cv2.imshow('c', imgc)
# cv2.imshow('d', imgd)

#img = cv2.imread('ko.jpg', cv2.IMREAD_UNCHANGED)
cv2.namedWindow("Trackbars", cv2.WINDOW_NORMAL)

# create trackbars for color change
cv2.createTrackbar("graybar", "Trackbars", 142, 255, nothing)  # 135  V
cv2.createTrackbar("bluebar", "Trackbars", 108, 255, nothing)  # 110  V
cv2.createTrackbar("greenbar", "Trackbars", 143, 255, nothing)  # 101  V
cv2.createTrackbar("redbar", "Trackbars", 148, 255, nothing)  # 101    V
cv2.createTrackbar("hsv hbar", "Trackbars", 173, 255, nothing)  # 255
cv2.createTrackbar("hsv sbar", "Trackbars", 118, 255, nothing)  # 115
cv2.createTrackbar("hsv vbar", "Trackbars", 175, 255, nothing)  # 141  V
cv2.createTrackbar("hsl hbar", "Trackbars", 80, 255, nothing)  # 255
cv2.createTrackbar("hsl sbar", "Trackbars", 115, 255, nothing)  # 170  V
cv2.createTrackbar("hsl lbar", "Trackbars", 55, 255, nothing)  # 175

# cv2.createTrackbar("graybar_", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("bluebar_", "Trackbars", 15, 255, nothing)  #  V
cv2.createTrackbar("greenbar_", "Trackbars", 0, 255, nothing)  # V
cv2.createTrackbar("redbar_", "Trackbars", 25, 255, nothing)    # V
cv2.createTrackbar("hsv hbar_", "Trackbars", 165, 255, nothing)
cv2.createTrackbar("hsv sbar_", "Trackbars", 170, 255, nothing)
cv2.createTrackbar("hsv vbar_", "Trackbars", 0, 255, nothing)  #  V
cv2.createTrackbar("hsl hbar_", "Trackbars", 53, 255, nothing)
cv2.createTrackbar("hsl sbar_", "Trackbars", 53, 255, nothing)
cv2.createTrackbar("hsl lbar_", "Trackbars", 144, 255, nothing)

cv2.createTrackbar("k1", "Trackbars", 25, 50, nothing)
cv2.createTrackbar("k2", "Trackbars", 25, 50, nothing)
cv2.createTrackbar("itera", "Trackbars", 5, 10, nothing)
cv2.createTrackbar("rank", "Trackbars", 5, 10, nothing)

kernel = np.ones((7, 7), np.uint8)
kernel1 = np.ones((15, 15), np.uint8)
edge_kernel = np.ones((5, 5), np.int8)

################# 영상일때는 while문 내로 이동 ###############################################

# col,row,_ = frame.shape # frame 화면크기 출력, (y ,x) = (480x640)
# print(col,row)
frame2 = img.copy()  # 영상원본

# 카메라 일때만 사용.
# img = cv2.GaussianBlur(img, (3, 3), 0)  # 원본에 가우시안 필터적용

gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blue, green, red = cv2.split(img)  # 원본에서 BGR 분리
frame_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

frame_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
H, L, S = cv2.split(frame_hls)  # H,L,S 분리

#########################################################################################

while(1):

    gray_c = cv2.getTrackbarPos("graybar", "Trackbars")
    blue_c = cv2.getTrackbarPos("bluebar", "Trackbars")
    green_c = cv2.getTrackbarPos("greenbar", "Trackbars")
    red_c = cv2.getTrackbarPos("redbar", "Trackbars")
    hsv_h_c = cv2.getTrackbarPos("hsv hbar", "Trackbars")
    hsv_s_c = cv2.getTrackbarPos("hsv sbar", "Trackbars")
    hsv_v_c = cv2.getTrackbarPos("hsv vbar", "Trackbars")
    hsl_h_c = cv2.getTrackbarPos("hsl hbar", "Trackbars")
    hsl_s_c = cv2.getTrackbarPos("hsl sbar", "Trackbars")
    hsl_l_c = cv2.getTrackbarPos("hsl lbar", "Trackbars")

    gray_c_ = cv2.getTrackbarPos("graybar_", "Trackbars")
    blue_c_ = cv2.getTrackbarPos("bluebar_", "Trackbars")
    green_c_ = cv2.getTrackbarPos("greenbar_", "Trackbars")
    red_c_ = cv2.getTrackbarPos("redbar_", "Trackbars")
    hsv_h_c_ = cv2.getTrackbarPos("hsv hbar_", "Trackbars")
    hsv_s_c_ = cv2.getTrackbarPos("hsv sbar_", "Trackbars")
    hsv_v_c_ = cv2.getTrackbarPos("hsv vbar_", "Trackbars")
    hsl_h_c_ = cv2.getTrackbarPos("hsl hbar_", "Trackbars")
    hsl_s_c_ = cv2.getTrackbarPos("hsl sbar_", "Trackbars")
    hsl_l_c_ = cv2.getTrackbarPos("hsl lbar_", "Trackbars")

    k1 = cv2.getTrackbarPos("k1", "Trackbars")
    k2 = cv2.getTrackbarPos("k2", "Trackbars")
    itera = cv2.getTrackbarPos("itera", "Trackbars")
    rank = cv2.getTrackbarPos("rank", "Trackbars")

    _, gray1 = cv2.threshold(gray_frame, gray_c, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, blue_c, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, green_c, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, red_c, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, hsv_h_c, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, hsv_s_c, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, hsv_v_c, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, hsl_h_c, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, hsl_s_c, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, hsl_l_c, 255, cv2.THRESH_BINARY_INV)

    _, gray_ = cv2.threshold(gray_frame, gray_c_, 255, cv2.THRESH_BINARY)
    _, blue_ = cv2.threshold(blue, blue_c_, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, green_c_, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, red_c_, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, hsv_h_c_, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, hsv_s_c_, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, hsv_v_c_, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, hsl_h_c_, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, hsl_s_c_, 255, cv2.THRESH_BINARY)
    _, S_ = cv2.threshold(S, hsl_l_c_, 255, cv2.THRESH_BINARY)

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

    final_mask = cv2.bitwise_and(final_mask, gray_)
    final_mask = cv2.bitwise_and(final_mask, blue_)
    final_mask = cv2.bitwise_and(final_mask, green_)
    final_mask = cv2.bitwise_and(final_mask, red_)
    # final_mask = cv2.bitwise_and(final_mask, h_)
    # final_mask = cv2.bitwise_and(final_mask, s_)
    final_mask = cv2.bitwise_and(final_mask, v_)
    # final_mask = cv2.bitwise_and(final_mask, H_)
    # final_mask = cv2.bitwise_and(final_mask, L_)
    # final_mask = cv2.bitwise_and(final_mask, S_)

    #final_mask = cv2.GaussianBlur(final_mask, (19, 19), 3)

    #final_mask = cv2.dilate(final_mask, kernel, iterations=3)
    #
    # final_mask = cv2.erode(final_mask, kernel1, iterations=1)
    #
    #final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)

    # 중요
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)
    final_mask = cv2.GaussianBlur(final_mask, (31, 31), 3)

    #final_mask = cv2.blur(final_mask, (15, 15))

    final_mask = cv2.erode(final_mask, kernel, iterations=3)
    final_mask = cv2.dilate(final_mask, kernel1, iterations=5)
    # final_mask = cv2.blur(final_mask, (17, 17))
    # final_mask = cv2.erode(final_mask, kernel, iterations=5)

    ret, final_mask = cv2.threshold(final_mask, 100, 255, cv2.THRESH_BINARY)

    final_mask = cv2.erode(final_mask, kernel, iterations=10)   # 사각형의 크기를 결정.

    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    edges = cv2.Canny(final_mask, 10, 100, apertureSize=3)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, edge_kernel)
    edges = cv2.dilate(edges, kernel, iterations=3)
    #ret, th1 = cv2.threshold(final_mask, 70, 255, cv2.THRESH_BINARY)

    #################### 중심좌표값 자동 저장용 ##########################

    # 관심영역(ROI, Range of Interest) 지정.
    for i in range(len(ROI_list)):
        img = cv2.rectangle(img, ROI_list[i][0], ROI_list[i][1], (150, 50, 150), 15)
        cv2.putText(img, 'ROI%d' % (i + 1), (ROI_list[i][0][0], ROI_list[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 3,
                    (0, 0, 255), 5, cv2.LINE_AA)

    pt_list = []
    right_mid_list = []
    left_mid_list = []
    minx_contour = []
    miny_contour = []
    square_center = []
    _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 컨투어 찾기


    if len(contours) != 0:
        for contour in contours:
            if (cv2.contourArea(contour) > 5000) and (cv2.contourArea(contour) < 80000):  # **필요한 면적을 찾아 중심점 좌표를 저장


                # 컨투어에서 사각형당 꼭지점을 찾기 위해 x,y값의 최소값을 구함.
                # if len(contour) != 0:
                #     for i in range(len(contour)):
                #         minx_contour.append(contour[i][0][0])   # x좌표에 대한 최소값을 찾기 위해. 리스트에 추가
                #         miny_contour.append(contour[i][0][1])   # y좌표에 대한 최소값을 찾기 위함.

                ball_area = cv2.contourArea(contour)
                mom = contour
                M = cv2.moments(mom)
                cx_origin = int(M['m10'] / M['m00'])
                cy_origin = int(M['m01'] / M['m00'])

                # 외곽선 근사화 시키기 (사각형의 형상을 얻기 위해)
                epsilon = 0.03 * cv2.arcLength(mom, True)
                approx = cv2.approxPolyDP(mom, epsilon, True)

                # print("근사시킨 꼭지점", approx)
                # print("approx 갯수", len(approx))

                #cv2.putText(img, 'num: %d' % (cnt), (cx_origin, cy_origin - 3), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2, cv2.LINE_AA)


                for i in range(len(ROI_list)):
                    if (cx_origin > ROI_list[i][0][0] and cy_origin > ROI_list[i][0][1]) and (cx_origin < ROI_list[i][1][0] and cy_origin < ROI_list[i][1][1]):

                        cv2.drawContours(img, [approx], 0, (255, 255, 255), 4)  # 근사화 시킨 컨투어 그리기
                        #cv2.drawContours(img, [mom], 0, (0, 255, 0), 5) # 실제 컨투어를 그림.
                        cv2.circle(img, (cx_origin, cy_origin), 15, (0, 255, 255), -1)  # 중심 좌표 표시


                        if len(approx) != 0:
                            if len(approx) == 4:
                                # midp = cal.midpoint(approx[0][0][0], approx[0][0][1], approx[3][0][0], approx[3][0][1])
                                for i in range(len(approx)):
                                    minx_contour.append(approx[i][0][0])  # x좌표에 대한 최소값을 찾기 위해. 리스트에 추가
                                    miny_contour.append(approx[i][0][1])  # y좌표에 대한 최소값을 찾기 위함.
                                    cv2.circle(img, (approx[i][0][0], approx[i][0][1]), 10, (0, 0, 255), -1)  # 근사화 사각에서의 꼭지점 표시
                                    # 왼쪽 오른쪽 중심부를 찾기 위한 선행작업.
                                    pt_list.append(tuple((minx_contour[i], miny_contour[i])))
                                    if pt_list[i][0] < cx_origin:
                                        left_mid_list.append(pt_list[i])
                                    else:
                                        right_mid_list.append(pt_list[i])


                                print("근사시킨 꼭지점", approx)
                                print("approx 갯수", len(approx))

                                print("x리스트:", minx_contour)
                                print("y리스트:", miny_contour)
                                print("중심점 x값:", cx_origin)



                                # for i in range(len(approx)):
                                #     pt_list.append(tuple((minx_contour[i], miny_contour[i])))
                                #     if pt_list[i][0] < cx_origin:
                                #         left_mid_list.append(pt_list[i])
                                #     else:
                                #         right_mid_list.append(pt_list[i])
                                #
                                # print("왼쪽좌표****", left_mid_list)
                                # print("오른쪽좌표****", right_mid_list)


                                cal = calulateCoordinate()  # 계산 클래스 객체 할당.

                                left_midpt = cal.midpoint(left_mid_list[0][0], left_mid_list[0][1], left_mid_list[1][0], left_mid_list[1][1])
                                right_midpt = cal.midpoint(right_mid_list[0][0], right_mid_list[0][1], right_mid_list[1][0], right_mid_list[1][1])
                                print("미드포인터값", left_midpt, right_midpt)

                                cv2.circle(img, left_midpt, 15, (255, 255, 255),-1)  # 근사화 시킨 사각형의 꼭지점 출력
                                cv2.circle(img, right_midpt, 15, (255, 255, 255), -1)  # 근사화 시킨 사각형의 꼭지점 출력
                                cv2.line(img, left_midpt, right_midpt, (255, 255, 255), 3)  # 사각형의 중심점을 선분으로 이음.

                                midDistance = cal.distance(left_midpt[0], left_midpt[1], right_midpt[0], right_midpt[1])
                                baseline = cal.distance(left_midpt[0], left_midpt[1], right_midpt[0], left_midpt[1])
                                height = cal.distance(right_midpt[0], right_midpt[1], right_midpt[0], left_midpt[1])
                                angle = cal.angle(baseline, height)
                                print("왼쪽의 좌표값:", left_midpt[0], left_midpt[1], right_midpt[0], right_midpt[1])
                                print("a의 좌표값", left_midpt[0], left_midpt[1], right_midpt[0], left_midpt[1])
                                print("중심점 거리값:", midDistance)
                                print("밑변 값:", baseline)
                                print("높이 값:", height)
                                print("***각도값:", angle)
                                cv2.putText(img, 'angle: %.2f' % (round(angle,2)), (cx_origin, cy_origin - 25), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 5, cv2.LINE_AA)

                        else:
                            print("사각형이 아닙니다.")

                        square_center.append([cx_origin, cy_origin])

                cnt = cnt + 1
                # 꼭지점 리스트를 비워줌
                minx_contour = []
                miny_contour = []

                left_mid_list = []
                right_mid_list = []
                pt_list = []

    # th1 = cv2.resize(th1, (1280, 960))
    # cv2.imshow('dam', th1)

    final_mask = cv2.resize(final_mask, (1280, 960))
    cv2.imshow('damm', final_mask)
    #
    if flag == 0:
        img =cv2.resize(img, (1280, 960))
        flag = 1
        cv2.imshow('ori',img)

    #edges = cv2.resize(edges, (1280, 960))
    #cv2.imshow('edge', edges)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
