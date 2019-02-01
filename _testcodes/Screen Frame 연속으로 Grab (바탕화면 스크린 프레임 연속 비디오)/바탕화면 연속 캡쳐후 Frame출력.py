from PIL import ImageGrab
import numpy as np
import cv2

while True:
    # Screen의 캡쳐할 좌표와 크기를 지정. (x시작좌표, y시작좌표, Width, Height)
    img = ImageGrab.grab(bbox=(0,0,1000,780)) #bbox specifies specific region (bbox= x,y,width,height)
    img_np = np.array(img)

    # 컬러 화면 그데로 출력함.
    frame_color = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    # 회색화면으로 변경
    frame_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", frame_gray)
    cv2.imshow("colour", frame_color)

    # q버튼을 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()