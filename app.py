import streamlit as st
import pypdf
import io
import re
from sentence_transformers import SentenceTransformer, util

# Page Config
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Dark Neon Theme UI
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

# Main Title Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
</div>
""", unsafe_allow_html=True)

# Load Local AI Embeddings Model (No Keys Required)
@st.cache_resource
def load_embed_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

embed_model = load_embed_model()

# Extract Text From PDF
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

# Topic Extractor without Duplicate Numbers
def extract_clean_topics(text):
    lines = text.split("\n")
    topics = []
    for line in lines:
        clean = line.strip()
        # Clean heading patterns
        if re.match(r'^(?:\d+\.\d*|\d+\b|[A-Z0-9\s\.\-]{3,50})$', clean) or (len(clean) < 60 and clean.istitle()):
            # Strip extra starting digits to fix double numbering bug
            cleaned_title = re.sub(r'^\d+[\.\s\-]+', '', clean)
            if cleaned_title and cleaned_title not in topics and len(cleaned_title) > 3:
                topics.append(cleaned_title)
    return topics[:12]

# AI Vector Similarity Search
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
        if score.item() > 0.25:  # Similarity threshold
            matched_chunks.append(chunks[idx.item()])

    return matched_chunks

# Session State Initializer
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

# Render Chat History
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
        
        # Conversational handling for casual inputs like "ok", "hi"
        casual_replies = {
            "ok": "Got it! Let me know if you need anything else from the document.",
            "okay": "Sure! Ask me any question about your PDF.",
            "hi": "Hello! Upload your document and ask me anything.",
            "hello": "Hey there! How can I help you analyze your document?",
            "thanks": "You're welcome! Glad to help.",
            "thank you": "You're welcome!"
        }

        if prompt_lower in casual_replies:
            reply = casual_replies[prompt_lower]
        elif uploaded_files:
            raw_text = extract_pdf_text(uploaded_files)
            if raw_text.strip():
                topic_triggers = ["topic", "topics", "heading", "headings", "index", "contents", "table of contents"]
                is_topic_request = any(t in prompt_lower for t in topic_triggers)

                if is_topic_request:
                    topics = extract_clean_topics(raw_text)
                    if topics:
                        reply = f"**🦖 PDF Document Topics ({model_choice}):**\n\n"
                        for idx, topic in enumerate(topics, 1):
                            reply += f"• **{topic}**\n"
                    else:
                        reply = "No distinct topic headings were detected in this document."
                else:
                    k_val = 2 if model_choice == "Flash ⚡" else 3 if model_choice == "Pro 🧠" else 5
                    results = semantic_search(prompt, raw_text, top_k=k_val)

                    if results:
                        reply = f"**🦖 T-Rex Analysis Results ({model_choice}):**\n\n"
                        for idx, res in enumerate(results, 1):
                            # Clean up redundant internal numbering
                            clean_res = re.sub(r'^\d+[\.\s\-]+', '', res)
                            reply += f"**Point {idx}:**\n{clean_res}\n\n---\n\n"
                    else:
                        reply = f"I couldn't find any relevant details for '{prompt}' in the document. Please try asking with different terms."
            else:
                reply = "The uploaded file appears to be empty."
        else:
            reply = f"T-Rex Active ({model_choice})! Please attach a PDF or TXT document using the 📎 button to start analyzing."

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
