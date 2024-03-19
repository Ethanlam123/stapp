
import streamlit as st
import google.generativeai as genai

with st.sidebar:
    st.title("Gemini API")
    # Set API key
    api_key = st.text_input("API key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.error("Missing API key.")
    select_model = st.selectbox("Select model", ["gemini-pro"])
    
    # Clear chat
    if st.button("Clear chat"):
        st.session_state["messages"] = []
        st.rerun()

# Function to get response
def get_response(messages, model="gemini-pro"):
    model = genai.GenerativeModel(model)
    res = model.generate_content(messages, stream=True,
                                safety_settings={'HARASSMENT':'block_none'})
    return res

# initialize messages in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
messages = st.session_state["messages"]

# Display chat messages
for item in messages:
    role, parts = item.values()
    if role == "user":
        st.chat_message("user").markdown(parts[0])
    elif role == "model":
        st.chat_message("assistant").markdown(parts[0])

# Chat input
chat_message = st.chat_input("Say something")

# Get response
if chat_message:
    st.chat_message("user").markdown(chat_message)
    res_area = st.chat_message("assistant").empty()
    messages.append(
        {"role": "user", "parts":  [chat_message]},
    )

    res = get_response(messages)

    res_text = ""
    for chunk in res:
        res_text += chunk.text
        res_area.markdown(res_text)
    messages.append(
        {"role": "model", "parts": [res_text]},
    )
