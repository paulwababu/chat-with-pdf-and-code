import os
import shutil
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from io import BytesIO
import zipfile

def load_and_unzip_file(uploaded_file):
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall('/tmp')
    repo_name = uploaded_file.name.replace(".zip", "")
    clone_path = f"/tmp/{repo_name}"
    text = ""
    for root, dirs, files in os.walk(clone_path):
        for file in files:
            with open(os.path.join(root, file), "r") as file:
                text += file.read()
    return text

def delete_unzipped_folder(uploaded_file):
    repo_name = uploaded_file.name.replace(".zip", "")
    clone_path = f"/tmp/{repo_name}"
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path)

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Git Repository",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    st.sidebar.subheader("Authentication")
    password = st.sidebar.text_input("Enter your password", type="password")

    if password != os.getenv("PASSWORD"):
        st.error('Invalid password. Please try again.')
        return

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with Git Repository :books:")
    user_question = st.text_input("Ask a question about your repository:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your Repository")
        uploaded_file = st.file_uploader("Upload your repository as a .zip file and click on 'Process'", type=['zip'])
        if st.button("Process"):
            with st.spinner("Processing"):
                # load and unzip file
                raw_text = load_and_unzip_file(uploaded_file)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)

                # delete unzipped folder
                delete_unzipped_folder(uploaded_file)


if __name__ == '__main__':
    main()