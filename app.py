import streamlit as st

# Page Config
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Custom Sleek Dark Neon UI
st.markdown("""
<style>
    /* Dark Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        color: #f0f6fc;
    }
    
    /* Modern Glassmorphism Header */
    .header-container {
        text-align: center;
        padding: 20px 10px;
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 25px;
    }

    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00FF87 0%, #60EFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }

    .sub-title {
        color: #8b949e;
        font-size: 1rem;
        font-weight: 400;
    }

    /* Custom Chat Message Bubbles */
    .stChatMessage {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    /* Input Box Styling */
    .stChatInputContainer {
        border-radius: 20px !important;
        border: 1px solid #30363d !important;
    }

    /* Hide Unnecessary Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main UI Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
    <div class="sub-title">Next-Gen Intelligent Conversational Interface</div>
</div>
""", unsafe_allow_html=True)

# Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input Box
if prompt := st.chat_input("Message T-Rex AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = f"UI updated successfully! Demo response for: '{prompt}'"
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
