from abc import ABC
from abc import abstractmethod

from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self):
        raise NotImplementedError

    @abstractmethod
    async def del_one(self):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self):
        res = await self.session.execute(select(self.model))
        return res.scalars().all()

    async def find_one(self, **filter_by):
        res = await self.session.execute(select(self.model).filter_by(**filter_by))
        res = res.scalar_one()
        return res

    async def find_all_by(self, **filter_by):
        res = await self.session.execute(select(self.model).filter_by(**filter_by))
        res = res.scalars().all()
        return res

    async def del_one(self, **filter_by):
        stmt = delete(self.model).where(self.model.id == filter_by["id"]).returning(self.model)
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        return res
