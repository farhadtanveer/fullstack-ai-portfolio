from ast import List

from fastapi import APIRouter, Depends, Response, status, Query, Body, Path
from database import get_db
from utils.dummy import Order_by
from .schemas import Todo_request, Todo
from .models import Todo as TodoModel
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)

@router.get("/", response_model=List[Todo], summary="Get all todos")
async def root(db: Session = Depends(get_db)):
    """
    - This endpoint returns a list of all todo items.
    - Each todo item includes an id, title, description, and completion status.
    - The response is a JSON array of todo items.
    """
    return db.query(TodoModel).order_by(TodoModel.id.desc()).all()

@router.get("/item/all")
async def all_items(order: Order_by = None):
    return {'items' : 'All items', 'order': order}

@router.get("/item/{id}")
async def item(id: int, response: Response):
    if id > 5:
        response.status_code = status.not_found
        return {"error": "id must be less than or equal to 5"}
    return {'item': f'Item with id {id}'}

@router.post('/new_todo/{id}', response_model = Todo)
async def create_todo(
    request: Todo_request,
    db: Session = Depends(get_db),
    ):

    new_todo = TodoModel(
        title=request.title,
        description=request.description,
        completed=request.completed
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo