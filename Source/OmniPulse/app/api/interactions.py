from fastapi import APIRouter

router = APIRouter(prefix="/interactions", tags=["Interactions"])

@router.post("/")
def record_interaction():
    return {"message": "Interaction recorded"}