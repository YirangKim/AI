# STEP 1: 모듈 가져오기
# STEP 2: 추론기 만듬
# STEP 3: 데이터 가져오기
# STEP 4: 추론
# STEP 5: 후처리 출력

# STEP 1. import modules
from transformers import pipeline

# STEP 2. create infernece instance
summarizer = pipeline("summarization", model="eenzeenee/t5-base-korean-summarization")

# STEP 3. prepare input data
text = "오늘은 비오는 토요일. 특강 수업을 듣고 있다"

# STEP 4. infrence
result = summarizer(text)

# STEP 5. visuallize
print(result)