import warnings
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import chromadb
from fastapi import APIRouter, UploadFile, File
import shutil
import logging

# 경고 메시지 무시
warnings.filterwarnings("ignore", category=FutureWarning)

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 임베딩 모델 로드 (SentenceTransformer 사용)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# ChromaDB 클라이언트 초기화
client = chromadb.PersistentClient(path="./data")

# 컬렉션 생성 또는 가져오기
collection = client.get_or_create_collection(name="case-law", metadata={"hnsw:space": "cosine"})

# 텍스트 길이 계산 함수
def tiktoken_len(text):
    return len(text)

# CSV 파일 로드 및 텍스트 청크 생성 함수 정의
def load_csv(file_path):
    try:
        # 잘못된 행 건너뛰기
        df = pd.read_csv(file_path, on_bad_lines='skip')
        docs = []
        for _, row in df.iterrows():
            # 판례내용과 메타데이터 저장
            text = row['판례내용']
            metadata = {
                "판례일련번호": row["판례일련번호"],
                "사건명": row.get("사건명", "없음"),
                "사건번호": row.get("사건번호", "없음"),
                "법원명": row.get("법원명", "없음"),
                "판결요지": row.get("판결요지", "없음") 
            }
            docs.append(Document(page_content=text, metadata=metadata))
        logger.info("CSV 파일 로드 성공")
        return docs
    except Exception as e:
        logger.error(f"CSV 파일 로드 실패: {e}")
        return None

# 텍스트 청크 생성 함수 정의
def get_text_chunks(documents):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=tiktoken_len
        )
        chunks = text_splitter.split_documents(documents)
        logger.info("텍스트 청크 처리 성공")
        return chunks
    except Exception as e:
        logger.error(f"텍스트 청크 처리 실패: {e}")
        return None

# CSV 파일 업로드 라우터 정의
router = APIRouter()

@router.post("/upload-csv-v2/")
async def upload_csv(file: UploadFile = File(...)):
    file_location = f"./{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # CSV 파일 로드
    docs = load_csv(file_location)
    if docs is None:
        return {"message": "CSV 파일 로드 실패"}

    chunked_docs = get_text_chunks(docs)
    if chunked_docs is None:
        return {"message": "텍스트 청크 처리 실패"}

    texts = [doc.page_content for doc in chunked_docs]
    metadatas = [doc.metadata for doc in chunked_docs]

    # 텍스트 임베딩 생성
    logger.info("임베딩 모델 함수 호출 시작...")
    try:
        embeddings = model.encode(texts, convert_to_tensor=False)
        if embeddings is None or len(embeddings) == 0:
            raise ValueError("임베딩 생성 실패")
        logger.info("임베딩 모델 함수 호출 완료, 생성된 임베딩 수:", len(embeddings))
    except Exception as e:
        logger.error(f"임베딩 모델 함수 호출 실패: {e}")
        return {"message": "임베딩 생성 실패"}

    # Chroma 벡터 데이터베이스에 문서 추가
    try:
        logger.info("벡터 DB 저장중입니다...")
        ids = [f"case-{i}" for i in range(len(texts))]
        collection.add(
            embeddings=embeddings,
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        logger.info("벡터 데이터베이스에 저장 성공")
    except Exception as e:
        logger.error(f"벡터 데이터베이스에 저장 실패: {e}")
        return {"message": "벡터 데이터베이스에 저장 실패"}

    return {"message": "ChromaDB에 저장되었습니다.", "num_documents": len(chunked_docs)}

# upload_router 정의
upload_router_v2 = router
