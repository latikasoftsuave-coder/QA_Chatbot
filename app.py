import streamlit as st
import requests
from datetime import datetime
import uuid

st.title("QA Chatbot")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "history" not in st.session_state:
    st.session_state.history = []

def load_history():
    try:
        response = requests.get(f"http://127.0.0.1:8000/history/{st.session_state.session_id}")
        messages = response.json()
        st.session_state.history = messages
    except Exception as e:
        st.error(f"Error loading history: {e}")

if not st.session_state.history:
    load_history()

for msg in st.session_state.history:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

if user_question := st.chat_input("Ask me anything..."):
    with st.chat_message("user"):
        st.write(user_question)

    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={"question": user_question}
        )
        data = response.json()

        if "answer" in data:
            answer = data["answer"]
            with st.chat_message("assistant"):
                st.write(answer)

            st.session_state.history.append({"role": "user", "content": user_question, "timestamp": datetime.utcnow().isoformat()})
            st.session_state.history.append({"role": "assistant", "content": answer, "timestamp": datetime.utcnow().isoformat()})
        else:
            st.error(data.get("error", "Unknown error occurred"))
    except Exception as e:
        st.error(f"Error: {e}")