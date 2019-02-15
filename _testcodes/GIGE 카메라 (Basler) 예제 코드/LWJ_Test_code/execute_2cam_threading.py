import threading, cv2
from pypylon import pylon, genicam
from time import sleep

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
    print("Using device ", cam.GetDeviceInfo().GetModelName())  # 연결된 카메라 이름 출력

print("카메라 리스트", camera_list)

# GIGe Basler 카메라 실행. (num: 카메라 번호)
def execute1():
    global camera_list
    camera = camera_list[0]

    print(camera)
    print(camera.GetDeviceInfo().GetModelName())

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)


            img = image.GetArray()

            # 화면 크기 조절
            #resize = cv2.resize(img, (640*2, 480*2), interpolation=cv2.INTER_LINEAR)

            cv2.namedWindow('title', cv2.WINDOW_NORMAL)
            cv2.imshow('title', img)
            #cv2.imshow('damm', resize)

            k = cv2.waitKey(1)
            if k == 27:
                break
        grabResult.Release()

    # Releasing the resource
    camera.StopGrabbing()
    cv2.destroyAllWindows()

def execute2():
    global camera_list
    camera = camera_list[1]

    print(camera)
    print(camera.GetDeviceInfo().GetModelName())

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)

            img = image.GetArray()

            # 화면 크기 조절
            #resize = cv2.resize(img, (640*2, 480*2), interpolation=cv2.INTER_LINEAR)

            cv2.namedWindow('title1', cv2.WINDOW_NORMAL)
            cv2.imshow('title1', img)
            #cv2.imshow('damm', resize)

            k = cv2.waitKey(1)
            if k == 27:
                break
        grabResult.Release()

    # Releasing the resource
    camera.StopGrabbing()
    cv2.destroyAllWindows()

# 객체를 할당하고 인자를 대입함.
# target = 함수이름, args = 전달받는 인자
t1 = threading.Thread(target=execute1, args=())
t2 = threading.Thread(target=execute2, args=())
# t3 = threading.Thread(target=camera3, args=())

# 반드시 객체뒤에 .start()를 붙여야 스레드가 가동됨.
t1.start()
t2.start()
# t3.start()
