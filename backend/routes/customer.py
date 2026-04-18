from fastapi import APIRouter
from pydantic import BaseModel
from backend.models.chatbot_model import Chatbot

router = APIRouter()
# This initializes the bot ONE TIME when you start the server
bot = Chatbot()

class Query(BaseModel):
    customer_id: str
    message: str

@router.post("/query")
async def chat(query: Query):
    response = bot.respond(query.message)
    return {"response": response}