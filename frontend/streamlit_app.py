"""
DebugMind — Professional Code Debugging Platform
Streamlit Frontend — Production Redesign
"""

import streamlit as st
import requests
import time
import uuid
import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DebugMind",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS — nuclear dark-theme override ─────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

  /* ══════════════════════════════════════════════════
     NUCLEAR DARK OVERRIDE — hits every Streamlit layer
     ══════════════════════════════════════════════════ */

  /* Root variables */
  :root {
    --bg:         #0B0D10;
    --surface:    #111418;
    --surface2:   #171B21;
    --border:     #262B33;
    --border-hi:  #353D49;
    --text1:      #F5F7FA;
    --text2:      #A8B0BB;
    --text3:      #6F7883;
    --accent:     #4F8CFF;
    --accent-dim: rgba(79,140,255,0.12);
    --err:        #FF6B6B;
    --warn:       #FFB347;
    --ok:         #52D18C;
    --r:          8px;
    --rl:         12px;
  }

  /* Every background layer Streamlit creates */
  html,
  body,
  .stApp,
  .stApp > div,
  .stApp > div > div,
  section[data-testid="stSidebar"],
  .main,
  .main > div,
  .block-container,
  [data-testid="stAppViewContainer"],
  [data-testid="stAppViewBlockContainer"],
  [data-testid="stHeader"],
  [data-testid="stToolbar"],
  [data-testid="stDecoration"],
  [data-testid="stBottom"],
  [class^="css"],
  [class*=" css"] {
    background-color: var(--bg) !important;
    color: var(--text1) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
  }

  /* Catch-all for any remaining white divs */
  div, section, main, aside, nav, header, footer, span, p, li {
    background-color: transparent;
  }

  /* Only re-set the app root solidly */
  .stApp { background-color: var(--bg) !important; }

  /* ── Hide chrome ── */
  #MainMenu, footer, header,
  [data-testid="stHeader"],
  [data-testid="stToolbar"],
  [data-testid="stDecoration"] {
    visibility: hidden !important;
    height: 0 !important;
  }

  /* ── Block container ── */
  .block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1160px !important;
    background-color: var(--bg) !important;
  }

  /* ── Subtle dot grid atmosphere ── */
  .stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle, rgba(79,140,255,0.07) 1px, transparent 1px);
    background-size: 28px 28px;
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
    width: 34px; height: 34px;
    background: var(--accent);
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .dm-name {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.55rem;
    font-weight: 600;
    color: var(--text1);
    letter-spacing: -0.5px;
    margin: 0; line-height: 1;
  }
  .dm-version {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: var(--text3);
    padding: 2px 7px;
    border: 1px solid var(--border);
    border-radius: 4px;
    letter-spacing: 0.5px;
    align-self: flex-end;
    margin-bottom: 2px;
    background: var(--surface2) !important;
  }
  .dm-sub {
    font-size: 0.82rem;
    color: var(--text3);
    margin-bottom: 1.8rem;
    font-weight: 400;
    letter-spacing: 0.1px;
  }

  /* ── Status chip ── */
  .status-chip {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    padding: 5px 13px;
    border-radius: 999px;
    border: 1px solid;
  }
  .status-chip .dot {
    width: 6px; height: 6px;
    border-radius: 50%; flex-shrink: 0;
  }
  .status-ok {
    background: rgba(82,209,140,0.07) !important;
    color: var(--ok) !important;
    border-color: rgba(82,209,140,0.2) !important;
  }
  .status-ok .dot  { background: var(--ok); box-shadow: 0 0 6px var(--ok); }
  .status-err {
    background: rgba(255,107,107,0.07) !important;
    color: var(--err) !important;
    border-color: rgba(255,107,107,0.2) !important;
  }
  .status-err .dot { background: var(--err); }

  /* ── Divider ── */
  .dm-rule {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.4rem 0;
  }

  /* ── Panels ── */
  .panel {
    background: var(--surface) !important;
    border: 1px solid var(--border);
    border-radius: var(--rl);
    padding: 1.15rem 1.35rem;
    margin-bottom: 0.85rem;
  }
  .panel-accent { border-left: 2px solid var(--accent) !important; }

  .panel-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    color: var(--text3);
    margin-bottom: 0.55rem;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .panel-body {
    font-size: 0.9rem;
    color: var(--text2);
    line-height: 1.72;
    margin: 0;
  }

  /* ── Severity badges ── */
  .sev {
    display: inline-flex;
    align-items: center;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 3px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    border: 1px solid;
  }
  .sev-crit { background:rgba(255,107,107,0.1) !important; color:#FF8A8A; border-color:rgba(255,107,107,0.25); }
  .sev-warn { background:rgba(255,179,71,0.1)  !important; color:#FFB347; border-color:rgba(255,179,71,0.25); }
  .sev-info { background:rgba(79,140,255,0.1)  !important; color:#4F8CFF; border-color:rgba(79,140,255,0.25); }
  .sev-ok   { background:rgba(82,209,140,0.1)  !important; color:#52D18C; border-color:rgba(82,209,140,0.25); }

  /* ── Options label ── */
  .opts-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    color: var(--text3);
    margin-bottom: 0.4rem;
  }

  /* ── Input overrides ── */
  textarea,
  .stTextArea textarea,
  [data-baseweb="textarea"] textarea,
  [data-baseweb="base-input"] textarea {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
    background-color: var(--surface2) !important;
    background: var(--surface2) !important;
    color: var(--text1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    line-height: 1.62 !important;
    caret-color: var(--accent) !important;
  }
  textarea:focus,
  .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,140,255,0.08) !important;
    outline: none !important;
  }

  /* Selectbox */
  .stSelectbox [data-baseweb="select"] > div,
  .stSelectbox [data-baseweb="select"] > div:hover,
  [data-baseweb="select"] [data-baseweb="popover"],
  [data-baseweb="popover"] {
    background-color: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
  }
  [data-baseweb="select"] span,
  [data-baseweb="select"] div {
    color: var(--text1) !important;
    font-size: 0.88rem !important;
  }
  [data-baseweb="menu"] {
    background-color: var(--surface2) !important;
    border: 1px solid var(--border) !important;
  }
  [data-baseweb="menu"] li {
    background-color: var(--surface2) !important;
    color: var(--text2) !important;
  }
  [data-baseweb="menu"] li:hover {
    background-color: var(--surface) !important;
    color: var(--text1) !important;
  }

  /* Label text */
  label, .stSelectbox label, .stTextArea label {
    color: var(--text3) !important;
    font-size: 0.75rem !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
  }

  /* ── Analyze button ── */
  .stButton > button {
    background-color: var(--accent) !important;
    background: var(--accent) !important;
    color: #fff !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: 1.5px !important;
    border: none !important;
    border-radius: var(--r) !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    text-transform: uppercase !important;
    transition: background 0.15s, box-shadow 0.15s !important;
  }
  .stButton > button:hover {
    background-color: #6AA3FF !important;
    box-shadow: 0 4px 22px rgba(79,140,255,0.3) !important;
  }
  .stButton > button:active {
    background-color: #3A72D4 !important;
  }
  /* Remove focus ring */
  .stButton > button:focus { outline: none !important; box-shadow: none !important; }

  /* ── Metadata bar ── */
  .meta-bar {
    display: flex;
    align-items: center;
    gap: 0;
    flex-wrap: wrap;
    padding: 0.8rem 1.2rem;
    background: var(--surface) !important;
    border: 1px solid var(--border);
    border-radius: var(--r);
    margin-bottom: 1.4rem;
  }
  .meta-item {
    display: flex; align-items: center; gap: 8px;
    padding: 0 16px;
    border-right: 1px solid var(--border);
  }
  .meta-item:first-child { padding-left: 0; }
  .meta-item:last-child  { border-right: none; }
  .meta-key {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: var(--text3);
    text-transform: uppercase;
    letter-spacing: 1.2px;
  }
  .meta-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: var(--text2);
    font-weight: 500;
  }

  /* ── Results section header ── */
  .results-heading {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: var(--text3);
    margin: 0 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .results-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  /* ── Optimizations list ── */
  .opt-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 9px 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.87rem;
    color: var(--text2);
    line-height: 1.62;
  }
  .opt-row:last-child { border-bottom: none; padding-bottom: 0; }
  .opt-idx {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: var(--text3);
    flex-shrink: 0;
    min-width: 20px;
    padding-top: 3px;
  }

  /* ── Code block ── */
  .stCodeBlock,
  [data-testid="stCodeBlock"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
  }
  pre, code {
    background: var(--surface2) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
  }

  /* ── Expander ── */
  [data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
  }
  [data-testid="stExpander"] summary {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    color: var(--text3) !important;
    background: var(--surface) !important;
  }
  [data-testid="stExpander"] summary:hover {
    color: var(--text2) !important;
  }

  /* ── Alert overrides ── */
  [data-testid="stAlert"],
  .stAlert {
    background: var(--surface) !important;
    border-radius: var(--r) !important;
    border: 1px solid var(--border) !important;
    font-size: 0.88rem !important;
    color: var(--text2) !important;
  }

  /* ── Spinner ── */
  [data-testid="stSpinner"] > div,
  .stSpinner > div { color: var(--accent) !important; }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: var(--text3); }

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

