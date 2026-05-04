# ============================================================
#  NEXUS — Intelligence Platform  |  app.py
#  Theme : Nova Crystal Glass (Bronze Gold × Deep Obsidian)
#  Stack : Streamlit · streamlit_mic_recorder
# ============================================================

import streamlit as st
import time
import re

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
/* ═══════════════════════════════════════
   NOVA TOKENS
═══════════════════════════════════════ */
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

/* ═══════════════════════════════════════
   GLOBAL RESET & BASE
═══════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: var(--fs) !important;
    color: var(--tx) !important;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
}

/* Subtle noise grain overlay */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    opacity: .025;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
    background-size: 128px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* Remove default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
.block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }

/* ═══════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════ */
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

/* Sidebar inputs */
[data-testid="stSidebar"] [data-testid="stTextInput"] input,
[data-testid="stSidebar"] div[data-baseweb="input"] input {
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--tx) !important;
    font-family: var(--fs) !important;
    font-size: 0.82rem !important;
}
[data-testid="stSidebar"] div[data-baseweb="input"]:focus-within {
    border-color: var(--accent-ring) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* Sidebar slider */
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: var(--accent) !important;
    border: none !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stTickBar"] {
    background: var(--accent) !important;
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

/* ═══════════════════════════════════════
   SIDEBAR COMPONENTS
═══════════════════════════════════════ */
.nova-sidebar-brand {
    padding: 18px 14px 14px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 6px;
}
.nova-sb-logo {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 10px;
}
.nova-sb-mark {
    width: 28px; height: 28px;
    border-radius: 7px;
    background: var(--accent-glow);
    border: 1px solid var(--accent-ring);
    display: flex; align-items: center; justify-content: center;
    color: var(--accent);
    font-family: var(--fb);
    font-size: 13px; font-weight: 800;
    letter-spacing: -.02em; flex-shrink: 0;
}
.nova-sb-name {
    font-family: var(--fb);
    font-size: 15px; font-weight: 700;
    color: var(--tx); letter-spacing: -.03em;
}
.nova-sb-pill {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 10px;
    background: rgba(200,167,120,0.07);
    border: 1px solid var(--accent-ring);
    border-radius: 20px;
    font-size: 10px; font-weight: 700;
    color: var(--accent); font-family: var(--fb);
    letter-spacing: .06em;
}
.nova-sb-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 6px var(--accent);
    animation: novaPulse 2s infinite;
}
@keyframes novaPulse {
    0%,100% { opacity:1; transform:scale(1); }
    50% { opacity:.5; transform:scale(1.3); }
}

.nova-sb-divider {
    display: flex; align-items: center; gap: 8px;
    margin: 14px 0 8px; padding: 0 4px;
}
.nova-sb-divider span {
    font-size: 9.5px; font-weight: 700; letter-spacing: .1em;
    text-transform: uppercase; color: var(--tx-3);
    font-family: var(--fb); white-space: nowrap;
}
.nova-sb-divider::before, .nova-sb-divider::after {
    content: ''; flex: 1; height: 1px; background: var(--border);
}

.nova-model-meta {
    font-size: 0.68rem; font-family: var(--fb);
    letter-spacing: .04em; margin-top: -4px;
    margin-bottom: 6px; padding: 0 2px;
}
.nova-api-status {
    font-size: 0.68rem; font-family: var(--fb);
    margin-top: -4px; margin-bottom: 6px; padding: 0 2px;
}
.nova-creativity-tag {
    font-size: 0.68rem; color: var(--tx-2);
    font-family: var(--fb); margin-top: -4px;
    margin-bottom: 6px; padding: 0 2px;
}

/* Stat mini cards */
[data-testid="stMetric"] {
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-family: var(--fb) !important;
    font-size: 1.3rem !important; font-weight: 800 !important;
}
[data-testid="stMetricLabel"] { color: var(--tx-2) !important; }
[data-testid="stMetricDelta"] { color: var(--accent) !important; }

/* ═══════════════════════════════════════
   LANDING PAGE
═══════════════════════════════════════ */
.nova-landing {
    min-height: 85vh;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; padding: 40px 20px;
    position: relative;
}
.nova-landing-mark {
    width: 72px; height: 72px;
    border-radius: 18px;
    background: var(--s1);
    border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 28px;
    font-family: var(--fb); font-size: 28px; font-weight: 800;
    color: var(--accent);
}
.nova-landing-eyebrow {
    font-family: var(--fb); font-size: 10px; font-weight: 700;
    letter-spacing: .14em; text-transform: uppercase;
    color: var(--tx-3); margin-bottom: 14px;
}
.nova-landing-title {
    font-family: var(--fb);
    font-size: clamp(2.8rem, 7vw, 5.5rem);
    font-weight: 800; letter-spacing: -.05em;
    color: var(--tx); line-height: 1.05;
    margin-bottom: 16px;
}
.nova-landing-title span {
    color: var(--accent);
}
.nova-landing-sub {
    font-family: var(--fs); font-size: 15px;
    color: var(--tx-2); max-width: 340px;
    line-height: 1.75; margin: 0 auto 38px;
}
.nova-cta-btn {
    display: inline-flex; align-items: center; gap: 10px;
    padding: 14px 32px;
    background: var(--accent-glow);
    border: 1px solid var(--accent-ring);
    border-radius: var(--r);
    color: var(--accent);
    font-family: var(--fb); font-size: 13px; font-weight: 700;
    letter-spacing: .06em; text-transform: uppercase;
    cursor: pointer;
    transition: var(--transition);
}
.nova-cta-btn:hover {
    background: rgba(200,167,120,.18);
    border-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px var(--accent-glow);
}

