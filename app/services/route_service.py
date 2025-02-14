from fastapi import HTTPException

from app.api.schemas.route_schema import RouteReturn
from app.utils.unitofwork import IUnitOfWork

class RouteService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_route(self, id: int):
        async with self.uow:
            route = await self.uow.users.find_one(id=id)
            route = RouteReturn()
            return route
        