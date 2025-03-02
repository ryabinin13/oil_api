from app.service import Service
from app.db.database import get_async_session
from app.cache.accessor import get_redis_connection


def get_service() -> Service:
    async_session = get_async_session()
    redis_connection = get_redis_connection()
    
    return Service(async_session, redis_connection)