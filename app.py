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
st.markdown('<div class="sub-title">Powered by Gemini 3.6 Flash</div>', unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY", None)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask T-Rex anything..."):
    if not api_key:
        st.error("API Key not found in Streamlit Secrets!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        client = genai.Client(api_key=api_key)
        
        with st.chat_message("assistant"):
            system_prompt = f"You are T-Rex AI, a helpful, witty, and smart AI assistant. Answer concisely and quickly: {prompt}"
            
            response_stream = client.models.generate_content_stream(
                model='gemini-3.6-flash',
                contents=system_prompt
            )
            
            message_placeholder = st.empty()
            full_response = ""
            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
                
    except Exception as e:
        st.error(f"Error: {e}")
