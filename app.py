from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import re
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.llms import Ollama
from typing import List

app = FastAPI()

# Ollama server details
OLLAMA_URL = "http://127.0.0.1:12345"
embedding_model = OllamaEmbeddings(base_url=OLLAMA_URL, model="nomic-embed-text:latest")
ollama_llm = Ollama(model="llama3:latest", base_url=OLLAMA_URL)

# Directory for saving uploaded files and Chroma DB
UPLOAD_DIR = "uploaded_files"
CHROMA_DIR = "chroma_db"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

# Initialize Chroma DB
chroma_db = None

def load_to_chroma(file_path: str):
    """Load PDF content, clean it, split it, and embed it in Chroma DB."""
    global chroma_db

    # Load PDF document
    loader = UnstructuredPDFLoader(file_path)
    documents = loader.load()

    # Clean the document text
    text_without_newlines = []
    for document in documents:
        text = document.page_content
        cleaned_text = re.sub(r'\n+', ' ', text)
        text_without_newlines.append(cleaned_text)

    # Split text into chunks with overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = text_splitter.split_text(" ".join(text_without_newlines))

    # Generate embeddings and save to Chroma DB
    chroma_db = Chroma.from_texts(chunks, embedding_model, persist_directory=CHROMA_DIR)
    chroma_db.persist()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint to upload a PDF file and process it."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        load_to_chroma(file_path)
        return {"message": "File uploaded and processed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

@app.post("/chat")
async def chat_with_file(query: str):
    """Endpoint to query the uploaded PDF file and get a response."""
    global chroma_db
    if chroma_db is None:
        raise HTTPException(status_code=400, detail="No file has been uploaded yet.")

    try:
        # Query Chroma DB
        query_embedding = embedding_model.embed_query(query)
        results = chroma_db.similarity_search_by_vector(query_embedding, k=3)

        if not results:
            return {"message": "No relevant results found."}

        # Combine retrieved text for the prompt
        retrieved_text = " ".join([result.page_content for result in results])

        # Prepare the prompt template
        prompt_template = f"""
        You are a helpful assistant. Using the following retrieved context and user query, generate an informative response  based on the query.

        Context:
        {retrieved_text}

        Query:
        {query}

        Please keep the response concise ,short and relevant.
        """

        # Generate response using Llama 3
        response = ollama_llm(prompt_template)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during query: {e}")
