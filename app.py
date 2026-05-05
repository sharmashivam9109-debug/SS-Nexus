# ============================================================
#  NEXUS — Intelligence Platform  |  app.py  (v5.1)
#  Themes  : Nova Crystal · Arctic Frost · Crimson Noir
#  Stack   : Streamlit · Neural Engine · youtube-transcript-api
#
#  requirements.txt:
#    streamlit>=1.31
#    groq
#    youtube-transcript-api
#    python-docx
#    streamlit-mic-recorder
#    Pillow
#    pdfplumber
# ============================================================

import streamlit as st
import re, os, tempfile, time, json, base64, io, unicodedata
from datetime import datetime

st.set_page_config(
    page_title="NEXUS — Intelligence Platform",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

FREE_MSG_LIMIT = 15  # Free messages per session before login wall

# ═══════════════════════════════════════════════════════
#  THEME DEFINITIONS
# ═══════════════════════════════════════════════════════
THEME_VARS = {
    "Nova Crystal": """
:root {
    --bg:           #0d0d10;
    --sb-bg:        #111116;
    --s1:           #17171d;
    --s2:           #1e1e26;
    --s3:           #252530;
    --border:       #232330;
    --border-h:     #2e2e3e;
    --tx:           #eae8e1;
    --tx-2:         #7c7a87;
    --tx-3:         #3f3d4a;
    --accent:       #c8a778;
    --accent-h:     #dbbe96;
    --accent-glow:  rgba(200,167,120,.1);
    --accent-ring:  rgba(200,167,120,.18);
    --usr-bub:      #1a1a22;
    --ai-bub:       #131318;
    --inp-bg:       #111116;
    --danger:       #d95555;
    --r:            11px;
    --r-sm:         7px;
    --fb:           'Plus Jakarta Sans', sans-serif;
    --fs:           'Sora', sans-serif;
    --transition:   all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}""",
    "Arctic Frost": """
:root {
    --bg:           #f5f6fa;
    --sb-bg:        #ffffff;
    --s1:           #ffffff;
    --s2:           #eef0f7;
    --s3:           #e4e7f0;
    --border:       #dde1ed;
    --border-h:     #c8cedf;
    --tx:           #1a1a2e;
    --tx-2:         #5a6175;
    --tx-3:         #9da4b8;
    --accent:       #4f9cf9;
    --accent-h:     #6eb3ff;
    --accent-glow:  rgba(79,156,249,.1);
    --accent-ring:  rgba(79,156,249,.22);
    --usr-bub:      #e4effe;
    --ai-bub:       #ffffff;
    --inp-bg:       #ffffff;
    --danger:       #e84040;
    --r:            11px;
    --r-sm:         7px;
    --fb:           'Plus Jakarta Sans', sans-serif;
    --fs:           'Sora', sans-serif;
    --transition:   all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}""",
    "Crimson Noir": """
:root {
    --bg:           #080808;
    --sb-bg:        #0c0c0c;
    --s1:           #111111;
    --s2:           #181818;
    --s3:           #1e1e1e;
    --border:       #2a1c1c;
    --border-h:     #3d2424;
    --tx:           #f2ede8;
    --tx-2:         #7a6868;
    --tx-3:         #3d3030;
    --accent:       #cc3333;
    --accent-h:     #e04545;
    --accent-glow:  rgba(204,51,51,.1);
    --accent-ring:  rgba(204,51,51,.22);
    --usr-bub:      #160f0f;
    --ai-bub:       #0c0c0c;
    --inp-bg:       #0c0c0c;
    --danger:       #ff4444;
    --r:            11px;
    --r-sm:         7px;
    --fb:           'Plus Jakarta Sans', sans-serif;
    --fs:           'Sora', sans-serif;
    --transition:   all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}""",
}

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&family=Sora:wght@300;400;500;600&display=swap');
{theme_vars}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body, [data-testid="stAppViewContainer"] {{
    background: var(--bg) !important;
    font-family: var(--fs) !important;
    color: var(--tx) !important;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
}}
::-webkit-scrollbar {{ width: 3px; height: 3px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}
#MainMenu, footer, header {{ visibility: hidden !important; }}
[data-testid="stDecoration"] {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}
.block-container {{ padding-top: 1rem !important; padding-bottom: 2rem !important; }}
[data-testid="stSidebar"] {{ background: var(--sb-bg) !important; border-right: 1px solid var(--border) !important; }}
[data-testid="stSidebar"] * {{ font-family: var(--fs) !important; }}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {{ color: var(--accent) !important; font-family: var(--fb) !important; }}
[data-testid="stSidebar"] [data-testid="stTextInput"] input,
[data-testid="stSidebar"] div[data-baseweb="input"] input {{
    background: var(--s1) !important; border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important; color: var(--tx) !important;
    font-family: var(--fs) !important; font-size: 0.82rem !important;
}}
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {{ background: var(--accent) !important; border: none !important; }}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider label {{
    color: var(--tx-2) !important; font-size: 0.72rem !important; font-weight: 600 !important;
    letter-spacing: 0.07em !important; text-transform: uppercase !important; font-family: var(--fb) !important;
}}
.nova-sidebar-brand {{ padding: 18px 14px 14px; border-bottom: 1px solid var(--border); margin-bottom: 6px; }}
.nova-sb-logo {{ display: flex; align-items: center; gap: 9px; margin-bottom: 10px; }}
.nova-sb-mark {{
    width: 28px; height: 28px; border-radius: 7px;
    background: var(--accent-glow); border: 1px solid var(--accent-ring);
    display: flex; align-items: center; justify-content: center;
    color: var(--accent); font-family: var(--fb);
    font-size: 13px; font-weight: 800; letter-spacing: -.02em; flex-shrink: 0;
}}
.nova-sb-name {{ font-family: var(--fb); font-size: 15px; font-weight: 700; color: var(--tx); letter-spacing: -.03em; }}
.nova-sb-pill {{
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 10px; background: rgba(200,167,120,0.07);
    border: 1px solid var(--accent-ring); border-radius: 20px;
    font-size: 10px; font-weight: 700; color: var(--accent);
    font-family: var(--fb); letter-spacing: .06em;
}}
.nova-sb-dot {{
    width: 5px; height: 5px; border-radius: 50%;
    background: var(--accent); box-shadow: 0 0 6px var(--accent);
    animation: novaPulse 2s infinite;
}}
@keyframes novaPulse {{ 0%,100%{{opacity:1;transform:scale(1);}}50%{{opacity:.5;transform:scale(1.3);}} }}
.nova-sb-divider {{ display: flex; align-items: center; gap: 8px; margin: 14px 0 8px; padding: 0 4px; }}
.nova-sb-divider span {{
    font-size: 9.5px; font-weight: 700; letter-spacing: .1em;
    text-transform: uppercase; color: var(--tx-3);
    font-family: var(--fb); white-space: nowrap;
}}
.nova-sb-divider::before, .nova-sb-divider::after {{ content: ''; flex: 1; height: 1px; background: var(--border); }}
.nova-model-meta {{ font-size: 0.68rem; font-family: var(--fb); letter-spacing: .04em; margin-top: -4px; margin-bottom: 6px; padding: 0 2px; }}
.nova-api-status {{ font-size: 0.68rem; font-family: var(--fb); margin-top: -4px; margin-bottom: 6px; padding: 0 2px; }}
.nova-creativity-tag {{ font-size: 0.68rem; color: var(--tx-2); font-family: var(--fb); margin-top: -4px; margin-bottom: 6px; padding: 0 2px; }}
[data-testid="stMetric"] {{ background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r) !important; padding: 0.8rem 1rem !important; }}
[data-testid="stMetricValue"] {{ color: var(--accent) !important; font-family: var(--fb) !important; font-size: 1.3rem !important; font-weight: 800 !important; }}
[data-testid="stMetricLabel"] {{ color: var(--tx-2) !important; }}
[data-testid="stMetricDelta"] {{ color: var(--accent) !important; }}
.nova-landing {{ min-height: 85vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 40px 20px; position: relative; }}
.nova-landing-mark {{ width: 72px; height: 72px; border-radius: 18px; background: var(--s1); border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; margin: 0 auto 28px; font-family: var(--fb); font-size: 28px; font-weight: 800; color: var(--accent); }}
.nova-landing-eyebrow {{ font-family: var(--fb); font-size: 10px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--tx-3); margin-bottom: 14px; }}
.nova-landing-title {{ font-family: var(--fb); font-size: clamp(2.8rem, 7vw, 5.5rem); font-weight: 800; letter-spacing: -.05em; color: var(--tx); line-height: 1.05; margin-bottom: 16px; }}
.nova-landing-title span {{ color: var(--accent); }}
.nova-landing-sub {{ font-family: var(--fs); font-size: 15px; color: var(--tx-2); max-width: 340px; line-height: 1.75; margin: 0 auto 38px; }}
.nova-header {{ padding: 20px 0 12px; border-bottom: 1px solid var(--border); margin-bottom: 22px; display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }}
.nova-header-brand {{ display: flex; align-items: center; gap: 10px; }}
.nova-header-mark {{ width: 32px; height: 32px; border-radius: 8px; background: var(--accent-glow); border: 1px solid var(--accent-ring); display: flex; align-items: center; justify-content: center; color: var(--accent); font-family: var(--fb); font-size: 14px; font-weight: 800; }}
.nova-header-name {{ font-family: var(--fb); font-size: 17px; font-weight: 700; color: var(--tx); letter-spacing: -.03em; }}
.nova-header-tag {{ font-size: 9.5px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--tx-3); background: var(--s1); border: 1px solid var(--border); padding: 2px 9px; border-radius: 20px; font-family: var(--fb); }}
.nova-stats-row {{ display: flex; gap: 10px; margin-bottom: 22px; flex-wrap: wrap; }}
.nova-stat-card {{ flex: 1; min-width: 100px; background: var(--s1); border: 1px solid var(--border); border-radius: var(--r); padding: 12px 16px; transition: border-color .18s; }}
.nova-stat-card:hover {{ border-color: var(--border-h); }}
.nova-stat-value {{ font-family: var(--fb); font-size: 1.4rem; font-weight: 800; color: var(--accent); letter-spacing: -.03em; }}
.nova-stat-label {{ font-size: 9.5px; color: var(--tx-3); text-transform: uppercase; letter-spacing: .1em; font-family: var(--fb); margin-top: 2px; }}
.nova-chip-row {{ display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 20px; }}
.nova-chip {{ padding: 3px 12px; background: var(--s1); border: 1px solid var(--border); border-radius: 20px; font-size: 11px; color: var(--tx-2); font-family: var(--fs); transition: var(--transition); }}
.nova-chip:hover {{ border-color: var(--accent-ring); color: var(--accent); }}
[data-testid="stTabs"] [role="tablist"] {{ background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r) !important; padding: 5px !important; gap: 3px !important; margin-bottom: 18px !important; }}
[data-testid="stTabs"] [role="tab"] {{ background: transparent !important; color: var(--tx-2) !important; border: 1px solid transparent !important; border-radius: var(--r-sm) !important; padding: 7px 18px !important; font-family: var(--fb) !important; font-weight: 600 !important; font-size: 0.8rem !important; letter-spacing: .02em !important; transition: var(--transition) !important; }}
[data-testid="stTabs"] [role="tab"]:hover {{ color: var(--tx) !important; background: var(--s2) !important; border-color: var(--border) !important; }}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{ background: var(--s2) !important; color: var(--accent) !important; border-color: var(--accent-ring) !important; }}
[data-testid="stTabs"] [data-testid="stTabPanel"] {{ border: none !important; padding: 0 !important; }}
.nova-card {{ background: var(--s1); border: 1px solid var(--border); border-radius: var(--r); padding: 22px 24px; margin-bottom: 16px; transition: border-color .18s; }}
.nova-card:hover {{ border-color: var(--border-h); }}
.nova-card-accent {{ background: var(--s1); border: 1px solid var(--accent-ring); border-radius: var(--r); padding: 22px 24px; margin-bottom: 16px; }}
.nova-card-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 16px; padding-bottom: 14px; border-bottom: 1px solid var(--border); }}
.nova-card-icon {{ width: 36px; height: 36px; border-radius: var(--r-sm); background: var(--accent-glow); border: 1px solid var(--accent-ring); display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }}
.nova-card-title {{ font-family: var(--fb); font-size: 14px; font-weight: 700; color: var(--tx); letter-spacing: -.02em; }}
.nova-card-sub {{ font-size: 11px; color: var(--tx-3); font-family: var(--fs); margin-top: 2px; }}
.nova-drop-zone {{ border: 1px dashed var(--border-h); border-radius: var(--r); padding: 36px 20px; text-align: center; background: var(--s1); transition: var(--transition); cursor: pointer; margin-bottom: 12px; }}
.nova-drop-zone:hover {{ border-color: var(--accent-ring); background: var(--accent-glow); }}
.nova-drop-icon {{ font-size: 1.6rem; margin-bottom: 10px; opacity: .7; }}
.nova-drop-title {{ font-family: var(--fb); font-size: 13px; font-weight: 600; color: var(--tx); margin-bottom: 4px; }}
.nova-drop-sub {{ font-size: 11px; color: var(--tx-3); }}
.nova-msg-wrap {{ margin-bottom: 18px; animation: novaMsgIn .2s ease both; }}
@keyframes novaMsgIn {{ from{{opacity:0;transform:translateY(5px);}}to{{opacity:1;transform:translateY(0);}} }}
.nova-msg-header-ai {{ display:flex; align-items:center; gap:8px; margin-bottom:6px; }}
.nova-msg-header-user {{ display:flex; align-items:center; gap:8px; margin-bottom:6px; justify-content:flex-end; }}
.nova-msg-av {{ width:26px; height:26px; border-radius:50%; flex-shrink:0; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; font-family:var(--fb); }}
.nova-msg-av.ai {{ background:var(--s1); color:var(--accent); border:1px solid var(--accent-ring); }}
.nova-msg-av.user {{ background:var(--s2); color:var(--tx-2); border:1px solid var(--border); }}
.nova-msg-who {{ font-size:9.5px; font-weight:700; letter-spacing:.07em; text-transform:uppercase; color:var(--tx-3); font-family:var(--fb); }}
.nova-bub-ai {{ background:var(--ai-bub); border:1px solid var(--border); padding:12px 15px; border-radius:2px var(--r) var(--r) var(--r); font-size:13.5px; line-height:1.72; color:var(--tx); }}
.nova-bub-user {{ background:var(--usr-bub); border:1px solid var(--border); padding:10px 14px; border-radius:var(--r) 2px var(--r) var(--r); font-size:13.5px; line-height:1.72; color:var(--tx); margin-left:auto; max-width:85%; }}
.nova-copy-row {{ display:flex; align-items:center; gap:6px; margin-top:5px; padding-left:2px; }}
.nova-dots {{ display:flex; gap:4px; padding:3px 0; align-items:center; }}
.nova-dots span {{ width:5px; height:5px; background:var(--tx-3); border-radius:50%; animation:novaDot 1.3s infinite; }}
.nova-dots span:nth-child(2){{animation-delay:.17s;}}
.nova-dots span:nth-child(3){{animation-delay:.34s;}}
@keyframes novaDot{{0%,80%,100%{{opacity:.2;transform:scale(.7);}}40%{{opacity:1;transform:scale(1);}}}}
.nova-response-card {{ background: var(--s1); border: 1px solid var(--border); border-radius: var(--r); padding: 20px 22px; margin-top: 16px; position: relative; overflow: hidden; }}
.nova-response-card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, var(--accent), transparent); }}
.nova-response-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }}
.nova-response-title {{ font-family: var(--fb); font-size: 13px; font-weight: 700; color: var(--tx); letter-spacing: -.02em; }}
.nova-response-label {{ font-size: 9px; font-family: var(--fb); color: var(--accent); letter-spacing: .1em; text-transform: uppercase; background: var(--accent-glow); border: 1px solid var(--accent-ring); padding: 2px 10px; border-radius: 20px; }}
.nova-thinking {{ background: var(--s1); border: 1px solid var(--border); border-radius: var(--r); padding: 20px; text-align: center; margin: 10px 0; }}
.nova-thinking-text {{ font-size: 11px; color: var(--accent); font-family: var(--fb); letter-spacing: .08em; text-transform: uppercase; margin-top: 8px; animation: novaFadeText 1.5s ease-in-out infinite; }}
@keyframes novaFadeText{{0%,100%{{opacity:.4;}}50%{{opacity:1;}}}}
.nova-voice-orb-wrap {{ display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 28px 20px; }}
.nova-voice-orb {{ width: 110px; height: 110px; border-radius: 50%; background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%); border: 1px solid var(--accent-ring); display: flex; align-items: center; justify-content: center; font-size: 2.4rem; box-shadow: 0 0 28px var(--accent-glow); animation: novaOrbPulse 3s ease-in-out infinite; cursor: pointer; transition: var(--transition); margin-bottom: 14px; }}
@keyframes novaOrbPulse{{0%,100%{{box-shadow:0 0 28px var(--accent-glow);}}50%{{box-shadow:0 0 50px var(--accent-ring);}}}}
.nova-voice-status {{ font-size: 10px; color: var(--tx-3); font-family: var(--fb); letter-spacing: .12em; text-transform: uppercase; }}
.nova-pipeline {{ background: var(--s2); border: 1px solid var(--border); border-radius: var(--r-sm); padding: 14px 16px; font-size: 11.5px; color: var(--tx-2); font-family: var(--fs); line-height: 2.1; }}
.nova-pipeline-title {{ font-family: var(--fb); font-size: 9.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--accent); margin-bottom: 6px; }}
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {{ background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; color: var(--tx) !important; font-family: var(--fs) !important; font-size: 0.87rem !important; }}
[data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {{ border-color: var(--accent-ring) !important; box-shadow: 0 0 0 3px var(--accent-glow) !important; outline: none !important; }}
[data-baseweb="select"] > div {{ background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; color: var(--tx) !important; }}
[data-testid="stFileUploader"] {{ background: var(--s1) !important; border: 1px dashed var(--border-h) !important; border-radius: var(--r) !important; }}
[data-testid="stAlert"] {{ background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; }}
[data-testid="stCheckbox"] label {{ color: var(--tx-2) !important; font-size: 0.82rem !important; }}
[data-testid="stRadio"] label {{ color: var(--tx-2) !important; font-size: 0.82rem !important; }}
code, pre {{ background: var(--s2) !important; border: 1px solid var(--border) !important; border-radius: 6px !important; color: var(--accent) !important; font-family: 'Courier New', monospace !important; }}
hr {{ border-color: var(--border) !important; margin: 1.5rem 0 !important; }}
[data-testid="stButton"] button {{ background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; color: var(--tx-2) !important; font-family: var(--fb) !important; font-size: 12.5px !important; font-weight: 600 !important; transition: var(--transition) !important; }}
[data-testid="stButton"] button:hover {{ background: var(--s2) !important; border-color: var(--border-h) !important; color: var(--tx) !important; }}
[data-testid="stButton"] button[kind="primary"] {{ background: var(--accent-glow) !important; border-color: var(--accent-ring) !important; color: var(--accent) !important; }}
[data-testid="stButton"] button[kind="primary"]:hover {{ background: rgba(200,167,120,.18) !important; border-color: var(--accent) !important; }}
[data-testid="stDownloadButton"] button {{ background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; color: var(--tx-2) !important; font-family: var(--fb) !important; font-size: 12px !important; }}
.nova-footer {{ text-align: center; padding: 24px 10px 12px; margin-top: 32px; border-top: 1px solid var(--border); }}
.nova-footer-text {{ font-size: 10px; color: var(--tx-3); font-family: var(--fb); letter-spacing: .1em; text-transform: uppercase; }}
.nova-footer-text span {{ color: var(--accent); }}
.nova-bub-ai .stMarkdown p,
.nova-bub-user .stMarkdown p {{ margin: 0 0 6px 0; }}
[data-testid="InputInstructions"] {{ display: none !important; }}
/* ── Login Wall ── */
.nexus-login-wall {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(13,13,16,0.96);
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    z-index: 999998;
    display: flex; align-items: center; justify-content: center;
    padding: 20px;
}
.nexus-login-card {
    background: var(--s1); border: 1px solid var(--border-h);
    border-radius: 18px; padding: 36px 32px;
    max-width: 420px; width: 100%; text-align: center;
    box-shadow: 0 24px 80px rgba(0,0,0,0.6);
}
.nexus-login-icon {
    font-size: 40px; margin-bottom: 16px;
}
.nexus-login-title {
    font-family: var(--fb); font-size: 20px; font-weight: 800;
    color: var(--tx); letter-spacing: -.03em; margin-bottom: 8px;
}
.nexus-login-sub {
    font-family: var(--fs); font-size: 13px; color: var(--tx-2);
    line-height: 1.7; margin-bottom: 24px;
}
.nexus-login-badge {
    display: inline-block; background: var(--accent-glow);
    border: 1px solid var(--accent-ring); border-radius: 20px;
    padding: 4px 14px; font-family: var(--fb); font-size: 11px;
    font-weight: 700; color: var(--accent); letter-spacing: .06em;
    margin-bottom: 20px;
}
.nexus-free-bar {
    background: var(--s2); border-radius: 8px; height: 6px;
    margin: 12px 0 20px; overflow: hidden;
}
.nexus-free-fill {
    height: 100%; border-radius: 8px;
    background: linear-gradient(90deg, var(--accent), var(--accent-h));
    transition: width .4s ease;
}
/* ── Image Vision Section ── */
.img-upload-zone {
    border: 2px dashed var(--border-h);
    border-radius: var(--r);
    padding: 32px 20px;
    text-align: center;
    background: var(--s1);
    transition: var(--transition);
    margin-bottom: 4px;
}
.img-upload-zone:hover { border-color: var(--accent); background: var(--s2); }
.img-upload-icon { font-size: 36px; margin-bottom: 10px; }
.img-upload-title {
    font-family: var(--fb); font-size: 14px; font-weight: 700;
    color: var(--tx); margin-bottom: 4px;
}
.img-upload-sub {
    font-family: var(--fb); font-size: 11px; color: var(--tx-3);
    letter-spacing: .06em; text-transform: uppercase;
}
.img-preview-wrap {
    border-radius: var(--r); overflow: hidden;
    border: 1px solid var(--border); margin: 12px 0;
    background: var(--s1);
}
.img-meta-row {
    display: flex; align-items: center; gap: 12px;
    padding: 8px 12px; background: var(--s2);
    border-top: 1px solid var(--border);
    font-family: var(--fb); font-size: 10px; color: var(--tx-3);
    letter-spacing: .05em;
}
.img-meta-dot { color: var(--accent); font-size: 8px; }
.img-mode-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 8px; margin: 12px 0;
}
.img-mode-card {
    background: var(--s1); border: 1px solid var(--border);
    border-radius: 10px; padding: 11px 14px; cursor: pointer;
    transition: var(--transition); text-align: left;
}
.img-mode-card:hover { border-color: var(--accent); background: var(--s2); }
.img-mode-card.selected { border-color: var(--accent); background: var(--accent-glow); }
.img-mode-icon { font-size: 18px; margin-bottom: 4px; }
.img-mode-label {
    font-family: var(--fb); font-size: 11px; font-weight: 700;
    color: var(--tx); display: block; margin-bottom: 2px;
}
.img-mode-desc { font-family: var(--fs); font-size: 10px; color: var(--tx-3); }
.img-result-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 18px; background: var(--s2);
    border: 1px solid var(--border); border-radius: var(--r) var(--r) 0 0;
    margin-top: 20px;
}
.img-result-title {
    font-family: var(--fb); font-size: 13px; font-weight: 700; color: var(--tx);
}
.img-result-badge {
    font-family: var(--fb); font-size: 9px; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    color: var(--accent); background: var(--accent-glow);
    border: 1px solid var(--accent-ring); border-radius: 20px; padding: 3px 10px;
}
.img-result-body {
    background: var(--s1); border: 1px solid var(--border);
    border-top: none; border-radius: 0 0 var(--r) var(--r);
    padding: 18px 18px 14px;
}
/* Hide keyboard_double artifact */
[data-testid="stSidebarContent"] > div:first-child > small,
.st-emotion-cache-pkbazv, .eyeqlp51 {{ display: none !important; }}
section[data-testid="stSidebar"] > div > div > div > div:first-child small {{ display:none !important; }}
/* Claude-like sidebar */
.nexus-new-chat {{
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; margin: 8px 8px 4px;
    background: transparent; border: 1px solid var(--border);
    border-radius: 10px; cursor: pointer; transition: var(--transition);
    font-family: var(--fb); font-size: 13px; font-weight: 600; color: var(--tx);
    width: calc(100% - 16px);
}}
.nexus-new-chat:hover {{ background: var(--s2); border-color: var(--border-h); }}
.nexus-new-chat-icon {{ font-size: 16px; }}
.nexus-section-label {{
    font-size: 9.5px; font-weight: 700; letter-spacing: .1em;
    text-transform: uppercase; color: var(--tx-3); font-family: var(--fb);
    padding: 14px 14px 6px; display: block;
}}
.nexus-chat-item {{
    display: flex; align-items: center; gap: 9px;
    padding: 9px 14px; margin: 1px 6px; border-radius: 8px;
    cursor: pointer; transition: background .12s;
    font-family: var(--fs); font-size: 13px; color: var(--tx-2);
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}}
.nexus-chat-item:hover {{ background: var(--s2); color: var(--tx); }}
.nexus-chat-item.active {{ background: var(--s2); color: var(--tx); }}
.nexus-chat-icon {{ font-size: 14px; flex-shrink: 0; opacity: .6; }}
.nexus-chat-title {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }}
.nexus-settings-btn {{
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; margin: 4px 6px;
    border-radius: 8px; cursor: pointer; transition: background .12s;
    font-family: var(--fb); font-size: 13px; color: var(--tx-2);
}}
.nexus-settings-btn:hover {{ background: var(--s2); color: var(--tx); }}
.nexus-settings-panel {{
    background: var(--s1); border: 1px solid var(--border);
    border-radius: var(--r); margin: 6px 8px; padding: 14px;
}}
.nexus-user-row {{
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; margin: 4px 6px;
    border-top: 1px solid var(--border); margin-top: 8px;
    font-family: var(--fb); font-size: 13px; color: var(--tx-2);
}}
.nexus-avatar {{
    width: 30px; height: 30px; border-radius: 50%;
    background: var(--accent-glow); border: 1px solid var(--accent-ring);
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700; color: var(--accent); flex-shrink: 0;
}}
[data-testid="stTextInput"] input {{ padding-right: 12px !important; }}
.nova-bub-ai {{ cursor: pointer; user-select: none; -webkit-user-select: none; }}
.nova-ctx-menu {{
    position: fixed; background: var(--s2); border: 1px solid var(--border-h);
    border-radius: 12px; padding: 6px 0; z-index: 99999;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    font-family: var(--fb); min-width: 160px;
    animation: ctxIn .15s ease;
}}
@keyframes ctxIn {{ from{{opacity:0;transform:scale(.95);}} to{{opacity:1;transform:scale(1);}} }}
.nova-ctx-item {{
    padding: 11px 18px; cursor: pointer; font-size: 13px;
    color: var(--tx); display: flex; align-items: center; gap: 10px;
    transition: background .12s;
}}
.nova-ctx-item:hover {{ background: var(--s3); }}
.nova-ctx-item:active {{ background: var(--border); }}
.nova-ctx-sep {{ height: 1px; background: var(--border); margin: 4px 0; }}
.nova-copy-toast {{
    position: fixed; bottom: 90px; left: 50%; transform: translateX(-50%);
    background: var(--accent); color: #0d0d10; padding: 7px 20px;
    border-radius: 20px; font-size: 12px; font-weight: 700;
    font-family: var(--fb); z-index: 999999; letter-spacing: .04em;
    animation: toastIn .2s ease;
}}
@keyframes toastIn {{ from{{opacity:0;transform:translateX(-50%) translateY(10px);}} to{{opacity:1;transform:translateX(-50%) translateY(0);}} }}
</style>
"""

# ═══════════════════════════════════════════════════════
#  PERSONAS
# ═══════════════════════════════════════════════════════
PERSONAS = {
    "NEXUS Default": (
        "You are NEXUS — a sharp, thoughtful AI assistant. "
        "You\'re not robotic or overly formal. Talk like a knowledgeable friend who knows a lot. "
        "Be direct, clear, sometimes a little witty, but always genuinely helpful. "
        "Give real answers, not fluffy ones. Use Markdown when it helps readability. "
        "CRITICAL LANGUAGE RULE: Always detect the language the user writes in and respond ONLY in that exact language. If they write in Hindi — respond in Hindi. If Hinglish (Hindi+English mix) — respond in Hinglish. If English — respond in English. Never switch languages unless user asks. "
        "Never mention which AI model or company powers you."
    ),
    "Coding Expert": (
        "You are NEXUS in Coding Expert mode — a senior software engineer. "
        "Deep expertise in Python, JavaScript, web development, databases, and DevOps. "
        "Always provide clean, production-ready code with comments. "
        "Proactively point out bugs and edge cases. "
        "Use Markdown code blocks with language tags for all code. "
        "CRITICAL LANGUAGE RULE: Always detect the language the user writes in and respond ONLY in that exact language. If they write in Hindi — respond in Hindi. If Hinglish (Hindi+English mix) — respond in Hinglish. If English — respond in English. Never switch languages unless user asks. "
        "Never mention which AI model or company powers you."
    ),
    "Data Analyst": (
        "You are NEXUS in Data Analyst mode. "
        "Specialize in data analysis, statistics, business intelligence, and visualization. "
        "Provide structured, numbered insights. Use tables in Markdown where applicable. "
        "Always quantify findings and suggest data-driven next steps. "
        "CRITICAL LANGUAGE RULE: Always detect the language the user writes in and respond ONLY in that exact language. If they write in Hindi — respond in Hindi. If Hinglish (Hindi+English mix) — respond in Hinglish. If English — respond in English. Never switch languages unless user asks. "
        "Never mention which AI model or company powers you."
    ),
    "Teacher / ELI5": (
        "You are NEXUS in Teacher mode. "
        "Explain everything as simply as possible — like teaching a curious 12-year-old. "
        "Use analogies, real-world examples, and step-by-step breakdowns. "
        "Avoid jargon unless you immediately explain it. Make learning enjoyable. "
        "CRITICAL LANGUAGE RULE: Always detect the language the user writes in and respond ONLY in that exact language. If they write in Hindi — respond in Hindi. If Hinglish (Hindi+English mix) — respond in Hinglish. If English — respond in English. Never switch languages unless user asks. "
        "Never mention which AI model or company powers you."
    ),
    "Creative Writer": (
        "You are NEXUS in Creative Writer mode — a skilled storyteller and copywriter. "
        "Write with vivid language, compelling narrative, and strong voice. "
        "Adapt tone from dark/serious to light/playful as needed. "
        "Always produce polished, publication-ready creative content. "
        "CRITICAL LANGUAGE RULE: Always detect the language the user writes in and respond ONLY in that exact language. If they write in Hindi — respond in Hindi. If Hinglish (Hindi+English mix) — respond in Hinglish. If English — respond in English. Never switch languages unless user asks. "
        "Never mention which AI model or company powers you."
    ),
}

# ═══════════════════════════════════════════════════════
#  PROMPT TEMPLATES
# ═══════════════════════════════════════════════════════
PROMPT_TEMPLATES = [
    ("🔍 Summarize", "Give me a concise summary of what we've discussed so far."),
    ("⚡ Key Points", "List the 5 most important key points from our conversation."),
    ("🐛 Debug This", "Review the code or content above and identify any bugs or issues."),
    ("📊 Analyze", "Analyze this in depth and give me structured insights."),
    ("🎯 Action Items", "Based on our conversation, what are the next concrete action steps?"),
    ("🔄 Simplify", "Explain this in the simplest possible terms."),
]

# ═══════════════════════════════════════════════════════
#  SAFETY FILTER
# ═══════════════════════════════════════════════════════
_BLACKLIST: dict = {
    "terrorism": [
        # Groups & ideology
        "isis","isil","al qaeda","al-qaeda","taliban","boko haram","hezbollah",
        "hamas attack","lashkar","jaish","hizbul","al shabaab","wagner group attack",
        "jihadist attack","holy war recruit","terrorist recruit","radicalize",
        "join isis","join taliban","terror cell","terror network","sleeper cell",
        # Attacks & planning
        "suicide bomber","suicide vest","suicide attack plan",
        "bomb making","bomb recipe","how to make a bomb","make a bomb",
        "build a bomb","assemble a bomb","improvised explosive device",
        "ied recipe","ied construction","detonator","car bomb","pipe bomb",
        "letter bomb","pressure cooker bomb","nail bomb","truck attack plan",
        "mass shooting plan","attack planning","attack government","attack civilians",
        "blow up building","blow up school","blow up mosque","blow up temple",
        "blow up church","blow up hospital","attack police","kill officers",
        "assassinate","assassination plan","kill politician","kill president",
        "hostage taking plan","kidnapping plan","ransom demand",
    ],
    "weapons": [
        # Firearms illegal
        "how to make a gun","make a gun at home","homemade gun","zip gun",
        "3d printed gun","3d print gun","ghost gun","untraceable firearm",
        "convert pistol to automatic","convert semi to full auto",
        "illegal silencer","suppressor diy","silencer diy",
        "how to get gun without license","buy gun illegally",
        # Explosives
        "make explosives","homemade explosives","explosive recipe",
        "fertilizer bomb","ammonium nitrate bomb","tnt recipe",
        "c4 explosive","plastic explosive","semtex","thermite recipe",
        "molotov cocktail recipe","incendiary device",
        # Chemical & bio
        "chemical weapon","weaponize chemical","nerve agent","sarin","vx nerve",
        "mustard gas","chlorine gas weapon","phosgene","tabun",
        "cyanide recipe","ricin recipe","how to make poison","poison weapon",
        "bioweapon","anthrax recipe","weaponize bacteria","weaponize virus",
        "plague weapon","ebola weapon","smallpox weapon",
        # Radiological
        "dirty bomb","radiological weapon","nuclear device","nuclear bomb recipe",
    ],
    "cybercrime": [
        # Malware creation
        "write malware","create malware","malware code","malware script",
        "ransomware code","ransomware script","create ransomware","write ransomware",
        "virus code","trojan code","worm code","spyware code",
        "rootkit","rootkit install","rootkit script",
        "backdoor script","create backdoor","inject backdoor",
        "rat tool","remote access trojan","create rat","write rat",
        # Attack tools
        "ddos script","ddos tool","ddos attack tool","launch ddos",
        "botnet script","create botnet","botnet setup",
        "exploit code","write exploit","create exploit","0day exploit code",
        "buffer overflow exploit","shell injection code",
        # Credential theft
        "phishing page code","phishing kit","phishing site code",
        "credential harvester","cookie stealer","session hijack script",
        "keylogger code","keylogger script","write keylogger","build keylogger",
        "password stealer","credential stuffing tool","brute force tool",
        "password cracker tool","hash cracker","rainbow table crack",
        # Account takeover
        "hack account","hack someone account","hack instagram","hack facebook",
        "hack whatsapp","hack gmail","hack snapchat","hack wifi password",
        "steal account","take over account","bypass otp","bypass 2fa hack",
        "sim swap hack","account takeover script",
        # System intrusion
        "hack into server","hack into database","hack into website",
        "sql injection attack","sqli attack","blind sql injection attack",
        "remote code execution attack","rce exploit","privilege escalation exploit",
        "penetrate network illegally","network intrusion script",
    ],
    "child_safety": [
        # CSAM
        "child abuse","child sexual abuse","csam","child pornography",
        "minor pornography","underage pornography","teen pornography",
        "child nude","minor nude","underage nude","nude minor",
        "child explicit","minor explicit","underage explicit",
        # Fictional but harmful
        "lolicon","shotacon","shota","loli sexual","loli explicit",
        "minor hentai","underage hentai",
        # Grooming
        "groom child","grooming child","groom minor","grooming minor",
        "seduce minor","seduce child","gain trust child","befriend child for sex",
        "child meeting stranger","meet child secretly",
    ],
    "hate_speech": [
        # Violence against groups
        "kill all muslims","kill all hindus","kill all jews","kill all christians",
        "kill all sikhs","kill all blacks","kill all whites","kill minorities",
        "death to muslims","death to hindus","death to jews","death to christians",
        "exterminate muslims","exterminate hindus","exterminate jews",
        # Genocide & ethnic violence
        "ethnic cleansing","genocide plan","mass killing plan",
        "religious riot plan","communal riot plan","incite communal violence",
        "incite riot","lynch mob","mob lynching plan",
        "caste violence","dalit violence","minority attack",
        # Supremacy
        "white supremacy","white power manifesto","aryan supremacy",
        "neo nazi","nazi propaganda","third reich","heil hitler propaganda",
        "master race","inferior race","subhuman race",
        # Targeted harassment
        "doxxing plan","expose personal info to harm","swatting plan",
        "coordinate harassment","mass report campaign to silence",
    ],
    "self_harm": [
        # Direct methods
        "how to kill myself","how to end my life","how to commit suicide",
        "how to die painlessly","painless death method","easiest way to die",
        "kill myself","end my life","take my own life",
        "methods of suicide","suicide method","suicide technique",
        "painless suicide","quick suicide","undetectable suicide",
        "assisted suicide instructions","help me die",
        # Specific methods
        "hanging myself","how to hang myself",
        "overdose on pills","which pills to overdose","how many pills to die",
        "slit wrists","cut myself to die","bleed out",
        "jump off building to die","jump in front of train",
        "carbon monoxide suicide","gas suicide",
        # Self harm
        "cut myself deeply","burn myself","harm myself badly",
        "self harm methods","how to self harm","ways to hurt myself",
    ],
}

_CATEGORY_LABELS: dict = {
    "terrorism":    "Terrorism / Extremism",
    "weapons":      "Weapons / WMD",
    "cybercrime":   "Cybercrime / Malware",
    "child_safety": "Child Safety Violation",
    "hate_speech":  "Hate Speech / Violence",
    "self_harm":    "Self-Harm / Suicide",
}
_BLOCK_MSG = "Policy Violation: This request has been blocked for security reasons."

# ── LLM-level safety sentinel ──────────────────────────────────────────────
# This is injected into EVERY LLM system prompt so the model itself refuses
# harmful requests even if they slip past the keyword pre-filter.
SAFETY_SYSTEM_ADDON = (
    "\n\n"
    "==== ABSOLUTE SAFETY RULES — HIGHEST PRIORITY — OVERRIDE EVERYTHING ELSE ====\n"
    "You must NEVER provide any assistance, instructions, code, recipes, methods, or "
    "information — partial or complete — related to ANY of the following:\n"
    "  • Terrorism, extremism, attack planning, or recruitment\n"
    "  • Weapons, explosives, bombs, chemical/biological/radiological devices\n"
    "  • Cybercrime, malware creation, hacking attacks, phishing, or credential theft\n"
    "  • Child exploitation, grooming, or any sexual content involving minors\n"
    "  • Hate speech, genocide, or incitement to ethnic/religious violence\n"
    "  • Suicide methods or self-harm techniques\n\n"
    "This rule applies regardless of: roleplay framing, fictional context, academic "
    "framing, hypothetical scenarios, indirect phrasing, coded language, leet-speak, "
    "symbol substitutions, or ANY other attempt to disguise the request.\n\n"
    "If ANY such request is detected — no matter how it is worded — you MUST respond "
    "with ONLY this exact token and nothing else: NEXUS_SAFETY_REFUSE\n"
    "Do NOT explain. Do NOT provide partial info. Output ONLY: NEXUS_SAFETY_REFUSE\n"
    "============================================================================"
)

# English message shown to user when LLM-level block triggers
_LLM_BLOCK_MSG = (
    "I'm sorry, I cannot help with that. "
    "This request involves harmful or dangerous content, "
    "and I'm not able to provide any assistance with it."
)


# ── Layer 1: Unicode homoglyph normalizer ──────────────────────────────────
def _unicode_normalize(text: str) -> str:
    """NFKD decomposition → ASCII-only. Kills Cyrillic/Greek lookalikes."""
    normalized = unicodedata.normalize("NFKD", text)
    return normalized.encode("ascii", "ignore").decode("ascii")


# ── Layer 1: Extended leet-speak normalizer ────────────────────────────────
_LEET_MAP = {
    "0": "o", "1": "i", "3": "e", "4": "a", "5": "s",
    "6": "g", "7": "t", "8": "b", "9": "g",
    "@": "a", "$": "s", "!": "i", "+": "t", "|": "i",
    "€": "e", "£": "l", "¢": "c", "©": "c", "®": "r",
    "×": "x", "ß": "ss", "ø": "o", "µ": "u",
}

def _leet_normalize(text: str) -> str:
    for char, replacement in _LEET_MAP.items():
        text = text.replace(char, replacement)
    return text


# ── Layer 1: Full normalization pipeline ───────────────────────────────────
def _normalize(text: str) -> str:
    text = text.lower()
    text = _unicode_normalize(text)            # homoglyphs (Cyrillic о → o)
    text = _leet_normalize(text)               # leet speak (h@ck → hack)
    # Remove character-splitting: "b.o.m.b" → "bomb", "b o m b" → "bomb"
    text = re.sub(r"(?<=[a-z])[.\-_*\s]+(?=[a-z])", "", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)  # remaining specials → space
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ── Layer 1: Keyword pre-filter ────────────────────────────────────────────
def is_safe(prompt: str) -> tuple:
    cleaned = _normalize(prompt)
    for category, terms in _BLACKLIST.items():
        for term in terms:
            normalized_term = _normalize(term)
            pattern = r"\b" + re.escape(normalized_term) + r"\b"
            if re.search(pattern, cleaned):
                return False, category
    return True, None


def show_block_error(category: str):
    label = _CATEGORY_LABELS.get(category, "Policy Violation")
    st.markdown(f"""
    <div style="background:rgba(217,85,85,0.08); border:1px solid rgba(217,85,85,0.35);
                border-left:3px solid #d95555; border-radius:var(--r);
                padding:16px 20px; margin:10px 0;">
        <div style="font-family:var(--fb); font-size:11px; font-weight:700;
                    letter-spacing:.1em; text-transform:uppercase; color:#d95555; margin-bottom:6px;">
            ⊘ Security Block — {label}
        </div>
        <div style="font-family:var(--fs); font-size:13px; color:#eae8e1; line-height:1.65;">
            {_BLOCK_MSG}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  RATE LIMITER
