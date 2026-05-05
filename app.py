# ================================================================
#  NEXUS v6.0 — Intelligence Platform
#  UI  : Ultra-Premium Pure Black Theme
#  Stack: Streamlit · Groq · yt-dlp · pdfplumber · python-docx
#
#  requirements.txt:
#    streamlit>=1.35
#    groq
#    youtube-transcript-api
#    python-docx
#    streamlit-mic-recorder
#    Pillow
#    pdfplumber
# ================================================================

import streamlit as st
import time
import json
from datetime import datetime

# ─────────────────────────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NEXUS",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

FREE_MSG_LIMIT = 15

MODELS = {
    "llama-3.3-70b-versatile": "Llama 3.3 · 70B",
    "llama-3.1-8b-instant":    "Llama 3.1 · 8B",
    "mixtral-8x7b-32768":      "Mixtral · 8×7B",
    "gemma2-9b-it":            "Gemma 2 · 9B",
}

# ─────────────────────────────────────────────────────────────────
#  THEME PALETTES
# ─────────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg":          "#000000",
        "sb_bg":       "#080808",
        "s1":          "#0D0D0D",
        "s2":          "#141414",
        "s3":          "#1A1A1A",
        "border":      "#1C1C1C",
        "border_h":    "#282828",
        "tx":          "#EAE8E1",
        "tx_2":        "#5C5C5C",
        "tx_3":        "#2A2A2A",
        "accent":      "#C8A778",
        "accent_dim":  "#8B6914",
        "accent_glow": "rgba(200,167,120,0.12)",
        "usr_bub":     "#141414",
        "inp_bg":      "#0D0D0D",
        "danger":      "#CC3333",
        "success":     "#3D9970",
        "code_bg":     "#080808",
    },
    "light": {
        "bg":          "#F5F4F0",
        "sb_bg":       "#FFFFFF",
        "s1":          "#FFFFFF",
        "s2":          "#EFEDE7",
        "s3":          "#E5E3DC",
        "border":      "#E0DDD5",
        "border_h":    "#C8C5BA",
        "tx":          "#1A1A14",
        "tx_2":        "#696760",
        "tx_3":        "#AEACA6",
        "accent":      "#8B6914",
        "accent_dim":  "#C8A778",
        "accent_glow": "rgba(139,105,20,0.10)",
        "usr_bub":     "#E8E6E0",
        "inp_bg":      "#FFFFFF",
        "danger":      "#CC3333",
        "success":     "#2E7D52",
        "code_bg":     "#F0EFE9",
    },
}

# ─────────────────────────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "messages":        [],
        "query_count":     0,
        "locked":          False,
        "active_tool":     None,
        "show_tools":      False,
        "theme":           "dark",
        "chat_history":    [],
        "sidebar_view":    "chat",
        "show_terms":      False,
        "show_privacy":    False,
        "uploaded_file":   None,
        "yt_url":          "",
        "tool_result":     None,
        "selected_model":  "llama-3.3-70b-versatile",
        "show_shortcuts":  False,
        "msg_count":       0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

T = THEMES[st.session_state.theme]

# ─────────────────────────────────────────────────────────────────
#  CSS — ULTRA PREMIUM THEME
# ─────────────────────────────────────────────────────────────────
def get_css():
    t = T
    is_dark = st.session_state.theme == "dark"
    grain_opacity = "0.025" if is_dark else "0.018"

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Sora:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── CSS VARIABLES ── */
:root {{
    --bg:           {t['bg']};
    --sb-bg:        {t['sb_bg']};
    --s1:           {t['s1']};
    --s2:           {t['s2']};
    --s3:           {t['s3']};
    --border:       {t['border']};
    --border-h:     {t['border_h']};
    --tx:           {t['tx']};
    --tx2:          {t['tx_2']};
    --tx3:          {t['tx_3']};
    --accent:       {t['accent']};
    --accent-dim:   {t['accent_dim']};
    --accent-glow:  {t['accent_glow']};
    --usr-bub:      {t['usr_bub']};
    --inp-bg:       {t['inp_bg']};
    --danger:       {t['danger']};
    --success:      {t['success']};
    --code-bg:      {t['code_bg']};
    --radius:       12px;
    --radius-lg:    18px;
    --radius-xl:    24px;
    --shadow:       0 4px 24px rgba(0,0,0,{'0.4' if is_dark else '0.12'});
    --shadow-lg:    0 8px 48px rgba(0,0,0,{'0.6' if is_dark else '0.18'});
}}

/* ── RESET ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

/* ── BASE ── */
html, body, [data-testid="stAppViewContainer"] {{
    background: var(--bg) !important;
    font-family: 'Sora', sans-serif !important;
    color: var(--tx) !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

/* ── GRAIN TEXTURE OVERLAY ── */
[data-testid="stAppViewContainer"]::after {{
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
    opacity: {grain_opacity};
    pointer-events: none;
    z-index: 99998;
}}

/* ── SCROLLBAR ── */
::-webkit-scrollbar {{ width: 3px; height: 3px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: var(--border-h); border-radius: 2px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--tx3); }}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header {{ display: none !important; visibility: hidden !important; }}
[data-testid="stDecoration"],
[data-testid="stToolbar"],
[data-testid="stStatusWidget"],
[data-testid="stHeader"] {{ display: none !important; }}

/* ── MAIN CONTAINER ── */
.main .block-container {{
    max-width: 800px !important;
    margin: 0 auto !important;
    padding: 1.5rem 1.5rem 180px 1.5rem !important;
}}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {{
    background: var(--sb-bg) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 268px !important;
    max-width: 268px !important;
    transition: transform 0.3s cubic-bezier(0.4,0,0.2,1) !important;
}}
[data-testid="stSidebar"] * {{
    font-family: 'Sora', sans-serif !important;
}}
[data-testid="stSidebarContent"] {{
    padding: 0 !important;
    overflow-x: hidden !important;
}}
[data-testid="stSidebar"] .stButton > button {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    text-align: left !important;
    box-shadow: none !important;
    font-weight: 400 !important;
    width: 100% !important;
    justify-content: flex-start !important;
    border-radius: 8px !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: var(--s2) !important;
    color: var(--tx) !important;
}}

