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
        box-shadow: 0 0 20px rgba(0, 255, 135, 0.15);
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

# Custom Component for Real-time Mouse Trail Waves
components.html("""
<script>
const parentDoc = window.parent.document;
let canvas = parentDoc.getElementById('mouse-wave-canvas');

if (!canvas) {
    canvas = parentDoc.createElement('canvas');
    canvas.id = 'mouse-wave-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '99999';
    parentDoc.body.appendChild(canvas);
}

const ctx = canvas.getContext('2d');
let width = canvas.width = parentDoc.defaultView.innerWidth;
let height = canvas.height = parentDoc.defaultView.innerHeight;

parentDoc.defaultView.addEventListener('resize', () => {
    width = canvas.width = parentDoc.defaultView.innerWidth;
    height = canvas.height = parentDoc.defaultView.innerHeight;
});

let particles = [];

parentDoc.addEventListener('mousemove', (e) => {
    for (let i = 0; i < 3; i++) {
        particles.push({
            x: e.clientX,
            y: e.clientY,
            size: Math.random() * 8 + 2,
            speedX: (Math.random() - 0.5) * 2,
            speedY: (Math.random() - 0.5) * 2,
            color: Math.random() > 0.5 ? '#00FF87' : '#60EFFF',
            alpha: 1
        });
    }
});

function draw() {
    ctx.clearRect(0, 0, width, height);
    for (let i = 0; i < particles.length; i++) {
        let p = particles[i];
        ctx.save();
        ctx.globalAlpha = p.alpha;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.shadowBlur = 12;
        ctx.shadowColor = p.color;
        ctx.fill();
        ctx.restore();

        p.x += p.speedX;
        p.y += p.speedY;
        p.size *= 0.95;
        p.alpha -= 0.02;

        if (p.alpha <= 0 || p.size <= 0.5) {
            particles.splice(i, 1);
            i--;
        }
    }
    requestAnimationFrame(draw);
}
draw();
</script>
""", height=0)

# Main UI Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
    <div class="sub-title">Interactive Mouse Glow Trail Active</div>
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
        response = f"Mouse Wave Effect Active! Received: '{prompt}'"
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
