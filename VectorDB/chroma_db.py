# 영화 데이터 로드
import pandas as pd

# CSV 파일에서 데이터 읽기
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

# 데이터 준비
# 인덱스 리스트
ids = []
# 메타데이터 리스트
doc_meta = []
# 텍스트 데이터를 벡터로 변환하여 저장할 리스트
documents = []

# 각 행에 대해 데이터 준비
for idx in range(len(filter_df)):
    item = filter_df.iloc[idx]
    # 이름을 소문자로 변환하고 공백을 '-'로 대체하여 ID 생성
    id = item['Name'].lower().replace(' ', '-')
    # 문서 내용을 이름, 줄거리, 출연진, 장르로 구성
    document = f"{item['Name']}: {item['Synopsis']} : {str(item['Cast']).strip().lower()} : {str(item['Genre']).strip().lower()}"
    # 메타데이터에 평점 추가
    meta = {
        "rating": item['Rating']
    }

    # 각 리스트에 데이터 추가
    ids.append(id)
    doc_meta.append(meta)
    documents.append(document)

# 데이터베이스에 데이터 저장
collection.add(
    documents=documents,
    metadatas=doc_meta,
    ids=ids
)

# 데이터베이스에 저장되었음을 출력
print("DB에 저장되었습니다.")

# 데이터베이스 쿼리 실행
results = collection.query(
    # query_texts는 검색하고자 하는 텍스트를 지정,  데이터베이스에서 검색 수행
    # 프롬프트 역할
    query_texts=["love drama about student"],
    # 데이터베이스에 저장된 각 문서와 쿼리 텍스트의 유사도를 계산하여
    # 가장 유사한 상위 5개의 문서가 반환
    n_results=5,
)

# 쿼리 결과 출력
print(results)