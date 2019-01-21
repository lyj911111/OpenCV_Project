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
        res = ser.readline()                #

        result = res.decode()[:len(res)-2]    # 자동으로 포함되어있는 개행을 제거하기 위해 [:len(res)-2] 를 추가함 : 즉, \r\n 을 제거함.

        print(result)

        if result == 'ready':
            print('OK')
        else:
            print('NG')