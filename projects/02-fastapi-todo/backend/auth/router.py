from fastapi import APIRouter, Depends

router = APIRouter (
    prefix="/auth",
    tags=["auth"],
)
