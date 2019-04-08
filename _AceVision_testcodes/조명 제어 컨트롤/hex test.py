'''
    조명 개별 제어.
    param 1 : 선택 조명 채널
    param 2 : 0~255 조명 밝기
'''

def seperateControl(channel, bright=100):

    Value = 0
    STX = hex(0x02).encode()        # start code 바이너리화

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

    ETX = hex(0x03).encode()        # end code 바이너리화
    print("전체 프로토콜 모양:", STX, COMMAND + Value, ETX)


'''
    전체 조명 제어.
    param 1 : 0~255 조명 밝기
'''
def wholeControl(bright=100):

    Value = 0
    STX = hex(0x02).encode()        # start code 바이너리화

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

    ETX = hex(0x03).encode()        # end code 바이너리화
    print("전체 프로토콜 모양:", STX, COMMAND + Value * 4 , ETX)




seperateControl(2, 245)
wholeControl(50)
