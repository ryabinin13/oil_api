from typing import Annotated, List
from fastapi import APIRouter, Depends
from app.depends import get_service
from app.service import Service
from app.schemas import SpimexTradingSchema
from datetime import date


oil_router = APIRouter(tags=["Oil"])

@oil_router.get("/dates")
async def get_last_trading_dates(
        service: Annotated[Service, Depends(get_service)],
        limit: int = 10
    ) -> List[date]:
    
    data = await service.get_last_trading_dates(limit)
    return data


@oil_router.get("/dynamics")
async def get_dynamics(
        left, 
        right, 
        service: Annotated[Service, Depends(get_service)]
    ) -> List[SpimexTradingSchema]:
    
    data = await service.get_dynamics(left, right)
    return data


@oil_router.get("/results")
async def get_trading_results(
        service: Annotated[Service, Depends(get_service)],
        limit: int = 10
    ) -> List[SpimexTradingSchema]:

    data = await service.get_trading_results(limit)
    return data


