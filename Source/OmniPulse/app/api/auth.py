from fastapi import APIRouter
from app.schemas.user import UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate):
    return {"message": "User registered", "email": user.email}

@router.post("/login")
def login():
    return {"access_token": "sample-jwt-token"}