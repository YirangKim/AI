#query
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

# OpenAI API 키 설정
openai.api_key = ""

# 텍스트 임베딩
model_name = "paraphrase-MiniLM-L6-v2"
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

@query_router.get("/query-v4/")
async def query_chromadb(query_text: str = Query(..., description="유사한 문서를 검색할 쿼리 텍스트"), num_results: int = Query(5, description="검색할 유사 문서의 개수"), collection = Depends(get_chroma_client)):
    try:
        search_results = search_similar_documents(query_text, collection, ko_embedding, num_results=num_results)
    except Exception as e:
        logger.error(f"문서 검색 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="문서 검색 중 오류가 발생했습니다.")
    
    similar_docs = []
    distances = []
    metadata_list = []
    for doc, dist, metadata in zip(search_results['documents'][0], search_results['distances'][0], search_results['metadatas'][0]):
        similar_docs.append(doc)
        distances.append(dist)
        metadata_list.append(metadata)
        logger.info(f"추출된 메타데이터: {metadata}")  # 디버깅용

    if not similar_docs:
        return {
            "query": query_text,
            "results": [],
            "distances": [],
            "answer": "유사한 문서가 없습니다.",
            "most_similar_info": []
        }

    # 문서의 내용을 줄이기 위해 처음 몇 개의 문서만 사용
    max_docs_for_summary = 3
    truncated_docs = similar_docs[:max_docs_for_summary]

    # 각 문서의 길이를 제한
    max_tokens_per_doc = 300
    truncated_docs = [truncate_text(doc, max_tokens_per_doc) for doc in truncated_docs]

    # 질문 타입 분류를 위한 프롬프트
    classification_prompt = f'''
    # Role
    You are a professional and accurate text classifier machine and translator machine.

    # Output Format
    {{
    "question": "{query_text}",
    "question_type": "{{{{question_type}}}}"
    }}

    # Task
    - The ultimate goal is to classify the type of the question by referring the question.
    - To do that, Let's think step by step.
    - For information about question types, see "##Question Types".
    - This is very important to my career. Please do your best.

    ## Step 1
    - You will be provided with a '{query_text}' question delimited by triple quotes.

    ## Step 2
    - Store the question content in the variable "question".

    ## Step 3
    - Classify the question type by referring the "question" extracted from the "Step 2" for the '{query_text}'.

    # Policy
    - Do not write any content other than the json string, because the resulting json string must be used directly in the script.
    - Do not write unnecessary explanations or instructions.
    - You must select one of the question types above.
    - If there is insufficient information to classify, select "ETC review"

    # Context
    ## Question Types and Examples
    1. 양육비 질문 - Questions related to non-payment of child support
       Example: "양육비를 지급하지 않는 남편에게 어떻게 대처해야 하나요?"
    2. 폭행 - Assault cases
       Example: "남편이 저를 폭행합니다. 어떻게 해야 하나요?"
    3. 재산분할 - Division of joint property
       Example: "이혼 시 공동 재산을 어떻게 나눌 수 있나요?"
    4. 위자료 - Compensation for mental suffering
       Example: "유책 배우자에게 위자료를 청구할 수 있나요?"
    5. 생활비 - Non-payment of living expenses
       Example: "생활비를 주지 않는데 이혼할 수 있을까요?"
    6. 별거 - Family breakdown due to separation
       Example: "별거 중인데 이혼을 원합니다. 어떻게 해야 하나요?"
    7. 부정행위 - Family breakdown due to adultery
       Example: "남편의 부정행위로 이혼을 원합니다. 절차가 어떻게 되나요?"
    8. 유책배우자 - Divorce claims from at-fault spouse
       Example: "유책 배우자가 이혼을 요구할 수 있나요?"
    9. ETC review - Questions not covered by the above categories.
       Example: "이혼 후 양육권은 어떻게 결정되나요?"
    '''

    classification_messages = [
        {"role": "system", "content": "You are a professional and accurate text classifier machine and translator machine."},
        {"role": "user", "content": classification_prompt}
    ]

    try:
        classification_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=classification_messages,
            max_tokens=500
        )
        logger.info(f"OpenAI 질문 분류 응답 생성 완료: {classification_response}")
        classified_question = classification_response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"OpenAI 질문 분류 응답 생성 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="질문 분류 중 오류가 발생했습니다.")

    # 분류된 질문 타입에 따라 적절한 답변 생성
    response_prompt = f'''
    # Role
    You are a helpful assistant.

    # Task
    Provide a detailed and informative answer to the following question based on its type:

    ## Question
    "{query_text}"

    ## Classified Question Type
    "{classified_question['question_type']}"

    # Response
    '''

    response_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": response_prompt}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=response_messages,
            max_tokens=500
        )
        logger.info(f"OpenAI 응답 생성 완료: {response}")
        final_response = response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"OpenAI 응답 생성 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="OpenAI 응답 생성 중 오류가 발생했습니다.")

    # 가장 유사한 판례의 메타데이터 추출 (최대 2개)
    most_similar_metadata = metadata_list[:2] if metadata_list else []
    most_similar_info = [
        {
            "법원명": metadata.get("법원명", "없음"),
            "사건번호": metadata.get("사건번호", "없음"),
            "판결요지": metadata.get("판결요지", "없음")
        }
        for metadata in most_similar_metadata
    ]

    return {
    "query": query_text,
    "results": similar_docs,
    "distances": distances,
    "answer": final_response,
    "most_similar_info": most_similar_info,
    "question_classification": classified_question  # 분류된 질문 타입 추가
}

# query_router 정의
query_router_v4 = query_router