from app.service import Service
from app.db.database import get_async_session
from app.cache.accessor import get_redis_connection
from app.SPRRepository import SpimexTradingResultRepository
from app.cache_repository import CacheRepository


def get_cache_repository() -> CacheRepository:
    redis_connection = get_redis_connection()
    return CacheRepository(redis_connection=redis_connection)


def get_spr_repository() -> SpimexTradingResultRepository:
    async_session = get_async_session()
    return SpimexTradingResultRepository(async_session=async_session)


def get_service() -> Service:
    spr_repository = get_spr_repository()
    cache_repository = get_cache_repository()
    
    return Service(spr_repository, cache_repository)