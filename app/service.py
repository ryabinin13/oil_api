import json
from app.db.models import SpimexTradingResults
from sqlalchemy import select, between
from sqlalchemy.orm import Session
from datetime import date, datetime
from redis import Redis

from app.schemas import SpimexTradingSchema



class Service:

    def __init__(self, async_session: Session, redis_connection: Redis):
        self.session = async_session
        self.redis = redis_connection


    async def get_last_trading_dates(self, limit: int):

        cache_key = f"last_trading_dates:{limit}"
        cached_data = self.redis.get(cache_key)
        if cached_data:
            return [date.fromisoformat(d) for d in json.loads(cached_data.decode('utf-8'))]
        
        async with self.session as session:
            
            query = (
                select(SpimexTradingResults.date)
                .distinct()
                .order_by(SpimexTradingResults.date.desc())
                .limit(limit)
            )

            res = await session.execute(query)

            dates = res.scalars().all()

            self.redis.set(cache_key, json.dumps(dates, default=str))

            return dates


    async def get_dynamics(self, left, right):

        cache_key = f"last_trading_dates:{left}-{right}"
        cached_data = self.redis.get(cache_key)
        if cached_data:
            cached_data = json.loads(cached_data.decode('utf-8'))
            data = [SpimexTradingSchema.model_validate(с) for с in cached_data]
            return data
    

        async with self.session as session:

            left_date = datetime.strptime(left, "%Y-%m-%d").date()
            right_date = datetime.strptime(right, "%Y-%m-%d").date()

            query = (
                select(SpimexTradingResults)
                .where(SpimexTradingResults.date.between(left_date, right_date))
                .order_by(SpimexTradingResults.oil_id, 
                          SpimexTradingResults.delivery_type_id, 
                          SpimexTradingResults.delivery_basis_id,
                          )
            )

            res = await session.execute(query)

            all_data = res.scalars().all()
            
            data_to_serialize = [item.as_dict() for item in all_data]

            self.redis.set(cache_key, json.dumps(data_to_serialize, default=str))

            data = [SpimexTradingSchema.model_validate(с.__dict__) for с in all_data]

            return data
        

    async def get_trading_results(self, limit: int):

        cache_key = f"last_trading_dates:{limit}"
        cached_data = self.redis.get(cache_key)
        if cached_data:
            cached_data = json.loads(cached_data.decode('utf-8'))
            data = [SpimexTradingSchema.model_validate(с) for с in cached_data]
            return data
        
        async with self.session as session:
            query = (
                select(SpimexTradingResults)
                .order_by(SpimexTradingResults.oil_id, SpimexTradingResults.delivery_type_id, SpimexTradingResults.delivery_basis_id)
                .limit(limit)
            )

            res = await session.execute(query)

            all_data = res.scalars().all()
            
            data_to_serialize = [item.as_dict() for item in all_data]

            self.redis.set(cache_key, json.dumps(data_to_serialize, default=str))

            data = [SpimexTradingSchema.model_validate(с.__dict__) for с in all_data]

            return data