# ═══════════════════════════════════════════════════════
RATE_LIMIT_MAX    = 20
RATE_LIMIT_WINDOW = 60


def check_rate_limit() -> bool:
    now = time.time()
    timestamps = st.session_state.get("rate_timestamps", [])
    timestamps = [t for t in timestamps if now - t < RATE_LIMIT_WINDOW]
    if len(timestamps) >= RATE_LIMIT_MAX:
        st.session_state.rate_timestamps = timestamps
        return False
    timestamps.append(now)
    st.session_state.rate_timestamps = timestamps
    return True


def approx_tokens(text: str) -> int:
    return max(1, int(len(text.split()) * 1.35))


# ═══════════════════════════════════════════════════════
#  NEURAL ENGINE — Groq Backend + Auto Fallback
# ═══════════════════════════════════════════════════════

# Internal model mapping — not shown in UI
MODEL_MAP = {
    "Ultra":    "llama-3.3-70b-versatile",
    "Balanced": "llama3-70b-8192",        # stable older 70b, not deprecated
    "Fast":     "llama-3.1-8b-instant",
}

VISION_MODEL   = "llama-3.2-11b-vision-preview"
WHISPER_MODEL  = "whisper-large-v3"

FALLBACK_MODELS = [
    "llama-3.3-70b-versatile",
    "llama3-70b-8192",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",          # mixtral removed from Groq, replaced with gemma2
]


