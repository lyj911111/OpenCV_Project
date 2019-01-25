# 함수의 작동 시간 측정함.
# 퍼포먼스(성능) 측정

import time

# 작동시간을 리턴
def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time-start_time))
        return result
    return wrapper_fn


@logging_time   # decorator기능, 함수나 클래서 위에 @를 앞에두고 작성하여 작동시간을 출력함.
def my_func1():
    print("Hello world"*10000000)


@logging_time
def my_func2():
    for i in range(10000):
        print("속도 지연 하기")

if __name__=="__main__":
    my_func1()
    my_func2()      # 함수가 끝나면서 decorator함수도 같이 실행함.

