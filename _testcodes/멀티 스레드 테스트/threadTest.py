import threading
from time import sleep

# 스레드로 출력 테스트
def Threading(id):
    print("%s - Hello World" % id)

# 무한루프 스레드 가동 함수 (아이디, 딜레이 초)
def thProc(id, sec):
    while True:
        Threading(id)
        sleep(sec)

# 객체를 할당하고 인자를 대입함.
# target = 함수이름, args = 전달받는 인자
t1 = threading.Thread(target=thProc, args=("Test1", 1))   # 1초마다 함수 무한루프 실행
t2 = threading.Thread(target=thProc, args=("Test2", 3))
t3 = threading.Thread(target=thProc, args=("젠장", 5))

# 반드시 객체뒤에 .start()를 붙여야 스레드가 가동됨.
t1.start()
t2.start()
t3.start()