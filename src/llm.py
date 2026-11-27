import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def api_key():
    key = os.getenv("GROQ_CLOUD_API_KEY")
    if key:
        return key
    try:
        import streamlit as st

        return st.secrets.get("GROQ_CLOUD_API_KEY")
    except Exception:
        return None


@lru_cache(maxsize=8)
def get_llm(key, model, temperature=0.7):
    return ChatGroq(
        api_key=key,
        model=model,
        temperature=temperature,
        max_tokens=1200,
        reasoning_effort="low",
        reasoning_format="hidden",
    )