def _groq_client(api_key: str):
    from groq import Groq
    return Groq(api_key=api_key)


def _call_groq(api_key: str, messages: list, model: str, temperature: float, stream: bool = False):
    client = _groq_client(api_key)
    return client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=2048,
        stream=stream,
    )


def _call_with_fallback(api_key: str, messages: list, primary_model: str, temperature: float) -> str:
    """Try primary model, then fallback chain. Injects safety into all system prompts."""
    # ── Inject safety addon into every system message (Layer 2) ──────────
    safe_messages = []
    has_system = False
    for msg in messages:
        if msg["role"] == "system":
            safe_messages.append({"role": "system", "content": msg["content"] + SAFETY_SYSTEM_ADDON})
            has_system = True
        else:
            safe_messages.append(msg)
    if not has_system:
        safe_messages.insert(0, {"role": "system", "content": SAFETY_SYSTEM_ADDON.strip()})

    models_to_try = [primary_model] + [m for m in FALLBACK_MODELS if m != primary_model]
    last_error = ""
    for model in models_to_try:
        try:
            resp = _call_groq(api_key, safe_messages, model, temperature)
            content = resp.choices[0].message.content

            # ── Layer 2 post-check: LLM refused with sentinel ─────────────
            if content and "NEXUS_SAFETY_REFUSE" in content.strip():
                return _LLM_BLOCK_MSG

            return content
        except Exception as e:
            last_error = str(e)
            if "invalid_api_key" in last_error.lower() or "authentication" in last_error.lower():
                return "❌ API Key galat hai. Sahi key daalo sidebar mein."
            if "rate_limit" in last_error.lower():
                time.sleep(1)
                continue
            continue
    return f"❌ Abhi kuch dikkat aa rahi hai, thodi der baad try karo. ({last_error[:80]})"


# ═══════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════

def _extract_pdf_text(file_bytes: bytes) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages_text = [page.extract_text() for page in pdf.pages]
            text = "\n\n".join(t for t in pages_text if t)
        return text.strip() or "[PDF mein koi readable text nahi mila]"
    except ImportError:
        pass
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = "\n\n".join(p.extract_text() for p in reader.pages if p.extract_text())
        return text.strip() or "[PDF text extract nahi hua]"
    except Exception as e:
        return f"[PDF extract error: {e}]"


def _extract_docx_text(file_bytes: bytes) -> str:
    try:
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    paragraphs.append(row_text)
        return "\n\n".join(paragraphs)
    except ImportError:
        return "[ERROR] python-docx not installed."
    except Exception as e:
        return f"[ERROR] Could not read DOCX: {e}"


# ═══════════════════════════════════════════════════════
#  BACKEND — Validate Key
# ═══════════════════════════════════════════════════════
def validate_api_key(api_key: str) -> tuple:
    if not api_key or len(api_key.strip()) < 20:
        return False, "Key too short or empty."
    try:
        resp = _call_groq(api_key, [{"role": "user", "content": "Say OK"}], "llama-3.1-8b-instant", 0.1)
        if resp.choices[0].message.content:
            return True, "API Key is valid ✓"
        return False, "Unexpected empty response."
    except Exception as e:
        err = str(e)
        if "invalid_api_key" in err.lower() or "authentication" in err.lower():
            return False, "Invalid API Key."
        elif "rate_limit" in err.lower():
            return True, "Key valid but rate limited right now."
        return False, f"Error: {err[:80]}"


# ═══════════════════════════════════════════════════════
#  BACKEND — Document Analysis
# ═══════════════════════════════════════════════════════
def analyze_document(
    file, api_key: str, temperature: float, model_tier: str, analysis_type: str,
    opt_hyperlinks: bool, opt_tables: bool, opt_images: bool, opt_pii: bool, opt_quotes: bool,
) -> str:
    if not api_key:
        return "⚠️ API Key nahi hai. Sidebar mein key daalo."
    try:
        file.seek(0)
        file_bytes = file.read()
        file_name  = file.name.lower()

        if file_name.endswith(".pdf"):
            content = _extract_pdf_text(file_bytes)
        elif file_name.endswith(".docx"):
            content = _extract_docx_text(file_bytes)
            if content.startswith("[ERROR]"):
                return f"❌ {content}"
        elif file_name.endswith(".csv"):
            content = file_bytes.decode("utf-8", errors="ignore")
        else:
            content = file_bytes.decode("utf-8", errors="ignore")

        if len(content) > 28000:
            content = content[:28000] + "\n\n[...document truncated at 28,000 chars...]"

        mode_instructions = {
            "Full Semantic Analysis": (
                "Provide a FULL SEMANTIC ANALYSIS:\n"
                "1. Executive Summary (3-4 lines)\n"
                "2. Key Points / Main Ideas\n"
                "3. Important Entities (names, places, numbers)\n"
                "4. Actionable Insights\n"
                "5. Overall Sentiment & Tone\n"
            ),
            "Data Extraction": (
                "Extract ALL structured data from this document:\n"
                "1. All numbers, statistics, dates, percentages\n"
                "2. Tables and lists (recreate in Markdown)\n"
                "3. Named entities: people, orgs, locations\n"
                "4. URLs, emails, phone numbers if present\n"
            ),
            "Executive Summary": (
                "Write a crisp EXECUTIVE SUMMARY (max 250 words):\n"
                "1. One-paragraph TL;DR\n"
                "2. Top 5 bullet-point takeaways\n"
                "3. Recommended next action\n"
            ),
            "Entity & Relation Mapping": (
                "Map ALL ENTITIES AND THEIR RELATIONS:\n"
                "1. People and their roles\n"
                "2. Organizations and affiliations\n"
                "3. Locations and context\n"
                "4. Key relationships between entities (as a table)\n"
            ),
            "Q&A Generation": (
                "Generate 10 insightful Q&A pairs from this document:\n"
                "Format each as:\n"
                "**Q:** [question]\n**A:** [detailed answer]\n\n"
                "Cover factual, inferential, and analytical questions.\n"
            ),
            "🔥 Roast My Document": (
                "You are a brutally honest, witty critic. ROAST this document mercilessly:\n"
                "1. What's embarrassingly wrong or weak about it\n"
                "2. The most cringe-worthy parts\n"
                "3. What a smart 10-year-old would do better\n"
                "4. A savage one-line summary\n"
                "5. Three serious improvements (after the roast)\n"
                "Be funny but constructive. Use 🔥 emoji liberally.\n"
            ),
            "🧒 ELI5 — Explain Simply": (
                "Explain this document as if talking to a curious 10-year-old:\n"
                "1. What is this about? (1-2 simple sentences)\n"
                "2. The main idea in plain English\n"
                "3. Why does it matter? (real-world analogy)\n"
                "4. 3 things to remember\n"
                "Use simple words, short sentences, fun analogies. No jargon.\n"
            ),
            "✨ Vibe Check": (
                "Do a VIBE CHECK on this document:\n"
                "1. Overall vibe: [confident/anxious/corporate/creative/etc]\n"
                "2. Emotional tone analysis\n"
                "3. Hidden intentions or subtext\n"
                "4. Trustworthiness score: X/10 (explain why)\n"
                "5. Who wrote this? (guess the author's personality)\n"
                "6. Vibe summary in one emoji + one sentence\n"
            ),
            "⚔️ Debate This": (
                "Generate a structured DEBATE on the main claims in this document:\n"
                "**PRO (Supporting arguments):**\n"
                "1. [strong argument for]\n2. [strong argument for]\n3. [strong argument for]\n\n"
                "**CON (Counter arguments):**\n"
                "1. [strong argument against]\n2. [strong argument against]\n3. [strong argument against]\n\n"
                "**Verdict:** Which side has stronger evidence based on the document?\n"
            ),
        }

        base_prompt = mode_instructions.get(analysis_type, mode_instructions["Full Semantic Analysis"])

        extra = "\nAdditional tasks:\n"
        if opt_hyperlinks: extra += "- Extract all hyperlinks found.\n"
        if opt_tables:     extra += "- Parse and reproduce all tables in Markdown.\n"
        if opt_images:     extra += "- Describe any embedded images or charts if mentioned.\n"
        if opt_pii:        extra += "- Flag and list any PII (names, emails, phone numbers, addresses).\n"
        if opt_quotes:     extra += "- Pull 3-5 notable direct quotes.\n"

        prompt = base_prompt + extra + "\nUse Markdown formatting throughout.\n"
        primary_model = MODEL_MAP.get(model_tier, MODEL_MAP["Ultra"])

        messages = [
            {"role": "system", "content": PERSONAS.get("NEXUS Default", "")},
            {"role": "user", "content": f"{prompt}\n\nDocument Content:\n\n{content}"}
        ]
        return _call_with_fallback(api_key, messages, primary_model, temperature)

    except Exception as e:
        return f"❌ Error: {str(e)[:100]}"


