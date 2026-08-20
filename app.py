import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="T-Rex AI", page_icon="🦖")

# Header
st.title("🦖 T-REX AI")
st.caption("Your Personal AI Assistant")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.markdown("[Get Free Key Here](https://aistudio.google.com/)")

# Initialize Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
if prompt := st.chat_input("Talk to T-Rex..."):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar!")
        st.stop()

    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # T-Rex Response
    try:
        client = genai.Client(api_key=api_key)
        
        with st.chat_message("assistant"):
            with st.spinner("T-Rex is thinking..."):
                full_prompt = f"Your name is T-Rex, a smart AI assistant. Answer this: {prompt}"
                
                # Updated Model Name Here
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=full_prompt
                )
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Error: {e}")