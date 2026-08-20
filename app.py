import streamlit as st
import streamlit.components.v1 as components
import pypdf
import io
import re
import math
from collections import Counter

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
        backdrop-filter: blur(16px);
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

# Fluid Waves Animation
components.html("""
<script>
const parentDoc = window.parent.document;
let canvas = parentDoc.getElementById('fluid-wave-canvas');

if (!canvas) {
    canvas = parentDoc.createElement('canvas');
    canvas.id = 'fluid-wave-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '0';
    parentDoc.body.appendChild(canvas);
}

const ctx = canvas.getContext('2d');
let width = canvas.width = parentDoc.defaultView.innerWidth;
let height = canvas.height = parentDoc.defaultView.innerHeight;

let mouse = { x: width / 2, y: height / 2, targetX: width / 2, targetY: height / 2 };

parentDoc.addEventListener('mousemove', (e) => {
    mouse.targetX = e.clientX;
    mouse.targetY = e.clientY;
});

let step = 0;

function renderFluidWaves() {
    ctx.clearRect(0, 0, width, height);
    mouse.x += (mouse.targetX - mouse.x) * 0.05;
    mouse.y += (mouse.targetY - mouse.y) * 0.05;
    step += 0.015;

    for (let i = 0; i < 5; i++) {
        ctx.beginPath();
        ctx.lineWidth = 1.5;
        
        let colorGrad = ctx.createLinearGradient(0, 0, width, 0);
        colorGrad.addColorStop(0, 'rgba(0, 255, 135, 0.02)');
        colorGrad.addColorStop(0.5, i % 2 === 0 ? 'rgba(0, 255, 135, 0.12)' : 'rgba(96, 239, 255, 0.12)');
        colorGrad.addColorStop(1, 'rgba(96, 239, 255, 0.02)');
        ctx.strokeStyle = colorGrad;

        for (let x = 0; x <= width; x += 20) {
            let dx = x - mouse.x;
            let distSq = dx * dx;
            let mouseEffect = Math.exp(-distSq / (180 * 180)) * (mouse.y - height / 2) * 0.35;
            let y = height / 2 + Math.sin(x * 0.005 + step + i * 0.8) * 45 + Math.cos(x * 0.008 - step + i) * 20 + mouseEffect;

            if (x === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.stroke();
    }
    requestAnimationFrame(renderFluidWaves);
}
renderFluidWaves();
</script>
""", height=0)

# Main UI Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
</div>
""", unsafe_allow_html=True)

# Document Text Parsing Engine
def extract_document_text(files):
    text_data = ""
    for file in files:
        if file.type == "application/pdf":
            reader = pypdf.PdfReader(io.BytesIO(file.read()))
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_data += extracted + "\n"
        elif file.type in ["text/plain", "text/markdown"]:
            text_data += file.read().decode("utf-8") + "\n"
    return text_data

# Built-in Pure Vector Cosine Similarity Search Engine
def cosine_similarity_search(query, text, top_k):
    # Sentence Chunking
    sentences = re.split(r'(?<=[.?!])\s+', text)
    chunks = [s.strip() for s in sentences if len(s.strip()) > 15]

    if not chunks:
        return []

    # Vectorizer
    def text_to_vector(text_str):
        words = re.findall(r'\w+', text_str.lower())
        return Counter(words)

    query_vec = text_to_vector(query)

    scores = []
    for chunk in chunks:
        chunk_vec = text_to_vector(chunk)
        intersection = set(query_vec.keys()) & set(chunk_vec.keys())
        
        numerator = sum([query_vec[x] * chunk_vec[x] for x in intersection])
        sum1 = sum([query_vec[x]**2 for x in query_vec.keys()])
        sum2 = sum([chunk_vec[x]**2 for x in chunk_vec.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        score = numerator / denominator if denominator else 0.0
        scores.append((score, chunk))

    scores.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scores[:top_k] if item[0] > 0]

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Control Bar
col_toggle, col_space, col_model = st.columns([1.5, 4, 2])

with col_toggle:
    attach_file = st.popover("📎 Attach Document")

with col_model:
    model_choice = st.selectbox("", ["Flash ⚡", "Pro 🧠", "Ultra 🚀"], label_visibility="collapsed")

uploaded_files = attach_file.file_uploader(
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
if prompt := st.chat_input("Ask T-Rex about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🦖"):
        if uploaded_files:
            raw_text = extract_document_text(uploaded_files)
            if raw_text.strip():
                k_val = 3 if model_choice == "Flash ⚡" else 5 if model_choice == "Pro 🧠" else 8
                relevant_chunks = cosine_similarity_search(prompt, raw_text, top_k=k_val)

                if relevant_chunks:
                    reply = f"**🦖 T-Rex RAG Agent Analysis ({model_choice}):**\n\n"
                    for idx, chunk in enumerate(relevant_chunks, 1):
                        reply += f"• **Match {idx}:** {chunk}\n\n"
                else:
                    reply = f"Document lo '{prompt}' ki direct semantic matches dorakaledu bro. Try broader terms."
            else:
                reply = "Document text extract avvaledu. Valid PDF/TXT file upload cheyandi."
        else:
            reply = f"T-Rex RAG Agent Active ({model_choice})! Upload document to search with local vector similarity."

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
