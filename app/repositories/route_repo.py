from sqlalchemy import update, insert, select

from app.db.models import Route
from app.repositories.basic_repo import Repository


class RouteRepository(Repository):
    model = Route

    async def add_route(self, user_id: int, title: str):
        stmt = insert(Route).values(**{"user_id": user_id, "title": title}).returning(Route)
        route = await self.session.execute(stmt)
        route_id = route.scalar_one().id
        stmt = update(Route).where(Route.id == route_id).values(main_route_id=route_id)
        await self.session.execute(stmt)
        await self.session.commit()

    # TODO: переписать всю функцию, невозможно добавить еще одну строчку таблицы, т.к. сюда нужно передавать все поля, а это бред
    async def update(self, title: str, description: str, photo: str, main_route_id: int, version: int,
                     content_blocks: dict):
        stmt = select(Route).where(main_route_id=main_route_id).order_by(Route.version.desc())
        route = await self.session.execute(stmt)
        route = route.scalars().first()
        stmt = insert(Route).values(**{"title": title,
                                       "description": description,
                                       "photo": photo})