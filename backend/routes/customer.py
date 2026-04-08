from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.models.chatbot_model import Chatbot

router = APIRouter()
# This creates the bot instance when the server starts
bot = Chatbot()

class CustomerQuery(BaseModel):
    customer_id: str
    message: str

@router.post("/query")
async def chat_with_support(query: CustomerQuery):
    try:
        # Call the respond function we defined above
        answer = bot.respond(query.message)
        return {"customer_id": query.customer_id, "response": answer}
    except Exception as e:
        print(f"Router Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")