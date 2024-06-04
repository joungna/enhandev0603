

import streamlit as st
import requests

# Streamlit 애플리케이션의 제목과 설명을 설정합니다.
st.title("잉한번역기")
st.write("영어문장을 잉한으로 번역해 단어학습하는 인공지능입니다.")

# 사용자가 입력할 주제를 받는 입력 상자를 만듭니다.
topic = st.text_input("영어문장을 입력하세요:")

# 사용자가 선택할 수 있도록 라디오 버튼을 만듭니다.
option = st.radio("작성을 원하는 항목을 선택하세요:", ("단어번역", "잉한번역"))
# 또는 selectbox를 사용하여 드롭다운 메뉴로 사용할 수 있습니다.
# option = st.selectbox("작성을 원하는 항목을 선택하세요:", )
# 버튼을 만들어 사용자가 클릭하면 API 요청을 보내도록 합니다.
if st.button("작성 요청 보내기"):
    if option == "단어번역":
        # 단어번역 작성 API에 POST 요청을 보냅니다.
        response = requests.post("http://localhost:8000/essay/invoke",
                                 json={'input': {'topic': topic}})
    else:
        # 잉한 작성 API에 POST 요청을 보냅니다.
        response = requests.post("http://localhost:8000/poem/invoke",
                                 json={'input': {'topic': topic}})

    # 응답을 JSON 형식으로 받아와서 출력합니다.
    if response.status_code == 200:
        st.write(f"### {option} 응답")
        content = response.json().get('output', {}).get('content', 'No content found')
        st.write(content)
        # content를 파일로 저장할 수 있도록 다운로드 버튼을 만듭니다.
        st.download_button(
            label="결과 다운로드",
            data=content,
            file_name=f"{option}_result.txt",
            # mime은 Multipurpose Internet Mail Extensions의 약자로, 인터넷에서 전송되는 파일의 형식을 명시하는 데 사용되는 표준입니다.
            mime="text/plain"
        )

    else:
        st.write(f"{option} API 요청에 실패했습니다.")
        
        
# 필요한 모듈을 가져옵니다.
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn

# dotenv 모듈을 사용하여 .env 파일에서 환경 변수를 로드합니다.
from dotenv import load_dotenv
import os

# .env 파일에서 API 키를 읽어옵니다.
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# FastAPI 애플리케이션을 생성합니다.
app = FastAPI(
    title="Langchain Server",  # 애플리케이션의 제목을 설정합니다.
    version="0.1",             # 애플리케이션의 버전을 설정합니다.
    description="simple langchain API Server"  # 애플리케이션의 설명을 설정합니다.
)

# OpenAI 모델을 설정합니다.
# ChatOpenAI 클래스를 사용하여 OpenAI 모델과의 상호작용을 설정합니다.
# 여기서는 API 키, 온도 설정, 모델 이름을 파라미터로 제공합니다.
model = ChatOpenAI(
    api_key=OPENAI_API_KEY,  # OpenAI API 키를 사용하여 인증합니다.
    temperature=0.7,         # 응답의 창의성(무작위성) 수준을 설정합니다. 0.7은 중간 정도의 창의성을 의미합니다.
    model='gpt-3.5-turbo'    # 사용할 OpenAI 모델의 이름을 지정합니다.
)

# Langchain API 경로를 추가합니다.
# add_routes 함수를 사용하여 FastAPI 애플리케이션에 경로를 추가합니다.
add_routes(
    app,
    model,  # ChatOpenAI 클래스의 인스턴스를 사용하여 OpenAI 모델과 상호작용합니다.
    path="/openai"  # 이 경로로 요청이 들어오면 ChatOpenAI 인스턴스를 통해 처리됩니다.
)


# 영어문장 작성용 프롬프트 템플릿을 생성합니다.
prompt1 = ChatPromptTemplate.from_template("영어문장에서 랜덤하게 단어 5개를 뽑아서 한국어로 번역해서 한국어 의미, 유사어를 작성해줘 {topic}")

# 작성용 프롬프트 템플릿을 생성합니다.
prompt2 = ChatPromptTemplate.from_template("영어단어와 문장을 먼저 발음하는대로 한글자음모음으로 변환해, 예를 들어 “Our Father in heaven”을 '아우어 파더 인 헤븐'처럼 변경된 문장으로 작성하세요 {topic}")

# 작성 API 경로를 추가합니다.
add_routes(
    app,
    prompt1 | model,  # 프롬프트 템플릿과 모델을 결합하여 요청을 처리합니다.
    path="/essay"  # 이 경로로 요청이 들어오면 작성합니다.
)

# 작성 API 경로를 추가합니다.
add_routes(
    app,
    prompt2 | model,  # 프롬프트 템플릿과 모델을 결합하여 요청을 처리합니다.
    path="/poem"  # 이 경로로 요청이 들어오면  작성합니다.
)

# 애플리케이션을 실행합니다.
if __name__ == "__main__":
    # localhost:8000에서 애플리케이션을 실행합니다.
    uvicorn.run(app, host="localhost", port=8000)
