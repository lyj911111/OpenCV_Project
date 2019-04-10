import cv2
from more_itertools import unique_everseen
import numpy as np


##### Right ###########
# 큰 리벳 검출할 영역(관심영역)을 지정 (start point to end point of Rectangle Box).
ROI_list = [
    [(5, 90), (500, 950)],
 ]

# 작은 리벳 검출할 영역(관심영역)을 지정 (start point to end point of Rectangle Box).
ROI_list_small = [
    [(550, 90), (720, 950)]
 ]
result = cv2.imread('C:/AceVision/right.png')   # 원형이 있는 이미지를 올림.
result = cv2.resize(result, (1280, 960), interpolation=cv2.INTER_LINEAR)
cv2.imshow("raw", result)

'''


##### Left ##########
result = cv2.imread('C:/AceVision/left.png')   # 원형이 있는 이미지를 올림.
result = cv2.resize(result, (1280, 960), interpolation=cv2.INTER_LINEAR)
cv2.imshow("raw", result)
# 큰 리벳 검출할 영역(관심영역)을 지정 (start point to end point of Rectangle Box).
ROI_list = [
    [(640, 30), (1300, 940)],
 ]

# 작은 리벳 검출할 영역(관심영역)을 지정 (start point to end point of Rectangle Box).
ROI_list_small = [
    [(30, 90), (500, 950)]
 ]
 '''

'''
result = cv2.imread('C:/AceVision/123.png')   # 원형이 있는 이미지를 올림.
result = cv2.resize(result, (1280, 960), interpolation=cv2.INTER_LINEAR)
cv2.imshow("raw", result)
# 큰 리벳 검출할 영역(관심영역)을 지정 (start point to end point of Rectangle Box).
ROI_list = [
    [(50, 0), (1000, 960)],
 ]

# 작은 리벳 검출할 영역(관심영역)을 지정 (start point to end point of Rectangle Box).
ROI_list_small = [
    [(1050, 0), (1250, 960)]
 ]
'''

# 예외처리 박스
ex_w = 30   # 가로 x 세로
ex_h = 30
except_box = [
    [(698, 60)],
    [(369, 320)]
]

def nothing(x):
    pass

def houghCircle():
    global ratio, gap, Param1, Param2, minR, maxR, result
    total_cir = 0


    result = cv2.resize(result, (1280, 960), interpolation=cv2.INTER_LINEAR)
    img2 = result.copy()

    img2 = cv2.GaussianBlur(img2, (9, 9), 0) # 0~9까지 가우시안 필터로 흐리게 만들어 조절함.

    imgray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) # 그레이 이미지로 바꿔서 실행해야함.

    # 큰 리벳 관심영역(ROI, Range of Interest) 지정.
    for i in range(len(ROI_list)):
        result = cv2.rectangle(result, ROI_list[i][0], ROI_list[i][1], (150, 50, 150), 5)
        #cv2.putText(result, 'big ROI%d' % (i + 1), (ROI_list[i][0][0], ROI_list[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # 큰 리벳 예외처리(Exception Box) 지정.
    for i in range(len(except_box)):
        result = cv2.rectangle(result, except_box[i][0], (except_box[i][0][0] + ex_w, except_box[i][0][1] + ex_h), (0, 255, 0), 1)
        #cv2.putText(result, 'big_expt%d' % (i + 1), (except_box[i][0][0], except_box[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)

###########################################################################################################################

    # 작은 리벳 관심영역(ROI, Range of Interest) 지정.
    for i in range(len(ROI_list_small)):
        result = cv2.rectangle(result, ROI_list_small[i][0], ROI_list_small[i][1], (50, 150, 50), 5)
        #cv2.putText(result, 'sml ROI%d' % (i + 1), (ROI_list_small[i][0][0], ROI_list_small[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

