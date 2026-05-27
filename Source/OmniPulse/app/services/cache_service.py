import json
import redis

# Redis connection
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)


class CacheService:

    DEFAULT_TTL = 3600

    @staticmethod
    def set_cache(key: str, data, ttl: int = DEFAULT_TTL):
        redis_client.setex(
            key,
            ttl,
            json.dumps(data)
        )

    @staticmethod
    def get_cache(key: str):
        cached_data = redis_client.get(key)

        if not cached_data:
            return None

        return json.loads(str(cached_data))

    @staticmethod
    def delete_cache(key: str):
        redis_client.delete(key)