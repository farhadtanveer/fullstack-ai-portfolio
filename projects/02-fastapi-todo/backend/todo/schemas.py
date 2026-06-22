from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None  # Now it's optional and defaults to None
    completed: bool = False

class Todo_request(BaseModel):
    title: str
    description: Optional[str] = None  # Match it here as well
    completed: bool = False