import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

st.title("📄 PDF Chatbot with LangChain & Ollama")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
if uploaded_file:
    st.session_state.uploaded_pdf = uploaded_file  # Store PDF in session state

# Upload button
if st.button("Upload PDF") and "uploaded_pdf" in st.session_state:
    st.write("Processing file...")
    files = {
        "file": (st.session_state.uploaded_pdf.name, 
                 st.session_state.uploaded_pdf.getvalue(), 
                 "application/pdf")
    }
    response = requests.post(f"{API_URL}/upload", files=files)
    
    if response.status_code == 200:
        st.success("File uploaded and processed successfully!")
    else:
        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

# Chat interface
st.subheader("Chat with the PDF")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Ask something about the PDF")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    
    data = {"query": query}  # Ensure correct JSON format
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(f"{API_URL}/chat", json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        bot_response = result.get("response", "No relevant information found in the document.")
    else:
        bot_response = f"Error: {response.json().get('detail', 'Unknown error')}"
    
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
