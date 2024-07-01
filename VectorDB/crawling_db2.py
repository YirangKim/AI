import warnings
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from collections import namedtuple

# 경고 메시지 무시
warnings.filterwarnings("ignore", category=FutureWarning)

# Document 클래스 정의
Document = namedtuple('Document', ['page_content'])

# 사전 작업
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

# 1 데이터 CSV 파일에서 데이터 읽기
docs = load_csv("./crawling2024.csv")

# 문서 내용 출력 테스트
for idx, doc in enumerate(docs):
    print(f"문서 {idx + 1} 내용: {doc.page_content}")

# 데이터 준비
# 인덱스 리스트
ids = []

# 텍스트 데이터를 벡터로 변환하여 저장할 리스트
# documents 리스트는 docs 리스트에 저장된 텍스트 데이터를 벡터로 변환한 결과를 저장하는 곳
documents = []
document_texts = []

# 임베딩 모델 로드
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# 2 고유한 ID 생성 및 문서 내용 출력
# 각 문서에 대해 데이터 준비
for idx, doc in enumerate(docs):
    # 인덱스를 포함한 고유한 ID 생성
    id = f"case-{idx}"
    # 문서 내용을 가져옴
    document = doc.page_content

    # 문서 텍스트를 임베딩
    embedding = model.encode(document).tolist()

    # 각 리스트에 데이터 추가
    ids.append(id)
    documents.append(embedding)
    document_texts.append(document)

    # 고유한 ID와 문서 내용 출력
    print(f"ID: {id}\nContent: {document}\n")

# 3 ChromaDB 클라이언트 초기화 및 데이터 저장
# ChromaDB 클라이언트 초기화
client = chromadb.PersistentClient(path="./data")

# 컬렉션 생성 또는 가져오기
collection = client.get_or_create_collection(
    name="case-law",
    metadata={"hnsw:space": "cosine"}
)

# VDB 데이터 저장
collection.add(
    embeddings=documents,
    ids=ids,
    documents=document_texts  # 문서 내용도 저장
)

# 데이터베이스에 저장되었음을 출력
print("ChromaDB에 저장되었습니다.")

# 저장된 documents 확인
stored_documents = collection.query(
    query_embeddings=documents,
    n_results=len(ids),
    include=['documents']
)

for idx, (id, doc) in enumerate(zip(stored_documents['ids'][0], stored_documents['documents'][0])):
    print(f"ID {id}의 저장된 문서 내용: {doc}")

# 쿼리 텍스트 임베딩
# 단어를 쿼리 텍스트를 임베딩 모델 사용 하여 벡터로 변환
query_text = "재산분할"
query_embedding = model.encode([query_text]).tolist()

# 쿼리 텍스트의 임베딩 값 출력
print(f"쿼리 텍스트: {query_text}")

# 4 쿼리 실행 및 결과 출력
# 변환된 쿼리 벡터를 사용하여
# ChromaDB에 저장된 벡터 데이터와 비교
# 가장 유사한 3개의 결과를 반환
results = collection.query(
    query_embeddings=query_embedding,
    n_results=3,
    include=['documents']  # 문서를 포함하도록 설정
)

# 결과 객체 출력하여 구조 확인
print("쿼리 결과 전체: ")

# 각 결과의 ID와 문서 내용 출력
for idx, (id, doc) in enumerate(zip(results['ids'][0], results['documents'][0])):
    print(f"ID {id}의 문서 내용: {doc}")