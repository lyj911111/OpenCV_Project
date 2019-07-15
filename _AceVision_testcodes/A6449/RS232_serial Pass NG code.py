import serial
import cv2


# 시리얼 연결 실패시 오류 메시지 클래스
class errorMessage(Exception):
    def __init__(self, msg='init_error_msg'):
        self.msg = msg
    def __str__(self):
        return self.msg


# 초기 시리얼 연결
try:
    print("Suceessfully connected with PLC")
    ser = serial.Serial(
        port='COM3',
        baudrate=9600,
        parity=serial.PARITY_NONE, \
        stopbits=serial.STOPBITS_ONE, \
        bytesize=serial.EIGHTBITS, \
        timeout=0.5                     # PLC가 1초에 한번 보내므로 그보다 적게.
    )
except:
    print("[ERROR] : please check PLC RS232")
    # raise errorMessage('[ERROR] : please check PLC RS232')


# PASS 때 '1' 보내고, RS232 통신 닫기
def passSignal():
    print("PASS the judgement")

    # PLC신호 읽음
    if ser.readable():
        res = ser.readline()
        PLC_ready = res.decode()
        PLC_ready = PLC_ready.lower()   # 소문자로 변환

        if PLC_ready[0:5] == 'ready':
            print("PLC로부터 받은 프로토콜:", PLC_ready[0:5])  # 받은 프로토콜
            passSig = '1'.encode()
            ser.write(passSig)  # 전송
            ser.close()         # 닫기


# NG 때 '2' 보내고, RS232 통신 닫기
def NGSignal():
    print("NG the judgement")

    # PLC신호 읽음
    if ser.readable():
        res = ser.readline()
        PLC_ready = res.decode()
        PLC_ready = PLC_ready.lower()   # 소문자로 변환

        if PLC_ready[0:5] == 'ready':
            print("PLC로부터 받은 프로토콜:", PLC_ready[0:5])  # 받은 프로토콜
            NGSig = '2'.encode()
            ser.write(NGSig)  # 전송
            ser.close()       # 닫기


'''
    PLC 에서 온 값 'READY'를 읽고,
    합격일때 : judgeSignal(1)
    불합일때 : judgeSignal(2)
    의 형태로 함수 사용.
'''
def judgeSignal(signal=0):
    print("checking PASS or NG signal...")

    # PLC신호 읽음
    if ser.readable():
        res = ser.readline()
        PLC_ready = res.decode()
        PLC_ready = PLC_ready.lower()  # 소문자로 변환

        if PLC_ready[0:5] == 'ready':
            print("PLC로부터 받은 프로토콜:", PLC_ready[0:5])  # 받은 프로토콜
            signal = str(signal)
            signal = signal.encode()
            ser.write(signal)  # 전송
            ser.close()  # 닫기

if __name__ == "__main__":
    while 1:
        judgeSignal()
        # passSignal()
        # NGSignal()
