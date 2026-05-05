# ================================================================
#  NEXUS v7.0  —  Intelligence Platform
#  UI     : Premium Pure-Black ChatGPT-style (God Level)
#  Backend: Full v5.1 — Groq · YouTube · PDF · Vision · Voice
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
import re, os, time, json, base64, io, unicodedata
from datetime import datetime

# ── PAGE CONFIG (must be first) ──────────────────────────────────
st.set_page_config(
    page_title="NEXUS",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

FREE_MSG_LIMIT    = 15
RATE_LIMIT_MAX    = 20
RATE_LIMIT_WINDOW = 60

# ════════════════════════════════════════════════════════════════
#  THEME SYSTEM
# ════════════════════════════════════════════════════════════════
THEMES = {
    "dark": {
        "bg":          "#0A0A0A",
        "sb_bg":       "#0F0F0F",
        "s1":          "#141414",
        "s2":          "#1A1A1A",
        "s3":          "#202020",
        "border":      "#1E1E1E",
        "border_h":    "#2A2A2A",
        "tx":          "#E8E6DF",
        "tx2":         "#6B6B6B",
        "tx3":         "#2E2E2E",
        "accent":      "#C9A96E",
        "accent_dim":  "#8B6A2E",
        "accent_glow": "rgba(201,169,110,0.08)",
        "accent_ring": "rgba(201,169,110,0.18)",
        "usr_bub":     "#1A1A1A",
        "inp_bg":      "#111111",
        "danger":      "#CC4444",
        "success":     "#4A9E6B",
    },
    "light": {
        "bg":          "#F9F8F5",
        "sb_bg":       "#FFFFFF",
        "s1":          "#FFFFFF",
        "s2":          "#F2F1EC",
        "s3":          "#E8E7E1",
        "border":      "#E0DED6",
        "border_h":    "#C8C6BE",
        "tx":          "#18180E",
        "tx2":         "#6B6960",
        "tx3":         "#B0AEA8",
        "accent":      "#8B6A2E",
        "accent_dim":  "#C9A96E",
        "accent_glow": "rgba(139,106,46,0.08)",
        "accent_ring": "rgba(139,106,46,0.18)",
        "usr_bub":     "#E8E7E1",
        "inp_bg":      "#FFFFFF",
        "danger":      "#CC4444",
        "success":     "#4A9E6B",
    },
}

# ════════════════════════════════════════════════════════════════
#  PERSONAS  (from v5.1)
# ════════════════════════════════════════════════════════════════
PERSONAS = {
    "NEXUS Default": (
        "You are NEXUS — a sharp, thoughtful AI assistant. "
        "You're not robotic or overly formal. Talk like a knowledgeable friend. "
        "Be direct, clear, sometimes a little witty, but always genuinely helpful. "
        "CRITICAL LANGUAGE RULE: Always detect the language the user writes in and respond ONLY in that exact language. "
        "If they write in Hindi — respond in Hindi. If Hinglish — respond in Hinglish. If English — respond in English. "
        "Never mention which AI model or company powers you."
    ),
    "Coding Expert": (
        "You are NEXUS in Coding Expert mode — a senior software engineer. "
        "Deep expertise in Python, JavaScript, web development, databases, and DevOps. "
        "Always provide clean, production-ready code with comments. "
        "Proactively point out bugs and edge cases. Use Markdown code blocks with language tags. "
        "CRITICAL LANGUAGE RULE: Respond in the same language the user writes in. "
        "Never mention which AI model or company powers you."
    ),
    "Data Analyst": (
        "You are NEXUS in Data Analyst mode. "
        "Specialize in data analysis, statistics, business intelligence, and visualization. "
        "Provide structured, numbered insights. Use tables in Markdown where applicable. "
        "CRITICAL LANGUAGE RULE: Respond in the same language the user writes in. "
        "Never mention which AI model or company powers you."
    ),
    "Teacher / ELI5": (
        "You are NEXUS in Teacher mode. "
        "Explain everything as simply as possible — like teaching a curious 12-year-old. "
        "Use analogies, real-world examples, and step-by-step breakdowns. "
        "CRITICAL LANGUAGE RULE: Respond in the same language the user writes in. "
        "Never mention which AI model or company powers you."
    ),
    "Creative Writer": (
        "You are NEXUS in Creative Writer mode — a skilled storyteller and copywriter. "
        "Write with vivid language, compelling narrative, and strong voice. "
        "CRITICAL LANGUAGE RULE: Respond in the same language the user writes in. "
        "Never mention which AI model or company powers you."
    ),
}

MODEL_MAP = {
    "Ultra":    "llama-3.3-70b-versatile",
    "Balanced": "llama3-70b-8192",
    "Fast":     "llama-3.1-8b-instant",
}
VISION_MODEL  = "llama-3.2-90b-vision-preview"
WHISPER_MODEL = "whisper-large-v3"
FALLBACK_MODELS = [
    "llama-3.3-70b-versatile",
    "llama3-70b-8192",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
]

# ════════════════════════════════════════════════════════════════
#  SAFETY SYSTEM  (from v5.1 — full 3-layer)
# ════════════════════════════════════════════════════════════════
_BLACKLIST = {
    "terrorism": [
        "isis","isil","al qaeda","al-qaeda","taliban","boko haram","hezbollah",
        "jihadist attack","terror cell","radicalize","join isis","join taliban",
        "suicide bomber","suicide vest","bomb making","bomb recipe","how to make a bomb",
        "make a bomb","build a bomb","improvised explosive device","ied recipe",
        "detonator","car bomb","pipe bomb","mass shooting plan","attack planning",
        "blow up building","assassinate","assassination plan","kill politician",
    ],
    "weapons": [
        "how to make a gun","homemade gun","3d printed gun","ghost gun",
        "convert pistol to automatic","convert semi to full auto",
        "illegal silencer","suppressor diy","how to get gun without license",
        "make explosives","homemade explosives","explosive recipe",
        "fertilizer bomb","ammonium nitrate bomb","tnt recipe","thermite recipe",
        "molotov cocktail recipe","chemical weapon","weaponize chemical",
        "nerve agent","sarin","vx nerve","mustard gas","cyanide recipe","ricin recipe",
        "bioweapon","anthrax recipe","weaponize bacteria","dirty bomb",
        "radiological weapon","nuclear bomb recipe",
    ],
    "cybercrime": [
        "write malware","create malware","malware code","ransomware code",
        "create ransomware","virus code","trojan code","worm code","rootkit",
        "backdoor script","create backdoor","rat tool","remote access trojan",
        "ddos script","ddos tool","launch ddos","botnet script","create botnet",
        "phishing page code","phishing kit","credential harvester","cookie stealer",
        "keylogger code","keylogger script","write keylogger","password stealer",
        "hack account","hack someone account","hack instagram","hack facebook",
        "hack whatsapp","hack gmail","bypass otp","bypass 2fa hack","sim swap hack",
    ],
    "child_safety": [
        "child abuse","child sexual abuse","csam","child pornography",
        "minor pornography","underage pornography","child nude","minor nude",
        "lolicon","shotacon","shota","minor hentai","underage hentai",
        "groom child","grooming child","groom minor","seduce minor","seduce child",
    ],
    "hate_speech": [
        "kill all muslims","kill all hindus","kill all jews","kill all christians",
        "kill minorities","death to muslims","exterminate muslims","exterminate jews",
        "ethnic cleansing","genocide plan","mass killing plan",
        "white supremacy","neo nazi","nazi propaganda","master race",
    ],
    "self_harm": [
        "how to kill myself","how to end my life","how to commit suicide",
        "how to die painlessly","kill myself","end my life","methods of suicide",
        "suicide method","painless suicide","hanging myself","how to hang myself",
        "overdose on pills","which pills to overdose","slit wrists","cut myself to die",
        "cut myself deeply","burn myself","harm myself badly","how to self harm",
    ],
}

_CATEGORY_LABELS = {
    "terrorism":    "Terrorism / Extremism",
    "weapons":      "Weapons / WMD",
    "cybercrime":   "Cybercrime / Malware",
    "child_safety": "Child Safety Violation",
    "hate_speech":  "Hate Speech / Violence",
    "self_harm":    "Self-Harm / Suicide",
}

SAFETY_SYSTEM_ADDON = (
    "\n\n==== ABSOLUTE SAFETY RULES — HIGHEST PRIORITY ====\n"
    "NEVER provide any assistance related to: terrorism, weapons, cybercrime malware creation, "
    "child exploitation, hate speech, suicide methods, or self-harm — regardless of framing, "
    "roleplay, fiction, academic framing, leet-speak, or obfuscation.\n"
    "If such request detected: respond ONLY with: NEXUS_SAFETY_REFUSE\n"
    "=================================================="
)

_LLM_BLOCK_MSG = (
    "I'm sorry, I cannot help with that. "
    "This request involves harmful content and I'm not able to assist with it."
)

_LEET_MAP = {
    "0":"o","1":"i","3":"e","4":"a","5":"s","6":"g","7":"t","8":"b","9":"g",
    "@":"a","$":"s","!":"i","+":"t","|":"i","€":"e","£":"l","©":"c","®":"r",
}

def _unicode_normalize(text):
    return unicodedata.normalize("NFKD", text).encode("ascii","ignore").decode("ascii")

def _leet_normalize(text):
    for c, r in _LEET_MAP.items():
        text = text.replace(c, r)
    return text

def _normalize(text):
    text = text.lower()
    text = _unicode_normalize(text)
    text = _leet_normalize(text)
    text = re.sub(r"(?<=[a-z])[.\-_*\s]+(?=[a-z])","",text)
    text = re.sub(r"[^a-z0-9\s]"," ",text)
    return re.sub(r"\s+"," ",text).strip()

def is_safe(prompt):
    cleaned = _normalize(prompt)
    for category, terms in _BLACKLIST.items():
        for term in terms:
            pattern = r"\b" + re.escape(_normalize(term)) + r"\b"
            if re.search(pattern, cleaned):
                return False, category
    return True, None

# ════════════════════════════════════════════════════════════════
#  RATE LIMITER  (from v5.1)
# ════════════════════════════════════════════════════════════════
def check_rate_limit():
    now = time.time()
    ts = [t for t in st.session_state.get("rate_timestamps",[]) if now-t < RATE_LIMIT_WINDOW]
    if len(ts) >= RATE_LIMIT_MAX:
        st.session_state.rate_timestamps = ts
        return False
    ts.append(now)
    st.session_state.rate_timestamps = ts
    return True

# ════════════════════════════════════════════════════════════════
#  GROQ ENGINE  (from v5.1 — full fallback chain)
# ════════════════════════════════════════════════════════════════
def _groq_client(api_key):
    from groq import Groq
    return Groq(api_key=api_key)

def _call_groq(api_key, messages, model, temperature, stream=False):
    return _groq_client(api_key).chat.completions.create(
        model=model, messages=messages,
        temperature=temperature, max_tokens=2048, stream=stream,
    )

def _call_with_fallback(api_key, messages, primary_model, temperature):
    safe_messages = []
    has_sys = False
    for m in messages:
        if m["role"] == "system":
            safe_messages.append({"role":"system","content": m["content"] + SAFETY_SYSTEM_ADDON})
            has_sys = True
        else:
            safe_messages.append(m)
    if not has_sys:
        safe_messages.insert(0, {"role":"system","content": SAFETY_SYSTEM_ADDON.strip()})

    chain = [primary_model] + [m for m in FALLBACK_MODELS if m != primary_model]
    for model in chain:
        try:
            resp = _call_groq(api_key, safe_messages, model, temperature)
            content = resp.choices[0].message.content
            if content and "NEXUS_SAFETY_REFUSE" in content:
                return _LLM_BLOCK_MSG
            return content
        except Exception as e:
            err = str(e)
            if "invalid_api_key" in err.lower() or "authentication" in err.lower():
                return "⚠ API Key galat hai. Sidebar → Settings mein sahi key daalo."
            if "rate_limit" in err.lower():
                time.sleep(1); continue
            continue
    return "⚠ Abhi kuch dikkat aa rahi hai. Thodi der baad try karo."

# ════════════════════════════════════════════════════════════════
#  BACKEND FUNCTIONS  (from v5.1 — exact)
# ════════════════════════════════════════════════════════════════

# ── Document Extraction ──────────────────────────────────────────
def _extract_pdf_text(file_bytes):
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = "\n\n".join(p.extract_text() for p in pdf.pages if p.extract_text())
        return text.strip() or "[PDF mein koi readable text nahi mila]"
    except Exception:
        pass
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = "\n\n".join(p.extract_text() for p in reader.pages if p.extract_text())
        return text.strip() or "[PDF text extract nahi hua]"
    except Exception as e:
        return f"[PDF extract error: {e}]"

def _extract_docx_text(file_bytes):
    try:
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        paras = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                r = " | ".join(c.text.strip() for c in row.cells if c.text.strip())
                if r: paras.append(r)
        return "\n\n".join(paras)
    except Exception as e:
        return f"[ERROR] Could not read DOCX: {e}"

# ── Document Analysis ────────────────────────────────────────────
DOC_MODES = {
    "Full Semantic Analysis": (
        "Provide a FULL SEMANTIC ANALYSIS:\n"
        "1. Executive Summary (3-4 lines)\n2. Key Points / Main Ideas\n"
        "3. Important Entities\n4. Actionable Insights\n5. Overall Sentiment & Tone\n"
    ),
    "Executive Summary": (
        "Write a crisp EXECUTIVE SUMMARY (max 250 words):\n"
        "1. One-paragraph TL;DR\n2. Top 5 bullet-point takeaways\n3. Recommended next action\n"
    ),
    "Data Extraction": (
        "Extract ALL structured data:\n"
        "1. Numbers, statistics, dates\n2. Tables (recreate in Markdown)\n"
        "3. Named entities: people, orgs, locations\n4. URLs, emails if present\n"
    ),
    "Q&A Generation": (
        "Generate 10 insightful Q&A pairs:\n"
        "**Q:** [question]\n**A:** [answer]\n\nCover factual, inferential, analytical questions.\n"
    ),
    "🔥 Roast My Document": (
        "Brutally roast this document:\n"
        "1. What's embarrassingly wrong\n2. Most cringe-worthy parts\n"
        "3. What a smart 10-year-old would do better\n4. A savage one-liner\n"
        "5. Three serious improvements\nBe funny but constructive. Use 🔥 freely.\n"
    ),
    "🧒 ELI5 — Explain Simply": (
        "Explain like talking to a curious 10-year-old:\n"
        "1. What is this about? (1-2 simple sentences)\n2. Main idea in plain English\n"
        "3. Why does it matter? (real-world analogy)\n4. 3 things to remember\n"
    ),
    "✨ Vibe Check": (
        "Do a VIBE CHECK:\n"
        "1. Overall vibe\n2. Emotional tone\n3. Hidden subtext\n"
        "4. Trustworthiness score X/10\n5. Guess author's personality\n6. Vibe: 1 emoji + 1 sentence\n"
    ),
}

def analyze_document(file, api_key, temperature, model_tier, mode,
                     opt_hyperlinks, opt_tables, opt_images, opt_pii, opt_quotes):
    if not api_key:
        return "⚠ API Key nahi hai. Sidebar → Settings mein daalo."
    try:
        file.seek(0)
        fb = file.read()
        fn = file.name.lower()
        if fn.endswith(".pdf"):     content = _extract_pdf_text(fb)
        elif fn.endswith(".docx"):  content = _extract_docx_text(fb)
        else:                       content = fb.decode("utf-8", errors="ignore")

        if len(content) > 28000:
            content = content[:28000] + "\n\n[...document truncated at 28,000 chars...]"

        base = DOC_MODES.get(mode, DOC_MODES["Full Semantic Analysis"])
        extra = "\nAdditional tasks:\n"
        if opt_hyperlinks: extra += "- Extract all hyperlinks.\n"
        if opt_tables:     extra += "- Parse all tables in Markdown.\n"
        if opt_images:     extra += "- Describe embedded images/charts.\n"
        if opt_pii:        extra += "- Flag PII (names, emails, phones).\n"
        if opt_quotes:     extra += "- Pull 3-5 notable direct quotes.\n"

        messages = [
            {"role":"system","content": PERSONAS["NEXUS Default"]},
            {"role":"user",  "content": f"{base}{extra}\nUse Markdown.\n\nDocument:\n\n{content}"}
        ]
        return _call_with_fallback(api_key, messages, MODEL_MAP.get(model_tier,"llama-3.3-70b-versatile"), temperature)
    except Exception as e:
        return f"⚠ Error: {str(e)[:100]}"

# ── YouTube Analysis ─────────────────────────────────────────────
YT_MODES = {
    "Full Transcript + Summary": (
        "Analyze this YouTube transcript:\n"
        "1. **Video Summary** — 3-4 line overview\n2. **Key Moments** — Important timestamps\n"
        "3. **Main Topics**\n4. **Actionable Insights**\n5. **Notable Quotes** — 2-3 lines\n"
    ),
    "Key Moments & Timestamps": (
        "Extract KEY MOMENTS with timestamps:\n"
        "- Every significant moment with [MM:SS]\n"
        "- Timestamp | Event | Why it matters (table)\n"
    ),
    "Actionable Insights Only": (
        "Extract ONLY actionable insights:\n"
        "- Every concrete tip / recommendation\n"
        "- Group by theme\n- Add timestamps\n"
    ),
    "Sentiment Timeline": (
        "Create SENTIMENT TIMELINE:\n"
        "1. Overall sentiment\n2. Shifts at timestamps\n"
        "3. Most positive / negative moments\n"
        "Table: [Timestamp | Topic | Sentiment | Reason]\n"
    ),
    "📝 Quiz Generator": (
        "Generate a QUIZ from this video:\n"
        "10 MCQ questions with 4 options each.\n"
        "**Q1.** [question]\nA) ... B) ... C) ... D) ...\n**Answer:** [correct]\n"
    ),
    "📖 Chapter Detection": (
        "Detect CHAPTERS:\n"
        "| # | Timestamp | Title | Duration | Summary |\n"
        "Every chapter with descriptive title + 1-line summary.\n"
    ),
}

def analyze_youtube(url, api_key, temperature, model_tier, yt_mode, output_format):
    if not api_key:
        return "⚠ API Key nahi hai."
    try:
        from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
        match = re.search(r"(?:v=|youtu\.be/|embed/)([^&\n?#]{11})", url)
        if not match:
            return "⚠ Invalid YouTube URL."
        vid_id = match.group(1)
        try:
            ytt = YouTubeTranscriptApi()
            tl = ytt.get_transcript(vid_id, languages=["en","hi","en-IN"])
        except (TypeError, AttributeError):
            try:
                tl = YouTubeTranscriptApi.get_transcript(vid_id, languages=["en","hi","en-IN"])
            except Exception as e2:
                return f"⚠ Transcript fetch nahi hua: {str(e2)[:80]}"
        except NoTranscriptFound:
            try:
                ytt2 = YouTubeTranscriptApi()
                tl = ytt2.list(vid_id).find_generated_transcript(["en","hi"]).fetch()
            except Exception:
                return "⚠ Is video mein transcript available nahi hai."
        except TranscriptsDisabled:
            return "⚠ Is video mein transcripts disabled hain."

        full_text = ""
        for e in tl:
            m,s = int(e["start"])//60, int(e["start"])%60
            full_text += f"[{m:02d}:{s:02d}] {e['text']}\n"
        if len(full_text) > 28000:
            full_text = full_text[:28000] + "\n[...truncated...]"

        fmt_map = {
            "Detailed Report":  "Present as a well-structured Markdown report with headers.",
            "Bullet Points":    "Present EVERYTHING as concise bullet points only.",
            "Twitter/X Thread": "Format as Twitter/X thread. Start with '🧵 1/' and number each tweet. Max 280 chars each.",
            "Email Brief":      "Format as a professional email brief. Subject line + body under 200 words.",
        }
        base = YT_MODES.get(yt_mode, YT_MODES["Full Transcript + Summary"])
        fmt  = fmt_map.get(output_format, fmt_map["Detailed Report"])
        prompt = f"{base}\nOutput format: {fmt}\n\nTranscript:\n\n{full_text}"

        messages = [
            {"role":"system","content": PERSONAS["NEXUS Default"]},
            {"role":"user",  "content": prompt}
        ]
        return _call_with_fallback(api_key, messages, MODEL_MAP.get(model_tier,"llama-3.3-70b-versatile"), temperature)
    except ImportError:
        return "⚠ `youtube-transcript-api` install nahi hai."
    except Exception as e:
        return f"⚠ Error: {str(e)[:100]}"

# ── Image Vision ─────────────────────────────────────────────────
IMG_MODE_PROMPTS = {
    "General Analysis":     "",
    "Text & OCR":           "Extract ALL text visible exactly as it appears, preserving formatting. Then brief summary.",
    "Object Detection":     "List ALL objects in a Markdown table:\n| # | Object | Location | Description |\nBe exhaustive.",
    "🔥 Roast This Image":  "Brutally roast this image! Clever + funny critique. 3 genuine improvements. Use 🔥.",
    "🧒 ELI5 Explain":      "Explain what's in this image like to a 10-year-old. Simple words, fun comparisons.",
    "✨ Vibe Check":         "VIBE CHECK:\n1. Overall vibe\n2. Emotional tone\n3. Aesthetic score /10\n4. Vibe: 1 emoji + 1 sentence",
}

def analyze_image(image_bytes, mime_type, question, api_key, temperature, model_tier):
    if not api_key:
        return "⚠ API Key nahi hai."
    try:
        b64 = base64.b64encode(image_bytes).decode()
        prompt = question if question.strip() else (
            "Analyze this image thoroughly:\n1. What is in it?\n"
            "2. Key objects, people, text\n3. Colors, mood, composition\n"
            "4. Notable details\nUse Markdown."
        )
        client = _groq_client(api_key)
        resp = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {"role":"system","content":"You are a helpful image analysis assistant." + SAFETY_SYSTEM_ADDON},
                {"role":"user","content":[
                    {"type":"text","text":prompt},
                    {"type":"image_url","image_url":{"url":f"data:{mime_type};base64,{b64}"}}
                ]}
            ],
            temperature=temperature, max_tokens=1024,
        )
        content = resp.choices[0].message.content
        if content and "NEXUS_SAFETY_REFUSE" in content:
            return _LLM_BLOCK_MSG
        return content
    except Exception as e:
        err = str(e)
        if "invalid_api_key" in err.lower():
            return "⚠ API Key galat hai."
        return f"⚠ Image analysis error: {err[:100]}"

