import streamlit as st
import pypdf
import io
import re
import math
from collections import Counter

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

# Title Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
</div>
""", unsafe_allow_html=True)

# Extract Text From Uploaded PDF/TXT Files
def extract_text_from_doc(files):
    extracted_text = ""
    for file in files:
        if file.type == "application/pdf":
            pdf_reader = pypdf.PdfReader(io.BytesIO(file.read()))
            for page in pdf_reader.pages:
                txt = page.extract_text()
                if txt:
                    extracted_text += txt + "\n"
        elif file.type in ["text/plain", "text/markdown"]:
            extracted_text += file.read().decode("utf-8") + "\n"
    return extracted_text

# Search Context Matching Algorithm (No External Key Needed)
def get_accurate_answers(query, full_text, top_count):
    sentences = re.split(r'(?<=[.?!])\s+', full_text)
    clean_sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    if not clean_sentences:
        return []

    def get_word_vector(text):
        words = re.findall(r'\w+', text.lower())
        return Counter(words)

    q_vector = get_word_vector(query)
    sentence_matches = []

    for sentence in clean_sentences:
        s_vector = get_word_vector(sentence)
        common_words = set(q_vector.keys()) & set(s_vector.keys())
        
        num = sum([q_vector[w] * s_vector[w] for w in common_words])
        den1 = sum([q_vector[w]**2 for w in q_vector.keys()])
        den2 = sum([s_vector[w]**2 for w in s_vector.keys()])
        denom = math.sqrt(den1) * math.sqrt(den2)

        match_score = num / denom if denom else 0.0
        sentence_matches.append((match_score, sentence))

    sentence_matches.sort(key=lambda x: x[0], reverse=True)
    return [match[1] for match in sentence_matches[:top_count] if match[0] > 0]

# Session State Initializer
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header Dropdowns Bar
col_attach, col_gap, col_model = st.columns([1.5, 4, 2])

with col_attach:
    attach_pop = st.popover("📎 Attach Document")

with col_model:
    model_mode = st.selectbox("", ["Flash ⚡", "Pro 🧠", "Ultra 🚀"], label_visibility="collapsed")

uploaded_files = attach_pop.file_uploader(
    "Upload PDF or TXT", 
    type=["pdf", "txt"], 
    accept_multiple_files=True
)

# Render Chat History
for msg in st.session_state.messages:
    icon = "👤" if msg["role"] == "user" else "🦖"
    with st.chat_message(msg["role"], avatar=icon):
        st.write(msg["content"])

# Main Chat Query Processing
if prompt := st.chat_input("Document gurinchi emaina adugu bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🦖"):
        if uploaded_files:
            document_content = extract_text_from_doc(uploaded_files)
            if document_content.strip():
                limit = 3 if model_mode == "Flash ⚡" else 5 if model_mode == "Pro 🧠" else 8
                matched_answers = get_accurate_answers(prompt, document_content, top_count=limit)

                if matched_answers:
                    reply = f"**🦖 T-Rex Analysis Results ({model_mode}):**\n\n"
                    for idx, point in enumerate(matched_answers, 1):
                        reply += f"• **Point {idx}:** {point}\n\n"
                else:
                    reply = f"Document lo '{prompt}' ki matching details em dorakaledu bro. Try different search terms."
            else:
                reply = "Document text extract avvaledu, valid PDF/TXT file upload cheyi bro."
        else:
            reply = f"T-Rex Engine Ready ({model_mode})! Document attach chesi question aduguthe document analysis start avutundi."

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
