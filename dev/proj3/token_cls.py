# STEP 1: 모듈 가져오기
# STEP 2: 추론기 만듬
# STEP 3: 데이터 가져오기
# STEP 4: 추론
# STEP 5: 후처리 출력

# STEP 1. import modules
from transformers import pipeline

# STEP 2. create infernece instance
classifier = pipeline("ner", model="stevhliu/my_awesome_wnut_model")

# STEP 3. prepare input dat
text = "The Golden State Warriors are an American professional basketball team based in San Francisco."

# STEP 4. infrence
result = classifier(text)

# STEP 5. visuallize
print(result)