# ── Neural Chat ──────────────────────────────────────────────────
def neural_chat_response(messages, api_key, temperature, model_tier, persona="NEXUS Default"):
    if not api_key:
        return "⚠ API Key nahi hai. Sidebar → Settings mein daalo."
    system_prompt = PERSONAS.get(persona, PERSONAS["NEXUS Default"])
    primary_model = MODEL_MAP.get(model_tier, MODEL_MAP["Ultra"])
    groq_msgs = [{"role":"system","content":system_prompt}]
    for m in messages:
        role = "assistant" if m["role"] == "assistant" else "user"
        groq_msgs.append({"role":role,"content":m["content"]})
    return _call_with_fallback(api_key, groq_msgs, primary_model, temperature)

# ── Voice Transcription ──────────────────────────────────────────
def transcribe_voice(audio_bytes, api_key):
    try:
        client = _groq_client(api_key)
        result = client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes, "audio/wav"),
            model=WHISPER_MODEL, response_format="text",
        )
        return str(result)
    except Exception as e:
        return f"[Transcription error: {str(e)[:80]}]"

# ── Text Transform ───────────────────────────────────────────────
TRANSFORM_MODES = [
    ("🐦","Twitter / X Thread",   "3-5 punchy tweets mein convert karo",         "Convert into a compelling Twitter/X thread. Punchy, engaging, emojis. Number each tweet. Max 280 chars."),
    ("💼","LinkedIn Post",         "Professional LinkedIn post banao",             "Convert into a professional LinkedIn post. Strong hook, key insights, CTA. 3-5 relevant hashtags at end."),
    ("📧","Formal Email",          "Professional email mein convert karo",         "Convert into a well-structured formal email. Subject line, greeting, body, professional sign-off."),
    ("📱","WhatsApp Message",      "Casual aur short message banao",               "Convert into a casual, friendly WhatsApp message. Short, conversational, natural."),
    ("📝","Short Summary",         "3-4 lines mein summarize karo",                "Summarize in exactly 3-4 concise sentences. Most essential points only. Be direct."),
    ("🌐","Hindi ↔ English",       "Language translate karo",                      "Detect language. If English → translate to fluent Hindi. If Hindi → translate to fluent English. Only translation, no explanation."),
    ("💬","Casual Explanation",    "Simple tarike se explain karo",                "Explain casually like to a friend over chai. No jargon. Use Hinglish if it helps."),
    ("⚡","Bullet Points",         "Key points bullets mein nikalo",               "Extract key points as clean bullet points. Max 1 line each. Start each with relevant emoji."),
]

