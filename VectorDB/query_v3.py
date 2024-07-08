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
    results = collection.query(query_embeddings=[query_embedding], n_results=num_results, include=["documents", "distances", "metadatas"])
    logger.info(f"유사한 문서 검색 결과: {results}")
    return results

# 텍스트 길이를 제한하는 함수
def truncate_text(text, max_tokens):
    tokens = text.split()
    if len(tokens) > max_tokens:
        return " ".join(tokens[:max_tokens])
    return text

# 메타데이터 포맷팅 함수
def format_metadata_response(metadata_list):
    response = ""
    for metadata in metadata_list:
        response += f"**법원명**: {metadata.get('법원명', '없음')}\n"
        response += f"**사건번호**: {metadata.get('사건번호', '없음')}\n"
        response += f"**판결요지**: {metadata.get('판결요지', '없음')}\n\n"
    logger.info("메타데이터 출력 중: 법원명, 사건번호, 판결요지")
    return response

# 쿼리 라우터 정의
query_router = APIRouter()

@query_router.get("/query-v3/")
async def query_chromadb(query_text: str = Query(..., description="Query text to search similar documents"), num_results: int = Query(5, description="Number of similar documents to retrieve"), collection = Depends(get_chroma_client)):
    try:
        search_results = search_similar_documents(query_text, collection, ko_embedding, num_results=num_results)
    except Exception as e:
        logger.error(f"문서 검색 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="Error occurred while searching for documents.")
    
    similar_docs = []
    distances = []
    metadata_list = []
    for doc, dist, metadata in zip(search_results['documents'][0], search_results['distances'][0], search_results['metadatas'][0]):
        similar_docs.append(doc)
        distances.append(dist)
        metadata_list.append(metadata)
        logger.info(f"추출된 메타데이터: {metadata}")  # 디버깅용

    # 문서의 내용을 줄이기 위해 처음 몇 개의 문서만 사용
    max_docs_for_summary = 3
    truncated_docs = similar_docs[:max_docs_for_summary]

    # 각 문서의 길이를 제한
    max_tokens_per_doc = 300
    truncated_docs = [truncate_text(doc, max_tokens_per_doc) for doc in truncated_docs]

    # 첫 번째 답변: 현재 결론 유지
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
        final_response = response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"OpenAI 응답 생성 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="Error occurred while generating OpenAI response.")

    # 두 번째 답변: 법원명, 사건번호, 판결요지
    metadata_response = format_metadata_response(metadata_list)

    # 가장 유사한 판례의 메타데이터 추출
    most_similar_metadata = metadata_list[0] if metadata_list else None
    if most_similar_metadata:
        most_similar_info = {
            "법원명": most_similar_metadata.get("법원명", "없음"),
            "사건번호": most_similar_metadata.get("사건번호", "없음"),
            "판결요지": most_similar_metadata.get("판결요지", "없음")
        }
    else:
        most_similar_info = {"법원명": "없음", "사건번호": "없음", "판결요지": "없음"}

    return {
        "query": query_text,
        "results": similar_docs,
        "distances": distances,
        "answer": final_response,
        "metadata_response": metadata_response,
        "most_similar_info": most_similar_info
    }

# query_router 정의
query_router_v3 = query_router
