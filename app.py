import streamlit as st

# Page Config
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Advanced Sleek UI Styling
st.markdown("""
<style>
    /* Dark Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        color: #f0f6fc;
    }
    
    /* Header Card Styling */
    .header-container {
        text-align: center;
        padding: 24px 15px;
        background: rgba(22, 27, 34, 0.7);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
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

    /* Custom Chat Message Cards */
    .stChatMessage {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
    }

    /* Hide Unnecessary Streamlit UI Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main Header Area
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
    <div class="sub-title">Next-Gen Intelligent Interface • Custom Avatars & Quick Actions</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Options
with st.sidebar:
    st.title("⚙️ T-Rex Settings")
    st.write("UI Version: **2.0 Ultra**")
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Memory State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages with Custom Avatars
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🦖"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# Quick Suggestion Buttons (If No Messages Yet)
if not st.session_state.messages:
    st.write("**Suggested Prompts:**")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💡 Tell me a cool science fact", use_container_width=True):
            st.session_state.selected_prompt = "Tell me a cool science fact"
    with col2:
        if st.button("💻 Write a Python Hello World code", use_container_width=True):
            st.session_state.selected_prompt = "Write a Python Hello World code"

# Input Handling
prompt = st.chat_input("Message T-Rex AI...")

if "selected_prompt" in st.session_state and st.session_state.selected_prompt:
    prompt = st.session_state.selected_prompt
    del st.session_state["selected_prompt"]

if prompt:
    # Render User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    # Render Assistant Reply with Dino Avatar
    with st.chat_message("assistant", avatar="🦖"):
        response = f"Custom UI Active! Received: '{prompt}'"
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
