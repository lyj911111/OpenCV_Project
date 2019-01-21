import serial

ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
)


while True:
    if ser.readable():
        res = ser.readline()                 # 시리얼로 날라온 bytes 값이 저장됨.
        ready = res.decode()[:len(res)-2]    # bytes를 decode 해서 str로 변환, 자동으로 포함되어있는 개행을 제거하기 위해 [:len(res)-2] 를 추가함 : 즉, \r\n 을 제거함.

        print(ready)        # 아두이노(PLC)에서 날라온 프로토콜.

        judge = input()             # 유저가 입력 '1' 또는 '2' 테스트 하기 위해.

        OK = chr(0x31)              # '1' 일때 OK
        NG = chr(0x32)              # '2' 일때 NG

        # 프로토콜을 받고 판독 시작.
        if ready == 'ready':
            if judge == OK:

                OK = OK.encode()     # OK일때 char 를 bytes로 인코딩
                ser.write(OK)        # 아스키코드 0x31 전송

            elif judge == NG:

                NG = NG.encode()     # NG일때 아스키코드 0x32 전송
                ser.write(NG)
            else:
                pass
