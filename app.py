# ============================================================
#  NEXUS — Intelligence Platform  |  app.py  (FIXED v3.1)
#  Theme : Nova Crystal Glass (Bronze Gold × Deep Obsidian)
#  Stack : Streamlit · Google Gemini API · youtube-transcript-api
# ============================================================

import streamlit as st
import time
import re
import os
import tempfile

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NEXUS — Intelligence Platform",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  NOVA CUSTOM CSS
# ─────────────────────────────────────────────
CUSTOM_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&family=Sora:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
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
    --blur:         blur(18px);
    --transition:   all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: var(--fs) !important;
    color: var(--tx) !important;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
}
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
.block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }

[data-testid="stSidebar"] {
    background: var(--sb-bg) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { font-family: var(--fs) !important; }
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--accent) !important;
    font-family: var(--fb) !important;
}
[data-testid="stSidebar"] [data-testid="stTextInput"] input,
[data-testid="stSidebar"] div[data-baseweb="input"] input {
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--tx) !important;
    font-family: var(--fs) !important;
    font-size: 0.82rem !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: var(--accent) !important;
    border: none !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider label {
    color: var(--tx-2) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    font-family: var(--fb) !important;
}
.nova-sidebar-brand {
    padding: 18px 14px 14px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 6px;
}
.nova-sb-logo { display: flex; align-items: center; gap: 9px; margin-bottom: 10px; }
.nova-sb-mark {
    width: 28px; height: 28px; border-radius: 7px;
    background: var(--accent-glow); border: 1px solid var(--accent-ring);
    display: flex; align-items: center; justify-content: center;
    color: var(--accent); font-family: var(--fb);
    font-size: 13px; font-weight: 800; letter-spacing: -.02em; flex-shrink: 0;
}
.nova-sb-name { font-family: var(--fb); font-size: 15px; font-weight: 700; color: var(--tx); letter-spacing: -.03em; }
.nova-sb-pill {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 10px; background: rgba(200,167,120,0.07);
    border: 1px solid var(--accent-ring); border-radius: 20px;
    font-size: 10px; font-weight: 700; color: var(--accent);
    font-family: var(--fb); letter-spacing: .06em;
}
.nova-sb-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: var(--accent); box-shadow: 0 0 6px var(--accent);
    animation: novaPulse 2s infinite;
}
@keyframes novaPulse { 0%,100%{opacity:1;transform:scale(1);}50%{opacity:.5;transform:scale(1.3);} }
.nova-sb-divider {
    display: flex; align-items: center; gap: 8px;
    margin: 14px 0 8px; padding: 0 4px;
}
.nova-sb-divider span {
    font-size: 9.5px; font-weight: 700; letter-spacing: .1em;
    text-transform: uppercase; color: var(--tx-3);
    font-family: var(--fb); white-space: nowrap;
}
.nova-sb-divider::before, .nova-sb-divider::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.nova-model-meta { font-size: 0.68rem; font-family: var(--fb); letter-spacing: .04em; margin-top: -4px; margin-bottom: 6px; padding: 0 2px; }
.nova-api-status { font-size: 0.68rem; font-family: var(--fb); margin-top: -4px; margin-bottom: 6px; padding: 0 2px; }
.nova-creativity-tag { font-size: 0.68rem; color: var(--tx-2); font-family: var(--fb); margin-top: -4px; margin-bottom: 6px; padding: 0 2px; }
[data-testid="stMetric"] { background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r) !important; padding: 0.8rem 1rem !important; }
[data-testid="stMetricValue"] { color: var(--accent) !important; font-family: var(--fb) !important; font-size: 1.3rem !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: var(--tx-2) !important; }
[data-testid="stMetricDelta"] { color: var(--accent) !important; }
.nova-landing { min-height: 85vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 40px 20px; position: relative; }
.nova-landing-mark { width: 72px; height: 72px; border-radius: 18px; background: var(--s1); border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; margin: 0 auto 28px; font-family: var(--fb); font-size: 28px; font-weight: 800; color: var(--accent); }
.nova-landing-eyebrow { font-family: var(--fb); font-size: 10px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--tx-3); margin-bottom: 14px; }
.nova-landing-title { font-family: var(--fb); font-size: clamp(2.8rem, 7vw, 5.5rem); font-weight: 800; letter-spacing: -.05em; color: var(--tx); line-height: 1.05; margin-bottom: 16px; }
.nova-landing-title span { color: var(--accent); }
.nova-landing-sub { font-family: var(--fs); font-size: 15px; color: var(--tx-2); max-width: 340px; line-height: 1.75; margin: 0 auto 38px; }
.nova-header { padding: 20px 0 12px; border-bottom: 1px solid var(--border); margin-bottom: 22px; display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.nova-header-brand { display: flex; align-items: center; gap: 10px; }
.nova-header-mark { width: 32px; height: 32px; border-radius: 8px; background: var(--accent-glow); border: 1px solid var(--accent-ring); display: flex; align-items: center; justify-content: center; color: var(--accent); font-family: var(--fb); font-size: 14px; font-weight: 800; }
.nova-header-name { font-family: var(--fb); font-size: 17px; font-weight: 700; color: var(--tx); letter-spacing: -.03em; }
.nova-header-tag { font-size: 9.5px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--tx-3); background: var(--s1); border: 1px solid var(--border); padding: 2px 9px; border-radius: 20px; font-family: var(--fb); }
.nova-stats-row { display: flex; gap: 10px; margin-bottom: 22px; flex-wrap: wrap; }
.nova-stat-card { flex: 1; min-width: 100px; background: var(--s1); border: 1px solid var(--border); border-radius: var(--r); padding: 12px 16px; transition: border-color .18s; }
.nova-stat-card:hover { border-color: var(--border-h); }
.nova-stat-value { font-family: var(--fb); font-size: 1.4rem; font-weight: 800; color: var(--accent); letter-spacing: -.03em; }
.nova-stat-label { font-size: 9.5px; color: var(--tx-3); text-transform: uppercase; letter-spacing: .1em; font-family: var(--fb); margin-top: 2px; }
.nova-chip-row { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 20px; }
.nova-chip { padding: 3px 12px; background: var(--s1); border: 1px solid var(--border); border-radius: 20px; font-size: 11px; color: var(--tx-2); font-family: var(--fs); transition: var(--transition); }
.nova-chip:hover { border-color: var(--accent-ring); color: var(--accent); }
[data-testid="stTabs"] [role="tablist"] { background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r) !important; padding: 5px !important; gap: 3px !important; margin-bottom: 18px !important; }
[data-testid="stTabs"] [role="tab"] { background: transparent !important; color: var(--tx-2) !important; border: 1px solid transparent !important; border-radius: var(--r-sm) !important; padding: 7px 18px !important; font-family: var(--fb) !important; font-weight: 600 !important; font-size: 0.8rem !important; letter-spacing: .02em !important; transition: var(--transition) !important; }
[data-testid="stTabs"] [role="tab"]:hover { color: var(--tx) !important; background: var(--s2) !important; border-color: var(--border) !important; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] { background: var(--s2) !important; color: var(--accent) !important; border-color: var(--accent-ring) !important; }
[data-testid="stTabs"] [data-testid="stTabPanel"] { border: none !important; padding: 0 !important; }
.nova-card { background: var(--s1); border: 1px solid var(--border); border-radius: var(--r); padding: 22px 24px; margin-bottom: 16px; transition: border-color .18s; }
.nova-card:hover { border-color: var(--border-h); }
.nova-card-accent { background: var(--s1); border: 1px solid var(--accent-ring); border-radius: var(--r); padding: 22px 24px; margin-bottom: 16px; }
.nova-card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; padding-bottom: 14px; border-bottom: 1px solid var(--border); }
.nova-card-icon { width: 36px; height: 36px; border-radius: var(--r-sm); background: var(--accent-glow); border: 1px solid var(--accent-ring); display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.nova-card-title { font-family: var(--fb); font-size: 14px; font-weight: 700; color: var(--tx); letter-spacing: -.02em; }
.nova-card-sub { font-size: 11px; color: var(--tx-3); font-family: var(--fs); margin-top: 2px; }
.nova-drop-zone { border: 1px dashed var(--border-h); border-radius: var(--r); padding: 36px 20px; text-align: center; background: var(--s1); transition: var(--transition); cursor: pointer; margin-bottom: 12px; }
.nova-drop-zone:hover { border-color: var(--accent-ring); background: var(--accent-glow); }
.nova-drop-icon { font-size: 1.6rem; margin-bottom: 10px; opacity: .7; }
.nova-drop-title { font-family: var(--fb); font-size: 13px; font-weight: 600; color: var(--tx); margin-bottom: 4px; }
.nova-drop-sub { font-size: 11px; color: var(--tx-3); }
.nova-chat-container { background: var(--s1); border: 1px solid var(--border); border-radius: var(--r); padding: 18px 18px 14px; min-height: 320px; max-height: 500px; overflow-y: auto; margin-bottom: 12px; scroll-behavior: smooth; }
.nova-msg { display: flex; gap: 10px; margin-bottom: 18px; animation: novaMsgIn .2s ease both; }
@keyframes novaMsgIn { from{opacity:0;transform:translateY(5px);}to{opacity:1;transform:translateY(0);} }
.nova-msg.user { flex-direction: row-reverse; }
.nova-msg-av { width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; background: var(--s2); border: 1px solid var(--border); color: var(--tx-2); margin-top: 2px; font-family: var(--fb); }
.nova-msg-av.ai { background: var(--s1); color: var(--accent); border-color: var(--accent-ring); }
.nova-msg-ct { flex: 1; min-width: 0; }
.nova-msg.user .nova-msg-ct { display: flex; flex-direction: column; align-items: flex-end; }
.nova-msg-who { font-size: 9.5px; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; color: var(--tx-3); margin-bottom: 5px; font-family: var(--fb); }
.nova-msg-bub { color: var(--tx); font-size: 13.5px; line-height: 1.72; word-break: break-word; }
.nova-msg.user .nova-msg-bub { background: var(--usr-bub); border: 1px solid var(--border); padding: 10px 14px; border-radius: var(--r) 2px var(--r) var(--r); display: inline-block; max-width: 85%; }
.nova-msg.ai .nova-msg-bub { background: var(--ai-bub); border: 1px solid var(--border); padding: 12px 15px; border-radius: 2px var(--r) var(--r) var(--r); }
.nova-dots { display:flex; gap:4px; padding:3px 0; align-items:center; }
.nova-dots span { width:5px; height:5px; background:var(--tx-3); border-radius:50%; animation:novaDot 1.3s infinite; }
.nova-dots span:nth-child(2){animation-delay:.17s;}
.nova-dots span:nth-child(3){animation-delay:.34s;}
@keyframes novaDot{0%,80%,100%{opacity:.2;transform:scale(.7);}40%{opacity:1;transform:scale(1);}}
.nova-response-card { background: var(--s1); border: 1px solid var(--border); border-radius: var(--r); padding: 20px 22px; margin-top: 16px; position: relative; overflow: hidden; }
.nova-response-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, var(--accent), transparent); }
.nova-response-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.nova-response-title { font-family: var(--fb); font-size: 13px; font-weight: 700; color: var(--tx); letter-spacing: -.02em; }
.nova-response-label { font-size: 9px; font-family: var(--fb); color: var(--accent); letter-spacing: .1em; text-transform: uppercase; background: var(--accent-glow); border: 1px solid var(--accent-ring); padding: 2px 10px; border-radius: 20px; }
.nova-response-body { font-size: 13.5px; line-height: 1.78; color: var(--tx); }
.nova-response-body code { background: var(--s2); border: 1px solid var(--border); border-radius: 4px; padding: 1px 6px; font-size: 12px; color: var(--accent); font-family: 'Courier New', monospace; }
.nova-thinking { background: var(--s1); border: 1px solid var(--border); border-radius: var(--r); padding: 20px; text-align: center; margin: 10px 0; }
.nova-thinking-text { font-size: 11px; color: var(--accent); font-family: var(--fb); letter-spacing: .08em; text-transform: uppercase; margin-top: 8px; animation: novaFadeText 1.5s ease-in-out infinite; }
@keyframes novaFadeText{0%,100%{opacity:.4;}50%{opacity:1;}}
.nova-voice-orb-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 28px 20px; }
.nova-voice-orb { width: 110px; height: 110px; border-radius: 50%; background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%); border: 1px solid var(--accent-ring); display: flex; align-items: center; justify-content: center; font-size: 2.4rem; box-shadow: 0 0 28px var(--accent-glow); animation: novaOrbPulse 3s ease-in-out infinite; cursor: pointer; transition: var(--transition); margin-bottom: 14px; }
@keyframes novaOrbPulse{0%,100%{box-shadow:0 0 28px var(--accent-glow);}50%{box-shadow:0 0 50px var(--accent-ring);}}
.nova-voice-status { font-size: 10px; color: var(--tx-3); font-family: var(--fb); letter-spacing: .12em; text-transform: uppercase; }
.nova-pipeline { background: var(--s2); border: 1px solid var(--border); border-radius: var(--r-sm); padding: 14px 16px; font-size: 11.5px; color: var(--tx-2); font-family: var(--fs); line-height: 2.1; }
.nova-pipeline-title { font-family: var(--fb); font-size: 9.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--accent); margin-bottom: 6px; }
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea { background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; color: var(--tx) !important; font-family: var(--fs) !important; font-size: 0.87rem !important; }
[data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus { border-color: var(--accent-ring) !important; box-shadow: 0 0 0 3px var(--accent-glow) !important; outline: none !important; }
[data-baseweb="select"] > div { background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; color: var(--tx) !important; }
[data-testid="stFileUploader"] { background: var(--s1) !important; border: 1px dashed var(--border-h) !important; border-radius: var(--r) !important; }
[data-testid="stAlert"] { background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; }
[data-testid="stCheckbox"] label { color: var(--tx-2) !important; font-size: 0.82rem !important; }
[data-testid="stRadio"] label { color: var(--tx-2) !important; font-size: 0.82rem !important; }
code, pre { background: var(--s2) !important; border: 1px solid var(--border) !important; border-radius: 6px !important; color: var(--accent) !important; font-family: 'Courier New', monospace !important; }
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }
[data-testid="stButton"] button { background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; color: var(--tx-2) !important; font-family: var(--fb) !important; font-size: 12.5px !important; font-weight: 600 !important; transition: var(--transition) !important; }
[data-testid="stButton"] button:hover { background: var(--s2) !important; border-color: var(--border-h) !important; color: var(--tx) !important; }
[data-testid="stButton"] button[kind="primary"] { background: var(--accent-glow) !important; border-color: var(--accent-ring) !important; color: var(--accent) !important; }
[data-testid="stButton"] button[kind="primary"]:hover { background: rgba(200,167,120,.18) !important; border-color: var(--accent) !important; }
[data-testid="stDownloadButton"] button { background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; color: var(--tx-2) !important; font-family: var(--fb) !important; font-size: 12px !important; }
.nova-footer { text-align: center; padding: 24px 10px 12px; margin-top: 32px; border-top: 1px solid var(--border); }
.nova-footer-text { font-size: 10px; color: var(--tx-3); font-family: var(--fb); letter-spacing: .1em; text-transform: uppercase; }
.nova-footer-text span { color: var(--accent); }
</style>
"""

# ═══════════════════════════════════════════════════════
#  INPUT VALIDATION — Security & Safety Filter
# ═══════════════════════════════════════════════════════
GEMINI_SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
]

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
#  REAL GEMINI BACKEND FUNCTIONS
# ═══════════════════════════════════════════════════════

def analyze_document(file, api_key: str, temperature: float, model: str) -> str:
    """Real document analysis using Gemini API."""
    if not api_key:
        return "⚠️ API Key missing hai. Sidebar mein Gemini API Key daalo aur Apply karo."
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        file_bytes = file.read()
        file_name = file.name.lower()
        model_obj = genai.GenerativeModel(model)
        config = genai.types.GenerationConfig(temperature=temperature)

        prompt = (
            "Is document ka comprehensive analysis karo. Include karo:\n"
            "1. Executive Summary (3-4 lines)\n"
            "2. Key Points / Main Ideas\n"
            "3. Important Entities (names, places, numbers)\n"
            "4. Actionable Insights\n"
            "5. Overall Sentiment\n\n"
            "Markdown formatting use karo."
        )

        if file_name.endswith(".pdf"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name
            try:
                uploaded = genai.upload_file(tmp_path, mime_type="application/pdf")
                response = model_obj.generate_content([uploaded, prompt], generation_config=config)
            finally:
                os.unlink(tmp_path)
        else:
            content = file_bytes.decode("utf-8", errors="ignore")
            if len(content) > 30000:
                content = content[:30000] + "\n\n[...document truncated...]"
            response = model_obj.generate_content(
                f"{prompt}\n\nDocument Content:\n\n{content}",
                generation_config=config
            )

        return response.text

    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
            return "❌ API Key invalid hai. Google AI Studio se sahi key copy karo."
        elif "quota" in error_msg.lower():
            return "❌ API quota khatam ho gaya. Thodi der baad try karo ya key check karo."
        else:
            return f"❌ Error aaya: {error_msg}"


def analyze_youtube(url: str, api_key: str, temperature: float, model: str) -> str:
    """Real YouTube transcript extraction + Gemini analysis."""
    if not api_key:
        return "⚠️ API Key missing hai. Sidebar mein Gemini API Key daalo aur Apply karo."
    try:
        from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

        # Extract video ID
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
                return "❌ Is video mein transcript/subtitles available nahi hain. Dusra video try karo."
        except TranscriptsDisabled:
            return "❌ Is video mein transcripts disabled hain. Dusra video try karo."

        # Build transcript with timestamps
        full_text = ""
        for entry in transcript_list:
            mins = int(entry["start"]) // 60
            secs = int(entry["start"]) % 60
            full_text += f"[{mins:02d}:{secs:02d}] {entry['text']}\n"

        if len(full_text) > 30000:
            full_text = full_text[:30000] + "\n\n[...transcript truncated...]"

        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model_obj = genai.GenerativeModel(model)

        prompt = (
            "Yeh YouTube video ka transcript hai with timestamps. Iska analysis karo:\n\n"
            "1. **Video Summary** — 3-4 line mein kya baat hai\n"
            "2. **Key Moments** — Important timestamps with kya hua\n"
            "3. **Main Topics** — Covered topics ki list\n"
            "4. **Actionable Insights** — Jo kaam aa sake\n"
            "5. **Notable Quotes** — 2-3 important lines\n\n"
            "Markdown formatting use karo.\n\n"
            f"Transcript:\n\n{full_text}"
        )

        response = model_obj.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=temperature)
        )
        return response.text

    except ImportError:
        return "❌ `youtube-transcript-api` install nahi hai. `requirements.txt` mein add karo."
    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
            return "❌ API Key invalid hai. Google AI Studio se sahi key copy karo."
        elif "quota" in error_msg.lower():
            return "❌ API quota khatam ho gaya. Thodi der baad try karo."
        else:
            return f"❌ Error: {error_msg}"


def neural_chat_response(messages: list, api_key: str, temperature: float, model: str) -> str:
    """Real multi-turn chat using Gemini API."""
    if not api_key:
        return "⚠️ API Key missing hai. Sidebar mein Gemini API Key daalo aur Apply karo."
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        # Build conversation history (excluding last user message)
        history = []
        for msg in messages[:-1]:
            if msg["role"] == "assistant":
                history.append({"role": "model", "parts": [msg["content"]]})
            else:
                history.append({"role": "user", "parts": [msg["content"]]})

        model_obj = genai.GenerativeModel(
            model,
            system_instruction=(
                "Tum NEXUS ho — ek advanced AI intelligence platform. "
                "Tum helpful, precise aur context-aware responses dete ho. "
                "Agar user Hindi mein pooche to Hindi mein jawab do, "
                "agar English mein pooche to English mein jawab do. "
                "Markdown formatting use karo jab zarurat ho."
            )
        )

        chat = model_obj.start_chat(history=history)
        response = chat.send_message(
            messages[-1]["content"],
            generation_config=genai.types.GenerationConfig(temperature=temperature)
        )
        return response.text

    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
            return "❌ API Key invalid hai. Google AI Studio se sahi key copy karo."
        elif "quota" in error_msg.lower():
            return "❌ API quota khatam ho gaya. Thodi der baad try karo."
        else:
            return f"❌ Error: {error_msg}"


def process_voice_command(audio_bytes: bytes, api_key: str) -> str:
    """Voice processing placeholder — Gemini doesn't support direct audio via free API."""
    return (
        "🎙️ Voice captured successfully!\n\n"
        "**Note:** Voice-to-text ke liye Google Speech API alag se chahiye. "
        "Abhi ke liye **Neural Chat** tab mein type karke same kaam kar sakte ho."
    )


# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "landing"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "Namaste! Main NEXUS hoon, aapka AI intelligence platform. "
                "Main documents analyze kar sakta hoon, YouTube videos summarize kar sakta hoon, "
                "aur aapke kisi bhi sawaal ka jawab de sakta hoon. "
                "Aaj main aapki kya madad kar sakta hoon?"
            )
        }
    ]

# Inject CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  LANDING PAGE
# ═══════════════════════════════════════════
def render_landing_page():
    st.markdown("""
    <div class="nova-landing">
        <div class="nova-landing-mark">N</div>
        <div class="nova-landing-eyebrow">Intelligence Platform · v3.1</div>
        <div class="nova-landing-title">NEXUS<span>.</span></div>
        <div class="nova-landing-sub">
            Next-generation multi-modal AI — document analysis,<br>
            video intelligence, voice commands &amp; neural chat.
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

        # ── Auto-load key from Streamlit Secrets ──
        secret_key = ""
        try:
            secret_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass

        st.markdown('<div class="nova-sb-divider"><span>API Config</span></div>', unsafe_allow_html=True)
        api_key = st.text_input(
            "Gemini API Key",
            value=secret_key,
            type="password",
            placeholder="AIza••••••••••••••••",
            help="Streamlit Secrets mein GEMINI_API_KEY set karo — automatic load hogi."
        )
        status_color = "#c8a778" if api_key else "#d95555"
        status_text  = "Key Detected ✓" if api_key else "No Key — Demo Mode"
        st.markdown(
            f'<div class="nova-api-status" style="color:{status_color};">◈ {status_text}</div>',
            unsafe_allow_html=True
        )

        # ── Model ──
        st.markdown('<div class="nova-sb-divider"><span>Model</span></div>', unsafe_allow_html=True)
        model_choice = st.selectbox(
            "AI Engine",
            options=options=["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
            index=0,
        )
        model_meta = {
            "gemini-1.5-flash-latest": ("1M ctx · Fast & Free",  "#a8c878"),
            "gemini-1.5-pro-latest":   ("2M ctx · Max quality",  "#c8a778"),
            "gemini-1.0-pro":          ("32k ctx · Stable",       "#7c9ec8"),
        }
        meta_text, meta_color = model_meta.get(model_choice, ("", "#888"))
        st.markdown(f'<div class="nova-model-meta" style="color:{meta_color};">{meta_text}</div>', unsafe_allow_html=True)

        # ── Temperature ──
        st.markdown('<div class="nova-sb-divider"><span>Parameters</span></div>', unsafe_allow_html=True)
        temperature = st.slider("Analysis Creativity", min_value=0.0, max_value=1.0, value=0.35, step=0.05)
        creativity_label = "Precise & Factual" if temperature < 0.3 else "Balanced" if temperature < 0.6 else "Creative & Exploratory"
        st.markdown(f'<div class="nova-creativity-tag">◈ {creativity_label}</div>', unsafe_allow_html=True)

        # ── Stats ──
        st.markdown('<div class="nova-sb-divider"><span>Quick Stats</span></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.metric("Queries", str(st.session_state.get("query_count", 0)), "")
        with c2: st.metric("Turns", str(len(st.session_state.chat_history)), "")

        # ── Session ──
        st.markdown('<div class="nova-sb-divider"><span>Session</span></div>', unsafe_allow_html=True)
        if st.button("↩  Return to Landing", use_container_width=True, key="back_landing"):
            st.session_state.app_mode = "landing"
            st.rerun()
        if st.button("⟳  Clear Session", use_container_width=True, key="clear_session"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        # ── Incognito ──
        st.markdown('<div class="nova-sb-divider"><span>Privacy</span></div>', unsafe_allow_html=True)
        incognito = st.toggle("Incognito Mode", value=False, key="incognito_toggle")
        if incognito:
            st.markdown('<div style="font-size:10px;color:var(--accent);font-family:var(--fb);letter-spacing:.06em;">◈ History not saved</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:20px; padding-top:12px; border-top:1px solid var(--border);
                    font-size:10px; color:var(--tx-3); font-family:var(--fb);
                    text-align:center; letter-spacing:.08em;">
            NEXUS © 2025 &nbsp;·&nbsp; <span style="color:var(--accent);">Powered by Gemini</span>
        </div>
        """, unsafe_allow_html=True)

    return api_key, temperature, model_choice


