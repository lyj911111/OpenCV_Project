'''
    Hole이 있는지 없는지 픽셀값으로 판독 하는 비전프로그램.

    1. Suction Hole 고정영역 12군대는 고정 좌표 지정. <변수명: ROI_list>
    2. 그 외 튜닝볼트가 있는 부분, 사용자 마우스로 좌표지정.
        2.1. 왼쪽마우스 더블클릭 -> 좌표지정, 오른쪽마우스 더블클릭 -> 좌표제거
        2.2. savetxt(TuneBoltList, False) 함수의 flag 설정. (True : 지금 지정한 좌표 정상종료시 txt저장, False: 저장안함)
    3. txt로부터 저장 좌표 불러오기.
        3.1. numlist = loadtxt() 함수를 활성화 시킴.

'''

import cv2
import re
import numpy as np

# 검출할 픽셀값 좌표를 찾기위해 보조선 가로,세로 크기 지정. <사각형 면적 크기>
ROI_w = 30
ROI_h = 30

# Suction hole 고정위치 좌표 지정. (12개)
ROI_list = [

    [(349, 182)],  # cover
    [(583, 185)],
    [(23, 248)],
    [(896, 259)],
    [(446, 323)],
    [(485, 323)],
    [(444, 569)],
    [(483, 570)],
    [(133, 655)],
    [(133, 701)],
    [(788, 656)],
    [(788, 700)],

    # # sample
    # [(380, 60)],
    # [(580, 52)],
    # [(726, 55)],
    # [(917, 74)],
    # [(307, 431)],
    # [(454, 459)],    # 453 460
    # [(687, 440)],
    # [(981, 447)],
    # [(571, 663)]
]

# 마우스 클릭 박스 크기
mouse_w = 20
mouse_h = 20

# 제거 영역 박스 크기
rmbox_w = 10
rmbox_h = 10

# 마우스 클릭에 의한 위치좌표 리스트에 추가
TuneBoltList = []
rmlist = []
def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:                # 왼쪽 누르고 땔때
        TuneBoltList.append([(int(x), int(y))])     # 설정할 볼트 좌표 지정
        print("볼트좌표", TuneBoltList)
    elif event == cv2.EVENT_RBUTTONDOWN:            # 오른쪽 클릭
        rmlist.append([(int(x), int(y))])           # 제거할 좌표 지정
        findNearValue(TuneBoltList, rmlist)         # 클릭 위치 근처값으로 찾아가 제거
        # findNearValue(numlist, rmlist)             # 불러온 데이터 좌표를 제거
        rmlist.clear()


# 이미지와 좌표값이 들어오면 픽셀과 주변 픽셀의 평균을 구함. (y, x)좌표로 들어옴.
def avg_fixel(img, y, x):

    pixel = img[y][x]
    pixelup = img[y][x - 2]
    pixeldown = img[y][x + 2]
    pixelleft = img[y - 2][x]
    pixelright = img[y + 2][x]
    pixelavg = (int(pixel) + int(pixelup) + int(pixeldown) + int(pixelleft) + int(pixelright))/5

    # 픽셀값이 어두우면 불합
    if pixelavg > 60:
        return 1
    else:
        return 0


# 리스트에 있는 값을 Text로 남기기. flag : 저장 on / off 기능
def savetxt(list, flag=True):
    if flag == True:
        file = open('./savedata.txt','w')
        for i in range(len(list)):
            file.write('%s\n' % list[i])
        file.close()
    else: pass


# text로 저장된 좌표를 읽어서 리스트를 리턴.
def loadtxt():
    loadlist = []
    file = open('./savedata.txt', 'r')              # 읽기모드로 파일열기
    lines = file.readlines()                        # 라인별로 읽기

    for i in range(len(lines)):
        loadlist.append((lines[i].split('\n')[0]))  # 개행을 기준으로 분류하여 리스트로

    coord_list = []
    for i in range(len(loadlist)):
        numbers = re.findall("\d+", loadlist[i])        # 문자열내 숫자만 뽑아냄.
        numbers = tuple([int (j) for j in numbers])     # 문자열을 int으로.
        coord_list.append([numbers])                   # 출력형태로 변환 => [ [(좌표)],[(좌표)]... ]
    #print(number_list)
    file.close()
    return coord_list


