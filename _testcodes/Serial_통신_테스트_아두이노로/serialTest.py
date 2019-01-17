import serial

ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=1
)

while True:
    if ser.readable():
        res = ser.readline()
        print(res.decode()[:len(res)-1])    # 자동으로 포함되어있는 개행을 제거하기 위해 [:len(res)-1] 를 추가함.