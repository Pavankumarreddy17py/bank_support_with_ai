from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class FraudRequest(BaseModel):
    transaction_id: str
    features: dict

@router.post("/predict")
async def predict_fraud(payload: FraudRequest):
    # Try to load the model from registry and return a prediction
    from backend.utils.model_registry import get_fraud_model
    from pandas import DataFrame

    model = get_fraud_model()
    features = payload.features
    if not model:
        return {"transaction_id": payload.transaction_id, "is_fraud": False, "score": None, "warning": "model not loaded"}

    df = DataFrame([features])
    preds, scores = model.predict(df), model.decision_function(df)
    # isolationforest: -1 anomaly (fraud), 1 normal
    is_fraud = bool((preds == -1).any())
    return {"transaction_id": payload.transaction_id, "is_fraud": is_fraud, "score": float(scores[0])}
