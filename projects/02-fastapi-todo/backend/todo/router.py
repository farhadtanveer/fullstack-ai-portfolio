from ast import List
from fastapi import APIRouter, Depends, HTTPException, Response, status, Query, Body, Path
from database import get_db
from .schemas import Todo_request, Todo
from .models import Todo as TodoModel
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)

@router.get("/", response_model=List[Todo], summary="Get all todos")
async def root(
    # ekhane keno amra db inject korchi? karon amra database er sathe interact korte chai, tai amra get_db function ke dependency hishebe use korchi. get_db function ta ekta database session return kore, ja amader CRUD operations er jonno dorkar.
   db: Session = Depends(get_db)
   ):
    """
    - This endpoint returns a list of all todo items.
    - Each todo item includes an id, title, description, and completion status.
    - The response is a JSON array of todo items.
    """
    return db.query(TodoModel).order_by(TodoModel.id.desc()).all()

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


@router.put('/{id}/update_todo', response_model = Todo)
async def update_todo(
    id: int,
    request: Todo_request,
    db: Session = Depends(get_db)
):
    todo_model = db.query(TodoModel).filter(TodoModel.id == id).first()

    if not todo_model:
     raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = request.title
    todo_model.description = request.description
    todo_model.completed = request.completed

    db.commit()
    db.refresh(todo_model)

    return todo_model