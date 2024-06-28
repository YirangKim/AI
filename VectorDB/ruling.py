import pandas as pd
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from tqdm import trange

# CSV 파일을 불러옵니다.
case_list = pd.read_csv('./cases2024.csv')

# 샘플로 하나의 URL을 가져와서 데이터 확인
sample_url = "https://www.law.go.kr" + case_list.loc[0]['판례상세링크'].replace('HTML', 'XML')
response = urlopen(sample_url).read()
xtree = ET.fromstring(response)

# XML의 구조를 확인하기 위해 요소를 출력합니다.
for elem in xtree.iter():
    print(elem)