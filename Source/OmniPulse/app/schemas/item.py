from pydantic import BaseModel, Field
from datetime import date

class ItemCreate(BaseModel):

    title: str = Field(min_length=1)
    type: str
    category: str
    genre: str
    description: str = Field(min_length=10)
    created_date: date
    ranking_score: float = Field(ge=0, le=10)
    popularity_score: float = Field(ge=0)