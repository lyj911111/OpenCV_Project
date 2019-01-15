# version Python 3.6.4
# 데이터 파씽 parsing 하는 test
# 명령행 인자를 받아서 실행되는 프로그램에서 인자를 파싱할때 사용.

import argparse

# parser를 선언하고, 명령행 인자를 파싱하는 method를 이용해 파싱 수행.
parser = argparse.ArgumentParser()                                                   # 이용자에게 데이터 파싱을 받음.
parser.add_argument("square", help="this is square of a given number", type=int)     # cmd에서 <python 모듈이름.py -h> 또는 <python 모듈이름.py --help> 입력하면 도움말 메세지를 남긴다.
                                                                                     # cmd에서 파씽받을 문자의 type을 int로 결정. (default는 문자열 형태이다)

args = parser.parse_args()

print(args.square ** 2)     #  <python 모듈이름.py 인자전달>  입력하면, 그 파씽한 데이터가 그대로 전달됨.
                            # int형 type을 정헀기때문에, 숫자가 아닌 다른 문자가 들어가면 에러 발생함.

'''
    ex) 모듈이름 lwj.py 
        
        cmd에서
        
        입력 >> python lwj.py 4
        출력 >> 16
        
        입력 >> python lwj.py damn
        출력 >> Error invalid int
    
'''