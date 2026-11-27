from config import LANGUAGES, LENGTHS

SYSTEM = """You are an elite LinkedIn ghostwriter.
Return only the post text. No preamble, quotes, markdown or bold.
- Line 1: scroll-stopping hook, under 12 words.
- Short paragraphs, one idea each, blank line between.
- Concrete, specific, first person, human.
- Avoid: "in today's fast-paced world", "game-changer", "delve", "unlock", "leverage", "landscape".
- End with a sharp question or clear CTA.
- Examples show style only; never copy them."""


def build(topic, length, language, tone, context="", hashtags=True, emojis=False, examples=()):
    lines = [
        f"Topic: {topic}",
        f"Length: {LENGTHS[length]}",
        f"Language: {LANGUAGES[language]}",
        f"Tone: {tone}",
        f"Emojis: {'sparingly' if emojis else 'none'}",
        f"Hashtags: {'3-5 at the end' if hashtags else 'none'}",
    ]
    if context.strip():
        lines.append(f"Key points: {context.strip()}")
    lines += [f"\nExample {i}:\n{e}" for i, e in enumerate(examples, 1)]
    return "\n".join(lines)
