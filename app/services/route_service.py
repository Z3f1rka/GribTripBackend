from fastapi import HTTPException

from app.api.schemas.route_schema import RouteReturn
from app.api.schemas.route_schema import RouteUpdateParameters
from app.utils.unitofwork import IUnitOfWork


class RouteService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_route_by_id(self, id: int, user_id: int):
        async with self.uow:
            route = await self.uow.routes.find_by_main_route_id_private(id)
            route = route[-1]
            if route.user_id == user_id:
                route = await self.uow.routes.find_by_main_route_id_private(id)
                return [RouteReturn.model_validate(i) for i in route]
            route = RouteReturn.model_validate(route)
            return route

    async def create_route(self, user_id: int, title: str):
        async with self.uow:
            await self.uow.routes.add_route(user_id=user_id, title=title)
            await self.uow.commit()

    async def update(self, route: RouteUpdateParameters, user_id: int):
        async with self.uow:
            db_route = await self.uow.routes.find_by_main_route_id_private(route.main_route_id)
            db_route = db_route[-1]
            if db_route.user_id == user_id:
                content_blocks = [i.model_dump() for i in route.content_blocks]
                await self.uow.routes.update(title=route.title, description=route.description, photo=route.photo,
                                             main_route_id=route.main_route_id,
                                             content_blocks=content_blocks)
                await self.uow.commit()
            else:
                raise HTTPException(403, "Пользователь не является владельцем маршрута")
