from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from user.models import User as UserModel
from pwdlib import PasswordHash
from .oauth import create_access_token

password_hash = PasswordHash.recommended()

router = APIRouter(tags=["auth"])


@router.post("/token")
def get_token(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(UserModel.username == request.username).first()

    if not user:
        raise HTTPException(status_code=402, detail="Incorrect username")

    if not password_hash.verify(request.password, user.password):
        raise HTTPException(status_code=402, detail="Incorrect password")
    
    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }