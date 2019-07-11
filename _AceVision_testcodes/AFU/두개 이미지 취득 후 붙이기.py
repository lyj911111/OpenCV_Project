import cv2
import numpy as np

# 프레임 사이즈 조절 W, H
size = (1280, 960)

'''
    0~1280 내값을 넣으면 화면비율을 축소시키는
'''
def downscale(img, x):
    if x > 1280:
        print("Down Scale not available because you exceed maximum size")
        return

    y = int(0.75 * x)
    print(x)
    print(y)
    img = cv2.resize(img, (x, y))
    cv2.imshow('b', img)
    return img


'''
    이미지 채도 향상.
    원본, 0~255 값
'''


def increase_brightness(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return img


'''
    이미지를 자르는 함수
    :param
        img  : 이미지
        x, y : 자를곳 시작 좌표
        w, h : 자를 폭과 길이
'''


def im_trim(img, x, y, w, h):
    imgtrim = img[y: y + h, x: x + w]
    return imgtrim


'''
    이미지를 돌리는 함수
    :param
        img    : 이미지
        degree : 회전각
'''


def im_rotate(img, degree):
    h, w = img.shape[:-1]

    crossLine = int(((w * h + h * w) ** 0.5))
    centerRotatePT = int(w / 2), int(h / 2)
    new_h, new_w = h, w

    rotatefigure = cv2.getRotationMatrix2D(centerRotatePT, degree, 1)
    result = cv2.warpAffine(img, rotatefigure, (new_w, new_h))
    # cv2.imshow('a',result)
    return result


'''
    이미지를 이동시키는 함수
    :param
        x : 값만큼 x방향 이동
        y : 값만큼 y방향 이동
'''


def im_move(img, x, y):
    h, w = img.shape[:-1]
    M = np.float32([[1, 0, x], [0, 1, y]])
    result = cv2.warpAffine(img, M, (w, h))
    cv2.imshow('a', result)
    return result


def execute():
    global size

    # 2대의 카메라 해상도 설정 및 출력.
    cap0 = cv2.VideoCapture(0)
    cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 4024)  # Width 4024
    cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 3036)  # Height 3036

    cap1 = cv2.VideoCapture(1)
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 4024)  # Width 4024
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 3036)  # Height 3036

    while True:

        # 첫번째, 두번째 카메라 프레임 읽기, 사이즈 조정
        _, leftimg = cap0.read()
        leftimg_cp = leftimg.copy()
        leftimg = cv2.resize(leftimg, size, interpolation=cv2.INTER_LINEAR)  # 화면에 맞는 해상도로 조절.

        _, rightimg = cap1.read()
        rightimg_cp = rightimg.copy()
        rightimg = cv2.resize(rightimg, size, interpolation=cv2.INTER_LINEAR)  # 화면에 맞는 해상도로 조절.

        leftimg = downscale(leftimg, 1100)
        rightimg = downscale(rightimg, 1100)

        # 이미지 회전시키기
        leftimg = im_rotate(leftimg, 0.0)
        rightimg = im_rotate(rightimg, -0.8)

        # 이미지 이동시키기
        leftimg = im_move(leftimg, 0, 0)
        rightimg = im_move(rightimg, 0, 7)

        # 이미지 자르기
        gap = 119  # 138 좌우의 갭
        leftimg = im_trim(leftimg, 0, 0, leftimg.shape[1] - gap, leftimg.shape[1])
        cv2.imshow('before', rightimg)
        rightimg = im_trim(rightimg, gap, 0, rightimg_cp.shape[0], leftimg_cp.shape[1])
        cv2.imshow('after', rightimg)

        # 이미지 좌우 합치기
        add_img = np.hstack((leftimg, rightimg))

        # cv2.imshow('Frame0', frame0)
        # cv2.imshow('Frame1', frame1)
        cv2.imshow('Frame', add_img)

        # 종료키
        if cv2.waitKey(1) & 0xff == ord('q'):
            break


if __name__ == "__main__":
    execute()