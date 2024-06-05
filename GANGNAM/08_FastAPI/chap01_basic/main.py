from fastapi import FastAPI
# fast API
# python으로 작성된 API를 만들기 위한 웹 프레임워크

# 장점
# 1. 고성능 : 아주빠른 선능을 제공하며, 기존의 flask 웹 프레임워크보다 2배가량 빠르다
# 2. 쉬운 사용 : 작성하기 쉬운 코드 방식을 가지고 있다.
# 3. 자동 문서화 = swagger 문서 지원
# 4. 비동기 지원 = 비동기 기능을 지원하여 비동기 작업을 쉽게 처리할 수 있다.

# app 객체를 통해 FastAPI 설정을 할 수 있다.
app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

# __name__ 변수.
# python 에서는 파일이 실행될떄 마다 특별한 변수인 __name__을 갖는다
# 스크립트가 실행 될 때, __name__변수는 "__main__"으로 설정된다
# 스크립트가 다른 모듈에 임포트 될 때 __name__ 변수는 해당 모듈의 이름으로 바뀐다
# main에서만 서버를 띄우겠다 : 다른데서는 막겠다
    
# main = main.py 파일을 위미
# app = main.py 에서 FastAPI()객체를 식별하는 app 객체를 의미
# --reload = 파일에 변화가 생기면 재시작 하겠다는 옵션

