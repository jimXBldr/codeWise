"""
DebugMind — Professional Code Debugging Platform
Streamlit Frontend — Production Redesign
"""

import streamlit as st
import requests
import time
import uuid

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DebugMind",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%234F8CFF'/><path d='M8 16h16M16 8v16M10 10l12 12M22 10L10 22' stroke='white' stroke-width='2' stroke-linecap='round'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

  /* ── CSS Variables ── */
  :root {
    --bg:          #0B0D10;
    --surface:     #111418;
    --surface-2:   #171B21;
    --border:      #262B33;
    --border-hi:   #313843;
    --text-1:      #F5F7FA;
    --text-2:      #A8B0BB;
    --text-3:      #6F7883;
    --accent:      #4F8CFF;
    --accent-dim:  rgba(79, 140, 255, 0.12);
    --accent-glow: rgba(79, 140, 255, 0.06);
    --err:         #FF6B6B;
    --warn:        #FFB347;
    --ok:          #52D18C;
    --radius:      8px;
    --radius-lg:   12px;
  }

  /* ── Reset ── */
  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text-1);
  }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container {
    padding-top: 2.5rem;
    padding-bottom: 4rem;
    max-width: 1160px;
  }

  /* ── Subtle grid texture ── */
  .stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(79,140,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(79,140,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  /* ── Wordmark ── */
  .dm-wordmark {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 4px;
  }
  .dm-mark {
    width: 34px;
    height: 34px;
    background: var(--accent);
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .dm-mark svg { display: block; }
  .dm-name {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.55rem;
    font-weight: 600;
    color: var(--text-1);
    letter-spacing: -0.5px;
    margin: 0;
    line-height: 1;
  }
  .dm-version {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: var(--text-3);
    padding: 2px 7px;
    border: 1px solid var(--border);
    border-radius: 4px;
    letter-spacing: 0.5px;
    align-self: flex-end;
    margin-bottom: 1px;
  }
  .dm-sub {
    font-size: 0.83rem;
    color: var(--text-3);
    margin-bottom: 2rem;
    font-weight: 400;
    letter-spacing: 0.1px;
  }

  /* ── Header row ── */
  .dm-header-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1.8rem;
  }

  /* ── Status indicator ── */
  .status-chip {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    padding: 5px 12px;
    border-radius: 999px;
    letter-spacing: 0.3px;
    border: 1px solid;
  }
  .status-chip .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  .status-ok {
    background: rgba(82,209,140,0.08);
    color: var(--ok);
    border-color: rgba(82,209,140,0.2);
  }
  .status-ok .dot { background: var(--ok); box-shadow: 0 0 6px var(--ok); }
  .status-err {
    background: rgba(255,107,107,0.08);
    color: var(--err);
    border-color: rgba(255,107,107,0.2);
  }
  .status-err .dot { background: var(--err); }

  /* ── Divider ── */
  .dm-rule {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
  }

  /* ── Panel cards ── */
  .panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    position: relative;
  }
  .panel-accent {
    border-left: 2px solid var(--accent);
  }
  .panel-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    color: var(--text-3);
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .panel-label .badge {
    background: var(--accent-dim);
    color: var(--accent);
    padding: 1px 7px;
    border-radius: 3px;
    font-size: 0.6rem;
    letter-spacing: 1px;
    border: 1px solid rgba(79,140,255,0.2);
    text-transform: uppercase;
  }
  .panel-body {
    font-size: 0.92rem;
    color: var(--text-2);
    line-height: 1.7;
    margin: 0;
  }

  /* ── Options sidebar panel ── */
  .opts-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    color: var(--text-3);
    margin-bottom: 0.5rem;
  }

  /* ── Input overrides ── */
  textarea, .stTextArea textarea {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.83rem !important;
    background: var(--surface-2) !important;
    color: var(--text-1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    line-height: 1.6 !important;
  }
  textarea:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
    outline: none !important;
  }
  .stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-1) !important;
    border-radius: var(--radius) !important;
    font-size: 0.88rem !important;
  }
  label { color: var(--text-3) !important; font-size: 0.78rem !important; }

  /* ── Analyze button ── */
  .stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 1.2px !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.62rem 2rem !important;
    width: 100% !important;
    text-transform: uppercase !important;
    transition: background 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 0 0 0 transparent !important;
  }
  .stButton > button:hover {
    background: #6AA3FF !important;
    box-shadow: 0 4px 20px rgba(79,140,255,0.25) !important;
  }
  .stButton > button:active {
    background: #3A72D4 !important;
  }

  /* ── Severity badges ── */
  .sev {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 600;
    padding: 3px 9px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    border: 1px solid;
  }
  .sev-critical { background: rgba(255,107,107,0.1); color: #FF8A8A; border-color: rgba(255,107,107,0.25); }
  .sev-warn     { background: rgba(255,179,71,0.1);  color: #FFB347; border-color: rgba(255,179,71,0.25); }
  .sev-info     { background: rgba(79,140,255,0.1);  color: #4F8CFF; border-color: rgba(79,140,255,0.25); }
  .sev-ok       { background: rgba(82,209,140,0.1);  color: #52D18C; border-color: rgba(82,209,140,0.25); }

  /* ── Optimizations list ── */
  .opt-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.88rem;
    color: var(--text-2);
    line-height: 1.6;
  }
  .opt-row:last-child { border-bottom: none; padding-bottom: 0; }
  .opt-idx {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-3);
    flex-shrink: 0;
    min-width: 22px;
    padding-top: 3px;
  }

  /* ── Metadata row ── */
  .meta-row {
    display: flex;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
    padding: 0.9rem 1.1rem;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    margin-bottom: 1.4rem;
  }
  .meta-item {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .meta-key {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 1.2px;
  }
  .meta-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-2);
    font-weight: 500;
  }
  .meta-sep {
    width: 1px;
    height: 18px;
    background: var(--border);
  }

  /* ── Results heading ── */
  .results-heading {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--text-3);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .results-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  /* ── Expander ── */
  .streamlit-expanderHeader {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    color: var(--text-3) !important;
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
  }
  .streamlit-expanderContent {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius) var(--radius) !important;
  }

  /* ── st.code override ── */
  .stCodeBlock { border-radius: var(--radius) !important; }

  /* ── Warning/error overrides ── */
  .stAlert {
    border-radius: var(--radius) !important;
    font-size: 0.88rem !important;
  }

  /* ── Spinner ── */
  .stSpinner > div { color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)

