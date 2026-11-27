import examples
from llm import get_llm
from prompts import SYSTEM, build


def stream_post(key, model, temperature, **params):
    shots = examples.pick(params["topic"], params["length"], params["language"])
    messages = [("system", SYSTEM), ("human", build(examples=shots, **params))]
    for chunk in get_llm(key, model, temperature).stream(messages):
        if chunk.content:
            yield chunk.content
