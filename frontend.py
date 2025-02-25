import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Welcome To Datamate")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file is not none:
    st.write("Processing file ...")
    files = {"file":(uploaded_file.name,uploaded_file.getvalue(),"application/pdf")}
    response =requests.post(f"{API_URL}/upload",files=files)
    if response.status_code == 200:
        st.success("File uploaded and processed successfully")
    else:
        st.error(f"Error: {response.json().get('detail','unknown error')}")
            



