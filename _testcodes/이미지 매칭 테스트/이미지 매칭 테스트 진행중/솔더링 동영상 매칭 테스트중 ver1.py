import os
import numpy as np
import cv2
import random


# 2대의 카메라 해상도 설정 및 출력.
cap0 = cv2.VideoCapture(0)
cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # Width 4608
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 960) # Height 3288
print("첫번째 카메라 현재 해상도 %d x %d" %(cap0.get(3), cap0.get(4)))

cap1 = cv2.VideoCapture(1)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 4608) # Width 4608
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 3288) # Height 3288
print("두번째 카메라 현재 해상도 %d x %d" %(cap1.get(3), cap1.get(4)))

##################### 관리자 지정 #########################################

# 검출할 영역(관심영역)을 지정 (start point to end point of Rectangle Box).
s_pt = (30, 200)
e_pt = (1200, 500)

## 추가한 template의 갯수만큼 <threshold, sensitivity> 지정. 지정안할 시 default값이 들어감.
template_setting = [
    [0.855, 300],
    [0.859, 300],
    [0.859, 300],
    [0.855, 300]
]

##########################################################################

# template 의 저장위치
path = "./templates/"
file_list = os.listdir(path)
print("저장된 template의 갯수:", len(file_list))

# 초기값
total_count = 0

# 2차원 배열.
template_list = []
template_str = []
template_mat_format = []
w_h_list = []
bgr_list = []
for i in range(len(file_list)):

    template_str = [path + file_list[i]]
    template_list.append(template_str)
    a = cv2.imread(template_list[i][0], 0)      # 이미지 행렬 포멧을 a으로 저장
    template_mat_format.append(a)               # a 행렬을 리스트에 추가
    w_h_list.append([a.shape[0], a.shape[1]])   # template 의 w(x), h(y)값 리스트를 저장.
    ran_b = random.randrange(0, 256)           # 마크를 위한 랜덤 색상.
    ran_g = random.randrange(0, 256)
    ran_r = random.randrange(0, 256)
    bgr_list.append((ran_b, ran_g, ran_r))

# print("색상은?",bgr_list)
# print(w_h_list)                         # template의 폭과 높이에 대한 리스트
# print(w_h_list[0][0], w_h_list[0][1])   # 첫번째 template의 h,w값
# print(w_h_list[1][0], w_h_list[1][1])   # 두번째 template의 h,w값
# print(w_h_list[2][0], w_h_list[2][1])
# print(w_h_list[3][0], w_h_list[3][1])
#
# print(template_mat_format)      # template의 2차원 배열에 대한 정보.
# cv2.imshow('0', template_mat_format[0])
# cv2.imshow('1', template_mat_format[1])   # 배열 출력.
# cv2.imshow('3', template_mat_format[3])

# threshold Default=0.815, 옵션이므로 3번째 인자에 튜닝된 값을 넣으면 된다.

def match_template(grayimg, template_mat, threshold=0.859):

    res = cv2.matchTemplate(grayimg, template_mat, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    return loc                          # match된 위치를 반환.

# match point를 찾는 함수. sensitivity는 옵션값으로 갯수를 샐 포인트값에 대한 민감도.
def find_loop(img, loc, color, sensitivity=500):

    f = set()
    # 매칭된 좌표값 Return as pt
    for pt in zip(*loc[::-1]):

        # 관심영역(ROI)으로 판독 제한
        if (pt[0] > s_pt[0] and pt[1] > s_pt[1]) and (
                (pt[0] + w_h_list[1][1] < e_pt[0]) and (pt[1] + w_h_list[1][0] < e_pt[1])):
            cv2.rectangle(img, pt, (pt[0] + w_h_list[1][1], pt[1] + w_h_list[1][0]), color, 1)  # 마킹
            f.add((round(pt[0] / sensitivity), round(pt[1] / sensitivity)))
    found_count = len(f)
    return found_count  # 찾은 갯수를 리턴.

def execute():
    global total_count

    while (True):
        total_count = 0

        # 프레임 읽기
        ret, frame = cap1.read()
        # 화면 크기 조절 (본인에게 맞는 해상도 조절)
        result = cv2.resize(frame, (1280, 960), interpolation=cv2.INTER_LINEAR)
        img_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)                          # gray로 변환.

        # 관심영역(ROI, Range of Interest) 지정.
        result = cv2.rectangle(result, s_pt, e_pt, (255, 0, 0), 2)
        cv2.putText(result, 'ROI', (s_pt[0], s_pt[1]-3), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        try:
            for i in range(len(file_list)):
                loc = match_template(img_gray, template_mat_format[i], template_setting[i][0])  # 첫번째 template
                found_count = find_loop(result, loc, bgr_list[i], template_setting[i][1])
                total_count = total_count + found_count
        except:
            print("Error Message : 등록한 template의 갯수만큼 동일한 <Thresold값, Sensitivity값> 을 입력해야 합니다.")
            return -1


        # # template 하나당 세트의 함수를 추가해야 함.
        # loc = match_template(img_gray, template_mat_format[0], template_setting[0][0])     # 첫번째 template
        # found_count = find_loop(result, loc, bgr_list[0], template_setting[0][1])
        # total_count = total_count + found_count
        # #print("1st count : ", found_count)
        #
        # loc = match_template(img_gray, template_mat_format[1], template_setting[1][0])     # 두번째 template
        # found_count = find_loop(result, loc, bgr_list[1], template_setting[1][1])
        # total_count = total_count + found_count
        # #print("2nd count : ", found_count)
        #
        # loc = match_template(img_gray, template_mat_format[2], template_setting[2][0])     # 세번째 template
        # found_count = find_loop(result, loc, bgr_list[2], template_setting[2][1])
        # total_count = total_count + found_count
        # #print("3nd count : ", found_count)
        #
        # loc = match_template(img_gray, template_mat_format[3], template_setting[3][0])  # 세번째 template
        # found_count = find_loop(result, loc, bgr_list[3], template_setting[3][1])
        # total_count = total_count + found_count
        # # print("3nd count : ", found_count)

        print("total count:", total_count)
        cv2.imshow('Test', result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap1.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 메인함수
    execute()