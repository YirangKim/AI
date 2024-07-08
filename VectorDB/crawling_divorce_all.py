import pandas as pd
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from tqdm import trange
import re

# CSV 파일을 불러옵니다.
case_list = pd.read_csv('./source/divorce_cases.csv')
contents = ['판시사항', '판결요지', '참조조문', '참조판례', '판례내용']

def remove_tag(content):
    cleaned_text = re.sub('<.*?>', '', content)
    cleaned_text = re.sub(r'[【】]', '', cleaned_text)  # 특수 기호 제거
    return cleaned_text

rows = []

for i in trange(len(case_list)):
    url = "https://www.law.go.kr"
    link = case_list.loc[i]['판례상세링크'].replace('HTML', 'XML')
    url += link
    response = urlopen(url).read()
    xtree = ET.fromstring(response)

    판례일련번호 = case_list.loc[i]['판례일련번호']
    사건명 = case_list.loc[i]['사건명']
    사건번호 = case_list.loc[i]['사건번호']
    선고일자 = case_list.loc[i]['선고일자']
    법원명 = case_list.loc[i]['법원명']
    사건종류명 = case_list.loc[i]['사건종류명']
    사건종류코드 = case_list.loc[i]['사건종류코드']
    판결유형 = case_list.loc[i]['판결유형']
    선고 = case_list.loc[i]['선고']

    판시사항, 판결요지, 참조조문, 참조판례, 판례내용 = "", "", "", "", ""

    for content in contents:
        element = xtree.find(content)
        if element is not None:
            text = element.text
            if text is None:
                text = '내용없음'
            else:
                text = remove_tag(text)
        else:
            text = '내용없음'

        if content == '판시사항':
            판시사항 = text
        elif content == '판결요지':
            판결요지 = text
        elif content == '참조조문':
            참조조문 = text
        elif content == '참조판례':
            참조판례 = text
        elif content == '판례내용':
            판례내용 = text

    rows.append({'판례일련번호': 판례일련번호,
                 '사건명': 사건명,
                 '사건번호': 사건번호,
                 '선고일자': 선고일자,
                 '법원명': 법원명,
                 '사건종류명': 사건종류명,
                 '사건종류코드': 사건종류코드,
                 '판결유형': 판결유형,
                 '선고': 선고,
                 '판시사항': 판시사항,
                 '판결요지': 판결요지,
                 '참조조문': 참조조문,
                 '참조판례': 참조판례,
                 '판례내용': 판례내용})

# 수집한 데이터를 데이터프레임으로 변환합니다.
df_crawling_divorce = pd.DataFrame(rows, columns=['판례일련번호', '사건명', '사건번호', '선고일자', '법원명', '사건종류명', '사건종류코드', '판결유형', '선고', '판시사항', '판결요지', '참조조문', '참조판례', '판례내용'])

# 필터링된 데이터를 CSV 파일로 저장
df_crawling_divorce.to_csv('crawling_divorce_all.csv', index=False, encoding='utf-8-sig')
print("Data collection complete. Saved to crawling_divorce_all.csv")

# 데이터프레임 출력
print(df_crawling_divorce.head())
