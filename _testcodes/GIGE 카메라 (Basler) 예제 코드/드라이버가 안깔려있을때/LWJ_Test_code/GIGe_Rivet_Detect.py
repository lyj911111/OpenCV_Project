'''
A simple Program for grabing video from basler camera and converting it to opencv frame.
Tested on Basler acA1300-200uc (USB3, linux 64bit , python 3.5)

'''
from pypylon import pylon, genicam
import numpy as np
import cv2

#  사용할 device 정보 찾기
maxCamerasToUse = 2                                                     # 사용할 "최대"카메라 갯수.
tlFactory = pylon.TlFactory.GetInstance()
devices = tlFactory.EnumerateDevices()
if len(devices) == 0:                                                   # device가 없으면 오류 띄우기.
    raise pylon.RUNTIME_EXCEPTION("No camera present.")
cameras = pylon.InstantCameraArray(min(len(devices), maxCamerasToUse))
l = cameras.GetSize()                                                   # 연결된 장치 갯수 출력
print(l, "개 카메라 연결")

camera_list = []    # 사용할 카메라의 instance 주소값을 리스트로 저장

# 연결된 장치 이름들 출력 (cameras는 Array로 주소값을 갖고있음)
for i, cam in enumerate(cameras):
    cam.Attach(tlFactory.CreateDevice(devices[i]))
    camera_list.append(cam)                                     # 카메라 instance 주소값을 리스트에 추가.
    # Print the model name of the camera.
    print("사용 카메라 모델명: ", cam.GetDeviceInfo().GetModelName())  # 연결된 카메라 이름 출력

##############################################################################
# conecting to the first available camera
#camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

def nothing(x):
    pass

def execute(num):

    # num 은 카메라 번호. 0~부터 사용할 카메라 선택.
    camera = camera_list[num]

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    # 필터링 트렉바 생성.
    cv2.namedWindow('Trackbars', cv2.WINDOW_NORMAL)
    # FIND_BLACK
    cv2.createTrackbar("graybar", "Trackbars", 225, 255, nothing)  # 135
    cv2.createTrackbar("bluebar", "Trackbars", 255, 255, nothing)  # 110
    cv2.createTrackbar("greenbar", "Trackbars", 255, 255, nothing)  # 101
    cv2.createTrackbar("redbar", "Trackbars", 255, 255, nothing)  # 101
    cv2.createTrackbar("hsv hbar", "Trackbars", 255, 255, nothing)  # 255
    cv2.createTrackbar("hsv sbar", "Trackbars", 255, 255, nothing)  # 115
    cv2.createTrackbar("hsv vbar", "Trackbars", 255, 255, nothing)  # 141
    cv2.createTrackbar("hsl hbar", "Trackbars", 255, 255, nothing)  # 255
    cv2.createTrackbar("hsl sbar", "Trackbars", 255, 255, nothing)  # 170
    cv2.createTrackbar("hsl lbar", "Trackbars", 255, 255, nothing)  # 175

    # cv2.createTrackbar("graybar_", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("bluebar_", "Trackbars", 0, 255, nothing)  # 33
    cv2.createTrackbar("greenbar_", "Trackbars", 5, 255, nothing)  # 35
    cv2.createTrackbar("redbar_", "Trackbars", 5, 255, nothing)
    cv2.createTrackbar("hsv hbar_", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("hsv sbar_", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("hsv vbar_", "Trackbars", 10, 255, nothing)
    cv2.createTrackbar("hsl hbar_", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("hsl sbar_", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("hsl lbar_", "Trackbars", 0, 255, nothing)

    cv2.createTrackbar("k1", "Trackbars", 0, 50, nothing)
    cv2.createTrackbar("k2", "Trackbars", 0, 50, nothing)
    cv2.createTrackbar("itera", "Trackbars", 0, 10, nothing)
    cv2.createTrackbar("rank", "Trackbars", 0, 10, nothing)

    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)
            frame = image.GetArray()                    # frame 영상 취득.
            # 화면 크기 세팅
            frame = cv2.resize(frame, (640*2, 480*2), interpolation=cv2.INTER_LINEAR)

            frame2 = frame.copy()  # 영상원본

            frame = cv2.GaussianBlur(frame, (3, 3), 0)  # 원본에 가우시안 필터적용
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            blue, green, red = cv2.split(frame)  # 원본에서 BGR 분리
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # HSV(색상, 채도, 명도) 분리
            h, s, v = cv2.split(frame_hsv)  # 분리후 저장.

            frame_hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)  # BGR -> HLS로
            H, L, S = cv2.split(frame_hls)  # H,L,S 분리
            kernel = np.ones((3, 3), np.uint8)

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

            # final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)
            # final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)
            # final_mask = cv2.blur(final_mask, (4, 4))

            final_mask = cv2.erode(final_mask, kernel, iterations=4)
            final_mask = cv2.dilate(final_mask, kernel, iterations=4)

            result = cv2.bitwise_and(frame2, frame2, mask=final_mask)

            ############# 테스트 ##########################################
            dilate = cv2.dilate(final_mask, kernel, iterations=1)
            di_di = cv2.dilate(dilate, kernel, iterations=1)
            erosion = cv2.erode(final_mask, kernel, iterations=1)
            ero_ero = cv2.erode(erosion, kernel, iterations=1)
            # opening = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)
            # closing = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)
            ############# 테스트 ##############################################

            #################### 리벳 중심좌표값 자동 저장용 ##########################

            Rivet_center = []

            _, contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 컨투어 찾기
            if len(contours) != 0:
                for contour in contours:
                    if (cv2.contourArea(contour) > 30) and (cv2.contourArea(contour) < 500):  # **필요한 면적을 찾아 중심점 좌표를 저장
                        ball_area = cv2.contourArea(contour)
                        mom = contour
                        M = cv2.moments(mom)
                        cx_origin = int(M['m10'] / M['m00'])
                        cy_origin = int(M['m01'] / M['m00'])

                        cv2.circle(frame, (cx_origin, cy_origin), 5, (0, 255, 255), -1)  # 중심 좌표 표시
                        Rivet_center.append([cx_origin, cy_origin])

            #cv2.namedWindow('title', cv2.WINDOW_NORMAL)
            #cv2.imshow('title', frame)
            cv2.imshow('Frame', frame)  # 원본
            cv2.imshow('final_mask', final_mask)  # 필터링후

            k = cv2.waitKey(1)
            if k == 27:
                break
        grabResult.Release()

    # Releasing the resource
    camera.StopGrabbing()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    # 카메라 번호 선택. 0번부터.
    #execute(1)
    execute(0)