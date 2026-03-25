from fastapi import FastAPI
from typing import Optional, List
from enum import Enum
from utils.dummy import dummy_todos
from todo.router import router as todo_router
from todo.schemas import Todo

# cors
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(todo_router, prefix="/api")



@app.get("/", response_model=List[Todo], summary="Get all todos")
async def root():
    """
    - This endpoint returns a list of all todo items.
    - Each todo item includes an id, title, description, and completion status.
    - The response is a JSON array of todo items.
    """
    return dummy_todos


