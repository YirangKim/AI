# 요청 응답

# POST, PUT, PATCH등의 메소드를 사용하는 경우 HTTP 본문(body)사용
# 단순 텍스트나 json을 이용한다

# pydantic으로 요청 본문 받기
# 데이터 유효성 검사 및 설정 관리를 위한 라이브러리

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class UserInfo(BaseModel): #BaseModel상속
    name : str # 필수
    password : str # 필수
            # url은 선택사항이며, URL형식으로 받아야 한다. 기본값은 None 이다
    url : Optional[HttpUrl] = None #Optional 선택사항 받아도되고, 안받아도됨
# UserInfo 클래스 (BaseModeld을 상속 받음)
# BaseModel을 상속 받아야 request body 부분을 받을 클래스로 이용할 수 있음

# post 요청
@app.post("/users")
def createUser(user:UserInfo): #UserInfo
    return user
# /users post 요청에 담겨온 body 부분을 userInfo자료형에 담아 user라는 객체를 생성한다.