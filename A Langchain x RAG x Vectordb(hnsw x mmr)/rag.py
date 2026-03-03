
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
CHUNK_SIZE = 2000
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "financial_data"

# Global vars
llm = None
vector_store = None


def initialize_components():
    """Initializing LLM and Vector Store once"""
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
            persist_directory=str(VECTORSTORE_DIR)
        )


def process_urls(urls):
    """Scraping data from URLs and store in vector DB"""
    yield("Initializing components...best investments")
    initialize_components()


    vector_store.reset_collection()

    yield("Loading data...")

    # Adding fake browser headers to fool sites like Yahoo Finance or else not working
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0 Safari/537.36"
        )
    }

    # Trying UnstructuredURLLoader first
    loader = UnstructuredURLLoader(urls=urls, headers=headers)


    data = loader.load()

    yield("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=CHUNK_SIZE
    )
    docs = text_splitter.split_documents(data)

    yield(f"Adding {len(docs)} documents to vector DB...")
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=uuids)


def generate_answer(query):
    if not vector_store:
        raise RuntimeError("Vector database is not initialized ") ##raising exception if no urls given

    chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vector_store.as_retriever())
    result = chain.invoke({"question": query}, return_only_outputs=True)
    sources = result.get("sources", "")

    return result['answer'], sources



if __name__ == '__main__':

    urls = [
        "https://www.investopedia.com/terms/m/mortgage.asp",
        "https://www.tradingeconomics.com/united-states/interest-rate",
        "https://finance.yahoo.com/news/mortgage-rates-climb-2024-120000000.html"
    ]

    process_urls(urls)

    answer,sources=generate_answer("Tell me what was the 30 year fixed mortgage rate along with the date?")
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")


