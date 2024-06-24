import torch
import torchvision.transforms as transforms #이미지 변환
from torchvision.models import resnet50 #ResNet50 모델을 임포트
from PIL import Image #이미지 처리를 위한 PIL 라이브러리
import numpy as np #수치 연산을 위한 numpy를 임포트
from numpy.linalg import norm #벡터 정규화를 위한 numpy.linalg.norm를 임포트

# 이미지 임베딩을 위한 모델 로드
model = resnet50(pretrained=True) # 이미지 인식 및 분류 작업
model = torch.nn.Sequential(*(list(model.children())[:-1]))  # 마지막 분류 레이어 제거
model.eval()

# 이미지 전처리 함수
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize(256), # 이미지를 256x256 크기로 조정
        transforms.CenterCrop(224), ## 이미지를 중앙에서 224x224 크기로 자릅니다.
        transforms.ToTensor(), # 이미지를 텐서로 변환
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert('RGB') # 이미지를 열고 RGB 모드로 변환
    image = transform(image).unsqueeze(0) # 이미지를 변환하고 배치 차원을 추
    return image  # 전처리된 이미지를 반환

# 이미지 임베딩 함수
def get_image_embedding(image_path):
    image = preprocess_image(image_path) # 이미지 경로를 받아 전처리
    with torch.no_grad(): # 그래디언트 계산을 비활성
        embedding = model(image)  # 이미지를 모델에 입력하여 임베딩 벡터를 추출
    return embedding.squeeze().numpy() # 임베딩 벡터를 numpy 배열로 변환하여 반환

# 이미지 경로
dog_image_path = 'dog.jpeg'
cat_image_path = 'cat.jpeg'

# 임베딩 벡터 생성
dog_embedding = get_image_embedding(dog_image_path)
cat_embedding = get_image_embedding(cat_image_path)

# 코사인 유사도 계산
# 두 임베딩 벡터 간의 코사인 유사도를 계산
cosine_similarity = np.dot(dog_embedding, cat_embedding) / (norm(dog_embedding) * norm(cat_embedding))

# 임베딩 벡터 출력
print("Dog Embedding:")
print(dog_embedding)
print("\nCat Embedding:")
print(cat_embedding)


# 코사인 유사도 출력
print(f"Cosine Similarity between dog and cat images: {cosine_similarity}")


# 유사도 판단
if cosine_similarity >= 0.5:
    print("The images are similar.")
else:
    print("The images are not similar.")