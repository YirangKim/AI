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
    cleaned_text = re.sub('<.*?>', '', content)
    return cleaned_text

# 폴더를 생성합니다.
for content in contents:
    os.makedirs('./판례/{}'.format(content), exist_ok=True)

# 각 판례에 대해 상세 내용을 가져와 파일로 저장합니다.
for i in trange(len(case_list)):
    url = "https://www.law.go.kr"
    link = case_list.loc[i]['판례상세링크'].replace('HTML', 'XML')
    url += link
    response = urlopen(url).read()
    xtree = ET.fromstring(response)

    for content in contents:
        text = xtree.find(content).text
        # 내용이 존재하지 않는 경우 None 타입이 반환되기 때문에 이를 처리해줌
        if text is None:
            text = '내용없음'
        else:
            text = remove_tag(text)

        # 파일 경로를 설정합니다.
        file_path = './판례/' + content + '/' + xtree.find('판례정보일련번호').text + '.txt'
        
        # 파일을 작성합니다.
        try:
            with open(file_path, 'w', encoding='utf-8') as c:
                c.write(text)
        except Exception as e:
            print(f"Failed to write file {file_path}: {e}")

print("Data collection and file saving complete.")