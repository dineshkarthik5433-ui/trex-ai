import streamlit as st
from google import genai

# Page Config
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Custom Styling (Sleek Dark Theme)
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* Header Styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00FF87 0%, #60EFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .sub-title {
        text-align: center;
        color: #8B949E;
        font-size: 0.95rem;
        margin-bottom: 30px;
    }

    /* Chat Messages Box */
    .stChatMessage {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin-bottom: 12px !important;
    }

    /* Hide Sidebar / Footer Fluff */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Custom Header
st.markdown('<div class="main-title">🦖 T-REX AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Powered by Gemini 3.6 Flash • Always Ready</div>', unsafe_allow_html=True)

# Fetch Key directly from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", None)

# Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
if prompt := st.chat_input("Ask T-Rex anything..."):
    if not api_key:
        st.error("API Key not found in Streamlit Secrets! Please check Secrets setup.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        client = genai.Client(api_key=api_key)
        
        with st.chat_message("assistant"):
            with st.spinner("T-Rex is thinking..."):
                system_prompt = f"You are T-Rex AI, a smart AI assistant. Answer: {prompt}"
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=system_prompt
                )
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Error: {e}")