/* ═══════════════════════════════════════
   DASHBOARD HEADER
═══════════════════════════════════════ */
.nova-header {
    padding: 20px 0 12px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 22px;
    display: flex; align-items: center;
    justify-content: space-between; gap: 12px;
    flex-wrap: wrap;
}
.nova-header-brand {
    display: flex; align-items: center; gap: 10px;
}
.nova-header-mark {
    width: 32px; height: 32px;
    border-radius: 8px;
    background: var(--accent-glow);
    border: 1px solid var(--accent-ring);
    display: flex; align-items: center; justify-content: center;
    color: var(--accent); font-family: var(--fb);
    font-size: 14px; font-weight: 800;
}
.nova-header-name {
    font-family: var(--fb); font-size: 17px; font-weight: 700;
    color: var(--tx); letter-spacing: -.03em;
}
.nova-header-tag {
    font-size: 9.5px; font-weight: 700; letter-spacing: .08em;
    text-transform: uppercase; color: var(--tx-3);
    background: var(--s1); border: 1px solid var(--border);
    padding: 2px 9px; border-radius: 20px; font-family: var(--fb);
}

/* Stats row */
.nova-stats-row {
    display: flex; gap: 10px;
    margin-bottom: 22px; flex-wrap: wrap;
}
.nova-stat-card {
    flex: 1; min-width: 100px;
    background: var(--s1);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 12px 16px;
    transition: border-color .18s;
}
.nova-stat-card:hover { border-color: var(--border-h); }
.nova-stat-value {
    font-family: var(--fb); font-size: 1.4rem;
    font-weight: 800; color: var(--accent);
    letter-spacing: -.03em;
}
.nova-stat-label {
    font-size: 9.5px; color: var(--tx-3);
    text-transform: uppercase; letter-spacing: .1em;
    font-family: var(--fb); margin-top: 2px;
}

/* Feature chips */
.nova-chip-row { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 20px; }
.nova-chip {
    padding: 3px 12px;
    background: var(--s1); border: 1px solid var(--border);
    border-radius: 20px; font-size: 11px; color: var(--tx-2);
    font-family: var(--fs); transition: var(--transition);
}
.nova-chip:hover { border-color: var(--accent-ring); color: var(--accent); }

/* ═══════════════════════════════════════
   TABS
═══════════════════════════════════════ */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    padding: 5px !important;
    gap: 3px !important;
    margin-bottom: 18px !important;
}
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: var(--tx-2) !important;
    border: 1px solid transparent !important;
    border-radius: var(--r-sm) !important;
    padding: 7px 18px !important;
    font-family: var(--fb) !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: .02em !important;
    transition: var(--transition) !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    color: var(--tx) !important;
    background: var(--s2) !important;
    border-color: var(--border) !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: var(--s2) !important;
    color: var(--accent) !important;
    border-color: var(--accent-ring) !important;
}
[data-testid="stTabs"] [data-testid="stTabPanel"] {
    border: none !important;
    padding: 0 !important;
}

/* ═══════════════════════════════════════
   NOVA GLASS CARDS
═══════════════════════════════════════ */
.nova-card {
    background: var(--s1);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 22px 24px;
    margin-bottom: 16px;
    transition: border-color .18s;
}
.nova-card:hover { border-color: var(--border-h); }
.nova-card-accent {
    background: var(--s1);
    border: 1px solid var(--accent-ring);
    border-radius: var(--r);
    padding: 22px 24px;
    margin-bottom: 16px;
}

.nova-card-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 16px; padding-bottom: 14px;
    border-bottom: 1px solid var(--border);
}
.nova-card-icon {
    width: 36px; height: 36px;
    border-radius: var(--r-sm);
    background: var(--accent-glow);
    border: 1px solid var(--accent-ring);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
}
.nova-card-title {
    font-family: var(--fb); font-size: 14px;
    font-weight: 700; color: var(--tx);
    letter-spacing: -.02em;
}
.nova-card-sub {
    font-size: 11px; color: var(--tx-3);
    font-family: var(--fs); margin-top: 2px;
}

/* ═══════════════════════════════════════
   DROP ZONE
═══════════════════════════════════════ */
.nova-drop-zone {
    border: 1px dashed var(--border-h);
    border-radius: var(--r);
    padding: 36px 20px; text-align: center;
    background: var(--s1);
    transition: var(--transition); cursor: pointer; margin-bottom: 12px;
}
.nova-drop-zone:hover {
    border-color: var(--accent-ring);
    background: var(--accent-glow);
}
.nova-drop-icon { font-size: 1.6rem; margin-bottom: 10px; opacity: .7; }
.nova-drop-title {
    font-family: var(--fb); font-size: 13px; font-weight: 600;
    color: var(--tx); margin-bottom: 4px;
}
.nova-drop-sub { font-size: 11px; color: var(--tx-3); }

