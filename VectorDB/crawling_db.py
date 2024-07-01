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
    df = pd.read_csv(file_path)
    docs = []
    for _, row in df.iterrows():
        text = " ".join([f"{col}: {val}" for col, val in row.items()])
        docs.append(Document(page_content=text))
    return docs

# 데이터 CSV 파일에서 데이터 읽기
docs = load_csv("/mnt/data/cases2024.csv")

# 데이터 준비
# 인덱스 리스트
ids = []
# 텍스트 데이터를 벡터로 변환하여 저장할 리스트
documents = []

# 임베딩 모델 로드
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

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

    # 고유한 ID와 문서 내용 출력
    print(f"ID: {id}\nContent: {document}\n")

# ChromaDB 클라이언트 초기화
client = chromadb.PersistentClient(path="../data")

# 컬렉션 생성 또는 가져오기
collection = client.get_or_create_collection(
    name="case-law",
    metadata={"hnsw:space": "cosine"}
)

# 데이터베이스에 데이터 저장
collection.add(
    embeddings=documents,
    ids=ids
)

# 데이터베이스에 저장되었음을 출력
print("DB에 저장되었습니다.")

# 쿼리 텍스트 임베딩
query_embedding = model.encode(["이혼"]).tolist()

# 데이터베이스 쿼리 실행
results = collection.query(
    query_embeddings=query_embedding,
    n_results=5,
)

# 쿼리 결과 출력
print("DB에 저장되었습니다.")
print(results)
