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

# 데이터 준비를 위한 리스트 초기화
ids = [] # 각 문서의 고유 ID를 저장할 리스트
documents = [] # 임베딩된 문서 벡터를 저장할 리스트
document_texts = [] # 원본 문서 텍스트를 저장할 리스트

# 임베딩 모델 로드 (SentenceTransformer 사용)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# 고유한 ID 생성 및 문서 내용 출력
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

# 임베딩 벡터 및 문서 ID 출력
print("임베딩 벡터 및 문서 ID 확인:")
for idx, (id, emb) in enumerate(zip(ids, documents)):
    print(f"ID: {id}\nEmbedding: {emb[:5]}...")  # 임베딩 벡터의 일부를 출력

# ChromaDB 클라이언트 초기화 및 데이터 저장
# 클라이언트 초기화
client = chromadb.PersistentClient(path="./data")
# 컬렉션 생성 또는 가져오기
collection = client.get_or_create_collection(name="case-law", metadata={"hnsw:space": "cosine"})
# 컬렉션에 데이터 추가 (임베딩된 문서 벡터, ID, 원본 문서 텍스트)
collection.add(embeddings=documents, ids=ids, documents=document_texts)

# 데이터베이스에 저장되었음을 출력
print("ChromaDB에 저장되었습니다.")
