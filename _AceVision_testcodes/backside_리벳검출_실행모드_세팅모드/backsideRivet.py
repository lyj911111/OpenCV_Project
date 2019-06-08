import cv2
import numpy as np
import glob
import re


'''
    함수) list 내부의 값을 text 로 저장.
    
    param
        list : list 값 [(1,2), (3,4), ...]
        flag : True 일 경우, 리스트의 값을 저장함. False 경우, 저장하지 않음.
'''
def savetxt(list, flag=True):
    if flag == True:
        file = open('./savedata.txt','w')
        for i in range(len(list)):
            coord = str(list[i])
            # print(coord)
            file.write(coord + '\n')
        file.close()
    else: pass


'''
    함수) text 에 있는 값을 line 단위로 읽어서 list에 저장. 

    return
        number_list : list 값 [(1,2), (3,4), ...]
'''
def loadtxt():
    loadlist = []
    file = open('./savedata.txt', 'r')              # 읽기모드로 파일열기
    lines = file.readlines()                        # 라인별로 읽기

    for i in range(len(lines)):
        loadlist.append((lines[i].split('\n')[0]))  # 개행을 기준으로 분류하여 리스트로

    number_list = []
    for i in range(len(loadlist)):
        numbers = re.findall("\d+", loadlist[i])        # 문자열내 숫자만 뽑아냄.
        numbers = tuple([int (j) for j in numbers])     # 문자열을 int으로.
        number_list.append(numbers)                   # [ (좌표),(좌표)... ]
    #print(number_list)
    file.close()
    return number_list



'''
    함수) 이미지와 좌표값이 들어오면 픽셀과 주변 픽셀의 평균을 구함. **주의** (y, x)좌표로 들어옴. (gray img)
    
    param
        img : 픽셀을 읽고자 하는 이미지 Array
        y   : y좌표
        x   : x좌표
        
    return
        0   : 픽셀 평균값 60 이하 (어두움)
        1   : 픽셀 평균값 60 이상 (밝음)
'''
def avg_pixel(img, y, x):

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