/* ── GLOBAL BUTTONS ── */
.stButton > button {{
    background: transparent !important;
    border: 1px solid var(--border-h) !important;
    color: var(--tx) !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    border-radius: var(--radius) !important;
    transition: all 0.18s cubic-bezier(0.4,0,0.2,1) !important;
    cursor: pointer !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em !important;
}}
.stButton > button:hover {{
    background: var(--s2) !important;
    border-color: var(--accent) !important;
    color: var(--tx) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px var(--accent-glow) !important;
}}
.stButton > button:active {{
    transform: translateY(0) !important;
}}
.stButton > button:focus {{
    outline: none !important;
    box-shadow: 0 0 0 2px var(--accent-glow) !important;
}}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessage"] {{
    background: transparent !important;
    border: none !important;
    padding: 8px 0 !important;
    gap: 14px !important;
    animation: nexusFadeUp 0.35s cubic-bezier(0.4,0,0.2,1) forwards;
    position: relative !important;
}}
[data-testid="stChatMessage"]:hover {{
    background: transparent !important;
}}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {{
    font-size: 15px !important;
    line-height: 1.82 !important;
    color: var(--tx) !important;
    font-weight: 400 !important;
    letter-spacing: -0.005em !important;
}}

/* Message content area */
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {{
    padding: 2px 0 !important;
}}

/* User message bubble */
[data-testid="stChatMessageAvatarUser"] + div [data-testid="stMarkdownContainer"],
.stChatMessage[data-message-author-role="user"] [data-testid="stMarkdownContainer"] {{
    background: var(--usr-bub) !important;
    border: 1px solid var(--border) !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 12px 16px !important;
    display: inline-block !important;
}}

/* Code blocks */
[data-testid="stMarkdownContainer"] pre {{
    background: var(--code-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 14px 16px !important;
    overflow-x: auto !important;
    margin: 10px 0 !important;
    position: relative !important;
}}
[data-testid="stMarkdownContainer"] code {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    color: var(--accent) !important;
    background: var(--code-bg) !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    border: 1px solid var(--border) !important;
}}
[data-testid="stMarkdownContainer"] pre code {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    color: var(--tx) !important;
    font-size: 13px !important;
    line-height: 1.7 !important;
}}

/* Lists in responses */
[data-testid="stMarkdownContainer"] ul,
[data-testid="stMarkdownContainer"] ol {{
    padding-left: 20px !important;
    margin: 8px 0 !important;
}}
[data-testid="stMarkdownContainer"] li {{
    font-size: 15px !important;
    line-height: 1.75 !important;
    margin-bottom: 4px !important;
}}
[data-testid="stMarkdownContainer"] li::marker {{
    color: var(--accent) !important;
}}
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--tx) !important;
    letter-spacing: -0.03em !important;
    margin: 16px 0 8px !important;
}}
[data-testid="stMarkdownContainer"] strong {{
    color: var(--tx) !important;
    font-weight: 700 !important;
}}
[data-testid="stMarkdownContainer"] blockquote {{
    border-left: 3px solid var(--accent) !important;
    padding-left: 14px !important;
    margin: 10px 0 !important;
    color: var(--tx2) !important;
    font-style: italic !important;
}}
[data-testid="stMarkdownContainer"] table {{
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 12px 0 !important;
}}
[data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] td {{
    border: 1px solid var(--border) !important;
    padding: 8px 12px !important;
    font-size: 13px !important;
    text-align: left !important;
}}
[data-testid="stMarkdownContainer"] th {{
    background: var(--s2) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    color: var(--tx2) !important;
}}
[data-testid="stMarkdownContainer"] tr:hover td {{
    background: var(--s1) !important;
}}

/* ── ASSISTANT AVATAR ── */
[data-testid="stChatMessageAvatarAssistant"] {{
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dim) 100%) !important;
    border-radius: 9px !important;
    color: #000 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 900 !important;
    width: 30px !important;
    height: 30px !important;
    border: none !important;
    box-shadow: 0 2px 8px var(--accent-glow) !important;
    flex-shrink: 0 !important;
}}

/* ── USER AVATAR ── */
[data-testid="stChatMessageAvatarUser"] {{
    background: var(--s3) !important;
    border-radius: 9px !important;
    border: 1px solid var(--border-h) !important;
    width: 30px !important;
    height: 30px !important;
    flex-shrink: 0 !important;
}}

/* ── CHAT INPUT AREA ── */
[data-testid="stChatInput"] {{
    position: fixed !important;
    bottom: 20px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(780px, calc(100vw - 32px)) !important;
    background: var(--inp-bg) !important;
    border: 1px solid var(--border-h) !important;
    border-radius: 20px !important;
    box-shadow: var(--shadow-lg), 0 0 0 1px var(--border), inset 0 1px 0 rgba(255,255,255,0.03) !important;
    z-index: 1000 !important;
    padding: 4px 8px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
[data-testid="stChatInput"]:focus-within {{
    border-color: var(--accent) !important;
    box-shadow: var(--shadow-lg), 0 0 0 1px var(--border), 0 0 0 3px var(--accent-glow) !important;
}}
[data-testid="stChatInput"] textarea {{
    background: transparent !important;
    color: var(--tx) !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    border: none !important;
    outline: none !important;
    resize: none !important;
    padding: 14px 16px !important;
    caret-color: var(--accent) !important;
}}
[data-testid="stChatInput"] textarea::placeholder {{
    color: var(--tx2) !important;
    font-size: 15px !important;
}}
[data-testid="stChatInput"] button[kind="primaryFormSubmit"],
[data-testid="stChatInput"] button {{
    background: var(--accent) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #000 !important;
    font-weight: 700 !important;
    transition: opacity 0.2s, transform 0.1s !important;
    margin-right: 4px !important;
}}
[data-testid="stChatInput"] button:hover {{
    opacity: 0.85 !important;
    transform: scale(1.04) !important;
}}

/* ── TEXT INPUT ── */
[data-testid="stTextInput"] input {{
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--tx) !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
    padding: 11px 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
[data-testid="stTextInput"] input:focus {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
    outline: none !important;
}}
[data-testid="stTextInput"] label {{
    color: var(--tx2) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: .04em !important;
    text-transform: uppercase !important;
}}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {{
    background: var(--s1) !important;
    border: 1.5px dashed var(--border-h) !important;
    border-radius: var(--radius) !important;
    transition: border-color 0.2s, background 0.2s !important;
}}
[data-testid="stFileUploader"]:hover {{
    border-color: var(--accent) !important;
    background: var(--s2) !important;
}}
[data-testid="stFileUploader"] section {{
    background: transparent !important;
    border: none !important;
    padding: 16px !important;
}}
[data-testid="stFileUploader"] label {{
    color: var(--tx2) !important;
    font-size: 13px !important;
}}

/* ── SELECTBOX ── */
[data-baseweb="select"] > div {{
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--tx) !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    transition: border-color 0.2s !important;
}}
[data-baseweb="select"] > div:hover {{
    border-color: var(--border-h) !important;
}}
[data-baseweb="menu"] {{
    background: var(--s2) !important;
    border: 1px solid var(--border-h) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-lg) !important;
}}

/* ── TOAST ── */
[data-testid="stToast"] {{
    background: var(--s2) !important;
    border: 1px solid var(--border-h) !important;
    border-radius: var(--radius) !important;
    color: var(--tx) !important;
    font-family: 'Sora', sans-serif !important;
    box-shadow: var(--shadow) !important;
}}

