'''
A simple Program for grabing video from basler camera and converting it to opencv img.
Tested on Basler acA1300-200uc (USB3, linux 64bit , python 3.5)

'''
from pypylon import pylon, genicam
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
    print("Using device ", cam.GetDeviceInfo().GetModelName())  # 연결된 카메라 이름 출력

##############################################################################
# conecting to the first available camera
#camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

def execute(num):

    camera = camera_list[num]

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
            resize = cv2.resize(img, (640*2, 480*2), interpolation=cv2.INTER_LINEAR)

            cv2.namedWindow('title', cv2.WINDOW_NORMAL)
            cv2.imshow('title', img)
            cv2.imshow('damm', resize)

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