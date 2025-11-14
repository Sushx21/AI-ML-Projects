**# 🏡 SUSNATA'S Real Estate Research Tool  
### A Fast, Accurate RAG System with HNSW + MMR Retrieval  
Powered by **LangChain**, **Groq Llama 3.3**, and **ChromaDB**  
Built by Susnata 🐺

---

## 📌 Overview

This project is a **Real Estate Research & Analysis Tool** that uses a **Retrieval-Augmented Generation (RAG)** pipeline to extract information from financial and real-estate websites.

It features:

- **HNSW vector indexing** (high-speed approximate nearest neighbor search)  
- **MMR Retrieval** (Maximal Marginal Relevance) for *diverse + relevant* context  
- **Groq Llama 3.3 model** for fast, factual reasoning  
- **Streamlit frontend** for an interactive UI  
- **URL scraping → chunking → vector storage → on-demand Q&A**

---

## 🚀 Features

### 🔍 1. Web Scraping  
Uses `UnstructuredURLLoader` to fetch text from real estate / finance websites.

### ✂️ 2. Intelligent Chunking  
Text is split into meaningful chunks using `RecursiveCharacterTextSplitter`.

### 📚 3. Vector Storage (ChromaDB)  
Stores embeddings with HNSW indexing:

```python
collection_metadata={"hnsw:space": "cosine"}**

### 🤖 4. MMR Retrieval

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20,
        "lambda_mult": 0.5
    }
)

💬 5. LLM-Powered Answering

The retrieved chunks are passed to:

ChatGroq(model="llama-3.3-70b-versatile")



###  6. Streamlit UI

Simple interface where the user:

Inputs URLs

Processes them

Asks natural-language questions

Gets fact-based answers with source citations