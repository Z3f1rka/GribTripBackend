from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

from app.api.schemas import UserFavoritesGet
from app.api.schemas import UserGetResponse
from app.api.schemas import UserUpdateParameters
from app.utils import create_token
from app.utils import verify_password
from app.utils.unitofwork import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def register(self, username: str, email: str, password: str):
        async with self.uow:
            user_id = await self.uow.users.add_user(username=username, email=email, password=password)
            access_token = create_token("access", user_id, "user")
            refresh_token = create_token("refresh", user_id, "user")
            await self.uow.commit()
            await self.uow.sessions.add_token(user_id=user_id, jwt=refresh_token)
            await self.uow.commit()
            return access_token, refresh_token

    async def login(self, email: str, password: str):
        async with self.uow:
            try:
                user = await self.uow.users.find_one(email=email)
            except NoResultFound:
                raise HTTPException(400, "Пользователя не существует")
            if not verify_password(password, user.hashed_password):
                raise HTTPException(400, "Неправильный пароль")
            access_token = create_token("access", user.id, user.role)
            refresh_token = create_token("refresh", user.id, user.role)
            await self.uow.sessions.add_token(user_id=user.id, jwt=refresh_token)
            await self.uow.commit()
            return access_token, refresh_token

    async def get_me(self, token: str):
        if isinstance(token, dict):
            async with self.uow:
                user = await self.uow.users.find_one(id=int(token["sub"]))
                user = UserGetResponse.model_validate(user)
            return user
        else:
            raise HTTPException(400, "Не валидный токен")

    async def get_user_by(self, **criterion):
        async with self.uow:
            try:
                user = await self.uow.users.find_one(**criterion)
            except NoResultFound:
                raise HTTPException(400, "Такого пользователя не существует")
            return UserGetResponse.model_validate(user)

    async def refresh(self, token: str):
        if isinstance(token, dict):
            async with self.uow:
                user = await self.uow.users.find_one(id=int(token["sub"]))
                access_token = create_token("access", user.id, user.role)
            return access_token
        else:
            raise HTTPException(400, "Не валидный токен")

    async def add_favorites(self, user_id: int, route_id: int):
        async with self.uow:
            try:
                user = await self.uow.users.find_one(id=user_id) # noqa
            except NoResultFound:
                raise HTTPException(400, "Пользователя не существует")
            try:
                favorites = await self.uow.users.get_favorites(user_id)  # noqa
                if favorites:
                    raise HTTPException(400, "Пользователь уже добавил маршрут в избранное")
            except NoResultFound:
                await self.uow.users.add_favorites(user_id, route_id)
                await self.uow.commit()

    async def delete_favorites(self, user_id: int, route_id: int):
        async with self.uow:
            try:
                user = await self.uow.users.find_one(id=user_id) # noqa
            except NoResultFound:
                raise HTTPException(400, "Пользователя не существует")
            favorites = await self.uow.users.get_favorites(user_id)
            if not any((i.user_id == user_id and i.route_id == route_id) for i in favorites):
                raise HTTPException(400, "У пользователя нет такого маршрута в избранных")
            await self.uow.users.delete_favorite(user_id, route_id)
            await self.uow.commit()

    async def get_favotries(self, user_id: int):
        async with self.uow:
            try:
                user = await self.uow.users.find_one(id=user_id) # noqa
            except NoResultFound:
                raise HTTPException(400, "Пользователя не существует")
            routes = await self.uow.users.get_favorites(user_id)
            return [UserFavoritesGet.model_validate(i).model_dump() for i in routes]

    async def update_user(self, user_id: int, user_params: UserUpdateParameters):
        async with self.uow:
            try:
                user = await self.uow.users.find_one(id=user_id) # noqa
            except NoResultFound:
                raise HTTPException(400, "Пользователя не существует")
            await self.uow.users.update_user(user_id, name=user_params.username,
                                             email=user_params.email, avatar=user_params.avatar)
            await self.uow.commit()
