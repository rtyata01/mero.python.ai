import json

from pathlib import Path
from app.services.embeddings import embed
from app.services.vector_store import VectorStore

texts=[x['text'] for x in json.loads(Path('app/data/scam_examples.json').read_text())]
embeddings=[embed(t) for t in texts]

vector_store=VectorStore(len(embeddings[0]))
vector_store.add(texts,embeddings)

def retrieve_similar_scams(message:str):
    return vector_store.search(embed(message),k=3)
