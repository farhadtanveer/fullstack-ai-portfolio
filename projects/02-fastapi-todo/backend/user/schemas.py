from pydantic import BaseModel, ConfigDict, Field, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(exclude=True, min_length=6, max_length=100)

    model_config = ConfigDict(
        from_attributes=True,
    )