'''
    함수) 이미지와 좌표값을 입력하면, 좌표값을 Display한 이미지 리턴. 픽셀 합불 여부값도 리턴.
          avg_pixel() 함수와 함께 사용.
          
    param
        img        : 이미지 array
        coordList  : 좌표값을 가지고 있는  List ex) [(1,2), (3,4), (5,6),...]
    return
        img        : Display 된 이미지 array
        ok_cnt     : 합격 픽셀 갯수
        ng_cnt     : 불합 픽셀 갯수
'''
def detect_display(img, coordList):
    ok_cnt = 0
    ng_cnt = 0
    gray_detect = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for i in range(len(coordList)):
        pix = avg_pixel(gray_detect, coordList[i][1], coordList[i][0])
        if pix == True:
            img = cv2.circle(img, (coordList[i][0], coordList[i][1]), coordList[i][2], (255, 0, 255), 2)  # x좌표, y좌표, 직경값
            img = cv2.circle(img, (coordList[i][0], coordList[i][1]), 1, (0, 0, 255), -1)
            cv2.putText(img, "OK", (coordList[i][0], coordList[i][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            ok_cnt = ok_cnt + 1
        else:
            img = cv2.circle(img, (coordList[i][0], coordList[i][1]), 1, (0, 0, 255), -1)
            cv2.putText(img, "NG", (coordList[i][0], coordList[i][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            ng_cnt = ng_cnt + 1
    return img, ok_cnt, ng_cnt


'''
    함수) Chess 보정 선행처리를 마친 이미지를 넣어 펼쳐진 이미지를 리턴.
    
    param
        img  :  왜곡된 이미지
    return
        dst  :  펼쳐진 이미지
'''
def calibration(img):
    global objpoints, imgpoints

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]

    # undistort
    mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
    dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)

    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]

    return dst




'''
    함수) 연속되는 Frame에서 1개의 이미지만 취득하여 리벳 유무 판독을 진행함.
    
    param    
        img      :  Raw(편집없는 원본) 이미지 array
        saveflag :  True or False 값 입력. [True = 판독한 값을 Text 저장 / False = 불러온 좌표값으로 판독]
    
    return
        img       :  판독을 완료한 이미지
        rivetlist :  리벳 좌표값을 List 리턴
'''
def judgeImage(img, saveflag):
    img = calibration(img)  # 보정된 이미지 리턴 (속도가 느려짐)
    img = cv2.resize(img, (1260, 960))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 리벳만 있는 구간만 뽑아내기 위해 마스크를 씌움.
    mask = np.zeros(img.shape[:2], np.uint8)
    mask = cv2.rectangle(mask, (310, 30), (325, 920), (255, 255, 255), -1)  # 첫번째 사각 마스크
    mask = cv2.rectangle(mask, (414, 30), (458, 920), (255, 255, 255), -1)  # 두번째 사각 마스크
    mask = cv2.rectangle(mask, (890, 30), (940, 920), (255, 255, 255), -1)  # 세번째 사각 마스크
    res = cv2.bitwise_and(gray, gray, mask=mask)  # 합성하여 뽑아냄.


    if saveflag == True:
        # 원 탐지 (중심 x좌표, 중심 y좌표, 직경)
        rivetlist = []
        circles = cv2.HoughCircles(res, cv2.HOUGH_GRADIENT, 1, 13, param1=110, param2=9, minRadius=4, maxRadius=7)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                rivetlist.append((i[0], i[1], i[2]))
        #print("판독한 리벳 리스트", rivetlist)
        img, ok_cnt, ng_cnt = detect_display(img, rivetlist)
        totalNo = len(rivetlist)
    else:
        rivetlist = loadtxt()  # text 저장된 list 좌표 불러옴.
        #print("저장된 리벳 리스트", rivetlist)
        img, ok_cnt, ng_cnt = detect_display(img, rivetlist)
        totalNo = len(rivetlist)


    # 총 리벳, OK, NG 갯수 디스플레이
    cv2.putText(img, "Total Rivet No. : %d" % totalNo, (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,
                cv2.LINE_AA)
    cv2.putText(img, "OK Rivet No. : %d" % ok_cnt, (500, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                cv2.LINE_AA)
    cv2.putText(img, "NG Rivet No. : %d" % ng_cnt, (500, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                cv2.LINE_AA)
    #print(ok_cnt)
    #print(ng_cnt)

    # cv2.imshow('mask', mask)
    # cv2.imshow('result', result)
    # cv2.imshow('c', res)
    # cv2.imshow('img', img)

    return img, rivetlist

'''
    함수) Main 함수 리벳 유무 판독 수행, flag 값에 따라 세팅하여 text으로 저장할지,
          text값을 불러와 판독할지 결정.
    
    param 
        flag

        세팅모드 = True
        실행모드 = False

        세팅모드
            'a' key: 현재 Frame 리벳 판독 시행.
            's' key: 판독된 리벳의 좌표를 text 저장.
            
        실행모드
            text 저장된 좌표 값을 기준으로 판독 수행.
'''
def main(flag):
    global objpoints, imgpoints

    # 체스판으로 이미지 보정.
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((9*13,3), np.float32)
    objp[:,:2] = np.mgrid[0:13,0:9].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob('C:/Users/DELL/Desktop/newmodel/chess/*.bmp')    # 체스 이미지들

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (13,9),None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners)


    #print("저장된 좌표", saved_list)

    while True:
        img = cv2.imread("./img/backside.bmp")      # 연속 이미지 취득 (비디오 프레임 가정)
        frame = img.copy()
        frame = cv2.resize(frame, (1260, 960))

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1)
        if k == 27:         # ESC 종료
            break
        elif k == -1:
            continue
        # 세팅 모드
        if flag == True:
            # print(k)
            if k == 97:                     # a 키를 눌렀을 때 키보드 이벤트 캡쳐, 판독.
                result, _ = judgeImage(img, flag)
                cv2.imshow('result', result)
                print("현재 판독 이미지를 출력합니다.")
            elif k == 115:                  # s 키를 누르면 현재 판독 좌표 저장.
                _, rivetlist = judgeImage(img, flag)
                savetxt(rivetlist, True)
                print("좌표를 저장하였습니다. 총 %d 개" % len(rivetlist))
        # 실행 모드
        else:
            if k == 97:                     # a 키를 눌렀을 때 Text에 저장된 좌표를 이용해 판독 실행.

                result, _ = judgeImage(img, flag)
                cv2.imshow('result', result)
                print("현재 판독 이미지를 출력합니다.")


'''
    세팅모드
        'a' key: 현재 Frame 리벳 판독 시행.
        's' key: 판독된 리벳의 좌표를 text 저장.
        
    실행모드
        text 저장된 좌표 값을 기준으로 판독 수행.
        
    Flag
        세팅모드 = True
        실행모드 = False
'''
if __name__ == "__main__":
    main(flag=True)