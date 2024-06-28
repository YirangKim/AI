import requests
from bs4 import BeautifulSoup
import pandas as pd

# CSV 파일 로드
cases_df = pd.read_csv('cases.csv')

# 판례상세링크 컬럼 추출
detailed_links = cases_df['판례상세링크']

# Base URL
base_url = "https://www.law.go.kr"

# XML 컨텐츠 파싱 함수
def parse_xml_content(xml_content):
    soup = BeautifulSoup(xml_content, 'lxml')  # 'xml' 대신 'lxml' 사용
    case_info = {}
    case_info['판례일련번호'] = soup.find('판례일련번호').text if soup.find('판례일련번호') else ''
    case_info['사건명'] = soup.find('사건명').text if soup.find('사건명') else ''
    case_info['사건번호'] = soup.find('사건번호').text if soup.find('사건번호') else ''
    case_info['선고일자'] = soup.find('선고일자').text if soup.find('선고일자') else ''
    case_info['법원명'] = soup.find('법원명').text if soup.find('법원명') else ''
    case_info['사건종류명'] = soup.find('사건종류명').text if soup.find('사건종류명') else ''
    case_info['판결유형'] = soup.find('판결유형').text if soup.find('판결유형') else ''
    case_info['선고'] = soup.find('선고').text if soup.find('선고') else ''
    return case_info

# 링크에 대한 XML 데이터 크롤링 및 파싱
def crawl_case_details(link, index, total):
    full_url = base_url + link
    response = requests.get(full_url)
    if response.status_code == 200:
        print(f"Processing {index+1}/{total} : {link} - Success")
        return parse_xml_content(response.content)
    else:
        print(f"Processing {index+1}/{total} : {link} - Failed with status code {response.status_code}")
        return {'Error': f"Failed to retrieve data for {link}, Status code: {response.status_code}"}

# 전체 링크 수
total_links = len(detailed_links)

# 크롤링된 데이터 저장
parsed_data = [crawl_case_details(link, index, total_links) for index, link in enumerate(detailed_links)]

# DataFrame으로 변환
parsed_df = pd.DataFrame(parsed_data)

# CSV 파일로 저장
output_file_path = 'parsed_cases.csv'
parsed_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

# 크롤링된 데이터 일부 출력
print(parsed_df.head())

print("CSV 파일로 저장 완료: parsed_cases.csv")
