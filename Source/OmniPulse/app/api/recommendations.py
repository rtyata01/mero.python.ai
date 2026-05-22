from fastapi import APIRouter
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

service = RecommendationService()

@router.get("/")
def get_recommendations():
    return service.recommend()

@router.get("/similar/{item_id}")
def similar_items(item_id: int):
    return {
        "item_id": item_id,
        "similar_items": [2, 5, 7]
    }