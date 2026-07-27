from ast import List
from fastapi import APIRouter, Depends, HTTPException, Response, status, Query, Body, Path
from database import get_db
from .schemas import Todo_request, Todo, Todo_title
from .models import Todo as TodoModel
from sqlalchemy.orm import Session
from typing import List
from auth.oauth import oauth2_scheme

# set prefix to /todo so that all todo endpoints are prefixed with /todo
# so that the full path to the endpoint is /api/todo/
router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)

@router.get("/", response_model=List[Todo_title], summary="Get all todos")
async def root(
    # ekhane keno amra db inject korchi? karon amra database er sathe interact korte chai, tai amra get_db function ke dependency hishebe use korchi. get_db function ta ekta database session return kore, ja amader CRUD operations er jonno dorkar.
   db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
   ):
    """
    - This endpoint returns a list of all todo items.
    - Each todo item includes an id, title, description, and completion status.
    - The response is a JSON array of todo items.
    """
    return db.query(TodoModel).order_by(TodoModel.id.desc()).all()

# Get a specific todo item by ID
@router.get("/{id}", response_model=Todo, summary="Get a todo by ID")
async def get_todo(id: int, db: Session = Depends(get_db)):
    """
    - This endpoint retrieves a specific todo item by its ID.
    - If the todo item is found, it returns the item as a JSON object.
    - If the todo item is not found, it raises a 404 HTTP exception.
    """
    todo_model = db.query(TodoModel).filter(TodoModel.id == id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_model

# Create a new todo item
@router.post('/new_todo', response_model = Todo)
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

# Update an existing todo item
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

@router.delete("/{id}/delete_todo", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo( id: int, db: Session = Depends(get_db)):
    todo_model = db.query(TodoModel).filter(TodoModel.id == id).delete()

    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)