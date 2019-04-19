'''
    파일을 read 하여 리스트에 저장하고, 그 리스트에 있는 문자열을 골라서 삭제
'''

with open("./test.txt", "r") as f:
    lines = f.readlines()
with open("./test.txt", "w") as f:
    for line in lines:
        if line.strip("\n") != "ich liebe dich so wie du mich":     # <= 이 문자열만 골라서 삭제
            f.write(line)