###########################################################################################################################

    # 큰 원을 탐지.
    # param1 = 250, param2 = 20
                                 # 원본과 비율 / 찾은 원들간의 최소 중심거리 / param1, param2를 조절해 원을 찾음
    circles = cv2.HoughCircles(imgray, cv2.HOUGH_GRADIENT, 1, 13, param1=110, param2=9, minRadius=4, maxRadius=7)

    # 큰 원형 탐지 시작.
    if circles is not None:
        circles = np.uint16(np.around(circles))

        whole_circle_list1 = []
        whole_circle_tuple = []
        except_center_list = []
        circle_area_list = []
        for i in circles[0, :]:

            # 큰원의 관심영역
            for j in range(len(ROI_list)):
                if (i[0] > ROI_list[j][0][0] and i[0] < ROI_list[j][1][0]) and (i[1] > ROI_list[j][0][1] and i[1] < ROI_list[j][1][1]):  # ROI 관심영역 내에서 찾아냄.
                    whole_circle_list1.append([i[0], i[1]])  # ROI 내 모든 중심점.
                    circle_area_list.append(i[2])
                    # 큰원 내 예외처리
                    for k in range(len(except_box)):
                        if (i[0] > except_box[k][0][0] and i[0] < (except_box[k][0][0] + ex_w)) and (i[1] > except_box[k][0][1] and i[1] < (except_box[k][0][1] + ex_h)):
                            except_center_list.append([i[0], i[1]])  # 예외처리 중심점을 리스트에 추가
                            whole_circle_list1.remove(except_center_list[0])  # 예외처리 리스트에 있는 중심점들을 전체 중심점리스트에서 제거
                            #print("예외처리 중심점:", except_center_list)
                            except_center_list.pop()                         # 제외 처리를 하고나서 값을 빼서 다음 값을 프로세스 진행하도록 함 (for문을 반복하기 위해)


                    length = len(whole_circle_list1)-1
                    whole_circle_tuple.append(tuple(whole_circle_list1[length]))
                    #print("튜플로 변환된", whole_circle_tuple)

        whole_circle_tuple = list(unique_everseen(whole_circle_tuple))     # 겹치는 항목 제거
        for z in range(len(whole_circle_tuple)):
            cv2.circle(result, whole_circle_tuple[z], circle_area_list[z], (0, 0, 255), 2)  # 원 외곽 컨투어 표시.
            cv2.circle(result, whole_circle_tuple[z], 3, (255, 0, 40), -1)  # 원의 중심점을 표시

        total_cir = total_cir + len(whole_circle_tuple)
        print("큰원의 갯수:", len(whole_circle_tuple))
#####################################################################################################
    # 작은 원을 탐지
    sml_circles = cv2.HoughCircles(imgray, cv2.HOUGH_GRADIENT, 1, 13, param1=110, param2=8, minRadius=2, maxRadius=4)


    # 작은 원형 탐지 시작.
    if sml_circles is not None:
        sml_circles = np.uint16(np.around(sml_circles))

        whole_circle_list2 = []
        whole_circle_tuple = []
        circle_area_list2 = []
        for i in sml_circles[0, :]:

            # 작은 원의 관심영역
            for j in range(len(ROI_list_small)):
                if (i[0] > ROI_list_small[j][0][0] and i[0] < ROI_list_small[j][1][0]) and (i[1] > ROI_list_small[j][0][1] and i[1] < ROI_list_small[j][1][1]):  # ROI 관심영역 내에서 찾아냄.
                    whole_circle_list2.append([i[0], i[1]])                          # ROI 내 모든 중심점.
                    circle_area_list2.append(i[2])

                    length = len(whole_circle_list2) - 1                             # list를 tuple로 바꾸기 위해 index값 추출.
                    whole_circle_tuple.append(tuple(whole_circle_list2[length]))     # 그 index를 이용해서 tuple로 변경.
                    # print("튜플로 변환된", whole_circle_tuple)

        for z in range(len(whole_circle_tuple)):
            cv2.circle(result, whole_circle_tuple[z], circle_area_list2[z], (0, 0, 255), 2)  # 원 외곽 컨투어 표시.
            cv2.circle(result, whole_circle_tuple[z], 3, (255, 0, 40), -1)  # 원의 중심점을 표시

        total_cir = total_cir + len(whole_circle_tuple)
        print("작은원의 갯수:", len(whole_circle_tuple))

        print("전체원의 갯수:", total_cir)
            # # 작은원의 관심영역
            # for j in range(len(ROI_list_small)):
            #     if (i[0] > ROI_list_small[j][0][0] and i[0] < ROI_list_small[j][1][0]) and (i[1] > ROI_list_small[j][0][1] and i[1] < ROI_list_small[j][1][1]):  # ROI 관심영역 내에서 찾아냄.
            #         cv2.circle(result, (i[0], i[1]), i[2], (0, 0, 255), 2)  # 원 외곽 컨투어 표시.
            #         cv2.circle(result, (i[0], i[1]), 3, (255, 0, 40), -1)  # 원의 중심점을 표시

        #cv2.imshow('ori',img2)
        cv2.imshow('HoughCircle', result)


        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('원을 찾을 수 없음')



houghCircle()

