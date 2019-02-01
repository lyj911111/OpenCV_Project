# -- coding: utf-8 --

import sys
import time
import msvcrt
import numpy as np
import cv2

from ctypes import *

# Device 번호
camera_num = 0

sys.path.append("C:/Users/Lee Won Jae/PycharmProjects/HIKvsion/MvImport")
from MvCameraControl_class import *

# ch: 开一个40MB的图像数据缓存大小 | en: Open a 40MB Image Buffer Size

if __name__ == "__main__":

    deviceList = MV_CC_DEVICE_INFO_LIST()
    tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE

    # ch:枚举设备 | en:Enum device
    ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
    if ret != 0:
        print("enum devices fail! ret[0x%x]" % ret)
        sys.exit()

    # 카메라가 없을 때 예외처리
    if deviceList.nDeviceNum == 0:
        print("find no device!")
        sys.exit()

    # 몇개의 장치를 찾았는지 출력 => 장치의 갯수가 이 객체 저장(deviceList.nDeviceNum)
    print("Find %d devices!" % deviceList.nDeviceNum)

    for i in range(0, deviceList.nDeviceNum):
        mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents

        # GIGE 카메라 일때.
        if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
            print("\ngige device: [%d]" % i)                                    # 장치의 번호 출력. (0번~ n번)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                strModeName = strModeName + chr(per)
            print("device model name: %s" % strModeName)                        # 장치의 모델명 출력.

            nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
            nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
            nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
            nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
            print("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))       # 장치의 현재 ip주소 출력

        # USB 카메라 일 때
        elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
            print("\nu3v device: [%d]" % i)                                     # 선택된 장치 번호
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                if per == 0:
                    break
                strModeName = strModeName + chr(per)
            print("device model name: %s" % strModeName)                        # 장치의 모델명 출력

            strSerialNumber = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                if per == 0:
                    break
                strSerialNumber = strSerialNumber + chr(per)
            print("user serial number: %s" % strSerialNumber)                   # 유저 시리얼 번호 출력

    #nConnectionNum = input("please input the index number of the device to connect:")
    nConnectionNum = camera_num         # 사용할 장치 번호 선택.

    # 장치번호 입력오류 예외 처리.
    if int(nConnectionNum) >= deviceList.nDeviceNum:
        print("intput error!")
        sys.exit()

    while True:

        # ch:创建相机实例 | en:Creat Camera Object 카메라 객체 생성.
        cam = MvCamera()

        # ch:选择设备并创建句柄 | en:Select device and create handle
        stDeviceList = cast(deviceList.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents

        ret = cam.MV_CC_CreateHandle(stDeviceList)
        if ret != 0:
            print("create handle fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:打开设备 | en:Open device
        ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != 0:
            print("open device fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
        if stDeviceList.nTLayerType == MV_GIGE_DEVICE:
            nPacketSize = cam.MV_CC_GetOptimalPacketSize()
            if int(nPacketSize) > 0:
                ret = cam.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
                if ret != 0:
                    print("Warning: Set Packet Size fail! ret[0x%x]" % ret)
            else:
                print("Warning: Get Packet Size fail! ret[0x%x]" % nPacketSize)

        # ch:设置触发模式为off | en:Set trigger mode as off
        ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
        if ret != 0:
            print("set trigger mode fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:设置图像像素格式为mono8 | en：Set pixel format as mono8
        ret = cam.MV_CC_SetEnumValue("PixelFormat", 0x01080001)
        if ret != 0:
            print("Set pixel format fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:开始取流 | en:Start grab image
        ret = cam.MV_CC_StartGrabbing()
        if ret != 0:
            print("start grabbing fail! ret[0x%x]" % ret)
            sys.exit()

        global MAX_BUF_SIZE
        MAX_BUF_SIZE = 1024 * 1024 * 40
        mv_frame_info = MV_FRAME_OUT_INFO_EX()
        memset(byref(mv_frame_info), 0, sizeof(mv_frame_info))      # 메모리 0으로 초기화
        data_buf = (c_ubyte * MAX_BUF_SIZE)()

        # ch: 获取一帧图像 | en: Get one frame / 한개의 Frame을 취득 실패시 Timeout 예외처리 (1000ms)
        ret = cam.MV_CC_GetOneFrameTimeout(data_buf, MAX_BUF_SIZE, mv_frame_info, 1000)
        if ret != 0:
            print("Get one frame fail! ret[0x%x]" % ret)
            sys.exit()

        # ch: 保存RGB裸数据至opencv | en: Save RGB raw data to numpy array for opencv
        data_buf_ch = data_buf[0:mv_frame_info.nFrameLen:1]

        data_buf_copy = np.array(data_buf_ch)

        # print(mv_frame_info.nFrameLen)
        # data_r = data_buf_copy[0:mv_frame_info.nFrameLen:3]
        # data_g = data_buf_copy[1:mv_frame_info.nFrameLen:3]
        # data_b = data_buf_copy[2:mv_frame_info.nFrameLen:3]
        data_mono_arr = data_buf_copy.reshape(mv_frame_info.nHeight, mv_frame_info.nWidth)      # 사용자 컴퓨터의 프레임정보를 배열로 reshape.
        # data_r_arr = data_r.reshape(mv_frame_info.nHeight, mv_frame_info.nWidth)
        # data_g_arr = data_g.reshape(mv_frame_info.nHeight, mv_frame_info.nWidth)
        # data_b_arr = data_b.reshape(mv_frame_info.nHeight, mv_frame_info.nWidth)

        numArray = np.zeros([mv_frame_info.nHeight, mv_frame_info.nWidth, 3], "uint8")

        numArray[:, :, 2] = data_mono_arr
        numArray[:, :, 1] = data_mono_arr
        numArray[:, :, 0] = data_mono_arr

        cv2.imshow("Hello World", numArray)
        cv2.waitKey(1)

        # ch:停止取流 | en:Stop grab image
        ret = cam.MV_CC_StopGrabbing()
        if ret != 0:
            print("stop grabbing fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:关闭设备 | Close device
        ret = cam.MV_CC_CloseDevice()
        if ret != 0:
            print("close deivce fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:销毁句柄 | Destroy handle
        ret = cam.MV_CC_DestroyHandle()
        if ret != 0:
            print("destroy handle fail! ret[0x%x]" % ret)
            sys.exit()

        del data_buf
