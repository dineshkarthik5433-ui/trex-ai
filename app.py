import streamlit as st
import pypdf
import io
import re
import requests
from sentence_transformers import SentenceTransformer, util

# Page Configuration
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Custom Styling (Dark Neon Theme)
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f17;
        color: #f0f6fc;
    }

    .header-container {
        text-align: center;
        padding: 15px;
        background: rgba(22, 27, 34, 0.85);
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

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main Title
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
</div>
""", unsafe_allow_html=True)

# Load Local Vector Model
@st.cache_resource
def load_embed_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

embed_model = load_embed_model()

# PDF Extractor
def extract_pdf_text(files):
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

# Free Conversational AI Engine (No API Key Required)
def query_free_ai(prompt):
    try:
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + prompt.split()[-1]
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            meaning = data[0]['meanings'][0]['definitions'][0]['definition']
            return f"Here is what I found regarding **{prompt.split()[-1]}**: {meaning}"
    except Exception:
        pass
    
    return f"I am T-Rex AI, your document analysis assistant! I am currently running in **{model_choice}** mode. Upload a PDF or TXT file using the 📎 button to extract summaries and answer questions."

# Semantic Vector Search
def semantic_search(query, text, top_k):
    chunks = [c.strip() for c in text.split("\n\n") if len(c.strip()) > 30]
    if not chunks:
        chunks = [c.strip() for c in text.split("\n") if len(c.strip()) > 30]

    if not chunks:
        return []

    query_embedding = embed_model.encode(query, convert_to_tensor=True)
    chunk_embeddings = embed_model.encode(chunks, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, chunk_embeddings)[0]
    top_results = scores.topk(k=min(top_k, len(chunks)))

    matched_chunks = []
    for score, idx in zip(top_results[0], top_results[1]):
        if score.item() > 0.2:
            matched_chunks.append(chunks[idx.item()])

    return matched_chunks

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header Dropdowns Bar
col_attach, col_gap, col_model = st.columns([1.5, 4, 2])

with col_attach:
    attach_pop = st.popover("📎 Attach Document")

with col_model:
    model_choice = st.selectbox("", ["Flash ⚡", "Pro 🧠", "Ultra 🚀"], label_visibility="collapsed")

uploaded_files = attach_pop.file_uploader(
    "Upload PDF or TXT files", 
    type=["pdf", "txt"], 
    accept_multiple_files=True
)

# Display Messages
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🦖"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# User Chat Input
if prompt := st.chat_input("Ask T-Rex AI anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🦖"):
        prompt_lower = prompt.lower().strip()

        # Conversational Intents Map
        conversational_intents = {
            "hi": "Hello! How can I help you today?",
            "hello": "Hey there! Upload a document or ask me a question.",
            "what are you doing": "I am standing by to help you read, analyze, and extract key points from your documents!",
            "who are you": "I am T-Rex AI, a document analysis and question-answering assistant.",
            "which type you": "I am an AI document analysis engine designed to extract information from PDFs and text files.",
            "what can you do": "I can read PDF/TXT files, extract topic outlines, and find answers to specific questions in your documents."
        }

        if prompt_lower in conversational_intents:
            reply = conversational_intents[prompt_lower]
        elif uploaded_files:
            raw_text = extract_pdf_text(uploaded_files)
            if raw_text.strip():
                k_val = 2 if model_choice == "Flash ⚡" else 3 if model_choice == "Pro 🧠" else 5
                results = semantic_search(prompt, raw_text, top_k=k_val)

                if results:
                    reply = f"**🦖 Analysis Results ({model_choice}):**\n\n"
                    for idx, res in enumerate(results, 1):
                        clean_res = re.sub(r'^\d+[\.\s\-]+', '', res)
                        reply += f"**Point {idx}:**\n{clean_res}\n\n---\n\n"
                else:
                    reply = f"I couldn't find relevant details for '{prompt}' in the attached document."
            else:
                reply = "The attached document contains no readable text."
        else:
            reply = query_free_ai(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