# ── Config ─────────────────────────────────────────────────────────────────────
BACKEND_URL = "http://localhost:5000"

LANG_MAP = {
    "Python":     "python",
    "JavaScript": "javascript",
    "TypeScript": "typescript",
    "C++":        "cpp",
    "Go":         "go",
    "Rust":       "rust",
    "Java":       "java",
}

# ── Session state ──────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8].upper()
if "run_count" not in st.session_state:
    st.session_state.run_count = 0

# ── Header ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def check_health():
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

healthy = check_health()

header_col, status_col = st.columns([5, 1])
with header_col:
    st.markdown("""
    <div class="dm-wordmark">
      <div class="dm-mark">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="9" cy="9" r="3" fill="white"/>
          <path d="M9 2V5M9 13V16M2 9H5M13 9H16M4.22 4.22L6.34 6.34M11.66 11.66L13.78 13.78M13.78 4.22L11.66 6.34M6.34 11.66L4.22 13.78" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </div>
      <h1 class="dm-name">DebugMind</h1>
      <span class="dm-version">v2.0</span>
    </div>
    <p class="dm-sub">Static analysis &amp; failure diagnosis for production code</p>
    """, unsafe_allow_html=True)

with status_col:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if healthy:
        st.markdown('<span class="status-chip status-ok"><span class="dot"></span>API Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-chip status-err"><span class="dot"></span>API Offline</span>', unsafe_allow_html=True)

st.markdown("<hr class='dm-rule'>", unsafe_allow_html=True)

# ── Input workspace ────────────────────────────────────────────────────────────
input_col, opts_col = st.columns([3, 1], gap="medium")

