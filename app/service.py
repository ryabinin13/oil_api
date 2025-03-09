import json
from app.SPRRepository import SpimexTradingResultRepository
from app.cache_repository import CacheRepository
from app.db.models import SpimexTradingResults
from sqlalchemy import select, between
from sqlalchemy.orm import Session
from datetime import date, datetime
from redis import Redis

from app.schemas import SpimexTradingSchema



class Service:

    def __init__(self, spr_repository: SpimexTradingResultRepository, cache_repository: CacheRepository):
        self.spr_repository = spr_repository
        self.cache_repository = cache_repository


    async def get_last_trading_dates(self, limit: int):

        cached_data = self.cache_repository.get_data(key=f'last_trading_dates:{limit}')
        if cached_data:
            return [date.fromisoformat(d) for d in json.loads(cached_data.decode('utf-8'))]
        
        dates = await self.spr_repository.get_last_trading_dates(limit)

        self.cache_repository.set_date(dates, key=f'last_trading_dates:{limit}')

        return dates

            


    async def get_dynamics(self, left, right):
        
        cached_data = self.cache_repository.get_data(key=f'get_dynamics:{left}-{right}')
        if cached_data:
            cached_data = json.loads(cached_data.decode('utf-8'))
            data = [SpimexTradingSchema.model_validate(с) for с in cached_data]
            return data
    
        all_data = await self.spr_repository.get_dynamics(left=left, right=right)
            
        self.cache_repository.set_spr(all_data=all_data, key=f'get_dynamics:{left}-{right}')

        data = [SpimexTradingSchema.model_validate(с.__dict__) for с in all_data]

        return data
        

    async def get_trading_results(self, limit: int):

        cached_data = self.cache_repository.get_data(key=f"get_trading_results:{limit}")
        if cached_data:
            cached_data = json.loads(cached_data.decode('utf-8'))
            data = [SpimexTradingSchema.model_validate(с) for с in cached_data]
            return data
        
        
        all_data = await self.spr_repository.get_trading_results(limit=limit)
            
        self.cache_repository.set_spr(all_data=all_data, key=f"get_trading_results:{limit}")

        data = [SpimexTradingSchema.model_validate(с.__dict__) for с in all_data]

        return data

