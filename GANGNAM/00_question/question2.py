### **문제: 은행 관리 프로그램**

# 1. `Account` 클래스를 정의하세요.
#     - `__init__` 메서드를 사용하여 은행 계좌의 소유주 이름과 초기 잔액을 설정합니다.
#     - `deposit` 메서드를 사용하여 입금을 처리합니다.
#     - `withdraw` 메서드를 사용하여 출금을 처리합니다. 출금할 금액이 잔액보다 크면 출금을 허용하지 않습니다.
#     - `display_balance` 메서드를 사용하여 현재 잔액을 출력합니다.
# 2. `Bank` 클래스를 정의하세요. 
#     - `__init__` 메서드를 사용하여 은행의 이름을 설정합니다.
#     - `create_account` 메서드를 사용하여 새로운 계좌를 생성합니다.
#     - `get_account` 메서드를 사용하여 계좌를 반환합니다.
#     - `display_accounts` 메서드를 사용하여 현재 은행에 있는 모든 계좌 정보를 출력합니다.
# 3. 사용자가 여러 번 계좌를 생성하고 입금, 출금, 잔액 조회 등의 작업을 수행할 수 있도록 하세요. 
# 사용자가 프로그램을 종료하고 싶을 때에는 "종료"를 입력하면 됩니다.


# 1 Account 클래스
class Account:
    
    # 은행 계좌의 소유주 이름과 초기 잔액을 설정
    # 생성자 : __init__ : 객체가 생성 자동 호출. 매개변수를 전달 받아 인스턴스 속성 초기화
    def __init__(self, owner, balance=0): #소유주 이름과 초기 잔액을 설정
        # 계좌 생성 시 잔액을 지정하지 않으면 0으로 설정
        self.owner = owner
        self.balance = balance #잔액

    # deposot 입금 처리
    def deposit(self,amount): #amount 입금, 출금 
        if amount > 0:
            self.balance += amount
            #입금 확인
            print(f"{amount}원이 입금되었습니다")
        else:
            print("입금액은 0보다 커야 합니다.")
    
    #withdarw 출금 처리
    def withdarw(self,amount):
        if 0 < amount <= self.balance: #self.balance 잔액
            self.balance -= amount
            print(f"{amount}원이 출금되었습니다") #출금 확인
        else:
            print("잔액이 부족하거나 잘못된 출금 금액입니다")
        
    # display_balance 잔액조회
    # 현재 계좌 소유주 이름과 잔액을 출력
    def display_balance(self): 
         print(f"{self.owner}님의 현재 잔액은 {self.balance}원 입니다.")


# 2 Bank 클래스
class Bank:

    #은행 이름을 설정
    def __init__(self, bankstore): #은행 이름
        self.bankstore = bankstore #은행 이름을 인스턴스 변수로 저장
        self.accounts = [] # 계좌 목록을 저장할 리스트 초기화
        #매개변수가 없어도 리스트 가질 수 있음

    #create_account 새로운 계좌 생성
    def create_account(self, owner, balance=0):
        account = Account(owner, balance) #상속
        self.accounts.append(account) #새로운 account 계좌 객체를 생성하고 self.accounts 리스트 추가
        print(f"{owner}님의 계좌가 생성되었습니다.")
    
    #get_account 계좌 반환
    def get_account(self, owner):
        for account in self.accounts:
            if account.owner == owner: #현재 계좌의 소유주 이름 (account.name)이 입력된 이름 (owner)과 같은지 확인
                return account #일치하는 계좌를 찾으면 그 계좌 객체를 반환하고 메서드를 종료
        print(f"{owner}님의 계좌를 찾을 수 없습니다.")

    #display_accounts 은행모든 계좌 정보
    def display_accounts(self):
        print(f"{self.bankstore} 모든 계좌 정보:")
        for account in self.accounts:
            print(f"소유주: {account.owner}, 잔액: {account.balance}원")

#bank = Bank("우리은행") #bankstore

# 계좌 생성
# bank.create_account("김이랑", 100000)
# bank.create_account("김루아", 200000)

# 특정 소유주의 계좌 검색
# account = bank.get_account("김이랑")
# if account:
#     account.display_balance()  # 김이랑님의 현재 잔액은 100000원 입니다.

# 모든 계좌 정보 출력
# bank.display_accounts()


# 3. 사용자가 여러 번 계좌를 생성하고 입금, 출금, 잔액 조회 등의 작업을 수행
# 사용자가 프로그램을 종료하고 싶을 때에는 "종료"를 입력하면 됩니다.
# 은행 생성

bank = Bank("우리은행") #bankstore

while True: #여러 번
    print("\n1. 계좌 생성")
    print("2. 입금")
    print("3. 출근")
    print("4. 잔액 조회")
    print("5. 은행 계좌 목록")
    print("종료")

    choice = input("원하는 작업을 선택하세요: ")

    if choice == "종료":
        print("프로그램을 종료합니다") #종료 입력시 종료
        break
    elif choice == "1":
        owner = input("소유주 이름을 입력하세요")
        bank.create_account(owner) #account 계좌
    elif choice == "2":
        owner = input("소유주 이름을 입력하세요: ")
        account = bank.get_account(owner)
        if account:
            amount = int(input("입금할 금액을 입력하세요: "))
            account.deposit(amount)
    elif choice == "3":
        owner = input("소유주 이름 입력: ")
        account = bank.get_account(owner)
        if account:
            amount = int(input("출금할 금액을 입력하세요: "))
            account.withdraw(amount) #amount 입출금
    elif choice == "4":
        owner = input("소유주 이름을 입력하세요: ")
        account = bank.get_account(owner)
        if account:
            account.display_balance()
    elif choice == "5":
        bank.display_accounts()
    
