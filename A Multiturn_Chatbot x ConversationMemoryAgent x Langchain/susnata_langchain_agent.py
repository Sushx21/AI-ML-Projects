import csv
import os
from typing import List
from typing_extensions import TypedDict

from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
from langchain.agents import create_agent

_ = load_dotenv()


def load_faq_csv(path: str) -> List[Document]:
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            q = row["question"].strip()
            a = row["answer"].strip()
            docs.append(Document(page_content=f"Q: {q}\nA: {a}"))
    return docs


docs = load_faq_csv("./lauki_qna.csv")
emb = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
chunks = splitter.split_documents(docs)
store = FAISS.from_documents(chunks, emb)


@tool
def search_faq(query: str) -> str:
    """Search the FAQ knowledge base for relevant information.
    Use this tool when the user asks questions about products, services, or policies.

    Args:
        query: The search query to find relevant FAQ entries

    Returns:
        Relevant FAQ entries that might answer the question
    """
    results = store.similarity_search(query, k=3)

    if not results:
        return "No relevant FAQ entries found."

    context = "\n\n---\n\n".join([
        f"FAQ Entry {i + 1}:\n{doc.page_content}"
        for i, doc in enumerate(results)
    ])

    return f"Found {len(results)} relevant FAQ entries:\n\n{context}"


@tool
def search_detailed_faq(query: str, num_results: int = 5) -> str:
    """Search the FAQ knowledge base with more results for complex queries.
    Use this when the initial search doesn't provide enough information.

    Args:
        query: The search query
        num_results: Number of results to retrieve (default: 5)

    Returns:
        More comprehensive FAQ entries
    """
    results = store.similarity_search(query, k=num_results)

    if not results:
        return "No relevant FAQ entries found."

    context = "\n\n---\n\n".join([
        f"FAQ Entry {i + 1}:\n{doc.page_content}"
        for i, doc in enumerate(results)
    ])

    return f"Found {len(results)} detailed FAQ entries:\n\n{context}"


@tool
def reformulate_query(original_query: str, focus_aspect: str) -> str:
    """Reformulate the query to focus on a specific aspect.
    Use this when you need to search for a different angle of the question.

    Args:
        original_query: The original user question
        focus_aspect: The specific aspect to focus on (e.g., "pricing", "activation", "troubleshooting")

    Returns:
        A reformulated query focused on the specified aspect
    """
    reformulated = f"{focus_aspect} related to {original_query}"
    results = store.similarity_search(reformulated, k=3)

    if not results:
        return f"No results found for aspect: {focus_aspect}"

    context = "\n\n---\n\n".join([
        f"Entry {i + 1}:\n{doc.page_content}"
        for i, doc in enumerate(results)
    ])

    return f"Results for '{focus_aspect}' aspect:\n\n{context}"


tools = [search_faq, search_detailed_faq, reformulate_query]

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

system_prompt = """You are a helpful FAQ assistant with access to a knowledge base.

Your goal is to answer user questions accurately using the available tools.

Guidelines:
1. Start by using the search_faq tool to find relevant information
2. If the initial search doesn't provide enough info, use search_detailed_faq for more results
3. If the query is complex, use reformulate_query to search different aspects
4. Synthesize information from multiple tool calls if needed
5. Always provide a clear, concise answer based on the retrieved information
6. If you cannot find relevant information, clearly state that

Think step-by-step and use tools strategically to provide the best answer."""

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt
)

if __name__ == "__main__":
    result = agent.invoke({"messages": [("human", "Explain roaming activation.")]})
    print(result['messages'][-1].content)
