from functools import lru_cache
from backend.models.chatbot_model import Chatbot
from backend.models.fraud_model import load_model


@lru_cache()
def get_chatbot():
    # set model_name via env/config in the future
    return Chatbot(model_name="gpt2")


@lru_cache()
def get_fraud_model():
    try:
        return load_model()
    except Exception:
        return None
