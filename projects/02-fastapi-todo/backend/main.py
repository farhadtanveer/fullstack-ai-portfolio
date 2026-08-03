from fastapi import FastAPI, Depends, HTTPException
from typing import Optional, List
from enum import Enum
from utils.dummy import dummy_todos
from todo.router import router as todo_router
from user.router import router as user_router
from auth.router import router as auth_router
from todo.schemas import Todo
from todo import models
from user import models
from database import engine, get_db
from todo.models import Todo as TodoModel
from sqlalchemy.orm import Session
from database import Base

# cors
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Include the todo router
# set prefix to /api so that all todo endpoints are prefixed with /api
app.include_router(todo_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

Base.metadata.create_all(bind=engine)