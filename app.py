import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Custom High-Performance CSS (Zero Flickering)
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

    /* Unified Bottom Input Pill Container */
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

    /* Clean Chat Message Styling */
    .stChatMessage {
        background-color: rgba(22, 27, 34, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
    }

    /* Minimal Top Selector Bar */
    .control-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0px 10px;
        margin-bottom: 10px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Smooth Fluid Waves Background Engine
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
</div>
""", unsafe_allow_html=True)

# State Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Top Model & Media Controls
col_toggle, col_space, col_model = st.columns([1.5, 4, 2])

with col_toggle:
    attach_file = st.popover("📎 Attach File")

with col_model:
    model_type = st.selectbox("", ["Flash ⚡", "Pro 🧠", "Ultra 🚀"], label_visibility="collapsed")

# Handle File Attachment inside popover to keep interface clean
uploaded_files = attach_file.file_uploader("Upload Documents or Media", accept_multiple_files=True)

# Render Chat History
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🦖"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# Native Native Chat Input (Prevents Input Glitches)
if prompt := st.chat_input("Ask T-Rex..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    # Generate Response
    with st.chat_message("assistant", avatar="🦖"):
        if uploaded_files:
            files_str = ", ".join([f.name for f in uploaded_files])
            response = f"Processed '{prompt}' with uploaded files: [{files_str}] using {model_type}."
        else:
            response = f"Response for: '{prompt}' using {model_type}."
        
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
