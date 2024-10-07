# face_detection_api.py

from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from face_detection import capture_face_from_webcam, set_exit_flag
from face_alignment import face_alignment

# FastAPI 앱 생성
app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# 얼굴 검출 시작 API 엔드포인트
@app.post("/start-capture/")
async def start_capture(background_tasks: BackgroundTasks):
    # 캡처 시작을 위한 종료 플래그 초기화
    set_exit_flag(False)
    # 백그라운드에서 얼굴 검출을 실행
    background_tasks.add_task(capture_face_from_webcam)
    return {"message": "웹캠 얼굴 검출 시작"}

# 얼굴 검출 중지 API 엔드포인트
@app.post("/stop-capture/")
async def stop_capture():
    # 캡처 중지를 위한 종료 플래그 설정
    set_exit_flag(True)
    return {"message": "웹캠 얼굴 검출 중지"}

# 얼굴 정렬 API 엔드포인트
@app.post("/align-face/")
async def align_face(file: UploadFile = File(...)):
    # 업로드된 파일을 저장
    image_path = f"uploaded_{file.filename}"
    with open(image_path, "wb") as f:
        f.write(file.file.read())

    # 얼굴 정렬 실행
    aligned_image_path = face_alignment(image_path)
    if aligned_image_path is None:
        return {"message": "얼굴을 찾을 수 없습니다."}

    return {"message": "얼굴 정렬 완료", "aligned_image_path": aligned_image_path}

# FastAPI 앱 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
