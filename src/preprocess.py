import json
from pathlib import Path

from langchain_core.output_parsers import JsonOutputParser

from config import MODELS
from llm import api_key, get_llm

DATA = Path(__file__).resolve().parent.parent / "data"
parser = JsonOutputParser()

METADATA = """Extract metadata from this LinkedIn post. Return JSON only:
{{"line_count": int, "language": "English"|"Hinglish"|"Bengali", "tags": [max 2 title-case tags]}}

{post}"""

UNIFY = """Merge these tags into a short canonical set (e.g. "Jobseekers", "Job Hunting" -> "Job Search").
Return JSON only, mapping every original tag to its Title Case unified tag.

{tags}"""


def ask(llm, prompt):
    return parser.parse(llm.invoke(prompt).content)


def process(raw=DATA / "raw-post.json", out=DATA / "processed-post.json"):
    llm = get_llm(api_key(), next(iter(MODELS.values())), 0)
    posts = json.loads(Path(raw).read_text(encoding="utf-8"))
    posts = [p | ask(llm, METADATA.format(post=p["text"])) for p in posts]
    mapping = ask(llm, UNIFY.format(tags=", ".join({t for p in posts for t in p["tags"]})))
    for p in posts:
        p["tags"] = sorted({mapping.get(t, t) for t in p["tags"]})
    Path(out).write_text(json.dumps(posts, indent=4, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    process()
