'''
    조명 시리얼 통신제어
    통신방식: RS-232C
    baudrate: 9600 bps
    data bit: 8 bits
    stop bit: 1 bit
    No parity
'''

import serial
import time

ser = serial.Serial(
    port='COM5',
    baudrate=9600,
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
)


class lightControl:

    def __init__(self):
        pass

    '''
        조명 개별 제어.
        param 1 : 선택 조명 채널
        param 2 : 0~255 조명 밝기
    '''
    def seperateControl(self, channel, bright=100):

        Value = 0
        STX = chr(0x02)        # start code 바이너리화

        # 조명 채널은 1~4까지만 있음, 예외처리.
        if 0 == channel or channel > 4:
            print("Error: Channel must be chosen between 1~4")
            return

        # 채널 선택 프로토콜 CH1S CH2S CH3S CH4S (3번째 인자는 숫자)
        COMMAND = chr(0x43) + chr(0x48) + chr(channel+0x30) + chr(0x53)

        # 0~255 까지 밝기 조절.
        if bright <= 255 and bright >= 0:       # 0~255 사이값만 입력

            bright = str(bright)

            if len(bright) == 3:
                Value = bright
            elif len(bright) == 2:
                Value = chr(0x30) + bright
            elif len(bright) == 1:
                Value = chr(0x30)*2 + bright

        else:
            print("Error: Please input the bright value under 255 value")
            return

        COMMAND = COMMAND + Value

        ETX = chr(0x03)        # end code 바이너리화
        print("전체 프로토콜 모양:", STX+COMMAND+ETX)
        DATA = STX+COMMAND+ETX

        if ser.readable():
            DATA = DATA.encode()
            ser.write(DATA)  # 시리얼 데이터 전송

    '''
        전체 조명 제어.
        param 1 : 0~255 조명 밝기
    '''
    def wholeControl(self, bright=100):

        Value = 0
        STX = chr(0x02)        # start code 바이너리화

        # 커맨드 프로토콜 'CHAS'
        COMMAND = chr(0x43) + chr(0x48) + chr(0x41) + chr(0x53)

        # 0~255 까지 밝기 조절.
        if bright <= 255 and bright >= 0:       # 0~255 사이값만 입력

            bright = str(bright)

            if len(bright) == 3:
                Value = bright
            elif len(bright) == 2:
                Value = chr(0x30) + bright
            elif len(bright) == 1:
                Value = chr(0x30)*2 + bright

        else:
            print("Error: Please input the bright value under 255 value")
            return
        COMMAND = COMMAND + Value * 4

        ETX = chr(0x03)        # end code 바이너리화
        print("전체 프로토콜 모양:", STX+COMMAND+ETX)
        DATA = STX+COMMAND+ETX

        if ser.readable():
            DATA = DATA.encode()
            ser.write(DATA)  # 시리얼 데이터 전송

    '''
        최대 출력으로 모든 light on
    '''
    def light_on(self):
        DATA = chr(0x02) + chr(0x43) + chr(0x48) + chr(0x41) + chr(0x53) + chr(0x32) + chr(0x35) + chr(0x35) + chr(
            0x32) + chr(0x35) + chr(0x35) + chr(0x32) + chr(0x35) + chr(0x35) + chr(0x32) + chr(0x35) + chr(0x35) + chr(
            0x03)
        if ser.readable():
            DATA = DATA.encode()
            ser.write(DATA)  # 시리얼 데이터 전송

    '''
        모든 light off
    '''
    def light_off(self):
        DATA = chr(0x02) + chr(0x43) + chr(0x48) + chr(0x41) + chr(0x53) + chr(0x30) + chr(0x30) + chr(0x30) + chr(
            0x30) + chr(0x30) + chr(0x30) + chr(0x30) + chr(0x30) + chr(0x30) + chr(0x30) + chr(0x30) + chr(0x30) + chr(
            0x03)

        if ser.readable():
            DATA = DATA.encode()
            ser.write(DATA)  # 시리얼 데이터 전송

    # def lightExecute(self, DATA):
    #
    #     while True:
    #         if ser.readable():
    #
    #             STX = DATA.encode()  # 시작 프로토콜 인코딩 byte형식 0x02
    #             ser.write(STX)  # 데이터 전송
    #
    #             # 응답 신호 읽기
    #             res = ser.readline()  # 시리얼로 날라온 bytes 값이 저장됨.
    #             reply = res.decode()  # bytes를 decode 해서 str로 변환, 자동으로 포함되어있는 개행을 제거하기 위해 [:len(res)-2] 를 추가함 : 즉, \r\n 을 제거함.
    #             print(reply)  # 조명에서 날라온 응답 프로토콜 데이터 출력.


if __name__=="__main__":

    light = lightControl()  # 클래스의 객체 할당.

    light.light_on()    # 조명 모두 최대 출력
    time.sleep(3)
    light.light_off()  # 조명 모두 끄기
    time.sleep(3)
    light.seperateControl(2, 100)    # 2번 채널의 조명 밝기 100으로.
    time.sleep(3)
    light.wholeControl(50)  # 전체 밝기 50으로 켜기
    time.sleep(3)
    light.light_off()       # 조명끄기