# ── Health check ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def check_health():
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

healthy = check_health()

# ── Header ─────────────────────────────────────────────────────────────────────
hdr_left, hdr_right = st.columns([5, 2])

with hdr_left:
    st.markdown("""
    <div class="dm-wordmark">
      <div class="dm-mark">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <circle cx="9" cy="9" r="2.5" fill="white"/>
          <path d="M9 2v3M9 13v3M2 9h3M13 9h3M4.05 4.05l2.12 2.12M11.83 11.83l2.12 2.12M13.95 4.05l-2.12 2.12M6.17 11.83l-2.12 2.12"
                stroke="white" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </div>
      <span class="dm-name">DebugMind</span>
      <span class="dm-version">v2.0</span>
    </div>
    <p class="dm-sub">Static analysis &amp; failure diagnosis for production code</p>
    """, unsafe_allow_html=True)

with hdr_right:
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if healthy:
        st.markdown('<span class="status-chip status-ok"><span class="dot"></span>Live</span>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-chip status-err"><span class="dot"></span>API Offline</span>',
                    unsafe_allow_html=True)

st.markdown("<hr class='dm-rule'>", unsafe_allow_html=True)

# ── Input workspace ────────────────────────────────────────────────────────────
col_code, col_opts = st.columns([3, 1], gap="medium")