/* ═══════════════════════════════════════
   CHAT
═══════════════════════════════════════ */
.nova-chat-container {
    background: var(--s1);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 18px 18px 14px;
    min-height: 320px;
    max-height: 500px;
    overflow-y: auto;
    margin-bottom: 12px;
    scroll-behavior: smooth;
}
.nova-msg {
    display: flex; gap: 10px;
    margin-bottom: 18px;
    animation: novaMsgIn .2s ease both;
}
@keyframes novaMsgIn {
    from { opacity:0; transform:translateY(5px); }
    to { opacity:1; transform:translateY(0); }
}
.nova-msg.user { flex-direction: row-reverse; }
.nova-msg-av {
    width: 28px; height: 28px; border-radius: 50%;
    flex-shrink: 0; display: flex; align-items: center;
    justify-content: center; font-size: 10px; font-weight: 700;
    background: var(--s2); border: 1px solid var(--border);
    color: var(--tx-2); margin-top: 2px; font-family: var(--fb);
}
.nova-msg-av.ai { background: var(--s1); color: var(--accent); border-color: var(--accent-ring); }
.nova-msg-ct { flex: 1; min-width: 0; }
.nova-msg.user .nova-msg-ct { display: flex; flex-direction: column; align-items: flex-end; }
.nova-msg-who {
    font-size: 9.5px; font-weight: 700; letter-spacing: .07em;
    text-transform: uppercase; color: var(--tx-3);
    margin-bottom: 5px; font-family: var(--fb);
}
.nova-msg-bub {
    color: var(--tx); font-size: 13.5px; line-height: 1.72;
    word-break: break-word;
}
.nova-msg.user .nova-msg-bub {
    background: var(--usr-bub); border: 1px solid var(--border);
    padding: 10px 14px;
    border-radius: var(--r) 2px var(--r) var(--r);
    display: inline-block; max-width: 85%;
}
.nova-msg.ai .nova-msg-bub {
    background: var(--ai-bub); border: 1px solid var(--border);
    padding: 12px 15px;
    border-radius: 2px var(--r) var(--r) var(--r);
}

/* Typing dots */
.nova-dots { display:flex; gap:4px; padding:3px 0; align-items:center; }
.nova-dots span {
    width:5px; height:5px; background:var(--tx-3);
    border-radius:50%; animation:novaDot 1.3s infinite;
}
.nova-dots span:nth-child(2){animation-delay:.17s;}
.nova-dots span:nth-child(3){animation-delay:.34s;}
@keyframes novaDot{
    0%,80%,100%{opacity:.2;transform:scale(.7);}
    40%{opacity:1;transform:scale(1);}
}

/* ═══════════════════════════════════════
   RESPONSE CARD
═══════════════════════════════════════ */
.nova-response-card {
    background: var(--s1);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 20px 22px;
    margin-top: 16px;
    position: relative; overflow: hidden;
}
.nova-response-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
}
.nova-response-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 14px; padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}
.nova-response-title {
    font-family: var(--fb); font-size: 13px; font-weight: 700;
    color: var(--tx); letter-spacing: -.02em;
}
.nova-response-label {
    font-size: 9px; font-family: var(--fb); color: var(--accent);
    letter-spacing: .1em; text-transform: uppercase;
    background: var(--accent-glow); border: 1px solid var(--accent-ring);
    padding: 2px 10px; border-radius: 20px;
}
.nova-response-body { font-size: 13.5px; line-height: 1.78; color: var(--tx); }
.nova-response-body code {
    background: var(--s2); border: 1px solid var(--border);
    border-radius: 4px; padding: 1px 6px;
    font-size: 12px; color: var(--accent);
    font-family: 'Courier New', monospace;
}

/* ═══════════════════════════════════════
   THINKING ANIMATION
═══════════════════════════════════════ */
.nova-thinking {
    background: var(--s1); border: 1px solid var(--border);
    border-radius: var(--r); padding: 20px;
    text-align: center; margin: 10px 0;
}
.nova-thinking-text {
    font-size: 11px; color: var(--accent);
    font-family: var(--fb); letter-spacing: .08em;
    text-transform: uppercase; margin-top: 8px;
    animation: novaFadeText 1.5s ease-in-out infinite;
}
@keyframes novaFadeText {
    0%,100% { opacity:.4; } 50% { opacity:1; }
}

/* ═══════════════════════════════════════
   VOICE MODULE
═══════════════════════════════════════ */
.nova-voice-orb-wrap {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 28px 20px;
}
.nova-voice-orb {
    width: 110px; height: 110px; border-radius: 50%;
    background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
    border: 1px solid var(--accent-ring);
    display: flex; align-items: center; justify-content: center;
    font-size: 2.4rem;
    box-shadow: 0 0 28px var(--accent-glow);
    animation: novaOrbPulse 3s ease-in-out infinite;
    cursor: pointer; transition: var(--transition);
    margin-bottom: 14px;
}
.nova-voice-orb:hover {
    transform: scale(1.05);
    box-shadow: 0 0 50px var(--accent-ring);
}
@keyframes novaOrbPulse {
    0%,100% { box-shadow: 0 0 28px var(--accent-glow); }
    50% { box-shadow: 0 0 50px var(--accent-ring); }
}
.nova-voice-status {
    font-size: 10px; color: var(--tx-3);
    font-family: var(--fb); letter-spacing: .12em;
    text-transform: uppercase;
}

/* ═══════════════════════════════════════
   PIPELINE STATUS BLOCK
═══════════════════════════════════════ */
.nova-pipeline {
    background: var(--s2); border: 1px solid var(--border);
    border-radius: var(--r-sm); padding: 14px 16px;
    font-size: 11.5px; color: var(--tx-2);
    font-family: var(--fs); line-height: 2.1;
}
.nova-pipeline-title {
    font-family: var(--fb); font-size: 9.5px; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    color: var(--accent); margin-bottom: 6px;
}

