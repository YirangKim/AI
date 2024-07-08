import warnings
from fastapi import APIRouter, HTTPException, Query, Depends
import openai
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
import logging
from dotenv import load_dotenv
import os

# 경고 메시지 무시
warnings.filterwarnings("ignore", category=FutureWarning)

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# .env 파일의 환경 변수를 로드합니다.
# OpenAI API 키 설정
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# 텍스트 임베딩
model_name = "paraphrase-MiniLM-L6-v2"  # 모델을 동일하게 설정
encode_kwargs = {'normalize_embeddings': True}
ko_embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    encode_kwargs=encode_kwargs
)

# ChromaDB 클라이언트 및 컬렉션 초기화 함수
def get_chroma_client():
    client = chromadb.PersistentClient(path="./data")
    collection = client.get_or_create_collection(name="case-law", metadata={"hnsw:space": "cosine"})
    return collection

# 쿼리를 벡터화하여 유사한 문서 검색 함수 정의
def search_similar_documents(query, collection, ko_embedding, num_results=5):
    query_embedding = ko_embedding.embed_query(query)
    logger.info(f"쿼리 임베딩 생성 완료: {query_embedding}")
    results = collection.query(query_embeddings=[query_embedding], n_results=num_results, include=["documents", "distances"])
    logger.info(f"유사한 문서 검색 결과: {results}")
    return results

# 텍스트 길이를 제한하는 함수
def truncate_text(text, max_tokens):
    tokens = text.split()
    if len(tokens) > max_tokens:
        return " ".join(tokens[:max_tokens])
    return text

# 쿼리 라우터 정의
router = APIRouter()

@router.get("/query-v2/")
async def query_chromadb(query_text: str = Query(..., description="Query text to search similar documents"), num_results: int = Query(5, description="Number of similar documents to retrieve"), collection = Depends(get_chroma_client)):
    try:
        search_results = search_similar_documents(query_text, collection, ko_embedding, num_results=num_results)
    except Exception as e:
        logger.error(f"문서 검색 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="Error occurred while searching for documents.")
    
    similar_docs = []
    distances = []
    for doc, dist in zip(search_results['documents'][0], search_results['distances'][0]):
        similar_docs.append(doc)
        distances.append(dist)

    # 문서의 내용을 줄이기 위해 처음 몇 개의 문서만 사용
    max_docs_for_summary = 10
    truncated_docs = similar_docs[:max_docs_for_summary]

    # 각 문서의 길이를 제한
    max_tokens_per_doc = 300
    truncated_docs = [truncate_text(doc, max_tokens_per_doc) for doc in truncated_docs]

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"The user asked: {truncate_text(query_text, 100)}\n\nHere are some similar documents:\n" + "\n".join(truncated_docs) + "\n\nBased on the above documents, provide a natural and informative response to the user's question in Korean."}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500
        )
        logger.info(f"OpenAI 응답 생성 완료: {response}")
    except Exception as e:
        logger.error(f"OpenAI 응답 생성 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="Error occurred while generating OpenAI response.")

    return {"query": query_text, "results": similar_docs, "distances": distances, "answer": response['choices'][0]['message']['content']}

# query_router 정의
query_router_v2 = router
