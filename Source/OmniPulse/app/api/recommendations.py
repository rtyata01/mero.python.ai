from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.item import Item
from app.services.recommendation_service import RecommendationService

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)

service = RecommendationService()

@router.get("/")
def get_recommendations():

    db = SessionLocal()

    items = db.query(Item).all()

    return service.get_top_recommendations(items)


@router.get("/similar/{item_id}")
def similar_items(item_id: int):

    db = SessionLocal()

    current_item = db.query(Item).filter(
        Item.id == item_id
    ).first()

    if not current_item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    other_items = db.query(Item).filter(
        Item.id != item_id
    ).all()

    recommendations = service.get_similar_items(
        current_item,
        other_items
    )

    return {
        "item_id": item_id,
        "title": current_item.title,
        "recommendations": recommendations
    }