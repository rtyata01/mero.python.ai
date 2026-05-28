import pandas as pd

from pathlib import Path
from app.database import SessionLocal
from app.models.item import Item
from app.ml.embeddings import generate_embedding

def import_movies_embeddings():
    db = SessionLocal()
    existing_count = db.query(Item).count()

    if existing_count > 0:
        return {
            "message": "Movies already imported",
            "count": existing_count
        }
    
    imported_count = 0

    # Read CSV
    BASE_DIR = Path(__file__).resolve().parent.parent
    csv_path = BASE_DIR / "data" / "movies.csv"
    df = pd.read_csv(csv_path)

    # DB session
    db = SessionLocal()

    for _, row in df.iterrows():

        # Create semantic embedding text
        embedding_text = f"""
        Title: {row['Title']}
        Type: {row['Type']}
        Category: {row['Category']}
        Description: {row['Description']}
        """

        # Generate embedding
        embedding = generate_embedding(embedding_text)

        # Create DB object
        movie = Item(
            title=row["Title"],
            type=row["Type"],
            category=row["Category"],
            genre=row["Genre"],
            description=row["Description"],
            created_date=row["Createddate"],
            ranking_score=float(row["RankingScore"]),
            popularity_score=float(row["PopularityScore"]),
            embedding=embedding.tolist()
        )

        db.add(movie)

        imported_count += 1

    # Commit once
    db.commit()

    return{
        "message": "Movies imported successfully",
        "count": imported_count
    }