# 좌표값과 이미지Array를 input, Display하여 output
def detect_display(coordList, img):
    for i in range(len(coordList)):
        img = cv2.circle(img, (coordList[i][0][0], coordList[i][0][1]), 3, (255, 0, 255), -1)
        #img = cv2.rectangle(img, (coordList[i][0][0] - int(mouse_w/2), coordList[i][0][1] - int(mouse_h/2)), (coordList[i][0][0] + int(mouse_w/2), coordList[i][0][1] + int(mouse_h/2)), (255, 0, 255), 2)
        img = cv2.line(img, (coordList[i][0][0] - int(mouse_w/2), coordList[i][0][1] - int(mouse_h/2)), (coordList[i][0][0] + int(mouse_w/2), coordList[i][0][1] + int(mouse_h/2)) , (255, 0, 255), 1)
        img = cv2.line(img, (coordList[i][0][0] - int(mouse_w / 2), coordList[i][0][1] + int(mouse_h / 2)), (coordList[i][0][0] + int(mouse_w / 2), coordList[i][0][1] - int(mouse_h / 2)), (255, 0, 255), 1)
        pix = avg_fixel(gray, coordList[i][0][1], coordList[i][0][0])
        if pix == True:
            cv2.putText(img, "OK", (coordList[i][0][0], coordList[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(img, "NG", (coordList[i][0][0], coordList[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    return img

def remove_display(coordList, img):
    for i in range(len(coordList)):
        img = cv2.circle(img, (coordList[i][0][0], coordList[i][0][1]), 3, (0, 255, 0), -1)
        img = cv2.rectangle(img, (coordList[i][0][0] - int(rmbox_w/2), coordList[i][0][1] - int(rmbox_h/2)), (coordList[i][0][0] + int(rmbox_w/2), coordList[i][0][1] + int(rmbox_h/2)), (255, 255, 0), 1)
        img = cv2.line(img, (coordList[i][0][0] - int(rmbox_w/2), coordList[i][0][1] - int(rmbox_h/2)), (coordList[i][0][0] + int(rmbox_w/2), coordList[i][0][1] + int(rmbox_h/2)) , (255, 255, 0), 1)
        img = cv2.line(img, (coordList[i][0][0] - int(rmbox_w / 2), coordList[i][0][1] + int(rmbox_h / 2)), (coordList[i][0][0] + int(rmbox_w / 2), coordList[i][0][1] - int(rmbox_h / 2)), (255, 255, 0), 1)

        cv2.putText(img, "Removed", (coordList[i][0][0], coordList[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
    return img


'''
    param 1 : 원본 list
    param 2 : 제거하고자 하는 list (주변 근사값 +,-10)
    결과 : <원본 list> 내의 <제거 list>와 일치하는 것을 제거
'''
rm_temp = []
def findNearValue(originalList, removeList):
    global rmbox_w, rmbox_h
    for i in range(len(originalList)):
        for j in range(len(removeList)):
            if (originalList[i][0][0] > removeList[j][0][0] - 10 and originalList[i][0][0] < removeList[j][0][0] + 10) and (originalList[i][0][1] > removeList[j][0][1] - 10 and originalList[i][0][1] < removeList[j][0][1] + 10):
                rm_temp.append([(originalList[i][0][0], originalList[i][0][1])])
    try:
        originalList.remove(rm_temp[0])
        rm_temp.clear()
    except:
        pass
    print("제거후 좌표", originalList)

############# 저장된 데이터 불러올때 ############
# text에 저장된 위치좌표 불러오기
numlist = loadtxt()
#############################################

while True:

    frame = cv2.imread('./image/cover.jpg')
    result = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 고정위치 홀 스티커 검사
    for i in range(len(ROI_list)):
        #result = cv2.rectangle(result, ROI_list[i][0], (ROI_list[i][0][0] + ROI_w, ROI_list[i][0][1] + ROI_h), (255, 0, 255), 2)
        result = cv2.line(result, ROI_list[i][0], (ROI_list[i][0][0] + ROI_w, ROI_list[i][0][1] + ROI_h), (255, 0, 255), 1)
        result = cv2.line(result, (ROI_list[i][0][0], ROI_list[i][0][1] + ROI_h), (ROI_list[i][0][0] + ROI_w, ROI_list[i][0][1]), (255, 0, 255), 1)
        result = cv2.circle(result, (ROI_list[i][0][0] + int(ROI_w/2), ROI_list[i][0][1] + int(ROI_h/2)), 3, (255, 0, 255), -1)
        # cv2.putText(result, 'CP%d' % (i + 1), (ROI_list[i][0][0], ROI_list[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1,
        #             (255, 0, 255), 2, cv2.LINE_AA)
        pix = avg_fixel(gray, ROI_list[i][0][1] + int(ROI_h/2), ROI_list[i][0][0] + int(ROI_w/2))
        if pix == True:
            cv2.putText(result, "OK", (ROI_list[i][0][0], ROI_list[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(result, "NG", (ROI_list[i][0][0], ROI_list[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # 불러온 데이터 화면에 쓰기
    try:
        result = detect_display(numlist, result)
    except:
        pass

    # 가변위치 홀 스티커 검사 (마우스클릭지정)
    cv2.setMouseCallback('result', onMouse, param=result)
    result = detect_display(TuneBoltList, result)           # 선택한 좌표 Display

    # 잘못된 위치 제거용
    cv2.setMouseCallback('result', onMouse, param=result)
    #result = remove_display(rmlist, result)                # 삭제된 부분 Display

    #cv2.imshow('gray', gray)
    cv2.imshow('result', result)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        savetxt(TuneBoltList, False)
        break

cv2.destroyAllWindows()
