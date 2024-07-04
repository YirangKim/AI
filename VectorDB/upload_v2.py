import warnings
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import chromadb
from fastapi import APIRouter, UploadFile, File
import shutil

# 경고 메시지 무시
warnings.filterwarnings("ignore", category=FutureWarning)

# 임베딩 모델 로드 (SentenceTransformer 사용)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# ChromaDB 클라이언트 초기화
client = chromadb.PersistentClient(path="./data")

# 컬렉션 생성 또는 가져오기
collection = client.get_or_create_collection(name="case-law", metadata={"hnsw:space": "cosine"})

# 텍스트 길이 계산 함수
def tiktoken_len(text):
    return len(text)

# 4. CSV 파일 로드 및 텍스트 청크 생성 함수 정의
def load_csv(file_path):
    try:
        # 잘못된 행 건너뛰기
        df = pd.read_csv(file_path, on_bad_lines='skip')
        docs = []
        for _, row in df.iterrows():
            # 5-1 판례내용과 판례일련번호를 결합하여 text에 저장
            text = row['판례내용']
            metadata = {
                "판례일련번호": row["판례일련번호"],
                # "사건명": row["사건명"],
                # "사건번호": row["사건번호"],
                # "선고일자": row["선고일자"],
                # "법원명": row["법원명"],
                # "사건종류명": row["사건종류명"],
                # "사건종류코드": row["사건종류코드"],
                # "판결유형": row["판결유형"],
                # "선고": row["선고"],
                # "판시사항": row["판시사항"],
                # "판결요지": row["판결요지"],
                # "참조조문": row["참조조문"],
                # "참조판례": row["참조판례"],
            }
            docs.append(Document(page_content=text, metadata=metadata))
        print("CSV 파일 로드 성공")
        return docs
    except Exception as e:
        print(f"CSV 파일 로드 실패: {e}")
        return None

# 6. 텍스트 청크 생성 함수 정의
def get_text_chunks(documents):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,   # 6-1 원하는 청크 크기
            chunk_overlap=100, # 6-2 원하는 청크 중첩
            length_function=tiktoken_len
        )
        chunks = text_splitter.split_documents(documents)
        print("텍스트 청크 처리 성공")
        return chunks
    except Exception as e:
        print(f"텍스트 청크 처리 실패: {e}")
        return None

# 7. CSV 파일 업로드 라우터 정의
router = APIRouter()

@router.post("/upload-csv-v2/")
async def upload_csv(file: UploadFile = File(...)):
    file_location = f"./{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # 7-1 CSV 파일 로드
    docs = load_csv(file_location)
    if docs is None:
        return {"message": "CSV 파일 로드 실패"}

    chunked_docs = get_text_chunks(docs)
    if chunked_docs is None:
        return {"message": "텍스트 청크 처리 실패"}

    texts = [doc.page_content for doc in chunked_docs]
    metadatas = [doc.metadata for doc in chunked_docs]

    # 7-3 텍스트 임베딩 생성
    print("임베딩 모델 함수 호출 시작...")
    try:
        embeddings = model.encode(texts, convert_to_tensor=False)
        if embeddings is None or len(embeddings) == 0:
            raise ValueError("임베딩 생성 실패")
        print("임베딩 모델 함수 호출 완료, 생성된 임베딩 수:", len(embeddings))
    except Exception as e:
        print(f"임베딩 모델 함수 호출 실패: {e}")
        return {"message": "임베딩 생성 실패"}

    # 7-4 Chroma 벡터 데이터베이스에 문서 추가
    try:
        print("벡터 DB 저장중입니다...")
        ids = [f"case-{i}" for i in range(len(texts))]
        collection.add(
            embeddings=embeddings,
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        print("벡터 데이터베이스에 저장 성공")
    except Exception as e:
        print(f"벡터 데이터베이스에 저장 실패: {e}")
        return {"message": "벡터 데이터베이스에 저장 실패"}

    return {"message": "ChromaDB에 저장되었습니다.", "num_documents": len(chunked_docs)}

# 8. upload_router 정의
upload_router_v2 = router