def run_transform(text, mode_idx, api_key, model_tier):
    if not api_key:
        return "⚠ API Key nahi hai."
    _, _, _, prompt_instr = TRANSFORM_MODES[mode_idx]
    full_prompt = f"{prompt_instr}\n\n---\n\n{text.strip()}"
    try:
        client = _groq_client(api_key)
        resp = client.chat.completions.create(
            model=MODEL_MAP.get(model_tier, MODEL_MAP["Ultra"]),
            messages=[
                {"role":"system","content":"You are a precise text transformation engine. Output only the transformed result." + SAFETY_SYSTEM_ADDON},
                {"role":"user","content":full_prompt}
            ],
            temperature=0.6, max_tokens=1200,
        )
        r = resp.choices[0].message.content.strip()
        return _LLM_BLOCK_MSG if "NEXUS_SAFETY_REFUSE" in r else r
    except Exception as e:
        return f"⚠ Error: {str(e)[:80]}"

# ── API Key Validation ───────────────────────────────────────────
def validate_api_key(api_key):
    if not api_key or len(api_key.strip()) < 20:
        return False, "Key too short or empty."
    try:
        resp = _call_groq(api_key, [{"role":"user","content":"Say OK"}], "llama-3.1-8b-instant", 0.1)
        if resp.choices[0].message.content:
            return True, "✓ API Key valid"
        return False, "Unexpected empty response."
    except Exception as e:
        err = str(e)
        if "invalid_api_key" in err.lower() or "authentication" in err.lower():
            return False, "Invalid API Key."
        elif "rate_limit" in err.lower():
            return True, "Key valid but rate limited."
        return False, f"Error: {err[:80]}"

# ════════════════════════════════════════════════════════════════
#  SESSION STATE
# ════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "messages":         [],
        "sessions":         [],
        "query_count":      0,
        "locked":           False,
        "rate_timestamps":  [],
        "theme":            "dark",
        "persona":          "NEXUS Default",
        "model_tier":       "Ultra",
        "temperature":      0.7,
        "active_tool":      None,
        "show_tools":       False,
        "tool_context":     None,
        "tool_result":      None,
        "input_counter":    0,
        "incognito":        False,
        "sidebar_view":     "chats",
        "doc_mode":         "Full Semantic Analysis",
        "doc_opts":         [True, True, False, False, True],
        "yt_mode":          "Full Transcript + Summary",
        "yt_fmt":           "Detailed Report",
        "img_mode_idx":     0,
        "transform_idx":    None,
        "validated_key":    False,
        "key_status":       "",
        "show_key_input":   False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

T = THEMES[st.session_state.theme]

# ════════════════════════════════════════════════════════════════
#  GET API KEY  (secrets-first, silent)
# ════════════════════════════════════════════════════════════════
def get_api_key():
    try:
        k = st.secrets.get("GROQ_API_KEY","")
        if k: return k
    except Exception:
        pass
    return st.session_state.get("user_api_key","")

# ════════════════════════════════════════════════════════════════
#  PREMIUM CSS — GOD LEVEL
# ════════════════════════════════════════════════════════════════
def inject_css():
    t = T
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@300;400;500;600&display=swap');

/* ─── RESET ─── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

/* ─── BASE ─── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {{
    background: {t['bg']} !important;
    font-family: 'Sora', sans-serif !important;
    color: {t['tx']} !important;
    -webkit-font-smoothing: antialiased;
}}

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar {{ width: 3px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {t['border_h']}; border-radius: 2px; }}

/* ─── HIDE STREAMLIT CHROME ─── */
#MainMenu, footer, header {{ display: none !important; visibility: hidden !important; }}
[data-testid="stDecoration"],
[data-testid="stToolbar"],
[data-testid="stStatusWidget"],
[data-testid="stHeader"],
[data-testid="InputInstructions"] {{ display: none !important; }}

/* ─── MAIN BLOCK ─── */
.main .block-container {{
    max-width: 780px !important;
    margin: 0 auto !important;
    padding: 0 1.25rem 180px !important;
}}

