from fastapi import APIRouter, Depends
from .schemas import User
from database import get_db
from sqlalchemy.orm import Session
from user.models import User as UserModel
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get("/")
async def get_users():
    return {"message": "welcome to the user endpoint!"}

@router.post("/new_user", response_model=User)
async def create_user(request: User, db:Session = Depends(get_db)):
    new_user = UserModel(username = request.username, email = request.email, password = password_hash.hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/all_users", response_model=list[User])
async def get_all_users(db:Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users