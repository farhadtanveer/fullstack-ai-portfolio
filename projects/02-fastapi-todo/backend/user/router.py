from fastapi import APIRouter, Depends, HTTPException
from .schemas import User
from database import get_db
from sqlalchemy.orm import Session
from user.models import User as UserModel
from pwdlib import PasswordHash
from auth.oauth import oauth2_scheme, create_access_token
from jose import jwt, JWTError
from auth.oauth import SECRET_KEY as secret_key

password_hash = PasswordHash.recommended()

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(UserModel).filter(UserModel.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

@router.get("/me", response_model=User)
async def read_current_user(current_user: UserModel = Depends(get_current_user)):
    return current_user

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