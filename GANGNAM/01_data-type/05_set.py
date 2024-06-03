# SET

# 중복을 허용하지 않으며 순서 없이 요소를 저장하는 컬렉션이다
# 따라서 중복 제거가 필요할 때 유용하게 사용할 수 있다
# {} 중괄호를 사용하여 집합을 생성한다

ohgiraffers = {'pig', 'squirrel','bear','gorilla', 'pig'}
print(ohgiraffers)

# 리스트로 set생성
another_safari_set = set(['monkey', 'tiger', 'wolf'])
print(another_safari_set)

mixed_set = {1, 'bear', (1,2,3)}
print(mixed_set)

ohgiraffers.remove('pig')
print(ohgiraffers)

ohgiraffers.add('pig')
print(ohgiraffers)

# SET 메소드
 
 # 1. update()
ohgiraffers1 = set(["monkey", 'tiger', 'wolf'])
print(ohgiraffers1)
ohgiraffers1.update(['monkey', 'wolf', 'tiger', 'squirrel'])
print(ohgiraffers1)

# 2. discard()
ohgiraffers1.discard('pig')

# 3. pop()
ohgiraffers1.pop()
print(ohgiraffers1)

# 4. clear() 모든 값 제거
ohgiraffers1.clear()
print(ohgiraffers1)

# 5. union() : 두 set 합집합
javaTeam = {'gorilla', 'tiger', 'monkey'}
pythonTeam = {'pig', 'bear', 'gorilla', 'tiger'}

ohgiraffers2 = javaTeam.union(pythonTeam)
print(ohgiraffers2)

# 6. interserction() : 두 set 자료형의 교집합을 반환
print(javaTeam.intersection(pythonTeam))

# 7. difference() : 좌향을 기준으로 우향의 차집합을 반환한다.
print(javaTeam.difference(pythonTeam))

# 8. copy : 대상 set을 복사하여 반환한다.
javaTeam1 = javaTeam.copy()
print(javaTeam1)
print(id(javaTeam1))

