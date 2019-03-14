import cv2
from more_itertools import unique_everseen
import numpy as np

# 2대의 카메라 해상도 설정 및 출력.
cap0 = cv2.VideoCapture(0)
cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # Width 4608
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 960) # Height 3288
print("첫번째 카메라 현재 해상도 %d x %d" %(cap0.get(3), cap0.get(4)))

cap1 = cv2.VideoCapture(1)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 4608) # Width 4608
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 3288) # Height 3288
print("두번째 카메라 현재 해상도 %d x %d" %(cap1.get(3), cap1.get(4)))

# 검사할 총 리벳갯수 입력 (기준값)
judge = 32

# 검출할 영역(관심영역)을 지정 (start point to end point of Rectangle Box).
ROI_list = [
    [(160, 50), (1200, 180)],
    [(150, 360), (1200, 500)],
    [(130, 640), (1250, 800)]
 ]

# 예외처리 박스
ex_w = 30   # 가로 x 세로
ex_h = 30
except_box = [
    [(205, 425)],
    [(910, 415)],
    [(440, 385)]
]

truevalue = 0
falsevalue = 0
wholevalue = 0

def judgefunc(cnt):
    global judge, truevalue, wholevalue, falsevalue

    wholevalue = wholevalue + 1         # 함수가 수행할때마다 증가
    if cnt == judge:                    # 판독값과 기준값이 일치할때 true값 증가
        truevalue = truevalue + 1
    else:                               # 판독값과 기준값이 일치할때 faluse값 증가
        falsevalue = falsevalue + 1


    # 함수가 5번 수행했을때 수행.
    if (wholevalue > 5):
        if truevalue > 3:               # true값이 3이상이다 합격(1)
            wholevalue = 0
            truevalue = 0
            return 1
        elif falsevalue > 3:            # false값이 3이상이다 불합격(-1)
            wholevalue = 0
            falsevalue = 0
            return -1
    else:                               # 판독안할 때는 그냥 return 0
        return 0

