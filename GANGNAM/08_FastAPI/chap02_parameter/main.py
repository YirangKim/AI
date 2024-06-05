from fastapi import FastAPI

app = FastAPI()

# 경로 매개변수
# URL 경로에 들어가는 매개변수

@app.get("/users/{user_id}")
def get_user(user_id):
    return {"user_id":user_id}