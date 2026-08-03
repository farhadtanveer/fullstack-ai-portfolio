from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, timezone, datetime
from typing import Optional
from jose import JWTError, jwt

oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/token")

SECRET_KEY = "ffe9fdf49426ec409ef59500975cb8b718164a9d2b55e90c078b46279ee3d3ca"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt