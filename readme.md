# Postcraft

AI LinkedIn post generator. Pick a topic, length, language and tone; get a ready-to-post draft in seconds, styled after high-performing example posts.

## Features

- Streaming generation on Groq (GPT-OSS 120B / 20B)
- Few-shot style matching ranked by topic, language, length and engagement
- English, Hinglish and Bengali output
- Tone, key points, hashtags and emoji controls
- Character limit check, one-click copy, download, regenerate and session history

## Setup

```bash
python -m venv venv
venv/Scripts/activate        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env         # add GROQ_CLOUD_API_KEY
streamlit run src/main.py
```

No key? Paste one into the app; it is kept for the session only. On Streamlit Cloud, set `GROQ_CLOUD_API_KEY` in Secrets.

## Structure

```
src/
  main.py        UI
  generator.py   streaming generation
  prompts.py     system prompt and request builder
  examples.py    few-shot example selection
  llm.py         Groq client
  config.py      models, lengths, languages, tones
  preprocess.py  raw posts -> tagged dataset
data/            raw and processed example posts
```

## Refresh the dataset

Add posts to `data/raw-post.json`, then run `python src/preprocess.py`.
