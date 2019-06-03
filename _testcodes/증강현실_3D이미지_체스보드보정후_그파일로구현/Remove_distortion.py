import numpy as np
import cv2

chessR = 9
chessC = 6

def saveCamCalibration():
    termination = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((chessR * chessC, 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessR, 0:chessC].T.reshape(-1, 2)

    objpoints = []
    imgpoints = []

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
        if count > 15:
            break

    cv2.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    np.savez('./calib.npz', ret=ret, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

    print("카메라 칼리브레이션 저장 완료")

saveCamCalibration()




