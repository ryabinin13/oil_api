from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import SpimexTradingResults

class SpimexTradingResultRepository():

    def __init__(self, async_session: Session):
        self.session = async_session

    async def get_last_trading_dates(self, limit: int):
        async with self.session as session:
            
            query = (
                select(SpimexTradingResults.date)
                .distinct()
                .order_by(SpimexTradingResults.date.desc())
                .limit(limit)
            )

            res = await session.execute(query)

            dates = res.scalars().all()

            return dates
        

    async def get_dynamics(self, left, right):
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

            return res.scalars().all()
    
    
    async def get_trading_results(self, limit: int):
        async with self.session as session:
            query = (
                select(SpimexTradingResults)
                .order_by(SpimexTradingResults.oil_id, SpimexTradingResults.delivery_type_id, SpimexTradingResults.delivery_basis_id)
                .limit(limit)
            )

            res = await session.execute(query)

            return res.scalars().all()