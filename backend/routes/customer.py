from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class CustomerQuery(BaseModel):
    customer_id: str
    message: str

@router.post("/query")
async def handle_query(payload: CustomerQuery):
    # Use chatbot model (stub) to respond
    from backend.utils.model_registry import get_chatbot

    bot = get_chatbot()
    response = bot.respond(payload.message)
    return {"customer_id": payload.customer_id, "response": response}
