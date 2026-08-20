import streamlit as st
import streamlit.components.v1 as components

# Page Config
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Base Dark Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
    }

    .header-container {
        text-align: center;
        padding: 24px 15px;
        background: rgba(22, 27, 34, 0.75);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 135, 0.2);
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(0, 255, 135, 0.1);
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

    .stChatMessage {
        background-color: rgba(22, 27, 34, 0.85) !important;
        border: 1px solid #30363d !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        backdrop-filter: blur(8px);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Soft & Subtle Interactive Mouse Spotlight
components.html("""
<script>
const parentDoc = window.parent.document;
let glowDiv = parentDoc.getElementById('mouse-glow-bg');

if (!glowDiv) {
    glowDiv = parentDoc.createElement('div');
    glowDiv.id = 'mouse-glow-bg';
    glowDiv.style.position = 'fixed';
    glowDiv.style.top = '0';
    glowDiv.style.left = '0';
    glowDiv.style.width = '100vw';
    glowDiv.style.height = '100vh';
    glowDiv.style.pointerEvents = 'none';
    glowDiv.style.zIndex = '0';
    glowDiv.style.transition = 'background 0.15s ease-out';
    parentDoc.body.appendChild(glowDiv);
}

parentDoc.addEventListener('mousemove', (e) => {
    const x = e.clientX;
    const y = e.clientY;
    
    // Very subtle, soft Radial Gradient Glow centered at mouse cursor
    glowDiv.style.background = `radial-gradient(400px circle at ${x}px ${y}px, rgba(0, 255, 135, 0.08), rgba(96, 239, 255, 0.04), transparent 80%)`;
});

parentDoc.addEventListener('mouseleave', () => {
    glowDiv.style.background = 'transparent';
});
</script>
""", height=0)

# Main UI Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
    <div class="sub-title">Soft Mouse Spotlight Active</div>
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
        response = f"Soft Glow UI Active! Received: '{prompt}'"
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
