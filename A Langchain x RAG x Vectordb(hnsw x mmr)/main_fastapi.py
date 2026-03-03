import streamlit as st
import requests

# Health Check
try:
    health = requests.get("http://127.0.0.1:8001/health")
    st.sidebar.success(f"Backend: {health.json().get('status')} 🟢")
except:
    st.sidebar.error("Backend NOT reachable ❌")

st.title("⚡ Susnata's Real Estate Research Tool")

# PROCESSING URLS
st.subheader("🌐 Please Add URLs for RAG Ingestion")

url1 = st.text_input("URL 1")
url2 = st.text_input("URL 2")
url3 = st.text_input("URL 3")

if st.button("Process URLs"):
    urls = [u for u in (url1, url2, url3) if u.strip() != ""]

    st.write("⏳ Processing URLs... Please wait...")

    response = requests.post(
        "http://127.0.0.1:8001/process_urls",
        json={"urls": urls}
    )

    st.write("###  Status:")
    st.write(response.json())



st.subheader("💬 Ask Your Question")

question = st.text_input("Question")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question!")
    else:
        response = requests.post(
            "http://127.0.0.1:8001/ask",
            json={"question": question}
        )

        data = response.json()

        # Debug view
        st.write("### Raw Backend Response:")
        st.write(data)

        # Safe answer display
        st.write("### Susnata's Answer:")
        st.write(data.get("answer", "⚠ No answer returned. Try processing URLs first."))

        st.write("### 📚 Sources:")
        st.write(data.get("sources", "⚠ No sources returned."))