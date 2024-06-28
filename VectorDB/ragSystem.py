import streamlit as st
import tiktoken
import pandas as pd  # pandas 임포트 추가
from loguru import logger  # 로그로 남기 위한 라이브러리

# 최신 LangChain 패키지 import
from langchain.chains import ConversationalRetrievalChain  # 대화형 검색 체인
from langchain.chat_models import ChatOpenAI  # langchain 모듈에서 가져옴

# 여러 개 문서 넣어도 이해할 수 있게
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 텍스트 나눌 때
from langchain.embeddings import HuggingFaceEmbeddings  # 임베딩할 때
from langchain.memory import ConversationBufferMemory  # 몇 개까지의 대화를 메모리로 넣어줄지
from langchain.vectorstores import FAISS
from langchain.callbacks import get_openai_callback
from langchain.memory import StreamlitChatMessageHistory


def main():
    st.set_page_config(
        page_title="DirChat",
        page_icon=":books:"
    )

    st.title("_Private Data: red[QA Chat]_ :books:")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    if "processComplete" not in st.session_state:
        st.session_state.processComplete = None

    with st.sidebar:
        uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        process = st.button("Process")

    if process:
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        if uploaded_file is not None:
            files_text = get_text_from_csv(uploaded_file)
            text_chunks = get_text_chunks(files_text)
            vectorestore = get_vectorstore(text_chunks)

            st.session_state.conversation = get_conversation_chain(vectorestore, openai_api_key)
            st.session_state.processComplete = True
        else:
            st.info("Please upload a CSV file to continue.")
            st.stop()

    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role": "assistant", 
                                         "content": "안녕하세요! 주어진 문서에 대해 궁금하신 것이 있으면 언제든 물어봐주세요!"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    history = StreamlitChatMessageHistory(key="chat_messages")

    # 채팅 로직
    if query := st.chat_input("질문을 입력해주세요."):
        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            chain = st.session_state.conversation

            with st.spinner("Thinking..."):
                result = chain({"question": query})
                with get_openai_callback() as cb:
                    st.session_state.chat_history = result['chat_history']
                response = result['answer']
                source_documents = result['source_documents']

                st.markdown(response)
                with st.expander("참고 문서 확인"):
                    for doc in source_documents:
                        st.markdown(doc.metadata['source'], help=doc.page_content)

        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    return len(tokens)


def get_text_from_csv(file):
    df = pd.read_csv(file)
    # 필요한 열만 선택
    filter_df = df.drop(["판례일련번호", "사건명", "사건번호", "선고일자", "법원명", "사건종류명", "사건종류코드", "판결유형", "선고", "판시사항", "판결요지", "참조조문", "참조판례", "판례내용"], axis=1, errors='ignore')
    documents = []
    for idx in range(len(filter_df)):
        item = filter_df.iloc[idx]
        document = f"{item['판례내용']}: {item['사건종류명']} : {str(item['판결요지']).strip().lower()} : {str(item['판례내용']).strip().lower()}"
        documents.append(document)
    return documents

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=100,
        length_function=tiktoken_len
    )
    chunks = text_splitter.split_documents(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-multitask",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    vectordb = FAISS.from_documents(text_chunks, embeddings)
    return vectordb


def get_conversation_chain(vetorestore, openai_api_key):
    llm = ChatOpenAI(openai_api_key=openai_api_key, model_name='gpt-3.5-turbo', temperature=0)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=vetorestore.as_retriever(search_type='mmr', verbose=True),
        memory=ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer'),
        get_chat_history=lambda h: h,
        return_source_documents=True,
        verbose=True
    )
    return conversation_chain


if __name__ == '__main__':
    main()