import cv2
import numpy as np

# 검출할 픽셀값 좌표를 찾기위해 보조선 가로,세로 크기 지정. <사각형 면적 크기>
ROI_w = 30
ROI_h = 30

# ROI 좌표 지정.
ROI_list = [

    [(349, 182)],  # 380 60
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


    # [(380, 60)],         # 380 60
    # [(580, 52)],
    # [(726, 55)],
    # [(917, 74)],
    # [(307, 431)],
    # [(454, 459)],    # 453 460
    # [(687, 440)],
    # [(981, 447)],
    # [(571, 663)]
]


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

red = (0, 0, 255)
blue = (255, 0, 0)

img = cv2.imread('./image/cover.jpg')


while True:

    frame = img
    result = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display Center point check
    for i in range(len(ROI_list)):
        result = cv2.rectangle(result, ROI_list[i][0], (ROI_list[i][0][0] + ROI_w, ROI_list[i][0][1] + ROI_h), (255, 0, 255), 2)
        result = cv2.line(result, ROI_list[i][0], (ROI_list[i][0][0] + ROI_w, ROI_list[i][0][1] + ROI_h), (255, 0, 255), 1)
        result = cv2.line(result, (ROI_list[i][0][0], ROI_list[i][0][1] + ROI_h), (ROI_list[i][0][0] + ROI_w, ROI_list[i][0][1]), (255, 0, 255), 1)
        result = cv2.circle(result, (ROI_list[i][0][0] + int(ROI_w/2), ROI_list[i][0][1] + int(ROI_h/2)), 3, (255, 0, 255), -1)
        # cv2.putText(result, 'CP%d' % (i + 1), (ROI_list[i][0][0], ROI_list[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1,
        #             (255, 0, 255), 2, cv2.LINE_AA)
        pix = avg_fixel(gray, ROI_list[i][0][1] + int(ROI_h/2), ROI_list[i][0][0] + int(ROI_w/2))
        if pix == True:
            cv2.putText(result, "OK", (ROI_list[i][0][0], ROI_list[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, blue, 2, cv2.LINE_AA)
        else:
            cv2.putText(result, "NG", (ROI_list[i][0][0], ROI_list[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2, cv2.LINE_AA)

        print("결과픽셀", pix)
        print("좌표", ROI_list[i][0][0] + int(ROI_w/2), ROI_list[i][0][1] + int(ROI_h/2))
        print("****")

    cv2.imshow('gray', gray)
    #cv2.imshow('frame', frame)
    cv2.imshow('result', result)

    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
