from fastapi import FastAPI
from pydantic import BaseModel
from app.services.scam_detector import analyze_message

app = FastAPI(title="ScamShield AI")

class ScamRequest(BaseModel):
    message: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(req: ScamRequest):
    result = analyze_message(req.message)
    return result