/* ═══════════════════════════════════════
   STREAMLIT WIDGET OVERRIDES (global)
═══════════════════════════════════════ */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--tx) !important;
    font-family: var(--fs) !important;
    font-size: 0.87rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent-ring) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
    outline: none !important;
}
[data-baseweb="select"] > div {
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--tx) !important;
}
[data-testid="stFileUploader"] {
    background: var(--s1) !important;
    border: 1px dashed var(--border-h) !important;
    border-radius: var(--r) !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-ring) !important;
}
[data-testid="stAlert"] {
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
}
[data-testid="stCheckbox"] label { color: var(--tx-2) !important; font-size: 0.82rem !important; }
[data-testid="stRadio"] label { color: var(--tx-2) !important; font-size: 0.82rem !important; }
code, pre {
    background: var(--s2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--accent) !important;
    font-family: 'Courier New', monospace !important;
}
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Buttons ─────────────────────────── */
[data-testid="stButton"] button {
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--tx-2) !important;
    font-family: var(--fb) !important;
    font-size: 12.5px !important; font-weight: 600 !important;
    transition: var(--transition) !important;
}
[data-testid="stButton"] button:hover {
    background: var(--s2) !important;
    border-color: var(--border-h) !important;
    color: var(--tx) !important;
}
[data-testid="stButton"] button[kind="primary"],
[data-testid="stButton"] button.nova-primary {
    background: var(--accent-glow) !important;
    border-color: var(--accent-ring) !important;
    color: var(--accent) !important;
}
[data-testid="stButton"] button[kind="primary"]:hover {
    background: rgba(200,167,120,.18) !important;
    border-color: var(--accent) !important;
}

/* ── Download button ─────────────────── */
[data-testid="stDownloadButton"] button {
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--tx-2) !important;
    font-family: var(--fb) !important;
    font-size: 12px !important;
}

/* ═══════════════════════════════════════
   FOOTER
═══════════════════════════════════════ */
.nova-footer {
    text-align: center;
    padding: 24px 10px 12px;
    margin-top: 32px;
    border-top: 1px solid var(--border);
}
.nova-footer-text {
    font-size: 10px; color: var(--tx-3);
    font-family: var(--fb); letter-spacing: .1em;
    text-transform: uppercase;
}
.nova-footer-text span { color: var(--accent); }
</style>
"""

# ═══════════════════════════════════════════════════════
#  INPUT VALIDATION LAYER  — Security & Safety Filter
# ═══════════════════════════════════════════════════════

# ── Gemini Safety Settings (used when real API is connected) ──
GEMINI_SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
]

# ── Keyword Blacklist ──────────────────────────────────
_BLACKLIST: dict[str, list[str]] = {

    # 1-A  Terrorism & Extremism
    "terrorism": [
        "terrorist", "terrorism", "jihad", "jihadist", "isis", "isil", "al-qaeda",
        "al qaeda", "taliban", "naxal", "naxalite", "maoists", "boko haram",
        "ied", "improvised explosive", "suicide bomber", "suicide vest",
        "bomb making", "bomb recipe", "how to make a bomb", "detonate",
        "detonator", "car bomb", "letter bomb", "pipe bomb",
    ],

    # 1-B  Weapons
    "weapons": [
        "gun mechanism", "how to make a gun", "3d print gun", "3d printed gun",
        "ghost gun", "untraceable firearm", "silencer diy", "suppressor diy",
        "chemical weapon", "nerve agent", "sarin", "vx nerve", "mustard gas",
        "poison gas", "cyanide recipe", "ricin recipe", "how to make poison",
        "bioweapon", "anthrax recipe", "weaponize", "hollow point ammunition",
    ],

    # 1-C  Cybercrime
    "cybercrime": [
        "hacking tool", "hack into", "how to hack", "ddos attack", "ddos script",
        "botnet", "sql injection script", "sql injection attack",
        "phishing page code", "phishing kit", "keylogger code", "keylogger script",
        "bypass security", "bypass authentication", "bypass 2fa",
        "exploit vulnerability", "zero day exploit", "malware code",
        "ransomware code", "rootkit", "backdoor script", "rat tool",
        "credential stuffing", "brute force script", "password cracker",
    ],

    # 2-A  Adult & Explicit Content
    "adult_content": [
        "porn", "pornography", "pornographic", "nsfw", "xxx",
        "child abuse", "child sexual", "csam", "lolicon", "shotacon",
        "sexual violence", "rape scene", "explicit sex", "explicit sexual",
        "nude image", "nude photo", "onlyfans leak",
    ],

    # 2-B  Hate Speech
    "hate_speech": [
        "kill all muslims", "kill all hindus", "kill all jews", "kill all christians",
        "hate muslims", "hate hindus", "hate christians", "hate jews",
        "casteism", "dalit slur", "racial slur", "n-word",
        "communal violence", "ethnic cleansing", "genocide plan",
        "religious riot", "incite riot", "lynch mob",
        "white supremacy", "neo nazi", "nazi propaganda",
    ],

    # 2-C  Self-Harm & Suicide
    "self_harm": [
        "suicide", "how to kill myself", "how to end my life", "want to die",
        "kill myself", "self harm", "self-harm", "cut myself",
        "overdose on pills", "how many pills to die", "hanging myself",
        "methods of suicide", "painless suicide", "assisted suicide instructions",
    ],
}

# Flatten all terms into one fast-lookup set
_ALL_BANNED_TERMS: list[str] = [
    term for group in _BLACKLIST.values() for term in group
]

# Category labels for the error message
_CATEGORY_LABELS: dict[str, str] = {
    "terrorism":     "Terrorism / Extremism",
    "weapons":       "Weapons / WMD",
    "cybercrime":    "Cybercrime / Hacking",
    "adult_content": "Adult / Explicit Content",
    "hate_speech":   "Hate Speech / Violence",
    "self_harm":     "Self-Harm / Suicide",
}

_BLOCK_MSG = "Policy Violation: This request has been blocked for security reasons."


def _normalize(text: str) -> str:
    """Lowercase + remove special characters, keep spaces."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _leet_normalize(text: str) -> str:
    """Basic leet-speak / character substitution decoder."""
    subs = {
        "0": "o", "1": "i", "3": "e", "4": "a",
        "@": "a", "$": "s", "!": "i", "+": "t",
        "5": "s", "7": "t", "8": "b", "9": "g",
    }
    for char, replacement in subs.items():
        text = text.replace(char, replacement)
    return text


