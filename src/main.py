import re
from pathlib import Path

import streamlit as st

import examples
from config import LANGUAGES, LENGTHS, MODELS, TONES
from generator import stream_post
from llm import api_key

st.set_page_config(page_title="Postcraft · LinkedIn Post Generator", page_icon="✦", layout="wide")
st.markdown(f"<style>{(Path(__file__).parent / 'styles.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

ss = st.session_state
ss.setdefault("history", [])
ss.setdefault("pending", None)


def label(text):
    st.markdown(f"<p class='label'>{text}</p>", unsafe_allow_html=True)


st.markdown("<div class='brand'><b>✦ Postcraft</b><span>LinkedIn posts that sound like you</span></div>", unsafe_allow_html=True)

key = api_key() or ss.get("groq_key")
left, right = st.columns([5, 7], gap="large")

with left:
    label("Brief")
    if not key and (entered := st.text_input("Groq API key", type="password", help="Free at console.groq.com. Kept for this session only.")):
        ss.groq_key = entered
        st.rerun()
    topic = st.selectbox("Topic", examples.tags(), accept_new_options=True, placeholder="Pick or type a topic")
    length = st.segmented_control("Length", list(LENGTHS), default="Medium")
    language = st.segmented_control("Language", list(LANGUAGES), default="English")
    tone = st.selectbox("Tone", TONES)
    context = st.text_area("Key points", placeholder="Optional: a story, a stat, a takeaway…", height=110)
    with st.expander("Advanced"):
        model = st.selectbox("Model", list(MODELS))
        temperature = st.slider("Creativity", 0.0, 1.0, 0.7, 0.05)
        a, b = st.columns(2)
        hashtags = a.toggle("Hashtags", True)
        emojis = b.toggle("Emojis", False)
    if st.button("Generate post", type="primary", width="stretch", disabled=not (key and topic)):
        ss.pending = {
            "model": MODELS[model],
            "temperature": temperature,
            "params": {
                "topic": topic,
                "length": length or "Medium",
                "language": language or "English",
                "tone": tone,
                "context": context,
                "hashtags": hashtags,
                "emojis": emojis,
            },
        }

with right:
    label("Draft")
    if ss.pending:
        job = ss.pending
        ss.pending = None
        try:
            with st.container(border=True):
                text = st.write_stream(stream_post(key, job["model"], job["temperature"], **job["params"]))
            ss.history.insert(0, {"text": re.sub(r"\n{3,}", "\n\n", text).strip(), **job["params"]})
            ss.last = job
            st.rerun()
        except Exception as e:
            st.error(f"Generation failed: {e}")
    elif ss.history:
        st.code(ss.history[0]["text"], language=None, wrap_lines=True)
    else:
        st.markdown("<div class='empty'>Your draft will appear here.</div>", unsafe_allow_html=True)
