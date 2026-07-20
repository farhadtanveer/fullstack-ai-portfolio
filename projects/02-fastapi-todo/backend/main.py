from fastapi import FastAPI, Depends, HTTPException
from typing import Optional, List
from enum import Enum
from utils.dummy import dummy_todos
from todo.router import router as todo_router
from todo.schemas import Todo
from todo import models
from database import engine, get_db
from todo.models import Todo as TodoModel
from sqlalchemy.orm import Session

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

# Include the todo router
# set prefix to /api so that all todo endpoints are prefixed with /api
app.include_router(todo_router, prefix="/api")

models.Base.metadata.create_all(bind=engine)

# from fastapi import FastAPI
# from typing import Optional, List
# from enum import Enum

# class Order_By(str, Enum):
#     asc = "asc"
#     desc = "desc"


# app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello, world!"}

# @app.get("/items")
# async def get_items():
#     return {"items": ["item1", "item2", "item3"]}

# @app.get("/items/all") 
# async def all_items(order: Order_By = None):
#     return {"items": ["item1", "item2", "item3", "item4"], 'order': order}

# @app.get("/items/{item_id}")
# async def get_item(item_id: int):
#     return {"item": f"Item {item_id}"}