# version Python 3.6.4
# 데이터 파씽 parsing 하는 test
# 명령행 인자를 받아서 실행되는 프로그램에서 인자를 파싱할때 사용.

# 옵션인자를 추가 옵션값 제한. [0, 1, 2]번의 선택 옵션.

import argparse

parser = argparse.ArgumentParser()                                                                          # 이용자에게 데이터 파싱을 받음.

parser.add_argument("square", type=int, help="This is display a square calculating of a number")            # 입력을 받으면 args.square에 파싱을 함.
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], help="increase ouput verboiity")      # 옵션 인자 -v 또는 --verboisty 를 추가하면 옵션에 진입.
                                                                                                            # choice = [0, 1, 2]를 이용해서 옵션 3가지만 한정함. 그외는 오류.

args = parser.parse_args()
answer = args.square ** 2

if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)

'''
  >>> python 모듈이름.py
   -> 에러
   
  >>> python 모듈이름.py 4
   -> 16                            (기본 디폴트가 2의 제곱으로 되어있어 16만 출력) else조건.
   
  >>> python 모듈이름.py 4 -v 1     (옵션 0번)                 
   -> 4^2 == 16                     (elif 1번 모양으로 출력 )
   
  >>> python 모듈이름.py 4 -v 1     (옵션 1번)                 
   -> 4^2 == 16                     (elif 1번 모양으로 출력 )

  >>> python 모듈이름.py 4 -v 2     (옵션 2번)
  ->  the square of 4 equals 16     (elif 2번 모양으로 출력) 
  
  >>> python 모듈이름.py 4 -v 4     (그외 -v 3,4,5... 등 을 파싱하면,)
  ->  에러

'''
