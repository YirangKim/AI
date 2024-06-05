from fastapi import FastAPI, Request, Depends, Form, status
import models
from database import engine, session_local
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

app = FastAPI()
# 데이터 베이스 테이블 생성. sqlalchemy 라이브러리 기능을 이용해 테이블 생성
models.Base.metadata.create_all(bind=engine)

# FastApi 애플리케이션 에서 Jinja2 템플릿 엔진을 사용하도록 설정
templates = Jinja2Templates(directory="templates")

# 데이터베이스 세션 가져오기
def get_db():
    db = session_local() #호출 될 때 마다 새로운 세션 객체를 생성
    try:
        yield db # 데이터베이스 세션 객체를 반환
    finally:
        db.close()

# 비동기 함수 제공
# 비동기 함수의 장점
# 성능 향상 : 비동기 함수는 여러 작업을 동시에 처리할 수 있다
# I/O 작업(ex)데이터베이스 쿼리, 외부 api호출)을 기다리는 동안 다른 작업을 처리할 수 있다.
# 블로킹 방지 : 동기 함수는 한번에 하나의 작업만 처리하므로, 작업이 끝날 때 까지 다른 요청을 처리할수 없다

# 비동기 함수를 사용하면 더 많은 클라이언트 요청을 동시에 처리할 수 있다. 예) async

@app.get("/") # request : HTTP요청 객체를 포함. # Depends 키워드로 인해 세션 객체가 먼저 생성됨 # home이 실행되지 전에 Session이 먼저 실행
async def home(request: Request, db : Session = Depends(get_db)):

    # 데이터베이스에서 Todo 모델을 조회하고, id를 기준으로 내림차순 정렬
    todos = db.query(models.Todo).order_by(models.Todo.id.desc())

    # 인덱스 템플릿을 렌더링하여 사용자에게 반환
    return templates.TemplateResponse("index.html", {"request":request, "todos":todos})

# 등록
@app.post("/add")                       #html에서 form태그로 넘겨준 값
async def add(request:Request, task:str=Form(...), db:Session = Depends(get_db)):
    
    #Todo 클래스의 인스턴스를 생성하고, task값을 전달하여 할 일을 생성함.
    todo = models.Todo(task=task)
    #생성한 할 일을 데이터베이스에 추가
    db.add(todo)
    # 변경 사항을 커밋
    db.commit()

    #요청이 성공적으로 처리됐으면 리디렉션
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER) #성공했을 때 303

# 선택한 번호 조회
@app.get('/edit/{todo_id}') 
async def add(request:Request, todo_id: int, db: Session = Depends(get_db)):

    # 데이터베이스에서 Todo 모델을 가져와, id가 todo_id와 일치하는 첫번째 항목을 가져옴
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    # 템플릿을 렌더링하여 사용자에게 반환
    return templates.TemplateResponse("edit.html", {"request" : request, "todo":todo})


# 수정
@app.post("/edit/{todo_id}")                     #사용자 임력값
async def add(request:Request, todo_id:int, task:str = Form(...), completed:bool = Form(False), db:Session = Depends(get_db)):

    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    # todo task 속성을 품에서 받아온 값으로 업데이트
    todo.task = task
    # todo의 completed 속성을 폼에서 받아온 completed 값으로 업데이트
    todo.completed = completed

    db.commit()

    # 홈으로 리디렉션
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

# 삭제
# @app.get("/delete/{todo_id}")                  #html에서 form태그로 넘겨준 값
# async def delete(request:Request, todo_id:int, task:str = Form(...), completed:bool = Form(False), db:Session = Depends(get_db)):
    
#     todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     # todo task 속성을 품에서 받아온 값으로 업데이트
#     todo.task = task
#     # todo의 completed 속성을 폼에서 받아온 completed 값으로 업데이트
#     todo.completed = completed

#     db.commit()

#     #요청이 성공적으로 처리됐으면 리디렉션
#     return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER) #성공했을 때 303

# 삭제
@app.get('/delete/{todo_id}') 
async def delete(request:Request, todo_id: int, db: Session = Depends(get_db)):

    # 데이터베이스에서 Todo 모델을 가져와, id가 todo_id와 일치하는 첫번째 항목을 가져옴
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    db.delete(todo) #삭제

    db.commit()

    # 홈으로 리디렉션
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
