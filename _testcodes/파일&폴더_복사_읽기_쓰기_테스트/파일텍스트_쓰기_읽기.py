########## 쓰기모드 #################

# 현재 디렉터리에 텍스트 파일 생성하기. 쓰기모드 열기
f = open("newfile.txt", 'w')

# 뒤에 계속 이어서 써짐.
data = "안녕"
f.write(data)   # data를 파일에 쓰기
data = "하세요\n"
f.write(data)   # data를 파일에 쓰기

# 개행으로 줄을 나눔
data = "안녕\n"
f.write(data)   # data를 파일에 쓰기
data = "하세요"
f.write(data)   # data를 파일에 쓰기
f.close() # 쓰기모드 닫기

########## 읽기 모드 ###############

# 현재 디렉터리에 텍스트파일을 읽기
f = open("newfile.txt", 'r')

# 한줄씩 계속 읽기 줄만 읽기, 출력
line = f.readline()
print(line)
line = f.readline()
print(line)
line = f.readline()
print(line)
f.close() # 읽기모드 닫기

# 현재 디렉터리에 텍스트파일을 읽기
f = open("newfile.txt", 'r')

# 한번에 모든 라인 읽기
while True:
    line = f.readline()
    if not line:        # 라인을 계속 읽고 출력하다가  line이 없으면 break, None을 return.
        break
    print(line)
f.close() # 읽기모드 닫기


# readlines() 함수 이용하기. - 각줄을 리스트에 담음
f = open("newfile.txt", 'r')
lines = f.readlines()
print(lines)    # 각 줄을 리스트에 담아서 출력.
for i in lines:
    print(i)
f.close()

# read() 함수 이용하기. - 텍스트파일 전체를 통째로 출력
f = open("newfile.txt", 'r')
data = f.read()
print("read() 함수:\n", data)
f.close()
