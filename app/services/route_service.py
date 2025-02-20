from fastapi import HTTPException

from app.api.schemas.route_schema import AllRouteReturn
from app.api.schemas.route_schema import RouteReturn
from app.api.schemas.route_schema import RouteReturnNoContentBlocks
from app.api.schemas.route_schema import RouteUpdateParameters
from app.utils.unitofwork import IUnitOfWork


class RouteService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_private_route_by_id(self, id: int, user_id: int):
        async with self.uow:
            routes = await self.uow.routes.find_by_main_route_id_private(id)
            if routes:
                route = routes[-1]
                if route.user_id == user_id:
                    return [RouteReturn.model_validate(i) for i in routes]
                else:
                    raise HTTPException(403, "Пользователь не является владельцем маршрута")
            return []

    async def get_public_route_by_id(self, id: int):
        async with self.uow:
            route = await self.uow.routes.find_by_main_route_id_public(id)
            if not route:
                raise HTTPException(404, "Публичных маршрутов с этим id не существует")
            route = RouteReturn.model_validate(route)
            return route

    async def create_route(self, user_id: int, title: str):
        async with self.uow:
            await self.uow.routes.add_route(user_id=user_id, title=title)
            await self.uow.commit()

    async def update(self, route: RouteUpdateParameters, user_id: int):
        async with self.uow:
            db_route = await self.uow.routes.find_by_main_route_id_private(route.main_route_id)
            db_route = db_route[0]
            if db_route.user_id == user_id:
                if not route.content_blocks:
                    if db_route.content_blocks:
                        content_blocks = [i.model_dump() for i in db_route.content_blocks]
                    else:
                        content_blocks = []
                else:
                    content_blocks = [i.model_dump() for i in route.content_blocks]
                await self.uow.routes.update(title=route.title, description=route.description, photo=route.photo,
                                             main_route_id=route.main_route_id,
                                             content_blocks=content_blocks)
                await self.uow.commit()
            else:
                raise HTTPException(403, "Пользователь не является владельцем маршрута")

    async def get_all_public_routes(self):
        async with self.uow:
            routes = await self.uow.routes.find_all_public_routes()
            return [AllRouteReturn.model_validate(i) for i in routes]
        
    async def get_all_user_routes(self, user_id: int, user: int):
        async with self.uow:
            if user_id != user:
                raise HTTPException(403, "Пользователь не является владельцем маршрутов")
            routes = await self.uow.routes.find_all_user_routes(user_id)
            return [RouteReturnNoContentBlocks.model_validate(i) for i in routes]
