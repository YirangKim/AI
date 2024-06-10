# 1 모듈 가져오기
from transformers import pipeline
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io

# 2 추론기 만듬 (PyTorch 기반)
captioner = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning", framework="pt")

# 3 FastAPI 애플리케이션 생성
app = FastAPI()

# 4 이미지 캡션 엔드포인트 구현
@app.post("/pose_text/")
async def get_caption(file: UploadFile):

        # 업로드된 이미지 파일 읽기
        image_bytes = await file.read()
        
        # 이미지 파일을 PIL 이미지로 변환
        image = Image.open(io.BytesIO(image_bytes))

        # 5 추론
        result = captioner(image)

        # 6 후 처리 및 결과 반환
        print(result)
        return JSONResponse(content=result)