import streamlit as st
import uuid
from susnata_langgraph_agent_with_memory import (
    run_with_memory,
    list_memory_items,
)

st.set_page_config(page_title="Susnata Agent", page_icon="🤖", layout="wide")

st.title("🤖 Susnata Multi-Turn Agent with Memory")

# ---------------------------
# Session Identifiers
# ---------------------------
if "actor_id" not in st.session_state:
    st.session_state["actor_id"] = "local_user"

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = "thread_" + str(uuid.uuid4())[:8]

if "messages" not in st.session_state:
    st.session_state["messages"] = []

actor_id = st.session_state["actor_id"]
thread_id = st.session_state["thread_id"]

# ---------------------------
# Top bar actions
# ---------------------------
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🆕 New Chat"):
        st.session_state["thread_id"] = "thread_" + str(uuid.uuid4())[:8]
        st.session_state["messages"] = []
        st.rerun()

with col2:
    if st.button("📂 Show Memory"):
        mems = list_memory_items(actor_id, thread_id)
        if mems:
            st.sidebar.title("Saved Memory Items")
            for m in mems:
                st.sidebar.write(f"**{m['role']}**: {m['content']}")
        else:
            st.sidebar.info("No memory stored yet.")

with col3:
    st.write(f"**Actor:** `{actor_id}` | **Thread:** `{thread_id}`")

# ---------------------------
# Display chat history
# ---------------------------
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# Chat Input

user_input = st.chat_input("Ask your question…")

if user_input:
    # Add user message
    st.session_state["messages"].append({"role": "human", "content": user_input})

    with st.chat_message("human"):
        st.write(user_input)

    # Call backend agent with memory
    with st.spinner("Thinking…"):
        assistant_response = run_with_memory(
            actor_id,
            thread_id,
            [("human", user_input)]
        )

    # Showing reply
    with st.chat_message("assistant"):
        st.write(assistant_response)

    # Saving assistant message
    st.session_state["messages"].append(
        {"role": "assistant", "content": assistant_response}
    )

    st.rerun()