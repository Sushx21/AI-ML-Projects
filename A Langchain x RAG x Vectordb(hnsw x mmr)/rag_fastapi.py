
# RAG Backend (MMR + HNSW) - FastAPI
#  uvicorn rag_fastapi:app --reload --port 8001
# Swagger: http://127.0.0.1:8001/docs

from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

#  CONFIG
CHUNK_SIZE = 1000
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "financial_data"

llm = None
vector_store = None

app = FastAPI()


# INITIALIZATION
def initialize_components():
    global llm, vector_store

    if llm is None:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.9,
            max_tokens=500
        )

    if vector_store is None:
        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code": True}
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR),
            collection_metadata={"hnsw:space": "cosine"}
        )


# URL INGESTION
def process_urls(urls):
    yield "Initializing components..."
    initialize_components()

    vector_store.reset_collection()

    yield "Loading URLs..."
    headers = {"User-Agent": "Mozilla/5.0"}

    loader = UnstructuredURLLoader(urls=urls, headers=headers)
    data = loader.load()

    yield "Splitting text into chunks..."
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=CHUNK_SIZE,
    )
    docs = splitter.split_documents(data)

    yield f"Adding {len(docs)} chunks to vector DB..."
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=uuids)


#  QUERY FUNCTION
def generate_answer(query):
    if vector_store is None:
        raise RuntimeError("Vector store not initialized")

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.5}
    )

    chain = RetrievalQAWithSourcesChain.from_llm(
        llm=llm,
        retriever=retriever
    )

    result = chain.invoke({"question": query}, return_only_outputs=True)
    return result.get("answer", ""), result.get("sources", "")


#  REQUEST MODELS
class URLRequest(BaseModel):
    urls: list[str]


class QueryRequest(BaseModel):
    question: str


# API ROUTES
@app.post("/process_urls")
async def process_urls_api(request: URLRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(_run_ingestion, request.urls)
    return {"status": "processing"}


def _run_ingestion(urls):
    for _ in process_urls(urls):
        pass


@app.post("/ask")
async def ask_api(request: QueryRequest):
    answer, sources = generate_answer(request.question)
    return {"answer": answer, "sources": sources}


@app.get("/")
async def health():
    return {"status": "ok"}