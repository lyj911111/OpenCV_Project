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
        PLC의 상태를 확인(Check)하기 위해 신호를 보냄.
    '''
    def ReadStatus(self):
        status = chr(0x02) + chr(0x30) + chr(0x30) + chr(0x31) + chr(0x30) + chr(0x30) + chr(0x30) + chr(0x32) + chr(
            0x03) + chr(0x35) + chr(0x36)
        print("Status 보낸 신호", status)

        # 시리얼 전송
        if ser.readable():
            status = status.encode()
            ser.write(status)

        '''
            받을 응답(이렇게 들어와야 함.)
            1st Photo sensor detected : (hex) 02 30 30 32 30 03 43 35
            Ready to Run              : (hex) 02 30 30 43 31 03 30 37
        '''
        # 응답을 받음.
        respond = ser.readline()
        respond = respond.decode()
        print("받은 신호", respond)
        return respond

    '''
        비전 판독 후, PLC에게 OK신호 보냄.
    '''
    def sendOK(self):
        OK = chr(0x02)+chr(0x37)+chr(0x30)+chr(0x32)+chr(0x30)+chr(0x38)+chr(0x03)+chr(0x30)+chr(0x34)
        print("OK 보낸 신호", OK)

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
        비전 판독 후, PLC에게 NG신호 보냄.
    '''
    def sendNG(self):
        NG = chr(0x02)+chr(0x37)+chr(0x30)+chr(0x33)+chr(0x30)+chr(0x38)+chr(0x03)+chr(0x30)+chr(0x35)
        print("NG 보낸 신호", NG)

        # 시리얼 전송
        if ser.readable():
            NG = NG.encode()
            ser.write(NG)

        # 응답을 받음.
        respond = ser.readline()
        respond = respond.decode()
        print("받은 신호", respond)
        return respond

    '''
        바코드를 읽었다는 신호를 PLC에게 보냄 (Option)
    '''
    def IReadBarcode(self):
        Readbarcode = chr(0x02)+chr(0x37)+chr(0x30)+chr(0x34)+chr(0x30)+chr(0x38)+chr(0x03)+chr(0x30)+chr(0x36)
        print("Read Barcode 보낸 신호", Readbarcode)

        # 시리얼 전송
        if ser.readable():
            Readbarcode = Readbarcode.encode()
            ser.write(Readbarcode)

        # 응답을 받음.
        respond = ser.readline()
        respond = respond.decode()
        print("받은 신호", respond)
        return respond


if __name__=="__main__":

    # 테스트 필요.

    a = sendCommandToPLC()  # 객체 할당.

    status = a.ReadStatus()   # Ready 신호 보냄
    OK = a.sendOK()      # OK 신호 보냄
    NG = a.sendNG()      # NG 신호 보냄
    print(status, OK, NG)    # 응답받은 리턴 값 출력 테스트.
