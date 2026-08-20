import streamlit as st
import pypdf
import io
import re

# Page Configuration
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Dark Neon Styling
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

# Extract Text From Uploaded Files
def extract_text(files):
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

# Clean Heading & Topic Extractor
def extract_document_topics(text):
    # Regex to capture section titles like 1.1, 1.2, Chapter names, or short heading lines
    lines = text.split("\n")
    topics = []
    
    for line in lines:
        clean = line.strip()
        # Heading filters: section numbers or short uppercase/title-case lines
        if re.match(r'^(?:\d+\.\d*|\d+\b|[A-Z0-9\s\.\-]{3,50})$', clean) or (len(clean) < 60 and clean.istitle()):
            if clean not in topics and len(clean) > 3:
                topics.append(clean)
                
    if not topics:
        # Fallback: take first lines of paragraphs
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 30]
        for p in paragraphs[:10]:
            first_line = p.split("\n")[0].strip()
            if first_line not in topics:
                topics.append(first_line[:60])
                
    return topics[:15]

# Specific Query Content Search Engine
def search_specific_query(query, text, limit):
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 40]
    if not paragraphs:
        paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 40]

    keywords = set(re.findall(r'\b[a-zA-Z]{3,}\b', query.lower())) - {"what", "how", "why", "give", "tell", "explain", "this", "that"}
    
    results = []
    for p in paragraphs:
        p_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', p.lower()))
        match_count = len(keywords & p_words)
        if match_count > 0:
            results.append((match_count, p))
            
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results[:limit]]

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Control Bar
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

# User Chat Input Handling
if prompt := st.chat_input("Document gurinchi emaina adugu bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🦖"):
        if uploaded_files:
            raw_text = extract_text(uploaded_files)
            if raw_text.strip():
                # Check if user is asking for topic list
                topic_triggers = ["topic", "topics", "heading", "headings", "index", "contents", "table of contents", "outline"]
                is_topic_request = any(trigger in prompt.lower() for trigger in topic_triggers)

                if is_topic_request:
                    topics_list = extract_document_topics(raw_text)
                    if topics_list:
                        response_md = f"**🦖 PDF Document Topics ({model_choice}):**\n\n"
                        for idx, topic in enumerate(topics_list, 1):
                            response_md += f"{idx}. **{topic}**\n"
                    else:
                        response_md = "Document lo clear headings emi detect avvaledu bro."
                else:
                    limit = 2 if model_choice == "Flash ⚡" else 3 if model_choice == "Pro 🧠" else 5
                    matched = search_specific_query(prompt, raw_text, limit)
                    if matched:
                        response_md = f"**🦖 Analysis Answer ({model_choice}):**\n\n"
                        for idx, chunk in enumerate(matched, 1):
                            response_md += f"**Point {idx}:**\n{chunk}\n\n---\n\n"
                    else:
                        response_md = f"Document lo '{prompt}' ki matching details em dorakaledu bro."

                st.write(response_md)
                st.session_state.messages.append({"role": "assistant", "content": response_md})
            else:
                st.write("Uploaded file lo text emi ledhu bro.")
        else:
            st.write(f"T-Rex Active ({model_choice})! Document upload chesi question adugu bro.")
