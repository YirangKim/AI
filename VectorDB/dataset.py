import pandas as pd
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from tqdm import trange

# OC 아이디를 설정합니다.
OC_ID = "cacao5424"
base_url = f"https://www.law.go.kr/DRF/lawSearch.do?OC={OC_ID}&target=prec&type=XML&query=대법원"

# 첫 번째 페이지의 데이터를 가져옵니다.
url = f"{base_url}&page=1"
response = urlopen(url).read()
xtree = ET.fromstring(response)

# 전체 건수를 가져옵니다.
totalCnt = int(xtree.find('totalCnt').text)

# 페이지를 반복하면서 데이터를 수집합니다.
page = 1
rows = []
for i in trange((totalCnt // 20) + 1):  # 총 페이지 수만큼 반복
    try:
        items = xtree[5:]  # 6번째 요소부터 데이터 항목
    except Exception as e:
        print(f"Error on page {page}: {e}")
        break
        
    for node in items:
        판례일련번호 = node.find('판례일련번호').text if node.find('판례일련번호') is not None else None
        사건명 = node.find('사건명').text if node.find('사건명') is not None else None
        사건번호 = node.find('사건번호').text if node.find('사건번호') is not None else None
        선고일자 = node.find('선고일자').text if node.find('선고일자') is not None else None
        법원명 = node.find('법원명').text if node.find('법원명') is not None else None
        사건종류명 = node.find('사건종류명').text if node.find('사건종류명') is not None else None
        사건종류코드 = node.find('사건종류코드').text if node.find('사건종류코드') is not None else None
        판결유형 = node.find('판결유형').text if node.find('판결유형') is not None else None
        선고 = node.find('선고').text if node.find('선고') is not None else None
        판례상세링크 = node.find('판례상세링크').text if node.find('판례상세링크') is not None else None

        rows.append({'판례일련번호': 판례일련번호,
                     '사건명': 사건명,
                     '사건번호': 사건번호,
                     '선고일자': 선고일자,
                     '법원명': 법원명,
                     '사건종류명': 사건종류명,
                     '사건종류코드': 사건종류코드,
                     '판결유형': 판결유형,
                     '선고': 선고,
                     '판례상세링크': 판례상세링크})
    
    # 다음 페이지로 이동합니다.
    page += 1
    url = f"{base_url}&page={page}"
    response = urlopen(url).read()
    xtree = ET.fromstring(response)

# 수집한 데이터를 데이터프레임으로 변환합니다.
df = pd.DataFrame(rows)

# 데이터를 CSV 파일로 저장합니다.
df.to_csv('law_cases.csv', index=False, encoding='utf-8-sig')
print("Data collection complete. Saved to law_cases.csv")

# 데이터프레임을 추가로 저장합니다.
cases = pd.DataFrame(rows)
cases.to_csv('./cases.csv', index=False)
print("Data collection complete. Saved to cases.csv")