"""
Model Service — loads the trained model ONCE at startup.

Key pattern: AI inference logic lives HERE, not in the router.
The router just calls this service. This separation makes
the code testable and clean.
"""
import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent.parent / "model" / "sentiment_model.joblib"

# Load model once when the app starts (not on every request)
_model = None


def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. "
                "Run the notebook first: notebooks/train_model.ipynb"
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_sentiment(text: str) -> dict:
    """
    Run inference on a single text input.
    Returns label ('positive' / 'negative') and confidence score.
    """
    model = get_model()
    prediction = model.predict([text])[0]
    probability = model.predict_proba([text])[0].max()

    return {
        "text": text,
        "sentiment": prediction,
        "confidence": round(float(probability), 4),
    }
