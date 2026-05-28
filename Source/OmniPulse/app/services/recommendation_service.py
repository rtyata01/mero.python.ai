import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from app.models.item import Item
from app.services.cache_service import CacheService

class RecommendationService:
    def get_top_recommendations(self, items: list[Item], limit: int = 10):
        ranked_items = sorted(
            items,
            key=lambda x: (
                x.ranking_score,
                x.popularity_score
            ),
            reverse=True
        )

        results = []

        for item in ranked_items[:limit]:

            results.append({
                "id": item.id,
                "title": item.title,
                "type": item.type,
                "category": item.category,
                "ranking_score": item.ranking_score,
                "popularity_score": item.popularity_score
            })

        return results

    def get_similar_items(self, current_item: Item, items: list[Item], limit: int = 5):

        cache_key = f"similar_items:{current_item.id}"
        cached_response = CacheService.get_cache(cache_key)
        if cached_response:
            print("Returning from Redis cache")
            return cached_response

        current_embedding = np.array(
            current_item.embedding
        ).reshape(1, -1)

        similarities = []

        for item in items:

            item_embedding = np.array(
                item.embedding
            ).reshape(1, -1)

            score = cosine_similarity(
                current_embedding,
                item_embedding
            )[0][0]

            similarities.append({
                "id": item.id,
                "title": item.title,
                "type": item.type,
                "category": item.category,
                "similarity_score": float(score)
            })

        similarities = sorted(
            similarities,
            key=lambda x: x["similarity_score"],
            reverse=True
        )

        response = similarities[:limit]
        CacheService.set_cache(
            cache_key,
            response
        )

        print("Stored in Redis cache")
        return response