# ═══════════════════════════════════════════════════════
#  BACKEND — Image Vision
# ═══════════════════════════════════════════════════════
def analyze_image(
    image_bytes: bytes, mime_type: str, question: str,
    api_key: str, temperature: float, model_tier: str,
) -> str:
    if not api_key:
        return "⚠️ API Key nahi hai. Sidebar mein key daalo."
    try:
        image_b64 = base64.b64encode(image_bytes).decode()
        prompt_text = question if question.strip() else (
            "Analyze this image thoroughly:\n"
            "1. What is in the image?\n"
            "2. Key objects, people, text visible\n"
            "3. Colors, mood, composition\n"
            "4. Any notable details or anomalies\n"
            "Use Markdown formatting."
        )

        client = _groq_client(api_key)
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful image analysis assistant." + SAFETY_SYSTEM_ADDON},
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_b64}"}}
                ]
            }],
            temperature=temperature,
            max_tokens=1024,
        )
        result_content = response.choices[0].message.content
        if result_content and "NEXUS_SAFETY_REFUSE" in result_content.strip():
            return _LLM_BLOCK_MSG
        return result_content

    except Exception as e:
        err = str(e)
        if "invalid_api_key" in err.lower() or "authentication" in err.lower():
            return "❌ API Key galat hai."
        elif "rate_limit" in err.lower():
            return "❌ Rate limit hit hua. Thodi der baad try karo."
        else:
            return f"❌ Image analysis error: {err[:100]}"


# ═══════════════════════════════════════════════════════
#  BACKEND — YouTube
# ═══════════════════════════════════════════════════════
def analyze_youtube(
    url: str, api_key: str, temperature: float, model_tier: str,
    yt_mode: str, output_format: str,
) -> str:
    if not api_key:
        return "⚠️ API Key nahi hai. Sidebar mein key daalo."
    try:
        from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

        match = re.search(r"(?:v=|youtu\.be/|embed/)([^&\n?#]{11})", url)
        if not match:
            return "❌ Invalid YouTube URL. Format: `https://www.youtube.com/watch?v=VIDEO_ID`"

        video_id = match.group(1)

        try:
            # youtube-transcript-api >= 0.6.0: instance method
            ytt = YouTubeTranscriptApi()
            transcript_list = ytt.get_transcript(video_id, languages=["en", "hi", "en-IN"])
        except TypeError:
            # Fallback for older library versions (class method)
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "hi", "en-IN"])
            except Exception as e2:
                return f"❌ Transcript fetch nahi hua: {str(e2)[:80]}"
        except NoTranscriptFound:
            try:
                ytt2 = YouTubeTranscriptApi()
                transcripts = ytt2.list(video_id)
                transcript_list = transcripts.find_generated_transcript(["en", "hi"]).fetch()
            except Exception:
                return "❌ Is video mein transcript available nahi hai."
        except TranscriptsDisabled:
            return "❌ Is video mein transcripts disabled hain."

        full_text = ""
        for entry in transcript_list:
            mins = int(entry["start"]) // 60
            secs = int(entry["start"]) % 60
            full_text += f"[{mins:02d}:{secs:02d}] {entry['text']}\n"

        if len(full_text) > 28000:
            full_text = full_text[:28000] + "\n\n[...transcript truncated...]"

        mode_prompts = {
            "Full Transcript + Summary": (
                "Analyze this YouTube transcript:\n"
                "1. **Video Summary** — 3-4 line overview\n"
                "2. **Key Moments** — Important timestamps\n"
                "3. **Main Topics** — List of topics\n"
                "4. **Actionable Insights** — Key takeaways\n"
                "5. **Notable Quotes** — 2-3 important lines\n"
            ),
            "Key Moments & Timestamps": (
                "Extract KEY MOMENTS with timestamps:\n"
                "- List every significant moment with [MM:SS] timestamp\n"
                "- For each: timestamp, event/topic, why it matters\n"
                "- Present as a timeline table in Markdown\n"
            ),
            "Actionable Insights Only": (
                "Extract ONLY actionable insights:\n"
                "- List every concrete tip, recommendation, or step-by-step instruction\n"
                "- Group by theme\n"
                "- Add timestamps where the insight appears\n"
            ),
            "Speaker Diarization": (
                "Analyze speaker patterns:\n"
                "1. Identify distinct speaking styles/voices if present\n"
                "2. Map who likely said what based on context\n"
                "3. Summarize each speaker's key points\n"
                "4. Note any Q&A or debate sections\n"
            ),
            "Sentiment Timeline": (
                "Create a SENTIMENT TIMELINE:\n"
                "1. Overall sentiment: positive/negative/neutral\n"
                "2. Sentiment shifts at key timestamps\n"
                "3. Most positive and most negative moments\n"
                "4. Emotional tone summary\n"
                "5. Present as a table: [Timestamp | Topic | Sentiment | Reason]\n"
            ),
            "📝 Quiz Generator": (
                "Generate a QUIZ from this video content:\n"
                "Create 10 MCQ questions with 4 options each.\n"
                "Format:\n"
                "**Q1.** [question]\n"
                "A) option  B) option  C) option  D) option\n"
                "**Answer:** [correct option]\n\n"
                "Cover key concepts from across the video. Vary difficulty.\n"
            ),
            "📖 Chapter Detection": (
                "Detect CHAPTERS in this video transcript:\n"
                "Identify natural topic transitions and create chapter markers:\n"
                "| # | Timestamp | Chapter Title | Duration | Summary |\n"
                "|---|-----------|---------------|----------|---------|\n"
                "List every chapter with a descriptive title and 1-line summary.\n"
            ),
        }

        format_instructions = {
            "Detailed Report":  "Present as a well-structured Markdown report with headers.",
            "Bullet Points":    "Present EVERYTHING as concise bullet points only. No paragraphs.",
            "Twitter/X Thread": (
                "Format as a Twitter/X thread. Start with '🧵 1/' and number each tweet. "
                "Each tweet max 280 chars. Make it engaging and shareable."
            ),
            "Email Brief": (
                "Format as a professional email brief:\n"
                "Subject: [concise subject line]\n"
                "Body: short intro, 3-5 key points, closing line.\n"
                "Keep it under 200 words."
            ),
        }

        base   = mode_prompts.get(yt_mode, mode_prompts["Full Transcript + Summary"])
        fmt    = format_instructions.get(output_format, format_instructions["Detailed Report"])
        prompt = f"{base}\nOutput format: {fmt}\n\nTranscript:\n\n{full_text}"

        primary_model = MODEL_MAP.get(model_tier, MODEL_MAP["Ultra"])
        messages = [
            {"role": "system", "content": PERSONAS.get("NEXUS Default", "")},
            {"role": "user", "content": prompt}
        ]
        return _call_with_fallback(api_key, messages, primary_model, temperature)

    except ImportError:
        return "❌ `youtube-transcript-api` install nahi hai. requirements.txt mein add karo."
    except Exception as e:
        return f"❌ Error: {str(e)[:100]}"


# ═══════════════════════════════════════════════════════
#  BACKEND — Neural Chat
# ═══════════════════════════════════════════════════════
def neural_chat_response(messages: list, api_key: str, temperature: float, model_tier: str, persona: str = "NEXUS Default") -> str:
    if not api_key:
        return "⚠️ API Key nahi hai. Sidebar mein key daalo."

    system_prompt = PERSONAS.get(persona, PERSONAS["NEXUS Default"])
    primary_model = MODEL_MAP.get(model_tier, MODEL_MAP["Ultra"])

    groq_messages = [{"role": "system", "content": system_prompt}]
    for msg in messages:
        role = "assistant" if msg["role"] == "assistant" else "user"
        groq_messages.append({"role": role, "content": msg["content"]})

    return _call_with_fallback(api_key, groq_messages, primary_model, temperature)


# ═══════════════════════════════════════════════════════
#  BACKEND — Voice Transcription
# ═══════════════════════════════════════════════════════
def transcribe_voice(audio_bytes: bytes, api_key: str) -> str:
    try:
        client = _groq_client(api_key)
        transcription = client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes, "audio/wav"),
            model=WHISPER_MODEL,
            response_format="text",
        )
        return str(transcription)
    except Exception as e:
        return f"[Transcription error: {str(e)[:80]}]"


# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
INITIAL_GREETING = {
    "role": "assistant",
    "content": (
        "Hey! Main NEXUS hoon — tumhara AI intelligence platform.\n\n"
        "Main kar sakta hoon:\n"
        "- 📄 Documents analyze karna (PDF, DOCX, TXT, CSV)\n"
        "- ▶️ YouTube videos summarize karna timestamps ke saath\n"
        "- 🖼️ Images analyze karna\n"
        "- 💬 Kisi bhi sawaal ka jawab dena\n\n"
        "Batao, aaj kya kaam hai?"
    )
}


