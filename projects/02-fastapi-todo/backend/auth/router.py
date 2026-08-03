from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
from sqlalchemy.orm import Session
from user.models import User as UserModel
from pwdlib import PasswordHash
from .oauth import create_access_token

password_hash = PasswordHash.recommended()

router = APIRouter (
    tags=["auth"],
)


@router.post("/token")
async def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == request.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not password_hash.verify(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(
        data = {"sub": user.username}
    )

    return {"access_token": access_token}