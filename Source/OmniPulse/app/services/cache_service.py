import redis
import json

redis_client = redis.Redis(host="redis", port=6379)

def cache_data(key, data):
    redis_client.setex(key, 3600, json.dumps(data))