/* ── SPINNER ── */
[data-testid="stSpinner"] {{
    color: var(--accent) !important;
}}

/* ── DIVIDER ── */
hr {{ border: none !important; border-top: 1px solid var(--border) !important; margin: 8px 0 !important; }}

/* ── ANIMATIONS ── */
@keyframes nexusFadeUp {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes nexusPopIn {{
    from {{ opacity: 0; transform: translateY(8px) scale(0.96); }}
    to   {{ opacity: 1; transform: translateY(0) scale(1); }}
}}
@keyframes nexusPulse {{
    0%, 100% {{ opacity: 1; }}
    50%       {{ opacity: 0.4; }}
}}
@keyframes nexusSlideRight {{
    from {{ opacity: 0; transform: translateX(-16px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
}}
@keyframes dotBounce {{
    0%, 80%, 100% {{ transform: translateY(0); }}
    40%           {{ transform: translateY(-6px); }}
}}
@keyframes shimmer {{
    0%   {{ background-position: -200% center; }}
    100% {{ background-position: 200% center; }}
}}

/* ── FREE COUNTER BADGE ── */
.nx-counter {{
    position: fixed;
    top: 14px;
    right: 18px;
    z-index: 9999;
    background: var(--s2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 5px 14px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11px;
    font-weight: 700;
    pointer-events: none;
    letter-spacing: .02em;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}}

/* ── TOOL POPUP ── */
.nx-tool-popup {{
    background: var(--s1);
    border: 1px solid var(--border-h);
    border-radius: 18px;
    padding: 12px;
    margin-bottom: 12px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    animation: nexusPopIn 0.22s cubic-bezier(0.34,1.56,0.64,1) forwards;
    box-shadow: var(--shadow-lg);
}}
.nx-tool-btn {{
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 13px 15px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 500;
    color: var(--tx2);
    background: transparent;
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.18s cubic-bezier(0.4,0,0.2,1);
    font-family: 'Sora', sans-serif;
    text-align: left;
    width: 100%;
    letter-spacing: -0.01em;
}}
.nx-tool-btn:hover {{
    background: var(--s2);
    border-color: var(--border-h);
    color: var(--tx);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}
.nx-tool-btn.active {{
    background: var(--accent-glow);
    border-color: var(--accent);
    color: var(--accent);
}}
.nx-tool-btn .icon {{
    font-size: 19px;
    flex-shrink: 0;
}}

/* ── TOOL PANEL ── */
.nx-panel {{
    background: var(--s1);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 14px;
    animation: nexusFadeUp 0.28s cubic-bezier(0.4,0,0.2,1) forwards;
    box-shadow: var(--shadow);
}}
.nx-panel-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
}}
.nx-panel-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--tx2);
    display: flex;
    align-items: center;
    gap: 8px;
}}
.nx-panel-badge {{
    background: var(--accent-glow);
    border: 1px solid var(--accent);
    color: var(--accent);
    font-size: 9px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 20px;
    letter-spacing: .06em;
    text-transform: uppercase;
}}

/* ── SIDEBAR BRAND ── */
.nx-sb-brand {{
    padding: 18px 16px 14px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 11px;
}}
.nx-sb-mark {{
    width: 32px; height: 32px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dim) 100%);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13px; font-weight: 900;
    color: #000;
    flex-shrink: 0;
    box-shadow: 0 2px 8px var(--accent-glow);
}}
.nx-sb-name {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 16px; font-weight: 900;
    letter-spacing: -.04em;
    color: var(--tx);
    line-height: 1;
}}
.nx-sb-version {{
    font-size: 9px;
    color: var(--tx2);
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
    margin-top: 2px;
}}

/* ── SIDEBAR ACTION BUTTONS ROW ── */
.nx-sb-actions {{
    display: flex;
    gap: 8px;
    padding: 12px 12px 4px;
}}

/* ── SIDEBAR SECTIONS ── */
.nx-sb-section-label {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9px; font-weight: 800;
    letter-spacing: .14em; text-transform: uppercase;
    color: var(--tx3);
    padding: 16px 16px 6px;
}}
.nx-sb-item {{
    padding: 9px 16px;
    font-size: 13px;
    color: var(--tx2);
    cursor: pointer;
    border-radius: 9px;
    margin: 1px 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    transition: background 0.15s, color 0.15s;
    font-family: 'Sora', sans-serif;
    animation: nexusSlideRight 0.3s ease forwards;
}}
.nx-sb-item:hover {{ background: var(--s2); color: var(--tx); }}
.nx-sb-item-meta {{
    font-size: 10px;
    color: var(--tx3);
    margin-left: 4px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
}}

/* ── SIDEBAR SETTINGS ── */
.nx-sb-setting-item {{
    padding: 10px 16px;
    font-size: 13px;
    color: var(--tx2);
    display: flex;
    align-items: center;
    gap: 10px;
    border-radius: 9px;
    margin: 1px 8px;
    transition: background 0.15s, color 0.15s;
    font-family: 'Sora', sans-serif;
    cursor: default;
}}
.nx-sb-setting-item:hover {{ background: var(--s2); color: var(--tx); }}

/* ── SIDEBAR STATUS BAR ── */
.nx-sb-status {{
    padding: 10px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

/* ── WELCOME SCREEN ── */
.nx-welcome {{
    text-align: center;
    padding: 72px 0 36px;
    animation: nexusFadeUp 0.5s cubic-bezier(0.4,0,0.2,1) forwards;
}}
.nx-welcome-mark {{
    width: 64px; height: 64px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dim) 100%);
    border-radius: 18px;
    display: inline-flex; align-items: center; justify-content: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 26px; font-weight: 900; color: #000;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px var(--accent-glow), 0 0 0 1px var(--accent-dim);
}}
.nx-welcome h1 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 30px; font-weight: 900;
    letter-spacing: -.05em; color: var(--tx);
    margin-bottom: 10px;
    line-height: 1.1;
}}
.nx-welcome-sub {{
    font-size: 15px; color: var(--tx2);
    line-height: 1.65;
    max-width: 440px;
    margin: 0 auto 32px;
}}
.nx-welcome-model {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: var(--s2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 11px;
    font-weight: 700;
    color: var(--tx2);
    font-family: 'Plus Jakarta Sans', sans-serif;
    letter-spacing: .04em;
    margin-bottom: 32px;
}}
.nx-welcome-model-dot {{
    width: 6px; height: 6px;
    background: var(--success);
    border-radius: 50%;
    animation: nexusPulse 2.4s infinite;
}}
.nx-suggestion-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 4px;
    text-align: left;
}}
.nx-suggestion {{
    background: var(--s1);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px 18px;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4,0,0.2,1);
    font-size: 13px;
    color: var(--tx2);
    line-height: 1.55;
}}
.nx-suggestion:hover {{
    background: var(--s2);
    border-color: var(--accent);
    color: var(--tx);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px var(--accent-glow);
}}
.nx-suggestion strong {{
    display: block;
    color: var(--tx);
    font-size: 13px;
    margin-bottom: 4px;
    font-weight: 700;
    font-family: 'Plus Jakarta Sans', sans-serif;
}}
.nx-suggestion-icon {{
    font-size: 20px;
    margin-bottom: 8px;
    display: block;
}}

