from fastapi import FastAPI
from typing import Optional
from enum import Enum

# cors
from fastapi.middleware.cors import CORSMiddleware

class Order_by(str, Enum):
    asc = "asc"
    desc = "desc"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

dummy_todos = [
    {"id": 1, "title": "Buy groceries", "completed": False},
    {"id": 2, "title": "Walk the dog", "completed": True},
    {"id": 3, "title": "Read a book", "completed": False},
    {"id": 4, "title": "Write code", "completed": True},
    {"id": 5, "title": "Cook dinner", "completed": False},
    {"id": 6, "title": "Exercise", "completed": True},
    {"id": 7, "title": "Call a friend", "completed": False},
    {"id": 8, "title": "Plan a trip", "completed": True},
    {"id": 9, "title": "Clean the house", "completed": False},
    {"id": 10, "title": "Pay bills", "completed": True},
]

@app.get("/")
def root():
    return {"message": "Hello from the server!"}

@app.get("/items/all")
async def items(order: Order_by = None):
    return {"items": "all the items", 'order': order}

@app.get("/items/{id}")
async def item(id: int):
    return {"item": f'the id of the items is {id}'}

