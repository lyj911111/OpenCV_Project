import os
import cv2
import random

path = "./templates/"
file_list = os.listdir(path)

# print(path + file_list[0])
# print(path + file_list[1])

# 2차원 배열.
template_list = []
template_str = []
template_mat_format = []
w_h_list = []
for i in range(len(file_list)):

    template_str = [path + file_list[i]]
    template_list.append(template_str)
    a = cv2.imread(template_list[i][0])     # 이미지 행렬 포멧을 a으로 저장
    template_mat_format.append(a)           # a 행렬을 리스트에 추가
    w_h_list.append([a.shape[0], a.shape[1]])


print(w_h_list)                 # template의 폭과 높이에 대한 리스트
print(w_h_list[0][0], w_h_list[0][1])
print(w_h_list[1][0], w_h_list[1][1])

#print(template_mat_format)      # template의 2차원 배열에 대한 정보.
cv2.imshow('0', template_mat_format[0])
cv2.imshow('1', template_mat_format[1])   # 배열 출력.

for i in range(3):
    print(random.randrange(0, 256))

#print(template_list[0][0])
#print(template_list[1][0])
#print(template_mat_format)
# a = cv2.imread(template_list[0][0])
# b = cv2.imread(template_list[1][0])
# print(a.shape)
# print(b.shape)



cv2.waitKey(0)