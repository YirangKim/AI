import pandas as pd
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from tqdm import trange
import re

# 특수 기호 제거 함수
def remove_tag_and_symbols(content):
    # 태그 제거
    cleaned_text = re.sub('<.*?>', '', content)
    # 특수 기호 제거
    cleaned_text = re.sub(r'[【】\[\]]', '', cleaned_text)
    return cleaned_text

# 크롤링한 데이터를 불러오고 특수 기호를 제거합니다.
def load_and_clean_data(filepath):
    df = pd.read_csv(filepath)
    for column in df.columns:
        df[column] = df[column].apply(lambda x: remove_tag_and_symbols(str(x)))
    return df

# 크롤링 데이터를 불러옵니다.
df_crawling_divorce = load_and_clean_data('./source/crawling_divorce_all.csv')

# 데이터 출력
print(df_crawling_divorce.head())

# 데이터를 다시 CSV 파일로 저장
df_crawling_divorce.to_csv('./source/crawling_divorce_cleaned.csv', index=False, encoding='utf-8-sig')
print("Cleaned data saved to crawling_divorce_cleaned.csv")