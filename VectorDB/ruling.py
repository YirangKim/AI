import pandas as pd
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from tqdm import trange
import re
import os

# 기존에 저장된 CSV 파일을 읽어옵니다.
case_list = pd.read_csv('./cases.csv')
contents = ['판시사항', '판결요지', '참조조문', '참조판례', '판례내용', '전문']

# HTML 태그를 제거하는 함수입니다.
def remove_tag(content):
    if content is None:
        return '내용없음'
    cleaned_text = re.sub('<.*?>', '', content)
    return cleaned_text

# 결과를 저장할 리스트를 초기화합니다.
rows = []

# 각 판례에 대해 상세 내용을 가져옵니다.
for i in trange(len(case_list)):
    url = "https://www.law.go.kr"
    link = case_list.loc[i]['판례상세링크'].replace('HTML', 'XML')
    url += link
    response = urlopen(url).read()
    xtree = ET.fromstring(response)

    # 각 항목에 대해 데이터를 추출합니다.
    case_data = {}
    case_data['판례일련번호'] = xtree.find('판례정보일련번호').text if xtree.find('판례정보일련번호') is not None else '내용없음'

    for content in contents:
        text = xtree.find(content).text if xtree.find(content) is not None else '내용없음'
        text = remove_tag(text)
        case_data[content] = text

    # 추출한 데이터를 리스트에 추가합니다.
    rows.append(case_data)

# 수집한 데이터를 데이터프레임으로 변환합니다.
df = pd.DataFrame(rows)

# 데이터를 CSV 파일로 저장합니다.
df.to_csv('ruling.csv', index=False, encoding='utf-8-sig')
print("Data collection complete. Saved to ruling.csv")