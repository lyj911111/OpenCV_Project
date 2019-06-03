'''
    참고 링크: http://blog.naver.com/PostView.nhn?blogId=samsjang&logNo=220664561517&parentCategoryNo=&categoryNo=66&viewDate=&isShowPopularPosts=false&from=postList

    카메라 왜곡을 보정하기 위해
    체스보드를 이용함.
    총 15장의 실시간 캡쳐를 통해 보정값 .npz 으로 저장. (그 카메라에서 재사용하기 위해)
'''

import numpy as np
import cv2

# 체스보드의 사이즈 지정. (반드시 일치해야 함.)
chessR = 9
chessC = 6

# 체스보드 교정할 횟수
Cal_Num = 15

def saveCamCalibration():
    global Cal_Num
    termination = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((chessR * chessC, 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessR, 0:chessC].T.reshape(-1, 2)

    objpoints = []
    imgpoints = []

    # 사용할 카메라 번호.
    cap = cv2.VideoCapture(0)

    count = 0
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray,(chessR, chessC), None)

        if ret:
            objpoints.append(objp)
            cv2.cornerSubPix(gray, corners, (11, 11), (-1, 1), termination)
            imgpoints.append(corners)

            cv2.drawChessboardCorners(frame, (chessR, chessC), corners, ret)
            count += 1
            print('[%d]' %count)

        cv2.imshow('img', frame)

        k = cv2.waitKey(0)
        if k == 27:
            break
        if count > Cal_Num:
            break

    cv2.destroyAllWindows()

    # 카메라 보정 계수값 저장.
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    np.savez('./calib.npz', ret=ret, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

    print("카메라 칼리브레이션 저장 완료")

saveCamCalibration()




