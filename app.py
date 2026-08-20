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
        background-color: #0b0f17;
        color: #f0f6fc;
    }

    .header-container {
        text-align: center;
        padding: 24px 15px;
        background: rgba(22, 27, 34, 0.75);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 135, 0.2);
        margin-bottom: 20px;
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

    /* Custom File Uploader Style */
    .stFileUploader {
        background: rgba(22, 27, 34, 0.8) !important;
        border: 1px dashed rgba(0, 255, 135, 0.4) !important;
        border-radius: 16px !important;
        padding: 10px !important;
        margin-bottom: 20px !important;
        backdrop-filter: blur(8px);
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

# Interactive Fluid Waves Component
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

# Main Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
    <div class="sub-title">Multimodal Supported AI Interface</div>
</div>
""", unsafe_allow_html=True)

# File Attachment Box (Upload Documents, Videos, Audios, Images)
uploaded_files = st.file_uploader(
    "📎 Attach Files, Documents, Audio, or Videos...",
    type=["pdf", "txt", "docx", "mp3", "wav", "mp4", "mov", "png", "jpg"],
    accept_multiple_files=True
)

# File Preview Logic
if uploaded_files:
    st.write("📂 **Uploaded Attachments:**")
    for file in uploaded_files:
        file_ext = file.name.split('.')[-1].lower()
        if file_ext in ["png", "jpg", "jpeg"]:
            st.image(file, width=250)
        elif file_ext in ["mp3", "wav"]:
            st.audio(file)
        elif file_ext in ["mp4", "mov"]:
            st.video(file)
        else:
            st.info(file.name)

# Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Previous Chat Messages
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "REX"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# Chat Input Box
if prompt := st.chat_input("Message T-Rex AI or ask about attached files..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🦖"):
        if uploaded_files:
            file_names = ", ".join([f.name for f in uploaded_files])
            response = f"Received your prompt: '{prompt}' along with attached file(s): [{file_names}]."
        else:
            response = f"Received prompt: '{prompt}'"

        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
