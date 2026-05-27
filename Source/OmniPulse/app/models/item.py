from sqlalchemy import Column, Integer, String, Float, Date
from pgvector.sqlalchemy import Vector
from app.database import Base

class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(String)
    category = Column(String)
    genre = Column(String)
    description = Column(String)
    created_date = Column(Date)
    ranking_score = Column(Float)
    popularity_score = Column(Float)
    embedding = Column(Vector(384))