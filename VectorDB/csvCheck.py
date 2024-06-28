import pandas as pd

# CSV 파일 경로
file_path = './crawling2024.csv'

# CSV 파일 읽기
df = pd.read_csv(file_path)

# CSV 파일의 열 이름 출력
print("CSV 파일의 열 이름:", df.columns.tolist())