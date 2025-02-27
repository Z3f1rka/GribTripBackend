from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

from app.api.schemas import AllRouteReturn
from app.api.schemas import CommentCreateParametrs
from app.utils.unitofwork import IUnitOfWork


class AdminService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def approve(self, id: int, user_id: int):
        async with self.uow:
            route = await self.uow.routes.find_by_main_route_id_private(id)
            if not route:
                raise HTTPException(400, "Маршрут не существует")
            route = route[0]
            try:
                user = await self.uow.users.find_one(id=user_id)
            except NoResultFound:
                raise HTTPException(400, "Такого пользователя не существует")

            if user.role != "admin":
                raise HTTPException(403, "У пользователя нет прав администратора")

            if route.status != "check":
                raise HTTPException(400, "Маршрут не находится на рассмотрении у админа")
            await self.uow.admins.approve(id, user_id)
            await self.uow.commit()

    async def reject(self, response: CommentCreateParametrs, user_id: int):
        async with self.uow:
            try:
                user = await self.uow.users.find_one(id=user_id)
            except NoResultFound:
                raise HTTPException(400, "Такого пользователя не существует")

            try:
                route = await self.uow.routes.find_one(main_route_id=response.route_id,
                                                       status="check")
            except NoResultFound:
                raise HTTPException(400, "Такого маршрута не существует")

            if user.role != "admin":
                raise HTTPException(403, "У пользователя нет прав администратора")
            if route.status != "check":
                raise HTTPException(400, "Маршрут не находится на рассмотрении у админа")
            await self.uow.admins.reject(user_id=user_id, text=response.text, route_id=response.route_id)
            await self.uow.routes.change_status(response.route_id, "private")
            await self.uow.commit()

    async def get_publication_requests(self, user_id: int):
        async with self.uow:
            try:
                user = await self.uow.users.find_one(id=user_id)
            except NoResultFound:
                raise HTTPException(400, "Такого пользователя не существует")
            if user.role != "admin":
                raise HTTPException(403, "У пользователя нет прав администратора")

            return [AllRouteReturn.model_validate(i) for i in await self.uow.admins.get_requests()]