/* ─── SIDEBAR ─── */
[data-testid="stSidebar"] {{
    background: {t['sb_bg']} !important;
    border-right: 1px solid {t['border']} !important;
    min-width: 260px !important;
    max-width: 260px !important;
}}
[data-testid="stSidebar"] * {{ font-family: 'Sora', sans-serif !important; }}
[data-testid="stSidebarContent"] {{ padding: 0 !important; }}

/* ─── GLOBAL BUTTONS ─── */
.stButton > button {{
    background: transparent !important;
    border: 1px solid {t['border_h']} !important;
    color: {t['tx']} !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    border-radius: 10px !important;
    transition: background 0.15s, border-color 0.15s !important;
    padding: 8px 14px !important;
    font-weight: 500 !important;
}}
.stButton > button:hover {{
    background: {t['s2']} !important;
    border-color: {t['border_h']} !important;
    color: {t['tx']} !important;
}}
.stButton > button:focus {{ outline: none !important; box-shadow: none !important; }}
.stButton > button[kind="primary"] {{
    background: {t['accent']} !important;
    border-color: {t['accent']} !important;
    color: #000 !important;
    font-weight: 700 !important;
}}
.stButton > button[kind="primary"]:hover {{ opacity: 0.88 !important; }}

/* ─── SIDEBAR BUTTONS ─── */
[data-testid="stSidebar"] .stButton > button {{
    border: none !important;
    padding: 9px 14px !important;
    border-radius: 8px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-size: 13px !important;
    width: 100% !important;
    color: {t['tx2']} !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: {t['s2']} !important;
    color: {t['tx']} !important;
    border: none !important;
}}

/* ─── CHAT INPUT (fixed bottom) ─── */
[data-testid="stChatInput"] {{
    position: fixed !important;
    bottom: 16px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(760px, calc(100vw - 2rem)) !important;
    background: {t['inp_bg']} !important;
    border: 1px solid {t['border_h']} !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 24px rgba(0,0,0,0.4), 0 0 0 1px {t['border']} !important;
    z-index: 900 !important;
    padding: 2px 6px !important;
    transition: border-color 0.2s !important;
}}
[data-testid="stChatInput"]:focus-within {{
    border-color: {t['accent_dim']} !important;
    box-shadow: 0 2px 24px rgba(0,0,0,0.4), 0 0 0 1px {t['border']}, 0 0 0 3px {t['accent_glow']} !important;
}}
[data-testid="stChatInput"] textarea {{
    background: transparent !important;
    color: {t['tx']} !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 15px !important;
    border: none !important;
    outline: none !important;
    resize: none !important;
    padding: 13px 14px !important;
    caret-color: {t['accent']} !important;
    line-height: 1.6 !important;
}}
[data-testid="stChatInput"] textarea::placeholder {{ color: {t['tx2']} !important; font-size: 14px !important; }}
[data-testid="stChatInput"] button {{
    background: {t['accent']} !important;
    border: none !important;
    border-radius: 10px !important;
    color: #000 !important;
    font-weight: 700 !important;
    margin: 4px 4px 4px 0 !important;
    transition: opacity 0.2s !important;
}}
[data-testid="stChatInput"] button:hover {{ opacity: 0.85 !important; }}

/* ─── CHAT MESSAGES ─── */
[data-testid="stChatMessage"] {{
    background: transparent !important;
    border: none !important;
    padding: 4px 0 !important;
    animation: nxFadeUp 0.25s ease forwards;
}}
[data-testid="stChatMessage"] p {{
    font-size: 15px !important;
    line-height: 1.8 !important;
    color: {t['tx']} !important;
}}
[data-testid="stChatMessageAvatarAssistant"] {{
    background: {t['accent_glow']} !important;
    border: 1px solid {t['accent_ring']} !important;
    border-radius: 8px !important;
    width: 28px !important; height: 28px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 11px !important; font-weight: 800 !important;
    color: {t['accent']} !important;
}}
[data-testid="stChatMessageAvatarUser"] {{
    background: {t['s2']} !important;
    border: 1px solid {t['border_h']} !important;
    border-radius: 8px !important;
    width: 28px !important; height: 28px !important;
}}

/* ─── TEXT INPUT ─── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {{
    background: {t['s1']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 10px !important;
    color: {t['tx']} !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
}}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {{
    border-color: {t['accent_dim']} !important;
    box-shadow: 0 0 0 3px {t['accent_glow']} !important;
}}

/* ─── FILE UPLOADER ─── */
[data-testid="stFileUploader"] {{
    background: {t['s1']} !important;
    border: 1px dashed {t['border_h']} !important;
    border-radius: 12px !important;
}}
[data-testid="stFileUploader"] section {{ background: transparent !important; border: none !important; }}
[data-testid="stFileUploader"] label {{ color: {t['tx2']} !important; font-size: 12px !important; }}

