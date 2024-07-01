# 파일을 실행하여 CSV 파일의 데이터를 
# ChromaDB에 저장합니다.

import warnings
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from collections import namedtuple

# 경고 메시지 무시
warnings.filterwarnings("ignore", category=FutureWarning)

# Document 클래스 정의
Document = namedtuple('Document', ['page_content'])

# CSV 파일 로드 및 변환 
def load_csv(file_path):
    # CSV 파일 로드
    df = pd.read_csv(file_path)
    docs = []
    # 각 행을 Document 객체로 변환
    for _, row in df.iterrows():
        text = " ".join([f"{col}: {val}" for col, val in row.items()])
        docs.append(Document(page_content=text))
    return docs

# 데이터 CSV 파일에서 데이터 읽기
docs = load_csv("./crawling2024.csv")

# 데이터 준비
ids = []
documents = []
document_texts = []

# 임베딩 모델 로드
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# 고유한 ID 생성 및 문서 내용 출력
for idx, doc in enumerate(docs):
    id = f"case-{idx}"
    document = doc.page_content
    embedding = model.encode(document).tolist()
    ids.append(id)
    documents.append(embedding)
    document_texts.append(document)

# 임베딩 벡터 및 문서 ID 출력
print("임베딩 벡터 및 문서 ID 확인:")
for idx, (id, emb) in enumerate(zip(ids, documents)):
    print(f"ID: {id}\nEmbedding: {emb[:5]}...")  # 임베딩 벡터의 일부를 출력

# ChromaDB 클라이언트 초기화 및 데이터 저장
client = chromadb.PersistentClient(path="./data")
collection = client.get_or_create_collection(name="case-law", metadata={"hnsw:space": "cosine"})
collection.add(embeddings=documents, ids=ids, documents=document_texts)

# 데이터베이스에 저장되었음을 출력
print("ChromaDB에 저장되었습니다.")