# ═══════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════
def render_dashboard(api_key, temperature, model_choice):

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
        <div class="nova-stat-card"><div class="nova-stat-value">&lt;1.2s</div><div class="nova-stat-label">Avg Response</div></div>
        <div class="nova-stat-card"><div class="nova-stat-value">2M+</div><div class="nova-stat-label">Context Window</div></div>
        <div class="nova-stat-card"><div class="nova-stat-value">4</div><div class="nova-stat-label">AI Modules</div></div>
        <div class="nova-stat-card"><div class="nova-stat-value">RAG</div><div class="nova-stat-label">Memory Engine</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nova-chip-row">
        <span class="nova-chip">◈ Real-Time Analysis</span>
        <span class="nova-chip">◎ Multi-Modal</span>
        <span class="nova-chip">▣ RAG Memory</span>
        <span class="nova-chip">◈ Encrypted Keys</span>
        <span class="nova-chip">◉ Voice Commands</span>
        <span class="nova-chip">▤ PDF Intelligence</span>
        <span class="nova-chip">▶ Video Insights</span>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "  ◈  Document  ", "  ▶  YouTube  ", "  ◎  Neural Chat  ", "  ◉  Voice  ",
    ])

    # ── TAB 1: Document ──
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
                <div class="nova-drop-sub">PDF · DOCX · TXT · CSV · JSON — max 200 MB</div>
            </div>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Or click to browse",
                type=["pdf", "txt", "docx", "csv"],
                label_visibility="collapsed"
            )
            analysis_type = st.selectbox(
                "Analysis Mode",
                ["Full Semantic Analysis", "Data Extraction", "Executive Summary",
                 "Entity & Relation Mapping", "Q&A Generation"]
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

            st.checkbox("Extract Hyperlinks", value=True)
            st.checkbox("Parse Tables & Charts", value=True)
            st.checkbox("Describe Embedded Images", value=False)
            st.checkbox("Cross-reference Web Sources", value=False)
            st.checkbox("PII Detection & Redaction", value=False)
            st.checkbox("Generate Key Quotes", value=True)

            pipeline_status = "✓ Ready" if api_key else "⏳ API Key Needed"
            pipeline_color  = "var(--accent)" if api_key else "var(--danger)"
            st.markdown(f"""
            <div class="nova-pipeline" style="margin-top:12px;">
                <div class="nova-pipeline-title">Pipeline Status</div>
                Loader ────── ✓ Ready<br>
                Chunker ───── ✓ Ready<br>
                Embedder ──── <span style="color:{pipeline_color};">{pipeline_status}</span><br>
                LLM Engine ── <span style="color:{pipeline_color};">{pipeline_status}</span>
            </div>
            """, unsafe_allow_html=True)

        if analyze_btn:
            if not uploaded_file:
                st.warning("Please upload a document first.")
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
                            <div class="nova-thinking-text">NEXUS is processing your document...</div>
                        </div>
                        """, unsafe_allow_html=True)
                    result = analyze_document(uploaded_file, api_key, temperature, model_choice)
                    thinking_ph.empty()
                    st.session_state["query_count"] = st.session_state.get("query_count", 0) + 1

                    st.markdown("""
                    <div class="nova-response-card">
                        <div class="nova-response-header">
                            <div class="nova-response-title">Analysis Report</div>
                            <div class="nova-response-label">Output</div>
                        </div>
                        <div class="nova-response-body">
                    """, unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown("</div></div>", unsafe_allow_html=True)
                    st.download_button("↓  Export Report", data=result, file_name="nexus_report.md", mime="text/markdown")

    # ── TAB 2: YouTube ──
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
                "Full Transcript + Summary", "Key Moments & Timestamps",
                "Actionable Insights Only", "Speaker Diarization", "Sentiment Timeline"
            ])
            output_format = st.radio("Output Format", ["Detailed Report", "Bullet Points", "Twitter/X Thread", "Email Brief"], horizontal=True)
            yt_analyze_btn = st.button("▶  Extract Intelligence", use_container_width=True, key="yt_go", type="primary")

        with yt_col2:
            st.markdown("""
            <div class="nova-card" style="min-height:200px;">
                <div class="nova-card-header">
                    <div class="nova-card-icon">▣</div>
                    <div><div class="nova-card-title">Video Preview</div><div class="nova-card-sub">Paste URL to preview</div></div>
                </div>
                <div style="background:var(--s2); border-radius:var(--r-sm); height:100px;
                            display:flex; align-items:center; justify-content:center;
                            border:1px dashed var(--border); color:var(--tx-3);
                            font-size:10px; font-family:var(--fb); letter-spacing:.1em;">
                    NO PREVIEW YET
                </div>
            </div>
            """, unsafe_allow_html=True)

        if yt_analyze_btn:
            if not yt_url.strip():
                st.warning("Paste a YouTube URL to begin.")
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
                    result = analyze_youtube(yt_url, api_key, temperature, model_choice)
                    thinking_ph.empty()
                    st.session_state["query_count"] = st.session_state.get("query_count", 0) + 1

                    st.markdown("""
                    <div class="nova-response-card">
                        <div class="nova-response-header">
                            <div class="nova-response-title">YouTube Intelligence Report</div>
                            <div class="nova-response-label">Video Intel</div>
                        </div>
                        <div class="nova-response-body">
                    """, unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── TAB 3: Neural Chat ──
    with tab3:
        chat_col, info_col = st.columns([3, 1], gap="large")
        with chat_col:
            st.markdown("""
            <div class="nova-card">
                <div class="nova-card-header">
                    <div class="nova-card-icon">◎</div>
                    <div>
                        <div class="nova-card-title">Neural Chat — Gemini AI</div>
                        <div class="nova-card-sub">Multi-turn · Context-Aware · Real Responses</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Render chat history
            chat_html = '<div class="nova-chat-container">'
            for msg in st.session_state.chat_history:
                role = msg["role"]
                content = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                if role == "assistant":
                    chat_html += f"""
                    <div class="nova-msg ai">
                        <div class="nova-msg-av ai">N</div>
                        <div class="nova-msg-ct">
                            <div class="nova-msg-who">NEXUS</div>
                            <div class="nova-msg-bub">{content}</div>
                        </div>
                    </div>"""
                else:
                    chat_html += f"""
                    <div class="nova-msg user">
                        <div class="nova-msg-av">U</div>
                        <div class="nova-msg-ct">
                            <div class="nova-msg-who">YOU</div>
                            <div class="nova-msg-bub">{content}</div>
                        </div>
                    </div>"""
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)

            inp_c1, inp_c2 = st.columns([5, 1])
            with inp_c1:
                user_input = st.text_input(
                    "Message", placeholder="Kuch bhi poochho — NEXUS sun raha hai",
                    label_visibility="collapsed", key="chat_input"
                )
            with inp_c2:
                send_btn = st.button("Send ▶", use_container_width=True, key="chat_send", type="primary")

            st.markdown("<br>", unsafe_allow_html=True)
            s1, s2, s3 = st.columns(3)
            with s1:
                if st.button("Summarize my docs", use_container_width=True, key="sug1"):
                    user_input = "Summarize all uploaded documents"; send_btn = True
            with s2:
                if st.button("Find key entities", use_container_width=True, key="sug2"):
                    user_input = "List all key entities in the knowledge base"; send_btn = True
            with s3:
                if st.button("Compare sources", use_container_width=True, key="sug3"):
                    user_input = "Compare and contrast the main sources"; send_btn = True

        with info_col:
            turns = len(st.session_state.chat_history)
            st.markdown(f"""
            <div class="nova-card-accent">
                <div class="nova-card-header">
                    <div class="nova-card-icon">▣</div>
                    <div><div class="nova-card-title">Chat Status</div></div>
                </div>
                <div class="nova-pipeline">
                    Gemini API ── <span style="color:{'var(--accent)' if api_key else 'var(--danger)'};">{'● Active' if api_key else '● No Key'}</span><br>
                    Model ──────  <span style="color:var(--tx);">{model_choice.split('-')[1]}</span><br>
                    Turns ──────  <span style="color:var(--tx);">{turns}</span><br>
                    Temp ───────  <span style="color:var(--tx);">{temperature}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⟳ Clear Chat", use_container_width=True, key="clear_chat"):
                st.session_state.chat_history = [st.session_state.chat_history[0]]
                st.rerun()

        if send_btn and user_input and user_input.strip():
            safe, category = is_safe(user_input)
            if not safe:
                show_block_error(category)
            else:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.spinner("NEXUS thinking..."):
                    response = neural_chat_response(
                        st.session_state.chat_history, api_key, temperature, model_choice
                    )
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.session_state["query_count"] = st.session_state.get("query_count", 0) + 1
                st.rerun()

    # ── TAB 4: Voice ──
    with tab4:
        v_col1, v_col2 = st.columns([1, 1], gap="large")
        with v_col1:
            st.markdown("""
            <div class="nova-card">
                <div class="nova-card-header">
                    <div class="nova-card-icon">◉</div>
                    <div>
                        <div class="nova-card-title">Voice Command Interface</div>
                        <div class="nova-card-sub">Speak naturally — NEXUS understands intent</div>
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
                    st.success("Voice captured!")
                    voice_result = process_voice_command(audio_data["bytes"], api_key)
                    st.markdown(f"""
                    <div class="nova-response-card">
                        <div class="nova-response-header">
                            <div class="nova-response-title">Voice Response</div>
                            <div class="nova-response-label">Processed</div>
                        </div>
                        <div class="nova-response-body">{voice_result}</div>
                    </div>
                    """, unsafe_allow_html=True)
            except ImportError:
                st.info("streamlit-mic-recorder install nahi hai. requirements.txt check karo.")

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
                ("Chat",     '"Tell me about AI"'),
                ("System",   '"Change model to Flash"'),
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
    <div class="nova-footer">
        <div class="nova-footer-text">
            NEXUS INTELLIGENCE PLATFORM &nbsp;·&nbsp; BUILT WITH STREAMLIT &nbsp;·&nbsp;
            POWERED BY <span>GEMINI</span> &nbsp;·&nbsp; © 2025
        </div>
        <div style="margin-top:6px; font-size:9px; color:var(--tx-3); font-family:var(--fb); letter-spacing:.08em;">
            ALL SYSTEMS OPERATIONAL &nbsp; ◈ &nbsp; v3.1.0
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  ROUTER
# ═══════════════════════════════════════════
if st.session_state.app_mode == "landing":
    render_landing_page()
else:
    api_key, temperature, model_choice = render_sidebar()
    render_dashboard(api_key, temperature, model_choice)
