from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from app.db.models import Favorites
from app.db.models import Route
from app.db.models import User
from app.repositories.basic_repo import Repository
from app.utils import get_password_hash


class UserRepository(Repository):
    model = User

    async def add_user(self, username: str, email: str, password: str):
        try:
            result = await super().add_one(
                {"username": username, "email": email, "hashed_password": get_password_hash(password), "role": "user"},
            )
            return result.id
        except IntegrityError:
            raise HTTPException(400, "Пользователь уже существует")

    async def add_favorites(self, user_id: int, route_id: int):
        stmt = select(Route).where(Route.main_route_id == route_id, Route.status == "public")
        routes = (await self.session.execute(stmt)).scalars().first()
        if not routes:
            raise HTTPException(400, "У маршрута нет опубликованных версий")
        stmt = insert(Favorites).values(user_id=user_id, route_id=route_id)
        await self.session.execute(stmt)

    async def delete_favorite(self, user_id: int, route_id: int):
        stmt = select(Favorites).where(Favorites.user_id == user_id, Favorites.route_id == route_id)
        try:
            user_favorite = (await self.session.execute(stmt)).scalar_one()
        except NoResultFound:
            raise HTTPException(400, "Маршрут не находится в избранном")
        await self.session.delete(user_favorite)

    async def get_favorites(self, user_id: int):
        stmt = select(Favorites).where(Favorites.user_id == user_id)
        user_favorite = (await self.session.execute(stmt)).scalars().all()
        for i in user_favorite:
            stmt = select(Route).where(Route.main_route_id == i.route_id, Route.status == "public").order_by(
                Route.version.desc())
            route = (await self.session.execute(stmt)).scalars().first()
            i.route = route
        return user_favorite
