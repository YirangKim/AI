# import oghiraModule
# from oghiraModule import another as an #모듈 안에 있는 특정 함수, an별칭
# from oghiraModule import ohgiraffers as oh #모듈 안에 있는 클래스, an별칭
import math #수학관련
import random 

#모듈 

# python 코드 파일로, 관련된 코드의 집합이다. 모듈은 함수, 클래스, 변수 등을 정의할 수 있으며
# 다른 python 프로그램에서 이를 가져와 사용할 수 있다.
# 모듈을 사용하면 코드의 재사용성을 높이고 코드 관리가 용이해지는 장점이 있다

# print(oghiraModule.ohgiraffers.Gorilla())
# print(oghiraModule.another())

# print(an())
# print(oh.Gorilla())

# 절대값
print(math.fabs(-5.5))

# 제곱근
print(math.sqrt(25))

# 거듭제곱
print(math.pow(2,3))

# 올림, 내림, 버림
print(math.ceil(4.2))
print(math.floor(4.2))
print(math.trunc(4.2))

# 반올림
print(round(3.1415))
print(round(3.1415, 2))
print(round(3.1415, 3))

# 팩토리얼
print(math.factorial(5))

# 1부터 6까지 랜덤 값 출력
print(random.randrange(1,7))

abc = ['a', 'b', 'c', 'd', 'e']
random.shuffle(abc)
print(abc)

# 아무 원소나 랜덤으로 하나 뽑아주는 함수
print(random.choice(abc))

