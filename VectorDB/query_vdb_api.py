import warnings
from sentence_transformers import SentenceTransformer
import chromadb
from fastapi import FastAPI

# 경고 메시지 무시
warnings.filterwarnings("ignore", category=FutureWarning)

# FastAPI 인스턴스 생성
app = FastAPI()

# 임베딩 모델 로드  (SentenceTransformer 사용)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# ChromaDB 클라이언트 초기화
client = chromadb.PersistentClient(path="./data")
# 컬렉션 생성 또는 가져오기
collection = client.get_or_create_collection(name="case-law", metadata={"hnsw:space": "cosine"})

# 쿼리 엔드포인트 정의
@app.get("/query/")
async def query_chromadb(query_text: str):
    # 쿼리 텍스트 임베딩(벡터화)
    query_embedding = model.encode([query_text]).tolist()

    # VDB ChromaDB에 쿼리 실행 및 결과 가져오기
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3,
        include=['documents']  # 문서를 포함하도록 설정
    )

    # 결과 객체 출력하여 구조 확인
    response = []
    for idx, (id, doc) in enumerate(zip(results['ids'][0], results['documents'][0])):
        response.append({"id": id, "document": doc})

    # 쿼리 텍스트와 결과 반환
    return {"query": query_text, "results": response}

# FastAPI 앱 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