/* ── LIMIT WALL ── */
.nx-limit-wall {{
    text-align: center;
    padding: 80px 20px;
    max-width: 480px;
    margin: 0 auto;
    animation: nexusFadeUp 0.4s ease forwards;
}}
.nx-limit-wall .nx-lw-icon {{
    font-size: 48px;
    margin-bottom: 20px;
    display: block;
    filter: grayscale(0.3);
}}
.nx-limit-wall h2 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 24px; font-weight: 900;
    color: var(--tx); margin-bottom: 12px;
    letter-spacing: -.04em;
}}
.nx-limit-wall p {{
    font-size: 15px; color: var(--tx2);
    line-height: 1.75; margin-bottom: 28px;
}}

/* ── TYPING INDICATOR ── */
.nx-typing {{
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 12px 0 4px;
}}
.nx-typing-dot {{
    width: 7px; height: 7px;
    background: var(--tx2);
    border-radius: 50%;
    animation: dotBounce 1.4s ease-in-out infinite;
}}
.nx-typing-dot:nth-child(2) {{ animation-delay: 0.16s; }}
.nx-typing-dot:nth-child(3) {{ animation-delay: 0.32s; }}

/* ── BOTTOM TOOLBAR ── */
.nx-bottom-toolbar {{
    position: fixed;
    bottom: 92px;
    left: 50%;
    transform: translateX(-50%);
    width: min(780px, calc(100vw - 32px));
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 999;
    padding: 0 4px;
    pointer-events: none;
}}
.nx-bottom-left {{
    display: flex;
    align-items: center;
    gap: 8px;
    pointer-events: all;
}}
.nx-bottom-right {{
    display: flex;
    align-items: center;
    gap: 8px;
    pointer-events: all;
}}
.nx-model-badge {{
    background: var(--s2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 5px 12px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: var(--tx2);
    letter-spacing: .02em;
    pointer-events: none;
    white-space: nowrap;
}}
.nx-active-tool-badge {{
    background: var(--accent-glow);
    border: 1px solid var(--accent);
    border-radius: 20px;
    padding: 5px 12px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: .02em;
    pointer-events: none;
    white-space: nowrap;
    animation: nexusFadeUp 0.2s ease forwards;
}}

/* ── SETTINGS ── */
.nx-settings-section {{
    background: var(--s1);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 16px;
    animation: nexusFadeUp 0.3s ease forwards;
}}
.nx-settings-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11px; font-weight: 800;
    letter-spacing: .1em; text-transform: uppercase;
    color: var(--tx2); margin-bottom: 18px;
}}
.nx-settings-row {{
    display: flex; align-items: center;
    justify-content: space-between;
    padding: 11px 0;
    border-bottom: 1px solid var(--border);
}}
.nx-settings-row:last-child {{ border-bottom: none; }}
.nx-settings-label {{ font-size: 14px; color: var(--tx); font-weight: 500; }}
.nx-settings-value {{ font-size: 12px; color: var(--tx2); font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 600; }}

/* ── LEGAL CONTENT ── */
.nx-legal-content {{
    font-size: 13px; line-height: 1.95;
    color: var(--tx2); padding: 4px 0;
}}
.nx-legal-content h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13px; font-weight: 800;
    color: var(--accent); margin: 18px 0 6px;
    letter-spacing: -.01em;
}}
.nx-legal-content p {{ margin-bottom: 12px; }}

/* ── STATUS INDICATOR ── */
.nx-status-dot {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
}}
.nx-status-dot::before {{
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--success);
    animation: nexusPulse 2.4s infinite;
    flex-shrink: 0;
}}

/* ── SYSTEM INFO MESSAGE ── */
.nx-sys-info {{
    text-align: center;
    font-size: 12px;
    color: var(--tx2);
    padding: 8px 16px;
    margin: 8px 0;
    border-radius: 20px;
    background: var(--s1);
    border: 1px solid var(--border);
    display: inline-block;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    letter-spacing: .02em;
    animation: nexusFadeUp 0.25s ease forwards;
}}
.nx-sys-info-wrap {{ text-align: center; }}

/* ── SIDEBAR SEARCH ── */
.nx-sb-search {{
    padding: 8px 12px 4px;
}}
.nx-sb-search input {{
    width: 100%;
    background: var(--s2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    font-size: 13px !important;
    color: var(--tx) !important;
    font-family: 'Sora', sans-serif !important;
}}

/* ── EXPANDER ── */
details {{
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}
details summary {{
    color: var(--tx) !important;
    font-size: 13px !important;
    padding: 12px 16px !important;
    cursor: pointer !important;
    font-weight: 600 !important;
}}

/* ── EXPLORE FEATURE CARD ── */
.nx-feature-card {{
    display: flex;
    gap: 14px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
    align-items: flex-start;
    transition: padding-left 0.2s;
}}
.nx-feature-card:last-child {{ border-bottom: none; }}
.nx-feature-card:hover {{ padding-left: 6px; }}
.nx-feature-card-icon {{
    font-size: 22px;
    flex-shrink: 0;
    margin-top: 1px;
}}
.nx-feature-card-name {{
    font-size: 14px; font-weight: 700;
    color: var(--tx);
    font-family: 'Plus Jakarta Sans', sans-serif;
    margin-bottom: 3px;
    letter-spacing: -.02em;
}}
.nx-feature-card-desc {{
    font-size: 12px; color: var(--tx2); line-height: 1.55;
}}

/* ── SHORTCUTS HINT ── */
.nx-shortcut-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
    color: var(--tx2);
}}
.nx-shortcut-row:last-child {{ border-bottom: none; }}
.nx-kbd {{
    background: var(--s3);
    border: 1px solid var(--border-h);
    border-radius: 5px;
    padding: 2px 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--tx2);
    letter-spacing: .04em;
}}

/* ── PROGRESS BAR (session usage) ── */
.nx-progress-wrap {{
    padding: 6px 16px 12px;
}}
.nx-progress-label {{
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: var(--tx3);
    margin-bottom: 5px;
}}
.nx-progress-bar {{
    width: 100%;
    height: 3px;
    background: var(--s3);
    border-radius: 2px;
    overflow: hidden;
}}
.nx-progress-fill {{
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--accent-dim), var(--accent));
    transition: width 0.4s cubic-bezier(0.4,0,0.2,1);
}}

