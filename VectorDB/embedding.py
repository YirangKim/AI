from sentence_transformers import SentenceTransformer

# SentenceTransformer는 문장 임베딩(sentence embedding)을 생성 Python 라이브러리
# 문장이나 텍스트 조각을 고차원 벡터로 변환하는 기능을 제공
# SentenceTransformer는 문장을 고차원 벡터로 변환하여 의미적으로 유사한 문장은 가까운 벡터로, 
# 그렇지 않은 문장은 먼 벡터로 표현

# SentenceTransformer 모델 로드
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# 예제 문장
sentences = ["Hello, how are you?", "I am fine, thank you.", "What about you?"]

# 문장 임베딩 생성
embeddings = model.encode(sentences)

# 결과 출력
for sentence, embedding in zip(sentences, embeddings):
    print(f"Sentence: {sentence}")
    print(f"Embedding: {embedding[:5]}...")  # 벡터의 일부만 출력
    print()