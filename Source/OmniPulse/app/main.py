from fastapi import FastAPI
from app.api import auth, items, recommendations, interactions
from app.database import engine
from app.models.item import Base

from app.api import items
from app.api import recommendations

# -----------------------------------------
# CREATE TABLES
# -----------------------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------------------
# FASTAPI APP
# -----------------------------------------
app = FastAPI(title="Recommendation System API")


# -----------------------------------------
# ROUTERS
# -----------------------------------------
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(recommendations.router)
app.include_router(interactions.router)

@app.get("/")
def root():
    return {"message": "Recommendation API Running"}