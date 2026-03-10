from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from app.services.model_service import predict_sentiment

router = APIRouter()


class PredictRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text cannot be empty")
        if len(v) > 1000:
            raise ValueError("text must be under 1000 characters")
        return v.strip()


class PredictResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float


@router.post("/", response_model=PredictResponse)
def predict(request: PredictRequest):
    """
    Predict sentiment of a given text.

    Returns: label (positive/negative) and confidence score.
    """
    try:
        result = predict_sentiment(request.text)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
