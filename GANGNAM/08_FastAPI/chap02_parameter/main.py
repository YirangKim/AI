from fastapi import FastAPI

app = FastAPI()

# 경로 매개변수
# URL 경로에 들어가는 매개변수

# @app.get("/users/{user_id}")
# def get_user(user_id):
#     return {"user_id":user_id}

# 타입을 정의하려면?
# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     return {"user_id":user_id}

# @app.get("/users/aaa")
# def get_current_user():
#     return {"user_id" : 123}

# 경로의 순서 문제 이해

# 쿼리 매개변수

# 호스트주소/path? 뒤에 오는 변수들을 쿼리 매개변수 라고 한다
# 각 매개변수는 & 기호로 구분되고 key=value 쌍으로 정의된다

# @app.get("/users")
# def get_users(limit:int, name: str):
#     return {"limit:":limit, "name":name}

# http://127.0.0.1:8000/users?limit=123&name=abc
# localhost주소/docs

@app.get("/users")
def get_users(limit:int = 200): #기본값 지정
    return {"limit":limit}

# 포트번호 지정
# uvicorn main:app --port=8080 --reload