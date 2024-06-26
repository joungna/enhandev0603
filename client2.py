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
        response = requests.post("http://14.39.221.117:8000/essay/invoke",
                                 json={'input': {'topic': topic}})
    else:
        # 잉한 작성 API에 POST 요청을 보냅니다.
        response = requests.post("http://14.39.221.117:8000/poem/invoke",
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
