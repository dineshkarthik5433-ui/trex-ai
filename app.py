import streamlit as st
import requests
import urllib.parse

# Page Config
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Sleek Dark UI Styling
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .main-title { 
        font-size: 2.5rem; 
        font-weight: 800; 
        background: linear-gradient(90deg, #00FF87 0%, #60EFFF 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        text-align: center; 
        margin-bottom: 0px; 
    }
    .sub-title { text-align: center; color: #8B949E; font-size: 0.95rem; margin-bottom: 30px; }
    .stChatMessage { background-color: #161B22 !important; border: 1px solid #30363D !important; border-radius: 12px !important; margin-bottom: 12px !important; }
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🦖 T-REX AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Free Unlimited AI • No Key Needed</div>', unsafe_allow_html=True)

# Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Old Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
if prompt := st.chat_input("Ask T-Rex anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("T-Rex is thinking..."):
            try:
                # Direct Fast Public Endpoint
                encoded_prompt = urllib.parse.quote(prompt)
                url = f"https://text.pollinations.ai/{encoded_prompt}?model=openai&system=You%20are%20T-Rex%20AI,%20a%20helpful%20assistant"
                
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200 and response.text.strip():
                    reply = response.text
                    st.write(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    st.error("Engine busy! Please ask again.")
            except Exception as e:
                st.error("Network issue, please try again!")
