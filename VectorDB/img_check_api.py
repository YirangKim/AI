from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image
import numpy as np
from numpy.linalg import norm
import io

app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 루트 경로에 대한 엔드포인트 추가
@app.get("/")
async def read_root():
    return {"message": "Welcome to the image comparison API"}

# 이미지 임베딩을 위한 모델 로드
# torchvision.models 모듈에서 제공하는 resnet50 모델
# resnet50 이미지 임베딩을 생성하고, 두 이미지의 유사도를 계산
model = resnet50(pretrained=True)
model = torch.nn.Sequential(*(list(model.children())[:-1]))
model.eval()

# 이미지 전처리 함수
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = image.convert('RGB')
    image = transform(image).unsqueeze(0)
    return image

# 이미지 임베딩 함수
def get_image_embedding(image):
    image = preprocess_image(image)
    with torch.no_grad():
        embedding = model(image)
    return embedding.squeeze().numpy()

@app.post("/compare-images")
async def compare_images(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    # 이미지 파일 읽기
    image1 = Image.open(io.BytesIO(await file1.read()))
    image2 = Image.open(io.BytesIO(await file2.read()))

    # 임베딩 벡터 생성
    embedding1 = get_image_embedding(image1)
    embedding2 = get_image_embedding(image2)

    # 코사인 유사도 계산
    cosine_similarity = np.dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))

    # 결과 응답
    similarity_result = "유사한 이미지 입니다." if cosine_similarity >= 0.5 else "일치하지 않음."
    response = {
        "cosine_similarity": float(cosine_similarity),
        "similarity_result": similarity_result,
        # "embedding1": embedding1.astype(float).tolist(),
        # "embedding2": embedding2.astype(float).tolist()
    }

    return JSONResponse(content=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("img_check_api:app", host="0.0.0.0", port=8000, reload=True)