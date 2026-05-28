from fastapi import APIRouter
from app.schemas.item import ItemCreate
from app.database import SessionLocal
from app.models.item import Item
from app.ml.movies_embeddings import import_movies_embeddings
from app.ml.embeddings import generate_embedding

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/")
def list_items(limit: int = 20, offset: int = 0):
    db = SessionLocal()

    if db.query(Item).count() == 0:
        import_movies_embeddings()

    items = (
        db.query(Item)
        .offset(offset)
        .limit(limit)
        .all()
    )

    results = []

    for item in items:

        results.append({
            "id": item.id,
            "title": item.title,
            "type": item.type,
            "category": item.category,
            "description": item.description
        })

    return {
        "count": len(results),
        "limit": limit,
        "offset": offset,
        "items": results
    }

@router.post("/import")
def import_movies():
    return import_movies_embeddings()

@router.post("/")
def create_item(item: ItemCreate):

    db = SessionLocal()

    # Create semantic embedding text
    embedding_text = f"""
    Title: {item.title}
    Type: {item.type}
    Category: {item.category}
    Description: {item.description}
    """

    embedding = generate_embedding(embedding_text)

    db_item = Item(
        title=item.title,
        type=item.type,
        category=item.category,
        genre=item.genre,
        description=item.description,
        created_date=item.created_date,
        ranking_score=item.ranking_score,
        popularity_score=item.popularity_score,
        embedding=embedding.tolist()
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return {
        "message": "Item created",
        "item": {
            "id": db_item.id,
            "title": db_item.title,
            "type": db_item.type,
            "category": db_item.category,
            "description": db_item.description
        }
    }