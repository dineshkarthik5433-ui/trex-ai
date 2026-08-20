import streamlit as st
import streamlit.components.v1 as components

# Page Config
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Base Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
    }

    .header-container {
        text-align: center;
        padding: 24px 15px;
        background: rgba(22, 27, 34, 0.75);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 135, 0.2);
        margin-bottom: 25px;
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

# Interactive Light Fluid Waves Component
components.html("""
<script>
const parentDoc = window.parent.document;
let canvas = parentDoc.getElementById('wave-canvas');

if (!canvas) {
    canvas = parentDoc.createElement('canvas');
    canvas.id = 'wave-canvas';
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

parentDoc.defaultView.addEventListener('resize', () => {
    width = canvas.width = parentDoc.defaultView.innerWidth;
    height = canvas.height = parentDoc.defaultView.innerHeight;
});

let ripples = [];

parentDoc.addEventListener('mousemove', (e) => {
    // Mouse move avthunnappudu soft wave rings append avthayi
    if (Math.random() > 0.2) {
        ripples.push({
            x: e.clientX,
            y: e.clientY,
            radius: 2,
            maxRadius: 45 + Math.random() * 25,
            alpha: 0.35,
            color: Math.random() > 0.5 ? '#00FF87' : '#60EFFF'
        });
    }
});

function drawWaves() {
    ctx.clearRect(0, 0, width, height);
    
    for (let i = 0; i < ripples.length; i++) {
        let r = ripples[i];
        
        ctx.save();
        ctx.beginPath();
        ctx.arc(r.x, r.y, r.radius, 0, Math.PI * 2);
        ctx.strokeStyle = r.color;
        ctx.lineWidth = 1.2;
        ctx.globalAlpha = r.alpha;
        ctx.stroke();
        ctx.restore();

        // Wave expanding effect
        r.radius += 1.2;
        r.alpha -= 0.008;

        if (r.alpha <= 0 || r.radius >= r.maxRadius) {
            ripples.splice(i, 1);
            i--;
        }
    }
    
    requestAnimationFrame(drawWaves);
}

drawWaves();
</script>
""", height=0)

# Main UI Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
    <div class="sub-title">Soft Interactive Ripple Waves Active</div>
</div>
""", unsafe_allow_html=True)

# Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🦖"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# User Input Box
if prompt := st.chat_input("Message T-Rex AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🦖"):
        response = f"Fluid Wave UI Active! Received: '{prompt}'"
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
