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
import re, os, tempfile, time, json, base64, io
from datetime import datetime

st.set_page_config(
    page_title="NEXUS — Intelligence Platform",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&family=Sora:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
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
.nova-token-tag {{ font-size:9px; font-family:var(--fb); color:var(--tx-3); letter-spacing:.06em; }}
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
</style>
"""

# ═══════════════════════════════════════════════════════
#  PERSONAS
# ═══════════════════════════════════════════════════════
PERSONAS = {
    "NEXUS Default": (
        "You are NEXUS — a sharp, thoughtful AI assistant. "
        "You're not robotic or overly formal. Talk like a knowledgeable friend who knows a lot. "
        "Be direct, clear, sometimes a little witty, but always genuinely helpful. "
        "Give real answers, not fluffy ones. Use Markdown when it helps readability. "
        "Respond in the same language the user writes in. "
        "Never mention which AI model or company powers you."
    ),
    "Coding Expert": (
        "You are NEXUS in Coding Expert mode — a senior software engineer. "
        "Deep expertise in Python, JavaScript, web development, databases, and DevOps. "
        "Always provide clean, production-ready code with comments. "
        "Proactively point out bugs and edge cases. "
        "Use Markdown code blocks with language tags for all code. "
        "Never mention which AI model or company powers you."
    ),
    "Data Analyst": (
        "You are NEXUS in Data Analyst mode. "
        "Specialize in data analysis, statistics, business intelligence, and visualization. "
        "Provide structured, numbered insights. Use tables in Markdown where applicable. "
        "Always quantify findings and suggest data-driven next steps. "
        "Never mention which AI model or company powers you."
    ),
    "Teacher / ELI5": (
        "You are NEXUS in Teacher mode. "
        "Explain everything as simply as possible — like teaching a curious 12-year-old. "
        "Use analogies, real-world examples, and step-by-step breakdowns. "
        "Avoid jargon unless you immediately explain it. Make learning enjoyable. "
        "Never mention which AI model or company powers you."
    ),
    "Creative Writer": (
        "You are NEXUS in Creative Writer mode — a skilled storyteller and copywriter. "
        "Write with vivid language, compelling narrative, and strong voice. "
        "Adapt tone from dark/serious to light/playful as needed. "
        "Always produce polished, publication-ready creative content. "
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
        "terrorist","terrorism","jihad","jihadist","isis","isil","al-qaeda",
        "al qaeda","taliban","naxal","naxalite","maoists","boko haram",
        "ied","improvised explosive","suicide bomber","suicide vest",
        "bomb making","bomb recipe","how to make a bomb","detonate",
        "detonator","car bomb","letter bomb","pipe bomb",
    ],
    "weapons": [
        "gun mechanism","how to make a gun","3d print gun","3d printed gun",
        "ghost gun","untraceable firearm","silencer diy","suppressor diy",
        "chemical weapon","nerve agent","sarin","vx nerve","mustard gas",
        "poison gas","cyanide recipe","ricin recipe","how to make poison",
        "bioweapon","anthrax recipe","weaponize","hollow point ammunition",
    ],
    "cybercrime": [
        "hacking tool","hack into","how to hack","ddos attack","ddos script",
        "botnet","sql injection script","sql injection attack",
        "phishing page code","phishing kit","keylogger code","keylogger script",
        "bypass security","bypass authentication","bypass 2fa",
        "exploit vulnerability","zero day exploit","malware code",
        "ransomware code","rootkit","backdoor script","rat tool",
        "credential stuffing","brute force script","password cracker",
    ],
    "adult_content": [
        "porn","pornography","pornographic","nsfw","xxx",
        "child abuse","child sexual","csam","lolicon","shotacon",
        "sexual violence","rape scene","explicit sex","explicit sexual",
        "nude image","nude photo","onlyfans leak",
    ],
    "hate_speech": [
        "kill all muslims","kill all hindus","kill all jews","kill all christians",
        "hate muslims","hate hindus","hate christians","hate jews",
        "casteism","dalit slur","racial slur","n-word",
        "communal violence","ethnic cleansing","genocide plan",
        "religious riot","incite riot","lynch mob",
        "white supremacy","neo nazi","nazi propaganda",
    ],
    "self_harm": [
        "suicide","how to kill myself","how to end my life","want to die",
        "kill myself","self harm","self-harm","cut myself",
        "overdose on pills","how many pills to die","hanging myself",
        "methods of suicide","painless suicide","assisted suicide instructions",
    ],
}

_CATEGORY_LABELS: dict = {
    "terrorism":     "Terrorism / Extremism",
    "weapons":       "Weapons / WMD",
    "cybercrime":    "Cybercrime / Hacking",
    "adult_content": "Adult / Explicit Content",
    "hate_speech":   "Hate Speech / Violence",
    "self_harm":     "Self-Harm / Suicide",
}
_BLOCK_MSG = "Policy Violation: This request has been blocked for security reasons."


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _leet_normalize(text: str) -> str:
    subs = {"0":"o","1":"i","3":"e","4":"a","@":"a","$":"s","!":"i","+":"t","5":"s","7":"t","8":"b","9":"g"}
    for char, replacement in subs.items():
        text = text.replace(char, replacement)
    return text


def is_safe(prompt: str) -> tuple:
    cleaned = _normalize(_leet_normalize(prompt))
    for category, terms in _BLACKLIST.items():
        for term in terms:
            pattern = r"\b" + re.escape(term) + r"\b"
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
    """Try primary model, then fallback chain."""
    models_to_try = [primary_model] + [m for m in FALLBACK_MODELS if m != primary_model]
    last_error = ""
    for model in models_to_try:
        try:
            resp = _call_groq(api_key, messages, model, temperature)
            return resp.choices[0].message.content
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
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_b64}"}}
                ]
            }],
            temperature=temperature,
            max_tokens=1024,
        )
        return response.choices[0].message.content

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
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "hi", "en-IN"])
        except NoTranscriptFound:
            try:
                transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
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
        "input_counter":   0,
        "query_count":     0,
        "incognito":       False,
        "theme":           "Nova Crystal",
        "persona":         "NEXUS Default",
        "model_tier":      "Ultra",
        "rate_timestamps": [],
        "copy_states":     {},
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


_init_state()

theme_vars = THEME_VARS.get(st.session_state.theme, THEME_VARS["Nova Crystal"])
st.markdown(BASE_CSS.format(theme_vars=theme_vars), unsafe_allow_html=True)


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
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="nova-sidebar-brand">
            <div class="nova-sb-logo">
                <div class="nova-sb-mark">N</div>
                <div class="nova-sb-name">NEXUS</div>
            </div>
            <div class="nova-sb-pill">
                <div class="nova-sb-dot"></div>
                System Online
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Load key from secrets
        secret_key = ""
        try:
            secret_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            pass

        st.markdown('<div class="nova-sb-divider"><span>API Config</span></div>', unsafe_allow_html=True)
        api_key = st.text_input(
            "Neural Engine Key",
            value=secret_key,
            type="password",
            placeholder="gsk_••••••••••••••••",
            help="Set GROQ_API_KEY in Streamlit Secrets for automatic loading."
        )
        status_color = "#c8a778" if api_key else "#d95555"
        status_text  = "Key Active ✓" if api_key else "No Key — Enter Above"
        st.markdown(
            f'<div class="nova-api-status" style="color:{status_color};">◈ {status_text}</div>',
            unsafe_allow_html=True
        )

        if api_key:
            if st.button("✓  Validate Key", use_container_width=True, key="validate_key"):
                with st.spinner("Checking..."):
                    is_valid, msg = validate_api_key(api_key)
                if is_valid:
                    st.toast(f"✅ {msg}", icon="✅")
                else:
                    st.toast(f"❌ {msg}", icon="❌")

        # Intelligence Tier
        st.markdown('<div class="nova-sb-divider"><span>Intelligence Tier</span></div>', unsafe_allow_html=True)
        model_tier = st.selectbox(
            "Engine Mode",
            options=["Ultra", "Balanced", "Fast"],
            index=["Ultra", "Balanced", "Fast"].index(st.session_state.model_tier),
            key="model_tier_select"
        )
        st.session_state.model_tier = model_tier
        tier_meta = {
            "Ultra":    ("Max intelligence · Best results",  "#c8a778"),
            "Balanced": ("Great balance of speed & quality", "#a8c878"),
            "Fast":     ("Lightning fast · Quick answers",   "#7c9ec8"),
        }
        meta_text, meta_color = tier_meta.get(model_tier, ("", "#888"))
        st.markdown(f'<div class="nova-model-meta" style="color:{meta_color};">◈ {meta_text}</div>', unsafe_allow_html=True)

        # Persona
        st.markdown('<div class="nova-sb-divider"><span>AI Persona</span></div>', unsafe_allow_html=True)
        persona = st.selectbox(
            "Active Persona",
            options=list(PERSONAS.keys()),
            index=list(PERSONAS.keys()).index(st.session_state.persona),
            key="persona_select"
        )
        st.session_state.persona = persona
        persona_desc = {
            "NEXUS Default":   "◈ Balanced general assistant",
            "Coding Expert":   "◈ Senior software engineer",
            "Data Analyst":    "◈ Data & insights specialist",
            "Teacher / ELI5":  "◈ Simple explanations mode",
            "Creative Writer": "◈ Storytelling & copywriting",
        }
        st.markdown(
            f'<div class="nova-creativity-tag">{persona_desc.get(persona, "")}</div>',
            unsafe_allow_html=True
        )

        # Temperature
        st.markdown('<div class="nova-sb-divider"><span>Parameters</span></div>', unsafe_allow_html=True)
        temperature = st.slider("Response Style", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
        creativity_label = (
            "Precise & Factual" if temperature < 0.3
            else "Balanced" if temperature < 0.6
            else "Creative & Expressive"
        )
        st.markdown(f'<div class="nova-creativity-tag">◈ {creativity_label}</div>', unsafe_allow_html=True)

        # Theme
        st.markdown('<div class="nova-sb-divider"><span>Theme</span></div>', unsafe_allow_html=True)
        theme = st.radio(
            "Visual Theme",
            options=list(THEME_VARS.keys()),
            index=list(THEME_VARS.keys()).index(st.session_state.theme),
            key="theme_radio",
            horizontal=False,
        )
        if theme != st.session_state.theme:
            st.session_state.theme = theme
            st.rerun()

        # Stats
        st.markdown('<div class="nova-sb-divider"><span>Quick Stats</span></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.metric("Queries", str(st.session_state.query_count))
        with c2: st.metric("Turns",   str(len(st.session_state.chat_history)))

        # Session
        st.markdown('<div class="nova-sb-divider"><span>Session</span></div>', unsafe_allow_html=True)
        if st.button("↩  Return to Landing", use_container_width=True, key="back_landing"):
            st.session_state.app_mode = "landing"
            st.rerun()
        if st.button("⟳  Clear Session", use_container_width=True, key="clear_session"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        # Privacy
        st.markdown('<div class="nova-sb-divider"><span>Privacy</span></div>', unsafe_allow_html=True)
        incognito = st.toggle("Incognito Mode", value=st.session_state.incognito, key="incognito_toggle")
        st.session_state.incognito = incognito
        if incognito:
            st.markdown(
                '<div style="font-size:10px;color:var(--accent);font-family:var(--fb);letter-spacing:.06em;">'
                '◈ History cleared on each message</div>',
                unsafe_allow_html=True
            )

        st.markdown("""
        <div style="margin-top:20px; padding-top:12px; border-top:1px solid var(--border);
                    font-size:10px; color:var(--tx-3); font-family:var(--fb);
                    text-align:center; letter-spacing:.08em;">
            NEXUS © 2026 &nbsp;·&nbsp; <span style="color:var(--accent);">Neural Intelligence</span>
        </div>
        """, unsafe_allow_html=True)

    return api_key, temperature, model_tier


# ═══════════════════════════════════════════
#  CHAT BUBBLE RENDERER
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

            token_count = approx_tokens(content)
            copy_col, token_col = st.columns([1, 4])
            with copy_col:
                if st.button("📋 Copy", key=f"copy_btn_{i}", help="Copy this response"):
                    st.session_state.copy_states[str(i)] = not st.session_state.copy_states.get(str(i), False)
            with token_col:
                st.markdown(f'<div class="nova-token-tag">~{token_count} tokens</div>', unsafe_allow_html=True)
            if st.session_state.copy_states.get(str(i), False):
                st.code(content, language=None)
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

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "  ◈  Document  ",
        "  ▶  YouTube  ",
        "  ◎  Neural Chat  ",
        "  🖼  Image Vision  ",
        "  ◉  Voice  ",
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
            elif not api_key:
                st.error("❌ API Key nahi hai. Sidebar mein daalo.")
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
            elif not api_key:
                st.error("❌ API Key nahi hai.")
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
        chat_col, info_col = st.columns([3, 1], gap="large")

        with chat_col:
            st.markdown("""
            <div class="nova-card">
                <div class="nova-card-header">
                    <div class="nova-card-icon">◎</div>
                    <div>
                        <div class="nova-card-title">Neural Chat</div>
                        <div class="nova-card-sub">Multi-turn · Context-Aware · Streaming · Markdown Rendered</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.container():
                st.markdown(
                    '<div style="background:var(--s1);border:1px solid var(--border);'
                    'border-radius:var(--r);padding:18px 18px 10px;'
                    'min-height:320px;max-height:520px;overflow-y:auto;margin-bottom:12px;">',
                    unsafe_allow_html=True
                )
                render_chat_history(st.session_state.chat_history)
                st.markdown("</div>", unsafe_allow_html=True)

            inp_c1, inp_c2 = st.columns([5, 1])
            with inp_c1:
                user_input = st.text_input(
                    "Message",
                    placeholder="Kuch bhi poochho — NEXUS sun raha hai...",
                    label_visibility="collapsed",
                    key=f"chat_input_{st.session_state.input_counter}"
                )
            with inp_c2:
                send_btn = st.button("Send ▶", use_container_width=True, key="chat_send", type="primary")

            st.markdown(
                '<div style="font-size:9.5px;font-family:var(--fb);letter-spacing:.08em;'
                'text-transform:uppercase;color:var(--tx-3);margin-bottom:6px;margin-top:4px;">'
                'Quick Templates</div>',
                unsafe_allow_html=True
            )
            tmpl_cols = st.columns(len(PROMPT_TEMPLATES))
            suggestion_triggered = None
            for idx, (label, prompt_text) in enumerate(PROMPT_TEMPLATES):
                with tmpl_cols[idx]:
                    if st.button(label, use_container_width=True, key=f"tmpl_{idx}"):
                        suggestion_triggered = prompt_text

            if suggestion_triggered:
                user_input = suggestion_triggered
                send_btn   = True

        with info_col:
            turns        = len(st.session_state.chat_history)
            total_tokens = sum(approx_tokens(m["content"]) for m in st.session_state.chat_history)
            st.markdown(f"""
            <div class="nova-card-accent">
                <div class="nova-card-header">
                    <div class="nova-card-icon">▣</div>
                    <div><div class="nova-card-title">Chat Status</div></div>
                </div>
                <div class="nova-pipeline">
                    Engine ──── <span style="color:{'var(--accent)' if api_key else 'var(--danger)'};">
                        {'● Active' if api_key else '● No Key'}</span><br>
                    Tier ───────  <span style="color:var(--tx);">{model_tier}</span><br>
                    Persona ──  <span style="color:var(--tx);">{st.session_state.persona.split()[0]}</span><br>
                    Turns ──────  <span style="color:var(--tx);">{turns}</span><br>
                    ~Tokens ──  <span style="color:var(--tx);">{total_tokens}</span><br>
                    Temp ────── <span style="color:var(--tx);">{temperature}</span><br>
                    Incognito ─  <span style="color:{'var(--accent)' if st.session_state.incognito else 'var(--tx-3)'};">
                        {'ON' if st.session_state.incognito else 'OFF'}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⟳ Clear Chat", use_container_width=True, key="clear_chat"):
                st.session_state.chat_history = [INITIAL_GREETING]
                st.session_state.copy_states  = {}
                st.session_state.input_counter += 1
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                '<div style="font-size:9.5px;font-family:var(--fb);letter-spacing:.08em;'
                'text-transform:uppercase;color:var(--tx-3);margin-bottom:6px;">Export Chat</div>',
                unsafe_allow_html=True
            )
            exp_c1, exp_c2 = st.columns(2)
            with exp_c1:
                st.download_button(
                    "↓ .md",
                    data=build_chat_export(st.session_state.chat_history, "md"),
                    file_name=f"nexus_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key="export_md"
                )
            with exp_c2:
                st.download_button(
                    "↓ .txt",
                    data=build_chat_export(st.session_state.chat_history, "txt"),
                    file_name=f"nexus_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="export_txt"
                )

        # Process message with streaming
        if send_btn and user_input and user_input.strip():
            if not api_key:
                st.error("❌ API Key nahi hai. Sidebar mein daalo.")
            elif not check_rate_limit():
                st.error("⏱ Rate limit. Thodi der baad try karo.")
            else:
                safe, category = is_safe(user_input)
                if not safe:
                    show_block_error(category)
                else:
                    st.session_state.chat_history.append({"role": "user", "content": user_input})

                    messages_to_send = (
                        [INITIAL_GREETING, {"role": "user", "content": user_input}]
                        if st.session_state.incognito
                        else st.session_state.chat_history
                    )

                    full_response = ""
                    try:
                        system_prompt = PERSONAS.get(st.session_state.persona, PERSONAS["NEXUS Default"])
                        primary_model = MODEL_MAP.get(model_tier, MODEL_MAP["Ultra"])

                        groq_messages = [{"role": "system", "content": system_prompt}]
                        for msg in messages_to_send:
                            role = "assistant" if msg["role"] == "assistant" else "user"
                            groq_messages.append({"role": role, "content": msg["content"]})

                        st.markdown("""
                        <div class="nova-msg-wrap">
                            <div class="nova-msg-header-ai">
                                <div class="nova-msg-av ai">N</div>
                                <div class="nova-msg-who">NEXUS</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        stream_ph = st.empty()
                        stream = _call_groq(api_key, groq_messages, primary_model, temperature, stream=True)

                        for chunk in stream:
                            delta = chunk.choices[0].delta.content
                            if delta:
                                full_response += delta
                                stream_ph.markdown(
                                    f'<div class="nova-bub-ai">{full_response} ▊</div>',
                                    unsafe_allow_html=True
                                )
                        stream_ph.markdown(
                            f'<div class="nova-bub-ai">{full_response}</div>',
                            unsafe_allow_html=True
                        )

                    except Exception as e:
                        err = str(e)
                        if "invalid_api_key" in err.lower() or "authentication" in err.lower():
                            full_response = "❌ API Key galat hai. Sahi key daalo."
                            st.toast("Invalid API Key!", icon="❌")
                        elif "rate_limit" in err.lower():
                            full_response = neural_chat_response(
                                messages_to_send, api_key, temperature, model_tier, st.session_state.persona
                            )
                        else:
                            full_response = f"❌ Kuch error aaya: {err[:80]}"
                            st.toast("Kuch gadbad hui.", icon="❌")
                        if full_response.startswith("❌"):
                            st.error(full_response)

                    if full_response:
                        st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                        st.session_state.query_count += 1

                    if st.session_state.incognito:
                        st.session_state.chat_history = [
                            INITIAL_GREETING,
                            {"role": "user",      "content": user_input},
                            {"role": "assistant", "content": full_response},
                        ]

                    st.session_state.input_counter += 1
                    st.rerun()

    # ═══ TAB 4: Image Vision ═══
    with tab4:
        img_col1, img_col2 = st.columns([3, 2], gap="large")

        with img_col1:
            st.markdown("""
            <div class="nova-card">
                <div class="nova-card-header">
                    <div class="nova-card-icon">🖼</div>
                    <div>
                        <div class="nova-card-title">Image Vision Engine</div>
                        <div class="nova-card-sub">Upload any image — NEXUS analyzes it</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="nova-drop-zone">
                <div class="nova-drop-icon">🖼</div>
                <div class="nova-drop-title">Upload Your Image</div>
                <div class="nova-drop-sub">PNG · JPG · JPEG · WEBP · GIF</div>
            </div>
            """, unsafe_allow_html=True)

            uploaded_img = st.file_uploader(
                "Or click to browse",
                type=["png", "jpg", "jpeg", "webp", "gif"],
                label_visibility="collapsed",
                key="img_uploader"
            )

            img_question = st.text_area(
                "Ask about the image (optional)",
                placeholder="What is in this image? Describe the colors, objects, text...",
                height=90,
                key="img_question"
            )

            img_mode = st.selectbox(
                "Vision Mode",
                [
                    "General Analysis",
                    "Text & OCR Extraction",
                    "Object Detection",
                    "🔥 Roast This Image",
                    "🧒 ELI5 — Explain Simply",
                    "✨ Vibe Check",
                ],
                key="img_mode"
            )

            analyze_img_btn = st.button("🖼  Analyze Image", use_container_width=True, key="img_analyze", type="primary")

        with img_col2:
            st.markdown("""
            <div class="nova-card-accent">
                <div class="nova-card-header">
                    <div class="nova-card-icon">▣</div>
                    <div>
                        <div class="nova-card-title">Image Preview</div>
                        <div class="nova-card-sub">Live preview of uploaded image</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if uploaded_img:
                st.image(uploaded_img, use_container_width=True)
                img_size_kb = len(uploaded_img.getvalue()) / 1024
                st.markdown(
                    f'<div style="font-size:10px;color:var(--tx-3);font-family:var(--fb);margin-top:6px;">'
                    f'◈ {uploaded_img.name} · {img_size_kb:.1f} KB · {uploaded_img.type}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown("""
                <div style="background:var(--s2);border-radius:var(--r-sm);height:160px;
                display:flex;align-items:center;justify-content:center;
                border:1px dashed var(--border);color:var(--tx-3);
                font-size:10px;font-family:var(--fb);letter-spacing:.1em;">
                    NO IMAGE YET
                </div>
                """, unsafe_allow_html=True)

        if analyze_img_btn:
            if not uploaded_img:
                st.warning("Pehle image upload karo.")
            elif not api_key:
                st.error("❌ API Key nahi hai.")
            elif not check_rate_limit():
                st.error("⏱ Rate limit. Thodi der baad try karo.")
            else:
                img_mode_prompts = {
                    "General Analysis": "",
                    "Text & OCR Extraction": "Extract ALL text visible in this image. Present it exactly as it appears, preserving formatting. Then provide a brief summary of what the text is about.",
                    "Object Detection": "List ALL objects visible in this image in a Markdown table:\n| Object | Location | Confidence | Description |\n|--------|----------|------------|-----------|\nBe thorough — include every visible item.",
                    "🔥 Roast This Image": "Brutally roast this image! What's wrong, weird, or cringe about it? Be funny and savage. Then give 3 genuine improvements. Use 🔥 emoji. End with a savage one-liner.",
                    "🧒 ELI5 — Explain Simply": "Explain what's in this image like you're talking to a 10-year-old. Use simple words, fun comparisons, and make it engaging.",
                    "✨ Vibe Check": "Do a VIBE CHECK on this image:\n1. Overall vibe (1 word)\n2. Emotional tone\n3. Hidden story or context\n4. Aesthetic score /10\n5. Vibe summary: 1 emoji + 1 sentence",
                }

                base_q = img_mode_prompts.get(img_mode, "")
                if img_question.strip():
                    final_question = f"{img_question}\n\nAdditionally: {base_q}" if base_q else img_question
                else:
                    final_question = base_q or ""

                thinking_ph = st.empty()
                with thinking_ph.container():
                    st.markdown("""
                    <div class="nova-thinking">
                        <div class="nova-dots"><span></span><span></span><span></span></div>
                        <div class="nova-thinking-text">NEXUS image dekh raha hai...</div>
                    </div>
                    """, unsafe_allow_html=True)

                img_bytes = uploaded_img.getvalue()
                mime_type = uploaded_img.type or "image/jpeg"
                result = analyze_image(img_bytes, mime_type, final_question, api_key, temperature, model_tier)
                thinking_ph.empty()
                st.session_state.query_count += 1

                if result.startswith("❌"):
                    st.error(result)
                    st.toast("Image analysis fail hua.", icon="❌")
                else:
                    st.toast("Image analyzed!", icon="✅")
                    st.markdown("""
                    <div class="nova-response-card">
                        <div class="nova-response-header">
                            <div class="nova-response-title">Vision Analysis Report</div>
                            <div class="nova-response-label">Image Intel</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(result)
                    st.download_button(
                        "↓  Export Report",
                        data=result,
                        file_name="nexus_image_report.md",
                        mime="text/markdown",
                        use_container_width=True,
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

                    if api_key:
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
                    else:
                        voice_result = "⚠️ API Key nahi hai. Sidebar mein key daalo."

                    st.markdown("""
                    <div class="nova-response-card">
                        <div class="nova-response-header">
                            <div class="nova-response-title">Voice Response</div>
                            <div class="nova-response-label">Processed</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(voice_result)

                    if api_key and not voice_result.startswith("⚠️"):
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


# ═══════════════════════════════════════════
#  ROUTER
# ═══════════════════════════════════════════
if st.session_state.app_mode == "landing":
    render_landing_page()
else:
    api_key, temperature, model_tier = render_sidebar()
    render_dashboard(api_key, temperature, model_tier)
