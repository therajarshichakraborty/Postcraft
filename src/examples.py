import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "processed-post.json"


def bucket(lines):
    return "Short" if lines < 5 else "Medium" if lines <= 10 else "Long"


@lru_cache(maxsize=1)
def load():
    posts = json.loads(DATA.read_text(encoding="utf-8"))
    for p in posts:
        p["length"] = bucket(p["line_count"])
    return posts


def tags():
    return [t for t, _ in Counter(t for p in load() for t in p["tags"]).most_common()]


def pick(topic, length, language, k=2, max_chars=1200):
    matches = [p for p in load() if topic in p["tags"]]
    matches.sort(
        key=lambda p: (p["language"] == language, p["length"] == length, p.get("engagement") or 0),
        reverse=True,
    )
    return [p["text"][:max_chars] for p in matches[:k]]
