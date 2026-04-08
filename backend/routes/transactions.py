from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class TransactionRequest(BaseModel):
    account_id: str
    start_date: str
    end_date: str

@router.post("/history")
async def get_history(payload: TransactionRequest):
    # TODO: implement transaction lookup/pagination
    return {"account_id": payload.account_id, "transactions": []}