with opts_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="opts-label">Language</p>', unsafe_allow_html=True)
    language = st.selectbox(
        "Language",
        list(LANG_MAP.keys()),
        index=0,
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel" style="margin-top:0">', unsafe_allow_html=True)
    st.markdown('<p class="opts-label">Error / Traceback</p>', unsafe_allow_html=True)
    error_input = st.text_area(
        "Error",
        placeholder="Paste traceback or runtime error here (optional)",
        height=148,
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    analyze_clicked = st.button("ANALYZE", use_container_width=True)

with input_col:
    st.markdown('<div class="panel panel-accent">', unsafe_allow_html=True)
    st.markdown('<p class="opts-label">Source Code</p>', unsafe_allow_html=True)
    code_input = st.text_area(
        "Code",
        placeholder="# Paste the code to diagnose\ndef example():\n    pass",
        height=310,
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Processing ─────────────────────────────────────────────────────────────────
if analyze_clicked:
    if not code_input.strip():
        st.warning("No source code provided. Paste the code you want to analyze.")
        st.stop()
    if not healthy:
        st.error("Backend is unreachable. Start the backend with `python app.py` inside the `backend/` directory.")
        st.stop()

    t_start = time.time()
    st.session_state.run_count += 1

    with st.spinner("Analyzing…"):
        try:
            resp = requests.post(
                f"{BACKEND_URL}/debug",
                json={
                    "code":     code_input,
                    "error":    error_input,
                    "language": language,
                },
                timeout=60,
            )
            data = resp.json()
        except requests.exceptions.ConnectionError:
            st.error("Connection refused. Confirm the backend server is running.")
            st.stop()
        except Exception as exc:
            st.error(f"Request failed: {exc}")
            st.stop()

    elapsed = time.time() - t_start

    if "error" in data:
        st.error(f"API returned an error: {data['error']}")
        st.stop()

    # ── Metadata bar ──────────────────────────────────────────────────────────
    import datetime
    ts = datetime.datetime.now().strftime("%H:%M:%S UTC")
    st.markdown(f"""
    <div class="meta-row">
      <div class="meta-item"><span class="meta-key">Session</span><span class="meta-val">{st.session_state.session_id}</span></div>
      <div class="meta-sep"></div>
      <div class="meta-item"><span class="meta-key">Run</span><span class="meta-val">#{st.session_state.run_count:03d}</span></div>
      <div class="meta-sep"></div>
      <div class="meta-item"><span class="meta-key">Language</span><span class="meta-val">{language}</span></div>
      <div class="meta-sep"></div>
      <div class="meta-item"><span class="meta-key">Duration</span><span class="meta-val">{elapsed:.2f}s</span></div>
      <div class="meta-sep"></div>
      <div class="meta-item"><span class="meta-key">Timestamp</span><span class="meta-val">{ts}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Results heading ───────────────────────────────────────────────────────
    st.markdown('<div class="results-heading">Failure Analysis Report</div>', unsafe_allow_html=True)

    # ── Two-column diagnostic panels ─────────────────────────────────────────
    r_left, r_right = st.columns(2, gap="medium")

    with r_left:
        # Error Summary
        st.markdown(f"""
        <div class="panel">
          <div class="panel-label">
            Error Summary
            <span class="sev sev-critical">Critical</span>
          </div>
          <p class="panel-body">{data.get("error_summary", "—")}</p>
        </div>
        """, unsafe_allow_html=True)

        # Root Cause
        st.markdown(f"""
        <div class="panel">
          <div class="panel-label">
            Root Cause Findings
            <span class="sev sev-warn">Warning</span>
          </div>
          <p class="panel-body">{data.get("root_cause", "—")}</p>
        </div>
        """, unsafe_allow_html=True)

        # Optimization Recommendations
        opts = data.get("optimizations", [])
        if opts:
            items_html = "".join(
                f'<div class="opt-row"><span class="opt-idx">{i+1:02d}</span><span>{opt}</span></div>'
                for i, opt in enumerate(opts)
            )
            st.markdown(f"""
            <div class="panel">
              <div class="panel-label">Optimization Recommendations</div>
              {items_html}
            </div>
            """, unsafe_allow_html=True)

    with r_right:
        # Explanation
        st.markdown(f"""
        <div class="panel">
          <div class="panel-label">
            Diagnostic Explanation
            <span class="sev sev-info">Detail</span>
          </div>
          <p class="panel-body">{data.get("explanation", "—")}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Fixed code — full width ───────────────────────────────────────────────
    st.markdown("""
    <div class="panel-label" style="margin-top:0.4rem;">
      Suggested Resolution
      <span class="sev sev-ok">Patch Ready</span>
    </div>
    """, unsafe_allow_html=True)

    fixed = data.get("fixed_code", "")
    st.code(fixed, language=LANG_MAP.get(language, "python"))

    # ── Raw payload expander ──────────────────────────────────────────────────
    with st.expander("Response Payload — Raw JSON"):
        st.json(data)