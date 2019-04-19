import shutil

############## 복사 #######################

# 현재 디렉터리에서 파일 복사하기 후 다른 폴더로 저장
shutil.copy('./copyTest.txt', './copyfolder')   # copyTest.txt 파일을 -> copyfolder 라는 폴더로 복사후 이동.

# 절대경로를 이용해 저장하기
shutil.copy('C:/AceVision/attached file/requirements.txt', 'C:/Users/Lee Won Jae/Desktop/client')   # 절대경로에있는 파일 -> 절대경로 client라는 폴더로 저장

# 같은 디렉터리에서 파일 사본 만들기. (파일명이 서로 같으면 오류 발생)
shutil.copy('./copyTest.txt', './newcopyTest.txt')  # copyTest.txt 파일의 내용물이 -> newcopyTest.txt 라는 이름으로 그데로 복사.

# 전체 디렉터리(폴더)를 전체 복사
shutil.copytree('./copyfolder', './copyfolder_copy')    # copyfolder의 모든 내용물과 함께, copyfolder_copy에 모든것이 그데로 복사.

################# 이동 ##########################

# newcopyTest.txt 파일을  movetest 라는 폴더로 이동
shutil.move('./newcopyTest.txt', './movetest')


