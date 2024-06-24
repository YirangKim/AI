import numpy as np
from numpy.linalg import norm

# 두 임베딩 벡터
embedding1 = [0.5421562, 0.18908182, 0.83483475, 0.0198371, -0.8182633]
embedding2 = [0.16795982, 0.4489935, 0.7201159, -0.4523684, 0.10894158]

# 코사인 유사도 계산
# 1에 가까울 수록 두 문장이 매우 유사함
# 0에 가까울 수록 유사하지 않음
# -1는 두 문장이 반대의미 
cosine_similarity = np.dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))
print(f"Cosine Similarity: {cosine_similarity}")