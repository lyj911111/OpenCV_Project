'''
    Resized된 화면에서 원하는 부분의 ROI 잡으면,
    원본영상에서 확대되어 출력.

    "i" key              : 화면 정지, ROI 지정모드
    마우스 좌클릭-드레그 : ROI 지정

'''

import cv2
import numpy as np
import glob
import re
import pyzbar.pyzbar as pyzbar

col, width, row, height = -1, -1, -1, -1
frame = None
frame2 = None
inputmode = False
rectangle = False
trackWindow = None
roi_hist = None


# 키보드 'i' 키를 누를때, 화면을 멈추고 마우스 클릭 모드 활성화
def onMouse(event, x, y, flags, param):
    global col, width, row, height, frame, frame2, inputmode, img
    global rectangle, roi_hist, trackWindow

    if inputmode:
        # 왼쪽 마우스 클릭시 rectangle 플레그 활성화,
        if event == cv2.EVENT_LBUTTONDOWN:
            rectangle = True                # 마우스가 움직일때 이벤트를 발생시키기 위해
            col, row = x, y                 # 왼쪽마우스 클릭시 좌표를 기억.
            print("왼쪽마우스 클릭 위치", x, y)
        # 마우스를 움직일 때 발생 이벤트
        elif event == cv2.EVENT_MOUSEMOVE:
            if rectangle:
                # 멈춘 화면에서 진행.
                frame = frame2.copy()
                cv2.rectangle(frame, (col, row), (x, y), (0, 255, 0), 2)
                cv2.imshow('frame', frame)
        elif event == cv2.EVENT_LBUTTONUP:
            print("좌표", (col, row), (x, y))

            inputmode = False
            rectangle = False
            cv2.rectangle(frame, (col, row), (x, y), (0, 255, 0), 2)
            height, width = abs(row - y), abs(col - x)
            trackWindow = (col, row, width, height)

            # 선택영역 확대
            displayRate(img, col, row, x, y)

            # roi_hist = cv2.calcHist([roi], [0], None, [180], [0, 180])
            # cv2.normalize(roi_hist, roi_hist, 0, 255 , cv2.NORM_MINMAX)
    return


def decode(im):
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)

    print(decodedObjects)

    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data, '\n')

    return decodedObjects


# Display barcode and QR code location
def display(im, decodedObjects):
    # Loop over all decoded objects
    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        # Number of points in the convex hull
        n = len(hull)

        # Draw the convext hull
        for j in range(0, n):
            cv2.line(im, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

    # 각도 회전시켜 수평으로 맞춤.
    im = rotate_bound(im, -90)

    # Display results
    cv2.imshow("Results", im)
    cv2.waitKey(0)
    cv2.destroyWindow('Results')        # 화면 파괴


'''
    함수) Resized된 ROI 구간을 원본영상에서 확대
        화면 비율 원본 - 4024 : 3036
        축소 비율      - 1260 : 960
        (계산 x축 => 1260:4024 = 1:x)
        (계산 y축 => 960:3036 = 1:y)
        화면 배율 x = 3.1936, y = 3.1625
        
        param
            ori_img : 원본 영상
            x1, y1  : Resized 된 영상속에서 ROI 지정. (시작지점)
            x2, y2  : Resized 된 영상속에서 ROI 지정. (끝지점)
'''
def displayRate(ori_img, x1, y1, x2, y2):

    x1 = int(x1 * 3.1936)
    x2 = int(x2 * 3.1936)
    y1 = int(y1 * 3.1625)
    y2 = int(y2 * 3.1625)

    # ROI 영역 원본영상에서 확대
    roi = ori_img[y1:y2, x1:x2]

    # 바코드가 선명해지도록 Contrast(대조) 적용
    roi = img_Contrast(roi)

    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    decodedObjects = decode(roi)
    display(roi, decodedObjects)

    # print(st_pt)
    # print(end_pt)


'''
    함수) 이미지와 각도를 입력하면, 회전된 이미지를 리턴.
'''
def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))


'''
    함수) 이미지를 더 선명하게 Contrast(대조) 기법을 적용시킴.
        
        param : 컬러 이미지
        return : 대조된 이미지
'''
def img_Contrast(img):

    # -----Converting image to LAB Color model-----------------------------------
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # -----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)

    # -----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    # -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl, a, b))

    # -----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return final


def main():
    global frame2, frame, inputmode, trackWindow, roi_hist, img

    # img = cv2.imread("./img/backside.bmp")  # 연속 이미지 취득 (비디오 프레임 가정) - 정상제품
    img = cv2.imread("./img/backside_no.bmp")  # 연속 이미지 취득 (비디오 프레임 가정) - 불량품

    # 해상도 지정.
    resolution = (1260, 960)

    # 기본 프레임.
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', onMouse, param=(frame, frame2))    # 'frame' 이라는 화면에 마우스 콜백 함수가 뒤에서 실행

    while True:
        #img = cv2.imread("./img/backside.bmp")     # 연속 이미지 취득 (비디오 프레임 가정) - 정상제품
        img = cv2.imread("./img/backside_no.bmp")  # 연속 이미지 취득 (비디오 프레임 가정) - 불량품

        frame = img.copy()
        frame = cv2.resize(frame, resolution)
        # print(frame.shape)

        print('continue')
        cv2.imshow('frame', frame)

        k = cv2.waitKey(1)
        if k == 27:  # ESC 종료
            break

        # i 키를 누를때 input Mode 활성화하고 화면을 멈춤. (바코드 리딩할 ROI 지정)
        if k == ord('i'):
            print('Select Area for Camshift and Enter a Key')
            inputmode = True
            frame2 = frame.copy()

            while inputmode:
                cv2.imshow('frame', frame)
                cv2.waitKey(0)


if __name__ == "__main__":
    main()