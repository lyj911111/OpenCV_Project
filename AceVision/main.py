import sys
from RivetDetect import RivetDetect
from QRDetect import QRDetect

#isExe = sys.argv[0]

# 테스트중...
# 이곳에 입력한 모듈 (.py)을 실행함.
test = 2

def main():

    # if isExe == 1:
    # elif isExe == 2:
    
    if test == 1:
        RivetDetect.execute()
    elif test == 2:
        QRDetect.execute()

    return

    
if __name__ == "__main__":
    main()
    