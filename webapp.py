import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

st.title("Scientific paper QA assistant\nQuery costs ~0.03$")
print(list(st.session_state.keys()))

#TODO try local llama to avoid api costs
def init_docs():

    from paperqa import Docs
    llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo", client=None, openai_api_key=os.environ['OPENAI_API_KEY'])
    embeddings = OpenAIEmbeddings(client=None, openai_api_key=os.environ['OPENAI_API_KEY'])
    docs = Docs(llm=llm, embeddings=embeddings)
    st.session_state.docs = docs

api_input = st.text_input('your OpenAI API key goes here\n!!!API KEY IS NOT ENCRYPTED, USE THROWAWAY KEY FOR YOUR SAFETY!!!')
if(api_input):
    os.environ['OPENAI_API_KEY'] = api_input
    print('RELOADING', os.environ['OPENAI_API_KEY'])
    init_docs()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
if uploaded_file is not None:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.read())
        # f.flush()
    st.session_state.docs.add(uploaded_file.name)

# React to user input
if prompt := st.chat_input("Ask a question about your files"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = st.session_state.docs.query(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})