/* ── QUIZ DIFFICULTY BADGE ── */
.nx-diff-easy   {{ color: var(--success); }}
.nx-diff-medium {{ color: var(--accent); }}
.nx-diff-hard   {{ color: #E07B39; }}
.nx-diff-expert {{ color: var(--danger); }}

/* ── SCROLLABLE CONTENT AREAS ── */
.nx-scroll-area {{
    max-height: 280px;
    overflow-y: auto;
    padding-right: 4px;
}}
</style>
"""

st.markdown(get_css(), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
#  BACKEND STUBS — Replace with real implementations
# ─────────────────────────────────────────────────────────────────

def get_ai_response(messages: list, api_key: str, model: str = "llama-3.3-70b-versatile") -> str:
    """
    PLUG IN: Replace with your real Groq API call.
    messages = [{"role": "user"|"assistant", "content": "..."}]
    """
    # ── REAL IMPLEMENTATION ──────────────────────────────────────
    # from groq import Groq
    # client = Groq(api_key=api_key)
    # response = client.chat.completions.create(
    #     model=model,
    #     messages=messages,
    #     max_tokens=2048,
    #     temperature=0.7,
    # )
    # return response.choices[0].message.content
    # ─────────────────────────────────────────────────────────────
    time.sleep(0.5)
    return "This is a **demo response** from NEXUS. Plug in your Groq API key to enable real AI responses. The interface is fully functional."

def process_document(file_bytes: bytes, filename: str) -> str:
    """PLUG IN: Your PDF / DOCX / TXT processing logic."""
    # import pdfplumber, docx ...
    return f"Document '{filename}' loaded. Ready for analysis."

def process_youtube(url: str) -> str:
    """PLUG IN: Your YouTube transcript extraction logic."""
    # from youtube_transcript_api import YouTubeTranscriptApi ...
    return f"YouTube transcript extracted from: {url}"

def process_image(file_bytes: bytes, filename: str) -> str:
    """PLUG IN: Your image analysis / vision logic."""
    return f"Image '{filename}' ready for vision analysis."

def transcribe_audio(audio_bytes: bytes) -> str:
    """PLUG IN: Your Whisper / speech-to-text logic."""
    return "Voice transcription placeholder."


# ─────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # ── BRAND ──
        st.markdown(f"""
        <div class="nx-sb-brand">
            <div class="nx-sb-mark">N</div>
            <div>
                <div class="nx-sb-name">NEXUS</div>
                <div class="nx-sb-version">v6.0 · Intelligence Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── TOP ACTION BUTTONS ROW ──
        col_new, col_tools = st.columns([1, 1])
        with col_new:
            if st.button("✦  New Chat", key="new_chat_btn", use_container_width=True):
                if st.session_state.messages:
                    preview = ""
                    for m in st.session_state.messages:
                        if m["role"] == "user":
                            preview = m["content"][:38]
                            break
                    st.session_state.chat_history.insert(0, {
                        "title": preview or "Chat",
                        "ts":    datetime.now().strftime("%b %d"),
                        "count": st.session_state.query_count,
                    })
                st.session_state.messages   = []
                st.session_state.active_tool = None
                st.session_state.show_tools  = False
                st.session_state.tool_result = None
                st.session_state.query_count = 0
                st.session_state.locked      = False
                st.rerun()

        with col_tools:
            tool_icon = "✕" if st.session_state.show_tools else "＋"
            tool_lbl  = f"{tool_icon}  Tools"
            if st.button(tool_lbl, key="sb_tools_btn", use_container_width=True):
                st.session_state.show_tools = not st.session_state.show_tools
                st.rerun()

        # ── VIEW TOGGLE ──
        col_c, col_s = st.columns(2)
        with col_c:
            is_chat = st.session_state.sidebar_view == "chat"
            if st.button("Chat", key="view_chat", use_container_width=True):
                st.session_state.sidebar_view = "chat"
                st.rerun()
        with col_s:
            if st.button("Settings", key="view_settings", use_container_width=True):
                st.session_state.sidebar_view = "settings"
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── CHAT VIEW ──
        if st.session_state.sidebar_view == "chat":
            st.markdown('<div class="nx-sb-section-label">Recent Chats</div>', unsafe_allow_html=True)
            if not st.session_state.chat_history:
                st.markdown(
                    f'<div style="padding:12px 16px;font-size:12px;color:{T["tx_3"]};font-family:\'Plus Jakarta Sans\',sans-serif;">'
                    f'No history yet — start chatting</div>',
                    unsafe_allow_html=True
                )
            else:
                for i, chat in enumerate(st.session_state.chat_history[:14]):
                    count_txt = f"· {chat.get('count',0)} msgs" if chat.get('count') else ""
                    st.markdown(
                        f'<div class="nx-sb-item">'
                        f'💬 {chat["title"]}…'
                        f'<span class="nx-sb-item-meta">{chat["ts"]} {count_txt}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

        # ── SETTINGS VIEW ──
        else:
            render_sidebar_settings()

        # ── SESSION PROGRESS BAR ──
        st.markdown("<hr>", unsafe_allow_html=True)
        remaining = max(0, FREE_MSG_LIMIT - st.session_state.query_count)
        used_pct   = (st.session_state.query_count / FREE_MSG_LIMIT) * 100
        bar_color  = T["danger"] if remaining <= 3 else T["accent"]
        st.markdown(f"""
        <div class="nx-progress-wrap">
            <div class="nx-progress-label">
                <span>Session Usage</span>
                <span style="color:{bar_color if remaining <= 5 else T['tx3']}">{remaining}/{FREE_MSG_LIMIT} left</span>
            </div>
            <div class="nx-progress-bar">
                <div class="nx-progress-fill" style="width:{used_pct}%;background:linear-gradient(90deg,{T['accent_dim']},{bar_color if remaining<=5 else T['accent']});"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="padding:0 16px 14px;text-align:center;">
            <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:9px;font-weight:800;
                 letter-spacing:.1em;text-transform:uppercase;color:{T['tx_3']}">
                NEXUS · Made in India · © 2026
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar_settings():
    t = T

    # ── APPEARANCE ──
    st.markdown('<div class="nx-sb-section-label">Appearance</div>', unsafe_allow_html=True)
    theme_label = "☀️  Light Mode" if st.session_state.theme == "dark" else "🌙  Dark Mode"
    if st.button(theme_label, key="toggle_theme", use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

    # ── MODEL ──
    st.markdown('<div class="nx-sb-section-label">AI Model</div>', unsafe_allow_html=True)
    model_display = MODELS.get(st.session_state.selected_model, st.session_state.selected_model)
    model_keys    = list(MODELS.keys())
    model_labels  = list(MODELS.values())
    try:
        cur_idx = model_keys.index(st.session_state.selected_model)
    except ValueError:
        cur_idx = 0
    chosen = st.selectbox(
        "Model",
        options=model_keys,
        format_func=lambda k: MODELS[k],
        index=cur_idx,
        key="model_select",
        label_visibility="collapsed",
    )
    if chosen != st.session_state.selected_model:
        st.session_state.selected_model = chosen
        st.rerun()

    # ── SYSTEM STATUS ──
    st.markdown('<div class="nx-sb-section-label">System</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin:0 8px;padding:13px 15px;background:{t['s2']};
         border:1px solid {t['border']};border-radius:11px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:9px;">
            <span style="font-size:12px;color:{t['tx_2']};font-family:'Sora',sans-serif;">Groq API</span>
            <span class="nx-status-dot" style="font-size:11px;color:{t['success']};font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;">LIVE</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:9px;">
            <span style="font-size:12px;color:{t['tx_2']};font-family:'Sora',sans-serif;">Context Window</span>
            <span style="font-size:11px;color:{t['tx_2']};font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;">128k tokens</span>
        </div>
        <div style="display:flex;justify-content:space-between;">
            <span style="font-size:12px;color:{t['tx_2']};font-family:'Sora',sans-serif;">Platform</span>
            <span style="font-size:11px;color:{t['tx_2']};font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;">Streamlit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SHORTCUTS ──
    st.markdown('<div class="nx-sb-section-label">Shortcuts</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin:0 8px;padding:12px 15px;background:{t['s2']};border:1px solid {t['border']};border-radius:11px;">
        <div class="nx-shortcut-row"><span>Send message</span><span class="nx-kbd">Enter</span></div>
        <div class="nx-shortcut-row"><span>New line</span><span class="nx-kbd">Shift+Enter</span></div>
        <div class="nx-shortcut-row"><span>New chat</span><span class="nx-kbd">✦ New Chat</span></div>
        <div class="nx-shortcut-row" style="border:none"><span>Toggle tools</span><span class="nx-kbd">＋ Tools</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ── LEGAL ──
    st.markdown('<div class="nx-sb-section-label">Legal</div>', unsafe_allow_html=True)
    if st.button("📋  Terms of Service",  key="show_terms_btn",   use_container_width=True):
        st.session_state.show_terms   = not st.session_state.show_terms
        st.session_state.show_privacy = False
        st.rerun()
    if st.button("🔒  Privacy Policy",    key="show_privacy_btn", use_container_width=True):
        st.session_state.show_privacy = not st.session_state.show_privacy
        st.session_state.show_terms   = False
        st.rerun()
    if st.button("📜  Content Policy",    key="show_content_btn", use_container_width=True):
        st.toast("Content policy: Be respectful, no harmful content.", icon="📜")


# ─────────────────────────────────────────────────────────────────
#  TOOLS POPUP
# ─────────────────────────────────────────────────────────────────
TOOLS = [
    ("document", "📄", "Document AI",    "PDF, DOCX, TXT, CSV"),
    ("youtube",  "▶️",  "YouTube IQ",    "Transcript & analysis"),
    ("image",    "🖼️",  "Vision AI",     "Image intelligence"),
    ("quiz",     "📝", "Quiz Master",    "Auto-generate quizzes"),
    ("explore",  "🔍", "Explore",        "Platform features"),
]

def render_tools_popup():
    if not st.session_state.show_tools:
        return

    st.markdown('<div class="nx-tool-popup">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, (tool_id, icon, label, desc) in enumerate(TOOLS):
        is_active = st.session_state.active_tool == tool_id
        with cols[i % 2]:
            st.markdown(
                f'<div class="nx-tool-btn {"active" if is_active else ""}" '
                f'style="pointer-events:none;">'
                f'<span class="icon">{icon}</span>'
                f'<div><div style="font-weight:600;color:{"var(--accent)" if is_active else "var(--tx)"};font-size:13px;">{label}</div>'
                f'<div style="font-size:11px;color:var(--tx2);margin-top:1px;">{desc}</div></div>'
                f'</div>',
                unsafe_allow_html=True
            )
            if st.button(
                f"{'✓ Active' if is_active else 'Select'}",
                key=f"tool_{tool_id}",
                use_container_width=True
            ):
                if is_active:
                    st.session_state.active_tool = None
                    st.session_state.tool_result = None
                else:
                    st.session_state.active_tool = tool_id
                st.session_state.show_tools = False
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
#  TOOL PANELS
# ─────────────────────────────────────────────────────────────────
def render_tool_panel():
    tool = st.session_state.active_tool
    if not tool:
        return

    TOOL_META = {
        "document": ("📄", "Document Analysis"),
        "youtube":  ("▶️",  "YouTube IQ"),
        "image":    ("🖼️",  "Vision AI"),
        "quiz":     ("📝", "Quiz Master"),
        "explore":  ("🔍", "Explore NEXUS"),
    }
    icon, label = TOOL_META.get(tool, ("🔧", tool.title()))

    status_html = ""
    if st.session_state.tool_result:
        status_html = f'<span class="nx-panel-badge">LOADED</span>'

    st.markdown(f"""
    <div class="nx-panel">
        <div class="nx-panel-header">
            <div class="nx-panel-title">{icon} &nbsp;{label} {status_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_close, col_clear = st.columns([1, 1])
    with col_close:
        if st.button("✕  Close Panel", key="close_panel", use_container_width=True):
            st.session_state.active_tool = None
            st.session_state.tool_result = None
            st.rerun()
    if st.session_state.tool_result:
        with col_clear:
            if st.button("🔄  Clear Data", key="clear_tool_data", use_container_width=True):
                st.session_state.tool_result = None
                st.rerun()

    # ── DOCUMENT ──
    if tool == "document":
        st.markdown(f'<p style="font-size:12px;color:{T["tx_2"]};margin:4px 0 8px;font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.06em;">Upload File</p>', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Upload",
            type=["pdf", "docx", "txt", "csv"],
            key="doc_uploader",
            label_visibility="collapsed",
        )
        if uploaded:
            with st.spinner("Processing document…"):
                result = process_document(uploaded.read(), uploaded.name)
            st.session_state.tool_result = result
            st.session_state.messages.append({
                "role":    "system_info",
                "content": f"📄 Document loaded: **{uploaded.name}**"
            })
            st.rerun()

    # ── YOUTUBE ──
    elif tool == "youtube":
        st.markdown(f'<p style="font-size:12px;color:{T["tx_2"]};margin:4px 0 8px;font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.06em;">YouTube URL</p>', unsafe_allow_html=True)
        yt_url = st.text_input(
            "YouTube URL",
            placeholder="https://youtube.com/watch?v=...",
            key="yt_input",
            label_visibility="collapsed",
        )
        if st.button("▶️  Extract Transcript", key="yt_extract", use_container_width=True):
            if yt_url:
                with st.spinner("Fetching transcript…"):
                    result = process_youtube(yt_url)
                st.session_state.tool_result = result
                st.session_state.messages.append({
                    "role":    "system_info",
                    "content": "▶️ YouTube transcript loaded — ask me anything about the video"
                })
                st.rerun()
            else:
                st.warning("Enter a YouTube URL first.")

    # ── IMAGE ──
    elif tool == "image":
        st.markdown(f'<p style="font-size:12px;color:{T["tx_2"]};margin:4px 0 8px;font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.06em;">Upload Image</p>', unsafe_allow_html=True)
        uploaded_img = st.file_uploader(
            "Upload image",
            type=["png", "jpg", "jpeg", "webp", "gif"],
            key="img_uploader",
            label_visibility="collapsed",
        )
        if uploaded_img:
            st.image(uploaded_img, use_container_width=True)
            with st.spinner("Analyzing image…"):
                result = process_image(uploaded_img.read(), uploaded_img.name)
            st.session_state.tool_result = result
            st.session_state.messages.append({
                "role":    "system_info",
                "content": f"🖼️ Image loaded: **{uploaded_img.name}** — ask me to describe or analyze it"
            })
            st.rerun()

    # ── QUIZ ──
    elif tool == "quiz":
        st.markdown(f'<p style="font-size:12px;color:{T["tx_2"]};margin:4px 0 8px;font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.06em;">Quiz Topic</p>', unsafe_allow_html=True)
        topic = st.text_input(
            "Topic",
            placeholder="e.g. Python basics, World War II, Machine Learning…",
            key="quiz_topic",
            label_visibility="collapsed",
        )
        col_diff, col_num = st.columns([3, 2])
        with col_diff:
            difficulty = st.selectbox(
                "Difficulty",
                ["Easy", "Medium", "Hard", "Expert"],
                key="quiz_diff",
                label_visibility="collapsed",
            )
        with col_num:
            q_count = st.selectbox(
                "Questions",
                [5, 10, 15, 20],
                key="quiz_count",
                label_visibility="collapsed",
            )
        if st.button("📝  Generate Quiz", key="quiz_gen", use_container_width=True):
            if topic:
                diff_emoji = {"Easy": "🟢", "Medium": "🟡", "Hard": "🟠", "Expert": "🔴"}.get(difficulty, "")
                prompt = (
                    f"Generate a {difficulty} level quiz on: **{topic}**. "
                    f"Include {q_count} multiple-choice questions with 4 options each. "
                    f"After all questions, provide the answer key. Format neatly with headers."
                )
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.active_tool = None
                st.rerun()
            else:
                st.warning("Enter a topic first.")

    # ── EXPLORE ──
    elif tool == "explore":
        features = [
            ("🧠", "Neural Chat",     "Multi-turn AI with full context memory"),
            ("📄", "Document AI",     "Analyze PDF, DOCX, TXT, CSV files instantly"),
            ("▶️",  "YouTube IQ",     "Extract & analyze video transcripts"),
            ("🖼️",  "Vision AI",      "Understand and describe any image"),
            ("📝", "Quiz Master",     "Auto-generate quizzes on any topic"),
            ("🎙️",  "Voice Input",    "Speak your queries (coming soon)"),
        ]
        for icon, name, desc in features:
            st.markdown(f"""
            <div class="nx-feature-card">
                <span class="nx-feature-card-icon">{icon}</span>
                <div>
                    <div class="nx-feature-card-name">{name}</div>
                    <div class="nx-feature-card-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
#  LEGAL MODALS
# ─────────────────────────────────────────────────────────────────
def render_terms():
    st.markdown(f"""
    <div class="nx-settings-section">
        <div class="nx-settings-title">📋 Terms of Service</div>
        <div class="nx-legal-content">
            <p><strong style="color:{T['tx']}">Effective Date:</strong> January 1, 2026 &nbsp;·&nbsp; v6.0</p>
            <h3>1. Acceptance of Terms</h3>
            <p>By using NEXUS, you confirm you are at least 13 years of age and have the legal capacity to accept these terms. Continued use constitutes acceptance of the current version of these terms.</p>
            <h3>2. Description of Service</h3>
            <p>NEXUS is a free, multi-modal AI intelligence platform providing document analysis, YouTube transcript intelligence, neural chat, image vision analysis, voice transcription, and text transformation — powered by third-party AI APIs.</p>
            <h3>3. Usage Limits</h3>
            <p><strong style="color:{T['tx']}">Free limit:</strong> {FREE_MSG_LIMIT} messages per browser session<br>
            <strong style="color:{T['tx']}">Rate limit:</strong> 20 requests per 60-second rolling window<br>
            <strong style="color:{T['tx']}">Context window:</strong> 128,000 tokens per session<br>
            <strong style="color:{T['tx']}">Upload size:</strong> Up to 200MB per file</p>
            <h3>4. Prohibited Uses</h3>
            <p>You may not use NEXUS to generate harmful, illegal, or deceptive content; create malware or cyberweapons; exploit minors; engage in hate speech; facilitate self-harm; or circumvent rate limits through automation.</p>
            <h3>5. Intellectual Property</h3>
            <p>All original design elements and code architecture are the intellectual property of the developer. Content you generate through NEXUS remains your own.</p>
            <h3>6. Disclaimer</h3>
            <p>NEXUS is provided "as is" without warranty. AI responses may contain inaccuracies. Do not rely on NEXUS for medical, legal, or financial decisions.</p>
            <h3>7. Governing Law</h3>
            <p>These terms are governed by the laws of India. Disputes shall be subject to the jurisdiction of Indian courts.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("✕  Close Terms", key="close_terms"):
        st.session_state.show_terms = False
        st.rerun()


def render_privacy():
    st.markdown(f"""
    <div class="nx-settings-section">
        <div class="nx-settings-title">🔒 Privacy Policy</div>
        <div class="nx-legal-content">
            <p><strong style="color:{T['tx']}">Effective Date:</strong> January 1, 2026 &nbsp;·&nbsp; v6.0</p>
            <h3>1. Data We Collect</h3>
            <p>NEXUS collects only the data you actively provide — messages, uploaded files, and configuration preferences. No personally identifiable information is collected or stored beyond your active browser session.</p>
            <h3>2. Data We Do Not Collect</h3>
            <p>We do not collect your name, email, IP address, or any identifying information. We do not use cookies for tracking. We do not sell or share your data with advertisers.</p>
            <h3>3. Session Data</h3>
            <p>Your conversation history and uploaded files exist only in your browser session (st.session_state). When you close the tab or refresh, all session data is permanently erased.</p>
            <h3>4. Third-Party Services</h3>
            <p>NEXUS transmits your messages to Groq's inference API for AI processing. Your data is subject to Groq's privacy policy. Uploaded documents are processed in-memory and never stored on our servers.</p>
            <h3>5. Your Rights</h3>
            <p>Since we collect no persistent personal data, there is nothing to delete or export. Starting a new session automatically clears all previous data.</p>
            <h3>6. Contact</h3>
            <p>For privacy concerns or questions, contact the developer directly through the platform's feedback channel.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("✕  Close Privacy", key="close_privacy"):
        st.session_state.show_privacy = False
        st.rerun()


# ─────────────────────────────────────────────────────────────────
#  WELCOME SCREEN
# ─────────────────────────────────────────────────────────────────
def render_welcome():
    model_name = MODELS.get(st.session_state.selected_model, st.session_state.selected_model)
    st.markdown(f"""
    <div class="nx-welcome">
        <div class="nx-welcome-mark">N</div>
        <h1>How can I help you?</h1>
        <p class="nx-welcome-sub">Ask anything, analyze documents, review YouTube videos,<br>or explore image intelligence.</p>
        <div class="nx-welcome-model">
            <span class="nx-welcome-model-dot"></span>
            {model_name} · Ready
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Suggestion cards as Streamlit buttons styled via CSS
    suggestions = [
        ("📄", "Analyze a document",      "Upload a PDF or DOCX and ask questions"),
        ("▶️",  "YouTube breakdown",       "Paste a URL for transcript analysis"),
        ("🖼️",  "Describe an image",       "Upload any image for vision AI"),
        ("🧠",  "Deep research",           "Ask complex multi-step questions"),
    ]
    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(suggestions):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="nx-suggestion">
                <span class="nx-suggestion-icon">{icon}</span>
                <strong>{title}</strong>
                {desc}
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
#  FREE COUNTER BADGE
# ─────────────────────────────────────────────────────────────────
def render_counter():
    remaining = max(0, FREE_MSG_LIMIT - st.session_state.query_count)
    color = T["accent"] if remaining > 5 else T["danger"]
    st.markdown(f"""
    <div class="nx-counter" style="color:{color};">
        {remaining} msgs left
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
#  LIMIT WALL
# ─────────────────────────────────────────────────────────────────
def render_limit_wall():
    st.markdown(f"""
    <div class="nx-limit-wall">
        <span class="nx-lw-icon">⬡</span>
        <h2>Session Limit Reached</h2>
        <p>You've used all {FREE_MSG_LIMIT} free messages in this session.<br>
        Start a new session to continue — no cooldown required.</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✦  Start New Session", key="new_session_btn", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ─────────────────────────────────────────────────────────────────
#  BOTTOM TOOLBAR
# ─────────────────────────────────────────────────────────────────
def render_bottom_toolbar():
    t = T
    model_name = MODELS.get(st.session_state.selected_model, "Model")

    active_tool_html = ""
    if st.session_state.active_tool:
        tool_icons = {
            "document": "📄", "youtube": "▶️", "image": "🖼️",
            "quiz": "📝", "explore": "🔍"
        }
        tool_icon = tool_icons.get(st.session_state.active_tool, "🔧")
        active_tool_html = f'<div class="nx-active-tool-badge">{tool_icon} {st.session_state.active_tool.title()} Active</div>'

    st.markdown(f"""
    <div class="nx-bottom-toolbar">
        <div class="nx-bottom-left" id="bottom-left-placeholder"></div>
        <div class="nx-bottom-right">
            {active_tool_html}
            <div class="nx-model-badge">⬡ {model_name}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bottom action buttons — positioned inline (Streamlit will render them)
    col_plus, col_mic, col_spacer = st.columns([1, 1, 6])
    with col_plus:
        icon  = "✕" if st.session_state.show_tools else "＋"
        label = f"{icon}  Tools"
        if st.button(label, key="bottom_tools_btn"):
            st.session_state.show_tools = not st.session_state.show_tools
            st.rerun()
    with col_mic:
        if st.button("🎙  Voice", key="mic_btn"):
            st.toast("Voice input — wire up streamlit-mic-recorder.", icon="🎙")


# ─────────────────────────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────────────────────────
def main():
    render_sidebar()
    render_counter()

    # ── LOCKED ──
    if st.session_state.query_count >= FREE_MSG_LIMIT:
        st.session_state.locked = True

    if st.session_state.locked:
        render_limit_wall()
        return

    # ── LEGAL MODALS ──
    if st.session_state.show_terms:
        render_terms()
        return
    if st.session_state.show_privacy:
        render_privacy()
        return

    # ── WELCOME SCREEN ──
    if not st.session_state.messages:
        render_welcome()

    # ── CHAT HISTORY ──
    for msg in st.session_state.messages:
        role    = msg["role"]
        content = msg["content"]

        if role == "system_info":
            st.markdown(
                f'<div class="nx-sys-info-wrap"><div class="nx-sys-info">{content}</div></div>',
                unsafe_allow_html=True
            )
        elif role == "user":
            with st.chat_message("user"):
                st.markdown(content)
        elif role == "assistant":
            with st.chat_message("assistant", avatar="◈"):
                st.markdown(content)

    # ── TOOL POPUP ──
    render_tools_popup()

    # ── TOOL PANEL ──
    render_tool_panel()

    # ── BOTTOM TOOLBAR ──
    render_bottom_toolbar()

    # ── CHAT INPUT ──
    hints = {
        "document": "Ask about your document…",
        "youtube":  "Ask about the YouTube video…",
        "image":    "Describe or analyze the image…",
        "quiz":     "Chat freely or set a quiz topic above…",
        "explore":  "What would you like to explore?",
    }
    placeholder = hints.get(st.session_state.active_tool, "Message NEXUS…") \
        if st.session_state.active_tool else "Message NEXUS…"

    prompt = st.chat_input(placeholder)

    if prompt:
        if st.session_state.query_count >= FREE_MSG_LIMIT:
            st.session_state.locked = True
            st.rerun()

        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.query_count += 1

        # Build AI message list
        ai_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
            if m["role"] in ("user", "assistant")
        ]

        # Prepend tool context
        if st.session_state.tool_result:
            ai_messages.insert(0, {
                "role":    "system",
                "content": f"Context from loaded tool:\n{st.session_state.tool_result}"
            })

        # Get AI response with typing indicator
        with st.chat_message("assistant", avatar="◈"):
            st.markdown("""
            <div class="nx-typing">
                <div class="nx-typing-dot"></div>
                <div class="nx-typing-dot"></div>
                <div class="nx-typing-dot"></div>
            </div>
            """, unsafe_allow_html=True)
            api_key  = st.secrets.get("GROQ_API_KEY", "") if hasattr(st, "secrets") else ""
            response = get_ai_response(ai_messages, api_key, st.session_state.selected_model)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


# ─────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__" or True:
    main()
