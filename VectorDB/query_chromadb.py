# 파일을 실행하여 쿼리 텍스트를 벡터로 변환하고, 
# ChromaDB에서 유사한 문서를 검색합니다.

import warnings
from sentence_transformers import SentenceTransformer
import chromadb

# 경고 메시지 무시
warnings.filterwarnings("ignore", category=FutureWarning)

# 임베딩 모델 로드
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# ChromaDB 클라이언트 초기화
client = chromadb.PersistentClient(path="./data")
collection = client.get_or_create_collection(name="case-law", metadata={"hnsw:space": "cosine"})

# 쿼리 텍스트 임베딩
query_text = "재산분할"
query_embedding = model.encode([query_text]).tolist()

# 쿼리 텍스트의 임베딩 값 출력
print(f"쿼리 텍스트: {query_text}")

# 쿼리 실행 및 결과 출력
results = collection.query(
    query_embeddings=query_embedding,
    n_results=3,
    include=['documents']  # 문서를 포함하도록 설정
)

# 결과 객체 출력하여 구조 확인
print("쿼리 결과 전체: ")
for idx, (id, doc) in enumerate(zip(results['ids'][0], results['documents'][0])):
    print(f"ID {id}의 문서 내용: {doc}")