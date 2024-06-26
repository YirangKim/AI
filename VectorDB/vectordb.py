# 영화 데이터 로드
import pandas as pd
from sentence_transformers import SentenceTransformer

# 데이터 CSV 파일에서 데이터 읽기
df = pd.read_csv("./kdrama.csv")

# 불필요한 열 제거
filter_df = df.drop(["Aired Date", "Aired On", "Duration", "Content Rating", "Production companies", "Rank"], axis=1)

# ChromaDB 클라이언트 초기화
import chromadb
client = chromadb.PersistentClient(path="../data")

# 컬렉션 생성 또는 가져오기
collection = client.get_or_create_collection(
    name="k-drama",
    metadata={"hnsw:space": "cosine"}
)

# 임베딩 모델 로드
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# 데이터 준비
# 인덱스 리스트
ids = []
# 텍스트 데이터를 벡터로 변환하여 저장할 리스트
documents = []

# 각 행에 대해 데이터 준비
for idx in range(len(filter_df)):
    item = filter_df.iloc[idx]
    # 이름을 소문자로 변환하고 공백을 '-'로 대체하여 ID 생성
    id = item['Name'].lower().replace(' ', '-')
    # 문서 내용을 이름, 줄거리, 출연진, 장르로 구성
    document = f"{item['Name']}: {item['Synopsis']} : {str(item['Cast']).strip().lower()} : {str(item['Genre']).strip().lower()}"

    # 문서 텍스트를 임베딩
    embedding = model.encode(document).tolist()

    # 각 리스트에 데이터 추가
    ids.append(id)
    documents.append(embedding)

# 데이터베이스에 데이터 저장
collection.add(
    embeddings=documents,
    ids=ids
)

# 데이터베이스에 저장되었음을 출력
print("DB에 저장되었습니다.")

# 쿼리 텍스트 임베딩
query_embedding = model.encode(["love drama about student"]).tolist()

# 데이터베이스 쿼리 실행
results = collection.query(
    query_embeddings=query_embedding,
    n_results=5,
)

# 쿼리 결과 출력
print(results)