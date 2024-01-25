import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
# import dotenv
# dotenv.load_dotenv()

st.title("LazyScience - Scientific paper QA assistant\nQuery costs ~0.03$")

#TODO try local llama to avoid api costs
def init_docs():
    from paperqa import Docs
    llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo", client=None, openai_api_key=os.environ['OPENAI_API_KEY'])
    embeddings = OpenAIEmbeddings(client=None, openai_api_key=os.environ['OPENAI_API_KEY'])
    docs = Docs(llm=llm, embeddings=embeddings)
    st.session_state.docs = docs

api_input = st.sidebar.text_input('your OpenAI API key goes here\n!!!API KEY IS NOT ENCRYPTED, BURN IT AFTER USE FOR YOUR SAFETY!!!')

if(api_input):
    os.environ['OPENAI_API_KEY'] = api_input

if "messages" not in st.session_state:
    st.session_state.messages = []

if(api_input):
    if('docs' not in st.session_state):
        init_docs()
        st.session_state.added_docs = []
    uploaded_files = st.sidebar.file_uploader('Choose your .pdf files', type="pdf", accept_multiple_files=True) #TODO extend to other file types?
    for uploaded_file in uploaded_files:
        if(uploaded_file.name not in st.session_state.added_docs):
            st.session_state.added_docs.append(uploaded_file.name)
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.read())
            st.session_state.docs.add(uploaded_file.name)

if("docs" in st.session_state and api_input):
    # st.sidebar.markdown([doc.docname for doc in st.session_state.docs.docs.values()])
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about your files"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        #TODO let user change params of query in UI, length_prompt="about 100 words"
        response = st.session_state.docs.query(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})