def _init_state():
    defaults = {
        "app_mode":        "landing",
        "chat_history":    [INITIAL_GREETING],
        "sessions":        [],          # saved chat sessions
        "input_counter":   0,
        "query_count":     0,
        "user_api_key":    "",      # Kept for compatibility
        "locked":          False,   # Whether login wall is shown
        "incognito":       False,
        "theme":           "Nova Crystal",
        "persona":         "NEXUS Default",
        "model_tier":      "Ultra",
        "temperature":     0.7,
        "rate_timestamps": [],
        "copy_states":     {},
        "show_settings":   False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


_init_state()

theme_vars = THEME_VARS.get(st.session_state.theme, THEME_VARS["Nova Crystal"])
st.markdown(BASE_CSS.replace("{theme_vars}", theme_vars), unsafe_allow_html=True)

# ─── Long-press context menu JS ───
st.markdown("""
<script>
(function() {
    let pressTimer = null;
    let activeMenu = null;
    let targetText = '';

    function removeMenu() {
        if (activeMenu) { activeMenu.remove(); activeMenu = null; }
    }

    function showToast(msg) {
        document.querySelectorAll('.nova-copy-toast').forEach(e => e.remove());
        const t = document.createElement('div');
        t.className = 'nova-copy-toast';
        t.textContent = msg;
        document.body.appendChild(t);
        setTimeout(() => t.remove(), 1600);
    }

    function showMenu(x, y, text) {
        removeMenu();
        const menu = document.createElement('div');
        menu.className = 'nova-ctx-menu';

        // Position - keep inside viewport
        const mx = Math.min(x, window.innerWidth - 175);
        const my = Math.min(y, window.innerHeight - 120);
        menu.style.left = mx + 'px';
        menu.style.top = my + 'px';

        const items = [
            { icon: '📋', label: 'Copy', action: () => {
                navigator.clipboard.writeText(text).then(() => showToast('✓ Copied!'));
                removeMenu();
            }},
            { sep: true },
            { icon: '✏️', label: 'Edit in Chat', action: () => {
                const inp = document.querySelector('[data-testid="stTextInput"] input');
                if (inp) {
                    inp.focus();
                    inp.value = text.substring(0, 200);
                    inp.dispatchEvent(new Event('input', { bubbles: true }));
                }
                removeMenu();
            }},
        ];

        items.forEach(item => {
            if (item.sep) {
                const sep = document.createElement('div');
                sep.className = 'nova-ctx-sep';
                menu.appendChild(sep);
            } else {
                const div = document.createElement('div');
                div.className = 'nova-ctx-item';
                div.innerHTML = '<span>' + item.icon + '</span><span>' + item.label + '</span>';
                div.onclick = (e) => { e.stopPropagation(); item.action(); };
                menu.appendChild(div);
            }
        });

        document.body.appendChild(menu);
        activeMenu = menu;

        setTimeout(() => {
            document.addEventListener('click', removeMenu, { once: true });
            document.addEventListener('touchstart', removeMenu, { once: true });
        }, 50);
    }

    function vibrate() {
        if (navigator.vibrate) navigator.vibrate(40);
    }

    function attachHandlers() {
        document.querySelectorAll('.nova-bub-ai').forEach(bubble => {
            if (bubble._lpAttached) return;
            bubble._lpAttached = true;

            // Touch (mobile)
            bubble.addEventListener('touchstart', (e) => {
                const text = bubble.innerText || bubble.textContent || '';
                pressTimer = setTimeout(() => {
                    vibrate();
                    const t = e.touches[0];
                    showMenu(t.clientX - 80, t.clientY - 10, text.trim());
                }, 550);
            }, { passive: true });

            bubble.addEventListener('touchend',  () => clearTimeout(pressTimer));
            bubble.addEventListener('touchmove', () => clearTimeout(pressTimer));

            // Desktop right-click
            bubble.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                const text = bubble.innerText || bubble.textContent || '';
                showMenu(e.clientX, e.clientY, text.trim());
            });
        });
    }

    // Run on load and after new messages appear
    attachHandlers();
    setInterval(attachHandlers, 1200);
})();
</script>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  LANDING PAGE
# ═══════════════════════════════════════════
def render_landing_page():
    st.markdown("""
    <div class="nova-landing">
        <div class="nova-landing-mark">N</div>
        <div class="nova-landing-eyebrow">Intelligence Platform · v5.1</div>
        <div class="nova-landing-title">NEXUS<span>.</span></div>
        <div class="nova-landing-sub">
            Next-generation multi-modal AI — document analysis,<br>
            video intelligence, image vision &amp; neural chat.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1, 1])
    with col_c:
        if st.button("[ INITIATE NEURAL LINK ]", use_container_width=True, key="cta_launch"):
            st.session_state.app_mode = "dashboard"
            st.rerun()

    st.markdown("""
    <div style="text-align:center; margin-top:44px; display:flex; justify-content:center; gap:18px; flex-wrap:wrap;">
        <span class="nova-chip">◈ Document Intelligence</span>
        <span class="nova-chip">▶ YouTube Architect</span>
        <span class="nova-chip">◎ Neural Chat</span>
        <span class="nova-chip">🖼 Image Vision</span>
        <span class="nova-chip">◉ Voice Command</span>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════
def render_limit_popup():
    """Show a friendly limit-reached popup — no API key, just start a new chat."""
    limit = FREE_MSG_LIMIT

    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.markdown(f"""
        <div style="text-align:center;padding:60px 0 28px;">
            <div style="width:64px;height:64px;border-radius:16px;
                        background:var(--accent-glow);border:1px solid var(--accent-ring);
                        display:inline-flex;align-items:center;justify-content:center;
                        font-size:28px;margin-bottom:22px;">✦</div>
            <div style="display:inline-block;background:var(--accent-glow);
                        border:1px solid var(--accent-ring);border-radius:20px;
                        padding:4px 16px;font-family:var(--fb);font-size:10px;
                        font-weight:700;color:var(--accent);letter-spacing:.1em;
                        text-transform:uppercase;margin-bottom:18px;display:block;">
                Session Limit Reached
            </div>
            <div style="font-family:var(--fb);font-size:24px;font-weight:800;
                        color:var(--tx);letter-spacing:-.03em;margin-bottom:14px;">
                You've used {limit} messages
            </div>
            <div style="font-family:var(--fs);font-size:14px;color:var(--tx-2);
                        line-height:1.85;max-width:340px;margin:0 auto 32px;">
                No worries — just start a fresh session.<br>
                Click <strong style="color:var(--accent);">New Chat</strong> to reset
                and continue enjoying NEXUS. ✨
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar — full
        st.markdown("""
        <div style="max-width:300px;margin:0 auto 32px;background:var(--s2);
                    border-radius:8px;height:5px;overflow:hidden;">
            <div style="height:100%;width:100%;border-radius:8px;
                        background:linear-gradient(90deg,var(--accent),var(--accent-h));"></div>
        </div>
        """, unsafe_allow_html=True)

        # Single CTA button
        if st.button("✦  New Chat — Continue Free", use_container_width=True,
                     type="primary", key="limit_new_chat_btn"):
            _save_current_session()
            st.session_state.chat_history  = [INITIAL_GREETING]
            st.session_state.copy_states   = {}
            st.session_state.input_counter += 1
            st.session_state.query_count   = 0
            st.session_state.locked        = False
            st.toast("✦ Fresh session started! Enjoy NEXUS.", icon="✅")
            st.rerun()

        st.markdown(
            '<div style="text-align:center;font-size:11px;color:var(--tx-3);'
            'font-family:var(--fb);margin-top:18px;line-height:1.7;">'
            'Your conversation history is saved in the sidebar.<br>'
            'New chat gives you another full session — completely free.'
            '</div>',
            unsafe_allow_html=True
        )

    st.stop()


def _save_current_session():
    """Save current chat to sessions history."""
    if len(st.session_state.chat_history) <= 1:
        return
    title = "New Chat"
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            title = msg["content"][:38] + ("\u2026" if len(msg["content"]) > 38 else "")
            break
    session = {
        "id":       datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "title":    title,
        "messages": list(st.session_state.chat_history),
        "time":     datetime.now().strftime("%b %d, %H:%M"),
    }
    st.session_state.sessions = [session] + [
        s for s in st.session_state.sessions if s["id"] != session.get("id")
    ][:19]


def render_sidebar():
    with st.sidebar:
        # Header
        st.markdown("""
        <div style="padding:14px 14px 6px; display:flex; align-items:center;
                    justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:9px;">
                <div class="nova-sb-mark">N</div>
                <span style="font-family:var(--fb);font-size:16px;font-weight:700;
                             color:var(--tx);letter-spacing:-.03em;">NEXUS</span>
            </div>
            <div class="nova-sb-pill"><div class="nova-sb-dot"></div>Online</div>
        </div>
        """, unsafe_allow_html=True)

        # New Chat
        if st.button("\u270f\ufe0f  New Chat", use_container_width=True, key="new_chat_btn"):
            _save_current_session()
            st.session_state.chat_history  = [INITIAL_GREETING]
            st.session_state.copy_states   = {}
            st.session_state.input_counter += 1
            st.session_state.query_count   = 0
            st.session_state.locked        = False
            st.rerun()

        # Chat History
        if st.session_state.sessions:
            st.markdown('<span class="nexus-section-label">Recents</span>', unsafe_allow_html=True)
            for sess in st.session_state.sessions[:15]:
                c1, c2 = st.columns([6, 1])
                with c1:
                    if st.button(
                        f"\U0001f4ac  {sess['title']}",
                        key=f"sess_{sess['id']}",
                        use_container_width=True,
                        help=sess["time"]
                    ):
                        _save_current_session()
                        st.session_state.chat_history  = list(sess["messages"])
                        st.session_state.input_counter += 1
                        st.rerun()
                with c2:
                    if st.button("\u2715", key=f"del_{sess['id']}"):
                        st.session_state.sessions = [s for s in st.session_state.sessions if s["id"] != sess["id"]]
                        st.rerun()

        st.markdown("<div style='height:1px;background:var(--border);margin:10px 8px;'></div>",
                    unsafe_allow_html=True)

        # Settings toggle
        show_settings = st.toggle("\u2699\ufe0f  Settings", value=st.session_state.show_settings, key="settings_toggle")
        st.session_state.show_settings = show_settings

        # Secrets key always loaded silently
        _secret_key = ""
        try:
            _secret_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            pass

        if show_settings:
            # api_key always comes from server secret — no user input
            api_key = _secret_key

            # Theme
            st.markdown('<div style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--tx-3);font-family:var(--fb);margin-bottom:6px;">\U0001f3a8 Theme</div>', unsafe_allow_html=True)
            theme_map = {"Nova Crystal": "\U0001f311 Nova Crystal", "Arctic Frost": "\u2744\ufe0f Arctic Frost", "Crimson Noir": "\U0001f534 Crimson Noir"}
            theme = st.radio("", options=list(THEME_VARS.keys()),
                format_func=lambda x: theme_map.get(x, x),
                index=list(THEME_VARS.keys()).index(st.session_state.theme),
                key="theme_radio", label_visibility="collapsed")
            if theme != st.session_state.theme:
                st.session_state.theme = theme
                st.rerun()

            st.divider()

            # Model + Persona + Temp
            model_tier = st.selectbox("\U0001f9e0 AI Mode",
                options=["Ultra", "Balanced", "Fast"],
                index=["Ultra", "Balanced", "Fast"].index(st.session_state.model_tier),
                key="model_tier_select")
            st.session_state.model_tier = model_tier

            persona = st.selectbox("\U0001f3ad Persona",
                options=list(PERSONAS.keys()),
                index=list(PERSONAS.keys()).index(st.session_state.persona),
                key="persona_select")
            st.session_state.persona = persona

            temperature = st.slider("\U0001f39a\ufe0f Response Style", 0.0, 1.0,
                value=st.session_state.temperature, step=0.05, key="temp_slider")
            st.session_state.temperature = temperature
            lbl = "Precise" if temperature < 0.3 else "Balanced" if temperature < 0.6 else "Creative"
            st.markdown(f'<div style="font-size:10px;color:var(--tx-3);font-family:var(--fb);margin-top:-6px;">{lbl}</div>',
                        unsafe_allow_html=True)

            st.divider()

            incognito = st.toggle("\U0001f575\ufe0f Incognito", value=st.session_state.incognito, key="incognito_toggle")
            st.session_state.incognito = incognito

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("\U0001f5d1\ufe0f  Clear All History", use_container_width=True, key="clear_all"):
                st.session_state.sessions = []
                st.rerun()
            if st.button("\u21a9  Home", use_container_width=True, key="back_landing"):
                st.session_state.app_mode = "landing"
                st.rerun()

        else:
            api_key     = _secret_key
            model_tier  = st.session_state.model_tier
            persona     = st.session_state.persona
            temperature = st.session_state.temperature
            incognito   = st.session_state.incognito

        # Footer
        st.markdown("""
        <div style="padding:12px 14px 6px;border-top:1px solid var(--border);margin-top:16px;
                    display:flex;align-items:center;gap:9px;">
            <div class="nexus-avatar">N</div>
            <div>
                <div style="font-family:var(--fb);font-size:12px;font-weight:600;color:var(--tx);">NEXUS User</div>
                <div style="font-size:10px;color:var(--tx-3);font-family:var(--fb);">v5.1 · Neural Engine</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    return api_key, temperature, model_tier


# ═══════════════════════════════════════════
def render_chat_history(history: list):
    for i, msg in enumerate(history):
        role    = msg["role"]
        content = msg["content"]

        if role == "assistant":
            st.markdown("""
            <div class="nova-msg-wrap">
                <div class="nova-msg-header-ai">
                    <div class="nova-msg-av ai">N</div>
                    <div class="nova-msg-who">NEXUS</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="nova-bub-ai">', unsafe_allow_html=True)
            st.markdown(content)
            st.markdown("</div>", unsafe_allow_html=True)

            # Copy handled by long-press JS context menu
        else:
            st.markdown("""
            <div class="nova-msg-wrap">
                <div class="nova-msg-header-user">
                    <div class="nova-msg-who">YOU</div>
                    <div class="nova-msg-av user">U</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f'<div class="nova-bub-user">{content}</div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  CHAT EXPORT
# ═══════════════════════════════════════════
def build_chat_export(history: list, fmt: str = "md") -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# NEXUS Chat Export\n_Exported: {ts}_\n\n---\n"]
    for msg in history:
        role    = "**NEXUS**" if msg["role"] == "assistant" else "**You**"
        content = msg["content"]
        if fmt == "txt":
            role = "NEXUS" if msg["role"] == "assistant" else "You"
            lines.append(f"{role}:\n{content}\n\n")
        else:
            lines.append(f"{role}:\n\n{content}\n\n---\n")
    return "".join(lines)


# ═══════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════
def render_dashboard(api_key, temperature, model_tier):

    st.markdown("""
    <div class="nova-header">
        <div class="nova-header-brand">
            <div class="nova-header-mark">N</div>
            <div class="nova-header-name">NEXUS</div>
            <div class="nova-header-tag">Intelligence Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nova-stats-row">
        <div class="nova-stat-card"><div class="nova-stat-value">99.2%</div><div class="nova-stat-label">Uptime SLA</div></div>
        <div class="nova-stat-card"><div class="nova-stat-value">&lt;1s</div><div class="nova-stat-label">Avg Response</div></div>
        <div class="nova-stat-card"><div class="nova-stat-value">128k</div><div class="nova-stat-label">Context Window</div></div>
        <div class="nova-stat-card"><div class="nova-stat-value">5</div><div class="nova-stat-label">AI Modules</div></div>
        <div class="nova-stat-card"><div class="nova-stat-value">Auto</div><div class="nova-stat-label">Fallback Engine</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nova-chip-row">
        <span class="nova-chip">◈ Real-Time Analysis</span>
        <span class="nova-chip">◎ Multi-Modal</span>
        <span class="nova-chip">▣ Auto Fallback</span>
        <span class="nova-chip">◈ Encrypted Keys</span>
        <span class="nova-chip">◉ Voice Commands</span>
        <span class="nova-chip">▤ PDF Intelligence</span>
        <span class="nova-chip">▶ Video Insights</span>
        <span class="nova-chip">🖼 Image Vision</span>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "  ◈  Document  ",
        "  ▶  YouTube  ",
        "  ◎  Neural Chat  ",
        "  🖼  Image Vision  ",
        "  ◉  Voice  ",
        "  🔄  Transform  ",
        "  ⓘ  About & Legal  ",
    ])

    # ═══ TAB 1: Document ═══
    with tab1:
        col_main, col_side = st.columns([3, 2], gap="large")
        with col_main:
            st.markdown("""
            <div class="nova-card">
                <div class="nova-card-header">
                    <div class="nova-card-icon">◈</div>
                    <div>
                        <div class="nova-card-title">Document Intelligence Engine</div>
                        <div class="nova-card-sub">PDF · DOCX · TXT · CSV — Multi-format analysis</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="nova-drop-zone">
                <div class="nova-drop-icon">▲</div>
                <div class="nova-drop-title">Drag &amp; Drop Your Document</div>
                <div class="nova-drop-sub">PDF · DOCX · TXT · CSV — max 200 MB</div>
            </div>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Or click to browse",
                type=["pdf", "txt", "docx", "csv"],
                label_visibility="collapsed"
            )

            analysis_type = st.selectbox(
                "Analysis Mode",
                [
                    "Full Semantic Analysis",
                    "Data Extraction",
                    "Executive Summary",
                    "Entity & Relation Mapping",
                    "Q&A Generation",
                    "🔥 Roast My Document",
                    "🧒 ELI5 — Explain Simply",
                    "✨ Vibe Check",
                    "⚔️ Debate This",
                ]
            )
            analyze_btn = st.button("◈  Analyze Document", use_container_width=True, key="doc_analyze", type="primary")

        with col_side:
            st.markdown("""
            <div class="nova-card-accent">
                <div class="nova-card-header">
                    <div class="nova-card-icon">▣</div>
                    <div>
                        <div class="nova-card-title">Analysis Options</div>
                        <div class="nova-card-sub">Configure extraction pipeline</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            opt_hyperlinks = st.checkbox("Extract Hyperlinks",         value=True)
            opt_tables     = st.checkbox("Parse Tables & Charts",       value=True)
            opt_images     = st.checkbox("Describe Embedded Images",    value=False)
            _              = st.checkbox("Cross-reference Web Sources", value=False)
            opt_pii        = st.checkbox("PII Detection & Redaction",   value=False)
            opt_quotes     = st.checkbox("Generate Key Quotes",         value=True)

            pipeline_status = "✓ Ready" if api_key else "⏳ Key Needed"
            pipeline_color  = "var(--accent)" if api_key else "var(--danger)"
            st.markdown(f"""
            <div class="nova-pipeline" style="margin-top:12px;">
                <div class="nova-pipeline-title">Pipeline Status</div>
                Loader ────── ✓ Ready<br>
                Chunker ───── ✓ Ready<br>
                Primary ───── <span style="color:{pipeline_color};">{pipeline_status}</span><br>
                Fallback ──── <span style="color:var(--accent);">✓ Auto</span>
            </div>
            """, unsafe_allow_html=True)

        if analyze_btn:
            if not uploaded_file:
                st.warning("Pehle document upload karo.")
            elif not check_rate_limit():
                st.error("⏱ Rate limit. Thodi der baad try karo.")
            else:
                safe, category = is_safe(analysis_type)
                if not safe:
                    show_block_error(category)
                else:
                    thinking_ph = st.empty()
                    with thinking_ph.container():
                        st.markdown("""
                        <div class="nova-thinking">
                            <div class="nova-dots"><span></span><span></span><span></span></div>
                            <div class="nova-thinking-text">NEXUS document padh raha hai...</div>
                        </div>
                        """, unsafe_allow_html=True)

                    result = analyze_document(
                        uploaded_file, api_key, temperature, model_tier,
                        analysis_type, opt_hyperlinks, opt_tables, opt_images, opt_pii, opt_quotes
                    )
                    thinking_ph.empty()
                    st.session_state.query_count += 1

                    if result.startswith("❌"):
                        st.error(result)
                        st.toast("Analysis fail hua.", icon="❌")
                    else:
                        st.toast("Analysis complete!", icon="✅")
                        st.markdown("""
                        <div class="nova-response-card">
                            <div class="nova-response-header">
                                <div class="nova-response-title">Analysis Report</div>
                                <div class="nova-response-label">Output</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(result)
                        dl1, dl2 = st.columns(2)
                        with dl1:
                            st.download_button("↓  Export as .md", data=result, file_name="nexus_report.md", mime="text/markdown", use_container_width=True)
                        with dl2:
                            st.download_button("↓  Export as .txt", data=result, file_name="nexus_report.txt", mime="text/plain", use_container_width=True)

    # ═══ TAB 2: YouTube ═══
    with tab2:
        st.markdown("""
        <div class="nova-card">
            <div class="nova-card-header">
                <div class="nova-card-icon">▶</div>
                <div>
                    <div class="nova-card-title">YouTube Intelligence Architect</div>
                    <div class="nova-card-sub">Extract · Summarize · Analyze video content</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        yt_col1, yt_col2 = st.columns([2, 1], gap="large")
        with yt_col1:
            yt_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
            yt_mode = st.selectbox("Extraction Mode", [
                "Full Transcript + Summary",
                "Key Moments & Timestamps",
                "Actionable Insights Only",
                "Speaker Diarization",
                "Sentiment Timeline",
                "📝 Quiz Generator",
                "📖 Chapter Detection",
            ])
            output_format = st.radio(
                "Output Format",
                ["Detailed Report", "Bullet Points", "Twitter/X Thread", "Email Brief"],
                horizontal=True
            )
            yt_analyze_btn = st.button("▶  Extract Intelligence", use_container_width=True, key="yt_go", type="primary")

        with yt_col2:
            preview_html = ""
            if yt_url.strip():
                vid_match = re.search(r"(?:v=|youtu\.be/|embed/)([^&\n?#]{11})", yt_url)
                if vid_match:
                    vid_id = vid_match.group(1)
                    preview_html = f"""
                    <iframe width="100%" height="130" src="https://www.youtube.com/embed/{vid_id}"
                        frameborder="0" allowfullscreen
                        style="border-radius:var(--r-sm);"></iframe>
                    """
            st.markdown(f"""
            <div class="nova-card" style="min-height:200px;">
                <div class="nova-card-header">
                    <div class="nova-card-icon">▣</div>
                    <div><div class="nova-card-title">Video Preview</div>
                    <div class="nova-card-sub">{"Live preview" if preview_html else "Paste URL to preview"}</div></div>
                </div>
                {preview_html if preview_html else
                 '<div style="background:var(--s2);border-radius:var(--r-sm);height:100px;'
                 'display:flex;align-items:center;justify-content:center;'
                 'border:1px dashed var(--border);color:var(--tx-3);'
                 'font-size:10px;font-family:var(--fb);letter-spacing:.1em;">NO PREVIEW YET</div>'}
            </div>
            """, unsafe_allow_html=True)

        if yt_analyze_btn:
            if not yt_url.strip():
                st.warning("YouTube URL paste karo.")
            elif not check_rate_limit():
                st.error("⏱ Rate limit. Thodi der baad try karo.")
            else:
                safe, category = is_safe(yt_url)
                if not safe:
                    show_block_error(category)
                else:
                    thinking_ph = st.empty()
                    with thinking_ph.container():
                        st.markdown("""
                        <div class="nova-thinking">
                            <div class="nova-dots"><span></span><span></span><span></span></div>
                            <div class="nova-thinking-text">Transcript fetch ho raha hai...</div>
                        </div>
                        """, unsafe_allow_html=True)

                    result = analyze_youtube(yt_url, api_key, temperature, model_tier, yt_mode, output_format)
                    thinking_ph.empty()
                    st.session_state.query_count += 1

                    if result.startswith("❌"):
                        st.error(result)
                        st.toast("Extraction fail hua.", icon="❌")
                    else:
                        st.toast("Video intelligence extracted!", icon="✅")
                        st.markdown("""
                        <div class="nova-response-card">
                            <div class="nova-response-header">
                                <div class="nova-response-title">YouTube Intelligence Report</div>
                                <div class="nova-response-label">Video Intel</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(result)
                        dl_c1, dl_c2 = st.columns(2)
                        with dl_c1:
                            st.download_button("↓  Export as .md", data=result, file_name="nexus_yt_report.md", mime="text/markdown", use_container_width=True)
                        with dl_c2:
                            st.download_button("↓  Export as .txt", data=result, file_name="nexus_yt_report.txt", mime="text/plain", use_container_width=True)

    # ═══ TAB 3: Neural Chat ═══
    with tab3:
        # Full-width chat — no side panel
        render_chat_history(st.session_state.chat_history)

        # Input row
        inp_c1, inp_c2 = st.columns([6, 1])
        with inp_c1:
            user_input = st.text_input(
                "Message",
                placeholder="Kuch bhi poochho — NEXUS sun raha hai...",
                label_visibility="collapsed",
                key=f"chat_input_{st.session_state.input_counter}"
            )
        with inp_c2:
            send_btn = st.button("▶", use_container_width=True, key="chat_send", type="primary")

        # Quick Templates — 2 per row (mobile friendly)
        suggestion_triggered = None
        for row_start in range(0, len(PROMPT_TEMPLATES), 2):
            row_items = PROMPT_TEMPLATES[row_start:row_start+2]
            cols = st.columns(len(row_items))
            for ci, (col, (label, prompt_text)) in enumerate(zip(cols, row_items)):
                with col:
                    if st.button(label, use_container_width=True, key=f"tmpl_{row_start+ci}"):
                        suggestion_triggered = prompt_text
        if suggestion_triggered:
            user_input = suggestion_triggered
            send_btn   = True

        # Bottom toolbar
        tb1, tb2, tb3 = st.columns([2, 1, 1])
        with tb1:
            msg_count = max(0, len(st.session_state.chat_history) - 1)
            st.markdown(
                f'<div style="font-size:11px;color:var(--tx-3);font-family:var(--fb);padding-top:8px;">'
                f'{msg_count} message{"s" if msg_count != 1 else ""}</div>',
                unsafe_allow_html=True)
        with tb2:
            st.download_button(
                "↓ Export",
                data=build_chat_export(st.session_state.chat_history, "md"),
                file_name=f"nexus_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True,
                key="export_md"
            )
        with tb3:
            if st.button("🗑️ Clear", use_container_width=True, key="clear_chat"):
                st.session_state.chat_history = [INITIAL_GREETING]
                st.session_state.copy_states  = {}
                st.session_state.input_counter += 1
                st.rerun()

        # ── Process send ──────────────────────────
        if send_btn and user_input.strip():
            if not check_rate_limit():
                st.error("⏱ Rate limit. Thodi der baad try karo.")
            else:
                safe, category = is_safe(user_input)
                if not safe:
                    show_block_error(category)
                else:
                    st.session_state.chat_history.append(
                        {"role": "user", "content": user_input}
                    )
                    thinking_ph = st.empty()
                    with thinking_ph.container():
                        st.markdown("""
                        <div class="nova-thinking">
                            <div class="nova-dots"><span></span><span></span><span></span></div>
                            <div class="nova-thinking-text">NEXUS soch raha hai...</div>
                        </div>
                        """, unsafe_allow_html=True)
                    reply = neural_chat_response(
                        st.session_state.chat_history,
                        api_key, temperature, model_tier,
                        st.session_state.persona
                    )
                    thinking_ph.empty()
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": reply}
                    )
                    st.session_state.query_count += 1
                    st.session_state.input_counter += 1
                    if not st.session_state.incognito:
                        _save_current_session()
                    st.rerun()

    # ═══ TAB 4: Image Vision ═══
    with tab4:

        # ── Header ──────────────────────────────────
        st.markdown("""
        <div style="display:flex;align-items:center;gap:12px;padding:4px 0 16px;">
            <div style="width:40px;height:40px;border-radius:10px;background:var(--s2);
                        border:1px solid var(--border);display:flex;align-items:center;
                        justify-content:center;font-size:18px;">🔍</div>
            <div>
                <div style="font-family:var(--fb);font-size:16px;font-weight:700;
                            color:var(--tx);letter-spacing:-.02em;">Image Vision</div>
                <div style="font-family:var(--fs);font-size:12px;color:var(--tx-3);
                            margin-top:1px;">Upload any image — NEXUS analyzes it with AI</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Upload Zone ─────────────────────────────
        st.markdown('<div class="img-upload-zone">' 
                    '<div class="img-upload-icon">🖼️</div>' 
                    '<div class="img-upload-title">Drop your image here</div>' 
                    '<div class="img-upload-sub">PNG · JPG · JPEG · WEBP · GIF</div>' 
                    '</div>', unsafe_allow_html=True)

        uploaded_img = st.file_uploader(
            "Upload Image",
            type=["png", "jpg", "jpeg", "webp", "gif"],
            label_visibility="collapsed",
            key="img_uploader"
        )

        # ── Image Preview ────────────────────────────
        if uploaded_img:
            img_size_kb = len(uploaded_img.getvalue()) / 1024
            img_size_str = f"{img_size_kb:.0f} KB" if img_size_kb < 1024 else f"{img_size_kb/1024:.1f} MB"
            st.markdown('<div class="img-preview-wrap">', unsafe_allow_html=True)
            st.image(uploaded_img, use_container_width=True)
            st.markdown(
                f'<div class="img-meta-row">' 
                f'<span class="img-meta-dot">◈</span>' 
                f'<span>{uploaded_img.name}</span>' 
                f'<span class="img-meta-dot">·</span>' 
                f'<span>{img_size_str}</span>' 
                f'<span class="img-meta-dot">·</span>' 
                f'<span>{uploaded_img.type.split("/")[-1].upper()}</span>' 
                f'</div></div>',
                unsafe_allow_html=True
            )

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        # ── Vision Mode Grid ─────────────────────────
        st.markdown(
            '<div style="font-family:var(--fb);font-size:10px;font-weight:700;' 
            'letter-spacing:.09em;text-transform:uppercase;color:var(--tx-3);margin-bottom:10px;">' 
            'Analysis Mode</div>',
            unsafe_allow_html=True
        )

        MODE_OPTIONS = [
            ("🔭", "General Analysis",       "Full detailed breakdown of the image"),
            ("🔤", "Text & OCR",             "Extract all visible text from image"),
            ("📦", "Object Detection",        "Detect & list all objects with positions"),
            ("🔥", "Roast This Image",        "Savage + funny critique of the image"),
            ("🧒", "ELI5 — Explain Simply",   "Explain like I'm 10 years old"),
            ("✨", "Vibe Check",              "Aesthetic score, mood & vibe analysis"),
        ]

        mode_labels = [m[1] for m in MODE_OPTIONS]
        # 2-column grid using columns
        mode_rows = [MODE_OPTIONS[i:i+2] for i in range(0, len(MODE_OPTIONS), 2)]
        selected_mode_idx = st.session_state.get("img_mode_idx", 0)

        new_idx = selected_mode_idx
        for row in mode_rows:
            cols = st.columns(len(row))
            for ci, (col, (icon, label, desc)) in enumerate(zip(cols, row)):
                global_idx = MODE_OPTIONS.index((icon, label, desc))
                with col:
                    is_sel = (global_idx == selected_mode_idx)
                    border_col = "var(--accent)" if is_sel else "var(--border)"
                    bg_col     = "var(--accent-glow)" if is_sel else "var(--s1)"
                    st.markdown(
                        f'<div style="background:{bg_col};border:1.5px solid {border_col};' 
                        f'border-radius:10px;padding:12px 14px;margin-bottom:2px;">' 
                        f'<div style="font-size:20px;margin-bottom:5px;">{icon}</div>' 
                        f'<div style="font-family:var(--fb);font-size:12px;font-weight:700;color:var(--tx);margin-bottom:2px;">{label}</div>' 
                        f'<div style="font-family:var(--fs);font-size:10px;color:var(--tx-3);">{desc}</div>' 
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    if st.button("Select" if not is_sel else "✓ Selected",
                                 key=f"img_mode_{global_idx}",
                                 use_container_width=True,
                                 type="primary" if is_sel else "secondary"):
                        st.session_state["img_mode_idx"] = global_idx
                        st.rerun()

        img_mode = mode_labels[st.session_state.get("img_mode_idx", 0)]

        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

        # ── Custom Question ──────────────────────────
        img_question = st.text_area(
            "💬 Custom Question (optional)",
            placeholder="e.g. What brand is shown? Is there any damage visible? What is the person doing?",
            height=80,
            key="img_question",
            label_visibility="visible"
        )

        # ── Analyze Button ───────────────────────────
        analyze_img_btn = st.button(
            "🔍  Analyze Image",
            use_container_width=True,
            key="img_analyze",
            type="primary",
            disabled=(uploaded_img is None)
        )

        if not uploaded_img:
            st.markdown(
                '<div style="text-align:center;font-family:var(--fb);font-size:10px;' 
                'color:var(--tx-3);margin-top:4px;letter-spacing:.05em;">' 
                '↑ Upload an image to enable analysis</div>',
                unsafe_allow_html=True
            )

        # ── Process ──────────────────────────────────
        if analyze_img_btn:
            if not uploaded_img:
                st.warning("Image upload karo pehle.")
            elif not check_rate_limit():
                st.error("⏱ Rate limit hit. Thodi der baad try karo.")
            else:
                img_mode_prompts = {
                    "General Analysis":     "",
                    "Text & OCR":           "Extract ALL text visible in this image exactly as it appears, preserving formatting and layout. Then provide a brief summary of what the text is about.",
                    "Object Detection":     "List ALL objects visible in this image in a Markdown table:\n| # | Object | Location in Frame | Description |\n|---|--------|------------------|-------------|\nBe exhaustive — include every visible item, person, or element.",
                    "Roast This Image":     "Brutally roast this image! What\'s wrong, weird, or cringe? Be clever and funny. Give 3 genuine improvements too. Use 🔥 emoji. End with one savage line.",
                    "ELI5 — Explain Simply":"Explain what\'s in this image like you\'re talking to a 10-year-old. Use simple words, fun comparisons, and make it engaging and easy to understand.",
                    "Vibe Check":           "Do a full VIBE CHECK on this image:\n1. **Overall vibe** (one word)\n2. **Emotional tone**\n3. **Hidden story or context**\n4. **Aesthetic score** /10\n5. **Best feature**\n6. **Vibe summary**: 1 emoji + 1 sentence",
                }

                base_q = img_mode_prompts.get(img_mode, "")
                if img_question.strip() and base_q:
                    final_question = f"{img_question.strip()}\n\nAlso: {base_q}"
                elif img_question.strip():
                    final_question = img_question.strip()
                else:
                    final_question = base_q or "Describe this image in detail."

                thinking_ph = st.empty()
                with thinking_ph.container():
                    st.markdown("""
                    <div class="nova-thinking">
                        <div class="nova-dots"><span></span><span></span><span></span></div>
                        <div class="nova-thinking-text">NEXUS image analyze kar raha hai...</div>
                    </div>
                    """, unsafe_allow_html=True)

                img_bytes = uploaded_img.getvalue()
                mime_type = uploaded_img.type or "image/jpeg"
                result = analyze_image(img_bytes, mime_type, final_question, api_key, temperature, model_tier)
                thinking_ph.empty()
                st.session_state.query_count += 1

                if result.startswith("❌"):
                    st.error(result)
                    st.toast("Analysis fail hua.", icon="❌")
                else:
                    st.toast("✅ Image analyzed!", icon="✅")
                    # Result card
                    st.markdown(
                        f'<div class="img-result-header">' 
                        f'<div class="img-result-title">📊 Vision Analysis Report</div>' 
                        f'<div class="img-result-badge">{img_mode}</div>' 
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown('<div class="img-result-body">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Export row
                    ex1, ex2 = st.columns(2)
                    with ex1:
                        st.download_button(
                            "↓ Export as .md",
                            data=result,
                            file_name=f"nexus_vision_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                            mime="text/markdown",
                            use_container_width=True,
                            key="img_export_md"
                        )
                    with ex2:
                        st.download_button(
                            "↓ Export as .txt",
                            data=result,
                            file_name=f"nexus_vision_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain",
                            use_container_width=True,
                            key="img_export_txt"
                        )

    # ═══ TAB 5: Voice ═══
    with tab5:
        v_col1, v_col2 = st.columns([1, 1], gap="large")
        with v_col1:
            st.markdown("""
            <div class="nova-card">
                <div class="nova-card-header">
                    <div class="nova-card-icon">◉</div>
                    <div>
                        <div class="nova-card-title">Voice Command Interface</div>
                        <div class="nova-card-sub">Speak naturally — NEXUS understands</div>
                    </div>
                </div>
                <div class="nova-voice-orb-wrap">
                    <div class="nova-voice-orb">◉</div>
                    <div class="nova-voice-status">Ready to listen</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            try:
                from streamlit_mic_recorder import mic_recorder

                audio_data = mic_recorder(
                    start_prompt="⏺  Start Recording",
                    stop_prompt="⏹  Stop Recording",
                    just_once=True,
                    use_container_width=True,
                    key="voice_recorder"
                )

                if audio_data and audio_data.get("bytes"):
                    st.success("✅ Voice capture ho gaya! Processing...")

                    # Initialize transcript before use — avoids NameError
                    transcript = None
                    raw_transcript = transcribe_voice(audio_data["bytes"], api_key)

                    if not raw_transcript.startswith("["):
                        transcript = raw_transcript
                        voice_messages = [
                            INITIAL_GREETING,
                            {"role": "user", "content": transcript}
                        ]
                        voice_ai_reply = neural_chat_response(
                            voice_messages, api_key, temperature, model_tier, st.session_state.persona
                        )
                        voice_result = f"**You said:** {transcript}\n\n---\n\n{voice_ai_reply}"
                    else:
                        voice_result = (
                            f"⚠️ Voice transcription fail hua: {raw_transcript}\n\n"
                            "**Tip:** Neural Chat tab mein type karke try karo."
                        )

                    st.markdown("""
                    <div class="nova-response-card">
                        <div class="nova-response-header">
                            <div class="nova-response-title">Voice Response</div>
                            <div class="nova-response-label">Processed</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(voice_result)

                    if not voice_result.startswith("⚠️"):
                        voice_label = f"[Voice] {transcript}" if transcript else "[Voice Input]"
                        st.session_state.chat_history.append({"role": "user", "content": voice_label})
                        st.session_state.chat_history.append({"role": "assistant", "content": voice_result})
                        st.session_state.query_count += 1
                        st.toast("Voice response Neural Chat mein save ho gaya!", icon="◉")

            except ImportError:
                st.info(
                    "📦 `streamlit-mic-recorder` install nahi hai.\n\n"
                    "Add `streamlit-mic-recorder` to your **requirements.txt** and redeploy."
                )

        with v_col2:
            st.markdown("""
            <div class="nova-card">
                <div class="nova-card-header">
                    <div class="nova-card-icon">▤</div>
                    <div>
                        <div class="nova-card-title">Voice Commands Guide</div>
                        <div class="nova-card-sub">Supported patterns</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            for label, example in [
                ("Document", '"Summarize this PDF"'),
                ("YouTube",  '"Extract key points from this video"'),
                ("Chat",     '"Tell me about machine learning"'),
                ("System",   '"Switch to Fast mode"'),
            ]:
                st.markdown(f"""
                <div style="background:var(--s1); border:1px solid var(--border);
                            border-left:2px solid var(--accent-ring); border-radius:var(--r-sm);
                            padding:9px 14px; margin-bottom:7px;
                            display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-size:11px; color:var(--accent); font-weight:600; font-family:var(--fb);">{label}</div>
                    <div style="font-size:11.5px; color:var(--tx-2); font-style:italic;">{example}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div class="nova-card" style="margin-top:12px;">
                <div class="nova-card-header">
                    <div class="nova-card-icon">◈</div>
                    <div>
                        <div class="nova-card-title">How Voice Works</div>
                        <div class="nova-card-sub">Neural audio processing</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            1. Click **Start Recording**
            2. Speak your query clearly
            3. Click **Stop Recording**
            4. NEXUS transcribes + responds
            5. Response saved to **Neural Chat** history
            """)

    # Footer
    st.markdown("""
    <div class="nova-footer">
        <div class="nova-footer-text">
            NEXUS INTELLIGENCE PLATFORM &nbsp;·&nbsp; BUILT WITH STREAMLIT &nbsp;·&nbsp;
            <span>NEURAL ENGINE</span> &nbsp;·&nbsp; © 2026
        </div>
        <div style="margin-top:6px; font-size:9px; color:var(--tx-3); font-family:var(--fb); letter-spacing:.08em;">
            ALL SYSTEMS OPERATIONAL &nbsp; ◈ &nbsp; v5.1.0
        </div>
    </div>
    """, unsafe_allow_html=True)




    # ═══ TAB 6: Transform ═══
    with tab6:

        # Header
        st.markdown("""
        <div style="display:flex;align-items:center;gap:12px;padding:4px 0 16px;">
            <div style="width:40px;height:40px;border-radius:10px;background:var(--s2);
                        border:1px solid var(--border);display:flex;align-items:center;
                        justify-content:center;font-size:18px;">🔄</div>
            <div>
                <div style="font-family:var(--fb);font-size:16px;font-weight:700;
                            color:var(--tx);letter-spacing:-.02em;">Transform</div>
                <div style="font-family:var(--fs);font-size:12px;color:var(--tx-3);margin-top:1px;">
                    Koi bhi text paste karo — ek click mein convert karo
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Input
        transform_input = st.text_area(
            "Input Text",
            placeholder="Yahan koi bhi text paste karo — article, paragraph, notes, anything...",
            height=160,
            key="transform_input",
            label_visibility="collapsed"
        )

        char_count = len(transform_input)
        st.markdown(
            f'<div style="font-family:var(--fb);font-size:10px;color:var(--tx-3);' 
            f'text-align:right;margin-top:-8px;margin-bottom:12px;">' 
            f'{char_count} characters</div>',
            unsafe_allow_html=True
        )

        # Transform modes — 2 per row
        TRANSFORM_MODES = [
            ("🐦", "Twitter / X Thread",   "3-5 punchy tweets mein convert karo",         "Convert this into a compelling Twitter/X thread. Make it punchy, engaging, and use emojis. Number each tweet. Max 280 chars each."),
            ("💼", "LinkedIn Post",         "Professional LinkedIn post banao",             "Convert this into a professional LinkedIn post. Add a strong hook, key insights, and a call-to-action. Use line breaks for readability. Add 3-5 relevant hashtags at the end."),
            ("📧", "Formal Email",          "Professional email mein convert karo",         "Convert this into a well-structured formal email. Include: Subject line, greeting, body paragraphs, and a professional sign-off."),
            ("📱", "WhatsApp Message",      "Casual aur short message banao",               "Convert this into a casual, friendly WhatsApp message. Keep it short, conversational, and natural. Use simple language."),
            ("📝", "Short Summary",         "3-4 lines mein summarize karo",                "Summarize this in exactly 3-4 concise sentences. Capture only the most essential points. Be direct."),
            ("🌍", "Hindi ↔ English",       "Language translate karo",                      "Detect the language of this text. If it is in English, translate it to fluent natural Hindi. If it is in Hindi, translate it to fluent natural English. Provide only the translation, no explanation."),
            ("📣", "Casual Explanation",    "Simple aur casual tarike se explain karo",     "Explain this in the most casual, friendly way possible — like explaining to a friend over chai. No jargon, no formality. Use Hinglish if it helps."),
            ("⚡", "Bullet Points",         "Key points bullets mein nikalo",               "Extract the key points from this text as clean bullet points. Each bullet should be concise (max 1 line). Start each with a relevant emoji."),
        ]

        st.markdown(
            '<div style="font-family:var(--fb);font-size:10px;font-weight:700;' 
            'letter-spacing:.09em;text-transform:uppercase;color:var(--tx-3);margin-bottom:10px;">' 
            'Choose Transform</div>',
            unsafe_allow_html=True
        )

        selected_transform = st.session_state.get("selected_transform", None)
        triggered_transform = None

        for row_start in range(0, len(TRANSFORM_MODES), 2):
            row = TRANSFORM_MODES[row_start:row_start+2]
            cols = st.columns(2)
            for ci, (col, (icon, label, desc, _prompt)) in enumerate(zip(cols, row)):
                gidx = row_start + ci
                is_sel = (selected_transform == gidx)
                with col:
                    border = "var(--accent)" if is_sel else "var(--border)"
                    bg     = "var(--accent-glow)" if is_sel else "var(--s1)"
                    st.markdown(
                        f'<div style="background:{bg};border:1.5px solid {border};' 
                        f'border-radius:10px;padding:11px 13px;margin-bottom:2px;">' 
                        f'<div style="font-size:18px;margin-bottom:4px;">{icon}</div>' 
                        f'<div style="font-family:var(--fb);font-size:12px;font-weight:700;color:var(--tx);margin-bottom:2px;">{label}</div>' 
                        f'<div style="font-family:var(--fs);font-size:10px;color:var(--tx-3);">{desc}</div>' 
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    btn_label = "✓ Selected" if is_sel else "Select"
                    btn_type  = "primary" if is_sel else "secondary"
                    if st.button(btn_label, key=f"tr_mode_{gidx}", use_container_width=True, type=btn_type):
                        st.session_state["selected_transform"] = gidx
                        st.rerun()

        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

        # Transform button
        can_transform = bool(transform_input.strip()) and selected_transform is not None
        transform_btn = st.button(
            "🔄  Transform Now",
            use_container_width=True,
            key="transform_go",
            type="primary",
            disabled=not can_transform
        )

        if not transform_input.strip():
            st.markdown('<div style="text-align:center;font-size:10px;color:var(--tx-3);font-family:var(--fb);">↑ Text paste karo upar</div>', unsafe_allow_html=True)
        elif selected_transform is None:
            st.markdown('<div style="text-align:center;font-size:10px;color:var(--tx-3);font-family:var(--fb);">↑ Transform mode select karo</div>', unsafe_allow_html=True)

        # Process
        if transform_btn and can_transform:
            if not check_rate_limit():
                st.error("⏱ Rate limit. Thodi der baad try karo.")
            else:
                _, _, _, prompt_instruction = TRANSFORM_MODES[selected_transform]
                icon_t, label_t, _, _ = TRANSFORM_MODES[selected_transform]

                full_prompt = f"{prompt_instruction}\n\n---\n\n{transform_input.strip()}"

                thinking_ph = st.empty()
                with thinking_ph.container():
                    st.markdown("""
                    <div class="nova-thinking">
                        <div class="nova-dots"><span></span><span></span><span></span></div>
                        <div class="nova-thinking-text">Transforming...</div>
                    </div>
                    """, unsafe_allow_html=True)

                try:
                    client = __import__('groq').Groq(api_key=api_key)
                    resp = client.chat.completions.create(
                        model=MODEL_MAP.get(model_tier, MODEL_MAP["Ultra"]),
                        messages=[
                            {"role": "system", "content": "You are a precise text transformation engine. Transform exactly as instructed. Output only the transformed result — no preamble, no explanation." + SAFETY_SYSTEM_ADDON},
                            {"role": "user",   "content": full_prompt}
                        ],
                        temperature=0.6,
                        max_tokens=1200,
                    )
                    raw_result = resp.choices[0].message.content.strip()
                    transform_result = _LLM_BLOCK_MSG if "NEXUS_SAFETY_REFUSE" in raw_result else raw_result
                except Exception as e:
                    transform_result = None
                    st.error(f"❌ Error: {str(e)[:80]}")

                thinking_ph.empty()

                if transform_result:
                    st.session_state.query_count += 1
                    st.toast(f"✅ Transformed to {label_t}!", icon="🔄")

                    # Result card
                    st.markdown(
                        f'<div class="img-result-header">' 
                        f'<div class="img-result-title">{icon_t} {label_t}</div>' 
                        f'<div class="img-result-badge">Transformed</div>' 
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown('<div class="img-result-body">', unsafe_allow_html=True)
                    st.markdown(transform_result)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Copy + Export row
                    cp1, cp2 = st.columns(2)
                    with cp1:
                        st.code(transform_result, language=None)
                    with cp2:
                        st.download_button(
                            "↓ Download",
                            data=transform_result,
                            file_name=f"nexus_transform_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain",
                            use_container_width=True,
                            key="transform_download"
                        )


    # ═══ TAB 7: About & Legal ═══
    with tab7:

        # ── Page Hero ──────────────────────────────────────────────────────
        st.markdown("""
        <div style="text-align:center;padding:40px 20px 32px;">
            <div style="width:64px;height:64px;border-radius:16px;
                        background:var(--accent-glow);border:1px solid var(--accent-ring);
                        display:inline-flex;align-items:center;justify-content:center;
                        font-family:var(--fb);font-size:26px;font-weight:800;
                        color:var(--accent);margin-bottom:20px;">N</div>
            <div style="font-family:var(--fb);font-size:10px;font-weight:700;
                        letter-spacing:.18em;text-transform:uppercase;
                        color:var(--tx-3);margin-bottom:12px;">Intelligence Platform · v5.1.0</div>
            <div style="font-family:var(--fb);font-size:32px;font-weight:800;
                        letter-spacing:-.04em;color:var(--tx);margin-bottom:10px;">
                NEXUS<span style="color:var(--accent);">.</span>
            </div>
            <div style="font-family:var(--fs);font-size:14px;color:var(--tx-2);
                        max-width:480px;margin:0 auto;line-height:1.8;">
                A multi-modal AI intelligence platform — built from scratch,
                designed for real use, and made to actually work.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:4px;background:linear-gradient(90deg,transparent,var(--accent-ring),transparent);margin-bottom:28px;'></div>", unsafe_allow_html=True)

        # ── SECTION 1: About the Platform ─────────────────────────────────
        with st.expander("◈  About NEXUS — The Full Story", expanded=True):
            st.markdown("""
<div style="font-family:var(--fs);font-size:13.5px;color:var(--tx);line-height:1.9;">

<div style="font-family:var(--fb);font-size:16px;font-weight:700;color:var(--accent);margin-bottom:14px;letter-spacing:-.02em;">
What is NEXUS?
</div>

NEXUS is a multi-modal AI intelligence platform built on top of Groq's ultra-fast inference engine. It's not just another chatbot wrapper — it's a full-stack productivity tool designed to handle real tasks: analyzing lengthy documents, breaking down YouTube videos you don't have time to watch, understanding images, processing voice commands, and transforming text into whatever format you need in seconds.

The idea was simple: most AI tools feel like toys. They're slow, they hallucinate constantly, and they don't actually fit into a real workflow. NEXUS was built to be different — fast, focused, and genuinely useful for someone who has actual work to do.

<br>

<div style="font-family:var(--fb);font-size:14px;font-weight:700;color:var(--tx);margin:18px 0 10px;letter-spacing:-.02em;">
What Can NEXUS Actually Do?
</div>

<b style="color:var(--accent);">◈ Document Intelligence</b> — Upload any PDF, DOCX, TXT, or CSV file and NEXUS will read the whole thing, find what matters, and present it in a format that saves you hours. From full semantic analysis to executive summaries, entity extraction to debate generation — it handles documents the way a sharp analyst would, not the way a search engine does.

<br><br>

<b style="color:var(--accent);">▶ YouTube Intelligence Architect</b> — Paste a YouTube URL and NEXUS fetches the transcript, processes it, and gives you key moments with timestamps, actionable insights, chapter breakdowns, quiz questions, and more. You get the value of a 40-minute video in under a minute.

<br><br>

<b style="color:var(--accent);">◎ Neural Chat</b> — The main conversation engine. Switch between five different personas — from a default sharp assistant to a coding expert, data analyst, teacher, or creative writer. The chat remembers context across the session and responds in the language you use. Hinglish, English, Hindi — it adapts.

<br><br>

<b style="color:var(--accent);">🖼 Image Vision</b> — Powered by a dedicated vision model, NEXUS can analyze any image you throw at it. Extract text, identify objects, check vibes, get roasted for your terrible design choices, or ask any custom question about what's in the frame.

<br><br>

<b style="color:var(--accent);">◉ Voice Command Interface</b> — Speak your query and NEXUS transcribes it using Whisper (a state-of-the-art speech recognition model) and then responds intelligently. Results automatically save to your Neural Chat history.

<br><br>

<b style="color:var(--accent);">🔄 Text Transform Engine</b> — Paste any text and convert it into Twitter threads, LinkedIn posts, formal emails, WhatsApp messages, summaries, bullet points, or translations with a single click. Eight transform modes, instant output.

<br>

<div style="font-family:var(--fb);font-size:14px;font-weight:700;color:var(--tx);margin:18px 0 10px;letter-spacing:-.02em;">
The Technical Stack
</div>

NEXUS runs on <b>Streamlit</b> for the UI, <b>Groq API</b> for inference, and a layered fallback engine that automatically switches models if one fails. The primary model is LLaMA 3.3 70B (Ultra tier) — one of the most capable open-weight models available. If that's unavailable, it falls through a chain to LLaMA 70B and then to LLaMA 8B Instant, so you almost never hit a dead end.

For image analysis, a dedicated vision model (LLaMA 3.2 Vision) handles multimodal inputs. Voice transcription runs on Whisper Large v3 — the same model that powers many production-grade transcription pipelines.

The themes are fully custom: Nova Crystal (dark gold), Arctic Frost (clean light), and Crimson Noir (dark red). The entire UI is hand-coded in CSS injected into Streamlit — no templates, no boilerplate.

</div>
""", unsafe_allow_html=True)

        # ── SECTION 3: How It Works (Technical Deep Dive) ─────────────────
        with st.expander("⚙️  How NEXUS Works — Technical Deep Dive"):
            st.markdown("""
<div style="font-family:var(--fs);font-size:13.5px;color:var(--tx);line-height:1.9;">

<div style="font-family:var(--fb);font-size:16px;font-weight:700;color:var(--accent);margin-bottom:14px;letter-spacing:-.02em;">
Architecture Overview
</div>

NEXUS is a single-file Streamlit application (~2,600 lines) organized into clearly separated layers: theme system, safety filter, backend functions, UI renderers, and a routing layer at the bottom. There's no database, no user authentication, no persistent server-side state — everything lives in Streamlit's session state for the duration of your browser session.

<br>

<div style="font-family:var(--fb);font-size:14px;font-weight:700;color:var(--tx);margin:18px 0 10px;letter-spacing:-.02em;">
The Inference Engine
</div>

All AI calls go through Groq's inference API. Groq uses custom hardware (LPUs — Language Processing Units) optimized specifically for transformer inference, which is why responses feel nearly instant compared to typical cloud GPU setups.

The fallback chain works like this:

<div style="background:var(--s2);border:1px solid var(--border);border-radius:var(--r-sm);padding:14px 18px;margin:12px 0;font-family:var(--fb);font-size:12px;line-height:2.2;">
Primary: LLaMA 3.3 70B Versatile (Ultra) <span style="color:var(--accent);">→</span> most capable<br>
Fallback 1: LLaMA 3 70B 8192 (Balanced) <span style="color:var(--accent);">→</span> stable, reliable<br>
Fallback 2: LLaMA 3.1 8B Instant (Fast) <span style="color:var(--accent);">→</span> lightweight, quick<br>
Fallback 3: Gemma 2 9B IT <span style="color:var(--accent);">→</span> last resort<br>
Vision: LLaMA 3.2 11B Vision Preview <span style="color:var(--accent);">→</span> image-only<br>
Voice: Whisper Large v3 <span style="color:var(--accent);">→</span> transcription-only
</div>

<br>

<div style="font-family:var(--fb);font-size:14px;font-weight:700;color:var(--tx);margin:18px 0 10px;letter-spacing:-.02em;">
The 3-Layer Content Safety System
</div>

NEXUS runs a three-layer content safety pipeline on every request:

<b style="color:var(--accent);">Layer 1 — Pre-filter (keyword blacklist):</b> Before any API call is made, the user's input goes through a normalization pipeline. This includes Unicode NFKD decomposition (to catch Cyrillic lookalike attacks), extended leet-speak normalization (0→o, @→a, €→e, and 18+ substitutions), and word-split removal (so "b.o.m.b" and "b o m b" both resolve to "bomb"). The normalized text is then matched against a six-category blacklist covering terrorism, weapons, cybercrime, child safety, hate speech, and self-harm. If there's a match, the request is blocked instantly — no API call is made.

<br><br>

<b style="color:var(--accent);">Layer 2 — LLM-level system prompt enforcement:</b> Every single API call — regardless of which feature triggered it — has a strict safety instruction block appended to the system prompt. The model is explicitly told that if it detects a request related to any banned category (regardless of phrasing, roleplay framing, academic framing, or any obfuscation attempt), it must respond with only a specific sentinel token and nothing else.

<br><br>

<b style="color:var(--accent);">Layer 3 — Post-response sentinel check:</b> After the model responds, NEXUS checks whether the response contains the sentinel token. If it does, the raw model output is discarded entirely and replaced with a clean English-language refusal message. The user never sees the sentinel or any partial harmful content.

<br>

<div style="font-family:var(--fb);font-size:14px;font-weight:700;color:var(--tx);margin:18px 0 10px;letter-spacing:-.02em;">
Session & Rate Limiting
</div>

Each browser session gets 15 free messages. The counter tracks across all features — chat, document analysis, YouTube, image, voice, and transforms all count toward the same session limit. When the limit is hit, a soft lock screen appears with the option to start a fresh session instantly (no login required).

Additionally, a rolling rate limiter allows a maximum of 20 requests per 60-second window per session. This prevents automated abuse and ensures fair use when the platform is under load.

<br>

<div style="font-family:var(--fb);font-size:14px;font-weight:700;color:var(--tx);margin:18px 0 10px;letter-spacing:-.02em;">
Document Processing Pipeline
</div>

Documents are processed entirely in-memory — nothing is written to disk. PDFs are parsed with pdfplumber (with PyPDF2 as fallback). DOCX files use python-docx. CSV and plain text files are decoded directly. Documents larger than 28,000 characters are truncated before being sent to the model, to stay within context limits. The truncation point is clearly marked in the output so you know if something was cut.

</div>
""", unsafe_allow_html=True)

        # ── SECTION 4: Privacy Policy ──────────────────────────────────────
        with st.expander("🔒  Privacy Policy"):
            st.markdown("""
<div style="font-family:var(--fs);font-size:13.5px;color:var(--tx);line-height:1.9;">

<div style="font-family:var(--fb);font-size:16px;font-weight:700;color:var(--accent);margin-bottom:14px;letter-spacing:-.02em;">
Privacy Policy — NEXUS Intelligence Platform
</div>

<div style="font-family:var(--fb);font-size:10px;color:var(--tx-3);letter-spacing:.08em;text-transform:uppercase;margin-bottom:18px;">
Last updated: 2026 · Effective immediately
</div>

This privacy policy explains how NEXUS handles your data. The short version: we collect as little as possible, we don't store anything on our end, and your conversations stay in your browser.

<br>

<b style="color:var(--accent);">What We Collect</b>

NEXUS does not collect, store, or transmit any personally identifiable information. There is no user registration, no login system, and no account creation. We do not store your name, email address, IP address, device identifiers, or any other personal data on our servers.

Your chat history, uploaded documents, and conversation context exist solely in your browser's session memory (Streamlit session state). When you close your browser tab or refresh the page, this data is gone permanently from our end. We cannot retrieve it, and we do not attempt to.

<br>

<b style="color:var(--accent);">API Calls and Third-Party Processing</b>

When you send a message, analyze a document, or upload an image, your input is transmitted to Groq's API for inference. This means your text or image data passes through Groq's servers for the purpose of generating a response. NEXUS does not control how Groq handles this data — you should review Groq's own privacy policy at groq.com if you have concerns about their data handling practices.

The Groq API key used by NEXUS is stored as a server-side secret and is never exposed to end users or included in any client-side code.

<br>

<b style="color:var(--accent);">YouTube Transcript Processing</b>

When you use the YouTube feature, NEXUS fetches publicly available transcripts from YouTube's servers using the youtube-transcript-api library. No login, cookies, or YouTube account credentials are used. Only publicly accessible transcript data is retrieved.

<br>

<b style="color:var(--accent);">Cookies and Tracking</b>

NEXUS does not use cookies. We do not use Google Analytics, Facebook Pixel, or any other third-party tracking or analytics service. We do not serve advertisements. There is no tracking of your behavior across sessions.

<br>

<b style="color:var(--accent);">Children's Privacy</b>

NEXUS is not intended for use by individuals under the age of 13. We do not knowingly collect any information from children. If you believe a child has submitted data through this platform, please contact us and we will take appropriate action.

<br>

<b style="color:var(--accent);">Changes to This Policy</b>

If this policy changes in a material way, we will update the "Last updated" date above. Continued use of the platform after changes constitutes acceptance of the revised policy.

</div>
""", unsafe_allow_html=True)

        # ── SECTION 5: Content Policy ──────────────────────────────────────
        with st.expander("⊘  Content Policy & Prohibited Uses"):
            st.markdown("""
<div style="font-family:var(--fs);font-size:13.5px;color:var(--tx);line-height:1.9;">

<div style="font-family:var(--fb);font-size:16px;font-weight:700;color:var(--accent);margin-bottom:14px;letter-spacing:-.02em;">
Content Policy
</div>

NEXUS runs a strict content safety filter. Certain categories of requests are blocked at multiple levels — before the API call, during the model's processing, and after the response is generated. This is not optional and cannot be bypassed.

<br>

<b style="color:var(--accent);">Absolutely Prohibited</b>

The following categories of content will always be blocked, regardless of framing, context, roleplay setup, fictional wrapping, academic justification, or any other framing technique:

<div style="background:rgba(217,85,85,0.06);border:1px solid rgba(217,85,85,0.2);border-left:2px solid #d95555;border-radius:var(--r-sm);padding:14px 18px;margin:12px 0;font-size:13px;line-height:2.1;">
⊘ &nbsp; Terrorism, extremist content, attack planning, or recruitment material<br>
⊘ &nbsp; Instructions for weapons, explosives, or weapons of mass destruction<br>
⊘ &nbsp; Malware creation, hacking attacks, phishing tools, or cybercrime assistance<br>
⊘ &nbsp; Any content involving the sexual exploitation of minors<br>
⊘ &nbsp; Hate speech, genocide planning, or incitement to ethnic or religious violence<br>
⊘ &nbsp; Detailed methods for suicide or self-harm
</div>

Attempting to bypass these filters using leet-speak (h@ck, b0mb), Unicode lookalike characters, word-splitting (b.o.m.b), or semantic obfuscation will not work. The safety system operates at the character normalization level, not just at surface pattern matching.

<br>

<b style="color:var(--accent);">What's Allowed</b>

NEXUS is designed for legitimate productivity, research, creative, and educational use. You can ask about cybersecurity concepts from a defensive or educational angle. You can discuss historical violence in an academic context. You can write fiction involving conflict. The filter is designed to catch requests for operational harmful assistance, not to prevent intelligent conversation about difficult topics.

<br>

<b style="color:var(--accent);">Consequences of Policy Violations</b>

Attempted violations are blocked silently at the application level. Repeated attempts within a session may consume rate limit tokens without generating responses. There are no account bans (since there are no accounts), but the filters do not fatigue or weaken with repeated attempts.

</div>
""", unsafe_allow_html=True)

        # ── SECTION 6: Terms & Conditions ─────────────────────────────────
        with st.expander("📋  Terms & Conditions — Full Text"):
            st.markdown("""
<div style="font-family:var(--fs);font-size:13.5px;color:var(--tx);line-height:1.9;">

<div style="font-family:var(--fb);font-size:16px;font-weight:700;color:var(--accent);margin-bottom:6px;letter-spacing:-.02em;">
Terms and Conditions of Use
</div>
<div style="font-family:var(--fb);font-size:10px;color:var(--tx-3);letter-spacing:.08em;text-transform:uppercase;margin-bottom:20px;">
NEXUS Intelligence Platform · v5.1.0 · Effective: 2026
</div>

Please read these Terms carefully before using NEXUS. By accessing or using this platform in any capacity, you agree to be bound by the terms stated here. If you do not agree with any part of these terms, you should stop using the platform immediately.

<br>

<b style="color:var(--accent);">1. Acceptance of Terms</b>

By using NEXUS, you confirm that you are at least 13 years of age (or the minimum age of digital consent in your jurisdiction, whichever is higher), that you have the legal capacity to enter into this agreement, and that you will use the platform in compliance with all applicable laws and regulations in your country or region.

<br>

<b style="color:var(--accent);">2. Description of Service</b>

NEXUS is a free-to-use, multi-modal AI intelligence platform providing the following core services: document analysis, YouTube transcript intelligence, neural chat, image vision analysis, voice transcription and response, and text transformation. These services are powered by third-party AI inference APIs and are subject to availability.

<br>

<b style="color:var(--accent);">3. Usage Limits and Fair Use</b>

<div style="background:var(--s2);border:1px solid var(--border);border-radius:var(--r-sm);padding:14px 18px;margin:10px 0;font-size:13px;line-height:2.3;">
<b style="color:var(--accent);">Free message limit:</b> &nbsp; 15 messages per browser session<br>
<b style="color:var(--accent);">Rate limit:</b> &nbsp; Maximum 20 requests per 60-second rolling window<br>
<b style="color:var(--accent);">Session reset:</b> &nbsp; Start a new session anytime — no cooldown required<br>
<b style="color:var(--accent);">Context window:</b> &nbsp; 128,000 tokens (shared across session)<br>
<b style="color:var(--accent);">Document size:</b> &nbsp; Up to 200MB upload, 28,000 characters processed<br>
<b style="color:var(--accent);">Image formats:</b> &nbsp; PNG, JPG, JPEG, WEBP, GIF<br>
<b style="color:var(--accent);">Document formats:</b> &nbsp; PDF, DOCX, TXT, CSV
</div>

These limits exist to ensure fair access for all users and to manage infrastructure costs. Attempting to circumvent limits through automation, scripting, or session manipulation is a violation of these terms.

<br>

<b style="color:var(--accent);">4. Prohibited Uses</b>

You agree not to use NEXUS for any of the following purposes:

(a) Generating, planning, or disseminating content related to terrorism, extremism, or political violence of any kind.

(b) Obtaining instructions for creating weapons, explosives, chemical agents, biological agents, radiological devices, or any other instrument designed to cause harm to persons or property.

(c) Creating, distributing, or assisting in the creation of malware, ransomware, trojans, spyware, keyloggers, phishing pages, credential harvesters, or any other malicious software or cyberweapon.

(d) Generating, soliciting, or distributing any content that sexually exploits or endangers minors in any form, whether realistic or fictional.

(e) Creating content designed to incite hatred, violence, or discrimination against any individual or group on the basis of race, ethnicity, religion, nationality, gender, sexual orientation, disability, or any other protected characteristic.

(f) Generating or distributing content that encourages, instructs, or facilitates suicide or self-harm.

(g) Impersonating any individual, organization, or entity in a manner that is deceptive or harmful.

(h) Using the platform for commercial scraping, bulk data harvesting, or any automated use without prior written permission.

(i) Attempting to reverse-engineer, decompile, or extract the underlying model, API keys, or safety filter logic of this platform.

(j) Using the platform in any way that violates applicable laws or regulations in your jurisdiction.

<br>

<b style="color:var(--accent);">5. Intellectual Property</b>

All original design elements, CSS styling, layout architecture, and code structure of NEXUS are the intellectual property of the developer. The underlying AI models are the property of their respective developers and are licensed separately. Content you upload or generate through NEXUS remains your own — we claim no ownership over your inputs or outputs.

<br>

<b style="color:var(--accent);">6. Disclaimer of Warranties</b>

NEXUS is provided on an "as is" and "as available" basis without any warranty of any kind, express or implied. We do not warrant that the platform will be uninterrupted, error-free, completely accurate, or free of harmful components. AI-generated responses may contain inaccuracies, hallucinations, or outdated information. You should not rely on NEXUS output for medical, legal, financial, or any other professional advice without independent verification.

<br>

<b style="color:var(--accent);">7. Limitation of Liability</b>

To the maximum extent permitted by applicable law, the developer of NEXUS shall not be liable for any indirect, incidental, special, consequential, or punitive damages arising from your use of or inability to use the platform. This includes, without limitation, damages for loss of data, loss of profits, or any harm resulting from reliance on AI-generated content.

<br>

<b style="color:var(--accent);">8. Third-Party Services</b>

NEXUS relies on the following third-party services: Groq (AI inference), YouTube Transcript API (transcript retrieval), and Streamlit (application framework). Your use of NEXUS implies transmission of data to these services as described in the Privacy Policy. The developer is not responsible for the practices, availability, or content policies of these third-party services.

<br>

<b style="color:var(--accent);">9. Availability and Modifications</b>

NEXUS is offered as a free service and may be modified, suspended, or discontinued at any time without notice. Features may be added, changed, or removed. Usage limits may be adjusted. The developer is not obligated to maintain any specific feature set or uptime guarantee.

<br>

<b style="color:var(--accent);">10. Governing Law</b>

These terms shall be governed by and construed in accordance with the laws of India. Any disputes arising from the use of this platform shall be subject to the exclusive jurisdiction of the courts of India.

<br>

<b style="color:var(--accent);">11. Changes to Terms</b>

These terms may be updated at any time. The most current version will always be visible on this page. Continued use of NEXUS after any modification constitutes your acceptance of the revised terms. If you do not agree to the updated terms, your only recourse is to discontinue use of the platform.

<br>

<b style="color:var(--accent);">12. Contact</b>

If you have questions about these terms, encounter a bug, want to report abuse, or just want to reach out about the platform, you can contact the developer directly. NEXUS is a solo-built project and feedback is taken seriously.

</div>
""", unsafe_allow_html=True)

        # ── Bottom legal strip ─────────────────────────────────────────────
        st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="border-top:1px solid var(--border);padding:24px 0 8px;text-align:center;">
            <div style="font-family:var(--fb);font-size:11px;font-weight:700;
                        letter-spacing:.1em;text-transform:uppercase;
                        color:var(--accent);margin-bottom:10px;">
                NEXUS Intelligence Platform
            </div>
            <div style="font-family:var(--fs);font-size:11px;color:var(--tx-3);line-height:2;">
                Powered by Nexus&nbsp;·&nbsp; v5.1.0 &nbsp;·&nbsp; © 2026<br>
                All rights reserved &nbsp;·&nbsp; Made in India
            </div>
            <div style="margin-top:16px;display:flex;justify-content:center;gap:20px;flex-wrap:wrap;">
                <span style="font-family:var(--fb);font-size:9.5px;color:var(--tx-3);letter-spacing:.08em;text-transform:uppercase;">Privacy Policy</span>
                <span style="color:var(--border);">·</span>
                <span style="font-family:var(--fb);font-size:9.5px;color:var(--tx-3);letter-spacing:.08em;text-transform:uppercase;">Terms & Conditions</span>
                <span style="color:var(--border);">·</span>
                <span style="font-family:var(--fb);font-size:9.5px;color:var(--tx-3);letter-spacing:.08em;text-transform:uppercase;">Content Policy</span>
                <span style="color:var(--border);">·</span>
                <span style="font-family:var(--fb);font-size:9.5px;color:var(--tx-3);letter-spacing:.08em;text-transform:uppercase;">Open Source Licenses</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  ROUTER
# ═══════════════════════════════════════════
if False:  # Landing page disabled — direct to app
    render_landing_page()
else:
    api_key, temperature, model_tier = render_sidebar()

    # Check if limit hit
    _limit_hit = st.session_state.query_count >= FREE_MSG_LIMIT
    if _limit_hit:
        st.session_state.locked = True

    if st.session_state.get("locked", False):
        render_limit_popup()
    else:
        # Show free messages counter in top right
        _remaining = max(0, FREE_MSG_LIMIT - st.session_state.query_count)
        _color = "#c8a778" if _remaining > 3 else "#d95555"
        st.markdown(
            f'<div style="position:fixed;top:14px;right:16px;z-index:9999;'
            f'background:var(--s2);border:1px solid var(--border);'
            f'border-radius:20px;padding:5px 12px;'
            f'font-family:var(--fb);font-size:11px;font-weight:700;color:{_color};">'
            f'{_remaining} free messages left</div>',
            unsafe_allow_html=True
        )
        render_dashboard(api_key, temperature, model_tier)
