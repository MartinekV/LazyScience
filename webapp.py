import streamlit as st
from paperqa import Docs
import os

st.title("Scientific paper QA assistant")

api_input = st.text_input('your OpenAI API key goes here')
if(api_input):
    st.write('API KEY UPDATED')
    os.environ['OPENAI_API_KEY'] = api_input
    st.write(os.environ['OPENAI_API_KEY'])

#TODO try local llama to avoid api costs
if "docs" not in st.session_state and api_input:
    docs = Docs()
    st.session_state.docs = docs


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
if uploaded_file is not None and api_input:
    
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