import streamlit as st
from susnata_langgraph_agent import agent   # import your backend agent

st.set_page_config(page_title="Susnata AI FAQ Agent", page_icon="🤖")

st.title("🤖 Susnata AI FAQ Agent")
st.write("Ask any question from your FAQ dataset.")

# Text input box
question = st.text_input("Enter your question:")

# Button to trigger agent
if st.button("Ask"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            result = agent.invoke({"messages": [("human", question)]})
            answer = result["messages"][-1].content
            st.write("### Answer:")
            st.write(answer)