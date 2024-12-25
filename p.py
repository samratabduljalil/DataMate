import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.llms import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from langchain.retrievers.multi_vector import MultiVectorRetriever
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = FastAPI()

# Global variable for the Q&A system
qa_system = None

# Step 1: Load and chunk PDF
def load_and_chunk_pdf(file_path, chunk_size=1000, overlap=200):
    loader = PyPDFLoader(file_path)
    documents = loader.load_and_split(chunk_size=chunk_size, overlap=overlap)
    return documents

# Step 2: Create embeddings and vectorstore
def setup_vectorstore(documents):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents, embedding=embeddings)
    return vectorstore

# Step 3: Load Llama 2 model
def load_llama_model():
    MODEL_NAME = "meta-llama/Llama-2-7b-hf"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=512, temperature=0)
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm

# Step 4: Setup MultiVectorRetriever
def setup_multi_retriever(vectorstore):
    retriever = MultiVectorRetriever(vectorstore=vectorstore)
    return retriever

# Step 5: Setup Q&A system with memory
def setup_qa_system(retriever, llm):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
    return qa_chain

# FastAPI endpoint for uploading a PDF
@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    global qa_system
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Process the PDF
    documents = load_and_chunk_pdf(file_path)
    vectorstore = setup_vectorstore(documents)
    llm = load_llama_model()
    retriever = setup_multi_retriever(vectorstore)
    qa_system = setup_qa_system(retriever, llm)

    return JSONResponse({"message": "PDF uploaded and processed successfully."})

# FastAPI endpoint for chatting with the system
@app.post("/chat/")
async def chat(query: str):
    global qa_system
    if not qa_system:
        raise HTTPException(status_code=400, detail="No PDF has been uploaded. Please upload a PDF first.")
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    response = qa_system({"question": query})
    return JSONResponse({"response": response["answer"]})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
