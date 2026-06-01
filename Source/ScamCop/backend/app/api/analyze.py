from fastapi import APIRouter
from app.models.schemas import AnalyzeRequest
from app.services.analyzer import analyze_message

router=APIRouter()

@router.post('/analyze')
async def analyze(request: AnalyzeRequest):
    return analyze_message(request.message)
