from fastapi import FastAPI
from app.routers import predict

app = FastAPI(
    title="AI Sentiment API",
    description="Project 03 — Serve a trained ML model via a FastAPI /predict endpoint.",
    version="0.1.0",
)

app.include_router(predict.router, prefix="/predict", tags=["prediction"])


@app.get("/")
def health_check():
    return {"status": "ok", "project": "03-ai-sentiment"}
