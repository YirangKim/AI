

try:
    4 / 0

except:
    print('예외발생')

try:
    4 / 0
except ZeroDivisionError as e:
    print(e)


try:
    a= [1,2]
    print(a[3])
    4/0
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다")
except IndexError:
    print('인덱싱 할 수 없습니다.')

# try-finally 문
# 예외 발생 여부와 상관없이 항상 수행되는 내용을 finally에 작성할 수 있다
# try:
#     f = open('foo.txt', 'r')
# finally:
#     f.close()

# try-else 문
# try 문에는 else절도 사용할 수 있다.
# try 문 수행 중 오류가 발생하면 except절, 오류가 발생하지 않으면 else절이 수행된다

try:
    age = int(input('나이를 입력 해주세요')) #나이입력
except:
    print("입력이 정확하지 않습니다")
else:
    if age <= 18:
        print("미성년자는 출입이 불가능합니다")
    else:
        print('환영합니다.')

# 오류 회피하기
# 코드를 작성하다 보면 특정 오류가 발생할 경우 그냥 통과 시켜야 할 경우가 있다
# try문 안에서 error가 발생할 경우 pass를 사용하여 오류를 그냥 지나가도록 작성할 수 있다

try:
    f=open("없는파일", 'r')
except FileNotFoundError:
    pass

# 예외 만들기
# 프로그램을 수행하다 보면 특수한 경우에 예외처리를 하려고 예외를 만드는 경우가 발생한다
# 파이썬 내장 클래스인 Exception 클래스를 상속하여 만들 수 있다.

class MyError(Exception): #Exception 상속
    pass

def say_nick(nick):
    if nick == '돼지':
        raise MyError()
    print(nick)

try:
    say_nick('곰')
    say_nick('돼지')
except MyError:
    print("허용되지 않은 별명입니다.")