import warnings
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from collections import namedtuple
from fastapi import FastAPI, UploadFile, File
import shutil

# 경고 메시지 무시
warnings.filterwarnings("ignore", category=FutureWarning)

# FastAPI 인스턴스 생성
app = FastAPI()

# Document 클래스 정의
Document = namedtuple('Document', ['page_content'])

# 임베딩 모델 로드
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# ChromaDB 클라이언트 초기화
client = chromadb.PersistentClient(path="./data")
collection = client.get_or_create_collection(name="case-law", metadata={"hnsw:space": "cosine"})

# CSV 파일 로드 및 변환 
def load_csv(file_path):
    df = pd.read_csv(file_path)
    docs = []
    for _, row in df.iterrows():
        text = " ".join([f"{col}: {val}" for col, val in row.items()])
        docs.append(Document(page_content=text))
    return docs

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    # 파일 저장
    file_location = f"./{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # CSV 파일에서 데이터 읽기
    docs = load_csv(file_location)

    # 데이터 준비
    ids = []
    documents = []
    document_texts = []

    # 고유한 ID 생성 및 문서 내용 출력
    for idx, doc in enumerate(docs):
        id = f"case-{idx}"
        document = doc.page_content
        embedding = model.encode(document).tolist()
        ids.append(id)
        documents.append(embedding)
        document_texts.append(document)

    # 임베딩 벡터 및 문서 ID 출력
    for idx, (id, emb) in enumerate(zip(ids, documents)):
        print(f"ID: {id}\nEmbedding: {emb[:5]}...")  # 임베딩 벡터의 일부를 출력

    # VDB 데이터 저장
    collection.add(embeddings=documents, ids=ids, documents=document_texts)

    return {"message": "ChromaDB에 저장되었습니다.", "num_documents": len(docs)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)