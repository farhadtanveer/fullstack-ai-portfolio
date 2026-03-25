from fastapi import APIRouter, Response, status, Query, Body, Path
from utils.dummy import Order_by
from .schemas import Todo_request, Todo


router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)

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
async def new_todo(
    todo: Todo_request = Body(...,description="The todo item to create"),
    id: int = Path(description="The ID of the todo item")):
    return {
        "id": id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed
    }