with col_opts:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="opts-label">Language</p>', unsafe_allow_html=True)
    language = st.selectbox("Language", list(LANG_MAP.keys()), index=0, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="opts-label">Error / Traceback</p>', unsafe_allow_html=True)
    error_input = st.text_area(
        "Error",
        placeholder="Paste traceback or runtime error (optional)",
        height=148,
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
    analyze_clicked = st.button("ANALYZE", use_container_width=True)

with col_code:
    st.markdown('<div class="panel panel-accent">', unsafe_allow_html=True)
    st.markdown('<p class="opts-label">Source Code</p>', unsafe_allow_html=True)
    code_input = st.text_area(
        "Code",
        placeholder="# Paste the code you want to diagnose\ndef example():\n    pass",
        height=315,
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Analysis ───────────────────────────────────────────────────────────────────
if analyze_clicked:
    if not code_input.strip():
        st.warning("No source code provided. Paste the code you want to analyze.")
        st.stop()
    if not healthy:
        st.error("Backend unreachable. Start it with `python app.py` inside the `backend/` directory.")
        st.stop()

    t_start = time.time()
    st.session_state.run_count += 1

    with st.spinner("Analyzing…"):
        try:
            resp = requests.post(
                f"{BACKEND_URL}/debug",
                json={"code": code_input, "error": error_input, "language": language},
                timeout=60,
            )
            data = resp.json()
        except requests.exceptions.ConnectionError:
            st.error("Connection refused. Confirm the backend is running.")
            st.stop()
        except Exception as exc:
            st.error(f"Request failed: {exc}")
            st.stop()

    elapsed = time.time() - t_start

    if "error" in data:
        st.error(f"API error: {data['error']}")
        st.stop()

    # ── Metadata bar ──────────────────────────────────────────────────────────
    ts = datetime.datetime.now().strftime("%H:%M:%S UTC")
    st.markdown(f"""
    <div class="meta-bar">
      <div class="meta-item"><span class="meta-key">Session</span><span class="meta-val">{st.session_state.session_id}</span></div>
      <div class="meta-item"><span class="meta-key">Run</span><span class="meta-val">#{st.session_state.run_count:03d}</span></div>
      <div class="meta-item"><span class="meta-key">Language</span><span class="meta-val">{language}</span></div>
      <div class="meta-item"><span class="meta-key">Duration</span><span class="meta-val">{elapsed:.2f}s</span></div>
      <div class="meta-item"><span class="meta-key">Timestamp</span><span class="meta-val">{ts}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Section heading ───────────────────────────────────────────────────────
    st.markdown('<div class="results-heading">Failure Analysis Report</div>', unsafe_allow_html=True)

    # ── Two-column panels ─────────────────────────────────────────────────────
    r_left, r_right = st.columns(2, gap="medium")

    with r_left:
        st.markdown(f"""
        <div class="panel">
          <div class="panel-label">Error Summary <span class="sev sev-crit">Critical</span></div>
          <p class="panel-body">{data.get("error_summary", "—")}</p>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="panel">
          <div class="panel-label">Root Cause Findings <span class="sev sev-warn">Warning</span></div>
          <p class="panel-body">{data.get("root_cause", "—")}</p>
        </div>""", unsafe_allow_html=True)

        opts = data.get("optimizations", [])
        if opts:
            items = "".join(
                f'<div class="opt-row"><span class="opt-idx">{i+1:02d}</span><span>{o}</span></div>'
                for i, o in enumerate(opts)
            )
            st.markdown(f"""
            <div class="panel">
              <div class="panel-label">Optimization Recommendations</div>
              {items}
            </div>""", unsafe_allow_html=True)

    with r_right:
        st.markdown(f"""
        <div class="panel">
          <div class="panel-label">Diagnostic Explanation <span class="sev sev-info">Detail</span></div>
          <p class="panel-body">{data.get("explanation", "—")}</p>
        </div>""", unsafe_allow_html=True)

    # ── Fixed code ────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="panel-label" style="margin-top:0.6rem">
      Suggested Resolution <span class="sev sev-ok">Patch Ready</span>
    </div>""", unsafe_allow_html=True)
    st.code(data.get("fixed_code", ""), language=LANG_MAP.get(language, "python"))

    # ── Raw payload ───────────────────────────────────────────────────────────
    with st.expander("Response Payload — Raw JSON"):
        st.json(data)