from fastapi import FastAPI
from app.api import auth, items, recommendations, interactions

app = FastAPI(title="Recommendation System API")

app.include_router(auth.router)
app.include_router(items.router)
app.include_router(recommendations.router)
app.include_router(interactions.router)

@app.get("/")
def root():
    return {"message": "Recommendation API Running"}