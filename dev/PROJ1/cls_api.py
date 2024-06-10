import PIL.Image
from fastapi import FastAPI, File, UploadFile

# STEP 1: Import the necessary modules. # 필요한 모듈 임포트
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python.components import processors
from mediapipe.tasks.python import vision


# STEP 2: Create an ImageClassifier object. # fast api 뜨기 전에 추론객체 만들어서 사용 # classifier 라는 추론기 만듬
base_options = python.BaseOptions(model_asset_path='models\\efficientnet_lite0 (2).tflite') # model 상대 경로 복사 후, 모델 경로 지정 # 모델 경로만 있는 옵션
options = vision.ImageClassifierOptions(
    base_options=base_options, max_results=3) # model 뱉어내는 추론 결과(output)
classifier = vision.ImageClassifier.create_from_options(options)


app = FastAPI()

import io # input output
import PIL
import numpy as np

# @app.post("/files/")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}


# UploadFile
# header만 보내니까 여러 파일 받고 읽을 때, 비동기 걸어주는 형식
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # file.content_type # 확장자 걸러주는 용도로 사용해도 됨.

    byte_file = await file.read()


    # STEP 3: Load the input image. # 추론할 데이터 (이미지) 로드
    #image = mp.Image.create_from_file(IMAGE_FILENAMES[1])

    # create_from_file
    # 3-1. convert char array to binary array # 이미지로 읽을 수 있는 binary로 바꿈.
    image_bin = io.BytesIO(byte_file)
    
    # 3-2. create PIL Image from binary array # binary 를 파이썬에서 다룰 수 있는 형태로 바꿈.
    pil_img = PIL.Image.open(image_bin)

    # 3-3. Convert MP Image from PIL IMAGE
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(pil_img))


    # STEP 4: Classify the input image. # 데이터 추론 # 고정
    classification_result = classifier.classify(image)
    print(classification_result)


    # STEP 5: Process the classification result. In this case, visualize it. # 추론한 결과 보여주는 후처리단 # 프로젝트 진행한다면, json으로 변경해서 보여주기
    # top_category = classification_result.classifications[0].categories[0]
    count = 3
    results = []
    for i in range(count):              # 사진에 대한 인덱스
        category = classification_result.classifications[0].categories[i]
        results.append({"category":category.category_name, "score":category.score})
    
    return{"result":results}