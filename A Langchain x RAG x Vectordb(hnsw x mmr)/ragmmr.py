#RAG Backend (with MMR + HNSW)


from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain_community.document_loaders import PlaywrightURLLoader   # fallback if my  headers fail to spoof
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings


# Load environment variables
load_dotenv()

# Constants
CHUNK_SIZE = 1000
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "financial_data"

# Global vars
llm = None
vector_store = None

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



# Process URLs  (GLOBAL FUNCTION)

def process_urls(urls):
    yield ("Initializing components...")
    initialize_components()

    vector_store.reset_collection()

    yield ("Loading data...")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0 Safari/537.36"
        )
    }

    loader = UnstructuredURLLoader(urls=urls, headers=headers)
    data = loader.load()

    yield ("Splitting text...")
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=CHUNK_SIZE,
    )
    docs = splitter.split_documents(data)

    yield (f"Adding {len(docs)} chunks...")
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=uuids)



# Generate Answer  (GLOBAL FUNCTION)

def generate_answer(query):
    if vector_store is None:
        raise RuntimeError("Vector database is not initialized")

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,  # final chunks given to LLM
            "fetch_k": 20, # chunks MMR considers before reranking
            "lambda_mult": 0.5 # balance between relevance & diversity where 1 is rigid relevance best for accuracy no penalty
            # if repeated chunks
            # and 0 is diversity best for broder summary Can select less relevant documents if they add new information
        }
    )

    chain = RetrievalQAWithSourcesChain.from_llm(
        llm=llm,
        retriever=retriever
    )

    result = chain.invoke({"question": query}, return_only_outputs=True)

    return result.get("answer", ""), result.get("sources", "")