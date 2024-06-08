# 1
from transformers import pipeline

# 2
question_answerer = pipeline("question-answering", model="my_awesome_qa_model")

# 3
question = "How many programming languages does BLOOM support?"
context = "BLOOM has 176 billion parameters and can generate text in 46 languages natural languages and 13 programming languages."

# 4
result = question_answerer(question=question, context=context)

# 5
print(result)