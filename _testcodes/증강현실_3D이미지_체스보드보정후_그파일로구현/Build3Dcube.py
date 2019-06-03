'''
    증강현실 테스트 (3D pose Estimate)
    참고링크 : http://blog.naver.com/PostView.nhn?blogId=samsjang&logNo=220664965832&categoryNo=66&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=postList&userTopListOpen=true&userTopListCount=10&userTopListManageOpen=false&userTopListCurrentPage=1


    체스판으로 보정한 파일 .npz 깂에서 이미지 왜곡을 해결 후,
    체스판의 보정된 위치 위에 Cube Box를 그리는 테스트.
'''

import numpy as np
import cv2

# 보정한 체스판 Row & col
chessR = 9
chessC = 6

def drawCube(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1, 2)
    cv2.drawContours(img, [imgpts[:4]], -1, (255, 0, 0), -3)

    for i, j in zip(range(4), range(4, 8)):
        cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (0, 255, 0), 2)

    cv2.drawContours(img, [imgpts[4:]], -1, (0, 255, 0), 2)

    return img

def poseEstimation():
    with np.load('calib.npz') as X:
        ret, mtx, dist, _, _ = [X[i] for i in ('ret', 'mtx', 'dist', 'rvecs', 'tvecs')]

    termination = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((chessR * chessC, 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessR, 0:chessC].T.reshape(-1, 2)
    axis = np.float32([[0, 0, 0], [0, 3, 0], [3, 3, 0], [3, 0, 0], [0, 0, -3], [0, 3, -3], [3, 3, -3], [3, 0, -3]])

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (chessR, chessC), None)

        if ret == True:
            cv2.cornerSubPix(gray, corners, (11, 11), (-1, 1), termination)
            _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners, mtx, dist)
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
            frame = drawCube(frame, corners, imgpts)


        cv2.imshow('frame', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

poseEstimation()