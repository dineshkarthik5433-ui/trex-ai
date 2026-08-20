import streamlit as st
import pypdf
import io
import re
from transformers import pipeline

# Page Config
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Custom High-Performance Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f17;
        color: #f0f6fc;
    }

    .header-container {
        text-align: center;
        padding: 15px;
        background: rgba(22, 27, 34, 0.65);
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 135, 0.25);
        margin-bottom: 20px;
    }

    .main-title {
        font-size: 2.3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00FF87 0%, #60EFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    div[data-testid="stChatInput"] {
        background-color: #1e1e1e !important;
        border: 1px solid #333333 !important;
        border-radius: 40px !important;
        padding: 6px 14px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        font-size: 1rem !important;
    }

    .stChatMessage {
        background-color: rgba(22, 27, 34, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
    }

    .topic-box {
        background: rgba(0, 255, 135, 0.05);
        border-left: 4px solid #00FF87;
        padding: 10px 15px;
        margin-bottom: 15px;
        border-radius: 4px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main Title Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
</div>
""", unsafe_allow_html=True)

# Document Text Extractor
def extract_document_text(files):
    full_text = ""
    for file in files:
        if file.type == "application/pdf":
            reader = pypdf.PdfReader(io.BytesIO(file.read()))
            for page in reader.pages:
                txt = page.extract_text()
                if txt:
                    full_text += txt + "\n"
        elif file.type in ["text/plain", "text/markdown"]:
            full_text += file.read().decode("utf-8") + "\n"
    return full_text

# Structural Topic Segmenter Logic
def find_topic_segments(query, text, mode_limit):
    # Separate topics by headings or section numbers (e.g., 1.1, 1.2, or All Caps)
    sections = re.split(r'\n(?=[0-9]+\.[0-9]+|[A-Z\s]{4,}:)', text)
    
    if len(sections) < 2:
        sections = [s.strip() for s in text.split("\n\n") if len(s.strip()) > 50]

    query_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', query.lower()))
    stopwords = {"what", "how", "why", "give", "tell", "topics", "pdf", "this", "that", "there"}
    filtered_query = query_words - stopwords

    matched_results = []

    for section in sections:
        section_lower = section.lower()
        # Calculate overlap score
        score = sum(1 for word in filtered_query if word in section_lower)
        if score > 0 or not filtered_query:
            # Extract First Line as Topic Title
            lines = [l.strip() for l in section.split("\n") if l.strip()]
            topic_title = lines[0] if lines else "General Topic"
            content = " ".join(lines[1:]) if len(lines) > 1 else section
            matched_results.append((score, topic_title, content))

    matched_results.sort(key=lambda x: x[0], reverse=True)
    return matched_results[:mode_limit]

# Session State Initializer
if "messages" not in st.session_state:
    st.session_state.messages = []

# Control Bar
col_attach, col_space, col_model = st.columns([1.5, 4, 2])

with col_attach:
    attach_pop = st.popover("📎 Attach Document")

with col_model:
    model_choice = st.selectbox("", ["Flash ⚡", "Pro 🧠", "Ultra 🚀"], label_visibility="collapsed")

uploaded_files = attach_pop.file_uploader(
    "Upload PDF or TXT files", 
    type=["pdf", "txt"], 
    accept_multiple_files=True
)

# Render Chat History
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🦖"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# User Chat Input
if prompt := st.chat_input("Document gurinchi emaina adugu bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🦖"):
        if uploaded_files:
            raw_text = extract_document_text(uploaded_files)
            if raw_text.strip():
                limit = 2 if model_choice == "Flash ⚡" else 4 if model_choice == "Pro 🧠" else 7
                segments = find_topic_segments(prompt, raw_text, mode_limit=limit)

                if segments:
                    response_md = f"**🦖 T-Rex Structured Analysis ({model_choice}):**\n\n"
                    for idx, (score, title, body) in enumerate(segments, 1):
                        response_md += f"📌 **Topic {idx}: {title}**\n\n{body}\n\n---\n\n"
                    st.markdown(response_md)
                    st.session_state.messages.append({"role": "assistant", "content": response_md})
                else:
                    err_msg = f"Document lo '{prompt}' ki matching topics ledu bro."
                    st.write(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
            else:
                st.write("PDF lo text blank undi bro.")
        else:
            def_msg = f"T-Rex Ready ({model_choice})! Attach document option dwara PDF upload cheyi bro."
            st.write(def_msg)
            st.session_state.messages.append({"role": "assistant", "content": def_msg})
