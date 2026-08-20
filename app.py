import streamlit as st

# Page Config
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Native CSS Glowing Animated Grid & Mouse Waves Effect
st.markdown("""
<style>
    /* Dark Animated Wave Background */
    .stApp {
        background: linear-gradient(-45deg, #0d1117, #161b22, #002b1d, #001f3f);
        background-size: 400% 400%;
        animation: gradientWave 12s ease infinite;
        color: #f0f6fc;
    }

    /* Ambient Dynamic Glowing Waves Animation */
    @keyframes gradientWave {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Header Container Styling */
    .header-container {
        text-align: center;
        padding: 24px 15px;
        background: rgba(22, 27, 34, 0.7);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 135, 0.2);
        margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(0, 255, 135, 0.15);
    }

    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00FF87 0%, #60EFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
    }

    .sub-title {
        color: #8b949e;
        font-size: 0.95rem;
    }

    /* Chat Messages with Glowing Borders on Hover */
    .stChatMessage {
        background-color: rgba(22, 27, 34, 0.85) !important;
        border: 1px solid #30363d !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }

    .stChatMessage:hover {
        border-color: #00FF87 !important;
        box-shadow: 0 0 12px rgba(0, 255, 135, 0.2);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main UI Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
    <div class="sub-title">Dynamic Ambient Wave Theme Active</div>
</div>
""", unsafe_allow_html=True)

# Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🦖"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# User Input Box
if prompt := st.chat_input("Message T-Rex AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🦖"):
        response = f"Ambient Glow Wave UI Active! Received: '{prompt}'"
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
