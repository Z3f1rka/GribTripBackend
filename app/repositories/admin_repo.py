# flake8: noqa
from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from app.db.models import Comment
from app.db.models import Route
from app.repositories.basic_repo import Repository


class AdminRepo(Repository):
    model = Route

    async def approve(self, id: int, admin_id: int):
        stmt = select(self.model).where(self.model.main_route_id == id).order_by(self.model.version.desc())
        route = await self.session.execute(stmt)
        route = route.scalars().first()
        if not route:
            raise HTTPException(400, "Такого маршрута не существует")
        if route.status != "check":
            raise HTTPException(400, "Маршрут не находится на проверке")
        route.status = "public"
        route.approved_id = admin_id
        self.session.add(route)

    async def reject(self, user_id: int, text: str, route_id: int):
        stmt = insert(Comment).values(**{"user_id": user_id, "text": text,
                                            "route_id": route_id, "type": "admin"})
        await self.session.execute(stmt)

    async def get_requests(self):
        stmt = select(self.model).where(self.model.status == "check")
        routes = (await self.session.execute(stmt)).scalars().all()
        return routes
    
    async def get_request_by_route_id(self, route_id: int):
        stmt = select(self.model).where(self.model.status == "check", self.model.main_route_id == route_id)
        route = (await self.session.execute(stmt)).scalars().first()
        return route
