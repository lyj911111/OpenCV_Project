'''
    미쓰비시 PLC와 통신하기 위한 프로토콜.
'''

import serial

# 시리얼 포트 지정.
ser = serial.Serial(
    port='COM5',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    )

# 시리얼 값을 받을때까지 기다림.
def WaitReceiveData():

    while True:
        if ser.readable():
            # 응답을 받음.
            respond = ser.readline()
            respond = respond.decode()
            print("받은 신호", respond)
            return respond


class sendCommandToPLC:

    def __init__(self):
        pass

    '''
        PLC에게 Read신호 보냄.
    '''
    def sendReady(self):
        ready = chr(0x02)+chr(0x30)+chr(0x30)+chr(0x31)+chr(0x30)+chr(0x30)+chr(0x30)+chr(0x32)+chr(0x03)
        print("보낸 신호", ready)

        # 시리얼 전송
        if ser.readable():
            ready = ready.encode()
            ser.write(ready)

        # 응답을 받음.
        respond = ser.readline()
        respond = respond.decode()
        print("받은 신호", respond)
        return respond

    '''
        PLC에게 OK신호 보냄.
    '''
    def sendOK(self):
        OK = chr(0x02)+chr(0x37)+chr(0x30)+chr(0x32)+chr(0x30)+chr(0x38)+chr(0x03)+chr(0x30)+chr(0x34)
        print("보낸 신호", OK)

        # 시리얼 전송
        if ser.readable():
            OK = OK.encode()
            ser.write(OK)

        # 응답을 받음.
        respond = ser.readline()
        respond = respond.decode()
        print("받은 신호", respond)
        return respond

    '''
        PLC에게 NG신호 보냄.
    '''
    def sendNG(self):
        NG = chr(0x02) + chr(0x37) + chr(0x30) + chr(0x33) + chr(0x30) + chr(0x38) + chr(0x03) + chr(0x30) + chr(0x34)
        print("보낸 신호", NG)

        # 시리얼 전송
        if ser.readable():
            NG = NG.encode()
            ser.write(NG)

        # 응답을 받음.
        respond = ser.readline()
        respond = respond.decode()
        print("받은 신호", respond)
        return respond


if __name__=="__main__":
    a = sendCommandToPLC()  # 객체 할당.

    Ready = a.sendReady()   # Ready 신호 보냄
    OK = a.sendOK()      # OK 신호 보냄
    NG = a.sendNG()      # NG 신호 보냄
    print(Ready, OK, NG)    # 응답받은 리턴 값 출력 테스트.
