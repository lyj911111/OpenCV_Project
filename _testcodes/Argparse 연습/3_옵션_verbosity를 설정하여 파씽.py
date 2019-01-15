# version Python 3.6.4
# 데이터 파씽 parsing 하는 test
# 명령행 인자를 받아서 실행되는 프로그램에서 인자를 파싱할때 사용.

# 옵션인자를 추가하는 방법. -v를 붙이면 아래 부연으로 작성한데로 파씽이 되며, 그외는 디폴트로 파씽이 된다.

import argparse

parser = argparse.ArgumentParser()                                                                          # 이용자에게 데이터 파싱을 받음.

parser.add_argument("square", type=int, help="This is display a square calculating of a number")            # 입력을 받으면 args.square에 파싱을 함.

#parser.add_argument("-v", "--verbosity", type=int, help="increase ouput verboiity", action="store_true")    # --verbosity라는 인자가 입력되면 (또는 -v 입력), "store_true"으로 플레그가 변경되어 if문에 들어감.
                                                                                                            # 지정하지 않으면 묵시적으로 Faluse임.
parser.add_argument("-v", "--verbosity", type=int, help="increase ouput verboiity")

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
   
  >>> python 모듈이름.py 4 -v 1     	(옵션 1번 / 순서가 바뀌어도 -v 만들어가기만 하면 똑같이 인식) 
   -> 4^2 == 16                     (elif 1번 모양으로 출력 )

  >>> python 모듈이름.py 4 -v 2     	(옵션 2번)
  ->  the square of 4 equals 16     (elif 2번 모양으로 출력) 

'''
