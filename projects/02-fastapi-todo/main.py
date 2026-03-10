from fastapi import FastAPI
from typing import Optional
from enum import Enum

class Order_by(str, Enum):
    asc = "asc"
    desc = "desc"

app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/items/all")
async def items(order: Order_by = None):
    return {"items": "all the items", 'order': order}

@app.get("/items/{id}")
async def item(id: int):
    return {"item": f'the id of the items is {id}'}

