from fastapi import FastAPI
from app.routers import items

app = FastAPI(
    title="FastAPI Basics",
    description="Project 01 — Learning FastAPI fundamentals: CRUD, Pydantic, routing.",
    version="0.1.0",
)

app.include_router(items.router, prefix="/items", tags=["items"])


@app.get("/")
def health_check():
    return {"status": "ok", "project": "01-fastapi-basics"}
