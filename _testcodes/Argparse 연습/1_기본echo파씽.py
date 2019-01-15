# version Python 3.6.4
# 데이터 파씽 parsing 하는 test
# 명령행 인자를 받아서 실행되는 프로그램에서 인자를 파싱할때 사용.

import argparse

# parser를 선언하고, 명령행 인자를 파싱하는 method를 이용해 파싱 수행.
parser = argparse.ArgumentParser()                                          # 이용자에게 데이터 파싱을 받음.
parser.add_argument("lwj", help="echo the string you use here")             # 입력한 lwj는 아래 print으로

args = parser.parse_args()

print(args.lwj)     #  cmd에서 <python name.py 내용>  입력하면, 그 파씽한 데이터가 그대로 전달됨 에코전달.