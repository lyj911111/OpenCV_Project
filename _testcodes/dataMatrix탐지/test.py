import cv2

from pylibdmtx.pylibdmtx import decode

# Read file using OpenCV


data = str(decode(cv2.imread("data.jpg")))


print(data)

sn = ""

for i in range(24, 37):
    sn += data[i]

print(sn)