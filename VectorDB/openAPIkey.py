from dotenv import load_dotenv
import openai
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def test_openai_api():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 최신 모델로 변경
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, world!"}
            ],
            max_tokens=50
        )
        print(response.choices[0].message['content'].strip())
    except Exception as e:
        print(f"API 호출 오류: {e}")

test_openai_api()
