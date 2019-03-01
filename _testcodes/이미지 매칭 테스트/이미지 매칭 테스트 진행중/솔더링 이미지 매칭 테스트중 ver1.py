import cv2
import numpy as np
from matplotlib import pyplot as plt

# 검출할 영역(관심영역)을 지정 (start point to end point of Rectangle Box).
s_pt = (30, 400)
e_pt = (1200, 500)

# before_point (이전좌표를 저장하기 위함)
bfr_pt = 0
init_pt = 0
max_cnt = 0
initial_flag = 0
base_flag = 0

# 중복 제거
def tuples(A):
    try: return tuple(tuples(a) for a in A)
    except TypeError: return A

# 메인실행 함수.
def execute():
    global bfr_pt, max_cnt, init_pt, initial_flag, base_pt

    # 원본 불러오기.
    img_rgb = cv2.imread('3.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)  # gray로 변환.
    result = img_rgb.copy()                               # 결과출력을 위한 원본 복사

    # 관심영역(ROI, Range of Interest) 지정.
    result = cv2.rectangle(result, s_pt, e_pt, (255, 0, 0), 2)
    cv2.putText(result, 'ROI', s_pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # 이미지 매칭할 template 불러옴. (2개의 template으로 이미지 매칭)
    template1 = cv2.imread('Vtemplate1.jpg',0)
    template2 = cv2.imread('Vtemplate2.jpg',0)

    # 매칭할 template의 가로, 세로 사이즈를 return
    w1, h1 = template1.shape[::-1]
    w2, h2 = template2.shape[::-1]




    ## 1번째 template 매칭.
    res1 = cv2.matchTemplate(img_gray,template1,cv2.TM_CCOEFF_NORMED)
    # 이미지 매칭률을 결정함.
    threshold = 0.815
    loc = np.where(res1 >= threshold)

    f = set()

    # 매칭된 좌표값 Return as pt
    for pt in zip(*loc[::-1]):

        # 관심영역(ROI)으로 판독 제한
        if (pt[0] > s_pt[0] and pt[1] > s_pt[1]) and ( (pt[0] + w1 < e_pt[0]) and (pt[1] + h1 < e_pt[1])):

            cv2.rectangle(result, pt, (pt[0] + w1, pt[1] + h1), (0, 0, 255), 1)     # 마킹

            # sensitivity = 580 => 확인 후 값 고정
            sensitivity = 300

            f.add((round(pt[0] / sensitivity), round(pt[1] / sensitivity)))

    found_count = len(f)
    print("1st count : ", found_count)




    ## 2번째 template 매칭.
    res2 = cv2.matchTemplate(img_gray, template2, cv2.TM_CCOEFF_NORMED)
    # 이미지 매칭률을 결정함.
    threshold = 0.72
    loc = np.where(res2 >= threshold)

    f = set()

    # 매칭된 좌표값 Return as pt
    for pt in zip(*loc[::-1]):

        # 관심영역(ROI)으로 판독 제한
        if (pt[0] > s_pt[0] and pt[1] > s_pt[1]) and ((pt[0] + w2 < e_pt[0]) and (pt[1] + h2 < e_pt[1])):
            cv2.rectangle(result, pt, (pt[0] + w2, pt[1] + h2), (0, 255, 0), 1)  # 마킹

            # sensitivity = 580 => 확인 후 값 고정
            sensitivity = 300

            f.add((round(pt[0] / sensitivity), round(pt[1] / sensitivity)))

    found_count = len(f)
    print("2nd count : ", found_count)





    # # 2번째 template 매칭.
    # res2 = cv2.matchTemplate(img_gray,template2,cv2.TM_CCOEFF_NORMED)
    # # 이미지 매칭률을 결정함.
    # threshold = 1.0
    # loc = np.where(res2 >= threshold)
    #
    # cnt = 0
    # max_cnt = 0
    # cnt_list = []
    # for pt in zip(*loc[::-1]):
    #
    #     if cnt == 0:
    #         cnt_list = []
    #
    #     if (pt[0] > s_pt[0] and pt[1] > s_pt[1]) and ((pt[0] + w2 < e_pt[0]) and (pt[1] + h2 < e_pt[1])):  # 관심영역(ROI)으로 판독 제한.
    #
    #         cnt = cnt + 1  # 매칭률에 따라 얼마나 매칭시켰는지 갯수를 셈.
    #
    #         cv2.rectangle(result, pt, (pt[0] + w2, pt[1] + h2), (0, 255, 0), 1)  # 판독위치 마킹.
    #         cnt_list.append(cnt)
    #         max_cnt = max(cnt_list)  # 판독 갯수 중 최대값 저장.
    #         str_cnt = str(max_cnt)   # string 으로 변환
    #
    #         # 초기에 before_point가 없으므로 있을경우에 if문 진입.
    #         if bfr_pt:
    #
    #             # x, y 좌표가 급격히 변하는 부분일때.
    #             if (abs(bfr_pt[1] - pt[1]) > 10) or (abs(bfr_pt[0] - pt[0]) > 10):
    #                 cv2.putText(result, 'match:' + str_cnt, bfr_pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
    #                 cnt = 0
    #         bfr_pt = pt
    # if max_cnt:
    #     str_cnt = str(max_cnt)
    #     cv2.putText(result, 'match:' + str_cnt, bfr_pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
    # else:
    #     print('no matched with template 2')




    cv2.imshow('res.png',result)
    cv2.waitKey(0)

if __name__ == "__main__":

    #카메라 번호 선택 0~2
    execute()