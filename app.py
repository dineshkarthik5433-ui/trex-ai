import streamlit as st

# Page Config
st.set_page_config(
    page_title="T-Rex AI",
    page_icon="🦖",
    layout="centered"
)

# Interactive Background Wave Effect (HTML/CSS Script)
st.markdown("""
<style>
    /* Dark Theme Base */
    .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
    }

    /* Interactive Mouse Canvas Overlay */
    #bg-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        pointer-events: none;
    }

    /* Keep UI elements above background */
    .block-container, .header-container, .stChatMessage, .stChatInputContainer {
        position: relative;
        z-index: 1 !important;
    }

    /* Header Styling */
    .header-container {
        text-align: center;
        padding: 24px 15px;
        background: rgba(22, 27, 34, 0.7);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
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

    /* Chat Messages */
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

<!-- Canvas for Interactive Waves/Glow -->
<canvas id="bg-canvas"></canvas>

<script>
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');

let width = canvas.width = window.innerWidth;
let height = canvas.height = window.innerHeight;

window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
});

let mouse = { x: width / 2, y: height / 2 };
let waves = [];

window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
    
    // Create new wave particle on mouse move
    if (Math.random() > 0.3) {
        waves.push({
            x: mouse.x,
            y: mouse.y,
            radius: 5,
            maxRadius: 120 + Math.random() * 80,
            alpha: 0.6,
            color: Math.random() > 0.5 ? '#00FF87' : '#60EFFF'
        });
    }
});

function animate() {
    ctx.clearRect(0, 0, width, height);
    
    for (let i = 0; i < waves.length; i++) {
        let w = waves[i];
        ctx.beginPath();
        ctx.arc(w.x, w.y, w.radius, 0, Math.PI * 2);
        ctx.strokeStyle = w.color;
        ctx.globalAlpha = w.alpha;
        ctx.lineWidth = 2;
        ctx.stroke();
        
        w.radius += 2.5;
        w.alpha -= 0.012;
        
        if (w.alpha <= 0 || w.radius >= w.maxRadius) {
            waves.splice(i, 1);
            i--;
        }
    }
    
    requestAnimationFrame(animate);
}
animate();
</script>
""", unsafe_allow_html=True)

# Main UI Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🦖 T-REX AI</div>
    <div class="sub-title">Interactive Wave Background UI</div>
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
        response = f"Interactive Wave UI active! Received: '{prompt}'"
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