def is_safe(prompt: str) -> tuple[bool, str | None]:
    """
    Returns (True, None)          — prompt is clean
    Returns (False, category_key) — prompt matched a banned category
    """
    # Step 1: normalize — lowercase, remove specials, decode leet-speak
    cleaned = _normalize(_leet_normalize(prompt))

    # Step 2: per-category check (report which category fired)
    for category, terms in _BLACKLIST.items():
        for term in terms:
            # Use word-boundary-aware check so 'isis' doesn't flag 'basis'
            pattern = r"\b" + re.escape(term) + r"\b"
            if re.search(pattern, cleaned):
                return False, category

    return True, None


def validate_and_run(prompt: str, callback, *args, **kwargs):
    """
    Gate any AI call through the safety check.
    If safe → runs callback(*args, **kwargs) and returns the result.
    If blocked → displays the Nova-styled error and returns None.
    """
    safe, category = is_safe(prompt)
    if not safe:
        label = _CATEGORY_LABELS.get(category, "Policy Violation")
        st.markdown(f"""
        <div style="background:rgba(217,85,85,0.08); border:1px solid rgba(217,85,85,0.35);
                    border-left:3px solid #d95555; border-radius:var(--r);
                    padding:16px 20px; margin:10px 0;">
            <div style="font-family:var(--fb); font-size:11px; font-weight:700;
                        letter-spacing:.1em; text-transform:uppercase;
                        color:#d95555; margin-bottom:6px;">
                ⊘ Security Block — {label}
            </div>
            <div style="font-family:var(--fs); font-size:13px; color:#eae8e1; line-height:1.65;">
                {_BLOCK_MSG}
            </div>
        </div>
        """, unsafe_allow_html=True)
        return None
    return callback(*args, **kwargs)


# ─────────────────────────────────────────────
#  PLACEHOLDER BACKEND FUNCTIONS
# ─────────────────────────────────────────────
def analyze_document(file, api_key: str, temperature: float, model: str) -> str:
    """PLACEHOLDER — Document intelligence pipeline."""
    time.sleep(1.2)
    return (
        "**Document Analysis Complete**\n\n"
        f"**Model Used:** `{model}` · **Creativity:** `{temperature}`\n\n"
        "---\n\n"
        "**Executive Summary**\n"
        "This document covers key themes around innovation, strategy, and technical architecture. "
        "NEXUS identified **3 core entities**, **7 key facts**, and **2 action items**.\n\n"
        "**Key Entities Detected:** `API Endpoints`, `Architecture Patterns`, `Cost Projections`\n\n"
        "**Sentiment:** Mostly Positive · **Readability Score:** 72/100\n\n"
        "> *Backend logic pending — connect your API key to activate full analysis.*"
    )


def analyze_youtube(url: str, api_key: str, temperature: float, model: str) -> str:
    """PLACEHOLDER — YouTube transcript extraction + summarization."""
    time.sleep(1.5)
    return (
        "**YouTube Intelligence Report**\n\n"
        f"**URL Processed:** `{url[:60]}...`\n"
        f"**Model:** `{model}` · **Temperature:** `{temperature}`\n\n"
        "---\n\n"
        "**Video Summary (Auto-Generated)**\n"
        "The video discusses advanced concepts in machine learning, covering topics such as "
        "transformer architectures, attention mechanisms, and emergent AI capabilities.\n\n"
        "**Key Timestamps:**\n"
        "- `00:02:15` — Introduction to self-attention layers\n"
        "- `00:08:40` — Real-world benchmark comparisons\n"
        "- `00:15:22` — Future roadmap discussion\n\n"
        "**Actionable Insights:** `3 found` · **Key Quotes:** `5 extracted`\n\n"
        "> *Connect API key for full transcript analysis.*"
    )


def neural_chat_response(messages: list, api_key: str, temperature: float, model: str) -> str:
    """PLACEHOLDER — RAG-based conversational AI."""
    time.sleep(0.8)
    user_msg = messages[-1]["content"] if messages else "Hello"
    return (
        f"I understand you're asking about *\"{user_msg[:80]}\"*. "
        "Using the connected knowledge base, I've retrieved **3 relevant passages** "
        "with a cosine similarity score above 0.87.\n\n"
        "The key insight is that **multi-modal reasoning** requires integrating visual, "
        "textual, and structured data in a unified embedding space — enabling NEXUS to "
        "answer complex, cross-domain queries with precision.\n\n"
        "> *RAG pipeline integration pending API connection.*"
    )


def process_voice_command(audio_bytes: bytes, api_key: str) -> str:
    """PLACEHOLDER — Voice-to-text + intent extraction."""
    return "Voice command received and processed. Intent classified as: **Information Query**. Routing to Neural Chat module..."


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
                "Hello. I'm NEXUS, your intelligence interface. "
                "I can answer questions grounded in your uploaded documents "
                "or general knowledge. How can I assist you today?"
            )
        }
    ]

