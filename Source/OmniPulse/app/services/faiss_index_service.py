import faiss
import numpy as np
from typing import Optional

from app.models.item import Item


class FaissIndexService:

    _index = None
    _items = []

    @classmethod
    def build_index(
        cls,
        items: list[Item]
    ):

        cls._items = items

        embeddings = np.array(
            [item.embedding for item in items],
            dtype=np.float32
        )

        faiss.normalize_L2(
            embeddings
        )

        n = embeddings.shape[0]
        dimension = embeddings.shape[1]

        cls._index = faiss.IndexFlatIP(dimension)
        cls._index.add(n, embeddings)

    @classmethod
    def search(
        cls,
        embedding,
        k=10
    ):
        
        if cls._index is None:
            raise RuntimeError(
                "FAISS index not initialized. Call build_index() first."
            )

        query = np.array(
            [embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(
            query
        )

        return cls._index.search(query, k)  # type: ignore

    @classmethod
    def get_item(
        cls,
        index: int
    ) -> Optional[Item]:

        if index < 0 or index >= len(cls._items):
            return None

        return cls._items[index]