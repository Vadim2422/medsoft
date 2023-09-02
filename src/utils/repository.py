from abc import ABC, abstractmethod

from sqlalchemy import select, delete, BinaryExpression
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker


class AbstractRepository(ABC):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def create(self, model):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, **filters):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, where: BinaryExpression = None, filters: dict = None, orders: tuple = None):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **filters):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_one(self, **filters):
        stmt = select(self.model).filter_by(**filters)
        res = await self.session.scalar(stmt)
        if res:
            return res.to_model()

    async def create(self, model_db):
        self.session.add(model_db)

    async def delete(self, **filters):
        stmt = delete(self.model).filter_by(**filters)
        await self.session.execute(stmt)

    async def find_all(self, where: BinaryExpression = None, filters: dict = None, orders: tuple = None):
        stmt = select(self.model)
        if where is not None:
            stmt = stmt.where(where)
        if filters:
            stmt = stmt.filter_by(**filters)
        if orders:
            stmt = stmt.order_by(*orders)
        res = [row for row in (await self.session.scalars(stmt)).unique()]
        return res
