from contextlib import asynccontextmanager
import datetime
from fastapi import FastAPI
# import redis
from app.routers import oil_router
import asyncio
import aioredis
from config import REDIS_DB, REDIS_HOST, REDIS_PORT


@asynccontextmanager
async def lifespan(app: FastAPI):
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    redis_client = aioredis.from_url(REDIS_URL)

    async def clear_redis_cache():
        await redis_client.flushdb()


    async def schedule_cache_clear():
        while True:
            now = datetime.datetime.now()
            
            target_time = now.replace(hour=14, minute=11, second=0, microsecond=0)

            if now >= target_time:
                await clear_redis_cache()
                sleep_time = datetime.timedelta(days=1) - (now - target_time)
            else:
                sleep_time = target_time - now

            await asyncio.sleep(sleep_time.total_seconds())

    asyncio.create_task(schedule_cache_clear())

    yield  

    await redis_client.close()