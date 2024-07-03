# 파일을 실행하여 CSV 파일의 데이터를 
# ChromaDB에 저장합니다.

# 라이브러리 및 모듈 임포트
import warnings
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from collections import namedtuple
from fastapi import FastAPI, UploadFile, File
import shutil

# 경고 메시지 무시
warnings.filterwarnings("ignore", category=FutureWarning)

# 1 FastAPI 인스턴스 생성
app = FastAPI()

# Document 클래스 정의
Document = namedtuple('Document', ['page_content'])

# 2 임베딩 모델 로드 (SentenceTransformer 사용)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# 3 ChromaDB 클라이언트 초기화
client = chromadb.PersistentClient(path="./data")
# 컬렉션 생성 또는 가져오기
collection = client.get_or_create_collection(name="case-law", metadata={"hnsw:space": "cosine"})

# 4 CSV 파일을 로드하고 각 행을 Document 객체로 변환하는 함수
def load_csv(file_path):
    # CSV 파일 로드
    df = pd.read_csv(file_path)
    docs = []
    # 각 행을 Document 객체로 변환
    for _, row in df.iterrows():
        # 각 컬럼의 값을 합쳐서 텍스트로 변환
        text = " ".join([f"{col}: {val}" for col, val in row.items()])
        docs.append(Document(page_content=text))
    return docs

# 5 CSV 파일 업로드 엔드포인트
@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    # 6 업로드된 파일을 서버에 저장
    file_location = f"./{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # 7 CSV 파일에서 데이터 읽기
    docs = load_csv(file_location)

    # 8 데이터 준비를 위한 리스트 초기화
    ids = []  # 각 문서의 고유 ID를 저장할 리스트
    documents = []  # 임베딩된 문서 벡터를 저장할 리스트
    document_texts = []  # 원본 문서 텍스트를 저장할 리스트]

    # 9 고유한 ID 생성 및 문서 내용 출력
    for idx, doc in enumerate(docs):
        # 인덱스를 포함한 고유한 ID 생성
        id = f"case-{idx}"
        # 문서 내용을 가져옴
        document = doc.page_content
        # 문서 텍스트를 임베딩(벡터화)
        embedding = model.encode(document).tolist()
        # 각 리스트에 데이터 추가
        ids.append(id)
        documents.append(embedding)
        document_texts.append(document)

    # 10 임베딩 벡터 및 문서 ID 출력
    for idx, (id, emb) in enumerate(zip(ids, documents)):
        print(f"ID: {id}\nEmbedding: {emb[:5]}...")  # 임베딩 벡터의 일부를 출력

    # 11 VDB 데이터 저장
    collection.add(embeddings=documents, ids=ids, documents=document_texts)

    # 12 응답 반환
    return {"message": "ChromaDB에 저장되었습니다.", "num_documents": len(docs)}

# 13 FastAPI 앱 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)