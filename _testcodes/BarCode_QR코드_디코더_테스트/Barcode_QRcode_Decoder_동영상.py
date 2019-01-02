# Python Version 3.7.1

import cv2                      # pip install opencv-python
import numpy as np              # pip install numpy
import pyzbar.pyzbar as pyzbar  # pip install pyzbar
import sys
import time

cap = cv2.VideoCapture(0)   #  cap에 비디오 영상을 저장.

# 바코드와 QR코드를 해독하는 클래스
def decode(im) :

  decodedObjects = pyzbar.decode(im)        # 바코드와 QR코드를 찾아냄

  for obj in decodedObjects:                # 바코드의 정보를 출력
    print('Type : ', obj.type)
    print('Data : ', str(obj.data), '\n')

  return decodedObjects                     # 바코드 정보를 return


# 받은 정보를 Display하는 클래스
def display(im, decodedObjects):            # 바코드와 QR코드의 정보를 받고, 위치를 display함

  # Loop over all decoded objects
  for decodedObject in decodedObjects:
    points = decodedObject.polygon

    # If the points do not form a quad, find convex hull
    if len(points) > 4 :
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else :
      hull = points

    # Number of points in the convex hull
    n = len(hull)

    # Draw the convext hull
    for j in range(0, n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255, 0, 0), 3)

  # Display results
  cv2.imshow("Results", im)
  #cv2.waitKey(0)

# Main
if __name__ == '__main__':
    while True:
        _, frame = cap.read()                # 영상 연속으로 읽기.

        #cv2.imshow('frame', frame)          # 원본 영상을 보여줌

        decodedObjects = decode(frame)      # Return값 바코드정보를 display에 넣기 위해
        display(frame, decodedObjects)      # 바코드의 위치를 화면에 출력하기 위해

        if cv2.waitKey(1) & 0xFF == ord('q'):                   #  'q'를 누르면 종료.
            break

cap.release()
cv2.destroyAllWindows()