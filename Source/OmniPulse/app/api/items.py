from fastapi import APIRouter
from app.schemas.item import ItemCreate
from app.database import SessionLocal
from app.models.item import Item
from app.ml.import_movies import import_movies

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/")
def create_item(item: ItemCreate):
    return {"message": "Item created", "item": item}

@router.post("/import")
def import_movies_api():
    return import_movies()

@router.get("/")
def list_items():
    db = SessionLocal()

    if db.query(Item).count() == 0:
        import_movies()

    items = db.query(Item).all()
    results = []

    for item in items:

        results.append({
            "id": item.id,
            "title": item.title,
            "type": item.type,
            "category": item.category,
            "description": item.description
        })

    return results