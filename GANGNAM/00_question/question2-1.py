class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"{amount}원이 입금되었습니다.")
        else:
            print("입금액은 0보다 커야 합니다.")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"{amount}원이 출금되었습니다.")
        else:
            print("잔액이 부족합니다.")

    def display_balance(self):
        print(f"{self.owner}님의 현재 잔액은 {self.balance}원 입니다.")

class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def create_account(self, owner, balance=0):
        account = Account(owner, balance)
        self.accounts.append(account)
        print(f"{owner}님의 계좌가 생성되었습니다.")

    def get_account(self, owner):
        for account in self.accounts:
            if account.owner == owner:
                return account
        print(f"{owner}님의 계좌를 찾을 수 없습니다.")

    def display_accounts(self):
        print(f"{self.name}의 모든 계좌 정보:")
        for account in self.accounts:
            print(f"소유주: {account.owner}, 잔액: {account.balance}원")

# 은행 생성
bank = Bank("MyBank")

# 메인 프로그램
while True:
    print("\n1. 계좌 생성")
    print("2. 입금")
    print("3. 출금")
    print("4. 잔액 조회")
    print("5. 은행 계좌 목록")
    print("종료")

    choice = input("원하는 작업을 선택하세요: ")

    if choice == "종료":
        print("프로그램을 종료합니다.")
        break
    elif choice == "1":
        owner = input("소유주 이름을 입력하세요: ")
        bank.create_account(owner)
    elif choice == "2":
        owner = input("소유주 이름을 입력하세요: ")
        account = bank.get_account(owner)
        if account:
            amount = int(input("입금할 금액을 입력하세요: "))
            account.deposit(amount)
    elif choice == "3":
        owner = input("소유주 이름을 입력하세요: ")
        account = bank.get_account(owner)
        if account:
            amount = int(input("출금할 금액을 입력하세요: "))
            account.withdraw(amount)
    elif choice == "4":
        owner = input("소유주 이름을 입력하세요: ")
        account = bank.get_account(owner)
        if account:
            account.display_balance()
    elif choice == "5":
        bank.display_accounts()