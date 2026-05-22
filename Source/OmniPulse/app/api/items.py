from fastapi import APIRouter
from app.schemas.item import ItemCreate

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/")
def create_item(item: ItemCreate):
    return {"message": "Item created", "item": item}

@router.get("/")
def list_items():
    return [
        {"id": 1, "title": "Sci-Fi Movie"},
        {"id": 2, "title": "AI Book"}
    ]