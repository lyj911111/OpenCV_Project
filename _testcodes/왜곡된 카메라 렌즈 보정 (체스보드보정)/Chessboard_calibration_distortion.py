import cv2
import numpy as np
import glob
from tqdm import tqdm   # pip install tqdm  / 루프의 진행상황을 display해줌
import PIL.ExifTags
import PIL.Image
# ============================================
# Camera calibration 카메라 보정
# ============================================
# Define size of chessboard target. 체스보드 패턴 사이즈 지정
chessboard_size = (9, 6)

# Define arrays to save detected points
obj_points = [] # 3D points in real world space
img_points = [] # 3D points in image plane

# Prepare grid and points to display
objp = np.zeros((np.prod(chessboard_size), 3), dtype=np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

# read images
calibration_paths = glob.glob('./calibration_images/*') # 폴더내 모든 패턴이미지 로드

cnt = 0
detectChess_list = []
# Iterate over images to find intrinsic matrix. 고유 Matrix값(보정값)을 찾기 위해 반복적으로 수행.
for image_path in tqdm(calibration_paths):
    # Load image
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    # 보정이미지를 위해 gray 전환
    print("Image loaded, Analizying...", "이미지 경로:", image_path)

    # find chessboard corners. 체스보드 코너점을 찾으면 ret True를 리턴, 그리고 coners 의 좌표값 리턴
    ret, corners = cv2.findChessboardCorners(gray_image, chessboard_size, None)

    # findChessboardConers 알고리즘의 코너값을 탐지하면 ret가 True를 반환.
    if ret == True:
        print("Chessboard detected!")
        print(image_path)

        # define criteria for subpixel accuracy. / critaria 의 변수값 (타입, 반복 횟수, 정확도)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # refine corner location (to subpixel accuracy) based on criteria. / 보정된 지점에 포인트 재배치하는 함수
        detectChess_list = cv2.cornerSubPix(gray_image, corners, (5, 5), (-1, -1), criteria)
        obj_points.append(objp)
        img_points.append(corners)

        detectChess = cv2.drawChessboardCorners(image, (9, 6), detectChess_list, ret)
        cv2.imshow('detect Chess points', detectChess)
        cv2.waitKey(1)

        # Calibrate camera / 보정된 값 5개를 리턴.
        ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray_image.shape[::-1], None, None)

        # Save parameters into numpy file 보정된 값의 파일 행렬로 저장. (계속 실행하여 시간낭비를 방지)
        np.save("./camera_params/ret", ret)
        np.save("./camera_params/K", K)
        np.save("./camera_params/dist", dist)
        np.save("./camera_params/rvecs", rvecs)
        np.save("./camera_params/tvecs", tvecs)

    else:
        cnt += 1
        print("코너 탐지 실패 %d" %cnt )

# Get exif data in order to get focal length.
exif_img = PIL.Image.open(calibration_paths[0])
print(exif_img)
exif_data = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in exif_img._getexif().items()
    if k in PIL.ExifTags.TAGS}
# Get focal length in tuple form
focal_length_exif = exif_data['FocalLength']
# Get focal length in decimal form
focal_length = focal_length_exif[0] / focal_length_exif[1]
np.save("./camera_params/FocalLength", focal_length)