from fastapi import FastAPI, File, UploadFile

# STEP 1: 모듈 가져오기 Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python.components import processors
from mediapipe.tasks.python import vision

# fast API 뜨기전에 추론기 미리 만듬
# STEP 2: 추론기 만듬 Create an ImageClassifier object. 
base_options = python.BaseOptions(model_asset_path='models\\efficientnet_lite0.tflite') # 1) 경로수정
options = vision.ImageClassifierOptions(
    base_options=base_options, max_results=1) # 2) 결과값1 
classifier = vision.ImageClassifier.create_from_options(options) #classifier 추론기

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):

    byte_file = await file.read() # 파일 복사

    # STEP 3: 추론 할 데이터 가져오기 Load the input image. WEB
    image = mp.Image.create_from_file(IMAGE_FILENAMES[1])

    # STEP 4: 추론 Classify the input image. 
    classification_result = classifier.classify(image)
    print("")
    print(classification_result)

    # STEP 5: 후 처리 출력  Process the classification result. WEB
    top_category = classification_result.classifications[0].categories[0]
    result = (f"{top_category.category_name} - ({top_category.score:.2f})") #스트링 포맷

    print(result)
    
    return {"filename": len(byte_file)}