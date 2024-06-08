# STEP 1. import modules
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification

# STEP 2. create infernece instance 요약 task
classifier = pipeline("sentiment-analysis", model="snunlp/KR-FinBert-SC")

# STEP 3. prepare input data
text = "대통령 당선"

# STEP 4. infrence
result = classifier(text)

# STEP 5. visuallize
print(result)