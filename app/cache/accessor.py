import redis
from config import REDIS_DB, REDIS_HOST, REDIS_PORT

def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB
    )

