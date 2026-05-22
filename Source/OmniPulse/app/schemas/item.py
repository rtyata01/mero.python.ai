from pydantic import BaseModel

class ItemCreate(BaseModel):
    title: str
    category: str
    description: str