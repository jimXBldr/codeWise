"""
DebugMind — AI Code Debugging Assistant
Streamlit Frontend
"""

import streamlit as st
import requests
import json

# Page config
st.set_page_config(
    page_title="DebugMind — AI Code Debugger",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

  /* ── Base reset ── */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d0f14;
    color: #e2e8f0;
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1100px;
  }

  /* ── Hero header ── */
  .dm-hero {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 6px;
  }
  .dm-logo {
    font-size: 2.4rem;
    line-height: 1;
  }
  .dm-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 55%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
  }
  .dm-tagline {
    font-size: 0.92rem;
    color: #64748b;
    font-weight: 400;
    margin-bottom: 2rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.3px;
  }
  .dm-tagline span {
    color: #38bdf8;
  }

  /* ── Card panels ── */
  .dm-card {
    background: #141720;
    border: 1px solid #1e2433;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
  }
  .dm-card-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.7rem;
  }

  /* ── Result section titles ── */
  .res-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    padding: 3px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 0.55rem;
  }
  .label-red   { background: #3b1219; color: #f87171; border: 1px solid #7f1d1d; }
  .label-amber { background: #2d1e08; color: #fbbf24; border: 1px solid #78350f; }
  .label-blue  { background: #0c1f3d; color: #60a5fa; border: 1px solid #1e3a5f; }
  .label-green { background: #052e16; color: #4ade80; border: 1px solid #14532d; }
  .label-purple{ background: #1e1147; color: #c084fc; border: 1px solid #3b0764; }

  .res-text {
    font-size: 0.95rem;
    color: #cbd5e1;
    line-height: 1.65;
  }

  /* ── Optimizations list ── */
  .opt-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 0;
    border-bottom: 1px solid #1e2433;
    font-size: 0.92rem;
    color: #cbd5e1;
    line-height: 1.55;
  }
  .opt-item:last-child { border-bottom: none; }
  .opt-bullet {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #c084fc;
    font-weight: 700;
    flex-shrink: 0;
    padding-top: 2px;
  }

  /* ── Divider ── */
  .dm-divider {
    border: none;
    border-top: 1px solid #1e2433;
    margin: 1.6rem 0;
  }

  /* ── Status pill ── */
  .status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 999px;
    letter-spacing: 0.5px;
  }
  .status-ok  { background: #052e16; color: #4ade80; border: 1px solid #166534; }
  .status-err { background: #3b1219; color: #f87171; border: 1px solid #991b1b; }

  /* ── Textarea / input overrides ── */
  textarea, .stTextArea textarea {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    background: #0d0f14 !important;
    color: #e2e8f0 !important;
    border: 1px solid #1e2433 !important;
    border-radius: 8px !important;
  }
  .stSelectbox > div > div {
    background: #141720 !important;
    border: 1px solid #1e2433 !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
  }

  /* ── Debug button ── */
  .stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    color: white !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 1px !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
  }
  .stButton > button:hover {
    opacity: 0.88 !important;
  }
</style>
""", unsafe_allow_html=True)

# Config
BACKEND_URL = "http://localhost:5000"

# Header
st.markdown("""
<div class="dm-hero">
  <div class="dm-logo">🧠</div>
  <h1 class="dm-title">DebugMind</h1>
</div>
<p class="dm-tagline">AI Code Debugging Assistant &nbsp;·&nbsp; <span>Powered by Groq × LLaMA 3.3</span></p>
""", unsafe_allow_html=True)

# Check backend health
@st.cache_data(ttl=30)
def check_health():
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

healthy = check_health()
if healthy:
    st.markdown('<span class="status-pill status-ok">⬤ &nbsp;API Connected</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="status-pill status-err">⬤ &nbsp;API Offline — start backend first</span>', unsafe_allow_html=True)

st.markdown("<hr class='dm-divider'>", unsafe_allow_html=True)

# Input layout
col_left, col_right = st.columns([3, 1])

with col_right:
    st.markdown('<div class="dm-card"><div class="dm-card-title" style="color:#818cf8">⚙ Options</div>', unsafe_allow_html=True)
    language = st.selectbox(
        "Language",
        ["Python", "JavaScript", "C++", "TypeScript", "Go", "Rust", "Java"],
        index=0,
        label_visibility="collapsed",
    )
    st.markdown(f"<p style='font-family:JetBrains Mono;font-size:0.72rem;color:#475569;margin-top:6px;'>Selected: <span style='color:#818cf8'>{language}</span></p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="dm-card"><div class="dm-card-title" style="color:#f59e0b">⚠ Error Message</div>', unsafe_allow_html=True)
    error_input = st.text_area(
        "Error",
        placeholder="Paste traceback or error here (optional)…",
        height=130,
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_left:
    st.markdown('<div class="dm-card"><div class="dm-card-title" style="color:#38bdf8">{'+'}'+" Code Input</div>", unsafe_allow_html=True)
    code_input = st.text_area(
        "Code",
        placeholder="# Paste your buggy code here…\ndef my_function():\n    pass",
        height=280,
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Debug button
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    debug_clicked = st.button("🔍  DEBUG CODE", use_container_width=True)

# Process + Display results
if debug_clicked:
    if not code_input.strip():
        st.warning("Please paste some code before clicking Debug.")
    elif not healthy:
        st.error("Backend is offline. Run `python app.py` inside the `backend/` folder first.")
    else:
        with st.spinner("DebugMind is analysing your code…"):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/debug",
                    json={
                        "code": code_input,
                        "error": error_input,
                        "language": language,
                    },
                    timeout=60,
                )
                data = resp.json()
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the backend. Make sure `python app.py` is running.")
                st.stop()
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
                st.stop()

        if "error" in data:
            st.error(f"**API Error:** {data['error']}")
            st.stop()

        st.markdown("<hr class='dm-divider'>", unsafe_allow_html=True)
        st.markdown("### 🔍 Debug Report", unsafe_allow_html=False)

        # Two-column results layout
        r_col1, r_col2 = st.columns(2)

        with r_col1:
            # Error Summary
            st.markdown(
                f'<div class="dm-card">'
                f'<span class="res-label label-red">Error Summary</span>'
                f'<p class="res-text">{data.get("error_summary", "N/A")}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
            # Root Cause
            st.markdown(
                f'<div class="dm-card">'
                f'<span class="res-label label-amber">Root Cause</span>'
                f'<p class="res-text">{data.get("root_cause", "N/A")}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
            # Optimizations
            opts = data.get("optimizations", [])
            if opts:
                items_html = "".join(
                    f'<div class="opt-item"><span class="opt-bullet">0{i+1}</span><span>{opt}</span></div>'
                    for i, opt in enumerate(opts)
                )
                st.markdown(
                    f'<div class="dm-card">'
                    f'<span class="res-label label-purple">Optimizations</span>'
                    f'{items_html}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        with r_col2:
            # Explanation
            st.markdown(
                f'<div class="dm-card">'
                f'<span class="res-label label-blue">Explanation</span>'
                f'<p class="res-text">{data.get("explanation", "N/A")}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # Fixed code — full width with syntax highlighting
        st.markdown('<span class="res-label label-green">Fixed Code</span>', unsafe_allow_html=True)
        fixed = data.get("fixed_code", "")
        lang_map = {
            "Python": "python", "JavaScript": "javascript",
            "C++": "cpp", "TypeScript": "typescript",
            "Go": "go", "Rust": "rust", "Java": "java",
        }
        st.code(fixed, language=lang_map.get(language, "python"))

        # Raw JSON expander for developers
        with st.expander("📦 Raw JSON Response"):
            st.json(data)