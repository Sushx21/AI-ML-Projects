# susnata_langgraph_agent_with_memory.py
import csv
import os
import json
import uuid
from typing import List, Tuple
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
from langchain.agents import create_agent

_ = load_dotenv()

# ---------------------------------------------------
# LOAD FAQ CSV → RAG KNOWLEDGE BASE
# ---------------------------------------------------
def load_faq_csv(path: str) -> List[Document]:
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            q = row["question"].strip()
            a = row["answer"].strip()
            docs.append(Document(page_content=f"Q: {q}\nA: {a}"))
    return docs

docs = load_faq_csv("./susnata_qna.csv")

emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
chunks = splitter.split_documents(docs)
store = FAISS.from_documents(chunks, emb)


# ---------------------------------------------------
# DISK MEMORY (LONG-TERM) + CHECKPOINT (SHORT-TERM)
# ---------------------------------------------------
MEMORY_ROOT = Path("./memory_store")
CHECKPOINT_ROOT = Path("./checkpoints")

MEMORY_ROOT.mkdir(parents=True, exist_ok=True)
CHECKPOINT_ROOT.mkdir(parents=True, exist_ok=True)


def _namespace_path(actor_id: str, thread_id: str) -> Path:
    p = MEMORY_ROOT / actor_id / thread_id
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_memory_item(actor_id: str, thread_id: str, role: str, content: str):
    ns = _namespace_path(actor_id, thread_id)
    item_id = str(uuid.uuid4())
    payload = {"id": item_id, "role": role, "content": content}
    with open(ns / f"{item_id}.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def list_memory_items(actor_id: str, thread_id: str) -> List[dict]:
    ns = _namespace_path(actor_id, thread_id)
    items = []
    for fpath in sorted(ns.glob("*.json")):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                items.append(json.load(f))
        except:
            pass
    return items


def search_memory(actor_id: str, thread_id: str, query: str, limit=5):
    q = query.lower()
    items = list_memory_items(actor_id, thread_id)
    matched = [it for it in items if q in it["content"].lower()]

    if not matched:
        actor_dir = MEMORY_ROOT / actor_id
        if actor_dir.exists():
            for fpath in sorted(actor_dir.glob("*/*.json")):
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        it = json.load(f)
                    if q in it["content"].lower():
                        matched.append(it)
                except:
                    pass

    return matched[:limit]


def save_checkpoint(actor_id: str, thread_id: str, messages: List[Tuple[str, str]]):
    cp_dir = CHECKPOINT_ROOT / actor_id
    cp_dir.mkdir(parents=True, exist_ok=True)
    fname = cp_dir / f"{thread_id}.json"
    normalized = [{"role": r, "content": c} for r, c in messages]
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)


def load_checkpoint(actor_id: str, thread_id: str) -> List[Tuple[str, str]]:
    fname = CHECKPOINT_ROOT / actor_id / f"{thread_id}.json"
    if not fname.exists():
        return []
    with open(fname, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [(d["role"], d["content"]) for d in data]


# ---------------------------------------------------
# TOOLS
# ---------------------------------------------------
@tool
def search_faq(query: str):
    """Search the FAQ knowledge base."""
    results = store.similarity_search(query, k=3)
    if not results:
        return "No relevant FAQ entries found."
    return "\n\n---\n\n".join(
        [f"FAQ Entry {i+1}:\n{doc.page_content}" for i, doc in enumerate(results)]
    )


@tool
def search_detailed_faq(query: str, num_results: int = 5):
    """Search for more (k=N) FAQ entries."""
    results = store.similarity_search(query, k=num_results)
    if not results:
        return "No relevant FAQ entries found."
    return "\n\n---\n\n".join(
        [f"FAQ Entry {i+1}:\n{doc.page_content}" for i, doc in enumerate(results)]
    )


@tool
def reformulate_query(original_query: str, focus_aspect: str):
    """Reformulate a query to focus on a specific aspect."""
    reformulated = f"{focus_aspect} related to {original_query}"
    results = store.similarity_search(reformulated, k=3)
    if not results:
        return f"No results for aspect: {focus_aspect}"
    return "\n\n---\n\n".join(
        [f"Entry {i+1}:\n{doc.page_content}" for i, doc in enumerate(results)]
    )


tools = [search_faq, search_detailed_faq, reformulate_query]


# ---------------------------------------------------
# LLM + AGENT
# ---------------------------------------------------
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

system_prompt = """You are a helpful FAQ assistant with access to tools and memory."""

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt
)


# ---------------------------------------------------
# MEMORY WRAPPER (MAIN FUNCTION STREAMLIT USES)
# ---------------------------------------------------
def run_with_memory(actor_id: str, thread_id: str, session_messages: List[Tuple[str, str]]):

    checkpoint = load_checkpoint(actor_id, thread_id)
    messages_to_send = checkpoint + session_messages

    last_user = None
    for r, c in reversed(messages_to_send):
        if r.lower() in ("human", "user"):
            last_user = c
            break

    if last_user:
        mems = search_memory(actor_id, thread_id, last_user, limit=5)
        if mems:
            memory_context = "\n".join(
                [f"- {m['role']}: {m['content']}" for m in mems]
            )
            messages_to_send.insert(0, ("system", f"Relevant memories:\n{memory_context}"))

    result = agent.invoke({"messages": messages_to_send})
    final_messages = result.get("messages", [])
    assistant_content = final_messages[-1].content if final_messages else "No response."

    for r, c in session_messages:
        if r.lower() in ("human", "user"):
            save_memory_item(actor_id, thread_id, "user", c)

    save_memory_item(actor_id, thread_id, "assistant", assistant_content)

    normalized = []
    for msg in final_messages:
        if hasattr(msg, "role") and hasattr(msg, "content"):
            normalized.append((msg.role, msg.content))
        elif isinstance(msg, (list, tuple)) and len(msg) == 2:
            normalized.append((msg[0], msg[1]))
        else:
            normalized.append(("assistant", str(msg)))

    save_checkpoint(actor_id, thread_id, normalized)

    return assistant_content