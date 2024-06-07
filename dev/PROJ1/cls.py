IMAGE_FILENAMES = ['burger.jpg', 'cat.jpg']

import cv2
import math

DESIRED_HEIGHT = 480
DESIRED_WIDTH = 480

# def resize_and_show(image):
#   h, w = image.shape[:2]
#   if h < w:
#     img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
#   else:
#     img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
#   #cv2_imshow(img)
#   cv2.imshow("test", img)
#   cv2.waitKey(0)


# # Preview the images.

# images = {name: cv2.imread(name) for name in IMAGE_FILENAMES}
# for name, image in images.items():
#   print(name)
#   resize_and_show(image)




# STEP 1: 모듈 가져오기 Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python.components import processors
from mediapipe.tasks.python import vision

# STEP 2: 추론기 만듬 Create an ImageClassifier object. 
base_options = python.BaseOptions(model_asset_path='models\\efficientnet_lite0.tflite') # 1) 경로수정
options = vision.ImageClassifierOptions(
    base_options=base_options, max_results=1) # 2) 결과값1 
classifier = vision.ImageClassifier.create_from_options(options) #classifier 추론기

# STEP 3: 추론 할 데이터 가져오기 Load the input image. 
image = mp.Image.create_from_file(IMAGE_FILENAMES[1])

# STEP 4: 추론 Classify the input image. 
classification_result = classifier.classify(image)
print("")
print(classification_result)

# STEP 5: 후 처리 출력  Process the classification result. In this case, visualize it. 
top_category = classification_result.classifications[0].categories[0]
result = (f"{top_category.category_name} - ({top_category.score:.2f})") #스트링 포맷

print(result)
#display_batch_of_images(images, predictions)