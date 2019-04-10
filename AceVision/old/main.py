import sys
from RivetDetect import *
from QRDetect import *
import serial

# 시리얼 통신.
# NANOserial = serial.Serial(
#     port='COM3',\
#     baudrate=115200,\
#     parity=serial.PARITY_NONE,\
#     stopbits=serial.STOPBITS_ONE,\
#     bytesize=serial.EIGHTBITS,\
#     timeout=0)


#isExe = sys.argv[0]

# 테스트중...
# 이곳에 입력한 모듈 (.py)을 실행함.
test = 1

# 바코드 시리얼 넘버 저장변수 (이곳에 시리얼 번호를 전달)
serialnum = 987654123456

def main():
    global serialnum

    # if isExe == 1:
    # elif isExe == 2:

    if test == 1:
        RivetDetect.execute(serialnum)
    elif test == 2:
        QRDetect.execute()

    return

    
if __name__ == "__main__":
    main()
    