/* ─── SELECTBOX ─── */
[data-baseweb="select"] > div {{
    background: {t['s1']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 10px !important;
    color: {t['tx']} !important;
    font-size: 13px !important;
}}
[data-baseweb="popover"] {{ background: {t['s2']} !important; }}

/* ─── CHECKBOX ─── */
[data-testid="stCheckbox"] label {{ color: {t['tx']} !important; font-size: 13px !important; }}
[data-testid="stCheckbox"] span[aria-checked="true"] {{ background: {t['accent']} !important; border-color: {t['accent']} !important; }}

/* ─── TOGGLE ─── */
[data-testid="stToggle"] label {{ color: {t['tx']} !important; font-size: 13px !important; }}

/* ─── SLIDER ─── */
[role="slider"] {{ background: {t['accent']} !important; border: none !important; }}

/* ─── RADIO ─── */
[data-testid="stRadio"] label {{ color: {t['tx']} !important; font-size: 13px !important; }}

/* ─── CODE ─── */
code, pre {{
    background: {t['s2']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 6px !important;
    color: {t['accent']} !important;
    font-family: 'Courier New', monospace !important;
}}

/* ─── EXPANDER ─── */
details {{
    background: {t['s1']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}
details summary {{
    color: {t['tx']} !important;
    font-size: 13px !important;
    padding: 12px 16px !important;
    cursor: pointer !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
}}

/* ─── ALERT ─── */
[data-testid="stAlert"] {{
    background: {t['s1']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 10px !important;
}}

/* ─── DOWNLOAD BUTTON ─── */
[data-testid="stDownloadButton"] button {{
    background: {t['s1']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 10px !important;
    color: {t['tx2']} !important;
    font-size: 12px !important;
    font-family: 'Sora', sans-serif !important;
}}

/* ─── DIVIDER ─── */
hr {{ border-top: 1px solid {t['border']} !important; margin: 8px 0 !important; }}

/* ─── ANIMATIONS ─── */
@keyframes nxFadeUp {{
    from {{ opacity:0; transform:translateY(8px); }}
    to   {{ opacity:1; transform:translateY(0); }}
}}
@keyframes nxPopIn {{
    from {{ opacity:0; transform:translateY(6px) scale(0.97); }}
    to   {{ opacity:1; transform:translateY(0) scale(1); }}
}}
@keyframes nxPulse {{
    0%,100% {{ opacity:1; }}
    50%     {{ opacity:0.4; }}
}}
@keyframes nxDot {{
    0%,80%,100% {{ opacity:.2; transform:scale(.7); }}
    40%         {{ opacity:1;  transform:scale(1); }}
}}

/* ─── NX COMPONENTS ─── */
.nx-sb-brand {{
    padding: 18px 16px 14px;
    border-bottom: 1px solid {t['border']};
    display: flex; align-items: center; gap: 10px;
}}
.nx-sb-mark {{
    width: 30px; height: 30px;
    background: {t['accent_glow']};
    border: 1px solid {t['accent_ring']};
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13px; font-weight: 800;
    color: {t['accent']};
    flex-shrink: 0;
}}
.nx-sb-name {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 15px; font-weight: 800;
    color: {t['tx']}; letter-spacing: -.03em;
}}
.nx-sb-tag {{
    font-size: 9px; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    color: {t['tx2']};
}}
.nx-sb-pill {{
    display: flex; align-items: center; gap: 5px;
    background: {t['accent_glow']};
    border: 1px solid {t['accent_ring']};
    border-radius: 20px;
    padding: 3px 10px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10px; font-weight: 700;
    color: {t['accent']};
    letter-spacing: .06em;
    margin-left: auto;
}}
.nx-sb-dot {{
    width: 5px; height: 5px;
    border-radius: 50%;
    background: {t['accent']};
    animation: nxPulse 2s infinite;
}}
.nx-section-label {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9px; font-weight: 700;
    letter-spacing: .12em; text-transform: uppercase;
    color: {t['tx3']};
    padding: 16px 16px 6px;
    display: block;
}}
.nx-chat-item {{
    display: flex; align-items: center; gap: 9px;
    padding: 8px 14px; margin: 1px 8px;
    border-radius: 8px; cursor: pointer;
    font-size: 13px; color: {t['tx2']};
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    transition: background .12s;
}}
.nx-chat-item:hover {{ background: {t['s2']}; color: {t['tx']}; }}
.nx-welcome {{
    text-align: center;
    padding: 64px 0 40px;
    animation: nxFadeUp 0.4s ease forwards;
}}
.nx-welcome-mark {{
    width: 60px; height: 60px;
    background: {t['accent_glow']};
    border: 1px solid {t['accent_ring']};
    border-radius: 16px;
    display: inline-flex; align-items: center; justify-content: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 24px; font-weight: 800;
    color: {t['accent']};
    margin-bottom: 22px;
}}
.nx-welcome h1 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 28px; font-weight: 800;
    letter-spacing: -.04em; color: {t['tx']};
    margin-bottom: 10px;
}}
.nx-welcome p {{
    font-size: 14px; color: {t['tx2']};
    line-height: 1.7; margin-bottom: 32px;
}}
.nx-grid {{
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 8px; text-align: left;
}}
.nx-suggestion {{
    background: {t['s1']};
    border: 1px solid {t['border']};
    border-radius: 12px;
    padding: 14px 16px;
    cursor: pointer;
    font-size: 13px; color: {t['tx2']};
    line-height: 1.55;
    transition: background .18s, border-color .18s;
}}
.nx-suggestion:hover {{ background: {t['s2']}; border-color: {t['border_h']}; color: {t['tx']}; }}
.nx-suggestion strong {{ display: block; color: {t['tx']}; font-size: 13px; margin-bottom: 3px; }}
.nx-tool-popup {{
    background: {t['s2']};
    border: 1px solid {t['border_h']};
    border-radius: 16px;
    padding: 10px;
    margin-bottom: 10px;
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 6px;
    animation: nxPopIn 0.18s ease forwards;
}}
.nx-panel {{
    background: {t['s1']};
    border: 1px solid {t['border']};
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 12px;
    animation: nxFadeUp 0.22s ease forwards;
}}
.nx-panel-hdr {{
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 14px;
}}
.nx-panel-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10px; font-weight: 700;
    letter-spacing: .12em; text-transform: uppercase;
    color: {t['tx2']};
}}
.nx-thinking {{
    display: flex; align-items: center; gap: 10px;
    padding: 10px 0;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11px; font-weight: 700;
    letter-spacing: .08em; text-transform: uppercase;
    color: {t['accent']};
    animation: nxPulse 1.5s infinite;
}}
.nx-dots {{ display: flex; gap: 3px; }}
.nx-dots span {{
    width: 5px; height: 5px;
    background: {t['accent']};
    border-radius: 50%;
    animation: nxDot 1.2s infinite;
}}
.nx-dots span:nth-child(2) {{ animation-delay: .15s; }}
.nx-dots span:nth-child(3) {{ animation-delay: .3s; }}
.nx-counter {{
    position: fixed; top: 12px; right: 16px;
    z-index: 9999;
    background: {t['s2']};
    border: 1px solid {t['border']};
    border-radius: 20px;
    padding: 5px 13px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10px; font-weight: 700;
    pointer-events: none; letter-spacing: .05em;
}}
.nx-mode-card {{
    background: {t['s1']};
    border: 1.5px solid {t['border']};
    border-radius: 10px;
    padding: 11px 13px;
    margin-bottom: 3px;
    transition: border-color .15s, background .15s;
}}
.nx-mode-card.sel {{ border-color: {t['accent']}; background: {t['accent_glow']}; }}
.nx-mode-card .ic {{ font-size: 18px; margin-bottom: 4px; }}
.nx-mode-label {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12px; font-weight: 700; color: {t['tx']};
    display: block; margin-bottom: 2px;
}}
.nx-mode-desc {{ font-size: 10px; color: {t['tx2']}; }}
.nx-result-hdr {{
    background: {t['s2']};
    border: 1px solid {t['border']};
    border-radius: 12px 12px 0 0;
    padding: 12px 16px;
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 18px;
}}
.nx-result-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13px; font-weight: 700; color: {t['tx']};
}}
.nx-result-badge {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9px; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    color: {t['accent']};
    background: {t['accent_glow']};
    border: 1px solid {t['accent_ring']};
    border-radius: 20px; padding: 3px 10px;
}}
.nx-result-body {{
    background: {t['s1']};
    border: 1px solid {t['border']};
    border-top: none;
    border-radius: 0 0 12px 12px;
    padding: 18px;
}}
.nx-block-err {{
    background: rgba(204,68,68,0.07);
    border: 1px solid rgba(204,68,68,0.3);
    border-left: 3px solid {t['danger']};
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0;
}}
.nx-block-err-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10px; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    color: {t['danger']}; margin-bottom: 6px;
}}
.nx-limit-wrap {{
    text-align: center; padding: 60px 20px;
    max-width: 440px; margin: 0 auto;
    animation: nxFadeUp 0.35s ease;
}}
.nx-limit-wrap h2 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 22px; font-weight: 800; color: {t['tx']};
    margin-bottom: 10px; letter-spacing: -.03em;
}}
.nx-limit-wrap p {{
    font-size: 14px; color: {t['tx2']};
    line-height: 1.75; margin-bottom: 28px;
}}
.nx-settings-row {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 0; border-bottom: 1px solid {t['border']};
}}
.nx-settings-row:last-child {{ border-bottom: none; }}
.nx-settings-label {{ font-size: 13px; color: {t['tx']}; }}
.nx-settings-val {{ font-size: 12px; color: {t['tx2']}; }}
.nx-footer-bar {{
    position: fixed; bottom: 0; left: 0; right: 0;
    height: 14px;
    background: linear-gradient(to top, {t['bg']}, transparent);
    pointer-events: none; z-index: 800;
}}
</style>
""", unsafe_allow_html=True)

inject_css()

# ════════════════════════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════════════════════════
def _save_session():
    if len(st.session_state.messages) < 1:
        return
    title = "New Chat"
    for m in st.session_state.messages:
        if m["role"] == "user":
            title = m["content"][:40] + ("…" if len(m["content"])>40 else "")
            break
    sess = {
        "id":       datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "title":    title,
        "messages": list(st.session_state.messages),
        "time":     datetime.now().strftime("%b %d, %H:%M"),
    }
    st.session_state.sessions = [sess] + [
        s for s in st.session_state.sessions if s.get("id") != sess["id"]
    ][:24]

def _new_chat():
    _save_session()
    st.session_state.messages     = []
    st.session_state.active_tool  = None
    st.session_state.show_tools   = False
    st.session_state.tool_context = None
    st.session_state.tool_result  = None
    st.session_state.query_count  = 0
    st.session_state.locked       = False
    st.session_state.input_counter += 1

def show_block_error(category):
    label = _CATEGORY_LABELS.get(category, "Policy Violation")
    st.markdown(f"""
    <div class="nx-block-err">
        <div class="nx-block-err-title">⊘ Security Block — {label}</div>
        <div style="font-size:13px;color:{T['tx']};line-height:1.65;">
            This request has been blocked by NEXUS content policy.
        </div>
    </div>
    """, unsafe_allow_html=True)

def thinking_spinner():
    st.markdown("""
    <div class="nx-thinking">
        <div class="nx-dots"><span></span><span></span><span></span></div>
        NEXUS is thinking…
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        t = T
        # Brand
        st.markdown(f"""
        <div class="nx-sb-brand">
            <div class="nx-sb-mark">N</div>
            <div>
                <div class="nx-sb-name">NEXUS</div>
                <div class="nx-sb-tag">Intelligence Platform v7.0</div>
            </div>
            <div class="nx-sb-pill"><div class="nx-sb-dot"></div>LIVE</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("✦  New Chat", key="new_chat_btn", use_container_width=True):
            _new_chat(); st.rerun()

        # View tabs
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Chats", key="view_chats", use_container_width=True):
                st.session_state.sidebar_view = "chats"; st.rerun()
        with c2:
            if st.button("Settings", key="view_settings", use_container_width=True):
                st.session_state.sidebar_view = "settings"; st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── CHATS VIEW ──
        if st.session_state.sidebar_view == "chats":
            st.markdown('<span class="nx-section-label">Recent Chats</span>', unsafe_allow_html=True)
            if not st.session_state.sessions:
                st.markdown(f'<div style="padding:8px 16px;font-size:12px;color:{t["tx3"]}">No history yet</div>', unsafe_allow_html=True)
            for sess in st.session_state.sessions[:20]:
                c_title, c_del = st.columns([6,1])
                with c_title:
                    if st.button(f"💬 {sess['title']}", key=f"sess_{sess['id']}", use_container_width=True, help=sess["time"]):
                        _save_session()
                        st.session_state.messages = list(sess["messages"])
                        st.session_state.input_counter += 1
                        st.rerun()
                with c_del:
                    if st.button("✕", key=f"del_{sess['id']}"):
                        st.session_state.sessions = [s for s in st.session_state.sessions if s["id"]!=sess["id"]]
                        st.rerun()

        # ── SETTINGS VIEW ──
        else:
            render_sidebar_settings()

        # Footer — session counter
        st.markdown("<hr>", unsafe_allow_html=True)
        remaining = max(0, FREE_MSG_LIMIT - st.session_state.query_count)
        color = t["accent"] if remaining > 5 else t["danger"]
        st.markdown(f"""
        <div style="padding:10px 16px;display:flex;align-items:center;justify-content:space-between;">
            <span style="font-size:10px;color:{t['tx2']};font-family:'Plus Jakarta Sans',sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.08em;">Session</span>
            <span style="font-size:11px;font-weight:700;color:{color};font-family:'Plus Jakarta Sans',sans-serif;">{remaining}/{FREE_MSG_LIMIT} msgs</span>
        </div>
        """, unsafe_allow_html=True)

        # User row
        st.markdown(f"""
        <div style="padding:10px 16px;border-top:1px solid {t['border']};display:flex;align-items:center;gap:10px;">
            <div style="width:28px;height:28px;border-radius:50%;background:{t['accent_glow']};border:1px solid {t['accent_ring']};display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:{t['accent']};font-family:'Plus Jakarta Sans',sans-serif;">U</div>
            <div style="font-size:12px;font-weight:600;color:{t['tx']};font-family:'Plus Jakarta Sans',sans-serif;">NEXUS User</div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar_settings():
    t = T

    # API Key
    st.markdown('<span class="nx-section-label">API Key</span>', unsafe_allow_html=True)
    secret_key = ""
    try: secret_key = st.secrets.get("GROQ_API_KEY","")
    except Exception: pass

    if secret_key:
        st.markdown(f'<div style="font-size:11px;color:{t["success"]};padding:6px 14px;font-family:Plus Jakarta Sans,sans-serif;font-weight:700;">✓ Server key active</div>', unsafe_allow_html=True)
    else:
        if st.button("🔑  Enter API Key", key="show_key_btn", use_container_width=True):
            st.session_state.show_key_input = not st.session_state.show_key_input
        if st.session_state.show_key_input:
            raw_key = st.text_input("Groq API Key", placeholder="gsk_...", type="password", key="api_key_input", label_visibility="collapsed")
            if raw_key:
                ok, msg = validate_api_key(raw_key)
                if ok:
                    st.session_state["user_api_key"] = raw_key
                    st.session_state.validated_key = True
                    st.session_state.key_status = msg
                    st.session_state.show_key_input = False
                else:
                    st.error(msg)
        if st.session_state.validated_key:
            st.markdown(f'<div style="font-size:11px;color:{t["success"]};padding:4px 14px;font-family:Plus Jakarta Sans,sans-serif;font-weight:700;">{st.session_state.key_status}</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Theme
    st.markdown('<span class="nx-section-label">Appearance</span>', unsafe_allow_html=True)
    theme_lbl = "☀️  Light Mode" if st.session_state.theme=="dark" else "🌙  Dark Mode"
    if st.button(theme_lbl, key="toggle_theme", use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme=="dark" else "dark"
        st.rerun()

    # AI Config
    st.markdown('<span class="nx-section-label">AI Configuration</span>', unsafe_allow_html=True)
    st.session_state.model_tier = st.selectbox(
        "🧠 AI Mode",
        ["Ultra","Balanced","Fast"],
        index=["Ultra","Balanced","Fast"].index(st.session_state.model_tier),
        key="model_select"
    )
    st.session_state.persona = st.selectbox(
        "🎭 Persona",
        list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.persona),
        key="persona_select"
    )
    st.session_state.temperature = st.slider(
        "🎚 Style", 0.0, 1.0,
        value=st.session_state.temperature, step=0.05, key="temp_slider"
    )
    lbl = "Precise" if st.session_state.temperature<0.3 else "Balanced" if st.session_state.temperature<0.6 else "Creative"
    st.markdown(f'<div style="font-size:10px;color:{t["tx2"]};margin-top:-6px;padding-left:2px;">{lbl}</div>', unsafe_allow_html=True)

    # Incognito
    st.markdown("<hr>", unsafe_allow_html=True)
    st.session_state.incognito = st.toggle("🕵️ Incognito Mode", value=st.session_state.incognito, key="incognito")

    # System Status
    st.markdown('<span class="nx-section-label">System Status</span>', unsafe_allow_html=True)
    api_key = get_api_key()
    status_clr = t["success"] if api_key else t["danger"]
    status_txt = "● CONNECTED" if api_key else "○ NO KEY"
    st.markdown(f"""
    <div style="margin:0 8px;padding:12px 14px;background:{t['s2']};border:1px solid {t['border']};border-radius:10px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
            <span style="font-size:12px;color:{t['tx2']}">Groq API</span>
            <span style="font-size:10px;font-weight:700;color:{status_clr};font-family:'Plus Jakarta Sans',sans-serif;">{status_txt}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
            <span style="font-size:12px;color:{t['tx2']}">Context</span>
            <span style="font-size:10px;color:{t['tx2']}">128k tokens</span>
        </div>
        <div style="display:flex;justify-content:space-between;">
            <span style="font-size:12px;color:{t['tx2']}">Model</span>
            <span style="font-size:10px;color:{t['tx2']}">LLaMA 3.3 70B</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Legal
    st.markdown('<span class="nx-section-label">Legal</span>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="padding:4px 14px;font-size:11px;color:{t['tx2']};line-height:2;">
        <a style="color:{t['tx2']};text-decoration:none;" href="#">Terms of Service</a><br>
        <a style="color:{t['tx2']};text-decoration:none;" href="#">Privacy Policy</a><br>
        <a style="color:{t['tx2']};text-decoration:none;" href="#">Content Policy</a>
    </div>
    <div style="padding:10px 14px 4px;font-family:'Plus Jakarta Sans',sans-serif;font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{t['tx3']};">
        NEXUS v7.0 · © 2026 · Made in India
    </div>
    """, unsafe_allow_html=True)

    # Clear history
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🗑️  Clear All History", key="clear_all_hist", use_container_width=True):
        st.session_state.sessions = []; st.rerun()

# ════════════════════════════════════════════════════════════════
#  WELCOME SCREEN
# ════════════════════════════════════════════════════════════════
def render_welcome():
    st.markdown(f"""
    <div class="nx-welcome">
        <div class="nx-welcome-mark">N</div>
        <h1>How can I help you?</h1>
        <p>Multi-modal AI — chat, documents, YouTube, images, voice & text transforms.</p>
        <div class="nx-grid">
            <div class="nx-suggestion"><strong>📄 Analyze a document</strong>Upload PDF or DOCX and ask anything about it</div>
            <div class="nx-suggestion"><strong>▶ YouTube breakdown</strong>Paste a URL for transcript + insights</div>
            <div class="nx-suggestion"><strong>🖼 Describe an image</strong>Upload any image for vision analysis</div>
            <div class="nx-suggestion"><strong>🔄 Transform text</strong>Convert to threads, emails, summaries</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  LIMIT WALL
# ════════════════════════════════════════════════════════════════
def render_limit_wall():
    t = T
    st.markdown(f"""
    <div class="nx-limit-wrap">
        <div style="font-size:40px;margin-bottom:18px;">⬡</div>
        <h2>Session Limit Reached</h2>
        <p>You've used all {FREE_MSG_LIMIT} free messages this session.<br>
        Start a new chat to continue — no cooldown, always free.</p>
        <div style="background:{t['s2']};border-radius:8px;height:5px;max-width:300px;margin:0 auto 28px;overflow:hidden;">
            <div style="height:100%;width:100%;border-radius:8px;background:linear-gradient(90deg,{t['accent']},{t['accent_dim']});"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    _, c, _ = st.columns([1,2,1])
    with c:
        if st.button("✦  New Chat — Continue Free", key="limit_new_btn", use_container_width=True, type="primary"):
            _new_chat(); st.rerun()

# ════════════════════════════════════════════════════════════════
#  TOOL POPUP
# ════════════════════════════════════════════════════════════════
TOOLS = [
    ("document", "📄", "Document Analysis"),
    ("youtube",  "▶️",  "YouTube Review"),
    ("image",    "🖼️",  "Image Intelligence"),
    ("voice",    "🎙️",  "Voice Command"),
    ("transform","🔄",  "Text Transform"),
    ("explore",  "✦",  "Explore NEXUS"),
]

def render_tool_popup():
    if not st.session_state.show_tools:
        return
    st.markdown('<div class="nx-tool-popup">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, (tid, icon, label) in enumerate(TOOLS):
        with cols[i%2]:
            if st.button(f"{icon}  {label}", key=f"tool_{tid}", use_container_width=True):
                st.session_state.active_tool  = tid
                st.session_state.show_tools   = False
                st.session_state.tool_context = None
                st.session_state.tool_result  = None
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  TOOL PANELS
# ════════════════════════════════════════════════════════════════
def render_tool_panel(api_key):
    tool = st.session_state.active_tool
    if not tool: return

    tool_meta = {k:(i,l) for k,i,l in [(t[0],t[1],t[2]) for t in TOOLS]}
    icon, label = tool_meta.get(tool, ("🔧", tool.title()))

    st.markdown(f"""
    <div class="nx-panel">
        <div class="nx-panel-hdr">
            <div class="nx-panel-title">{icon} &nbsp;{label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    hdr_c, close_c = st.columns([5,1])
    with close_c:
        if st.button("✕", key="close_panel_btn"):
            st.session_state.active_tool  = None
            st.session_state.tool_context = None
            st.session_state.tool_result  = None
            st.rerun()

    # ── DOCUMENT ────────────────────────────────────────────────
    if tool == "document":
        uploaded = st.file_uploader(
            "Upload document (PDF, DOCX, TXT, CSV)",
            type=["pdf","docx","txt","csv"],
            key="doc_uploader", label_visibility="collapsed"
        )
        doc_mode = st.selectbox("Analysis Mode", list(DOC_MODES.keys()), key="doc_mode_sel")
        c1,c2,c3 = st.columns(3)
        with c1: opt_h = st.checkbox("Hyperlinks", value=True, key="opt_h")
        with c2: opt_t = st.checkbox("Tables",     value=True, key="opt_t")
        with c3: opt_q = st.checkbox("Key Quotes", value=True, key="opt_q")
        c4,c5 = st.columns(2)
        with c4: opt_img = st.checkbox("Images", value=False, key="opt_img")
        with c5: opt_pii = st.checkbox("PII Detect", value=False, key="opt_pii")

        if st.button("◈  Analyze Document", key="doc_go_btn", use_container_width=True, type="primary"):
            if not uploaded:
                st.warning("Pehle document upload karo.")
            elif not api_key:
                st.error("API Key nahi hai. Sidebar → Settings mein daalo.")
            elif not check_rate_limit():
                st.error("Rate limit hit. Thodi der baad try karo.")
            else:
                safe, cat = is_safe(doc_mode)
                if not safe:
                    show_block_error(cat)
                else:
                    ph = st.empty()
                    with ph.container(): thinking_spinner()
                    result = analyze_document(uploaded, api_key, st.session_state.temperature,
                                              st.session_state.model_tier, doc_mode,
                                              opt_h, opt_t, opt_img, opt_pii, opt_q)
                    ph.empty()
                    st.session_state.query_count += 1
                    st.session_state.tool_result = result
                    if not st.session_state.incognito:
                        st.session_state.messages.append({"role":"user","content":f"[Document: {uploaded.name}] → {doc_mode}"})
                        st.session_state.messages.append({"role":"assistant","content":result})
                        _save_session()

                    if result.startswith("⚠"):
                        st.error(result)
                    else:
                        st.toast("✅ Analysis complete!", icon="✅")
                        st.markdown(f'<div class="nx-result-hdr"><div class="nx-result-title">📄 Analysis Report</div><div class="nx-result-badge">{doc_mode}</div></div>', unsafe_allow_html=True)
                        st.markdown('<div class="nx-result-body">', unsafe_allow_html=True)
                        st.markdown(result)
                        st.markdown('</div>', unsafe_allow_html=True)
                        d1,d2 = st.columns(2)
                        with d1: st.download_button("↓ Export .md", data=result, file_name="nexus_doc.md", mime="text/markdown", use_container_width=True)
                        with d2: st.download_button("↓ Export .txt",data=result, file_name="nexus_doc.txt",mime="text/plain",  use_container_width=True)

    # ── YOUTUBE ─────────────────────────────────────────────────
    elif tool == "youtube":
        yt_url = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...", key="yt_url_inp", label_visibility="collapsed")
        yt_mode = st.selectbox("Extraction Mode", list(YT_MODES.keys()), key="yt_mode_sel")
        yt_fmt  = st.radio("Output Format", ["Detailed Report","Bullet Points","Twitter/X Thread","Email Brief"], horizontal=True, key="yt_fmt_sel")

        # Preview
        if yt_url.strip():
            m = re.search(r"(?:v=|youtu\.be/|embed/)([^&\n?#]{11})", yt_url)
            if m:
                vid_id = m.group(1)
                st.markdown(f'<iframe width="100%" height="120" src="https://www.youtube.com/embed/{vid_id}" frameborder="0" style="border-radius:10px;margin:8px 0;" allowfullscreen></iframe>', unsafe_allow_html=True)

        if st.button("▶  Extract Intelligence", key="yt_go_btn", use_container_width=True, type="primary"):
            if not yt_url.strip():
                st.warning("YouTube URL paste karo.")
            elif not api_key:
                st.error("API Key nahi hai.")
            elif not check_rate_limit():
                st.error("Rate limit hit.")
            else:
                safe, cat = is_safe(yt_url)
                if not safe:
                    show_block_error(cat)
                else:
                    ph = st.empty()
                    with ph.container(): thinking_spinner()
                    result = analyze_youtube(yt_url, api_key, st.session_state.temperature,
                                             st.session_state.model_tier, yt_mode, yt_fmt)
                    ph.empty()
                    st.session_state.query_count += 1

                    if result.startswith("⚠"):
                        st.error(result)
                    else:
                        st.toast("✅ Video intelligence extracted!", icon="▶")
                        if not st.session_state.incognito:
                            st.session_state.messages.append({"role":"user","content":f"[YouTube: {yt_url}] → {yt_mode}"})
                            st.session_state.messages.append({"role":"assistant","content":result})
                            _save_session()

                        st.markdown(f'<div class="nx-result-hdr"><div class="nx-result-title">▶ YouTube Intelligence</div><div class="nx-result-badge">{yt_mode}</div></div>', unsafe_allow_html=True)
                        st.markdown('<div class="nx-result-body">', unsafe_allow_html=True)
                        st.markdown(result)
                        st.markdown('</div>', unsafe_allow_html=True)
                        d1,d2 = st.columns(2)
                        with d1: st.download_button("↓ Export .md", data=result, file_name="nexus_yt.md",  mime="text/markdown", use_container_width=True)
                        with d2: st.download_button("↓ Export .txt",data=result, file_name="nexus_yt.txt", mime="text/plain",   use_container_width=True)

    # ── IMAGE ────────────────────────────────────────────────────
    elif tool == "image":
        st.markdown(f'<div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{T["tx2"]};margin-bottom:8px;">Upload Image</div>', unsafe_allow_html=True)
        uploaded_img = st.file_uploader("Image", type=["png","jpg","jpeg","webp","gif"], key="img_up", label_visibility="collapsed")
        if uploaded_img:
            st.image(uploaded_img, use_container_width=True)

        # Mode grid
        st.markdown(f'<div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{T["tx2"]};margin:12px 0 8px;">Analysis Mode</div>', unsafe_allow_html=True)
        IMG_MODES_LIST = list(IMG_MODE_PROMPTS.keys())
        MODE_ICONS = ["🔭","🔤","📦","🔥","🧒","✨"]
        MODE_DESCS = ["Full detailed breakdown","Extract all visible text","List all objects","Savage funny critique","Explain like I'm 10","Aesthetic & vibe score"]
        selected_img_mode_idx = st.session_state.get("img_mode_idx", 0)

        for row_start in range(0, len(IMG_MODES_LIST), 2):
            cols = st.columns(2)
            for ci in range(2):
                gidx = row_start + ci
                if gidx >= len(IMG_MODES_LIST): break
                with cols[ci]:
                    is_sel = (gidx == selected_img_mode_idx)
                    sel_cls = "sel" if is_sel else ""
                    st.markdown(f'<div class="nx-mode-card {sel_cls}"><div class="ic">{MODE_ICONS[gidx]}</div><span class="nx-mode-label">{IMG_MODES_LIST[gidx]}</span><span class="nx-mode-desc">{MODE_DESCS[gidx]}</span></div>', unsafe_allow_html=True)
                    if st.button("✓" if is_sel else "Select", key=f"img_m_{gidx}", use_container_width=True,
                                 type="primary" if is_sel else "secondary"):
                        st.session_state["img_mode_idx"] = gidx; st.rerun()

        img_q = st.text_area("Custom question (optional)", placeholder="What brand is shown? Is there damage?", height=70, key="img_q", label_visibility="visible")

        if st.button("🖼  Analyze Image", key="img_go_btn", use_container_width=True, type="primary", disabled=(uploaded_img is None)):
            if not api_key:
                st.error("API Key nahi hai.")
            elif not check_rate_limit():
                st.error("Rate limit hit.")
            else:
                img_mode = IMG_MODES_LIST[st.session_state.get("img_mode_idx",0)]
                base_q = IMG_MODE_PROMPTS.get(img_mode,"")
                final_q = (f"{img_q.strip()}\n\nAlso: {base_q}" if img_q.strip() and base_q
                           else img_q.strip() or base_q or "Describe this image in detail.")
                ph = st.empty()
                with ph.container(): thinking_spinner()
                result = analyze_image(uploaded_img.getvalue(), uploaded_img.type or "image/jpeg",
                                       final_q, api_key, st.session_state.temperature, st.session_state.model_tier)
                ph.empty()
                st.session_state.query_count += 1
                if result.startswith("⚠"):
                    st.error(result)
                else:
                    st.toast("✅ Image analyzed!", icon="🖼")
                    if not st.session_state.incognito:
                        st.session_state.messages.append({"role":"user","content":f"[Image: {uploaded_img.name}] → {img_mode}"})
                        st.session_state.messages.append({"role":"assistant","content":result})
                        _save_session()
                    st.markdown(f'<div class="nx-result-hdr"><div class="nx-result-title">🖼 Vision Analysis</div><div class="nx-result-badge">{img_mode}</div></div>', unsafe_allow_html=True)
                    st.markdown('<div class="nx-result-body">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)
                    d1,d2 = st.columns(2)
                    with d1: st.download_button("↓ Export .md", data=result, file_name="nexus_vision.md",  mime="text/markdown", use_container_width=True)
                    with d2: st.download_button("↓ Export .txt",data=result, file_name="nexus_vision.txt", mime="text/plain",   use_container_width=True)

    # ── VOICE ────────────────────────────────────────────────────
    elif tool == "voice":
        st.markdown(f'<div style="text-align:center;padding:16px 0 8px;"><div style="font-size:40px;">🎙️</div><div style="font-size:12px;color:{T["tx2"]};margin-top:8px;font-family:Plus Jakarta Sans,sans-serif;font-weight:600;letter-spacing:.08em;text-transform:uppercase;">Voice Command Interface</div></div>', unsafe_allow_html=True)
        try:
            from streamlit_mic_recorder import mic_recorder
            audio_data = mic_recorder(
                start_prompt="🎙  Start Recording",
                stop_prompt="⏹  Stop Recording",
                just_once=True,
                use_container_width=True,
                key="voice_rec"
            )
            if audio_data and audio_data.get("bytes"):
                if not api_key:
                    st.error("API Key nahi hai.")
                else:
                    ph = st.empty()
                    with ph.container(): thinking_spinner()
                    transcript = transcribe_voice(audio_data["bytes"], api_key)
                    if not transcript.startswith("["):
                        voice_msgs = [{"role":"user","content":transcript}]
                        ai_reply = neural_chat_response(voice_msgs, api_key,
                                                        st.session_state.temperature,
                                                        st.session_state.model_tier,
                                                        st.session_state.persona)
                        result = f"**You said:** {transcript}\n\n---\n\n{ai_reply}"
                        if not st.session_state.incognito:
                            st.session_state.messages.append({"role":"user","content":f"🎙 {transcript}"})
                            st.session_state.messages.append({"role":"assistant","content":ai_reply})
                            _save_session()
                    else:
                        result = f"⚠ Transcription failed: {transcript}"
                    ph.empty()
                    st.session_state.query_count += 1
                    st.markdown(result)
        except ImportError:
            st.info("📦 `streamlit-mic-recorder` nahi hai. requirements.txt mein add karo.")

    # ── TRANSFORM ────────────────────────────────────────────────
    elif tool == "transform":
        transform_input = st.text_area(
            "Input Text",
            placeholder="Koi bhi text paste karo — article, paragraph, notes...",
            height=140, key="transform_inp", label_visibility="collapsed"
        )
        char_c = len(transform_input)
        st.markdown(f'<div style="font-size:10px;color:{T["tx2"]};text-align:right;margin-top:-6px;margin-bottom:12px;">{char_c} chars</div>', unsafe_allow_html=True)

        st.markdown(f'<div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{T["tx2"]};margin-bottom:8px;">Transform Mode</div>', unsafe_allow_html=True)
        sel_tr = st.session_state.get("transform_idx", None)
        for row_start in range(0, len(TRANSFORM_MODES), 2):
            cols = st.columns(2)
            for ci in range(2):
                gidx = row_start + ci
                if gidx >= len(TRANSFORM_MODES): break
                icon_t, label_t, desc_t, _ = TRANSFORM_MODES[gidx]
                with cols[ci]:
                    is_sel = (gidx == sel_tr)
                    sel_cls = "sel" if is_sel else ""
                    st.markdown(f'<div class="nx-mode-card {sel_cls}"><div class="ic">{icon_t}</div><span class="nx-mode-label">{label_t}</span><span class="nx-mode-desc">{desc_t}</span></div>', unsafe_allow_html=True)
                    if st.button("✓" if is_sel else "Select", key=f"tr_m_{gidx}", use_container_width=True,
                                 type="primary" if is_sel else "secondary"):
                        st.session_state["transform_idx"] = gidx; st.rerun()

        can_go = bool(transform_input.strip()) and sel_tr is not None
        if st.button("🔄  Transform Now", key="tr_go_btn", use_container_width=True, type="primary", disabled=not can_go):
            if not api_key:
                st.error("API Key nahi hai.")
            elif not check_rate_limit():
                st.error("Rate limit hit.")
            else:
                safe, cat = is_safe(transform_input)
                if not safe:
                    show_block_error(cat)
                else:
                    ph = st.empty()
                    with ph.container(): thinking_spinner()
                    result = run_transform(transform_input, sel_tr, api_key, st.session_state.model_tier)
                    ph.empty()
                    st.session_state.query_count += 1
                    if result.startswith("⚠"):
                        st.error(result)
                    else:
                        icon_t, label_t, _, _ = TRANSFORM_MODES[sel_tr]
                        st.toast(f"✅ Transformed to {label_t}!", icon="🔄")
                        if not st.session_state.incognito:
                            st.session_state.messages.append({"role":"user","content":f"[Transform → {label_t}]: {transform_input[:60]}…"})
                            st.session_state.messages.append({"role":"assistant","content":result})
                            _save_session()
                        st.markdown(f'<div class="nx-result-hdr"><div class="nx-result-title">{icon_t} {label_t}</div><div class="nx-result-badge">Transformed</div></div>', unsafe_allow_html=True)
                        st.markdown('<div class="nx-result-body">', unsafe_allow_html=True)
                        st.markdown(result)
                        st.markdown('</div>', unsafe_allow_html=True)
                        d1,d2 = st.columns(2)
                        with d1: st.code(result, language=None)
                        with d2: st.download_button("↓ Download", data=result, file_name=f"nexus_transform.txt", mime="text/plain", use_container_width=True)

    # ── EXPLORE ──────────────────────────────────────────────────
    elif tool == "explore":
        t = T
        features = [
            ("🧠","Neural Chat",      "Multi-turn AI with 5 personas + full context"),
            ("📄","Document AI",      "PDF · DOCX · TXT · CSV — 8 analysis modes"),
            ("▶️", "YouTube IQ",       "Transcripts · Insights · Chapters · Quiz"),
            ("🖼️","Image Vision",     "LLaMA 3.2 Vision — 6 analysis modes"),
            ("🎙️","Voice Commands",   "Whisper Large v3 transcription + AI response"),
            ("🔄","Text Transform",   "8 transforms — threads, emails, summaries"),
        ]
        for icon_f, name_f, desc_f in features:
            st.markdown(f"""
            <div style="display:flex;gap:14px;padding:12px 0;border-bottom:1px solid {t['border']};">
                <span style="font-size:22px;flex-shrink:0;">{icon_f}</span>
                <div>
                    <div style="font-size:13px;font-weight:700;color:{t['tx']};font-family:'Plus Jakarta Sans',sans-serif;">{name_f}</div>
                    <div style="font-size:12px;color:{t['tx2']}">{desc_f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:20px;background:{t['s1']};border:1px solid {t['border']};border-radius:12px;padding:16px 20px;">
            <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:{t['accent']};margin-bottom:12px;">System Stats</div>
            <div style="font-size:12px;color:{t['tx2']};line-height:2.3;">
                Uptime SLA &nbsp;·&nbsp; 99.2%<br>
                Context Window &nbsp;·&nbsp; 128k tokens<br>
                Fallback Chain &nbsp;·&nbsp; 4 models<br>
                Safety Layers &nbsp;·&nbsp; 3 (pre-filter + LLM + post-check)<br>
                Free Messages &nbsp;·&nbsp; {FREE_MSG_LIMIT} per session
            </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  BOTTOM ACTION BAR
# ════════════════════════════════════════════════════════════════
def render_action_bar(api_key):
    t = T
    c_plus, c_mid, c_mic = st.columns([1.2, 6, 1.2])
    with c_plus:
        plus_label = "✕  Close" if st.session_state.show_tools else "+  Tools"
        if st.button(plus_label, key="toggle_tools_btn", use_container_width=True):
            st.session_state.show_tools = not st.session_state.show_tools
            st.rerun()
    with c_mid:
        if st.session_state.active_tool:
            hints = {
                "document":  "Document loaded — ask questions below…",
                "youtube":   "YouTube processed — ask about the video…",
                "image":     "Image ready — ask about it below…",
                "voice":     "Voice mode active — or type your message…",
                "transform": "Transform done — type to continue chatting…",
                "explore":   "Exploring NEXUS — or just chat below…",
            }
            st.markdown(f'<div style="text-align:center;font-size:11px;color:{t["tx2"]};padding:8px 0;font-family:Plus Jakarta Sans,sans-serif;font-weight:600;letter-spacing:.05em;">Active: {st.session_state.active_tool.upper()} &nbsp;·&nbsp; {hints.get(st.session_state.active_tool,"")}</div>', unsafe_allow_html=True)
    with c_mic:
        if st.button("🎙", key="quick_mic_btn", use_container_width=True):
            st.session_state.active_tool = "voice"
            st.session_state.show_tools  = False
            st.rerun()

# ════════════════════════════════════════════════════════════════
#  FREE COUNTER BADGE
# ════════════════════════════════════════════════════════════════
def render_counter():
    remaining = max(0, FREE_MSG_LIMIT - st.session_state.query_count)
    color = T["accent"] if remaining > 5 else T["danger"]
    st.markdown(f'<div class="nx-counter" style="color:{color};">{remaining} msgs left</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  MAIN APP
# ════════════════════════════════════════════════════════════════
def main():
    render_sidebar()
    render_counter()

    api_key = get_api_key()

    # Limit check
    if st.session_state.query_count >= FREE_MSG_LIMIT:
        st.session_state.locked = True
    if st.session_state.locked:
        render_limit_wall()
        return

    # Welcome screen
    if not st.session_state.messages:
        render_welcome()

    # Chat history
    for msg in st.session_state.messages:
        role    = msg["role"]
        content = msg["content"]
        if role == "user":
            with st.chat_message("user"):
                st.markdown(content)
        elif role == "assistant":
            with st.chat_message("assistant", avatar="◈"):
                st.markdown(content)

    # Tool popup (above input bar)
    render_tool_popup()

    # Tool panel
    render_tool_panel(api_key)

    # Action bar (+ mic)
    render_action_bar(api_key)

    # ── CHAT INPUT ──────────────────────────────────────────────
    hint = "Message NEXUS…"
    if st.session_state.active_tool:
        hints_map = {
            "document":  "Ask about your document…",
            "youtube":   "Ask about the YouTube video…",
            "image":     "Ask about the image…",
            "voice":     "Type your question or use mic…",
            "transform": "Continue the conversation…",
            "explore":   "What would you like to explore?",
        }
        hint = hints_map.get(st.session_state.active_tool, hint)

    prompt = st.chat_input(hint)

    if prompt:
        # Guard — limit
        if st.session_state.query_count >= FREE_MSG_LIMIT:
            st.session_state.locked = True; st.rerun()

        # Guard — rate limit
        if not check_rate_limit():
            st.warning("Rate limit hit. Thodi der baad try karo."); return

        # Guard — safety
        safe, cat = is_safe(prompt)
        if not safe:
            show_block_error(cat); return

        # Append user message
        st.session_state.messages.append({"role":"user","content":prompt})
        st.session_state.query_count += 1

        # Build context
        ai_msgs = [
            {"role":m["role"],"content":m["content"]}
            for m in st.session_state.messages
            if m["role"] in ("user","assistant")
        ]
        # Prepend tool context if exists
        if st.session_state.tool_result:
            ai_msgs = [
                {"role":"system","content":f"Context from loaded tool:\n{st.session_state.tool_result}"}
            ] + ai_msgs

        # AI response
        with st.chat_message("assistant", avatar="◈"):
            ph = st.empty()
            with ph.container(): thinking_spinner()
            reply = neural_chat_response(ai_msgs, api_key,
                                         st.session_state.temperature,
                                         st.session_state.model_tier,
                                         st.session_state.persona)
            ph.empty()
            st.markdown(reply)

        st.session_state.messages.append({"role":"assistant","content":reply})
        if not st.session_state.incognito:
            _save_session()

        st.session_state.input_counter += 1
        st.rerun()


# ════════════════════════════════════════════════════════════════
#  ENTRY
# ════════════════════════════════════════════════════════════════
main()
