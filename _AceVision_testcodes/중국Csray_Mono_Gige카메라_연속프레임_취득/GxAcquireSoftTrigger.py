'''
    개발 환경:
        python 3.6.4
        pip 19.1.1

    기본 모듈:
        pip install opencv-python==3.4.5
        pip install Pillow==5.4.1
        pip install numpy==1.16.0
        pip install image==1.5.27

    중국 카메라 소프트웨어 설치 및 세팅:
        1. 중국 카메라 소프트웨어 설치 CSR_Setup_cn.zip 압축 해제, 설치
        2. GigE IP 세팅. ex) 카메라 IP: 169.254.138.115 // My PC IP 설정: 169.254.138.114 (주의, Submask: 255.255.255.0)

    파이썬 모듈(gxipy) 설치 및 세팅:
        1. Window -> cmd 실행
        2. 경로 변경 -> cd "CSR_V1.0.2_Python\api\" (api가 있는 곳 까지)
        3. 빌드      -> python setup.py build
        4. 패키지설치 -> python setup.py install

'''
# gxipy version : 1.0.1808.9101
import gxipy as gx
from PIL import Image
import cv2


# 컬러 카메라 취득
def acq_color(device, num):
    """
           :brief      acquisition function of color device
           :param      device:     device object[Device]
           :param      num:        number of acquisition images[int]
    """
    for i in range(num):
        # send software trigger command
        device.TriggerSoftware.send_command()

        # get raw image
        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            continue

        # get RGB image from raw image
        rgb_image = raw_image.convert("RGB")
        if rgb_image is None:
            continue

        # create numpy array with data from raw image
        numpy_image = rgb_image.get_numpy_array()
        if numpy_image is None:
            continue

        # show acquired image
        img = Image.fromarray(numpy_image, 'RGB')
        img.show()

        # print height, width, and frame ID of the acquisition image
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width()))


# 모노 카메라 취득
def acq_mono(device, num):
    """
           :brief      acquisition function of mono device
           :param      device:     device object[Device]
           :param      num:        number of acquisition images[int]
    """
    for i in range(num):
        # send software trigger command
        device.TriggerSoftware.send_command()

        # get raw image
        raw_image = device.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            continue

        # create numpy array with data from raw image / 영상 Array값 리턴
        numpy_image = raw_image.get_numpy_array()
        if numpy_image is None:
            continue

        # show acquired image / 비트맵으로 캡쳐
        #img = Image.fromarray(numpy_image, 'L')
        #img.show()

        # print height, width, and frame ID of the acquisition image
        print("Frame ID: %d   Height: %d   Width: %d"
              % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width()))
        return numpy_image


def main():
    # print the demo information
    print("")
    print("-------------------------------------------------------------")
    print("Sample to show how to acquire mono or color image continuously according to camera type "
          "and show acquired image.")
    print("-------------------------------------------------------------")
    print("")
    print("Initializing......")
    print("")

    # create a device manager
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num is 0:
        print("Error: Number of enumerated devices is 0")
        return

    # open the first device
    cam = device_manager.open_device_by_index(1)

    # set exposure / 노출값(exposure Time) 조절
    cam.ExposureTime.set(10000)

    # set gain / 선명도 조절
    cam.Gain.set(5.0)

    # send software trigger command
    cam.TriggerMode.set(gx.GxSwitchEntry.ON)
    cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)

    # start data acquisition
    cam.stream_on()

    while True:
        # camera is color / 컬러일 때
        if cam.PixelColorFilter.is_implemented() is True:
            acq_color(cam, 1)
        # camera is mono / 모노일 때
        else:
            frame = acq_mono(cam, 10)
            cv2.imshow('array', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):                   #  'q'를 누르면 종료.
            # stop acquisition
            cam.stream_off()
            # close device
            cam.close_device()
            break

if __name__ == "__main__":
    main()
