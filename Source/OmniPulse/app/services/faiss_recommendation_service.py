from app.models.item import Item
from app.services.cache_service import CacheService
from app.services.faiss_index_service import FaissIndexService


class FaissRecommendationService:

    def get_top_recommendations(
        self,
        items: list[Item],
        limit: int = 10
    ):
        ranked_items = sorted(
            items,
            key=lambda x: (
                x.ranking_score,
                x.popularity_score
            ),
            reverse=True
        )

        return [
            {
                "id": item.id,
                "title": item.title,
                "type": item.type,
                "category": item.category,
                "ranking_score": item.ranking_score,
                "popularity_score": item.popularity_score
            }
            for item in ranked_items[:limit]
        ]

    def get_similar_items(
        self,
        current_item: Item,
        limit: int = 5
    ):

        cache_key = f"similar_items:{current_item.id}"

        cached_response = CacheService.get_cache(
            cache_key
        )

        if cached_response:
            print("Returning from Redis cache")
            return cached_response

        # Search FAISS index
        scores, indices = FaissIndexService.search(
            embedding=current_item.embedding,
            k=limit + 1
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            item = FaissIndexService.get_item(int(idx))

            if item is None:
                continue

            # Exclude self
            if int(item.id) == int(current_item.id): # type: ignore
                continue

            results.append({
                "id": item.id,
                "title": item.title,
                "type": item.type,
                "category": item.category,
                "similarity_score": float(score)
            })

            if len(results) >= limit:
                break

        CacheService.set_cache(
            cache_key,
            results
        )

        print("Stored in Redis cache")

        return results