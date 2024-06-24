from sentence_transformers import SentenceTransformer
import chromadb

def main():
    """
    메인 함수
    """
    # 임베딩 모델 로드
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    
    # Chroma 클라이언트 설정
    client = chromadb.Client()
    
    # 텍스트 데이터
    texts = ["Hello, World!", "This is a test.", "How are you?"]
    
    # 텍스트 데이터를 임베딩으로 변환
    embeddings = model.encode(texts)
    
    # Chroma 컬렉션 생성
    collection_name = "text_embeddings"
    if collection_name not in client.list_collections():
        client.create_collection(collection_name)
    
    # 컬렉션 가져오기
    collection = client.get_collection(collection_name)
    
    # 임베딩 데이터 추가
    for i, embedding in enumerate(embeddings):
        collection.add_document(str(i), embedding)
    
    # 유사한 텍스트 검색
    query = "Hello"
    query_embedding = model.encode([query])[0]
    results = collection.query(query_embedding, top_k=1)
    
    # 검색 결과 출력
    print("Query:", query)
    for result in results:
        print("Similar Text:", texts[int(result['id'])], "Score:", result['score'])

if __name__ == "__main__":
    main()