# ─────────────────────────────────────────────
#  INJECT CSS
# ─────────────────────────────────────────────
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  LANDING PAGE
# ═══════════════════════════════════════════
def render_landing_page():
    st.markdown("""
    <div class="nova-landing">
        <div class="nova-landing-mark">N</div>
        <div class="nova-landing-eyebrow">Intelligence Platform · v3.0</div>
        <div class="nova-landing-title">NEXUS<span>.</span></div>
        <div class="nova-landing-sub">
            Next-generation multi-modal AI — document analysis,<br>
            video intelligence, voice commands & neural chat.
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

        # ── API Config ──
        st.markdown('<div class="nova-sb-divider"><span>API Config</span></div>', unsafe_allow_html=True)
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIza••••••••••••••••",
            help="Your Google Gemini API key — stored only in session."
        )
        status_color = "#c8a778" if api_key else "#d95555"
        status_text = "Key Detected" if api_key else "No Key — Demo Mode"
        st.markdown(
            f'<div class="nova-api-status" style="color:{status_color};">◈ {status_text}</div>',
            unsafe_allow_html=True
        )

        # ── Model Selection ──
        st.markdown('<div class="nova-sb-divider"><span>Model</span></div>', unsafe_allow_html=True)
        model_choice = st.selectbox(
            "AI Engine",
            options=["gemini-1.5-pro-latest", "gemini-1.5-flash-latest", "gemini-1.0-pro"],
            index=0,
        )
        model_meta = {
            "gemini-1.5-pro-latest":   ("2M ctx · Max quality",  "#c8a778"),
            "gemini-1.5-flash-latest": ("1M ctx · Low latency",  "#a8c878"),
            "gemini-1.0-pro":          ("32k ctx · Stable",       "#7c9ec8"),
        }
        meta_text, meta_color = model_meta.get(model_choice, ("", "#888"))
        st.markdown(
            f'<div class="nova-model-meta" style="color:{meta_color};">{meta_text}</div>',
            unsafe_allow_html=True
        )

        # ── Temperature ──
        st.markdown('<div class="nova-sb-divider"><span>Parameters</span></div>', unsafe_allow_html=True)
        temperature = st.slider("Analysis Creativity", min_value=0.0, max_value=1.0, value=0.35, step=0.05)
        creativity_label = (
            "Precise & Factual" if temperature < 0.3
            else "Balanced" if temperature < 0.6
            else "Creative & Exploratory"
        )
        st.markdown(
            f'<div class="nova-creativity-tag">◈ {creativity_label}</div>',
            unsafe_allow_html=True
        )

        # ── Stats ──
        st.markdown('<div class="nova-sb-divider"><span>Quick Stats</span></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Queries", "1,247", "+18")
        with c2:
            st.metric("Tokens", "4.2M", "+320k")

        # ── Session Controls ──
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
            st.markdown(
                '<div style="font-size:10px;color:var(--accent);font-family:var(--fb);'
                'letter-spacing:.06em;">◈ History not saved</div>',
                unsafe_allow_html=True
            )

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

    # Header
    st.markdown("""
    <div class="nova-header">
        <div class="nova-header-brand">
            <div class="nova-header-mark">N</div>
            <div class="nova-header-name">NEXUS</div>
            <div class="nova-header-tag">Intelligence Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats Row
    st.markdown("""
    <div class="nova-stats-row">
        <div class="nova-stat-card"><div class="nova-stat-value">99.2%</div><div class="nova-stat-label">Uptime SLA</div></div>
        <div class="nova-stat-card"><div class="nova-stat-value">&lt;1.2s</div><div class="nova-stat-label">Avg Response</div></div>
        <div class="nova-stat-card"><div class="nova-stat-value">2M+</div><div class="nova-stat-label">Context Window</div></div>
        <div class="nova-stat-card"><div class="nova-stat-value">4</div><div class="nova-stat-label">AI Modules</div></div>
        <div class="nova-stat-card"><div class="nova-stat-value">RAG</div><div class="nova-stat-label">Memory Engine</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Feature Chips
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

    # ── Tabs ──
    tab1, tab2, tab3, tab4 = st.tabs([
        "  ◈  Document  ",
        "  ▶  YouTube  ",
        "  ◎  Neural Chat  ",
        "  ◉  Voice  ",
    ])

    # ────────────────────────────
    #  TAB 1 — Document Intelligence
    # ────────────────────────────
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
                <div class="nova-drop-title">Drag & Drop Your Document</div>
                <div class="nova-drop-sub">PDF · DOCX · TXT · CSV · JSON — max 50 MB</div>
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

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="nova-pipeline">
                <div class="nova-pipeline-title">Pipeline Status</div>
                Loader ────── ✓ Ready<br>
                Chunker ───── ✓ Ready<br>
                Embedder ──── ⏳ API Key Needed<br>
                LLM Engine ── ⏳ API Key Needed
            </div>
            """, unsafe_allow_html=True)

        if analyze_btn:
            if not uploaded_file:
                st.warning("Please upload a document first.")
            else:
                # ── Safety check on selected analysis type ──
                safe, category = is_safe(analysis_type)
                if not safe:
                    label = _CATEGORY_LABELS.get(category, "Policy Violation")
                    st.markdown(f"""
                    <div style="background:rgba(217,85,85,0.08); border:1px solid rgba(217,85,85,0.35);
                                border-left:3px solid #d95555; border-radius:var(--r);
                                padding:16px 20px; margin:10px 0;">
                        <div style="font-family:var(--fb); font-size:11px; font-weight:700;
                                    letter-spacing:.1em; text-transform:uppercase;
                                    color:#d95555; margin-bottom:6px;">
                            ⊘ Security Block — {label}
                        </div>
                        <div style="font-family:var(--fs); font-size:13px; color:#eae8e1; line-height:1.65;">
                            {_BLOCK_MSG}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
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

                st.download_button(
                    "↓  Export Report as Markdown",
                    data=result,
                    file_name="nexus_document_report.md",
                    mime="text/markdown"
                )

    # ────────────────────────────
    #  TAB 2 — YouTube Architect
    # ────────────────────────────
    with tab2:
        st.markdown("""
        <div class="nova-card">
            <div class="nova-card-header">
                <div class="nova-card-icon">▶</div>
                <div>
                    <div class="nova-card-title">YouTube Intelligence Architect</div>
                    <div class="nova-card-sub">Extract · Summarize · Analyze video content at scale</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        yt_col1, yt_col2 = st.columns([2, 1], gap="large")

        with yt_col1:
            yt_url = st.text_input(
                "YouTube URL",
                placeholder="https://www.youtube.com/watch?v=...",
                help="Paste any public YouTube video link"
            )
            yt_mode = st.selectbox(
                "Extraction Mode",
                ["Full Transcript + Summary", "Key Moments & Timestamps",
                 "Actionable Insights Only", "Speaker Diarization", "Sentiment Timeline"]
            )
            output_format = st.radio(
                "Output Format",
                ["Detailed Report", "Bullet Points", "Twitter/X Thread", "Email Brief"],
                horizontal=True
            )
            yt_analyze_btn = st.button("▶  Extract Intelligence", use_container_width=True, key="yt_go", type="primary")

        with yt_col2:
            st.markdown("""
            <div class="nova-card" style="min-height:200px;">
                <div class="nova-card-header">
                    <div class="nova-card-icon">▣</div>
                    <div>
                        <div class="nova-card-title">Video Preview</div>
                        <div class="nova-card-sub">Thumbnail appears here</div>
                    </div>
                </div>
                <div style="background:var(--s2); border-radius:var(--r-sm); height:100px;
                            display:flex; align-items:center; justify-content:center;
                            border:1px dashed var(--border); color:var(--tx-3);
                            font-size:10px; font-family:var(--fb); letter-spacing:.1em;">
                    NO PREVIEW YET
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="nova-chip-row" style="flex-direction:column; gap:6px;">
                <span class="nova-chip">✓ Transcript API</span>
                <span class="nova-chip">✓ Chapter Detection</span>
                <span class="nova-chip">⏳ Translation (Pro)</span>
            </div>
            """, unsafe_allow_html=True)

        if yt_analyze_btn:
            if not yt_url.strip():
                st.warning("Paste a YouTube URL to begin.")
            else:
                safe, category = is_safe(yt_url)
                if not safe:
                    label = _CATEGORY_LABELS.get(category, "Policy Violation")
                    st.markdown(f"""
                    <div style="background:rgba(217,85,85,0.08); border:1px solid rgba(217,85,85,0.35);
                                border-left:3px solid #d95555; border-radius:var(--r);
                                padding:16px 20px; margin:10px 0;">
                        <div style="font-family:var(--fb); font-size:11px; font-weight:700;
                                    letter-spacing:.1em; text-transform:uppercase;
                                    color:#d95555; margin-bottom:6px;">
                            ⊘ Security Block — {label}
                        </div>
                        <div style="font-family:var(--fs); font-size:13px; color:#eae8e1; line-height:1.65;">
                            {_BLOCK_MSG}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    thinking_ph = st.empty()
                    with thinking_ph.container():
                        st.markdown("""
                        <div class="nova-thinking">
                            <div class="nova-dots"><span></span><span></span><span></span></div>
                            <div class="nova-thinking-text">Fetching transcript and analyzing with NEXUS...</div>
                        </div>
                        """, unsafe_allow_html=True)
                    result = analyze_youtube(yt_url, api_key, temperature, model_choice)
                    thinking_ph.empty()

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

    # ────────────────────────────
    #  TAB 3 — Neural Chat
    # ────────────────────────────
    with tab3:
        chat_col, info_col = st.columns([3, 1], gap="large")

        with chat_col:
            st.markdown("""
            <div class="nova-card">
                <div class="nova-card-header">
                    <div class="nova-card-icon">◎</div>
                    <div>
                        <div class="nova-card-title">Neural Chat — RAG Engine</div>
                        <div class="nova-card-sub">Retrieval-Augmented · Context-Aware · Multi-turn</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Chat history render
            chat_html = '<div class="nova-chat-container">'
            for msg in st.session_state.chat_history:
                role = msg["role"]
                content = msg["content"]
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
                            <div class="nova-msg-who">You</div>
                            <div class="nova-msg-bub">{content}</div>
                        </div>
                    </div>"""
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)

            # Input row
            inp_c1, inp_c2 = st.columns([5, 1])
            with inp_c1:
                user_input = st.text_input(
                    "Message",
                    placeholder="Ask anything — NEXUS is listening",
                    label_visibility="collapsed",
                    key="chat_input"
                )
            with inp_c2:
                send_btn = st.button("Send ▶", use_container_width=True, key="chat_send", type="primary")

            # Suggested prompts
            st.markdown("<br>", unsafe_allow_html=True)
            s1, s2, s3 = st.columns(3)
            with s1:
                if st.button("Summarize my docs", use_container_width=True, key="sug1"):
                    user_input = "Summarize all uploaded documents"
                    send_btn = True
            with s2:
                if st.button("Find key entities", use_container_width=True, key="sug2"):
                    user_input = "List all key entities in the knowledge base"
                    send_btn = True
            with s3:
                if st.button("Compare sources", use_container_width=True, key="sug3"):
                    user_input = "Compare and contrast the main sources"
                    send_btn = True

        with info_col:
            st.markdown("""
            <div class="nova-card-accent">
                <div class="nova-card-header">
                    <div class="nova-card-icon">▣</div>
                    <div><div class="nova-card-title">RAG Status</div></div>
                </div>
                <div class="nova-pipeline">
                    Vector Store ── <span style="color:var(--accent)">● Active</span><br>
                    Embeddings ─── <span style="color:var(--tx-3)">● Pending</span><br>
                    Retrieval k ─── <span style="color:var(--accent)">5 chunks</span><br>
                    Reranker ───── <span style="color:var(--accent)">● On</span><br>
                    Context ──────  <span style="color:var(--accent)">8k tokens</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="nova-pipeline" style="margin-top:10px;">
                <div class="nova-pipeline-title">Memory</div>
                Session turns: <span style="color:var(--tx);">1</span><br>
                Tokens used: <span style="color:var(--tx);">~128</span><br>
                Sources loaded: <span style="color:var(--tx);">0</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⟳ Clear Chat", use_container_width=True, key="clear_chat"):
                st.session_state.chat_history = [st.session_state.chat_history[0]]
                st.rerun()

        if send_btn and user_input and user_input.strip():
            safe, category = is_safe(user_input)
            if not safe:
                label = _CATEGORY_LABELS.get(category, "Policy Violation")
                st.markdown(f"""
                <div style="background:rgba(217,85,85,0.08); border:1px solid rgba(217,85,85,0.35);
                            border-left:3px solid #d95555; border-radius:var(--r);
                            padding:16px 20px; margin:10px 0;">
                    <div style="font-family:var(--fb); font-size:11px; font-weight:700;
                                letter-spacing:.1em; text-transform:uppercase;
                                color:#d95555; margin-bottom:6px;">
                        ⊘ Security Block — {label}
                    </div>
                    <div style="font-family:var(--fs); font-size:13px; color:#eae8e1; line-height:1.65;">
                        {_BLOCK_MSG}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.spinner("NEXUS is thinking..."):
                    response = neural_chat_response(
                        st.session_state.chat_history, api_key, temperature, model_choice
                    )
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

    # ────────────────────────────
    #  TAB 4 — Voice Command
    # ────────────────────────────
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
                    st.success("Voice captured — processing...")
                    with st.spinner("Transcribing audio..."):
                        voice_result = process_voice_command(audio_data["bytes"], api_key)
                    # Validate transcribed text before showing response
                    safe, category = is_safe(voice_result)
                    if not safe:
                        label = _CATEGORY_LABELS.get(category, "Policy Violation")
                        st.markdown(f"""
                        <div style="background:rgba(217,85,85,0.08); border:1px solid rgba(217,85,85,0.35);
                                    border-left:3px solid #d95555; border-radius:var(--r);
                                    padding:16px 20px; margin:10px 0;">
                            <div style="font-family:var(--fb); font-size:11px; font-weight:700;
                                        letter-spacing:.1em; text-transform:uppercase;
                                        color:#d95555; margin-bottom:6px;">
                                ⊘ Security Block — {label}
                            </div>
                            <div style="font-family:var(--fs); font-size:13px; color:#eae8e1; line-height:1.65;">
                                {_BLOCK_MSG}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="nova-response-card">
                            <div class="nova-response-header">
                                <div class="nova-response-title">Voice Response</div>
                                <div class="nova-response-label">Transcribed</div>
                            </div>
                            <div class="nova-response-body">{voice_result}</div>
                        </div>
                        """, unsafe_allow_html=True)
            except ImportError:
                st.info("Install `streamlit-mic-recorder` to enable voice input.")

        with v_col2:
            st.markdown("""
            <div class="nova-card">
                <div class="nova-card-header">
                    <div class="nova-card-icon">▤</div>
                    <div>
                        <div class="nova-card-title">Voice Commands Guide</div>
                        <div class="nova-card-sub">Supported natural language patterns</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            commands = [
                ("Document", '"Summarize this PDF for me"'),
                ("YouTube",  '"Extract key points from this video"'),
                ("Chat",     '"Ask the knowledge base about AI"'),
                ("System",   '"Change model to Flash"'),
                ("Report",   '"Generate a full analysis report"'),
                ("Search",   '"Find all mentions of revenue"'),
            ]
            for label, example in commands:
                st.markdown(f"""
                <div style="background:var(--s1); border:1px solid var(--border);
                            border-left:2px solid var(--accent-ring); border-radius:var(--r-sm);
                            padding:9px 14px; margin-bottom:7px;
                            display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-size:11px; color:var(--accent); font-weight:600; font-family:var(--fb);">
                        {label}
                    </div>
                    <div style="font-size:11.5px; color:var(--tx-2); font-style:italic;">
                        {example}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div class="nova-pipeline" style="margin-top:10px;">
                <div class="nova-pipeline-title">Capabilities</div>
                ✓ 50+ language support<br>
                ✓ Intent classification (NLU)<br>
                ✓ Noisy environment handling<br>
                ✓ Continuous conversation mode
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="nova-footer">
        <div class="nova-footer-text">
            NEXUS INTELLIGENCE PLATFORM &nbsp;·&nbsp; BUILT WITH STREAMLIT &nbsp;·&nbsp;
            POWERED BY <span>GEMINI</span> &nbsp;·&nbsp; © 2025
        </div>
        <div style="margin-top:6px; font-size:9px; color:var(--tx-3); font-family:var(--fb); letter-spacing:.08em;">
            ALL SYSTEMS OPERATIONAL &nbsp; ◈ &nbsp; v3.0.0
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
