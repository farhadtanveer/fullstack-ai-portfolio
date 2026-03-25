from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

class Todo_request(BaseModel):
    title: str
    description: str
    completed: bool = False

