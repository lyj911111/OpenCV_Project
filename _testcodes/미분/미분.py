import math
from sympy import symbols, Limit    # pip install sympy

x, a, h = symbols('x, a, h')

fx = 3 * (x**2) - 4 * x + 1     # 함수 f(x) 정의
fxa = fx.subs({x: a})           # f(x)에 x = a 대입
fxh = fx.subs({x: a + h})       # f(x)에 x = a + h 대입

result = Limit( (fxh - fxa)/h, h, 0 ).doit()     # 극한값(미분계수) 계산

print(fx)
print(fxa)
print(fxh)

print("미분 Result:", result)