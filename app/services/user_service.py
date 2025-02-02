from fastapi import HTTPException

from app.api.schemas import UserGetMeResponse
from app.utils import create_token
from app.utils import verify_password
from app.utils.unitofwork import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def register(self, username: str, email: str, password: str, role: str):
        async with self.uow:
            user_id = await self.uow.users.add_user(username=username, email=email, password=password, role=role)
            access_token = create_token("access", user_id)
            refresh_token = create_token("refresh", user_id)
            await self.uow.commit()
            await self.uow.sessions.add_token(user_id=user_id, jwt=refresh_token)
            await self.uow.commit()
            return access_token, refresh_token

    async def login(self, email: str, password: str):
        async with self.uow:
            user = await self.uow.users.find_one(email=email)
            if not verify_password(password, user.hashed_password):
                raise HTTPException(400, "Неправильный пароль")
            access_token = create_token("access", user.id)
            refresh_token = create_token("refresh", user.id)
            await self.uow.sessions.add_token(user_id=user.id, jwt=refresh_token)
            await self.uow.commit()
            return access_token, refresh_token

    async def get_me(self, token: str):
        if isinstance(token, dict):
            async with self.uow:
                user = await self.uow.users.find_one(id=int(token["sub"]))
                user = UserGetMeResponse(
                    user_id=user.id,
                    name=user.username,
                    email=user.email,
                    role=user.role,
                    created_at=user.created_at,
                )
            return user
        else:
            raise HTTPException(400, "Не валидный токен")

    async def refresh(self, token: str):
        if isinstance(token, dict):
            access_token = create_token("access", token["sub"])
            return access_token
        else:
            raise HTTPException(400, "Не валидный токен")
