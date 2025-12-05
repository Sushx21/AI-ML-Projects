# 🐺 Customer Service Conversational Agent with Memory
A multi-turn AI assistant for telecom customer support, built using LangChain, Groq LLMs, and a custom memory system.

---

## 📌 Overview

This project implements a customer service automation agent capable of:

- Multi-turn conversational understanding  
- Short-term & long-term memory  
- FAQ retrieval using FAISS vector search  
- Tool-augmented reasoning  
- Streamlit-based UI for easy interaction  
- Fast inference using Groq’s GPT-OSS-20B model  

This simulates an enterprise-grade agent (like Amazon Bedrock Agents) but is fully custom, explainable, and locally runnable.

---

## 🧠 Memory Architecture

### **1. Short-Term Memory (STM)**
- Stored in `checkpoints/`  
- Represents the ongoing conversation  
- Automatically restored when a session continues  
- Powers follow-up questions (e.g., “Okay, how do I activate it?”)

### **2. Long-Term Memory (LTM)**
- Stored in `memory_store/`  
- Persists across sessions  
- Stored as JSON files for full transparency  
- Used to recall past user queries or preferences  

This dual memory reflects real-world CS automation systems.

---

## 🔍 FAQ Retrieval System (RAG)

The agent uses:
- `sentence-transformers/all-MiniLM-L6-v2` for embeddings  
- FAISS for vector search  
- Tools for structured retrieval:

### Tools:
1. `search_faq(query)` — quick top-3 search  
2. `search_detailed_faq(query, k)` — deep search  
3. `reformulate_query(original, aspect)` — rephrasing for alternate search angles  

These enable hybrid reasoning + retrieval for accurate answers.

---

## ⚙️ Tech Stack

| Component | Technology |
|----------|------------|
| LLM | Groq “openai/gpt-oss-20b” |
| Framework | LangChain Agents |
| Retrieval | FAISS |
| Memory | JSON disk-based STM + LTM |
| UI | Streamlit |





## 🚀 Workflow

### 1. User asks a question
Example: “What is roaming?”

### 2. Load Short-Term Memory
Restores all previous messages in the session.

### 3. Load Long-Term Memory
Searches past stored memories for relevance.

### 4. Execute Tools
The agent may call `search_faq("roaming")` or reformulate your query.

### 5. Generate Final Answer
The LLM combines:
- conversation history
- retrieved FAQ entries
- remembered context

### 6. Save Memory
- STM ✔ stored as a full conversation snapshot
- LTM ✔ appended as JSON items for persistent recall

---

## 🧪 Use Cases

- Telecom customer service bot
- Billing queries
- Network troubleshooting
- Roaming & activation help
- Family plan controls
- Enterprise customer support
- Interview demonstration of agents + memory + RAG

---



## 🐺 Final Note

This project demonstrates end-to-end AI engineering:

- Memory architecture  
- Retrieval-Augmented Generation  
- LangChain agents  
- Tool orchestration  
- Multi-turn reasoning  
- Real UI + real LLM  

Built by one and only  developer — Susnata  Das
