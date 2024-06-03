# ### **문제 2: 학생 성적 관리 프로그램**

# 학생들의 성적을 관리하는 프로그램을 작성하세요. 프로그램은 다음 기능을 포함해야 합니다:

# 1. 학생의 이름과 성적을 입력 받아 저장합니다.
# 2. 특정 학생의 성적을 조회합니다.
# 3. 모든 학생의 평균 성적을 계산하여 출력합니다.
# 4. 성적이 특정 점수 이상인 학생들의 이름을 출력합니다.


# 1. 학생 이름 성적 입력 받기
print("학생 이름을 입력하세요: ")
student = input()
#print(student) 	
score = 0

# 2. 특정 학생 성적 조회
match student:
    case "김이랑":
        print("김이랑 학생 성적은")
        score = 80
    case "김루아":
        print("김루아 학생 성적은")
        score = 90
    case "배정현":
        print("배정현 학생 성적은")
        score = 100
    case _:
        print("해당 학생이 없습니다")
print(str(score) + "점 입니다.")    
        

# 3. 모든 학생 평균
allstudents = [80, 90, 100]
avg = sum(allstudents)/len(allstudents)
print("===모든 학생 평균 점수는 ===")
print(avg )