def houghCircle():
    fail = 0
    overfail = 0
    underfail = 0

    while True:

        # 프레임 읽기
        ret, frame = cap1.read()

        # 화면 크기 조절 (본인에게 맞는 해상도 조절)
        result = cv2.resize(frame, (1280, 960), interpolation=cv2.INTER_LINEAR)
        img_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)  # gray로 변환.

        # 관심영역(ROI, Range of Interest) 지정.
        for i in range(len(ROI_list)):
            result = cv2.rectangle(result, ROI_list[i][0], ROI_list[i][1], (150, 50, 150), 5)
            cv2.putText(result, 'ROI%d' %(i + 1), (ROI_list[i][0][0], ROI_list[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # 예외처리(Exception Box) 지정.
        for i in range(len(except_box)):
            result = cv2.rectangle(result, except_box[i][0], (except_box[i][0][0]+ex_w, except_box[i][0][1]+ex_h), (0, 255, 0), 1)
            cv2.putText(result, 'expt%d' %(i + 1), (except_box[i][0][0], except_box[i][0][1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)


        # param1 = 250, param2 = 20
                                     # 원본과 비율 / 찾은 원들간의 최소 중심거리 / param1, param2를 조절해 원을 찾음 250 20 5 30
        circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1.208, 10, param1=34, param2=24, minRadius=10, maxRadius=13)

        # 관심영역내 원만을 탐지함.
        if circles is not None:
            circles = np.uint16(np.around(circles))

            # 미리 예외 처리 하고 들어감.
            # if ( (i[0] < except_box[0][0][0] or i[0] > except_box[0][0][0]+ex_w) or (i[1] < except_box[0][0][1] or i[1] > except_box[0][0][1]+ex_h) ):
            #     if ( (i[0] < except_box[1][0][0] or i[0] > except_box[1][0][0]+ex_w) or (i[1] < except_box[1][0][1] or i[1] > except_box[1][0][1]+ex_h) ):
            #         cv2.circle(result, (i[0], i[1]), i[2], (0, 0, 255), 2)  # 원 외곽 컨투어 표시.
            #         cv2.circle(result, (i[0], i[1]), 3, (255, 0, 40), -1)  # 원의 중심점을 표시

            cnt = 0
            whole_circle_list = []
            whole_circle_tuple = []
            except_center_list = []
            for i in circles[0, :]:
                for j in range(len(ROI_list)):
                    if (i[0] > ROI_list[j][0][0] and i[0] < ROI_list[j][1][0]) and (i[1] > ROI_list[j][0][1] and i[1] < ROI_list[j][1][1]):  # ROI 관심영역 내에서 찾아냄.
                        whole_circle_list.append([i[0], i[1]])  # ROI 내 모든 중심점.
                        # cnt = cnt + 1

                        for k in range(len(except_box)):
                            if (i[0] > except_box[k][0][0] and i[0] < (except_box[k][0][0] + ex_w)) and (i[1] > except_box[k][0][1] and i[1] < (except_box[k][0][1] + ex_h)):
                                except_center_list.append([i[0], i[1]])             # 예외처리 중심점을 리스트에 추가
                                whole_circle_list.remove(except_center_list[0])     # 예외처리 리스트에 있는 중심점들을 전체 중심점리스트에서 제거
                                # print("예외처리 중심점:", except_center_list)
                                except_center_list.pop()                            # 제외 처리를 하고나서 값을 빼서 다음 값을 프로세스 진행하도록 함.

                        # 예외박스에 있는 부분 중심좌표 제거
                        # if (i[0] > except_box[0][0][0] and i[0] < (except_box[0][0][0] + ex_w)) and (i[1] > except_box[0][0][1] and i[1] < (except_box[0][0][1] + ex_h)):
                        #     except_center_list.append([i[0], i[1]])
                        #     whole_circle_list.remove(except_center_list[0])

                        # if (i[0] > except_box[1][0][0] and i[0] < (except_box[1][0][0] + ex_w)) and (i[1] > except_box[1][0][1] and i[1] < (except_box[1][0][1] + ex_h)):
                        #     except_center_list.append([i[0], i[1]])
                        #     whole_circle_list.remove(except_center_list[0])

                        # if (i[0] > except_box[2][0][0] and i[0] < (except_box[2][0][0] + ex_w)) and (i[1] > except_box[2][0][1] and i[1] < (except_box[2][0][1] + ex_h)):
                        #     except_center_list.append([i[0], i[1]])
                        #     whole_circle_list.remove(except_center_list[0])

                # 처리가 다된 리스트를 튜플로 전환 (화면 출력을 위해)
                for n in range(len(whole_circle_list)):
                    whole_circle_tuple.append(tuple(whole_circle_list[n]))
            # 화면 출력
            whole_circle_tuple = list(unique_everseen(whole_circle_tuple))      # 중복 리스트 제거함수. unique_everseen
            for z in range(len(whole_circle_tuple)):
                cv2.circle(result, whole_circle_tuple[z], i[2], (0, 0, 255), 2)  # 원 외곽 컨투어 표시.
                cv2.circle(result, whole_circle_tuple[z], 3, (255, 0, 40), -1)  # 원의 중심점을 표시

            #
            # cnt = 0
            # for i in circles[0, :]:
            #     if (i[0] > ROI_list[0][0][0] and i[0] < ROI_list[0][1][0]) and (i[1] > ROI_list[0][0][1] and i[1] < ROI_list[0][1][1]):        # ROI 관심영역 내에서 찾아냄.
            #
            #         cv2.circle(result, (i[0], i[1]), i[2], (0, 0, 255), 2)    # 원 외곽 컨투어 표시.
            #         cv2.circle(result, (i[0], i[1]), 3, (255, 0, 40), -1)     # 원의 중심점을 표시
            #         cnt = cnt + 1
            #
            #     if (i[0] > ROI_list[1][0][0] and i[0] < ROI_list[1][1][0]) and (i[1] > ROI_list[1][0][1] and i[1] < ROI_list[1][1][1]):        # ROI 관심영역 내에서 찾아냄.
            #
            #         cv2.circle(result, (i[0], i[1]), i[2], (0, 0, 255), 2)    # 원 외곽 컨투어 표시.
            #         cv2.circle(result, (i[0], i[1]), 3, (255, 0, 40), -1)     # 원의 중심점을 표시
            #         cnt = cnt + 1
            #
            #     if (i[0] > ROI_list[2][0][0] and i[0] < ROI_list[2][1][0]) and (i[1] > ROI_list[2][0][1] and i[1] < ROI_list[2][1][1]):        # ROI 관심영역 내에서 찾아냄.
            #
            #         cv2.circle(result, (i[0], i[1]), i[2], (0, 0, 255), 2)    # 원 외곽 컨투어 표시.
            #         cv2.circle(result, (i[0], i[1]), 3, (255, 0, 40), -1)     # 원의 중심점을 표시
            #         cnt = cnt + 1



            # 원의 갯수
            cnt = len(whole_circle_list)

            PassOrNG = judgefunc(cnt)

            if (PassOrNG == 1):
                print("PASS")
            elif (PassOrNG == -1):
                print("NG")
            else:
                pass

            # cv2.imshow('ori',img2)
            cv2.imshow('HoughCircle', result)

            # if cnt != 32:
            #     fail = fail + 1
            #     #cv2.imwrite('./failcase/fail%d.jpg' %fail, result)
            #
            # if(cnt > 32):
            #     overfail = overfail + 1
            #     cv2.imwrite('./failcase/overfail/fail%d.jpg' % overfail, result)
            # elif(cnt < 32):
            #     underfail = underfail + 1
            #     #cv2.imwrite('./failcase/underfail/fail%d.jpg' % underfail, result)
            #
            # print("불량횟수: %d // 초과 횟수: %d // 미만 횟수: %d" % (fail, overfail, underfail))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print('원을 찾을 수 없음')

    cap1.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # 메인함수
    houghCircle()