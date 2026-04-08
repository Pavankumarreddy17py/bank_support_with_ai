# Simple chatbot model wrapper (stub)
# Integrate Hugging Face / local models here

from typing import List

class Chatbot:
    def __init__(self, model_name: str = "gpt2"):
        self.model_name = model_name
        # TODO: load tokenizer and model (transformers)

    def respond(self, prompt: str) -> str:
        # TODO: use model to generate responses
        return f"[placeholder response to] {prompt}"

    def batch_respond(self, prompts: List[str]) -> List[str]:
        return [self.respond(p) for p in prompts]
