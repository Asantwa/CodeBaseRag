# Codebase RAG GUI
import os
import requests
from openai import OpenAI
import streamlit as st

st.title("Codebase RAG GUI ")

# Model Info

api_key = st.secrets["GROQ_API_KEY"]
model_url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
# Fetch Avail Mods
response = requests.get(model_url, headers=headers)

if response.status_code == 200:
    available_models = response.json()
    st.write("Available Models:", available_models)
else:
    st.error(f"Failed to fetch models: {response.status_code} - {response.text}")
# Verify the API Key is Included in the Request

#client = OpenAI(
#   base_url="https://api.groq.com/openai/v1",
#    api_key=os.environ.get("GROQ_API_KEY")
#)


# Store session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat interface
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Make a request to the Groq API
    completion_url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama-3.1-8b-instant",  # Replace with a valid model name
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(completion_url, headers=headers, json=payload)
        response.raise_for_status()
        assistant_reply = response.json()["choices"][0]["message"]["content"]
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
        st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error: {http_err}")
    except Exception as err:
        st.error(f"Unexpected error: {err}")