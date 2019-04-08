'''
    조명 시리얼 통신제어
    통신방식: RS-232C
    baudrate: 9600 bps
    data bit: 8 bits
    stop bit: 1 bit
    No parity
'''

import serial

ser = serial.Serial(
    port='COM5',
    baudrate=9600,
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
)


'''
    개별 제어 조명.
    1 param: 1 ~ 4 까지 채널선택.
    2 param: 0~255 까지 조명밝기.
'''
def seperateControl(channel, bright=100):

    Value = 0
    STX = hex(0x02)        # start code 바이너리화

    # 조명 채널은 1~4까지만 있음, 예외처리.
    if 0 == channel or channel > 4:
        print("Error: Channel must be chosen between 1~4")
        return

    # 채널 선택 프로토콜
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


    ETX = hex(0x03)        # end code 바이너리화
    print("전체 프로토콜 모양:", STX, COMMAND, ETX)
    return STX, COMMAND, ETX



'''
    전체 조명 제어.
    param 1 : 0~255 조명 밝기
'''
def wholeControl(bright=100):

    Value = 0
    STX = hex(0x02)        # start code 바이너리화

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

    ETX = hex(0x03)        # end code 바이너리화
    print("전체 프로토콜 모양:", STX, COMMAND, ETX)
    return STX, COMMAND, ETX


def lightExecute(STX, COMMAND, ETX):
    while True:
        if ser.readable():
            # 신호 보내기.
            # 프로토콜을 받고 판독 시작.

            STX = STX.encode()  # 시작 프로토콜 인코딩 byte형식 0x02
            ser.write(STX)  # 데이터 전송

            COMMAND = COMMAND.encode()  # DATA값 전송. 아스키코드
            ser.write(COMMAND)  # 데이터 전송

            ETX = ETX.encode()  # 끝 프로토콜 인코딩 byte형식 0x03
            ser.write(ETX)  # 데이터 전송

            # 응답 신호 읽기
            res = ser.readline()  # 시리얼로 날라온 bytes 값이 저장됨.
            reply = res.decode()  # bytes를 decode 해서 str로 변환, 자동으로 포함되어있는 개행을 제거하기 위해 [:len(res)-2] 를 추가함 : 즉, \r\n 을 제거함.
            print(reply)  # 조명에서 날라온 응답 프로토콜 데이터 출력.


if __name__=="__main__":

    # 개별 조명 제어 함수로부터 start값, data값, end값을 return
    #STX, COMMAND, ETX = seperateControl(3, 255)

    # 전체 조명 제어 함수로부터 start값, data값, end값을 return
    STX1, COMMAND1, ETX1 = wholeControl(50)

    lightExecute(STX1, COMMAND1, ETX1)

