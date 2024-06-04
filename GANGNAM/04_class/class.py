#class Class_name:

class Person:
    national = 'korea'

    def greeting(self):
        return 'hello this is python'
    
# 클래스 속성 : 클래스 자체에 속하는 변수로, 모든 인스턴스가 공유하는 속성이다

class Person:
    national = 'korea'
    language = 'korean'

# 메소드 : 클래스 내부에 정의함 함수로, 인스턴스의 데이터를 조작하거나 동작을 정의한다.
    # self : 필드 및 메소드에 접근하는 객체를 의미한다.
    #        객체를 통해 접근 시 호출되는 메소드의 첫번째 인자로 항상 self를 넘겨 주어야 한다
        

class Person:
    national = 'korea'
    language = 'korean'

    def greeting(self):
        return 'hello, this is python'
    
    def infomation(self):
        return "i'm from" + self.national + "and i use" + self.language
    
    def favorite(self,color):
        return "i love" + color #매개변수

# 생성자 : __init__ : 객체가 생성될 떄 자동으로 호출된다. 매개변수를 전달 받아 인스턴스 속성을 초기화 할수 있다

class Student:
    # 클래스 변수 : 모든 인스턴스가 공유
    total_students = 0
    
    def __init__(self,name,score):
        # 인스턴스 변수 : 각 인스턴스가 별도로 가지는 변수
        self.name = name
        self.score = score
        Student.total_students += 1

    def display_info(self):
        print(f'student name : {self.name}')
        print(f'score : {self.score}')
        print(f'total students : {Student.total_students}')
        
# 학생 인스턴스 생성
student1 = Student("Alice", 95) #name, score
student2 = Student("bob", 88)

student1.display_info()
student2.display_info()


# 네임  스페이스

# 네임 스페이스는 크게 다섯가지로 나누어 볼 수 있다
# 1. 지역 네임스페이스 : 현재 함수나 메소드 내의 네임 스페이스
# 2. 인스턴스 네임스페이스 : 인스턴스 객체의 네임스페이스
# 3. 클래스 네임스페이스 : 클래스 객체의 네임스페이스
# 4. 전역 네임스페이스 : 모듈 내의 전역 네임 스페이스
# 5. 내장 네임스페이스 : 파이썬 내장 함수와 예의를 포함하는 네임스페이스

# 네임 스페이스의 검색 순서는 가장 가까운(가장 작은) 스코프 순서로 보통 로컬 > 전역 순이다.

# 전역 네임스페이스
variable = 'global variable'
print("전역 : ", variable)

def outer_function():
    # 외부 함수 네임스페이스
    variable = "outer variable"
    print("지역(외부 함수): ", variable)

    def inner_function():
        variable = "inner variable"
        print("지역(내부함수):", variable)

    inner_function()
outer_function()

class Test_class:
    # 클래스 네임스페이스
    variable = "class variavle"

    def __init__(self, value):
        self.variable = value # 인스턴스 네임스페이스
    
    def class_function(self):
        variable = "local variable"
        print("클래스 지역:", variable)

obj = Test_class("instance variable")
print("인스턴스 : ", obj.variable)
obj.class_function()

# global
# 함수 내부에서 전역변수를 참조하거나 수정할 때 이용하며, 함수 내부에서 전역변수에 접근할 수 있다
# 설정 값을 전역적으로 유지하고 여러 함수에서 이 값을 변경하거나 참조할 떄 요용하다

g_variable = "global variable" # 전역변수 선언

def modify_global(): #함수
    global g_variable
    g_variable = "global modified in function"

print(g_variable) #기존 내용
modify_global() #메소드 작동시켜야 전역변수 수정됨
print(g_variable) # 함수실행되서 수정됨

# nonlocal
# 중첩 함수에서 바깥 함수의 변수를 참조하거나 수정할 때 사용한다.

def outer_function(): #1-1
    variable = "outer variable" #2

    def inner_function(): #4
        nonlocal variable
        variable = "outer modified in inner function"

    print(variable) #2-1
    inner_function()#3
    print(variable) #4-1

outer_function() #1

# private

class BankAccount:

    def __init__(self,account_number,balance):
        self.account_number = account_number #공개 속성, 접근 허용
        self.__balance = balance             #__비공개 속성, 접근 제한

    def get_balance(self):
        return self.__balance
    
    def deposit(self,amount):
        if amount > 0:
            self.__balance += amount
        else:
            raise ValueError("입금 금액은 양수여야 합니다.")
        
    def withdarw(self,amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
        else:
            raise ValueError("잔액이 부족하거나 잘못된 출금 금액입니다")


# 계좌 생성
my_account = BankAccount("123-456-789", 100000) #account_number, balance / self 기입 안해줌

# 계좌 번호 출력
print("계좌 번호: ", my_account.account_number)

# 비공개 속성에 직접 접근 시도
# __(언더스코어 2개)로 시작하는 속성은 완전한 의미의 private는 아니지만, 어느 정도 보호되는 속성으로 취급함
# 이를 이름 장싱(name mangling)이라고 함
# 속성의 이름을 내부적으로 변경하여 클래스 외부에서 직접 접근하는 것을 어렵게 만듦
print(my_account._BankAccount__balance) # 클래스 쓰고, 비공개 속성

# 비공개 속성에 접근하는 메소드 사용
print("잔액 : ", my_account.get_balance())

# 입금
my_account.deposit(50000)
print("입금 전 후 잔액:", my_account.get_balance())

# 출금
my_account.withdarw(30000)
print("출금 후 잔액:", my_account.get_balance())

# 잘못된 금액으로 출금 시도
try:
    my_account.withdarw(150000)
except ValueError as e:
    print("오류", e)

# 상속

# 파이썬도 클래스의 상속을 지원한다
# 자식 클래스는 부모 클래스의 필드나 메소드를 사용할 수 있다.

class Person:
    national = 'korea'

    def greeting(self):
        return 'hello, this is python'

class Student(Person): #상속
    pass #구문상 필요는 하지만 프로그램이 아무 작업도 하지 않기를 원하는 경우 사용

student3 = Student()
print(student3.greeting())

# 다중 상속

class Learner:
    def greeting(self):
        return 'hello i am Leaner'
    
    def learn(self):
        return 'i am learning python'
    
class Student1(Person,Learner):
    pass

student4 = Student1()
print(student4.greeting())
print(student4.learn())
print(student4.greeting())

# ========== 질문 하기 ================
# 부모 클래스 속성을 오버라이딩 할 수 있다.

class Person1:
    national = 'korea'

    def greeting(self):
        return 'hello, this is python'
    
class Learner1(Person1): #Person1 상속
    def __init__(self,subject):
        self.subject = subject

    def learn(self):
        return 'i am learning' + self.subject
    
class Student2(Learner1): #Learner1 상속
    def __init__(self, name, subject):
        Learner1.__init__(self, subject)
        self.name = name

    def greeting(self):
        return "hello, my name is" + self.name
    
student5 = Student2('홍길동', 'python') # name, subject
print(student5.greeting())
print(student5.learn())