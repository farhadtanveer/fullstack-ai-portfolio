from pydantic import BaseModel, ConfigDict
from typing import Optional

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

class Todo_request(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool 

class Todo_title(BaseModel):
    id: int
    title: str

    # keno config_dict use korchi? karon amra chachhi je pydantic model ta database model er attribute theke data nibe. from_attributes = True mane hocche je pydantic model ta database model er attribute theke data nibe, na je json body theke.
    model_config = ConfigDict(
        from_attributes = True 
    )
