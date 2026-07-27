from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

SECRET_KEY = "5821ad58a8fe27dff414d96c80a16b12ccf2b2270f3958280d51b47d05919136"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data: dict, expires_delta: timedelta = Optional[timedelta(minutes=15)]):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    enconded_JWT =  jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

    return enconded_JWT