import numpy as np
import cv2

# 해상도 결정, 출력.
cap0 = cv2.VideoCapture(0)
cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # Width 4608
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 960) # Height 3288
print("첫번째 카메라 현재 해상도 %d x %d" %(cap0.get(3), cap0.get(4)))


cap1 = cv2.VideoCapture(1)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 4608) # Width 4608
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 3288) # Height 3288
print("두번째 카메라 현재 해상도 %d x %d" %(cap1.get(3), cap1.get(4)))

# 검출할 영역(관심영역)을 지정 (start point to end point of Rectangle Box).
s_pt = (30, 200)
e_pt = (1200, 500)

# before_point (이전좌표)
bfr_pt = 0

def execute():


    while (True):
        global bfr_pt

        # 프레임 읽기
        ret, frame = cap1.read()
        # 화면 크기 조절 (본인에게 맞는 해상도 조절)
        result = cv2.resize(frame, (1280, 960), interpolation=cv2.INTER_LINEAR)
        img_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)                          # gray로 변환.

        # 관심영역(ROI, Range of Interest) 지정.
        result = cv2.rectangle(result, s_pt, e_pt, (255, 0, 0), 2)
        cv2.putText(result, 'ROI', (s_pt[0], s_pt[1]-3), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # 이미지 매칭할 template 불러옴. (2개의 template으로 이미지 매칭)
        template1 = cv2.imread('Vtemplate1.jpg', 0)
        template2 = cv2.imread('Vtemplate2.jpg', 0)

        # 매칭할 template의 가로, 세로 사이즈를 return
        w1, h1 = template1.shape[::-1]
        w2, h2 = template2.shape[::-1]

        ## 1번째 template 매칭.
        res1 = cv2.matchTemplate(img_gray, template1, cv2.TM_CCOEFF_NORMED)
        # 이미지 매칭률을 결정함.
        threshold = 0.805 # 0.815
        loc = np.where(res1 >= threshold)

        f = set()
        # 매칭된 좌표값 Return as pt
        for pt in zip(*loc[::-1]):

            # 관심영역(ROI)으로 판독 제한
            if (pt[0] > s_pt[0] and pt[1] > s_pt[1]) and ((pt[0] + w1 < e_pt[0]) and (pt[1] + h1 < e_pt[1])):
                cv2.rectangle(result, pt, (pt[0] + w1, pt[1] + h1), (0, 0, 255), 1)  # 마킹

                # sensitivity = 580 => 확인 후 값 고정
                sensitivity = 300

                f.add((round(pt[0] / sensitivity), round(pt[1] / sensitivity)))

        found_count = len(f)
        print("1st count : ", found_count)

        ## 2번째 template 매칭.
        res2 = cv2.matchTemplate(img_gray, template2, cv2.TM_CCOEFF_NORMED)
        # 이미지 매칭률을 결정함.
        threshold = 0.859
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


        #cv2.namedWindow('window title', cv2.WINDOW_NORMAL)
        #cv2.imshow('window title', gray)
        cv2.imshow('Test', result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap1.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 메인함수
    execute()