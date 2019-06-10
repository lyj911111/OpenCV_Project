import cv2
import numpy as np

def nothing(x):
    pass

def img_filtering(img):

    img = cv2.GaussianBlur(img, (5, 5), 0)      # Blur 필터링

    frame2 = img.copy()  # 영상원본

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blue, green, red = cv2.split(img)  # 원본에서 BGR 분리
    frame_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
    h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

    frame_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
    H, L, S = cv2.split(frame_hls)  # H,L,S 분리
    # kernel = np.ones((3, 3), np.uint8)

    _, gray1 = cv2.threshold(gray_frame, 255, 255, cv2.THRESH_BINARY_INV)
    _, blue1 = cv2.threshold(blue, 255, 255, cv2.THRESH_BINARY_INV)
    _, green1 = cv2.threshold(green, 255, 255, cv2.THRESH_BINARY_INV)
    _, red1 = cv2.threshold(red, 255, 255, cv2.THRESH_BINARY_INV)
    _, h1 = cv2.threshold(h, 128, 255, cv2.THRESH_BINARY_INV)
    _, s1 = cv2.threshold(s, 128, 255, cv2.THRESH_BINARY_INV)
    _, v1 = cv2.threshold(v, 255, 255, cv2.THRESH_BINARY_INV)
    _, H1 = cv2.threshold(H, 128, 255, cv2.THRESH_BINARY_INV)
    _, L1 = cv2.threshold(L, 255, 255, cv2.THRESH_BINARY_INV)
    _, S1 = cv2.threshold(S, 128, 255, cv2.THRESH_BINARY_INV)

    _, blue_ = cv2.threshold(blue, 90, 255, cv2.THRESH_BINARY)
    _, green_ = cv2.threshold(green, 90, 255, cv2.THRESH_BINARY)
    _, red_ = cv2.threshold(red, 90, 255, cv2.THRESH_BINARY)
    _, h_ = cv2.threshold(h, 128, 255, cv2.THRESH_BINARY)
    _, s_ = cv2.threshold(s, 128, 255, cv2.THRESH_BINARY)
    _, v_ = cv2.threshold(v, 90, 255, cv2.THRESH_BINARY)
    _, H_ = cv2.threshold(H, 128, 255, cv2.THRESH_BINARY)
    _, L_ = cv2.threshold(L, 128, 255, cv2.THRESH_BINARY)
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

    result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

    # Bushing 만 있는 구간만 뽑아내기 위해 마스크를 씌움.
    global Mask1st, Mask2nd
    Mask1st = [(910, 3), (990, 40)]
    Mask2nd = [(920, 920), (995, 955)]
    ROImask = np.zeros(img.shape[:2], np.uint8)
    ROImask = cv2.rectangle(ROImask, Mask1st[0], Mask1st[1], (255, 255, 255), -1)  # 첫번째 사각 마스크
    ROImask = cv2.rectangle(ROImask, Mask2nd[0], Mask2nd[1], (255, 255, 255), -1)  # 두번째 사각 마스크
    final_mask = cv2.bitwise_and(final_mask, final_mask, mask=ROImask)  # 합성하여 뽑아냄.


    #cv2.imshow('c', img)
    #cv2.imshow('b',ROImask)
    cv2.imshow('a',final_mask)
    cv2.waitKey(0)

    return final_mask


'''
    함수) threshold 이진화된 영상을 받아 면적값과 중심점값을 반환.
    
        param
            masked_img : Threshold 영상 (이진화 영상)
        
        return
            center_pt :  좌표 List
'''
def find_area(masked_img, img):

    centerPoint = []
    try:
        _, contours, _ = cv2.findContours(masked_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
    except:
        contours, _ = cv2.findContours(masked_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기

    if len(contours) != 0:
        for contour in contours:
            if (cv2.contourArea(contour) > 1000) and (cv2.contourArea(contour) < 5000):  # **필요한 면적을 찾아 중심점 좌표를 저장 (영역 제한)
                # area = cv2.contourArea(contour)       # 면적값 출력
                # print(area)
                mom = contour
                M = cv2.moments(mom)
                cx_origin = int(M['m10'] / M['m00'])
                cy_origin = int(M['m01'] / M['m00'])
                cv2.drawContours(img, contour, -1, (0, 255, 0), 2)
                cv2.circle(img, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시
                centerPoint.append([cx_origin, cy_origin])

        return centerPoint


'''
    함수)
        
        param
            coord     : 좌표 List
            imgSize_h :

'''
def judge(img ,coordList, imgSize_h):
    global Mask1st, Mask2nd

    imgSize_h = int(imgSize_h/2)
    print(coordList)
    print(imgSize_h)
    if coordList == None:     # 없을 때
        cv2.putText(img, 'UpperSide NG', (Mask1st[0][0], Mask1st[1][1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(img, 'LowerSide NG', (Mask2nd[0][0], Mask2nd[1][1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    elif len(coordList) == 1:   # 1개 있을 때
        if coordList[0][1] < imgSize_h:         # 위에만 있을 때
            print("값은?", coordList[0][1])
            cv2.putText(img, 'UpperSide OK', (Mask1st[0][0], Mask1st[1][1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(img, 'LowerSide NG', (Mask2nd[0][0], Mask2nd[1][1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:                                   # 아래만 있을 때
            cv2.putText(img, 'UpperSide NG', (Mask1st[0][0], Mask1st[1][1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(img, 'LowerSide OK', (Mask2nd[0][0], Mask2nd[1][1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:                       # 2개 있을 때
        cv2.putText(img, 'UpperSide OK', (Mask1st[0][0], Mask1st[1][1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img, 'LowerSide OK', (Mask2nd[0][0], Mask2nd[1][1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

def main():

    while True:
        # 이미지 불러오기
        #img = cv2.imread('./img/backside.bmp')  # Bushing 있을 때
        #img = cv2.imread('./img/nobushing.bmp')  # Bushing 없을 때
        img = cv2.imread('./img/onebushing.bmp')  # Bushing 없을 때
        img = cv2.resize(img, (1260, 960))
        size_h = img.shape[0]   # 세로사이즈
        size_w = img.shape[1]   # 가로사이즈
        #print(size_w, size_h)

        # 이미지 필터링
        final_mask = img_filtering(img)

        cv2.imshow('final msk', final_mask)

        # Bushing 의 좌표
        centerptList = find_area(final_mask, img)
        print(centerptList)

        judge(img , centerptList, size_h)

        # centerPoint = []
        # try:
        #     _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
        # except:
        #     contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
        # print("갯수",len(contours))
        # if len(contours) != 0:
        #     for contour in contours:
        #         if (cv2.contourArea(contour) > 1000) and (cv2.contourArea(contour) < 5000):  # **필요한 면적을 찾아 중심점 좌표를 저장 (영역 제한)
        #             print("갯수", len(contour))
        #             area = cv2.contourArea(contour)
        #             cv2.drawContours(img, contour, -1, (0, 255, 0), 2)
        #             mom = contour
        #             M = cv2.moments(mom)
        #             cx_origin = int(M['m10'] / M['m00'])
        #             cy_origin = int(M['m01'] / M['m00'])
        #
        #             cv2.circle(img, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시
        #             centerPoint.append([cx_origin, cy_origin])
        #
        #             print(area)
        #     print(centerPoint)

        cv2.imshow('ori',img)

        k = cv2.waitKey(0) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()