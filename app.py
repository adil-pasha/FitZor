import streamlit as st
import requests

# Load API key from secrets
DIFY_API_KEY = st.secrets["DIFY_API_KEY"]
DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"

# Streamlit App UI
st.set_page_config(page_title="FitZor", page_icon="🏋️", layout="centered")

st.title("🏋️ Fitness Chatbot")
st.write("Ask me anything about fitness, workouts, and healthy living!")

# Store conversation in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if user_input := st.chat_input("Type your fitness question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send request to Dify API
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {},
        "query": user_input,
        "user": "streamlit_user"
    }
    
    response = requests.post(DIFY_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json().get("answer", "Sorry, I couldn't generate a response.")
    else:
        reply = f"Error: {response.status_code} - {response.text}"

    # Add bot reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
